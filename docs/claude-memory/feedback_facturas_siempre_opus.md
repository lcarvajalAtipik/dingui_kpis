---
name: feedback-facturas-siempre-opus
description: "REGLA (usuario 17/09/2026): revisar/leer facturas y documentos de la gestoría (PDF, xls, imágenes) NUNCA con Fable; siempre delegar a un subagente Opus. Fable solo consolida."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2d5cd319-1b67-48a7-9ce5-dd6ce5c74c27
  modified: 2026-09-17T10:51:39.426Z
---

El usuario (17/09/2026) fijó como regla permanente: **"no revises facturas con Fable, siempre Opus"**. Aplica a facturas, tickets, modelos de Hacienda (303, 111, 200), nóminas (RN/HS/IC/ITA de Stipendium), estados de cuentas de proveedores y cualquier PDF/xls/imagen documental.

**Why:** coste de tokens (Fable es el modelo caro) y el trabajo es mecánico; el criterio de negocio lo pone Fable al consolidar.

**How to apply:** ante cualquier documento de este tipo, lanzar `Agent` con `model: "opus"` y un prompt cerrado (rutas, campos a extraer, JSON de salida) sin esperar a que el usuario diga "con Opus". Fable no abre esos ficheros ni con Read ni con Bash (ni siquiera "para echar un vistazo"); como mucho lista nombres de fichero (`ls`/`find`) para armar el encargo. Es una versión más estricta de [[feedback-delegar-opus]]. Relacionado: [[sistema-facturas-drive]], [[conciliacion-iva-contable-junago]].
