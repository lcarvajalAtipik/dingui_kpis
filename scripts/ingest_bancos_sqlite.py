#!/usr/bin/env python
"""Ingesta de los exports bancarios de data/bancos/inbox/ a la SQLite local.

Mismo flujo que ingest_bancos_to_bq pero contra db/kpis.sqlite:
parse_any → Categorizer → INSERT OR REPLACE (dedupe por raw_tx_id).

Uso: uv run python scripts/ingest_bancos_sqlite.py
"""
from __future__ import annotations

from datetime import datetime

from kpis import config, db
from kpis.categorizer import Categorizer, should_ignore_fx
from kpis.ingest.bancos import parse_any

from apply_bank_overrides import apply_overrides

INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"


def main() -> None:
    cat = Categorizer()
    conn = db.connect()
    total_new = 0
    for path in sorted(INBOX.iterdir()):
        if path.suffix.lower() not in (".csv", ".xls", ".xlsx") or path.name.startswith("."):
            continue
        df, iban, bank = parse_any(path)
        if df is None or not len(df):
            print(f"⚠ {path.name}: sin filas")
            continue
        before = conn.execute("select count(*) from bank_transactions").fetchone()[0]
        for _, row in df.iterrows():
            r = cat.categorize(concept=row["concept"], importe=row["amount_eur"],
                               bank=row["bank"], extra=row.get("extra"))
            source = "manual_csv" if path.suffix.lower() == ".csv" else "manual_xlsx"
            conn.execute(
                """INSERT OR IGNORE INTO bank_transactions
                   (bank, account_iban, booking_date, value_date, amount_eur, currency,
                    concept, extra, counterpart, category, cat_method, cat_confidence,
                    user_override, raw_tx_id, source_file, source, ingested_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (row["bank"], iban or "", str(row["booking_date"]),
                 str(row.get("value_date") or row["booking_date"]), float(row["amount_eur"]),
                 "EUR", row["concept"], row.get("extra") or "", None,
                 r.category, r.method, float(r.confidence), 0,
                 row["raw_tx_id"], path.name, source, datetime.now().isoformat(timespec="seconds")),
            )
        conn.commit()
        after = conn.execute("select count(*) from bank_transactions").fetchone()[0]
        print(f"✓ {path.name} ({bank}): {len(df)} filas → +{after - before} nuevas en DB")
        total_new += after - before
    # Reaplica las categorizaciones manuales (data/bank_overrides.csv, trackeado en git)
    # para que no se pierdan al reconstruir la DB en otra máquina.
    applied, missing = apply_overrides(conn)
    conn.commit()
    print(f"Overrides manuales reaplicados: {applied}" + (f" | sin match: {missing}" if missing else ""))

    n, dmin, dmax = conn.execute(
        "select count(*), min(booking_date), max(booking_date) from bank_transactions").fetchone()
    print(f"\nDB: {n} movimientos, {dmin} → {dmax} (+{total_new} nuevos)")


if __name__ == "__main__":
    main()
