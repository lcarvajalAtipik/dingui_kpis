---
name: feedback-chat-only-workflow
description: "El usuario consume todo el análisis dentro de la conversación con Claude — nada de notebooks, dashboards o apps externas"
metadata:
  type: feedback
---

Toda la interfaz de análisis es la conversación con Claude. El usuario no quiere abrir Jupyter, Streamlit, dashboards ni herramientas separadas para ver resultados. (Preferencia establecida en fondeo_kpis; aplica igual aquí.)

**Why:** Lo dijo explícitamente en Fondeo: "la conversación siempre la voy a tener contigo por aquí por claude así que no quiero tener que abrir notebooks etc". Quiere fricción cero — pide, recibe respuesta en el chat.

**How to apply:**
- Scripts Python autoejecutables (yo los corro con Bash), no notebooks `.ipynb`.
- Resultados en el chat: tablas markdown, números en línea, o imágenes PNG en `outputs/` referenciadas con markdown.
- Nada de "abre este notebook y ejecuta la celda 3".
- No proponer dashboards (Streamlit, Metabase, Looker…) a menos que él lo pida.
