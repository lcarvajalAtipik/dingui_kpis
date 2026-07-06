-- Log de ingestas, para auditar carga/recarga de archivos.

CREATE TABLE IF NOT EXISTS `{project}.{dataset}.ingest_runs` (
  run_id        STRING    NOT NULL OPTIONS(description="UUID de la ingesta"),
  source        STRING    NOT NULL OPTIONS(description="bancos | contabilidad | tipsi | forecast | nominas"),
  source_file   STRING    OPTIONS(description="Archivo concreto si aplica"),
  started_at    TIMESTAMP NOT NULL,
  finished_at   TIMESTAMP,
  status        STRING    NOT NULL OPTIONS(description="running | ok | error"),
  rows_in       INT64     OPTIONS(description="Filas leídas del origen"),
  rows_new      INT64     OPTIONS(description="Filas nuevas insertadas (post-dedupe)"),
  rows_dup      INT64     OPTIONS(description="Filas duplicadas ignoradas"),
  notes         STRING    OPTIONS(description="Mensajes/errores")
)
OPTIONS(description="Log de cargas a BQ — para idempotencia y auditoría.");
