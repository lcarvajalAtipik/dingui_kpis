"""Cliente para la API interna de Tipsi Pro (backend-green.tipsipro.com).

Contrato REAL (descubierto por ingeniería inversa del back office + del bundle JS y
validado contra la cuenta de Dingui, 2026-07-07):

- Base: `https://backend-green.tipsipro.com`, rutas `/api/{Controller}/{Action}` (ASP.NET).
- **Autenticación en dos pasos**: se hace `GET /api/Login/LoginWeb` con cabecera HTTP
  Basic `base64("email:password")`; la respuesta 200 devuelve el usuario y, sobre todo,
  fija una **cookie de sesión** (`user_id` + `ARRAffinity` para el balanceo blue/green).
  El resto de endpoints autorizan con esa cookie (la Basic sola da 401 en ellos). Por eso
  hay que reutilizar el mismo cliente httpx (mantiene el cookie jar) y llamar a `login()`
  antes que nada.
- La mayoría de informes son **GET con query params**; unos pocos son POST con body JSON.
- **Los booleanos en query string van en minúscula** (`order=true`, `showIssues=false`);
  con `True`/`False` de Python el binding de ASP.NET falla con 500.
- Fechas: `YYYY-MM-DDTHH:MM:SS.mmm` (sin `Z`).
- Respuestas paginadas: `{ "Items": [...], "TotalItems": N, ... }` → parada exacta por
  TotalItems.
- `brandId`/`localId` (GUIDs) se resuelven solos: `Brands/GetUsersBrands` +
  `Locals/GetBrandLocalListAsync?brandId=...`.

Uso desde scripts (ver scripts/tipsi_extract.py):

    with TipsiClient() as t:          # email/password de .env
        t.login()                     # fija la cookie de sesión
        t.resolve_context()           # autodetecta brandId/localId
        for page, payload, rows, total in t.paged("Tickets/GetPagedTicketsAsync",
                                                   t.paged_params(frm, to, "tickets")):
            ...

API no documentada ni soportada por Tipsi: puede cambiar sin aviso. Conviene pactar el
acceso automatizado con ellos.
"""
from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterator

import httpx

from .. import config

# ─────────────────────────────────────────────────────────────────────────────
# Plataforma
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_BACKEND = "https://backend-green.tipsipro.com"
APP_ORIGIN = "https://tipsipro.com"
LOGIN_ACTION = "Login/LoginWeb"
BRANDS_ACTION = "Brands/GetUsersBrands"
LOCALS_ACTION = "Locals/GetBrandLocalListAsync"

TIPSI_DIR = config.DATA_DIR / "tipsi"
DISCOVERY_DIR = TIPSI_DIR / "discovery"
RAW_DIR = TIPSI_DIR / "raw"

DEFAULT_PAGE_SIZE = 200


# ─────────────────────────────────────────────────────────────────────────────
# Catálogo de informes. `kind` decide cómo se construyen los params y se itera:
#   paged  → {pageNumber,itemsPerPage,localId,startDate,endDate, **extra}, pagina por TotalItems
#   byday  → {localId, date, dateToCompare} por cada día del rango (informe por horas)
# `extra` son params fijos ya validados (columna de orden, flags). Orden: de más a menos
# granular / útil.
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Report:
    key: str
    action: str
    kind: str = "paged"                 # paged | byday
    method: str = "GET"                 # GET | POST
    extra: dict[str, Any] = field(default_factory=dict)
    detail: bool = False                # baja el detalle línea a línea de cada ítem (tickets)
    experimental: bool = False          # contrato no confirmado (puede fallar; se registra)
    desc: str = ""


REPORTS: tuple[Report, ...] = (
    Report("tickets", "Tickets/GetPagedTicketsAsync", kind="paged", detail=True,
           extra={"column": "CheckOutDate", "order": "true", "showIssues": "false"},
           desc="Tickets (cabecera) + detalle línea a línea con pagos, descuentos, IVA, "
                "camarero, mesa y comensales"),
    Report("ventas_totales", "SalesStatistics/GetLocalSalesAsync", kind="paged",
           extra={"column": "Date", "order": "true"},
           desc="Ventas diarias del local"),
    Report("descuentos", "SalesStatistics/GetListDiscounts", kind="paged",
           desc="Descuentos aplicados (+ resumen)"),
    Report("devoluciones", "SalesStatistics/GetListDevolutions", kind="paged",
           extra={"column": "ArticleName", "order": "true"},
           desc="Devoluciones / anulaciones por artículo"),
    Report("invitaciones", "SalesStatistics/GetListInvitations", kind="paged",
           extra={"column": "ArticleName", "order": "true"},
           desc="Invitaciones / consumos internos"),
    Report("ventas_por_personal", "SalesStatistics/GetListStaffSales", kind="paged",
           extra={"column": "StaffName", "order": "true"},
           desc="Ventas por camarero/empleado"),
    Report("arqueos", "ClosingCash/GetLocalClosingCashesAsync", kind="paged",
           desc="Cierres de caja (arqueos): desglose por forma de pago"),
    Report("salidas_caja", "ClosingCash/GetLocalCashFlowOutsAsync", kind="paged",
           desc="Salidas de caja"),
    Report("ventas_por_hora", "SalesStatistics/GetSaleDetailsDailyByHour", kind="byday",
           desc="Ventas por hora del día (uno por jornada)"),
    # --- Contrato aún no cerrado (POST con body propio); se intentan y se registran ----
    Report("ventas_por_articulo", "SalesStatistics/GetLocalSalesPerArticleAsync", kind="paged",
           method="POST", experimental=True,
           desc="Ventas por artículo (POST; contrato por confirmar — usar detalle de ticket)"),
    Report("ventas_por_familia", "SalesStatistics/GetLocalSalesPerFamilyAsync", kind="paged",
           method="POST", experimental=True,
           desc="Ventas por familia (POST; contrato por confirmar)"),
)

TICKET_DETAIL_ACTION = "Tickets/GetLocalTicketDetailsAsync"


# ─────────────────────────────────────────────────────────────────────────────
# Fechas
# ─────────────────────────────────────────────────────────────────────────────
def _parse_date(d: str | date) -> date:
    if isinstance(d, date):
        return d
    return datetime.strptime(d[:10], "%Y-%m-%d").date()


def fmt_dt(d: date, *, end: bool = False) -> str:
    """Formato que espera la API: 'YYYY-MM-DDTHH:MM:SS.mmm' (sin Z)."""
    return d.strftime("%Y-%m-%dT23:59:59.999" if end else "%Y-%m-%dT00:00:00.000")


def month_windows(start: str | date, end: str | date) -> list[tuple[date, date]]:
    """Divide [start, end] en ventanas mensuales inclusivas (sin huecos ni solapes)."""
    s, e = _parse_date(start), _parse_date(end)
    if s > e:
        return []
    windows: list[tuple[date, date]] = []
    cur = s
    while cur <= e:
        month_end = (date(cur.year, 12, 31) if cur.month == 12
                     else date(cur.year, cur.month + 1, 1) - timedelta(days=1))
        windows.append((cur, min(month_end, e)))
        cur = min(month_end, e) + timedelta(days=1)
    return windows


def day_range(start: date, end: date) -> Iterator[date]:
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


# ─────────────────────────────────────────────────────────────────────────────
# Respuestas: extracción de filas y detección de error
# ─────────────────────────────────────────────────────────────────────────────
_LIST_KEYS = ("items", "data", "results", "rows", "list", "records", "tickets", "value")
_ERROR_KEYS = ("error", "errormessage", "exceptionmessage", "modelstate", "errors", "message")


def _ci_get(payload: dict[str, Any], key_lower: str) -> Any:
    for k, v in payload.items():
        if k.lower() == key_lower:
            return v
    return None


def extract_rows(payload: Any) -> list[Any]:
    """Lista de filas de una respuesta, sea cual sea su envoltura (case-insensitive)."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in _LIST_KEYS:
            v = _ci_get(payload, k)
            if isinstance(v, list):
                return v
        for k in _LIST_KEYS:
            v = _ci_get(payload, k)
            if isinstance(v, dict):
                inner = extract_rows(v)
                if inner:
                    return inner
    return []


def total_items(payload: Any) -> int | None:
    """`TotalItems` de una respuesta paginada, si lo trae."""
    if isinstance(payload, dict):
        v = _ci_get(payload, "totalitems")
        if isinstance(v, int):
            return v
    return None


def response_error(payload: Any) -> str | None:
    """Mensaje si la respuesta parece un error de la API; None si es una respuesta normal
    (incluida una legítimamente vacía en pre-apertura)."""
    if not isinstance(payload, dict):
        return None
    # Una respuesta paginada normal trae Items/TotalItems aunque esté vacía.
    if _ci_get(payload, "items") is not None or _ci_get(payload, "totalitems") is not None:
        return None
    for k in _ERROR_KEYS:
        v = _ci_get(payload, k)
        if v:
            return str(v)[:300]
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Cliente HTTP
# ─────────────────────────────────────────────────────────────────────────────
def _coerce_params(params: dict[str, Any]) -> dict[str, Any]:
    """Serializa los valores para la query string: bool → 'true'/'false', quita None."""
    out: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, bool):
            out[k] = "true" if v else "false"
        else:
            out[k] = v
    return out


class TipsiClient:
    """Cliente httpx contra la API interna de Tipsi (Basic + cookie de sesión)."""

    _TRANSIENT = (429, 500, 502, 503, 504)

    def __init__(
        self,
        *,
        email: str | None = None,
        password: str | None = None,
        base_url: str | None = None,
        brand_id: str | None = None,
        local_id: str | None = None,
        timeout: float = 60.0,
        max_retries: int = 3,
        min_interval: float = 0.0,
        retry_500: bool = False,
    ) -> None:
        self.base_url = (base_url or config.TIPSI_API_BASE or DEFAULT_BACKEND).rstrip("/")
        self.brand_id = brand_id
        self.local_id = local_id
        self.local_name: str | None = None
        self.user: dict[str, Any] | None = None
        self.max_retries = max_retries
        self.min_interval = min_interval
        # Un 500 suele ser "parámetros inválidos" (no transitorio); por defecto NO se
        # reintenta para no multiplicar peticiones fallidas. Actívalo si el backend
        # da 500 intermitentes de verdad.
        self._transient = self._TRANSIENT if retry_500 else (429, 502, 503, 504)
        self._last_request = 0.0

        email = email or config.TIPSI_EMAIL
        password = password or config.TIPSI_PASSWORD
        if not email or not password:
            raise RuntimeError(
                "Faltan credenciales de Tipsi: define TIPSI_EMAIL/TIPSI_PASSWORD en .env."
            )
        auth = base64.b64encode(f"{email}:{password}".encode()).decode()
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            follow_redirects=True,
            headers={
                "Accept": "application/json, text/plain, */*",
                "Authorization": f"Basic {auth}",
                "Origin": APP_ORIGIN,
                "Referer": f"{APP_ORIGIN}/",
                "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"),
            },
        )

    # -- ciclo de vida ----------------------------------------------------------
    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "TipsiClient":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    # -- llamadas ---------------------------------------------------------------
    def _throttle(self) -> None:
        if self.min_interval <= 0:
            return
        elapsed = time.monotonic() - self._last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

    def _request(self, method: str, action: str, *, params: dict | None = None,
                 body: Any | None = None) -> Any:
        path = f"/api/{action.lstrip('/')}"
        qp = _coerce_params(params) if params else None
        last: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            self._throttle()
            try:
                resp = self._client.request(method, path, params=qp, json=body)
            except httpx.TransportError as exc:
                last = exc
                if attempt < self.max_retries:
                    time.sleep(min(2 ** attempt, 15))
                    continue
                raise
            finally:
                self._last_request = time.monotonic()

            if resp.status_code in self._transient and attempt < self.max_retries:
                time.sleep(self._retry_after(resp) or min(2 ** attempt, 15))
                continue
            resp.raise_for_status()
            if not resp.content:
                return None
            try:
                return resp.json()
            except json.JSONDecodeError:
                return {"_raw_text": resp.text}
        assert last is not None
        raise last

    @staticmethod
    def _retry_after(resp: httpx.Response) -> float | None:
        raw = resp.headers.get("Retry-After")
        return min(float(raw), 60.0) if raw and raw.isdigit() else None

    def get(self, action: str, params: dict | None = None) -> Any:
        return self._request("GET", action, params=params)

    def post(self, action: str, body: Any | None = None) -> Any:
        return self._request("POST", action, body=body if body is not None else {})

    # -- auth y contexto --------------------------------------------------------
    def login(self) -> dict[str, Any]:
        """GET LoginWeb con Basic → fija la cookie de sesión. Devuelve el usuario."""
        user = self.get(LOGIN_ACTION)
        self.user = user if isinstance(user, dict) else None
        return self.user or {}

    def resolve_context(self, brand_id: str | None = None, local_id: str | None = None) -> None:
        """Fija brandId/localId. Usa los pasados, si no los autodetecta de la cuenta."""
        self.brand_id = brand_id or self.brand_id
        self.local_id = local_id or self.local_id
        if not self.brand_id:
            brands = extract_rows(self.get(BRANDS_ACTION)) or self.get(BRANDS_ACTION)
            if isinstance(brands, list) and brands:
                self.brand_id = brands[0].get("Id")
        if not self.local_id and self.brand_id:
            locals_ = self.get(LOCALS_ACTION, {"brandId": self.brand_id})
            rows = locals_ if isinstance(locals_, list) else extract_rows(locals_)
            if rows:
                self.local_id = rows[0].get("Id")
                self.local_name = rows[0].get("Name")

    # -- construcción de params por informe -------------------------------------
    def paged_params(self, frm: date, to: date, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        p = {
            "localId": self.local_id,
            "startDate": fmt_dt(frm),
            "endDate": fmt_dt(to, end=True),
        }
        if extra:
            p.update(extra)
        return p

    def byday_params(self, day: date) -> dict[str, Any]:
        return {"localId": self.local_id, "date": fmt_dt(day, end=True),
                "dateToCompare": fmt_dt(day)}

    # -- paginación -------------------------------------------------------------
    def paged(
        self,
        action: str,
        params: dict[str, Any],
        *,
        method: str = "GET",
        page_size: int = DEFAULT_PAGE_SIZE,
        max_pages: int = 10_000,
    ) -> Iterator[tuple[int, Any, list[Any], int | None]]:
        """Itera páginas y cede (page, payload, filas, total). Parada exacta por TotalItems
        (con respaldo por página vacía/corta si el endpoint no lo devuelve)."""
        collected = 0
        for page in range(1, max_pages + 1):
            p = dict(params, pageNumber=page, itemsPerPage=page_size)
            payload = self.get(action, p) if method == "GET" else self.post(action, p)
            rows = extract_rows(payload)
            total = total_items(payload)
            yield page, payload, rows, total
            collected += len(rows)
            if not rows:
                break
            if total is not None:
                if collected >= total:
                    break
            elif len(rows) < page_size:
                break

    def ticket_detail(self, ticket_id: str) -> Any:
        return self.get(TICKET_DETAIL_ACTION, {"ticketId": ticket_id, "localId": self.local_id})


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades de descubrimiento (opcional): lo que capturó tipsi_discover.py
# ─────────────────────────────────────────────────────────────────────────────
def load_discovery_credentials(discovery_dir: Path | None = None) -> dict[str, Any]:
    d = discovery_dir or DISCOVERY_DIR
    path = d / "credentials.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def action_name(url: str) -> str | None:
    marker = "/api/"
    i = url.find(marker)
    if i == -1:
        return None
    return (url[i + len(marker):].split("?", 1)[0].strip("/")) or None
