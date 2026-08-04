#!/usr/bin/env python
"""Stock teórico semanal de bebida = compras acumuladas − consumo acumulado.

Válido porque Dingui abrió de cero (stock inicial = 0). El consumo se estima de
Tipsi (copas/chupitos/botellas) + invitaciones de los cierres del gerente.

    uv run python scripts/stock_teorico.py

Supuestos (ajustables): copa = 5 cl de licor, chupito = 4 cl, botella reservado = 1
botella entera. Coste medio botella = media ponderada real de las facturas.
Da STOCK TEÓRICO: la diferencia con el recuento físico real = merma + derrames.
"""
import re
import pandas as pd

CL_COPA = 5 / 70      # fracción de botella 70cl por copa
CL_CHUP = 4 / 70
ROOT = __import__('pathlib').Path(__file__).resolve().parent.parent


def cargar_consumo():
    df = pd.read_parquet(ROOT / 'data/tipsi/lineas_tickets.parquet')
    df['dt'] = pd.to_datetime(df.dt, format='ISO8601')
    df['noche'] = (df['dt'] - pd.Timedelta(hours=8)).dt.date
    df['sem'] = pd.to_datetime(df.noche).dt.to_period('W-SUN')

    def g(a):
        if not isinstance(a, str):
            return 'x'
        s = a.strip().lower()
        if re.match(r'^copa', s):
            return 'copa'
        if s in ('chaman', 'tequila') or s.startswith('chup'):
            return 'chupito'
        # cortada/caña/entera = tirada de BARRIL; tercio/botellín/radler/desperados = botella 33cl
        if s in ('cortada', 'entera') or s.startswith('caña') or s.startswith('cana'):
            return 'cerv_barril'
        if s in ('tercio', 'botellin', 'radler', 'desperados') or 'tercio' in s or 'botellin' in s:
            return 'cerv_botellin'
        if s.startswith(('bot', 'bote', 'botell', 'reservado')) or 'botella' in s:
            return 'botella'
        return 'x'
    df['g'] = df.articulo.map(g)
    return df.groupby(['sem', 'g']).qty.sum().unstack(fill_value=0), df.noche.max()


def cargar_invitaciones():
    ci = pd.read_csv(ROOT / 'data/cierres_gerente/cierres_gerente.csv')
    ci['sem'] = pd.to_datetime(ci.fecha).dt.to_period('W-SUN')
    cols = ['inv_socios_copas', 'inv_personal_copas', 'inv_rpps_copas',
            'inv_socios_chupitos', 'inv_personal_chupitos']
    for c in cols:
        ci[c] = pd.to_numeric(ci[c], errors='coerce').fillna(0)
    inv = ci.groupby('sem').agg(
        copas=('inv_socios_copas', 'sum'), copas2=('inv_personal_copas', 'sum'),
        rpps=('inv_rpps_copas', 'sum'), chup=('inv_socios_chupitos', 'sum'), chup2=('inv_personal_chupitos', 'sum'))
    inv['copas_tot'] = inv.copas + inv.copas2 + inv.rpps
    inv['chup_tot'] = inv.chup + inv.chup2
    return inv


def main():
    cons, ult = cargar_consumo()
    inv = cargar_invitaciones()
    lin = pd.read_csv(ROOT / 'data/facturas/lineas_facturas.csv')
    lin['sem'] = pd.to_datetime(lin.fecha_factura, errors='coerce').dt.to_period('W-SUN')

    alc = lin[(lin.tipo_bebida == 'alcohol') & (lin.formato == 'botella')]
    compra_alc = alc.groupby('sem').unidades.sum()
    coste_bot = alc[alc.importe_eur > 0].importe_eur.sum() / alc[alc.importe_eur > 0].unidades.sum()

    barril = lin[(lin.tipo_bebida == 'cerveza') & (lin.formato == 'barril')].groupby('sem').unidades.sum()
    botellin = lin[(lin.tipo_bebida == 'cerveza') & (lin.formato == 'botellin')].groupby('sem').unidades.sum()

    sem_all = sorted(set(cons.index) | set(compra_alc.index) | set(inv.index) | set(barril.index))
    st_alc = st_bar = st_bot = 0.0
    rows = []
    for s in sem_all:
        copa = cons.get('copa', pd.Series()).get(s, 0) + inv.copas_tot.get(s, 0)
        chup = cons.get('chupito', pd.Series()).get(s, 0) + inv.chup_tot.get(s, 0)
        bots = cons.get('botella', pd.Series()).get(s, 0)
        cons_alc = copa * CL_COPA + chup * CL_CHUP + bots
        st_alc += compra_alc.get(s, 0) - cons_alc
        # barril: cortada ~0.20L + entera ~0.33L → ~0.25L medio, sobre barril 50L
        litros_barril = cons.get('cerv_barril', pd.Series()).get(s, 0) * 0.25
        st_bar += barril.get(s, 0) - litros_barril / 50
        # botellín: tercio/botellín/radler = 1 botella; compra en cajas de 24
        st_bot += botellin.get(s, 0) - cons.get('cerv_botellin', pd.Series()).get(s, 0) / 24
        rows.append({
            'semana': str(s)[-5:] + '→' + str(s)[:5] if False else str(s),
            'alc_compra': round(compra_alc.get(s, 0)), 'alc_consumo': round(cons_alc),
            'alc_stock': round(st_alc), 'alc_valor_€': round(st_alc * coste_bot),
            'barril_stock': round(st_bar, 1), 'botellin_cajas_stock': round(st_bot, 1),
        })
    t = pd.DataFrame(rows)
    pd.set_option('display.width', 220)
    print(f"Coste medio botella licor: {coste_bot:.2f} € | detalle Tipsi hasta {ult}\n")
    print(t.to_string(index=False))
    print(f"\nSTOCK ACTUAL (teórico): {t.alc_stock.iloc[-1]:.0f} botellas licor (~{t['alc_valor_€'].iloc[-1]:,.0f} €), "
          f"{t.barril_stock.iloc[-1]:.1f} barriles, {t.botellin_cajas_stock.iloc[-1]:.1f} cajas botellín")


if __name__ == '__main__':
    main()
