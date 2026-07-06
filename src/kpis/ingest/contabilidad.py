"""Ingesta de la contabilidad mensual de la gestoría.

Pendiente. Flujo previsto (mismo que fondeo_kpis):
1. Usuario sube el informe/export a carpeta Drive compartida.
2. MCP de Google Drive descarga a `data/contabilidad/`.
3. Este módulo parsea (pdfplumber o openpyxl según formato) y normaliza a `pnl_lines`.

Por confirmar: qué gestoría/software lleva la contabilidad de Dingui (en Fondeo
era Avalon — si es el mismo, el parser de libro diario de fondeo_kpis se porta directo).
"""
from __future__ import annotations


def _not_implemented() -> None:
    raise NotImplementedError("Parser de contabilidad pendiente — esperando primera muestra.")
