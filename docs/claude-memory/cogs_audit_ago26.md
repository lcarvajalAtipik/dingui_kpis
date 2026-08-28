---
name: cogs-audit-ago26
description: "Auditoría COGS 27/08/2026: banco 130,6K vs facturas 138,2K dedup; 8 facturas duplicadas, 13 sin base, faltan facturas Dilaso/Hielo; pendiente pago ~15,4K"
metadata: 
  node_type: memory
  type: project
  originSessionId: dde61c19-f7ff-4012-880b-6389bdf5173d
  modified: 2026-08-27T13:15:30.120Z
---

Auditoría COGS 27/08/2026 (banco hasta 27/08, facturas hasta 24/08). PENDIENTE de decisiones del usuario, nada corregido aún:

- **Banco COGS**: 93 movs, −130.604,85 (jun −2.436 / jul −29.832 / ago −98.337).
- **Facturas F&B registro**: 144.688 c/IVA brutas → **138.198 tras dedup** (base registrada 93.351).
- **8 facturas DUPLICADAS** en registro (distinto drive_id, mismo prov+num+importe): Melgarejo N3371 (3.436), Jamones FA260250 (1.152,32), Picking 2026001808/1809 y una sin num (716,32), Plato al Centro 073639/075292/075449, Bazar 50140. Total duplicado 6.490 (base 5.633). +3 filas Coca-Cola todas NaN (basura).
- **13 facturas SIN base extraída** (26.326 c/IVA ≈ 21,7K base): 5 Melgarejo ago, 3 Jamones ago, 5 Makro jul. Afecta a COGS ago si se suma base del registro.
- **Faltan facturas**: Dilaso (3.292 pagados por recibo, 0 facturas), Hielo Express/Mellis (pagado 6.909 vs facturado 3.121 → gap 3.788; ¿facturan?), Makro tickets menores (−517), Cash Lepe/El Jamón/frutería (compras tarjeta sin ticket, ~180).
- **Cuadres que validan**: Melgarejo facturado 50.859 vs pagado 50.889 (diff −30, las transferencias "Deuda 1/2" 9K eran stock inicial); Picking y Berlys/Monbake cuadran a 0.
- **Pendiente de pago por facturas** (facturado dedup − pagado): Merino 10.702,55 + Coca-Cola 2.077,31 + Jamones Encina 1.748,33 + Ipasur 641,16 + menores 232 ≈ **15.400**. Merino incluye 25K de transferencias a cuenta ("Pago Merino 1/2/3" + 10K).
- P&L jul usó COGS 44.495; registro dedup da jul base 46.275 (diff 1.780 por revisar qué dedup aplicó el P&L).
