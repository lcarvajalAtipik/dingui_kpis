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

    # ========================================================================
    # FASE OPERATIVA (apertura ≈ mediados de junio 2026, TPV desde el 18/06).
    # Reglas nuevas vistas en los extractos de mayo-julio 2026.
    # ========================================================================

    # --- Traspasos entre cuentas propias (Caixa ↔ Santander, titular Nuevo VH SL).
    # "Nuevo Vh" en el concepto = la propia sociedad → siempre interno.
    # Backup de mark_internal_transfers() para cuando falte la otra pata.
    ("de nuevo vh", "Movimiento entre cuentas"),
    ("a favor de nuevo vh", "Movimiento entre cuentas"),

    # --- TPV Santander: liquidaciones del datáfono = ventas (neto de comisión;
    # el bruto viene en Referencia 1 / extra). El detalle real de ventas está en Tipsi.
    ("liquidacion efectuada", "Ingresos"),

    # --- Confirming/factoring Santander: el abono y el cargo a vencimiento rotan
    # (neto 0); el coste real son los intereses ("comisiones/intereses" ya matchea
    # arriba). La factura subyacente financiada se reclasifica a mano si procede.
    ("factoring y confirming", "Financiero"),
    ("cobro a vencimiento", "Financiero"),

    # --- Gastos de servicio Santander (TPV y cuenta)
    ("cuota app android", "Financiero"),
    ("liquidacion del contrato", "Financiero"),
    ("liquidacion indemnizatorio", "Financiero"),

    # --- COGS: mayoristas de alimentación/bebida (compras del local)
    ("makro", "COGS"),
    ("picking gades", "COGS"),
    ("cash lepe", "COGS"),

    # --- Equipamiento sonido/luces (Thomann/Madrid HiFi/Betopper/Lightcloud)
    ("thomann", "Sonido/Luces"),
    ("madrid hifi", "Sonido/Luces"),
    ("betopperdj", "Sonido/Luces"),
    ("lightcloud", "Sonido/Luces"),

    # --- Costes fijos: telecom del local
    ("o2 fibra", "Costes Fijos"),

    # --- Asesorías/gestoría (recibos mensuales)
    ("stipendium", "Legal, gestión, software"),
    ("remesa ases", "Legal, gestión, software"),

    # ========================================================================
    # Categorías nuevas validadas por el usuario el 04/08/2026 tras conciliar
    # los movimientos con las facturas de Drive (registro_facturas.csv).
    # ========================================================================

    # --- Equipamiento: aparatos, menaje y ferretería del local.
    # ID Hostelería (neveras/mesa fría/tostadora) paga con conceptos manuales,
    # pero estos comercios sí se repiten en el extracto.
    ("bazar chino", "Equipamiento"),
    ("bazar vi", "Equipamiento"),        # BAZAR VI§ADOR (Viñador, encoding roto en Caixa)
    ("aqualar", "Equipamiento"),         # ferretería/mantenimiento
    ("suministrso unic", "Equipamiento"),  # typo del banco: Suministros Unic SL
    ("suministros unic", "Equipamiento"),
    ("decofiesta", "Equipamiento"),
    ("carref el paseo", "Equipamiento"),  # OJO: si empieza a haber compra de comida en Carrefour, revisar

    # --- Gastos extra actividad: gasto menor dentro de la actividad normal
    # (comidas del equipo, taxis, consumibles de puerta…)
    ("restaurante plato", "Gastos extra actividad"),
    ("rest.booking", "Gastos extra actividad"),
    ("venta la blanca", "Gastos extra actividad"),
    ("licencia taxi", "Gastos extra actividad"),

    # --- Marketing operativo
    ("barter consultanc", "Marketing"),   # Barter Consultancy: mensualidad marketing digital

    # --- Software operativo
    ("pago prezo", "Legal, gestión, software"),  # Prezo (Future is an Attitude SL)

    # --- Constructora: Lorente y Millán. Los pagos de certificaciones suelen ir
    # como "PAGO TRANSFERENCIAS" (ya exact-match → Obra) o conceptos manuales
    # "parte N certifica"; este patrón caza las variantes con "certifica".
    ("certifica", "Obra"),
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
    # Coca-Cola Europacific: cargo = compra de producto (COGS); abono = rappel.
    if "coca cola" in concept_norm or "coca-cola" in concept_norm:
        return "COGS" if importe is not None and importe < 0 else "Rappels"
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
            # Guardia de época: el GT pre-apertura enseñó TRASPASO/TRANSF. A SU
            # FAVOR/TRANSFER INMEDIATA → Aportaciones, pero una aportación nunca
            # es un cargo. Un "traspaso" SALIENTE es dinero movido a otra cuenta
            # propia (Santander desde 06/2026) → Movimiento entre cuentas.
            if r.category == "Aportaciones" and importe is not None and importe < 0:
                return CategorizeResult("Movimiento entre cuentas", 0.9,
                                        "ambiguous_resolved", norm_concept_only)
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


# ============================================================================
# Traspasos entre cuentas propias (Caixa ↔ Santander)
# ============================================================================
# Desde 06/2026 Nuevo VH SL tiene dos cuentas. Un traspaso interno aparece como
# cargo en una y abono en la otra → no es P&L. Se detecta cruzando importes
# opuestos entre bancos distintos con fechas cercanas. Se ejecuta ANTES de
# aceptar la categoría del categorizador (pisa lo que este diga).

INTERNAL_TRANSFER_CATEGORY = "Movimiento entre cuentas"

# Al menos una pata debe oler a transferencia/traspaso para no emparejar
# casualidades de importe (p.ej. un gasto y un ingreso iguales el mismo día).
_INTERNAL_HINTS = ("traspaso", "transfer", "transferencia", "nuevo vh", "santabder")


def mark_internal_transfers(df: pd.DataFrame, max_days: int = 3) -> pd.Series:
    """Devuelve una Series booleana: True = pata de un traspaso entre cuentas.

    Requiere columnas: bank, booking_date, amount_eur, concept. Empareja
    greedy 1:1 (cada pata solo se usa una vez) cargos de un banco con abonos
    del mismo importe en otro banco a ≤ max_days de distancia.
    """
    flags = pd.Series(False, index=df.index)
    candidates = df[
        df["concept"].astype(str).str.lower().apply(
            lambda c: any(h in _strip_accents(c) for h in _INTERNAL_HINTS)
        )
    ]
    outs = candidates[candidates["amount_eur"] < 0]
    ins_ = candidates[candidates["amount_eur"] > 0]
    used: set = set()
    for oi, o in outs.iterrows():
        m = ins_[
            (~ins_.index.isin(used))
            & (ins_["bank"] != o["bank"])
            & (ins_["amount_eur"].round(2) == round(-o["amount_eur"], 2))
            & ((ins_["booking_date"] - o["booking_date"]).abs().dt.days <= max_days)
        ]
        if len(m):
            ii = m.index[0]
            used.add(ii)
            flags.loc[[oi, ii]] = True
    return flags
