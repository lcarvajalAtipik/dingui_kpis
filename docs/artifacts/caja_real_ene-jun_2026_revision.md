# Caja real mensual — Nuevo VH SL (Dingui) · ene–jun 2026 + 1–8 jul

Fuentes: extracto CaixaBank (20/08/2025–08/07/2026, 197 mov.), extracto Santander TPV (12/06–08/07/2026, 42 mov.), hoja `movimientos 30 abril 2026` del sheet Proyecciones (ground truth hasta 30/04) y `data/bank_overrides.csv`.

**Cobertura: 100 %.** Ningún movimiento queda en `sin_asignar` y el control de cuadre da diferencia 0,00 € en los siete periodos.

## 1. Tabla mensual (euros redondeados, signo del banco)

| Fila | 2026-01 | 2026-02 | 2026-03 | 2026-04 | 2026-05 | 2026-06 | 2026-07-01a08 | TOTAL |
|---|---|---|---|---|---|---|---|---|
| **ENTRADAS** | | | | | | | | |
| in_aportaciones | — | 136.439 | — | 64.200 | 87.700 | — | — | 288.339 |
| in_tpv | — | — | — | — | — | 2.313 | 17.223 | 19.536 |
| in_prestamo_socios | — | — | — | — | — | 12.000 | — | 12.000 |
| in_iva_redeme | — | — | — | — | — | — | — | — |
| in_otros | — | — | — | — | — | 2.000 | — | 2.000 |
| **PROYECTO DE APERTURA** | | | | | | | | |
| proj_lorente | — | — | -54.935 | — | -108.673 | -9.000 | — | -172.608 |
| proj_viento | — | — | — | -10.890 | — | — | -2.372 | -13.262 |
| proj_yuste | — | -24.271 | — | — | — | — | — | -24.271 |
| proj_bs | — | — | — | -20.000 | -5.000 | — | — | -25.000 |
| proj_aycoa | — | — | — | — | — | -10.000 | — | -10.000 |
| proj_cabina | — | — | -8.582 | -4.361 | -3.290 | — | — | -16.233 |
| proj_stima | — | — | -8.470 | -3.025 | — | — | — | -11.495 |
| proj_licencias | — | -3.693 | — | -8.061 | — | — | — | -11.754 |
| proj_equip | — | — | — | -543 | -3.577 | -1.732 | -51 | -5.902 |
| proj_otros | — | -1.784 | -13 | -2.254 | -22 | — | — | -4.073 |
| **OPERATIVA** | | | | | | | | |
| op_cogs | — | — | — | — | — | -2.436 | -605 | -3.041 |
| op_personal | — | — | — | — | — | — | — | — |
| op_ss | — | — | — | — | — | — | — | — |
| op_irpf | — | — | — | — | — | — | — | — |
| op_djs | — | — | — | — | — | — | — | — |
| op_alquiler | — | -3.017 | -2.297 | -2.297 | -2.297 | — | — | -9.908 |
| op_fijos | — | -116 | -131 | 403 | -217 | -640 | -477 | -1.177 |
| op_marketing | — | — | — | -342 | -234 | — | -605 | -1.181 |
| op_extra | — | — | — | -202 | — | -203 | -111 | -515 |
| **FINANCIERO E IMPUESTOS** | | | | | | | | |
| fin_comisiones | -30 | -136 | -137 | 190 | -194 | -911 | -87 | -1.305 |
| fin_plazo | — | — | — | — | — | — | -3.000 | -3.000 |
| fin_confirming | — | — | — | — | — | — | — | — |
| tax_iva | — | — | — | — | — | — | — | — |
| tax_is | — | — | — | — | — | — | — | — |
| **INTERNOS / RESIDUAL** | | | | | | | | |
| internal | — | — | — | — | — | — | — | — |
| sin_asignar | — | — | — | — | — | — | — | — |
| **NETO (sin internal)** | **-30** | **103.422** | **-74.566** | **12.819** | **-35.802** | **-8.608** | **9.916** | **7.149** |

## 2. Saldos de banco a fin de periodo

Calculados anclando al último saldo conocido (Caixa 296,44 € y Santander 14.183,36 € el 08/07/2026) y descontando los movimientos hacia atrás. Santander se abre el 12/06/2026 (saldo 0 antes).

| Corte | CaixaBank | Santander | Total |
|---|---:|---:|---:|
| 2025-12-31 | 7,330.32 | 0.00 | 7,330.32 |
| 2026-01 | 7,300.32 | 0.00 | 7,300.32 |
| 2026-02 | 110,722.26 | 0.00 | 110,722.26 |
| 2026-03 | 36,156.05 | 0.00 | 36,156.05 |
| 2026-04 | 48,974.59 | 0.00 | 48,974.59 |
| 2026-05 | 13,172.42 | 0.00 | 13,172.42 |
| 2026-06 | 1,245.25 | 3,318.69 | 4,563.94 |
| 2026-07-08 | 296.44 | 14,183.36 | 14,479.80 |

## 3. Control de cuadre (suma de filas vs variación de saldos)

| Periodo | Suma filas | Δ saldo bancos | Diferencia |
|---|---:|---:|---:|
| 2026-01 | -30.00 | -30.00 | 0.00 |
| 2026-02 | 103,421.94 | 103,421.94 | 0.00 |
| 2026-03 | -74,566.21 | -74,566.21 | 0.00 |
| 2026-04 | 12,818.54 | 12,818.54 | 0.00 |
| 2026-05 | -35,802.17 | -35,802.17 | 0.00 |
| 2026-06 | -8,608.48 | -8,608.48 | 0.00 |
| 2026-07-01a08 | 9,915.86 | 9,915.86 | 0.00 |

Diferencia 0,00 € en todos los periodos. Los traspasos internos suman 0 dentro de cada mes (ninguna pareja cruza fin de mes), así que excluirlos de `suma_filas` no rompe el cuadre.

## 4. Decisiones dudosas

- **Cogesur = 1.633,50 € partido en dos pagos.** Los dos cargos que el sheet marca `Obra` sin identificar — `tecnico` −326,70 (05/02) y `factura 277` −1.306,80 (26/02) — suman exactamente 1.633,50 €, que es el importe que indicaste para Cogesur (pruebas de carga). Los he mandado los dos a **proj_otros**, no a proj_lorente. Confírmalo: es la única deducción por importe que he hecho.
- **`pulseras` −95,59 (07/05) → op_marketing.** El override del usuario lo marca `Gastos extra actividad`, pero en la taxonomía de esta tarea nombras expresamente «Gráficas Pedraza 95,59» dentro de op_marketing. He dado prioridad a la instrucción específica sobre el override genérico. Si prefieres respetar el override, son 95,59 € que pasan de op_marketing a op_extra en mayo.
- **`CUOTA T. V.Ele.Bu` −33,00 (26/02) → fin_comisiones.** El sheet lo marca `Otros` (que pre-mayo traduzco a proj_otros), pero es la cuota de la tarjeta, y en fin_comisiones nombras «cuota tarjeta». Va a fin_comisiones.
- **`PRECIO SERVIC.PAGOS` −137,34 (07/03) → fin_comisiones.** El sheet lo marca `Legal, gestión, software`, pero es un gasto de servicio de CaixaBank idéntico a los de 28/02, 02/05 y 21/05, que el propio sheet marca `Financiero`. Lo trato como comisión bancaria (parece un error de tecleo del sheet).
- **`Trimble` −18,99 (06/03) → op_fijos.** El sheet lo marca `Otros` esa vez y `Legal, gestión, software` el 06/04. Unifico todos los Trimble (SketchUp) como software recurrente en op_fijos.
- **Restaurantes y compras menores pre-apertura → op_extra.** NARIGONI, NARBONA SOLIS, VISTAHERMOSA, MARKET PTO SANTA y Packlink (abr-2026) están como `Otros` en el sheet, que la regla traduciría a proj_otros. Los he mandado a **op_extra** porque los nombras explícitamente en esa fila. Son 201,72 € en abril.
- **`WWW.AMAZON` −12,99 (25/03) → proj_otros.** Sheet `Otros` pre-mayo y sin pista de qué se compró; podría ser proj_equip.
- **`TRANSF. A SU FAVOR` +524,15 (09/04) → op_fijos (positivo).** Abono entrante que el sheet marca `Legal, gestión, software`. No es una aportación de socio (el sheet lo distingue). Por la regla «resto → op_fijos» queda ahí, en positivo. Si en realidad es una devolución de la notaría o del registro, debería ir a proj_licencias. **Pendiente de confirmar qué es.**
- **`TRASPASO` +2.000,00 (27/06) → in_otros.** No tiene pareja en Santander dentro de ±3 días (el override lo marca «Movimiento entre cuentas», pero la otra pata no existe en los extractos). Siguiendo tu regla, va a in_otros. **Pendiente de identificar.**
- **`h` −150,00 (23/02) → proj_otros.** Sheet `Obra`, concepto ilegible. Sin identificar.
- **`UME` −8.582,50 (12/03) → proj_cabina.** Por el override: no es UME sino Profesional DJ (cabina DJ, pedido 98063). Falta la factura.
- **`UME` +189,99 (16/04) → fin_comisiones.** Devolución marcada `Financiero` en overrides, tal como indicaste. Es raro que una devolución de un proveedor vaya a comisiones bancarias; si es una devolución de la compra de cabina debería ir a proj_cabina.
- **Devoluciones netas contra su fila de origen.** +1.126,85 (01/05, CNX Edistribución) → proj_otros; +10.000 (08/06, Lorente) → proj_lorente; +860,05 Madrid Hifi (21/05) y +815,00 Thomann (23/05) → proj_cabina. Todas en positivo, neteando el cargo original.
- **Confirming del 22/06 → neto 0.** `Cobro A Vencimiento 19/06/2026` −32.343,05 y `Transferencia De Santander Factoring Y Confirming` +32.343,05 el mismo día, los dos en **fin_confirming**. Suman 0: es la refinanciación de una factura, no caja nueva. El coste real son los 892,29 € de «Comisiones/intereses por financiación» (24/06) y los 302,50 € de comisión de formalización (19/06), que van a fin_comisiones.
- **Devoluciones de comisiones del 12/06.** CaixaBank devolvió 283,59 € en ocho apuntes positivos (P.SERV.CERTIF., MANTENIMIENTO, P.SERV. ORDEN TRF/S). Van a fin_comisiones en positivo, por eso junio sale −911,20 y no peor.
- **Filas vacías en el rango.** in_iva_redeme, op_personal, op_ss, op_irpf, op_djs, tax_iva y tax_is quedan a 0: no hay ni un movimiento de esos tipos hasta el 08/07/2026. La devolución de IVA de 40.059,78 € es del 31/07 y el primer modelo 111 (−73,69) del 20/07, ambos fuera de rango. Los primeros pagos a DJs y las disposiciones de efectivo para personal empiezan el 13/07.

## 5. Movimientos sin asignar

Ninguno. Los 172 movimientos del rango (ene-2026 → 08/07/2026) están clasificados.

## 6. Traspasos internos (excluidos del neto)

| Fecha | Banco | Concepto | Importe | Pareja |
|---|---|---|---:|---|
| 2026-06-11 | caixa | traspaso | -9,000.00 | santander 2026-06-12 +9.000 'Concepto Traspaso' |
| 2026-06-12 | santander | Transferencia De Nuevo Vh Sociedad Limitada, Concepto Traspa | 9,000.00 | caixa 2026-06-11 -9.000 'traspaso' |
| 2026-06-19 | caixa | santabder | -500.00 | santander 2026-06-19 +500 'Concepto Santabder' |
| 2026-06-19 | santander | Transferencia Inmediata De Nuevo Vh Sociedad Limitada, Conce | 500.00 | caixa 2026-06-19 -500 'santabder' |
| 2026-06-24 | caixa | traspaso | -400.00 | santander 2026-06-24 +400 'Concepto Traspaso' |
| 2026-06-24 | santander | Transferencia Inmediata De Nuevo Vh Sociedad Limitada, Conce | 400.00 | caixa 2026-06-24 -400 'traspaso' |
| 2026-06-29 | caixa | traspaso | -1,300.00 | santander 2026-06-29 +1.300 'Concepto Traspaso' |
| 2026-06-29 | santander | Transferencia Inmediata De Nuevo Vh Sociedad Limitada, Conce | 1,300.00 | caixa 2026-06-29 -1.300 'traspaso' |
| 2026-07-06 | caixa | TRANSFER INMEDIATA | 900.00 | santander 2026-07-06 -900 'Traspaso Caixa' |
| 2026-07-06 | santander | Transferencia Inmediata A Favor De Nuevo Vh Concepto Traspas | -900.00 | caixa 2026-07-06 +900 'TRANSFER INMEDIATA' |

Todas las parejas cuadran dentro de ±1 día y dentro del mismo mes. El único traspaso entrante sin pareja es el +2.000 del 27/06 (ver dudas).

## 7. Movimientos grandes (|importe| ≥ 1.000 €), 85 apuntes

| Fecha | Banco | Concepto | Importe | Fila | Motivo |
|---|---|---|---:|---|---|
| 2026-02-03 | caixa | TRANSF. A SU FAVOR | 4,800.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-03 | caixa | TRASPASO | 6,400.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-04 | caixa | TRANSF. A SU FAVOR | 2,500.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-04 | caixa | TRANSF. A SU FAVOR | 6,400.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-04 | caixa | TRANSF. A SU FAVOR | 16,000.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-05 | caixa | TRANSF. A SU FAVOR | 2,300.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-05 | caixa | TRANSFER INMEDIATA | 8,000.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-05 | caixa | TRASPASO | 9,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-05 | caixa | TRASPASO | 9,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-07 | caixa | TRANSF. A SU FAVOR | 6,400.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-07 | caixa | TRANSF. A SU FAVOR | 6,400.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-07 | caixa | TRANSF. A SU FAVOR | 9,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-12 | caixa | alquiler febrero | -2,297.02 | `op_alquiler` | Realmivo - renta/comunidad/fianza del local |
| 2026-02-12 | caixa | TRANSFER INMEDIATA | 6,050.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-12 | caixa | TRASPASO | 30,000.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-13 | caixa | TRANSF. A SU FAVOR | 11,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-02-19 | caixa | 209-2026Nuevo Vh | -2,100.00 | `proj_licencias` | notaria (escritura 209-2026) |
| 2026-02-26 | caixa | factura 277 | -1,306.80 | `proj_otros` | Cogesur pruebas de carga (1.633,50 total = 326,70 'tecnico' + 1.306,80 'factura 277') |
| 2026-02-27 | caixa | PAGO TRANSFERENCIAS | -24,271.39 | `proj_yuste` | Sanchez Yuste / Mantec - climatizacion |
| 2026-03-06 | caixa | PAGO TRANSFERENCIAS | -54,935.38 | `proj_lorente` | Lorente y Millan - obra (sheet Tipo=Obra) |
| 2026-03-12 | caixa | UME | -8,582.50 | `proj_cabina` | Profesional DJ (mal rotulado 'UME' en banco) - cabina DJ, pedido 98063 |
| 2026-03-13 | caixa | honorarios proyec | -8,470.00 | `proj_stima` | Stima 21 - arquitectura/ingenieria |
| 2026-03-18 | caixa | REALMIVO SL. | -2,297.02 | `op_alquiler` | Realmivo - renta/comunidad/fianza del local |
| 2026-04-08 | caixa | REALMIVO SL. | -2,297.02 | `op_alquiler` | Realmivo - renta/comunidad/fianza del local |
| 2026-04-17 | caixa | TRIBUTOS | -4,935.99 | `proj_licencias` | tasas/tributos ayuntamiento (licencia de apertura / ICIO) |
| 2026-04-17 | caixa | redaccion proyect | -3,025.00 | `proj_stima` | Stima 21 - arquitectura/ingenieria |
| 2026-04-17 | caixa | TRIBUTOS | -1,885.10 | `proj_licencias` | tasas/tributos ayuntamiento (licencia de apertura / ICIO) |
| 2026-04-17 | caixa | TRIBUTOS | -1,240.20 | `proj_licencias` | tasas/tributos ayuntamiento (licencia de apertura / ICIO) |
| 2026-04-22 | caixa | TRANSF. A SU FAVOR | 7,200.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-29 | caixa | TRASPASO | 4,800.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-29 | caixa | TRASPASO | 6,000.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-29 | caixa | TRANSFER INMEDIATA | 9,000.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-29 | caixa | TRASPASO | 14,400.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-30 | caixa | parte 1 facrura | -20,000.00 | `proj_bs` | BS Aislamientos - insonorizacion |
| 2026-04-30 | caixa | acopio material | -10,890.00 | `proj_viento` | Viento Creativo - rotulacion/tematizacion (factura 181) |
| 2026-04-30 | caixa | THOMANN DE | -4,361.20 | `proj_cabina` | equipo de sonido/cabina DJ |
| 2026-04-30 | caixa | CNX 0001176170 | -1,126.85 | `proj_otros` | Edistribucion CNX (acometida electrica); uno de los dos cargos fue devuelto el 01/05 |
| 2026-04-30 | caixa | CNX 0001176170 | -1,126.85 | `proj_otros` | Edistribucion CNX (acometida electrica); uno de los dos cargos fue devuelto el 01/05 |
| 2026-04-30 | caixa | TRASPASO | 3,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-30 | caixa | TRASPASO | 9,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-04-30 | caixa | TRANSF. A SU FAVOR | 9,600.00 | `in_aportaciones` | aportacion de socios (sheet Tipo=Aportaciones) |
| 2026-05-01 | caixa | PAGO TRANSFERENCIAS | -36,494.16 | `proj_lorente` | Lorente y Millan - obra (sheet Tipo=Obra) |
| 2026-05-01 | caixa | TRANSF. A SU FAVOR | 1,126.85 | `proj_otros` | devolucion cargo duplicado CNX Edistribucion (netea uno de los dos -1.126,85 del 30/04) |
| 2026-05-03 | caixa | TRASPASO | 9,600.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-05 | caixa | TRANSF. A SU FAVOR | 8,000.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-06 | caixa | betopperdj | -2,923.45 | `proj_cabina` | equipo de sonido/cabina DJ |
| 2026-05-07 | caixa | REALMIVO SL. | -2,297.02 | `op_alquiler` | Realmivo - renta/comunidad/fianza del local |
| 2026-05-08 | caixa | 2 parte factura | -5,000.00 | `proj_bs` | BS Aislamientos - insonorizacion |
| 2026-05-08 | caixa | TRANSF. A SU FAVOR | 9,600.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-08 | caixa | TRANSFER INMEDIATA | 10,000.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-09 | caixa | TRANSF. A SU FAVOR | 12,000.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-15 | caixa | mesa refrigerada | -1,200.32 | `proj_equip` | equipamiento / mobiliario del local |
| 2026-05-20 | caixa | PAGO TRANSFERENCIAS | -40,000.00 | `proj_lorente` | Lorente y Millan - obra (sheet Tipo=Obra) |
| 2026-05-22 | caixa | parte 2 certifica | -12,000.00 | `proj_lorente` | certificacion de obra Lorente y Millan |
| 2026-05-22 | caixa | TRANSF. A SU FAVOR | 14,900.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-26 | caixa | parte 3 certifica | -10,000.00 | `proj_lorente` | certificacion de obra Lorente y Millan |
| 2026-05-26 | caixa | TRASPASO | 3,600.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-26 | caixa | TRANSF. A SU FAVOR | 15,000.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-05-27 | caixa | neveras | -2,376.21 | `proj_equip` | equipamiento / mobiliario del local |
| 2026-05-28 | caixa | ultima parte cert | -10,178.54 | `proj_lorente` | certificacion de obra Lorente y Millan |
| 2026-05-28 | caixa | software | -1,149.33 | `proj_otros` | alta Tipsi (software PoS) |
| 2026-05-28 | caixa | TRANSF. A SU FAVOR | 5,000.00 | `in_aportaciones` | transferencia entrante sin pareja interna -> aportacion de socios |
| 2026-06-05 | caixa | sonido 1parte | -10,000.00 | `proj_aycoa` | Aycoa - sonido/iluminacion (1a parte) |
| 2026-06-07 | caixa | TRANSFER INMEDIATA | 4,000.00 | `in_prestamo_socios` | prestamo de socios entrante (override usuario) |
| 2026-06-07 | caixa | TRANSFER INMEDIATA | 5,000.00 | `in_prestamo_socios` | prestamo de socios entrante (override usuario) |
| 2026-06-08 | caixa | parte 1 certifica | -10,000.00 | `proj_lorente` | certificacion de obra Lorente y Millan |
| 2026-06-08 | caixa | TRASPASO | 3,000.00 | `in_prestamo_socios` | prestamo de socios entrante (override usuario) |
| 2026-06-08 | caixa | TRANSFER INMEDIATA | 10,000.00 | `proj_lorente` | devolucion de Lorente: netea el -10.000 'parte 1 certifica' del mismo dia |
| 2026-06-11 | caixa | traspaso | -9,000.00 | `internal` | traspaso entre cuentas propias (pareja en Santander +-3d) |
| 2026-06-12 | santander | Transferencia De Nuevo Vh Sociedad Limitada, Concepto T | 9,000.00 | `internal` | traspaso entre cuentas propias |
| 2026-06-15 | santander | Transferencia A Favor De Florente Concepto: Parte 1 Cer | -9,000.00 | `proj_lorente` | Lorente y Millan (alias bancario 'Florente') - certificacion obra |
| 2026-06-22 | santander | Cobro A Vencimiento 19/06/2026 | -32,343.05 | `fin_confirming` | confirming Santander (par -32.343,05 / +32.343,05 el 22/06, neto 0) |
| 2026-06-22 | santander | Transferencia De Santander Factoring Y Confirming S.a.  | 32,343.05 | `fin_confirming` | confirming Santander (par -32.343,05 / +32.343,05 el 22/06, neto 0) |
| 2026-06-27 | caixa | TRASPASO | 2,000.00 | `in_otros` | TRASPASO +2.000 sin pareja en Santander (+-3d) -> abono sin identificar |
| 2026-06-29 | caixa | traspaso | -1,300.00 | `internal` | traspaso entre cuentas propias (pareja en Santander +-3d) |
| 2026-06-29 | santander | Transferencia Inmediata De Nuevo Vh Sociedad Limitada,  | 1,300.00 | `internal` | traspaso entre cuentas propias |
| 2026-07-02 | santander | Su Orden De Imposicion En Contrato A Plazo 0049 7343 30 | -3,000.00 | `fin_plazo` | contrato a plazo Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 05/07/2026 A Edingui 4 4.862 8 | 1,164.43 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 05/07/2026 A Edingui 4 4.862 8 | 1,250.72 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 04/07/2026 A Edingui 4 4.862 8 | 1,338.61 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 04/07/2026 A Edingui 4 4.862 8 | 1,668.23 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 04/07/2026 A Edingui 4 4.862 8 | 1,681.36 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-06 | santander | Liquidacion Efectuada El 05/07/2026 A Edingui 4 4.862 8 | 2,960.04 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-07 | santander | Liquidacion Efectuada El 07/07/2026 A Edingui 4 4.862 8 | 1,104.39 | `in_tpv` | liquidacion TPV Santander |
| 2026-07-08 | santander | Transferencia Inmediata A Favor De Viento Creativo Conc | -2,371.60 | `proj_viento` | Viento Creativo - cartel fachada |
