---
name: artifact-dingui-mes-a-mes
description: "Artifact 'Dingui mes a mes' (P&L + caja ene-2026 → dic-2027). v5 publicada 17/09/2026 (extractos a 16/09): res26 254,2K, IS26 38,1K, liquidez fin sept 118,5K, dic-26 150,4K, dic-27 334,1K. URL, fuente en docs/artifacts/, convenciones."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2d5cd319-1b67-48a7-9ce5-dd6ce5c74c27
  modified: 2026-09-17T10:25:08.538Z
---

**Artifact publicado el 17/09/2026 para la reunión de socios:** https://claude.ai/artifact/2h6bfZBG3uVqSrDScQt2dh (título "Dingui mes a mes", favicon 🌊). Réplica del "Fondeo mes a mes" de Madrid (https://claude.ai/artifact/ScLg4LdaUkpV3MWHP53riD) adaptada a Dingui.

**Fuente en el repo:** `docs/artifacts/dingui_mes_a_mes.html` (página completa) + `docs/artifacts/dingui_model.js` (solo el modelo, con los datos reales inyectados). Para republicar desde otra máquina: `Artifact publish` con `url` = la de arriba y ese HTML.

**Convenciones del modelo (decididas al construirlo, coherentes con [[liquidez-2026-snapshot]] y [[conciliacion-liquidez-2808]]):**
- Cada celda = suma de componentes `[etiqueta, importe]` → el panel "de dónde sale" lista los componentes. Sin fórmulas ocultas.
- Liquidez = bancos + plazo fijo 6.000 + saldo Fourvenues. Traspasos entre esas bolsas (plazo, retiradas FV) no son flujo.
- Real ene→ago 2026: ene-jun reconstruido de los extractos locales (Caixa CSV 08/07 + Santander XLS; cuadre 0,00 € con los saldos mensuales); jul y ago (hasta el 27/08) de la memoria + overrides. Cada mes real lleva una línea "Ajuste al saldo real del extracto" en «Otros ingresos» (ago −6.745 €, el resto < 400 €).
- Septiembre 2026 = tramo real 28/08→07/09 + lista comprometida VIGENTE de docs/liquidez_cierre_2026.md (act. 07/09 2ª: Cruzcampo +30K, confirming 39.996, Aycoa 19.114, Viento 12.280, RRPP 12.998, DR 10.000, TC1 8.400, Stima 6.000, nómina 5.600, vacaciones 5.000, alquiler 4.594, gestoría 400, IVA ago 17.500). Fin sept 119.653 · fin 2026 133.077 (coincide al euro con el doc).
- P&L: ventas y compras desde julio; **alquiler, comunidad y fijos del local se devengan desde enero/febrero 2026 (petición del usuario 17/09)**; el resto pre-julio = proyecto (criterio 28/08; fila memo "Inversión del proyecto" = filas de proyecto de caja). Fila "Resultado antes de amortización e impuestos" porque la amortización (45K/año) está PENDIENTE DE ESTUDIAR con la gestoría (usuario 17/09). Jul real; ago = cierres 1-26 + 3 noches previstas ≈ 360K con IVA. Personal según estructura oficial (líquido + extras B + IRPF + SS − DJ nómina); DJs caché del sheet; RRPP imputado a agosto; amortización 45K/año desde julio; IS 15 % sobre resultado (param).
- 2027 = repetición de 2026 (cobros/pagos bancarios jul-ago-sep escalados por `ventas27`), parámetros: ventas27, jun27 (% de julio, 0), cogs27 22 %, personal27 17,9 %, djs27 2,6 %, rrpp27 12.998, pepsi27 17.000, preap27 0 (regla 30/08: sin cifrar), vac27 5.000, is 15 %, ivaAgo26 17.500, amortAnual 45.000. IS 2026 se paga jul-27; 202 (18 % cuota 26) oct y dic 27.

**Cifras por defecto (v3, 17/09, con contabilidad de la gestoría — [[contabilidad-gestoria-junago]]):** EBITDA 2026 +248.778 · resultado 2026 +226.278 (jul 106.390 · ago 143.554) · IS 2026 ≈ 33.942 · resultado 2027 +196.115 · liquidez sept-26 117.985 (mínimo) · dic-26 131.409 · dic-27 ≈ 329.871. IVA ago = 3.374,73 (usuario). Septiembre incluye ~13.800 de bebida pendiente según contabilidad. **Junio 2027 = supuesto en € con IVA (`jun27`, default 0) con la estructura de costes y cobros de julio** (petición usuario 17/09). Defaults 2027: cogs27 24,2 %, personal27 18,6 %. Préstamo socios: 12K in / 12K out (5K 20/07, 3K+4K 05/08) — el 4K del 05/08 no está en overrides, va en el modelo.

**Puente ventas→cobros jul-ago 2026 (sección propia en la página):** ventas 575.366 con IVA (jul cierres, ago facturado) = efectivo 51.841 (no pasa por banco) + Fourvenues 89.171 + tarjeta 434.354; TPV liquidado 411.182 + cola sept 21.075 = 432.257 → diferencia 2.097 (0,5 %) = comisión del datáfono. CERRADO. Julio −12.893 = lag de liquidación (30-31/07 cobran en agosto).

**Resueltos por el usuario 17/09:** +524,15 (09/04) = devolución de la notaría → Licencias/legal · +189,99 UME (16/04) = devolución equipamiento DJ → cabina (override cambiado a Sonido/Luces) · +2.000 TRASPASO 27/06 = 3ª transferencia del préstamo de un socio → préstamo total 14.000, devueltos 12.000, **pendientes 2.000** (override cambiado a Préstamo socios). Queda: el ajuste de agosto −2.745 (abonos/salidas menores entre el 8/7 y el 27/8 no desglosados en local: esta máquina no tiene la DB de 735 movs).

**How to apply:** si cambian cifras (IVA ago real, nómina ago, cargos confirming, Cruzcampo), editar `REAL_CAJA`/`SEP_PEND` en `docs/artifacts/dingui_model.js`, regenerar el HTML (sustituir el bloque del modelo) y republicar con la misma URL. Relacionado: [[reference-fondeo-repo]], [[feedback-delegar-opus]] (la categorización bancaria y el HTML los hicieron subagentes Opus).


**v4 PUBLICADA 17/09/2026 (tarde, otra máquina con la DB completa):** extractos Santander + Caixa hasta 16/09 (liquidez real 16/09 = 177.232,49, el modelo cuadra a 0,50 €). Cambios:
- **Alquiler P&L corregido** (la v3 metía 2.297,02 CON IVA + 240 de comunidad aparte): renta 1.700 + comunidad 198,36 (hasta jul) / 216,68 (desde ago) sin IVA, en la misma factura. Caja 2.319,18/mes desde oct.
- **Nueva fila P&L «Rappels de marcas»** (cuenta propia, decisión usuario): Pernod Ricard 6.000 (jul 2.405 / ago 3.595 por botellas — reparto supuesto), Cruzcampo ago 401,50 (Melgarejo RU1113), Melgarejo jul 681,82 (movido desde Acuerdos). Param `rappel27` = 6.000. Margen = ventas + acuerdos + compras + rappels.
- **Devoluciones de compras restan compras**: Melgarejo N4574 base 4.817 en sept (caja +5.818).
- **13.946,03 del 21/08 = devolución de IVA** (fila in_redeme), no retirada FV. **FV cuadra con los cierres**: FV_REAL jun 0 / jul 42.525 / ago 83.700 → LIQ_REAL jun 4.564, jul 128.478; in_fv ago 41.175. Tabla puente: diferencia temporada −7.568 (comisión TPV + efectivo estimado).
- **Devolución IVA junio 11.095,82 en octubre** (fecha supuesta).
- **Septiembre real 28/08→16/09** (SEP_REAL): Aycoa cerrada (9.000 + 10.114,18), Realmivo 4.878,39, IVA ago 3.374,73, RRPP Security 15.172,87 (confirmado), DJs +8.718, Merino 5.944, Ramón Romero 3.389,67, Melgarejo +5.818 / +485,82 / +484 (este sin identificar).
- **SEP_PEND a 16/09**: Cruzcampo +30.000 · confirming 44.999,05 (usuario) · Viento 12.280,05 · licencia DR 10.000 · TC1 ago 10.393,44 · bebida 8.498 (por proveedor) · Stima 2.117,50 factura + 4.000 efectivo · gestoría 400. **Nómina, vacaciones y finiquitos de agosto ya pagados (usuario) → fuera.**
- RRPP P&L ago = 15.172,87 / 1,21; rrpp27 = 15.172,87. Coste proyecto 532.415,12 (Stima).
**Cifras v4:** resultado 2026 242.675 · IS 36.401 · resultado 2027 207.761 · liquidez fin sept 114.544 (mínimo) · dic-26 138.997 · dic-27 317.485. Ajustes a extracto: jul +350, ago −2.698 (explicable: alquiler jul/ago mal repartido en REAL_CAJA, 2º recibo Barter, varios).
**Abierto:** P&L ago personal lleva «vacaciones estimadas −5.000» (esperar finiquitos reales); Pernod: reparto y fecha de cobro; +484 Melgarejo; posible pago doble a Lorente (fact 23); 3 € del confirming; Cala Santa (motivo).

**v5 PUBLICADA 17/09/2026 (noche):** Pernod Ricard 6.200 + IVA (P&L jul/ago por botellas; caja octubre +7.502; `rappel27` 6.200 cobro oct-27) · Melgarejo +484 = aportación comercial (P&L acuerdos sept 400; caja in_acuerdos) · abonos Merino 1244/1245 base 8.207,97 restan compras de septiembre; bebida pendiente sin Merino = 4.554 (saldo a favor Merino 5.987 NO contado hasta saber si lo devuelven) · **amortización lineal a 10 años (contrato de alquiler de 10 años): `amortAnual` 39.500** sobre ~394.600 € sin IVA (contab 325.041 + Stima 22.100 + Viento con factura ~28.150 + tasas 8.250 + sonido menor ~6.300 + equipamiento ~2.500 + conexiones ~2.300); máximo fiscal ~44.700 (sonido 20 %). Jul/ago amort calculada dentro de modelo() (reacciona al supuesto).
**Cifras v5:** resultado 2026 254.233 · IS 38.135 · resultado 2027 213.461 · liquidez fin sept 118.488 (mínimo) · dic-26 150.443 · dic-27 334.075.
**Abierto:** Merino ¿devuelve 5.987 o crédito?, ¿más abonos? · Lorente fact 23 ¿pago doble? · 3 € confirming.
