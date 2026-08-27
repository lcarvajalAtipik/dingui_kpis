---
name: reference_dj_sheet
description: Google Sheet de programación/caché de DJs de Dingui (ID + estructura de columnas + Presu. vs factura registrada).
metadata: 
  node_type: memory
  type: reference
  originSessionId: d3b75570-55a0-4046-801b-dacf6e19f045
  modified: 2026-08-27T09:49:19.000Z
---

Sheet de programación de DJs de Dingui en Drive (Excel subido, `rtpof=true`). ID `1P1zBFi6vyMRwf_3O4vgrMCNa5Uk7EjSd`, pestaña principal `gid=1439535795`. Dueño = cuenta personal lmcarvajal96; **compartido 04/08/2026 con l.carvajal@atipikproperties.com** → ya legible vía MCP Google Drive.

Estructura (Hoja 1), una fila por artista/slot y varias filas por día:
FECHA · Semana · ARTISTA · HORARIO · Horas · Artistas Dispo. · **Presu.** · **Total Fra** · Observaciones · FRA. · IBAN · Contacto.
- `Presu.` = caché acordado (€) por artista.
- `Total Fra` = forma de pago (tag inconsistente): `nomina/nom/NOM` = nómina; `factura/fact` = factura; `si` = ambiguo (lo interpreto como factura, confirmar); vacío = sin marcar.
- Junio = casi todo "NO DJ" (arranque). Agosto en adelante = planificado, mayormente sin caché.

Reconciliación: `Presu.` es caché pactado, NO pago confirmado. Julio 2026 suma **6.080€** (nómina 2.940 / factura+si 1.820 / sin marcar 1.320), pero solo **742€** de facturas DJ registradas a 04/08 → faltan facturas por llegar/registrar o Presu. > pagado. Nómina no aparece en facturas (va por payroll, extracto solo hasta 08/07). Ver [[coste_personal]] y [[sistema_facturas_drive]].

**Esta hoja ES la fuente del coste de DJs para el P&L.** Categoría de banco **"DJs / Programación"** (confirmada por el usuario como categoría propia, 27/08) = pagos por transferencia "Pago Dj" (desde agosto: Marina Aguilar, Lucas Haurie, Francisco Ruiz, Adrián León). Pero el coste completo de DJs de un mes se toma de ESTE sheet (`Presu.`), NO del banco, porque los DJs se pagan por 3 vías: **nómina** (posible solape con [[coste_personal]] → no doble-contar), **factura** (registro facturas) y **transferencia/efectivo**. Para el P&L de un mes: usar el caché del sheet y descontar la parte que ya va en Personal. Julio ≈ 6.080 caché (de los cuales ~2.940 por nómina). Ver [[pl_categories]] y [[project_bank_ingest_state]].
