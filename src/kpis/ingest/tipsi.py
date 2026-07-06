"""Cliente Tipsi (PoS).

PENDIENTE: confirmar el mecanismo de acceso a los datos de Tipsi.
Opciones a explorar cuando el usuario dé acceso:
  a) API (si Tipsi la expone) — auth y endpoints por descubrir.
  b) Exports del back office (CSV/XLSX) → parsear a `tipsi_sales` / `tipsi_products`.

El equivalente en fondeo_kpis fue REVO (`ingest/revo.py` + `scripts/revo_probe_*.py`);
esos probes sirven de plantilla para explorar la API de Tipsi.
"""
from __future__ import annotations

import httpx

from .. import config


class TipsiClient:
    def __init__(
        self,
        *,
        user: str | None = None,
        token: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
    ) -> None:
        self.user = user or config.TIPSI_API_USER
        self.token = token or config.TIPSI_API_TOKEN
        self.base_url = (base_url or config.TIPSI_API_BASE or "").rstrip("/")
        if not self.base_url:
            raise RuntimeError("Falta TIPSI_API_BASE en .env (URL de la API por confirmar)")
        if not self.token:
            raise RuntimeError("Falta TIPSI_API_TOKEN en .env")
        headers = {"Accept": "application/json"}
        if not self.user:
            # Si no hay usuario, probamos Bearer. Si lo hay, httpx usa Basic vía `auth`.
            headers["Authorization"] = f"Bearer {self.token}"
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            auth=(self.user, self.token) if self.user else None,
            headers=headers,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "TipsiClient":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def get(self, path: str, **kwargs: object) -> httpx.Response:
        return self._client.get(path, **kwargs)
