# FLD1 RESULT: does the folded region reach as far as the law is seen? (2026-11-10)

Criteria 992c992ade; amendment A1 ea324cde77 (local hashes; origin ids at the end). TEST lane, quarantined: adopts nothing,
relabels nothing, registers nothing. Footings never pooled.

## Label

**DOES NOT / DOES NOT** (canonical / alt). Every known answer passes.

- **Covered: rotation curves.** The folded region holds every SPARC galaxy's last measured radius (175 of 175; the worst
  sits at 0.47 of R_fold) and every RC100 galaxy at z 0.6 to 2.5, at 2.2 R_e and at 4 R_e (100 of 100; the worst at
  0.39).
- **Not covered: lensing.** At the four KiDS masses the outer edge of ONE1's inner window lies 1.3 to 2.3 times beyond
  R_fold(z = 0), and the middle window's edge 3.1 to 5.4 times beyond. Form B's own cap (the radius where the law's halo
  holds PD1's share, X = 59.5) lies 1.1 to 4.2 times beyond R_fold(0) for log M_b 8 to 11.5 (canonical; alt 1.0 to 3.8).
- **What fails.** Any completion that puts the law only behind the fold, at today's fold reach, misses the law-level
  lensing signal the record sees at 100 to 1000 kpc. It also cannot hold form B's share inside its own halo.

| log M_b | R_fold at z 0 / 1 / 2 / 4 (kpc) | R_ta at z 0 | SPARC: largest R_last within 0.25 dex (number) | RC100: largest 2.2 R_e within 0.25 dex | KiDS inner / middle window edge | PD1 cap R_cap |
|---|---|---|---|---|---|---|
| 7 | 10 / 5 / 3 / 0.9 | 19 | none in the sample | - | - | 7 |
| 8 | 21 / 11 / 7 / 2.5 | 40 | 3 (4) | - | - | 23 |
| 9 | 46 / 25 / 16 / 5.6 | 88 | 12 (26) | - | - | 73 |
| 9.4 | 62 / 34 / 21 / 7.6 | 120 | 23 (45) | - | 81 / 190 | 116 |
| 10 | 99 / 54 / 34 / 12.1 | 190 | 54 (29) | 15 at z 0.82 | - | 232 |
| 10.45 | 139 / 76 / 48 / 17.2 | 268 | 54 (23) | 22 at z 0.91 | 272 / 637 | 389 |
| 10.7 | 169 / 92 / 58 / 21.0 | 325 | 71 (29) | 22 at z 0.91 | 362 / 849 | 518 |
| 10.9 | 197 / 108 / 68 / 24.5 | 378 | 71 (29) | 22 at z 1.12 | 456 / 1069 | 653 |
| 11.2 | 248 / 136 / 85 / 31.0 | 476 | 108 (24) | 22 at z 1.12 | - | 922 |
| 11.5 | 312 / 171 / 107 / 39.2 | 600 | 108 (9) | 20 at z 2.19 | - | 1302 |

The table is canonical; alt differs by under 0.5 % in R_fold, and its cap is 9 % smaller. All radii are physical kpc. The
full table for both footings is in `fld1_compare.out`. Each galaxy is graded against R_fold at its own mass and redshift,
not against these rows.

## What it means, in plain words

**The fold grows slowly and stays at about half the turnaround radius.**
- R_fold / R_ta is 0.52 today at every mass. Earlier it is lower: 0.46 at z 1, 0.43-0.44 at z 2, 0.31-0.33 at z 4.
  R_fold grows roughly as M_b^{1/3}.
- A Milky-Way-like mass (log M_b 10.7) has folded out to 21 kpc by z 4, 58 kpc by z 2, 92 kpc by z 1 and 169 kpc
  today.
- That is far more than any rotation curve needs: SPARC's last radii sit at a median 0.15 of R_fold, and RC100's 2.2 R_e
  at a median 0.16.
- It is far less than lensing needs. ONE1's inner window for that mass runs to 362 kpc and its middle window to 849 kpc.

**For closure.** CLOSURE.md asks for a completion that makes the clock static behind the fold.
- This lane shows that such a completion cannot by itself give the law where KiDS sees it, or where form B puts its
  share.
- At 100 to 1000 kpc the clock has not folded by today; by the action's own shell dynamics it is still falling in or still
  expanding.
- In action (A) a free-falling clock carries no law (A = 0, so P = 0; FB1, COL1).
- So a completion of this family must also give the law in clock that has never folded. That is something the action as
  written does not do.
- The rotation-curve side gives no such constraint: the fold covers it with a large margin.

**A halo ending at R_fold(0)** is ONE1's truncated halo with share X_fold = [-1 + sqrt(1 + 4 x^2)]/2, x = R_fold / r_M. At
the four KiDS masses X_fold is 31.6, 21.0, 19.1 and 17.6 (canonical; alt 34.8 to 19.4). That is below the range ONE1's
frozen statistic accepts at 1.6 R_h (the census cap 53.64 through 59.5). ONE1 also rejects the smaller basin and cosmic
shares at more than 4 sigma. This is a mapped reading, not a graded run: ONE1's machinery takes one share for all lenses,
and it was not rerun.

## Lines (per footing; `fld1_compare.out`)

| line | canonical | alt |
|---|---|---|
| (a1) SPARC: R_fold(0; M_b) >= R_last for all 175 (Upsilon 0.5; 0.3 and 0.8 give the same) | **PASS** (0 beyond; worst UGC00128 0.47) | **PASS** |
| (a2) KiDS inner window edge, log M_b 9.4 / 10.45 / 10.7 / 10.9 | **FAIL** (x1.30 / 1.95 / 2.15 / 2.32 beyond) | **FAIL** (same) |
| (a2) KiDS middle window edge | **FAIL** (x3.06 / 4.57 / 5.03 / 5.43) | **FAIL** |
| (b) RC100 at 2.2 R_e (4 R_e reported) | **PASS** (0 / 100; 0 at 4 R_e; worst zC 405226 at z 2.29, 0.39) | **PASS** |
| (c) PD1's cap, log M_b 7 to 11.5 | **FAIL** (x0.75 at 7, x1.09 at 8, rising to x4.17 at 11.5) | **FAIL** (x0.68, x1.00, to x3.79) |

At log M_b 6.5 and 7 the fold reaches past the cap. That is because the 1 kpc softening and the 0.3 kpc reflection radius
are not small there; at those masses r_M is 0.07 to 0.12 kpc.

## Known answers (`fld1_ka.out`, `fld1_compare.out`)

| known answer | result | line |
|---|---|---|
| KA1a static field, energy across reflections (A1), both footings | apocentre/start median 1.00010 / 1.00014; largest deviation 1.5e-3 / 1.7e-3 | 1e-3 / 1e-2: PASS |
| KA1b round-off: R_fold at z 4 / 2 / 1 / 0 under r x (1 + 1e-12) | 1.6e-8 | 1e-3: PASS |
| KA1c COL1's 3 kpc first-crossing times, 8 rows | within 2.3e-4 to 1.9e-3 | 2 %: PASS |
| KA2 Kepler shells: r at 0.9 t_ff; time to the reflection radius | 9.3e-5; 8.2e-5 | 1e-3: PASS |
| KA3 shell number, R_fold at z 4 / 2 / 1 / 0 for N 1200 / 2400 / 4800 | 17.2 / 47.8 / 76.1 / 139.3 at every N (differences < 0.1 kpc) | 5 %: PASS |
| Lean FLD1.lean | 4 theorems, exit 0; FLD1_MUTATE.lean 3 false statements, 3 errors, exit 1 | PASS |

## MUTATE (canonical, log M_b 10.45; line: R_fold(0) moves >= 5 % in the stated direction)

| arm | R_fold(0) | change | result |
|---|---|---|---|
| M1 law off (the clock gravitates on itself) | 160.9 kpc | +15.5 % (up, as stated) | bites |
| M2 start redshift halved (z_i 5) | 135.8 kpc | -2.5 % (down, as stated, but under 5 %) | **does not bite** |
| M3 mass x 10 (log M_b 11.45) | 300.5 kpc | +116 % (up) | bites |

M2 moves in the stated direction but by less than the line. The fold reach today is set by late infall and hardly depends
on when the mass appeared. The start-redshift brackets show the same: z_i 20 and 30 move R_fold(0) by +1.1 % and +1.4 %.

## Brackets (reported)

- **Start redshift 20 / 30:** R_fold(0) moves by +1.1 / +1.4 % and R_fold(z 2) by +6 / +8 % (log M_b 10.45). At log M_b 8
  it moves by +1 / +1 % and +7 / +8 %.
- **At rest against Hubble flow** (today's mean density, no expansion): R_fold after 13.3 Gyr is 170 kpc against 139 kpc
  (log M_b 10.45), and 26 against 21 kpc (log M_b 8). At the time z 2 has in the primary it is 54 against 48 kpc. Neither
  start reaches the KiDS inner window.
- **mu_K 0.1 per Mpc with the dust's leading correction:** R_fold equal to the limit's to 0.1 kpc at every epoch (both
  masses).
- **Where the law-dominated limit holds**, (mu_K R)^2 <= 0.1: out to 3.2 Mpc at mu_K 0.1, 178 kpc at 1.78, 85 kpc at
  3.71, and 2 kpc at KD1's 198 per Mpc.
  - At mu_K 1.78 and 3.71 the KiDS windows lie outside the limit, so the numbers above do not apply there.
  - At the CMB-side constants the clock is dust on galaxy scales (COL1 Part 0), and this lane does not apply to them.

## What it does not settle

- **It tests a necessary condition only.** Passing it (rotation curves) does not make a completion work. Failing it
  (lensing, the cap) kills only the family that puts the law behind the fold and nowhere else.
- **Non-spherical infall and mergers.** Radial shells around one mass turn around and fold in order. Real haloes
  assemble by mergers, and a 3D fold region can reach further along filaments. Spherical symmetry may underestimate the
  reach, and by how much is not computed.
- **The fold's own physics.** R_fold uses each crossed shell's trajectory after its first crossing from the same
  independent-shell equation. That equation is exact only up to the crossing. Behind the fold the action gives no answer
  (COL1), so the reach of whatever a completion puts there is not fixed by this lane.
- **The baryons are a softened point mass switched on over 1 Gyr.** Discs, gas and feedback are absent.
- **ONE1's statistic for a halo ending at R_fold** is mapped, not rerun.
- **RC100's outer radii** are the sample's stated extent (mean 2.2 R_e, maximum 4 R_e), not per-galaxy measurements. The
  record holds none.

## Anything in COL1 or CLOSURE.md this lane finds wrong

1. **COL1's A4 diagnostic: the first-crossing times outside 10, 30 and 100 kpc are wrong.**
   - They came from energy gained at the flux-cap wall. A4 reflected shells at 1.001 r_w, where the force is 500 a0, with
     a leapfrog step straddling the reflection.
   - In a static field, shells reflected that way come back to a median 36 times their start radius.
   - The times also changed by up to 20 % with arithmetic order.
   - With the corrected reflection (A1), the first crossing outside 10 / 30 / 100 kpc comes at 0.56 to 1.25 / 1.20 to 4.51
     / 4.8 to 8.0 Gyr after z 10 (z 5.5-3.6 / 3.7-1.2 / 1.1-0.5). At log M_b 9.4 no shell at 100 kpc has crossed by z 0. A4 had 0.43 to 1.04 / 1.02 to 1.52 /
     1.8 to 2.4 Gyr. The table is in `fld1_compare.out` (KA1c).
   - The 3 kpc times, set by the central focusing, were right.
   - COL1's graded label (the central caustic) does not involve reflections and stands.
2. **COL1's z = 0 charge reads** used the same reflections. Corrected on A4's grid, counting every shell, the clock charge inside 10 to 300 kpc at z 0 is
   1.6 to 5.1 % of the law's halo (A4: 1.0 to 4.0 %). Counting only uncrossed shells it is zero inside 10 kpc and at most
   1.3 % at 300 kpc. So a halo of advected clock charge is short by 20 to 60, not 25 to 100. The "about 1.06 M_b turned around" figure is
   unchanged (it does not depend on reflections).
3. **CLOSURE.md** repeats COL1's "1 to 4 %" and "short by 25 to 100": read 1.6 to 5.1 % and 20 to 60. It also quotes "COL1's shells first cross outside 10 kpc at z 4 to 6 and outside 100 kpc at z 2.3 to 2.8". With
   the correction this becomes z 3.6 to 5.5 for 10 kpc, and z 0.5 to 1.1 for 100 kpc (never by z 0 at log M_b 9.4). CLOSURE.md's expectation
   that the fold reaches "several hundred kpc by today" is wrong: R_fold(0) is 62 to 197 kpc at the KiDS masses.

## Disclosures

- **A1 is post hoc**: development runs at N = 600 on A4's grid showed the artefact. Their numbers are listed in A1.
- **KA1 as frozen** (reproduce A4's table to its printed digits) could not be a known answer, because the outer times were
  an artefact. A1 replaced it before any production run.
- **The SPARC baryon mass** uses Upsilon 0.5 (QX8 marginalises Upsilon). The brackets 0.3 and 0.8 change no galaxy's
  status.
- **Resources.** 54 production rows plus 8 rows on A4's grid, single thread each, 12 at a time; about 12 min per row at
  N = 2400. Under 0.2 GB. Nothing downloaded.

## Files

- Criteria and amendment: `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`.
- Shells: `fld1_shells.py` -> `runs/*.json` (one row each; the series column order is in each file).
- Known answers: `fld1_ka.py` -> `fld1_ka.out` / `.json`.
- Grader: `fld1_compare.py` -> `fld1_compare.out` / `.json`.
- Lean: `FLD1.lean`, `FLD1_MUTATE.lean`, `compile.txt`, `compile_MUTATE.txt`.

[ORIGIN_IDS]

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
