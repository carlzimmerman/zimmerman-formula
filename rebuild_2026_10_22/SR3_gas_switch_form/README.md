# SR3_gas_switch_form: NO CLEAN FORM. No real form passes discs at the frozen line on either footing. Scrambled f does as well as real f, and a pure cluster label does better, so f here acts as a sample label. The T0 and T1FY planted form-recovery checks FAILED, so "nothing found" isn't a proven absence

Criteria `FROZEN_CRITERIA.md` (98ae891f33), committed alone first. Scripts `sr3_core.py`, `sr3_search.py`, `sr3_known.py`, `sr3_grade.py`, `sr3_post.py`, `sr3_acc.py`, `run_search.sh`. Numbers in `sr3_grade.out`, `sr3_grade.json`, `sr3_post.out`, `sr3_known.out`, `fronts/`, `results/`. **Not blind.** A description: no action, no field equation. Fitted constants are labelled. kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Frozen labels, per tier
PySR on BF1's train set, leaves f, y, yg, ys, at most 2 fitted, 300 iterations. Free per-galaxy Upsilon on FG1's path. It's a profile minimum, not a true marginal over a prior.

| Job | canonical | alt |
|---|---|---|
| T0, H free | NEAR, DISCS SOFT (2 rows) | NEAR, DISCS SOFT (2 rows) |
| T1F, H = 1 + f E | NEAR, DISCS SOFT (2 rows) | NO FORM |
| T1FY, also H -> 1 at high y | NO FORM | NO FORM |
| Fixed-Upsilon search, T0, graded on free path | NEAR, DISCS SOFT (1 row) | not run |
| Fixed-Upsilon search, T1FY, graded on free path | NO FORM | not run |

**Zero real rows of 141 pass G2**, so zero reach TRAIN ONLY or better. NEAR is no credit. X-COP train alone is easy: G1 passes in 98 of 141 rows. Discs are the failure, as in BF1, and free Upsilon doesn't change that.

Train and held-out law rms on the free path: canonical 0.0489, 0.0575; alt 0.0468, 0.0586. G2 line is 1.05 x law on train: 0.0513, 0.0491.

## Pareto: closest rows
Inside U and tilt, lowest train rms. c is tree complexity (T1 frame adds 4), k fitted. Every constant is fitted.

| Job | c, k | X-COP train | unseen | SPARC train / law | U, tilt | SPARC held / law | LT | Limits |
|---|---|---|---|---|---|---|---|---|
| canonical T0 | 17, 2 | +0.002, 0.068 | -0.014, 0.043 | 0.0772 / 0.0489 | 0.50, +0.00 | 0.0901 / 0.0575 | -0.016 | none |
| canonical T1F | 25, 2 | +0.001, 0.058 | +0.010, 0.095 | 0.0567 / 0.0489 | 0.50, +0.10 | 0.0611 / 0.0575 | -0.026 | f only |
| canonical fixed T0 | 16, 2 | +0.001, 0.088 | -0.042, 0.075 | 0.0573 / 0.0489 | 0.50, +0.04 | 0.0606 / 0.0575 | +0.105 | none |
| alt T0 | 17, 2 | +0.001, 0.083 | -0.034, 0.078 | 0.0567 / 0.0468 | 0.50, -0.09 | 0.0642 / 0.0586 | -0.078 | none |
| alt T0, simplest NEAR | 13, 2 | +0.001, 0.082 | -0.030, 0.079 | 0.0594 / 0.0468 | 0.51, -0.13 | 0.0741 / 0.0586 | -0.109 | none |

T1FY's lowest-loss rows with both limits pass G1 and lose elsewhere. Canonical c21: U 0.45, SPARC 0.0630, LT -0.245. Alt c25: SPARC 0.0500, held 0.0590, U 0.46, tilt +0.18, LT -0.064, the nearest on discs and low on U, with c25 and 2 fitted **not clean**. Canonical fixed T1FY c25: 0.0501, U 0.50, tilt +0.23. No front's form reads as clean: the equations are nested exp, log1p and square with steep fitted scales. Constants near 1, 2, 1/2, pi on real rows: one, 0.99589 at c7 of the fixed front, not on a graded near row, so no snapped row earns a report. Every front's rows are in `sr3_grade.out`.

Not cleaner than BF1 in any useful sense: lower complexity exists (c13-14), but it brings 2 fitted constants, where BF1 has none. BF1's best, reading only (BF2 owns it): free path 0.0576 / 0.0489, U 0.47, held 0.0783 / 0.0575, **LT +0.411**.

## Controls
- **Scrambled, f shuffled inside y deciles, sample contrast kept:** no G2 passer, so the title rule doesn't fire. But nearest inside U and tilt reads **0.0554 at c9**, against the real 0.0567 at c17 and c25. T1FY: 0.0502 at c21, U 0.48. **Real f inside a sample adds nothing visible.** Its transfer to real holdouts is worse (held 0.0878, LT -0.141). One seed.
- **Label control, f = 0 on SPARC, 1 on X-COP:** 12 rows read CLEAN on my frozen gates: c13, k 2, X +0.000, 0.075, unseen -0.024, 0.068, SPARC 0.0397 / 0.0489, U 0.52, held 0.0547 / 0.0575, LT +0.033. It reads a label, so it's no candidate. **Real forms don't beat it as a class.** Unseen-cluster rms on the nearest real rows runs 0.043 to 0.095 against the label's 0.068; the one at 0.043 has SPARC 0.0772, against the label's 0.0397. It also changes the law at f = 0 through y, so its gain on discs isn't a switch at all, and I didn't test that further.
- **Planted, H = 1 + 3 f^2 y/(1 + y^2): FAILED, both frozen recovery lines.** T1FY worst 0.046 dex, line 0.02. T0 worst 0.111, line 0.05, on a constant row. **By the criteria this voids "nothing found" for those tiers.** Post-result, no label: T1FY rows at c5-c14 have rms error 0.014-0.017 dex and pass my gates (8 rows CLEAN), but their forms aren't the plant's, e.g. exp(0.986 - y) y. So the search reaches the gates when a form exists, while **it can't recover an equation here. Any form on these fronts is a fit, not an identification.** The planted mock's G2 is also easier than the real one, since its law rms already sits at its noise floor, so this isn't equal power. T1F had no plant: the criteria listed none.

## RQ3, both footings, Bullet through B28, frozen selection
All **REJECTED**. Selected by lowest loss at c <= 15 with G1, since none passed G1-G4. Not the same as the closest rows above. Fitted constants in `candidates/`.

| Form, found on | Footing | PASS/FAIL | Keys | Keys joint p, B20 | A1, A2 | LT | A21 BTFR | A12 Z | M300, 1e14 | dkappa | Planets |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sr3_0, alt T1F, c15 | canonical | 25/19 | 12 | 0.077 | 0.0707, 0.54 | -0.103 | FAIL 0.18 | +4.93 | 3.31, 1.94 | -0.203, -0.447 | law's own fail |
| | alt | 26/18 | 13 | 0.049 | 0.0710, 0.50 | -0.133 | FAIL 0.21 | | 3.40, 1.99 | -0.206, -0.458 | law's own |
| sr3_1, canonical T1F, c14 | canonical | 22/22 | 10 | 2.5e-4 | 0.0794, 0.50 | -0.105 | FAIL 0.21 | +4.93 | 3.13, 2.00 | -0.120, -0.044 | law's own |
| | alt | 22/22 | 11 | 5.8e-4 | 0.0809, **0.42 FAIL** | -0.118 | FAIL 0.23 | | 3.34, 2.07 | -0.117, -0.071 | law's own |
| sr3_2, alt T0, c13 | canonical | 19/25 | 7 | 1.5e-6 | 0.0732, 0.58 | -0.029 | PASS 0.03 | +5.46 | 3.46, 2.04 | -0.216, -0.449 | **Z 6e10** |
| | alt | 18/26 | 5 | 6e-9 | 0.0676, 0.51 | -0.109 | PASS 0.06 | | 3.56, 2.09 | -0.222, -0.466 | **Z 6e10** |

Read these as hard as a pass:
- **Bullet FAILS in all six.** M300 is right on the record's 3.5, 2.3, within the PROVISIONAL 15 %, all |Z| under 1.1 on that sigma. **dkappa is wrong-signed at both subclusters in all six.** Amount right, place wrong, as UX6 found. Form 1 is much smaller at the sub (-0.04 to -0.07, UX3 -1.16), still the wrong sign. A form in present local (f, y) has no route to a peak on the galaxies.
- **A1 passes at 0.07-0.08 and A2 mostly passes, on all 175.** That's FG1's line, and it's looser than my G2. Against UX3's U 0.30, median U is real progress, and it costs BTFR on forms 0, 1.
- **Keys:** form 0 reads 12 canonical, 13 alt, p 0.077, 0.049; UX3's are 14 canonical, 10 alt, so alt gains and canonical loses. G-OUT-all and G-MID-T3 stay over 2. No form clears 15.
- **Dwarfs fail** like the law, as H -> about 1 for gas-free; A12 Z about +5. Lensing, TDG, A10 IC 1613 Z -4.4 to -5.1 fail. A10 got no help.
- **Planets:** forms 0, 1 are exactly the law at f = 0, so they inherit the law's own Z of order 1e4. Form 2 has no f limit and fails by 6e10.
- LT row A9 reads PASS on its soft total-error Z for -0.10 to -0.13, while my G4 fails those at |E| > 0.10.

## Physical sense
Canonical, fixed U, medians.

| Place | f | y | H sr3_0 | H sr3_1 | H sr3_2 |
|---|---|---|---|---|---|
| X-COP | 0.90 | 0.175 | 2.93 | 3.18 | 3.04 |
| X-COP inner, x 0.1 | 0.71 | 0.26 | 3.41 | 3.40 | 3.12 |
| X-COP outer, x 0.7 | 0.94 | 0.11 | 2.46 | 2.27 | 2.66 |
| LITTLE THINGS | 0.82 | 0.021 | 1.43 | 1.35 | 1.06 |
| SPARC f > 0.7 | 0.80 | 0.043 | 2.32 | 1.96 | 0.87 |
| Massive disc, outer | 0.14 | 0.11 | 1.01 | 1.03 | 0.93 |
| Bullet gas, my estimate | 0.9 | 14 | 4.34 | 21 | 5.25 |
| Saturn | 0 | 6.9e5 | 1 | 1 | 0.87 |
| f 1, y 1e4, unpinned | 1 | 1e4 | 7.87 | 1 | 7.38 |

**What stops it.** Gas-rich clusters against gas-rich dwarfs: **y, not gas share.** They differ by 0.2 in f at most, and y is about 4-9 times higher in clusters. Massive disc against cluster, at the same y: f. So H is high f times a y threshold near 0.05-0.1. That's a surface brightness-like switch at g_b near a0/10, with no reason given, and it's what clusters and dwarfs happen to occupy.

- **Only 5 of 35 X-COP rows (14 %) have a SPARC train row within 0.05 in f and 0.2 dex in y.** So on these data, (f, y) can't separate physics from sample label, which is what the two controls read.
- **The threshold bites gas-rich discs.** At f > 0.7, y 0.043, forms 0, 1 lift H by 2 or more, near the disc break UX3 found, while form 2 goes under 1. The gas-rich dwarf rows are where forms part.
- **The high-y corner is unpinned**, and it's where the Bullet's gas sits. H at (0.9, 14) spans 4 to 21 between forms with the same score. So the limit is decided by the search, not by data.

## Checks
K1-K4 and LITTLE THINGS on the law: PASS. K2 reproduces BF1's numbers within 0.001. K3 law on all 175 equals RQ3's. K5 Julia loss against Python: all 13 fronts within 1e-6. K6: harness copy, law identical to RQ3 from copied key cache (disclosed); UX3 from a **fresh** key run identical on both footings, B28 4.92, 2.44.
**MUTATE:** a0 x 1.5 fails K1 (two), K2, K3, exit 1 (`sr3_known_MUTATE.out`, `sr3_grade_MUTATE.out`). K4 and LT use the harness's a0 and don't move; that's by my construction. Under it no real, scrambled or label row reads NEAR or above, and planted rows drop from CLEAN to XDISC. The acceptance harness twin wasn't rerun here, RQ3 did it.
**Rerun:** grade byte-identical. A short 8-iteration planted job twice: csv identical. 13 full searches were not rerun.

## Errors and limits, disclosed
- Bug caught by K5 before real jobs: my Julia probes array was transposed. Fixed; real jobs ran after.
- The first grade crashed on a math domain error in the LITTLE THINGS loop at H <= 0, before any harvest printed. Fixed to read NaN and fail G4.
- **sr3_core.py was edited for that after the scripts commit**; the search isn't affected.
- The rows of X-COP outside BF1's 0.05, 0.10 and inside real errors (2 sigma on stat plus 0.12 dex HSE, about 0.24): 43 of 141 real rows. The selected forms have Z about 0 on train and unseen. A real-error gate is much looser than this one, so it doesn't rescue G2, the actual failure.
- X-COP train is 20 rows from 4 clusters and hydrostatic. Two fitted constants fit that easily.
- Loss weights SPARC against 0.110, far above the law's 0.05, so the search is weakly steered on discs while the gate is tight. **A loss with G2's line could find closer rows; I didn't run that, since it's a change after seeing results.** That's the biggest limit on "NO FORM".
- Max-norm recovery lines are harsh on a form good in the bulk, and I set them; the failure stands.
- Fixed-U search and alt runs have no own plant or control. Scrambled and label are one seed. compute_queue wasn't used; plain nice 19, two chains, load 30-60. Wall about 4 hours.
- Selected forms come from lowest loss, so sr3_0 fails U-tilt on train while A1, A2 pass on all 175. My Bullet gas (f, y) is an estimate. RQ3's overall reads REJECTED for all candidates so far, so it doesn't discriminate.

## Expectation against result
Lower complexity than BF1, fitting train: 70 %, half yes (complexity, not G2). G1 and G2 under free U: 50 %, no. G1-G4 T0 15 %, T1FY 7 %: no. U with G1, 35 %: yes for some. Bullet 3 %: no. Scrambled close to real, 60 %: yes. CLEAN 5 %: no. "y separates clusters from dwarfs, and the switch is y window times high f": yes. I didn't expect the planted recovery to fail or the label control to beat everything.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
