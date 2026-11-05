# WG6_screened_phantom_web: screening the law's extra mass by hand doesn't land CMB lensing. A post-result shape check shows the law alone gets the spectrum's shape wrong under every rule tried

**Commits.**
- Criteria: 1a7c1cdde9, committed alone before any script or number.
- Engine, G-gal and driver: ea103b0e2d.
- Grader: c287c201f5, before any run finished.
- Result and shape diagnostic: this commit.

**Origin.** Owner 2026-11-04: "OK lets do that then", on a mass term that weakens the law beyond tens of Mpc, put in by hand.

**Correction recorded in the criteria.** The record's own v3/AeST μ_K term has the oscillating sign (+μ_K²ψ), not a screening one, and it comes with v3's retired khronon dust. So this lane tests a **new, by-hand Yukawa screening** of the phantom only.

**Standing.** κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework.

## The frozen result
- **Setup:** a0 tracks ρ_DE (DESI CPL), measured-style expansion B2D, baryons-only start, Planck PR4 8-400.
- **Statistic:** r is one best-fit amplitude.

| μ (screening length) | r (A_s 1e-9 / 4e-9) | frozen label | G-gal (phantom force at 1 Mpc) |
|---|---|---|---|
| 0.01 Mpc⁻¹ (100 Mpc) | 0.650 / 0.674 | WITHIN ×2 | PASS (0.9999) |
| 0.03 Mpc⁻¹ (33 Mpc) | 0.321 / 0.290 | FAILS LOW | PASS (0.9990) |
| 0.1 Mpc⁻¹ (10 Mpc) | 9.9e20 / 2.1e15 | FAILS HIGH | PASS (0.9905) |

- **Checks:** all K checks pass (K1, K2, K3, K4b, K10, K11). K5 at μ 0.03 holds (0.303 vs 0.288, same label). MUTATE bites.
- **Frozen lane reading:** "a screening length of 100 Mpc lands within ×2: FITTED, not derived, allowed by the galaxy-lensing gate".

## Why that reading is not a landing (POST-RESULT)
1. **The shape fails.**
   - At 100 Mpc, model/data per bin falls from 0.82 at L ≈ 28 to 0.14 at L ≈ 377.
   - The χ² after the best amplitude is 261 for 8 dof.
   - "Within ×2" was the averaged amplitude only. The frozen AMPLITUDE PASS clause, which also needs p ≥ 0.001, is not met.
2. **μ 0.1's FAILS HIGH is a projection artifact.**
   - Screening makes Δ²_Ψ rise toward the cut (high-k slope +1.8 to +3.1), so the frozen power-law extrapolation explodes.
   - Of the C_L in the bins, 0 % comes from in-box k.
   - The zero-beyond variant reads r 0.0025, which is FAILS LOW.

## Post-result shape diagnostic: every law-alone lane (`wg6_shape_diag.py`, `wg6_shape_diag.out`)
Model over data per PR4 bin (PLAIN W), at L_av 28, 64, 106, 150, 195, 240, 286, 331, 377:

| run | L 28 | L 106 | L 377 | shape χ² (8 dof) |
|---|---|---|---|---|
| law off (WG2 R0, B2) | 3.4e-4 | 3.7e-5 | 5.1e-6 | 1308 |
| QUMOND, a0 flat (WG2, 128³ / 192³) | 14.1 / 13.8 | 0.46 / 0.44 | 0.072 / 0.082 | 1574 / 1582 |
| T1τ0 (WG3) | 1.49 | 0.049 | 0.008 | 1572 |
| QUMOND, a0 tracks ρ_DE (WG4, 128³ / 192³) | 8.0 / 7.8 | 0.24 / 0.23 | 0.033 / 0.038 | 1589 / 1594 |
| screened 100 Mpc (WG6) | 0.82 | 0.68 | 0.14 | 261 |
| screened 33 Mpc (WG6, 128³ / 192³) | 0.13 / 0.12 | 0.28 / 0.28 | 0.29 / 0.22 | 126 / 137 |

**Reading.**
- **The law alone gets the CMB-lensing spectrum's shape wrong under every rule tried.** With QUMOND on, it is about 14× the measured value at L ≈ 28 and 0.08× at L ≈ 377. That is converged from 128³ to 192³ bin by bin.
- **The cause is the starting field and the law's growth.**
  - A baryons-only start is Silk-damped, so it has little small-scale potential.
  - The law's deep-regime growth boosts the largest scales most.
- **a0 tracking ρ_DE (WG4) lowers the whole spectrum by 0.46-0.57×,** about uniformly, without changing its shape.
- **Screening removes the large-scale excess but leaves the rest low:**
  - 1.5-7× low at L ≳ 100 at 100 Mpc;
  - 2.6-8× low everywhere at 33 Mpc.
- **No single factor fixes it.** The record's earlier "factor of about ½", and WG3's T1τ0 "within ×2", came from grading one amplitude dominated by the lowest bin. Both are withdrawn.

## What this means for the record
- **D9 for the law alone: FAILS, in shape.** It is too much at L ≲ 60 when the law is on, and far too little at L ≳ 100 under every rule.
- **The requirement on any future rule is now a shape.** It must keep large-scale lensing within reach of the data while adding about 5-15× more small-scale (L ≳ 100) lensing than a baryons-only start supplies. No rule on record does both.
- **WG2, WG3 and WG4** carry dated notes pointing here. PAPER67's CMB paragraph is rewritten to the shape statement.

## What this lane can't say
- The screening term is not from any action on record.
- G-gal is an isolated point lens.
- The shape diagnostic is post-result and ungated. Its numbers come from the same projection and data as the frozen labels.
- Everything WG2 can't say also holds here: mesh, A_s bracket, lensing assumed to see the dynamical potential, no primary-CMB test.
- Nothing here reinstates the cold sector.

## Files
- `FROZEN_CRITERIA.md`
- Scripts: `wg6_pm.py`, `wg6_ggal.py`, `wg6_run_all.py`, `wg6_grade.py`, `wg6_shape_diag.py`.
- Outputs: `wg6.out`, `wg6_results.json` (and `_MUTATE`), `wg6_ggal.out`, `wg6_ggal.json`, `wg6_shape_diag.out`, `runs/*.json`.
