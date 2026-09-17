---
name: contabilidad-gestoria-junago
description: "Libros de Stipendium jun-ago 2026 (diario, mayor, registros) leídos el 17/09: P&L contable jul +121K / ago +186K, nómina ago real (bruto 27.423, TC1 10.393), IVA ago no reproducible (usuario dice 3.374,73), 17 anomalías (sin alquiler devengado, sin amortización, cuenta puente BANCOS −142K, caja sin movimientos, Stima a gasto)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2d5cd319-1b67-48a7-9ce5-dd6ce5c74c27
  modified: 2026-09-17T11:14:37.499Z
---

**Fuente:** `data/gestoria/2026-jun-ago/` (4 xlsx de Stipendium, emitidos 10-15/09/2026; copia del `~/Downloads/Archive 4` del usuario). Informe completo (tablas por cuenta, IVA, balances, comparación) en **`docs/contabilidad_gestoria_jun-ago_2026.md`** (git) + JSON en `docs/artifacts/`. Leído por subagente Opus ([[feedback-facturas-siempre-opus]]).

**Datos firmes incorporados al modelo ([[artifact-dingui-mes-a-mes]]):**
- Ventas facturadas (705, todo al 10 %): jun 1.604,82 · jul 204.157,51 (= cierres 203.310 + rappel Melgarejo 681,82 + Gloria Durán 165,29) · **ago 319.750,15** (351.725 con IVA; los cierres 1-26 dan 298.761 → las últimas noches ≈ 21K base). Agosto real < los 360K estimados.
- Compras contabilizadas (600+602, sin existencias): jun 12.655 · jul 47.643 · ago 79.183.
- **Nómina agosto:** bruto 27.423,23 · SS empresa 8.717,44 · SS trab 1.676,00 · IRPF 547,50 · líquido 24.348,11 · anticipos 851,62 · **TC1 10.393,44** (paga ~fin sept). Julio confirmado (28.062,18).
- DJs con factura (607): jul 700 · ago 4.950 (Ignacio Lara 2.900…). RRPP: **cero facturas** (todo efectivo).
- Fijos sin Stima: jul 788 · ago 3.068 (Stipendium 2.220).
- Deuda proveedores 31/08 (acreedor): 102.075, de los que bebida ≈ 38.085 (Merino 19.564, CCEP 5.710, Chamán 4.766, Melgarejo 4.412, Ipasur 1.863, hielo 1.045…) → tras lo pagado 28/08-07/09 (22.257) y devoluciones CCEP sept (2.032) quedan **~13.800 de bebida pendiente** (añadido a la limpieza de sept). Javier Quintero Alarcón 2.046 sin identificar.
- Inmovilizado contable 325.041 (sin Stima 10.850 ni cartel Viento 1.960, que van a gasto) y **amortización acumulada 0**. Bancos 31/08: Caixa 20.080,52 + Santander 166.331,86.

**IVA:** mayor ago: rep 31.978 − sop 30.803 = 1.175; registros: 31.975 − 27.618 = 4.357; **el usuario dice 3.374,73** (no reproducible → pedir PDF 303 ago). El registro de recibidas va CORTO frente al mayor (ago −3.185 de IVA, casi todo Melgarejo; jul −1.605): si el 303 sale del registro, se paga IVA de más. 470 "HP deudor IVA" 54.006 (preapertura) sin usar; pago 20/08 de 9.420,95 vs cálculo jul 9.378. Aycoa F61 ya con NIF correcto.

**Anomalías a tratar con Stipendium (prioridad):** (1) registro recibidas incompleto vs mayor; (2) crédito IVA preapertura 54K sin compensar; (3) sin asientos de liquidación de IVA; (4) **alquiler jul-ago NO devengado** (faltan facturas Realmivo) ni comunidad; (5) cuenta puente 572.1 BANCOS −142.443 y proveedores de obra con saldo deudor 166.427 (pagos contabilizados dos veces: Mantec 49.439, Lorente 41.323, eDistribución 22.254, Viento 18.174, Stima 11.495, Realmivo 9.188, BS 8.146); (6) caja 570 sin movimientos + clientes 430 +143.083 (efectivo de barra no contabilizado); (7) ni amortización ni existencias; (8) capital social 6.000 en vez de 3.000; (9) Stima y cartel Viento a gasto; (10) comisión factoring duplicada 1.191; (11) diario truncado (asiento 1272); (12) todo al 10 % incl. entradas ([[iva-rates]]); (13) nóminas jul-ago figuran sin pagar (465 −43.668); (14) nada de Fourvenues ni Pepsi en emitidas; (15) socios en 551 c/c (165.650) no como fondos propios.

Relacionado: [[coste-personal]], [[conciliacion-iva-contable-junago]], [[obra-proveedores-ledger]], [[pnl-2026-snapshot]].
