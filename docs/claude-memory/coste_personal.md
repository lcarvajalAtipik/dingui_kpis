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


**REGLAS DE MODELADO validadas por el usuario (06/08/2026):** DJs en nómina → IRPF 2% (régimen artistas); DJs con factura → retención 15%; trabajadores de sala → IRPF normal + SS trabajador 6,48%; empresa → SS ~32% sobre bruto. (Modelo YA SUPERADO por datos reales ↓)

**DATOS REALES — NÓMINAS JULIO (gestoría, 07/08/2026):** la gestoría laboral es **Stipendium Asesores** (Alejandra Romera, alejandra@stipendium.es). **Flujo mensual: email a info@dinguiclub.com asunto "NOMINAS NUEVO VH \<MES\>"** con 4 adjuntos: HS (nóminas individuales PDF), IC (informe conceptos xlsx), ITA (trabajadores en alta PDF), **RN (resumen por trabajador .xls — LA fuente: header fila 7, datos desde fila 9; cols BRUTO/LIQUIDO/COSTE EMPR/TOTAL TC1/IRPF/SS EMPLEAD/SS EMPRESA)**. Guardar en `data/nominas/<YYYY-MM>/` (data/* gitignored — NO subir al repo, datos personales).

**Julio 2026 real (30 personas con nómina, 1ª alta 03/07 — junio TODO informal):** bruto 21.060,10 · **líquido 19.319,67** · **IRPF 388,81** (1,85% medio; modelo 111 trimestral) · SS trabajador 1.351,62 (6,42%) · SS empresa 7.002,08 (33,2%) · **TC1 a pagar TGSS 8.353,70** (cargo ~fin agosto) · **coste empresa total 28.062,18**. Cuadre interno exacto. (IC difiere del RN en ~87€ por complemento IT/absentismo — RN es la referencia.) ITA a 07/08: 22 en alta (2 altas ese mismo día: Daniel Terrero, Juan Luis López Montero; ~10 de julio ya de baja; muchos a tiempo parcial CTP 500/200).

**GAP RESUELTO por el usuario (07/08): el efectivo por encima de nómina+DJs son HORAS EXTRA EN B** (gente sin alta / horas no declaradas, pagadas de caja). Se contabilizan como línea propia del coste de personal.

**ESTRUCTURA OFICIAL del coste de personal mensual (definida por el usuario 07/08):** nóminas (líquido) + horas extra B + DJs + IRPF + SS = coste de personal del mes. Formación va FUERA (OPEX). **Criterio DJs elegido: TODO el caché del sheet** (julio 7.850) **con línea de ajuste −caché "nom"** (julio −2.940) para no duplicar con nómina (los DJs de plantilla — Marina Aguilar, Lucas Haurie, David Venegas… — cobran vía nómina + B).

**JULIO CERRADO: nóminas líquido 19.319,67 + horas extra B 8.523,03 + DJs caché 7.850,00 − ajuste nom −2.940,00 + IRPF 388,81 + SS 8.353,70 = 41.495,21** (20,4% s/ingresos 203.310). Cuadre: = efectivo cierres 32.752,70 + IRPF + SS exacto. Horas extra B = cash − líquido − DJs externos cash (4.910). PENDIENTE: facturas de DJs "fact" solo 742 de 2.270 recibidas (faltan Nacho Lara, Fonseka, Coke Fesser, Adrián León…); "Yanes"/"Halcón" marcados nom no localizados en RN.