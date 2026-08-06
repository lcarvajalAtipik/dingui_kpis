---
name: obra-proveedores-ledger
description: "Cuentas corrientes de la obra verificadas al céntimo (06/08/2026): Lorente y Millán pagada salvo 178,54€ (asignación cert a cert); Sánchez Yuste CERRADA (0,00); pendientes Aycoa 20K sin factura y BS Aislamientos por reconstruir"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Método validado por el usuario:** los pagos de obra van EN ORDEN CRONOLÓGICO según las certificaciones, a veces por partes ("parte 1/2/3 certifica"). Las certificaciones de Lorente DEDUCEN las anteriores (los importes de factura ya son netos incrementales — verificado leyendo los PDFs: "A DEDUCIR 1ª PROVISIÓN DE FONDOS −45.401,14…"). Los alias bancarios: "Florente"=Lorente y Millán, "Mantec"=Sánchez Yuste. "PAGO TRANSFERENCIAS" (Caixa) es concepto GENÉRICO — asignar por importe/cronología, no asumir proveedor.

**LORENTE Y MILLÁN (obra) — facturado 213.714,15 / pagado 213.535,61 / PENDIENTE 178,54 €:**
- Provisión 30% (4/3) 54.935,38 ← pago 6/3 exacto
- Cert 2 (27/4) 36.494,16 ← pago 1/5 exacto
- Cert 3 (15/5) 72.178,54 ← 40.000 (20/5, "PAGO TRANSFERENCIAS") + 12.000 (22/5 "parte 2") + 10.000 (26/5 "parte 3") + 10.000 (8/6 "parte 1 certifica") = 72.000 → faltan 178,54
- Cert 4 (4/6) 32.343,05 ← CONFIRMING Santander 19-22/6 exacto
- Cert 5 (15/6) 17.763,02 ← 9.000 (15/6) + 5.000 (9/7) + 3.763,02 (20/7 "Finalización") exacto
(El recuerdo del usuario "faltaban >20K" era el estado de primeros de julio: cert 5 aún debida + confirming rotando; hoy liquidada.)

**SÁNCHEZ YUSTE / Mantec (clima-frío) — CERRADA A CERO:** facturado 50.486,19 (0165+0215+0216+0375) = pagado 50.486,19 (24.271,39 el 27/2 "PAGO TRANSFERENCIAS" + 5.000 + 10.000 + 11.214,80 jul-ago).

**"2 parte factura" (−5.000, 08/05):** NO es Lorente (cert 2 ya pagada, cert 3 aún no emitida) NI Sánchez Yuste (cuadra sin él) → hipótesis: pago parcial a **BS Aislamientos** (factura OB113 45.798,50 del 15/4; el pago del 20/7 se llama "ÚLTIMO Pago Bs" 8.145,50 → hubo parciales anteriores). Reconstruir cuenta BS pendiente.

**AYCOA (sonido): 20.000 € pagados SIN NINGUNA factura** (10K "sonido 1parte" 5/6 + 5K "Deuda David" 14/7 + 5K "Deuda Sonido" 29/7) — mayor agujero documental; pedir factura.

**PRÉSTAMO SOCIOS (corregido 06/08): 22.000 € entraron** (7/6: 4K+5K · 8/6: 10K + 3K "TRASPASO"), devueltos 8.000 (5K el 20/7, 3K el 5/8) → **14.000 pendientes de devolver**.

Relacionado: [[pl-categories]], [[project-bank-ingest-state]], [[business-overview]].
