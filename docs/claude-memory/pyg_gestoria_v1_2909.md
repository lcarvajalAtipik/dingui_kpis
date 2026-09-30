---
name: pyg-gestoria-v1-2909
description: "1ª PyG 2026 de la gestoría (PDF 29/09, Cris Roque): resultado 123.804 vs mi modelo 249.233; el gap (−125K) viene casi todo de 623+629 = 214K (en los libros jun-ago eran ~19K). Pendiente de que manden detalle."
metadata:
  type: project
---
PDF `data/gestoria/2026-pyg/NUEVO_VH_PYG_29-09-2026.pdf` (local, data/ no está en git). Cifras: 705 ventas 526.032,48 · 600 −36.649,60 · 602 −80.182,66 · 608 devol +975,95 · 640 −47.631,71 · 642 −15.719,52 · 621 −7.593,44 · 622 −1.350 · 623 −32.980,85 · 629 −181.096,85 · resultado 123.803,80. Sin amortización, sin gastos financieros, sin otros ingresos, sin IS.

Cruce con [[artifact-dingui-mes-a-mes]] (res26 249.233): ventas = jun 1.604,82 + jul 204.157,51 + ago 319.750,15 + 520 sin identificar. 621 = exactamente 4 × 1.898,36 (4 meses de Realmivo; yo devengo 11). Compras brutas 116.832 < 139.481 de los libros jun-ago (faltan ~22,6K ¿reclasificados?); devoluciones solo 976 (faltan Merino 8.208, Melgarejo 4.817, CCEP ~2.032). Personal = jul+ago formal −851. **623+629 = 214K frente a ~19K en los libros jun-ago → HIPÓTESIS (no confirmada): obra/pre-apertura llevada a gasto.** Faltan Pepsi 17K, Pernod 6.200, amortización ~19,75K. El usuario ha pedido más detalle a la gestoría (30/09). Relacionado: [[contabilidad-gestoria-junago]], [[coste-proyecto-apertura]].

**Desglose recibido 30/09** (`data/gestoria/2026-pyg/NUEVO VH DESGLOSADO.xls`, libro de compras y gastos 6xx, 284 líneas, cuadra al céntimo con la PyG). Hallazgos:
- **Obra/equipamiento llevado a gasto: 138.578,20** → Lorente 60.996,19 (facts 21, 23, 28 en 629) · Aycoa 36.458 (41+61, 629) · Stima 20.350 (623 9.500 + 600 3.750 + 629 7.100) · Viento 11.032,80 (602 9.072,80 + 629 1.960) · Thomann 3.604,30 − 673,55 · Big Dipper láser 2.842,27 · Mantec 1.606,12 · eDistribución 931,28 · Igmacerrajeros 720 · Digital Audimagen 710,79.
- **Abonos de fin de temporada contabilizados como COMPRAS en positivo (600, sept):** Merino 1244/1245 8.207,97 + Melgarejo N4574 4.817 → error de 2 × 13.024,97 = 26.049,94 de gasto de más.
- Bebida en 629 en vez de 600: Merino 57.309,72 (30 facts), Melgarejo 4.756,18, Ipasur 638, Picking 345, Quintero 502. F&B neto total 126.167 (incl. junio 12,7K) ≈ modelo.
- Realmivo: 621 feb-may (4 × 1.898,36) + ene 595,08 en 629 + jun 2.251,98 en 602 → faltan facturas jul-sep. 640 incluye −851,62 de anticipos restando sueldos (error menor). Sin 625 seguros (Mapfre estaba en los libros jun-ago), sin 626 comisiones, sin amortización. Factoring 1.191,43 en 629. RRPP Security 12.539,56 en 623.
- PyG corregida estimada ≈ 277K (123,8 + 138,6 + 26,0 − 0,9 − amort 19,75 − alquiler ~11,5 + Pepsi/Pernod/rappels 24 − ~3,5 comisiones/fijos) → sin el B (~33,8K) y sin pre-apertura/junio coincide con el modelo 249K. IS 15 % ≈ 41-42K, igual que el modelo.

**30/09 (tarde):** la contable dice que "no ha visto la factura de Lorente". Las 6 facturas de Lorente están en Drive, cada una en la carpeta de su mes (6 prov. fondos 1T, 14 abril, 18 mayo, 21 y 23 junio, 28 agosto) y en registro_facturas.csv con drive_id. Además, en SUS libros del 15/09 ya estaban las 6 en inmovilizado (219.2 = 6+14+18 = 135.213,29; 215.4/215.5/215.8 = 21/23/28), igual que Aycoa 41/61 (215.9/215.7). En la PyG del 29/09 las 21/23/28 y Aycoa aparecen en 629 → o las han pasado de 215 a gasto o están DOBLES (215 + 629). Hay que pedir el balance para saberlo.
