# CFG255 — FROZEN CRITERIA: does the KiDS-1000 lensing signal at fixed g_bar change with lens redshift as a₀ ∝ H(z) predicts? (the orchestrator's lane, 2026-09-30)

**This file is committed before any CFG255 script exists and before any redshift-split lensing number has been read by the author of this lane.**

**Disclosures:**
- CFG110 (committed earlier) contains a reported row, R4: a redshift-halves split as a "photo-z check", scored against zero, B and ΛCDM, never against the rival. Its numbers were NOT read before this file. They exist in the record and other sessions may have seen them.
- The KiDS colour, mass and nulls results of CFG61, CFG110, CFG115 and CFG116 are known to the author.

Other standing terms: κ = ½ is FITTED. ΛCDM has no a₀; its line is CFG67's stack, reported only. Nothing is fetched.

## Data and estimator (all on disk, gitignored; nothing new fetched)
- **Per-lens sums:** `real_research/data/lensing_rar/cfg110_perlens.npz`, from CFG110's one pass of the June KiDS-1000 estimator over 181,477 KiDS-bright lenses.
- **Lenses:** `lr_lenses.npz` (photo-z, M_gal, colour class).
- **Patches:** the 50 June jackknife patches (`lr_esd_jackknife.npz`).
- **Signal bins:** ESD = Σ wgE / Σ W in each g_bar bin; K1 = bins 8–14 (deep regime), per class: 14 bins.

## The split (one design, fixed here)
- Within each colour class, compare the HIGH-z third (z ≥ the class 2/3 quantile) with the LOW-z third (z < the class 1/3 quantile); the middle third is unused. D = ESD(high) − ESD(low) on K1, per class: 14 numbers.
- The lens photo-z range is 0.10–0.50 and the median is about 0.31; the quantiles are computed by the script from the photo-z column, which is not a lensing number.
- Thirds are chosen over halves for the larger redshift lever. This choice is made here, before any power number exists.

## Models (no fit)
- **FLAT, the framework (both footings):** CFG61's law stack on each subset's lenses (the CFG110 machinery).
- **RIVAL, a₀ ∝ H(z):** the same law stack with every profile rebuilt at a₀ × E(z_grid), E = √(0.3(1+z)³ + 0.7), anchored so that a₀(0) is the footing value. The turnaround truncation uses the same a₀(z).
- **ΛCDM (reported):** CFG67's colour-split stack on the subsets. Its tables have no redshift dependence beyond the lens mass distribution, and this limitation is stated in the output.

## Stage A — the pre-flight (printed and committed before stage B is run)
Computed from the jackknife covariance of D alone; D itself is never printed in stage A.
- **A1, power:** Δχ²_pred = (D_RIVAL − D_FLAT)ᵀ C⁻¹ (D_RIVAL − D_FLAT) × Hartlap (50 patches, p = 14), per footing.
- **A2, amplitude:** ΔA_model = A_RIVAL − A_FLAT, where A = log10 of the ratio of pair-weighted sums over K1 (CFG110's R2b form), per class, then combined inverse-variance. σ_A comes from the jackknife.
- **A3, the systematic budget, declared, not measured.** A stellar-mass calibration drift δ (dex) between the two thirds shifts the g_bar binning. In the deep regime it moves A by δ/2, exactly mimicking an a₀ change, so the photometric M* drift with z cannot be separated from an a₀ drift by this statistic.
  - Declared scenarios: δ = 0.02 dex and δ = 0.05 dex. Neither is sourced; they are scenarios.
- **A4, the decision:**
  - POSSIBLE_STAT if A1 ≥ 9 on both footings.
  - POSSIBLE_SYS(δ) if |ΔA_model| ≥ 2√(σ_A² + (δ/2)²) on both footings.
  - Stage B attaches verdict words ("the rival is disfavoured / FLAT-consistent / the rival is favoured") ONLY at the δ scenarios where POSSIBLE_SYS holds. Otherwise stage B is descriptive.

## Stage B — the measurement (run only after stage A is committed)
- **B1:** χ² of D against FLAT, RIVAL, zero and ΛCDM (Hartlap, 14 dof), per footing for FLAT and RIVAL.
- **B2:** the amplitude A_data ± σ_A against A_FLAT, A_RIVAL and A_ΛCDM.
- **B3, the reading,** by A4's gate:
  - FLAT-consistent and RIVAL disfavoured: χ²_FLAT p > 0.01, χ²_RIVAL p < 0.01, and Δχ² ≥ 9.
  - The reverse reading is "the rival is favoured", with the same thresholds.
  - Anything else is "not separated".
  - The reading is never "the data favour the framework". A FLAT-consistent result is also scored against ΛCDM by the same rule.

## Controls
- **C1:** the per-lens sums, summed by (patch, class), reproduce the June per-patch sums to 1e-9 relative.
- **C2:** the thirds are disjoint, and each holds 1/3 of its class to within 1%.
- **C3:** with the full-class mask, the FLAT machinery reproduces CFG61's committed law stacks to 1e-9.
- **C4:** the RIVAL machinery with E(z) ≡ 1 reproduces FLAT to 1e-9.
- **C5:** covariance calibration. The mean Hartlap χ² of 200 random within-class one-third-versus-one-third draws (seed 255) on K1 lies in [9.8, 18.2].
- **MUTATE=1:** the high-z third's wgE is multiplied per K1 bin by the model ratio [RIVAL(high)/RIVAL(low)] / [FLAT(high)/FLAT(low)] (canonical). Stage B must then read "the rival is favoured" or at least reject FLAT. If it does not, the test is declared NON-DISCRIMINATING whatever stage A said.
- MUTATE outputs go to separate files.

## What this lane cannot say
- It cannot separate an a₀ drift from a stellar-mass calibration drift between z ≈ 0.2 and 0.4 (A3).
- It tests the rival only over the lever E(0.43)/E(0.18) ≈ 1.16.
- A null here does not test a₀ at z ≈ 2.5.
