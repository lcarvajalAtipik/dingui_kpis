"""Parsers de extractos bancarios → DataFrame normalizado.

Dingui opera con dos cuentas (ambas de Nuevo VH SL):
  - CaixaBank: export CSV de CaixaBankNow ("CaixaBank_digital_CaixaBankNow_*.csv").
    OJO: NO es el XLS antiguo de Fondeo — ver [[bank-format-caixa]].
  - Santander (ES47 0049 7343 71 2310017971, abierta 06/2026 para el TPV):
    export XLSX con extensión .xls ("Documento_*.xls", contenedor zip OOXML).

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


def parse_caixa_now(path: Path) -> tuple[pd.DataFrame, str | None]:
    """Lee el export CSV de CaixaBankNow (banca digital).

    Formato (validado con el primer export real de Dingui, 08/07/2026):
      - Separador `;`, sin comillas. Header: Concepto;Fecha;Importe;Saldo.
      - Orden descendente (más reciente primero).
      - Concepto TRUNCADO a ~18 chars por el banco ("MAKRO CENTRO 18", "BARTER CONSULTANC").
      - Fecha DD/MM/YYYY. Importe/Saldo tipo "+1.000,00EUR" / "-293,48EUR"
        (separador de miles opcional, coma decimal, sufijo EUR pegado).
      - NO incluye IBAN ni fecha valor.
    """
    df = pd.read_csv(path, sep=";", dtype=str)
    fechas = pd.to_datetime(df["Fecha"], dayfirst=True, errors="coerce")
    out = pd.DataFrame({
        "bank": "caixa",
        "account_iban": None,  # el CSV no trae IBAN
        "booking_date": fechas,
        "value_date": fechas,
        "amount_eur": df["Importe"].apply(_parse_amount_es),
        "concept": df["Concepto"].astype(str).str.strip(),
        "extra": "",
    })
    saldo = df["Saldo"].apply(_parse_amount_es)
    out["raw_tx_id"] = [
        _hash_row(r["bank"], r["booking_date"], r["amount_eur"], r["concept"], r["extra"], s)
        for (_, r), s in zip(out.iterrows(), saldo)
    ]
    return out, None


# ============================================================================
# Santander
# ============================================================================

def parse_santander(path: Path) -> tuple[pd.DataFrame, str | None]:
    """Lee el export de Santander ("Documento_*.xls" — en realidad XLSX/zip).

    Estructura (validada con el primer export, 08/07/2026):
      - 1 sheet "movimientos". Filas 1-5: titular / saldos / cuenta.
      - Fila 5 col C: IBAN ("ES47 0049 7343 71 2310017971").
      - Fila 7 (índice): headers = Fecha Operación | Fecha Valor | Concepto |
        Importe | Divisa | Saldo | Divisa | Código | Número de documento |
        Referencia 1 | Referencia 2 | Información adicional.
      - Fechas string DD/MM/YYYY; importes float nativos con signo.
      - En liquidaciones TPV ("Liquidacion Efectuada El ... A Edingui ...")
        Referencia 1 lleva el importe BRUTO cobrado; el Importe es el neto
        tras la comisión del datáfono.
    """
    raw = pd.read_excel(path, sheet_name=0, header=None, engine="openpyxl")
    # El IBAN está en la celda bajo el rótulo "Cuenta" (layout fijo: fila 5, col 2)
    iban = None
    for _, row in raw.head(8).iterrows():
        for cell in row:
            found = _parse_iban(str(cell)) if cell is not None else None
            if found:
                iban = found
                break
        if iban:
            break

    hdr_row = raw.index[raw.iloc[:, 0].astype(str).str.strip() == "Fecha Operación"][0]
    data = raw.iloc[hdr_row + 1:].copy()
    data.columns = [str(c).strip() for c in raw.iloc[hdr_row]]
    data = data.dropna(subset=["Importe"]).reset_index(drop=True)

    # "Referencia 1" (bruto TPV o ref transferencia) como extra para categorizar/auditar
    ref1 = data.get("Referencia 1", pd.Series([""] * len(data)))
    out = pd.DataFrame({
        "bank": "santander",
        "account_iban": iban,
        "booking_date": pd.to_datetime(data["Fecha Operación"], dayfirst=True, errors="coerce"),
        "value_date": pd.to_datetime(data["Fecha Valor"], dayfirst=True, errors="coerce"),
        "amount_eur": data["Importe"].astype(float),
        "concept": data["Concepto"].astype(str).str.strip(),
        "extra": ref1.astype(str).str.strip().replace("nan", ""),
    })
    saldo = data.get("Saldo", pd.Series([None] * len(data)))
    out["raw_tx_id"] = [
        _hash_row(r["bank"], r["booking_date"], r["amount_eur"], r["concept"], r["extra"], s)
        for (_, r), s in zip(out.iterrows(), saldo)
    ]
    return out, iban


# ============================================================================
# Dispatcher: por nombre/contenido decide qué parser usar
# ============================================================================

def parse_any(path: Path) -> tuple[pd.DataFrame, str | None, str]:
    """Detecta el banco por filename/contenido y aplica el parser correspondiente.

    Devuelve (df, iban, bank_label). Formatos conocidos:
      - `CaixaBank_digital_CaixaBankNow_*.csv` → CSV de CaixaBankNow.
      - `Movimientos_cuenta_{ultimos7_iban} (N).xls` → XLS antiguo CaixaBank (OLE2).
      - `Documento_*.xls` → Santander (zip OOXML pese a la extensión).
    Para archivos renombrados, distingue por contenido: CSV con header
    `Concepto;Fecha;...` → CaixaBankNow; zip → Santander; OLE2 → CaixaBank XLS.
    """
    import zipfile

    name = path.name.lower()
    if name.startswith("movimientos_cuenta"):
        df, iban = parse_caixa(path)
        return df, iban, "caixa"
    if path.suffix.lower() == ".csv":
        header = path.read_text(encoding="utf-8", errors="replace").split("\n", 1)[0]
        if header.strip().startswith("Concepto;Fecha;Importe"):
            df, iban = parse_caixa_now(path)
            return df, iban, "caixa"
    elif path.suffix.lower() in (".xls", ".xlsx"):
        if zipfile.is_zipfile(path):  # Santander exporta XLSX con extensión .xls
            df, iban = parse_santander(path)
            return df, iban, "santander"
        df, iban = parse_caixa(path)
        return df, iban, "caixa"
    raise ValueError(
        f"No reconozco el formato del archivo: {path.name}. "
        "Parsers disponibles: CaixaBank (XLS antiguo y CSV CaixaBankNow) y "
        "Santander (XLSX) — si es otro banco/formato, añadirlo en ingest/bancos.py."
    )
