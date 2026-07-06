---
name: pl-categories
description: "Categorías reales de Dingui (columna Tipo del sheet) — fase pre-apertura; las operativas llegarán al abrir. 96,6% de acierto del categorizador vs ground truth."
metadata:
  type: project
---

**Categorías REALES de Dingui** (columna `Tipo` de la hoja "movimientos 30 abril 2026" — 88 movimientos, 20/08/2025 → 30/04/2026, todos categorizados por el usuario):

| Tipo | n | Total € |
|---|---:|---:|
| Aportaciones | 31 | +221.638,53 |
| Obra | 8 | -94.133,97 |
| Alquiler/Fianza | 5 | -21.211,11 |
| Insonorización | 1 | -20.000,00 |
| Arquitectos | 2 | -11.495,00 |
| Sonido/Luces | 1 | -8.582,50 |
| Licencia/Trámites | 6 | -8.251,54 |
| Legal, gestión, software | 14 | -3.464,49 |
| Marketing | 1 | -342,00 |
| Otros | 8 | -266,70 |
| Financiero | 11 | -12,72 |

Son categorías de **pre-apertura** (coinciden con las partidas del forecast "VdE - FC inicial"). Al abrir aparecerán las operativas (Ingresos, COGS, Nominas, DJ, Rappels… al estilo Fondeo).

**Reglas clave aprendidas (en `src/kpis/categorizer.py`):**
- `TRASPASO` / `TRANSF. A SU FAVOR` / `TRANSFER INMEDIATA` → **Aportaciones** (⚠ SOLO en pre-apertura; al abrir, transferencias entrantes podrán ser Ingresos — revisar estas reglas entonces).
- `TRIBUTOS` → **Licencia/Trámites** (⚠ pre-apertura; cuando haya nóminas, TRIBUTOS IRPF será Nominas como en Fondeo).
- `realmivo` / `cuota comunidad` / `fianza y garantia` → Alquiler/Fianza.
- `p.serv` / `precio servic` / `corresp.` / `mantenimiento` → Financiero (gastos de servicio CaixaBank).
- docusign / godaddy / apple / adobe / google workspace / trimble → Legal, gestión, software.
- **notaría/notariado → Legal, gestión, software** (confirmado 2026-07-06; OJO: en Fondeo notaría era Financiero).
- `UME` → Sonido/Luces si cargo, Financiero si abono (resolver por signo).

**Validación (confirmada por el usuario 2026-07-06):** cobertura 100%, acierto 98,9% (87/88). Las 3 inconsistencias del sheet quedaron resueltas: Trimble → Legal/software; PRECIO SERVIC.PAGOS -137,34 → Financiero; la devolución de +524,15 € en TRANSF. A SU FAVOR **es notariado** → Legal, gestión, software. Esta última es el único caso que el categorizador no puede distinguir por concepto (idéntico a las aportaciones) — se resuelve con `user_override` al ingestar; está registrada en `CONFIRMED_CORRECTIONS` de `scripts/validate_categorizer.py`.

**OJO al matching contra extractos crudos:** en el sheet el usuario a veces sustituye el concepto del banco por descripción propia ("alquiler febrero", "acopio material", "honorarios proyec"…). Esas reglas exactas NO matchearán el export crudo — la prueba real llega con el primer XLS de CaixaBank.

Relacionado: [[business-overview]], [[reference-proyecciones-sheet]], [[ignorar-fx-convention]].
