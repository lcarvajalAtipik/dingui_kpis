---
name: pendientes-dingui-1709
description: "Punto de retoma tras la sesión del 17/09/2026 (artifact v8): preguntas abiertas al usuario, a la gestoría y siguientes pasos (extractos, confirming, DJs, marketing junio)."
metadata:
  type: project
---

**Estado al cerrar el 17/09/2026:** artifact "Dingui mes a mes" **v8** publicado ([[artifact-dingui-mes-a-mes]]), extractos ingeridos hasta **16/09** ([[project-bank-ingest-state]]), repo y memoria commiteados y pusheados.

**Preguntas abiertas AL USUARIO (no re-preguntar lo ya respondido — ver [[feedback-persist-decisions]]):**
1. **DJs: faltan 2 facturas por recibir para pagar** — ¿de quién y cuánto? (el coste ya está en P&L vía calendario; falta el pago en caja).
2. **Marketing: pago de junio de 500 € pendiente** — sin factura en registro/correo ni cargo en banco. ¿A quién? ¿Está dentro de los 3.000 de Álvaro Pastor (factura sin periodo)?
3. ¿En agosto se pagó a algún DJ en EFECTIVO? (posible doble conteo personal-cierres vs fila DJs).
4. Lorente factura 23: ¿pago doble? (confirming 5.000 del 03/09 = fact 23 según Santander, pero la Cert 05 ya estaba pagada por transferencia) · 3 € de diferencia confirming (44.999,05 vs 44.996,05).
5. Álvaro Pastor 3.000: periodo (hoy imputado a agosto).

**NO preguntar:** nóminas/vacaciones/finiquitos ([[feedback-nominas-cerradas]]); Security = RRPP; Melgarejo +484 = aportación comercial; Pernod 6.200+IVA octubre; Merino devuelve 5.987 en dinero; Cala Santa = comida equipo; contrato alquiler 10 años.

**Para la gestoría (Stipendium → traspaso a Asesoría Castilla desde 31/08):** 303 de enero–mayo 2026; versión 15/09 de los libros (en esta máquina solo la del 01/09); que cancelen la 470 (54.005,81 ya cobrados: 40.059,78 en 555 + 13.946,03 sin contabilizar); estado de la devolución del 303 de junio (11.095,82, sin cobrar a 16/09); Evans es fotógrafo (607 → marketing); alquiler jul-ago sin devengar; amortización (propuesta lineal 10 años, 39.500/año); retención IRPF en alquiler Realmivo (ninguna factura la lleva); lista de anomalías en [[contabilidad-gestoria-junago]].

**Siguientes pasos cuando lleguen datos:** extractos nuevos → ingest + borrar 11 dups Santander 05/08 + validar saldos + casar confirming (44.999,05), Viento 12.280,05, licencia DR 10.000, TC1 ago 10.393,44, Cruzcampo +30.000, devolución IVA junio +11.095,82, Merino +5.987,26, Stima 2.117,50 + 4.000 efectivo, marketing 5.540 (Pastor 3.420, Juan Máximo 1.060, Evans 1.060) → actualizar SEP_REAL/SEP_PEND en docs/artifacts/dingui_model.js, copiar bloque al HTML, render check (Playwright con Chrome del sistema), publicar con la URL, commit + sync memoria.
**Otros:** Tipsi login da 401 desde septiembre (¿baja temporal?); FV sigue con 0 retiradas (saldo 83.700 visto 28/08); registro de facturas sin base/IVA en Melgarejo agosto y faltan Merino 26691/26702/27223 y abonos 1244/1245.
