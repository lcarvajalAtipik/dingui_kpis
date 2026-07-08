"""Extracción granular de datos de Tipsi Pro por su API interna.

Autoservicio (no necesita nada previo salvo TIPSI_EMAIL/TIPSI_PASSWORD en .env):
  1. login()          → cookie de sesión.
  2. resolve_context()→ autodetecta brandId/localId (o usa --brand/--local / .env).
  3. Por cada informe del catálogo (src/kpis/ingest/tipsi.py: REPORTS) trocea por meses,
     pagina por TotalItems y guarda el JSON crudo en data/tipsi/raw/<informe>/.
  4. Para tickets, baja además el DETALLE línea a línea de cada uno (pagos, descuentos,
     IVA por tipo, camarero, mesa, comensales) → data/tipsi/raw/detalle_tickets/.

Uso:
    uv run python scripts/tipsi_extract.py
    uv run python scripts/tipsi_extract.py --desde 2026-06-01 --hasta 2026-07-07
    uv run python scripts/tipsi_extract.py --solo tickets,arqueos,devoluciones
    uv run python scripts/tipsi_extract.py --sin-detalle-tickets
    uv run python scripts/tipsi_extract.py --limite-detalle 200     # prueba rápida

Idempotente (salta lo ya bajado; --forzar rehace). Distingue "sin datos" (OK) de "error".
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from kpis import config
from kpis.ingest import tipsi
from kpis.ingest.tipsi import Report, TipsiClient

RAW = tipsi.RAW_DIR
DEFAULT_DESDE = "2026-01-01"


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def _save(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _win_tag(frm: date, to: date) -> str:
    return f"{frm:%Y-%m-%d}_{to:%Y-%m-%d}"


_TICKET_ID_KEYS = ("id", "ticketid", "idticket", "ticketguid", "guid")


def _ticket_id(row: Any) -> str | None:
    if not isinstance(row, dict):
        return None
    for want in _TICKET_ID_KEYS:
        for k, v in row.items():
            if k.lower() == want and v not in (None, ""):
                return str(v)
    return None


# ─────────────────────────────────────────────────────────────────────────────
def extract_report(client: TipsiClient, report: Report, windows: list[tuple[date, date]],
                   manifest: dict[str, Any], *, force: bool) -> list[str]:
    """Descarga un informe (todas sus ventanas). Devuelve los ids de ticket vistos
    (solo relevante para el informe de tickets, para bajar su detalle después)."""
    out_dir = RAW / report.key
    flag = " [experimental]" if report.experimental else ""
    log(f"\n=== {report.key}  ({report.action}){flag} ===")
    total_rows = 0
    errors: list[str] = []
    ticket_ids: list[str] = []

    if report.kind == "byday":
        iter_units = [(d, d) for w in windows for d in tipsi.day_range(*w)]
    else:
        iter_units = windows

    for frm, to in iter_units:
        tag = f"{frm:%Y-%m-%d}" if report.kind == "byday" else _win_tag(frm, to)
        try:
            if report.kind == "byday":
                out = out_dir / f"{tag}.json"
                if out.exists() and not force:
                    continue
                payload = client.get(report.action, client.byday_params(frm))
                _save(out, payload)
                total_rows += len(tipsi.extract_rows(payload))
            else:
                params = client.paged_params(frm, to, report.extra)
                page_count = 0
                for page, payload, rows, total in client.paged(
                    report.action, params, method=report.method,
                ):
                    total_rows += len(rows)
                    page_count += 1
                    if report.detail:
                        ticket_ids.extend(filter(None, (_ticket_id(r) for r in rows)))
                    out = out_dir / f"{tag}_p{page:03d}.json"
                    if out.exists() and not force:
                        continue
                    _save(out, payload)
                    err = tipsi.response_error(payload)
                    if err:
                        errors.append(f"{tag} p{page}: {err}")
                        break
                log(f"  {tag}: {page_count} pág.")
        except Exception as exc:  # noqa: BLE001 — un informe/ventana no debe tumbar el resto
            errors.append(f"{tag}: {exc}")
            log(f"  ⚠ {tag}: {exc}")

    manifest["reports"][report.key] = {
        "action": report.action, "rows": total_rows,
        "experimental": report.experimental, "errors": errors,
    }
    log(f"  → {total_rows} filas" + (f"  ⚠ {len(errors)} errores" if errors else ""))
    return ticket_ids


def extract_ticket_details(client: TipsiClient, ticket_ids: list[str], manifest: dict[str, Any],
                           *, force: bool, limit: int | None) -> None:
    """Detalle línea a línea de cada ticket (la fuente MÁS granular)."""
    out_dir = RAW / "detalle_tickets"
    ids = list(dict.fromkeys(ticket_ids))   # únicos, preservando orden
    log(f"\n=== detalle_tickets  ({tipsi.TICKET_DETAIL_ACTION}) — {len(ids)} tickets ===")
    fetched = 0
    errors: list[str] = []
    for tid in ids:
        out = out_dir / f"{tid}.json"
        if out.exists() and not force:
            fetched += 1
            continue
        try:
            _save(out, client.ticket_detail(tid))
            fetched += 1
            if fetched % 100 == 0:
                log(f"  … {fetched}/{len(ids)}")
            if limit is not None and fetched >= limit:
                log(f"  Alcanzado --limite-detalle={limit}, paro.")
                break
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{tid}: {exc}")
    log(f"  → {fetched} detalles guardados" + (f"  ⚠ {len(errors)} errores" if errors else ""))
    manifest["reports"]["detalle_tickets"] = {
        "action": tipsi.TICKET_DETAIL_ACTION, "tickets": fetched, "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Descarga granular de Tipsi por API.")
    parser.add_argument("--desde", default=DEFAULT_DESDE, help="Fecha inicio AAAA-MM-DD.")
    parser.add_argument("--hasta", default=date.today().isoformat(), help="Fecha fin AAAA-MM-DD.")
    parser.add_argument("--solo", default="", help="Solo estos informes (claves separadas por comas).")
    parser.add_argument("--sin-experimentales", action="store_true",
                        help="Salta informes con contrato no confirmado.")
    parser.add_argument("--sin-detalle-tickets", action="store_true", help="No bajar el detalle línea a línea.")
    parser.add_argument("--limite-detalle", type=int, default=None, help="Máx. tickets a detallar (prueba).")
    parser.add_argument("--brand", default=None, help="brandId (si no, se autodetecta).")
    parser.add_argument("--local", default=None, help="localId (si no, se autodetecta).")
    parser.add_argument("--pausa", type=float, default=0.1, help="Pausa mínima entre peticiones (s).")
    parser.add_argument("--forzar", action="store_true", help="Reprocesa aunque exista el fichero.")
    args = parser.parse_args()

    windows = tipsi.month_windows(args.desde, args.hasta)
    if not windows:
        sys.exit(f"Rango de fechas vacío o invertido: {args.desde} → {args.hasta}")

    try:
        client = TipsiClient(min_interval=args.pausa)
    except RuntimeError as exc:
        sys.exit(str(exc))

    with client:
        log("Login…")
        user = client.login()
        log(f"  ✓ {user.get('Name','?')} <{user.get('Email','?')}>")
        client.resolve_context(brand_id=args.brand or config.TIPSI_BRAND_ID,
                               local_id=args.local or config.TIPSI_LOCAL_ID)
        if not client.local_id:
            sys.exit("No pude resolver localId. Pásalo con --local o TIPSI_LOCAL_ID en .env.")
        log(f"  brandId={client.brand_id}  localId={client.local_id}  local={client.local_name}")
        log(f"Rango: {args.desde} → {args.hasta}  ({len(windows)} meses)")

        only = {s.strip() for s in args.solo.split(",") if s.strip()}
        reports = [r for r in tipsi.REPORTS
                   if (not only or r.key in only)
                   and (not args.sin_experimentales or not r.experimental)]

        manifest: dict[str, Any] = {
            "started_at": datetime.now().isoformat(), "desde": args.desde, "hasta": args.hasta,
            "brand_id": client.brand_id, "local_id": client.local_id,
            "local_name": client.local_name, "reports": {},
        }

        ticket_ids: list[str] = []
        for report in reports:
            ids = extract_report(client, report, windows, manifest, force=args.forzar)
            if report.detail:
                ticket_ids.extend(ids)

        want_detail = (not args.sin_detalle_tickets
                       and (not only or "detalle_tickets" in only or "tickets" in only))
        if want_detail and ticket_ids:
            extract_ticket_details(client, ticket_ids, manifest,
                                   force=args.forzar, limit=args.limite_detalle)

    manifest["finished_at"] = datetime.now().isoformat()
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                       encoding="utf-8")

    log("\n" + "=" * 60)
    for key, info in manifest["reports"].items():
        n = info.get("rows", info.get("tickets", 0))
        err = len(info.get("errors", []))
        log(f"  {key:24s} {n:>8}" + (f"  ⚠ {err}" if err else ""))
    log("=" * 60)
    log(f"Datos crudos en: {RAW}")


if __name__ == "__main__":
    main()
