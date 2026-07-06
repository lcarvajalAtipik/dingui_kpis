---
name: feedback-bank-format-stable
description: El formato de export de cada banco es estable — parser dedicado y minucioso por banco, una sola vez
metadata:
  type: feedback
---

Cada banco exporta siempre el mismo formato; no cambia entre meses ni entre cuentas del mismo banco. (Preferencia establecida en fondeo_kpis: "Muy importante te hagas experto en leer esos archivos, siempre serán mismo formato para cada banco".)

**How to apply:**
- Parser dedicado por banco con conocimiento del layout exacto (filas de cabecera, columnas, formato de fechas/números, IBAN). Para Dingui: CaixaBank, ya documentado en [[bank-format-caixa]].
- Documentar el formato en memoria con un ejemplo de fila tipo.
- Si llega un archivo con layout distinto al documentado, **parar y avisar** — no inventar parseo.

Relacionado: [[bank-format-caixa]], [[feedback-no-prefilter-data]].
