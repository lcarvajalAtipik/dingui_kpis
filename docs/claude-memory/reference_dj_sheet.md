---
name: reference_dj_sheet
description: Google Sheet de programación/caché de DJs de Dingui (ID + estructura de columnas + Presu. vs factura registrada).
metadata: 
  node_type: memory
  type: reference
  originSessionId: d3b75570-55a0-4046-801b-dacf6e19f045
  modified: 2026-08-27T09:57:55.982Z
---

Sheet de programación de DJs de Dingui en Drive (Excel subido, `rtpof=true`). ID `1P1zBFi6vyMRwf_3O4vgrMCNa5Uk7EjSd`, pestaña principal `gid=1439535795`. Dueño = cuenta personal lmcarvajal96; **compartido 04/08/2026 con l.carvajal@atipikproperties.com** → ya legible vía MCP Google Drive.

Estructura (Hoja 1), una fila por artista/slot y varias filas por día:
FECHA · Semana · ARTISTA · HORARIO · Horas · Artistas Dispo. · **Presu.** · **Total Fra** · Observaciones · FRA. · IBAN · Contacto.
- `Presu.` = caché acordado (€) por artista.
- `Total Fra` = forma de pago (tag inconsistente): `nomina/nom/NOM` = nómina; `factura/fact` = factura; `si` = ambiguo (lo interpreto como factura, confirmar); vacío = sin marcar.
- Junio = casi todo "NO DJ" (arranque). Agosto en adelante = planificado, mayormente sin caché.

Reconciliación: `Presu.` es caché pactado, NO pago confirmado. Julio 2026 suma **6.080€** (nómina 2.940 / factura+si 1.820 / sin marcar 1.320), pero solo **742€** de facturas DJ registradas a 04/08 → faltan facturas por llegar/registrar o Presu. > pagado. Nómina no aparece en facturas (va por payroll, extracto solo hasta 08/07). Ver [[coste_personal]] y [[sistema_facturas_drive]].

**Esta hoja ES la fuente del coste de DJs para el P&L. REGLA DE CÁLCULO (confirmada por el usuario 27/08):**
- **DJs es UNA categoría propia** en el P&L, con el caché TOTAL del mes (col `Presu.`).
- Los marcados **`Total Fra` = nómina/nom/NOM** se pagaron **EN EFECTIVO** → ese dinero YA está dentro de [[coste_personal]] (el personal se paga en efectivo). Por tanto: **restar el importe DJ-nómina del coste de Personal** y moverlo a DJs (evita doble conteo).
- Los marcados **`Total Fra` = factura/fact** se pagan **por transferencia aparte** → coste DJ independiente (aparecen en banco como "Pago Dj" y en registro de facturas). NO se restan de Personal.
- `si`/vacío = por confirmar; contarlos en DJs, no tocar Personal.
Efecto neto en el P&L del mes: `Personal_final = Personal − DJ_nómina`; `DJs = Presu_total_mes`. Pagos DJ por banco "Pago Dj" desde agosto: Marina Aguilar, Lucas Haurie, Francisco Ruiz, Adrián León. **Cifras reales leídas del sheet vivo el 27/08** (descargado xlsx "Dingui Calendario DJs.xlsx" vía MCP Drive, parseado por col Presu.+Total Fra):
- **JULIO: caché total 7.650** = nómina 2.940 (efectivo→restar de Personal) + factura 910 + "si" 520 + sin marcar 3.280.
- **AGOSTO: caché total 5.980**, TODO sin marcar aún (falta taggear forma de pago). OJO agosto: "19/8 pagado en sala" (Toto/Halcón 200), "25/8 ¿no cobra? WARNING SONIDO". Los 4 pagos DJ por banco de agosto (1.873,22: Marina Aguilar, Lucas Haurie, Francisco Ruiz, Adrián León) son parte de esto.
- Aplicado al P&L julio: DJs=7.650, Personal=28.062−2.940=25.122 (resultado julio pasó de 76.153 a **71.443**). El snapshot viejo (6.080 a 04/08) quedó obsoleto — el sheet creció. Ver [[pl_categories]] y [[project_bank_ingest_state]].
