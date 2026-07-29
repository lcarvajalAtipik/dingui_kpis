---
name: pl-categories
description: "Categorías P&L de Dingui — pre-apertura (validadas 98,9%) + operativas desde jun 2026 (Ingresos, COGS, Costes Fijos, Movimiento entre cuentas). Propuestas pendientes de validar con el usuario."
metadata: 
  node_type: memory
  type: project
  originSessionId: a861d9eb-9449-477a-89e6-e7bb7676b867
---

**Categorías pre-apertura** (columna `Tipo` del sheet, 88 movimientos 20/08/2025 → 30/04/2026, validadas por el usuario): Aportaciones (+221.638,53), Obra (-94.133,97), Alquiler/Fianza, Insonorización, Arquitectos, Sonido/Luces, Licencia/Trámites, Legal gestión software, Marketing, Otros, Financiero. Validación categorizador: cobertura 100%, acierto 98,9% (única excepción: devolución notaría +524,15 → user_override, en `CONFIRMED_CORRECTIONS` de `scripts/validate_categorizer.py`).

**Categorías OPERATIVAS en uso desde la apertura (~jun 2026)**, añadidas al categorizador el 08/07/2026 (estilo Fondeo):
- **Ingresos** — liquidaciones TPV Santander (`liquidacion efectuada` → neto de comisión; bruto en extra/Referencia 1).
- **COGS** — mayoristas: `makro`, `picking gades`, `cash lepe`; Coca-Cola resuelto por signo (cargo → COGS, abono → Rappels).
- **Costes Fijos** — `o2 fibra` (telecom).
- **Movimiento entre cuentas** — traspasos Caixa↔Santander. Detección: `mark_internal_transfers()` en categorizer.py (cruce de importes opuestos entre bancos, ≤3 días, con hint de transferencia) + patrones `de nuevo vh`/`a favor de nuevo vh` + guardia "Aportaciones nunca negativas".
- **Financiero** — confirming (`factoring y confirming`, `cobro a vencimiento` — rotan neto 0), gastos TPV (`cuota app android`, `liquidacion del contrato`, `liquidacion indemnizatorio`).
- **Sonido/Luces** — `thomann`, `madrid hifi`, `betopperdj`, `lightcloud`.
- **Legal, gestión, software** — asesorías `stipendium`, `remesa ases`.

**⚠ Reglas de época pre-apertura aún activas:** transferencias ENTRANTES sueltas (TRASPASO / TRANSF. A SU FAVOR / TRANSFER INMEDIATA sin pata cruzada) siguen → Aportaciones. Corrección conocida pendiente de aplicar: TRANSF. A SU FAVOR **+1.126,85 (01/05/2026)** es la devolución del cargo duplicado CNX 0001176170 de obra → Obra, no Aportación (user_override al ingestar).

**Propuestas PENDIENTES de validar con el usuario (08/07/2026):** certificaciones "parte N certifica" → Obra; "sonido 1parte" → Sonido/Luces; neveras/mesa refrigerada/tostadora → ¿categoría nueva "Equipamiento"?; bazares/Carrefour/supermercados → ¿COGS o menaje?; restaurantes (comidas equipo) → ¿Otros?; y aún sin identificar: Discount_ES, ALIEXPRESS, imposición a plazo 3.000 €.

**✅ Misterios RESUELTOS por la conciliación con facturas (29/07/2026)** — identificados al céntimo, aplicar en el categorizador:
- **La constructora es "LORENTE Y MILLÁN CONSTRUCCIONES S.L."** (no "Florente" — lectura errónea del concepto bancario). Certificaciones = "PAGO TRANSFERENCIAS".
- **El confirming Santander financia una certificación de obra de Lorente y Millán (32.343,05 €, fact. 04/06, cobro a vencimiento 19-22/06)** — pregunta antigua zanjada. Comisión: Santander Factoring 892,29 € (fact. 22/06).
- `pago prezo` = FUTURE IS AN ATTITUDE S.L. (181,45) · `SUMINISTRSO UNIC` = Suministros Unic SL · `BARTER CONSULTANC` = Barter Consultancy Partners SL (605) · `pulseras` = Gráficas Pedraza (95,59) · `TRF.INTERNACIONAL` = BA visuals LLC (138) · `AQUALAR` = Aqualar Piscinas, ferretería/mantenimiento · neveras/mesa refrigerada/tostadora = Innovación y Diseño para Hostelería SL (equipamiento cocina) · Viento Creativo: "acopio material" 10.890 (30/04) + cartas menú 88 + un cargo 2.371,60 (08/07) SIN factura en Drive.
- Facturas SIN cargo bancario visible aún y cargos SIN factura: ver columnas `pago_estado` en `data/facturas/registro_facturas.csv` (53 conciliadas / 36 sin extracto / 27 no encontradas).

Relacionado: [[business-overview]], [[reference-proyecciones-sheet]], [[ignorar-fx-convention]], [[bank-format-santander]].
