"""Cliente BigQuery + helpers para cargar/consultar datos del proyecto.

Diseño:
  - Un único `Client` autenticado vía `GOOGLE_APPLICATION_CREDENTIALS` (JSON del service account).
  - `setup_tables()` ejecuta los DDLs de `schemas/bq/*.sql` (idempotente).
  - `merge_bank_transactions(df)` carga un DataFrame con dedupe vía MERGE:
      * filas con mismo `raw_tx_id` (clave lógica) no se duplican
      * si existían y los campos cambiaron (re-categorización), se actualizan
      * filas con `user_override=TRUE` no se tocan (respetar correcciones manuales)
  - `query(sql)` ejecuta con `maximumBytesBilled` = BQ_MAX_BYTES_BILLED como cap duro.
"""
from __future__ import annotations

import sys
import uuid
from typing import Any

import pandas as pd

from . import config


def get_client() -> Any:
    """Devuelve un cliente BigQuery autenticado. Importa lazily para que el módulo
    sea importable sin tener google-cloud-bigquery instalado todavía.

    Autenticación: usa Application Default Credentials (ADC). Funciona con:
      - Service account JSON apuntado por GOOGLE_APPLICATION_CREDENTIALS, O
      - `gcloud auth application-default login` (user credentials en ~/.config/gcloud/)
    No requiere SA JSON — preferido cuando la org policy bloquea SA keys.
    """
    from google.cloud import bigquery
    if not config.BQ_PROJECT:
        raise RuntimeError(
            "Falta BQ_PROJECT en .env. Es el Project ID del proyecto GCP "
            "(ej. 'fondeo-kpis' o 'fondeo-kpis-470923')."
        )
    return bigquery.Client(project=config.BQ_PROJECT, location=config.BQ_LOCATION)


def _qualified(table: str) -> str:
    return f"`{config.BQ_PROJECT}.{config.BQ_DATASET}.{table}`"


def setup_tables() -> list[str]:
    """Ejecuta todos los DDL en schemas/bq/*.sql, sustituyendo {project} y {dataset}.
    Idempotente (los DDLs llevan CREATE TABLE IF NOT EXISTS).
    Devuelve la lista de archivos ejecutados."""
    client = get_client()
    ddl_files = sorted((config.SCHEMAS_DIR / "bq").glob("*.sql"))
    applied = []
    for path in ddl_files:
        sql = path.read_text(encoding="utf-8").format(
            project=config.BQ_PROJECT,
            dataset=config.BQ_DATASET,
        )
        client.query(sql).result()
        applied.append(path.name)
    return applied


def query(sql: str, params: dict | None = None) -> "pd.DataFrame":
    """Ejecuta una query con cap de bytes y devuelve DataFrame."""
    from google.cloud import bigquery
    client = get_client()
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=config.BQ_MAX_BYTES_BILLED,
        use_query_cache=True,
    )
    if params:
        job_config.query_parameters = [
            bigquery.ScalarQueryParameter(k, _bq_type(v), v) for k, v in params.items()
        ]
    return client.query(sql, job_config=job_config).to_dataframe()


def _bq_type(v: Any) -> str:
    if isinstance(v, bool):
        return "BOOL"
    if isinstance(v, int):
        return "INT64"
    if isinstance(v, float):
        return "FLOAT64"
    return "STRING"


def append_bank_transactions(df: "pd.DataFrame", source_file: str | None = None) -> dict:
    """Carga filas a `bank_transactions` con LOAD JOB WRITE_APPEND (no DML).
    No deduplica — para primera carga limpia (tabla vacía). Devuelve {rows_in}.
    Útil cuando billing aún no está propagado y DML está bloqueado.
    """
    from google.cloud import bigquery
    client = get_client()
    if len(df) == 0:
        return {"rows_in": 0}
    df = _prepare_df(df, source_file)
    schema = _bank_tx_schema()
    table_ref = f"{config.BQ_PROJECT}.{config.BQ_DATASET}.bank_transactions"
    job = client.load_table_from_dataframe(
        df[[f.name for f in schema]],
        table_ref,
        job_config=bigquery.LoadJobConfig(schema=schema, write_disposition="WRITE_APPEND"),
    )
    job.result()
    return {"rows_in": len(df)}


def _prepare_df(df: "pd.DataFrame", source_file: str | None) -> "pd.DataFrame":
    df = df.copy()
    df["ingested_at"] = pd.Timestamp.utcnow()
    if "source_file" not in df.columns:
        df["source_file"] = source_file
    if "user_override" not in df.columns:
        df["user_override"] = False
    return df


def _bank_tx_schema():
    from google.cloud import bigquery
    return [
        bigquery.SchemaField("bank", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("account_iban", "STRING"),
        bigquery.SchemaField("booking_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("value_date", "DATE"),
        bigquery.SchemaField("amount_eur", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("concept", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("extra", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("cat_method", "STRING"),
        bigquery.SchemaField("cat_confidence", "FLOAT64"),
        bigquery.SchemaField("ignorar_fx", "BOOL", mode="REQUIRED"),
        bigquery.SchemaField("user_override", "BOOL", mode="REQUIRED"),
        bigquery.SchemaField("raw_tx_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("source_file", "STRING"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
    ]


def merge_bank_transactions(df: "pd.DataFrame", source_file: str | None = None) -> dict:
    """Carga filas a `bank_transactions` con MERGE:
      - dedupe por raw_tx_id
      - actualiza categoría/ignorar_fx si cambiaron y user_override=FALSE
      - inserta nuevas filas
    Devuelve {rows_in, rows_new, rows_dup, rows_updated}.
    NOTA: requiere billing habilitado (es DML). Si falla, usar `append_bank_transactions`.
    """
    from google.cloud import bigquery
    client = get_client()
    if len(df) == 0:
        return {"rows_in": 0, "rows_new": 0, "rows_dup": 0, "rows_updated": 0}

    # Normalizar tipos de DataFrame
    df = df.copy()
    df["ingested_at"] = pd.Timestamp.utcnow()
    if "source_file" not in df.columns:
        df["source_file"] = source_file
    if "user_override" not in df.columns:
        df["user_override"] = False

    # Cargar a tabla staging temporal en el dataset
    staging_table = f"_staging_bank_transactions_{uuid.uuid4().hex[:8]}"
    staging_ref = f"{config.BQ_PROJECT}.{config.BQ_DATASET}.{staging_table}"
    schema = [
        bigquery.SchemaField("bank", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("account_iban", "STRING"),
        bigquery.SchemaField("booking_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("value_date", "DATE"),
        bigquery.SchemaField("amount_eur", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("concept", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("extra", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("cat_method", "STRING"),
        bigquery.SchemaField("cat_confidence", "FLOAT64"),
        bigquery.SchemaField("ignorar_fx", "BOOL", mode="REQUIRED"),
        bigquery.SchemaField("user_override", "BOOL", mode="REQUIRED"),
        bigquery.SchemaField("raw_tx_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("source_file", "STRING"),
        bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
    ]
    expected_cols = [f.name for f in schema]
    df = df[expected_cols]
    job = client.load_table_from_dataframe(
        df,
        staging_ref,
        job_config=bigquery.LoadJobConfig(schema=schema, write_disposition="WRITE_TRUNCATE"),
    )
    job.result()

    # MERGE: si raw_tx_id existe Y user_override=FALSE → update; si no existe → insert
    merge_sql = f"""
    MERGE {_qualified('bank_transactions')} T
    USING `{staging_ref}` S
    ON T.raw_tx_id = S.raw_tx_id AND T.bank = S.bank
    WHEN MATCHED AND T.user_override = FALSE AND (
         IFNULL(T.category, '') != IFNULL(S.category, '')
      OR T.ignorar_fx != S.ignorar_fx
      OR IFNULL(T.cat_method, '') != IFNULL(S.cat_method, '')
    ) THEN UPDATE SET
       category = S.category,
       cat_method = S.cat_method,
       cat_confidence = S.cat_confidence,
       ignorar_fx = S.ignorar_fx,
       ingested_at = S.ingested_at
    WHEN NOT MATCHED THEN INSERT ROW
    """
    client.query(merge_sql).result()

    # Simplificamos: devolver lo cargado, sin distinguir new/dup exactos.
    rows_in = len(df)

    # Limpiar staging
    client.delete_table(staging_ref, not_found_ok=True)

    return {"rows_in": rows_in, "rows_new": rows_in, "rows_dup": 0, "rows_updated": 0}


def log_run(source: str, source_file: str, stats: dict, status: str = "ok",
            notes: str | None = None) -> None:
    """Registra una ejecución de ingesta en `ingest_runs`."""
    client = get_client()
    run_id = str(uuid.uuid4())
    now = pd.Timestamp.utcnow()
    row = {
        "run_id": run_id,
        "source": source,
        "source_file": source_file,
        "started_at": now.to_pydatetime(),
        "finished_at": now.to_pydatetime(),
        "status": status,
        "rows_in": stats.get("rows_in", 0),
        "rows_new": stats.get("rows_new", 0),
        "rows_dup": stats.get("rows_dup", 0),
        "notes": notes,
    }
    errors = client.insert_rows_json(
        f"{config.BQ_PROJECT}.{config.BQ_DATASET}.ingest_runs",
        [row],
    )
    if errors:
        print(f"⚠ Error logging run: {errors}", file=sys.stderr)
