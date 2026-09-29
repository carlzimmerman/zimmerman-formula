# CFG88 — does the KiDS early/late split survive a data-driven covariance? FROZEN CRITERIA

Written 2026-09-29, before any 1-halo (K1) number, ΛCDM comparison, null test or MUTATE was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

**Disclosure.** Before writing this file I printed the June 2026 all-15-bin analysis:
- χ² 126.0/15 raw and 84.8/15 Hartlap-corrected;
- its per-bin early-minus-late difference and the diagonal jackknife errors, from `lr_esd_jackknife_analysis.npz`.

No K1 full-covariance χ², ΛCDM comparison, null test or MUTATE had been computed.

## Why

The KiDS early/late lensing split is candidate B's one failure specific to B in shared machinery (CFG61, CFG67). CFG77 (a736715f8) showed it is fragile:
- the law's χ² is the zero-model χ², so every colour-blind dark mass fails it equally;
- the released covariance is near-diagonal and carries no systematic terms;
- errors × 1.5 give p = 0.086.

A data-driven covariance addresses the second point, as far as patch-level variation goes.

## Data (on disk, git-ignored; built in June 2026)

- **The re-measurement:** `real_research/reviews/lensing_rar/lr_esd_remeasure.py` (v4) and `agentK_jackknife_stack.py`. They cover 181,477 isolated lenses (`lr_lenses.npz`, the same lenses and classes CFG61/CFG67 used as proxies), 21.3 M KiDS-1000 SOM-gold sources, and 50 sky patches.
- **The sums:** the estimator sums per (patch, class, g_bar bin) are in `real_research/data/lensing_rar/lr_esd_jackknife.npz`. The June analysis is in `lr_esd_jackknife_analysis.npz`.
- **The ESD:** ESD = Σ wgE / Σ W in M☉/pc². Class 0 is late and class 1 is early (u−r > 2.0 at the LePhare valley). The 15 g_bar bins have the edges of CFG61's `EDGES`.

## Models (declared once)

- **L, B's law (colour-blind):** a predicted early-minus-late difference D = 0. CFG61's C4 and CFG77 put |D_L|/σ below 3.3 × 10⁻³, and D = 0 is every colour-blind model's prediction.
- **Λ, CFG67's colour-split ΛCDM:**
  - D_Λ = me − ml from `CFG67_lcdm_control_kids_split_results.json`. That model was built lens by lens from the same `lr_lenses`, with Mandelbaum's colour-split halo masses.
  - The amplitude is fixed at 1, with no refit.
  - The weightings differ: CFG61's model stack weights by lens class and not by source pairs, as the measurement does. This is accepted, as in CFG61/CFG67.

## Statistic

- **Bins:** K1 = CFG61's seven 1-halo bins [8, 9, 10, 11, 12, 13, 14].
- **Covariance:** C = the 7 × 7 K1 block of the leave-one-patch-out covariance of the difference, Cd = (N−1)/N Σ (D_(p) − D̄)(D_(p) − D̄)ᵀ with N = 50.
- **χ² = Dᵀ C⁻¹ D × h**, where h = (N − p − 2)/(N − 1) = 41/49 is the Hartlap factor for p = 7.
- **The p-value** comes from χ² with 7 degrees of freedom.
- **Why a common calibration does not matter:** a common multiplicative calibration, such as the re-measurement's constant −1.5% against the released convention, scales both D and C and cancels in the χ² of the difference. It does not cancel against D_Λ; the 1.5% is reported.

## Checks

- **C1 CONTROL:** the June analysis is reproduced from the per-patch sums: the ESD, the difference, and the all-15-bin χ² raw (125.9599) and Hartlap-corrected (84.8301), to 10⁻⁹ relative.
- **C2 CONTROL:** K1 equals CFG61's committed K1, and the June bin edges equal CFG61's `EDGES` to 10⁻¹².
- **C3 CONTROL, covariance calibration by a null:**
  - Draw 200 random halvings of the 50 patches (seed 88).
  - For each halving, D_null = ESD_early(half A) − ESD_early(half B) on K1, with its own leave-one-patch-out covariance and the same Hartlap factor.
  - The mean χ²_null over the halvings must lie in [4.9, 9.1], i.e. 7 ± 30%. If it does not, the jackknife covariance is miscalibrated and H1/H2 are non-diagnostic.
- **H1 [HEADLINE; MUTATE must fail]:** the colour-blind zero model is rejected on K1 under the jackknife covariance: the Hartlap-corrected χ² has p < 0.0027.
- **H2:** CFG67's ΛCDM colour-split difference is consistent on K1 under the jackknife covariance: p > 0.01.

## Reported rows

- **R1:** raw (no Hartlap) and diagonal-only χ² for L and Λ on K1.
- **R2:** 25 merged patches (June's pairing; Hartlap with N = 25, p = 7), for L and Λ.
- **R3:** the error-inflation factor that brings L's Hartlap χ² on K1 to p = 0.0027, and to p = 0.05.
- **R4:** jackknife σ against Brouwer+2021's released analytic σ in K1, per bin, as a plain ratio. The samples differ: 181,477 against 259,383 lenses, a colour cut at 2.0 against 2.5, and a different isolation.
- **R5:** all 15 bins, the June number, for L and Λ.
- **R6:** Λ with its best-fit amplitude on K1 under the jackknife covariance.
- **R7:** K1 with each bin dropped in turn (χ²/6), for L.

## MUTATE

MUTATE=1: in each patch, the early and late class sums are swapped with probability ½ (seed 88) before stacking. This destroys the class split and keeps the patch noise, so H1 must fail and the script must exit 1.

## Readings (declared)

- **H1 PASS with C3 PASS:** the rejection of every colour-blind dark mass by the 1-halo split survives a covariance that includes cosmic variance and patch-level systematics.
  - CFG77's fragility point is answered for those terms only.
  - Calibration systematics common to all patches (shear m-bias, photo-z), colour-class contamination and satellites are not seen by a jackknife and stay open.
- **H1 FAIL with C3 PASS:** the split is not robust under the data-driven covariance, and B's one specific failure is downgraded.
- **C3 FAIL:** the covariance is miscalibrated, so H1 and H2 are non-diagnostic.
- **H2** says whether ΛCDM's colour-split halos stay consistent with the re-measured split under the same covariance.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
