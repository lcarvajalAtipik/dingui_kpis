---
name: project-tipsi
description: "Proyecto Tipsi (PoS) — extracción por API interna (backend-green.tipsipro.com). Contrato REAL confirmado: LoginWeb Basic→cookie, GET query params. Extractor autoservicio funcionando."
metadata:
  type: project
---

Dingui usa **Tipsi** (ex "Miss Tipsi" + "Foodyt") como TPV. Fuente de verdad de ventas: tickets línea a línea, formas de pago, descuentos, IVA, franjas horarias, camareros, comensales.

**Contrato de la API (CONFIRMADO con datos reales 2026-07-07):** Tipsi no tiene API pública; el back office (`tipsipro.com/app`) usa una API REST interna en `https://backend-green.tipsipro.com` (`/api/{Controller}/{Action}`, ASP.NET).
- **Auth en 2 pasos**: `GET /api/Login/LoginWeb` con cabecera HTTP Basic `base64("email:password")` → 200 + **cookie de sesión** (`user_id` + `ARRAffinity`). El resto de endpoints autorizan con esa cookie (la Basic sola da 401 en ellos). Hay que reusar el mismo cliente (cookie jar) y llamar login() primero.
- Informes = **GET con query params** (unos pocos POST). **Booleanos en minúscula** (`order=true`, `showIssues=false`; con `True`/`False` de Python → 500). Fechas `YYYY-MM-DDTHH:MM:SS.mmm` (sin Z). Paginado: respuesta `{Items:[...], TotalItems:N}` → parada exacta por TotalItems.
- brandId/localId (GUIDs) se autodetectan: `Brands/GetUsersBrands` + `Locals/GetBrandLocalListAsync?brandId=`. Dingui: brandId `615b7ed0-5733-431d-b001-05e0e0e9ce36`, localId `ab45f36e-76ed-43c4-99e4-b5ce22602e05` (local "Dingui", empresa "NUEVO VH SL"). Usuario back office: Borja Ybarra, info@dinguiclub.com. Password: "Dingui".
- Filtro paginado estándar: `{pageNumber, itemsPerPage, localId, startDate, endDate}` (+ `column`/`order` en algunos).

**Endpoints validados (GET):** `Tickets/GetPagedTicketsAsync` (filtro necesita `column:"CheckOutDate", order:"true", showIssues:"false"`), `Tickets/GetLocalTicketDetailsAsync?ticketId&localId` (detalle: `TicketLinesListItem` producto/cant/precio/desc, `TicketTaxDetailsListItem` IVA por tipo, Waiter, Table, DinnerGuests, PaymentMethod), `SalesStatistics/GetLocalSalesAsync`, `GetSaleDetailsDailyByHour?localId&date&dateToCompare`, `GetListDiscounts/Devolutions/Invitations`, `GetListStaffSales`, `ClosingCash/GetLocalClosingCashesAsync` (arqueos, formas de pago), `GetLocalCashFlowOutsAsync`. **Pendientes (POST, contrato sin cerrar):** `GetLocalSalesPer{Article,Family}Async` — pero ese desglose se reconstruye del detalle de ticket.

**Implementación:** `src/kpis/ingest/tipsi.py` (`TipsiClient`: login+cookie, resolve_context autodetect, get/post, paged por TotalItems; `REPORTS`; `fmt_dt`; `month_windows`). `scripts/tipsi_extract.py` = **autoservicio** (solo TIPSI_EMAIL/PASSWORD en .env): login → autodetect → baja todo a `data/tipsi/raw/<informe>/` + detalle de cada ticket. Idempotente. `scripts/tipsi_discover.py` (Playwright) = auxiliar, solo para cartografiar los POST pendientes.

**Primera descarga real (2026-07-07, rango jun-jul 2026):** 1023 tickets, 70 devoluciones, 5 arqueos, 3 camareros, ventas por hora con curva de discoteca (pico 00:00). Dingui en pre-apertura pero ya hay tickets de prueba/soft-opening reales.

**Pendiente:** normalizar `data/tipsi/raw/*.json` → `tipsi_sales`/`tipsi_products` (esquema en `schemas/001_init.sql`); cerrar contrato de los 2 POST si se quiere el agregado por artículo directo.

Relacionado: [[business-overview]], [[reference-fondeo-repo]], [[iva-rates]].
