---
name: feedback-no-prefilter-data
description: "El usuario sube los datos crudos sin filtrar — yo soy responsable de deduplicar, filtrar por rangos de fechas y normalizar"
metadata:
  type: feedback
---

El usuario NO pre-filtra ni pre-procesa los datos antes de subirlos. Sube exports completos tal y como los descarga del banco, del PoS o de la gestoría. (Preferencia establecida en fondeo_kpis; aplica igual aquí.)

**Why:** Lo dijo explícitamente en Fondeo: "no voy a subirte los datos filtrados sino que tendrás que filtrar tu por lo que necesites, yo descargo y subo tu te encargas de procesar todo".

**How to apply:**
- Asumir solapamientos entre uploads sucesivos → **deduplicar siempre por `raw_tx_id`** (bancos), `tipsi_id` (ventas Tipsi), `(period, account_code)` (P&L).
- No asumir rango de fechas: inspeccionar fechas dentro del archivo antes de ingestar.
- Mantener `ingest_runs` con rangos efectivos y rows_in/rows_out para auditar cargas.
- Validar el contenido contra lo esperado — no procesar a ciegas por filename.
- Si algo del input no encaja con lo esperado, parar y preguntar antes de inventar parseo.
