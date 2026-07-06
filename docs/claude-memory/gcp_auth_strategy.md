---
name: gcp-auth-strategy
description: "Auth a GCP/BigQuery — usar ADC con gcloud (no SA JSON keys, bloqueadas por org policy). Proyecto/dataset BQ de Dingui por crear."
metadata:
  type: reference
---

Misma estrategia que en fondeo_kpis (la org de Workspace del usuario tiene `iam.disableServiceAccountKeyCreation` activada → no se pueden crear JSON keys de service accounts):

**Application Default Credentials (ADC)** vía `gcloud auth application-default login`.

- El código (`src/kpis/bq.py`) usa `bigquery.Client(project=config.BQ_PROJECT)` que resuelve credenciales de `~/.config/gcloud/application_default_credentials.json`.
- `.env` solo necesita `BQ_PROJECT` (y opcionalmente `BQ_DATASET`, default `dingui_kpis`).

**Pendiente decidir con el usuario:** ¿dataset `dingui_kpis` dentro del mismo proyecto GCP de Fondeo, o proyecto GCP nuevo? Ambas valen; misma auth. Luego `uv run python scripts/setup_bq.py` crea las tablas.

**Si falla con "could not automatically determine credentials"** → `gcloud auth application-default login`.

Relacionado: [[reference-fondeo-repo]].
