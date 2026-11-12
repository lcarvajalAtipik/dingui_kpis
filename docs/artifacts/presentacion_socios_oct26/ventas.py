import csv, datetime as dt, collections, json
r=list(csv.DictReader(open('data/cierres_gerente/cierres_gerente.csv')))
f=lambda x: float(x) if x not in ('',None) else 0.0
rows=[(dt.date.fromisoformat(x['fecha']), f(x['total_caja']), f(x['total_efectivo']), f(x['fourvenues']), f(x['gasto_personal_eur'])) for x in r]
jul=sum(t for d,t,*_ in rows if d.month==7); ago=sum(t for d,t,*_ in rows if d.month==8)
print('jul',round(jul,2),'ago1-26',round(ago,2),'resid 27-29', round(351725-ago,2))
print('efectivo jul',round(sum(e for d,t,e,*_ in rows if d.month==7),2),'ago',round(sum(e for d,t,e,*_ in rows if d.month==8),2))
print('personal jul',round(sum(p for d,t,e,fv,p in rows if d.month==7),2),'ago',round(sum(p for d,t,e,fv,p in rows if d.month==8),2), 'jun', sum(p for d,t,e,fv,p in rows if d.month==6))
print('FV jul',sum(fv for d,t,e,fv,p in rows if d.month==7),'ago',sum(fv for d,t,e,fv,p in rows if d.month==8))
res=351725-ago
nights={d:t for d,t,*_ in rows}
nights[dt.date(2026,8,27)]=3700
rest=res-3700
nights[dt.date(2026,8,28)]=rest/2; nights[dt.date(2026,8,29)]=rest/2
wk=collections.OrderedDict()
for d in sorted(nights):
    m=d-dt.timedelta(days=d.weekday()); wk.setdefault(m,[0,0]); wk[m][0]+=nights[d]; wk[m][1]+=1
for m,(t,n) in wk.items(): print(m, m+dt.timedelta(6), round(t), n, round(t/n))
print('total', round(sum(nights.values())))
dias=['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
by=collections.defaultdict(list)
for d,t in nights.items():
    if d in (dt.date(2026,8,28),dt.date(2026,8,29)): continue
    by[d.weekday()].append((t,d))
for k in sorted(by):
    v=by[k]; mx=max(v); print(dias[k], len(v), round(sum(t for t,_ in v)/len(v)), round(mx[0]), mx[1], 'desde15/07:', round(sum(t for t,d in v if d>=dt.date(2026,7,15))/max(1,len([1 for t,d in v if d>=dt.date(2026,7,15)]))))
