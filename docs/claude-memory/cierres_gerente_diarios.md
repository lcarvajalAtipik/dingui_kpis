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

**Estado 14/07/2026:** 10 noches transcritas (26/6, 3-4/7, 6-11/7, 13/7). Confirmado por el usuario (14/07): la 2ª hoja fechada "jueves 9 julio" (caja 10.861 €, 517 clientes) era en realidad VIERNES 10/7 (corregida en CSV — las hojas pueden venir mal fechadas, validar siempre fecha vs día de semana y perfil de la noche); las noches 27/6→2/7, 5/7 y 12/7 el local estuvo CERRADO (no faltan hojas). Pendiente: imágenes originales sin soltar en `imagenes/`. Total 10 noches: caja 50.083 €, personal 9.986 € (19,9%).

Relacionado: [[business-overview]], [[project-tipsi]], [[fourvenues-puerta-ticketing]], [[reference-proyecciones-sheet]].
