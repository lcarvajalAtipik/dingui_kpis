---
name: feedback-delegar-opus
description: "Comando del usuario para delegar trabajo a un subagente Opus 5 (extracción mecánica, lectura de imágenes/PDFs en bloque) mientras Fable orquesta y decide"
metadata:
  type: feedback
---

El usuario (2026-09-17) quiere un **comando explícito en el prompt** que signifique: "esto lo hace un subagente con Opus 5, tú (Fable) orquestas y consolidas".

**Comando:** cualquiera de estas formas en el prompt → delegar a Opus:
- `/opus` o `con Opus` o `usa Opus` o `delega a Opus`

(Propuesto por Claude como valor por defecto; el usuario puede cambiar la palabra. Si aparece otra forma inequívoca de "hazlo con Opus", aplicar igual.)

**Why:** ahorrar coste/tiempo en tareas mecánicas (leer fotos de facturas/tickets, extraer tablas de PDFs, procesar muchos archivos) sin perder el criterio de negocio, que depende de la memoria y del contexto de la conversación que solo tiene el orquestador.

**How to apply:**
- Lanzar `Agent` con `model: "opus"` y un prompt cerrado y autocontenido (rutas de archivos, formato de salida esperado, normalmente JSON). El subagente no tiene memoria ni contexto de la conversación: darle todo lo que necesite.
- Fable se queda con: categorías P&L ([[pl-categories]]), conciliación con proveedores, política [[ignorar-fx-convention]], decisiones y el resumen final al usuario.
- Sin el comando, trabajar como siempre (Fable directamente). Si la tarea es claramente delegable pero el usuario no lo ha dicho, proponerlo en una línea, no delegar por cuenta propia.
- Si el usuario quiere automatizarlo, la alternativa es un agente en `.claude/agents/<nombre>.md` con `model: opus` en el frontmatter.

Relacionado: [[feedback-ask-more]], [[feedback-chat-only-workflow]].
