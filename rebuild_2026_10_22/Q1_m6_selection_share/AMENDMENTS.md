# Q1_m6_selection_share: AMENDMENTS

## A1 (after the first complete run, before the rerun; label only)

- **What happened.** The first complete run (script a2b07453d4) passed 7/7 checks. The graded verdict was BUDGET BINDS AT
  RECORD RETENTION on both footings. Two *reported* variant verdicts (alt, band +0.5 dex and SAT-LOW) printed
  "MIXED:  within budget at eps_ref" with an empty corner list. In those variants one corner (q_hi, stars + cold gas,
  q → 1) exceeds F_allowed even at full retention, so the case falls to MIXED, but the label only listed corners within
  budget at ε_ref.
- **Change.** The MIXED label now names the corners in each state, following criteria §4 ("the flipping corners are
  named"): corners over budget at full retention, and corners within budget at ε_ref. No number, rule, threshold or
  check changes. The graded verdicts are not MIXED, so they are unaffected.
- The first run (an earlier, pre-run attempt stopped at Step 0 with a missing-file error before any number; the untracked
  closure population file was then copied into this worktree with the pinned sha256) is otherwise the run reported.
