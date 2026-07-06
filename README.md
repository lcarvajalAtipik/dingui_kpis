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
| Tipsi (PoS) | Por confirmar (API o exports del back office) | Pendiente |
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

## Scripts de análisis pendientes de portar

En `fondeo_kpis/scripts/` hay análisis completos (valoración DCF/traspaso, tesorería mensual
detallada, forecast calibrado, P&L mensual desde libro contable…) que se portarán cuando Dingui
tenga datos equivalentes. No se copian en vacío: dependen de la forma concreta de los datos.
