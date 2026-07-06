"""Crea las tablas BQ ejecutando los DDLs de schemas/bq/*.sql.

Idempotente: usa CREATE TABLE IF NOT EXISTS. Se puede ejecutar varias veces sin daño.

Uso: `uv run python scripts/setup_bq.py`
"""
from __future__ import annotations

import sys

from kpis import bq, config


def main() -> None:
    if not config.BQ_PROJECT:
        print("ERROR: BQ_PROJECT no está en .env", file=sys.stderr)
        sys.exit(1)

    print(f"Proyecto: {config.BQ_PROJECT}")
    print(f"Dataset:  {config.BQ_DATASET}")
    print(f"Region:   {config.BQ_LOCATION}")
    auth = (
        config.GOOGLE_APPLICATION_CREDENTIALS
        if config.GOOGLE_APPLICATION_CREDENTIALS
        else "ADC (gcloud auth application-default login)"
    )
    print(f"Auth:     {auth}")
    print()

    applied = bq.setup_tables()
    print(f"DDLs aplicados ({len(applied)}):")
    for name in applied:
        print(f"  ✓ {name}")

    # Mostrar tablas existentes para confirmar
    df = bq.query(f"""
        SELECT table_name, table_type, creation_time
        FROM `{config.BQ_PROJECT}.{config.BQ_DATASET}.INFORMATION_SCHEMA.TABLES`
        ORDER BY table_name
    """)
    print(f"\nTablas en {config.BQ_DATASET}:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
