-- Esquema canónico v1 (Dingui). Evolucionará a medida que conectemos cada fuente.
-- Convenciones:
--   * Importes en EUR, signo positivo = entrada/ingreso, negativo = salida/gasto.
--   * Fechas como TEXT ISO-8601 (YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS) — SQLite lo prefiere.
--   * `source_doc` rastrea de dónde salió el dato (path al PDF, id de transacción, etc).

PRAGMA foreign_keys = ON;

-- ============================================================================
-- P&L: líneas de cuenta de resultados (contabilidad real + forecast)
-- ============================================================================
CREATE TABLE IF NOT EXISTS pnl_lines (
    id              INTEGER PRIMARY KEY,
    source          TEXT NOT NULL CHECK (source IN ('contabilidad', 'forecast', 'manual')),
    period_year     INTEGER NOT NULL,
    period_month    INTEGER NOT NULL CHECK (period_month BETWEEN 1 AND 12),
    account_code    TEXT,
    account_name    TEXT NOT NULL,
    category        TEXT NOT NULL,    -- ingresos, coste_ventas, personal, alquiler, suministros, marketing, financieros, impuestos, otros
    subcategory     TEXT,
    amount_eur      REAL NOT NULL,
    source_doc      TEXT,
    ingested_at     TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (source, period_year, period_month, account_code, account_name)
);
CREATE INDEX IF NOT EXISTS idx_pnl_period   ON pnl_lines (period_year, period_month);
CREATE INDEX IF NOT EXISTS idx_pnl_category ON pnl_lines (category);

-- ============================================================================
-- Bancos: movimientos crudos. Dingui opera con CaixaBank; si se abre otra
-- cuenta en otro banco, ampliar el CHECK y añadir parser en ingest/bancos.py.
-- ============================================================================
CREATE TABLE IF NOT EXISTS bank_transactions (
    id              INTEGER PRIMARY KEY,
    bank            TEXT NOT NULL CHECK (bank IN ('caixa')),
    account_iban    TEXT NOT NULL,
    booking_date    TEXT NOT NULL,    -- YYYY-MM-DD
    value_date      TEXT NOT NULL,
    amount_eur      REAL NOT NULL,    -- positivo = entrada, negativo = salida
    currency        TEXT NOT NULL DEFAULT 'EUR',
    concept         TEXT NOT NULL,
    counterpart     TEXT,             -- contrapartida si la conocemos
    category        TEXT,             -- categorización posterior (proveedor, nómina, impuestos…)
    raw_tx_id       TEXT,             -- id natural del banco para dedupe
    source          TEXT NOT NULL CHECK (source IN ('gocardless', 'manual_csv')),
    ingested_at     TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (bank, account_iban, raw_tx_id)
);
CREATE INDEX IF NOT EXISTS idx_bank_tx_date ON bank_transactions (booking_date);
CREATE INDEX IF NOT EXISTS idx_bank_tx_bank ON bank_transactions (bank, account_iban);

-- ============================================================================
-- Plantilla y nóminas
-- ============================================================================
CREATE TABLE IF NOT EXISTS employees (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    role        TEXT NOT NULL,        -- rol libre: cocina, sala, barra, puerta… (estructura por confirmar)
    hire_date   TEXT,
    end_date    TEXT,
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive'))
);

CREATE TABLE IF NOT EXISTS nominas (
    id              INTEGER PRIMARY KEY,
    employee_id     INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    period_year     INTEGER NOT NULL,
    period_month    INTEGER NOT NULL CHECK (period_month BETWEEN 1 AND 12),
    gross_eur       REAL NOT NULL,
    net_eur         REAL NOT NULL,
    ss_company_eur  REAL NOT NULL,    -- coste SS empresa
    ss_employee_eur REAL NOT NULL,    -- retención SS trabajador
    irpf_eur        REAL NOT NULL,
    total_cost_eur  REAL NOT NULL,    -- coste total empresa (bruto + SS empresa)
    source_doc      TEXT,
    ingested_at     TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (employee_id, period_year, period_month)
);

-- ============================================================================
-- Tipsi (PoS): catálogo y ventas
-- ============================================================================
CREATE TABLE IF NOT EXISTS tipsi_products (
    id                  INTEGER PRIMARY KEY,
    tipsi_id            TEXT NOT NULL UNIQUE,
    name                TEXT NOT NULL,
    family              TEXT,
    current_price_eur   REAL,
    cost_eur            REAL,         -- coste escandallo (materia prima)
    active              INTEGER NOT NULL DEFAULT 1,
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tipsi_sales (
    id              INTEGER PRIMARY KEY,
    tipsi_id        TEXT NOT NULL UNIQUE,     -- id de la línea en Tipsi (dedupe)
    ticket_id       TEXT NOT NULL,
    closed_at       TEXT NOT NULL,            -- ISO timestamp del cierre del ticket
    product_id      TEXT,                     -- FK lógica a tipsi_products.tipsi_id
    product_name    TEXT NOT NULL,            -- snapshot por si el producto desaparece del catálogo
    family          TEXT,
    qty             REAL NOT NULL,
    unit_price_eur  REAL NOT NULL,
    discount_eur    REAL NOT NULL DEFAULT 0,
    total_eur       REAL NOT NULL,            -- después de descuento, antes de IVA
    vat_rate        REAL,
    ingested_at     TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_tipsi_sales_date    ON tipsi_sales (closed_at);
CREATE INDEX IF NOT EXISTS idx_tipsi_sales_product ON tipsi_sales (product_id);

-- ============================================================================
-- Metadatos de ingestas (para saber cuándo se cargó cada fuente y desde dónde)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ingest_runs (
    id          INTEGER PRIMARY KEY,
    source      TEXT NOT NULL,        -- tipsi, bancos, contabilidad, forecast_sheet, nominas
    started_at  TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    status      TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running', 'ok', 'error')),
    rows_in     INTEGER,
    rows_out    INTEGER,
    notes       TEXT
);
