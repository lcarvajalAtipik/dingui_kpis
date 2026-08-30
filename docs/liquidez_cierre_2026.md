# Liquidez cierre de temporada 2026 — desglose y puentes — FUENTE DE VERDAD

**Cerrado en sesión 28-29/08/2026 con el usuario.** Último dato bancario: 27/08 (Santander) / 26/08 (Caixa).
Comparar contra este fichero, no recalcular de cero. Actualizar y commitear cuando cambie algo.

## Convenciones

- Liquidez total = bancos + plazo fijo Santander + saldo Fourvenues (retirable a demanda).
- Última noche de la temporada: **sábado 29/08/2026** (decidido por el usuario).
- Todo verificado contra los 676 movimientos bancarios de `db/kpis.sqlite` (cuadre al céntimo).
- El efectivo físico de la caja del local queda FUERA del perímetro (no medido).

## 1. Desglose desde el origen hasta el 27/08 (real, cuadra al céntimo)

### Entradas: 786.575,22

| | € |
|---|--:|
| Aportaciones de socios | 313.712,68 |
| Cobros TPV (liquidaciones Santander, desde soft-opening jun) | 413.506,73 |
| Devolución IVA obra (REDEME, jul) | 40.059,78 |
| Retirada Fourvenues 21/08 (recategorizada 29/08) | 13.946,03 |
| Abonos por identificar (ver hipótesis) | 5.350,00 |
| Préstamo socios (12.000 in / 12.000 devuelto) | 0 |

### Salidas: 608.717,79

| | € |
|---|--:|
| Inversión proyecto pagada por banco (ver docs/coste_proyecto_apertura.md) | 426.070,70 |
| Operativa jul-ago: COGS 128.169 + nóminas 25.800 + alquiler 4.594 + DJs/fijos/extra/otros 6.312 | 164.874,58 |
| IVA julio (pagado 20/08) | 9.494,64 |
| Financiero (gasto real 2.277,87 + plazo fijo 6.000) | 8.277,87 |

### Posición 27/08

| | € |
|---|--:|
| Santander (TPV) | 157.732,50 |
| CaixaBank | 20.124,93 |
| **Bancos** | **177.857,43** |
| Plazo fijo Santander | 6.000,00 |
| Fourvenues (saldo real visto 28/08) | 83.700,00 |
| **LIQUIDEZ TOTAL 27/08** | **≈267.557** |

⚠ Corrección 29/08: antes se decía ~281K porque el saldo FV se estimaba en ~97K sumando cierres;
83.700 (real) + 13.946,03 (retirada del 21/08 ya en Caixa) = 97.646 ≈ la estimación → estaban
contados doble ~14K. El abono del 21/08 se recategorizó de "Aportaciones" a retirada FV.

## 2. Puente 27/08 → fin de septiembre

```
LIQUIDEZ 27/08                                  ≈267.600

+ Cola TPV últimas 4 noches                      +27.000
    mié 26: 6.084 real · jue 27: 3.700 real
    vie 28 y sáb 29: ~10.000 c/u (previsión usuario)
    → ~30K ventas, neto de efectivo y comisiones

+ Préstamo Mahou, 1er pago                       +30.000
    (40K total; 10K restantes ppios 2027; se amortiza
     con pedidos de cerveza, sin salidas de devolución;
     aval 6.000 bloqueado)

− Limpieza final (todo comprometido)            −177.100
    Confirming Santander (Lorente C04 + BS)  −44.996
    Bebida agosto pendiente de cargar        −22.000
    Aycoa (resto sonido)                     −19.114
    IVA agosto (ESTIMACIÓN, pdte gestoría)   −17.500
    Viento (resto tematización)              −15.710
    Nómina agosto pendiente (tras adelantos) ~−15.000
    Licencia DR                              −10.000
    SS julio + agosto (TC1 ×2)               −16.754
    Stima (resto arquitecto, efectivo)        −6.000
    Vacaciones fijos discontinuos (si aplica) ~−5.000
    Alquiler ago+sep                          −4.594
    Gestoría/seguros/alarma sept                −400

− Pago RRPP                                      −12.000
                                                ────────
FIN DE SEPTIEMBRE                               ≈135.500
    (proyecto y proveedores a CERO)
```

## 3. Puente oct → dic (local cerrado)

```
Alquiler Realmivo (2.297,02 × 3)                 −6.891
Gestoría nueva (120+IVA = 145,20 × 3)              −436
Seguros Mapfre + Prosegur + O2 (~250 × 3)          −750
Modelo 111 (IRPF 3T, octubre)                    −1.200
Devoluciones IVA menores (REDEME)                +1.800
    Barter (605/mes): TERMINA en agosto — nada
                                                ────────
Neto oct-dic                                     −7.500

FIN DE AÑO 2026                                 ≈128.000
    de los cuales 6.000 bloqueados en aval Mahou
    → DISPONIBLE ≈122.000
    (+10.000 de Mahou llegan ene-2027)
```

## 4. Resumen para socios

| | € |
|---|--:|
| Aportaciones de socios (real banco) | ~314K (comprometido en cap table: 322K) |
| Coste total del proyecto | 532K |
| Resultado operativo del año (jul-dic) | ~+300K |
| Ventas agosto (cierre ~360K con IVA) | jul 224K + ago ~360K |
| Caja a 31/12, todo pagado, sin deuda salvo Mahou | ~128K (~122K disponibles) |
| − IS 2026 (escenario prudente, vence jul-2027) | −35K |
| **Libre para dividendo + colchón 2027** | **~87K** (+10K Mahou ene-27) |

IS: base ≈ 247K (300 op − 28 pre-apertura deducible − 23 amortización − 2 financiero) × 15% ≈ 37K.
Palancas gestoría (pueden dejarlo entre 0 y 37K): amortización según duración del contrato de
alquiler, amortización acelerada pyme (art. 103 LIS), libertad de amortización por creación de
empleo (art. 102 LIS, ~30 empleos creados). Reparto formal de dividendo: con cierre contable,
junta y reserva legal (10%), vía gestoría en 2027.

## 5. Marco IVA (REDEME mensual — añadido 30/08)

Estamos en REDEME (devolución MENSUAL, no trimestral): la devolución de 40.060 de la obra llegó
en julio por esto. Confirmar con gestoría nueva que seguimos inscritos (salir = devoluciones a 2027).

| Liquidación | Resultado | Cash |
|---|--:|---|
| Agosto: repercutido ~32,7K − soportado ~15K | −17,5K | paga 20/09 |
| Septiembre: solo soportado (Viento 2,7 + RRPP 2,1 + fijos 0,5) | +5,3K | cobra ~nov |
| Oct/nov/dic: fijos | +0,4K/mes | oct cobra dic; nov-dic cobran ene-feb 2027 |

Neto caja 2026: −11,8K → **fin de año sube a ≈132K (~126K disponibles)**.

## 6. Puente fin de año → reapertura junio 2027 (añadido 30/08)

```
FIN 2026                                     ≈132.000
Ene-may: alquiler −11.485, gestoría/seguros −2.000,
  mod 111 −1.200, Mahou 2º pago +10.000, IVA +1.000
MAYO 2027                                    ≈128.300
Pre-apertura: stock −18.000, puesta a punto −5.000,
  marketing −2.000
PUNTO MÁS BAJO (primeros de junio)           ≈103.000
IS 2026 (~35K prudente) vence JULIO 2027 — con caja del verano.
```

**Dividendo: repartible cómodo ≈50K ahora** (deja punto bajo ~53K en jun-27); repartir 87K
dejaría ~16K, tan justo como el arranque 2026 (4,6K). Resto tras el verano 2027.
Si gestoría deja IS 2026 ≈0 (libertad amortización): margen sube a ~65-70K.

## Hipótesis abiertas (29/08)

1. **+10.000 del 08/06** categorizado "Obra" (transfer entrante, mismo día que préstamo 3K y pago cert 1):
   si es aportación → aportaciones 323,7K ≈ cap table 322K. Si es préstamo → deuda viva 10K. PREGUNTAR.
2. Efectivos "Ybarra Navarrete Francisco" (+2.850 el 14/07, +500 el 26/08): ¿caja del local o aportación?
3. +2.000 (27/06), +2.100 y +1.750 (20/08): por identificar.
4. Aval Mahou 6.000: ¿es el plazo fijo Santander existente (20/07) o dinero nuevo?
5. IVA agosto ~17,5K y nómina agosto ~15K: cifras reales de gestoría/Stipendium (sept).
6. Vacaciones no disfrutadas fijos discontinuos: ¿se liquidan al suspender? (gestoría).
7. Cierres pendientes de transcribir: dom 23/08, jue 27/08 (3,7K), vie 28 y sáb 29.
8. Efectivo físico en caja del local: sin medir (ventas efectivo ago 26,5K; de ahí PROMOs y adelantos).
