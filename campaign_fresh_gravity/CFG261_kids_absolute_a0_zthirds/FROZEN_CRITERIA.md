# CFG261 — FROZEN CRITERIA: absolute implied-a₀ levels from the KiDS-1000 lensing RAR in lens-redshift thirds (z ≈ 0.2 and 0.4)

**This file is committed before any CFG261 script exists and before this lane has computed any absolute level (an implied a₀, or a data-to-model amplitude) from the KiDS lensing stacks.**

> **κ = ½ FITTED. ΛCDM has no a₀ (the "PROXY" below is CFG223's effective-a₀ curve, not ΛCDM). The level asked for is calibration-limited by construction, and this lane says so in advance. No sentence in its outputs says the data favour a law.**

Request (the owner, relayed 2026-10-01 by the "High-z kinematic corpus analysis" session; a relay is a request, not an approval of anything that needs one): KiDS-1000 lens-redshift thirds (z ≈ 0.20 versus 0.40), the **absolute implied-a₀ level** of each, as points in the `chart_a0z_points.csv` shape (s\* on the canonical 9.3603e-11, 68/95 % statistical interval, inner ±0.15 dex and outer ±0.30 dex baryon bands, no-root flags, extra recipe/quality columns). **Name the M\* calibration as the dominant systematic; the halves differ by 0.465 dex in mean log M.** Nothing is fetched: all data are on disk.

## 0. What is already known before this freeze (disclosure; the hand estimates in §9 were written after reading it)

1. **CFG255 (committed, orchestrator's lane; re-run byte-identical):** the same lens thirds per colour class (z medians 0.205 / 0.400 late, 0.232 / 0.378 early); the **difference** between the thirds, not a level. Combined amplitude A_data = +0.060 ± 0.038 dex (late −0.16 ± 0.10, early +0.096 ± 0.041) against FLAT +0.001; verdict NOT POSSIBLE (rival lever +0.018 dex) and NON-DISCRIMINATING by its own MUTATE; "even with infinite statistics the test is walled by the stellar-mass drift".
2. **CFG61 H3 (committed):** with the law at s = 1 the absolute early/late profiles in the seven 1-halo bins give χ² 51.9/7 (early) and 12.6/7 (late): "the law sits between the two classes: late types slightly below it, early types well above it". CFG67 H3 and the chart README state that both models' absolute profiles fail in this machinery. CFG61 R4: a colour-blind dark mass fits the class split only if early-type lenses hold about 1–1.5 × (stars + cold gas) of extra baryons (a lower bound, point-mass hot gas), untested.
3. **The July lane (b3be606a0, `real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md`, read in full before this freeze):** a different estimator (free-a₀ RAR fit in g_obs, P2 kernel, REL g_bar > 1e-13, M/L ± 0.2 dex plus a one-sided CGM) in two z halves: a₀ = 2.187e-10 (z_eff 0.236, stat ±0.041 dex, syst band 1.08–3.48e-10) and 2.864e-10 (z_eff 0.372, ±0.044, 1.43–4.54e-10), ratio 1.31 ± 0.21; "the deep-MOND degeneracy a₀_hat(δ) = a₀_hat(0)·10^−δ swamps the absolute level"; the halves differ by **0.465 dex in mean log M** (10.214 → 10.679), f_cold ≈ 0.55 → 0.21. **So for the all-class mixture the absolute level in a different estimator was above canonical before this freeze.** No number from it is a target here (different light path and different conversion).
4. **Baryon-side and redshift facts, printed while designing (no lensing signal):**

| set | N per third | z median lo / hi | mean log M\* lo / hi | Δ mean log M\* |
|---|---|---|---|---|
| late, thirds (CFG255) | 31,133 | 0.205 / 0.400 | 9.757 / 10.647 | **+0.890** |
| early, thirds (CFG255) | 29,360 | 0.232 / 0.378 | 10.509 / 10.842 | **+0.333** |
| late, window 10.3 ≤ log M\* < 10.9 (MM) | 14,736 | 0.289 / 0.421 | 10.498 / 10.686 | +0.188 |
| early, MM | 21,675 | 0.237 / 0.364 | 10.582 / 10.767 | +0.185 |

   Median f_cold = 10^(−0.69 lm + 6.63): late-LO 0.80, late-HI 0.18, early-LO 0.22, early-HI 0.14. Lens log M\* ≤ 11.0 (Brouwer's cut). **The thirds are far from mass-matched** (0.89 dex in the late class). The window MM was fixed by this table before any lensing number (counts per third ≥ 14,000 and Δ mean log M\* ≤ 0.19 dex in both classes; the z lever is reduced).
5. **Kernel facts (function evaluations only):** ν_mono(y) √y = 1.016 / 1.051 / 1.116 and P2's 1.0005 / 1.005 / 1.025 at y = 1e-3 / 1e-2 / 5e-2 (the 1-halo bins span y ≈ 1e-3 – 5e-2); **ν_mono and the exponential RAR kernel are the same function at these y** (so the "RAR" kernel is not a separate knob here).
6. **M\* calibration sources quoted by the data chat (PHASE1A_DATA_SCOPING_2026-09-30.md; not verified by this lane):** 0.29 dex per-galaxy (0.11 from redshift, 0.27 from magnitudes), 0.2 dex method-to-method, −0.056 dex offset to GAMA, an early-type factor 1.4 (0.146 dex) between two analyses of the same photometry (Mistele & McGaugh). The programme's standard bands (±0.15 / ±0.30 dex on every baryon mass) cover these; they are not new numbers.

## 1. Data (all on disk, gitignored; sha256 prefixes recorded by the stage-A output)
- `real_research/data/lensing_rar/cfg110_perlens.npz`: CFG110's per-lens sums over 181,477 KiDS-bright lenses (WG = Σ w·ΔΣ-estimator, WW = Σ w, NN = pair counts, 15 g_bar bins).
- `lr_lenses.npz` (photo-z, log M\*, M_gal = M\*(1 + f_cold), colour class typ 0 late / 1 early), `lr_esd_jackknife.npz` (the 50 June patches).
- Signal: ESD_k = ΣWG / ΣWW / KG in M⊙/pc² per bin k; **K1 = bins 8–14** (deep regime, R ≲ 0.3 Mpc), as CFG255.

## 2. Rows (fixed here)
- **Primary rows (4):** CFG255's thirds within each colour class: LO = z < the class 1/3 quantile, HI = z ≥ the class 2/3 quantile; `T-late-LO`, `T-late-HI`, `T-early-LO`, `T-early-HI`.
- **Secondary rows (4, "mass-matched"):** the same construction inside the window 10.3 ≤ log M\* < 10.9, quantiles computed within window and class: `MM-late-LO/HI`, `MM-early-LO/HI`. Reported with the same estimator; they answer "how much of a level is the mass difference between the thirds".
- **Joint rows (2):** `J-LO` = late-LO + early-LO and `J-HI` = late-HI + early-HI fitted with ONE s (14 bins), reported to show whether one a₀ describes both classes; **a joint row is never the headline** and carries the class-agreement flag (§7).
- z of a row = the median lens z of its lenses (z_shown = z).

## 3. The model (no new physics; CFG255's committed machinery, generalised in one parameter)
- The **L law stack** of CFG61/CFG255 (`law_stack`): lens by lens, in g_bar bin k the pairs sit at R = √(G M_gal / g); within a bin 8 log sub-points weighted 1/g, across lenses weight M_gal; ΔΣ of M_L(<r) = M_gal ν_mono(G M_gal / r² a₀), truncated at r_e = 0.40 r_ta (CFG7's r_ta at the lens redshift), plus the point baryons M_gal/(π R²); projector, grids (LMG 8.00–11.80 step 0.05, ZG 0.05–0.55 step 0.10, RG, rgrid) and cell assignment exactly CFG61's.
- **s is the a₀ scale: every profile (law, turnaround radius, truncation) is rebuilt at a₀·s**, a₀ = the canonical 9.3603e-11. Implied absolute a₀ = s\* × 9.3603e-11. The model depends on a₀ only through this product, so the alt footing (1.1312e-10) implies the same absolute a₀ (control C5).
- The model stack is evaluated on the grid **log₁₀ s ∈ {−1.00, −0.75, … , +1.25}** (10 points) and interpolated by a cubic spline in (log s, log m_k); a solver grid of step 0.001 in log₁₀ s with parabolic refinement. A minimum on the grid boundary is flagged **no-root / unbounded**.
- "True baryon mass" shifts (bands, scenarios) rebuild the tables with every lens's M_gal multiplied by 10^Δ **in the profile and the point term only**; the g_bar binning (the data's) keeps the nominal M_gal. (This is CFG61's `dshift` semantics for the whole M_gal.)

## 4. The estimator (headline) and its alternatives
- **Headline: inverse-variance least squares in s.** s\* = argmin over log s of Σ_{k∈K1} (d_k − m_k(s))² / σ_k², with d_k the row's stacked ESD and σ_k² the full-sample jackknife variance of d_k (50 patches). The estimator depends on the model amplitude and shape only; it uses no pair-count weights beyond the stack.
- **Statistical interval: a patch bootstrap**, B = 10,000 resamples of the 50 patches (each resample recomputes d from the per-patch sums; the model, σ_k² and the grid are held fixed; seed = crc32(row label) mod 100000), 68 % = 16–84 and 95 % = 2.5–97.5 percentiles of log s\*; the fraction of unbounded replicates is reported; the jackknife SD of log s\* (50 leave-one-patch-out solves) is reported beside it. Joint rows resample the same patches for both classes.
- **Reported alternatives (never the headline):** (i) full-covariance GLS with the Hartlap-corrected jackknife covariance; (ii) the pair-weighted amplitude (CFG110's R2b form: Σ_k NN_k d_k = Σ_k NN_k m_k(s)); (iii) the χ² of d against the model at s\* and at s = 1 (full covariance, Hartlap factor (50 − p − 2)/49, dof p − 1 and p).

## 5. The calibration bands, the named systematic, and the knobs (declared, not measured)
- **M\* calibration — named as the DOMINANT systematic.** Inner band: every baryon mass × 10^(±0.15); outer band: × 10^(±0.30) (model-side shifts, §3), s\* re-solved against the actual data. The deep-regime lever is d log₁₀ s\*/dΔ = −(1 + 2r), r = the point-baryon-to-dark ESD ratio (≈ (4/π)√y, so about −1.1 to −1.5 over the K1 bins): an under- or over-estimate of the stellar-mass zero point moves the level one-for-one or more. **For the all-lens levels the M\* zero point therefore enters the answer with a lever ≥ 1, and the lane reports the band as the headline uncertainty.**
- **Mass-dependent calibration drift (the thirds differ in mass):** scenario ε = ±0.10 dex per dex, the true baryon mass of a lens being 10^(ε (lm − 10.5)) × nominal; reported as its effect on each row's level and on the difference d = log s\*(HI) − log s\*(LO) per class. **Redshift drift:** a shift of +δ in the HI third only, δ = 0.02 and 0.05 dex (CFG255's scenarios; unsourced).
- **Cold-gas prescription (the 0.465-dex mass mismatch makes this non-cancelling):** the nominal f_cold(lm) = 10^(−0.69 lm + 6.63) is multiplied by 0.5 and by 1.5 in the model's true M_gal (the July lane's 50 % amplitude uncertainty).
- **Hot gas (early class; CFG61 R4):** a reported scenario row, extra point-mass baryons f_hot × (stars + cold gas), f_hot = 0.5 and 1.0 (Δ = +0.176 and +0.301 dex in the model's true baryon mass); **not** part of the bands.
- **Recipe knobs (the recipe band; each rebuilt or re-solved with everything else at the headline):** (a) kernel P2 for ν_mono; (b) truncation factor 0.20 and 0.80 for 0.40; (c) lens weights WW (the data's own per-bin weight sums) for M_gal; (d) f_cold × 0.5 / × 1.5 as above; (e) K1 = bins 9–14 and bins 8–12; (f) the estimator alternatives of §4. Recipe half-width = the quadrature over knobs of the largest |Δ log₁₀ s\*| inside each knob; reported in dex, **excluding the baryon bands** (kept separate, as CFG260).
- **Not modelled (stated):** satellite contamination (higher for red lenses; K1 stays inside Brouwer's isolation-reliable R ≲ 0.3 Mpc), Eddington bias in the lens M\* (scatter 0.29 dex on a steep mass function; its mass and redshift dependence is unquantified), the lens-sample reconstruction (181,477 against Brouwer's 259,383), the colour-class proxy (rest-frame u−r > 2.0), lens photo-z scatter.
- **Expected laws for the flags:** FLAT s = 1; H(z) = CFG223's `curves["H(z)"]` and PROXY = `curves["PROXY"]` interpolated at the row's median z (E at Ω_m = 0.3153: 1.109 at z = 0.2, 1.245 at 0.4; PROXY 1.03–1.06). All laws lie within 0.09 dex of each other at these redshifts, inside the inner band.

## 6. Stage A — the blind pre-flight (committed and its outputs committed before stage B is run)
Computed from the jackknife covariance, the model and mocks; **no row's data-to-model amplitude, level, ESD or difference is printed**.

**Controls (each a check that can fail):**
- **C1 (data)** the per-lens sums, summed by (patch, class), reproduce the June per-patch sums to 1e-9 relative.
- **C2 (data)** the CFG255 thirds are disjoint and each holds 1/3 of its class to 1 %; the MM counts equal the table of §0 (14,736 ± 1 and 21,675 ± 1 per third).
- **C3 (model)** the generalised stack at (s = 1, Δ = 0, ν_mono, truncation 0.40, f_cold nominal, M_gal weights) reproduces CFG61's committed law stacks for the full classes and CFG255's `law_stack` for each of the 4 + 4 sets, to 1e-9 relative, all 15 bins.
- **C4 (model)** the spline reproduces a direct rebuild at off-grid log₁₀ s = −0.625, +0.125, +0.875 to 1e-3 relative in every K1 bin of every row.
- **C5 (model)** the alt footing at s′ = s × (9.3603e-11 / 1.1312e-10) gives the canonical tables to 1e-9 (the model depends on a₀ only through a₀·s).
- **C6 (estimator)** noiseless data = model(s_true) returns s_true to 1e-4 dex in every row for s_true = 0.5, 1, 2.5; the same through the joint row.
- **C7 (error calibration, blind)** for 200 random pairs of disjoint class thirds (random assignment, seed 261) Δ = log s\*(A) − log s\*(B) and its jackknife σ_Δ are computed internally; **only** mean(Δ/σ_Δ) ∈ [−0.25, 0.25] and SD(Δ/σ_Δ) ∈ [0.8, 1.25] are printed (no single level).
- **C8 (mocks)** 2,000 mocks per row at s_true = 1 and 2.5 with noise N(0, C_row), C_row = the row's jackknife covariance: |mean(Δ log s\*)| ≤ 0.2 SD, and the analytic linearised σ within 15 % of the mock SD.
- **C9 (the pre-flight cannot see a planted level):** not applicable at stage A (no data level exists); the reactivity control is **M2 at stage B**.

**Reported (pre-flight tables):**
- **A1 levers (model against model, noiseless):** the baryon lever L_b and the band half-widths (±0.15, ±0.30) per row; each recipe knob's Δ log s\* (kernel, truncation, weights, f_cold; K1 and estimator knobs need data and are stage-B only); the hot-gas scenarios; the drift scenarios on levels and on d per class.
- **A2 statistical precision:** the mock SD of log₁₀ s\* and the analytic σ, per row.
- **A3 the calibration-dominance ratio** R_cal = 0.15 |L_b| / (68 % statistical half-width, dex), per row.
- **A4 the thirds' difference:** the jackknife σ_diff of d per class (no value of d printed); the rival's expected d = log₁₀[H(z_HI)/H(z_LO)] and PROXY's.

**Decisions (the frozen map):**
- **PF-D1 ESTIMATOR VALIDATED** iff C1–C8 pass. A failed C7 or C8 does not stop the measurement; it is carried as "error not calibrated" on every row.
- **PF-D2 CALIBRATION-LIMITED** per row iff R_cal ≥ 1 (the inner M\* band exceeds the statistical error); the output label for every row is then "M\* zero point dominates (±0.15 dex baryon → ± L_b × 0.15 dex)".
- **PF-D3 FLAT versus H(z) at z ≈ 0.2 → 0.4 from the thirds' levels**: POSSIBLE_STAT iff |d_rival| ≥ 2 σ_diff in both classes; POSSIBLE_SYS(δ) iff |d_rival| ≥ 2 √(σ_diff² + (|L_b| δ)²) for δ ∈ {0.02, 0.05}. **Expected: NOT POSSIBLE** (it is CFG255's statistic and CFG255's verdict; this lane adds no resolving power).
- **PF-D4 DRAWABLE** iff PF-D1 passes: each row is then drawn as a calibration-limited level with the stat 68 % interval, the inner and the outer band, and its label; a failed PF-D1 means NOT DRAWABLE.

## 7. Stage B — the measurement (run once, after stage A and the script are committed)
- Per row: s\*, a₀ (1e-10 m s⁻²), the patch-bootstrap 68 / 95 % intervals, the jackknife SD, χ²(s\*) with its Hartlap p (dof p − 1), χ²(s = 1) with its p, the bands (inner, outer), the recipe knob table and half-width, the hot-gas rows, the drift rows, the alternatives of §4, **the baryon mass shift (dex) that would bring s\* to 1 (a diagnostic, interpolated/extrapolated from the band solutions)**.
- Per class: d = log₁₀ s\*(HI) − log₁₀ s\*(LO) with its jackknife σ and its band-and-scenario budget; compared with CFG255's committed amplitudes (control M3).
- **Flags per law (FLAT, H(z), PROXY):** `in95` (the law's s inside the statistical 95 % interval), `in15` (inside the hull of that interval and the inner band's two solutions), `in30` (the same with the outer band); written as three letters Y/n per law.
- **Class agreement flag (per third):** the late and early rows' 95 % statistical intervals, each widened by the outer band, overlap → "classes consistent within the outer band"; otherwise "classes disagree: one a₀ does not describe both".
- **Shape adequacy flag:** χ²(s\*) p ≥ 0.01 → "amplitude-and-shape adequate"; else "amplitude-matched only (shape fails)".
- The **points file** `cfg261_points.csv`: first 18 columns equal `chart_a0z_points.csv`'s header (control M4), then `recipe_half_dex, recipe_lo, recipe_hi, n, class, third, set, R_cal, chi2_s, p_shape, flags_FLAT, flags_H(z), flags_PROXY, quality`; gas_class = "LENS (scaling-relation cold gas)".
- **No verdict words.** The reading is descriptive: a level, its bands, its label, its flags.

**Controls at stage B:**
- **M2 MUTATE=1 (reactivity; separate output files):** the lenses of every row are multiplied bin by bin in WG by m_k(s = 2)/m_k(s = 1) of that lens's own cell, so the data shift is the model's own amplitude change; the measured Δ log₁₀ s\* against the main run must be +0.301 ± 0.02 in every row (the planted factor 2), including the joint rows. A failure declares the estimator NON-REACTIVE whatever stage A said.
- **M3 (consistency with CFG255, reported):** d (HI − LO) per class equals 2 × (A_data − A_FLAT) of CFG255's committed stage-B JSON within 1 σ_diff (different estimators: GLS-to-the-model versus pair-weighted ratio).
- **M4** the points file's first 18 columns equal the chart header.
- **M5** every joint row's log s\* lies between its two class rows' (the hull), within the bootstrap error.

**SELFTEST (allowed before the measurement, debugging only; outputs to `_SELFTEST` files):** fabricated per-lens sums WG = WW × KG × (the lens cell's own model ESD at s_true) plus noise drawn from each row's covariance; the stage-B pipeline must return s_true within its bootstrap interval for every row. It reads no real signal.

## 8. Run order and outputs
`cfg261_kids_abs.py` with `STAGE=A` (pre-flight; commit `.out` + `_results.json`), then `STAGE=B` once (and `STAGE=B MUTATE=1`), `README.md`; first runs kept as `*_firstrun*` whenever a control fails and the script is changed; every post-hoc change is a dated addendum to this file written before the rerun. Commit explicit paths only; push; send the hashes to the orchestrator for the re-run (no LEDGER.md edit for this lane).

## 9. Hand estimates (written after §0; scored by stage A, kept as they fall)
- **HE1 baryon lever:** L_b ∈ [−1.50, −1.12] for every primary row (central −1.3; r = (4/π)√y over y = 1e-3…5e-2).
- **HE2 band half-widths:** inner ∈ [0.17, 0.23] dex, outer ∈ [0.34, 0.45] dex in s\*.
- **HE3 statistical precision (SD of log₁₀ s\* in the mocks, 68 % half-width):** late-LO 0.12–0.30, late-HI 0.07–0.20, early-LO 0.04–0.12, early-HI 0.04–0.12 dex.
- **HE4 calibration dominance:** R_cal ≥ 1.5 for both early rows, ≥ 1.0 for late-HI, between 0.6 and 1.6 for late-LO.
- **HE5 kernel:** P2 against ν_mono moves every row by Δ log₁₀ s\* = +0.03 … +0.08 (P2 is the smaller kernel; the amplitude ratio (1.116/1.025)² over y ≈ 0.05 shrinks toward 1 at small y).
- **HE6 truncation 0.20 / 0.80:** |Δ log₁₀ s\*| ≤ 0.01.
- **HE7 weights WW against M_gal (model against model):** |Δ| ≤ 0.03.
- **HE8 cold gas × 0.5 (× 1.5 has the opposite sign, about 0.75 of the size):** Δ log₁₀ s\* = late-LO +0.10 … +0.20; late-HI +0.03 … +0.07; early-LO +0.04 … +0.08; early-HI +0.02 … +0.06.
- **HE9 drift ε = +0.10 dex/dex on d (HI − LO):** late −0.09 … −0.14, early −0.03 … −0.055; MM rows about 0.025 either class. δ = 0.05 on HI alone: |Δd| = 0.055 … 0.075.
- **HE10 hot gas on the early rows:** f_hot = 0.5: Δ log₁₀ s\* = −0.20 … −0.26; f_hot = 1.0: −0.35 … −0.44.
- **HE11 error calibration (C7):** mean(Δ/σ_Δ) ∈ [−0.25, 0.25], SD ∈ [0.8, 1.25]; **HE12 mocks (C8):** pass.
- **HE13 PF-D3:** NOT POSSIBLE_STAT in both classes (σ_diff: late ≈ 0.2, early ≈ 0.09 dex against |d_rival| ≈ 0.05).
- **HE14 (scored at stage B; the levels were NOT estimated blind):** late-class levels s\* ∈ [0.4, 1.4]; early-class levels s\* ∈ [1.5, 6]; the two classes disagree at the 95 % level before the bands (a restatement of CFG61 H3) and the joint rows fail the shape flag; d late ∈ [−0.7, +0.1], d early ∈ [0.0, +0.4] (a restatement of CFG255's amplitudes ×2 and therefore a consistency check, not an independent estimate); MM rows differ from their T rows by ≤ 0.25 dex for late-HI and both early rows and by ≤ 0.5 dex for late-LO.

## 10. What this lane cannot say
- It does not measure a₀ at z ≈ 0.2–0.4: the level is the product of the assumed baryon census (the M\* zero point, the cold-gas prescription, any hot gas) and the law, with a lever of at least one; the inner band is the programme's smallest honest uncertainty and is not smaller than the statistical error for most rows.
- It cannot separate FLAT from H(z) or PROXY (PF-D3; all laws lie within 0.09 dex of each other at these redshifts).
- It cannot say whether the classes disagree because of baryons (hot gas, M\* by colour) or because of the law (CFG61 R4 leaves this open).
- It adds no information on the change between the thirds beyond CFG255 and the July lane; the new content is the absolute scale and its calibration budget.
- A level near, above or below the canonical a₀ is not read as support or tension for any law.
