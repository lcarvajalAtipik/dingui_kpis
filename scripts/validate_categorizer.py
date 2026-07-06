"""Valida el categorizador contra el ground truth del usuario.

Recorre la hoja de movimientos categorizados (Tipo = verdad) y compara con lo que
predice el Categorizer. Reporta accuracy global, por método, y el detalle de fallos.

OJO: las reglas exact se aprenden de este mismo sheet, así que la métrica mide sobre
todo COBERTURA (cuánto se auto-categoriza) y consistencia de la cascada, no
generalización pura. La prueba real llegará con el primer extracto crudo de CaixaBank.

Uso: `uv run python scripts/validate_categorizer.py`
"""
from __future__ import annotations

import pandas as pd

from kpis.categorizer import Categorizer, _default_sheet_path, _load_ground_truth


# Correcciones confirmadas por el usuario (2026-07-06) sobre inconsistencias del sheet.
# (concepto, importe) → categoría buena. Sustituyen al Tipo del sheet en la validación.
CONFIRMED_CORRECTIONS: dict[tuple[str, float], str] = {
    ("Trimble", -18.99): "Legal, gestión, software",        # 1 vez estaba como "Otros"
    ("PRECIO SERVIC.PAGOS", -137.34): "Financiero",          # comisión banco, no software
    # Devolución de provisión de notaría — imposible de distinguir por concepto
    # ("TRANSF. A SU FAVOR" = mismo que aportaciones). Se resuelve con user_override
    # en la ingesta; aquí queda como el único caso manual conocido.
    ("TRANSF. A SU FAVOR", 524.15): "Legal, gestión, software",
}


def main() -> None:
    gt = _load_ground_truth(_default_sheet_path())
    if gt is None:
        print(f"No existe el ground truth en {_default_sheet_path()}")
        return

    cat = Categorizer()
    print(f"Ground truth: {len(gt)} movimientos  |  reglas exact aprendidas: {len(cat.exact_rules)}")
    print(f"Rango fechas: {pd.to_datetime(gt['Fecha']).min().date()} → "
          f"{pd.to_datetime(gt['Fecha']).max().date()}")

    rows = []
    for _, r in gt.iterrows():
        importe = float(r["Importe"])
        real = CONFIRMED_CORRECTIONS.get((str(r["Concepto"]), importe), r["category"])
        res = cat.categorize(str(r["Concepto"]), importe=importe)
        rows.append({
            "concept": r["Concepto"],
            "importe": importe,
            "real": real,
            "pred": res.category,
            "method": res.method,
            "ok": res.category == real,
        })
    df = pd.DataFrame(rows)

    total = len(df)
    categorized = df["pred"].notna().sum()
    correct = df["ok"].sum()
    print(f"\nCobertura:  {categorized}/{total} ({categorized/total*100:.1f}%) auto-categorizados")
    print(f"Aciertos:   {correct}/{total} ({correct/total*100:.1f}%) coinciden con el Tipo del usuario")

    print("\nPor método:")
    by_m = df.groupby("method").agg(n=("ok", "count"), aciertos=("ok", "sum"))
    by_m["accuracy_%"] = (by_m["aciertos"] / by_m["n"] * 100).round(1)
    print(by_m.to_string())

    fails = df[~df["ok"]]
    print(f"\nFallos / sin categorizar: {len(fails)}")
    for _, f in fails.iterrows():
        print(f"  [{f['importe']:>10,.2f}€]  {str(f['concept'])[:45]:45s}  "
              f"real='{f['real']}'  pred='{f['pred']}'  ({f['method']})")


if __name__ == "__main__":
    main()
