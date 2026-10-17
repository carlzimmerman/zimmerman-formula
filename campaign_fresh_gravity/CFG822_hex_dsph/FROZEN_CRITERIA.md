# CFG822 FROZEN CRITERIA: canonical v2's expelled-gas rule (S4 / H-EX) applied as written to the MW classical dSphs (committed before any script)

**Why.** CFG821 showed the classical dSphs sit ~2× above even the unscreened law. THEORY_CANONICAL v2 (2026-10-16) includes
H-EX: the cold share of expelled baryons is free, and retained baryons tether only their own share. The dSphs are gas-free
and expelled most of their catchment baryons (census f_ret = 0.10 below log M_ta 12.5). This is a FORWARD application of the
written theory with the existing machinery; no rule is added.

## Setup per dSph (the 11 of CFG821)
- **Stars:** M_b = 2 L_V (as CFG821), Plummer profile with a = r_h. No gas.
- **Machinery:** CFG809's H-EX split, unchanged (`cfg809.py` defs; `run_system` with variant EX).
  - Census catchment fixed point bc = M_b / f_ret(M_ta).
  - Settled law of the stars, capped at the retained share 5.364 M_b.
  - Free share 5.364 (bc − M_b), placed by Method A.
  - Canonical and alt footings; kernel ν_s; z = 0.
- **Prediction:** σ_pred = √(G M_tot(<r_{1/2}) / (3 r_{1/2})) (Wolf), with r_{1/2} = (4/3) r_h and M_tot = stars + settled
  + free inside r_{1/2}.

## Statistic and classes
- χ² = Σ [ln σ_obs − ln σ_pred]² / [(e_σ/σ_obs)² + (ln 10 × 0.15/2)²], with 10 dof (11 dSphs, no fitted parameter).
- **H-EX EXPLAINS dSphs** if p ≥ 0.01 AND it improves on the unscreened law (CFG821 χ² 58.4 canonical).
- **IMPROVES** if χ² falls but p < 0.01.
- **NO HELP** otherwise.
- Report per dSph: free mass inside r_{1/2} / M_b, and σ_pred against σ_obs.

## Controls
- K1: with the free share forced to 0, σ_pred equals the law-settled value (stars + settled), within 2% of CFG821's
  isolated-law σ for a spot dSph. (The Wolf vs CFG821 estimator differ only by the M/2 convention, which is declared.)
- MUTATE (separate output): with the free mass placed uniformly to r_ta, the inner free mass must drop.

κ = ½ fitted; cold energy mass required; not theory closed.
