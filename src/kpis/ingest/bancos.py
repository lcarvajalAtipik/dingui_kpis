"""Parsers de extractos bancarios → DataFrame normalizado.

Dingui opera solo con CaixaBank. El formato está documentado en memoria
([[bank-format-caixa]]) — es el mismo layout que ya conocemos de fondeo_kpis.
Si se abre cuenta en otro banco, añadir aquí su parser dedicado.

Output común:
    columns = ['bank', 'account_iban', 'booking_date', 'value_date',
               'amount_eur', 'concept', 'extra', 'raw_tx_id']
con tipos:
    booking_date, value_date  → pd.Timestamp
    amount_eur                → float (negativo = salida, positivo = entrada)
    concept                   → str
    extra                     → str (info adicional o ref)
    raw_tx_id                 → str (hash determinista para dedupe)

Las funciones devuelven (df, account_iban).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd


# ============================================================================
# Helpers comunes
# ============================================================================

def _hash_row(*parts: object) -> str:
    """Hash determinista para identificar una fila (dedup)."""
    s = "|".join(str(p) if p is not None else "" for p in parts)
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:16]


def _parse_iban(text: str) -> str | None:
    """Extrae IBAN español: ES + 22 dígitos. Tolera espacios entre grupos
    (CaixaBank usa 4+4+4+4+4)."""
    if not text:
        return None
    m = re.search(r"\bES\s*\d[\d\s]{20,40}", text)
    if not m:
        return None
    digits = re.sub(r"\s+", "", m.group(0))
    if len(digits) >= 24 and digits[:2] == "ES" and digits[2:24].isdigit():
        return digits[:24]
    return None


def _parse_amount_es(value) -> float | None:
    """Convierte '1.234,56' o '1.234,56 EUR' o numeric → float."""
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace("€", "").replace("EUR", "").strip()
    # Formato europeo: punto = miles, coma = decimal
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


# ============================================================================
# CaixaBank
# ============================================================================

def parse_caixa(path: Path) -> tuple[pd.DataFrame, str | None]:
    """Lee un export de CaixaBank en formato XLS antiguo (OLE2).

    Estructura (layout estable, ver memoria bank-format-caixa):
      Fila 0 col 0: título con el IBAN ("Movimientos de la cuenta ES..").
      Fila 1 col 0: "Importes expresados en euros".
      Fila 2: headers = Fecha | Fecha valor | Movimiento | Más datos | Importe | Saldo.
      Fila 3+: datos. Fechas datetime nativo Excel; importes float con signo.
    """
    raw = pd.read_excel(path, sheet_name=0, header=None, engine="xlrd")
    iban = _parse_iban(str(raw.iloc[0, 0]))

    # Headers en fila índice 2
    hdr_row = 2
    headers = raw.iloc[hdr_row].tolist()
    data = raw.iloc[hdr_row + 1:].copy()
    data.columns = headers
    data = data.dropna(how="all").reset_index(drop=True)

    out = pd.DataFrame({
        "bank": "caixa",
        "account_iban": iban,
        "booking_date": pd.to_datetime(data["Fecha"], dayfirst=True, errors="coerce"),
        "value_date": pd.to_datetime(data["Fecha valor"], dayfirst=True, errors="coerce"),
        "amount_eur": data["Importe"].apply(lambda v: float(v) if not pd.isna(v) else None),
        "concept": data["Movimiento"].astype(str).str.strip(),
        "extra": data["Más datos"].astype(str).str.strip().replace("nan", ""),
    })
    # El Saldo entra en el hash: evita colisiones entre cargos idénticos del mismo día
    # (mismo día + importe + concepto) y es estable entre exports solapados.
    saldo = data.get("Saldo", pd.Series([None] * len(data)))
    out["raw_tx_id"] = [
        _hash_row(r["bank"], r["booking_date"], r["amount_eur"], r["concept"], r["extra"], s)
        for (_, r), s in zip(out.iterrows(), saldo)
    ]
    return out, iban


# ============================================================================
# Dispatcher: por nombre de archivo decide qué parser usar
# ============================================================================

def parse_any(path: Path) -> tuple[pd.DataFrame, str | None, str]:
    """Detecta el banco por filename y aplica el parser correspondiente.

    Devuelve (df, iban, bank_label). CaixaBank exporta como
    `Movimientos_cuenta_{ultimos7_iban} (N).xls`.
    """
    name = path.name.lower()
    if name.startswith("movimientos_cuenta_") or name.startswith("movimientos_cuenta"):
        df, iban = parse_caixa(path)
        return df, iban, "caixa"
    raise ValueError(
        f"No reconozco el formato del archivo: {path.name}. "
        "Solo hay parser de CaixaBank — si es de otro banco, añadir parser en ingest/bancos.py."
    )
