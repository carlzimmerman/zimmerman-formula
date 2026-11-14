# BJ1 RESULT (2026-11-14, written about 15:35 EST by the clock): the charge-budget junction, light stage

Criteria 9e7ce0dfe6 (FROZEN_CRITERIA.md), amendment A1 1334d9f23b (round-off tolerance on profile known answer iv and on
the t-free check; written after the first known-answer run, before every gate number). TEST lane, NOT blind, post hoc
(the fourth settled-radius variant of the day). Adopts nothing. Footings never pooled. Cold dark energy is a gravitating
field component; no particle is added.

**The flux-level forest (build B) has not been run.** Its driver, runner and grader are committed unrun
(`bj1b_run.py`, `run_b.sh`, `bj1b_grade.py`); the lead launches it. The words below are therefore NOT RESOLVED, as the
criteria say, because no gate has failed. A flux-level result will be added by a dated note.

## 1. Lane words (criteria section 3), per footing and case

| case | canonical | alt |
|---|---|---|
| B1 (first caustic) | NOT RESOLVED (caustic 1): flux level not run | NOT RESOLVED (caustic 1): flux level not run |
| B2 (second caustic) | NOT RESOLVED (caustic 2): flux level not run | NOT RESOLVED (caustic 2): flux level not run |
| B3 (third caustic) | NOT RESOLVED (caustic 3): flux level not run | NOT RESOLVED (caustic 3): flux level not run |

G-RC passes and G-L passes in all six cells. The matter-level forest number, reported first by the criteria and not a
label, is far over the gate in all six cells (section 3): 238 / 556 to 560 against 4. On that number alone a flux-level
FAILS is the likely outcome, but the word needs the flux-level run.

## 2. Gates

**G-RC, rotation curves (`bj1_sparc.py`; PD1's statistic and gate, XJ1's copy of it, budget layout at z = 0).**

| footing | case | rms (line) | mean | massive rms (line) | massive mean | word | galaxies beyond R_set (M/L 0.5 / 0.3 / 0.8) |
|---|---|---|---|---|---|---|---|
| canonical | B1 | 0.0560 (0.0660) | +0.0008 | 0.0375 (0.0475) | +0.0025 | PASS | 0 / 0 / 0 (worst NGC3741 0.434) |
| canonical | B2 | 0.0560 (0.0660) | +0.0008 | 0.0375 (0.0475) | +0.0025 | PASS | 0 / 0 / 0 (worst NGC3741 0.567) |
| canonical | B3 | 0.0560 (0.0660) | +0.0008 | 0.0375 (0.0475) | +0.0025 | PASS | 0 / 0 / 0 (worst NGC3741 0.686) |
| alt | B1 | 0.0558 (0.0658) | -0.0023 | 0.0326 (0.0426) | +0.0030 | PASS | 0 / 0 / 0 (worst NGC3741 0.477) |
| alt | B2 | 0.0558 (0.0658) | -0.0023 | 0.0326 (0.0426) | +0.0030 | PASS | 0 / 0 / 0 (worst UGC00128 0.629) |
| alt | B3 | 0.0558 (0.0658) | -0.0023 | 0.0326 (0.0426) | +0.0030 | PASS | 0 / 0 / 0 (worst UGC00128 0.778) |

No galaxy has a measured point beyond R_set at any of the three mass-to-light ratios (worst at 0.3: D564-8 0.460 /
0.594 / 0.715 canonical, UGC00128 0.822 alt at B3), so every curve is the law's own and the numbers equal PD1's L0
exactly (fitted median mass-to-light 0.58 / 0.52, as the law). No SPARC galaxy is above v*(0). Branches at z = 0 among
the 175: under 121 / 114 / 107, over 54 / 61 / 68 (canonical B1 / B2 / B3); under 138 / 123 / 120, over 37 / 52 / 55
(alt). R_set / R_fold over the galaxies: 0.41 to 2.74, median 0.81 / 0.61 / 0.49 (canonical), 0.37 to 2.21, median
0.74 / 0.55 / 0.45 (alt). The reported variant with the exact-field term only inside R_set gives the same numbers
(nothing lies outside).

**G-L, lensing (`bj1_lens.py`; JNT2's G4 chain, ONE1's KiDS gate as SRH1 ran it).** PASS in all six cells.

| footing | case | z all / late / early | chi2 | type difference z | word |
|---|---|---|---|---|---|
| canonical | B1 | -0.759 / -1.428 / -0.276 | 1.268 | +1.224 | PASS |
| canonical | B2 | -0.759 / -1.428 / -0.276 | 1.268 | +1.224 | PASS |
| canonical | B3 | -0.759 / -1.428 / -0.276 | 1.268 | +1.224 | PASS |
| alt | B1 | +0.091 / -1.197 / +0.528 | 0.794 | +1.278 | PASS |
| alt | B2 | +0.091 / -1.197 / +0.528 | 0.794 | +1.279 | PASS |
| alt | B3 | +0.091 / -1.197 / +0.528 | 0.794 | +1.279 | PASS |

Early-type z: -0.28 canonical, +0.53 alt, for every k. Fitted k (all) 2.50 / 2.09, higher than the record's junction at
f 2 (1.87 / 1.84). Share of lens-table cells in the over branch 0.50 to 0.54 / 0.46 to 0.50; R_set / R_fold 0.19 to 7.5.

**G-F at matter level (`bj1_matter.py`; JNT2's G1 route, gate 4).** FAIL in all six cells.

| case | canonical | alt |
|---|---|---|
| B1 | 238.82 FAIL | 559.58 FAIL |
| B2 | 238.74 FAIL | 559.06 FAIL |
| B3 | 238.10 FAIL | 555.67 FAIL |

The 1D ratio reaches 0.909 / 0.871 at z 2.2, the same for every k: the suppression comes from the over branch, whose
R_set is the equal-charge radius beyond every caustic and so does not depend on k. For comparison (seen before the
freeze): FZS1's junction 8.8 / 10.9 at f 5 and 194 / 288 at f 10; the exact junction at the third caustic 2.87 / 6.37.

**G-F at flux level: not run** (section 6 gives the command).

## 3. Known answers

- (i) to (vii), profile level (`bj1_ka_tables.py`), 321 haloes, 12 forest redshifts, both footings, B1 B2 B3: PASS in
  all 24 cells with A1's tolerance on (iv). Worst: (i) 0; (ii) 6.9e-16; (iii) 0; (iv) smallest step -1.0e-16 of C_tot
  (read to the letter it fails everywhere; the law's own C_B = M_B - Bar has steps to -4.3e-16, which is why A1 was
  written); (v) 6.1e-16; (vi) 6.2e-16 / exactly 0; (vii) exactly 0. t-free check (each node's C equals C_B, Q_k or C_R
  at that node to 1e-12): true everywhere. XJ1's shell runs install with deviation 0 from FLD1's loaded series.
- (viii) G-RC: R_set infinite reproduces PD1's stored L0 with deviation 0.0 on both footings: PASS.
- (ix) Matter level: FZS1's junction at f 2 and 3 reproduces JNT2's stored values (0.0492 / 0.1456, 1.9898 / 6.4321)
  within 9e-4: PASS. Lensing: SRH1's own profile at f 2 reproduces JNT2's stored f2.00 row with deviation 0: PASS.
- Lens-chain checks (reported): x_k forced to x_ta gives mode B to 1.2e-16 of X; x_k = 0 gives the reference exactly;
  the zero-flux identity holds to 3.6e-16 of X.
- Milky Way chain: PLT1's printed line and no-field pulls reproduce (0.008 / 0.005): PASS.

## 4. Reported items

**Branch shares (halo grid below v*; `bj1_ka_tables.out`).** Under / over at z 0, 2.2, 3.0, 3.8, 4.4:

| case | canonical | alt |
|---|---|---|
| B1 | 200/40, 76/75, 59/70, 51/59, 52/46 | 219/31, 88/73, 72/67, 64/56, 65/43 |
| B2 | 196/44, 76/75, 67/62, 66/44, 72/26 | 214/36, 89/72, 80/59, 79/41, 85/23 |
| B3 | 192/48, 81/70, 76/53, 78/32, 83/15 | 210/40, 95/66, 89/50, 91/29, 96/12 |

At the forest's redshifts the under haloes are the light ones (the heaviest under halo sits at log M_b 8.0 to 8.9 canonical, 8.3 to 9.2 alt, by z and k) and
the over haloes the heavier ones (canonical z 3.0, B3: log M200m 8 to 9 all under, 9 to 10 36 under / 4 over, 10 to 12 all
over). No over halo reaches r_ta at the forest's redshifts; at z 0, 7 / 4 do at B1.

**R_set / R_k and R_set / R_fold** (forest redshifts): under R_set / R_k 0.50 to 1.00 for every k (smallest 0.495); R_set / R_fold under
0.52 to 1.00 (B1), 0.26 to 0.64 (B2), 0.17 to 0.49 (B3); over R_set / R_fold 1.1 to 17.5 (B1), 1.1 to 17.5 (B2), 1.5 to
17.5 (B3), rising with redshift (z 4.4: 5.9 to 17.5). D_k = Q_k / C_B(R_k) runs 0.46 to 1.83.

**Milky Way (`bj1_mw.py`, reported).** At log M_b 10.825, z 0, the Milky Way is in the over branch at every k: R_set =
271 kpc canonical, 200 kpc alt (D_k 1.12 to 1.25 / 1.02 to 1.13). The line at 150 / 200 / 273 kpc is 10.4 / 13.7 / 18.6
e11 canonical (the law's at 150 and 200, the reference's at 273), 11.4 / 15.1 / 18.6 alt; median pulls field stars /
satellites and streams +1.39 / +0.85 canonical, +1.57 / +1.01 alt: the law's own pulls on canonical, and on alt the
law's for field stars with the reference's for satellites.

**t-free check:** no factor in the code (`bj1_lib.budget_row`, `bj1_lens.profile_B`); the node-by-node check holds.

## 5. Hand estimate against what came out

- G-RC: guessed 0 to 8 galaxies beyond R_set at k = 3, pass 55 to 70 %. Came out: 0 beyond at every k and mass-to-light
  ratio; PASS everywhere. The over branch, not foreseen for SPARC, holds 37 to 68 galaxies, whose R_set lies beyond the
  caustic.
- G-L: guessed PASS for every k (70 %). PASS.
- G-F, matter level: guessed 5 to 100 canonical, FAIL (65 %). FAIL, at 238 canonical, above the guessed range; 556 to
  560 alt.
- Branch shares: guessed under haloes "very few at the forest's redshifts". Wrong: on the halo grid about half are under
  (52 to 96 of 98 to 161), the light end. The over branch is the heavier half, as guessed.
- Lane word guessed FAILS THE FOREST for every k on both footings (50 %): cannot be read until the flux level runs.

## 6. Flux-level stage (for the lead)

    cd closure_2026_11_14/BJ1_charge_budget_junction
    nohup ./run_b.sh a > logs/run_b_a.log 2>&1 &          # optional second copy: ./run_b.sh b
    nice -n 19 python3 -I -B bj1b_grade.py               # when run_b_a.done exists -> bj1b_grade.json / .out

The runner waits while more than two of the other heavy drivers (fwn2a, fwn2b, xj1b, xj1a, xj1b2, wlj2_lwb) are alive
(`BJ1_MAXOTHER`). Every case passes G-RC, so all three fields are built (`BJ1B_CASES` defaults to B1,B2,B3). Fields
R, B1, B2, B3 and, at the anchors, TWB = R + 2 (B1 - R); parts in `parts_b/`. The grader composes the lane words with
G-RC and G-L as section 3 of the criteria states; KA-R checks this lane's R against XJ1's first-pass R parts.

## 7. What counts against (whatever the labels)

- Post hoc, the fourth settled-radius variant of the day; the capture surface is again a choice of k, and here the
  choice barely matters: the forest and lensing numbers are almost independent of k because the over branch sets R_set
  at the equal-charge radius beyond every caustic.
- The rotation-curve pass is by containment: every SPARC curve lies inside R_set, so G-RC reads the law's own L0 and
  tests nothing of the junction's outside.
- The delivered charge is the halo model's reference, not a flow of the action (CSD1); the emptied shell in the under
  branch neglects charge in transit; momentum, energy, the approach to rest and stability are untouched.
- The over branch puts the law's layout out to 6 to 17.5 fold radii at z 4.4 in the heavier forest haloes, and the
  matter-level number (238 / 560) is above even FZS1's junction at f 10 (194 / 288).
- The gas inputs of the forest gate are provisional and inherited.
- Not blind; a HOLDS would be a hit awaiting a frozen, blind re-grade, and nothing here can say the data favour the
  framework.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
