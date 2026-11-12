const m = require('/Users/luismdecarvajal/Desktop/dingui_kpis/docs/artifacts/dingui_model.js');
const r = m.modelo(m.P); const V=r.V;
const S=(k,a,b)=>V[k].slice(a,b+1).reduce((x,y)=>x+y,0);
const per={pre:[0,5],tem:[6,7],cie:[8,11]};
const rows={};
for (const k of ["ventas","acuerdos","rappels","cogs","personal","djs","rrpp","alquiler","fijos","marketing","extra","financiero","amort"]) rows[k]={pre:S(k,0,5),tem:S(k,6,7),cie:S(k,8,11)};
// ajustes v9
rows.acuerdos.cie += -17000+14125;              // Schweppes 14.125 (30/09) en vez de Pepsi 17.000
rows.cogs.tem += rows.cogs.cie; rows.cogs.cie=0; // devoluciones de fin de temporada a la temporada
rows.cogs.tem += 2032.09/1.10;                    // abono Coca-Cola 25/09
rows.fijos.tem += -6722.35/1.21;                  // luz Elega (recibos sep-oct)
rows.fijos.cie += -580.80/1.21 - 3*400/1.21;      // AS Castilla extra + luz oct-dic estimada
rows.extra.cie += -(82.28+119.79)/1.21;
rows.financiero.cie += -(225+74.92+167.10);
const ac = {pre:0,tem:rows.acuerdos.tem+rows.rappels.tem,cie:rows.acuerdos.cie+rows.rappels.cie};
const T=o=>o.pre+o.tem+o.cie;
const marg={}, eb={}, res={};
for (const p of ["pre","tem","cie"]){ marg[p]=rows.ventas[p]+ac[p]+rows.cogs[p];
 eb[p]=marg[p]+rows.personal[p]+rows.djs[p]+rows.rrpp[p]+rows.alquiler[p]+rows.fijos[p]+rows.marketing[p]+rows.extra[p]+rows.financiero[p];
 res[p]=eb[p]+rows.amort[p]; }
const out=(n,o)=>console.log(n.padEnd(12), [o.pre,o.tem,o.cie,T(o)].map(x=>Math.round(x)).join('\t'), (100*T(o)/T(rows.ventas)).toFixed(1));
for (const k in rows) if(k!=="acuerdos"&&k!=="rappels") out(k,rows[k]);
out('acu+rap',ac); out('margen',marg); out('ebitda',eb); out('resultado',res);
const B=8523.03+(43435+4100-24348.11); const base=T(res)+B; const is=0.15*base;
console.log('B',Math.round(B),'base',Math.round(base),'IS',Math.round(is),'neto',Math.round(T(res)-is));
// previsión de liquidez
const fij=-(395+400), rent=-2319.18;
const f=[
 ['oct (16–31)', [['IRPF 3T, modelo 111 (20/10)',-1500]]],
 ['nov', [['Préstamo Cruzcampo, 1er tramo',30000],['Schweppes 14.125 + IVA (factura 30/09)',17091.25],['Rappel Pernod Ricard 6.200 + IVA',7502],['Licencia para la DR',-10000],['Bebida pendiente (Ipasur, Dilaso, Monbake)',-2588],['Alquiler Realmivo',rent],['Fijos y luz',fij]]],
 ['dic', [['Stima 21, último pago en efectivo',-4000],['Alquiler',rent],['Fijos y luz',fij]]],
 ['ene', [['Préstamo Cruzcampo, 2º tramo',10000],['Alquiler',rent],['Fijos y luz',fij]]],
 ['feb', [['Alquiler',rent],['Fijos y luz',fij]]],['mar', [['Alquiler',rent],['Fijos y luz',fij]]],['abr', [['Alquiler',rent],['Fijos y luz',fij]]],['may', [['Alquiler',rent],['Fijos y luz',fij]]],
 ['jun', [['Cobros temporada (50K ventas: TPV + Fourvenues)',50000*(145782+42525)/223641],['Compras pagadas en junio',-29832*50000/223641],['Personal (efectivo)',-13640*50000/223641],['Equipo y varios',-50000/1.1*0.0142*1.21],['Software, comisiones',-165-190*50000/223641],['Alquiler',rent],['Fijos y luz',fij]]],
];
let s=108619.24; for (const [mes,it] of f){ const n=it.reduce((a,b)=>a+b[1],0); s+=n; console.log(mes, Math.round(n), Math.round(s), it.map(x=>x[0]+' '+Math.round(x[1])).join(' | ')); }
