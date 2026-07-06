# Claude Code memory — backup en repo

Este directorio es una **copia versionada** de la memoria del Claude Code CLI para este proyecto.
La fuente "viva" original vive en `~/.claude/projects/-Users-<usuario>-Desktop-dingui-kpis/memory/`,
fuera del repo.

## Por qué está aquí

Las memorias del Claude Code son locales a cada máquina. Para que viajen entre ordenadores
(laptop, oficina, etc.), se copian a este directorio que SÍ se versiona en git.

## Cómo usar

### En máquina nueva (primera vez)

```bash
git clone <repo>
cd dingui_kpis
bash scripts/sync_claude_memory.sh pull
```

Esto crea `~/.claude/projects/<encoded>/memory/` y copia todos los archivos. La próxima vez
que abras Claude Code en este proyecto, tendrá toda la memoria disponible.

### Para guardar cambios de memoria desde Claude (push al repo)

```bash
bash scripts/sync_claude_memory.sh push
git add docs/claude-memory/
git commit -m "memoria Claude: actualización"
git push
```

(Además, el hook de `.claude/settings.local.json` copia automáticamente al repo cada memoria
que Claude escribe — el push manual es el fallback.)

### Para ver diferencias entre repo y memoria activa

```bash
bash scripts/sync_claude_memory.sh status
```

## Notas

- El script calcula el `encoded path` de Claude Code automáticamente desde el directorio del repo.
- Las memorias son archivos markdown legibles. Puedes editarlas a mano si hace falta.
- `MEMORY.md` es el índice; las demás son una por concepto.
