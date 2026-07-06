---
name: ignorar-fx-convention
description: "Flag `ignorar_fx` — excluye movimientos del cashflow sin borrarlos; política de Dingui AÚN VACÍA (definir con el usuario)"
metadata:
  type: project
---

El pipeline hereda de fondeo_kpis el flag **`ignorar_fx`** en `bank_transactions`:

- `ignorar_fx=TRUE` → el movimiento se excluye de cashflow/liquidez (`WHERE ignorar_fx = FALSE` en todos los análisis) pero se conserva en la tabla.
- En Fondeo la política cubría: gastos pagados con la tarjeta personal del socio, traspasos entre cuentas propias, anulaciones/pares que se compensan.

**Estado en Dingui:** `IGNORAR_FX_PATTERNS` en `src/kpis/categorizer.py` está **vacío**. Cuando llegue el primer extracto, preguntar al usuario si existe una casuística equivalente (¿paga cosas de Dingui con tarjeta personal? ¿hay traspasos con otras cuentas suyas o con Fondeo?) y definir la política.

**How to apply:** no marcar nada como ignorar_fx por analogía con Fondeo sin confirmar. Un traspaso Dingui↔Fondeo, si existiera, hay que decidir explícitamente cómo tratarlo (¿préstamo entre sociedades? ¿aportación?) — preguntar.

Relacionado: [[pl-categories]], [[feedback-ask-more]].
