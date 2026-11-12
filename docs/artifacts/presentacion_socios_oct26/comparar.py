# Declarado (gestoría v4 08/10, desglose 13/10) por nuestras partidas, + lo que falta hasta 31/12; y nuestro real con Stima como gasto
K=['ventas','acuerdos','compras','personal','djs','rrpp','alquiler','fijos','marketing','extra','financiero','stima','obra_equipo','legal_tipsi','fondeo']
dec={'ventas':1604.82+203475.69+319750.15+120,'acuerdos':14125+400+681.82+401.50,'compras':-123236.42-401.50-3558.95,'personal':-63351.23,
 'djs':-9237.69+752.69,'rrpp':-12539.56,'alquiler':-16370.58,'fijos':-5971.68,'marketing':-6517.00,'extra':-6430.66+3558.95-752.69,'financiero':-1191.43,
 'stima':-22100,'obra_equipo':-11687.49,'legal_tipsi':-2103.30-949.87,'fondeo':-884.57}
pend={  # lo que falta en la contabilidad hasta 31/12 (estimado)
 'acuerdos':[('Rappel Pernod Ricard (sin facturar aún)',6200)],
 'alquiler':[('Alquiler oct–dic (3 × 1.916,68)',-5750.04)],
 'fijos':[('Luz del verano: recibos Elega sin factura (6.722/1,21 − 2.891)',-(6722.35/1.21-2890.78)),('Seguros Mapfre y Multiservicios (no contabilizados)',-1265),('Fijos y luz oct–dic',-(3*395+3*400/1.21)),('Recibo extra AS Castilla',-480)],
 'djs':[('Facturas de DJs de jul–ago aún no contabilizadas',-(13630-2940-8485.0))],
 'marketing':[('Barter agosto (sin contabilizar)',-500)],
 'financiero':[('Comisiones bancarias, TPV y aval',-(191+307+225+74.92+167.10))],

 'fondeo':[('Anular gastos de Fondeo',884.57)],
}
ours={'ventas':523225.84+1604.82+120,'acuerdos':21808.32,'compras':-111953.0-10993.0-1655.0,'personal':-97121.0,'djs':-13630,
 'rrpp':-12539.56,'alquiler':-21172.0,'fijos':-13476.0,'marketing':-6000-1017,'extra':-7584.0-403.0-752.69,'financiero':-1264.0-1746.59,
 'stima':-22100,'obra_equipo':0,'legal_tipsi':0,'fondeo':0}
d31={k:dec[k]+sum(v for _,v in pend.get(k,[])) for k in K}
E=lambda d:sum(d[k] for k in K)
amD=-25978.53; amO=-(19750-22100/10/2)
print(f"{'partida':12s} {'decl0810':>10s} {'pend':>9s} {'decl3112':>10s} {'nuestro':>10s} {'dif':>9s}")
for k in K: print(f"{k:12s} {dec[k]:10.0f} {d31[k]-dec[k]:9.0f} {d31[k]:10.0f} {ours[k]:10.0f} {ours[k]-d31[k]:9.0f}")
print('EBITDA', round(E(dec)), round(E(d31)), round(E(ours)), round(E(ours)-E(d31)))
print('amort', amD, round(amO)); rD=E(d31)+amD; rO=E(ours)+amO
print('resultado', round(E(dec)+amD), round(rD), round(rO))
isD=0.15*rD; print('IS (15% s/ declarado 31/12)', round(isD), 'neto declarado', round(rD-isD), 'neto nuestro', round(rO-isD))
