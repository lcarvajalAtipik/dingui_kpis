#!/usr/bin/env python
"""Extractor de facturas del buzón de Dingui vía IMAP (Gmail).

Mismo espíritu que tipsi_extract.py: autoservicio con credenciales en .env,
idempotente (no re-descarga lo ya visto), estado versionado en git.

Config (.env):
    GMAIL_USER=info@dinguiclub.com
    GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx   (contraseña de aplicación, requiere 2FA)
    GMAIL_IMAP_HOST=imap.gmail.com           (opcional)

Uso:
    uv run python scripts/gmail_facturas.py                    # últimos 30 días
    uv run python scripts/gmail_facturas.py --dias 90
    uv run python scripts/gmail_facturas.py --desde 2026-06-01
    uv run python scripts/gmail_facturas.py --listar           # solo listar, sin descargar
    uv run python scripts/gmail_facturas.py --buscar "merino"  # además filtra por texto

Qué hace:
    1. Busca en INBOX (y "[Gmail]/Todos" si existe) correos con adjuntos
       PDF/JPG/PNG desde la fecha indicada. Sin pre-filtrar por "factura":
       se baja todo adjunto candidato y la clasificación la hace Claude después.
    2. Deduplica contra data/facturas/email_registro.csv (message_id + sha256
       del adjunto) y contra los sha256 de lo ya procesado.
    3. Descarga los adjuntos nuevos a data/facturas/email_inbox/ (gitignored)
       con nombre <fecha>_<remitente>_<nombre_original>.
    4. Apunta cada adjunto en email_registro.csv con estado 'descargado'.
       Estados posteriores ('subido_drive', 'procesado', 'descartado') los
       gestiona Claude al revisar la bandeja.
"""

import argparse
import csv
import email
import email.utils
import hashlib
import imaplib
import io
import os
import re
import sys
import unicodedata
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / "data" / "facturas" / "email_registro.csv"
INBOX_DIR = ROOT / "data" / "facturas" / "email_inbox"
CAMPOS = [
    "message_id", "fecha_email", "remitente", "asunto", "adjunto_original",
    "archivo_local", "sha256", "bytes", "estado", "drive_id", "notas",
]
EXT_OK = {".pdf", ".jpg", ".jpeg", ".png", ".zip"}
MIN_BYTES = 8_000  # adjuntos más pequeños suelen ser logos/firmas


def cargar_env():
    envfile = ROOT / ".env"
    if envfile.exists():
        for line in envfile.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def slug(s: str, maxlen: int = 40) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:maxlen] or "sin-nombre"


def cargar_registro() -> list[dict]:
    if not REGISTRO.exists():
        return []
    with open(REGISTRO, newline="") as f:
        return list(csv.DictReader(f))


def guardar_registro(filas: list[dict]) -> None:
    with open(REGISTRO, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)


def decodificar(texto) -> str:
    if texto is None:
        return ""
    partes = email.header.decode_header(texto)
    out = []
    for p, enc in partes:
        out.append(p.decode(enc or "utf-8", "replace") if isinstance(p, bytes) else p)
    return "".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Descarga adjuntos candidatos a factura del buzón de Dingui.")
    ap.add_argument("--dias", type=int, default=30, help="Ventana hacia atrás (por defecto 30).")
    ap.add_argument("--desde", help="Fecha inicio AAAA-MM-DD (ignora --dias).")
    ap.add_argument("--buscar", help="Filtro adicional de texto (remitente o asunto, insensible a mayúsculas).")
    ap.add_argument("--listar", action="store_true", help="Solo listar, no descargar.")
    ap.add_argument("--limite", type=int, default=0, help="Máx. correos a procesar (prueba).")
    args = ap.parse_args()

    cargar_env()
    user = os.environ.get("GMAIL_USER", "")
    pwd = os.environ.get("GMAIL_APP_PASSWORD", "")
    host = os.environ.get("GMAIL_IMAP_HOST", "imap.gmail.com")
    if not user or not pwd:
        print("⚠ Falta GMAIL_USER / GMAIL_APP_PASSWORD en .env")
        print("  La contraseña de aplicación se genera en: Cuenta de Google → Seguridad")
        print("  → Verificación en 2 pasos → Contraseñas de aplicación.")
        return 1

    desde = (
        datetime.strptime(args.desde, "%Y-%m-%d")
        if args.desde
        else datetime.now() - timedelta(days=args.dias)
    )
    imap_date = desde.strftime("%d-%b-%Y")

    registro = cargar_registro()
    vistos_msg = {r["message_id"] for r in registro}
    vistos_sha = {r["sha256"] for r in registro if r.get("sha256")}

    print(f"Conectando a {host} como {user} …")
    M = imaplib.IMAP4_SSL(host)
    try:
        M.login(user, pwd.replace(" ", ""))
    except imaplib.IMAP4.error as e:
        print(f"⚠ Login IMAP falló: {e}")
        print("  Revisa que la cuenta tenga 2FA + contraseña de aplicación e IMAP habilitado.")
        return 1

    # "[Gmail]/All Mail" cubre archivados; si no existe (idioma), caemos a INBOX.
    buzon = None
    for candidato in ('"[Gmail]/All Mail"', '"[Gmail]/Todos"', "INBOX"):
        ok, _ = M.select(candidato, readonly=True)
        if ok == "OK":
            buzon = candidato
            break
    print(f"Buzón: {buzon} | desde {desde.date()}")

    ok, data = M.search(None, f'(SINCE "{imap_date}")')
    ids = data[0].split() if ok == "OK" else []
    if args.limite:
        ids = ids[-args.limite:]
    print(f"{len(ids)} correos en ventana; analizando adjuntos…")

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    nuevos, saltados = [], 0
    for n, mid in enumerate(reversed(ids), 1):
        ok, data = M.fetch(mid, "(RFC822)")
        if ok != "OK" or not data or data[0] is None:
            continue
        msg = email.message_from_bytes(data[0][1])
        message_id = (msg.get("Message-ID") or f"sin-id-{mid.decode()}").strip()
        remitente = decodificar(msg.get("From", ""))
        asunto = decodificar(msg.get("Subject", ""))
        fecha_hdr = msg.get("Date")
        try:
            fecha = email.utils.parsedate_to_datetime(fecha_hdr).strftime("%Y-%m-%d")
        except Exception:
            fecha = ""

        if args.buscar and args.buscar.lower() not in (remitente + " " + asunto).lower():
            continue

        for parte in msg.walk():
            fn = parte.get_filename()
            if not fn:
                continue
            fn = decodificar(fn)
            if Path(fn).suffix.lower() not in EXT_OK:
                continue
            contenido = parte.get_payload(decode=True)
            if not contenido or len(contenido) < MIN_BYTES:
                continue

            # Los ZIP (p.ej. facturas Coca-Cola de invoices1Iberian@ccep.com) se
            # expanden y cada miembro PDF/imagen sigue el flujo normal de dedup.
            if Path(fn).suffix.lower() == ".zip":
                try:
                    zf = zipfile.ZipFile(io.BytesIO(contenido))
                except zipfile.BadZipFile:
                    continue
                miembros = []
                for zi in zf.infolist():
                    if zi.is_dir() or Path(zi.filename).suffix.lower() not in (EXT_OK - {".zip"}):
                        continue
                    datos_m = zf.read(zi)
                    if len(datos_m) < 1_000:
                        continue
                    miembros.append((Path(zi.filename).name, datos_m))
                for nombre_m, datos_m in miembros:
                    sha = hashlib.sha256(datos_m).hexdigest()
                    if sha in vistos_sha:
                        saltados += 1
                        continue
                    dominio = remitente.split("@")[-1].strip(">").split(".")[0] if "@" in remitente else "desc"
                    local = f"{fecha or 'sinfecha'}_{slug(dominio, 20)}_{slug(nombre_m, 60)}"
                    print(f"  [{n:>3}] {fecha} {slug(dominio,18):18} {nombre_m[:38]} (zip: {fn[:20]}) {len(datos_m)//1024:>5} KB"
                          + ("  (LISTAR)" if args.listar else ""))
                    if not args.listar:
                        (INBOX_DIR / local).write_bytes(datos_m)
                    nuevos.append({
                        "message_id": message_id, "fecha_email": fecha, "remitente": remitente,
                        "asunto": asunto, "adjunto_original": f"{fn}!{nombre_m}", "archivo_local": local,
                        "sha256": sha, "bytes": len(datos_m),
                        "estado": "listado" if args.listar else "descargado",
                        "drive_id": "", "notas": f"extraído de {fn}",
                    })
                    vistos_sha.add(sha)
                continue

            sha = hashlib.sha256(contenido).hexdigest()
            if message_id in vistos_msg and sha in vistos_sha:
                saltados += 1
                continue
            if sha in vistos_sha:
                saltados += 1
                continue

            dominio = remitente.split("@")[-1].strip(">").split(".")[0] if "@" in remitente else "desc"
            local = f"{fecha or 'sinfecha'}_{slug(dominio, 20)}_{slug(fn, 60)}"
            print(f"  [{n:>3}] {fecha} {slug(dominio,18):18} {fn[:45]:47} {len(contenido)//1024:>5} KB"
                  + ("  (LISTAR)" if args.listar else ""))
            if not args.listar:
                (INBOX_DIR / local).write_bytes(contenido)
            nuevos.append({
                "message_id": message_id, "fecha_email": fecha, "remitente": remitente,
                "asunto": asunto, "adjunto_original": fn, "archivo_local": local,
                "sha256": sha, "bytes": len(contenido),
                "estado": "listado" if args.listar else "descargado",
                "drive_id": "", "notas": "",
            })
            vistos_sha.add(sha)
        vistos_msg.add(message_id)

    M.logout()

    if not args.listar and nuevos:
        guardar_registro(registro + nuevos)
    print(f"\n{len(nuevos)} adjuntos nuevos"
          + ("" if args.listar else f" → {INBOX_DIR.relative_to(ROOT)}")
          + f" | {saltados} ya conocidos (dedup)")
    if not args.listar and nuevos:
        print(f"Registro actualizado: {REGISTRO.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
