---
name: tipsi-no-brand-modifiers
# Clasificación de artículos Tipsi (validada 31/07 con 10.288 líneas de detalle):
# COPAS: "COPA 1" (7,72 s/IVA), "COPA 2" (8,65), "COPA 3" (9,03), COPA <marca>. CHUPITOS: "CHAMAN"
# (el chupito de la casa, 3,18) y "TEQUILA" (3,18). CERVEZA: TERCIO (3,79) / CORTADA (1,90, caña
# pequeña) / ENTERA (3,18) / BOTELLIN / RADLER. BOTELLAS reservado: "Bot *" (texto libre del camarero,
# muy sucio). PUERTA: "Visas puerta"/"Efect puerta" = lotes de taquilla. "CONSUMICIÓN" 0€ = canje
# de entrada. Comida: BIK./GILDAS/TOST. etc. Detalle en data/tipsi/lineas_tickets.parquet (gitignored,
# regenerable de raw/detalle_tickets).
description: "Tipsi de Dingui NO captura la marca del destilado ni modificadores. COPA 1/2/3/* son tramos de precio (7,5/8,5/9,5/10€), no marcas. Solo hay marca en el nombre para vinos/cócteles/refrescos."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 84abf2a4-b0ee-40eb-a33d-d4637ef9e3ce
---

**No se puede sacar la marca del destilado (ni ginebra/ron/vodka) de Tipsi hoy.** Verificado por 3 vías (2026-07-07):

1. **Detalle de ticket:** `TicketDetailsListItem` (sublista de modificadores) = **null en el 100%** de las 1326 líneas. `FamilyMealId`/`HasFamilyMealId` sin usar. `ParentSaleDetailsId` solo modela **devoluciones** (línea negativa → misma venta), no ingredientes.
2. **Catálogo de artículos** (`Articles/GetBrandListSaleArticle?brandId=`): 79 artículos, todos con `SaleFormats=[]`, `MenuFamilies=[]`, `ExceptionsToRemove=[]` **vacíos**. `Articles/GetBrandCombinationListAsync` = **[]** (cero combinaciones/modificadores configurados). 9 familias (`Articles/GetBrandSaleFamiliesNames`): BIKINS, CERVEZA, COCKTELES, ENTRANTES/TAPAS, GILDAS, PLATOS, POSTRES, TOSTAS, VINOS — los destilados NO están clasificados en familia.
3. **Informe de combinaciones** (`SalesStatistics/GetPagedSalesPerCombinationAsync`, POST): funciona pero `TotalItems=0` (vacío) porque no hay combinaciones definidas.

**Causa = operativa, no técnica:** `COPA 1/2/3/*` son **tramos de precio** (COPA *=7,5€, COPA 1=8,5€, COPA 2=9,5€, COPA 3=10€). El camarero pulsa "COPA 2" sin elegir marca → la marca nunca se captura en origen; ninguna API la puede devolver.

**Lo que SÍ hay:** marca embebida en el propio `Articulo`/`Name` para **vinos y cócteles/refrescos con marca**: COPA MONTECILLO, COPA CROFT TWIST, DESPERADOS, TERCIO HEINEKEN/PILSEN, COCA COLA, RED BULL, SCHWEPPES, etc. → parseable con un diccionario. Los destilados (COPA 1/2/3, ~80% de la caja) NO.

**Cómo tenerlo en el futuro:** configurar en la carta de Tipsi **modificadores o artículos por marca** (que el camarero elija "Beefeater" al cobrar). Entonces `GetPagedSalesPerCombinationAsync` lo desglosaría sin tocar código. Decisión de Dingui.

**Contratos POST descifrados (de paso, para el extractor):**
- `SalesStatistics/GetLocalSalesPerArticleAsync` (POST): body `{localId, startDate, endDate, pageNumber, itemsPerPage, articles:[], showFormats:true, tpvId:null, column:"Name", order:true}`. OJO `column` debe ser "Name" (con "ArticleName" → 500). Devuelve `{Name, FormatName, Reference, Amount, Total}`.
- `SalesStatistics/GetPagedSalesPerCombinationAsync` (POST): body `{localId, brandId, startDate, endDate, pageNumber, itemsPerPage, combinations:[], column:"Combination", order:true}` (faltaban `brandId` y `combinations:[]` → 500).

Relacionado: [[project-tipsi]], [[fourvenues-puerta-ticketing]].
