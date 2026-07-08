---
name: bank-format-santander
description: "Formato del export de Santander (cuenta TPV de Nuevo VH SL) — XLSX con extensión .xls, headers en fila 8; liquidaciones TPV con bruto en Referencia 1"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a861d9eb-9449-477a-89e6-e7bb7676b867
---

Cuenta **Santander ES47 0049 7343 71 2310017971** (titular NUEVO VH SL, abierta 12/06/2026 para el TPV de Dingui). Validado con el primer export real (08/07/2026). Parser: `parse_santander` en `src/kpis/ingest/bancos.py`.

**Cómo identificar:** archivo `Documento_{random}.xls` — **es un XLSX (zip OOXML) con extensión .xls** (magic `PK`, `zipfile.is_zipfile()` = True; openpyxl lo abre si se ignora la extensión). NO usar xlrd.

**Estructura (sheet "movimientos"):**
- Filas 1-5: bloques Titular / Saldo disponible / Saldo real / Cuenta (IBAN en texto) / Retenciones / Saldo consolidado.
- Fila 6: "Movimientos Fecha desde DD/MM/YYYY Fecha Hasta DD/MM/YYYY" + timestamp del export.
- Fila 7 (índice 0-based): headers = `Fecha Operación | Fecha Valor | Concepto | Importe | Divisa | Saldo | Divisa | Código | Número de documento | Referencia 1 | Referencia 2 | Información adicional`.
- Datos: fechas como **string** DD/MM/YYYY; importes **float nativos** con signo.

**Conceptos clave:**
- `Liquidacion Efectuada El DD/MM/YYYY A Edingui 4 4.862 8.614 N` = **liquidación TPV** (N = nº de terminal 0-4). El `Importe` es el **neto** tras comisión del datáfono; **Referencia 1 lleva el bruto** (ej. neto 203,83 / bruto 204,50). Código 135.
- `Transferencia [Inmediata] De/A Favor De Nuevo Vh ...` = **traspaso interno** con la cuenta CaixaBank (Nuevo Vh = la propia sociedad).
- `Transferencia De Santander Factoring Y Confirming... Abono Facturas A Vto.` / `Cobro A Vencimiento DD/MM/YYYY` = rotación de confirming (neto 0); el coste real es `Comisiones/intereses Por Financiación`.
- Gastos TPV: `Comision Por Instalacion O Mantenimiento De Tpv`, `Cuota App Android. Comercio: NNN`, `Liquidacion Del Contrato`, `Liquidación Indemnizatorio`.
- `Su Orden De Imposicion En Contrato A Plazo` = depósito a plazo propio (no P&L).

**Deduplicación:** hash de `(bank, Fecha Operación, Importe, Concepto, Referencia 1, Saldo)`.

Relacionado: [[bank-format-caixa]], [[business-overview]], [[feedback-bank-format-stable]].
