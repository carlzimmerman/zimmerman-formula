# DPR1 RESULT: distinctive, dated predictions of form B

## Verdict

**No candidate meets the frozen definition, on either footing. Nothing was sealed.**

- 17 candidates were examined: 16 of form B as adopted, and 1 CONDITIONAL ON THE JOINT.
- None is DISTINCTIVE on data due on or before 2027-12-31.
- Form B as adopted has no prediction that is its own, separates it from both rivals by 3 expected errors, and rests on
  dated data. That is the lane's answer, not a failure of the lane.
- Closest: the KO2 own-field statistic, early types, Euclid DR1 shear (2027-06-16). Form B is 18-19 expected errors from
  the law (R2) but only 1.9 / 2.6 (canonical / alt) from the record's cold reference (R1); on KiDS, which exists, the
  measurement already sits 6.4 / 6.9 KiDS errors above form B.

Criteria `FROZEN_CRITERIA.md` (ded8ccd8e4, committed alone first). Scripts and outputs: bcfea35c0d. TEST lane. Registers
nothing and edits no registry. Footings never pooled. kappa = 1/2 FITTED; not theory closed. Adopts nothing.

## The one new computation: R1 through KO2's machinery

The record had no value for R1 on KO2's statistic, so this lane computed one.
- **Machinery.** `dpr1_ko2_r1.py` is `ko2_formB.py` (KO2 amendment A3, ece364d804) with only the halo profile replaced.
- **R1's profile.** The record's cold reference (FRZ1's rule as written in `srh1r_model.py`): form B's own total cold mass
  (PD1's share, 59.49 / 59.50 M_b), laid out as an NFW profile to the turnaround radius.
- **Same designs.** Every lens and every neighbour follows the rule, and the planted sums are fitted with KO2's designs.
- **Cache and checks.** KO2's cache was rebuilt by re-running `ko2.py` from a copy outside the repo (reproduces its 12 of 13
  checks and the KA-3b fail). 9 of 9 checks pass on both runs; KA-B5 reproduces `ko2.json`'s data readings to 2e-16.

KO2 primary statistic R_ext (the law as a galaxy's own field gives 1; no own field beyond the inner window gives 0):

| type | form B (canonical / alt) | R1, median lens z 0.308 / z 0 | R2 (the law) | KiDS measured |
|---|---|---|---|---|
| early | 0.034 / -0.001 | 0.135 / 0.187 | 0.9999 | 0.487 +- 0.071 |
| late | 0.038 / 0.007 | 0.141 / 0.183 | 0.9999 | 0.277 +- 0.183 |

Euclid error: KO2's statistical part scaled by (area x n_eff)^-1/2, 0.05 floor kept: sigma_D 0.053 early / 0.077 late
(1,900 deg^2, n_eff 30; n_eff 20 gives 0.054 / 0.087; inputs PROVISIONAL). Separations from B in sigma_D: early R1 1.9 /
2.6, R2 18.3 / 19.0; late R1 1.3 / 1.7, R2 12.5 / 13.0. A concentration spread only widens R1's band, so it was not run.

## All candidates (separations in expected errors of the dated data; canonical / alt)

| # | candidate | data and date | B | R1 | R2 | class |
|---|---|---|---|---|---|---|
| 1 | KO2 own field, early types | Euclid DR1 shear, 2027-06-16 (PROVISIONAL scope) | 0.034 / -0.001 | 0.135-0.187 | 1.00 | NOT DISTINCTIVE: R1 at 1.9 / 2.6; KiDS already 6.4 / 6.9 above B (post-diction) |
| 2 | KO2 own field, late types | same | 0.038 / 0.007 | 0.141-0.183 | 1.00 | NOT DISTINCTIVE: R1 at 1.3 / 1.7 |
| 3 | host-free shape, ONE1 / SRH1R statistic | same | law to x_t | NFW | law to r_ta | NOT DISTINCTIVE: proxy from SRH1R's T values, R1 at 4.0 / 2.6, R2 at 0.6 / 0.3 |
| 4 | wide binaries, gamma_v | Gaia DR4, 2026-12-02 | 1.000 | 1.000 | 1.149 / 1.208 (CW1) | NOT DISTINCTIVE: B = R1; registered (CQ2) |
| 5 | hosted dwarfs keep their own halo (no external field effect) | none dated | RB2 | NFW | lower (external field) | NO DATED DATA; existing data: RB2's ultra-faints FAIL high, DSB1 NO POWER |
| 6 | a0 tied to rho_DE: ALMA vc875, condor units, C159 | 2026-11-13 to 2027-09-24 | V_flat ratio [0.90, 1] | no a0 | 1 | NOT DISTINCTIVE: B's band contains R2 (constant dark energy in B's carried cosmology); registered |
| 7 | a0(z) on high-z rotators (KT2) | no sample | as 6 | - | 1 | NO DATED DATA; registered |
| 8 | CONDITIONAL ON THE JOINT: break at R_fold ~ M_b^(1/3), shrinking with z | ALMA, Euclid | break beyond the data | - | - | NOT DISTINCTIVE: vc875 reaches 0.36 R_fold, RC100 0.39, SPARC 0.47; lensing cannot see R_set (SRH1R) |
| 9 | share 5.41 to turnaround (groups) | none dated | 5.410 / 5.412 | the same fit | - | NOT DISTINCTIVE: B = R1 by construction; GO2's error 0.9-1.8 against a gate of 0.20 |
| 10 | Euclid wide and group-hosted strong lenses; 4MOST source redshifts | Euclid now; 4MOST no date | the law inside R_E | NFW | the law inside R_E | NOT DISTINCTIVE: B = R2 for the lens's own halo |
| 11 | cosmic shear, 1-halo redistribution | Euclid 2027-06-16 | -0.6 / -1.0 % at k 1; -5.1 / -8.8 % at k 3 (CO1) | 0, plus feedback spread | no prediction | NOT DISTINCTIVE: inside R1's feedback spread (PROVISIONAL) |
| 12 | forest P1D | DESI DR2 P1D: no date | FAILS on DR1 at matter level; flux level unsettled (FRZ3 / FRZ3R) | 1 | no prediction | NO DATED DATA; POST-DICTION fail |
| 13 | Milky Way dlnM/dlnr, 100-200 kpc | needs a profile; no date | 0.964 / 0.967 | 0.582 (DESI's NFW) | about B (13.4 vs 13.7 at 200 kpc) | NOT DISTINCTIVE: B = R2; registered (row 32) |
| 14 | Milky Way potential depth (escape speed) | Gaia DR4; analysis has no date | 490 / 507 km/s from 30 kpc to infinity | 451 | 443 / 457 (crude) | NO DATED DATA; depends on the escape convention (to 460 kpc: 408 / 427 against 401); DR3-era measurements exist |
| 15 | vertical force and local density at the Sun | Gaia DR4; no scorer (DR4 map C10) | the law's phantom | round NFW | the law's phantom | NOT DISTINCTIVE vs R2 (argument; the field is negligible at R0); not computed |
| 16 | spectroscopically isolated lenses | DESI DR2 spectra, "early 2027" PROVISIONAL | as 1-3 | as 1-3 | as 1-3 | NOT DISTINCTIVE: same statistics, smaller area than Euclid |
| 17 | LMC reflex and mass | existing data | RFX1 | - | - | POST-DICTION (RFX1, today) |

## Why none passes

These are reasons, not new labels.
- **Inside its truncation radius form B is the law,** with a host's field that is negligible for isolated systems, so it
  agrees with R2 (rows 3, 10, 13, 15).
- **On large scales form B is the cold reference** by construction, so it agrees with R1 (rows 4, 9, 11).
- **Where both differ:**
  - Beyond the truncation radius (rows 1, 2), B and R1 lie within 2.6 expected errors of each other: both put form B's
    total cold mass inside a few hundred kpc.
  - In hosted dwarfs and the forest (rows 5, 12), no data are dated, and existing data already count against B.
- **The a0(z) tie** (rows 6, 7) is distinctive only if dark energy evolves. Form B's own cosmology carries constant dark
  energy, so B's band contains R2.

## What surprised, or contradicts the brief

- **Form B can be confirmed nowhere before 2028 by the frozen standard; Gaia DR4, Euclid's own-field statistic and the
  a0(z) units can only kill it.** That matches the lead's estimate for 2026 and extends it through 2027.
- **The conditional joint was expected to be where distinctive predictions live.** It is not: its break lies beyond every
  dated rotation curve, and lensing does not see inside R_set (SRH1R). The lead's estimate is not borne out there.
- **Post hoc, never graded:** KiDS's early-type KO2 value (0.487 +- 0.071) sits about 5.0 KiDS errors above R1's 0.135, as
  well as 6.4 above form B and 7.3 below the law.
  - The record's cold reference layout misses the early-type outer shape as badly as form B does.
  - KO2's R3 flag (unseen neighbours) may be part of the reason.
- **Rows 13-14:** B's Milky Way and R1's differ in slope (0.96 against 0.58) and in total mass (cap 598 / 544 kpc,
  60.5 M_b). R2 at a literature field shares B's slope, so the slope does not separate B from both.

## PROVISIONAL and unverified

- Euclid DR1 area and shear products (A6, web read) and both n_eff values; the error rule assumes a KiDS-density lens sample
  and that KO2's machinery runs on Euclid's catalogue (not tested). Row 3 is a proxy (SRH1R stores no model vectors); row
  14's R2 is a crude cut at EFC1's saturation mass; row 11's feedback spread is literature; row 15 is an argument.

## Files

`FROZEN_CRITERIA.md`; `dpr1_ko2_r1.py` -> `dpr1_ko2_r1.json` / `.out` and `dpr1_ko2_r1_z0.json` / `.out` (851 s each, peak
0.6 GB, one thread); `dpr1_candidates.py` -> `dpr1_candidates.json` / `.out`. Caches stayed in the session scratchpad.
Nothing was fetched.

Adopts nothing. kappa = 1/2 FITTED; not theory closed.
