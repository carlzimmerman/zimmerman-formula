# Final verification

The corrected sources are recorded in commit `e8bebc5f8303540dc1c0ea4d6cbf432bb03ed870` on the local checkpoint branch `codex/mass-budget-2026-11-14`. The active shared checkout and its index were not switched to this branch.

## Observed checks

- PAPER72: **1,584/1,584** literal/provenance and limited arithmetic checks pass.
- PAPER72 mutation check: **1,567/1,567** checks pass. These mutate source literals; they are not physics-model falsification tests.
- CJ1: **128/128** scorecard checks pass.
- WLJ1: **7/7** full-grader regression tests pass; all six saved grading outputs are byte-identical; the reconstructed shared-flag bug is rejected. An independent reviewer also ran the seven tests successfully.
- **Nine accepted computation manifests** validate against current input/output hashes, each with `run.status=completed`: calculation runs 001–004 and 006; latest_review run 007; both latest_sn_review runs; WLJ1 run 01. `accepted_manifests.json` stores each validator result.
- Corrected PAPER72 TeX compiled successfully with the desktop compiler. `../latex_compile.json` stores its actual response.
- Changed existing sources pass `git diff --check`.
- The local deposited v1.4 PDF and supplement still match the MD5 values in their unchanged deposit receipt.

The paper audits were run with a temporary Git context whose HEAD is the genuine correction commit, with object reads from this repository and the shared working tree explicitly selected. This preserves the audit's committed-source requirement without moving Claude's active main branch. The six source hashes matched before and after. `audit_results.json` records the context, hashes and outcomes. The first CJ1 launch failed because the temporary bare context had no worktree; its traceback and initial result are preserved, then the explicit worktree configuration fixed the harness. No source or test was changed to resolve that launch failure.

Earlier diagnostic computation records are retained as history and are not presented as accepted runs. In particular, calculation run 005 failed during JSON serialization; run 006 is the successful unchanged-formula replacement. Earlier latest_review records predate the final source/proof changes; run 007 is authoritative here.

The independent mathematical/code review is `../INDEPENDENT_REVIEW.md`. It checked the same-radius mass algebra, source/units, actual-profile reconstruction, full-current matching, restricted stationary obstruction, constructive continuity theorem and finite-charge radius bound. It resolved the overly broad phrase "inner law" in favor of "supplied B interior" and required a C1 mixing schedule.

These checks establish the stated finite computations and conditional mathematical claims. They do not establish a dynamically closed gravity theory or a TOE.
