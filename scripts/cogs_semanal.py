# -*- coding: utf-8 -*-
"""COGS semanal de Dingui, dos familias: COPAS (alcohol+mixer) y CERVEZA.

Método (resumido):
 1. VENTA por producto: de los tickets de Tipsi (líneas), suma sin IVA.
 2. CONSUMO físico: nº de tragos vendidos (Tipsi) + invitaciones (parte del gerente).
 3. CONSUMO a coste (COGS): cada trago × su "cost card" (coste unitario real de factura).
 4. COMPRAS (pedidos): líneas de factura sin IVA, por familia.
 5. STOCK teórico acumulado = Σ compras − Σ COGS (válido: se abrió de stock 0).
"""
import pandas as pd, re, json

# ---------- COST CARDS (coste unitario, € sin IVA, derivado de facturas reales) ----------
C_BOT   = 13.09                 # botella licor 70cl (media ponderada real)
MIXER   = 0.55                  # 1 refresco/mixer por copa (tónica 0.4 / RedBull 1.2 / cola 0.3 → media)
HIELO   = 0.10
C_COPA  = 5/70*C_BOT + MIXER + HIELO   # copa = 5cl licor + mixer + hielo
C_CHUP  = 4/70*10.0             # chupito 4cl de licor barato (chamán ~10€/botella)
C_BOTE  = 22.0                  # botella reservado (blend champán/premium, ESTIMADO)
C_REFR  = 0.55                  # refresco vendido suelto
C_BARRIL_L = 168/50            # barril Cruzcampo 50L → €/L = 3.36
C_CORTADA = 0.20*C_BARRIL_L    # 0.67
C_ENTERA  = 0.33*C_BARRIL_L    # 1.11
C_TERCIO  = 1.10               # botellín 33cl (caja 24 / 26.4€)

def famtipsi(a):
    if not isinstance(a,str): return 'x'
    s=a.strip().lower()
    if re.match(r'^copa',s): return 'copa'
    if s in ('chaman','tequila') or s.startswith('chup'): return 'chupito'
    if s.startswith(('bot','bote','botell','reservado')) or 'botella' in s: return 'botella'
    if s.startswith(('refresco','agua','coca','red bull','tonica','seven','fanta','pepsi','nestea')): return 'refresco'
    if s in ('cortada',) or s.startswith(('caña','cana')): return 'cortada'
    if s=='entera': return 'entera'
    if s=='tercio' or 'tercio' in s or s in ('botellin','radler','desperados') or 'botellin' in s: return 'tercio'
    return 'x'

df=pd.read_parquet('data/tipsi/lineas_tickets.parquet')
df['dt']=pd.to_datetime(df.dt,format='ISO8601')
df['sem']=(pd.to_datetime((df['dt']-pd.Timedelta(hours=8)).dt.date)).dt.to_period('W-SUN')
df['f']=df.articulo.map(famtipsi)
U=df.groupby(['sem','f']).qty.sum().unstack(fill_value=0)
V=df.groupby(['sem','f']).subtotal.sum().unstack(fill_value=0)

ci=pd.read_csv('data/cierres_gerente/cierres_gerente.csv'); ci['sem']=pd.to_datetime(ci.fecha).dt.to_period('W-SUN')
for c in ['inv_socios_copas','inv_personal_copas','inv_rpps_copas','inv_socios_chupitos','inv_personal_chupitos','mercaderias_pct','total_caja']:
    ci[c]=pd.to_numeric(ci[c],errors='coerce').fillna(0)
inv=ci.groupby('sem').apply(lambda d: pd.Series({
    'icopa': d.inv_socios_copas.sum()+d.inv_personal_copas.sum()+d.inv_rpps_copas.sum(),
    'ichup': d.inv_socios_chupitos.sum()+d.inv_personal_chupitos.sum(),
    'merc_caja': (d.mercaderias_pct*d.total_caja).sum()/100 if d.total_caja.sum() else 0,
    'caja': d.total_caja.sum()}))

lin=pd.read_csv('data/facturas/lineas_facturas.csv'); lin['sem']=pd.to_datetime(lin.fecha_factura,errors='coerce').dt.to_period('W-SUN')
lin['fam']=lin.tipo_bebida.map(lambda t:'cerveza' if t=='cerveza' else ('copas' if t in ('alcohol','refresco','vino','agua') else 'otro'))
compra=lin[lin.categoria=='bebida'].groupby(['sem','fam']).importe_eur.sum().unstack(fill_value=0)

def gv(t,s,c): return t.get(c,pd.Series(dtype=float)).get(s,0) if s in getattr(t,'index',[]) else 0
sems=[s for s in sorted(set(U.index)|set(compra.index)|set(inv.index)) if str(s)>='2026-06-15']
st_copa=st_cerv=0; rows=[]
for s in sems:
    copa=gv(U,s,'copa'); chup=gv(U,s,'chupito'); bote=gv(U,s,'botella'); refr=gv(U,s,'refresco')
    cort=gv(U,s,'cortada'); ent=gv(U,s,'entera'); ter=gv(U,s,'tercio')
    icopa=inv.icopa.get(s,0) if s in inv.index else 0; ichup=inv.ichup.get(s,0) if s in inv.index else 0
    # --- COPAS (alcohol+mixer) ---
    v_copas=gv(V,s,'copa')+gv(V,s,'chupito')+gv(V,s,'botella')+gv(V,s,'refresco')
    cogs_copas=(copa+icopa)*C_COPA + (chup+ichup)*C_CHUP + bote*C_BOTE + refr*C_REFR
    comp_copas=compra.get('copas',pd.Series()).get(s,0) if 'copas' in compra else 0
    st_copa+=comp_copas-cogs_copas
    # --- CERVEZA ---
    v_cerv=gv(V,s,'cortada')+gv(V,s,'entera')+gv(V,s,'tercio')
    cogs_cerv=cort*C_CORTADA+ent*C_ENTERA+ter*C_TERCIO
    comp_cerv=compra.get('cerveza',pd.Series()).get(s,0) if 'cerveza' in compra else 0
    st_cerv+=comp_cerv-cogs_cerv
    rows.append({'sem':str(s),
        'cop_venta':round(v_copas),'cop_cogs':round(cogs_copas),'cop_pct':round(100*cogs_copas/v_copas,1) if v_copas else 0,
        'cop_compra':round(comp_copas),'cop_stock':round(st_copa),
        'cer_venta':round(v_cerv),'cer_cogs':round(cogs_cerv),'cer_pct':round(100*cogs_cerv/v_cerv,1) if v_cerv else 0,
        'cer_compra':round(comp_cerv),'cer_stock':round(st_cerv),
        'merc_gerente':round(inv.merc_caja.get(s,0)) if s in inv.index else 0})
t=pd.DataFrame(rows)
LAB={'2026-06-29/2026-07-05':'30/6–5/7','2026-07-06/2026-07-12':'6–12/7','2026-07-13/2026-07-19':'13–19/7',
     '2026-07-20/2026-07-26':'20–26/7','2026-07-27/2026-08-02':'27/7–2/8','2026-08-03/2026-08-09':'3–9/8'}
t['sem']=t['sem'].map(lambda x:LAB.get(x,x))
pd.set_option('display.width',240)
print("COST CARDS  copa={:.2f}  chupito={:.2f}  botella_reserv={:.0f}  refresco={:.2f}  |  cortada={:.2f}  entera={:.2f}  tercio={:.2f}".format(
    C_COPA,C_CHUP,C_BOTE,C_REFR,C_CORTADA,C_ENTERA,C_TERCIO))
print("\n===== COPAS (alcohol + refresco/mixer) =====")
print(t[['sem','cop_venta','cop_cogs','cop_pct','cop_compra','cop_stock']].to_string(index=False))
print("\n===== CERVEZA =====")
print(t[['sem','cer_venta','cer_cogs','cer_pct','cer_compra','cer_stock']].to_string(index=False))
print("\n===== CRUCE: mi COGS total vs mercaderías del gerente =====")
t['cogs_tot']=t.cop_cogs+t.cer_cogs
print(t[['sem','cogs_tot','merc_gerente']].to_string(index=False))
jul=t[t['sem'].isin(['30/6–5/7','6–12/7','13–19/7','20–26/7','27/7–2/8'])]
print(f"\nJULIO — COPAS: venta {jul.cop_venta.sum():,.0f} / COGS {jul.cop_cogs.sum():,.0f} ({100*jul.cop_cogs.sum()/jul.cop_venta.sum():.1f}%)")
print(f"JULIO — CERVEZA: venta {jul.cer_venta.sum():,.0f} / COGS {jul.cer_cogs.sum():,.0f} ({100*jul.cer_cogs.sum()/jul.cer_venta.sum():.1f}%)")
print(f"JULIO — COGS total {jul.cogs_tot.sum():,.0f} vs mercaderías gerente {jul.merc_gerente.sum():,.0f}")
json.dump(t.to_dict('records'),open('data/stock/cogs_semanal.json','w'),ensure_ascii=False)
