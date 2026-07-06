"""Análisis de liquidez sobre `bank_transactions` en BigQuery.

Convenciones:
  - Cashflow / liquidez excluye `ignorar_fx = TRUE` (política por definir para Dingui).
  - Mes = primer día del mes (DATE_TRUNC).
  - Importes positivos = entradas, negativos = salidas.
"""
from __future__ import annotations

import pandas as pd

from .. import bq, config


TABLE = f"`{config.BQ_PROJECT}.{config.BQ_DATASET}.bank_transactions`"

# Categorías one-off de apertura y movimientos financiero-estructurales que
# distorsionan la vista "operativa recurrente". Ajustar cuando existan las
# categorías reales de Dingui (préstamos concretos, sponsorings, etc.).
ONE_OFF_CATEGORIES: tuple[str, ...] = (
    "Obra",
    "Fianza",
    "Aportación Socios",
    "Préstamos bancarios",
    "Primera Cuota Renting",
    "Movimiento entre cuentas",
)


def _one_off_sql_list() -> str:
    return ", ".join(f"'{c}'" for c in ONE_OFF_CATEGORIES)


# ============================================================================
# Saldos
# ============================================================================

def saldo_neto_por_banco() -> pd.DataFrame:
    """Suma de todos los movimientos por banco (= saldo neto desde el primer movimiento)."""
    return bq.query(f"""
        SELECT
          bank,
          MIN(booking_date) AS first_date,
          MAX(booking_date) AS last_date,
          COUNT(*) AS n_movs,
          ROUND(SUM(amount_eur), 2) AS saldo_neto_eur
        FROM {TABLE}
        WHERE NOT ignorar_fx
        GROUP BY bank
        ORDER BY bank
    """)


def saldo_mensual_acumulado() -> pd.DataFrame:
    """Saldo running por banco al cierre de cada mes (suma acumulada)."""
    return bq.query(f"""
        WITH monthly AS (
          SELECT
            bank,
            DATE_TRUNC(booking_date, MONTH) AS mes,
            SUM(amount_eur) AS cashflow_mes
          FROM {TABLE}
          WHERE NOT ignorar_fx
          GROUP BY bank, mes
        )
        SELECT
          bank,
          mes,
          ROUND(cashflow_mes, 2) AS cashflow_mes,
          ROUND(SUM(cashflow_mes) OVER (PARTITION BY bank ORDER BY mes), 2) AS saldo_acum
        FROM monthly
        ORDER BY mes, bank
    """)


# ============================================================================
# Cashflow por categoría
# ============================================================================

def cashflow_por_categoria_mes() -> pd.DataFrame:
    """Matriz categoría × mes con la suma de importes."""
    return bq.query(f"""
        SELECT
          category,
          DATE_TRUNC(booking_date, MONTH) AS mes,
          ROUND(SUM(amount_eur), 2) AS total_eur,
          COUNT(*) AS n_movs
        FROM {TABLE}
        WHERE NOT ignorar_fx
        GROUP BY category, mes
        ORDER BY mes, ABS(total_eur) DESC
    """)


def totales_por_categoria() -> pd.DataFrame:
    return bq.query(f"""
        SELECT
          category,
          COUNT(*) AS n_movs,
          ROUND(SUM(amount_eur), 2) AS total_eur,
          ROUND(SUM(IF(amount_eur > 0, amount_eur, 0)), 2) AS entradas_eur,
          ROUND(SUM(IF(amount_eur < 0, amount_eur, 0)), 2) AS salidas_eur
        FROM {TABLE}
        WHERE NOT ignorar_fx
        GROUP BY category
        ORDER BY ABS(total_eur) DESC
    """)


# ============================================================================
# Ingresos vs Gastos por mes
# ============================================================================

def ingresos_vs_gastos_mes() -> pd.DataFrame:
    return bq.query(f"""
        SELECT
          DATE_TRUNC(booking_date, MONTH) AS mes,
          ROUND(SUM(IF(amount_eur > 0, amount_eur, 0)), 2) AS ingresos,
          ROUND(SUM(IF(amount_eur < 0, amount_eur, 0)), 2) AS gastos,
          ROUND(SUM(amount_eur), 2) AS neto,
          COUNT(*) AS n_movs
        FROM {TABLE}
        WHERE NOT ignorar_fx
        GROUP BY mes
        ORDER BY mes
    """)


def ingresos_vs_gastos_mes_excluyendo_one_off() -> pd.DataFrame:
    """Mismo, excluyendo categorías one-off de apertura y financiero-estructurales."""
    return bq.query(f"""
        SELECT
          DATE_TRUNC(booking_date, MONTH) AS mes,
          ROUND(SUM(IF(amount_eur > 0, amount_eur, 0)), 2) AS ingresos,
          ROUND(SUM(IF(amount_eur < 0, amount_eur, 0)), 2) AS gastos,
          ROUND(SUM(amount_eur), 2) AS neto,
          COUNT(*) AS n_movs
        FROM {TABLE}
        WHERE NOT ignorar_fx
          AND category NOT IN ({_one_off_sql_list()})
        GROUP BY mes
        ORDER BY mes
    """)


# ============================================================================
# Alertas
# ============================================================================

def cuotas_impagadas() -> pd.DataFrame:
    return bq.query(f"""
        SELECT
          bank,
          booking_date,
          ROUND(amount_eur, 2) AS amount_eur,
          concept
        FROM {TABLE}
        WHERE LOWER(concept) LIKE '%impagada%'
          AND NOT ignorar_fx
        ORDER BY booking_date
    """)


def meses_con_neto_critico(threshold: float = -5000) -> pd.DataFrame:
    """Meses donde el cashflow neto operativo (sin one-off) fue muy negativo."""
    return bq.query(f"""
        WITH mensual AS (
          SELECT
            DATE_TRUNC(booking_date, MONTH) AS mes,
            SUM(amount_eur) AS neto
          FROM {TABLE}
          WHERE NOT ignorar_fx
            AND category NOT IN ({_one_off_sql_list()})
          GROUP BY mes
        )
        SELECT mes, ROUND(neto, 2) AS neto_operativo
        FROM mensual
        WHERE neto < {threshold}
        ORDER BY neto
    """)
