# FZS1 RESULT: the forest row with the law's layout only inside the settled radius

**FOREST ROW FAILS, FRAGILE (x 0.5) / FOREST ROW FAILS, FRAGILE (x 0.5) (canonical / alt). Lane label: FAILS (FRAGILE).**

Delta chi^2 is **38.7 / 36.7** against the record's gate of 4. Every known answer passes and both MUTATE arms bite.
The bracket R_set x 0.5 passes (0.19 / 0.19), so the label carries FRAGILE. R_set x 2 fails (452 / 275), and so does
reading V (39.1 / 36.9).

TEST lane, quarantined. Criteria 73defd766f. Footings are graded separately and never pooled. Cold dark energy is a
gravitating field component; no particle is added. **The rule is post hoc to FRZ1's fail.** It is not in PAPER72. A hold
under any bracket would need an independent re-grade; nothing here is a pass of form B.

## What was asked and what came out

FRZ1 laid each halo's cold dark energy out by the law out to its turnaround radius at z 2.2 to 4.4 and failed (9916 /
9009). Here the law's layout applies only inside FLD1's folded radius R_fold(z, M_b). Outside it, the cold reference's
layout is kept. The cold mass enclosed at R_set equals the reference's.

1. **The settled rule takes away 99.6 % of FRZ1's Delta chi^2, but not enough.** 9916 -> 38.7 (canonical) and 9009 -> 36.7
   (alt).
2. **The fail sits in the low-redshift bins.** z 2.2 to 2.8 fail on their own (11.9, 9.9, 5.5, 3.6 canonical). From z 3.2
   up each bin is under 1, and from z 3.8 up it is under 0.01. R_fold shrinks fast with redshift (FLD1), so the rule
   switches itself off at high z.
3. **The rule moves the 1D power by at most 5.7 % / 5.6 %** (1D ratio 0.943 to 1.000). The DESI bins at z 2.2 to 2.8 are
   precise enough to see that.
4. **What drives it: the cluster-regime haloes** (v_vir above v_stiff; at z 2.2 about 1e13 Msun/h).
   - Their baryon mass FB M200c is large, so R_set reaches about 0.8 r200m.
   - Inside R_set, their law's layout is flatter than the NFW reference, because the phantom is sourced by the extended
     gas profile. Cold mass inside 0.25 / 0.5 R_set: 0.13 / 0.37 of the mass inside R_set, against the reference's
     0.18 / 0.46.
   - So their U(k) falls: U_S / U_R is 0.991 at k 3 and 0.804 at k 10 (`fzs1_diag.out`).
   - Galaxy-regime haloes go the other way, but only slightly. Their law's shape is isothermal and cuspier than the NFW
     interior, and U rises by at most 0.3 % at k 10.

## Graded reading, per footing and DESI bin

| z | canonical R_cold at k 1 / 3 / 5 / 10 h/Mpc | canonical Delta chi^2 (bin) | alt R_cold at k 1 / 3 / 5 / 10 | alt Delta chi^2 (bin) |
|---|---|---|---|---|
| 2.2 | 0.9991 / 0.9861 / 0.9658 / 0.9118 | 11.89 | 0.9991 / 0.9858 / 0.9655 / 0.9143 | 11.51 |
| 2.4 | | 9.85 | | 9.48 |
| 2.6 | | 5.50 | | 5.20 |
| 2.8 | | 3.61 | | 3.20 |
| 3.0 | 0.9999 / 0.9970 / 0.9914 / 0.9745 | 2.21 | 0.9999 / 0.9970 / 0.9915 / 0.9759 | 2.02 |
| 3.2 | | 0.98 | | 0.87 |
| 3.4 | | 0.35 | | 0.29 |
| 3.6 | | 0.075 | | 0.055 |
| 3.8 to 4.4 | (z 4.4) 1.0000 / 1.0000 / 1.0000 / 1.0000 | 0.006 / 0.001 / 0.000 / 0.000 | (z 4.4) 1.0000 / 1.0000 / 1.0000 / 1.0001 | 0.004 / 0.001 / 0.000 / 0.000 |
| **all 755 points (full covariance)** | | **38.74 FAIL** | | **36.66 FAIL** |

Per-bin values use each bin's own covariance block. They are reported and do not sum to the total. R_cold at every bin
is in `fzs1_hm.json`.

## Brackets (reported; Delta chi^2 over 755 points, gate 4)

| bracket | canonical | alt |
|---|---|---|
| graded rule (R_set = R_fold) | 38.74 FAIL | 36.66 FAIL |
| R_set x 0.5 | **0.19 PASS (crosses: FRAGILE)** | **0.19 PASS (crosses: FRAGILE)** |
| R_set x 2 | 452.1 | 275.1 |
| reading V (virial scope, same R_set) | 39.14 | 36.93 |

The row's outcome turns on the size of the settled region within a factor of 2. FLD1's R_fold is a spherical,
law-dominated limit. FLD1 itself says that mergers and filaments may make the 3D folded region larger, and it did not
compute by how much.

## Known answers (all pass) and MUTATE (both bite)

| item | result |
|---|---|
| KA-F: FLD1's quoted R_fold from its files (canonical, z 0 / 2 / 4, log M_b 9.4 / 10.45 / 10.7 / 10.9) | PASS: 62.2 / 21.3 / 7.59; 139.3 / 47.8 / 17.24; 168.8 / 57.9 / 20.96; 196.9 / 67.6 / 24.51 |
| KA-T: R_set = r_ta reproduces FRZ1 | PASS: R_cold to 1.1e-15; Delta chi^2 9916.246 / 9008.690 equal to FRZ1's; per-bin to 1.6e-12 |
| KA-0: R_set = 0 | PASS: R_cold - 1 = 0 exactly; Delta chi^2 0 |
| KA-M: z 3, mass at r_ta conserved, non-decreasing (graded, x 2, V) | PASS: 6.6e-16 |
| KA-Z0: z 0, R_set = r_ta against CO1's R_tot | PASS: 1.4e-15 / 1.7e-15 |
| FRZ1's KA2 (R = 1 -> 0, DESI md5) and KA3 (HLF1's held reading) inside the executed pipeline | PASS / PASS |
| MS1: R_set x 10 (capped at r_ta) must fail | bites: 8626 / 8044 |
| MS2: z dependence reversed; canonical abs(R_cold(k 10) - 1) must fall at z 2.2 and rise at z 4.4 by 20 % | bites: 0.0882 -> 0.0008 at z 2.2; 0.00004 -> 0.0642 at z 4.4. Forest, reported: 10.1 / 7.5 |

## What counts against the rule (stated in advance)

**z = 0.** The same rule puts the law only inside R_fold(0) = 62 to 197 kpc at the KiDS masses. FLD1 found that radius
short of the KiDS windows and of form B's cap. What the rule does to the z = 0 redistribution (lensing not re-graded):

| footing | R_tot at k 1 / 3 h/Mpc, z 0, under the rule | CO1's R_tot (law out to r_ta) | KL1, quoted |
|---|---|---|---|
| canonical | 1.0019 / 1.0125 | 1.0033 / 1.0282 | 0.982 -> 0.972 at k 1 (C2 response); no k 3 value |
| alt | 1.0053 / 1.0389 | 1.0076 / 1.0645 | same line, as KL1 reports it |

- At z 0 the rule keeps 58 to 70 % of CO1's excess power at k 1 and 44 to 60 % at k 3.
- A rule that saves the forest by shrinking the law's region therefore also shrinks the redistribution at the lensing
  scales.
- That redistribution is form B's lensing amplitude (CO1, KL1, BX1).

**Other caveats:**
- R_fold comes from FLD1's law-dominated limit: a softened point mass, radial shells, and no cold dark energy mass in the
  shells' own gravity.
- Above log M_b 12, R_set is extrapolated as M_b^(1/3). FLD1 clamps there instead. This affects the cluster-regime
  haloes that drive the fail.
- FRZ1's inherited ingredients stay inherited:
  - present-day baryon shapes;
  - no halo list measured at z 2 to 4 (Tinker 2008's z-scaling and Duffy's c(M, z), both from memory: PROVISIONAL);
  - a linear 1D projection with no thermal or absorption physics;
  - the layout put in by hand (the joint is not derived).
- The shape inside R_set (the law's, rescaled) is a choice.
- The rule is post hoc to FRZ1's fail.

## Hand estimates against the outcome

**Mine** (criteria section 7): R_cold above 1 (centres cuspier), under 0.003 off at k <= 5 and +0.003 to +0.01 at k 10;
Delta chi^2 0.5 to 30 with even odds of a hold; x 0.5 holds; x 2 more likely fails.
- Found: R_cold below 1, and Delta chi^2 38.7 / 36.7, just above my range.
- The sign was right for galaxy-regime haloes and wrong overall. I did not think through the cluster-regime layout, where
  the phantom of the extended gas is flatter than NFW and R_set reaches 0.8 r200m.
- The brackets came out as I estimated: x 0.5 holds, x 2 fails.

**The closure chat's:** the row holds or comes close on the primary rule, and x 2 may fail.
- It came close, with Delta chi^2 down from about 9,900 to about 38, but did not hold.
- x 2 fails.

## Disclosures

- Numpy's matmul in CFG556's `U_of` prints divide-by-zero, overflow and invalid-value RuntimeWarnings, and FRZ1's own log
  has the same three. KA-T and KA-Z0 reproduce FRZ1 and CO1 to 1e-15, so they leave no trace in the numbers.
- `fzs1_diag.py` was written after the graded numbers were seen. It explains the sign and grades nothing.
- The house line "kappa = 1/2 FITTED; not theory closed." was appended after the run to the files whose writer did not print
  it (`fzs1_forest_<footing>.out`, `fzs1_diag.out`, and the local logs). A re-run differs from them by that line
  only.

## Files

- `FROZEN_CRITERIA.md`. Commits (local / origin): criteria 73defd766f / 1b686f5871 (alone, before any script or number);
  result 4d7b24c2a1 / 52696df066. Pushed by replay; no history rewritten.
- `fzs1_hm.py` -> `fzs1_hm.json` / `.out`, `fzs1_hm_MUTATE.json` (532 s, one thread). Executes FRZ1's
  `frz1_hm.py` up to its run marker, read-only, from its own path. Reads FLD1's `runs/*.json`.
- `fzs1_forest.py` -> `fzs1_forest_<footing>.json` / `.out`, `fzs1_forest_<footing>_MUTATE.json` (about
  30 s each). Executes FRZ1's `frz1_forest.py` up to the line that reads its
  `frz1_hm.json`.
- `fzs1_diag.py` -> `fzs1_diag.out` (reported only).
- The console logs `run_*.log` are gitignored (as FRZ1's are) and stay local; every number in them is in the `.out` / `.json` files.
- Nothing was downloaded. Nothing was written outside this folder.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
