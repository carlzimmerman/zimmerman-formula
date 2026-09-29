# CFG96 — do satellites drive the KiDS early/late split? FROZEN CRITERIA

Written 2026-09-29, before any isolation flag, stack or number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

The KiDS early/late split in the seven 1-halo bins (CFG61's K1) is candidate B's one failure specific to B in shared machinery:
- it survives a data-driven covariance (CFG88: 4.4σ);
- it survives B's own stellar-mass calibration (CFG95: 2.8σ released, 3.6σ re-measured).

Its main open systematic is **satellites among the "isolated" lenses**.
- A satellite's lensing signal at 44–286 kpc includes part of its host's halo. Red galaxies are more often satellites.
- That would raise the early class's ΔΣ for any colour-blind model.
- A stricter isolation window removes more of the likely satellites. If satellites drive the split, the split should shrink.

## Data and samples (declared once)

- **The base sample** is the June 2026 re-measurement's 181,477 isolated lenses (`lr_lenses.npz`). A lens is isolated if no neighbour in the KiDS bright sample with M* > 0.1 M*_lens lies within 3 Mpc transverse with |Δχ| < 10 Mpc (photo-z comoving distance).
- **The stricter samples** use the same rule with |Δχ| < 20 Mpc (headline) and < 30 Mpc (reported). They are subsets of the base by construction.
- **The isolation flags** are recomputed with the code of `real_research/reviews/lensing_rar/lr_esd_remeasure.py` (`stage_lens`, v4, including the +0.15 dex fluxscale), vectorised but logically unchanged.
- **The stack** is `agentK_jackknife_stack.py`'s estimator, re-run in one pass over the base lenses, with sums accumulated separately for each window.
  - The 50 sky patches are assigned once, on the base sample, with `assign_patches`, and kept for every subset.
  - The sources are the 21.3 M KiDS-1000 SOM-gold sources on disk.
- **Git-ignored intermediate files** go in `real_research/data/lensing_rar/cfg96_*.npz`.

## Statistic

The statistic is CFG88's, applied per window W:
- D_W is the early-minus-late ESD difference on K1.
- C_W is its 7 × 7 leave-one-patch-out covariance.
- The χ² of the colour-blind zero model is D_Wᵀ C_W⁻¹ D_W × 41/49 (Hartlap).
- The amplitude relative to the base is A_W = (D_10ᵀ C_10⁻¹ D_W) / (D_10ᵀ C_10⁻¹ D_10).
- σ_A comes from a joint leave-one-patch-out jackknife: A_W is recomputed with both D_W and D_10 rebuilt without each patch.

## Checks

- **C1 CONTROL:** the recomputed Δχ = 10 isolated set reproduces `lr_lenses.npz` exactly: the same 181,477 lenses in the same order, with identical ra, dec, z, M_gal and class.
- **C2 CONTROL:** the Δχ = 10 re-stack reproduces the June per-patch sums (`lr_esd_jackknife.npz`: wgE, W, NN) to 1e-9 relative, and the patch labels exactly.
- **C3 CONTROL:** the samples are nested, Δχ 30 ⊂ 20 ⊂ 10, with every count printed.
- **H1 [HEADLINE; MUTATE must fail]:** at |Δχ| < 20 Mpc the 1-halo split persists. Both conditions must hold:
  - the colour-blind zero model is rejected on K1 at p < 0.0027;
  - A_20 is within 2σ_A of 1.

## Reported rows

- **R1:** the same numbers at |Δχ| < 30 Mpc.
- **R2:** the class composition per window: the number of lenses, the early fraction, and the median log M_gal per class.
- **R3:** the per-bin ratio D_W / D_10 on K1.
- **R4:** the zero-model χ² on all 15 bins per window.

## MUTATE

MUTATE=1: the early and late labels are swapped in the stricter samples' sums before scoring. D_W changes sign, so A_W ≈ −1; H1 must fail, and the script must exit 1.

## Readings (declared)

- **H1 PASS:** removing the lenses that have a qualifying neighbour within a line-of-sight window twice as wide does not change the split. Satellites, as removed by this isolation, do not drive it.
- **H1 FAIL because A_20 is more than 2σ below 1:** the split shrinks under stricter isolation, so satellite contamination contributes to it. For every colour-blind model this is a systematic escape, and it needs a quantified satellite model before the split can count against B.
- **H1 FAIL because p ≥ 0.0027 while A_20 is consistent with 1:** the stricter sample has lost the power to decide. Non-diagnostic.

## Caveats (declared)

- The Δχ window is a photo-z proxy. A wider window removes more true satellites, but it also removes field lenses by projection.
- The Δχ = 10 window was calibrated to Brouwer's isolated count.
- A jackknife cannot see calibration systematics common to all patches.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
