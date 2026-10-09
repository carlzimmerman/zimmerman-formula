# CFG566: forward-model the high-z implied-a₀ estimators under three truths. FROZEN before any script or number exists

κ = ½ is FITTED. Both footings for the framework and flat truths: a₀ = 9.3603e-11 (canonical, the estimator's internal scale) and 1.1312e-10 (alt). No dark-matter particle is added; the cold mass is still required. ΛCDM is the comparator, and no sentence will say the data favour the framework over ΛCDM.

**Why.** CFG565 found that ΛCDM-with-feedback's RAR scale g† (a full-RAR fit) rises ×2.8 / ×4.9 at z = 2 / 2.5, against the framework's a₀ tracking ρ_DE (~0.87 / ~0.82). The record's high-z numbers are not full-RAR fits. They are CFG223's median-residual implied-a₀ estimator applied to a few near-Newtonian points per galaxy. The two are not comparable until both truths are pushed through the same estimator, on the same galaxies, with the same inputs.

## 1. Rows (the committed estimators reused, unedited)
- **R1: KMOS3D pooled PT1 (CFG270, b2e86a913).** 72 T1 fits, z 2.00–2.68, median 2.23. Estimator: `hzq_core.s_status` (CFG223's `implied`, read-only) on D = g_obs/g_bar,★ at r = 2.2 r_d, with stars-only thin-disc baryons (H-band R_e). Committed value s★ = 2.4413. The inputs (z, log M★, R_e, r) are rebuilt by exec'ing CFG270's committed source up to its `STAGE A` marker, which writes no file. The T1 mask is CFG270's.
- **R2–R5: RC100 native route B quartiles Q1–Q4 (CFG303, 2d9bdc1b9).** z medians 0.81 / 1.36 / 2.01 / 2.26. Estimator: CFG223's `analyse` / `implied` (exec'd from `cfg223_a0_over_time.py` up to its CONTROLS marker, as CFG303 does). Baryons: SED M★ (col 6) × (1 + μ_t18) in CFG216's thin disc at R_e. g_obs = V_c²/R_e. Inputs are read from the committed `cfg303_rc100_pergalaxy_LCDMFREE.csv`. Committed: 1.483 / 1.014 / 0.842 / no root (floor). Q3 and Q4 are the high-z rows; Q1 and Q2 are reported with the same rules.
- **MUSE-DARK native routes (CFG303): NOT run (declared now).** Their g_obs is CFG262's DC14 model slit velocity, a ΛCDM-halo fit output, and needs run files beside the repo. Their z ≤ 1.2, where CFG565's C and the framework differ by ≤ ×1.2, and their recipe half-widths are 0.74–0.93 dex. A forward model there cannot discriminate and would reuse a halo-model g_obs.
- R1 and RC100 share galaxies (14 T1 fits match RC100), so the rows are not independent. They are never combined into one statistic.

## 2. Truths (g_obs at each galaxy's own radius and redshift, from the TRUE baryons)
- **(A) Framework, a₀ tracking ρ_DE:** g_obs = g_bar ν_mono(g_bar / a₀(z)), with a₀(z) = a₀(0) × M-DEC(z) from `CFG223_a0_over_cosmic_time/cfg223_results.json` (the curve the chart uses: 0.873 at z = 2.01, 0.849 at 2.23). Both footings.
- **(B) Flat a₀:** the same with M-DEC ≡ 1. Both footings. Reported; not part of the A-vs-C verdict.
- **(C) ΛCDM with feedback:** g_obs = g_bar + g_halo(r). CFG565's machinery at the galaxy's z: halo mass from inverting Moster+13(z) at the catalogue M★ (stars), 0.15 dex SHMR scatter (in M★ at fixed Mh, mapped through the local slope as CFG565 does); Dutton-Macciò c(M, z) with 0.11 dex scatter; DC14 profile at X = log M★ − log Mh with its concentration boost; R₂₀₀ at 200 ρ_c(z) (Ω_m 0.315, h 0.7). The `moster`, `inv` and `cdm` functions are exec'd from CFG565's committed source; `XG`, `menc` and `dc14` from CFG477's, as CFG565 does. The halo is not re-fitted; the radii are the measured high-z radii, so CFG565's size-evolution law is NOT used.

## 3. True baryons, noise and systematics (declared; the same for every truth)
- **Gas in the truth.** R1's estimator sees stars only. Two branches, never pooled:
  - **G0:** no gas. This is the minimum-baryon truth and gives the lowest prediction for every truth.
  - **G1:** CFG270's B2 scaling gas, μ_mol(z, M★), in the stellar disc geometry. This is the maximum declared gas.
  - RC100 route B's baryons already contain μ_t18 gas, so its truth is the catalogue baryons (one branch).
- **Per galaxy and realisation:** true baryon mass = catalogue × 10^(δ_shared + δ_i), with δ_i ~ N(0, 0.20) dex (CFG270 C6's M★ error). The observed g_obs = true × 10^N(0, 0.15) dex (CFG270 C6). (C) also draws its halo scatter per galaxy and realisation.
- **Shared baryon zero-point:** δ_shared ~ N(0, 0.15) dex per realisation (the record's inner calibration band).
- **R1 recipe systematic:** the committed PT1 recipe half-width, 0.61 dex (pressure, inclination, geometry, kernel), is taken as 1σ. It is added to each realisation's log s★ when the realisation has a root. RC100 B carries no separate recipe width beyond its baryon band, which δ_shared models.
- 1,000 realisations per truth per branch; seed 566. The estimator output for one realisation is the pooled point value for the row: no root with median D ≤ 1 is the FLOOR (log s★ = −3); no root with median D > 1 is the CEILING (+3), per hzq_core's rule.

## 4. Statistic and power (stated before comparing to data)
- **Per row, per truth:** the predicted distribution of log s★, reported as median and 16 / 84 / 2.3 / 97.7 %. Also p_lo = P(pred ≤ obs) and p_hi = P(pred ≥ obs), counting ties, with obs the committed value (−3 for a floor).
- **Power per row:** Δ = |median_A − median_C| / √(hw_A² + hw_C²), with hw = (p84 − p16)/2 of log s★. A is taken at the footing that gives the smaller Δ. For R1, power is computed in G0. Power < 1 makes a row NON-DISCRIMINATING. A diagnostic power without the recipe systematic and without δ_shared is also printed; it is not used for any verdict.

## 5. Verdicts (per row, then overall)
- **R1 (stars-only data side; the "upper bound" row).**
  - A truth is **TOO HIGH** if p_lo < 0.0228 in G0. Its prediction then exceeds the committed bound at > 2σ even with no gas.
  - It is **TOO LOW** if p_hi < 0.0228 in G1. Even the maximum declared gas then cannot reach the data.
- **RC100 rows (measured value).** A truth **MISSES** if min(p_lo, p_hi) < 0.00135 (> 3σ).
- A truth is **disfavoured on a row** if it is TOO HIGH, TOO LOW or MISSES there. The framework counts as disfavoured only if both footings are.
- **Overall:**
  - **FEEDBACK-LCDM DISFAVOURED:** C is disfavoured on ≥ 1 row with power ≥ 1, and the framework is not disfavoured on that row.
  - **FRAMEWORK DISFAVOURED:** the same rule with the roles of A and C swapped.
  - **BOTH DISFAVOURED:** if both of the above hold, on different rows.
  - **NEITHER FITS:** if A and C are both disfavoured on the same powered row. This is reported per row.
  - **NON-DISCRIMINATING:** if no row has power ≥ 1. This verdict overrides the others, which are then reported as row flags only.
  - **CONSISTENT WITH BOTH:** otherwise.
- Flat-a₀ (B) flags are reported and enter no verdict.

## 6. Controls
- **K1:** R1's committed PT1 s★ is reproduced from CFG270's inputs (V₂₂, σ₀, pressure term 2(r/r_d) σ₀²) within 1e-3: 2.4413.
- **K2:** RC100 B Q1–Q3 log s★ and Q4's no-root are reproduced from the committed per-galaxy CSV through CFG223's `analyse`, to 1e-6.
- **K3:** noiseless injection. A at the canonical footing, G0, with no noise, no δ and no recipe, returns R1's pooled s★ within 0.03 dex of the median of a₀(z_i)/a₀C over the 72 rows. B returns 1.000 to 1e-6.
- **K4:** CFG565's K2 holds in the exec'd code (the Moster z-terms vanish at z = 0).
- Every control is kept as it falls; a failed control is reported, not fixed after the fact.

## 7. MUTATE (`--mutate`)
The A and C mocks swap labels: the "C" row is fed A's mocks and vice versa. Detection: the C-labelled R1 (G0) median log s★ moves by > 0.1 dex from the main run. The script reports whether any verdict word changes and exits 1 when the shift is detected.

## 8. Hand estimates (frozen; scored as they fall)
- **HE1:** R1 G0 prediction under A is 0.6–1.2. Under C it is ≥ 2.
- **HE2:** R1 power (with recipe) < 1, so it is NON-DISCRIMINATING because of the 0.61 dex recipe and the baryon lever.
- **HE3:** R1 diagnostic power, without recipe or δ_shared, is ≥ 1.

## 9. Compute and files
Light; niced, BLAS threads 1. On-disk data only; nothing fetched. Outputs go to this directory only, and MUTATE outputs carry `_MUTATE`.
