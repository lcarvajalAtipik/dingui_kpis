# Cierres diarios del gerente

El gerente envía cada día una imagen (hoja de cierre) con el resumen de la noche anterior.
El usuario la pega en el chat de Claude y (idealmente) suelta el archivo original en `imagenes/`.

## Contenido

- **`cierres_gerente.csv`** — transcripción estructurada, una fila por noche. La mantiene
  Claude al recibir cada imagen. Columna `flag` para incidencias (p. ej. fecha dudosa).
- **`imagenes/`** — las imágenes originales, nombradas `YYYY-MM-DD.png` (fecha de la noche
  que reporta la hoja, no la fecha de envío). Si un día tiene dos versiones (corrección
  posterior), la nueva sustituye a la vieja; si conviven, sufijo `-v2`.

Este directorio SÍ viaja por git (excepción en `.gitignore`): son datos transcritos a mano
que no se pueden regenerar de ninguna fuente. ~80 imágenes/verano ≈ 10-25 MB, asumible.

## Cómo se lee la hoja (convenciones)

- Bloque superior (CIERRE): filas Barra 1 / Reservados / Taquilla × columnas
  Efectivo / Visas / Total / Z / Descuadre. **Descuadre = contado − Z** (positivo = sobra).
- **TOTAL CAJA = Barras + Reservados + Taquilla(=Puerta) + Fourvenues (+ Otras)**.
- **Puerta = entradas × precio** (10 € mar-jue, 15 € vie-sáb y lunes — hasta ahora).
- **% gasto personal = gasto personal / TOTAL CAJA** de esa noche.
- Mercaderías % = consumo de producto sobre venta (sube con botellas de invitación).
- Invitaciones: socios vs personal (copas/chupitos/cervezas/DJ copas).
- El comentario de la noche siempre se transcribe ÍNTEGRO al CSV (columna `comentario`).

## Flujo al recibir una imagen nueva

1. Mirar si ya hay fila en el CSV para esa fecha → si existe, comparar campo a campo
   (puede ser una corrección del gerente; actualizar y anotar en `flag`).
2. Transcribir todos los campos + comentario íntegro.
3. Validar cuadres: total cierre = barra1+reservados+taquilla; caja = cierre+FV;
   descuadre = contado−Z; puerta = entradas×precio; % personal declarado ≈ calculado.
4. Avisar al usuario de descuadres grandes o anomalías del comentario.
5. Guardar imagen en `imagenes/YYYY-MM-DD.png` (la suelta el usuario; Claude la renombra).
