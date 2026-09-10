---
name: conciliacion-iva-contable-junago
description: "Cruce 10/09/2026 del registro de IVA soportado del contable (jun-ago 2026) contra registro_facturas.csv: 15 facturas que le faltan (~18.868 €, ~3.205 € de IVA) + errores detectados en su registro"
metadata:
  type: project
---

**Fuente:** `REGISTRO RECIBIDAS DE JUN A AGOSTO 2026 (1).xlsx` (Stipendium/Asesoría, emitido 08/09/2026), 3 hojas: Facturas 175 filas (base 231.893,84 / cuota 46.611,36), Rectificativas 12 (−220,58), Adquisiciones intracom 2 (3,40). **Cuota total 46.394,18** (jun 11.713,02 · jul 9.454,74 · ago 25.226,42).

**Resultado del cruce (10/09/2026):** el contable YA tiene todo el lote que subí a Drive el 07/09 (agosto completo). **Le faltan 15 documentos = 18.868,44 € con ~3.205,18 € de IVA soportado**, casi todos de JUNIO (13 docs, 3.155,25 € de IVA; jul 49,93; ago 0). El 68% del IVA que falta es **una sola factura: AYCOA nº 41 (05/06, 12.515,03, IVA 2.172,03)**. Resto: Melgarejo N2971 (30/06, 4.040,35, IVA 692,32), Picking 2026001801 (01/06, 716,32, IVA 65,12), vidaXL ×2 (17 y 18/06), Stipendium 2026/1033 (18/06, 242), CCEP 2722713452 (19/06), Bazar Chino ×3, Aqualar 26000713/1, CoverManager 2026070232 (30/06), Google 5609868288 (30/06, intracom), CCEP Rectificativa 2724414935 (29/07, −110,35) y Dilaso FA2543 (31/07). PDFs reunidos en `~/Downloads/facturas_pendientes_contable_jun-ago/` (16 archivos, incluye el N4004).

**⚠ ERROR EN SU REGISTRO:** AYCOA factura 61 (10/08, 31.599,15, IVA 5.484,15) está asentada con **NIF y nombre de "SHANTOU XIAN KEJI YOUXIANGONGSI" (N0023815D)** en lugar de AYCOA Distribuciones S.L. (B-11827763); el concepto sí dice "AYCOA F61 INST SONIDO". Corregir por el 347/libro registro. Además 2 asientos **sin NIF**: REALMIVO 57/26 (01/06, 2.297,02, con retención 427,88 — arrendador) y Tipsi F2611902 (NIF correcto B90384298). Sánchez Yuste aparece como "MANTEC SY" (B06906341) — es correcto, solo nombre abreviado.

**Ellos tienen y yo NO** (pedir copia para Drive): REALMIVO 57/26 (2.297,02) y FRANCISCO GUZMÁN SADA nº 7 (09/06, 700,00). Hielo Express 1791 (17/08, 2.037,20) está en Drive como `CamScanner 17-08-2026 15.14.pdf` pero sin procesar en mi registro.

**Errores míos detectados de paso (pendientes de corregir en `registro_facturas.csv`):** Ipasur FA534 duplicada (2 filas 'procesada' para el mismo doc), Picking 2026001801 con desglose mal extraído (base 651,20 + IVA 65,12, no 674,76 + 41,56), Melgarejo N4004 registrada como −24,72 cuando el neto real es 0,00 (cambio de referencia Barceló↔Havana). Chamán 68-26: el PDF dice fecha 06/07 y el contable la asienta 01/08 — yo la archivé en la carpeta de julio.

**Contexto fiscal:** Nuevo VH está en REDEME (303 mensual); los MOD 303 de junio y julio ya están presentados (los envió Stipendium el 04/09). Las de junio se pueden deducir en una declaración posterior (derecho a deducir 4 años) en vez de rectificar — a confirmar con el asesor.

Relacionado: [[sistema-facturas-drive]], [[obra-proveedores-ledger]], [[iva-rates]], [[cogs-audit-ago26]].
