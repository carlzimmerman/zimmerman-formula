# HLF1 RESULT: CO1's redistribution rows with the record's own halo list, and the forest row computed for form B

**NO VERDICT / NO VERDICT (canonical / alt).**

- **Part A, the halo list.** As frozen: NO VERDICT / NO VERDICT, because mutation arm MA1 did not bite. Under AMENDMENT A1
  (post hoc; committed before any row was computed): **ROWS HOLD WITH THE OWN LIST / ROWS HOLD WITH THE OWN LIST**, with
  c(M) and masses below M_lo still inherited. A result that reads as a hold needs an independent re-grade; it is not a pass.
- **Part B, the forest row.** **NO VERDICT / NO VERDICT.** The record's forest gate (Delta chi^2 <= 4) fails when CO1's z = 0
  redistribution is held to the forest's redshifts: 160.7 / 1025.6. It passes trivially (0) under the record's fade, which
  removes the redistribution above z = 1. The row turns on how the redistribution evolves from z 0 to z 3, and the record
  does not compute that.

TEST lane, quarantined. Criteria 123947b9dc; amendment A1 657e245086. Footings are graded separately and never pooled.
Cold dark energy is a gravitating field component; no particle is added. Nothing here says the data favour the framework.

## What was asked and what came out

1. **The record's own run left no particle positions.** CFG596's S0 run (L100, 1024^3) saves positions only when N <= 512.
   It left 256^3 block means of the density (cells of 0.39 Mpc/h). The own halo list is therefore measured with a
   spherical-overdensity finder on that grid.
2. **The grid resolves halos of M200m from 1e13 to 5.6e14 Msun/h, and that range carries 60 % / 55 % of the
   redistribution at k = 1 h/Mpc.** Planted NFW halos are recovered to 4 to 9 % (median) from 1e13 upwards. In the range,
   the run has 0.59 to 1.45 times Tinker 2008's counts and 0.82 to 1.13 times Tinker 2010's bias.
3. **With the own mass function and bias in that range, CO1's rows do not move.** On KiDS, d_cold goes from +1.148 to
   +1.153 (canonical) and from +2.206 to +2.282 (alt), both CONSISTENT. On PR4 lensing r_eff - 1 stays +0.00003 / +0.00005
   (PASS). R_cold at k = 1 is unchanged; at k = 5 it goes from 1.090 to 1.075 and from 1.159 to 1.149. CO1's lane label stays
   ROWS HOLD on both footings.
4. **The forest cannot be decided with what is on disk.** Form B changes the forest relative to the cold reference only
   through the redistribution (rule 5). The law is not a force on the IGM gas, and the forest's gas is in the falling-clock
   regime (rule 3). CO1 computed the redistribution at z = 0 only. Held at z 2.2 to 4.4 it changes the 1D power by +1.0 to
   +3.3 % (canonical) and +3.3 to +10.0 % (alt), which DESI DR1 rejects at Delta chi^2 161 / 1026. Faded as the record's
   shear lanes fade it, it is zero there. Which reading is right depends on the layout of halos at z ~ 3, which no lane has
   computed.

## Part A table (z = 0; CO1's pipeline copied, inherited list against own list)

| row | canonical, inherited (CO1) | canonical, own | alt, inherited (CO1) | alt, own | line |
|---|---|---|---|---|---|
| f_res at k 1 / 3 (resolved share, A.2) | 0.604 / 0.626 | | 0.551 / 0.627 | | >= 0.5 for a label |
| R_cold at k 1 / 3 / 5 h/Mpc | 1.006 / 1.051 / 1.090 | 1.006 / 1.052 / 1.075 | 1.010 / 1.088 / 1.159 | 1.010 / 1.094 / 1.149 | reported |
| **C4** PR4 lensing r_eff - 1 | +0.00003 PASS | +0.00003 **PASS** | +0.00005 PASS | +0.00005 **PASS** | within 0.0481 |
| C4 shape chi^2 | 8.56 | 8.56 | 8.56 | 8.56 | <= 18.48 |
| **C5** raw KiDS-1000 d_cold (104 points) | +1.148 CONSISTENT | +1.153 **CONSISTENT** | +2.206 CONSISTENT | +2.282 **CONSISTENT** | klass |
| robust widen2 / noIA / fade / DESI | +0.55 / +1.99 / +0.88 / +0.72 | +0.57 / +1.96 / +0.88 / +0.72 | +1.15 / +3.70 / +1.65 / +1.44 | +1.20 / +3.80 / +1.70 / +1.50 | all < 9 |
| tooth chi^2_min (null 1.11) | 1.01 NOT VISIBLE | 1.00 NOT VISIBLE | 1.15 NOT VISIBLE | 1.15 NOT VISIBLE | >= 9 visible |
| CO1 lane label | ROWS HOLD | ROWS HOLD | ROWS HOLD | ROWS HOLD | |

- **The own list** (`hlf1_halos.out`). 1855 halos were found, 455 of them above M_lo = 1e13 Msun/h. Seven 0.25-dex bins
  run to M_hi = 5.62e14; the largest halo is 7.8e14. Counts against Tinker 2008 (r_j): 0.785, 0.939, 0.994, 0.657, 0.591,
  1.107, 1.453 (191, 131, 77, 27, 12, 10 and 5 halos). Bias, by 0.5-dex bin against Tinker 2010: 1.09 +- 0.07 against 1.23,
  1.34 +- 0.10 against 1.64, 2.69 +- 0.25 against 2.39, 3.37 +- 0.64 against 3.55. All four bins are used; the last one's
  error is 19 %, just inside the 20 % rule.
- **Reported bracket (A1): own list only from 5e13 up.** d_cold +1.146 / +2.261; R_cold at k 5 1.075 / 1.147. Same labels.
- **Brackets under the own list (reported, never graded).** CO1's brackets were re-run on the own list. Every one stays
  inside CO1's band except one: c(M) x 0.7 on alt is +4.25, past the TENSION line (4.00 with the inherited list).
  Canonical c(M) x 0.7 is +2.62. Lagrangian scope (M4): +1528 / +1638. So the part of the list this run cannot see,
  c(M), still moves d_cold more than the part it can.

## Part B table (DESI DR1 P1D, 755 points, z 2.2 to 4.4; gate Delta chi^2 <= 4; form B's own spectrum as the reference)

| reading | canonical | alt | gate |
|---|---|---|---|
| **H**: CO1's R_cold held in z | **160.74 FAIL** (ratio 1.0099 to 1.0335) | **1025.57 FAIL** (1.0327 to 1.0998) | <= 4 |
| **F**: the record's fade (R - 1 scaled by 1 - z, zero above z 1) | **0.00 PASS** | **0.00 PASS** | <= 4 |
| **Part B label** | **NO VERDICT** (readings disagree) | **NO VERDICT** | |
| reported: H with R = 1 above 10 h/Mpc | 196.56 | 665.91 | |
| reported: H with Part A's own-list R_cold | 99.88 | 852.69 | |
| reported: H per z (own covariance block) | 1.3 to 20.7, largest at z 3.0 to 3.2 | 9.3 to 132.1, largest at z 3.0 to 3.2 | |
| reported: form B's spectrum against the pipeline's original reference | 1518.9 (ratio 1.081) | 1753.6 (1.087) | not a gate |

- **The row and its gate, as the record states them.** PD1 P4 (FROZEN_CRITERIA line 44, RESULT line 113) carries "forest
  Delta chi^2 0" from WM1 gate 8 (FROZEN_CRITERIA line 76): `ss1_cosmo.forest_eval` on DESI DR1 P1D, gate Delta chi^2 <= 4.
  It is a gate on a modification at fixed parameters, not an absolute fit to the data. The record's absolute forest models
  (P1D1, P1D2, P1D4) are all NOT DIAGNOSTIC.
- **Why reading H fails.** CO1's R_cold is 1.05 to 1.09 (canonical) and 1.09 to 1.16 (alt) at 3 to 5 h/Mpc, and the forest's
  projected power integrates exactly that range. DESI's errors are at the percent level on 755 points.
- **Why it is not a FAIL label.** CO1's R_cold describes halo interiors at z = 0. At z 3 the nonlinear mass is
  roughly a thousand times smaller (hand estimate). The forest's gas also sits mostly outside the haloes. Holding the z = 0 ratio there
  very likely overstates it, but by how much is not computed, so the frozen rule gives NO VERDICT.
- **The reported last row is not a gate.** The pipeline's original reference has A_s fixed at a placeholder of 2.0e-9.
  Form B's fitted amplitude (sigma8 0.8405 / 0.8429) is 8 % above it in power, and the statistic sees that. It is a
  difference in parameters, not a rule of form B.

## Known answers and MUTATE

| item | result |
|---|---|
| KA-A1 planted halos | PASS. Median deviation 0.089 at 1e13, 0.032 at 2e13, 0.037 at 3e13, 0.012 at 5e13, 0.022 at 1e14, 0.009 at 3e14 and 0.004 at 1e15 (largest 0.162 at 1e13). M_lo = 1e13; every 3e14 and 1e15 halo is within 0.02. The finder reads 1 to 5 % low (cell discreteness) |
| KA-A2 Tinker 2008 (reported) | Poisson chi^2 20.7 on 7 bins; every bin's ratio is inside [0.5, 2] |
| KA-A3 inherited list put back | PASS, exact: 632 halo-model arrays, 128 linear, 190 shear and 270 row scalars match CO1's stored JSON with difference 0; CO1's labels are reproduced |
| KA-A4 bias code | PASS: 1.481 +- 0.162 against the 1.538 expected (Poisson field, b0 = 2 smoothed) |
| CO1's own KA1 to KA7, KA_limber, in every run | PASS (after the code fix below) |
| KA-B1 carried row | PASS: R = 1 gives 0 exactly; DESI md5 matches |
| KA-B2 WM1 MN-W replay | PASS: 167379.35 / 167378.92, equal to the stored values (relative difference 0) |
| MA1 (finder sees structure), as frozen | **DOES NOT BITE**: 160 of 455 above 1e13 in the cell-permuted grid |
| MA1 restated (A1, above 5e13) | bites: 0 against 71 (above 2e13: 18 against 236; above 1e14: 0 against 29) |
| MA2 (finder sees growth) | bites: 199 at z 1 against 455 at z 0 |
| MA3 (list reaches the rows) | bites: doubling every r_j changes P_std at k 1 by +57.9 % |
| MB1 3 keV warm cutoff | bites: 3775.0 / 3772.6 |
| MB2 candidate B's R held | bites: 20596 / 44364 |
| CO1's M1 to M3, M4 restated | bite in every run; M4 as frozen does not (as in CO1) |

- **Code fix, disclosed.** In the first own-list run, CO1's KA2 null failed (8.2e-2). My copy computed KA2's reference
  spectrum under the Tinker population, before it switched to the own list. The fix recomputes it after the switch
  (`hlf1_hm.py`, comment "HLF1 code fix"); it is identical for the inherited list, and KA-A3 still matches exactly. The
  graded arrays do not use that reference. Re-running the own-list linear and shear steps on the regenerated file gave
  JSON identical to the first run (timings aside). The own5e13 linear and shear files were not re-run: they read the same
  graded arrays, which the fix does not touch.
- **What MA1 showed.** Below about 4e13 Msun/h the finder cannot tell a halo from one dense cell. The densest cell holds
  3.96e13. In the run those cells are halo cores, but the planted test used smooth profiles only. The from-5e13 bracket
  moves nothing (d_cold +1.146 / +2.261).

## Hand estimates against the outcome

- M_lo: estimated 2e13 to 5e13; found 1e13. Halos above it: estimated 100 to 200; found 455. M_hi: estimated 2e14 to 5e14;
  found 5.6e14.
- f_res: estimated 0.4 to 0.7; found 0.60 / 0.55. Counts against Tinker: estimated 0 to 40 % high (the high draw); found
  0.59 to 1.45, mixed in sign, so the draw does not show as an excess in counts. Rows: estimated to hold with a shift below
  1; found shifts of +0.005 / +0.076.
- Forest, reading H: estimated 10^2 to 10^3; found 161 / 1026. Reading F: 0, as built. Label: NO VERDICT, as estimated.
  MB1: estimated 10^2 or more; found 3.8e3. MB2: estimated 10^4; found 2.1e4 / 4.4e4.

## What is still inherited

- c(M) at every mass (the grid cannot see a scale radius); every mass below 1e13 and above 5.6e14 Msun/h (masses above
  5.6e14 carry 19 % / 23 % of the k = 1 signal, masses below 1e13 carry 21 % / 22 %); and CFG556's declared baryon shapes
  (S0 is gravity-only).
- The bias in the resolved range is the run's only through the ratio to Tinker 2010 inside each 0.5-dex bin.
- The run is one 100 Mpc/h box with a high large-scale draw. The counts are the run's own and are not corrected.
- In Part B: CO1's R_cold at z = 0, the linear 1D projection of the record's pipeline (no thermal or FGPA physics), and the
  layout itself (put in by hand: open item 1).

## Not computed, only estimated, or PROVISIONAL

- **Not computed: the redistribution at the forest's redshifts.** This is the one number Part B needs.
  - The halo model would have to be evaluated at z 2 to 4.4: Tinker 2008 with its z-dependent parameters, the layout's
    v_vir and turnaround at z, and a0 constant.
  - A frozen statement would be needed of what rule 5 does with the charge of haloes that are still assembling.
  - That is a new lane of minutes of compute.
  - An own list at those redshifts cannot be measured: the S0 run saved block means only at z <= 1 (and z 49). It would
    need a new run saving z 2 to 4 snapshots.
- **Not run: a positions-saving rerun of S0.** It would give an own list below 1e13 and own concentrations. The run is
  9.3 h at 14 threads and 42 GB resident (CFG596's log), and a 512^3 version would not resolve below about 1e12 either. Not
  started: it is far over this lane's limits.
- **Not computed:**
  - a second, independent finder (friends-of-friends on the N256 S0 runs that have positions: different seed and
    resolution);
  - concentrations;
  - the alt footing's own PM run (S0 is footing-free);
  - CMB lensing above L 400.
- **Only an estimate:** that holding the z = 0 ratio overstates the forest signal (argued, not computed).
- **PROVISIONAL:** nothing in this lane rests on a web look-up. DESI's fiducial f sigma8 inside CO1's C3, which is
  re-executed here, was transcribed from memory there.

## Files

- `FROZEN_CRITERIA.md` (123947b9dc), `AMENDMENT_A1_2026-11-11.md` (657e245086).
- `hlf1_halos.py` -> `hlf1_halos.json/.out` (7 s); `_MUTATE` (MA1 as frozen, MA2; 10 s); `hlf1_ma1_check.py` ->
  `hlf1_ma1_check.json/.out` (MA1 restated; 10 s).
- `hlf1_hm.py`, `hlf1_linear.py`, `hlf1_shear.py`, `hlf1_grade.py`: copies of CO1's scripts. `HLF1_LIST` is
  inherited, own or own5e13. They write `hlf1_hm_*`, `hlf1_linear_*`, `hlf1_shear_*`, `hlf1_rows_*` and `hlf1_hm_MUTATE.*`
  (MA3). Run times: 80 to 103 s, 17 s, 247 to 277 s and under 1 s per list; peak RSS 0.84 GB.
- `hlf1_ka_a3.py` -> `hlf1_ka_a3.json/.out`.
- `hlf1_forest.py` -> `hlf1_forest_<footing>.json/.out` (24 s each) and `_MUTATE` (MB1, MB2; 15 s each).
- `run_*.log`: the console logs.
- Read-only inputs: CFG596's S0 block means, CFG556's library, CO1's stored JSON, the F1A fits, SS1's `ss1_cosmo.py`
  prefix, WM1's stored MN-W row and DESI DR1 P1D. Nothing was downloaded. Nothing was written outside this folder.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
