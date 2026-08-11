---
name: sistema-facturas-drive
description: "Sistema de registro de facturas de Dingui: Drive (carpeta por mes) → registro_facturas.csv + lineas_facturas.csv con drive_id para NO reprocesar. Taxonomía bebida: refresco/cerveza/alcohol/vino, marca, y cerveza barril vs botellín"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
  modified: 2026-08-11T11:17:02.755Z
---

**Encargo del usuario (29/07/2026):** sistema que reconozca las facturas de Drive (qué son, qué contienen) y lo deje anotado con su link/id para no reprocesar. **Primer objetivo: facturas de comida y bebida** — bebida diferenciada por refrescos/cerveza/alcohol, con marca; cerveza por **barril vs botellines**.

**Carpetas Drive:**
- Documentación Dingui: `1jF3ZauLnSpD1TsG-NWGVffZLKK7KCErW`
- Facturas (subcarpeta por mes): `1Y2gqblXGgD5QTlHrbf2EwGddiZtcBWpH`

**Acceso:** concedido 29/07 (compartidas con `l.carvajal@atipikproperties.com`, cuenta del conector). **Censo COMPLETO 29/07/2026: 118/118 facturas procesadas** (5 subcarpetas: 1er trimestre, abril, mayo, junio, julio 26), 389 líneas F&B. Bebida 18 fact/~31K (alcohol 19,2K > refrescos 3,1K [casa Pepsi/Schweppes vía Melgarejo; CCEP solo 160€ vidrio retornable] > vino 2,1K [Dom Pérignon, Moët] > cerveza 346€ [solo 2 barriles Cruzcampo 50L — Dingui vende copas, no cerveza]). Comida ~3,9K (La Encina jamones 2,5K, Makro, Picking). Proveedor bebida dominante: **Miguel Merino Distribuciones** (~20K). Detectado y marcado 1 duplicado (Melgarejo N3371 subida 2 veces). Las facturas de Coca-Cola CCEP vienen en formato albarán con envases retornables — a los agentes les cuesta, revisar sus líneas a mano.

**Dónde vive:** `data/facturas/` (git-tracked, excepción en .gitignore): `registro_facturas.csv` (una fila por archivo Drive, clave = drive_id — el diff contra esto evita reprocesar), `lineas_facturas.csv` (detalle línea a línea SOLO comida/bebida) y `README.md` (esquema completo). PDFs NO van al repo: cache local `data/facturas/cache/` (gitignored), Drive es la fuente.

**Email → facturas (montado 29/07, credenciales OK en `.env`):** `scripts/gmail_facturas.py` — extractor IMAP de info@dinguiclub.com. Baja adjuntos PDF/JPG/PNG/**ZIP** ≥8KB sin pre-filtrar (los ZIP se expanden y cada PDF interno sigue el dedup normal — añadido 11/08 tras descubrir que se saltaba los de Coca-Cola), dedup por sha256+message_id en `email_registro.csv` (git-tracked), archivos a `email_inbox/` (gitignored). Ciclo completo previsto: email → revisar bandeja → subir a Drive (carpeta del mes) → workflow procesar-facturas → conciliar banco. Para ENVIAR email desde info@dinguiclub.com: smtplib SMTP_SSL smtp.gmail.com:465 con las mismas credenciales + `ssl.create_default_context(cafile=certifi.where())` (sin certifi falla el SSL en este Mac).

**⚠ COCA-COLA (CCEP), aclarado 11/08/2026:** lo que reparte Guadalete ("Entrega realizada en DINGUI", administracion@guadalete.com.es) son ALBARANES ("NOTA ENTR.", nº tipo 45346…) — NO facturas, la contable los rechaza. Las FACTURAS reales llegan de **invoices1Iberian@ccep.com como ZIP** (1 factura por albarán, referencia "Núm.Albarán" dentro; rectificativas incluidas), SEPA domiciliación Caixa con vto +7 días, cliente 1196600 / cta CCEP 19241964; portal www.tuportalcocacolaep.es. Conciliar factura↔albarán por ese nº para no duplicar COGS (los albaranes 381,04 y 1.579,19 están en el registro como "procesada" con líneas — al registrar las facturas, cruzar). Descuadres abiertos 11/08: cargo banco 249,62 (17/07) sin factura recibida; factura 717,00 (2724124379, vto 23/07) sin cargo en banco; albarán 4534480605 (194,08, 01/07) sin factura entre las recibidas.

**⚠ SUBIR archivos a Drive: usar SIEMPRE el montaje de Google Drive desktop** — `~/Library/CloudStorage/GoogleDrive-lmcarvajal96@gmail.com/My Drive/DINGUI (pto)/Facturas/Facturas/<subcarpeta mes>/` (cp y el cliente sincroniza; borrar duplicados con rm ahí mismo). NO usar el MCP create_file para PDFs: exige base64 inline y con archivos >~40KB los agentes truncan la salida (subidas corruptas — pasó el 30/07, 2 archivos reemplazados). El MCP no tiene delete. Estado 04/08: registro 160 facturas, 100% con drive_id/url reales; carpeta "Facturas Agosto 2026" creada por el equipo (id 1vSc_jNObj-ZiSHgo-AprShqpF7kp4v98), que además sube fotos de tickets directamente a Drive. Proveedores nuevos detectados: Monbake (pan), DJs facturan (DJ Chaver/Fernando Chávarri, Daniel Félix ~212-265€/noche); CCEP/Coca-Cola volvió el 31/7 (pedido 1.579€, 60 cajas vidrio retornable — NO estaba discontinuada, era compra puntual); Melgarejo semanal incluye cerveza Ouro y El Águila además de Cruzcampo/Heineken. Los remitentes gmail/hotmail TAMBIÉN traen facturas (DJs, La Encina) — no filtrar por remitente al identificar.

**Procesamiento:** workflow `.claude/workflows/procesar-facturas.js` (committeado): Inventario Drive → diff vs registro → un agente por factura nueva (descarga+Read+extracción con schema) → verificación adversarial de sumas y clasificación en las F&B. Pasar `args.procesados` = drive_ids ya en el CSV.

**Taxonomía bebida:** tipo_bebida = refresco (incl. tónicas/zumos/energéticas) | cerveza | alcohol (destilados/licores) | vino (incl. cava/champán; Moët=vino) | agua | otros. Marca siempre normalizada (Coca-Cola, Cruzcampo, Ballantine's…). Cerveza: formato barril | botellin | lata. Hielo/desechables = otros_consumo.

**Contexto útil:** proveedores conocidos por el banco: Makro, Picking Gades, Cash Lepe, Coca-Cola (y una "cervecera" financió parte de la obra — probable contrato con marca de cerveza). Promo con Ballantine's (parte del 11/7). Los totales de facturas deben cuadrar con los cargos bancarios COGS.

Relacionado: [[pl-categories]], [[business-overview]], [[cierres-gerente-diarios]].
