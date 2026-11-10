# KL1R RESULT: blind, independent regrade of KL1 Part B (form B's weak-lensing amplitude against raw KiDS-Legacy)

## Label (per footing, never pooled)

| reading | canonical (a0 9.3603e-11) | alt (a0 1.1312e-10) |
|---|---|---|
| **Frozen (KL1 Part B + PB1, as written)** | **NO VERDICT** | **NO VERDICT** |
| Under amendment A1 (post hoc) | AMPLITUDE CONSISTENT WITH RAW LENSING | AMPLITUDE CONSISTENT WITH RAW LENSING |

- **Why NO VERDICT as frozen:** MA2 cannot bite on DES Y3. With every density halved, only 4 / 4 DES points are signal-dominated,
  so test (ii) reads NOT EVALUABLE. The DES A2 / ALL rows are therefore NO VERDICT, and the overall label takes the worse of Legacy
  and DES. Legacy alone passes every guard as frozen (KB3, MA2, MA3, MB1 all bite / pass) and reads **CONSISTENT** at BALL on both
  footings (p 0.111 / 0.101).
- **Under A1:** MA2b (densities doubled) bites on DES, and DES's ALL row reads CONSISTENT (p 0.157 / 0.161). The overall label is
  AMPLITUDE CONSISTENT WITH RAW LENSING, which rests on the post-hoc amendment.
- **What still counts against form B (Part B section 5):** the Legacy gap stays above 2 widths. Legacy prefers sigma8 0.7875 /
  0.7855 +- 0.0116 at BALL, 2.13 / 2.30 widths below the neutrino-floor target 0.8121 / 0.8120 (3.09 / 3.27 widths at B1). BALL is
  not at TENSION, and MB1 bites.
- **MB2 does not bite** (moving to KiDS-1000's redshift prior means shifts the Legacy best sigma8 by -0.09 / -0.09 widths; 0.5
  needed). I read it as frozen in my criteria section 2.7: it is reported and does not change the label. Under the strict reading,
  where MB2 guards every Legacy row, the label would also be NO VERDICT.
- Every label is "for form B with the neutrino floor, its own layout with RB1's gas, the covariance at the model; gravity-only S0
  box; inherited halo list".

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. **kappa = 1/2 FITTED; not theory closed.** Cold dark
energy, never a particle. Criteria: `FROZEN_CRITERIA.md`, commit **1792bd07ea**, committed alone before any script or number. It
adopts KL1 Part A 99a42c78ef, Part B d26939ed4f, PB1 7787483300 and A1 e01d1b9a35. The blindness was not clean: KL1's headline
numbers were visible in context before this lane began, which criteria section 1 discloses.

## Numbers (KiDS-Legacy: 173 of 357 published-kept points pass the support cut; DES Y3: 52 of 227)

Target sigma8: CO2's pin 0.8271 / 0.8271 at X0; my neutrino-floor refit 0.8121 / 0.8120 from X1 on. p is the chi^2_data survival
at N. Best sigma8 and width use CO2's rule (grid 0.70 to 0.90, parabola, Delta chi^2 = 1). "gap" is (target - best) / width.

**KiDS-Legacy**

| row | chi^2 (data) can / alt | p can / alt | label | best sigma8 can / alt (width) | gap can / alt | Delta chi^2 target vs best |
|---|---|---|---|---|---|---|
| B0 (CO2 pin, published cov) | 215.56 (211.25) / 218.01 (213.50) | 0.025 / 0.020 | TENSION | 0.7767 / 0.7748 (0.0115 / 0.0114) | 4.40 / 4.60 | 21.20 / 23.01 |
| B1 (neutrino floor) | 204.42 (201.67) / 206.18 (203.32) | 0.067 / 0.057 | CONSISTENT | same as B0 | 3.09 / 3.27 | 10.07 / 11.18 |
| B2 (+ covariance at model) | 200.24 (197.72) / 201.75 (199.15) | 0.096 / 0.084 | CONSISTENT | 0.7835 / 0.7814 (0.0115) | 2.49 / 2.66 | 6.20 / 7.07 |
| B3 (+ RB1 gas, published cov) | 202.17 (199.68) / 203.54 (200.95) | 0.080 / 0.072 | CONSISTENT | 0.7808 / 0.7788 (0.0117 / 0.0116) | 2.68 / 2.86 | 7.75 / 8.73 |
| **BALL** | **198.33 (196.03) / 199.49 (197.11)** | **0.111 / 0.101** | **CONSISTENT** | **0.7875 / 0.7855 (0.0116 / 0.0115)** | **2.13 / 2.30** | 4.51 / 5.27 |

BALL delta-z pulls at the target, in prior widths, per bin: 0.24, 0.79, -0.79, -0.95, -0.15, -0.29 (canonical); alt within 0.03 of
these. At the best sigma8: 0.05, 0.75, -0.65, -0.53, 0.13, -0.04. No pull exceeds 1 width. The alignment amplitude is 0.64 / 0.67.

**DES Y3** (CFG592's DES nuisances unchanged)

| row | chi^2 (data) can / alt | p can / alt | label | best sigma8 (width) | gap can / alt |
|---|---|---|---|---|---|
| A0 (CO2 pin) | 74.69 (69.78) / 74.67 (69.76) | 0.050 / 0.051 | CONSISTENT (on the line) | 0.7308 / 0.7312 (0.025 / 0.024) | 3.84 / 4.04 |
| A1 | 69.04 / 68.97 | 0.096 / 0.097 | CONSISTENT | same | 3.24 / 3.40 |
| A2 | 64.63 / 64.66 | 0.161 / 0.158 | CONSISTENT | 0.7426 / 0.7361 (0.022 / 0.020) | 3.15 / 3.87 |
| A3 | 69.08 / 68.89 | 0.096 / 0.098 | CONSISTENT | 0.7315 / 0.7305 | 3.30 / 3.51 |
| **ALL** | **64.71 / 64.58** | **0.157 / 0.161** | **CONSISTENT** (NO VERDICT as frozen: MA2) | 0.7401 / 0.7428 (0.026 / 0.022) | 2.81 / 3.12 |

**Known answers and MUTATE arms** (canonical / alt where they differ)

| item | result | reading |
|---|---|---|
| sha256 of the tarball | `7fdf214c...57f77`, same as the fetch log; the three files used are byte-identical to the tarball members | PASS |
| KB1 Legacy loader | 189 + 189 points, 6 bins, 21 pairs, 9 angular bins, COVMAT positive definite (min eigenvalue 1.3e-14), n(z) weights sum to 1.000 per bin, at most 1e-4 of any bin beyond z 3.5 | PASS |
| KB2 CO2's P4 through my loader and fit (KiDS-1000) | 157.890 / 159.355 against 157.890 / 159.355, N 104 | PASS |
| KA1 neutrino harness | (i) my CAMB call with mnu 0 gives CO2's PA and chi2_E exactly; (ii) CLASS sigma8 with 0.06 eV at the pin is 0.81524 / 0.81521 (0.8152) | PASS |
| A1 refit (one 0.06 eV neutrino) | tau 0.0562 / 0.0563, ln 1e10 A_s 3.0470 / 3.0471, n_s 0.9692 / 0.9693, omega_d 0.1198 / 0.1197; CMB total **better** by 1.18 / 1.31 than CO2's massless pin; CLASS sigma8 **0.8121 / 0.8120**, Omega_m 0.3147 / 0.3143 | adequate (cost < 9) |
| MA1 (0.6 eV) | sigma8 falls by 0.0958 / 0.0958 | bites |
| KA3 gas layout | (i) 2e-16 / 0, (ii) 2e-7 / 3e-8, (iii) mass 5e-16, monotone | PASS |
| KA4 response | median alpha below k 0.12: 0.956, 0.975, 0.987 | PASS |
| KB3 (KA2 on Legacy) | area 852.6 / 851.7 deg^2 (Wright et al. quote 967.4); (i) 183 points, 16th to 84th percentile 0.944 to 1.053; (ii) 95 points, median 1.040, min 0.830; median abs(dr) 0.012 | PASS |
| KA2 on DES | area 3477 deg^2; (i) 111 points, 0.973 to 1.026; (ii) 39 points, median 1.229, min 1.083 | PASS |
| MA2 (densities halved) | Legacy: (ii) 45 / 43 points, median 2.24 / 2.27 → fails (ii), **bites**. DES: (ii) **4 points, NOT EVALUABLE** ((i) fails narrowly: 0.907 to 1.155) | Legacy bites; **DES does not** |
| MA2b (densities doubled, A1) | Legacy (ii) median 0.48, bites; DES (ii) 90 / 91 points, median 0.65, **bites** | bites |
| MA3 (f_ret 0.2) | R at k 1 moves by -0.079 / -0.081; Legacy chi^2 at the B1 target moves by -4.97 / -6.39 | bites (DES's move is -0.55 / -0.58, reported: it would not bite) |
| MB1 / MP4 (sigma8 0.90 under BALL) | Legacy p 8.2e-6 / 3.9e-6 | bites |
| MB2 (KiDS-1000 redshift prior means) | Legacy best sigma8 moves by -0.09 / -0.09 widths | **does not bite** (reported; strict reading: NO VERDICT) |
| KB4 (context) | Legacy best sigma8 for form B 0.7767 / 0.7748 at B0, against KiDS-1000's 0.7358 / 0.7341 (CO2): +0.041. Wright et al. 2025 give Legacy S8 0.815 +0.016 -0.021 | context |

**Brackets on BALL (reported, never graded), Legacy p canonical / alt (DES):** gamma 0: 0.105 / 0.095 (0.150 / 0.151); gamma 3:
0.113 / 0.103; fiducial -0.02: 0.129 / 0.119; +0.02: 0.092 / 0.083; R200c gas edge: 0.103 / 0.092; power-law f_ret: 0.117 / 0.109;
**A5c1 alignment off: 0.052 / 0.044 (DES 0.027 / 0.027), with best sigma8 0.7782 / 0.7760 +- 0.0104 and a gap of 3.26 / 3.46
widths: it goes against**; A5a long modes (CFG411 L200 splice plus box deficit): 0.251 / 0.253 (DES 0.309 / 0.311); A5a with
CFG424 seed 360: 0.228 / 0.217. Scan with ln det C: Legacy best 0.7833 / 0.7813, DES 0.7298 / 0.7308.

## What carried the gap on Legacy (from B0 to BALL, canonical)

The release accounts for most of it: the Legacy best sigma8 for form B's spectrum sits 0.041 above KiDS-1000's, and B0's gap is
4.4 widths, against CO2's 5.6 on KiDS-1000. The neutrino floor lowers the target by 0.015 and takes B0's gap of 4.40 to 3.09. The
covariance at the model takes 3.09 to 2.49, mostly by moving the best sigma8 up by 0.007. The gas takes 3.09 to 2.68. All three
together give 2.13. The alignment-off bracket and MB2's missing teeth are the open points against the reading.

## Disclosures

- **One code bug, found after numbers were seen, fixed toward the frozen formula.** In my first run, the cosmic-variance part of my
  Gaussian covariance was divided by 2 pi twice. The ell weight carried 1 / (2 pi), and the sum was divided by 2 pi again. That
  first run had graded only Legacy, and KB3 failed there, with (ii) median 3.9. Fixing it makes the code match the formula frozen in
  Part A's A2 as written, and every grade was rerun. The rows that do not use G (B0, B1, B3, MB2) are identical in both runs. The
  first run's outputs are kept in `parts/buggy_2pi/`. No setting or choice was changed.
- MB2's mapping (by mean redshift): Legacy bins 1 to 6 have mean z 0.335, 0.477, 0.587, 0.789, 0.940, 1.224; KiDS-1000's five have
  0.257, 0.403, 0.564, 0.792, 0.984. KiDS-1000's bins 1 and 2 both go to Legacy bin 1 (their mean is used). Legacy bins 2 and 6
  receive none and keep their own shifts.
- The support cut keeps 173 of Legacy's 357 published-kept points. Large-angle points need modes beyond the 100 Mpc/h box.
- Files: `kl1r_nu.py` (refit), `kl1r_gas.py` (gas), `kl1r_lib.py`, `kl1r_known.py`, `kl1r_grade.py`, `kl1r_label.py`,
  `kl1r_check_data.py`, with outputs in `parts/`, `kl1r.out` and `kl1r.json`. All Python reading the release ran with `-I`.

## Comparison with KL1

(Added after this file is committed; see below.)
