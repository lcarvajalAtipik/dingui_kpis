export const meta = {
  name: 'procesar-facturas',
  description: 'Inventaria las facturas de Drive, procesa solo las nuevas (no registradas) y extrae cabecera + líneas de comida/bebida',
  whenToUse: 'Cuando el usuario pida procesar/actualizar las facturas de Drive de Dingui',
  phases: [
    { title: 'Inventario', detail: 'listar subcarpetas de mes y archivos en Drive' },
    { title: 'Procesar', detail: 'un agente por factura nueva: descargar, leer, extraer' },
    { title: 'Verificar', detail: 'validar sumas y clasificación de las facturas F&B' },
  ],
}

// args: { carpeta: '<drive folder id>', procesados: ['drive_id', ...], cacheDir: '<abs path>' }
const CARPETA = args?.carpeta || '1Y2gqblXGgD5QTlHrbf2EwGddiZtcBWpH'
const PROCESADOS = new Set(args?.procesados || [])
const CACHE = args?.cacheDir || 'data/facturas/cache'

const INV_SCHEMA = {
  type: 'object', required: ['archivos'],
  properties: {
    archivos: { type: 'array', items: {
      type: 'object', required: ['id', 'nombre', 'mime', 'carpeta_mes'],
      properties: {
        id: { type: 'string' }, nombre: { type: 'string' }, mime: { type: 'string' },
        carpeta_mes: { type: 'string' }, url: { type: 'string' }, modified: { type: 'string' },
      } } },
  },
}

const FACT_SCHEMA = {
  type: 'object', required: ['registro', 'lineas'],
  properties: {
    registro: { type: 'object', required: ['drive_id', 'proveedor', 'categoria', 'estado'],
      properties: {
        drive_id: { type: 'string' }, proveedor: { type: 'string' }, cif: { type: 'string' },
        num_factura: { type: 'string' }, fecha_factura: { type: 'string' },
        base_imponible_eur: { type: 'number' }, iva_eur: { type: 'number' }, total_eur: { type: 'number' },
        categoria: { type: 'string', enum: ['comida', 'bebida', 'comida+bebida', 'otros'] },
        contiene: { type: 'string' }, estado: { type: 'string', enum: ['procesada', 'ilegible', 'duplicada', 'no_factura'] },
        notas: { type: 'string' },
      } },
    lineas: { type: 'array', items: {
      type: 'object', required: ['descripcion_original', 'categoria', 'importe_eur'],
      properties: {
        descripcion_original: { type: 'string' },
        categoria: { type: 'string', enum: ['comida', 'bebida', 'otros_consumo'] },
        tipo_bebida: { type: 'string', enum: ['refresco', 'cerveza', 'alcohol', 'vino', 'agua', 'otros', ''] },
        marca: { type: 'string' }, formato: { type: 'string' }, contenido: { type: 'string' },
        unidades: { type: 'number' }, precio_unitario_eur: { type: 'number' },
        importe_eur: { type: 'number' }, iva_pct: { type: 'number' },
      } } },
  },
}

const VERIF_SCHEMA = {
  type: 'object', required: ['ok'],
  properties: { ok: { type: 'boolean' }, problemas: { type: 'array', items: { type: 'string' } },
    correcciones: { type: 'string' } },
}

phase('Inventario')
const inv = await agent(
  `Usa ToolSearch para cargar las herramientas de Google Drive (search_files). Lista TODAS las subcarpetas de la carpeta Drive id ${CARPETA} (query: parentId = '${CARPETA}') y después TODOS los archivos dentro de cada subcarpeta (pagina si hace falta con pageToken). Devuelve el listado completo: id, nombre, mime, carpeta_mes (título de la subcarpeta), url, modified. Incluye también archivos sueltos en la raíz de la carpeta (carpeta_mes='(raíz)'). No omitas ninguno.`,
  { label: 'inventario-drive', schema: INV_SCHEMA })

const nuevos = inv.archivos.filter(a => !PROCESADOS.has(a.id) && a.mime !== 'application/vnd.google-apps.folder')
log(`${inv.archivos.length} archivos en Drive; ${nuevos.length} nuevos por procesar`)
if (!nuevos.length) return { inventario: inv.archivos.length, nuevos: 0, resultados: [] }

const EXTRACT_PROMPT = (a) => `Procesa la factura "${a.nombre}" (Drive id ${a.id}, mime ${a.mime}, carpeta "${a.carpeta_mes}") del restaurante/discoteca Dingui (NUEVO VH SL, El Puerto de Santa María).

1. Usa ToolSearch para cargar mcp__claude_ai_Google_Drive__download_file_content. Descárgala (si es Google Doc nativo exporta a PDF). El resultado llega como JSON con content en base64: guárdalo con Bash+python en ${CACHE}/${a.id}.<ext> y léelo con Read (los PDF se leen con pages).
2. Extrae la CABECERA: proveedor, CIF, nº factura, fecha (YYYY-MM-DD), base imponible, IVA, total.
3. CLASIFICA la factura: comida | bebida | comida+bebida | otros (suministros, alquiler, servicios, equipamiento...).
4. SOLO si tiene comida/bebida: extrae TODAS las líneas de producto. Por línea:
   - descripcion_original: texto literal
   - categoria: comida | bebida | otros_consumo (hielo, vasos, desechables, menaje)
   - tipo_bebida: refresco | cerveza | alcohol | vino | agua | otros (vacío si no es bebida). Reglas: refrescos incluyen tónicas/zumos/energéticas; "alcohol" = destilados y licores; el vino/cava/champán va como "vino" (Moët = vino); cerveza aparte.
   - marca NORMALIZADA (Coca-Cola, Fanta, Schweppes, Red Bull, Cruzcampo, Estrella Galicia, Ballantine's, Beefeater, Absolut, Moët & Chandon...). Si la línea no trae marca, deduce del texto; si imposible, "".
   - formato: para cerveza OBLIGATORIO distinguir barril | botellin | lata (barril=keg/50L/30L/20L; botellin=botella 20/25/33cl, packs). Para el resto: botella, caja, garrafa, kg, ud...
   - contenido: volumen/pack si consta ("50L", "24x25cl", "70cl", "1L")
   - unidades, precio_unitario_eur, importe_eur (sin IVA si la factura desglosa; si no, indica en notas), iva_pct
5. Si el archivo no es una factura (albarán, foto suelta, presupuesto) → estado 'no_factura'. Si no se puede leer → 'ilegible'. Si es duplicado evidente de otra factura del mismo proveedor/nº → 'duplicada' con nota.

Devuelve exactamente el objeto {registro, lineas} del schema. Las facturas de categoría 'otros' devuelven lineas=[].`

phase('Procesar')
const resultados = await pipeline(
  nuevos,
  a => agent(EXTRACT_PROMPT(a), { label: `factura:${a.nombre.slice(0, 40)}`, phase: 'Procesar', schema: FACT_SCHEMA })
        .then(r => r && ({ ...r, _archivo: a })),
  async (r, a) => {
    if (!r) return null
    const esFB = r.registro.categoria !== 'otros' && r.lineas.length > 0
    if (!esFB) return { ...r, verificacion: { ok: true, problemas: [] } }
    const v = await agent(
      `Verificación adversarial de la extracción de la factura "${a.nombre}" (Drive id ${a.id}) de ${r.registro.proveedor}. El archivo está cacheado en ${CACHE}/${a.id}.* — léelo tú mismo (Read; PDFs con pages) y comprueba SIN fiarte de la extracción:
1. ¿La suma de importe_eur de las líneas cuadra con la base imponible ${r.registro.base_imponible_eur} (±1€ por redondeos)? ¿Faltan líneas de producto?
2. ¿Los tipo_bebida son correctos? (refresco/cerveza/alcohol/vino/agua; tónica=refresco, Moët=vino)
3. ¿Las marcas son correctas y están normalizadas?
4. En cervezas, ¿el formato barril/botellin/lata es correcto según la descripción?
Extracción a auditar: ${JSON.stringify(r.lineas).slice(0, 6000)}
Devuelve ok=true solo si TODO cuadra; si no, lista los problemas concretos y en 'correcciones' un JSON con las líneas corregidas.`,
      { label: `verif:${a.nombre.slice(0, 40)}`, phase: 'Verificar', schema: VERIF_SCHEMA })
    return { ...r, verificacion: v }
  }
)

const okRes = resultados.filter(Boolean)
log(`Procesadas ${okRes.length}/${nuevos.length}; con problemas de verificación: ${okRes.filter(r => r.verificacion && !r.verificacion.ok).length}`)
return { inventario: inv.archivos.length, nuevos: nuevos.length, resultados: okRes }
