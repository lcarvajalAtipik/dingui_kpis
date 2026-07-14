---
name: fourvenues-puerta-ticketing
description: "Desde 07/07/2026 la PUERTA se tickea en Tipsi (validado al céntimo); FV NO aparece en la caja Tipsi (validado 14/07 con datos). Comisiones Fourvenues: 8% gestión = 7% FV (coste) + 1% empresa. Entradas 10/12/15€ (media 13), son copas."
metadata: 
  node_type: memory
  type: project
  originSessionId: 84abf2a4-b0ee-40eb-a33d-d4637ef9e3ce
---

**Cambio (desde 2026-07-07):** la **puerta/taquilla** (y reservados) pasa a tickearse en **Tipsi**. Antes quedaba fuera del TPV: en el cuadre de la noche del 6→7 jul, Tipsi (barra) solo captaba ~65% de la caja (3.701 € de 5.656 €; puerta 690 € y FV 1.135 € iban aparte). **VALIDADO 14/07/2026 cruzando tickets Tipsi vs cierres del gerente:** desde el 7/7 los tickets Tipsi = Z del cierre al céntimo (7/7 +0,50; 9/7 0,00; 13/7 +5,00; 10/7 −132,50; 11/7 −261). **PERO Fourvenues NO aparece en la caja de Tipsi** (9/7 FV 340, 10/7 FV 150, 13/7 FV 2.548 — todos fuera de la Z; quizá se tickean a 0 €): TOTAL CAJA del gerente = Z(Tipsi) + FV. Para noches **anteriores al 7/7** hay que sumar puerta + FV desde el parte del gerente; para posteriores, solo FV.

**Convención de jornada Tipsi:** la taquilla/reservados se tickean EN LOTE al cierre (madrugada, a veces pasadas las 06:00). El `WorkDay` de los arqueos rota a las 06:00 → cajas cerradas después caen al día siguiente (pasó el 4-5/7 y el 10-11/7). Para agrupar tickets por noche usar corte a las **08:00** (noche = fecha de `TicketDateTime − 8h`), no 06:00.

**Fourvenues (venta anticipada de entradas online):**
- Precios de entrada vendidos: **10 €, 12 € y 15 €**. Sin desglose por precio → **asumir precio medio 13 €**.
- Lo que se vendía por FV eran **copas** (la entrada = una copa). Al analizar mix de producto, tratar las entradas FV como copas a ~13 € de media.
- **Gastos de gestión** (sobre la compra anticipada): **8% total = 7% para FV + 1% para la empresa**.
  - El 7% es el **mínimo obligatorio de FV** (coste de comisión que se queda FV).
  - Lo que pongamos por encima del 7% es para la empresa; el mínimo para que salga rentable es **8%** (es decir, **+1% de gestión para nosotros**).
  - El 8% de gestión es **contexto del precio de la entrada** (lo paga el cliente por encima), NO algo que reste a lo que recibe Dingui.

**Importe FV a usar = el que figura en el parte del encargado** (línea FORVENUES dentro de TOTAL CAJA). Es lo que Dingui recibe del canal FV (p.ej. **1.135 €** la noche del 6 jul 2026). No aplicar más descuentos de comisión sobre esa cifra. (Zanjado con el usuario: "el parte lo explica".)

**Puerta/taquilla:** entradas cobradas en puerta (se paga 15 € una copa en puerta). En el parte del 6 jul fueron 690 € (120 efvo + 570 visa). Desde 07/07 también en Tipsi.

**How to apply:** para "facturación de la noche" real usar barra + puerta + FV (desde 07/07 todo sale de Tipsi). En P&L, aplicar el 7% de comisión FV como coste sobre la venta del canal FV. Ver [[project-tipsi]] (extractor), [[business-overview]], [[iva-rates]].
