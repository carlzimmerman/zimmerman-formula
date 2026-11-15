# WLJ2 LEAD CHECK (2026-11-14): commit ids, the lead's re-runs, the comparison with WLJ1, and how far the words go

Written by the lead session after the lane's result was committed. TEST lane, not blind; adopts nothing, relabels
nothing. The agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| frozen criteria (alone) | c3bc2d3871 | c2d89bc0b2 |
| scripts and first-stage outputs (halo model, C4, the reported diagnostic) | 5509573df4 | 4295b94b5c |
| run outputs of the long stages and the grader outputs | 43bbb06ead | 61fe3c8598 |
| RESULT.md | b1287ac89c | 38e7e4f382 |

## What the lead checked

- **Order.** The criteria were committed alone at 13:52 EST, 17 minutes before the first script commit. The agent's tool
  calls were listed by script: 104 calls, no web call, no push, no history rewrite. It read WLJ1's and XJ1's results
  before the freeze, as its criteria say, so the lane is not blind.
- **Graders re-run.** Every tracked file of the lane was copied into a new folder at the same depth (not committed,
  removed afterwards). `wlj2_grade.py` and `wlj2_grade.py --as-frozen` were run there. All six grader output files are
  byte-identical to the committed ones.
- **First stage re-run.** `wlj2_hm.py`, `wlj2_c4.py` and `wlj2_diag.py` were run from scratch in the same copy (279 s
  for the halo model). The five data files (`wlj2_hm.json`, `wlj2_hm_MUTATE.json`, `wlj2_c4.json`, `wlj2_c4_MUTATE.json`,
  `wlj2_diag.json`) and `wlj2_diag.out` are byte-identical to the committed ones. The four printed outputs of the halo
  model and C4 differ only in their elapsed-time stamps.
- **Long stages not re-run.** The shear stage, LWB1, LWB1R and the six KL1 / BX1 groups took 8 h 56 min of compute and
  were not repeated by the lead. Their nine stage markers all hold exit code 0, and the disk and swap guard never
  tripped (free disk 13 GB or more, swap 5.4 GB or less).
- **WLJ1's stored numbers reproduced, checked with the lead's own comparison** (not the lane's known answers). For the
  three cases the two lanes share (REF, ADOPT and the split at f 2), every number the two lanes both store was compared
  file against file:

  | stage file | numbers compared | largest relative difference |
  |---|---|---|
  | halo model | 47,544 | 0 |
  | C4 | 114 | 0 |
  | shear (C5, HLF1, P4, T1) | 774 | 0 |
  | LWB1 | 962 | 0 |
  | LWB1R | 846 | 0 |
  | KL1 / BX1, legacy (each footing) | 1,956 | 0 |
  | KL1 / BX1, DES and KiDS-1000 (each footing) | 2,384 | 0 |
  | KL1 / BX1, polished (each footing) | 328 | 0 |

  At gate level, the 148 numbers of the 54 gate entries the two graders share differ by 0. The differences are in
  words only:
  - WLJ1's grader appended "WITH THE SPLIT" to REF's and ADOPT's words; WLJ2's does not.
  - The costly brackets were run at Ec2 only. So the split's bracket lists for KL1, BX1, LWB1 and LWB1R are absent
    here, and its FRAGILE tags on LWB1 and LWB1R, which stand in WLJ1, do not appear in this lane's grade.
- **RESULT.md against the grader's output.** The tension table, the row words and the twin line agree with
  `wlj2_grade.out`.
- **Files.** No home path in any committed file. The run logs are untracked because they carry machine paths.

## How far the words go, in the lead's reading

1. **Row 25's fail is mostly the reference's own.** By the same gate rule the pure reference reads ROW FAILS: KL1's
   DES row is +2.16 / +2.11 widths, over the line at two, with no junction at all. The reference's shear p is 0.00315,
   just above the 3 sigma line at 0.0027. The exact junction adds 0.3 to 3.1 (canonical) and 0.8 to 6.8 (alt) to a
   chi^2 of about 156, which carries p under that line at four of the five graded radii. So the lane shows no relief
   and a small worsening. It does not show a new failure that the junction creates.
2. **Size.** The largest move is +0.54 widths of raw KiDS (alt, 0.5 fold radii) and +0.73 widths of the Legacy gap
   (alt, third caustic), against a tension of about 5.4 widths. On alt the raw-KiDS statistic is not one the rule
   uses, because the doubled-layout twin does not bite on it; it moves the same way.
3. **One fold radius is marginal.** On canonical the word at E1 rests on one statistic at +0.043 against a floor of
   0.02. The floors were the agent's own choice from WLJ1's scatter, frozen before any number, and the result says so.
4. **Row 24.** The one departure is alt at the third caustic: raw-KiDS d_cold 4.85 against the line at 4. Every other
   graded radius holds on both footings. No hold differs from the adopted form's word, so nothing is a hit and no
   blind re-grade is owed. The other side of that: the worsening is not blind-confirmed either.
5. **The direction was a surprise and is traced, not independently rebuilt.** The agent expected the exact junction to
   sit between the split and the full law in small-scale power. At the caustics it is above the full law. The lane's
   reported diagnostic puts this in groups of log M 13 to 14.1 just below the crossing speed, where the law holds more
   cold mass inside the settled radius than the reference does and the rest is laid outside in the reference's shape.
   The two limiting checks pass (settled radius 0 gives the reference, settled radius at turnaround gives the adopted
   form). The lead re-ran the diagnostic but built no second halo model.
6. **What it inherits.** XJ1's layout: the rule for the mass outside the settled radius is a choice no action derives,
   and the caustic radii were found by looking. At z = 0 the baryon mass above 10^12 solar masses is extrapolated with
   FZS1's M_b^(1/3) rule, and that range covers the groups that carry the whole signal. KL1 and BX1 transfer the
   junction onto RB1's gas layout and do not rebuild it.
7. **Scorecard.** Rows 24 and 25 keep their words for the completed form (PASSES TRIVIALLY and NO POWER). Both were
   placed for the record's junction, and this lane grades a different layout. Their notes now record this lane. Under
   the exact junction row 25 would be placed FAILS, as the adopted form is; that change is the owner's decision.
8. **Compute.** The stage chain ran from 14:08 to 23:04 EST, 8 h 56 min: shear 51 min, LWB1R 14, LWB1 33, and the six
   KL1 / BX1 groups 50, 94, 46, 91, 80 and 76 min. The brief said about half an hour. That estimate was the lead's
   error: it was taken from two of WLJ1's stage logs and left out the KL1 / BX1 scans.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
