---
name: feedback-sync-memoria
description: "El usuario trabaja desde varios ordenadores — mantener repo (GitHub) y memoria sincronizados; ante 'update memoria para otro ordenador', hacer sync push + commit + push"
metadata:
  type: feedback
---

El usuario trabaja en este proyecto desde **más de un ordenador** (avisó el 2026-07-06 de que empezaba en una máquina nueva). Remoto: `https://github.com/lcarvajalAtipik/dingui_kpis.git` (mismo patrón que fondeo_kpis).

**Qué viaja por git:** código, esquemas, scripts, `docs/claude-memory/` (backup versionado de la memoria) y `.claude/settings.json` (hook de auto-copia de memoria).
**Qué NO viaja (recrear en cada máquina):** `data/` (re-descargar el sheet de Drive — ver [[reference-proyecciones-sheet]]), `db/` (regenerar con `init_db.py`), `outputs/`, `.env` (desde `.env.example`), auth de gcloud.

**How to apply:**
- Al cerrar una sesión con cambios de memoria o antes de que cambie de máquina: `bash scripts/sync_claude_memory.sh push` + `git add` + commit + push (el hook ya copia cada memoria al repo automáticamente; el push manual es el fallback).
- Cuando el usuario pida "update memoria para otro ordenador" o similar: ejecutar exactamente ese flujo.
- En máquina nueva: `git clone` → `uv sync` → `bash scripts/sync_claude_memory.sh pull` → seguir la sección "Setup en máquina nueva" del README.

Relacionado: [[reference-proyecciones-sheet]], [[gcp-auth-strategy]].
