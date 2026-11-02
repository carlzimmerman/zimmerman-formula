# BK2_dimensional_law_search, level L1: NO HIT on both footings. 2.7e10 dimensioned expressions per footing, zero through G1-G3 on either reading, and the scrambled control comes as close on the lines. L2 and canonical's control are still running

Criteria: `FROZEN_CRITERIA.md` (28aa67bde5), committed alone first; `AMENDMENT_A1.md` holds A1 (11462b5388) and A2, both before any candidate number. Scripts `bk2_lib.py`, `bk2_search.py`, `bk2_read.py`, `bk2_stage2.py`, `bk2_gates.py`, `bk2_dear.py`, `bk2_checks.py`, driver `run_bk2.sh`, watcher `bk2_watch.sh`. Numbers in `bk2_train_*.json`, `bk2_stage2_*`, `bk2_dear_*`, `bk2_checks.out`. **Not blind.** No action, no CMB. kappa = 1/2 FITTED. The cold sector stays retired; nothing here reinstates it. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Counts, level L1 (CAP_D, CAP_A 3e4)
| | canonical | alt | alt scrambled control | canonical control |
|---|---|---|---|---|
| Enumerated, dimension valid | 2.739e10 | 2.739e10 | 2.736e10 | running |
| In G1a's window at Saturn | 8.97e8 | 8.97e8 | 8.98e8 | |
| G1a Newton, 3 points | 1.228e8 | 1.231e8 | 1.178e8 | |
| G1b Cassini, of those | 5.00e7 | 5.00e7 | 4.68e7 | |
| Prefilter X-COP | 2.72e7 | 2.87e7 | 2.76e7 | |
| Prefilter SPARC subsample, hits | 4.82e6 | 4.95e6 | 3.50e6 | |
| Distinct on X-COP train | 2.60e6 | 2.65e6 | 1.78e6 | |
| G3 LINE | 34,545 | 28,948 | **10** | |
| G3 ERR | **0** | **0** | **0** | |
| G2 LINE, in the X-COP zone | 173 | 144 | 47 | |
| G2 ERR, in the X-COP zone | 1,129 | 871 | 139 | |
| **G2 and G3, LINE** | **0** | **0** | **0** | |
| **G2 and G3, ERR** | **0** | **0** | **0** | |
| Closest to the lines (1 = on the line) | 1.08 | 1.07 | **1.02** | |
| Smallest Z_max | 9.3 | 8.2 | 32 | |

**Labels, frozen: NO HIT, both footings, at L1. SURVIVOR 0. WITHIN ERRORS, OUTSIDE A LINE 0. FAILS ONLY CASSINI 0. Look-elsewhere:** N_eff is under 2.7e10 and no train pass exists to correct. Real over control: G3 LINE is 3000 x higher, since the control destroys X-COP's radial order. On combined closeness, **the control does as well as the real data**, so no near miss below earns weight from its closeness alone.

Downstream counts run on the 50 near misses only, so they aren't a census. In them G9 and G10 pass 0 of 50 on both readings, canonical and alt: **no near miss touches the dwarfs or IC 1613.**

## The closest rows, no label
**(a) No fit: g = I5(g_b, a0) [(8 pi/3) g_gas/sqrt(a0 g_b) + (g_star/g_b)^4].** Also with I1, which fails Cassini by the a0 tail. The bracket's second term goes to 1 in stellar systems and to nothing in clusters, so on clusters g is about (8 pi/3) g_b, a fixed M/M_b near 8.4.
| Gate | canonical | alt | |
|---|---|---|---|
| G1b Cassini | pass | pass | I5's tail is exponentially small |
| G3 X-COP train | +0.005, 0.096 LINE pass | +0.012, 0.097 pass | Z_shape 28, 29 |
| G5 X-COP unseen | -0.037, 0.088 pass | -0.029, 0.085 pass | Z_shape 20 |
| **G8 keys, unseen, primary cell** | **15 of 15, both h. M3 -0.09, -0.21; chi^2 7.3, 11.0; p 0.95, 0.75** | **15 of 15. M3 +0.03, -0.11; p 0.94, 0.73** | The other three cells weren't run |
| G2 SPARC train | **FAIL** rms 0.192, line 0.174; Z 2.78 | **FAIL** 0.190; Z 2.58 | |
| G4 SPARC unseen | **FAIL** 0.204, line 0.195; Z 2.10; FG1's S passes at 0.070, U 0.51 | **FAIL** Z 2.18; S U 0.48 on all, 0.51 on even | |
| G6 LITTLE THINGS | **FAIL** +0.107, line 0.10; **ERR passes,** Z 1.03: within errors, outside the line | same, +0.108, Z 1.04 | |
| G7 groups | pass Z +0.31 | pass -0.31 | gas-free, equals the law |
| G9 dwarfs | **FAIL** E2: UFD +7.84, bright M31 +5.24, M31 others +3.44 | **FAIL** | The law's failure, unchanged |
| G10 IC 1613 | **FAIL** Z -6.75 | **FAIL** -7.46 | |
| G11 Milky Way | wide priors only, D 0.72 | FEASIBLE IN PRIORS, 18 cells | MW taken gas-free, [READING] |
| G12 DiskMass | **FAIL** r 1.25; ERR Z 0.86 passes | **FAIL** 1.21; Z 0.75 | |
| **G13 Bullet** | **FAIL** dkappa -0.23, -0.79; carried -0.59, -0.56. Main Z -4.58 | **FAIL** -0.23, -0.76; carried -0.57, -0.55 | **Sign wrong on both readings** |

**Read this as hard as a win.** Passing all 15 keys and X-COP's unseen clusters with no fitted number is the strongest cluster row I've seen in this lane's reading, and the keys were never in the search. **But:**
- 8 pi/3 was chosen from twelve constants in a 2.7e10 search on X-COP train, and clusters' M/M_b near 8.4 is close to what any such constant must give. It's a level with one physical content, **total mass follows the gas,** and the Bullet says it doesn't: the same statement UX6 made. Carrying gas with the galaxies doesn't fix it here.
- (g_star/g_b)^4 is a gas-fraction switch, UX3's "not a cluster" in another dress. It costs discs: rms 0.192 against the law's 0.166.
- Chi^2 7.3 on 15 is low, keys are correlated, and I've not chased why.
- X-COP's Z_shape of 28 means it misses X-COP's radial form badly against the mass errors.
It's a description of relaxed clusters, as UX3's row was. It fails five or six lines.

**(b) FITTED, one constant: g = I5(g_b, a0) + k g_gas sqrt(Phi_b)/c, k about 2000.** SPARC nearly untouched, 0.167 against 0.166, unseen 0.186 against 0.186, S rms 0.0536, U 0.50, LT -0.03. X-COP train +0.017, 0.110, **misses by 10 %,** unseen -0.029, 0.085. Cassini passes. Keys 8 of 15, M3 -2.6, p 0.036, 0.015 at nearby k. Bullet FAIL, dkappa -0.30, -0.68. Dwarfs and IC 1613 as the law. The term switches on with potential depth, so it is "clusters are big" written in Phi. Canonical's row; alt's U is 0.42, FAIL.

The rest are in `bk2_stage2_L1_*.json`, `bk2_dear_*`, ranked by Z and by line.

## What the search says, within its limits
- **Cassini costs nothing in discs.** 5e7 of 1.2e8 Newton-limit forms pass it, and I5, I2, I6 versions of near misses read as well or better than the law's I1, as the record's alpha = 1 note expected. So the law's tail isn't what any line here needs.
- **Nothing in this grammar lifts the dwarfs,** since their leaves are gas-free stars and one point, so any gas or potential term reduces to the law.
- **The Bullet:** every near miss graded reads wrong-signed dkappa, present and carried.

## Checks
K1 law row, both footings: X-COP, SPARC, LT, groups, S all to print precision. K2 dwarfs 0. K4 Cassini 2557, 3091 x, as CFG770. K5 DiskMass 1.239, 1.204. K6 UX3's 0.217. K7 dimension: 0 wrong of 254 monomials. K8 window equals full loop. Keys path law row: M3 +4.76, chi^2 65.0, as LW1. MW law row 10 and 17 cells, D 0.78, 0.60, as LW1. Bullet law row dkappa -0.068, -0.111, as UX6.
**Planted: RECOVERED** at T0 and L1, residual 1e-17, passes G2-G5 LINE. MUTATE tolerance 1e-6: 0 hits on alt. `bk2_checks --mutate` exit 1. Rerun byte-identical at T0.

**Failed or short:**
- **K3 FAILS as frozen:** IC 1613 X1 row -0.535, Z -6.75, against LW1's printed -0.593, Z -7.9, BS1's row. A1 stated it first.
- **The fast key tier failed its own frozen check,** max dZ 0.38; refused. The real path turned out to take 2 minutes.
- **My G3 ERR is too strict, and I can't widen it now.** Z_shape uses mass and model errors only, with no cluster-to-cluster scatter, none being on disk. So no row anywhere passes, and ERR on G3 is tighter than the LINE. That breaks the owner's "neither too strict". Flagged, not changed. `bk2_read.py` now also tallies, tagged POST and with no label, G3 ERR without Z_shape, on runs from canonical's control on.
- Planted's L1 harvest was stopped at 4.0e6 of 4.8e6 hits to free its core; recovery was checked directly in `bk2_planted_check.py`.
- First harvest killed at 100 hits/s: A2. Harvests aren't checkpointed. A third short process ran during some dear-gate tests, against the 2-process limit.
- Near misses' keys ran the primary cell only; a formula reaching G8 by passing would get all. G-OUT-M3's Z_tot is at a fixed s, within 0.1 of LW1's.
- DiskMass, MW take g_gas 0, so gas terms don't bite there: [READING], and their passes say little.
- Bullet leaves r, Sigma_b, rho_b, Phi_b are readings of F on Plummer baryons. One formula's I5(g_star, ...) reads nan on the map: NOT EVALUABLE at its zero-star cells.

## Limits
**T and sigma aren't in the grammar:** not on any train row. Files that would lift it, none downloaded: X-COP temperature profiles, Ghirardini+ 2019, the X-COP site's tables, under 1 MB; SPARC gas dispersions have no public table I know of. Caps bound: D closure 1.2e5 before the cap of 3e4; A 1.2e5 before 3e4. One-point samples can't see Sigma_b, rho_b slopes. Enclosed-mass forms mean nothing in a merger without a field equation. No Cassini Q2. This is no impossibility statement.

## Expectation against result
Passing G1 and G2 LINE: yes. G1-G3 ERR 60 %: no, by my own Z_shape. G1-G3 LINE 25 %: no. I didn't expect 15 of 15 keys on a no-fit near miss.

## Unfinished, running
Canonical's mutate and control L1, then L2 (CAP_D 1e5, CAP_A 3e5, about 3e12 enumerated per run) real and control, both footings, nice 19, two processes, days. Watcher: `bk2_watch.sh`, writes `bk2_status.out` every 30 min, runs `bk2_stage2.py` as each harvest lands, sets `SURVIVOR_FLAG` on an all-LINE cheap pass; commits nothing. Restart: `./run_bk2.sh canonical`, `./run_bk2.sh alt`; they resume. A flag means: dear gates, then a separate recheck before any label. **This README covers L1 only until it's updated.**

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
