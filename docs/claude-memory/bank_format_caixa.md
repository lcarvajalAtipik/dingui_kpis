---
name: bank-format-caixa
description: "Formato REAL del export de CaixaBank de Dingui — CSV de CaixaBankNow (Concepto;Fecha;Importe;Saldo, conceptos truncados a ~18 chars), NO el XLS antiguo de Fondeo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a861d9eb-9449-477a-89e6-e7bb7676b867
---

**Validado con el primer export real de Dingui (08/07/2026):** el usuario exporta desde la banca digital **CaixaBankNow**, formato **CSV**, no el XLS antiguo que usaba Fondeo. Parser: `parse_caixa_now` en `src/kpis/ingest/bancos.py` (el parser XLS `parse_caixa` se mantiene por si acaso).

**Cómo identificar:** archivo `CaixaBank_digital_CaixaBankNow_{YYYYMMDD}.csv`. Header exacto: `Concepto;Fecha;Importe;Saldo`.

**Estructura:**
- Separador `;`, sin comillas. Orden descendente (más reciente primero).
- `Concepto`: **truncado a ~18 caracteres** por el banco ("MAKRO CENTRO 18", "BARTER CONSULTANC"). En transferencias emitidas por el usuario, el concepto es el texto que él tecleó, en minúsculas ("traspaso", "parte 2 certifica", "neveras", "santabder").
- `Fecha`: DD/MM/YYYY. **No hay fecha valor.**
- `Importe`/`Saldo`: formato `+1.000,00EUR` / `-293,48EUR` — signo explícito, separador de miles opcional (punto), coma decimal, sufijo EUR pegado. Codificación con rarezas: `Ñ`→`§`/`ç` ("BAZAR VI§ADOR", "LICENCIA TAXI Nç").
- **NO incluye IBAN ni titular** — el CSV no identifica la cuenta.
- Es exactamente el formato que el usuario pegó en la hoja "movimientos 30 abril 2026" del sheet de Proyecciones (mismas 4 columnas), así que el export CSV concilia 1:1 contra el ground truth por (fecha, importe).

**Conceptos recurrentes:** `TRANSF. A SU FAVOR` / `TRANSFER INMEDIATA` / `TRASPASO` (entrantes = aportaciones de socios; salientes = traspasos a Santander), `PAGO TRANSFERENCIAS` (lote de transferencias enviadas juntas — históricamente Obra), `P.SERV.*` / `PRECIO SERVIC.*` / `CORRESP.` (comisiones), `CNX NNNNNN` (¿cargos obra?).

**Deduplicación:** hash de `(bank, Fecha, Importe, Concepto, Saldo)` — el saldo desambigua cargos idénticos el mismo día.

Relacionado: [[bank-format-santander]], [[feedback-bank-format-stable]], [[business-overview]].
