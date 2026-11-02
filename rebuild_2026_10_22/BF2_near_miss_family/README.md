# BF2_near_miss_family: REJECTED, the best forms read NEAR MISS, DISCS AND CLUSTERS on the frozen label and die on galaxy lensing, groups, stars-only systems and the Bullet. NOT ABOVE CONTROL

Criteria `FROZEN_CRITERIA.md` (6d697dea87), committed alone first. `AMENDMENT_A1.md` (c6ff1733e8), post-result, before its runs. **Not blind**: the forms were already seen and came from about 1.7e11 tries. A description: no action, no field equation, no fitted float. **NEAR MISS is the ceiling here; a second implementation is owed before anything beyond it, and none has been written.** BF1's NO HIT at Stage 1 stands; its run is untouched and still going. kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

## Read this first
- **NOT ABOVE CONTROL.** Scrambled train clusters give 0, 15 and 266 hits where the real data give 19, on the same jobs. Everything below is on forms from a search that doesn't beat its own control.
- **Your suspicion about the statistic was right.** On BF1's fixed Upsilon rms, 0 of 3,952 hits clear the line. On FG1's free Upsilon, 3,943 clear rms 0.110 and 715 also hold Upsilon 0.50-0.80 (canonical). Rank agreement between the two is only +0.46. The line is generous, though: the law reads 0.054, these 0.069-0.095.
- **So the frozen label is reached.** P7 and P8 hold it on both footings: A1, A2, A3, A4, A9, X-COP all 7, 14 of 15 keys. **Both are post-result picks under A1, two of eight forms put through keys.** P3, picked by the frozen rule, reads **15 of 15 keys on both footings**, with no fitted float, and misses A2 at U 0.47, 0.45, so its frozen label is X-COP ONLY.
- **It isn't a law.** Each fails, by a wide margin, things the discs and clusters don't test:

| Kill | P3 | P7 | P8 | a0 law | What goes wrong |
|---|---|---|---|---|---|
| A30 galaxy lensing, chi^2/56, Z | 885, +78 | 846, +75 | 845, +75 | 154, +9.3 | The cut-off. Model/data 0.2-0.4 by bin, outer radii 0.03-0.06 |
| Groups at assumed f 0.3-0.85, Z | -9.2 to -7.2 | -8.9 to -6.6 | -8.8 to -6.6 | passes | Same cut-off: model short 0.35-0.49 dex |
| Saturn, stars-only, Z | 9.7e3 (the law's) | 2.4e9 | 1.7e9 | 9.7e3 | P7, P8 have H(f=0) 0.64, 0.75: gravity 36 %, 25 % below Newton at a planet |
| Bullet, local f | DEAD | DEAD | DEAD | fail | dkappa wrong sign at both, peaks by the gas |
| TDG chi^2 (A23a, line as RQ3) | 69 | 82 | 85 | 10.8 | |

- **The new form trades one failure for another.** Family (a), the rewritten gas term, has no cut-off: at assumed f >= 0.6 groups pass, and lensing fails less hard (Z +16 to +28), but with H(f=0) below 1 it breaks stars-only rows. Family (b), the cut-off you noticed, protects gas-rich dwarfs and that same protection starves everything at low acceleration with any gas: weak lensing and groups. LITTLE THINGS sees y near where the cut-off turns on; lensing sees y down to 1e-4.

## Step 1, families
Snapshot: 4,018 lines, sha256 eec6238b…, 363,814 jobs. Later lines not used. 3,952 scored; 66 non-finite on BF1's own rows, listed in `bf2_scan.json`. 1,307 structural families, `bf2_scan.out`. Both f and y: 3,950; ell: 1,544; H(f=0) = 1 identically: 122. W3 3,223, W2 508, W1 221. My counts by rough regex on the signature, not a clean partition:

| Class | Hits | Example, simplest of the largest family | Plain words | Median U, LT | S <= 1 |
|---|---|---|---|---|---|
| (a) grows with f y | 2,692 | `log1p(f+1) + 12.3 y f` (W3) | **UX3's term again**: law x (c + k g_gas/a0), k = 5/ln 1.5 = 12.33 or pi^2. A rewrite, not a new form. Nothing at f = 0 protects a star-only system: c is 0.69 here | 0.40, -0.156 | 19 |
| (b) cut-off at low y | 1,052 | `inv1p(sqrt(f)/(pi y)) x sq((f+1/2)(f+2))` (W2, P3) | Multiply the source by a rising function of gas share, then switch it off where f/y is large, that is, gas-rich at low acceleration. **New against UX3's switches, as you said:** it needs no label, only f, y | 0.45, -0.136 | 17 |
| other | 208 | mixed | | 0.48, -0.081 | 3 |

S is the largest of rms/0.110, |U-0.65|/0.15, |tilt|/0.15, |LT|/0.10, X-COP mean/0.05, rms/0.10.
**A coincidence to not over-read:** P2 and P5 read C1 PASS, Z 3e-8, since inv1p(inv1p(y)) = (1+y)/(2+y) cancels the law's 1 + 1/y - 1/y^2 through second order at f = 0. So they restore Newton at planets, by a term picked from 1.7e11 tries, and halve the law at low y (H 0.5), which breaks dwarfs (A12 Z +7.4). f = 1 at Saturn is Z 5.7e16. **The Sun is gas physically; f = 0 is a labelling choice.** Every form here needs "stars" to be a category the field can read.

## Step 2, why SPARC breaks. `bf2_sparc.out`
Canonical, Q <= 2, free Upsilon rms (fixed Upsilon rms in brackets). Alt is in the file.
| | Law | P1 | P3 | P7 | P8 |
|---|---|---|---|---|---|
| all: rms, U, tilt | 0.054, 0.52, +0.02 | 0.069, 0.50, +0.06 | 0.072, 0.47, +0.04 | 0.076, 0.55, +0.09 | 0.080, 0.60, -0.14 |
| V 1-60 (n 12) | 0.093 (0.179) | 0.246 (0.297) | 0.224 (0.293) | 0.239 (0.338) | 0.238 (0.308) |
| V 60-100 (n 35) | 0.107 (0.197) | 0.143 (0.238) | 0.183 (0.235) | 0.206 (0.260) | 0.204 (0.237) |
| V 150-200 (n 25) | 0.035 (0.129) | 0.050 (0.148) | 0.048 (0.150) | 0.053 (0.138) | 0.056 (0.141) |
| gas tercile low (n 51) | 0.047 (0.139) | 0.050 (0.144) | 0.051 (0.147) | 0.048 (0.168) | 0.054 (0.176) |
| gas tercile high (n 51) | 0.106 (0.209) | 0.168 (0.266) | 0.187 (0.259) | 0.209 (0.291) | 0.208 (0.269) |
| U at floor 0.30, of 153 | 29 | 35 | 40 | 35 | 35 |

**The break is gas-rich slow galaxies, where rms doubles.** Massive gas-poor discs stay near the law. The worst galaxies at fixed Upsilon (CamB, UGC 7577, UGC 11557) are the law's worst too, and no form rescues them. My reading: the overall rms passes because well-measured massive discs dominate the weights. More galaxies also sit at the Upsilon floor, so free Upsilon hides some damage. **Passing rms 0.110 at up to twice the law's scatter is a weak pass.**

Surface-brightness slope A4: all pass; P1 +0.09, Z 1.15; P3 +0.067, Z 0.81; P7 +0.026; P8 -0.015; law -0.016. LITTLE THINGS A9: P1 **+0.411, Z 3.21, fails its line**; P3 +0.129, Z 1.67; P7 +0.075; P8 +0.072; law -0.025. **P1, BF1's interim best, is the form that fails here most clearly: the cut-off over-protects.**

## Step 3, RQ3 on both footings. `results/`, `bf2_k1.out`. Tolerances unmoved, |Z| <= 2
P1-P4 frozen rule. P5-P8 Amendment A1. Row counts of 96; computed 44 (43 for P8), as RQ3 records for gas-reading g. All REJECTED; p_joint below 1e-50 every time, on lens or solar.
| Form, wrap, H | Footing | PASS / FAIL | Keys, over 2 | A1, A2 | A3 tilt | A9 LT | X-COP 7 | B25 | Label |
|---|---|---|---|---|---|---|---|---|---|
| a0 law | can | 22 / 25 | 10 | .054, .52 | +.02 | -.025 | +.468, .476 | -3.04 | BROKEN |
| | alt | 20 / 27 | 10 | .054, .44 | -.02 | -.064 | +.435, .444 | -2.86 | BROKEN |
| P1 W3 `sq((f+2)/inv1p(f)) inv1p(f+pi+f/y)` | can | 24 / 20 | 10; Mall +4.1, M3 +4.0 | .069, .50 | +.06 | **+.411** | +.015, .090 | pass | none fits: A9 fails |
| | alt | 22 / 22 | 10 | .069, **.48** | +.14 | **+.448** | +.025, .091 | pass | X-COP ONLY |
| P2 W3 `inv1p(inv1p(y)) + log1p(log1p(f)) + 12.33 y f` | can | 26 / 18 | 13; MID-T3 +2.00, OUT-all -2.85 | .095, .52 | -.04 | -.057 | +.001, .088 | +.61 | none fits: 13 keys |
| | alt | 23 / 21 | 10; OUT-all -3.27 | .093, .50 | -.13 | -.088 | +.020, .089 | -.47 | none fits |
| **P3** W2 `inv1p(sqrt(f)/(pi y)) sq((f+.5)(f+2))` | can | 28 / 16 | **15, max |Z| 1.53; M3 Ztot +0.45, joint p 0.72** | .072, **.47** | +.04 | +.129 | -.029, .098 | +1.29 | **X-COP ONLY** |
| | alt | 28 / 16 | **15, max 1.68; +0.56, p 0.65** | .071, **.45** | +.06 | +.131 | -.015, .093 | +.63 | **X-COP ONLY** |
| P4 W3 `log1p(f+1) + 12.33 y f` | can | 22 / 22 | 10 | .092, **.46** | -.15 | -.098 | -.004, .088 | +.70 | X-COP ONLY |
| | alt | 21 / 23 | 10 | .091, **.42** | -.17 | -.129 | +.014, .087 | -.44 | X-COP ONLY |
| P5 W3 | can | 26 / 18 | 13; MID-T3 +2.07, OUT-all -2.64 | .093, .57 | +.06 | -.030 | +.003, .090 | +.59 | none fits |
| | alt | 24 / 20 | 10 | .090, .55 | -.02 | -.060 | +.024, .091 | -.54 | none fits |
| P6 W3 | can | 22 / 22 | 10 | .091, .57 | -.11 | -.060 | -.001, .089 | +.71 | none fits |
| | alt | 21 / 23 | 10; joint p .036 | .088, .56 | -.13 | -.092 | +.016, .089 | -.53 | none fits |
| **P7** W2 `sq(sqrt2 + pi f) / (inv1p(inv1p(y)) (1/(2y) + pi))` | can | 28 / 16 | **14; OUT-all -2.16** | .076, .55 | +.09 | +.075 | -.003, .092 | +1.28 | **NEAR MISS** |
| | alt | 29 / 15 | **14; OUT-all -2.14** | .076, .52 | +.09 | +.075 | -.002, .091 | +.61 | **NEAR MISS** |
| **P8** W3 `sq(inv1p(ell) + 2f) / sqrt(sqrt(pi) + f/y)` | can | 27 / 16 | **14; OUT-all -2.24** | .079, .60 | -.14 | +.072 | +.010, .093 | +1.19 | **NEAR MISS** |
| | alt | 27 / 16 | **14; OUT-all -2.21** | .078, .55 | -.14 | +.073 | +.008, .092 | -.71 | **NEAR MISS** |

Compare UX3's fitted term: canonical 14, alt 10, A2 U 0.30. These forms, with no fitted float, do as well or better on keys and much better on A2. G-OUT-all is again the row that won't clear, as in UX3, on P2, P4-P8.

**Other failures, both footings, P3 (P7) canonical:** A5 +4.2 (+5.0), A6 +6.0 (+6.4), A7 -2.6 (pass), A10 IC 1613 -3.2 (-3.6), A12 dwarfs +4.9 (+10.4), A13 +7.8 (+9.8), A20 pass (-5.0), A21 BTFR 0.12, 0.13 dex fail, A23a 69 (82), A23b -3.3 (pass, -1.8), A24 +2.3 (+6.0), A26a +3.2 (+5.4), A30, B2 +3.6 (+3.2), B28, C1. Dwarf rows run at f = 0 because the harness gives them no gas, as for UX3; **a reading with their real gas isn't computed**, and the harness's stars-only rows are worst hit where H(f=0) isn't 1. NOT COMPUTABLE stays so: A11, A14, all action rows, CMB, B1 and A15-A17 (no gas on file).

### Reported beside, never in place: assumed f. `bf2_supp.out`, `bf2_supp2.out`. PROVISIONAL inputs of mine
| | Groups f 0.3, 0.6, 0.85, Z canonical | Milky Way f 0.05: A15 K, A16 | f 0.15 |
|---|---|---|---|
| P1 | -10.2, -10.1, -9.6 | 69.4, FEASIBLE IN PRIORS | 64.7, wide priors only |
| P2 | -2.3, -1.0, -0.4 | 80.4 Z +3.5, V+K ONLY | 98.5 Z +8.1, INFEASIBLE |
| P3 | -9.2, -8.0, -7.2 | 70.2, FEASIBLE IN PRIORS | 67.0, INFEASIBLE |
| P4 | -1.5, -0.5, +0.1 | 74.1, V+K ONLY | 97.5, INFEASIBLE |
| P7, P8 | -8.9, -7.5, -6.6; -8.8, -7.6, -6.6 | not run | not run |

**A30's direction, `bf2_lens_dir.out`, canonical, model/data before two-halo.** Law 0.89-1.03. P2 0.72-0.87. P3, P7, P8 0.20-0.39, outer five radii 0.03-0.06. At log M* 10.6, g/law is 0.92 at y 0.09, 0.49 at y 0.011, 0.17 at y 0.001, for P3. A30 gas x 0.5 and x 0.25, reported: P3 950, 959; P2 399, 491: **less gas doesn't help, it gets worse, since the boost shrinks and the cut-off stays.** Those are before the two-halo fit (b >= 0), which can't supply the inner deficit; the gas in the lens model is CRG1's reading.

## Step 4, Bullet and mergers. `bf2_bullet.out`. Sigmas PROVISIONAL. Canonical (alt in the file); Clowe M300 3.5, 2.3
| Form, reading | main d_gas, d_BCG, Z | sub d_gas, d_BCG, Z | dkappa main, sub | M300 (Z) | UX6 label |
|---|---|---|---|---|---|
| law | 40, 247, -4.15 | 51, 209, -3.47 | -.068, -.111 | 1.11 (-4.5), .73 (-4.5) | reference |
| P3 Fa, local field | 45, 166, -4.03 | 32, 141, -4.10 | -.250, **-.971** | 4.71 (+2.3), 2.41 (+.3) | **DEAD** |
| P3 Fb, enclosed | 81, 130, -3.16 | 269, 427, +3.60 | +.009, -.116 | 4.45 (+1.8), 1.30 (-2.9) | **DEAD** |
| P3 Fc, density | 40, 230, -4.15 | 36, 188, -3.95 | -.318, -1.029 | 4.64 (+2.2), 2.23 (-.2) | **DEAD** |
| P3 Fb2, gas restored on BCG | 112, 98, -2.40 | 117, 41, -1.33 | +.095, +.358 | 5.08 (+3.0), 1.37 (-2.7) | WOUNDED; cells FAIL, TENSION |
| P7 Fa | 14, 197, -4.78 | 40, 196, -3.83 | -.235, -.627 | 3.88 (+.7), 2.15 (-.4) | **DEAD** |
| P7 Fb2 | 134, 76, -1.85 | 117, 41, -1.33 | +.089, +.218 | 4.19 (+1.3), 1.51 (-2.3) | WOUNDED; TENSION, TENSION |
| P8 Fa | 10, 206, -4.88 | 40, 196, -3.83 | -.226, -.576 | 3.68 (+.3), 2.07 (-.7) | **DEAD** |
| P8 Fb2 | 143, 67, -1.63 | 124, 36, -1.11 | +.081, +.190 | 3.96 (+.9), 1.50 (-2.3) | WOUNDED; TENSION, TENSION |

**All 24 present-gas cells, 8 forms x Fa, Fb, Fc, read DEAD, both footings.** Again the amount is about right and the place is wrong: f is highest at the gas, so the boost sits there. **Fb2 is the closest and it isn't a rescue.** It's UX6's N2: gas that has left is credited to the galaxies, so something must ride along holding the memory, no carrier is named, and it inherits every failure above. Local-gas robustness: gas x 0.8, 1.2 on P1, P2 keeps the sign wrong. MG1's pair model, 9 resolved subclusters, PROVISIONAL: Fa **DEAD IN GENERAL, 8 of 9 wrong in 6 systems, all forms, both footings**. Fb NOT GENERALISED, 5 of 9 in 4 systems. Fb2 right sign at every one, which any galaxy-following mass also gives.

## Step 5, Saturn. sigma 9.68e-15 from RQ3
Canonical (alt): law Z 9.67e3 (1.17e4). P3 at f = 0: the law's, 9.67e3. P1 2.3e8, P4 2.0e9, P6 2.6e9, P7 2.4e9, P8 1.7e9. P2, P5 pass at f = 0, the coincidence above. At f = 1: 1.3e11 (P3), 3.7e10 (P7), 3.8e10 (P8), 5.7e16 (P2, P4-P6). **C1 fails on every form that isn't P2 or P5.**

## Step 6, look-elsewhere
BF1's L3: real 18 prefilter hits, control 1, Stage 1 none in either, on one scramble. At L4, same closure list, one thread: **real 4,000 random completed jobs (1.9e9 expressions), arms on the first 2,000 of them (9.5e8), about 0.6 % of what BF1 has run.**
| Arm, 2,000 jobs | Hits | Jobs with a hit | Fixed rms <= 0.20 | Unseen X-COP passes | Lowest fixed rms |
|---|---|---|---|---|---|
| real | 19 | 13 | 0 | 15 | 0.213 |
| BF1's scramble, seed 20261102 | 0 | 0 | 0 | 0 | none |
| seed 1 | 266 | 110 | 4 | 50 | 0.187 |
| seed 2 | 15 | 14 | 1 | 7 | 0.187 |

Real against the mean control: **0.20, bootstrap over jobs 0.08-0.39. The frozen rule, above 3 with lower bound above 1, fails: NOT ABOVE CONTROL.** The spread among seeds is the finding: BF1's own seed gave 0 and another gave 266, on identical jobs, so **BF1's L3 "18 against 1" was one draw of a very wide distribution and can't be read as signal.** Three scrambles only, so the mean control is dominated by seed 1. Scrambling f and ell across rows of 4 train clusters leaves much of what the prefilter needs, f being near 0.9 everywhere there; the control asks little, and these forms pass it easily. One point on the other side: 15 of 19 real hits pass the unseen clusters against 50 of 266 and 7 of 15, thin and clustered by job, not graded. **Control hits were not put through keys or RQ3, so this says nothing either way about whether a scrambled-train form would also read 14-15 keys.** Limits as frozen: scrambled arms reuse the real closure list. **Budget:** at load about 40, arms cut to 2,000 jobs from my planned 4,000, wall about 2.5 hours rather than 2.

## Checks
K1 RQ3 through my loader: law, 0 differences against `results/law.json` in RQ3, labels, values, Z, 1e-9. **K2 H = 1 FAILS at the frozen 1e-9 on one number:** C1 Z canonical 16491.95652 against 16491.95659, relative 4.6e-9. Rounding: the generator computes g/2 + sqrt(g^2/4 + a g) where law.py computes g(1/2 + sqrt(1/4 + a/g)), and a planet's anomaly is a difference near 1e-6 of g. Every other number and every label agree. Published as a failure; no consequence, since Z is 1e4. K3 flat fit equals CRG1's on the law, rms equal to 1e-9, UX3's term equal to the printed six figures (I'd written a tolerance of 1e-3 for that, in code, loose). K4 P1 reproduces BF1 interim to 1e-3; H = 1 X-COP +0.4675. K5 law and UX3 L1 reproduce UX6, 1e-6, 1e-3. K6 real arm reproduces the snapshot's hits exactly on 4,000 jobs, 31 of 31. K7 RSS not logged for RQ3's runs: closure about 1 GB by array size, machine not swapping that I saw, so **K7 is unverified.**
**MUTATE, H x 1.5:** K3 law, K4 P1, K4 X-COP FAIL; K5 LAW FAILS (gas x 2 on the law row); exit 1. K3 UX3, K5 L1 still pass, not touched by the mutation. Control's real arm, 250 jobs: 4 hits against the snapshot's 2, K6 FAILS (`control_real_N250_MUTATE.json`). Control sample not rerun whole: the real arm's match to BF1's own hits stands in, and the three scrambled arms have no rerun. No MUTATE of the full RQ3 run: RQ3 has its own (RQ3's README). Rerun: `bf2_scan.json` byte-identical, `bf2_scan.out` differs only in the wall-time line; `results/P1.json`, `.out` byte-identical, on cached keys; Bullet P1-P4 and law rows equal to the first run, 44 of 44 (`bf2_bullet_firstrun_P1P4.*`); P5-P8 Bullet not rerun.

## Errors and limits, disclosed
- **First RQ3 chain was wrong.** My loader put outputs one directory too deep, the keys subprocess died on a path, and every key row read NOT COMPUTABLE. K1 caught it. Rerun at the lane's root.
- **Amendment A1 is a further look.** P7, P8's label depends on it. The frozen rule alone gives no NEAR MISS.
- Frozen wording: "Compute: one thread" held per process, but the scan and a Bullet script ran alongside a paused or running control for short spells. A `pgrep` pattern matched my own shell and stopped it once; recovered, no output affected.
- Stray copy of a results file went to the machine's temp directory; removed.
- P8 reads ell, so RQ3's B28 is NOT COMPUTABLE for it (no r on a map); my Bullet map takes ell = 0, and ell is about 3e-5 there. `snapshot.json` is gitignored at 3.7 MB; its hash is above, and BF1's chunks are gitignored too.
- Only 8 of 3,952 forms went through keys. There may be others like P7, P8; the kills above follow from their shape, and I'd expect them to share lens or stars-only failure, unverified.
- f in the keys harness is the fixed cosmic gas ratio, not a measured profile, as for UX3.

## Expectation against result
Free Upsilon lifts forms over rms 60 %: yes. U out of range for boosted forms 70 %: most (median 0.40-0.48), not all. NEAR MISS on a footing 12 %, both 5 %: **happened, under the amendment; I'd rated it low.** P1 keys >= 14 at 25 %: no, 10. Bullet DEAD every reading 85 %: **no**, Fb2 is WOUNDED on 4 forms; every present-gas reading is DEAD. C1 FAIL every form 97 %: **no, P2, P5 pass by the cancellation.** I didn't list lensing as the first kill; you called the Bullet the likely one, and it does kill, but **A30 is harder, by a factor of 8 against the law.** Real above control by 3, 40 %: no, it reads 0.2.

kappa = 1/2 FITTED. Not theory closed.
