# CFG115 — is the KiDS colour dependence at fixed g_bar a step or a gradient?

- **Criteria:** frozen in `CFG115_FROZEN_CRITERIA.md` (e416f3bea), before any colour-binned lensing number.
- **Script:** `CFG115_kids_colour_gradient.py`, about 3 minutes. It execs CFG110's machinery read-only.
- **Runs:**
  - The main run passes 10 of 11 and exits 1. The one failure is H1: the sharp step is rejected.
  - The MUTATE run (a within-class gradient injected) also fails H1 and exits 1.
  - As the frozen file said in advance, the control is therefore uninformative for H1. It does show that an injected slope is recovered (below).

## Bottom line

**By the frozen map: NON-DISCRIMINATING between a step and a gradient.** The power row gives λ = 4.8, below the declared 9, for a gradient of the class-difference size.

**What the data show at fixed g_bar in the 1-halo bins:**
- **There is no sharp step at the red/blue valley.** The two tertiles on either side of u − r = 2.0 have identical amplitudes: L3 −0.049 ± 0.039 and E1 −0.049 ± 0.034.
  - A step that is constant within each class is rejected: **χ² 18.1/4, p = 0.001** (H1 fails).
  - A linear gradient in colour fits: 6.3/4 (p 0.18), with slope +0.34 ± 0.06 dex/mag.
  - A within-class slope is seen at +0.44 ± 0.12 dex/mag (Δχ² 12.8).
- **But the within-class variation sits in the boundary tertiles.** The outer-tertile contrasts, A(L1) − A(L2) = +0.10 ± 0.10 and A(E3) − A(E2) = +0.07 ± 0.05, are consistent with zero (χ² 3.25/2, p 0.20).
  - Colour errors blurring a true step would also make the two boundary tertiles equal.
  - So "an intrinsic gradient" and "a step blurred by colour noise" both fit, and this machinery cannot tell them apart.
- **B's law (no colour dependence) is rejected in this view too:** 36.3/5 with a free offset (R6). The frozen R1's 305/6 is a normalisation artefact (see Disclosures).

| bin | u − r range | N | median u − r | median log M_gal | median z | A_c (dex) ± jackknife |
|---|---|---|---|---|---|---|
| L1 | < 1.507 | 31,030 | 1.344 | 10.01 | 0.270 | −0.165 ± 0.077 |
| L2 | 1.507–1.749 | 31,222 | 1.632 | 10.48 | 0.318 | −0.267 ± 0.077 |
| L3 | 1.749–2.0 | 31,146 | 1.870 | 10.70 | 0.324 | −0.049 ± 0.039 |
| E1 | 2.0–2.228 | 29,313 | 2.128 | 10.73 | 0.293 | −0.049 ± 0.034 |
| E2 | 2.228–2.351 | 29,135 | 2.297 | 10.77 | 0.299 | +0.050 ± 0.031 |
| E3 | > 2.351 | 29,631 | 2.401 | 10.90 | 0.332 | +0.123 ± 0.024 |

A_c is the lensing amplitude over K1 relative to the full sample, with common weights.

**The models** are descriptive only: none of them models colour errors, and the ΛCDM comparators exist only for the two classes. The χ² below each include a free offset (R6), with 5 dof.

| model | predicted pattern | χ² |
|---|---|---|
| B's law | flat | 36.2 (p 9 × 10⁻⁷) |
| colour-split ΛCDM (Mandelbaum halos by class) | a sharp 0.22-dex jump between L3 and E1, which the data do not show | 21.1 (p 8 × 10⁻⁴) |
| colour-blind Moster | a smooth, mass-driven rise | 12.2 (p 0.03) |

## Controls

- **C1:** all 181,477 lenses match the KiDS bright sample by exact position, and u − r > 2.0 reproduces the June early/late label for every lens.
- **C2:** the six bins partition the sample, and their sums reproduce the full-sample and class sums to 3 × 10⁻¹⁶.
- **C3:** 200 random equal-count thirds per class give a mean χ² of 3.76 for 4 dof (fraction p < 0.05: 0.035), so the covariance is calibrated.
- **MUTATE:** it injects a within-class slope of β_true = 0.270 dex/mag, the class difference over the class colour difference. The run then measures 0.739 ± 0.123 against the main run's 0.441, so it recovers 0.298 against 0.270 injected.

## Disclosures

- **R6 was added after the first run** as a reported row. Every other line of both logs is unchanged apart from timing.
- **Why R6 was needed:** the frozen amplitude definition divides by the jackknifed full-sample denominator. That leaves a near-null covariance direction, a normalisation constraint: the condition number is 3200 and the smallest eigenvalue 2.2 × 10⁻⁶.
  - The frozen rows with no free offset are inflated by the curvature of that constraint: R1 (B's null, 305/6) and R5 (the model χ² 304, 77.6 and 29.2).
  - Against a fixed, non-jackknifed reference the covariance is well-conditioned (condition number 10.8). Every model with a free common offset then gets **exactly** the frozen fit χ²: step 18.11, gradient 6.29, step + slope 5.34, Δχ² 12.77. So H1 and R2 stand as computed.
  - The zero-offset rows become B 36.2/5, colour-split ΛCDM 21.1/5 and Moster 12.2/5.
- **An exploratory pseudo-inverse** that simply dropped the near-null direction gave Δχ² 0.19. It is not used, because it discards data: the direction is set by the amplitudes themselves. The well-conditioned fixed-reference form reproduces the full-inverse numbers exactly.

## Caveats

- **The colour system differs.** The colours are the June lens stage's LePhare rest-frame u − r, split at 2.0, not Brouwer's GAaP colours (split at 2.5).
- **Colour noise blurs a step.** Its size in this catalogue is not modelled.
- **Colour tracks mass within a class.** Median log M_gal runs from 10.0 (L1) to 10.9 (E3). CFG110 found no within-class mass dependence at its power, and CFG100 notes that power is limited.
- **The late-class amplitudes are noisy** (± 0.08).
- **Missing covariance terms:** the jackknife has no photo-z, intrinsic-alignment or satellite terms (CFG100).

## Reading

- **The shape of the dependence:** the KiDS colour dependence at fixed g_bar is not a sharp step at the red/blue valley. The signal rises smoothly through the boundary.
- **What remains open:** whether that is an intrinsic gradient or a colour-noise-blurred step.
- **For B:** the colour (type) dependence remains its one specific failure. This lane changes its structure, not its existence.
- **For ΛCDM:** a colour-split halo model needs either colour-noise blurring or a continuous colour–halo relation to match the boundary bins.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
