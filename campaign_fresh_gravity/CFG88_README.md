# CFG88 — does the KiDS early/late split survive a data-driven covariance?

- **Criteria:** frozen in `CFG88_FROZEN_CRITERIA.md` (7db367888), before any number in the seven 1-halo (K1) bins.
- **Script:** `CFG88_kids_split_jackknife.py`, under 1 s.
- **Runs:**
  - The main run passes 12 of 12 and exits 0.
  - The MUTATE run (a random per-patch early/late swap) fails H1 and H2 and exits 1.
  - The two runs fail different checks, so the control is informative.
- **Outputs:** `.out` / `_results.json`, and the `_MUTATE` pair.

## Bottom line

**The split survives a data-driven covariance.**
- **The data.** The repo's own June 2026 re-measurement of the KiDS-1000 lensing: 181,477 isolated lenses and 21.3 M sources.
- **The covariance.** A leave-one-patch-out jackknife over 50 sky patches, which includes cosmic variance and patch-to-patch systematics. It passes a calibration null.
- **B's law is rejected.** The colour-blind zero model (B's law, and every colour-blind dark mass) is rejected in CFG61's seven 1-halo bins at **χ² 35.0/7, p = 1.1 × 10⁻⁵ (4.4σ)**. That is stronger than with Brouwer's released covariance (28.1/7).
- **ΛCDM fits.** CFG67's colour-split ΛCDM, built from the same lenses, fits: **7.4/7 (p = 0.39)**, with best-fit amplitude 0.89 ± 0.14.

**What this answers, and what it does not.**
- **It answers CFG77's fragility point** (errors × 1.5 → p = 0.086) for sample variance and patch-level systematics.
  - The jackknife errors are close to the released ones once scaled for sample size. The median ratio is 1.22 (late) and 1.05 (early), against √(259,383/181,477) = 1.20. They show no 1.3–1.6× underestimate.
  - The split would still need errors 1.27× larger to fall to 3σ, and 1.58× larger to reach p = 0.05.
- **It does not answer the rest.** A jackknife cannot see systematics common to all patches (shear calibration, photo-z), colour-class contamination, or satellite fractions that differ by colour. These remain open.
- **The zero-model caveat stands.** This rejects every colour-blind dark mass, not B specifically among them (CFG77).

## Results (K1: g_bar bins 8–14, 10^−12.9 to 10^−11.4 m/s²)

| | χ² / 7 (Hartlap 0.837) | p |
|---|---|---|
| **B's law (zero difference)** | **35.04** | **1.1 × 10⁻⁵ (4.4σ)** |
| **CFG67's ΛCDM** | **7.37** | **0.39** |
| B's law, raw / diagonal only | 41.9 / 38.9 | |
| B's law, 25 merged patches | 23.6 | 1.3 × 10⁻³ (3.2σ) |
| ΛCDM, 25 merged patches | 5.1 | 0.64 |
| all 15 bins (the June number): law / ΛCDM | 84.8/15 / 17.1/15 | 9 × 10⁻¹² / 0.31 |

Early minus late in K1 (M☉/pc²), with the jackknife σ and CFG67's ΛCDM prediction:

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| measured D | 3.26 | 7.14 | 5.61 | 5.33 | 11.92 | 21.48 | 33.28 |
| jackknife σ | 1.79 | 2.14 | 3.02 | 3.18 | 7.09 | 7.89 | 11.81 |
| ΛCDM D | 4.18 | 5.84 | 7.92 | 10.37 | 13.08 | 15.85 | 18.43 |

- **Correlations.** The jackknife correlations between K1 bins are small: the largest |r| is 0.23, and the mean is 0.00.
- **Dropping one bin.** With any single K1 bin dropped, B's law stays rejected at p ≤ 2.9 × 10⁻⁴. The weakest case is dropping bin 9: 25.4/6.

## Controls

- **C1:** the June analysis is reproduced from the per-patch sums exactly: the ESD, the difference, and the all-15 χ² of 125.96 raw and 84.83 Hartlap, to 2 × 10⁻¹⁶.
- **C2:** K1 equals CFG61's committed K1, and the June g_bar edges equal CFG61's EDGES exactly.
- **C3, the covariance-calibration null.** Take 200 random halvings of the 50 patches, and score the early class in half A minus half B, with its own jackknife covariance.
  - The mean χ² is 6.73 (median 5.97), against an expected 7.
  - 0.5% of the nulls reach p < 0.0027. So the jackknife covariance is not underestimating the variance of a difference.
- **MUTATE.** In each patch, the classes are swapped with probability ½; 27 of 50 patches were swapped.
  - B's zero model falls to 5.67/7 (p = 0.58), so H1 fails as required.
  - ΛCDM goes to 38.2/7, because its predicted split is no longer in the data.

## Caveats

- **This is the repo's own re-measurement, not Brouwer's released sample.** It uses its own isolation window and a colour cut at u−r = 2.0 (the LePhare valley) rather than GAaP 2.5, with 181,477 lenses against 259,383. Its profiles were validated against the released ones in June (early 0.4σ, late 1.3σ; `real_research/reviews/lensing_rar/agentK_remeasure_errors.md`).
- **The two stacks weight lenses differently.** The ΛCDM model difference is CFG67's, built lens by lens from the same lenses with CFG61's class weighting. That approximates the measurement's source-pair weighting.
- **A constant −1.5% calibration offset** against the released convention cancels in the difference χ² but not against the ΛCDM prediction. It is far below the errors.
- **Fewer patches.** With 25 merged patches (a noisier covariance and a larger Hartlap penalty), B's law is at 3.2σ.

## Disclosures

Before the criteria were frozen, the June all-15-bin numbers were printed (126.0/15 raw, 84.8 Hartlap), together with the per-bin difference and the diagonal jackknife errors. No K1 full-covariance χ², ΛCDM comparison or null had been computed. The frozen thresholds are standard: p < 0.0027 for H1, p > 0.01 for H2, and 7 ± 30% for C3.

## Data requirements (not in git)

- `real_research/data/lensing_rar/lr_esd_jackknife.npz` and `lr_esd_jackknife_analysis.npz` (June 2026, from `agentK_jackknife_stack.py` over the KiDS-1000 SOM-gold catalogue on disk).
- `brouwer2021_rar/Fig-8_*` (for R4).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.


## Correction at adoption (appended 2026-09-29)

- Read "every colour-blind dark mass" or "any colour-blind model" above as **"any model whose predicted early-minus-late difference at fixed g_bar is negligible"**. It is not every colour-blind model: CFG67's colour-blind Moster halo, whose halo mass depends on M* only, fits the split at 6.9/7.


## Notes after the independent re-run (appended 2026-09-29; no result changed)

- LEDGER_VERIFICATION Part 5 (84910a506, at HEAD 4fa9f54e3) re-ran both modes; both reproduce. The data it needs are listed above (`lr_esd_jackknife*.npz` and `brouwer2021_rar/`).
