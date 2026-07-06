-- Tabla de forecast mensual por categoría.
-- Soporta múltiples escenarios (Break Even del user vs YoY automático).

CREATE TABLE IF NOT EXISTS `{project}.{dataset}.forecast_monthly` (
  year         INT64    NOT NULL,
  month_num    INT64    NOT NULL OPTIONS(description="1-12"),
  month_date   DATE     NOT NULL OPTIONS(description="primer día del mes (year-month-01)"),
  category     STRING   NOT NULL OPTIONS(description="categoría P&L (alineada con bank_transactions.category)"),
  amount_eur   FLOAT64  NOT NULL OPTIONS(description="importe esperado del mes (negativo=gasto, positivo=ingreso)"),
  scenario     STRING   NOT NULL OPTIONS(description="break_even | yoy | manual"),
  source_note  STRING   OPTIONS(description="origen/nota sobre cómo se calculó"),
  ingested_at  TIMESTAMP NOT NULL OPTIONS(description="set en cada insert")
)
PARTITION BY DATE_TRUNC(month_date, MONTH)
CLUSTER BY scenario, category;
