---
name: cierres-gerente-diarios
description: "Flujo diario NUEVO (desde 14/07/2026): el gerente envía cada día una imagen con el cierre de la noche anterior; se transcribe ÍNTEGRA a data/cierres_gerente/cierres_gerente.csv (git-tracked) y la imagen se archiva por fecha"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Desde el 14/07/2026 el gerente de Dingui envía a diario una imagen con el cierre de la noche anterior** (hoja Excel fotografiada/pantallazo). El usuario la pega en el chat; puede traer correcciones de días ya enviados.

**Dónde vive:** `data/cierres_gerente/` — EXCEPCIÓN en `.gitignore` (`data/*` + `!data/cierres_gerente/`), viaja por git porque no se regenera de ninguna fuente. Contiene `cierres_gerente.csv` (una fila por noche, comentario íntegro), `imagenes/YYYY-MM-DD.png` (originales, ~80/verano) y `README.md` con las convenciones completas de lectura.

**Cómo se lee la hoja:** TOTAL CAJA = Barras + Reservados + Taquilla(=Puerta) + Fourvenues. Descuadre = contado − Z (positivo sobra). Puerta = entradas × precio (10 € mar-jue, 15 € vie-sáb-lun hasta ahora). % gasto personal = personal/total caja. Mercaderías % sube con botellas de invitación. Bloques: cierre por caja (efectivo/visas/Z), invitaciones socios vs personal, horas apertura/cierre, comentario de la noche (SIEMPRE transcribir entero).

**Why:** es la única fuente con efectivo real, invitaciones, pax, gasto de personal por noche y contexto cualitativo — nada de eso está en Tipsi ni en bancos. Complementa: Tipsi = detalle por ticket; banco = solo lo que se liquida por TPV.

**How to apply:** al recibir una imagen: (1) buscar si ya hay fila para esa fecha en el CSV → dedup/actualización; (2) transcribir todos los campos + comentario; (3) validar cuadres (script inline: cierre=b1+resv+taq; caja=cierre+FV; descuadre=contado−Z; puerta≈entradas×precio; % personal); (4) avisar de anomalías; (5) archivar imagen como `imagenes/YYYY-MM-DD.png`; (6) commit (viaja por git).

**Estado 29/07/2026:** 23 noches transcritas (26/6 → 28/7; imágenes archivadas en `imagenes/`). Cerrado: 27/6→2/7, 5/7, 12/7, 14/7 sin hoja (total conocido 7.478 € por lista del gerente), 26/7 cerrado (0 tickets Tipsi). El gerente a veces fecha mal las hojas (10/7, 21/7, 24/7 corregidas) — cuando el usuario pone el día en el nombre del archivo ("viernes 24.jpeg"), MANDA EL TÍTULO. Las hojas llegan como WhatsApp jpeg a ~/Downloads. Desde el 20/7 hay categoría de invitaciones "RPPS COP" (relaciones públicas, 26-42/noche) → columna `inv_rpps_copas`. Los reservados con nombre a veces van DENTRO de barras (no en la fila Reservados del cierre) — el box "Reservados" con nombres es informativo. 14/7 recibida (29/07). Del 19/6 (apertura, 600 €) NO SE HIZO caja — no existe hoja, el total viene de la lista del gerente; histórico de hojas COMPLETO. Escala: desde el 15/7 la media es ~10,4K €/noche (vs ~5K antes); puerta subió de 10-15 € a 20-30 €.

Relacionado: [[business-overview]], [[project-tipsi]], [[fourvenues-puerta-ticketing]], [[reference-proyecciones-sheet]].
