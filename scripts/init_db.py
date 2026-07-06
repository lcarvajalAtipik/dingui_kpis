"""Crea la base SQLite local aplicando todos los `schemas/*.sql`.

Idempotente — se puede ejecutar tantas veces como haga falta.
Uso: `uv run python scripts/init_db.py`
"""
from __future__ import annotations

from kpis import config, db


def main() -> None:
    applied = db.apply_schemas()
    print(f"DB lista en: {config.DB_PATH}")
    print(f"Schemas aplicados: {', '.join(applied) if applied else '(ninguno)'}")


if __name__ == "__main__":
    main()
