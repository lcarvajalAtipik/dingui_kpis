---
name: coste-personal
description: "Estructura del coste de personal de Dingui y qué fuente lo aporta: DJs = facturas de autónomos (categoría personal-dj); nóminas/Seg.Social/IRPF = movimientos bancarios (aún no disponibles, banco solo llega a 08/07); gasto_personal del gerente = cifra nocturna que MEZCLA todo"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Encargo del usuario (04/08/2026):** ver el coste de personal separando **nóminas / Seguridad Social / IRPF** de los **DJs**.

**Las 4 patas del coste de personal y su fuente:**
1. **DJs (personal externo autónomo)** → FACTURAS. Reclasificados 04/08 de `otros` a categoría **`personal-dj`** en `registro_facturas.csv`. A 04/08: 3 facturas, 742 € (DJ Chaver/Fernando Chávarri 116/2026 265€ + 119/2026 212€; Daniel Félix Alonso 48/2026 265€, ~212-265€/sesión). OJO: la factura "Profesional DJ" 8.508€ (07/03) es EQUIPAMIENTO de cabina (sonido/luces), NO servicio — se queda fuera de personal.
2. **Nóminas netas** (transferencias a trabajadores) → BANCO. **NO disponible**: el extracto llega solo a 08/07 y la 1ª nómina de un local abierto a mediados de junio se paga a fin de julio → cae fuera. Cero movimientos de nómina en el banco actual.
3. **Seguridad Social empresa** (cargo TGSS, ~fin de mes) → BANCO. NO disponible (mismo motivo).
4. **IRPF retenido** (modelo 111 trimestral vía AEAT + retención en factura de autónomos) → BANCO / gestoría. NO disponible.

**⚠ El "gasto de personal" de los cierres del gerente NO es la nómina:** es una cifra nocturna (efectivo/estimada) que **MEZCLA camareros + DJs + seguridad/cabina**. 24 noches (26/6→28/7) = 28.898 € (~14,9% de la caja). Sirve como control de coste variable por noche, NO para desglosar nóminas/SS/IRPF ni para el P&L formal. Los DJs facturados (742€) están DENTRO de esa cifra, no se suman.

**How to apply:** para el coste de personal REAL hacen falta (a) extractos bancarios frescos (transferencias a trabajadores, cargos TGSS, pagos AEAT modelo 111/303) y (b) idealmente las nóminas/TC de la gestoría → montar tabla `nominas` (hoy vacía en la DB). Hasta entonces solo tenemos: DJs facturados (exacto) + gasto_personal del gerente (agregado nocturno, mezclado).

Relacionado: [[pl-categories]], [[cierres-gerente-diarios]], [[business-overview]], [[sistema-facturas-drive]].


**REGLAS DE MODELADO validadas por el usuario (06/08/2026):** DJs en nómina → IRPF 2% (régimen artistas); DJs con factura → retención 15%; trabajadores de sala → IRPF normal (uso 2% mínimo de contratos temporales hostelería, ajustable) + SS trabajador 6,48%; empresa → SS ~32% sobre bruto. El cash de los partes se trata como NETO. Julio: neto sala 32.011 → bruto 34.977 → +SS empresa 11.193; DJs factura 742 (ret. 111); formación 700 → personal formalizado 47.612 vs cash real 33.453 (sobrecoste de formalización ~14.200, hoy NO pagado).