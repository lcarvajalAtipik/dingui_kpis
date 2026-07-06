---
name: reference-proyecciones-sheet
description: "Sheet 'Proyecciones PuertoSantamaria' (Drive id 1Qpcu53iCU4neCCV0kQaSeLPpObLYEvMFM2zSDTbvTew) — proyecciones + ground truth de movimientos categorizados"
metadata:
  type: reference
---

Google Sheet del usuario **"Proyecciones PuertoSantamaria"** (owner `lmcarvajal96@gmail.com`, id `1Qpcu53iCU4neCCV0kQaSeLPpObLYEvMFM2zSDTbvTew`). Descargado como xlsx a `data/categorization/proyecciones_puertosantamaria.xlsx` — para refrescar, re-descargar de Drive (MCP `download_file_content` con export xlsx) y sobreescribir.

**9 hojas — cuáles importan:**
- **`movimientos 30 abril 2026`** ← GROUND TRUTH de categorización. 88 filas. Columnas: `Concepto | Fecha | Importe | Saldo | Mes | Año | Año-mes | Tipo`. La categoría es **`Tipo`**. La suma de importes (53.878,50 €) cuadra con el saldo final → completo. El usuario irá añadiendo movimientos nuevos aquí (o pasaremos a extractos crudos + revisión CSV).
- **`VdE - FC inicial`** — forecast de caja pre-apertura: presupuesto de inversión (insonorización, licencias, mobiliario cocina, sonido, arquitecto, demolición, salida de humos, obra…) + proyección de pagos mensual por las MISMAS categorías que `Tipo`, y fuentes (Aportaciones, Cervecera, Banco, Renting). Incluye proyección de devolución de IVA (21% de la inversión).
- **`Modelo Accionariado`** — cap table: capital 338.414 €, fundadores 322.000 €; socios con aportación y % (Borja Ybarra 57K, Nacho Lara 30K, Luis M. de Carvajal 15K, + ~11 más). También break-even: PE ventas, clientes mínimos (~1.036/mes a ticket 17 €).
- `VdE - Inicio y crecimiento` — modelo de ocupación (brunch/comidas/cenas, delivery) + análisis de pernoctaciones hoteleras de la zona.
- `Proyecciones Bar`, `Modelo Semanal y Margen Bebidas`, `Modelo Accionariado 2`, `Modelo Costes`, `Modelo Horario IGNORE` — **plantillas antiguas/borradores** (dicen "Jersey Amarillo", "Madrid", "2023-24"); no usar como fuente de verdad sin confirmar con el usuario.

**Roles de plantilla previstos** (Modelo Costes): Encargado, Cocinero, Asistente Cocina, Jefe de Rango, Runner/Barra, Extras.

**How to apply:** el categorizador (`src/kpis/categorizer.py`) carga las reglas exact de la hoja de movimientos automáticamente. Cuando el usuario diga que actualizó el sheet, re-descargar el xlsx y re-validar con `scripts/validate_categorizer.py`.

Relacionado: [[pl-categories]], [[business-overview]].
