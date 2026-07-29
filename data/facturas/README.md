# Registro de facturas (Drive → CSV, sin reprocesar)

Sistema de reconocimiento de facturas de Dingui. **Drive es la fuente única** (los PDFs no
se suben al repo); aquí solo viven los metadatos y líneas extraídas, con el `drive_id` de
cada archivo para no reprocesar jamás.

## Carpetas Drive (compartir con l.carvajal@atipikproperties.com — cuenta del conector)

- Documentación Dingui: `1jF3ZauLnSpD1TsG-NWGVffZLKK7KCErW`
- **Facturas (por mes)**: `1Y2gqblXGgD5QTlHrbf2EwGddiZtcBWpH`

## Archivos

### `registro_facturas.csv` — una fila por archivo de Drive
| campo | contenido |
|---|---|
| `drive_id` / `drive_url` | Identidad del archivo en Drive (clave de dedup) |
| `carpeta_mes` | Subcarpeta de origen (p. ej. "julio 2026") |
| `nombre_archivo`, `mime_type`, `modified_time` | Metadatos Drive |
| `proveedor`, `cif`, `num_factura`, `fecha_factura` | Cabecera de la factura |
| `base_imponible_eur`, `iva_eur`, `total_eur` | Importes |
| `categoria` | `comida` \| `bebida` \| `comida+bebida` \| `otros` (suministros, alquiler, servicios…) |
| `contiene` | Tags libres: `refrescos,cerveza,alcohol,comida,hielo…` |
| `n_lineas_fb` | Nº de líneas volcadas a `lineas_facturas.csv` |
| `estado` | `procesada` \| `ilegible` \| `duplicada` \| `no_factura` |
| `procesado_at`, `notas` | Trazabilidad |

### `lineas_facturas.csv` — detalle línea a línea SOLO de comida y bebida
| campo | contenido |
|---|---|
| `drive_id`, `proveedor`, `fecha_factura` | Enlace con el registro |
| `descripcion_original` | Texto literal de la línea en la factura |
| `categoria` | `comida` \| `bebida` \| `otros_consumo` (hielo, desechables…) |
| `tipo_bebida` | `refresco` \| `cerveza` \| `alcohol` \| `vino` \| `agua` \| `otros` |
| `marca` | Marca normalizada (Coca-Cola, Cruzcampo, Ballantine's, Moët…) |
| `formato` | Cerveza: `barril` \| `botellin` \| `lata`; resto: `botella`, `caja`, `garrafa`, `kg`… |
| `contenido` | Volumen/pack si consta ("50L", "24x33cl", "70cl") |
| `unidades`, `precio_unitario_eur`, `importe_eur`, `iva_pct` | Números de la línea |

## Flujo (al llegar facturas nuevas)

1. Listar archivos de TODAS las subcarpetas de mes en Drive.
2. Diff contra `registro_facturas.csv` por `drive_id` → solo lo nuevo se procesa.
3. Por cada factura nueva: descargar (cache local en `cache/`, gitignored), leer,
   extraer cabecera + clasificar; si es comida/bebida, extraer TODAS las líneas.
4. Volcar a los dos CSV, commit + push (viajan por git).
5. Los importes se cruzan contra los cargos del banco (categorías COGS del categorizador).

Reglas de clasificación de bebida: ver memoria `sistema_facturas_drive.md`.
