---
name: bank-format-caixa
description: Formato del export de CaixaBank (movimientos cuenta) — layout conocido de fondeo_kpis; IBAN de Dingui pendiente de confirmar con el primer export
metadata:
  type: reference
---

Conocimiento portado de fondeo_kpis (mismo banco, mismo export). **Pendiente validar con el primer archivo real de la cuenta de Dingui** — si el layout difiere, actualizar aquí.

**Cómo identificar:** archivo XLS antiguo (OLE2, magic `D0CF11E0`), nombre `Movimientos_cuenta_{ultimos7_iban} ({N}).xls`. El `(N)` es el contador de descargas. Código de entidad **2100** en el IBAN.

**Estructura:**
- 1 sheet, llamado igual que el archivo.
- Fila 0 col 0: título tipo "Movimientos de la cuenta ES.. 2100 ..." — **de aquí se extrae el IBAN** con regex `ES\d{2}(?:\s*\d{4}){5}`.
- Fila 1 col 0: "Importes expresados en euros".
- Fila 2: **headers reales** = `Fecha`, `Fecha valor`, `Movimiento`, `Más datos`, `Importe`, `Saldo`.
- Fila 3+: datos.

**Formatos:**
- Fechas: **datetime nativo de Excel** (pandas las parsea a `Timestamp` directamente, NO son strings).
- Importes: float decimal con **punto**, sin separador miles. Signo negativo = salida.
- Saldo: float, saldo después de cada movimiento.
- `Movimiento`: string corto, concepto principal.
- `Más datos`: string libre con detalle adicional (emisor de transferencias, nº contrato…), puede ser NaN. **Clave para categorizar** — concatenar con el concepto.

**Engine pandas:** `pd.read_excel(path, engine="xlrd", header=None)` + headers en fila 2 (así lo hace `parse_caixa` en `src/kpis/ingest/bancos.py`).

**Deduplicación:** no hay id natural. Hash de `(bank, Fecha, Importe, Movimiento, Más datos, Saldo)` — el Saldo evita colisiones cuando hay cargos repetidos el mismo día con mismo importe.

**Conceptos típicos de CaixaBank** (vistos en Fondeo; los de Dingui serán distintos pero el banco usa vocabulario similar): `TRANSFER INMEDIATA`, `TRANSF. A SU FAVOR`, `RECIBO …`, `PRES.{nºcontrato}` para préstamos, `PRECIO AVAL`, `COMISION …`.

Relacionado: [[feedback-bank-format-stable]], [[business-overview]].
