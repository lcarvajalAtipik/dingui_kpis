"""Categorizador de movimientos bancarios → categorías P&L de Dingui.

Misma arquitectura en cascada que fondeo_kpis, pero con reglas propias:
los proveedores y conceptos bancarios de Dingui son completamente distintos,
así que las reglas se construyen desde cero conforme lleguen los extractos.

Cascada:
  1) Match exacto del concepto normalizado contra reglas aprendidas del ground truth.
  2) Resolución de ambigüedades conocidas (UME, etc.).
  3) Match por substring/keyword (HARDCODED_PATTERNS).
  4) Marca distribuidora en abono entrante → Rappels.
  5) Fuzzy match contra el histórico para residuales.
  6) Default abono por transferencia → Ingresos.
  7) Si nada, devuelve None (a marcar "Sin categorizar" para revisión humana).

Ground truth: hoja `movimientos 30 abril 2026` del sheet "Proyecciones PuertoSantamaria"
(descargado a `data/categorization/proyecciones_puertosantamaria.xlsx`). Columnas:
Concepto | Fecha | Importe | Saldo | Mes | Año | Año-mes | Tipo. La categoría es `Tipo`.

OJO fase pre-apertura (hasta que abra el local): las transferencias entrantes
(TRASPASO / TRANSF. A SU FAVOR / TRANSFER INMEDIATA) son APORTACIONES de socios y así
las aprende el exact-match. Al abrir, revisar esas reglas: pasarán a convivir con
pagos de clientes por transferencia (→ Ingresos). Ver memoria pl-categories.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from . import config


# ============================================================================
# Normalización de concepto bancario
# ============================================================================

def _strip_accents(s: str) -> str:
    """Convierte á→a, é→e, ñ→n, etc. para comparar texto sin importar acentos."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def normalize_concept(raw: str) -> str:
    """Quita ruido típico para hacer conceptos comparables.

    Aplica:
      - lowercase
      - quita tildes (ñ→n, á→a, etc.) para tolerar variantes ortográficas
      - elimina DocNum:NNNN
      - elimina fechas DD/MM/YYYY
      - elimina IDs largos (15+ dígitos seguidos) pero PRESERVA números medianos
        que pueden ser contratos de préstamo (~10-12 dígitos)
      - normaliza espacios
    """
    if not isinstance(raw, str):
        return ""
    s = raw.lower().strip()
    s = _strip_accents(s)
    s = re.sub(r"-\s*docnum:\d+", "", s)
    s = re.sub(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b", "", s)
    s = re.sub(r"\b\d{15,}\b", "", s)  # solo eliminar números muy largos (no contratos)
    s = re.sub(r"\bdel\s+\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b", "", s)
    s = re.sub(r"\b\d{4}[xX*]+\d{4}\b", "<tarjeta>", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.strip(",.-: ")


# ============================================================================
# Reglas hard-coded — punto de partida para Dingui
# ============================================================================

# Patrones (substring case-insensitive en concepto normalizado) → categoría.
# Se aplican en orden — primer match gana. Usar después del exact-match.
HARDCODED_PATTERNS: list[tuple[str, str]] = [
    # IMPORTANTE: orden = prioridad. Patrones MÁS específicos primero.
    # El matching es contra concepto + extra concatenados (ver categorize()).

    # --- Universales de banca / impuestos (válidos para cualquier local) ---
    ("seguros sociales tgss", "Nominas"),
    ("transferencia a seguridad social", "Nominas"),
    ("irpf retenciones", "Nominas"),
    ("cuota impagada prestamo", "Financiero"),
    ("comision ", "Financiero"),
    ("intereses", "Financiero"),
    ("precio abono trf", "Financiero"),
    ("precio ed. extracto", "Financiero"),
    ("canje de efectivo", "Financiero"),
    # Gastos de servicio CaixaBank (vistos en el ground truth de Dingui)
    ("p.serv", "Financiero"),          # P.SERV. TRF. AJENA, P.SERV.CERTIF.
    ("precio servic", "Financiero"),   # PRECIO SERVIC.PAGOS
    ("corresp.", "Financiero"),        # CORRESP. MM/YYYY (correo/extracto)
    # TPV / datáfono
    ("abono tpv", "Ingresos"),
    # Rappels explícitos en el concepto
    ("rappel", "Rappels"),
    # Energía (utilities)
    ("endesa energia", "Costes Fijos"),
    ("naturgy", "Costes Fijos"),
    ("iberdrola", "Costes Fijos"),

    # ========================================================================
    # PROVEEDORES / CONCEPTOS DINGUI (confirmados por el ground truth del sheet,
    # hoja "movimientos 30 abril 2026"). Ampliar conforme lleguen extractos.
    # ========================================================================

    # Alquiler del local — arrendador Realmivo SL, cuota 2.297,02 €/mes
    ("realmivo", "Alquiler/Fianza"),
    ("cuota comunidad", "Alquiler/Fianza"),
    ("cuota cominidad", "Alquiler/Fianza"),  # typo visto en el sheet
    ("fianza y garantia", "Alquiler/Fianza"),
    # Tributos pre-apertura = tasas de licencias/ICIO (NO nóminas — aún no hay plantilla)
    ("tributos", "Licencia/Trámites"),
    # Software / gestión
    ("docusign", "Legal, gestión, software"),
    ("godaddy", "Legal, gestión, software"),
    ("apple.com/bill", "Legal, gestión, software"),
    ("adobe systems", "Legal, gestión, software"),
    ("google workspace", "Legal, gestión, software"),
    ("trimble", "Legal, gestión, software"),  # SketchUp; unificado (confirmado user 2026-07-06)
    # Notaría → Legal (confirmado user 2026-07-06; OJO en Fondeo notaría era Financiero)
    ("notaria", "Legal, gestión, software"),
    ("notariado", "Legal, gestión, software"),
]


# ============================================================================
# Marcas distribuidoras → categoría Rappels
# ============================================================================
# Cuando un ABONO entrante (importe > 0) viene de una de estas marcas, es un
# rappel comercial (descuento por compras de su producto), no un ingreso normal.
# Punto de partida: marcas nacionales típicas. Ajustar a los distribuidores
# reales de Dingui cuando se confirmen.

RAPPEL_BRANDS: list[str] = [
    "mahou",
    "heineken",
    "damm",
    "redbull",
    "red bull",
    "coca cola",
    "cocacola",
    "coca-cola",
    "diageo",
    "pernod ricard",
]


def is_rappel_brand(concept: str) -> bool:
    norm = normalize_concept(concept)
    return any(b in norm for b in RAPPEL_BRANDS)


# ============================================================================
# Patrones que indican una transferencia entrante (default = Ingresos)
# ============================================================================
# Si importe > 0 y matchea uno de estos patrones, default a "Ingresos"
# salvo que (a) sea de una marca rappel, (b) ya esté en reglas exactas.

INGRESO_TRANSFERENCIA_PATTERNS: list[str] = [
    "abono transferencia de",
    "transferencia de ",
    "transfer inmediata",
    "transf. a su favor",
]


# ============================================================================
# Política ignorar_fx — POR DEFINIR para Dingui
# ============================================================================
# En Fondeo, `ignorar_fx=TRUE` excluía del cashflow los gastos pagados con la
# tarjeta personal del socio y ciertos traspasos. Para Dingui aún no hay
# política: la lista queda vacía hasta que el usuario la defina.

IGNORAR_FX_PATTERNS: list[str] = []


def should_ignore_fx(concept: str) -> bool:
    """Devuelve True si el concepto matchea la policy de ignorar_fx del usuario."""
    norm = normalize_concept(concept)
    return any(p in norm for p in IGNORAR_FX_PATTERNS)


# ============================================================================
# Resolutores específicos para conceptos ambiguos del histórico
# ============================================================================

def resolve_ambiguous(concept_norm: str, importe: float, bank: str | None = None) -> str | None:
    """Conceptos que en el histórico tienen 2+ categorías se resuelven aquí por
    contexto (importe, signo, banco)."""
    # UME (equipo de sonido/luces): cargo grande = compra Sonido/Luces;
    # abono = devolución que el usuario marcó como Financiero.
    if concept_norm == "ume":
        return "Sonido/Luces" if importe is not None and importe < 0 else "Financiero"
    return None


# ============================================================================
# Carga de reglas aprendidas desde el ground truth
# ============================================================================

@dataclass(frozen=True)
class Rule:
    concept_norm: str
    category: str
    support: int  # cuántas veces se vio en el histórico
    confidence: float  # fracción del support sobre el total de ese concepto


# Sheet "Proyecciones PuertoSantamaria" del usuario, descargado de Drive
# (id 1Qpcu53iCU4neCCV0kQaSeLPpObLYEvMFM2zSDTbvTew). Refrescar re-descargando.
GROUND_TRUTH_XLSX = "proyecciones_puertosantamaria.xlsx"
GROUND_TRUTH_SHEET = "movimientos 30 abril 2026"
GT_COL_CONCEPT = "Concepto"
GT_COL_CATEGORY = "Tipo"


def _default_sheet_path() -> Path:
    return config.REPO_ROOT / "data" / "categorization" / GROUND_TRUTH_XLSX


def _load_ground_truth(sheet_path: Path) -> pd.DataFrame | None:
    """Lee la hoja de movimientos categorizados del sheet del usuario, o None si no existe.

    OJO: en el sheet el usuario a veces sobreescribe el concepto del banco con una
    descripción propia ("alquiler febrero", "acopio material"...). Esas filas generan
    reglas que no matchearán contra el extracto crudo — cubren la revisión manual,
    no la ingesta automática.
    """
    if not sheet_path.exists():
        return None
    df = pd.read_excel(sheet_path, sheet_name=GROUND_TRUTH_SHEET, engine="openpyxl")
    df["concept_norm"] = df[GT_COL_CONCEPT].apply(normalize_concept)
    df["category"] = df[GT_COL_CATEGORY].astype(str).str.strip()
    return df


def load_rules_from_ground_truth(
    sheet_path: Path | None = None,
    min_support: int = 1,
    min_confidence: float = 0.9,
) -> dict[str, Rule]:
    """Extrae reglas exactas concepto_norm → categoría desde el sheet del usuario.

    Solo guarda reglas donde el concepto es consistente (≥ min_confidence en una
    sola categoría) y con suficiente volumen (≥ min_support). Si el sheet no
    existe todavía (Dingui arranca sin histórico), devuelve dict vacío.
    """
    df = _load_ground_truth(sheet_path or _default_sheet_path())
    if df is None:
        return {}

    rules: dict[str, Rule] = {}
    for concept_norm, group in df.groupby("concept_norm"):
        if not concept_norm:
            continue
        cats = group["category"].value_counts()
        total = cats.sum()
        if total < min_support:
            continue
        top_cat = cats.index[0]
        top_n = int(cats.iloc[0])
        confidence = top_n / total
        if confidence >= min_confidence:
            rules[concept_norm] = Rule(concept_norm, top_cat, total, confidence)
    return rules


# ============================================================================
# Categorizador principal
# ============================================================================

@dataclass
class CategorizeResult:
    category: str | None  # None = sin categorizar
    confidence: float  # 0-1
    method: str  # 'exact', 'hardcoded', 'ambiguous_resolved', 'fuzzy', 'unmatched'
    matched_pattern: str | None = None


class Categorizer:
    def __init__(self, sheet_path: Path | None = None) -> None:
        sheet_path = sheet_path or _default_sheet_path()
        self.exact_rules = load_rules_from_ground_truth(sheet_path)
        # Para fuzzy match cargamos también los conceptos del histórico
        self._historical_concepts: list[tuple[str, str]] = []
        df = _load_ground_truth(sheet_path)
        if df is not None:
            for cn, group in df.groupby("concept_norm"):
                if not cn:
                    continue
                modal = group["category"].mode()
                if len(modal):
                    self._historical_concepts.append((cn, modal.iloc[0]))

    def categorize(
        self,
        concept: str,
        importe: float | None = None,
        bank: str | None = None,
        extra: str | None = None,
    ) -> CategorizeResult:
        # Combinamos concept + extra: CaixaBank pone info clave (nº contrato, emisor)
        # en el campo "Más datos" en lugar de en el concepto principal.
        full_text = f"{concept or ''} {extra or ''}"
        norm = normalize_concept(full_text)
        if not norm:
            return CategorizeResult(None, 0.0, "unmatched")

        norm_concept_only = normalize_concept(concept)

        # 1) Match exacto en reglas aprendidas del ground truth
        if norm_concept_only in self.exact_rules:
            r = self.exact_rules[norm_concept_only]
            return CategorizeResult(r.category, r.confidence, "exact", norm_concept_only)

        # 2) Ambigüedad conocida del histórico
        amb = resolve_ambiguous(norm, importe or 0, bank)
        if amb is not None:
            return CategorizeResult(amb, 0.95, "ambiguous_resolved", norm)

        # 3) Hardcoded substring patterns (incluyen las reglas user-confirmed).
        for pattern, category in HARDCODED_PATTERNS:
            pat_norm = _strip_accents(pattern.lower())
            if pat_norm in norm:
                return CategorizeResult(category, 0.85, "hardcoded", pattern)

        # 4) Rappel brand: solo si NADA de lo anterior matcheó, para abonos entrantes
        #    de marcas distribuidoras.
        if importe is not None and importe > 0:
            for b in RAPPEL_BRANDS:
                if b in norm:
                    return CategorizeResult("Rappels", 0.95, "rappel_brand", b)

        # 5) Fuzzy match contra histórico (ratio ≥ 0.85) — recupera variantes ortográficas
        best_ratio = 0.0
        best_cat: str | None = None
        best_match: str | None = None
        for hist_concept, hist_cat in self._historical_concepts:
            r = SequenceMatcher(None, norm_concept_only, hist_concept).ratio()
            if r > best_ratio:
                best_ratio = r
                best_cat = hist_cat
                best_match = hist_concept
        if best_ratio >= 0.85 and best_cat:
            return CategorizeResult(best_cat, best_ratio, "fuzzy", best_match)

        # 6) Default para abonos entrantes por transferencia → "Ingresos"
        #    (clientes B2B / eventos privados pagando por transferencia; las marcas
        #    rappel ya fueron filtradas en el paso 4).
        if importe is not None and importe > 0:
            if any(p in norm for p in INGRESO_TRANSFERENCIA_PATTERNS):
                return CategorizeResult("Ingresos", 0.70,
                                        "ingreso_transferencia_default", norm)

        # 7) Sin matching
        return CategorizeResult(None, 0.0, "unmatched")
