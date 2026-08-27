---
name: project-bank-ingest-state
description: "Estado ingesta bancaria: 659 movs hasta 27/08/2026 (Caixa+Santander). Personal se paga EN EFECTIVO (confirmado por usuario). Comisión TPV va descontada de origen (neto=venta real). Categoría nueva 'DJs / Programación'. Solo 1 sin categorizar (Discount_ES). OJO dedup entre exports solapados."
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
  modified: 2026-08-27T09:45:33.351Z
---

**ACTUALIZACIÓN 27/08/2026:** re-ingesta con export Santander nuevo (12/06→27/08). DB ahora **659 movs, 2025-08-20 → 2026-08-27**. Solo **1 sin categorizar** (Discount_ES −747,89, 15/06, sigue sin identificar). Nueva categoría **"DJs / Programación"** (pagos DJ por banco desde agosto: Marina Aguilar, Lucas Haurie, Francisco Ruiz, Adrián León, concepto "Pago Dj"; en julio NO hay DJs por banco). Usuario CONFIRMÓ: personal se paga en efectivo; comisión TPV va descontada de origen (el neto liquidado ES la venta real); alquiler se imputa al mes devengado. **⚠ LECCIÓN DEDUP:** exports Santander solapados generan raw_tx_id DISTINTO para el día de solape (05/08 dio 11 duplicados exactos) → tras re-ingestar, dedup fino por (fecha, importe, concepto) y borrar los del export más nuevo. **⚠ SIEMPRE `dump_bank_overrides.py` tras recategorizar en DB**: la reingesta reaplica el CSV y revierte cambios solo-en-DB (pasó con id 136, la devolución +10.000 de Lorente del 8/6 volvió a 'Préstamo socios'; ya persistido a Obra en el CSV).

**⚠ EXPORT SANTANDER 05/08 INCOMPLETO (resuelto 27/08):** el re-export del 27/08 trae el 05/08 completo; los 11 movs del 05/08 coincidían exactos con el export viejo (0 filas nuevas ese día), así que el hueco de −22,4K era del tramo 4/8 y quedó cubierto. Check de continuidad de saldos sigue como práctica estándar.

**[histórico 05/08] ⚠ EXPORT SANTANDER 05/08 INCOMPLETO:** verificación de continuidad de saldos detecta −22.369,05 € de cargos del 4-5/8 que el saldo refleja pero NO están como filas (el saldo salta de 71.612,95 a 51.426,96). PEDIR re-export. El check de integridad (saldo fila a fila) queda como práctica estándar en cada ingesta. Caixa 05/08: 0 rupturas, completo. Saldos 5/8: Santander 26.874,85.

**Estado 05/08/2026:** `scripts/ingest_bancos_sqlite.py` (nuevo, dedup por raw_tx_id) → DB local 489 movimientos, 2025-08-20 → 2026-08-05. Exports en data/bancos/inbox/ (Caixa CSV 05/08 + Santander XLS 05/08).

**⚙ OVERRIDES QUE VIAJAN POR GIT (montado 07/08/2026):** la DB (`db/kpis.sqlite`) y los exports están en .gitignore → se reconstruyen por máquina, así que las categorías puestas A MANO se perderían. Ahora viven en **`data/bank_overrides.csv` (SÍ trackeado**, excepción en .gitignore), clave = `raw_tx_id` (hash determinista banco+fecha+importe+concepto+saldo, estable entre exports; fallback por banco+fecha+importe+concepto). Flujo: (1) recategorizas en la DB → (2) `uv run python scripts/dump_bank_overrides.py` refresca el CSV → (3) commit. Al re-ingestar, `ingest_bancos_sqlite.py` llama a `apply_bank_overrides.py` y las reaplica solas. A 07/08: 113 overrides capturados. Probado round-trip (rompí y restauró). SIEMPRE hacer dump+commit tras categorizar a mano.

**HALLAZGOS del tramo 08/07→05/08:**
1. **CERO nóminas, CERO TGSS, IRPF solo 73,69 € (AEAT 20/07)** → el personal de sala se paga EN EFECTIVO desde la caja nocturna (el "gasto personal" de los partes). No hay estructura formal de nómina visible aún (salvo "Formación Cocina Paco" 700 €). Tema laboral/fiscal a tratar con el usuario y gestoría — el gross-up de SS/IRPF que estimábamos NO se está pagando (aún).
2. **El efectivo de caja casi no se ingresa en banco** (solo 1 ingreso 2.850 de Borja Ybarra) — se usa para pagar personal y gastos.
3. **Proveedores de bebida se pagan por "deuda" en importes redondos**, no por factura: Merino 25.000 pagados (facturado ~36,5K → pendiente ~11,5K), Melgarejo 9.000 (facturado 26,1K → pendiente ~17K).
4. **HIELO real: 3.121,10 € pagados** (521 + 1.069,10 + 1.531 el 04/08) → existe una 3ª factura de hielo ~1.531 SIN capturar (pedirla). Hielo julio ≈ 2.800 sin IVA → ~0,25-0,27 €/copa.
5. **TPV julio-agosto: 179.355 € netos** en 152 liquidaciones.
6. **La obra/instalaciones se está pagando con la caja del verano**: desde 8/7 → Mantec/Sánchez Yuste (aires) 26,2K + Stima (arquitecto) 13,1K + BS Aislamientos 8,1K + Aycoa (sonido) 10K + Florente 8,8K + Viento Creativo 7,4K ≈ **74K de deuda de obra liquidada en un mes**.
7. **57 movimientos sin categorizar (−131,7K)**: casi todo las transferencias anteriores (conceptos con alias: "Florente", "Mantec", "Aycoa", "Stima") → añadir reglas al categorizador. NOTA: los alias de transferencia usan apodos ("Florente" = Lorente y Millán).

Relacionado: [[coste-personal]], [[pl-categories]], [[mercaderia-gerente]], [[sistema-facturas-drive]].
