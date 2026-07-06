"""Procesa el xlsx editado por el usuario con las categorizaciones definitivas.

Compara `mi_sugerencia` (lo que Claude propuso) con `p_l` (decisión final del usuario).
Reporta:
  - Total filas
  - Distribución final por categoría
  - Filas donde el usuario cambió mi sugerencia (correcciones)
  - Filas donde el usuario llenó casillas vacías (nuevas reglas)
  - Filas marcadas como `ignorar_fx=TRUE`
  - Notas y comentarios

Genera además `outputs/user_review_processed.csv` con las decisiones finales para
integrarlas como reglas del categorizador.

Uso: `uv run python scripts/process_user_review.py <path_xlsx>`
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from kpis import config


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: uv run python scripts/process_user_review.py <path_xlsx>", file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"ERROR: archivo no existe: {src}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(src, engine="openpyxl")
    # Normaliza columnas (a veces Excel mete spaces / NaN raros)
    df.columns = [c.strip() for c in df.columns]
    for col in ("mi_sugerencia", "p_l", "ignorar_fx", "notas"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().replace({"nan": "", "NaN": ""})

    # Booleano ignorar_fx
    df["ignorar_fx_bool"] = df["ignorar_fx"].str.upper().isin(["TRUE", "1", "YES", "SI", "SÍ"])

    print(f"Total filas: {len(df)}")
    print(f"Cambios respecto a mi sugerencia: {(df['p_l'] != df['mi_sugerencia']).sum()}")
    print(f"Marcadas ignorar_fx=TRUE: {df['ignorar_fx_bool'].sum()}")

    print("\n=== DISTRIBUCIÓN FINAL POR p_l ===")
    print(df["p_l"].value_counts(dropna=False).to_string())

    print("\n=== CORRECCIONES (usuario cambió mi sugerencia) ===")
    changed = df[df["p_l"] != df["mi_sugerencia"]].copy()
    if len(changed) == 0:
        print("(ninguna)")
    else:
        for _, r in changed.iterrows():
            print(f"  [{r['bank']:9s}] {r['booking_date']}  {float(r['amount_eur']):>12,.2f}€  "
                  f"{r['concept'][:55]:55s}  "
                  f"mi='{r['mi_sugerencia']}' → tu='{r['p_l']}'"
                  + ("  [ignorar_fx]" if r["ignorar_fx_bool"] else "")
                  + (f"  notas:{r['notas']}" if r.get("notas") else ""))

    print("\n=== FILAS MARCADAS ignorar_fx=TRUE ===")
    igf = df[df["ignorar_fx_bool"]].copy()
    if len(igf) == 0:
        print("(ninguna)")
    else:
        for _, r in igf.iterrows():
            print(f"  [{r['bank']:9s}] {r['booking_date']}  {float(r['amount_eur']):>12,.2f}€  "
                  f"{r['concept'][:60]:60s}  → {r['p_l']}")

    print("\n=== NOTAS DEL USUARIO ===")
    notas_rows = df[df["notas"].astype(str).str.len() > 0]
    if len(notas_rows) == 0:
        print("(ninguna)")
    else:
        for _, r in notas_rows.iterrows():
            print(f"  [{r['bank']:9s}] {r['booking_date']}  {r['concept'][:50]}: {r['notas']}")

    # Salida procesada para integración
    out = config.REPO_ROOT / "outputs" / "user_review_processed.csv"
    df[["bank", "booking_date", "amount_eur", "concept", "extra",
        "mi_sugerencia", "p_l", "ignorar_fx", "ignorar_fx_bool", "notas"]].to_csv(out, index=False)
    print(f"\nCSV procesado guardado en: {out}")


if __name__ == "__main__":
    main()
