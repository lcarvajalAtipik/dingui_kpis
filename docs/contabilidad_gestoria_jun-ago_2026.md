# Contabilidad Stipendium jun–ago 2026 (Nuevo VH SL) — lectura del diario y el mayor

Fuentes: `data/gestoria/2026-jun-ago/` — DIARIO y MAYOR (emitidos 15/09/2026, periodo 01/01–31/08/2026), REGISTRO EMITIDAS (emitido 10/09, jun–ago) y REGISTRO RECIBIDAS (emitido 15/09, **solo jul–ago**).

Notas de parseo: el **mayor cuadra** (debe = haber = 3.438.254,14) y lo uso como fuente principal; el **diario está truncado** (le faltan las 2 últimas líneas del asiento 1272 del 31/08: 640 por 74,88 y 642 por 48,30; el propio total del diario descuadra en −123,18). 133 cuentas, sin hojas de rectificativas ni intracomunitarias en los registros nuevos.

---

## 1. Cuenta de resultados mensual (signo: ingreso +, gasto −)

### 1.a Filas del modelo

| Fila del modelo | Cuentas incluidas | jun | jul | ago | jun–ago |
|---|---|---:|---:|---:|---:|
| **Ventas** | 700 Ventas de mercaderías, 705 Prestaciones de servicios | 1.604,82 | 204.157,51 | 319.750,15 | 525.512,48 |
| Acuerdos comerciales / rappels | — (no existe cuenta 759/609) | 0 | 0 | 0 | 0 |
| **Compras bebida y comida** | 600 Compras de mercaderías, 602 Otros aprovisionamientos (×2 subcuentas), 608 Devoluciones | −12.654,99 | −47.642,51 | −79.182,84 | −139.480,34 |
| **Personal** | 640 Sueldos y salarios, 642 SS a cargo de la empresa | 0 | −28.062,18 | −36.140,67 | −64.202,85 |
| **DJs / artistas** | 607 Trabajos realizados por otras empresas | 0 | −700,00 | −4.950,00 | −5.650,00 |
| RRPP / relaciones públicas | — (no hay nada identificable) | 0 | 0 | 0 | 0 |
| **Alquiler y comunidad** | 621 Arrendamientos y cánones | −2.251,98 | **0** | **0** | −2.251,98 |
| **Fijos (gestoría, seguros, telecom, software)** | 623 Prof. independientes, 625 Primas de seguros, 628 Telefonía, 629.1 Otros servicios, 629.2 Creacción BBDD | −1.010,42 | −4.538,17 | −10.168,19 | −15.716,78 |
| **Marketing / publicidad** | 627 Marketing digital | −500,00 | −500,00 | −1.351,60 | −2.351,60 |
| **Gastos de equipo y varios** | 622 Reparación y conservación, 629.0 Otros servicios | −115,46 | −764,78 | −2.082,10 | −2.962,34 |
| **Financiero** | 626 Servicios bancarios, 626.1 Comisiones factoring | −1.803,49 | −680,61 | −109,32 | −2.593,42 |
| Amortización | — (**no hay 680/681 ni 28x**) | 0 | 0 | 0 | 0 |
| Impuesto de sociedades | — (no hay 630) | 0 | 0 | 0 | 0 |
| Otros tributos (631) | 631 (solo feb: 190,25) | 0 | 0 | 0 | 0 |
| **RESULTADO contable** | | **−16.731,52** | **121.269,26** | **185.765,43** | **290.303,17** |

No queda ninguna cuenta de los grupos 6/7 fuera de la clasificación (la fila «otros» está vacía).

### 1.b Detalle por cuenta

| Cuenta | Nombre | jun | jul | ago |
|---|---|---:|---:|---:|
| 700 | Ventas de mercaderías | 0 | 0 | 4.545,46 |
| 705 | Prestaciones de servicios | 1.604,82 | 204.157,51 | 315.204,69 |
| 600 | Compras de mercaderías | −12.090,83 | −45.768,89 | −74.717,78 |
| 602.0 | Compras de otros aprovisionamientos | −564,16 | −1.873,62 | −3.689,92 |
| 602.1 | Compra de otros aprovisionamientos | 0 | 0 | −775,14 |
| 607 | Trabajos realizados por otras empresas (DJs) | 0 | −700,00 | −4.950,00 |
| 621.0 | Arrendamientos y cánones | −2.251,98 | 0 | 0 |
| 622.1 | Reparación y conservación | 0 | −584,71 | 0 |
| 623.0 | Servicios profesionales indep. | −752,69 | 0 | 0 |
| 623.1 | Servicios de prof. independientes | 0 | −3.750,00 | −9.389,91 |
| 625 | Primas de seguros | 0 | −746,17 | −519,05 |
| 626.0 | Servicios bancarios y similares | −911,20 | −381,47 | −109,32 |
| 626.1 | Comisiones factoring Santander | −892,29 | −299,14 | 0 |
| 627.1 | Marketing digital | −500,00 | −500,00 | −1.351,60 |
| 628.4 | Suministro de telefonía e internet | 0 | −9,12 | −31,40 |
| 629.0 | Otros servicios | −115,46 | −180,07 | −2.082,10 |
| 629.1 | Otros servicios | −107,77 | −32,88 | −60,88 |
| 629.2 | Creacción BBDD | −149,96 | 0 | −166,95 |
| 640 | Sueldos y salarios | 0 | −21.060,10 | −27.423,23 |
| 642 | Seguridad Social a cargo de la empresa | 0 | −7.002,08 | −8.717,44 |

### 1.c Quién hay dentro de cada partida «blanda»

- **DJs / artistas (607)** — jul: Fernando Chavarri 450 + Daniel Félix Alonso 250. ago: Ignacio Lara Viguera 2.900, José María Carrión Evans 1.000, Rubén Sanz Lanero 400, Daniel Félix Alonso 250, Juan Fco. García Zajara 200, Sonlive Group 200. Todos con retención de IRPF (cuenta 4751) → son artistas/profesionales facturando, no nómina. **Los DJs que cobran por nómina están dentro del 640**, no aquí.
- **Fijos (623/625/628/629.1/629.2)** — jun: Francisco Guzmán Sada 752,69 · Master Gift 107,77 · Future is an Attitude 149,96. jul: **Stima 21 3.750** · Mapfre 746,17 · Telefónica 9,12 · Google 8,10 · Farmacia Saralegui 24,78. ago: **Stima 21 7.100** · **Stipendium 2.220** · Tipsi 69,91 · Mapfre/Multiservicios 519,05 · Telefónica 31,40 · Google 16,20 · Maldonado 44,68 · Future is an Attitude 166,95.
  ⚠ **Stima 21 (arquitecto) va a gasto corriente en la contabilidad**; en nuestro modelo es obra/inmovilizado (`proj_stima`). Son 10.850 € de jul+ago que no deberían estar en el P&L operativo.
- **Equipo y varios (622/629.0)** — jun: Plato al Centro 115,46. jul: Sonicolor 262,99, Suministros Industriales Bahía 180,77, Leroy Merlin 96,25, Lumisur 24,32, Fco. Ponce 14,17, Fesama 6,21, CoverManager 73,45, Plato al Centro 33,82, Viento Creativo 72,80. ago: **Viento Creativo 1.960 (cartel de fachada, factura 314)** + CoverManager 122,10.
  ⚠ El cartel de Viento Creativo también es obra en nuestro modelo.
- **Marketing (627)** — Barter Consultancy 500/mes (jun y jul) y **Henris Brand 1.351,60 en agosto**, que en realidad son los **uniformes** (nuestro modelo los lleva a «equipo y varios»).
- **Financiero (626)** — jun incluye comisión de formalización de confirming 302,50 y varias regularizaciones negativas; jul, la comisión de factoring.

---

## 2. IVA por mes

### 2.a Según el mayor (devengo contable)

| | jun | jul | ago | total |
|---|---:|---:|---:|---:|
| Repercutido (477) | 160,48 | 20.435,51 | 31.978,05 | 52.574,04 |
| Soportado (472) | 11.729,22 | 11.057,54 | 30.802,64 | 53.589,40 |
| **Resultado** | **−11.568,74** (a compensar/devolver) | **+9.377,97** (a ingresar) | **+1.175,41** (a ingresar) | −1.015,36 |

### 2.b Según los libros registro

| | jun | jul | ago |
|---|---:|---:|---:|
| Repercutido (emitidas) | 160,48 | 20.433,81 | 31.974,65 |
| Soportado (recibidas) | *no viene en este export* | 9.453,04 | 27.617,57 |
| **Resultado** | — | **+10.980,77** | **+4.357,08** |

El registro de emitidas difiere del mayor en 1,70 € (jul) y 3,40 € (ago): son los apuntes de **Google Cloud (adquisición intracomunitaria)**, que generan IVA repercutido y soportado simultáneo y el registro de emitidas no recoge.

### 2.c ¿Se reproduce el IVA de agosto de 3.374,73 €? **No.**

Con estos libros salen dos cifras para agosto y ninguna es 3.374,73:

- **1.175,41 €** si usas el mayor (repercutido 31.978,05 − soportado 30.802,64).
- **4.357,08 €** si usas los libros registro tal cual (31.974,65 − 27.617,57).

La cifra del usuario cae justo entre las dos. El origen del hueco está identificado: **el registro de recibidas de agosto tiene 3.185,07 € menos de IVA soportado que el mayor**, y la diferencia es casi toda de **Melgarejo (mayor 5.583,84 vs registro 2.858,53 → +2.725,31)**, más **Hielo Express (+311,07)**, **Makro (+145,29)** y **Google intracom (+3,40)**. En julio pasa lo mismo: mayor 11.057,54 vs registro 9.453,04 (Melgarejo +1.259,26, Hielo Express +82,11, Makro +259,27, Farmacia +2,16, Google +1,70). O sea: **el libro registro fiscal que usan para el 303 está incompleto frente a su propia contabilidad.**

Para llegar a 3.374,73 habría que declarar un soportado de **28.599,92 €** (982,35 € más que el registro, 2.202,72 € menos que el mayor). No hay ninguna combinación limpia de facturas que dé ese número. **Pide a Stipendium el PDF del 303 de agosto** para cerrar esto.

**Composición del soportado de agosto (mayor, 30.802,64 €) — facturas grandes:**

| Proveedor | Fra. | Fecha | Base | IVA |
|---|---|---|---:|---:|
| AYCOA Distribuciones | 61 (inst. sonido) | 10/08 | 26.115,00 | **5.484,15** |
| Lorente y Millán | 28 (6ª certificación obra) | 07/08 | 19.586,22 | 4.113,11 |
| AYCOA Distribuciones | 41 (inst. sonido) | 01/08 | 10.343,00 | 2.172,03 |
| Melgarejo | N4039 | 17/08 | 7.900,25 | 1.659,06 |
| Stima 21 | T32665 | 05/08 | 7.100,00 | 1.491,00 |
| Grupo Merino | 26210/26A | 20/08 | 5.022,13 | 1.054,65 |
| Melgarejo | N4121 | 24/08 | — | 1.097,28 |
| Melgarejo | N3996 | 11/08 | — | 851,73 |
| Chamán Spiritual Drinks | 68-26 | 01/08 | 3.939,00 | 827,19 |
| Grupo Merino | 24797/26A | 10/08 | 3.491,24 | 733,16 |
| Melgarejo | N4169 | 31/08 | 3.355,00 | 704,56 |
| Grupo Merino | 27223/26A | 28/08 | 3.259,83 | 684,56 |
| Melgarejo | N2971 | 01/08 | — | 682,53 |
| Grupo Merino | 24584/26A | 10/08 | 3.074,80 | 645,71 |
| Viento Creativo | /26-000314 (cartel) | 01/08 | 1.960,00 | 411,60 |
| Ignacio Lara (DJ) | 32/2026 | 31/08 | 2.900,00 | 290,00 |
| Stipendium | 1033 + 1407 + 1580 | ago | 2.220,00 | 466,20 |

Solo **AYCOA 61 + AYCOA 41 + Lorente 28 = 11.769,29 € de IVA** (38 % del soportado de agosto): son obra/inmovilizado, no gasto del mes. Sin ellos el IVA de agosto habría sido ~12.945 € a ingresar.

✅ **Buena noticia**: la **AYCOA F61 ya está con el NIF correcto (B11827763)** en este registro nuevo; el error de «Shantou Xian Keji» que detectamos el 10/09 está corregido.

### 2.d Pagos y saldos de IVA

- **20/08/2026: pago de 9.420,95 €** (cuenta 475, «2026iva Autoliquidación», contra Santander). Corresponde al **303 de julio** (REDEME, mensual). Mi cálculo de julio da 9.377,97 (mayor) → **descuadre de 42,98 €** con lo efectivamente pagado.
- ⚠ **La gestoría no ha contabilizado ninguna liquidación de IVA**: no hay asientos que salden 477 contra 472. Por eso a 31/08 quedan vivos 477 = −52.574,04 y 472 = +54.598,24, y la 475 queda con **saldo deudor de 9.420,95** (pagaron sin reconocer la deuda).
- **470 «HP deudor IVA [C]» = 54.005,81 €** a 31/08: es todo el IVA soportado de la preapertura (ene–jun), reclasificado el 10/06. Está pendiente de devolución o compensación; **no se está usando para compensar los 303 mensuales** (de hecho pagaron 9.420,95 en agosto teniendo ese crédito). Hay que aclararlo con Stipendium.

---

## 3. Ventas emitidas por mes y tipo de IVA

| Mes | Base 10 % | Base 21 % | **Base total** | Cuota | Nº facturas |
|---|---:|---:|---:|---:|---:|
| junio | 1.604,82 | 0 | **1.604,82** | 160,48 | 1 |
| julio | 203.992,22 | 165,29 | **204.157,51** | 20.433,81 | 103 |
| agosto | 319.750,15 | 0 | **319.750,15** | 31.974,65 | 149 |
| **total** | **525.347,19** | **165,29** | **525.512,48** | **52.568,94** | **253** |

Destinatarios:

- **«CLIENTES (EUROS)» al 10 %** — es prácticamente todo: las facturas resumen diarias de los tickets del TPV (`FS<ddmm><letra>`, p. ej. FS0108A…FS0108F, varias por noche, de ~2.272,73 € cada una). jun 1.604,82 · jul 203.310,40 · **ago 319.750,15**.
- **Melgarejo Distribuidores, 681,82 al 10 %** (julio) — única factura a un tercero identificado; es el **rappel/acuerdo comercial**, pero facturado al 10 % y contabilizado como venta (705), no como 759.
- **Gloria Durán SL, 165,29 al 21 %** (julio) — única venta al 21 % de todo el periodo.
- **No aparece nada de Fourvenues ni de Pepsi**, ni ninguna factura de rappel de bebida más allá de Melgarejo. Las entradas de puerta/Fourvenues están dentro del bloque de tickets al 10 % (o no están).

⚠ **Todo se factura al 10 %, incluidas las entradas de discoteca.** Sigue pendiente de confirmar con la gestoría (ver nota de `iva_rates`): si Hacienda considera la entrada un servicio al 21 %, hay contingencia.

---

## 4. Nóminas según la contabilidad

| | jun | jul | ago |
|---|---:|---:|---:|
| Bruto (640) | 0 | 21.060,10 | **27.423,23** |
| SS empresa (642) | 0 | 7.002,08 | **8.717,44** |
| **Coste empresa** | 0 | **28.062,18** | **36.140,67** |
| Líquido a pagar (465) | 0 | 19.319,67 | 24.348,11 |
| IRPF retenido (4751) | 0 | 388,81 | **547,50** |
| SS trabajador | 0 | 1.351,62 | 1.676,00 |
| Anticipos (460) | 0 | 0 | 851,62 |
| TC1 total (476, abono del mes) | 0 | 8.353,70 | 10.393,44 |
| SS pagada en el mes (476, cargo) | 0 | 0 | 8.387,32 (31/08, TGSS) |

Cuadre agosto: 24.348,11 líquido + 547,50 IRPF + 1.676,00 SS trabajador + 851,62 anticipos = **27.423,23 = bruto**. ✔

**Saldos a 31/08:**

| Cuenta | Saldo |
|---|---:|
| 465 Remuneraciones pendientes de pago | **−43.667,78** |
| 476 Organismos de la SS acreedores | **−10.359,82** |
| 4751 HP acreedora retenciones practicadas | **−3.037,45** (de los que 936,31 son IRPF de nómina y 2.101,14 de profesionales/arrendador) |
| 460 Anticipos de remuneraciones | −851,62 (saldo acreedor; debería ser deudor — revisar) |

⚠ **Las nóminas de julio y agosto no figuran como pagadas**: la 465 acumula los dos líquidos íntegros (19.319,67 + 24.348,11). En la realidad sí se pagaron; los pagos están sin aplicar (cuenta 555) o son pagos en efectivo no contabilizados.

---

## 5. Balances a 31/08/2026

### 5.a Deuda con proveedores (saldo acreedor, 400+410) — total **−102.074,87 €**

| Proveedor | Saldo |
|---|---:|
| AYCOA Distribuciones | −44.114,18 |
| Grupo Merino Vinos & Destilados | −19.564,43 |
| Coca-Cola Europacific | −5.710,47 |
| Chamán Spiritual Drinks | −4.766,19 |
| Melgarejo Distribuidores | −4.412,20 |
| Ignacio Lara Viguera (DJ) | −2.755,00 |
| Stipendium Asesores | −2.686,20 |
| Viento Creativo | −2.371,60 |
| Javier Quintero Alarcón | −2.045,86 |
| Ipasur Licores y Vinos | −1.862,56 |
| Henris Brand | −1.635,44 |
| Santander Factoring/Confirming | −1.191,43 |
| José María Carrión Evans (DJ) | −1.060,00 |
| Hielo Express Los Mellis | −1.045,20 |
| vidaXL | −747,89 |
| Ulivo Catering | −712,80 |
| Francisco Guzmán Sada | −700,00 |
| Leroy Merlin | −601,38 |
| Daniel Félix Alonso (DJ) | −530,00 |
| Fernando Chavarri (DJ) | −477,00 |
| Dilaso | −424,86 |
| Rubén Sanz Lanero (DJ) | −424,00 |
| Sonicolor Sevilla | −318,22 |
| Monbake | −299,57 |
| Sonlive Group | −242,00 |
| Sum. Industriales Bahía | −218,73 |
| Juan Fco. García Zajara (DJ) | −212,00 |
| Bazar Vinador | −154,75 |
| Restaurant Booking (CoverManager) | −147,74 |
| Master Gift | −130,40 |
| Resto (13 proveedores < 90 €) | −512,77 |

### 5.b ⚠ Proveedores con **saldo deudor** (pagos sin factura o pagos duplicados) — total **+166.426,54 €**

| Proveedor | Saldo deudor |
|---|---:|
| Mantec SY (Sánchez Yuste) | 49.439,15 |
| Lorente y Millán | 41.323,47 |
| eDistribución Redes Digitales | 22.253,70 |
| Viento Creativo | 18.173,51 |
| Stima 21 | 11.495,00 |
| Realmivo (arrendador) | 9.188,06 |
| BS Aislamientos | 8.145,50 |
| Innovación y Diseño para Hostelería | 3.576,53 |
| Laboratorios Cogesur | 1.633,50 |
| Palermo Legal | 907,50 |
| Resto | 290,62 |

Esto no es deuda a favor: es un **defecto de contabilización**. El patrón es claro — el mismo pago se registra dos veces: una en el asiento de la factura (contra la cuenta puente **572.1 «BANCOS»**) y otra al puntear el extracto real (contra **CAIXA** o **SANTANDER**). Por eso la cuenta 572.1 «BANCOS» tiene saldo **acreedor de −142.442,55 €**, que no existe. Hay que regularizar 572.1 contra estos saldos deudores.

### 5.c Socios y capital

| Cuenta | Saldo |
|---|---:|
| 551 Cuenta corriente con socios | **−165.650,00** (aportado: 71.400 en abril + 94.250 en mayo) |
| 100 Capital social | **−6.000,00** ⚠ debería ser 3.000: hay un saldo de apertura de 3.000 **y** un asiento de 3.000 el 01/01 |

No hay cuentas 553, 555 de socios ni 118 (aportaciones de socios). Todo el dinero de los socios está como **cuenta corriente (deuda a corto)**, no como fondos propios.

### 5.d Hacienda

| Cuenta | Saldo |
|---|---:|
| 470.1 HP deudor IVA [C] | +54.005,81 |
| 472.0 HP IVA soportado | +54.598,24 |
| 472.1 HP IVA soportado (antigua) | −860,32 |
| 475.0 HP acreedora (pago 303 de julio) | +9.420,95 (saldo **deudor**, anómalo) |
| 4751 HP acreedora retenciones | −3.037,45 |
| 476 Organismos SS acreedores | −10.359,82 |
| 477 HP IVA repercutido | −52.574,04 |

### 5.e Tesorería

| Cuenta | Saldo |
|---|---:|
| 572.2 CAIXA | **20.080,52** |
| 572.3 SANTANDER | **166.331,86** |
| 572.1 «BANCOS» (cuenta puente ficticia) | **−142.442,55** ⚠ |
| 570.1 Caja / euros | **−10.890,00** ⚠ saldo de caja negativo (un único apunte, 30/04, contrapartida del pago en efectivo de Viento Creativo fra. 181) |
| **Neto** | **33.079,83** |

CAIXA + SANTANDER = **186.412,38 €**, que es la foto real de bancos a 31/08.

### 5.f Clientes y existencias

- **430 Clientes (euros): +143.083,12 €.** Las facturas de tickets se cargan a clientes y solo se abonan con los **ingresos del TPV en Santander** (jun 2.313,48 · jul 145.032,55 · ago 286.702,27). El saldo pendiente es, básicamente, **el efectivo de barra que nunca se ha contabilizado**: la cuenta 570 Caja tiene un único apunte de todo el año (−10.890 el 30/04) y **cero movimientos operativos** desde la apertura.
- **430.1 Gloria Durán 200,00** y **430.2 Melgarejo 750,00** pendientes de cobro.
- **Existencias (300): no existe la cuenta.** No hay inventario inicial ni final ni variación de existencias (61x). Todas las compras van directas a resultado.

### 5.g Inmovilizado (grupo 2) — base amortizable

| Cuenta | Concepto | Saldo |
|---|---|---:|
| 219.2 | Reforma local discoteca | 135.213,29 |
| 215.1 | Aire acondicionado | 40.118,00 |
| 215.2 | Insonorización discoteca | 37.850,00 |
| 215.4 | Instalación fra. 21 Lorente y Millán | 26.729,79 |
| 215.7 | AYCOA F61 instalación sonido | 26.115,00 |
| 215.8 | 6ª certificación F28 Lorente | 19.586,22 |
| 215.5 | Fra. 23 Lorente y Millán | 14.680,18 |
| 215.9 | AYCOA F41 instalación sonido | 10.343,00 |
| 219.1 | Pioneer (cabina DJ) | 7.031,40 |
| 215.3 | Luces | 2.829,66 |
| 216.1 | Armario, fregadero, botellero | 1.963,81 |
| 216.2 | Mesa refrigerada | 992,00 |
| 215.6 | Mantenimiento instalaciones | 868,32 |
| 216.5 | Mobiliario metálico | 720,00 |
| **Total inmovilizado** | | **325.040,67** |

**Amortización acumulada (28x): 0. No hay ninguna dotación.** Nuestro modelo estima ~400.000 € de base amortizable y ~3.750 €/mes desde julio; la contabilidad va 325.041 € de base (faltan por activar Stima 21 ~10.850 y el cartel de Viento 1.960, que están en gasto) y **cero amortización**. Hay que pedirle a Stipendium el cuadro de amortización y los coeficientes.

---

## 6. Comparación con nuestro modelo (sin IVA, devengo)

### Julio 2026

| Fila | Modelo | Gestoría | Dif. | Explicación |
|---|---:|---:|---:|---|
| Ventas | 203.310 | **204.158** | +848 | Prácticamente clavado. El extra son el rappel de Melgarejo 681,82 y Gloria Durán 165,29, que nosotros no contamos como venta. |
| Compras | 44.495 | **47.643** | +3.148 | La gestoría no lleva existencias: todo lo comprado es gasto del mes. Nuestro modelo ajusta a consumo. |
| Personal | 33.645 | **28.062** | −5.583 | Cuadra al céntimo si se ajusta: 28.062 (bruto+SS empresa) **+ 8.523 extras en efectivo − 2.940 DJs por nómina = 33.645**. La gestoría solo ve lo declarado. |
| DJs | 7.650 | **700** | −6.950 | La gestoría solo tiene 2 facturas (Chavarri 450, D. Félix 250). Otros 2.940 están dentro del 640 (DJs en nómina) y ~4.010 se pagaron en efectivo sin factura. |
| Alquiler + comunidad | 2.537 | **0** | −2.537 | ⚠ **La gestoría no ha devengado el alquiler de julio ni el de agosto.** Solo tiene el pago de 4.594,02 del 03/08 como saldo deudor en Realmivo. Faltan 2 facturas de renta. |
| Fijos | 562 | **4.538** | +3.976 | Casi todo es **Stima 21 (3.750)**, que para nosotros es obra. Sin Stima: 788 vs 562. |
| Marketing | 500 | **500** | 0 | ✔ Barter Consultancy. |
| Varios | 464 | **765** | +301 | Reparaciones de Sonicolor, Leroy, etc. |
| Financiero | 490 | **681** | +191 | Incluye la **comisión de factoring duplicada** (299,14 en 626.1 por la factura + 299,14 en 626.0 por el cargo bancario). |

### Agosto 2026

| Fila | Modelo | Gestoría | Dif. | Explicación |
|---|---:|---:|---:|---|
| Ventas | 327.273 | **319.750** | −7.523 (−2,3 %) | Nosotros contamos los cierres del gerente (incluye efectivo); la gestoría, solo lo tickeado/facturado. Falta por facturar ~7.500 € de base (~8.275 con IVA). |
| Compras | 72.000 | **79.183** | +7.183 | Sin variación de existencias: en agosto se compró más de lo consumido (stock de cierre no reconocido). |
| Personal | 61.335 | **36.141** | −25.194 | La gestoría solo tiene la nómina oficial (bruto 27.423 + SS 8.717). Nuestro modelo añade los cierres en efectivo (~43.435 en el mes), vacaciones estimadas y la SS real. **Es la diferencia más grande y la más importante de aclarar.** |
| DJs | 5.980 | **4.950** | −1.030 | Faltan facturas por ~1.030 € (o se pagaron en efectivo). |
| RRPP | 10.742 | **0** | −10.742 | ⚠ **No hay ni una sola factura de RRPP en la contabilidad.** Todo se pagó en efectivo sin soporte. |
| Alquiler + comunidad | 2.537 | **0** | −2.537 | Igual que julio: sin devengar. |
| Fijos | 2.040 | **10.168** | +8.128 | **Stima 21 7.100** (obra en nuestro modelo) + **Stipendium 2.220**. Sin Stima: 3.068. |
| Marketing | 500 | **1.352** | +852 | La gestoría metió los **uniformes Henris (1.351,60)** en marketing; nosotros los llevamos a equipo y varios y contamos 500 de marketing que la gestoría no tiene. |
| Varios | 6.531 | **2.082** | −4.449 | La gestoría solo tiene el cartel de Viento (1.960, que además es obra) y CoverManager. Las comidas del equipo, taxis y el ordenador de Tipsi no están. |
| Financiero | 307 | **109** | −198 | — |

### Resumen

| | Modelo (nuestro) | Gestoría | Dif. |
|---|---:|---:|---:|
| Resultado julio | 112.967 | **121.269** | +8.302 |
| Resultado agosto | 165.301 | **185.765** | +20.464 |

La gestoría da **más beneficio** porque le faltan los costes pagados en efectivo (personal extra, RRPP, DJs, comidas), el alquiler, y la amortización; y le sobra lo que debería ir a inmovilizado (Stima, cartel). **Nuestro modelo es el bueno para gestionar; el suyo, el fiscal.**

---

## 7. Dudas y anomalías (por orden de importancia)

1. **IVA de agosto 3.374,73 no reproducible.** Mis dos cálculos son 1.175,41 (mayor) y 4.357,08 (registros). Pedir el PDF del 303 de agosto.
2. **El libro registro de recibidas está incompleto frente al mayor**: le faltan 3.185,07 € de IVA soportado en agosto y 1.604,50 € en julio, sobre todo de **Melgarejo**. Si el 303 se hace con el registro, **estamos pagando IVA de más**. Es lo primero que hay que cruzar con Stipendium.
3. **No se está usando el crédito de IVA de la preapertura (470 = 54.005,81 €).** Se pagaron 9.420,95 € el 20/08 teniendo ese saldo a favor. ¿Se pidió devolución? ¿En qué estado está?
4. **No hay asientos de liquidación de IVA** (477 nunca se salda contra 472), y la 475 queda con saldo deudor de 9.420,95.
5. **No se devenga el alquiler desde julio** (faltan 2 facturas de Realmivo, ~4.504 € de base). Ni la comunidad.
6. **Cuenta puente 572.1 «BANCOS» con −142.442,55 €** y 166.426,54 € de saldos deudores en proveedores: **pagos duplicados de la obra** (Lorente, Mantec, eDistribución, Viento, BS, Stima). Hay que regularizarlo o el balance no vale.
7. **Caja (570) sin un solo movimiento operativo** (único apunte: −10.890 el 30/04) **y clientes en +143.083 €**: el efectivo de barra no está contabilizado. Es el mismo agujero por los dos lados.
8. **Cero amortización y cero existencias.** Sin 68x, sin 28x, sin 300, sin 61x. El resultado de jun–ago (+290.303) está inflado por ambas cosas.
9. **Capital social contabilizado por 6.000 € en vez de 3.000.**
10. **Stima 21 (10.850 jul+ago) y el cartel de Viento Creativo (1.960) van a gasto** cuando son inmovilizado. Afecta al P&L y a la base amortizable.
11. **Comisión de factoring duplicada** (626.0 y 626.1): 892,29 en junio + 299,14 en julio = 1.191,43 € de gasto contado dos veces. El proveedor «Santander Factoring» queda con −1.191,43 sin pagar.
12. **El diario exportado está truncado**: el último asiento (1272, 31/08) no tiene las líneas de 640 y 642, y el propio total del fichero descuadra en 123,18 €. El mayor sí está completo. Pedir el diario bien exportado.
13. **Todo se factura al 10 %**, entradas incluidas. Contingencia a confirmar con la gestoría.
14. **460 Anticipos de remuneraciones con saldo acreedor** (−851,62) — signo raro.
15. **Las nóminas de julio y agosto figuran como no pagadas** (465 = −43.667,78).
16. **Nada de Fourvenues ni de Pepsi** en las emitidas. ¿Las entradas de Fourvenues están dentro de los tickets de Tipsi (desde el 07/07) o faltan? ¿El rappel de Pepsi/Coca-Cola no se ha facturado todavía?
17. **El registro de recibidas de este envío solo cubre jul–ago** (el encabezado dice «De 01 Jul a 31 Ago»), pese al nombre del fichero. Falta el de junio para cerrar el trimestre.
