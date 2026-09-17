---
name: artifact-dingui-mes-a-mes
description: "Artifact 'Dingui mes a mes' (P&L + caja ene-2026 → dic-2027) publicado 17/09/2026: URL, fuente en docs/artifacts/, convenciones del modelo y cifras clave (res26 261K, IS26 39K, liquidez dic-26 133K, dic-27 ~326K)"
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
- P&L operativo arranca en julio (criterio 28/08: pre-julio = proyecto; fila memo "Inversión del proyecto" = filas de proyecto de caja). Jul real; ago = cierres 1-26 + 3 noches previstas ≈ 360K con IVA. Personal según estructura oficial (líquido + extras B + IRPF + SS − DJ nómina); DJs caché del sheet; RRPP imputado a agosto; amortización 45K/año desde julio; IS 15 % sobre resultado (param).
- 2027 = repetición de 2026 (cobros/pagos bancarios jul-ago-sep escalados por `ventas27`), parámetros: ventas27, jun27 (% de julio, 0), cogs27 22 %, personal27 17,9 %, djs27 2,6 %, rrpp27 12.998, pepsi27 17.000, preap27 0 (regla 30/08: sin cifrar), vac27 5.000, is 15 %, ivaAgo26 17.500, amortAnual 45.000. IS 2026 se paga jul-27; 202 (18 % cuota 26) oct y dic 27.

**Cifras por defecto:** resultado 2026 +261.040 (jul 109.217 · ago 161.551 · sep-dic −9.7K con Pepsi +17K) · IS 2026 ≈ 39.156 · resultado 2027 +215.609 · liquidez dic-26 133.077 · dic-27 ≈ 326.116 · mínimo desde sept: 119.653 (sept-26).

**Pendientes que salieron al construirlo (preguntar):** +524,15 TRANSF. A SU FAVOR 09/04 (¿devolución notaría?) · +2.000 TRASPASO 27/06 sin pareja · +189,99 UME 16/04 (¿devolución cabina, no financiero?) · el ajuste de agosto −6.745 (abonos/salidas menores entre el 8/7 y el 27/8 no desglosados en local: esta máquina no tiene la DB de 735 movs).

**How to apply:** si cambian cifras (IVA ago real, nómina ago, cargos confirming, Cruzcampo), editar `REAL_CAJA`/`SEP_PEND` en `docs/artifacts/dingui_model.js`, regenerar el HTML (sustituir el bloque del modelo) y republicar con la misma URL. Relacionado: [[reference-fondeo-repo]], [[feedback-delegar-opus]] (la categorización bancaria y el HTML los hicieron subagentes Opus).
