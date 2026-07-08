"""Descubrimiento del contrato de la API interna de Tipsi Pro (herramienta AUXILIAR).

NOTA: `tipsi_extract.py` ya funciona por sí solo (se autoautentica por Basic + cookie y
autodetecta brandId/localId), así que NO necesitas este script para la extracción normal.
Sirve solo para capturar el contrato de endpoints cuyos parámetros aún no conocemos
(p.ej. los POST `SalesStatistics/GetLocalSalesPer{Article,Family}Async`): abre el back
office real, navegas al informe en cuestión con datos, y aquí queda registrada su petición
exacta (método, URL, query params y/o body) para poder replicarla.

Captura TODO el XHR/fetch contra `backend-green.tipsipro.com` y guarda:
  - api_calls.jsonl   → una línea por llamada (método, URL, params, body, respuesta).
  - responses/        → respuesta JSON íntegra de cada llamada.
  - endpoints_seen.json → catálogo real de endpoints observados.
  - credentials.json  → brandId, localId (GUIDs) + base_url.
  - storage_state.json / session.har / debug/ → sesión, traza y diagnóstico.

Uso:
    uv run playwright install chromium   # si no está
    uv run python scripts/tipsi_discover.py             # headed; navega a mano y pulsa Enter
    uv run python scripts/tipsi_discover.py --auto-only # solo rutas conocidas, sin esperar

Recomendado (interactivo, por defecto): cuando el navegador esté logueado, entra a mano en
el informe que quieras cartografiar, pon un rango de fechas CON DATOS y pulsa "buscar";
así se captura su petición exacta. Al terminar, vuelve a la terminal y pulsa Enter.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from typing import Any

from kpis import config
from kpis.ingest import tipsi

OUT = tipsi.DISCOVERY_DIR
RESP_DIR = OUT / "responses"
DEBUG_DIR = OUT / "debug"

# Rutas hash del back office cuyo XHR queremos provocar para capturar su contrato.
# (No dependemos de que carguen datos: basta con que disparen su petición.)
KNOWN_ROUTES = [
    "listTickets",
    "listVentas",
    "salesPerArticle",
    "salesPerFamily",
    "salesByHour",
    "salesByTimeSlot",
    "listDiscounts",
    "listDevolutions",
    "listInvitations",
    "staffSales",
    "dailyReport",
    "hourReport",
    "listClosingCash",
    "invoicesList",
]


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def _short_name(url: str, idx: int) -> str:
    action = tipsi.action_name(url) or "unknown"
    return f"{idx:04d}_{action.replace('/', '.')}.json"


async def _capture_response(response: Any, state: dict[str, Any]) -> None:
    """Handler de respuestas: registra las llamadas al backend de Tipsi."""
    req = response.request
    url = response.url
    if req.resource_type not in ("xhr", "fetch"):
        return
    if "tipsipro.com" not in url:
        return
    action = tipsi.action_name(url)

    # Cuerpo de la petición como JSON si se puede.
    request_body: Any = None
    raw_post = req.post_data
    if raw_post:
        try:
            request_body = json.loads(raw_post)
        except (json.JSONDecodeError, TypeError):
            request_body = raw_post

    # Respuesta íntegra (JSON si aplica).
    resp_json: Any = None
    resp_text: str | None = None
    try:
        body_bytes = await response.body()
        try:
            resp_json = json.loads(body_bytes)
        except (json.JSONDecodeError, UnicodeDecodeError):
            resp_text = f"<{len(body_bytes)} bytes no-JSON>"
    except Exception as exc:  # noqa: BLE001 — la respuesta pudo no estar disponible
        resp_text = f"<sin cuerpo: {exc}>"

    idx = state["counter"]
    state["counter"] += 1

    call_record = {
        "idx": idx,
        "timestamp": datetime.now().isoformat(),
        "method": req.method,
        "url": url,
        "action": action,
        "status": response.status,
        "request_headers": dict(req.headers),
        "request_body": request_body,
        "response_file": None,
    }

    if resp_json is not None:
        fname = _short_name(url, idx)
        (RESP_DIR / fname).write_text(
            json.dumps(resp_json, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        call_record["response_file"] = f"responses/{fname}"
    elif resp_text is not None:
        call_record["response_note"] = resp_text

    # api_calls.jsonl incremental (flush por llamada: si algo peta, no perdemos nada).
    with (OUT / "api_calls.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(call_record, ensure_ascii=False) + "\n")

    if action:
        state["endpoints"][action] = state["endpoints"].get(action, 0) + 1
        log(f"  ← {req.method} {action}  [{response.status}]  (filas: {len(tipsi.extract_rows(resp_json))})")


async def _read_local_storage(page: Any) -> dict[str, str]:
    return await page.evaluate(
        "() => { const o = {}; for (let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k);} return o; }"
    )


# Tras el login, el back office guarda en localStorage (la sesión de datos va por cookie,
# no hay cabecera Basic almacenada): `brandId` = "<guid>", `localSelected` = {"Id":..},
# `user` = {"Id":..}. Usamos esas claves como señal de autenticación y para los GUIDs.
def _maybe_id(raw: str | None) -> Any:
    if not raw:
        return None
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    if isinstance(obj, dict):
        for k in ("Id", "id", "ID", "brandId", "localId"):
            if k in obj:
                return obj[k]
    return obj


def _is_authenticated(local_storage: dict[str, str]) -> bool:
    return bool(local_storage.get("brandId") or local_storage.get("user")
                or local_storage.get("localSelected"))


def _extract_credentials(local_storage: dict[str, str]) -> dict[str, Any]:
    """De localStorage saca brandId y localId (GUIDs). La auth de la extracción no
    necesita cabecera: tipsi_extract.py reautentica por Basic + cookie."""
    return {
        "base_url": tipsi.DEFAULT_BACKEND,
        "brand_id": _maybe_id(local_storage.get("brandId")),
        "local_id": _maybe_id(local_storage.get("localSelected")),
        "note": "La sesión de datos va por cookie (GET LoginWeb con Basic la fija). "
                "El extractor se autoautentica; aquí solo interesan brand_id/local_id.",
    }


async def _dismiss_overlays(page: Any) -> None:
    """Cierra banners de cookies/consentimiento que puedan interceptar los clicks."""
    labels = ["Aceptar", "Aceptar todo", "Aceptar todas", "De acuerdo", "Entendido",
              "Accept", "Accept all", "Got it", "OK"]
    for label in labels:
        try:
            btn = page.get_by_role("button", name=label, exact=False).first
            if await btn.is_visible(timeout=500):
                await btn.click(timeout=1500)
                log(f"  (cerrado overlay: '{label}')")
                await page.wait_for_timeout(300)
                return
        except Exception:  # noqa: BLE001 — si no hay banner, seguimos
            continue


async def _do_login(page: Any) -> None:
    """Login por formulario si hace falta. Señal positiva: aparece `brandId`/`user` en localStorage."""
    log("Abriendo back office…")
    await page.goto(tipsi.APP_URL, wait_until="domcontentloaded")
    await page.wait_for_timeout(3000)
    await _dismiss_overlays(page)

    ls = await _read_local_storage(page)
    if _is_authenticated(ls):
        log("  Ya hay sesión activa (storage_state). No relogueo.")
        return

    email = config.TIPSI_EMAIL
    password = config.TIPSI_PASSWORD
    if not email or not password:
        raise SystemExit(
            "Faltan TIPSI_EMAIL / TIPSI_PASSWORD en .env para el login inicial."
        )

    log("  Rellenando formulario de login…")
    try:
        email_field = page.locator("input[type='email'], input[type='text'], input[name='email']").first
        await email_field.wait_for(timeout=15000)
        await email_field.fill(email)
        await page.locator("input[type='password']").first.fill(password)
        btn = page.locator(
            "button[type='submit'], input[type='submit'], "
            "button:has-text('Entrar'), button:has-text('Iniciar'), button:has-text('Acceder')"
        ).first
        try:
            await btn.click(timeout=5000)
        except Exception:  # noqa: BLE001 — overlay que intercepta: reintenta forzando
            await _dismiss_overlays(page)
            await btn.click(force=True, timeout=5000)
    except Exception as exc:  # noqa: BLE001
        log(f"  ⚠ No pude autocompletar el login ({exc}). Hazlo a mano en la ventana.")

    # Espera activa hasta que aparezca brandId/user en localStorage (señal positiva de auth).
    log("  Esperando autenticación (hasta 120 s; resuelve captcha/2FA en la ventana si aparece)…")
    for _ in range(120):
        await page.wait_for_timeout(1000)
        ls = await _read_local_storage(page)
        if _is_authenticated(ls):
            log("  ✓ Autenticado.")
            return

    # Diagnóstico antes de rendirse: volcamos localStorage y una captura.
    try:
        ls = await _read_local_storage(page)
        (OUT / "localstorage.json").write_text(
            json.dumps(ls, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        await _dump_debug(page, "login_failed")
    except Exception:  # noqa: BLE001
        pass
    raise SystemExit(
        "No se detectó autenticación (no apareció brandId/user en localStorage). "
        f"Revisa {OUT/'localstorage.json'} y {DEBUG_DIR} para ver qué guardó la app."
    )


async def _visit_routes(page: Any, routes: list[str]) -> None:
    for route in routes:
        url = f"{tipsi.APP_URL}#!/index/{route}"
        try:
            log(f"  → visitando #!/index/{route}")
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(4000)  # deja que dispare sus XHR
        except Exception as exc:  # noqa: BLE001
            log(f"    ⚠ {route}: {exc}")


async def _dump_debug(page: Any, tag: str) -> None:
    ts = datetime.now().strftime("%H%M%S")
    try:
        await page.screenshot(path=str(DEBUG_DIR / f"{tag}_{ts}.png"), full_page=True)
        (DEBUG_DIR / f"{tag}_{ts}.html").write_text(await page.content(), encoding="utf-8")
        (DEBUG_DIR / f"{tag}_{ts}.url.txt").write_text(page.url, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        log(f"  ⚠ No pude volcar debug: {exc}")


async def run(args: argparse.Namespace) -> None:
    from playwright.async_api import async_playwright

    for d in (OUT, RESP_DIR, DEBUG_DIR):
        d.mkdir(parents=True, exist_ok=True)
    # Empezamos api_calls.jsonl limpio en cada corrida de discovery.
    (OUT / "api_calls.jsonl").write_text("", encoding="utf-8")

    state: dict[str, Any] = {"counter": 0, "endpoints": {}}
    pending_tasks: set[Any] = set()   # referencia fuerte a las tareas del handler (evita GC)
    storage_state_path = OUT / "storage_state.json"
    har_path = OUT / "session.har"
    routes = KNOWN_ROUTES + [r for r in (args.routes or "").split(",") if r.strip()]

    def _on_response(r: Any) -> None:
        task = asyncio.create_task(_capture_response(r, state))
        pending_tasks.add(task)
        task.add_done_callback(pending_tasks.discard)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=args.headless)
        context = await browser.new_context(
            accept_downloads=True,
            locale="es-ES",
            storage_state=str(storage_state_path) if storage_state_path.exists() else None,
            record_har_path=str(har_path),
            record_har_content="embed",
        )
        page = await context.new_page()
        page.on("response", _on_response)

        try:
            await _do_login(page)

            # Persistir credenciales y sesión cuanto antes.
            ls = await _read_local_storage(page)
            (OUT / "localstorage.json").write_text(
                json.dumps(ls, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            creds = _extract_credentials(ls)
            (OUT / "credentials.json").write_text(
                json.dumps(creds, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            await context.storage_state(path=str(storage_state_path))
            log(f"  brandId={creds.get('brand_id')}  localId={creds.get('local_id')}")

            log("Navegando rutas conocidas para capturar contratos…")
            await _visit_routes(page, routes)

            if not args.auto_only:
                print("\n" + "=" * 70)
                print("  Navega A MANO por los informes que te interesen en la ventana.")
                print("  Pon un rango de fechas CON DATOS y pulsa 'buscar' en cada uno")
                print("  (así capturo el cuerpo de petición exacto de cada informe).")
                print("  Cuando termines, vuelve aquí y pulsa ENTER para cerrar.")
                print("=" * 70 + "\n")
                await asyncio.get_event_loop().run_in_executor(None, input)

            await _dump_debug(page, "final")
        except Exception as exc:  # noqa: BLE001
            log(f"⚠ Error: {exc}")
            await _dump_debug(page, "error")
            raise
        finally:
            # Deja terminar las capturas en vuelo antes de cerrar (si no, se pierden).
            if pending_tasks:
                await asyncio.gather(*list(pending_tasks), return_exceptions=True)
            # Resumen de endpoints observados.
            (OUT / "endpoints_seen.json").write_text(
                json.dumps(
                    dict(sorted(state["endpoints"].items(), key=lambda kv: -kv[1])),
                    ensure_ascii=False, indent=2,
                ),
                encoding="utf-8",
            )
            await context.close()  # cierra y escribe el HAR
            await browser.close()

    log(f"\n✓ Discovery terminado. {state['counter']} llamadas capturadas, "
        f"{len(state['endpoints'])} endpoints distintos.")
    log(f"  Revisa: {OUT}")
    log("  Siguiente paso: uv run python scripts/tipsi_extract.py")


def main() -> None:
    parser = argparse.ArgumentParser(description="Descubre el contrato de la API de Tipsi (Playwright).")
    parser.add_argument("--headless", action="store_true", help="No abrir ventana (sin captcha/2FA).")
    parser.add_argument("--auto-only", action="store_true", help="Solo rutas conocidas; no esperar interacción.")
    parser.add_argument("--routes", default="", help="Rutas hash extra separadas por comas.")
    args = parser.parse_args()
    try:
        asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\nInterrumpido.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
