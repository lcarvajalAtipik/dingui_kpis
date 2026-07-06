"""Genera reporte completo de liquidez + gráficos PNG en outputs/.

Uso: `uv run python scripts/liquidity_report.py`
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

from kpis import config
from kpis.analysis import liquidity

OUT = config.OUTPUTS_DIR
OUT.mkdir(parents=True, exist_ok=True)


def fmt_eur(x):
    return f"{x:>14,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def section(title: str) -> None:
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print("=" * 80)


def chart_saldo_acumulado(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(12, 6))
    for bank in df["bank"].unique():
        sub = df[df["bank"] == bank].sort_values("mes")
        ax.plot(sub["mes"], sub["saldo_acum"], marker="o", linewidth=2, label=bank.capitalize())
    ax.set_title("Saldo acumulado por banco (cashflow running)", fontsize=14)
    ax.set_ylabel("€")
    ax.axhline(0, color="black", linewidth=0.5, alpha=0.5)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f} €"))
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT / "01_saldo_acumulado.png", dpi=130)
    plt.close(fig)


def chart_ingresos_vs_gastos(df_all: pd.DataFrame, df_op: pd.DataFrame) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 9), sharex=True)
    for ax, df, title in [(ax1, df_all, "Todo (incluye apertura/préstamos/aportaciones)"),
                          (ax2, df_op, "Operativo recurrente (sin one-off ni financiero)")]:
        df = df.sort_values("mes")
        ax.bar(df["mes"], df["ingresos"], width=20, label="Ingresos", color="#3a7d44", alpha=0.85)
        ax.bar(df["mes"], df["gastos"], width=20, label="Gastos", color="#c1121f", alpha=0.85)
        ax.plot(df["mes"], df["neto"], color="black", marker="o", linewidth=1.5, label="Neto")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(title, fontsize=12)
        ax.set_ylabel("€/mes")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper left", fontsize=9)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    fig.suptitle("Ingresos vs Gastos mensuales (Dingui)", fontsize=14, y=0.995)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUT / "02_ingresos_vs_gastos.png", dpi=130)
    plt.close(fig)


def chart_categorias_pie(df: pd.DataFrame) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    # Entradas
    ent = df[df["total_eur"] > 0].copy().sort_values("total_eur", ascending=False).head(8)
    ax1.pie(ent["total_eur"], labels=ent["category"], autopct="%1.0f%%", startangle=90)
    ax1.set_title(f"Entradas ({ent['total_eur'].sum():,.0f}€ top 8)", fontsize=12)
    # Salidas
    sal = df[df["total_eur"] < 0].copy()
    sal["abs"] = sal["total_eur"].abs()
    sal = sal.sort_values("abs", ascending=False).head(10)
    ax2.pie(sal["abs"], labels=sal["category"], autopct="%1.0f%%", startangle=90)
    ax2.set_title(f"Salidas ({-sal['total_eur'].sum():,.0f}€ top 10)", fontsize=12)
    fig.suptitle("Distribución de cashflow por categoría", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "03_categorias_pie.png", dpi=130)
    plt.close(fig)


def chart_heatmap_categorias(df: pd.DataFrame) -> None:
    """Heatmap categoría × mes con importes."""
    df = df.copy()
    df["mes_str"] = pd.to_datetime(df["mes"]).dt.strftime("%Y-%m")
    pivot = df.pivot_table(index="category", columns="mes_str", values="total_eur",
                           aggfunc="sum", fill_value=0)
    # Ordenar categorías por abs total descendente
    pivot["abs_sum"] = pivot.abs().sum(axis=1)
    pivot = pivot.sort_values("abs_sum", ascending=False).drop(columns="abs_sum").head(15)
    fig, ax = plt.subplots(figsize=(max(12, len(pivot.columns) * 0.4), 8))
    im = ax.imshow(pivot.values, aspect="auto", cmap="RdYlGn", vmin=-15000, vmax=15000)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)
    ax.set_title("Cashflow por categoría × mes (top 15 categorías)", fontsize=13)
    fig.colorbar(im, ax=ax, label="€/mes")
    fig.tight_layout()
    fig.savefig(OUT / "04_heatmap_categorias.png", dpi=130)
    plt.close(fig)


def main() -> None:
    # === 1. Saldo neto y por banco ===
    section("1. Saldo neto agregado (suma de todos los movimientos)")
    saldo_b = liquidity.saldo_neto_por_banco()
    print(saldo_b.to_string(index=False))
    total = saldo_b["saldo_neto_eur"].sum()
    print(f"\n  TOTAL agregado: {fmt_eur(total)}")

    # === 2. Cashflow mensual acumulado ===
    section("2. Cashflow acumulado por banco × mes")
    sal_mes = liquidity.saldo_mensual_acumulado()
    print(sal_mes.tail(15).to_string(index=False))
    chart_saldo_acumulado(sal_mes)
    print(f"\n  Gráfico → {OUT / '01_saldo_acumulado.png'}")

    # === 3. Ingresos vs gastos por mes ===
    section("3. Ingresos vs gastos por mes (todo)")
    iv_all = liquidity.ingresos_vs_gastos_mes()
    print(iv_all.tail(15).to_string(index=False))

    section("4. Operación recurrente (sin apertura/préstamos/aportaciones)")
    iv_op = liquidity.ingresos_vs_gastos_mes_excluyendo_one_off()
    print(iv_op.tail(15).to_string(index=False))
    chart_ingresos_vs_gastos(iv_all, iv_op)
    print(f"\n  Gráfico → {OUT / '02_ingresos_vs_gastos.png'}")

    # === 5. Totales por categoría ===
    section("5. Totales por categoría (ordenado por |importe|)")
    tot_cat = liquidity.totales_por_categoria()
    print(tot_cat.to_string(index=False))
    chart_categorias_pie(tot_cat)
    print(f"\n  Gráfico → {OUT / '03_categorias_pie.png'}")

    # === 6. Heatmap categoría × mes ===
    cm = liquidity.cashflow_por_categoria_mes()
    chart_heatmap_categorias(cm)
    print(f"\n  Heatmap → {OUT / '04_heatmap_categorias.png'}")

    # === 7. Alertas ===
    section("7. ALERTAS — Cuotas impagadas")
    imp = liquidity.cuotas_impagadas()
    if len(imp) == 0:
        print("  (ninguna detectada)")
    else:
        print(imp.to_string(index=False))

    section("8. ALERTAS — Meses con cashflow operativo crítico (< -5.000€)")
    crit = liquidity.meses_con_neto_critico(threshold=-5000)
    if len(crit) == 0:
        print("  (ninguno)")
    else:
        print(crit.to_string(index=False))


if __name__ == "__main__":
    main()
