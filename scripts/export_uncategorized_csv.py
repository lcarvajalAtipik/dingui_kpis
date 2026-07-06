"""Exporta los movimientos sin categorizar a un CSV editable.

CSV con una fila por movimiento (no agrupado, para que el usuario pueda matizar caso por caso).
Columnas:
  - bank, booking_date, amount_eur, concept, extra
  - mi_sugerencia (read-only, lo que Claude propone)
  - p_l            (editable — el usuario sobreescribe esta celda si quiere cambiar mi sugerencia;
                    si la deja igual o vacía, asumimos mi_sugerencia)
  - ignorar_fx     (TRUE/FALSE — por defecto FALSE; el usuario lo cambia si aplica)
  - notas          (libre)

Tras la revisión del usuario: `uv run python scripts/process_user_review.py <xlsx>`,
y las decisiones se consolidan como reglas en src/kpis/categorizer.py.

Uso: `uv run python scripts/export_uncategorized_csv.py`
"""
from __future__ import annotations

import csv

import pandas as pd

from kpis import config
from kpis.categorizer import Categorizer
from kpis.ingest.bancos import parse_any


INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"
OUT = config.REPO_ROOT / "outputs" / "uncategorized_for_review.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

BANK_LABELS = {"caixa": "CaixaBank"}

# Sugerencias ad-hoc para los movimientos sin matchear, en base a mi análisis.
# Cada regla es (substring case-insensitive en concepto+extra, categoría sugerida).
# VACÍO al arrancar Dingui — se rellena al analizar el primer extracto, antes de
# pasar el CSV al usuario.
SUGGESTION_PATTERNS: list[tuple[str, str]] = []


def best_suggestion(concept: str, extra: str | None) -> str:
    """Devuelve la mejor categoría sugerida para un movimiento."""
    text = f"{concept or ''} {extra or ''}".lower()
    for pattern, category in SUGGESTION_PATTERNS:
        if pattern in text:
            return category
    return ""  # sin sugerencia


def collect_uncategorized() -> pd.DataFrame:
    cat = Categorizer()
    frames = []
    for path in sorted(p for p in INBOX.glob("*") if p.suffix.lower() in (".xls", ".xlsx")):
        try:
            df, _iban, bank_label = parse_any(path)
        except ValueError as e:
            print(f"⚠ SKIP {path.name}: {e}")
            continue
        df["bank_label"] = BANK_LABELS.get(bank_label, bank_label)
        cats = []
        for _, row in df.iterrows():
            r = cat.categorize(row["concept"], importe=row["amount_eur"], bank=row["bank"],
                               extra=row.get("extra"))
            cats.append(r.category)
        df["category"] = cats
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    all_df = pd.concat(frames, ignore_index=True)
    return all_df[all_df["category"].isna()].copy()


def main() -> None:
    df = collect_uncategorized()
    if len(df) == 0:
        print("No hay movimientos sin categorizar (o no hay archivos en el inbox).")
        return
    df = df.sort_values(["bank_label", "booking_date", "amount_eur"],
                        ascending=[True, True, True])

    rows = []
    for _, r in df.iterrows():
        sugg = best_suggestion(r["concept"], r.get("extra"))
        rows.append({
            "bank": r["bank_label"],
            "booking_date": r["booking_date"].strftime("%Y-%m-%d") if pd.notna(r["booking_date"]) else "",
            "amount_eur": f"{r['amount_eur']:.2f}" if pd.notna(r["amount_eur"]) else "",
            "concept": r["concept"],
            "extra": (r.get("extra") or "") if str(r.get("extra")) != "nan" else "",
            "mi_sugerencia": sugg,
            "p_l": sugg,  # pre-rellenado con mi sugerencia, el usuario edita
            "ignorar_fx": "FALSE",
            "notas": "",
        })

    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["bank", "booking_date", "amount_eur", "concept", "extra",
                        "mi_sugerencia", "p_l", "ignorar_fx", "notas"],
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nCSV escrito en: {OUT}")
    print(f"Total filas: {len(rows)}")
    print("\nDistribución de sugerencias:")
    sugg_counts = pd.Series([row["mi_sugerencia"] or "(sin sugerencia)" for row in rows]).value_counts()
    print(sugg_counts.to_string())

    print("\n--- Preview primeras 5 filas ---")
    for row in rows[:5]:
        print(f"  [{row['bank']:9s}] {row['booking_date']}  {row['amount_eur']:>10s}€  "
              f"{(row['concept'] or '')[:50]:50s}  → {row['mi_sugerencia']}")


if __name__ == "__main__":
    main()
