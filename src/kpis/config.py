"""Configuración central — carga `.env` y expone rutas y credenciales."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

DB_PATH = REPO_ROOT / "db" / "kpis.sqlite"
DATA_DIR = REPO_ROOT / "data"
OUTPUTS_DIR = REPO_ROOT / "outputs"
SCHEMAS_DIR = REPO_ROOT / "schemas"

# Tipsi (PoS) — API interna (backend-green.tipsipro.com): login Basic → cookie de sesión.
TIPSI_EMAIL = os.getenv("TIPSI_EMAIL")
TIPSI_PASSWORD = os.getenv("TIPSI_PASSWORD")
TIPSI_API_BASE = os.getenv("TIPSI_API_BASE")
# brandId/localId del establecimiento (se autodetectan; fijar solo para saltarse la detección).
TIPSI_BRAND_ID = os.getenv("TIPSI_BRAND_ID")
TIPSI_LOCAL_ID = os.getenv("TIPSI_LOCAL_ID")

# Google Cloud BigQuery
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT = os.getenv("BQ_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET", "dingui_kpis")
BQ_LOCATION = os.getenv("BQ_LOCATION", "EU")
BQ_MAX_BYTES_BILLED = int(os.getenv("BQ_MAX_BYTES_BILLED", str(100 * 1024 * 1024)))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
