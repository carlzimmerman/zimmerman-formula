# GO2 RESULT: NOT EVALUABLE [r_ta NOT REACHED] / NOT EVALUABLE [r_ta NOT REACHED]. Form B's groups row is neither falsified nor left standing

Criteria df55a3237c (committed alone, before any stacking script or stacked number). No amendment. TEST lane: adopts nothing,
relabels nothing (GO1's and RB1's labels stand). Footings canonical (a0 9.3603e-11) and alt (1.1312e-10), never pooled; f_ret
holds no a0 and both footings give identical numbers. Cold dark energy is a gravitating field component, never a particle.

## Label (per footing)

| | canonical | alt |
|---|---|---|
| graded (isolated DESI groups, delta_ta 5.55) | **NOT EVALUABLE [r_ta NOT REACHED]** | **NOT EVALUABLE [r_ta NOT REACHED]** |
| every one of the 16 brackets | NOT EVALUABLE (the reason changes in 5) | same |

- The stack's mean enclosed density is **5.88 ± 4.59 rho_m at 16 R500** (9.1 Mpc), so it does not fall through 5.55 inside the
  grid; r_ta is reached in only 12 of 30 jackknife realisations. delta is 16.8 ± 6.5 at 5.66 R500, 9.1 ± 3.0 at 8, 6.5 ± 3.9 at 11.3.
- Brackets where the reason changes: x^-3 lens tail (r_ta 15.5, 17/30), no tail (r_ta 9.7, 30/30, sigma f_ret 1.77), delta_ta 11
  (r_ta 7.2, 30/30, f_ret 0.65 ± 0.92), lambda_n 2.5e-3 (r_ta 12.7, 24/30), z 0.05-0.20 (too few groups). All NOT EVALUABLE.
- **Where r_ta can be located at all, sigma(f_ret(<r_ta)) is 0.9-1.8**, against the frozen gate of 0.20. The hand estimate
  (0.6-0.9, NOT EVALUABLE) was right in kind; the stack is noisier than estimated.
- Isolation lowered the outer density relative to GO1 (GO1: 18.5 / 16.6 / 16.7 at 8 / 11.3 / 16 R500; here 9.1 / 6.5 / 5.9), but
  M1 below shows the non-isolated control is no higher, so this lane cannot credit that drop to the isolation cut.

## Groups after each cut

- DESI DR1 BGS centrals in the KiDS-1000 N box x ACT strip, z 0.05-0.30, log10 M_HALO 13.5-14.5, spectroscopic z: **4,956**.
- 10 Mpc disc >= 90 % inside the DESI footprint: **4,606**. Isolated (no central with >= 0.5 M_HALO within 10 Mpc projected and
  2000 km/s): **788**. Kept by GO1's rules: **369** (dropped: 339 too few KiDS sources, 72 empty bin, 6 y mask, 2 randoms).
- The criteria expected about 530 isolated. That was the scout's count after a KiDS-coverage proxy that the frozen selection does
  not apply (KiDS coverage enters through the source rule instead). The kept number, 369, is inside the expected 350-450.
- Kept sample: median z 0.22. Lensing-weighted mean M_HALO 8.4e13 Msun/h; M500 6.7e13 (converted, an import); R500 0.57 Mpc;
  T500 1.48 keV. Stacked shear total S/N 9.2, the same as GO1's 102 eRASS1 groups: more groups, but about 0.6 of the mass.

## Numbers (reported, not graded; primary census, jackknife errors)

| x = r/R500 | M_exc lensing | y gas 1..x | M_b | delta / rho_m | f_ret | f_ret lower bound |
|---|---|---|---|---|---|---|
| 1 | 3.07e13 ± 0.92e13 | - | 2.79e12 | 515 ± 150 | 0.54 ± 0.20 | 0.54 ± 0.20 |
| 2 | 7.50e13 ± 1.67e13 | 3.5e12 ± 2.7e12 | 7.17e12 | 158 ± 34 | 0.57 ± 0.30 | 0.49 ± 0.23 |
| 4 | 3.1e13 ± 4.0e13 | 6.6e12 ± 13.7e12 | 1.00e13 | 9 ± 10 | 2.2 ± 5.8 | 1.6 ± 3.2 |
| 8 | 2.47e14 ± 0.91e14 | 1.7e13 ± 4.8e13 | 2.90e13 | 9.1 ± 3.0 | 0.63 ± 1.19 | 0.42 ± 0.39 |
| 16 | 1.2e15 ± 1.1e15 | 1.3e14 ± 4.2e14 | 1.97e14 | 5.9 ± 4.6 | 0.86 ± 2.39 | 0.40 ± 0.48 |

- **At R500:** f_ret 0.54 ± 0.20 (GO1 0.53 ± 0.14; RB1 0.597). Gas500 from y at T500 1.51e12 ± 0.53e12 (bracket 0.0536 M500:
  3.6e12); stars (KVM18) 1.29e12; visible DESI members' stellar mass 6.7e11 (a floor).
- The x = 4 shell dips below x = 2.83: deprojection noise.
- **Law row** (the only place a0 enters): the law's mass from the census baryons over the lensing mass is 0.85 / 1.46 at
  x = 1 / 3 (canonical) and 0.93 / 1.60 (alt).

## Known answers (all pass)

- **KA1a:** GO2's measurement code on GO1's eRASS1 selection reproduces GO1's checkpointed shear sums for 10 groups exactly
  (max relative difference 0).
- **KA1b:** GO2's stacker on GO1's checkpoint reproduces go1.json's delta and M_exc at x = 1, 4, 8, 11.3, 16 exactly
  (delta 18.48 / 16.58 / 16.68 at 8 / 11.3 / 16).
- **KA2 random-position stack:** random-minus-random M_exc z +1.10 / +1.67 / +1.32 at x 3 / 8 / 16; y gas z -0.37 / -0.50 / -1.60
  at x 1 / 3 / 8. Cross shear z -1.98 / -0.69 / -0.65.
- **KA3:** deprojection 1.023 / 1.029 / 1.044 (5 %), mock bias <= 0.15 sd. Beta y template within 10 % in shells 1-4 (1.13,
  1.01, 0.96, 0.97). Map geometry 7e-11 pix. Identity passes; footings identical.

## Mutations

- **M2 (e_t sign flipped): BITES.** M_exc(<16) = -1.2e15, no r_ta.
- **M1 (isolation off): DOES NOT BITE.** In 277 kept non-isolated groups, delta(11.3) = 1.96 ± 5.15, against 6.54 ± 3.89 for the
  isolated groups; the control reaches r_ta at 8.1. So the isolation cut does not raise or lower the outer density measurably at
  this noise. GO1's 17 is not reproduced by DESI groups of either kind, so its excess may belong to eRASS1's selection or to noise.
- **M3 (y at positions shifted 1-3 deg): DOES NOT BITE.** The shifted gas inside R500 is 1.23e12 (z +2.80), the real one 1.51e12
  (z +2.82). The y gas inside R500 is not separated from a local y offset around the groups. The random stack is null, so the
  offset is local to the group fields and not a stacking error. The y census of these groups has no power.
- **M4 (R x 2):** cannot run (no r_ta).

## Inherited from GO1, and changed

- Inherited verbatim: the estimator and KiDS columns, bins, weights, randoms rule, jackknife, A1 deprojection, y reader, onion,
  beam correction, T(x), stars, background, T_close, law row.
- Changed: the group catalogue and isolation cut; the random box is the N box only (no DESI groups in the KiDS S box). Gas inside
  R500 now comes from y at T500, because DESI groups carry no X-ray gas mass. R500 is from M_HALO, read as M200m in Msun/h through
  an NFW with c = 6. This is a disclosed import, used as the unit, for T500 and for the stars; the M500 x 0.7 / x 1.4 bracket
  changes T500 and the stars but not the measured unit.

## Not checked
The M_HALO mass definition (not stated in the docs); the DESI group randoms (not fetched; footprint approximated from 0.25 deg
galaxy cells); neighbour completeness at z > 0.2; the local y offset behind M3; any temperature outside R500 (y sees pressure
only); DES or HSC shear (not on disk).

## Data

- `bgs-groups-dr1-v1.0.fits`, 289,877,760 bytes, sha256 fa209a94993c9500ef04960b367ec55dcc799e9a3d0ac00bf2af762add39368b (= published),
  from https://data.desi.lbl.gov/public/dr1/vac/dr1/bgs-groups/v1.0/ (docs .../doc/releases/dr1/vac/bgs-groups/, PROVISIONAL); not in git.
- Licence CC BY 4.0. Requirements: cite DESI Collaboration et al. (2026), "Data Release 1 of the Dark Energy Spectroscopic
  Instrument"; cite Williams et al. (2026) and Tinker et al. (2021, 2022) for the group finder; include DESI's acknowledgement
  text (https://data.desi.lbl.gov/doc/acknowledgments/, beginning "This research used data obtained with the Dark Energy
  Spectroscopic Instrument (DESI).").

## Files and commits

Files: `FROZEN_CRITERIA.md`; `go2_scout.py` -> `go2_scout.out` (pre-freeze counts); `go2_measure.py` -> `go2_ka1a.out`,
`go2_measure_log.txt`; `go2.py` -> `go2.out`, `go2.json`, `go2_MUTATE.out`. Commits: criteria df55a3237c (alone); scripts,
outputs and RESULT 57afae3555; this id line in the commit after. Not pushed.

Origin commit ids: criteria 896e71ca82 (alone); scripts, outputs and RESULT db4a558fc6; id line 436df3f85f. Re-run by the lead from a copy at
the same folder depth, measuring the groups afresh into a new checkpoint (the scout, the DESI measurement, KA1a and the
stacker with its mutations), using the same KiDS column cache and GO1 checkpoint as the lane: of 6 output files, 5
equal the committed ones byte for byte and 1 differ only in timing or resume lines. A re-run reproduces the arithmetic
and is not an independent re-grade. Pushed by replay; no history rewritten.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
