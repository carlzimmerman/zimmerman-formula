# CFG115 — is the KiDS colour dependence at fixed g_bar a step or a gradient? FROZEN CRITERIA

Written 2026-09-29, before any colour-binned lensing number. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. The orchestrator approved the lane and named the number.

## Why

At fixed g_bar, the KiDS lensing signal of isolated lenses depends on galaxy type (CFG61, CFG88, CFG95, CFG96). Within a type it shows no detectable dependence on stellar mass (CFG110; power-limited, CFG100). B's law predicts no colour dependence at all.

The question here is the structure of the colour dependence:
- **A step at the red/blue valley** points to two populations: a morphology or class property (for example misclassified satellites, or halo assembly by class). The colour-split ΛCDM (Mandelbaum halos by class) builds in exactly such a step.
- **A gradient across colour** points to a continuous colour–halo or colour–(M/L) link.

## Data (on disk; nothing downloaded)

- **Per-lens sums:** `cfg110_perlens.npz`. CFG110's C1 showed they reproduce the June sums to 3 × 10⁻¹¹. Also `lr_lenses.npz`, and June's patch labels from `lr_esd_jackknife.npz`.
- **Per-lens colour:** u − r = MAG_ABS_u − MAG_ABS_r from `KiDS_DR4_brightsample_LePhare.fits`. It is row-aligned with `KiDS_DR4_brightsample.fits` (IDs equal), and each lens is matched by exact (RA, Dec).
  - A data join done before freezing (no lensing number) matched all 181,477 lenses exactly. u − r > 2.0 reproduces lr_lenses' early/late label for every lens.
  - This is the June lens stage's own colour (lr_esd_remeasure.py). It is not Brouwer's GAaP u − r, whose split is at 2.5: the systems differ in zeropoint and k-correction.
- **Machinery:** CFG110's script exec'd read-only up to its model-control banner, with MUTATE forced to 0 for that exec. From it: `esd_and_loo` (ESD = Σ wgE / Σ W / KG, leave-one-patch-out over 50 patches), K1 = bins 8–14, and the model stacks `law_stack` (CFG61) and `lcdm_stack` (CFG67).

## Colour bins (declared)

- **Six bins:** each class split at its own colour tertiles.
  - Late (u − r ≤ 2.0): L1 < 1.507 ≤ L2 < 1.749 ≤ L3.
  - Early: E1 < 2.228 ≤ E2 < 2.351 ≤ E3.
  - The edges are computed in the script as the 1/3 and 2/3 quantiles. The values above come from the data join.
- **Amplitude per bin:** A_c = log10[Σ_k w_k ESD_ck / Σ_k w_k ESD_all,k] over the K1 bins.
  - The weights w_k = Σ WW_k are the full sample's pair weights, the same for every colour bin. This removes the bias from colour bins having different g_bar mixes.
  - ESD_all is the full sample (both classes).
- **Covariance:** the leave-one-patch-out jackknife of the six amplitudes jointly, C = (N − 1)/N Σ (A_i − Ā)(A_i − Ā)ᵀ with N = 50. For a p-dimensional χ² the Hartlap factor is (N − p − 2)/(N − 1).

## Models for the six amplitudes

- **M0 (B's law):** A_c = 0. There is no colour dependence at fixed g_bar.
- **Step:** A_c = s_L for the late bins and s_E for the early bins (2 parameters).
- **Gradient:** A_c = α + β(ū_c − 2.0), with ū_c the bin's median u − r (2 parameters).
- **Step + slope:** A_c = s_class + β_w(ū_c − ū_class), a common within-class slope (3 parameters). It is nested on the step, so Δχ²(step − step+slope) with 1 dof is the within-class gradient test.

## Checks

- **C1 CONTROL:** all 181,477 lenses match the bright sample by exact position, and (u − r > 2.0) reproduces lr_lenses' `typ` for every lens.
- **C2 CONTROL:** the six bins partition the sample. Their summed per-lens K1 sums reproduce the full-sample and per-class sums exactly (relative 10⁻¹²).
- **C3 CONTROL (calibration):** 200 random partitions of each class into equal-count thirds, at random and not by colour. The mean Hartlap χ² of the within-class constancy test (4 dof) must fall within [2.5, 5.5].
- **R0 (POWER; printed before any colour-bin amplitude):**
  - The inputs are the covariance of the six amplitudes and the class-level amplitudes (the known CFG88 split, in this machinery; disclosed).
  - The quantity is the expected Δχ² of the within-class slope test (1 dof) if the truth were a pure linear gradient in u − r with the observed class difference: β_true = (s_E − s_L)/(ū_E − ū_L), with ū the class medians.
  - Declared: λ ≥ 9 means the test can tell a gradient of that size from a step.
- **H1 [HEADLINE; MUTATE must fail]:** the colour dependence is a step. Within each class the three amplitudes are consistent with a constant: Hartlap χ² with 4 dof has p > 0.05, and Δχ²(step − step+slope) < 4.

## Reported rows

- **R1:** M0 (B's law): χ² with 6 dof.
- **R2:** the fits: the step (s_L, s_E, s_E − s_L with its error), the gradient (α, β), step + slope (β_w with its error), their χ², and χ²(step) − χ²(gradient).
- **R3 (colour-noise-robust):** the outer-tertile contrasts, A(L1) − A(L2) and A(E3) − A(E2), with the tertiles next to the valley left out (2 dof χ² against zero).
  - Colour errors blur a true step near the boundary into an apparent gradient in L3 and E1.
  - A gradient that shows only through the boundary tertiles is consistent with a blurred step. One in the outer tertiles is not.
- **R4:** per bin: N, median u − r, median log M_gal, median z, and the seven-bin ESD profile.
- **R5, the models' predicted amplitudes** for the six bins, with the same amplitude definition on the model stacks:
  - B's law (`law_stack`, canonical);
  - the colour-split ΛCDM (`lcdm_stack`: red halos for early bins, blue for late);
  - the colour-blind Moster (`lcdm_stack`, "moster").
  - For each, χ² against the data amplitudes.
  - The ΛCDM comparators exist only for the two classes. Their within-class differences come only through each bin's lens masses, so this comparison is descriptive.

## MUTATE

MUTATE=1 injects a within-class gradient. Every lens's wgE in the K1 bins is multiplied by 10^(β_inj (u − r − ū_class)), with β_inj = (s_E − s_L)/(ū_E − ū_L) computed in the same run from the unmodified data. This is a gradient of the class-difference slope, applied inside the classes. H1 must fail and the script must exit 1.

- **If R0 < 9,** the injection may not be detected. The MUTATE then "fails to fail", which is itself the finding: the test cannot see a gradient of that size. The reading is then non-discriminating.
- **If the main run's H1 fails too,** the control is uninformative for H1.

## Readings (declared)

- **R0 ≥ 9 and H1 PASS:** a step at the valley. A gradient of the class-difference size is excluded; within-class colour does not matter at this power.
- **R0 ≥ 9 and Δχ²(step − step+slope) ≥ 9:** a gradient. R3 says whether it survives with the boundary tertiles left out, and whether it could be a blurred step.
- **Δχ² between 4 and 9:** leaning towards a gradient, not established.
- **R0 < 9:** non-discriminating between a step and a gradient.
- **Caveats (declared):**
  - LePhare colours are not Brouwer's.
  - Photometric colour noise blurs a step.
  - Colour correlates with mass within a class (R4). CFG110 found no within-class mass dependence at this power.
  - The jackknife has no photo-z, intrinsic-alignment or satellite terms (CFG100).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
