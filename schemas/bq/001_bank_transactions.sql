-- BigQuery DDL para `bank_transactions`. Se ejecuta vía scripts/setup_bq.py.
-- Convenciones:
--   * Importes en EUR, signo positivo = entrada/ingreso, negativo = salida/gasto.
--   * Fechas como DATE (no TIMESTAMP) — las fechas bancarias no llevan hora útil.
--   * `raw_tx_id` es un hash SHA1 corto (16 chars) para dedupe — UNIQUE lógico
--     vía MERGE en cada carga (BQ no soporta UNIQUE constraint duro).

CREATE TABLE IF NOT EXISTS `{project}.{dataset}.bank_transactions` (
  bank             STRING    NOT NULL OPTIONS(description="caixa (único banco de Dingui por ahora)"),
  account_iban     STRING    OPTIONS(description="IBAN español ES + 22 dígitos"),
  booking_date     DATE      NOT NULL OPTIONS(description="Fecha de operación"),
  value_date       DATE      OPTIONS(description="Fecha valor"),
  amount_eur       FLOAT64   NOT NULL OPTIONS(description="Positivo = entrada, negativo = salida"),
  concept          STRING    NOT NULL OPTIONS(description="Concepto principal del movimiento"),
  extra            STRING    OPTIONS(description="Info adicional (columna 'Más datos' de CaixaBank)"),
  category         STRING    OPTIONS(description="Categoría P&L según el categorizador"),
  cat_method       STRING    OPTIONS(description="exact | ambiguous_resolved | hardcoded | rappel_brand | fuzzy | ingreso_transferencia_default | unmatched"),
  cat_confidence   FLOAT64   OPTIONS(description="Confianza 0-1 del categorizador"),
  ignorar_fx       BOOL      NOT NULL OPTIONS(description="TRUE = excluir del cashflow (política por definir para Dingui)"),
  user_override    BOOL      NOT NULL OPTIONS(description="TRUE si el usuario sobrescribió manualmente; no se re-categoriza"),
  raw_tx_id        STRING    NOT NULL OPTIONS(description="Hash SHA1[:16] para dedupe"),
  source_file      STRING    OPTIONS(description="Nombre del archivo de origen"),
  ingested_at      TIMESTAMP NOT NULL OPTIONS(description="Cuándo se cargó esta fila a BQ")
)
PARTITION BY DATE_TRUNC(booking_date, MONTH)
CLUSTER BY bank, category
OPTIONS(
  description="Movimientos bancarios normalizados + categorización P&L. Partitioned por mes, clustered por banco y categoría para queries rápidas."
);
