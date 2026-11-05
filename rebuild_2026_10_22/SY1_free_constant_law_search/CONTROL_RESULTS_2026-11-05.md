# SY1 controls completed, 2026-11-05

Completed at 09:53 Eastern. All 166 searches have both a DONE record and
progress=1500: planted64, real48, scrambled48, mutation6. Independent
verify_controls.py checks every expected job and records hashes in
CONTROL_VERIFICATION_2026-11-05.json. These hashes are a retrospective snapshot,
not invented before-run provenance.

Both arms recover every required planted form. The strict mutation gate returns
zero survivors on both its own fronts and the real fronts: T0/86 and0/641;
Z0/88 and0/679. Those are the known-answer and rejection checks that passed.
The shuffled-y baseline returns444 distinct Stage1 hits in the typed arm
(660 grammar entries), and97 in the zero-float arm (694 grammar entries).
This is a baseline count, not a failed frozen threshold: none was specified.
It means a training-set hit alone is not evidence of a new law. The reader
stores only the first200 scrambled survivors where the count exceeds200.

The interrupted scrambled search was actually stuck in SymPy export after a
Julia search slice, not blocked by L1 memory demand. The tested export fix is
commit4616c17563. The repaired detached run completed all searches and read
controls in the prescribed order. L1 and CB1 holds were not changed.

Real holdout grading was started only after these controls completed. A full
Stage3 pass was also attempted: the first candidate sy1_T_1 completed and was
REJECTED on both footings (30/33 FAIL, respectively). The next candidate sy1_T_4 also completed before its stop signal arrived;
its stored result is REJECTED on both footings. Both completed outputs are
retained. The parent acceptance pass was stopped before grading the full set. Full
Stage3 grading of the remaining candidates is pending and must not be labeled
as completed or replaced by the favorable intermediate gate counts. The
separate Stage1/Stage2 reader can complete without those expensive calls.

The original reader uses the string "HOLDS OUT, FAILS ACCEPTANCE (stage 3
pending)" before acceptance runs. In that case only HOLDS OUT and STAGE3 PENDING
are established; do not turn the wording into an actual acceptance-failure
claim. No candidate has been established as a healthy action by SY1.

Kappa=1/2 FITTED. A fitted rule is a data description, not a derived action.

## Completed Stage1/Stage2 holdout grading

The separate reader completed both arms under the original200-candidate cap.
Typed arm:363 Stage1 survivors versus444 scrambled; zero-float:262 versus97
scrambled. Fronts and candidates are correlated; these are not independent
trial counts and no significance level is inferred.

| arm | graded | canonical G3/G4/G5 | alternate G3/G4/G5 |
|---|---:|---|---|
| T | 200 | 183 / 175 / 161 | 105 / 104 / 0 |
| Z | 200 | 176 / 176 / 161 | 57 / 56 / 0 |

Thus161 candidates per arm pass Stage2 on the canonical footing, but none
of the400 graded candidates passes G5 on the alternate footing. Candidates
outside the200-per-arm cap were not graded. Full acceptance is still pending
for the canonical survivors except sy1_T_1 and sy1_T_4, both already rejected.
The no-stage3 summary file does not merge those separate completed Stage3
results; consult results/sy1_T_1.json and results/sy1_T_4.json explicitly.
No SURVIVOR or healthy-action claim is supported by these results.
