# SR3_gas_switch_form: FROZEN CRITERIA (committed alone, before any script or number from this lane)

Owner's standing go, 2026-11-02. **Not blind:** BF1's README, criteria, code and L4 interim near misses, AF1, UX3, UX6, UX7, CU1 and RQ3's README and harness were read. I know the best BF1 form, its numbers, and that it isn't near-law at f = 0. kappa = 1/2 FITTED. No particle, no cold component; the cold sector stays retired and nothing here reinstates it. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Any result is a description: no action, no field equation.

BF2 tests BF1's near-miss formulas; this lane doesn't. BF1's best appears only as a known answer on the loader. BF1's run isn't touched.

## Question
Is there a cleaner closed form g = law(g_b, a0) x H, H of the gas share, than BF1's, found by PySR with gas leaves offered, on BF1's train set, that survives free per-galaxy Upsilon and the holdouts? What in it separates gas-rich clusters from gas-rich dwarfs?

## Data, BF1's split
- **Train:** odd positions of the 175 sorted SPARC names with Q < 3, inclination >= 30; X-COP clusters at sorted positions 0, 2, 4, 6, x = 0.1, 0.2, 0.3, 0.5, 0.7 R500, hydrostatic forward masses, gas plus stars.
- **Held out of all fitting:** even SPARC names, the other 3 X-COP clusters, LITTLE THINGS, everything in RQ3.

## Leaves and operators
f = gas share, clipped to [0, 1]; y = g_b/a0; yg = f y; ys = (1 - f) y. Fixed-number leaves 1, 2, pi, which aren't fitted. Operators + - * /, sqrt, square, log1p, exp. maxsize 25, depth 10, constant complexity 1. **Fitted constants: at most 2, enforced in the loss, counted and labelled "fitted" in every row.** A fitted constant within 1 % of 1, 2, 1/2 or pi is not snapped in the graded row; a snapped row is reported beside it.

## Upsilon
**Primary, free:** FG1's path. Disc U, bulge 1.4 U, per galaxy, weighted rms with FG1's weights (per-point velocity error floored at 1 km/s), per-galaxy minimum. f, y, yg, ys are recomputed at each U. The search grid is U in {0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1.00, 1.20}. **Grading is on FG1's 0.01 grid, all gates.** Minimising over U is a profile, not a true marginal over a prior; disclosed.
**Comparison, fixed:** BF1's disc 0.5, bulge 0.7, unweighted pointwise rms.

## Tiers
- **T0:** tree is H, free.
- **T1F:** H = 1 + f E, tree is E. H -> 1 at f -> 0 unless E diverges there, checked.
- **T1FY:** as T1F, plus a penalty on |log10 H| at y from 1e6 to 1e12, f from 0.1 to 1. Search penalty 100 x (max |log10 H| on those probes)^2 when above 1e-3.

H must be finite and positive on all rows. Reported complexity counts the tree; T1 frames add 4 nodes, reported.

## Loss, in the search
(rms_S / 0.110)^2 + (mean_X / 0.05)^2 + (rms_X / 0.10)^2 + P_U, where rms_S is the free path's, and P_U = (distance of median log10 U outside log10 [0.50, 0.80] / 0.05)^2. Fixed-path runs use rms_S as BF1's over 0.1747 and no P_U.

## Jobs
canonical free T0, T1F, T1FY; alt free T0, T1F, T1FY; canonical fixed T0, T1FY; scrambled and planted at canonical free T0 and T1FY; label control at canonical free T0. Same operators, seed, iterations. PySR 1.5.9, serial, one Julia thread per job, nice 19, at most two jobs at once. Iterations 300, cut by an amendment only, before real jobs, if a timed planted run shows the full list over 8 hours. A killed job restarts from scratch; a finished job's csv is never rerun.

## Gates, per form, per footing
Errors: SPARC per-point eV, as FG1 weights it. X-COP stat from EM_FORW, with 0.12 dex HSE systematic from RQ3's `tolerances.json`. LITTLE THINGS sE 0.075 per system. Reported Z on those for each X-COP mean.
**BF1's 0.05, 0.10 is a search line, tighter than the real error: |mean| under 2 sigma on stat and HSE would be about 0.24.** Gate uses BF1's line, so results compare. Any row outside BF1's line and inside real errors is printed as such.
- **G1 X-COP train:** |mean log10(M_HSE/M)| <= 0.05, rms <= 0.10.
- **G2 SPARC train, free path:** rms <= 1.05 x the law's same statistic on the same set; median U in 0.50-0.80; |tilt| <= 0.15 on the train galaxies' FG1 definition. Rows passing all but the 1.05 line and with rms <= 0.110 (FG1's own line) read G2-SOFT.
- **G3:** same as G1 and G2 on the held-out clusters and even names.
- **G4 LITTLE THINGS:** |median E| <= 0.10, gas from Oh+ 2015, as in RQ3.
- **Limits:** H at f = 0 exactly, y from 1e-4 to 1e9, |H - 1| <= 1e-3 (F-LIMIT); and <= 1e-10 at f = 0 (F-EXACT: what Saturn's bound can need). H at y from 1e6 to 1e12, f from 0.1 to 1, |log10 H| <= 1e-3 (Y-LIMIT). Checked on every graded row, whatever its tier.

## Top few
At most 3 forms overall go to RQ3's `acceptance.py`, unchanged code, on both footings, reading Bullet through its B28, UX6's path, and keys. Order: forms passing G1-G4, lowest complexity, at most one per tier; if fewer than 3, forms by lowest train loss at complexity <= 15 with G1 passing, one per tier and footing. Acceptance outputs go in this lane, not RQ3's. Each runs on both footings with the formula unchanged; the footing it was found on is stated. Acceptance rows are read, not a gate for the label below: every candidate there so far reads REJECTED.

## Labels
- **CLEAN FORM:** G1-G4, complexity <= 15, at most 2 fitted, on the footing it was found on, and on the other footing with the formula unchanged, stated.
- **FORM, NOT CLEAN:** G1-G4, complexity above 15.
- **X-COP AND DISCS ONLY:** G1-G3, fails G4.
- **TRAIN ONLY:** G1, G2, fails G3.
- **NEAR, DISCS SOFT:** G1 and G2-SOFT only. No credit.
- **NO FORM:** nothing passes G1 and G2.
Given per tier and footing. A1 limit fail on a T0 form is printed beside its label. **A form passing with limits failed can't be called a law reduction on stars-only systems.**

## Controls
- **Scrambled:** f replaced within each sample by f from another row in the same y decile, at each U, yg and ys recomputed. X-COP train: f permuted across rows, as BF1. So sample-level f contrast survives; a front that matches the real one means f acts as a sample label. If scrambled yields a G1 and G2 passer at the same or lower complexity, the title says so.
- **Label control:** f replaced by 0 on SPARC, 1 on X-COP, yg and ys recomputed. A pure switch. The real form must beat this on the held-out clusters or say it doesn't. On SPARC the label can't lose; real rows are printed beside it.
- **Planted:** mock with H = 1 + 3 f^2 y/(1 + y^2), true U 0.6 scattered by 0.1 dex per galaxy, Gaussian noise at each row's FG1 error floored at 0.05 dex, X-COP at 0.05 dex. PASS: at complexity <= 15, max |log10 H_found - log10 H_plant| <= 0.02 dex over the train rows' (f, y) for T1FY, and <= 0.05 for T0. A fail is published and voids that tier's "nothing found".

## Known answers (grader, before any harvest)
- K1 H = 1, X-COP all 7: +0.4675, 0.4763 within 0.001; SPARC fixed train 0.1664.
- K2 BF1's best form, reading only: train 0.184, -0.012; X +0.033, 0.099; held-out X -0.009, 0.077; held-out SPARC 0.213; within 0.001.
- K3 law on the free path, all 175: equals RQ3 `results/law.json` A1, A2 within 1e-4.
- K4 UX3's term, k fit, free path, all 175: rms 0.0907, U 0.30, tilt -0.05 as RQ3 reads, within 0.001; X-COP all 7 -0.016, 0.089.
- K5 Julia's loss against the Python grader's on the search grid, law and one test form, relative 1e-6.
- K6 acceptance copy in this lane, law: same PASS, FAIL counts as RQ3's on both footings. M300 law 1.11, 0.73; UX3 4.92, 2.44 through B28.
- **MUTATE:** grader with a0 x 1.5 labelled the law must fail K1 and K3, exit 1. Rerun of grading byte-identical. PySR search reruns are not all done; one short planted job is rerun for identity.

## Physical sense, reported for every form graded
H at: X-COP's median (f, y); LITTLE THINGS; SPARC f > 0.7 rows; massive disc outer rows; Bullet gas; Saturn. Overlap: share of X-COP train and unseen rows with a SPARC row within 0.05 in f and 0.2 dex in y; if near zero, (f, y) can't separate physics from sample label here. Named: what stops the term in gas-rich clusters against gas-rich dwarfs. H at f near 1 and high y, a place no data pins.

## Expectation, mine, on record
T0 finds a form at lower complexity than BF1's, fitting train: 70 %. G1 and G2 under free Upsilon: 50 %. G1-G4 at T0: 15 %. T1FY G1-G4: 7 %. Median U passes with G1: 35 %, as UX3's U 0.30 is the known danger. Bullet passing: 3 %. Scrambled's front close to real: 60 %. CLEAN FORM: 5 %. Most likely: y separates clusters from dwarfs, and the "switch" is y window times high f.

## Compute
Nice 19, one Julia thread per job, two jobs at most, under 4 GB per job. BF1 and AR1 untouched. No downloads.
