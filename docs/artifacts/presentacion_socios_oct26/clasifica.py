import csv,collections,re
r=list(csv.reader(open('desglose.csv')))
def cat(f,cta,ter,b):
    t=ter.upper(); m=int(f[3:5])
    if cta in('640','642'): return 'personal'
    if cta=='681': return 'amort'
    if cta=='621': return 'alquiler'
    if cta=='628': return 'fijos'
    if 'STIMA' in t: return 'stima'
    if 'SEGURITY' in t or 'SECURITY' in t: return 'rrpp'
    if any(k in t for k in ['LAMINAS','AMAZON']) or (t.startswith('COMPRA') and m>=9) or (t.startswith('OTROS SERV') and m>=9) or (t.startswith('COMPRAS DE MERC') and m>=9): return 'fondeo'
    if cta=='608':
        if m==5: return 'obra'
        if abs(b-401.5)<0.01 or (m==9 and False): return 'acuerdos'
        return 'compras'
    if any(k in t for k in ['THOMAN','BIG DIPPER','MANTEC','AUDIMAGEN','FASTSPRING','SONICOLOR','COGESUR','EDISTRIBUCION','IGMACERRAJ']): return 'obra'
    if any(k in t for k in ['LEGAL V','PALERMO','RODRIGUEZ Y CAPITAN','BOLETIN']): return 'legal_preap'
    if 'TIPPDIPSD' in t: return 'tipsi_preap' if m<=5 else ('extra' if b>400 else 'fijos')
    if any(k in t for k in ['BARTER','PASTOR CRUZ','MÁXIMO','MAXIMO','CARRION','BA VISUALS','JOSE J DIAZ','PEDRAZA']): return 'marketing'
    if any(k in t for k in ['STIPENDIUM','ASESORAMIENTO','TELEFONICA','GOOGLE','BOOKING','FUTURE IS','AUCTANE']): return 'fijos'
    if 'FACTORING' in t: return 'financiero'
    if any(k in t for k in ['LARA VIGUERA','EVENTS BRANCH','BRUCE MOOD','ALONSO RODRIGUEZ','RUBEN SANZ','CHAVARRI','SONLIVE','GARCIA ZAJARA','PESCADOR','PEREZ DE AYALA','BERMUDEZ','MIRASIERRA','XITE','GUZMAN SADA']): return 'djs'
    if cta=='600': return 'compras'
    if any(k in t for k in ['HIELO','MAKRO','MONBAKE','DILASO','HIELOS','CARREF','NARBONA','SUMINISTROS UNIC']): return 'compras'
    return 'extra'
agg=collections.defaultdict(float); det=collections.defaultdict(list); bym=collections.defaultdict(float)
for f,cta,ter,b,t in r:
    b=float(b); c=cat(f,cta,ter,b); s=b if cta=='608' else b  # 608 viene negativo
    agg[c]+=s; det[c].append((f,ter[:28],b)); bym[(c,'pre' if int(f[3:5])<=5 else ('jun' if int(f[3:5])==6 else 'jul+'))]+=s
for k,v in sorted(agg.items(),key=lambda x:-x[1]): print(f'{k:12s} {v:11.2f}', {p:round(bym[(k,p)]) for p in ['pre','jun','jul+'] if bym[(k,p)]})
print('total',round(sum(agg.values()),2))
for k in ['extra','djs','fondeo','obra','legal_preap','marketing','fijos']:
    print('---',k, [(f[:5],t,round(b)) for f,t,b in det[k]])
