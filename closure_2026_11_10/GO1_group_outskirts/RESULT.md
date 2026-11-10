# GO1 RESULT: NOT EVALUABLE [r_ta NOT REACHED] / NOT EVALUABLE [r_ta NOT REACHED]. Form B's turnaround census is not reached by KiDS-1000; nothing is decided

Criteria c1a9527ebf (committed alone before any script or number). AMENDMENT A1 05f48b8a6d is post hoc, committed alone before the
graded run, and disclosed. TEST lane: adopts nothing, relabels nothing (RB1's labels stand), registers nothing. Form B = the a0 law
with cold dark energy counted once; kappa = 1/2 FITTED; not theory closed. Cold dark energy is a gravitating field component,
never a particle. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled. f_ret contains no a0, and both footings
give identical numbers (KA5).

**Part 0** (eRASS1 X-ray tile plan, nothing downloaded) is in `DATA_PLAN.md`:
- 11 of the 20 Lovisari groups are in the eRASS1-DE DR1 footprint.
- 50 tiles cover them: 726,234,784 bytes (0.73 GB); the 11 central tiles alone are 154 MB.
- The site states no licence; it requires an acknowledgement and a citation.
- Depth is 80-210 s, too shallow for one group at 3-5 R500.

## Label

| reading | canonical | alt |
|---|---|---|
| **f_ret at turnaround (graded)** | **NOT EVALUABLE [r_ta NOT REACHED]** | **NOT EVALUABLE [r_ta NOT REACHED]** |
| every bracket (lens tail x^-1.5 / x^-3 / none, y tail, no beam correction, CIB-deprojected y, Mgas x 0.8, stars 0 / x 1.5 beyond R500, R 5.562, delta_ta 11, lambda_n 2.5e-7 / 2.5e-3, z 0.05-0.20) | same | same |

- The stack's mean enclosed density never falls to 5.55 rho_m inside 16 R500 (10.6 Mpc). This holds in all 30 jackknife
  realisations and in every bracket, and the lower-bound census reads the same way.
- It is 18.5 ± 5.2 at 8 R500, 16.6 ± 6.2 at 11.3 and 16.7 ± 7.8 at 16.
- So the turnaround radius is not located, and B's requirement f_ret(<r_ta) = 1 is not tested.
- The frozen power gate would very likely have failed anyway: M_exc at 8 R500 is uncertain by 29 %, and 36 % in the mocks.
- **Form B is neither supported nor falsified by this lane.** Predicted in A1 before the graded run: NOT EVALUABLE.

## The numbers (reported, not graded)

**Sample.**
- 102 eRASS1 groups kept of 220 selected. Selection: KiDS-1000 boxes, the ACT y strip, Mgas500 1.35e12-1.15e13, z 0.05-0.30.
- Dropped: 93 with too few KiDS sources, 19 with an empty radial bin, 6 failing the y mask.
- Median z 0.143. Lensing-weighted means: M500 1.0e14 (catalogue), Mgas500 5.36e12, R500 0.66 Mpc, T500 1.94 keV.

**Stacked census, primary** (T = T500 x^-0.6 outside R500). f_ret = R M_b / (M_tot - M_b), R = 5.41; jackknife errors.

| x = r/R500 | M_exc lensing (Msun) | y gas 1..x (Msun) | M_b (Msun) | delta / rho_m | f_ret | f_ret lower bound (isothermal T500) |
|---|---|---|---|---|---|---|
| 1 | 7.9e13 ± 1.8e13 | - | 7.0e12 | 1033 ± 236 | **0.53 ± 0.14** | 0.53 ± 0.14 |
| 1.41 | 1.31e14 ± 0.29e14 | 3.7e12 ± 1.4e12 | 1.16e13 | 601 ± 126 | 0.53 ± 0.14 | 0.50 ± 0.13 |
| 2 | 0.74e14 ± 0.43e14 | 6.3e12 ± 2.9e12 | 1.33e13 | 122 ± 68 | 1.17 ± 0.81 | 1.05 ± 0.70 |
| 2.83 | 2.20e14 ± 0.40e14 | 1.26e13 ± 0.69e13 | 2.22e13 | 128 ± 21 | 0.60 ± 0.17 | 0.49 ± 0.10 |
| 4 | 3.25e14 ± 0.68e14 | 2.2e13 ± 1.7e13 | 3.40e13 | 67 ± 13 | 0.62 ± 0.35 | 0.45 ± 0.17 |
| 5.66 | 6.0e14 ± 1.4e14 | 0.6e13 ± 2.6e13 | 2.40e13 | 44 ± 10 | 0.22 ± 0.25 | 0.23 ± 0.10 |
| 8 | 6.9e14 ± 2.0e14 | -0.4e13 ± 5.1e13 | 1.90e13 | 18.5 ± 5.2 | 0.15 ± 0.38 | 0.21 ± 0.11 |
| 11.3 | 1.7e15 ± 0.7e15 | 7.7e13 ± 7.5e13 | 1.29e14 | 16.6 ± 6.2 | 0.41 ± 0.28 | 0.23 ± 0.08 |
| 16 | 4.9e15 ± 2.4e15 | -6.7e14 ± 3.4e14 | -5.4e14 | 16.7 ± 7.8 | -0.50 ± 0.41 | 0.01 ± 0.09 |

**At R500.** The lensing mass gives f_ret = **0.53 ± 0.14**. RB1 had 0.597 from hydrostatic masses, on different groups. The
same ~40 % shortfall shows up without the hydrostatic assumption.
- Lensing M_exc(<R500) = 7.9e13 ± 1.8e13, against the catalogue's 1.0e14 (which is LCDM-calibrated, and used here only as the scale).
- Gas 5.36e12 (eRASS1 X-ray) plus stars 1.67e12 (KVM18).

**At 3 R500** (the radius the brief named). f_ret = 0.60 ± 0.17 on the primary T(r); the isothermal lower bound is 0.48 ± 0.10;
excess-only 0.60.
- **On hot gas, the census does not rise toward 1 between R500 and 3 R500.**
- The y gas outside R500 is detected at only 2.0 sigma at 3 R500 (MUTATE M2 below). It amounts to 1.3e13 ± 0.7e13 out to
  2.83 R500, about twice the gas inside R500.
- This is not graded. Inside r_ta, B allows f_ret < 1 (gas expelled further out than the cold).
- Read it as a direction, not a verdict: if B is right, the missing baryons are not hot gas inside 3 R500. They would have to be
  beyond 3 R500, or cooler than about T500 x^-0.6, or both.

**Beyond 5 R500** the y census is not usable. The x = 16 shell is 2 sigma negative: large-scale residuals in the NILC map, and the
truncated onion's last shell absorbs everything projected from outside. The lensing excess there is dominated by the groups'
environment, out to 4.9e15 Msun inside 10.6 Mpc.

**T scale check.** The y-weighted temperature in 0.5-1 R500, over the eRASS1 beta-model gas, is **1.00 T500**. So the T500 used to
turn pressure into mass agrees with the X-ray gas where both are measured.

**Law row** (the only place a0 enters). The law's own mass from the census baryons, over the lensing mass:
- canonical 0.62 at R500 and 1.10 at 3 R500;
- alt 0.68 and 1.21.

## Known answers, nulls, MUTATE

- **KA1 PASS:** CFG686's esd (exec'd from its file) and the GO1 copy agree bit for bit (max relative difference 0) on 5 selected
  groups; CFG686's SIS self-test 0.996-1.000 (`go1_ka1.out`).
- **KA2 (A1 method) PASS:** analytic NFW plus an r^-2 excess comes back as 1.023 / 1.028 / 1.044 at x = 1 / 2.83 / 8 (A1 tolerance 5 %).
  **KA2b PASS:** 200 noisy mocks give bias 0.14 / 0.19 / 0.16 sd and relative sd 0.21 / 0.22 / 0.36.
- **KA3 PASS:** a beta-model y template, beam-corrected by the gNFW correction, is recovered at 0.997 / 0.984 / 0.986 / 0.992 in the
  shells from 1 to 4 R500. Map geometry against WCS agrees to 7e-11 pix.
- **KA4 PASS** (identity) and **KA5 PASS** (footings identical).
- **N1 cross shear PASS:** M_exc z +1.58 / +0.09 / -1.60 at x 1 / 3 / 8.
- **N2 random-minus-random PASS:** M_exc z -2.03 / +0.26 at x 3 / 8; y gas +0.64 / -0.07.
- **M1 (R x 2): cannot run.** With no r_ta there is nothing for it to move. The script prints DOES NOT BITE.
- **M2: DOES NOT BITE.** The shifted-position y gas is consistent with zero (z -1.91 / -0.30), but the real stack's y gas outside
  R500 is itself only +2.03 / -0.09 sigma. The hot-gas census beyond R500 has no 3-sigma power.
- **M3 BITES:** with the sign of e_t flipped, M_exc(<16) = -4.9e15.

## Disclosed

1. **KiDS-Legacy cannot be stacked.** The release on disk holds cosmic-shear 2-point data, chains and n(z), and no shear
   catalogue. Part A uses KiDS-1000 only.
2. **A1 was written after a failed run.** The first run (uncommitted) failed the frozen KA2 by orders of magnitude: a uniform
   core shell against a cusp, in an ill-conditioned (cond 2e4) square solve.
   - A1 replaced the method: a point-mass core, weighted least squares and a Tikhonov penalty.
   - It loosened KA2 from 3 % to 5 %.
   - Before writing A1 I had seen the stacked shear per bin and mock tests.
3. **One code fix after A1, no rule change.** The first A1 run crashed in the nulls on log(negative density) in the r_ta
   interpolation. The fix: linear interpolation when delta <= 0. The primary numbers printed before the crash are identical to
   the final ones.
4. **Imports.** R500 and M500 come from eROSITA's LCDM-calibrated scaling relations. They are used only as the radial unit, for
   T500 (self-similar) and for KVM18 stars, never as a mass in f_ret. omega_b = 0.0224, and T(r) = T500 x^-0.6 (FR3's tau), are
   stated imports.
5. **Part 0 lookup.** The Part 0 draft came from a delegated web-lookup agent and was read in full here. It used one small query to
   eRODat's upper-limit service for exposures.

## Limits, and what would decide it

1. **Too few groups for the lensing.** 102 groups give a shear S/N of about 9. To reach r_ta, and to get sigma(f_ret) <= 0.20 there,
   needs several times more groups (eRASS1 x HSC or DES Y3, which are not on disk) or a deeper survey.
2. **The environment.** Around eRASS1 groups the enclosed overdensity stays at about 17 out to 10 Mpc. Either r_ta is beyond
   16 R500 for these groups, or an additive shear systematic of the kind CFG687 found (~2 Msun/pc^2) inflates the outer mass.
   I cannot tell which from these data.
3. **y sees pressure, not mass.** Without an independent temperature, a census that falls short can never falsify B. The X-ray
   density beyond R500 (Part 0's tiles, or better the published 827-group eRASS1 stack) is the missing half.
4. **Stars beyond R500** are modelled (they trace the lensing excess with the KVM18 ratio), not measured. The brackets with 0 and
   x 1.5 do not move the label.

## Files and commits

`FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `DATA_PLAN.md`, `go1_extract.py` (KiDS column cache to the session scratch),
`go1_measure.py` (per-group shear + y, checkpointed, 17 s), `go1_ka1.py` -> `go1_ka1.out`, `go1.py` -> `go1.out` / `go1.json` /
`go1_MUTATE.out`, and this file.

| commit | local `main` | origin/main (replayed by merge-tree + commit-tree) |
|---|---|---|
| FROZEN_CRITERIA.md, alone | c1a9527ebf | 7c3bfd513a |
| AMENDMENT_A1.md, alone (post hoc) | 05f48b8a6d | a9fefb6365 |
| scripts, outputs, DATA_PLAN.md, RESULT.md | c07fbc9052 | e643ea014d |
| this id table | the commit that adds it | its replay, the last GO1 commit on origin |

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
