---
name: reference-fondeo-repo
description: "fondeo_kpis (repo hermano en ~/Desktop/fondeo_kpis) es la implementación de referencia — parsers, categorizador, scripts de análisis y memoria completa"
metadata:
  type: reference
---

Este repo (dingui_kpis) es un port de `/Users/luismdecarvajal/Desktop/fondeo_kpis`, el sistema equivalente del otro local del usuario (Fondeo Sin Playa). Ahí está la implementación madura de todo:

- **Parsers multi-banco** (`src/kpis/ingest/bancos.py`): Caixa (mismo formato que Dingui), Sabadell, Santander.
- **Categorizador completo** (`src/kpis/categorizer.py`): ~200 reglas de proveedores de Fondeo + ground truth sheet. Las reglas NO aplican a Dingui (proveedores distintos), pero el patrón de construcción sí.
- **Scripts de análisis listos para portar cuando haya datos**: `valoracion_traspaso.py`, `valoracion_dcf_2025.py`, `tesoreria_mensual_detallada.py`, `forecast_calibrated.py`, `build_pl_monthly.py`, `export_tesoreria_excel.py`, `real_vs_forecast.py`…
- **Ingest especializados** (rappels con distribución por cobros, renting normalizado, seguridad M-1, DJs desde sheet) — atados a los proveedores/contratos de Fondeo; rehacer con los de Dingui.
- **Memoria completa** en `fondeo_kpis/docs/claude-memory/`: reglas de devengo, IVA, formatos de banco, calibración de forecast… Consultarla antes de reinventar metodología.

**How to apply:** Ante cualquier tarea nueva en Dingui, mirar primero cómo se resolvió en fondeo_kpis y portar adaptando. No copiar reglas de proveedores/conceptos: son de Fondeo.

Relacionado: [[business-overview]], [[pl-categories]], [[bank-format-caixa]].
