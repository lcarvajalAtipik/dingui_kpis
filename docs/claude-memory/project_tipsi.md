---
name: project-tipsi
description: "Proyecto Tipsi (PoS) — análisis operativo de ventas; mecanismo de acceso a datos POR CONFIRMAR (API vs exports)"
metadata:
  type: project
---

Dingui usa **Tipsi** como software de punto de venta (en Fondeo era Revo). Es la fuente de verdad para: mix de ventas, tickets, productos, márgenes por producto, facturación por franja horaria, dimensionado de plantilla.

**Estado (2026-07-06):** estructura preparada (`src/kpis/ingest/tipsi.py`, tablas `tipsi_products` / `tipsi_sales` en el esquema), pero el **mecanismo de acceso está por confirmar**:
- ¿Tipsi expone API? (auth, endpoints — investigar con el usuario cuando tenga credenciales del back office)
- ¿O trabajamos con exports CSV/XLSX del back office? (entonces el cliente HTTP no se usa y hay que escribir parsers de export)

En fondeo_kpis los scripts `revo_probe_*.py` sirven de plantilla para explorar una API desconocida.

**How to apply:** antes de construir análisis de ventas, resolver el acceso a datos (mismo principio que en Fondeo: automatizar el acceso ANTES de construir análisis). Preguntar al usuario qué puede exportar/ver en el back office de Tipsi.

Relacionado: [[business-overview]], [[reference-fondeo-repo]].
