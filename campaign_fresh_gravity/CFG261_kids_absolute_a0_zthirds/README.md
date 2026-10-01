# CFG261 — KiDS-1000 lensing: absolute implied-a₀ levels in lens-redshift thirds (z ≈ 0.2 and 0.4), M\* calibration named as the dominant systematic

> **κ = ½ FITTED. ΛCDM has no a₀ (PROXY = CFG223's effective-a₀ curve). The levels are calibration-limited by construction: the lens stellar-mass zero point enters with a lever of −1.1 dex per dex, so ±0.15 dex in baryon mass is ±0.17 dex in the implied a₀ and ±0.30 dex is ±0.34 dex. No sentence says the data favour a law.**
> Hashes: criteria **ec413346f** (before any script) · stage A pre-flight **c55ea0fc1** (before any real level) · measurement script + SELFTEST **aa3c155d5** (before the measurement) · measurement, MUTATE and this README: the commit that carries this file. Data on disk only (CFG110's per-lens sums of the June KiDS-1000 estimator, 181,477 KiDS-bright lenses); nothing fetched.

## Bottom line
1. **The absolute level depends on colour class, and the two classes diverge with redshift.** The implied a₀ scale s\* (relative to the canonical 9.3603e-11; absolute a₀ = s\* × 0.936e-10) in the CFG255 thirds:

| row | z | N | s\* | a₀ (1e-10) | 68 % | 95 % | ±0.15 dex M\* band | ±0.30 dex band | recipe ± dex |
|---|---|---|---|---|---|---|---|---|---|
| late, low-z third | 0.205 | 31,133 | **1.67** | 1.56 | 1.29–2.10 | 0.98–2.54 | 1.13–2.43 | 0.76–3.49 | 0.19 |
| late, high-z third | 0.400 | 31,133 | **0.68** | 0.64 | 0.43–0.99 | 0.25–1.33 | 0.45–1.01 | 0.29–1.47 | 0.16 |
| early, low-z third | 0.232 | 29,360 | **2.48** | 2.33 | 2.19–2.80 | 1.94–3.12 | 1.70–3.59 | 1.15–5.16 | 0.06 |
| early, high-z third | 0.378 | 29,360 | **4.12** | 3.85 | 3.71–4.53 | 3.35–4.97 | 2.83–5.93 | 1.92–8.50 | 0.06 |

   - **Late-type lenses** sit near or below the canonical scale (s\* 1.67 → 0.68; both consistent with 1 inside the 95 % intervals).
   - **Early-type lenses** sit well above it at both redshifts (2.5 and 4.1) and **outside even the outer ±0.30 dex band** for the FLAT, H(z) and PROXY values (flags `nnn`).
   - **At the high-z third the classes disagree** (late [0.25, 1.33] against early [3.35, 4.97] at 95 %, still apart after widening by the outer band): **one a₀ does not describe both classes**, which is CFG61's colour split (3.7σ in the 1-halo bins) seen again as an absolute level, and it grows with redshift.
2. **The thirds' difference d = log₁₀ s\*(high z) − log₁₀ s\*(low z)** (jackknife σ):

| class | d | σ | the rival H(z) expects | CFG255's committed amplitude ×2 |
|---|---|---|---|---|
| late | **−0.388** | 0.222 | +0.049 | −0.321 |
| early | **+0.219** | 0.074 | +0.037 | +0.189 |

   The opposite signs in the two classes and the size in the early class (3σ) are **not read as evidence for or against a₀(z)**: the stellar-mass drift between the thirds moves d by only −0.025 (early) / −0.075 (late) per +0.10 dex-per-dex mass-dependent calibration slope and by −0.054 per +0.05 dex in the high-z third alone (all scenarios in the output), so a calibration offset of about +0.2 dex (the high-z early third's true baryon mass above the assigned one, relative to the low-z third) would remove the early-class d. FLAT versus H(z) from the thirds' levels was **NOT POSSIBLE before the measurement** (stage A: σ_diff 0.222 / 0.074 against the rival's +0.049 / +0.037) and remains so.
3. **The M\* calibration is the dominant systematic and it is a lever of −1.1 (−1.06 to −1.24) in every row:**
   - to bring the early class to s\* = 1 the baryon mass would have to be higher by **+0.36 dex (low-z) and +0.57 dex (high-z)**, i.e. extra baryons of **1.3× and 2.7×** the stars-plus-cold-gas mass if they sit inside the lens as a point mass (CFG61 R4 estimated at least 1–1.5×); for the late class the shifts are **+0.20 dex (low-z) and −0.15 dex (high-z)**;
   - the stated per-galaxy stellar-mass scatter (0.29 dex), the method-to-method systematic (0.2 dex) and the early-type factor between two analyses of the same photometry (0.146 dex; Mistele & McGaugh) are all of the order of the inner band, and the Eddington bias of a steep mass function with that scatter is unquantified and mass-and-redshift dependent.
4. **Mass-matching changes little where it is measurable:** within 10.3 ≤ log M\* < 10.9 the thirds differ by 0.19 dex in mean log M\* (not 0.89 late, 0.33 early) and the early rows barely move (2.70 and 4.60: +0.04 and +0.05 dex against the thirds); the late high-z row is poorly constrained there (s\* 0.37, 68 % 0.12–0.78, 14 % of the resamples reach the grid floor).
5. **What this does not add:** the thirds' difference carries CFG255's verdict (NOT POSSIBLE, NON-DISCRIMINATING) and the July lane's null; the new content is the absolute scale, its class dependence, and its calibration budget.

## Result details
- **Estimator (frozen):** inverse-variance least squares in s over the seven 1-halo bins (K1 = 8–14) with the full-sample jackknife variances; model = CFG61/CFG255's L law stack with every profile (law, turnaround radius, truncation) rebuilt at a₀ × s on a 10-node log s grid; patch bootstrap B = 10,000 (the jackknife SD is within 5 % of the bootstrap SD in every row but MM-late-HI, 0.388 against 0.338).
- **Shape adequacy:** χ²(s\*) is acceptable in all single rows (late-LO 16.5/6, p = 0.011; the others p = 0.25–0.82), so the amplitude-matched model also fits the radial shape; the joint rows do not fit one s (J-HI 48.9/13, p = 4.6e-6; J-LO 26.4/13, p = 0.015). At s = 1 the early rows are rejected (37.0/7 and 99.9/7), the late low-z row marginally (19.4/7, p = 0.007) and the late high-z row not (3.4/7).
- **Recipe knobs (Δ log₁₀ s\*, whole table in the output):** kernel P2 for ν_mono +0.03…+0.08; truncation 0.20 up to −0.02; weights WW 0.000; cold gas × 0.5 / × 1.5 +0.09 / −0.08 (late-LO), ≤ ±0.05 elsewhere; K1 variants up to +0.16 (late-LO, bins 8–12, i.e. dropping the two highest-g_bar bins); estimator alternatives (full-covariance GLS, pair-weighted amplitude) up to +0.23 (MM-late-HI). Recipe half-width 0.06–0.26 dex: at or below the inner M\* band (0.17) in every row except T-late-LO (0.19) and MM-late-HI (0.26).
- **Hot-gas scenario on the early rows:** f_hot = 0.5 / 1.0 moves s\* by −0.19…−0.21 / −0.33…−0.37 dex (not part of the bands).
- **Footing:** the absolute a₀ is footing-independent (the model depends on a₀ only through a₀ × s; control C5 exact).

## Controls and MUTATE (nothing hidden)
- **Stage A (c55ea0fc1): C1–C8 pass** (stack equals CFG61/CFG255 to 9e-16, spline 8.9e-4, alt-footing identity exact, noiseless identity 6e-7, mocks unbiased with σ within 15 %, **blind random-thirds calibration mean −0.003 / SD 1.014 over 200 pairs**).
- **Stage B: M3** (the thirds' difference against CFG255's committed amplitudes within 1 σ_diff) **passes**; **M5** (each joint row inside the hull of its classes) passes; **M4** (points-file header) passes. **M2 MUTATE=1 passes: the planted factor 2 moves every row by +0.291 … +0.311 dex (planted +0.301; tolerance ±0.02), joint rows included.**
- **SELFTEST** (aa3c155d5): fabricated sums at s_true = 1.7 return the truth in every single row (the early rows −0.11 dex, the common noise draw; the noiseless variant returns 1.700 exactly).

## Hand estimates (frozen before any number; kept as they fall)
- **Stage A:** hits HE1, HE3, HE4, HE5, HE7, HE10–HE13; **misses HE2, HE6, HE8, HE9** (PREFLIGHT_RESULTS.md).
- **HE14 (stage B; the levels were NOT estimated blind):** late levels ∈ [0.4, 1.4] — **late-LO 1.67 misses**, late-HI 0.68 hits; early levels ∈ [1.5, 6] — **hits** (2.48, 4.12); "the two classes disagree at 95 % before the bands" — **hits at the high-z third only** (low-z third: late 0.98–2.54 against early 1.94–3.12 overlap); "the joint rows fail the shape flag" — **J-HI fails (p 4.6e-6), J-LO does not (p 0.015)**; d late ∈ [−0.7, +0.1] hits (−0.388); d early ∈ [0.0, +0.4] hits (+0.219); MM rows within 0.25 dex of their T rows (0.5 for late-LO) — hits for early-LO/HI and late-LO (+0.04, +0.05, +0.08), **misses for late-HI (−0.27)**.

## Disclosures
- Before the freeze the author had read CFG255's amplitudes, CFG61 H3 (law at s = 1: late 12.6/7, early 51.9/7) and the July lane's free-a₀ per-half fits (2.19e-10 / 2.86e-10; a different estimator, REL cut g_bar > 1e-13, P2 kernel). The early-class excess and the late-class near-canonical level are the same pattern as CFG61 H3; the July all-class mixture (about 2.3 and 3.1 in s\*) lies between the class rows here.
- The 160 model tables take about 11 minutes cold and are cached in the untracked `_cache/`; the generalised stack is control-tied to CFG61/CFG255. `RuntimeWarning: invalid value encountered in matmul` lines are the known numpy 1.26 / Accelerate artefact (all results finite).
- Not modelled (stated in the criteria): satellite contamination (K1 stays inside R ≲ 0.3 Mpc), lens-sample reconstruction (181,477 against Brouwer's 259,383), the colour-class proxy (rest-frame u−r > 2.0), photo-z scatter, the Eddington bias.
- **A level is not a measurement of a₀ at z ≈ 0.2–0.4.** It is the product of the assumed baryon census and the law; two baryon censuses (late-type and early-type) disagree by a factor of 1.5–6 at the same nominal M\*.

## Files
`FROZEN_CRITERIA.md`, `PREFLIGHT_RESULTS.md`, `cfg261_kids_abs.py`; outputs `cfg261_stageA.out` / `_results.json`, `cfg261_stageB.out` / `_results.json`, `cfg261_points_stageB.csv` (chart shape; 10 rows), `cfg261_stageB_MUTATE1.*`, `cfg261_stageB_SELFTEST*.*`. Run: `STAGE=A python3 cfg261_kids_abs.py`, then `STAGE=B` (and `STAGE=B MUTATE=1`); needs `real_research/data/lensing_rar/` (about 17 GB, gitignored) and the CFG61 prefix chain (`hunt_2026/` at the repo root).
