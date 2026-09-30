# CFG216 — RC100 within-sample δ(z) test with velocities (100 massive discs, z 0.61–2.52)

- **Criteria:** `FROZEN_CRITERIA.md` (96d384dba), committed before any number. **κ = ½ FITTED, NOT DERIVED.** Author decompositions, not a direct a₀ measurement.
- **Run:** `python3 campaign_fresh_gravity/CFG216_rc100_within_sample/cfg216_rc100.py`, about 14 s. The main run passes 3/3 checks, with C2 the reported cross-check. `MUTATE=1` (an injected slope of +0.2 per unit z) passes 4/4: the slope moves by exactly +0.200 and the outcome flips to W-mixed.
- **Data:** the RC100 table (Nestor Shachar+2023): V_c(R_e), f_DM(R_e), R_e and z per galaxy. No geometry assumption is needed: D_obs = 1/(1 − f_DM), g_obs = V_c²/R_e, and g_bar = (1 − f_DM) g_obs. All 100 rows are analysed.

## Bottom line

**Within this one homogeneous analysis, the rival's z-dependence is not in the data. The frozen outcome is W-flat in all four kernel and footing cells.**

- **Slope of δ_flat on z (ν_mono, canonical): −0.029 [−0.071, +0.002] per unit z.** That is consistent with flat, since the CI contains 0 (barely).
- **Slope of δ_rival on z: −0.092 [−0.128, −0.055].** It is negative at 4.8σ, which is the drift a true flat law would produce.
- **Expected slopes if each law were exactly true,** with g_obs and z held at the sample's values:

| if this law were exactly true | slope of δ_flat | slope of δ_rival |
|---|---|---|
| flat | 0.000 | −0.060 |
| rival | **+0.073** | 0.000 |

  - The observed δ_flat slope (−0.029 ± 0.018) is 1.6σ from the flat expectation and **5.5σ from the rival expectation**.
  - The observed δ_rival slope (−0.092 ± 0.019) is 1.7σ from the flat expectation and **4.9σ from the rival expectation**.
- **Level (ν_mono, canonical):**
  - flat: median +0.031 [+0.008, +0.064], marginally DISFAVOURED-over (D_obs above the flat prediction by 7%);
  - rival: median −0.052 [−0.074, −0.023], DISFAVOURED-under.
- **By z-half:**

| half | n | median z | flat | rival |
|---|---|---|---|---|
| z ≤ 1.53 | 51 | 0.99 | +0.041 [+0.014, +0.099] over | +0.003 [−0.054, +0.049] consistent |
| z > 1.53 | 49 | 2.19 | +0.009 [−0.007, +0.064] consistent | **−0.096 [−0.136, −0.051] under** |

  In the high-z half, where the rival's a₀ is about 3 times larger, the rival over-predicts the hidden mass and flat is consistent.

## Sensitivities (reported beside the primary)

| variant | n | flat: median, slope | rival: median, slope |
|---|---|---|---|
| (a) the RC41 subset | 38 | +0.041, +0.005 [−0.062, +0.068] | −0.035, −0.056 [−0.124, +0.015] |
| (b) the other galaxies | 62 | +0.017, **−0.055 [−0.099, −0.007]** | −0.060, −0.112 [−0.154, −0.067] |
| (c) g_bar < 3 a₀ | 67 | +0.042, −0.035 [−0.091, +0.020] | −0.061, −0.104 [−0.159, −0.051] |
| (d) g_bar from the table's M_bar (thin disc) | 100 | +0.049, −0.040 [−0.099, +0.019] | −0.049, −0.095 [−0.156, −0.047] |

- The sign of the flat slope is negative in every variant, and the rival's slope excludes 0 in all of them. The route/selection-dependent label does not apply: variant (d) has the same sign.
- In the 62 non-RC41 galaxies the flat slope excludes 0 on the negative side (−0.055). That is, D_obs falls slightly below the flat law's prediction as z rises. That is not the rival's direction. It is the direction of a slowly DECLINING a₀ or of heavier baryons at high z, and it is not resolved here.

## Cross-check of CFG215 (C2), and a correction to it

- **38 of the 41 RC41 galaxies are found in RC100 by name.** The median of [δ_flat(RC100's V_c and f_DM) − δ_flat(CFG215's disc + bulge geometry)] is **−0.042 dex** (range −0.35 to +0.03), inside the frozen 0.05 line.
- The consequence is that CFG215's RC41 flat median of +0.102 was partly geometry. On RC100's own V_c and f_DM, the RC41 subset gives **+0.041 [+0.004, +0.109]**, borderline rather than clearly DISFAVOURED-over. A correction section has been appended to CFG215's README.

## Limits

- **Overlap:** RC100 contains the RC41 galaxies (38 of 41 matched). This lane is not independent of CFG215's RC41 or of CFG213's samples of the same fitting method.
- **M_bar is prior-anchored** to SED plus gas, and the gas scaling grows with z. Any z-dependence of that prior, or of the sample selection, enters the slopes. Variant (d) gives the same sign but uses the same M_bar column.
- **f_DM and V_c are model outputs** (an NFW halo, with the authors' pressure correction already applied). The statistic uses MAP values, and the fits' own uncertainties are not propagated.
- Nothing here says the data favour the framework. The result is that this sample shows no rival-like z-dependence.

## Post hoc: the a₀(z) power-law index RC100 prefers (appended 2026-09-29, after the frozen run; reported only)

- `cfg216_posthoc_index.py` solves for a₀(z) = a₀,can × 10^c × (1 + z)^p such that the median δ = 0 and the Theil–Sen slope of δ on z = 0, with a galaxy bootstrap (2,000 resamples).
- **Result (ν_mono, canonical): p = −0.72 [−1.49, +0.14] (σ 0.42), c = +0.44 dex.**
  - Flat (p = 0) is 1.7σ away and the rival (p = 1.29 over this z range) is 4.8σ away.
  - The alt footing gives the same p (−0.72 [−1.47, +0.16]).
  - The wide interval reflects D's weak dependence on a₀ at these accelerations: δ = +0.03 corresponds to about ×1.4 in a₀.
- **Caveat from CFG217.** A differential baryon-mass systematic of about 0.15 to 0.25 dex between z ≈ 0.6 and 2.5 moves p by about 1 to 1.5. So the index inherits the gas-route limit and should be quoted with it.
