---
name: project-bank-ingest-state
description: "Estado de la ingesta bancaria — SQLite local con histórico completo hasta 08/07/2026, 38 movimientos sin categorizar pendientes de revisar con el usuario"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d5c392d-c027-49d3-b367-5eebd439e97e
---

Ingesta bancaria persistida el 15/07/2026 en `db/kpis.sqlite` (tabla `bank_transactions`, esquema v2 de `schemas/001_init.sql`: admite caixa+santander, columnas extra/cat_method/cat_confidence/user_override): 239 movimientos (20/08/2025 → 08/07/2026), Caixa 197 + Santander 42. Exports fuente copiados a `data/bancos/inbox/` (`CaixaBank_digital_CaixaBankNow_20260708.csv`, `Documento_69nUd17E.xls`).

**OJO**: `db/` y `data/` están en el gitignore → el SQLite y los exports SOLO existen en la máquina donde se ingirió (la del 15/07). En otra máquina hay que re-pedir los exports y re-ejecutar la ingesta. Ver [[feedback-sync-memoria]].

Quedan 38 movimientos con `category IS NULL` (35 post-30/04) pendientes de resolver con el usuario: certificaciones de obra escritas a mano ("parte N certifica", Florente), equipamiento de cocina (neveras, mesa refrigerada, tostadora), gastos pequeños de tarjeta (bazares, restaurantes, Carrefour), imposición a plazo Santander −3.000€, cartel fachada Viento Creativo −2.371,60€. Al resolverlos: marcar `user_override=1` y añadir regla en [[pl-categories]] / categorizer.py si es recurrente.
