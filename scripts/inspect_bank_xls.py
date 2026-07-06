"""Inspecciona archivos Excel bancarios (o de cualquier fuente) para aprender su layout.

Muestra por archivo: magic bytes (OLE2 vs ZIP), sheets, shape y primeras 15 filas.
Útil al recibir el primer export de CaixaBank de Dingui para validar que el layout
coincide con el documentado en memoria (bank-format-caixa).

Uso:
  uv run python scripts/inspect_bank_xls.py                 # todo data/bancos/inbox/
  uv run python scripts/inspect_bank_xls.py <path> [...]    # archivos concretos
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from kpis import config

INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"


def show(path: Path) -> None:
    print(f"\n{'=' * 80}")
    print(f"FILE: {path.name}  ({path.stat().st_size:,} bytes)")
    print("=" * 80)
    head = path.read_bytes()[:8].hex()
    print(f"first8 bytes hex: {head}  (d0cf11e0 = OLE2/xls antiguo; 504b0304 = ZIP/xlsx)")
    try:
        xl = pd.ExcelFile(path)
        print(f"sheets: {xl.sheet_names}")
        for sh in xl.sheet_names:
            df = xl.parse(sh, header=None)
            print(f"\n-- Sheet '{sh}': {df.shape[0]} rows x {df.shape[1]} cols")
            with pd.option_context("display.max_columns", None, "display.width", 200,
                                   "display.max_colwidth", 50):
                print(df.head(15).to_string())
    except Exception as e:
        print(f"  pandas read error: {type(e).__name__}: {e}")


def main() -> None:
    if len(sys.argv) > 1:
        paths = [Path(a) for a in sys.argv[1:]]
    else:
        paths = sorted(p for p in INBOX.glob("*") if p.suffix.lower() in (".xls", ".xlsx"))
    if not paths:
        print(f"No hay archivos que inspeccionar en {INBOX}")
        return
    for p in paths:
        if not p.exists():
            print(f"SKIP (not found): {p}", file=sys.stderr)
            continue
        show(p)


if __name__ == "__main__":
    main()
