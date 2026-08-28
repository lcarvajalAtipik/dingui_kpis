---
name: liquidez-2026-snapshot
description: "Análisis de liquidez 27/08/2026: mensual ene→ago real + proyección sep-dic. Liquidez 27/08 ≈281K (bancos 177,9 + plazo 6 + FV ~97). Sept = mes de limpieza (~163K salidas). Fin de año ≈174K (165-185K). IS 2027 ~30-45K aparte."
metadata: 
  node_type: memory
  type: project
  originSessionId: f72e837b-7c96-428b-adcb-caea463d9752
  modified: 2026-08-28T16:30:46.887Z
---

**Análisis de liquidez presentado 27/08/2026** (conversación; convención chat-only). Definición acordada: **liquidez total = bancos + plazo fijo Santander (6.000 desde 20/07) + saldo Fourvenues** ([[fourvenues-puerta-ticketing]]: DECIDIDO 27/08 que FV cuenta SIEMPRE como disponible, retirable a demanda).

**Saldos fin de mes 2026 (reales, validados contra columna Saldo de los extractos; bancos en K€):**
ene 7,3 · feb 110,7 · mar 36,2 · abr 49,0 · may 13,2 · jun 4,6 (+FV 8,5 = 13,1) · jul 86,0 con plazo (+FV 51,0 = 137,0) · **27/08: Caixa 20,1 (26/08) + Santander 157,7 + plazo 6 = 183,9 + FV ~97 = ≈281K (máximo del año)**.
⚠ El saldo de un día concreto por "última fila del export" puede engañar (orden intradía arbitrario); reconstruir por suma de movimientos anclada al saldo final.

**Narrativa del año:** ene-may: obra consume ~289K de aportaciones (feb 136,4 / abr 64,7 / may 87,7); may el peor mes (Certs 02+03 −107,5). Jun: apertura 19/06 con 4,6K en banco, puente con préstamo socios 12K (devuelto íntegro en jul-ago) y Cert 04 vía confirming. Jul-ago: ~470K de entradas (TPV jul 145,8 + REDEME 40,1; TPV ago 265,4 + aportaciones ago 17,8), pagan casi toda la deuda de obra y bebida.

**SEPTIEMBRE 2026 = mes de la limpieza final (~163K de salidas proyectadas):** confirming 44.996 + intereses ([[obra-proveedores-ledger]]) · Aycoa 19.114 · IVA agosto ~20K est. (cargo 20/09) · TC1 SS julio 8.354 + agosto ~8.400 · Viento tematización 15.710 · recibos bebida pendientes ~25K · licencia DR 10.000 · Stima efectivo 6.000 · alquiler ago+sep 4.594. Entradas: cola TPV agosto ~65K. Oct-dic (CERRADO, [[pnl-2026-snapshot]]): ~−3,3K/mes fijos, +~0,6K/mes devoluciones REDEME menores; mod. 111 3T −1,2 en oct.

**Proyección fin de año: ≈174K de liquidez total (rango 165–185K).** Fuera de 2026: **IS del ejercicio ~30–45K vence julio 2027** (tipo 15% nueva creación; mod. 202 oct/dic a cero por método cuota año anterior — HIPÓTESIS a validar con gestoría) → colchón real para temporada 2027 ≈130–145K.

**Marco IVA (REDEME mensual):** +40.060 devuelto jul (IVA inversión) · −9.421 pagado 20/08 (IVA julio) · ~−20K IVA agosto 20/09 (ESTIMACIÓN MÍA: repercutido ~38K − soportado ~18K; validar con gestoría, es la cifra menos firme) · sep-dic ~neutro/devoluciones pequeñas.

**Pendiente que afinaría el cuadro:** cifra real IVA agosto (gestoría) · confirmar 202 a cero · mecánica de retirada FV y a qué cuenta llega (0 abonos en banco a 27/08) · finiquitos fin de temporada (salen de efectivo de caja, asumido neutro).

Relacionado: [[obra-proveedores-ledger]], [[pnl-2026-snapshot]], [[fourvenues-puerta-ticketing]], [[project-bank-ingest-state]], [[coste-personal]].
