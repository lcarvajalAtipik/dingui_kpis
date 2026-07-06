"""Helpers para SQLite local."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from collections.abc import Iterator

from . import config


def connect() -> sqlite3.Connection:
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaction() -> Iterator[sqlite3.Connection]:
    conn = connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def apply_schemas() -> list[str]:
    """Ejecuta todos los `schemas/*.sql` en orden alfabético. Idempotente."""
    applied: list[str] = []
    sql_files = sorted(config.SCHEMAS_DIR.glob("*.sql"))
    with transaction() as conn:
        for sql_file in sql_files:
            conn.executescript(sql_file.read_text(encoding="utf-8"))
            applied.append(sql_file.name)
    return applied
