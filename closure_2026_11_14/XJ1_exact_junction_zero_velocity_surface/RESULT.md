# XJ1 RESULT (2026-11-14, first written 13:38 EST by the clock): the law exactly inside the settled radius

Criteria ef8ccdde98 (committed 10:40 EST, alone, before any script or number). Amendments, each committed before the
numbers it governs were read: A1 38c6539631 (a round-off tolerance), A2 38ec13e099 (rotation curves under the record's
junction; clock-time correction), A3 4d9d08a7e1 (0.5 and 0.75 fold radii), A4 65a8b3c71a (build A's two cases), A5
ed8c276b92 (the second and third caustic). A2 to A5 are post hoc: each was written after earlier reported numbers of
this lane were read, and each says what had been seen.

TEST lane, not blind. Adopts nothing, relabels nothing, registers nothing. Footings are graded separately and never
pooled (canonical / alt throughout). A HOLDS is a hit that awaits a frozen, blind re-grade; it is not a pass of the
theory. Nothing here says the data favour the framework over LCDM.

**State of the lane when this file was first written:** build B's primary stage is complete and graded in both passes
(96 files each). Its bracket stage is still running, so no label below carries its FRAGILE flag yet. Build A (the
second, independently written implementation) has not landed. Both are added by dated notes at the end of this file.

## 1. The lane words

| | canonical | alt |
|---|---|---|
| **Q1, the junction (frozen)** | THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION | THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION |
| **Q2, the fold radius (frozen)** | NOT RESOLVED (the fold radius): NO VERDICT | FAILS (the fold radius) |
| **Q2, the zero-velocity surface (frozen)** | FAILS (the zero-velocity surface) | FAILS (the zero-velocity surface) |
| **Q3, the window under the exact junction (A3, post hoc)** | A WINDOW IS LEFT: f in [0.5, 0.75] | A WINDOW IS LEFT: f in [0.5, 0.75] |
| **Q4, the second caustic (A5, post hoc)** | HOLDS WITH NO FREE CONSTANT (the second caustic) | HOLDS WITH NO FREE CONSTANT (the second caustic) |
| **Q4, the third caustic (A5, post hoc)** | HOLDS WITH NO FREE CONSTANT (the third caustic) | HOLDS WITH NO FREE CONSTANT (the third caustic) |

Said plainly, as the criteria require when Q1 reads this way: **the record's forest holds at f = 2 and 3 (FRZ6, FRZ6R,
FWN1R, and the window of JNT2 and JNT2R) belong to a layout whose inside is not the law.** With the law itself inside
the settled radius, 2 and 3 fold radii fail the forest at flux level on both footings, and so does the zero-velocity
surface.

The two holds of Q4 are hits found by looking, from a family of two, after one frozen surface (the zero-velocity
surface) had failed at matter level. They need a frozen, blind lane before they mean anything.

## 2. Labels (build B: FWN1R's library, 4 seeds in all 12 bins, DESI DR1 P1D, 755 points, gate 4)

D is the 12-bin flux-level Delta chi^2 against the reference layout; SE is the jackknife over seeds.

| case | settled radius | canonical D (SE) | canonical label | alt D (SE) | alt label |
|---|---|---|---|---|---|
| J5 (control, the record's junction) | 5 R_fold | 8.834 (0.333) | fails, as FWN1R stored it | 10.897 (0.564) | fails, as FWN1R stored it |
| E0.5 (A3) | 0.5 R_fold | 0.583 (0.050) | FOREST ROW HOLDS AT FLUX LEVEL | 0.794 (0.059) | FOREST ROW HOLDS AT FLUX LEVEL |
| Ec3 (A5) | third caustic, 0.47 to 0.51 R_fold at z 2.2 to 4.4 | 0.512 (0.049) | FOREST ROW HOLDS AT FLUX LEVEL | 0.691 (0.052) | FOREST ROW HOLDS AT FLUX LEVEL |
| Ec2 (A5) | second caustic, 0.60 to 0.65 R_fold | 1.213 (0.095) | FOREST ROW HOLDS AT FLUX LEVEL | 1.648 (0.133) | FOREST ROW HOLDS AT FLUX LEVEL |
| E0.75 (A3) | 0.75 R_fold | 1.909 (0.138) | FOREST ROW HOLDS AT FLUX LEVEL | 2.584 (0.209) | FOREST ROW HOLDS AT FLUX LEVEL |
| E1 (frozen) | R_fold, the first caustic | 3.938 (0.263) | NO VERDICT (unresolved: within 2 SE of 4) | 5.366 (0.390) | FOREST ROW FAILS AT FLUX LEVEL |
| E2 (frozen) | 2 R_fold | 16.37 (0.79) | FOREST ROW FAILS AT FLUX LEVEL | 25.73 (1.96) | FOREST ROW FAILS AT FLUX LEVEL |
| Ezv (frozen) | zero-velocity surface, 2.3 to 3.5 R_fold | 25.06 (1.12) | FOREST ROW FAILS AT FLUX LEVEL | 42.08 (2.86) | FOREST ROW FAILS AT FLUX LEVEL |
| E3 (frozen) | 3 R_fold | 42.76 (1.86) | FOREST ROW FAILS AT FLUX LEVEL | 78.36 (4.47) | FOREST ROW FAILS AT FLUX LEVEL |

- **The junction's own effect (reported, frozen as not a gate):** at 2 R_fold the exact junction reads 16.37 / 25.73
  where the record's junction reads 0.024 / 0.029 (FRZ6R's J2), a factor 671 / 878. At 3 R_fold it reads 42.76 / 78.36
  where the record's reads 0.572 / 0.691 (FWN1R's J3), a factor 75 / 113. Both differ by FWN1R's bite rule.
- **Where the exact junction crosses the gate (reported, interpolated in f between 0.5, 0.75, 1, 2, 3):** D reaches 4
  at f = 1.01 canonical (0.96 to 1.08 for D + 2 SE and D - 2 SE) and at f = 0.89 alt (0.84 to 0.95).
- **Known answers, every one a PASS on both footings:** KA-5 (this lane's R and J5 equal FWN1R's stored parts in all
  96 files, largest deviation 0; J5's D and SE equal FWN1R's to every digit and it still fails), KA-C and KA-INF (read
  from FWN1R's grade file), KA-N (haloes above v* equal JNT2's counts), KA-F (largest 2.0e-14), KA-M and KA-S per case,
  KA-E with A1's tolerance (worst t_min -1.2e-15 in the first pass; 0.78 in the second), KA-Z, KA-R2 (the second pass's
  R equals the first pass's, largest deviation 0), KA-K (24 shell runs reproduce FLD1's stored runs exactly; reader and
  ordering pass).
- **Twins, every one bites:** TW-A (read from FWN1R: 1.50 / 1.26), TW-B at E3 (x 3.58 / 3.78), TW-B2 at E0.75 (x 3.56 /
  3.92).
- **Verification:** both graders were re-run into a separate output folder from the committed parts; every number
  and label is identical (0 differences in each grade file).
- Per case: t (the factor on the reference's shape outside R_set) runs 0.91 to 1.04 at the third caustic and 0.0 to
  1.40 at 3 R_fold; no halo's settled radius is capped at r_ta. The factor s that the record's junction would have
  applied at the same radii runs 0.47 to 1.70 at the third caustic. Per-bin D and R_F are in `xj1b_grade.out` and
  `xj1b2_grade.out`.

## 3. Reported beside the labels (never a label of this lane)

**Matter level, the record's older convention (JNT2's G1 route, gate 4; no gas physics).** Anchors reproduce JNT2's
stored values (record's junction at f 2: 0.0492 / 0.1456; f 3: 1.9898 / 6.4321).

| case | canonical | alt |
|---|---|---|
| Ec3 | 2.87 PASS | 6.37 FAIL |
| E0.5 | 3.43 PASS | 7.65 FAIL |
| Ec2 | 8.15 FAIL | 19.04 FAIL |
| E0.75 | 14.16 FAIL | 33.86 FAIL |
| E1 | 32.22 FAIL | 78.73 FAIL |
| E2 | 134.80 FAIL | 326.90 FAIL |
| Ezv | 176.03 FAIL | 423.28 FAIL |
| E3 | 212.19 FAIL | 494.54 FAIL |

So at matter level the third caustic passes on canonical only and the second caustic fails on both footings. The
record has graded the forest row at flux level since FRZ4; the matter-level number multiplies the data by a matter
power ratio and is kept here because the scorecard still carries a matter-level row (21).

**Lensing, G4 (JNT2's chain, ONE1's KiDS gate as SRH1 ran it; 40,667 host-free lenses), with the exact junction:**
PASS on both footings at every radius of this lane. Early-type z: 0.5 R_fold +0.64 / +1.09; third caustic +0.57 /
+1.04; second caustic +0.28 / +0.85; 0.75 R_fold +0.16 / +0.78; R_fold -0.06 / +0.65; 2 R_fold -0.19 / +0.57;
zero-velocity surface -0.19 / +0.57; 3 R_fold -0.27 / +0.44. The record's junction fails this gate at f = 1 (+2.003 /
+2.037) and passes from 1.25; that lower edge of f does not exist under the exact junction. SRH1R found this gate
cannot see f in a blind build; that stands.

**How far the record's junction sits from the law today (z = 0, SRH1's lens profile):** inside R_set the law's halo
is multiplied by s = 0.47 to 0.93 at f 1.25, 0.57 to 0.78 at f 2, 0.69 to 0.72 at f 3 and 0.56 to 0.79 at the
zero-velocity surface for log M_b 8 to 10.45 (canonical; alt within 0.09 of these). s passes 1 near log M_b 10.7 to 11.2.

**Rotation curves under the record's junction (A2; PD1's P2-SPARC statistic, 175 galaxies; known answer s = 1
reproduces PD1's stored numbers exactly).** Gate: rms at most 0.0660 / 0.0658 for all galaxies and 0.0475 / 0.0426 for
the massive tail; the law itself reads 0.0560 / 0.0558.

| settled radius | canonical | alt | median s | fitted median mass-to-light (law 0.58 / 0.52) |
|---|---|---|---|---|
| 1.25 R_fold | PASS, rms 0.0646 | PASS, rms 0.0640 | 0.75 / 0.68 | 0.79 / 0.75 |
| 2 R_fold | FAIL, rms 0.0682 | PASS, rms 0.0654 | 0.62 / 0.59 | 0.85 / 0.78 |
| 3 R_fold | FAIL, rms 0.0691, massive 0.0480 | FAIL, massive 0.0469 | 0.70 / 0.70 | 0.80 / 0.75 |
| zero-velocity surface | FAIL, rms 0.0680 | PASS, rms 0.0653 | 0.63 / 0.59 | 0.87 / 0.80 |

Under the record's junction 45 to 61 galaxies sit at the top of the mass-to-light grid (the law: 22 to 26). The
scorecard's row 1 reads EQUALS THE LAW under rule 6 from membership alone; with the record's junction that is exact
only where s = 1. With the exact junction it is exact for every galaxy wholly inside the settled radius.

**Where the caustics are (`xj1_shells.py`: FLD1's shell code with a passage counter; all 24 runs reproduce FLD1's
stored series exactly).** R_fold is the first caustic (ratio 1.000 at every redshift). The second caustic is at 0.68
R_fold today and 0.60 to 0.65 at z 2.2 to 4.4; the third at 0.535 today and 0.47 to 0.51; the same within 0.01 for log
M_b 9.4 to 12 (0.40 to 0.47 for the third at log M_b 8 beyond z 2).

**Do today's rotation curves lie inside? (`xj1_contain.py`)** Yes: 0 of 175 SPARC galaxies have their last measured
point beyond the third caustic (largest ratio 0.77, UGC00128; 0.81 at mass-to-light 0.3, UGC09133), the second
(0.60) or the fold (0.41). So with the exact junction at either caustic every SPARC curve is the law's own and PD1's
numbers carry over unchanged.

**The z about 2 discs (read from stored numbers, no new run).** JNT2's stored largest 2.2 R_e / R_fold among the RC100
discs below v*(z) is 0.391 on both footings; the smallest third-caustic ratio over z 0 to 2.7 is 0.446 (log M_b 8) to
0.480 (log M_b 12). So every RC100 disc below v* stays inside the third caustic at 2.2 R_e, and the coverage row is
unchanged: it still fails on coverage only, through the 10 / 2 discs above v*(z).

**The Milky Way's outer mass (`xj1_mw.py`, post hoc reading; PLT1's line and pulls reproduced within 0.4 % and 0.008).**
At log M_b 10.825 the third caustic is at 99 kpc and the second at 127 kpc. Median pulls of the field-star masses /
of the satellite and stream masses beyond 100 kpc: the law at every radius +1.39 / +0.85 (canonical) and +1.57 / +1.18
(alt); exact junction at the third caustic +1.40 / +0.75 and +1.47 / +0.86; at the second caustic +1.37 / +0.70 and
+1.47 / +0.85; the reference at every radius +1.57 / +1.01. The row's reading is not changed by moving the junction
inside 100 kpc.

## 4. Hand estimates against the results

- Criteria section 11 (before any number): E1 0.02 to 0.5 and HOLDS 75 %; E2 0.1 to 3; E3 2 to 20; Ezv 0.5 to 10.
  Results: 3.94 / 5.37; 16.4 / 25.7; 42.8 / 78.4; 25.1 / 42.1. **The estimate was wrong by a factor 5 to 30 at every
  frozen radius**, in the direction it named (the exact junction moves cold mass across R_set) but far larger. The
  frozen favourite, the zero-velocity surface (HOLDS 40 %), fails clearly. TW-B bites (90 %): yes. The junction
  comparison bites at f = 3 (80 %): yes, and at f = 2. Matter level E2 over the gate on alt (60 %): yes, on both.
  Lensing G4 passes at 2, 3 and the zero-velocity surface (70 %): yes, and at the fold.
- A3: matter level 3 to 15 at 0.5 R_fold and 10 to 40 at 0.75 (canonical): 3.43 and 14.2, inside. Flux level E0.5
  HOLDS 60 %: holds. E0.75 HOLDS 40 %: holds. Lensing passes at 0.75 (65 %): yes; uncertain at 0.5: passes.
- A5: matter level Ec3 3 to 5 / 7 to 10: 2.87 / 6.37, just below both ranges. Ec2 7 to 12 / 16 to 28: 8.15 / 19.0,
  inside. Flux level Ec3 HOLDS 60 %: holds. Ec2 HOLDS 45 %: holds. Lensing passes for both (65 %): yes. No SPARC galaxy
  beyond the third caustic (80 %): none.

## 5. What this means for the record (no row is relabelled here)

- Rows 21, 22 and 44 of the scorecard (the forest, and f): the holds at f = 2 and 3 and the window [1.25, between 3 and
  5] were measured on the record's rescaled junction. Under the exact junction the forest allows a settled radius up
  to about the fold radius (canonical) or 0.9 of it (alt), and the lensing gate sets no lower edge down to 0.5 R_fold.
  The lower edge is now set by where rotation curves are measured (0.47 R_fold today; 0.39 for the z about 2 discs).
- Rows that read EQUALS THE LAW or PASSES for the completed form under the record's junction at f in [1.25, 3] were
  graded on, or carried from, a layout with s different from 1 inside (rows 1, 3, 4, 11, 26, 29 to 34, 38, 39, 41).
  For the exact junction at a caustic: rows wholly inside the settled radius are the law exactly (row 1 shown here);
  row 11 passes (shown here); row 30 is read here and does not change. Not re-graded here: rows 7 and 8 (resolved
  discs), 17 and 18 (groups), 24 and 25 (WLJ1's matter-power and lensing-amplitude rows with the split), 31 and 34
  (the Milky Way's enclosed-mass profile and the LMC reflex, which reach past 99 kpc), 35 to 37 (dwarfs against their
  own caustics).
- PAPER72 v1.3 and v1.4 state the forest holds at f = 2 and 3 and call the galaxy rows equal to the law under rule 6.
  Both statements are true of the record's junction only. This lane does not edit or deposit anything.

## 6. What counts against (whatever the labels)

- Everything constructive here is post hoc. The search went: the zero-velocity surface (frozen; fails), then, after
  the matter-level numbers, 0.5 and 0.75 R_fold, then the caustics. A hold of the second or third caustic is a hit
  found by looking, from a family of two.
- The integer k is a choice. k = 1 (the fold) is NO VERDICT / FAILS; k = 2 and k = 3 both hold; nothing here was run
  for k = 4 and beyond, where rotation curves would start to reach outside (the worst SPARC galaxy sits at 0.77 of the
  third caustic). So the forest and the rotation curves leave k = 2 or 3, and they do not choose between them.
- At matter level (the older gate) the third caustic passes on canonical only and the second fails on both.
- A hold here means the layout departs from the reference by little enough at z 2.2 to 4.4. It is not evidence for
  the law inside; it does not separate the framework from LCDM.
- The exact junction is a choice for the outside (the remaining cold mass in the reference's shape). The action
  derives no junction, and none of the caustics: R_2 and R_3 come from FLD1's reflecting-centre device behind the
  fold, where its shell equation is not exact and the action gives no answer (COL1). FLD1's start-redshift brackets
  move R_fold at z 2 by 6 to 8 %.
- The gas inputs are provisional and inherited; build B's grid marginally resolves the smoothing scale; the gate fits
  no gas parameter (FRZ5). The bracket stage had not finished when the labels above were read.
- The boundary v*(z), the coverage row that fails (RC100), form B's failing rows (dwarfs, hosted dwarfs, the halo-star
  row, X-COP's two-sided amount, outer cluster shear) and the fitted constants are untouched.

## 7. Procedure notes

- **Clock times.** FROZEN_CRITERIA.md says "written about 11:40 EST" and AMENDMENT_A1.md "about 12:10 EST"; both were
  guesses and are wrong. A3's header says 11:06; it was committed at 11:03. The commit times are the record: criteria
  10:40, A1 10:43, A3 11:03, A4 11:12, A5 11:19. The frozen files are not edited.
- **A1** exists because KA-E (iv) was frozen as "t >= 0" with no tolerance and the tables gave -4e-16 to -1.2e-15
  where the law's halo reaches its cap. It was committed alone before any box number.
- **A partial look, disclosed.** At 11:44 the first pass was told to stop after its current part (written 11:46; 48
  of 96 primary files, the six bins z 2.2 to 3.2 complete) because free disk had fallen to 13 GB and swap had risen to
  8 GB; the second pass ran in its slot (11:48 to 13:32) and the first pass resumed by itself at about 12:34, when
  another lane's run ended, and finished its primary stage at 13:27. While it was paused, a script
  (`xj1b_partial.py`, output `xj1b_partial_first_pass.out`, committed at 11:50 as 21596c949a) read those six bins:
  E1 3.89 / 5.30, E2 16.1 / 25.3, E3 42.0 / 77.0, Ezv 24.4 / 40.9. No criterion, case, gate or amendment was written or
  changed after that look (A5, the last, was committed at 11:19). The graded 12-bin numbers are within 3 % of it.
- The second-pass runner was stopped and relaunched three times while it had started no part (to add the caustic
  cases, to change the limit on other heavy processes, and to take the paused first pass's slot).
- Both graders were first run at 13:29 to 13:33 with the bracket stage unfinished; their outputs list the missing
  brackets. The lead read the matter-level number of every case before its flux-level number, as A3 and A5 say.
- Build A's agent implemented the exact junction from the criteria text, was told not to open A2, A3, A4's reasons or
  any build-B file, and reported having seen only two single-seed smoke numbers at z 2.2 (SE2 3.27, SEzv 4.06). At
  matter level its numbers (SE2 134.799 / 326.899, SEzv 176.034 / 423.28, SE0.5 3.428 / 7.649) equal build B's to the
  printed digits.
- Nothing was downloaded. Nothing was written outside this folder.

## 8. Files

Criteria and amendments: `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md` to `AMENDMENT_A5.md`. Build B: `xj1_lib.py`,
`xj1_lib2.py`, `xj1b_run.py`, `xj1b2_run.py`, `run_b.sh`, `run_b2.sh`, `parts_b/`, `parts_b2/`, `xj1b_grade.py` ->
`xj1b_grade.json/.out`, `xj1b2_grade.py` -> `xj1b2_grade.json/.out` (and their `_MUTATE` files for the twins).
Profile-level known answers: `xj1_ka_tables{,2,3}.*`. Reported chains: `xj1_matter{,2,3}_<footing>.*`,
`xj1_lens{,2,3}.*`, `xj1_sparc.*`, `xj1_shells.py` and `shells/`, `xj1_contain.*`, `xj1_mw.*`,
`xj1b_partial_first_pass.out`. Build A: `xj1a_*`, `parts_a/`.

## 9. Dated notes

**2026-11-14, 14:14 EST by the clock. Amendment A6 (63aff5a4e6; reported, post hoc, no label, no forest run): how far the
integer can go before rotation curves are cut.** Section 6 says nothing was run for k = 4 and beyond; this note
supersedes that sentence for the rotation curves only.

- `xj1_shells45.py` carries the passage count to 5. All 24 runs reproduce this lane's stored shell runs in their
  first eight columns (largest relative deviation 0). The fourth caustic is at 0.448 R_fold today and the fifth at
  0.389 (log M_b 9.4 to 12, both footings; 0.442 and 0.383 at log M_b 8); at z 2.2 they are at 0.405 and 0.350.
- `xj1_contain45.py`, SPARC's 175 galaxies at z = 0, mass-to-light 0.5: no galaxy's last measured point lies beyond
  the fourth caustic (largest ratio 0.916, UGC00128); one lies beyond the fifth (UGC00128, 1.055). At mass-to-light
  0.3: none beyond the fourth (0.967, UGC09133), two beyond the fifth (UGC00128 1.099, UGC09133 1.112). At 0.8: none
  beyond the fourth (0.869); UGC00128 sits at 1.000 of the fifth. The two footings agree to 0.001.
- So today's rotation curves allow k = 2, 3 and 4 and are cut, by one galaxy and 5 %, at k = 5. The forest was run for
  k = 1, 2 and 3 only; nothing is claimed about it at k = 4. The integer is therefore not fixed by this record: it is
  one of 2, 3 or 4 as far as rotation curves go, and 2 or 3 as far as anything here was graded.
- Hand estimate (A6, before any number): R_4 about 0.44 and R_5 about 0.38 of R_fold (0.448 and 0.389); no galaxy
  beyond R_4 (60 %): none; 1 to 5 beyond R_5 (70 %): one.
- Files: `xj1_shells45.py`, `xj1_contain45.py`, `run_shells45.sh`, `shells45/`, `xj1_contain45.json/.out`.

**2026-11-14, 15:31 EST by the clock. The bracket stage landed (96 files in each pass) and both graders were re-run; these
are the final labels of build B.** Every known answer passes, every twin bites, and both graders reproduce byte for
byte when run again into a separate folder. No D or SE of section 2 changes; the brackets add the FRAGILE flags.

| case | canonical, final label | alt, final label |
|---|---|---|
| E0.5 | FOREST ROW HOLDS AT FLUX LEVEL | FOREST ROW HOLDS AT FLUX LEVEL |
| Ec3 | FOREST ROW HOLDS AT FLUX LEVEL | FOREST ROW HOLDS AT FLUX LEVEL |
| Ec2 | FOREST ROW HOLDS AT FLUX LEVEL | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) |
| E0.75 | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) | FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5; gam_1.6) |
| E1 | NO VERDICT, FRAGILE (lam_x0.5; gam_1.6; tau_x0.9) | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lam_x2; gam_1.2) |
| E2 | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lam_x2) | FOREST ROW FAILS AT FLUX LEVEL |
| E3 | FOREST ROW FAILS AT FLUX LEVEL | FOREST ROW FAILS AT FLUX LEVEL |
| Ezv | FOREST ROW FAILS AT FLUX LEVEL, FRAGILE (lam_x2) | FOREST ROW FAILS AT FLUX LEVEL |

Lane words with the flags, canonical / alt:
- Q1: THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION / the same. E3 fails under every bracket on both footings (lowest
  5.08 / 12.88, at twice the smoothing scale). E2 on canonical is FRAGILE: twice the smoothing scale gives 2.19, and
  over the measured range of that scale (PROVISIONAL, reported) it runs from 11.07 to 3.24, failing at one end and
  holding at the other; on alt it fails throughout (17.49 to 6.39; lowest bracket 4.97).
- Q2, the fold: NOT RESOLVED (the fold radius): NO VERDICT, FRAGILE (lam_x0.5; gam_1.6; tau_x0.9) / FAILS (the fold
  radius), FRAGILE (lam_x2; gam_1.2). Q2, the zero-velocity surface: FAILS (the zero-velocity surface), FRAGILE
  (lam_x2) / FAILS (the zero-velocity surface).
- Q3: A WINDOW IS LEFT: f in [0.5, 0.75] (FRAGILE: FRAGILE (lam_x0.5; gam_1.6)) / the same (the doubled word is the
  grader's formatting; the flag belongs to the 0.75 end).
- Q4, the second caustic: HOLDS WITH NO FREE CONSTANT (the second caustic) / HOLDS WITH NO FREE CONSTANT (the second
  caustic), FRAGILE (lam_x0.5). Q4, the third caustic: HOLDS WITH NO FREE CONSTANT (the third caustic) / the same,
  with no flag.

The brackets of the two caustic cases (12-bin estimates; gate 4):

| bracket | Ec3 canonical | Ec3 alt | Ec2 canonical | Ec2 alt |
|---|---|---|---|---|
| smoothing scale x 0.5 | 1.632 | 2.115 | 3.955 | 4.385 |
| smoothing scale x 2 | 0.044 | 0.082 | 0.120 | 0.211 |
| gamma 1.2 | 0.139 | 0.231 | 0.348 | 0.577 |
| gamma 1.6 | 1.250 | 1.307 | 3.102 | 3.305 |
| tau_eff x 0.9 | 0.584 | 0.774 | 1.396 | 1.863 |
| tau_eff x 1.1 | 0.456 | 0.623 | 1.073 | 1.474 |
| measured range, 91.4 to 138.6 comoving kpc (reported) | 0.406 to 0.070 | 0.443 to 0.114 | 0.912 to 0.192 | 1.107 to 0.293 |

- **The third caustic holds under every frozen bracket on both footings**, the halved smoothing scale included; so
  does 0.5 R_fold (largest bracket 2.04 / 2.63). The second caustic holds under every bracket on canonical, by a
  margin of 0.05 at the halved smoothing scale, and crosses the gate there on alt.
- Limits that stand: FWN1R's cell is 77 comoving kpc, so half the smoothing scale is not resolved by this build, and
  the look-up GAS1 (PROVISIONAL) puts that half scale mostly outside the measurements. A hold that is not FRAGILE is
  still a post hoc hit from a family of two, in one build.

**2026-11-14, 15:31 EST. What landed beside this lane after the first writing, and one correction.**
- **Charge conservation at the junction.** The Codex session's note
  (`codex_mass_budget_2026_11_14/latest_review/JUNCTION_THEOREM.md`), its independent audit
  (`reviews/codex_mass_budget_audit_2026_11_14/`) and lane CSD1
  (`closure_2026_11_14/CSD1_charge_delivery_at_the_caustic/`) bear on this lane's caustic layouts as states the clock
  could reach. With no surface reservoir a conserved current obeys [J^r] - Rdot [J^t] = 0 at the junction; the
  action's non-advective flux is 3e-7 to 5e-7 of the advective one for a Milky-Way-mass system at 100 kpc; over 7,110
  snapshots of Ec2 and Ec3 the law's density just inside the caustic is below the outer density in 3,706 and above it
  in 3,373; and the clock's own shell flow delivers 0.9 to 6.8 % of the charge the law's halo needs inside the third
  caustic (1.7 to 12 % with a cosmologically seeded patch), while the reference layout taken as the supply holds 0.49
  to 1.67 of it. So Ec2 and Ec3 pass profile gates as drawn profiles; no flow of the action is shown to assemble them.
  This lane's exact junction pays for the law inside R_set by rescaling the outside (t), which moves charge across the
  junction by fiat. Lane BJ1 (`closure_2026_11_14/BJ1_charge_budget_junction/`, criteria 9e7ce0dfe6) grades the
  layout that moves none.
- **The blind lane XJ1R's light stage** (built without sight of this lane's numbers) gives the same caustic ratios, no
  SPARC galaxy beyond either caustic (largest ratios 0.602 and 0.767) and the same matter-level numbers (8.146 / 19.037
  and 2.872 / 6.368). Its forest run, the part that grades the hit, had not started when this note was written.
- **Correction.** Section 6 and `COMPLETED_FORM_V2_CANDIDATE.md` list X-COP's two-sided amount among form B's failing
  rows. Since CJ1's tenth scorecard update (4767bb49f2, 14:10 EST, on the owner's decision) that row reads DEPENDS ON
  AN UNTESTED ASSUMPTION, not FAILS; form B's failing rows are the outer cluster shear, the halo-star row, the
  ultra-faints and M31's bright dwarfs, and the hosted low rows.

**2026-11-14, 16:04 EST. Amendment A7 (4ac81dbc01; reported, post hoc, no label): the lens profile inside the settled
radius, with FRZ1's leftover term.** The lens chain of section 3 used the law's capped halo alone inside R_set; the
forest tables use FRZ1's mode "B", which adds the unused share spread in proportion to radius where the law's halo has
not used the whole share by the turnaround radius. BJ1's builder pointed out the difference. `xj1_lens4.py` repeats G4
for Ec2 and Ec3 with the term included.
- The leftover term is not zero in 285 of 2,178 lens-table cells on canonical and 199 on alt (largest 0.40 / 0.34 of
  the share; it adds up to 81 % / 61 % to the enclosed cold mass at R_set in those cells).
- The gate does not move: PASS for both cases on both footings, with every statistic equal to the stored one to the
  four printed decimals (early-type z: Ec2 +0.2764 / +0.8530, Ec3 +0.5674 / +1.0407). The cells with a leftover term are
  the systems whose law halo cannot use the share, which the boundary v*(z) already hands to the reference, so the
  term never reaches a lens that carries the exact junction.
- Hand estimate (A7): the early-type z moves by less than 0.1 and both words stay PASS: yes. "Zero for most lenses":
  it is zero for every lens below v*, and not zero in about a tenth of the table's cells.
- The frozen cases (E1, E2, E3, Ezv) and A3's two radii were not re-run with the term; the same argument applies to
  them, and it is an argument, not a computation.

**2026-11-14, 16:19 EST. Lean certificate (on the owner's instruction; it certifies algebra, not physics, and no number
or label).** `XJ1.lean`: the exact junction's outside factor and total (`junction_factor`, `junction_total`), its
sign (`junction_factor_nonneg`), monotonicity outside R_set (`junction_outside_monotone`), and that FZS1's rescaled
inside is the law exactly when s = 1 (`rescaled_is_law_iff`, `rescale_gap`). Compiled against the repository's
Mathlib build: `compile.txt` ends "exit 0" with no error. The twin `XJ1_MUTATE.lean` states four false variants;
`compile_MUTATE.txt` ends "exit 1" with one error per theorem.

**2026-11-14, 16:31 EST. Build A landed (criteria section 8 as changed by A4): the read-across at 0.5 and 2 R_fold.**
Build A is the second, independently written implementation of the exact junction, in FWN1's build (12 seeds at z 2.2,
seed 0 at five other redshifts). It was graded by the lead with the builder's committed grader
(`xj1a_grade.py canonical`, `alt`). Every known answer of that build passes on both footings (its control equals
FRZ6's stored one exactly and still fails; its junction's profile checks pass) and both twins bite. It landed after
PAPER72 v1.5 was deposited, so it is not in that version.

| case | build A, canonical: D (SE); label | build A, alt | build B, canonical | build B, alt |
|---|---|---|---|---|
| E0.5 | 0.780 (0.409); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) | 1.246 (0.670); FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) | 0.583 (0.050); HOLDS | 0.794 (0.059); HOLDS |
| E2 | 16.45 (7.02); NO VERDICT (unresolved at 12 seeds: D 16.5, SE 7.02) | 22.84 (7.75); FOREST ROW FAILS AT FLUX LEVEL | 16.37 (0.79); FAILS, FRAGILE (lam_x2) | 25.73 (1.96); FAILS |

Read across, per footing (reported, never a label on the theory):
- **E0.5: HOLDS IN BOTH BUILDS / HOLDS IN BOTH BUILDS.** In build A the hold is FRAGILE to half the gas smoothing
  scale on both footings (29.9 / 74.7 there); in build B it is not (2.04 / 2.63). Neither build's grid resolves that
  half scale in the same way, and the look-up GAS1 puts it mostly outside the measurements.
- **E2: NOT RESOLVED / FAILS IN BOTH BUILDS.** On canonical the two builds agree in size (16.45 and 16.37) and differ
  in word, because build A's seed error at 12 seeds is nine times build B's; on alt both fail.
- Against FZS1's junction in the same build (FRZ6's split at f = 2: 0.196): the exact junction is 84 times higher on
  canonical, which bites by FWN1R's rule.
- Matter level in build A: 3.428 / 7.649 at 0.5 R_fold and 134.81 / 326.91 at 2 R_fold, equal to build B's chain to four
  figures.
- So the junction finding (Q1) is reproduced by an independently written implementation on alt and in size on
  canonical, and the hold just outside the third caustic is reproduced on both footings. The caustic cases themselves
  (Ec2, Ec3) were not in build A; the blind lane XJ1R grades them.
- Files: `xj1a_grade_<footing>.json/.out`, their `_MUTATE` files, `parts_a/` (40 files).

**2026-11-14, 21:20 EST. The blind lane XJ1R landed** (`closure_2026_11_14/XJ1R_blind_caustic_junction/RESULT_BLIND.md`;
its own caustic computation and junction in FWN1's build, grader committed before any heavy part; graded by the lead
with that grader unchanged). Its lane words on both footings: CAUSTIC 2 HOLDS, BLIND, FRAGILE (lam_x0.5) and CAUSTIC 3
HOLDS, BLIND, FRAGILE (lam_x0.5). Numbers: third caustic 0.760 (0.389) / 1.141 (0.595), second 1.553 (0.708) / 1.660
(0.852), against this lane's 0.512 / 0.691 and 1.213 / 1.648; its control equals FWN1's stored one; every known answer
passes and both twins bite. So Q4's two holds are confirmed as labels by a blind build on both footings. The builds
differ on half the gas smoothing scale: there the blind build reads 33.9 / 47.5 for the third caustic and this
lane's build 1.63 / 2.12, so the hold is FRAGILE to that bracket in one build and not in the other. It landed after
PAPER72 v1.5 was deposited and is not in that version. What counts against the holds (section 6 and the notes above:
post hoc choice of caustic; a drawn profile that no flow of the action assembles; BJ1's charge-conserving layout fails
the forest) is unchanged by a blind confirmation.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
