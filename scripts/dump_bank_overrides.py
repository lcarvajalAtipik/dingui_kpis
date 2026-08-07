#!/usr/bin/env python
"""Vuelca las categorizaciones manuales de la DB a data/bank_overrides.csv (git).

Inverso de apply_bank_overrides.py. Flujo de trabajo:
  1. Categorizas/recategorizas movimientos a mano en db/kpis.sqlite.
  2. `uv run python scripts/dump_bank_overrides.py`  → refresca el CSV trackeado.
  3. git add data/bank_overrides.csv && commit → la categorización viaja a otras máquinas.
Al re-ingestar en cualquier máquina, apply_bank_overrides.py las reaplica.

Captura todo lo que el categorizador automático NO produce de forma determinista
(decisiones humanas y conciliaciones contra facturas).
"""
from __future__ import annotations

import pandas as pd

from kpis import config, db

OUT = config.REPO_ROOT / "data" / "bank_overrides.csv"

QUERY = """
    select bank, raw_tx_id, booking_date, amount_eur, concept, category, cat_method
    from bank_transactions
    where user_override=1
       or cat_method in ('user','user_override','override_csv','manual_conciliacion',
                         'ambiguous_resolved','factura_conciliada','factura_probable')
    order by booking_date, bank
"""


def main() -> None:
    conn = db.connect()
    ov = pd.read_sql(QUERY, conn)
    ov["booking_date"] = ov.booking_date.str[:10]
    # 'override_csv' es el método que deja apply_*; al volcar lo normalizamos a 'user'
    ov["cat_method"] = ov.cat_method.replace("override_csv", "user")
    # conserva la nota previa si el CSV ya existía (match por raw_tx_id)
    notas = {}
    if OUT.exists():
        prev = pd.read_csv(OUT)
        if "nota" in prev.columns:
            notas = dict(zip(prev.raw_tx_id, prev.nota.fillna("")))
    ov["nota"] = ov.raw_tx_id.map(lambda r: notas.get(r, ""))
    ov = ov[["bank", "raw_tx_id", "booking_date", "amount_eur", "concept", "category", "cat_method", "nota"]]
    ov.to_csv(OUT, index=False)
    print(f"volcados {len(ov)} overrides → {OUT.relative_to(config.REPO_ROOT)}")
    print(ov.category.value_counts().to_string())


if __name__ == "__main__":
    main()
