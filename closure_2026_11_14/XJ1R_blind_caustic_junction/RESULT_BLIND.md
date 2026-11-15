# XJ1R RESULT (BLIND): the law unscaled inside the second and third caustic, graded in an independent build

2026-11-14, written 21:20 EST by the clock. Blind re-grade of the caustic cases of lane XJ1. The builder worked from
`BLIND_BRIEF.md` (b4eb931fe3 on origin) without sight of any number of XJ1; it froze its own criteria
(`FROZEN_CRITERIA.md`, committed alone), wrote its own caustic computation and its own exact junction in FWN1's forest
build, committed its grader before any heavy part existed, launched the forest run and handed back. The run finished
at 21:17 EST (40 parts). The lead, who is not blind, then ran the builder's committed grader unchanged
(`xj1r_grade.py canonical`, `alt`) and wrote this file; nothing of the build was altered after the numbers were seen.
TEST lane. Adopts nothing, relabels nothing. Footings never pooled. A HOLDS means "not excluded in this build"; it does
not say the data favour the framework.

## 1. Lane words (brief section 3; the builder's criteria section 8)

| | canonical | alt |
|---|---|---|
| second caustic | CAUSTIC 2 HOLDS, BLIND, FRAGILE (lam_x0.5) | CAUSTIC 2 HOLDS, BLIND, FRAGILE (lam_x0.5) |
| third caustic | CAUSTIC 3 HOLDS, BLIND, FRAGILE (lam_x0.5) | CAUSTIC 3 HOLDS, BLIND, FRAGILE (lam_x0.5) |

## 2. Gate (a), the forest at flux level (FWN1's build: 12 seeds at z 2.2, seed 0 at five other redshifts; gate 4)

| case | canonical: D (SE); D + 2 SE; label | alt: D (SE); D + 2 SE; label |
|---|---|---|
| SEc2 | 1.553 (0.708); 2.970; FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) | 1.660 (0.852); 3.363; FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) |
| SEc3 | 0.760 (0.389); 1.537; FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) | 1.141 (0.595); 2.331; FOREST ROW HOLDS AT FLUX LEVEL, FRAGILE (lam_x0.5) |
| control S5 (FZS1's junction at 5 R_fold) | 8.085 (2.414), equal to FWN1's stored value; above the gate | 9.448 (2.790), equal to FWN1's; above the gate |

- Every known answer passes on both footings (the control's fields and graded value equal FWN1's; the junction's
  profile checks; the caustic checks KS1 to KS4) and both twins bite (the change doubled in every box: x 3.03 / 4.08 for
  SEc2 and x 3.27 / 3.51 for SEc3).
- **Brackets (12-bin estimates).** Half the gas smoothing scale takes every case far over the gate in this build:
  SEc2 46.5 / 60.4, SEc3 33.9 / 47.5. Every other frozen bracket stays under it: the largest is gamma 1.6 at 3.46 / 3.36
  for SEc2 and 1.58 / 1.57 for SEc3; twice the smoothing scale gives 0.07 / 0.41 and 0.04 / 0.12; over the measured
  range of the smoothing scale (reported) SEc2 runs 0.82 to 0.10 / 1.93 to 0.88 and SEc3 0.43 to 0.09 / 1.06 to 0.49.
- Matter level by the record's older route (reported, never a label): SEc2 8.147 / 19.038, SEc3 2.872 / 6.369.

## 3. Gate (b), rotation curves

No SPARC galaxy has its last measured point beyond R_2 or R_3 at z = 0 on either footing, at mass-to-light 0.5, 0.3 or
0.8. Largest ratios at 0.5: UGC00128 0.602 (second caustic) and 0.767 (third). So a galaxy's curve inside the settled
radius is the law's own and PD1's numbers carry over. (`xj1r_rc.out`.)

## 4. Beside XJ1 (added by the lead after grading; the builder never saw these)

| | XJ1 build B (FWN1R's library, 4 seeds in 12 bins) | this lane (FWN1's build, blind) |
|---|---|---|
| third caustic, canonical / alt | 0.512 (0.049) / 0.691 (0.052); HOLDS / HOLDS, no flag | 0.760 (0.389) / 1.141 (0.595); HOLDS, FRAGILE (lam_x0.5) on both |
| second caustic | 1.213 (0.095) / 1.648 (0.133); HOLDS / HOLDS, FRAGILE (lam_x0.5) | 1.553 (0.708) / 1.660 (0.852); HOLDS, FRAGILE (lam_x0.5) on both |
| half the smoothing scale, third caustic | 1.63 / 2.12 | 33.9 / 47.5 |
| caustic ratios, containment, matter level | | the same to the printed digits |

- **The blind build confirms XJ1's two holds as labels, on both footings.** It is the first hit of the candidate
  sixth rule that a blind build has confirmed as a label.
- The two builds disagree on one thing: what half the gas smoothing scale does. In XJ1's build the third caustic stays
  under the gate there; in this build nothing does. Neither grid resolves that half scale, and the look-up GAS1
  (PROVISIONAL) puts it mostly outside the measurements. The flag stays.

## 5. What counts against

- The statement graded was found by looking, in XJ1, from a family of two caustics after other radii had failed. A
  blind build confirms that the layout is not excluded by the forest in a second build; it does not make the choice of
  caustic any less post hoc.
- A hold means the layout departs little enough from the reference at z 2.2 to 4.4. It is not evidence for the law
  inside, and it does not separate the framework from LCDM.
- The layout is a drawn profile. CSD1 finds that the clock's own flow delivers 1 to 12 % of the charge the law's halo
  needs inside the caustic, and BJ1 finds that the layout which conserves charge fails the forest at flux level.
  Neither the junction nor the caustic follows from the action.
- FRAGILE to half the gas smoothing scale in this build. The gas inputs are provisional and inherited.
- The builder's disclosures stand: the control's "must still fail" was read as D above 4 (FWN1's own label for it is NO
  VERDICT); the control was recomputed at two seeds for field identity and graded from FWN1's parts; one test part ran
  as a fourth heavy process for two minutes; it saw one PAPER72 commit subject in the commit list, which carried no
  number of the caustic cases.

## 6. Files

`BLIND_BRIEF.md`, `FROZEN_CRITERIA.md`, `xj1r_shells.py`, `xj1r_rk.*`, `xj1r_rc.*`, `xj1r_tables.py`, `xj1r_run.py`,
`xj1r_c0*`, `xj1r_grade.py`, `xj1r_grade_<footing>.json/.out` and their `_MUTATE` files, `parts/` (40 files),
`runs/` (24 shell runs).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
