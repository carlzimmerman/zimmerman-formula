# CFG714 FROZEN CRITERIA: does the SLACS inner extra (CFG713) predict the KiDS outer early-type excess (CFG721)? (block CFG710–719)

Date: 2026-10-13. Committed ALONE before any CFG714 code or number. κ = ½ FITTED; footings separate; cold energy mass required; no
particle species; not "theory closed"; nothing will say the data favour the framework.

## Hypothesis H-ONE: the early-type extra is ONE extended isothermal cold component, bound to each galaxy, added to the law.
- Inner (strong lensing): CFG713 per lens gives f_x and hence the isothermal normalisation A (M_x(<r) = A r), circular velocity
  V_x² = G A, and the H-X stellar mass M* (Chabrier-like).
- Outer (weak lensing, g_bar ≤ 1e-12): the law gives g = √(g_bar a0) = V_f²/r with V_f⁴ = G M_b a0 (M_b = M*, gas neglected for
  passive lenses); the extra adds V_x²/r. At fixed g_bar the observed-to-law ratio is **1 + V_x²/V_f²**.
- **Prediction:** Δ_pred = median over CFG713 lenses with 0 ≤ f_x < 0.95 of log10(1 + V_x²/V_f²), per footing; bootstrap σ; variant
  including the f_x ≥ 0.95 lenses at f_x = 0.95 and f_x < 0 at 0.
- **Data:** CFG721 Part A: red − blue Δlog ESD = +0.220 ± 0.030 (colour split), +0.181 ± 0.029 (Sérsic split), B21 isolated lenses
  at g_bar ≤ 1e-12. Blue lenses sit near the law (CFG663), so red − blue is read as red − law (stated assumption).
## Verdict (per footing; vs the colour split primary, Sérsic secondary)
CONSISTENT if |Δ_pred − Δ_obs| ≤ 2 σ_comb (σ_comb = quadrature of bootstrap and data errors); INCONSISTENT if > 3 σ_comb; TENSION
between. Limits stated: SLACS (log M* ≈ 11.2–11.8) vs KiDS lens mass range differ; isothermal shape assumed to r ~ 100 kpc.
MUTATE (`CFG714_MUTATE=1`): f_x → 0 must give Δ_pred = 0 exactly (exit 1 iff it bites).
