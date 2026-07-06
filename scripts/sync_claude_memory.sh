#!/usr/bin/env bash
# Sync Claude Code memory directory ↔ repo (docs/claude-memory/)
#
# Uso:
#   bash scripts/sync_claude_memory.sh push     # Copia ~/.claude/.../memory → docs/claude-memory/
#   bash scripts/sync_claude_memory.sh pull     # Copia docs/claude-memory/ → ~/.claude/.../memory
#   bash scripts/sync_claude_memory.sh status   # Compara los dos directorios
#
# El path en ~/.claude/projects/ se calcula automáticamente a partir del directorio actual.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_MEMORY="$REPO_DIR/docs/claude-memory"

# Encode current repo path como hace Claude Code: reemplaza / y _ por -
# /Users/luismdecarvajal/Desktop/fondeo_kpis → -Users-luismdecarvajal-Desktop-fondeo-kpis
ENCODED_PATH="$(echo "$REPO_DIR" | tr '/_' '-')"
CLAUDE_MEMORY="$HOME/.claude/projects/${ENCODED_PATH}/memory"

cmd="${1:-status}"

case "$cmd" in
  push)
    echo "→ Copiando ~/.claude/.../memory → docs/claude-memory/"
    mkdir -p "$REPO_MEMORY"
    if [[ -d "$CLAUDE_MEMORY" ]]; then
      cp -r "$CLAUDE_MEMORY"/* "$REPO_MEMORY/"
      echo "  ✓ Copiados $(ls "$REPO_MEMORY" | wc -l | xargs) archivos a $REPO_MEMORY"
    else
      echo "  ⚠ No existe $CLAUDE_MEMORY"
      exit 1
    fi
    ;;
  pull)
    echo "→ Copiando docs/claude-memory/ → ~/.claude/.../memory"
    mkdir -p "$CLAUDE_MEMORY"
    if [[ -d "$REPO_MEMORY" ]]; then
      cp -r "$REPO_MEMORY"/* "$CLAUDE_MEMORY/"
      echo "  ✓ Copiados $(ls "$CLAUDE_MEMORY" | wc -l | xargs) archivos a $CLAUDE_MEMORY"
    else
      echo "  ⚠ No existe $REPO_MEMORY"
      exit 1
    fi
    ;;
  status)
    echo "Repo path:      $REPO_DIR"
    echo "Claude memory:  $CLAUDE_MEMORY"
    echo "Repo memory:    $REPO_MEMORY"
    echo ""
    if [[ -d "$CLAUDE_MEMORY" ]] && [[ -d "$REPO_MEMORY" ]]; then
      diff -rq "$CLAUDE_MEMORY" "$REPO_MEMORY" || true
    else
      [[ ! -d "$CLAUDE_MEMORY" ]] && echo "  ⚠ $CLAUDE_MEMORY no existe"
      [[ ! -d "$REPO_MEMORY" ]] && echo "  ⚠ $REPO_MEMORY no existe"
    fi
    ;;
  *)
    echo "Uso: $0 {push|pull|status}"
    exit 1
    ;;
esac
