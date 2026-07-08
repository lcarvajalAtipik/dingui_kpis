"""Smoke test del parser bancario + categorización en pipe.

Recorre todos los archivos de data/bancos/inbox/, los parsea con parse_any,
aplica el categorizador y muestra resumen por archivo.

Uso: `uv run python scripts/test_parsers.py`
"""
from __future__ import annotations

import pandas as pd

from kpis import config
from kpis.categorizer import Categorizer, should_ignore_fx
from kpis.ingest.bancos import parse_any


INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"


def apply_categorization(df: pd.DataFrame, cat: Categorizer) -> pd.DataFrame:
    """Añade columnas `category`, `cat_method`, `cat_confidence`, `ignorar_fx`."""
    cats, methods, confs = [], [], []
    for _, row in df.iterrows():
        r = cat.categorize(row["concept"], importe=row["amount_eur"], bank=row["bank"],
                           extra=row.get("extra"))
        cats.append(r.category)
        methods.append(r.method)
        confs.append(round(r.confidence, 2))
    df["category"] = cats
    df["cat_method"] = methods
    df["cat_confidence"] = confs
    df["ignorar_fx"] = df["concept"].apply(should_ignore_fx)
    return df


def report(name: str, df: pd.DataFrame, iban: str | None) -> None:
    print(f"\n{'=' * 90}")
    print(f"  {name}  |  IBAN: {iban}  |  filas: {len(df)}")
    if len(df) > 0:
        print(f"  Rango: {df['booking_date'].min().date()} → {df['booking_date'].max().date()}")
        print(f"  Total importe: {df['amount_eur'].sum():,.2f} €")
    print("=" * 90)
    print("\nDistribución por categoría:")
    cat_summary = df.groupby("category", dropna=False).agg(
        n=("amount_eur", "count"),
        total=("amount_eur", "sum"),
    ).sort_values("n", ascending=False)
    print(cat_summary.to_string(float_format=lambda v: f"{v:,.2f}"))

    print(f"\nignorar_fx: TRUE={df['ignorar_fx'].sum()}  FALSE={(~df['ignorar_fx']).sum()}")

    unmatched = df[df["category"].isna()]
    print(f"\nSin categorizar: {len(unmatched)}")
    if len(unmatched) > 0:
        print("Top 10 conceptos sin categorizar (por frecuencia):")
        print(unmatched["concept"].value_counts().head(10).to_string())


def main() -> None:
    files = sorted(p for p in INBOX.glob("*") if p.suffix.lower() in (".xls", ".xlsx", ".csv"))
    if not files:
        print(f"No hay archivos en {INBOX} — descarga los exports (CaixaBank/Santander) y déjalos ahí.")
        return
    cat = Categorizer()
    for path in files:
        try:
            df, iban, bank_label = parse_any(path)
            df = apply_categorization(df, cat)
            report(f"{bank_label.upper()} — {path.name}", df, iban)
        except Exception as e:
            print(f"\n❌ ERROR en {path.name}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
