# CFG821 FROZEN CRITERIA: an upper bound on the stiffness length L* from the Milky Way classical dwarf spheroidals (committed before any script)

**Why.** CFG820 found L* ≥ 24 pc (outer globulars must be screened). The classical dSphs (r_h ~ 150–2400 pc, sub-a₀ internal
acceleration) show the extra gravity the law predicts. Too large an L* would screen them toward Newton, so they bound L*
from above. Together the two give a two-sided window.

**Data.** LVD `real_research/data/dsph/lvd_dwarf_mw.csv`: MW satellites with M_V ≤ −7.7 and a measured vlos_sigma. LMC, SMC
(rotating discs) and Sagittarius (disrupting) are excluded, leaving 11 dSphs. r_h is rhalf_sph_physical (pc). L_V comes
from M_V (M_V,☉ = 4.83). M = Υ_V L_V with Υ_V = 2.0 (the record's dSph convention, CFG784), width 0.15 dex.

**Prediction (as CFG820).** σ²_pred = σ²_N [1 + S(s)(B_law − 1)].
- Wolf estimator; S(s) is CFG691's profile; s = (4/3) r_h / ℓ_γ, with ℓ_γ = L*²/(2 r_M).
- **Primary B_law:** the ISOLATED law, y = G(M/2)/r_{1/2}²/a₀ (record rule FG001 class A for satellites: isolated law of
  their baryons, no EFE).
- **Bracket:** the law with the MW's algebraic EFE (g_ext = G 6e10 M☉ / R_GC², as in CFG332).

**Statistic.** χ²(L*) = Σ [ln σ_obs − ln σ_pred]² / [(e_σ/σ_obs)² + (ln 10 × 0.15/2)²], with L* on a log grid from 5.75 to
3000 pc.
- **Upper bound L*_95,up:** the largest L* with χ² − χ²_min ≤ 3.84.
- **Report** χ² at L* → 0 (unscreened) and at L* → ∞ (Newton). If the unscreened fit itself is poor (p < 0.01), the bound
  is CONDITIONAL.

**Classes.**
- **WINDOW CLOSED (two-sided)** if L*_95,up < 3000 pc and > CFG820's 24 pc.
- **INCONSISTENT** if L*_95,up < 24 pc: the globulars and dSphs disagree.
- **NO UPPER BOUND** otherwise.

**Controls.**
- K1: L* → ∞ gives Newton; K2: L* → 0 gives the law (identities).
- MUTATE (separate output): with S := 0 everywhere (all screened), only the Newton χ² remains and there is no upper bound.

Both footings, never pooled. κ = ½ fitted; not theory closed.
