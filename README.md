# dingui_kpis

Análisis financiero y operativo de Dingui (restaurante / discoteca, Madrid).

Misma arquitectura que `fondeo_kpis` (repo hermano), con tres proyectos sobre una misma capa de datos:
- **P&L / EBITDA** — cuenta de resultados real, forecast y desviaciones.
- **Tesorería / Liquidez** — caja real (CaixaBank) y previsión.
- **Tipsi (PoS)** — mix de ventas, márgenes, franjas horarias, dimensionado de plantilla.

Toda la interacción se hace a través de la conversación con Claude — no hay notebooks ni dashboards.

## Diferencias vs fondeo_kpis

| | Fondeo | Dingui |
|---|---|---|
| PoS | Revo | **Tipsi** |
| Bancos | Santander + CaixaBank + Sabadell | **CaixaBank** |
| Partidas P&L | 26 categorías | Mismas partidas (punto de partida) |
| Proveedores / conceptos bancarios | — | **Completamente distintos** (reglas del categorizador por construir) |

## Setup

```bash
uv sync
cp .env.example .env  # rellenar credenciales
uv run python scripts/init_db.py
```

## Setup en máquina nueva

Todo el código, la memoria de Claude y el hook de sincronización viajan por git.
Lo que NO viaja (gitignored) se regenera así:

```bash
git clone https://github.com/lcarvajalAtipik/dingui_kpis.git
cd dingui_kpis
uv sync                                    # entorno Python (instalar uv antes si no está)
bash scripts/sync_claude_memory.sh pull    # memoria Claude → ~/.claude/projects/.../memory
cp .env.example .env                       # rellenar BQ_PROJECT cuando haya BigQuery
uv run python scripts/init_db.py           # SQLite local
gcloud auth application-default login      # solo si se usa BigQuery
```

Los datos crudos (`data/`) se regeneran desde sus fuentes: el sheet de proyecciones se
re-descarga de Drive (Claude lo hace — id en `docs/claude-memory/reference_proyecciones_sheet.md`)
y los extractos de CaixaBank se vuelven a exportar a `data/bancos/inbox/`. Los conectores de
claude.ai (Drive, etc.) van con la cuenta de Claude, no con la máquina.

## Estructura

```
src/kpis/           Paquete Python (config, db, bq, categorizer, ingest, analysis)
schemas/            DDL SQL — el esquema canónico vive aquí (SQLite + BigQuery)
scripts/            Entrypoints ejecutables (init_db, ingest, reportes)
docs/               Notas operativas + backup de memoria Claude
data/               (gitignored) Datos crudos por fuente
db/                 (gitignored) SQLite local
outputs/            (gitignored) Gráficos y CSVs generados
```

## Fuentes de datos

| Fuente | Mecanismo | Estado |
|---|---|---|
| Tipsi (PoS) | API REST interna (`backend-green.tipsipro.com`, Basic auth) vía `tipsi_discover.py` + `tipsi_extract.py` | Extractor listo, esperando primer login |
| CaixaBank | XLS mensual exportado por el usuario → `data/bancos/inbox/` | Parser listo, esperando primer export |
| Contabilidad | Export de la gestoría → Drive | Esperando muestra |
| Nóminas | Por confirmar (CSV/PDF) → Drive | Pendiente |
| Forecast | Google Sheets | Pendiente crear sheet |

## Flujo de ingesta bancaria

1. Descargar movimientos de CaixaBank (XLS) y dejarlos en `data/bancos/inbox/`.
2. `uv run python scripts/test_parsers.py` — smoke test de parseo + categorización.
3. `uv run python scripts/show_uncategorized.py` — ver qué conceptos faltan por categorizar.
4. `uv run python scripts/export_uncategorized_csv.py` → el usuario revisa el CSV →
   `uv run python scripts/process_user_review.py <xlsx>` — roundtrip de revisión manual.
5. Las decisiones del usuario se consolidan como reglas en `src/kpis/categorizer.py`.
6. `uv run python scripts/ingest_bancos_to_bq.py` — carga a BigQuery.
7. `uv run python scripts/liquidity_report.py` — informe de liquidez + gráficos.

## Flujo de extracción de Tipsi (PoS)

Tipsi no tiene API pública, pero su back office (`tipsipro.com/app`) consume una API REST
interna en `backend-green.tipsipro.com`. Autenticación: `GET /api/Login/LoginWeb` con
cabecera HTTP **Basic** (`base64("email:password")`) fija una **cookie de sesión**; el resto
de endpoints (GET con query params) autorizan con esa cookie.

**Es autoservicio: solo necesitas las credenciales.** Rellena `TIPSI_EMAIL`/`TIPSI_PASSWORD`
en `.env` y ejecuta:

```bash
uv run python scripts/tipsi_extract.py                                  # todo, autodetecta local
uv run python scripts/tipsi_extract.py --desde 2026-06-01 --hasta 2026-07-07
uv run python scripts/tipsi_extract.py --solo tickets,arqueos,devoluciones
uv run python scripts/tipsi_extract.py --sin-detalle-tickets            # más rápido, sin líneas
uv run python scripts/tipsi_extract.py --limite-detalle 100             # prueba rápida
```

Hace login, autodetecta `brandId`/`localId`, y baja cada informe en JSON crudo a
`data/tipsi/raw/<informe>/` (+ `manifest.json`). Idempotente (salta lo ya bajado;
`--forzar` rehace). Cobertura confirmada con datos reales:

| Informe | Endpoint | Contenido |
|---|---|---|
| `tickets` + `detalle_tickets` | `Tickets/GetPagedTicketsAsync` + `GetLocalTicketDetailsAsync` | Tickets y **detalle línea a línea**: producto, cantidad, precio, descuento, **IVA por tipo**, forma de pago, camarero, mesa, comensales |
| `ventas_totales` | `SalesStatistics/GetLocalSalesAsync` | Ventas diarias |
| `ventas_por_hora` | `SalesStatistics/GetSaleDetailsDailyByHour` | Facturación por hora (uno por jornada) |
| `descuentos` / `devoluciones` / `invitaciones` | `SalesStatistics/GetList*` | Descuentos, anulaciones, invitaciones |
| `ventas_por_personal` | `SalesStatistics/GetListStaffSales` | Ventas por camarero |
| `arqueos` / `salidas_caja` | `ClosingCash/GetLocal*` | Cierres de caja (formas de pago) y salidas |

El catálogo vive en `src/kpis/ingest/tipsi.py` (`REPORTS`). Dos informes por artículo/familia
son POST y su contrato aún no está cerrado (marcados `experimental`; se saltan con
`--sin-experimentales`) — de todas formas ese desglose se reconstruye del detalle de ticket.

`scripts/tipsi_discover.py` (Playwright) es **auxiliar**: solo hace falta para cartografiar
esos endpoints POST pendientes, no para la extracción normal.

> API no documentada ni soportada por Tipsi: puede cambiar sin aviso. Conviene pactar el
> acceso automatizado con ellos. Normalización de `data/tipsi/raw/*.json` a
> `tipsi_sales`/`tipsi_products` pendiente de calibrar.

## Scripts de análisis pendientes de portar

En `fondeo_kpis/scripts/` hay análisis completos (valoración DCF/traspaso, tesorería mensual
detallada, forecast calibrado, P&L mensual desde libro contable…) que se portarán cuando Dingui
tenga datos equivalentes. No se copian en vacío: dependen de la forma concreta de los datos.
