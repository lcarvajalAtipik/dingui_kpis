import re, collections, csv
L=open('desglose.txt').read().split('\n')
recs=[]; cur=None
dre=re.compile(r'^(\d\d/\d\d/\d\d)\s+(\d{7}\s+)?(6\d{10})\s+(.*)$')
amt=re.compile(r'(-?\d{1,3}(?:\.\d{3})*,\d{2})')
for l in L:
    m=dre.match(l)
    if m:
        if cur: recs.append(cur)
        cur={'fecha':m.group(1),'doc':m.group(2),'cta':m.group(3),'txt':m.group(4)}
    elif cur and l.strip() and '308.550,01' not in l and not l.strip().startswith(('Página','Empresa','Desde','Fecha','LIBRO')):
        cur['txt']+=' || '+l.strip()
if cur: recs.append(cur)
out=[]
for r in recs:
    t=re.sub(r'[A-Z]\d{8}|\d{8}[A-Z]|[A-Z]\d{7}[A-Z]','  ',r['txt'])
    a=amt.findall(t)
    base=float(a[-1].replace('.','').replace(',','.')) if a else None
    ter=re.search(r'Su factura de pagos\s+(.*?)\s{2,}',r['txt']+'  ')
    out.append([r['fecha'],r['cta'][:3],ter.group(1) if ter else r['txt'][:60],base,r['txt'][:200]])
tot=collections.defaultdict(float)
for o in out: tot[o[1]]+=o[3] or 0
print(len(out)); print({k:round(v,2) for k,v in sorted(tot.items())})
csv.writer(open('desglose.csv','w')).writerows(out)
