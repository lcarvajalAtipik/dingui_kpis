// ===================================================================================
//  DINGUI MES A MES — modelo de resultado (P&L, sin IVA) y caja (liquidez, con IVA)
//  Enero 2026 → diciembre 2027. Cada celda es la SUMA de componentes etiquetados
//  (label, importe, fuente) para poder explicar de dónde sale cada número.
//  Convenciones:
//    · Liquidez = bancos (CaixaBank + Santander) + plazo fijo Santander + saldo Fourvenues.
//      Los traspasos entre esas tres bolsas NO son flujo (incl. imposiciones a plazo y retiradas FV).
//    · Enero–agosto 2026 = real (banco). Agosto llega hasta el 27/08; el tramo 28/08→16/09 real
//      está en septiembre. Desde el 17/09 es proyección (extractos al 16/09, v4 17/09/2026).
//    · P&L: criterio 28/08 → lo anterior al 01/07/2026 es coste de proyecto (fuera del P&L), salvo el
//      alquiler, la comunidad y los fijos del local, que se devengan desde enero/febrero (petición del usuario 17/09).
//      Las ventas y compras arrancan en julio de 2026.
//    · 2027 repite 2026 (temporada julio–agosto) con parámetros.
// ===================================================================================

const MES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
const MESN = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
const N = 24;
const COLS = [];
for (let i = 0; i < N; i++){ const y = 2026 + Math.floor(i/12), m = i % 12; COLS.push({y, m, label: MES[m] + " " + String(y).slice(2), real: i <= 7, mixto: i === 8}); }
const idx = (y, m) => (y - 2026)*12 + m;

// ---------------------------------------------------------------- filas
// [etiqueta, clave, clase css, fuente genérica]
const FILAS_PL = [
  ["Ventas (barra, puerta y Fourvenues)","ventas","","Julio: cierres diarios del gerente (total caja de cada noche) ÷ 1,10, que coincide con lo facturado en Tipsi según la contabilidad. Agosto: lo facturado según la contabilidad de la gestoría (149 facturas resumen de tickets al 10 %). Los cierres de agosto están completos solo hasta el 26."],
  ["Acuerdos comerciales","acuerdos","","Pepsi: 17.000 € + IVA, cobro en octubre de 2026 (dato del usuario 07/09)."],
  ["Compras de bebida y comida","cogs","","Compras contabilizadas por la gestoría (cuentas 600 y 602) por fecha de factura. No hay inventario ni variación de existencias: lo comprado y no consumido (stock al cierre de agosto) está dentro. Las devoluciones de compras restan aquí (Melgarejo, fin de temporada, septiembre)."],
  ["Rappels de marcas","rappels","","Cuenta propia (decisión del usuario 17/09). Pernod Ricard: 6.200 € + IVA de la temporada 2026 (cobro en octubre), repartidos entre julio y agosto según las botellas de licor consumidas (1.602 / 2.394). Cruzcampo agosto 401,50 € (Melgarejo RU1113). Melgarejo julio 681,82 € (facturado)."],
  ["Margen bruto","margen","rule",""],
  ["Personal (nóminas, extras, IRPF y Seguridad Social)","personal","","Estructura oficial del coste de personal (07/08): nóminas líquidas + horas extra en efectivo + IRPF + Seguridad Social, menos los DJs que cobran por nómina (van en la fila de DJs). Nómina y Seguridad Social reales de Stipendium (contabilidad); el efectivo, de los cierres del gerente; vacaciones al cierre estimadas."],
  ["DJs","djs","","Caché total del mes según el calendario de DJs (columna Presu.): julio 7.650 €, agosto 5.980 €."],
  ["Relaciones públicas","rrpp","","Pago RRPP de la temporada: 15.172,87 € con IVA a Security («Comunicación eventos», 14/09), base 12.539,56 €; se imputa a agosto."],
  ["Alquiler y comunidad","alquiler","","Facturas de Realmivo: renta 1.700 € + comunidad del centro comercial (198,36 €/mes hasta julio, 216,68 € desde agosto), todo en la misma factura, sin IVA en el resultado. La comunidad no se paga aparte. Renta desde febrero de 2026 (carencia hasta enero). Se devenga cada mes aunque el banco lo pague con retraso (junio y julio se pagaron el 03/08; agosto y septiembre el 11/09)."],
  ["Gestoría, seguros, alarma, telecom y software","fijos","","Enero–junio: lo pagado por banco (gestoría Remesa/Stipendium, GoDaddy, DocuSign, Trimble, Apple, Google, Adobe) ÷ 1,21. Julio y agosto: contabilidad de la gestoría (cuentas 623, 625, 628, 629) sin Stima 21, que es obra; agosto incluye 2.220 € de Stipendium. Desde septiembre: gestoría 120 + seguros, alarma y telecom ~250 €/mes."],
  ["Marketing","marketing","","Barter Consultancy 605 €/mes con IVA (500 € base), junio–agosto. Foto y vídeo (Juan Máximo 1.000, Evans 1.000) y gestión comercial de Álvaro Pastor (3.000), facturados en septiembre y repartidos por fecha de servicio."],
  ["Gastos de equipo y varios","extra","","Comidas del equipo, taxis, uniformes (Henris 1.635 €), ordenador Tipsi, farmacia… Sin IVA (÷1,21)."],
  ["Gastos financieros","financiero","","Comisiones bancarias y del TPV, comisión e intereses del confirming (302,50 + 892,29 + 299,14 €). Las imposiciones a plazo NO son gasto."],
  ["Resultado antes de amortización e impuestos","ebitda","rule",""],
  ["Amortización","amort","","Activo amortizable ≈ 394.600 € sin IVA: inmovilizado de la contabilidad 325.041 + lo que falta activar (Stima 22.100, Viento con factura ~28.150, tasas de licencia 8.250, sonido menor ~6.300, equipamiento ~2.500, conexiones y pruebas ~2.300). Contrato de alquiler de 10 años → lineal al 10 %: ~39.500 €/año desde julio de 2026 (3.292 €/mes). El máximo fiscal sería ~44.700 (sonido al 20 %) y con amortización acelerada de empresa reducida el doble."],
  ["Resultado antes de impuestos","resultado","rule total",""],
  ["Impuesto de sociedades","is","","Tipo del 15 % (empresa de nueva creación, también en 2027) sobre el resultado del año. La gestoría puede bajarlo con amortización acelerada (art. 103 LIS) y libertad de amortización por creación de empleo (art. 102): cambia el tipo efectivo en los supuestos."],
  ["Resultado neto","neto","rule total",""],
  ["Inversión del proyecto pagada en el mes (con IVA, fuera del P&L)","proyecto","memo","Suma de las filas de proyecto de la tabla de caja: obra, instalaciones, arquitecto, licencias, equipamiento y confirming. Coste total del proyecto: 532.415,12 € (cerrado el 28/08 en 532.297,62 y actualizado el 17/09 con Stima)."]
];
const FILAS_CAJA = [
  ["Aportaciones de socios","in_aportaciones","","Transferencias entrantes de los socios (cap table: 322.000 € comprometidos; banco real ≈ 313.700 €)."],
  ["Cobros del TPV","in_tpv","","Liquidaciones del datáfono Santander, netas de comisión. Las ventas en efectivo no pasan por el banco: pagan al personal y las promos."],
  ["Ventas por Fourvenues","in_fv","","Entradas anticipadas vendidas en Fourvenues. El saldo de Fourvenues cuenta como liquidez (decisión 27/08: retirable a demanda). Las retiradas a CaixaBank son traspasos internos."],
  ["Préstamos (socios y Cruzcampo)","in_prestamos","","Préstamo de socios: 14.000 € entrados (4.000 + 5.000 el 07/06, 3.000 el 08/06 y 2.000 el 27/06) y 12.000 devueltos (5.000 el 20/07, 3.000 + 4.000 el 05/08): quedan 2.000 € por devolver. Cruzcampo: 30.000 € en septiembre de 2026 y 10.000 € en enero de 2027; se amortiza con pedidos de cerveza, sin cuotas; aval de 6.000 € en el plazo fijo."],
  ["Devoluciones de IVA","in_redeme","","REDEME (devolución mensual). IVA de preapertura: 40.059,78 € (31/07) + 13.946,03 € (21/08) = 54.005,81 €, igual que la cuenta 470 de la contabilidad. Junio: 11.095,82 € pedidos el 18/07, sin cobrar a 16/09 (supuesto octubre). Septiembre sale a devolver (~5.300 €, cobro en noviembre); octubre con Pepsi sale a pagar."],
  ["Acuerdos comerciales","in_acuerdos","","Pepsi 17.000 € + IVA = 20.570 € y rappel de Pernod Ricard 6.200 € + IVA = 7.502 €, ambos en octubre de 2026. Melgarejo: rappel de Cruzcampo de agosto 485,82 € y aportación comercial 484 € (septiembre)."],
  ["Otros ingresos y por identificar","in_otros","","Abonos sin pareja (ingresos en efectivo de Ybarra 2.850 + 500, 2.100 y 1.750 del 20/08), devoluciones de proveedores y el residuo hasta cuadrar con el saldo real del banco."],
  ["Ingresos","ingresos","rule",""],
  ["Obra: Lorente y Millán","proj_lorente","","Constructora, 6 certificaciones = 237.413,48 €. Cuenta cerrada el 12/08. La certificación 04 (32.343,05 €) se pagó por confirming (ver fila Confirming)."],
  ["Obra: Viento Creativo","proj_viento","","Tematización (presupuesto 31.600,38 €), cartel de fachada 2.371,60 € y cartas. Estado de cuentas del proveedor del 02/09: pendiente 10.148,80 + IVA = 12.280,05 €."],
  ["Clima: Sánchez Yuste","proj_yuste","","Ventilación y climatización (alias bancario Mantec), 4 facturas = 50.486,19 €. Cerrada."],
  ["Insonorización: BS Aislamientos","proj_bs","","Factura OB-113 de 45.798,50 €: 33.145,50 € por cuenta y 12.653 € por confirming (cargo en septiembre)."],
  ["Sonido e iluminación: Aycoa","proj_aycoa","","Facturas 41 + 61 = 44.114,18 €. Pagada entera: 25.000 € hasta agosto + 9.000 (07/09) + 10.114,18 (08/09). Cerrada."],
  ["Cabina DJ y sonido menor","proj_cabina","","Profesional DJ 8.582,50 € (concepto bancario UME), Thomann, Betopper, Madrid Hifi, Wolfmix, Sonicolor."],
  ["Arquitecto: Stima 21","proj_stima","","Presupuesto 26.350 € + IVA. Pagados por banco 24.623,50 €. Pendiente: factura extra T32670 (2.117,50 €) y 4.000 € en efectivo sin IVA este año."],
  ["Licencias, tasas y legal","proj_licencias","","Tasas del ayuntamiento 8.251,54 €, notaría (provisión 2.100 el 19/02, devueltos 524,15 el 09/04), Palermo Legal, Registro Mercantil. Pendiente: 10.000 € de licencia para la DR."],
  ["Equipamiento y mobiliario","proj_equip","","ID Hostelería, cerrajería, neveras y mesa refrigerada, vidaXL, bazares, ferretería, ordenador Tipsi."],
  ["Otros del proyecto","proj_otros","","Alta de Tipsi, Cogesur (pruebas de carga), Edistribución (conexión), pequeños."],
  ["Confirming Santander","proj_confirming","","Santander Factoring. 03/09: 5.000 € de la factura 23 de Lorente (según el detalle de Santander). Pendiente según el usuario (17/09): 44.999,05 € (Lorente C04 32.343,05 + BS 12.653). Sin calendario de vencimientos."],
  ["Compras de bebida y comida","op_cogs","","Merino, Melgarejo, Makro, Picking Gades, Coca-Cola, hielo, La Encina, Dilaso, Chamán… Pagos por banco (transferencias a cuenta y recibos)."],
  ["Personal: efectivo y nóminas","op_personal","","Disposiciones de efectivo en ventanilla Santander para pagar nóminas y extras (el personal cobra en efectivo), formación y vacaciones. El grueso del personal se paga con las ventas en efectivo, que no pasan por el banco."],
  ["Seguridad Social (TC1)","op_ss","","Cargo de la TGSS a fin del mes siguiente: julio 8.387 € (31/08), agosto 10.393,44 € (fin de septiembre)."],
  ["IRPF (modelo 111)","op_irpf","","Retenciones trimestrales: 3T en octubre (~1.200 €), 4T en enero."],
  ["DJs pagados por banco","op_djs","","Transferencias a DJs desde agosto (agosto 1.873; pagos de agosto en septiembre 5.957 + 8.718). El calendario de DJs recoge todo el coste (sin IVA)."],
  ["Relaciones públicas","op_rrpp","","Pago RRPP a Security de 15.172,87 € el 14/09/2026."],
  ["Alquiler y comunidad","op_alquiler","","Realmivo 2.297,02 €/mes; fianza y garantía 13.600 € (septiembre de 2025); comunidad 720,05 € (febrero). En septiembre de 2026 se pagan agosto y septiembre."],
  ["Gestoría, seguros, alarma, telecom y software","op_fijos","","Stipendium / Remesa Asesores, Mapfre, Prosegur, O2, GoDaddy, DocuSign, Trimble, Apple, Google, Adobe, CoverManager. Cierre: ~395 €/mes."],
  ["Marketing","op_marketing","","Barter 605 €/mes (junio–agosto), Otherview, BA visuals, Gráficas Pedraza."],
  ["Gastos de equipo y varios","op_extra","","Comidas del equipo, taxis, uniformes, farmacia, varios."],
  ["Puesta a punto reapertura 2027","op_preapertura","","Sin cifrar por el usuario (regla 30/08: no asumir importes). Por defecto 0; cámbialo en los supuestos."],
  ["Comisiones e intereses","fin_comisiones","","Comisiones de cuenta y TPV, comisión e intereses del confirming. Las imposiciones a plazo (6.000 € desde el 20/07) son un traspaso dentro de la liquidez, no un gasto."],
  ["IVA (modelo 303)","tax_iva","","REDEME mensual: se paga o se devuelve cada mes. Julio 9.420,95 € (20/08), agosto 3.374,73 € (pagado el 14/09), octubre 3.170 € por Pepsi (20/11)."],
  ["Impuesto de sociedades","tax_is","","IS 2026 (modelo 200) se paga del 1 al 25 de julio de 2027. Pagos a cuenta (modelo 202): 18 % de la cuota de 2026 en octubre y diciembre de 2027. En 2026 los 202 son cero (cuota 2025 = 0)."],
  ["Gastos","gastos","rule",""],
  ["Neto del mes","neto",""," "],
  ["Liquidez a fin de mes","saldo","rule total","Bancos + plazo fijo + Fourvenues. Enero–agosto 2026: saldos reales de los extractos."]
];
const IN_KEYS = ["in_aportaciones","in_tpv","in_fv","in_prestamos","in_redeme","in_acuerdos","in_otros"];
const PROJ_KEYS = ["proj_lorente","proj_viento","proj_yuste","proj_bs","proj_aycoa","proj_cabina","proj_stima","proj_licencias","proj_equip","proj_otros","proj_confirming"];
const OP_KEYS = ["op_cogs","op_personal","op_ss","op_irpf","op_djs","op_rrpp","op_alquiler","op_fijos","op_marketing","op_extra","op_preapertura","fin_comisiones","tax_iva","tax_is"];
const OUT_KEYS = PROJ_KEYS.concat(OP_KEYS);
const PL_KEYS = ["ventas","acuerdos","cogs","rappels","personal","djs","rrpp","alquiler","fijos","marketing","extra","financiero","amort","is"];

// ---------------------------------------------------------------- supuestos
const P = {
  ventas27: 100,      // % de las ventas de 2026 (julio y agosto)
  jun27: 0,           // ventas de junio de 2027, € con IVA; costes y cobros con la estructura de julio
  cogs27: 24.2,       // % de ventas (2026 según contabilidad, sin ajuste de existencias)
  personal27: 18.6,   // % de ventas (2026 con TC1 real de agosto)
  djs27: 2.6,         // % de ventas (2026: 13.630 / 530.583)
  rrpp27: 15172.87,   // € con IVA, septiembre (2026: Security 15.172,87)
  pepsi27: 17000,     // € sin IVA, octubre
  rappel27: 6200,     // € sin IVA, rappel Pernod Ricard temporada 2027, cobro en octubre (2026: 6.200)
  preap27: 0,         // € con IVA, junio: stock, puesta a punto, marketing…
  vac27: 5000,        // € vacaciones no disfrutadas al suspender, septiembre
  is: 15,             // % tipo efectivo del impuesto de sociedades
  ivaAgo26: 3374.73,  // € IVA de agosto de 2026 según la gestoría (modelo 303, pago 20/09)
  amortAnual: 39500   // € amortización anual: lineal a 10 años (contrato de alquiler) sobre ~394.600 € sin IVA
};
const GRUPOS = [
  ["Temporada 2027", [
    ["ventas27","Ventas de julio y agosto sobre 2026","%",5,"2026: jul 223.641 · ago 351.725 con IVA (facturado)"],
    ["jun27","Ventas de junio 2027","€ con IVA",5000,"2026: apertura el 19/06, 2.313 € por TPV. Compras, personal, DJs y cobros con la estructura de julio"],
    ["cogs27","Compras de producto","% ventas",0.5,"2026 (contabilidad, sin existencias): jul 23,4 · ago 24,8"],
    ["personal27","Personal (con IRPF y SS)","% ventas",0.5,"2026: jul 16,5 · ago 19,9"],
    ["djs27","DJs","% ventas",0.1,"2026: 2,6"],
    ["rrpp27","Relaciones públicas","€ con IVA",500,"2026: 15.172,87 (Security)"],
    ["preap27","Puesta a punto en junio","€ con IVA",1000,"Sin cifrar: stock, limpieza, marketing…"],
    ["vac27","Vacaciones al cierre","€",500,"2026: pagadas con los finiquitos de agosto"]
  ]],
  ["Acuerdos e impuestos", [
    ["pepsi27","Pepsi 2027","€ sin IVA",1000,"2026: 17.000 en octubre"],
    ["rappel27","Rappel Pernod Ricard 2027","€ sin IVA",500,"2026: 6.200 + IVA, cobro en octubre"],
    ["is","Impuesto de sociedades, tipo efectivo","%",1,"15 % nueva creación; 0 si la gestoría aplica libertad de amortización"],
    ["ivaAgo26","IVA de agosto 2026","€",500,"Modelo 303 pagado el 14/09 (real)"],
    ["amortAnual","Amortización anual","€",1000,"Lineal a 10 años (contrato de 10 años) sobre ~394.600 € sin IVA; máximo fiscal ~44.700 (sonido al 20 %)"]
  ]]
];

// ---------------------------------------------------------------- datos reales
// Ventas con IVA de los cierres del gerente
const VENTAS_IVA = {jul: 223641, ago: 351725};   // julio: cierres del gerente; agosto: facturado según la contabilidad (319.750,15 base)
const REAL_PL = {   // sin IVA, julio y agosto de 2026
  jul: {
    ventas: [["Cierres del gerente, 26 noches: 223.641 € con IVA ÷ 1,10 (= 203.310 facturado en Tipsi según la contabilidad)", 203310.40],["Venta a Gloria Durán SL (al 21 %)", 165.29]],
    rappels: [["Pernod Ricard: 6.200 € × 1.602 / 3.996 botellas de licor consumidas (julio / temporada)", 6200*1602/3996],["Melgarejo, rappel facturado en julio (la gestoría lo contabilizó como venta al 10 %)", 681.82]],
    cogs: [["Compras contabilizadas por la gestoría (600 mercaderías 45.769 + 602 otros aprovisionamientos 1.874), sin ajuste de existencias", -47642.51]],
    personal: [["Nóminas líquidas (Stipendium, 30 personas)", -19319.67],["Horas extra pagadas en efectivo", -8523.03],["IRPF retenido", -388.81],["Seguridad Social (TC1 julio)", -8353.70],["DJs que cobran por nómina, van en DJs", 2940]],
    djs: [["Caché del calendario de DJs", -7650]],
    alquiler: [["Renta de julio (factura 68/26)", -1700],["Comunidad del centro comercial (en la misma factura)", -198.36]],
    fijos: [["Contabilidad: Mapfre 746,17, Telefónica, Google, farmacia (sin Stima 21, que es obra)", -788.17]],
    marketing: [["Barter Consultancy", -500],["Juan Máximo, foto y vídeo 10 y 14/07 (factura 51-2026, 200 €/día)", -400],["Evans, sesión de fotos 24/07 (factura 2334, 200 €/sesión)", -200]],
    extra: [["Contabilidad: Sonicolor 263, Suministros Bahía 181, Leroy 96, CoverManager 73, Viento (cartas) 73, Plato al Centro 34, ferreterías", -764.78]],
    financiero: [["Intereses confirming 8/7", -299.14],["Comisiones bancarias y TPV", -191]]
  },
  ago: {
    ventas: [["Facturado en Tipsi según la contabilidad: 149 facturas resumen de tickets, base al 10 % (351.725 € con IVA). Los cierres del gerante del 1 al 26 suman 298.761 € de base; el resto son las últimas noches", 319750.15]],
    cogs: [["Compras contabilizadas por la gestoría (600 mercaderías 74.718 + 602 otros 4.465), sin ajuste de existencias: incluye el stock que quedó al cerrar", -79182.84]],
    personal: [["Gasto de personal de los cierres 1–26 (efectivo)", -43435],["Noches 27–29 (estimado)", -4100],["Seguridad Social, TC1 de agosto real (empresa 8.717,44 + trabajador 1.676,00)", -10393.44],["IRPF retenido en nómina (real)", -547.50],["Vacaciones no disfrutadas al suspender (estimado, pendiente gestoría)", -5000]],
    djs: [["Caché del calendario de DJs", -5980]],
    rappels: [["Pernod Ricard: 6.200 € × 2.394 / 3.996 botellas de licor consumidas (agosto estimado: Tipsi hasta el 24/08 escalado)", 6200*2394/3996],["Cruzcampo, rappel de agosto (Melgarejo RU1113: 300 barriles + 92 tercios…)", 401.50]],
    rrpp: [["Pago RRPP a Security 15.172,87 € con IVA ÷ 1,21 (14/09)", -15172.87/1.21]],
    alquiler: [["Renta de agosto (factura pendiente de recibir)", -1700],["Comunidad del centro comercial (en la misma factura)", -216.68]],
    fijos: [["Contabilidad: Stipendium 2.220 (laboral), Mapfre y Multiservicios 519, Tipsi 70, Telefónica, Google, Future is an Attitude, farmacia (sin Stima 21, que es obra)", -3068.19]],
    marketing: [["Barter (605 € con IVA)", -500],["Juan Máximo, foto y vídeo 01, 02 y 29/08 (factura 51-2026)", -600],["Evans, sesiones 14, 21 y 22/08 doble (factura 2334)", -800],["Álvaro Pastor, gestión comercial, captación, publicidad y marketing (factura 07/09, sin periodo: imputada a agosto)", -3000]],
    extra: [["Comidas del equipo y taxis de agosto (2.070 € con IVA)", -2070/1.21],["Comidas, taxis y varios pagados del 28/08 al 07/09 (3.587 € con IVA)", -3587/1.21],["Uniformes Henris (1.635 € con IVA)", -1635/1.21],["Ordenador Tipsi (610 € con IVA)", -610/1.21],["CoverManager (contabilidad)", -122.10]],
    financiero: [["Comisiones bancarias y TPV", -307]]
  }
};
// Liquidez real a fin de mes (bancos + plazo + Fourvenues), extractos validados
const LIQ_REAL = {0: 7300, 1: 110722, 2: 36156, 3: 49000, 4: 13172, 5: 4564, 6: 128478, 7: 267557};
const LIQ_DIC25 = 7330;   // saldo CaixaBank a 31/12/2025
const FV_REAL = {5: 0, 6: 42525, 7: 83700};   // saldo Fourvenues = acumulado de los cierres (jul 42.525 + ago 39.750 hasta el 26 + últimas noches) ≈ 83.700 visto el 28/08

// Caja real enero–junio 2026 por fila (banco; lo rellena la reconstrucción de los extractos)
// Formato: {i: {fila: [[label, importe], ...]}}
const REAL_CAJA = {
  0: {
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", -30.0]]
  },
  1: {
    in_aportaciones: [["03/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 4800.0], ["03/02 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 6400.0], ["04/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 2500.0], ["04/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 6400.0], ["04/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 16000.0], ["05/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 2300.0], ["05/02 · TRANSFER INMEDIATA — aportacion de socios (sheet Tipo=Aportaciones)", 8000.0], ["05/02 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 9600.0], ["05/02 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 9600.0], ["07/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 6400.0], ["07/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 6400.0], ["07/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 9600.0], ["12/02 · TRANSFER INMEDIATA — aportacion de socios (sheet Tipo=Aportaciones)", 6050.0], ["12/02 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 30000.0], ["13/02 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 11600.0], ["Resto de movimientos menores de 1.000 €", 788.53]],
    proj_yuste: [["27/02 · PAGO TRANSFERENCIAS — Sanchez Yuste / Mantec - climatizacion", -24271.39]],
    proj_licencias: [["19/02 · 209-2026Nuevo Vh — notaria (escritura 209-2026)", -2100.0], ["Resto de movimientos menores de 1.000 €", -1592.75]],
    proj_otros: [["26/02 · factura 277 — Cogesur pruebas de carga (1.633,50 total = 326,70 'tecnico' + 1.306,80 'factura 277')", -1306.8], ["Resto de movimientos menores de 1.000 €", -476.7]],
    op_alquiler: [["12/02 · alquiler febrero — Realmivo - renta/comunidad/fianza del local", -2297.02], ["Resto de movimientos menores de 1.000 €", -720.05]],
    op_fijos: [["Movimientos del extracto (todos menores de 1.000 €)", -115.85]],
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", -136.03]]
  },
  2: {
    proj_lorente: [["06/03 · PAGO TRANSFERENCIAS — Lorente y Millan - obra (sheet Tipo=Obra)", -54935.38]],
    proj_cabina: [["12/03 · UME — Profesional DJ (mal rotulado 'UME' en banco) - cabina DJ, pedido 98063", -8582.5]],
    proj_stima: [["13/03 · honorarios proyec — Stima 21 - arquitectura/ingenieria", -8470.0]],
    proj_otros: [["Movimientos del extracto (todos menores de 1.000 €)", -12.99]],
    op_alquiler: [["18/03 · REALMIVO SL. — Realmivo - renta/comunidad/fianza del local", -2297.02]],
    op_fijos: [["Movimientos del extracto (todos menores de 1.000 €)", -130.98]],
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", -137.34]]
  },
  3: {
    in_aportaciones: [["22/04 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 7200.0], ["29/04 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 4800.0], ["29/04 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 6000.0], ["29/04 · TRANSFER INMEDIATA — aportacion de socios (sheet Tipo=Aportaciones)", 9000.0], ["29/04 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 14400.0], ["30/04 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 3600.0], ["30/04 · TRASPASO — aportacion de socios (sheet Tipo=Aportaciones)", 9600.0], ["30/04 · TRANSF. A SU FAVOR — aportacion de socios (sheet Tipo=Aportaciones)", 9600.0]],
    proj_viento: [["30/04 · acopio material — Viento Creativo - rotulacion/tematizacion (factura 181)", -10890.0]],
    proj_bs: [["30/04 · parte 1 facrura — BS Aislamientos - insonorizacion", -20000.0]],
    proj_cabina: [["30/04 · THOMANN DE — equipo de sonido/cabina DJ", -4361.2]],
    proj_stima: [["17/04 · redaccion proyect — Stima 21 - arquitectura/ingenieria", -3025.0]],
    proj_licencias: [["17/04 · TRIBUTOS — tasas/tributos ayuntamiento (licencia de apertura / ICIO)", -4935.99], ["17/04 · TRIBUTOS — tasas/tributos ayuntamiento (licencia de apertura / ICIO)", -1885.1], ["17/04 · TRIBUTOS — tasas/tributos ayuntamiento (licencia de apertura / ICIO)", -1240.2]],
    proj_equip: [["Movimientos del extracto (todos menores de 1.000 €)", -542.71]],
    proj_otros: [["30/04 · CNX 0001176170 — Edistribucion CNX (acometida electrica); uno de los dos cargos fue devuelto el 01/05", -1126.85], ["30/04 · CNX 0001176170 — Edistribucion CNX (acometida electrica); uno de los dos cargos fue devuelto el 01/05", -1126.85]],
    op_alquiler: [["08/04 · REALMIVO SL. — Realmivo - renta/comunidad/fianza del local", -2297.02]],
    op_fijos: [["Movimientos del extracto (todos menores de 1.000 €)", -120.96]],
    op_marketing: [["Movimientos del extracto (todos menores de 1.000 €)", -342.0]],
    op_extra: [["Movimientos del extracto (todos menores de 1.000 €)", -201.72]],
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", 0.0]],
    proj_cabina: [["16/04 · UME — devolución de equipamiento de música DJ (usuario 17/09)", 189.99]],
    proj_licencias: [["09/04 · TRANSF. A SU FAVOR — devolución de la notaría (usuario 17/09)", 524.15]]
  },
  4: {
    in_aportaciones: [["03/05 · TRASPASO — transferencia entrante sin pareja interna -> aportacion de socios", 9600.0], ["05/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 8000.0], ["08/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 9600.0], ["08/05 · TRANSFER INMEDIATA — transferencia entrante sin pareja interna -> aportacion de socios", 10000.0], ["09/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 12000.0], ["22/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 14900.0], ["26/05 · TRASPASO — transferencia entrante sin pareja interna -> aportacion de socios", 3600.0], ["26/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 15000.0], ["28/05 · TRANSF. A SU FAVOR — transferencia entrante sin pareja interna -> aportacion de socios", 5000.0]],
    proj_lorente: [["01/05 · PAGO TRANSFERENCIAS — Lorente y Millan - obra (sheet Tipo=Obra)", -36494.16], ["20/05 · PAGO TRANSFERENCIAS — Lorente y Millan - obra (sheet Tipo=Obra)", -40000.0], ["22/05 · parte 2 certifica — certificacion de obra Lorente y Millan", -12000.0], ["26/05 · parte 3 certifica — certificacion de obra Lorente y Millan", -10000.0], ["28/05 · ultima parte cert — certificacion de obra Lorente y Millan", -10178.54]],
    proj_bs: [["08/05 · 2 parte factura — BS Aislamientos - insonorizacion", -5000.0]],
    proj_cabina: [["06/05 · betopperdj — equipo de sonido/cabina DJ", -2923.45], ["Resto de movimientos menores de 1.000 €", -366.05]],
    proj_equip: [["15/05 · mesa refrigerada — equipamiento / mobiliario del local", -1200.32], ["27/05 · neveras — equipamiento / mobiliario del local", -2376.21]],
    proj_otros: [["01/05 · TRANSF. A SU FAVOR — devolucion cargo duplicado CNX Edistribucion (netea uno de los dos -1.126,85 del 30/04)", 1126.85], ["28/05 · software — alta Tipsi (software PoS)", -1149.33]],
    op_alquiler: [["07/05 · REALMIVO SL. — Realmivo - renta/comunidad/fianza del local", -2297.02]],
    op_fijos: [["Movimientos del extracto (todos menores de 1.000 €)", -216.7]],
    op_marketing: [["Movimientos del extracto (todos menores de 1.000 €)", -233.59]],
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", -193.65]]
  },
  5: {
    in_tpv: [["Movimientos del extracto (todos menores de 1.000 €)", 2313.48]],
    in_prestamos: [["07/06 · TRANSFER INMEDIATA — prestamo de socios entrante (override usuario)", 4000.0], ["07/06 · TRANSFER INMEDIATA — prestamo de socios entrante (override usuario)", 5000.0], ["08/06 · TRASPASO — prestamo de socios entrante (override usuario)", 3000.0], ["27/06 · TRASPASO — préstamo de socio, tercera transferencia (usuario 17/09)", 2000.0]],
    proj_lorente: [["08/06 · parte 1 certifica — certificacion de obra Lorente y Millan", -10000.0], ["08/06 · TRANSFER INMEDIATA — devolucion de Lorente: netea el -10.000 'parte 1 certifica' del mismo dia", 10000.0], ["15/06 · Transferencia A Favor De Florente Concepto: Parte 1 Certificación 3 — Lorente y Millan (alias bancario 'Florente') - certificacion o", -9000.0]],
    proj_aycoa: [["05/06 · sonido 1parte — Aycoa - sonido/iluminacion (1a parte)", -10000.0]],
    proj_equip: [["Movimientos del extracto (todos menores de 1.000 €)", -1731.75]],
    op_cogs: [["Movimientos del extracto (todos menores de 1.000 €)", -2436.16]],
    op_fijos: [["Movimientos del extracto (todos menores de 1.000 €)", -640.15]],
    op_extra: [["Movimientos del extracto (todos menores de 1.000 €)", -202.7]],
    fin_comisiones: [["Movimientos del extracto (todos menores de 1.000 €)", -911.2]],
  }
};

// Julio 2026 (mes completo) — memoria 27/08 + overrides bancarios
REAL_CAJA[6] = {
  in_tpv: [["Liquidaciones TPV de julio (netas de comisión)", 145782]],
  in_fv: [["Ventas Fourvenues de julio (cierres del gerente)", 42525]],
  in_redeme: [["Devolución del IVA de la obra (REDEME), 31/07", 40059.78]],
  in_otros: [["Ingreso en efectivo de Ybarra, 14/07", 2850],["Otros abonos", 750]],
  proj_lorente: [["Florente, parte cert. 05 (9/7)", -5000],["Florente, resto cert. 05 (18/7)", -3763.02]],
  proj_viento: [["Cartel de fachada (8/7)", -2371.60],["A cuenta tematización (15/7)", -5000]],
  proj_yuste: [["Mantec (28/7)", -5000],["Mantec (28/7)", -10000]],
  proj_bs: [["BS Aislamientos, último pago (20/7)", -8145.50]],
  proj_aycoa: [["Aycoa (14/7)", -5000],["Aycoa (29/7)", -5000]],
  proj_stima: [["Stima 21, factura T32661 (13/7)", -4537.50]],
  proj_equip: [["Equipamiento menor (5 cargos)", -1339]],
  op_cogs: [["Merino, Melgarejo, Makro, Picking, hielo… (16 cargos)", -29832]],
  op_personal: [["Disposiciones de efectivo en ventanilla (9.500 + 3.000) y formación", -13640]],
  op_irpf: [["AEAT 20/07", -73.69]],
  in_prestamos: [["Devolución préstamo socios (20/7)", -5000]],
  op_alquiler: [["Realmivo, renta de julio", -2297.02]],
  op_fijos: [["Gestoría, seguros, telecom y software", -746]],
  op_marketing: [["Barter", -605]],
  op_extra: [["Comidas del equipo, taxis, farmacia (10 cargos)", -562]],
  fin_comisiones: [["Intereses confirming (8/7) y comisiones", -490]]
};
// Agosto 2026 hasta el 27/08 — memoria 27/08 + overrides bancarios
REAL_CAJA[7] = {
  in_tpv: [["Liquidaciones TPV del 1 al 27 de agosto", 265400]],
  in_fv: [["Ventas Fourvenues de agosto: saldo 83.700 € visto el 28/08 − 42.525 € de julio (cierres: 39.750 hasta el 26/08 + últimas noches)", 41175]],
  in_redeme: [["Devolución del IVA de preapertura, 2ª parte (21/08, CaixaBank). Antes se tomó por retirada de Fourvenues; cuadra al céntimo con la cuenta 470 de la contabilidad (40.059,78 + 13.946,03 = 54.005,81)", 13946.03]],
  in_otros: [["Abonos del 20/08 (2.100 + 1.750) e ingreso en efectivo de Ybarra (500)", 4350]],
  proj_lorente: [["Factura 28, certificación 06 (12/8) — cuenta cerrada", -23699.33]],
  proj_yuste: [["Mantec, último pago (5/8) — cuenta cerrada", -11214.80]],
  proj_aycoa: [["“Pago sonido” (24/8)", -5000]],
  proj_stima: [["Stima 21, factura T32665 (5/8)", -8591]],
  op_cogs: [["Recibos Melgarejo y Merino, transferencias a cuenta, Makro… (43 cargos)", -98337]],
  op_personal: [["Disposiciones de efectivo en ventanilla (3.500 + 7.500 + otras)", -12160]],
  op_djs: [["Pago Dj: Marina Aguilar, Lucas Haurie, Francisco Ruiz, Adrián León", -1873]],
  in_prestamos: [["Devolución préstamo socios (5/8)", -3000],["Devolución préstamo socios, último tramo (5/8)", -4000]],
  op_alquiler: [["Realmivo, renta de agosto (pagada dentro de los 4.594 € de julio–agosto)", -2297.02]],
  op_fijos: [["Prosegur, O2, software", -519]],
  op_marketing: [["Barter (27/8, último recibo)", -605]],
  op_extra: [["Comidas del equipo y taxis (5 cargos)", -2070]],
  fin_comisiones: [["Comisiones bancarias y TPV", -307]],
  tax_iva: [["IVA de julio, autoliquidación 20/08", -9420.95]]
};
// Septiembre 2026: tramo real 28/08 → 07/09
const SEP_REAL = {
  in_tpv: [["Liquidaciones TPV 28/08–07/09 (cola de las últimas noches)", 21075]],
  in_otros: [["Devolución Amazon", 147]],
  op_cogs: [["Bebida de agosto: recibos Merino/Melgarejo, Chamán 4.766…", -22257],["Recibos Merino (08–09/09)", -5943.91],["Devolución de compras Melgarejo N4574 (15/09)", 5818.00]],
  op_ss: [["TC1 de julio (TGSS, 31/08)", -8387]],
  op_personal: [["Adelantos de nómina de agosto (disposiciones)", -9400]],
  op_djs: [["DJs de agosto", -5957],["DJs de agosto por transferencia, 08–16/09 (15 pagos, incl. agencia Events Branch)", -8566.58],["Bodegas Mirasierra (DJ), 16/09", -151.25]],
  proj_confirming: [["Confirming: Lorente factura 23 (Santander, cobro 03/09)", -5000]],
  op_extra: [["Comidas del equipo, taxis, uniformes Henris, varios", -3587],["Reembolso a Ramón Romero: Cala Santa 2.401,50 (30/08) + Leroy Merlin y Makro 988,17 (15/09)", -3389.67]],
  op_fijos: [["Stipendium (gestoría laboral) y varios", -1947 - 708],["Notaría Legal V35 (10/09)", -417.72],["Prosegur (09/09)", -54.33]],
  // tramo 08/09 → 16/09 (extractos del 17/09)
  proj_aycoa: [["Aycoa, “sonido penúltima” (07/09, CaixaBank)", -9000],["Aycoa, “último pago sonido” (08/09) — cuenta cerrada", -10114.18]],
  in_acuerdos: [["Rappel Cruzcampo de agosto, Melgarejo RU1113 (15/09)", 485.82],["Aportación comercial de Melgarejo, 400 + IVA (16/09, CaixaBank)", 484]],
  op_alquiler: [["Realmivo, agosto y septiembre (11/09)", -4878.39]],
  op_rrpp: [["Pago RRPP a Security, “Comunicación eventos” (14/09)", -15172.87]],
  fin_comisiones: [["Comisiones TPV y extracto", -27.20]]
};
// Septiembre 2026: comprometido pendiente al 07/09 (docs/liquidez_cierre_2026.md, act. 07/09 2ª)
const SEP_PEND = {
  in_prestamos: [["Préstamo Cruzcampo, primer pago (no ha llegado a 16/09)", 30000]],
  proj_confirming: [["Confirming pendiente según el usuario (17/09): Lorente C04 32.343,05 + BS Aislamientos 12.653 (+3 € sin explicar)", -44999.05]],
  proj_viento: [["Viento Creativo, estado de cuentas del 02/09", -12280.05]],
  op_marketing: [["Facturas de temporada sin pagar a 16/09, netas de retención: Álvaro Pastor 3.420, Juan Máximo 1.060, Evans 1.060", -5540]],
  proj_licencias: [["Licencia para la DR", -10000]],
  op_ss: [["TC1 de agosto según la nómina contabilizada (8.717,44 + 1.676,00)", -10393.44]],
  op_cogs: [["Bebida pendiente: deuda a 31/08 según la contabilidad menos lo pagado por banco hasta el 16/09 — Ipasur 1.863, Coca-Cola ~985 (5.710 − 2.693 − devoluciones 2.032), hielo ~981, Dilaso y Monbake ~725. Merino: la factura 27223/26A (3.944,39) queda compensada con sus abonos por devolución (−9.931,65); el saldo a favor se devuelve en dinero (ver abajo)", -4554],["Merino devuelve en dinero el saldo a favor: abonos 1244/1245 (9.931,65) − factura 27223/26A (3.944,39)", 5987.26]],
  proj_stima: [["Stima 21, factura extra T32670 (17/09): 1.750 + IVA, por transferencia", -2117.50],["Stima 21, 4.000 € en efectivo sin IVA antes de fin de año (usuario 17/09; antes 6.000)", -4000]],
  op_fijos: [["Gestoría y seguros", -400]]
};

// 2027 repite el patrón de caja de 2026 (banco), escalado por ventas. Importes de 2026:
const PATRON = {   // [mes, fila, label, importe 2026, escala con ventas?]
  jun: [["op_cogs","Stock inicial (2026: 2.436 €)", -2436.16, true]],
  jul: [["in_tpv","Liquidaciones TPV (2026: 145.782)", 145782, true],["in_fv","Ventas Fourvenues (2026: 42.525)", 42525, true],
        ["op_cogs","Compras (2026: 29.832)", -29832, true],["op_personal","Disposiciones de efectivo (2026: 13.640)", -13640, true],
        ["op_alquiler","Realmivo", -2319.18, false],["op_fijos","Gestoría, seguros, telecom, software", -746, false],["op_marketing","Barter", -605, false],
        ["op_extra","Comidas del equipo, taxis (2026: 562)", -562, true],["fin_comisiones","Comisiones", -190, false],["op_irpf","Retenciones de junio", -74, false]],
  ago: [["in_tpv","Liquidaciones TPV (2026: 265.400 hasta el 27/08)", 265400, true],["in_fv","Ventas Fourvenues (2026: 41.175)", 41175, true],
        ["op_cogs","Compras (2026: 98.337)", -98337, true],["op_personal","Disposiciones de efectivo (2026: 12.160)", -12160, true],
        ["op_ss","TC1 de julio (2026: 8.387)", -8387, true],["op_djs","Pago Dj por banco (2026: 1.873)", -1873, true],
        ["op_alquiler","Realmivo", -2319.18, false],["op_fijos","Gestoría, seguros, telecom, software", -519, false],["op_marketing","Barter", -605, false],
        ["op_extra","Comidas del equipo y taxis (2026: 2.070)", -2070, true],["fin_comisiones","Comisiones", -307, false],["tax_iva","IVA de julio (2026: 9.421)", -9420.95, true]],
  sep: [["in_tpv","Cola del TPV de las últimas noches (2026: 21.075)", 21075, true],
        ["op_cogs","Bebida de agosto pagada en septiembre (2026: 22.257 + 13.800 pendientes)", -36057, true],["op_personal","Adelantos y resto de nómina de agosto (2026: 9.400 + 5.600)", -15000, true],
        ["op_ss","TC1 de agosto (2026: 10.393)", -10393.44, true],["op_djs","DJs de agosto (2026: 5.957 + 8.718)", -14674.83, true],
        ["op_extra","Comidas, taxis, uniformes (2026: 3.587)", -3587, true],["op_fijos","Gestoría laboral y varios (2026: 2.655)", -2655, false],
        ["op_alquiler","Realmivo", -2319.18, false],["tax_iva","IVA de agosto (2026: 3.375)", null, false]],
  oct: [["op_irpf","Modelo 111 del 3T", -1200, false],["op_alquiler","Realmivo", -2319.18, false],["op_fijos","Gestoría y seguros", -395, false]],
  nov: [["in_redeme","Devolución del IVA de septiembre", 5300, true],["tax_iva","IVA de octubre (Pepsi)", null, false],["op_alquiler","Realmivo", -2319.18, false],["op_fijos","Gestoría y seguros", -395, false]],
  dic: [["op_alquiler","Realmivo", -2319.18, false],["op_fijos","Gestoría y seguros", -395, false]]
};

// ---------------------------------------------------------------- modelo
function modelo(p){
  const pl = {}, caja = {};
  for (const [,k] of FILAS_PL) pl[k] = Array.from({length: N}, () => []);
  for (const [,k] of FILAS_CAJA) caja[k] = Array.from({length: N}, () => []);
  const add = (t, k, i, label, v) => { if (v !== null && v !== undefined && Math.abs(v) > 0.004) t[k][i].push([label, v]); };
  const s = p.ventas27/100, rj = p.jun27/VENTAS_IVA.jul;   // rj = junio 2027 como fracción de julio 2026

  // ===== P&L 2026 =====
  // Enero–junio: el local ya se pagaba (alquiler, comunidad, gestoría y software) aunque el resto sea coste de proyecto
  const FIJOS_PRE = {1: -116, 2: -131, 3: -121.15, 4: -217, 5: -640};   // banco, con IVA
  for (let i = 0; i <= 5; i++){
    if (i >= 1) add(pl, "alquiler", i, "Renta Realmivo", -1700);
    add(pl, "alquiler", i, "Comunidad del centro comercial (en la factura de Realmivo)", -198.36);
    if (FIJOS_PRE[i]) add(pl, "fijos", i, "Gestoría y software pagados por banco ÷ 1,21", FIJOS_PRE[i]/1.21);
  }
  for (const [mes, i] of [["jul", 6], ["ago", 7]]) for (const k in REAL_PL[mes]) for (const [l, v] of REAL_PL[mes][k]) add(pl, k, i, l, v);
  for (const i of [6, 7]) add(pl, "amort", i, `Lineal a 10 años: ${p.amortAnual.toLocaleString("es")} €/año ÷ 12`, -p.amortAnual/12);
  for (let i = 8; i <= 11; i++){
    add(pl, "alquiler", i, "Renta Realmivo", -1700); add(pl, "alquiler", i, "Comunidad del centro comercial", -216.68);
    add(pl, "fijos", i, "Gestoría 120 + Mapfre, Prosegur, O2 ~250 + software", -395);
    add(pl, "amort", i, `${p.amortAnual.toLocaleString("es")} €/año ÷ 12`, -p.amortAnual/12);
  }
  add(pl, "acuerdos", 9, "Pepsi, 17.000 € + IVA (cobro en octubre)", 17000);
  add(pl, "cogs", 8, "Devolución de compras a Melgarejo al cierre (N4574, 07/09): base 4.817 € (mercancía 4.058 + envases 759)", 4817.00);
  add(pl, "cogs", 8, "Devolución de compras a Merino al cierre (abonos 1244/26N y 1245/26N del 02/09): base 277,61 + 7.930,36", 8207.97);
  add(pl, "acuerdos", 8, "Aportación comercial de Melgarejo (16/09, 400 € + IVA)", 400);
  // ===== P&L 2027 =====
  const ventas27 = {5: p.jun27/1.1, 6: VENTAS_IVA.jul/1.1*s, 7: VENTAS_IVA.ago/1.1*s};
  for (let m = 0; m < 12; m++){
    const i = 12 + m, V = ventas27[m] || 0;
    if (V > 0){
      add(pl, "ventas", i, m === 5 ? `Supuesto: ${p.jun27.toLocaleString("es")} € con IVA ÷ 1,10` : `${MESN[m]} 2026 (${Math.round((m === 6 ? VENTAS_IVA.jul : VENTAS_IVA.ago)/1.1).toLocaleString("es")} €) × ${p.ventas27} %`, V);
      add(pl, "cogs", i, `${p.cogs27} % de las ventas`, -V*p.cogs27/100);
      add(pl, "personal", i, `${p.personal27} % de las ventas`, -V*p.personal27/100);
      add(pl, "djs", i, `${p.djs27} % de las ventas`, -V*p.djs27/100);
      add(pl, "marketing", i, "Barter (500 € base)", -500);
      if (m === 6 || m === 7) add(pl, "marketing", i, `Foto, vídeo y gestión comercial como ${m === 6 ? "julio" : "agosto"} de 2026`, (m === 6 ? -600 : -4400)*s);
      add(pl, "extra", i, m === 7 ? "Como agosto de 2026 (8.700 € con IVA)" : "Como julio de 2026 (562 € con IVA)", (m === 7 ? -7902/1.21*s : (m === 5 ? -464*rj : -464*s)));
      add(pl, "financiero", i, "Comisiones bancarias, TPV", m === 6 ? -490 : -300);
      add(pl, "fijos", i, m === 7 ? "Fijos 395 + gestoría laboral de cierre 1.600" : "Fijos 395 + software y telecom de temporada", m === 7 ? -1995 : -560);
    } else add(pl, "fijos", i, "Gestoría 120 + Mapfre, Prosegur, O2 ~250", -395);
    if (m === 7) add(pl, "rrpp", i, `RRPP ${p.rrpp27.toLocaleString("es")} € con IVA ÷ 1,21`, -p.rrpp27/1.21);
    if (m === 5 && p.preap27 > 0) add(pl, "extra", i, "Puesta a punto de la reapertura (÷1,21)", -p.preap27/1.21);
    if (m === 8 && p.vac27 > 0) add(pl, "personal", i, "Vacaciones al cierre", -p.vac27);
    add(pl, "alquiler", i, "Renta Realmivo", -1700); add(pl, "alquiler", i, "Comunidad del centro comercial", -216.68);
    if (m === 6 || m === 7) add(pl, "rappels", i, `Rappel Pernod Ricard ${p.rappel27.toLocaleString("es")} € × ${m === 6 ? "1.602" : "2.394"} / 3.996 botellas (reparto de 2026)`, p.rappel27*(m === 6 ? 1602 : 2394)/3996);
    add(pl, "amort", i, `${p.amortAnual.toLocaleString("es")} €/año ÷ 12`, -p.amortAnual/12);
    if (m === 9) add(pl, "acuerdos", i, `Pepsi 2027 (supuesto)`, p.pepsi27);
  }
  // ===== totales P&L =====
  const sum = a => a.reduce((x, c) => x + c[1], 0);
  const val = (t, k, i) => sum(t[k][i]);
  const sumY = (t, k, y) => { let z = 0; for (let m = 0; m < 12; m++) z += val(t, k, idx(y, m)); return z; };
  const V = {}; for (const k of PL_KEYS) V[k] = COLS.map((_, i) => val(pl, k, i));
  V.margen = COLS.map((_, i) => V.ventas[i] + V.acuerdos[i] + V.cogs[i] + V.rappels[i]);
  V.ebitda = COLS.map((_, i) => V.margen[i] + V.personal[i] + V.djs[i] + V.rrpp[i] + V.alquiler[i] + V.fijos[i] + V.marketing[i] + V.extra[i] + V.financiero[i]);
  V.resultado = COLS.map((_, i) => V.ebitda[i] + V.amort[i]);
  const res26 = V.resultado.slice(0, 12).reduce((a, b) => a + b, 0), res27 = V.resultado.slice(12).reduce((a, b) => a + b, 0);
  const cuota26 = Math.max(0, res26)*p.is/100, cuota27 = Math.max(0, res27)*p.is/100;
  add(pl, "is", 11, `${p.is} % × resultado 2026 (${Math.round(res26).toLocaleString("es")} €)`, -cuota26);
  add(pl, "is", 23, `${p.is} % × resultado 2027 (${Math.round(res27).toLocaleString("es")} €)`, -cuota27);
  V.is = COLS.map((_, i) => val(pl, "is", i));
  V.neto = COLS.map((_, i) => V.resultado[i] + V.is[i]);

  // ===== caja 2026 real =====
  for (let i = 0; i <= 7; i++) for (const k in REAL_CAJA[i]) for (const [l, v] of REAL_CAJA[i][k]) add(caja, k, i, l, v);
  for (const k in SEP_REAL) for (const [l, v] of SEP_REAL[k]) add(caja, k, 8, l, v);
  for (const k in SEP_PEND) for (const [l, v] of SEP_PEND[k]) add(caja, k, 8, l, v);
  add(caja, "tax_iva", 8, "IVA de agosto (modelo 303), pagado el 14/09", -p.ivaAgo26);
  add(caja, "in_redeme", 9, "Devolución del IVA de junio (303 del 18/07, 11.095,82 €): sin cobrar a 16/09, fecha supuesta", 11095.82);
  // oct–dic 2026
  add(caja, "in_acuerdos", 9, "Pepsi 17.000 € + IVA", 20570);
  add(caja, "in_acuerdos", 9, "Rappel Pernod Ricard 6.200 € + IVA", 7502);
  add(caja, "op_irpf", 9, "Modelo 111 del 3T", -1200);
  add(caja, "op_irpf", 9, "Retenciones de las facturas de marketing (150 + 150 + 210)", -510);
  add(caja, "in_redeme", 10, "Devolución del IVA de septiembre (Viento, RRPP, fijos)", 5300);
  add(caja, "tax_iva", 10, "IVA de octubre: Pepsi 3.570 − fijos 400, pago 20/11", -3170);
  for (let i = 9; i <= 11; i++){ add(caja, "op_alquiler", i, "Realmivo (1.700 + comunidad 216,68 + IVA)", -2319.18); add(caja, "op_fijos", i, "Gestoría 145,20 + Mapfre, Prosegur, O2 ~250", -395); }
  // ===== caja 2027 =====
  add(caja, "in_prestamos", 12, "Préstamo Cruzcampo, segundo pago", 10000);
  add(caja, "in_redeme", 12, "Devolución del IVA de noviembre de 2026", 400);
  add(caja, "in_redeme", 13, "Devolución del IVA de diciembre de 2026", 400);
  add(caja, "op_irpf", 12, "Modelo 111 del 4T de 2026", -1200);
  for (let m = 0; m <= 4; m++){ add(caja, "op_alquiler", 12 + m, "Realmivo", -2319.18); add(caja, "op_fijos", 12 + m, "Gestoría y seguros", -395); }
  if (p.preap27 > 0) add(caja, "op_preapertura", 17, "Supuesto del usuario", -p.preap27);
  add(caja, "op_alquiler", 17, "Realmivo", -2319.18); add(caja, "op_fijos", 17, "Gestoría y seguros", -395);
  const ivaAgo27 = -p.ivaAgo26*s;
  for (const [mes, m] of [["jun", 5], ["jul", 6], ["ago", 7], ["sep", 8], ["oct", 9], ["nov", 10], ["dic", 11]]){
    const i = 12 + m, esc = s;
    for (const [k, l, v, escala] of PATRON[mes]){
      let x = v;
      if (k === "tax_iva" && v === null) x = m === 8 ? ivaAgo27 : -3170*(p.pepsi27/17000);
      if (k === "op_cogs" && m === 5){ add(caja, k, i, l, v*s); continue; }   // stock inicial: escala con ventas, no con junio
      add(caja, k, i, l, escala ? x*esc : x);
    }
  }
  if (p.jun27 > 0){
    const Vj = p.jun27, txt = `${Vj.toLocaleString("es")} € de ventas × proporción de julio 2026`;
    add(caja, "in_tpv", 17, "Liquidaciones TPV: " + txt + " (145.782 / 223.641)", 145782*rj);
    add(caja, "in_fv", 17, "Ventas Fourvenues: " + txt + " (42.525 / 223.641)", 42525*rj);
    add(caja, "op_cogs", 17, "Compras pagadas en el mes: " + txt + " (29.832 / 223.641)", -29832*rj);
    const cogsJunIva = p.cogs27/100*Vj/1.1*1.10, restoJun = Math.max(0, cogsJunIva - 29832*rj);
    add(caja, "op_cogs", 18, `Compras de junio pagadas en julio: ${Math.round(cogsJunIva).toLocaleString("es")} € con IVA menos lo pagado en junio`, -restoJun);
    add(caja, "op_personal", 17, "Disposiciones de efectivo: " + txt + " (13.640 / 223.641)", -13640*rj);
    add(caja, "op_ss", 18, "TC1 de junio: " + txt + " (8.387 / 223.641)", -8387*rj);
    add(caja, "tax_iva", 18, "IVA de junio: " + txt + " (9.421 / 223.641)", -9420.95*rj);
    add(caja, "op_extra", 17, "Comidas del equipo, taxis: " + txt + " (562 / 223.641)", -562*rj);
    add(caja, "op_marketing", 17, "Barter", -605);
    add(caja, "op_fijos", 17, "Software y telecom de temporada", -165);
    add(caja, "fin_comisiones", 17, "Comisiones TPV", -190*rj);
  }
  add(caja, "in_acuerdos", 21, "Pepsi 2027 + IVA", p.pepsi27*1.21);
  add(caja, "in_acuerdos", 21, "Rappel Pernod Ricard 2027 + IVA", p.rappel27*1.21);
  add(caja, "op_rrpp", 20, "Pago RRPP", -p.rrpp27);
  add(caja, "op_marketing", 20, "Foto, vídeo y gestión comercial de la temporada (2026: 5.540 netos)", -5540*s);
  add(caja, "op_irpf", 21, "Retenciones de marketing (2026: 510)", -510*s);
  if (p.vac27 > 0) add(caja, "op_personal", 20, "Vacaciones al cierre", -p.vac27);
  add(caja, "tax_is", 18, `IS 2026 (modelo 200), ${p.is} % × ${Math.round(res26).toLocaleString("es")} €`, -cuota26);
  add(caja, "tax_is", 21, "Modelo 202: 18 % de la cuota de 2026", -0.18*cuota26);
  add(caja, "tax_is", 23, "Modelo 202: 18 % de la cuota de 2026", -0.18*cuota26);

  // ===== ajuste de los meses reales al saldo del extracto =====
  // Cada mes real se cuadra con la liquidez real a fin de mes; la diferencia (movimientos menores no desglosados, redondeos) va a "otros / por identificar".
  { let acum = LIQ_DIC25;
    for (let i = 0; i <= 7; i++){
      const neto = IN_KEYS.concat(OUT_KEYS).reduce((a, k) => a + val(caja, k, i), 0);
      const dif = LIQ_REAL[i] - (acum + neto);
      if (Math.abs(dif) >= 1) add(caja, "in_otros", i, "Ajuste al saldo real del extracto: movimientos menores no desglosados y abonos por identificar", dif);
      acum = LIQ_REAL[i];
    } }
  // ===== totales de caja =====
  const C = {}; for (const k of IN_KEYS.concat(OUT_KEYS)) C[k] = COLS.map((_, i) => val(caja, k, i));
  C.ingresos = COLS.map((_, i) => IN_KEYS.reduce((a, k) => a + C[k][i], 0));
  C.gastos = COLS.map((_, i) => OUT_KEYS.reduce((a, k) => a + C[k][i], 0));
  C.neto = COLS.map((_, i) => C.ingresos[i] + C.gastos[i]);
  C.saldo = []; let sal = LIQ_DIC25;
  C.neto.forEach((x, i) => { sal += x; C.saldo.push(sal); });
  V.proyecto = COLS.map((_, i) => -PROJ_KEYS.reduce((a, k) => a + C[k][i], 0));
  return {pl, caja, V, C, res26, res27, cuota26, cuota27, s, rj};
}

if (typeof module !== "undefined") module.exports = {modelo, P, COLS, FILAS_PL, FILAS_CAJA, IN_KEYS, OUT_KEYS, PROJ_KEYS, OP_KEYS, PL_KEYS, GRUPOS, LIQ_REAL, MES, MESN};
