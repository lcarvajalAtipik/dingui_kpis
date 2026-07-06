# Memory Index

- [User role](user_role.md) — Propietario de Dingui (y Fondeo) e ingeniero de software. Idioma: español.
- [Business overview](business_overview.md) — Dingui EN PRE-APERTURA (obra en curso) en El Puerto de Santa María (Cádiz). CaixaBank, Tipsi, alquiler Realmivo 2.297€/mes. Caja 30/04/2026: 53.878€.
- [Reference: fondeo_kpis repo](reference_fondeo_repo.md) — Repo hermano (~/Desktop/fondeo_kpis) = implementación de referencia; portar de ahí, sin copiar reglas de proveedores.
- [Reference: sheet Proyecciones](reference_proyecciones_sheet.md) — Sheet "Proyecciones PuertoSantamaria" en Drive: ground truth de movimientos (hoja "movimientos 30 abril 2026", columna Tipo) + FC inicial + cap table.
- [P&L categories](pl_categories.md) — Categorías reales pre-apertura (Aportaciones, Obra, Licencia/Trámites…). Categorizador validado: 96,6% acierto, 100% cobertura.
- [Bank format: CaixaBank](bank_format_caixa.md) — Layout exacto del export XLS de CaixaBank (portado de Fondeo; validar con primer export de Dingui).
- [ignorar_fx convention](ignorar_fx_convention.md) — Flag de exclusión de cashflow; política de Dingui aún vacía, definir con el usuario.
- [IVA rates](iva_rates.md) — Hostelería 10%, gastos 21%, rappels 21%; entradas discoteca probablemente 21% (CONFIRMAR con gestoría).
- [Project: Tipsi (PoS)](project_tipsi.md) — Análisis de ventas; mecanismo de acceso a datos por confirmar (API vs exports).
- [GCP auth strategy](gcp_auth_strategy.md) — ADC vía `gcloud auth application-default login`; proyecto/dataset BQ por crear.
- [Feedback: chat-only workflow](feedback_chat_only_workflow.md) — Todo el análisis se consume en la conversación. Nada de notebooks/dashboards.
- [Feedback: no pre-filter data](feedback_no_prefilter_data.md) — El usuario sube exports crudos; yo deduplico y delimito rangos.
- [Feedback: bank format stable](feedback_bank_format_stable.md) — Cada banco exporta siempre el mismo formato; parser dedicado por banco.
- [Feedback: ask more](feedback_ask_more.md) — Cuando dude, preguntar (no asumir). Crítico en Dingui: casi todo está sin documentar aún.
- [Feedback: sync memoria](feedback_sync_memoria.md) — Usuario multi-ordenador; repo en GitHub (lcarvajalAtipik/dingui_kpis). Sync memoria: push + commit + push; en máquina nueva, pull.
