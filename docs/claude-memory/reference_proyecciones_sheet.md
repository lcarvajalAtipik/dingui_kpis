---
name: reference-proyecciones-sheet
description: "Sheet 'Proyecciones PuertoSantamaria' (Drive id 1Qpcu53iCU4neCCV0kQaSeLPpObLYEvMFM2zSDTbvTew) — proyecciones + ground truth de movimientos categorizados"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 84abf2a4-b0ee-40eb-a33d-d4637ef9e3ce
---

Google Sheet del usuario **"Proyecciones PuertoSantamaria"** (owner `lmcarvajal96@gmail.com`, id `1Qpcu53iCU4neCCV0kQaSeLPpObLYEvMFM2zSDTbvTew`). Descargado como xlsx a `data/categorization/proyecciones_puertosantamaria.xlsx` — para refrescar, re-descargar de Drive (MCP `download_file_content` con export xlsx) y sobreescribir.

**9 hojas — cuáles importan:**
- **`movimientos 30 abril 2026`** ← GROUND TRUTH de categorización. 88 filas. Columnas: `Concepto | Fecha | Importe | Saldo | Mes | Año | Año-mes | Tipo`. La categoría es **`Tipo`**. La suma de importes (53.878,50 €) cuadra con el saldo final → completo. El usuario irá añadiendo movimientos nuevos aquí (o pasaremos a extractos crudos + revisión CSV).
- **`VdE - FC inicial`** — forecast de caja pre-apertura: presupuesto de inversión (insonorización, licencias, mobiliario cocina, sonido, arquitecto, demolición, salida de humos, obra…) + proyección de pagos mensual por las MISMAS categorías que `Tipo`, y fuentes (Aportaciones, Cervecera, Banco, Renting). Incluye proyección de devolución de IVA (21% de la inversión).
- **`Modelo Accionariado`** — cap table: capital 338.414 €, fundadores 322.000 €; socios con aportación y % (Borja Ybarra 57K, Nacho Lara 30K, Luis M. de Carvajal 15K, + ~11 más). También break-even: PE ventas, clientes mínimos (~1.036/mes a ticket 17 €).
- `VdE - Inicio y crecimiento` — modelo de ocupación (brunch/comidas/cenas, delivery) + análisis de pernoctaciones hoteleras de la zona.
- **`Modelo Semanal y Margen Bebidas`** — ✅ CONFIRMADO por usuario (2026-07) como el MODELO SEMANAL (facturación esperada por día). Etiquetas heredadas ("Jersey Amarillo/Madrid/2023-24") pero los números son el plan. Facturación esperada/día (SIN IVA): Lun 2.700 / Mar 1.890 / Mié 1.890 / Jue 7.245 / Vie 9.315 / Sáb 9.315 / Dom 1.890 → semana ≈33,4K, mes (temporada) ≈140,4K. Aforo objetivo Vie/Sáb 450. Copas PP 2 (jue-sáb). PVP copa 8,1 s/IVA (9,0 c/IVA), cerveza 4,5/5,0. Margen operativo 81%; margen copa 5€, cerveza 5,62€.
- **`Proyecciones Bar`** — ✅ CONFIRMADO como P&L MENSUAL (Año 1). Etiquetas heredadas (Restaurante/Madrid/REVO). ESTACIONAL: solo factura Jun-Sep (factores 0,7/1/1/0,2). Ingresos año 407.238€; EBITDA 114.655€ (28%). Por mes temporada: Jul/Ago 140.427€ ingr / 50.893€ EBITDA; Jun 98.299/29.687; Sep 28.085/5.199. Costes 72% (materia prima 26%, personal fijo 21%, variables DJs/seguridad/limpieza 13%, local 8%). OJO: de EBITDA hacia abajo (amortización, IS, FC) hay #REF! rotos.
- `Modelo Accionariado 2`, `Modelo Costes`, `Modelo Horario IGNORE` — plantillas/borradores, no usar sin confirmar.

**Realidad vs plan (Tipsi, jun-jul 2026):** noches entre semana POR ENCIMA del plan (real ~3.700€ barra vs plan 1.890-2.700€), pero Vie/Sáb ~HALF del objetivo (real ~4.500€ barra / ~5.656€ caja total vs plan 9.315€). Gap = ticket/gasto por persona más bajo del proyectado.

**Roles de plantilla previstos** (Modelo Costes): Encargado, Cocinero, Asistente Cocina, Jefe de Rango, Runner/Barra, Extras.

**How to apply:** el categorizador (`src/kpis/categorizer.py`) carga las reglas exact de la hoja de movimientos automáticamente. Cuando el usuario diga que actualizó el sheet, re-descargar el xlsx y re-validar con `scripts/validate_categorizer.py`.

Relacionado: [[pl-categories]], [[business-overview]].
