# FRZ3 RESULT: the forest row at flux level

**NO VERDICT / NO VERDICT (canonical / alt), as frozen.** Known answer (b) fails: the painted fields carry only about half
of FRZ1's matter-level redistribution at k 3 to 5 h/Mpc, so the painting is not validated. The primary flux numbers are
reported, but they grade nothing: **Delta chi^2(flux) 4.71 / 2.58** (gate 4), against **4720 / 4120** from the record's
matter-level projection of the same painted fields. **Softening factor 0.0010 / 0.0006.** If (b) had passed, the readings
would have been FAILS (FRAGILE) on canonical and HOLDS (FRAGILE) on alt; brackets cross the gate on both footings.

TEST lane. Criteria e56c67ae91; amendments A1 1483ae75ef (density floor) and A2 50dcbd956e (A1's claim corrected; code fix
before the first part). Footings never pooled. Cold dark energy is a gravitating field component; no particle is added.
Nothing here says the data favour the framework. A HOLDS reading would not be a pass, and it would need an independent re-grade.

## What came out
- **The flux hardly sees rule 5.** The matter ratio falls (painted R at z 3, k 3 / 5: 0.928 / 0.798), and the 1D gas ratio
  falls by 4 to 16 %. The flux ratio instead RISES slightly, by +0.1 to +0.9 %. The mass that rule 5 takes out of halo
  centres sits in saturated pixels in both fields. The mean-flux retuning absorbs most of the rest.
- **Saturation is the step that matters.** Mutation M1 keeps tau but removes the exponential, and the anchor-bin Delta chi^2
  goes from 1.49 to 975 (canonical; matter level 890) and from 0.90 to 1109 (alt; matter level 767). Pressure smoothing
  alone (gas level, 538 / 569) takes off a factor of about 9. Saturation and mean-flux matching take off a further 100 to 200.
- **Post hoc reading (not graded, not in the criteria).** Doubling the painted difference roughly restores FRZ1's matter
  amplitude: 2 x (1 - R_paint) at z 3 is 0.144 / 0.40 at k 3 / 5, against FRZ1's 0.155 / 0.335. That raises the anchor
  Delta chi^2 by 3.8x (canonical) and 3.7x (alt). Scaled to 12 bins this gives about 18 / 10: both over the gate, and about
  500x below FRZ1's 9916 / 9009.

## Table (seed mean of 4; R_F +- seed scatter; Delta chi^2 per bin on its own covariance block)

| z | canonical R_F at k_par 0.005 / 0.01 / 0.02 / 0.03 s/km | can flux / matter (painted) | alt R_F at 0.005 / 0.01 / 0.02 / 0.03 | alt flux / matter |
|---|---|---|---|---|
| 2.2 | 1.0087 / 1.0092 / 1.0072 / - (+-0.002) | 1.16 / 231 | 1.0071 / 1.0081 / 1.0086 / - | 0.77 / 231 |
| 2.6 | 1.0051 / 1.0049 / 1.0035 / - | 0.66 / 303 | 1.0039 / 1.0039 / 1.0038 / - | 0.38 / 275 |
| 3.0 | 1.0034 / 1.0024 / 1.0016 / 1.0036 (+-0.0007) | 0.33 / 617 | 1.0022 / 1.0018 / 1.0025 / 1.0060 | 0.13 / 499 |
| 3.4 | 1.0025 / 1.0015 / 1.0011 / 1.0021 | 0.13 / 592 | 1.0019 / 1.0011 / 1.0019 / 1.0041 | 0.07 / 549 |
| 3.8 | 1.0016 / 1.0007 / 1.0007 / 1.0011 | 0.02 / 154 | 1.0012 / 1.0006 / 1.0013 / 1.0027 | 0.01 / 134 |
| 4.4 | 1.0007 / 1.0004 / 1.0001 / 1.0005 (+-0.0002) | 0.00 / 44 | 1.0006 / 1.0005 / 1.0006 / 1.0015 | 0.00 / 39 |
| **all 755 points** | | **4.71 / 4720** (gas 1D 538) | | **2.58 / 4120** (gas 1D 569) |

All twelve bins were computed (four seeds each; none interpolated). The other bins are in `frz3_<foot>.out`. The flux
Delta chi^2 is concentrated at z 2.2 to 2.8.

## Brackets (anchor bins, scaled to 12 bins; gate 4)

| bracket | canonical | alt |
|---|---|---|
| primary | 4.71 | 2.58 |
| gamma 1.2 / 1.6 | 4.2 / 4.8 | 1.8 / 3.8 |
| lambda_P x 0.5 / x 2 | **11.0** / **2.5** | **8.5** / 1.8 |
| minimum halo mass 1e10 | 5.0 | 2.7 |
| FRZ1 reading V | **1e-4** | 7e-5 |
| FRZ1R remainder | 4.3 | 2.5 |

- Canonical: lambda_P x 2 and reading V land under the gate.
- Alt: lambda_P x 0.5 lands over the gate.
- So both conditional labels would carry FRAGILE. The result is set mostly by the pressure scale, which is PROVISIONAL.

## Known answers, scatter, mutations
- (a) Difference switched off: R_F = 1 exactly, Delta chi^2 0. PASS.
- (b) **FAIL.** Painted R against FRZ1 at k 1 / 3 / 5:
  - z 3 canonical: 0.995 / 0.928 / 0.798 against 0.992 / 0.845 / 0.665.
  - z 4.4: 0.954 / 0.835 against 0.903 / 0.686 at k 3 / 5.
  - k 1 passes everywhere; alt z 2.2 passes.
  - The b0 check passed before the freeze (the copied layout's halo model equals FRZ1's R_cold). So the shortfall is in the
    painted field, not in the layout. The likely cause is extra small-scale power in the reference field (the lognormal
    smooth part plus the halo two-point term), which dilutes the ratio. Not tested.
- (c) Optically thin limit against the 1D gas ratio: largest deviation 0.002 of the tolerance. PASS.
- (d) Mean flux matched to 3e-16. PASS. DESI md5 matches; R = 1 gives 0.
- Scatter against effect at z 2.2 / 3.0 / 4.4: S/E = 0.23 / 0.27 / 0.33 (canonical) and 0.21 / 0.22 / 0.21 (alt). OK.
- M1 (saturation removed) bites on both footings: it moves toward the matter level.
- M2 (difference doubled) bites on both footings: 1.49 -> 5.72 and 0.90 -> 3.37.
- A2 floor-off re-run (z 3, seed 0): R_F identical (no pixel there falls below the floor). Floored pixels exist only at
  z 2.2 (6.6e-5 of pixels, the same in both fields). A floor-off run at z 2.2 was not made.

## Inherited / left out / not checked
- **Inherited:**
  - FRZ1's layout and its halo-model ingredients: Tinker / Duffy z-scalings PROVISIONAL, PD1 share at z 1, Delta_ta
    interpolation.
  - FGPA constants T0 1.2e4 K, gamma 1.4, lambda_P 80 proper kpc, and Becker et al. 2013 mean flux: all from memory,
    PROVISIONAL, not checked against sources.
- **Left out of the flux model:**
  - peculiar velocities (real space only);
  - hydrodynamics, shock heating, self-shielding, DLA masking, UV and temperature fluctuations, metals;
  - continuum and noise;
  - halo exclusion and overlap;
  - halo positions, which are a biased-Poisson draw on a lognormal field, not N-body.
  The reference field's absolute P1D was not compared with DESI. Only paired ratios are used.
- **Not checked:**
  - why (b) falls short;
  - a larger box (20 Mpc/h; DESI points below 0.0024 to 0.0030 s/km take the first-mode value);
  - redshift-space distortions, which could undo part of the softening.

## Files
- `frz3_layout.py`: the layout, copied from FRZ1R with FRZ1's conventions.
- `frz3_fields.py`, `run_all.sh`, `parts/` (48 parts), `parts_check/`; console logs in `logs/` are git-ignored (local only).
- `frz3_grade.py`, which writes `frz3_<foot>.json/.out` and `frz3_<foot>_MUTATE.json/.out`.
- About 1.7 h of machine time: 4 threads, nice 19, peak resident memory 6.8 GB.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
