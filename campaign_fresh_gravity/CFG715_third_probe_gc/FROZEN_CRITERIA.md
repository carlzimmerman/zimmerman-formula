# CFG715 FROZEN CRITERIA: does the CFG714 extra component predict the SLUGGS globular-cluster excess? (third probe; block CFG710–719)

Date: 2026-10-13. Committed ALONE before reading the committed SLUGGS numbers' JSON. Seen: CFG55's README line "the law under-
predicts the outer GC dispersions of 19 massive early types by +0.080 dex (3.3σ)" (CFG38 base, SLUGGS's own stellar masses).
κ = ½ FITTED; footings separate; cold energy mass required; not "theory closed"; nothing will say the data favour the framework.

## Prediction (nothing re-fitted)
An isothermal extra with V_x² = q V_f² adds a constant to V_c² at large radii; for the same tracer and anisotropy the outer LOS
dispersion scales as √(1 + q) ⇒ **Δlog σ_pred = ½ log10(1 + q)**, q from CFG714 per footing: q = 10^Δ_pred − 1 (Δ_pred = CFG714
primary median; uncertainty propagated from its bootstrap σ). Variant: CFG714's all-43 Δ.
## Data
The committed CFG38/CFG55 outer-GC offset of the bare law (value and σ read from their results JSON by this lane's script; SLUGGS's
own stellar masses as primary, as CFG55 states; CFG55's dynamical-mass variant reported as context).
## Verdict (per footing)
CONSISTENT if |Δ_pred − Δ_obs| ≤ 2σ_comb; INCONSISTENT if > 3σ_comb; TENSION between. Limits: the GC radial range is ~10–50 kpc
(between CFG713's ~5 kpc and CFG714's ~100 kpc); anisotropy assumed unchanged by the extra; SLUGGS ≠ SLACS sample.
MUTATE (`CFG715_MUTATE=1`): q → 0 must give Δ_pred = 0 (exit 1 iff it bites).
