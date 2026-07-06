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

# Tipsi (PoS) — mecanismo de acceso por confirmar (API vs exports del back office)
TIPSI_API_TOKEN = os.getenv("TIPSI_API_TOKEN")
TIPSI_API_USER = os.getenv("TIPSI_API_USER")
TIPSI_API_BASE = os.getenv("TIPSI_API_BASE")

# Google Cloud BigQuery
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT = os.getenv("BQ_PROJECT")
BQ_DATASET = os.getenv("BQ_DATASET", "dingui_kpis")
BQ_LOCATION = os.getenv("BQ_LOCATION", "EU")
BQ_MAX_BYTES_BILLED = int(os.getenv("BQ_MAX_BYTES_BILLED", str(100 * 1024 * 1024)))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
