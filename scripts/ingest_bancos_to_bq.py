"""Ingesta de los XLS bancarios de data/bancos/inbox/ a BigQuery.

Flujo por archivo:
  1. Detecta banco por filename (parse_any).
  2. Parser → DataFrame normalizado.
  3. Aplica Categorizer (category, cat_method, cat_confidence, ignorar_fx).
  4. Carga a `bank_transactions` (dedupe por raw_tx_id con MERGE cuando billing lo permita).
  5. Resumen final desde BQ.

Uso: `uv run python scripts/ingest_bancos_to_bq.py`
"""
from __future__ import annotations

import sys

import pandas as pd

from kpis import bq, config
from kpis.categorizer import Categorizer, should_ignore_fx
from kpis.ingest.bancos import parse_any


INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"


def prepare_df(df: pd.DataFrame, cat: Categorizer) -> pd.DataFrame:
    """Añade columnas de categorización y normaliza tipos para BQ."""
    cats, methods, confs = [], [], []
    for _, row in df.iterrows():
        r = cat.categorize(
            concept=row["concept"],
            importe=row["amount_eur"],
            bank=row["bank"],
            extra=row.get("extra"),
        )
        cats.append(r.category)
        methods.append(r.method)
        confs.append(float(r.confidence))
    df = df.copy()
    df["category"] = cats
    df["cat_method"] = methods
    df["cat_confidence"] = confs
    df["ignorar_fx"] = df["concept"].apply(should_ignore_fx)
    df["user_override"] = False
    # Limpieza tipos
    df["booking_date"] = pd.to_datetime(df["booking_date"]).dt.date
    df["value_date"] = pd.to_datetime(df["value_date"], errors="coerce").dt.date
    df["amount_eur"] = df["amount_eur"].astype(float)
    df["concept"] = df["concept"].astype(str)
    df["extra"] = df["extra"].astype(str).replace("nan", None).replace("None", None)
    df["account_iban"] = df["account_iban"].astype(str).replace("nan", None).replace("None", None)
    return df


def main() -> None:
    if not config.BQ_PROJECT:
        print("ERROR: BQ_PROJECT no está en .env", file=sys.stderr)
        sys.exit(1)

    files = sorted(p for p in INBOX.glob("*") if p.suffix.lower() in (".xls", ".xlsx"))
    if not files:
        print(f"No hay archivos en {INBOX} — nada que ingestar.")
        return

    cat = Categorizer()
    grand_total = 0
    for path in files:
        print(f"\n=== {path.name} ===")
        try:
            df, iban, bank_label = parse_any(path)
        except ValueError as e:
            print(f"  ⚠ SKIP: {e}")
            continue
        print(f"  Parseado ({bank_label}): {len(df)} filas, IBAN={iban}")
        df = prepare_df(df, cat)
        # Con dedupe (MERGE) — idempotente ante exports solapados. Si billing de BQ
        # aún no permite DML, cambiar a bq.append_bank_transactions (solo primera carga).
        stats = bq.merge_bank_transactions(df, source_file=path.name)
        print(f"  Cargado: {stats}")
        grand_total += stats["rows_in"]

    print(f"\nTotal filas procesadas: {grand_total}")
    print("\nResumen de tablas BQ:")
    summary = bq.query(f"""
        SELECT
          bank,
          COUNT(*) AS n_movs,
          MIN(booking_date) AS first_date,
          MAX(booking_date) AS last_date,
          ROUND(SUM(amount_eur), 2) AS net_eur,
          COUNTIF(ignorar_fx) AS ignorar_fx_true
        FROM `{config.BQ_PROJECT}.{config.BQ_DATASET}.bank_transactions`
        GROUP BY bank
        ORDER BY bank
    """)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
