---
name: project-bank-ingest-state
description: "Estado ingesta bancaria: 489 movs hasta 05/08/2026 (Caixa+Santander). HALLAZGO CLAVE: cero nóminas/TGSS/IRPF en banco → personal se paga en efectivo de caja. Proveedores bebida se pagan por 'deuda' en redondos. 57 movs nuevos sin categorizar (transferencias obra con alias)"
metadata:
  type: project
---

**Estado 05/08/2026:** `scripts/ingest_bancos_sqlite.py` (nuevo, dedup por raw_tx_id) → DB local 489 movimientos, 2025-08-20 → 2026-08-05. Exports en data/bancos/inbox/ (Caixa CSV 05/08 + Santander XLS 05/08).

**HALLAZGOS del tramo 08/07→05/08:**
1. **CERO nóminas, CERO TGSS, IRPF solo 73,69 € (AEAT 20/07)** → el personal de sala se paga EN EFECTIVO desde la caja nocturna (el "gasto personal" de los partes). No hay estructura formal de nómina visible aún (salvo "Formación Cocina Paco" 700 €). Tema laboral/fiscal a tratar con el usuario y gestoría — el gross-up de SS/IRPF que estimábamos NO se está pagando (aún).
2. **El efectivo de caja casi no se ingresa en banco** (solo 1 ingreso 2.850 de Borja Ybarra) — se usa para pagar personal y gastos.
3. **Proveedores de bebida se pagan por "deuda" en importes redondos**, no por factura: Merino 25.000 pagados (facturado ~36,5K → pendiente ~11,5K), Melgarejo 9.000 (facturado 26,1K → pendiente ~17K).
4. **HIELO real: 3.121,10 € pagados** (521 + 1.069,10 + 1.531 el 04/08) → existe una 3ª factura de hielo ~1.531 SIN capturar (pedirla). Hielo julio ≈ 2.800 sin IVA → ~0,25-0,27 €/copa.
5. **TPV julio-agosto: 179.355 € netos** en 152 liquidaciones.
6. **La obra/instalaciones se está pagando con la caja del verano**: desde 8/7 → Mantec/Sánchez Yuste (aires) 26,2K + Stima (arquitecto) 13,1K + BS Aislamientos 8,1K + Aycoa (sonido) 10K + Florente 8,8K + Viento Creativo 7,4K ≈ **74K de deuda de obra liquidada en un mes**.
7. **57 movimientos sin categorizar (−131,7K)**: casi todo las transferencias anteriores (conceptos con alias: "Florente", "Mantec", "Aycoa", "Stima") → añadir reglas al categorizador. NOTA: los alias de transferencia usan apodos ("Florente" = Lorente y Millán).

Relacionado: [[coste-personal]], [[pl-categories]], [[mercaderia-gerente]], [[sistema-facturas-drive]].
