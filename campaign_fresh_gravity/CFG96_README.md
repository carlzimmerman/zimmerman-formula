# CFG96 — do satellites drive the KiDS early/late split?

- **Criteria:** frozen in `CFG96_FROZEN_CRITERIA.md` (cb2876df0), before any flag, stack or number.
- **Scripts:**
  - `CFG96_stage_stack.py`: the isolation flags and one stacking pass; 103 s; log in `CFG96_stage_stack.out`.
  - `CFG96_kids_split_isolation.py`: the scoring; under 1 s.
- **Runs:**
  - The main run passes 8 of 8 and exits 0.
  - The MUTATE run (labels swapped) fails H1 and exits 1.
  - The two runs fail different checks, so the control is informative.

## Bottom line

**Satellites, as removed by a stricter isolation cut, do not drive the split.**

- **What was done.** We re-stacked the June KiDS-1000 re-measurement keeping only lenses with no qualifying neighbour within a line-of-sight window twice as wide: |Δχ| < 20 Mpc, which keeps 51% of the 181,477 lenses.
- **The split persists undiminished in the seven 1-halo bins.**
  - The colour-blind zero model (B's law, and every colour-blind dark mass) is still rejected at **32.0/7, p = 4.0 × 10⁻⁵ (4.1σ)**.
  - The split's amplitude relative to the base sample is **A₂₀ = 0.97 ± 0.19**.
- **An even stricter window.** At |Δχ| < 30 Mpc (32% of the lenses) the amplitude is 1.17 ± 0.27, and the significance falls with the sample size (2.7σ).
- **So the split is not driven by the satellites this isolation removes.** If satellites carried a large part of the early-type signal, removing the lenses with nearby neighbours would have shrunk it.

| isolation window | lenses | early fraction | 1-halo zero-model χ² / 7 | p | A (relative to base) |
|---|---|---|---|---|---|
| \|Δχ\| < 10 Mpc (June base) | 181,477 | 48.5% | 35.04 | 1.1 × 10⁻⁵ | 1 |
| **\|Δχ\| < 20 Mpc** | **93,020** | 48.0% | **32.02** | **4.0 × 10⁻⁵ (4.1σ)** | **0.97 ± 0.19** |
| \|Δχ\| < 30 Mpc | 57,265 | 46.4% | 19.12 | 7.8 × 10⁻³ (2.7σ) | 1.17 ± 0.27 |

**Outside the 1-halo range the signal does respond to isolation.** Over all 15 bins the zero-model χ² falls from 84.8 to 54.6 to 26.1 (/15). So the 2-halo and environment signal shrinks as neighbours are removed. The 1-halo split that carries B's failure does not.

## Controls

- **C1:** the vectorised isolation recomputation reproduces the June lens list (`lr_lenses.npz`) exactly: 181,477 lenses, the same order and every column.
- **C2:** the |Δχ| < 10 re-stack reproduces the June per-patch sums exactly (maximum relative deviation 0.0), with the June patch labels. The whole re-run is therefore validated.
- **C3:** the windows are nested, 30 within 20 within 10.
- **MUTATE:** swapping the classes in the stricter windows gives A₂₀ = −0.97, so H1 fails as required.

## Caveats

- **The line-of-sight window is a photo-z proxy.** Photo-z errors are tens of Mpc in χ, so each window catches only part of the true satellites. A wider window catches more of them, and it also removes field lenses by projection. "Satellites as removed by this isolation" is the precise claim; a spectroscopic isolation would be cleaner.
- **The per-bin ratios scatter.** At |Δχ| < 20 they range from 0.44 to 2.66, within the errors of the smaller sample. The amplitude A is the declared summary.
- **Other systematics remain open.** A jackknife cannot see calibration systematics common to all patches (shear m, photo-z), and colour-class contamination is not tested here.

## Standing of the KiDS split after CFG88, CFG95 and CFG96

It remains candidate B's one failure specific to B in shared machinery, and it has now survived three stress tests:
- a data-driven covariance (4.4σ; CFG88);
- B's own stellar-mass calibration (2.8σ released, 3.6σ re-measured; CFG95);
- a twice-stricter isolation (4.1σ, amplitude unchanged; CFG96).

It is still a failure that every colour-blind dark mass shares (CFG77).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
