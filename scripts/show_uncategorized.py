"""Muestra los movimientos sin categorizar agrupados, listos para que el usuario los etiquete.

Salida: conceptos únicos con count, total €, fechas representativas.
También guarda CSV en outputs/uncategorized.csv para procesar.

Uso: `uv run python scripts/show_uncategorized.py`
"""
from __future__ import annotations

import pandas as pd

from kpis import config
from kpis.categorizer import Categorizer, normalize_concept, should_ignore_fx
from kpis.ingest.bancos import parse_any

INBOX = config.REPO_ROOT / "data" / "bancos" / "inbox"
OUT_DIR = config.REPO_ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BANK_LABELS = {"caixa": "CaixaBank"}


def collect_all() -> pd.DataFrame:
    cat = Categorizer()
    frames = []
    for path in sorted(p for p in INBOX.glob("*") if p.suffix.lower() in (".xls", ".xlsx")):
        try:
            df, _iban, bank_label = parse_any(path)
        except ValueError as e:
            print(f"⚠ SKIP {path.name}: {e}")
            continue
        df["bank_label"] = BANK_LABELS.get(bank_label, bank_label)
        cats, methods, confs = [], [], []
        for _, row in df.iterrows():
            r = cat.categorize(row["concept"], importe=row["amount_eur"], bank=row["bank"],
                               extra=row.get("extra"))
            cats.append(r.category)
            methods.append(r.method)
            confs.append(r.confidence)
        df["category"] = cats
        df["cat_method"] = methods
        df["cat_confidence"] = confs
        df["ignorar_fx"] = df["concept"].apply(should_ignore_fx)
        df["concept_norm"] = df["concept"].apply(normalize_concept)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def main() -> None:
    all_df = collect_all()
    if len(all_df) == 0:
        print(f"No hay archivos parseables en {INBOX}.")
        return
    unmatched = all_df[all_df["category"].isna()].copy()
    print(f"Total movimientos: {len(all_df)}")
    print(f"Sin categorizar: {len(unmatched)} ({len(unmatched)/len(all_df)*100:.1f}%)")

    # Guardar CSV con detalle
    out_csv = OUT_DIR / "uncategorized.csv"
    unmatched[["bank_label", "booking_date", "amount_eur", "concept", "extra",
               "concept_norm"]].to_csv(out_csv, index=False)
    print(f"\nCSV guardado en: {out_csv}\n")

    for bank in unmatched["bank_label"].unique():
        sub = unmatched[unmatched["bank_label"] == bank].copy()
        print(f"\n{'#' * 90}")
        print(f"  {bank}  —  {len(sub)} movimientos sin categorizar")
        print(f"{'#' * 90}")
        # Agrupar por concept_norm
        groups = sub.groupby("concept_norm").agg(
            n=("amount_eur", "count"),
            total=("amount_eur", "sum"),
            min_date=("booking_date", "min"),
            max_date=("booking_date", "max"),
            sample_concept=("concept", "first"),
            sample_extra=("extra", "first"),
        ).reset_index().sort_values(["n", "total"], ascending=[False, True])

        for _, g in groups.iterrows():
            sign = "+" if g["total"] >= 0 else ""
            dr = (
                g["min_date"].strftime("%Y-%m-%d") if pd.notna(g["min_date"]) else "?"
            ) + (
                "" if g["min_date"] == g["max_date"] or pd.isna(g["max_date"])
                else " → " + g["max_date"].strftime("%Y-%m-%d")
            )
            print(f"\n  [{g['n']:2d}× {sign}{g['total']:>11,.2f}€]  {dr}")
            print(f"     concepto:  {g['sample_concept'][:85]}")
            if g["sample_extra"] and str(g["sample_extra"]) not in ("nan", ""):
                print(f"     extra:     {str(g['sample_extra'])[:85]}")


if __name__ == "__main__":
    main()
