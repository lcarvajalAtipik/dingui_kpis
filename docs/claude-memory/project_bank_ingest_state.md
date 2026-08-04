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

04/08/2026: resueltos 35 de los 38 sin categorizar vía conciliación con facturas ([[pl-categories]] tiene el detalle y las 2 categorías nuevas validadas: Equipamiento, Gastos extra actividad). Quedan solo 3 con `category IS NULL`: ALIEXPRESS −542,71 (30/04), "2 parte factura" −5.000 (08/05) y Discount_ES −747,89 (15/06). El extracto ingerido sigue llegando solo hasta el 08/07/2026 — pedir exports nuevos para julio.
