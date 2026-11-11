# SRH1 RESULT: one history of the settled radius against the forest, rotation curves and galaxy lensing

**WINDOW EMPTY / WINDOW EMPTY (canonical / alt). The forest (G1) and galaxy lensing (G4) exclude each other.**

- **G1, the forest, sets an upper limit.** f <= 0.70 on the grid (the edge interpolates to 0.722 / 0.725).
- **G4, KiDS lensing, sets a lower limit.** f >= 1.25 on the grid (the edge interpolates to 1.004 / 1.050).
- **The gap is a factor of 1.39 / 1.45.** No single f passes both.
- **A window opens only with a redshift tilt.** This comes from post hoc AMENDMENT A1 and is reported, not graded. With
  f = f0 (1 + z)^beta, beta -1 (f0 1.5, 2.0) and beta -0.5 (f0 1.25) pass all four gates on both footings. That is the
  outcome the criteria named in advance as counting against. The frozen tilt grid (f0 <= 1) opens none.
- **The rotation curves do not bind.** G2 (high-z) needs f >= 0.391 / 0.391. G3 (SPARC) holds at every grid f.
- **Checks.** Every known answer passes and every MUTATE arm bites.

**The fail is near its line.** G4 fails inside the forest's range on one line only: early-type lenses at the 1.6 R_h veto,
+2.16 to +2.22 sigma against a 2 sigma line. All lenses together sit at +1.86 to +1.92 sigma, and the other G4 lines
pass. Reported, not graded: the KO1R tie rule reads +1.7 sigma (all lenses), and the 1.0 R_h veto reads +1.1 sigma.

TEST lane, quarantined. Criteria 5ed8a37ec6 (committed alone before any script or number). AMENDMENT A1 68969e177e
(post hoc, reported tilt cases only; grades nothing). Footings are graded separately and never pooled. Cold dark energy is
a gravitating field component; no particle is added.
- **The family is post hoc.** It was chosen after FRZ1 and FZS1 were seen.
- **An empty window is not a derivation either way.** It is a statement about this family: R_set = f x FLD1's R_fold,
  with FZS1's junction.
- **It needs an independent re-grade.** It is not in PAPER72.

## What was asked and what came out

**The question.** Is there one constant f with R_set(z, M_b) = f R_fold(z, M_b) that satisfies all four gates? The law's
layout holds inside R_set and the cold reference's (NFW) layout outside it, and the enclosed cold mass at R_set is the
reference's (FZS1's rule).

1. **The forest wants the settled region small at z 2.2 to 4.4.** Delta chi^2 grows smoothly with f: 0.19 at 0.5, 3.17 at
   0.7, 5.35 at 0.75, 38.7 at 1 (canonical). G1 passes for f <= 0.70 on both footings.
2. **Lensing wants the law's region to reach into ONE1's inner window today.** For f <= 0.55, G4 reads exactly as if the
   cold reference held everywhere (f = 0). R_set then lies inside the innermost KiDS radii, and the stack cannot see it.
   - **The reference's layout is more concentrated than the law's halo.** With k fitted on the inner window it predicts
     an outer/inner ratio R_s = 0.545 / 0.540 (k 1.39). The data read 0.811 +- 0.134 / 0.809 +- 0.133. ONE1's
     counted-once halo gives 1.004 / 0.847 (k 2.50 / 2.11).
   - **R_s climbs only once R_set enters the window:** 0.573 at f 1, 0.602 at 1.25, 0.719 at 2 (canonical).
   - **G4 first passes at f 1.25.**
3. **The rotation curves are covered with room to spare.** RC100 at 2.2 R_e needs f >= 0.391 (zC 405226 at z 2.29). SPARC
   last radii need f >= 0.467 (UGC00128) for coverage, and PD1's truncated-curve line holds even below that (rms 0.0557 /
   0.0553 at f 0.30, line 0.0660). So G3 holds at every grid f.
4. **So the lower limit that kills the window is lensing at z ~ 0.3, not rotation curves.** The upper limit is the forest
   at z 2.2 to 2.8. A constant f cannot be both at most 0.72 at z ~ 2.5 and at least about 1.0 at z ~ 0.3.

## Graded table (canonical; alt in the second table)

G4 columns: z = (data - model) / sigma for all / late / early at 1.6 R_h (line |z| <= 2), and the profile chi^2 (line
9.49). The type-difference line G-K3 passes at every f and at both comparators (+1.13 to +1.43 sigma).

| f | G1 Delta chi^2 | G2 | G3 | G4 | G4 z all / late / early, chi^2 | family-layout SPARC rms (reported) | z = 0 R_tot k 1 / 3 (reported) |
|---|---|---|---|---|---|---|---|
| 0 (reference) | 0 | F | - (not evaluated) | FAIL | +1.89 / -0.78 / +2.19, 4.43 | - | 0.9975 / 0.9784 |
| 0.30 | 0.001 P | F | P | FAIL | +1.89 / -0.78 / +2.19, 4.43 | 0.0624 | 0.9971 / 0.9738 |
| 0.40 | 0.022 P | P | P | FAIL | +1.89 / -0.78 / +2.19, 4.43 | 0.0618 | 0.9963 / 0.9648 |
| 0.50 | 0.189 P | P | P | FAIL | +1.90 / -0.78 / +2.19, 4.44 | 0.0621 | 0.9947 / 0.9486 |
| 0.60 | 0.923 P | P | P | FAIL | +1.89 / -0.78 / +2.19, 4.40 | 0.0622 | 0.9924 / 0.9287 |
| 0.65 | 1.774 P | P | P | FAIL | +1.87 / -0.78 / +2.17, 4.36 | 0.0622 | 0.9920 / 0.9300 |
| **0.70** | **3.173 P** | P | P | **FAIL** | +1.86 / -0.78 / **+2.16**, 4.29 | 0.0622 | 0.9929 / 0.9430 |
| 0.75 | 5.350 F | P | P | FAIL | +1.84 / -0.79 / +2.14, 4.22 | 0.0623 | 0.9951 / 0.9631 |
| 0.80 | 8.58 F | P | P | FAIL | +1.81 / -0.79 / +2.12, 4.14 | 0.0623 | 0.9981 / 0.9859 |
| 0.90 | 19.5 F | P | P | FAIL | +1.76 / -0.80 / +2.07, 3.94 | 0.0626 | 1.0019 / 1.0125 |
| 1.00 | 38.7 F | P | P | FAIL | +1.69 / -0.82 / +2.00 (2.003), 3.70 | 0.0630 | 1.0019 / 1.0125 |
| **1.25** | **134.0 F** | P | P | **PASS** | +1.48 / -0.87 / +1.81, 3.05 | 0.0646 | 1.0019 / 1.0124 |
| 1.50 | 279.7 F | P | P | PASS | +1.22 / -0.93 / +1.58, 2.36 | 0.0662 (over) | 1.0019 / 1.0123 |
| 2.00 | 452.1 F | P | P | PASS | +0.65 / -1.08 / +1.04, 1.26 | 0.0682 (over) | 1.0019 / 1.0118 |
| inf (R_set = r_ta) | 9916 F | P | P | PASS | = ONE1's halo: -1.15 / -1.46 / -0.65, 1.93 | - | CO1 1.0033 / 1.0282 |

Grid values 0.35, 0.45 and 0.55 are in `srh1_grade.out`; they change nothing.

**Alt**, same layout. G1 is 3.085 P at f 0.70 and 5.181 F at 0.75. G4 is FAIL from 0.30 to 1.00 (early +2.19 to +2.22 for
f <= 0.70; +2.04 at 1.00) and PASS from 1.25 (+1.85 early). G2 is F at 0.30 and 0.35. G3 is P everywhere. The family-layout
SPARC reading holds at every f (rms 0.0613 to 0.0654). z = 0 R_tot at k 1 / 3: 0.9953 / 0.9632 at f 0.70, 1.0053 / 1.0389
from f 0.90 up (CO1: 1.0076 / 1.0645).

| edge (interpolated, reported) | canonical | alt |
|---|---|---|
| G1 upper (Delta chi^2 = 4) | 0.722 | 0.725 |
| G4 lower (early-type z = 2) | 1.004 | 1.050 |
| gap, G4 lower / G1 upper | 1.39 | 1.45 |
| G2 lower, 2.2 R_e (4 R_e, reported) | 0.391 (0.711) | 0.391 (0.712) |
| G3(a) coverage (G3 itself holds below it by line b) | 0.467 | 0.467 |

## Qualifiers and what counts against (stated in advance; how each came out)

- **G4 does test the history.** Its status changes inside the grid (FAIL up to 1.00, PASS from 1.25), and the two
  comparators differ (f = 0 FAIL, f = inf PASS). The "does not test the history" qualifier does not fire.
- **Amplitude.** In the forest's range s (the junction factor) is near 1 at galaxy scale. SPARC: median 0.88 to 0.94
  canonical, 5-95 % 0.55 to 1.43. KiDS lenses at z 0.15 to 0.45: median 1.24, range 0.86 to 1.77. The family-layout SPARC
  reading holds PD1's line at every f <= 1.25 on both footings. The amplitude qualifier does not fire.
- **Empty window: yes.** That is the result.
- **A window only with the tilt: yes.** A1's post hoc cases with beta -1 or -0.5 open one; the frozen tilt grid does not
  (tilt section below).
- **R_fold is FLD1's law-dominated limit.** The limits are in units of that limit: a softened point mass, radial
  shells, no cold mass in the shells' own gravity.
  - FLD1 says mergers and filaments could make the 3D settled region larger. A uniformly larger R_fold rescales both
    limits by the same factor, so the gap (1.39 / 1.45) stays.
  - What would change the answer is a different redshift dependence. That is what the tilt tests.
- **Inherited from the reused lanes.**
  - G1: FRZ1's halo model (Tinker 2008 z-scaling and Duffy c(M, z), from memory: PROVISIONAL; present-day baryon shapes;
    a linear 1D projection).
  - G4: neighbours keep ONE1's counted-once halos and are not re-laid out. The lens model keeps ONE1's central-point
    baryons; FRZ1's uncondensed baryons and cluster regime are dropped.
  - G2: RC100's 2.2 R_e is the sample's mean extent.

## The tilt, f = f0 (1 + z)^beta (reported, never graded)

Here f(z) = f0 (1 + z)^beta. f at the lenses (z 0.31) and at the forest's first bin (z 2.2) are given. G3(a) holds for
every case (f0 >= 0.467). Files: `srh1_tilt.out`; G1 for the frozen cases is in `srh1_forest_<footing>.out`.

| case | f(0.31) / f(2.2) | G1 canonical / alt | G2 | G4 early z canonical / alt | all four |
|---|---|---|---|---|---|
| frozen beta -1, f0 0.5 / 0.75 / 1.0 | 0.38-0.76 / 0.16-0.31 | P (<= 0.001) | F | +2.12 to +2.19 / +2.15 to +2.22 (FAIL) | no |
| frozen beta -0.5, f0 0.5 / 0.75 / 1.0 | 0.44-0.87 / 0.28-0.56 | P (<= 0.41) | F / P / P | +2.07 to +2.19 / +2.11 to +2.22 (FAIL) | no |
| frozen beta +0.5, f0 0.5 / 0.75 / 1.0 | 0.57-1.15 / 0.89-1.79 | F (26 to 460 / 25 to 276) | P | FAIL / FAIL / PASS (+1.91 / +1.94) | no |
| A1 beta -1, f0 1.25 | 0.95 / 0.39 | P (0.01) | F | +2.01 / +2.05 (FAIL) | no |
| **A1 beta -1, f0 1.5** | 1.15 / 0.47 | P (0.07 / 0.07) | P | +1.87 / +1.91 | **yes / yes** |
| **A1 beta -1, f0 2.0** | 1.53 / 0.63 | P (0.87 / 0.86) | P | +1.51 / +1.56 | **yes / yes** |
| **A1 beta -0.5, f0 1.25** | 1.09 / 0.70 | P (2.47 / 2.43) | P | +1.93 / +1.96 | **yes / yes** |
| A1 beta -0.5, f0 1.5 | 1.31 / 0.84 | F (9.39 / 9.11) | P | +1.74 / +1.78 | no |

- **The frozen tilt grid opens no window on either footing.**
  - beta < 0 passes the forest, but it leaves f at the lenses (0.38 to 0.87) below G4's edge.
  - beta +0.5 reaches G4 only where the forest fails.
- **A1's cases (post hoc) do open one.** Three cases pass all four gates on both footings. This is the "window that exists
  only with the tilt" that section 7 named in advance as counting against.
- **What a passing history needs.** In plain terms: R_set / R_fold at least about 1.1 at z ~ 0.3 and at most about 0.7 at
  z ~ 2.2. So the settled radius must grow by a factor of at least about 1.5 more than FLD1's R_fold does between z 2.2
  and z 0.3 (R_set proportional to R_fold (1 + z)^beta with beta about -0.5 or steeper).
  - FLD1's spherical fold gives no such extra growth. Nothing in the record derives it.
- **Amplitude at z = 0 for those cases**, read from the primary grid at f = f0 (z = 0, so f(0) = f0):
  - The family-layout SPARC reading holds at f0 1.25 (canonical 0.0646). It goes over PD1's 0.0660 at f0 1.5 and 2.0 on
    canonical (0.0662, 0.0682). It holds on alt (0.0640 to 0.0654).
  - So on canonical, only beta -0.5, f0 1.25 keeps that reported reading too.
  - The z = 0 redistribution for f0 >= 1.25 is FZS1's level, 1.0019 / 1.0124 (canonical) and 1.0053 / 1.0387 (alt).
- **The tilt is reported, never graded.** It does not change the label. A tilt grid of 5 post hoc points is not a scan.

## The z = 0 redistribution factor (reported, not graded)

This is the factor that the weak-lensing amplitude row uses (R_tot at k 1 / 3 h/Mpc, z 0; FZS1's z = 0 table at each f).
- **In the forest's range (f <= 0.70) it sits below 1.**
  - Canonical 0.9920 to 0.9971 at k 1 and 0.929 to 0.974 at k 3; alt 0.9928 to 0.9971 and 0.934 to 0.974.
  - The pure cold reference (f 0) gives 0.9975 / 0.978.
  - CO1's law-to-r_ta value is 1.0033 / 1.0282 canonical and 1.0076 / 1.0645 alt.
  - KL1 quotes 0.982 -> 0.972 at k 1 under its C2 response.
- **So a history the forest accepts removes all of CO1's excess power at k 1 to 3 and goes below the reference.** The
  cluster-regime haloes' law layout inside R_set is flatter than NFW (FZS1's diagnostic).
- **From f 0.90 up it is FZS1's 1.0019 / 1.0125 (canonical).**
- The lensing-amplitude row is not re-graded here.

## Known answers (all pass) and MUTATE (all bite)

| item | result |
|---|---|
| KA-G1 | f 1: 38.741 / 36.658 (FZS1 38.741 / 36.658); f 0.5: 0.189 / 0.185 (FZS1 0.189 / 0.185); R_set = r_ta 9916.246 / 9008.690 = FRZ1 (R_cold to 1.1e-15, per bin 1.1e-12 / 1.6e-12); R_set = 0 gives 0; FZS1's KA-F, KA-M (6.6e-16), KA-Z0 (1.4e-15 / 1.7e-15) and FRZ1's KA2 / KA3 pass inside the copy |
| KA-Z0 (f 1) | z = 0 R_tot equals FZS1's table to 0 |
| KA-G2 / KA-G3 | at f 1, worst ratios 0.391237 / 0.391383 (2.2 R_e), 0.711340 / 0.711606 (4 R_e), 0.467132 / 0.467178 (SPARC) equal FLD1's to 1e-6; 100 / 100 and 175 / 175 covered; no galaxy outside FLD1's mass grid |
| KA-G3b | PD1's `sparc()` with its own share table: rms 0.05627 / 0.05583 (stored 0.05627 / 0.05583); truncation off 0.05605 / 0.05583 = stored law-only; this lane's law mode the same |
| KA-G4a | ONE1 rerun exactly as ONE1 ran it: model R_s 1.0034 / 0.7923 / 0.9990 (canonical all / late / early), z -1.14 / -1.46 / -0.65, gate PASS / PASS; relative deviation from the stored run 0 |
| KA-G4b | this lane's projection of ONE1's halo against ONE1's `dsig`, u 0.1 to 1e4: 3.6e-8 |
| KA-G4c | ONE1's halo through this lane's table, interpolation and 9-node neighbour grid: R_s 1.004 / 0.847, z -1.15 / -0.23; 0.13 / 0.07 of the tolerance |
| KA-4c (pooled) | law to R_t: 20 / 59 over, worst -0.635 (canonical); 24 / 59, -0.675 (alt) = PD1's original P2-KiDS |
| MU1, f 10 | G1 8626 / 8044: bites |
| MU2, f 0.05 | G2 and G3 both fail: bites |
| MU3a, R_fold z reversed in the forest (f 0.6) | canonical abs(R_cold(k 10) - 1): 0.0172 -> 0.00005 at z 2.2, 0.00009 -> 0.0065 at z 4.4: bites (forest 0.082 / 0.058, reported) |
| MU3b, R_fold read at 3.1 - z for RC100 | G2 lower limit 0.391 -> 0.496 (+27 %): bites |
| MU4, reference outside R_set removed (f 0.5) | canonical model R_s 0.545 -> 0.295 (G4 FAIL on three lines): bites |

## Pooled reading (PD1's P2-KiDS pointwise line; reported, not graded)

Brouwer et al. 2021's isolated-lens mass bins, all types pooled, 59 points, the settled layout at z 0.31.
- **It fails at every f and at both comparators.** In the forest's range 47 to 49 / 59 points are over 0.05 dex, against
  20 / 24 for ONE1's halo (law to R_t). The worst point is the same outer point (-0.635 / -0.675) throughout.
- **This line compares a one-halo model with the law at 1 to 3 Mpc**, where any halo that ends fails. It cannot test the
  history, as PD1 found for its own halo.

## Hand estimates against the outcome

**Mine** (criteria section 8).
- G1 upper near 0.72: right (0.722 / 0.725).
- G2 0.39: right. G3 0.47: right for coverage, but G3 as frozen does not bind at all, because PD1's line (b) holds below
  coverage.
- **G4 wrong.** I expected it to pass at every f and not to test the history (70 %). It fails across the forest's whole
  range and passes only from f 1.25. I had the concentration argument backwards for this statistic. The NFW reference is
  more concentrated, so after the inner-window fit it predicts too little outer signal (R_s 0.55 against 0.81). It does
  not lower R_s toward the data from above.
- So I expected ONE HISTORY PASSES with a window of about 0.5 to 0.70. It is WINDOW EMPTY.
- Family-layout SPARC passes in the forest's range: right. z = 0 R_tot at f 0.6 near 1.001: wrong, it is 0.992.

**The closure chat's.** G1 at most about 0.72: right. G3 at least about 0.47: right for coverage. G2 0.3 to 0.6: right
(0.39). "G4 is the unknown and may empty it": it does.

## Disclosures

- **Post hoc.** The family was chosen after FRZ1 and FZS1 were seen, and A1 after G2, G3 and G4 numbers were seen. A1
  grades nothing.
- **The G4 fail is one line, 0.16 to 0.22 sigma over a 2 sigma line,** on early types at the graded veto. Small changes
  of the reused machinery could move it across. Examples: the neighbours' own layout (kept as ONE1's), the tie rule
  (KO1R reads +1.7 sigma for all lenses), the veto (1.0 R_h reads +1.1 sigma, and ONE1's halo itself misses by -2.7
  there).
  - The data-side errors are ONE1's jackknife.
  - The window's emptiness rests on the 2 sigma line as ONE1 froze it. It is not a high-significance exclusion.
- **G1's numbers at f 1 and 2 equal FZS1's primary and x 2.** The copy is FZS1's code with only the case list changed.
- **G4 for f <= 0.55 is identical to f = 0 to three decimals.** R_set lies inside the innermost KiDS radii there; this is
  not a bug in the layout. MU4 shows the pipeline responds to the outer layout (0.545 -> 0.295).
- **Numpy RuntimeWarnings.** CFG556's `U_of` prints divide-by-zero, overflow and invalid-value warnings, as in FRZ1's and
  FZS1's logs. KA-T reproduces FRZ1 to 1e-15.
- **House line.** "kappa = 1/2 FITTED; not theory closed." is printed at the end of each `.out` by its writer.

## Files

- `FROZEN_CRITERIA.md` (5ed8a37ec6, alone, before any script or number); `AMENDMENT_A1.md` (68969e177e, alone, post hoc).
- `srh1_hm.py` -> `srh1_hm.json` / `.out`, `srh1_hm_MUTATE.json` (2092 s, one thread). This is FZS1's `fzs1_hm.py` with
  only the case list, the z = 0 table and the output names changed. It executes FRZ1's `frz1_hm.py` prefix read-only and
  reads FLD1's `runs/*.json`.
- `srh1_forest.py` -> `srh1_forest_<footing>.json` / `.out` (FZS1's `fzs1_forest.py`, same changes).
- `srh1_rc.py` -> `srh1_rc.json` / `.out` (G2, G3, the family-layout SPARC reading). It executes FLD1's
  `fld1_compare.py` and PD1's `pd1.py` up to `def xcop(`, read-only.
- `srh1_lens.py` -> `srh1_lens.json` / `.out` (G4, 1087 s). It executes ONE1's `one1_kids.py` up to its primary marker,
  read-only.
- `srh1_tilt.py` -> `srh1_tilt.json` / `.out` (tilt, A1).
- `srh1_grade.py` -> `srh1_grade.json` / `.out` (window and labels).
- The console logs `run_*.log` stay local; every number in them is in the `.out` / `.json` files. Nothing was downloaded.
  Nothing was written outside this folder.
- Commits (local / origin): criteria 5ed8a37ec6 / 20a7258e0a; A1 68969e177e / d10a712a4d; result bcb50d3c1f / f64f8b0b2b. Pushed
  by replay; no history rewritten.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
