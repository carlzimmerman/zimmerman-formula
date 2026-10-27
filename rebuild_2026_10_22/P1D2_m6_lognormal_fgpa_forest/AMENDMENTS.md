# P1D2_m6_lognormal_fgpa_forest: AMENDMENTS

## A1 (committed alone, before any script run): variance reduction in the patch layer and the MC-variance step

1. **Patch count.** At μ = 1 the 4000 Mpc/h skewer set holds only λL ≈ 80 (canonical) / 55 (alt) chords. Poisson noise
   in that count would move the M6 signal by about 10 %. The implementation therefore:
   - fixes N₁ = round(λ₁ L) chords at μ = 1;
   - draws their positions uniformly (seed 1) and their u (chord length) uniformly (seed 1);
   - assigns **stratified tags** (i + 0.5)/N₁ in a random permutation, and keeps a chord when tag ≤ μ;
   - for μ > 1, adds round((μ − 1) λ₁ L) extra chords from seed 2.

   This is the patch analogue of the fixed-amplitude Gaussian modes. S0e (covered fraction = f_V within 3 Poisson σ) is
   unchanged.
2. **Model MC variance (§3).** It is estimated once per z at the μ = 0 best fit of a first pass. The first pass uses the
   data covariance only. The variance is then added to the covariance diagonal, and every fit, Asimov and scan is
   rerun with the augmented covariance. Both passes are reported.
3. **μ scan.** The grid is μ ∈ {0, 0.25, 0.5, 1, 2, 4, 8}. It is followed by a bounded refinement around the grid
   minimum, and by root-finding for μ_95. Thresholds are unchanged.
4. **Shared null.** μ = 0 is identical across footings (no patches), so the null fit is computed once per configuration
   and shared. This is exact.

Gates, thresholds, model physics and variants are unchanged.

## A2 (committed before the restart): memory cap and warm starts (code only)

The first launch reached 0.97 GB RSS during the primary configuration's K3/K4 planted scans and was stopped with
SIGTERM. The checkpoint held no completed configuration. Its primary-config lines remain at the top of
`p1d2_m6_fgpa.out`, which is opened in append mode.

- **Fixes, all code only:**
  - Patch cache capped at 8 entries and g-field cache at 16.
  - Mocks freed after each configuration.
  - Planted (K3/K4) μ scans warm-start from the null best fit, as the data scans already do.
- **Unchanged:** model, gates, thresholds and variants. The restart recomputes the primary from scratch.
