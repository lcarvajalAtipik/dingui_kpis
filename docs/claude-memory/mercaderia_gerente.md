---
name: mercaderia-gerente
description: "La casilla 'MERCADERIAS %' de los partes del gerente NO es un coste medido: es una fórmula ≈ 34€ × cajas de refresco de la noche (R²=0,99). Es un escandallo sobre mixers, con punto ciego en el alcohol/pour"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 0fcf9b70-bc26-470d-ac7f-733d5eca643e
---

**Ingeniería inversa (05/08/2026):** la casilla "MERCADERIAS %" que el gerente escribe en cada parte se reconstruye casi perfecto como **mercadería € = ~34 € × nº cajas de refresco** de esa noche (R²=0,99; base fija 34,0 €/caja, sube a 35-39 € las noches con invitaciones/premium). NO es un recuento físico de botellas vacías — es un **escandallo/fórmula** aplicado a las cajas de refresco que gasta.

**Implicaciones (clave para no malinterpretar los datos):**
1. Su lógica = 1 caja refresco ≈ 24 mixers ≈ 24 copas → **~1,47 €/copa implícito** (≈ mi cost card 1,58 €). Por eso mi COGS teórico y su mercadería coinciden (~24K julio): **son la MISMA lógica (copas × coste unitario), NO validación independiente.** La única prueba independiente sería un recuento físico de stock.
2. **Confirma el pour ~5-6cl** (12-14 copas/botella): su 1,47 €/copa descarta el pour generoso de 9 copas/botella (~2 €/copa).
3. **⚠ PUNTO CIEGO:** su fórmula solo mira cajas de refresco, IGNORA el alcohol servido. Si un camarero sobre-sirve (7cl en vez de 5), el coste real sube pero su "mercadería %" NO lo detecta — seguiría ~11%. Ahí se escapa el margen y su indicador no lo ve → motivo #1 para pedir un recuento de stock de alcohol.

**Números julio:** mercadería gerente = 24.491 € (11,0% de caja) = Σ (su % × caja noche). Mi COGS teórico mismo periodo 23.911 € (−2,4%). Ambos ~11% de caja / ~19-21% de la venta de barra.

**Hielo (RESUELTO 07/08):** Hielo Express Los Mellis factura semanal (facturas simplificadas): nº1353 13/07 base 473,64 + nº1430 20/07 base 932,81 (julio = 1.406,45 base) + nº1572 02/08 base 1.362,90 (total 1.531,00 = transferencia Caixa 04/08 exacta; ~74% hielo al 10%, resto Coca-Cola/agua al 21%; cubre el último finde de julio). Se paga por TRANSFERENCIA, no en efectivo.

Relacionado: [[coste-personal]], [[cierres-gerente-diarios]], [[sistema-facturas-drive]].
