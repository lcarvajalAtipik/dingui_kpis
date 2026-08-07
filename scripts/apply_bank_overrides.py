#!/usr/bin/env python
"""Reaplica las categorizaciones MANUALES del banco tras cada ingesta.

Problema que resuelve: db/kpis.sqlite está en .gitignore y se reconstruye desde
los exports en cada máquina, así que las categorías que asigna una persona a mano
(las que el categorizador automático no acierta) se perderían al re-ingestar o al
abrir el proyecto en otro ordenador.

Solución: esas decisiones viven en data/bank_overrides.csv (SÍ trackeado en git).
Este script las vuelve a aplicar sobre la DB. Se llama automáticamente al final de
ingest_bancos_sqlite.py, y también puede ejecutarse suelto:

    uv run python scripts/apply_bank_overrides.py

Clave de emparejamiento: raw_tx_id (hash determinista de banco+fecha+importe+
concepto+saldo → estable entre exports). Fallback: (bank, fecha, importe, concepto)
por si el saldo cambió entre exports solapados.
"""
from __future__ import annotations

import csv

from kpis import config, db

OVERRIDES = config.REPO_ROOT / "data" / "bank_overrides.csv"


def apply_overrides(conn=None) -> tuple[int, int]:
    """Aplica data/bank_overrides.csv sobre bank_transactions.

    Devuelve (aplicados, no_encontrados).
    """
    if not OVERRIDES.exists():
        return 0, 0
    own = conn is None
    if own:
        conn = db.connect()
    applied = missing = 0
    with OVERRIDES.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cat = (row.get("category") or "").strip()
            if not cat:
                continue
            bank = row["bank"]
            rid = row["raw_tx_id"]
            cur = conn.execute(
                """update bank_transactions
                   set category=?, cat_method='override_csv', cat_confidence=1.0, user_override=1
                   where bank=? and raw_tx_id=?""",
                (cat, bank, rid),
            )
            if cur.rowcount == 0:
                # fallback: por (banco, fecha, importe, concepto) si el hash cambió
                cur = conn.execute(
                    """update bank_transactions
                       set category=?, cat_method='override_csv', cat_confidence=1.0, user_override=1
                       where bank=? and substr(booking_date,1,10)=? and round(amount_eur,2)=?
                             and concept=?""",
                    (cat, bank, row["booking_date"][:10],
                     round(float(row["amount_eur"]), 2), row["concept"]),
                )
            if cur.rowcount:
                applied += cur.rowcount
            else:
                missing += 1
                print(f"  ⚠ override sin match: {bank} {row['booking_date'][:10]} "
                      f"{row['amount_eur']} {row['concept'][:30]!r}")
    if own:
        conn.commit()
    return applied, missing


def main() -> None:
    applied, missing = apply_overrides()
    print(f"overrides reaplicados: {applied} | sin encontrar: {missing}")


if __name__ == "__main__":
    main()
