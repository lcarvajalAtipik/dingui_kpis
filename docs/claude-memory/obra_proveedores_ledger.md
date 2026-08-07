---
name: obra-proveedores-ledger
description: "Cuentas corrientes de la obra verificadas al céntimo (06/08/2026): Lorente y Millán pagada salvo 178,54€ (asignación cert a cert); Sánchez Yuste CERRADA (0,00); pendientes Aycoa 20K sin factura y BS Aislamientos por reconstruir"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Método validado por el usuario:** los pagos de obra van EN ORDEN CRONOLÓGICO según las certificaciones, a veces por partes ("parte 1/2/3 certifica"). Las certificaciones de Lorente DEDUCEN las anteriores (los importes de factura ya son netos incrementales — verificado leyendo los PDFs: "A DEDUCIR 1ª PROVISIÓN DE FONDOS −45.401,14…"). Los alias bancarios: "Florente"=Lorente y Millán, "Mantec"=Sánchez Yuste. "PAGO TRANSFERENCIAS" (Caixa) es concepto GENÉRICO — asignar por importe/cronología, no asumir proveedor.

**LORENTE Y MILLÁN (obra) — CORREGIDO 06/08 con "ultima parte cert" (−10.178,54, 28/5):** las 5 facturas conocidas (213.714,15) están pagadas EXACTAS cert a cert: Provisión←6/3; Cert2←1/5; Cert3←40.000(20/5)+12.000+10.000+10.178,54(28/5 "ultima parte cert"); Cert4←confirming; Cert5←9.000+5.000+3.763,02. PERO hay un pago EXTRA de 10.000 (8/6 "parte 1 certifica") sin certificación que lo respalde → **existe una CERT 6 / liquidación final NO capturada** (pedirla a Lorente; el usuario recordaba ">20K pendientes" → la cert 6 podría ser ~20-30K con 10K ya a cuenta).

**SÁNCHEZ YUSTE / Mantec (clima-frío) — CERRADA A CERO:** facturado 50.486,19 (0165+0215+0216+0375) = pagado 50.486,19 (24.271,39 el 27/2 "PAGO TRANSFERENCIAS" + 5.000 + 10.000 + 11.214,80 jul-ago).

**BS AISLAMIENTOS (insonorización):** factura OB-113 45.798,50 (15/4). Pagos: "parte 1 facrura" 20.000 (30/4) + "2 parte factura" 5.000 (8/5, categorizado Insonorización 06/08, conf. 0.85) + "Último Pago Bs" 8.145,50 (20/7) = 33.145,50 → **aparente pendiente 12.653** PERO el pago del 20/7 dice "ÚLTIMO" → ¿cierre con descuento negociado? PREGUNTAR al usuario.

**STIMA 21 (arquitectos) — completado 07/08 con facturas del email:** facturado 24.623,50 (T42575 3.025 dic-25 + T12619 8.470 feb + T32661 4.537,50 jun, pagada 13/7 exacta + T32665 8.591 jul, pagada 5/8 exacta). Pagos visibles 21.598,50 → **T42575 (3.025, dic-2025) sin pago bancario visible** — ¿pagada antes del inicio del extracto (20/8/25→…, sí cubre dic) o en efectivo/otra cuenta? PREGUNTAR.

**AYCOA (sonido): 20.000 € pagados SIN NINGUNA factura** (10K "sonido 1parte" 5/6 + 5K "Deuda David" 14/7 + 5K "Deuda Sonido" 29/7) — mayor agujero documental; pedir factura.

**PRÉSTAMO SOCIOS (corregido 06/08): 22.000 € entraron** (7/6: 4K+5K · 8/6: 10K + 3K "TRASPASO"), devueltos 8.000 (5K el 20/7, 3K el 5/8) → **14.000 pendientes de devolver**.

Relacionado: [[pl-categories]], [[project-bank-ingest-state]], [[business-overview]].
