# CFG110 — does the KiDS lensing signal at fixed g_bar depend on lens mass within a class? FROZEN CRITERIA

Written 2026-09-29, before any subset stack or number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

The lane is numbered 110 to stay clear of another session's sequential numbering (CFG97 was taken minutes before this file).

**Disclosure.** Before writing this file I read the June 2026 memo `real_research/reviews/lensing_rar/agentZ_second_variable.md`.
- It reports that in coarse g_bar super-bins, the early/late offset has no significant stellar-mass dependence within a class: early −0.044 dex (1.3σ), late −0.153 dex (1.9σ).
- The type offset stands at +0.194 dex at fixed M*, z and density.
- Its binning, statistic and covariance differ from this lane's. No K1-bin mass-split number or model prediction for these subsets has been computed.

## Why

In CFG61's seven 1-halo bins (K1, g_bar = 10^−12.9 to 10^−11.4 m/s², all ≪ a₀), the two models make different predictions:
- **B's law:** the ΔΣ at fixed g_bar does not depend on the lens mass (the deep-regime identity; CFG61's C4, to 4 × 10⁻⁶).
- **A standard halo:** the ΔΣ at fixed g_bar rises with mass, because halo mass grows steeply with M*.

Within a colour class, the high-mass minus low-mass difference is therefore a direct test of the law's core lensing scaling, in the same machinery as CFG61, CFG67 and CFG88. It is the mass analogue of the colour split, which B fails.

## Samples (declared once)

- **The lenses:** the June re-measurement's 181,477 isolated lenses (`lr_lenses.npz`).
- **Mass halves:** within each class, split at the class median of log10 M_gal (number median). That is 10.448 for late and 10.810 for early; a lens at the median goes to the upper half.
- **Redshift halves (reported rows only):** split at the class median of z (0.305 late, 0.310 early).
- **The stack:** one pass of the June estimator (`agentK_jackknife_stack.py`, verbatim per lens, as in CFG96), with sums kept per (subset, patch, class, bin) and the June patch labels.

## Statistic

- For class c: D_c = ESD(c, high) − ESD(c, low) on K1.
- The data vector is D = [D_late, D_early], 14 bins.
- C is its joint leave-one-patch-out covariance over 50 patches. The Hartlap factor is h = (50 − 14 − 2)/49 = 34/49.
- For each model, χ² = (D − D_model)ᵀ C⁻¹ (D − D_model) × h, with 14 degrees of freedom.

## Models, computed on the same subsets and not fitted

- **B:** the law's stack (CFG61's forward model, both footings), restricted to each subset's lenses.
- **Λ:** CFG67's colour-split ΛCDM (Mandelbaum halos, red for early and blue for late), restricted the same way.
- **Λ_m (reported):** CFG67's colour-blind Moster variant.

## Checks

- **C1 CONTROL:** the full-class re-stack reproduces the June per-patch sums (`lr_esd_jackknife.npz`) exactly (relative deviation ≤ 1e-9), with the June patch labels.
- **C2 CONTROL:** the mass halves and the redshift halves each partition each class exactly.
- **C3 CONTROL:** with the full-class mask, the model machinery reproduces CFG61's committed law stacks and CFG67's committed ΛCDM stacks (ml, me), canonical, to 1e-9 relative.
- **C4 CONTROL, the covariance calibration null:**
  - Take 200 random within-class halvings of the lenses (seed 110). For each, D_null = ESD(random half A) − ESD(half B) per class, on K1 (14 bins).
  - Each has its own jackknife covariance and the Hartlap factor.
  - The mean χ²_null must lie in [9.8, 18.2], i.e. 14 ± 30%.
- **H1 [HEADLINE]:** B's law is consistent with the within-class mass dependence: p > 0.01 on both footings.
- **H2:** CFG67's colour-split ΛCDM is consistent with it: p > 0.01.

## Reported rows

- **R0, the power of the test:** Δχ²_pred = (D_Λ − D_B)ᵀ C⁻¹ (D_Λ − D_B) × h. It needs only the covariance, and it is printed before any data comparison.
- **R1:** the per-class χ² (7 bins) for B, Λ and Λ_m.
- **R2:** the mass-split amplitude per class. This is the lens-weighted mean over K1 of log10[ESD(high)/ESD(low)], in dex, with a jackknife σ, for the data and each model.
- **R3:** Λ_m (colour-blind Moster) on the 14 bins.
- **R4, the redshift split (the photo-z check):** the data difference high-z minus low-z per class on K1, with its jackknife covariance, and each model's prediction for the same subsets. The law's prediction is not zero here: the edge and the lens weighting depend on z.

## MUTATE

MUTATE=1 injects ΛCDM's predicted mass dependence into the data. In each class, the high-mass half's wgE sums are multiplied per bin by the ratio [ESD_Λ(high)/ESD_Λ(low)] / [ESD_B(high)/ESD_B(low)] (canonical), so the data carry ΛCDM's hi/lo contrast relative to B's.
- H1 must fail, and the script must exit 1.
- If H1 does not fail, the test cannot see ΛCDM's predicted mass dependence, and it is declared NON-DISCRIMINATING whatever the main run shows.
- If the main run already fails H1, the MUTATE is uninformative for the headline; the README says so.

## Readings (declared)

- **H1 PASS, H2 FAIL, and R0 ≥ 9:** the data follow B's mass-independence and reject ΛCDM's mass dependence. That is **a ΛCDM-specific failure in shared machinery, the first found**. It sits beside the colour split, a B-specific failure in the same data.
- **H1 FAIL and H2 PASS:** the lensing signal at fixed g_bar rises with mass as ΛCDM predicts. That is **a second B-specific failure.**
- **Both pass:** NON-DISCRIMINATING if R0 < 9; otherwise both models are acceptable.
- **Both fail:** neither model describes the within-class mass dependence.
- **Caveats.** The model stacks weight lenses by class and M_gal, not by source pairs; the absolute profiles of both models fail in this machinery (CFG67 H3); the difference statistic cancels part of that.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
