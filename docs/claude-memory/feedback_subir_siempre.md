---
name: feedback-subir-siempre
description: "REGLA (usuario 30/09/2026): 'sube todo siempre tú' — subir facturas a Drive y hacer commit+push al repo sin pedir confirmación"
metadata:
  type: feedback
---

El usuario (30/09/2026), tras una ingesta de email en la que el push a GitHub quedó bloqueado y le pedí que lo hiciera él: **"sube todo siempre tú"**.

**Why:** no quiere hacer pasos manuales (subir a Drive, commit, push); lo delega entero.

**How to apply:** al cerrar cualquier ingesta/actualización: subir los documentos a Drive (montaje desktop, ver [[sistema-facturas-drive]]), `bash scripts/sync_claude_memory.sh push`, `git add` de lo tracked (email_registro.csv, registro_facturas.csv, docs/claude-memory…), commit y push a lcarvajalAtipik/dingui_kpis sin preguntar. Esto incluye facturas con dudas (p. ej. DJ Varosa con NIF inválido: se sube igual y la gestoría ya dirá). Relacionado: [[feedback-sync-memoria]].
