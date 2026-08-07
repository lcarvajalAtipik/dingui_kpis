---
name: feedback-ask-more
description: Usuario prefiere que pregunte cuando dude en lugar de asumir. Auto mode no significa decidir todo.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

Cuando haya ambigüedad o falte información para una decisión que afecta el análisis (importe, frecuencia, mapeo de proveedor a partida, etc.) → **preguntar**, no asumir. (Feedback dado en fondeo_kpis el 27/05/2026: "no me gusta que asumes mucho y me preguntas poco, prefiero que me preguntes más cuando dudes".)

**⚠ REFORZADO 07/08/2026 ("importantísimo"):** presenté una deducción como hecho — etiqueté 74,50 € de diferencia en un pago como "portes" sin ningún documento que lo dijera. El usuario: "este tipo de deducciones no las hagas sin preguntarme, estas assumptions son peligrosas". La regla es dura: **una cifra o etiqueta que no salga de un documento (factura, extracto, sheet) NUNCA se escribe como hecho** en registro/Excel/memoria/respuestas.

**How to apply:**
- Varias interpretaciones plausibles → AskUserQuestion antes de codificar.
- Dato cuantitativo que no está en banco/sheets → preguntar.
- Cambio que afecta saldo/deuda/forecast → confirmar primero.
- **Conciliaciones inferidas (importe≈, cronología, alias): distinguir SIEMPRE tres niveles: (a) documentado, (b) aritmética exacta, (c) hipótesis. Las (c) se marcan "SIN justificar / hipótesis" y se preguntan al usuario ANTES de fijarlas; jamás inventar la explicación del hueco (portes, descuento, redondeo…).**
- Especialmente relevante en Dingui al principio: casi todo (proveedores, contratos, plantilla) está aún sin documentar — no rellenar huecos con datos de Fondeo.

Relacionado: [[feedback-chat-only-workflow]], [[feedback-no-prefilter-data]].
