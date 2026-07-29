---
name: sistema-facturas-drive
description: "Sistema de registro de facturas de Dingui: Drive (carpeta por mes) → registro_facturas.csv + lineas_facturas.csv con drive_id para NO reprocesar. Taxonomía bebida: refresco/cerveza/alcohol/vino, marca, y cerveza barril vs botellín"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Encargo del usuario (29/07/2026):** sistema que reconozca las facturas de Drive (qué son, qué contienen) y lo deje anotado con su link/id para no reprocesar. **Primer objetivo: facturas de comida y bebida** — bebida diferenciada por refrescos/cerveza/alcohol, con marca; cerveza por **barril vs botellines**.

**Carpetas Drive:**
- Documentación Dingui: `1jF3ZauLnSpD1TsG-NWGVffZLKK7KCErW`
- Facturas (subcarpeta por mes): `1Y2gqblXGgD5QTlHrbf2EwGddiZtcBWpH`

**⚠ Acceso:** el conector Drive de claude.ai va con `l.carvajal@atipikproperties.com` y a 29/07 esa cuenta NO ve estas dos carpetas (el sheet de proyecciones sí, está compartido). El usuario debe compartirlas con esa cuenta; hasta entonces el sistema está montado pero sin datos.

**Dónde vive:** `data/facturas/` (git-tracked, excepción en .gitignore): `registro_facturas.csv` (una fila por archivo Drive, clave = drive_id — el diff contra esto evita reprocesar), `lineas_facturas.csv` (detalle línea a línea SOLO comida/bebida) y `README.md` (esquema completo). PDFs NO van al repo: cache local `data/facturas/cache/` (gitignored), Drive es la fuente.

**Procesamiento:** workflow `.claude/workflows/procesar-facturas.js` (committeado): Inventario Drive → diff vs registro → un agente por factura nueva (descarga+Read+extracción con schema) → verificación adversarial de sumas y clasificación en las F&B. Pasar `args.procesados` = drive_ids ya en el CSV.

**Taxonomía bebida:** tipo_bebida = refresco (incl. tónicas/zumos/energéticas) | cerveza | alcohol (destilados/licores) | vino (incl. cava/champán; Moët=vino) | agua | otros. Marca siempre normalizada (Coca-Cola, Cruzcampo, Ballantine's…). Cerveza: formato barril | botellin | lata. Hielo/desechables = otros_consumo.

**Contexto útil:** proveedores conocidos por el banco: Makro, Picking Gades, Cash Lepe, Coca-Cola (y una "cervecera" financió parte de la obra — probable contrato con marca de cerveza). Promo con Ballantine's (parte del 11/7). Los totales de facturas deben cuadrar con los cargos bancarios COGS.

Relacionado: [[pl-categories]], [[business-overview]], [[cierres-gerente-diarios]].
