#!/usr/bin/env python
"""Genera un PDF gemelo de cada foto de ticket en las carpetas de facturas de Drive.

Motivo: el equipo sube fotos desde el móvil, muchas SIN extensión ("Ferretería",
"Bazar chino") y alguna en HEIC — en Windows la contable no puede abrirlas.
Un PDF con el mismo nombre base se abre en cualquier sitio.

Uso:
    uv run python scripts/facturas_img2pdf.py           # convierte lo que falte
    uv run python scripts/facturas_img2pdf.py --dry-run # solo listar

- Recorre todas las subcarpetas de mes del montaje de Google Drive desktop.
- Detecta imágenes por CONTENIDO (magic bytes), no por extensión.
- Respeta la orientación EXIF (fotos de móvil giradas).
- Idempotente: si ya existe "<nombre>.pdf" al lado, no hace nada.
- HEIC: requiere pillow-heif; si no está instalado, avisa y lo salta.

Tras ejecutar: registrar los PDFs nuevos en registro_facturas.csv como
'duplicada' (copia del original) para que procesar-facturas no los trate
como facturas nuevas.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageOps

BASE = Path(
    "/Users/luismdecarvajal/Library/CloudStorage/GoogleDrive-lmcarvajal96@gmail.com"
    "/My Drive/DINGUI (pto)/Facturas/Facturas"
)

MAGIA = {
    b"\xff\xd8\xff": "jpeg",
    b"\x89PNG": "png",
}


def tipo_imagen(path: Path) -> str | None:
    try:
        head = path.open("rb").read(32)
    except OSError:
        return None
    for magic, t in MAGIA.items():
        if head.startswith(magic):
            return t
    if head[4:12] in (b"ftypheic", b"ftypheix", b"ftypmif1", b"ftypmsf1"):
        return "heic"
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not BASE.exists():
        sys.exit(f"No existe el montaje de Drive: {BASE}")

    try:
        import pillow_heif  # noqa: F401

        pillow_heif.register_heif_opener()
        heic_ok = True
    except ImportError:
        heic_ok = False

    hechos, saltados = 0, 0
    for f in sorted(BASE.rglob("*")):
        if not f.is_file() or f.suffix.lower() == ".pdf":
            continue
        t = tipo_imagen(f)
        if t is None:
            continue
        # Solo tratar como extensión los sufijos de imagen reales; "Chino 02.08.2026"
        # debe dar "Chino 02.08.2026.pdf", no "Chino 02.08.pdf".
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic"}:
            destino = f.with_name(f.stem + ".pdf")
        else:
            destino = f.with_name(f.name + ".pdf")
        if destino.exists():
            continue
        rel = f.relative_to(BASE)
        if t == "heic" and not heic_ok:
            print(f"  SALTADO (HEIC, falta pillow-heif): {rel}")
            saltados += 1
            continue
        print(f"  {rel}  ->  {destino.name}" + ("  (DRY)" if args.dry_run else ""))
        if not args.dry_run:
            img = Image.open(f)
            img = ImageOps.exif_transpose(img)
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img.save(destino, "PDF", resolution=150.0)
        hechos += 1

    print(f"\n{hechos} PDFs {'a generar' if args.dry_run else 'generados'}, {saltados} saltados")


if __name__ == "__main__":
    main()
