# CFG198 — MUSE-DARK per galaxy: a₀(z) at R_e, and whether III's rise survives swapping the fitted disc mass

- **Criteria:** `FROZEN_CRITERIA.md` (d5a73127b), committed before any number. **κ = ½ FITTED, NOT DERIVED.**
- **Data:** `data_assembly/musedark_catalogues/musedark_numeric.csv` (data chat, be78f2054 / f17dae96c). Its definitions are as read and are unverified against the papers' PDFs.
- **Run:** `python3 campaign_fresh_gravity/CFG198_musedark_pergalaxy_a0z/cfg198_musedark_a0z.py`, about 90 s; `MUTATE=1` runs the control.
- **Result:** 3/3 controls pass, and the MUTATE control passes.

## Bottom line

- **III's rise travels with the fitted-mass route.**
  - The DC14 run's fitted disc mass falls against the SED stellar mass by **0.72 dex per unit z** (95% CI 0.50–0.97).
  - With III's own fitted masses (route i), the per-galaxy a₀ at R_e rises by **+0.79 dex per unit z** (CI +0.51 to +1.07). That is steeper than III's published law (+0.30 over the same z).
  - With SED stars + main-sequence H₂ (route ii) the rise is gone: **−0.04 dex per unit z** (CI −0.47 to +0.36).
  - The paired change is **−0.94** (CI −1.26 to −0.63). Its sign and significance are the same in every gas, H₂, kernel and route row (R2 ROBUST).
- **Once the fitted-mass route is removed, the data do not discriminate between the laws.**
  - In the primary, flat, a₀ ∝ E(z) and III's law all lie inside route (ii)'s CI.
  - Flat is never excluded in any row. E(z) is excluded only with Σ_HI = 0; III's law only with Σ_HI = 0 or H₂ × 2 (R1 NOT robust: gas- and H₂-dependent).
  - So these data do not establish III's rise, and they do not establish a flat a₀ either.
- **Against interest (reported, not graded).** At z ≈ 0.5, the implied a₀ level is 0.25–0.65 dex above both footings in every route.
  - The level is 2.0–4.1 × 10⁻¹⁰ m s⁻², against 0.94 and 1.13 × 10⁻¹⁰.
  - At face value this is a problem for a flat a₀'s normalisation.
  - It moves with the M* scale, the pressure term inside the model's v_c, and the disc geometry used here. The frozen criteria grade slopes only.

## Numbers (primary: ν_mono, fitted Σ_HI, μ_mol × 1; slopes in dex per unit z, 95% bootstrap CIs, 10,000 resamples)

- **Sample:** 126 rows → 124 with every needed column → 14 bulge galaxies set aside → 110 disc-only → **109** with 0 < fDM(R_e) < 1.

| quantity | value |
|---|---|
| P1: Δ* = log M_fit − log M*_SED against z | **−0.723** [−0.966, −0.498]; median −0.112 dex |
| P1: Δ* − log(1 + μ_mol) (fitted disc vs SED + H₂) | **−0.868** [−1.107, −0.616]; median −0.512 dex |
| route (i) III's own products, n = 108 | **+0.789** [+0.514, +1.071] |
| route (ii) SED + H₂, n = 85 (D ≤ 1.05: 9 low-z, 15 high-z) | **−0.041** [−0.467, +0.360] |
| route (iii) SED stars only, n = 99 | +0.075 [−0.233, +0.349] |
| paired Δb = b_ii − b_i, n = 84 | **−0.939** [−1.261, −0.633] |
| b_iii − b_i, n = 98 | −0.693 [−0.931, −0.480] |
| reference slopes over the sample's z | flat 0; E(z) +0.258; III's law +0.298 |
| median log₁₀ a₀ at z ≈ 0.52 (lowest third): routes i / ii / iii | −9.65 / −9.69 / −9.38 (footings −10.03 / −9.95) |

**Robustness rows (R0 / R1 / R2):**

| row | b_i | b_ii | Δb | R1 for route (ii): excluded |
|---|---|---|---|---|
| primary | +0.789 | −0.041 | −0.939 | none |
| Σ_HI = 0 | +0.775 | −0.182 [−0.640, +0.233] | −1.111 | E(z), III's law |
| Σ_HI = 15 | +0.822 | +0.106 | −0.819 | none |
| μ_mol × 0.5 | +0.789 | −0.011 | −0.866 | none |
| μ_mol × 2 | +0.789 | −0.202 [−0.683, +0.289] | −1.127 | III's law |
| ν_RAR | +0.789 | −0.040 | −0.938 | none |
| route (iii) in place of (ii) | +0.789 | +0.075 | −0.693 | none |

- **R0 (closure).** Route (i)'s CI never contains III's slope, because route (i) is steeper than III's law.
  - The frozen label "does not reproduce III's rise" therefore means that it **overshoots** III's law. A rise is seen.
  - This R_e-only, per-galaxy reconstruction is not III's multi-radius RAR fit on its 79 galaxies (which 79 is not in these files).

## What this does and does not show

- **It shows** that III's rise depends on which stellar mass enters g_bar. The dynamically fitted mass has no SED prior and is fitted together with the halo (X = log M*/M_vir). It drifts against the SED mass by about 0.7 dex per unit z, and that drift is what makes a₀ rise.
- **It does not show which mass is right.**
  - The fitted "disc" is meant to include H₂, which grows with z, so its fall against SED + H₂ (−0.87 dex per unit z) is the opposite of what a correct decomposition should give.
  - Still, a z-dependent bias in the SED masses would produce the same Δ*.
- **Relation to CFG190.** CFG190 found that II (bTFR on SED masses with scaling-relation gas) and III (RAR on fitted masses) cannot share one a₀(z) law. CFG198 places that split in the mass route.
- **Stated approximations:**
  - A1: a thin exponential disc at R_e stands in for the MGE Sérsic disc of aspect 0.15.
  - A2: g_HI = πGΣ_HI, with Σ_HI prior-dominated.
  - The H₂ uses the main-sequence scaling as coded in CFG90.
  - g_obs is the model's total at R_e from its own fitted mass, Σ_HI and fDM, and includes its pressure correction. The data chat infers that correction is about half of v_c² for many of these galaxies (unverified).
- **Variant (reported): v22 at 2.2 R_d, reading v22 as v_c there (A3, unverified).**
  - The two g_obs estimates disagree: the median ratio is 0.44 (16–84% 0.22–0.61), where a flat curve would give 0.76. So v22 is probably not the same v_c.
  - In this variant route (i) gives +0.461 [+0.054, +0.886], consistent with III's law. Route (ii) gives −0.082 [−0.542, +0.417], and Δb is −0.855 [−1.213, −0.540]. R2 holds here too.

## Fixes after the first runs (all outputs kept)

1. **C1's Keplerian check.** It computed g R/(GM) instead of g R²/(GM) and reported 0.02004 (= 1.002/50).
   - The check was fixed; the disc code was unchanged, and every number was identical.
   - Kept as `*_firstrun*`.
2. **g_obs recomputed per configuration.** g_obs at R_e was recomputed inside each configuration, so the Σ_HI = 0 / 15 rows and the MUTATE run changed the total along with the baryons. That contradicts the frozen "held fixed in every route".
   - It is now computed once, from the model's own fitted mass and Σ_HI.
   - The primary numbers and the μ_mol and ν_RAR rows are unchanged.
   - The Σ_HI = 0 row's route (ii) moved from −0.106 [−0.499, +0.325] (nothing excluded) to −0.182 [−0.640, +0.233] (E(z) and III's law excluded). The Σ_HI = 15 row moved from +0.165 to +0.106 (nothing excluded either way).
   - The second main run is kept as `*_secondrun*`. The first MUTATE run is kept as `*_MUTATE_firstrun*`: it failed its control because of this bug (b_i fell by 0.31 instead of rising).
   - The fixed MUTATE run passes: b_i +0.789 → +1.126, and Δb −0.939 → −1.315.

## Correction after CFG199 (appended 2026-09-29; the text above is unchanged)

- **The "Against interest" level statement above is WITHDRAWN.**
  - CFG199 (`../CFG199_musedark_level_pressure/`) used the model's own rotation velocity at R_e from the 126 `true_Vrot.dat` files. The total that CFG198 reconstructed (D × its thin-disc g_bar) is 3–7 times larger in acceleration: median log₁₀ ratio −0.75 in reading (a) and −0.49 in reading (b).
  - On the model's own velocity, the no-pressure lower bound on the z ≈ 0.52 level is −10.38 [−10.71, −10.12] in reading (a), below both footings, and −10.14 [−10.45, −9.94] in reading (b), consistent with them. The v22 variant above was also below the footings (−10.33).
  - The 0.25–0.65 dex excess was a property of CFG198's g_obs scale, not of the data.
- **The slope findings stand.** On the model's own velocity:
  - Route (i) rises by +0.63 to +0.65. That is now consistent with III's law, so R0's overshoot was also partly the g_obs scale.
  - Route (ii) is −0.20 to −0.22.
  - Δb = −1.03 [−1.34, −0.74].
