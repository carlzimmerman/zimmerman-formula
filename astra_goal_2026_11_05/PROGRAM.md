# Active all-lanes research program

Owner target: execute `ASTRA_GOAL_2026-11-05_HANDOFF_LANES.md` completely,
tier by tier, with new frozen criteria, actual rerunnable computations,
known-answer checks, negative controls, two footings and numerical convergence.
Start: brief revision `97f1753e4a`; current shared checkout may advance.
Kappa = 1/2 FITTED; not theory closed. Adopt nothing and do not push.

Additional owner instruction: do not trust inherited verdicts. Inspect raw
actions, code, numerical evidence and applicability before transferring a
claim, including the coordinator's previous AZC1 construction.

## Execution state

- Tier 1 lane 1: AZ31 main PASS both; screening-off physical/reference checks
  fail but its convergence label remains UNDECIDED. Results complete.
- Tier 1 lane 2: AZ32 committed96fb3e43fa. Radial ladder/restricted TT PASS
  both; full mixed-mode W4c UNDECIDED. Negative controls bite.
- Tier 1 lane 3: AZ33 committed47da097d08. LW1 folded; both vertical forms
  visible, 34/34 board controls caught, all32 integration checks pass.
- Tier 1 lane 4: AZ34 criteria825835993f; partial structural audit executed.
  Exact bounded-energy/unbounded-H(div) witness confirms an existence-proof
  gap, not nonexistence. Matter conservation's off-shell-zero wording is
  disproved; the matter-shell Noether identity is verified. Original global
  quadrature fails two checks; separately frozen post-result A1 mapped
  quadrature passes unchanged tolerances. Inverted switch bites. BH and
  coupling recomputations and the six-tile board regrade remain pending.
  C8's no-radiative-channel claim conflicts with P3; preserve this caveat.
- Tiers 2-5: pending, in the order specified by the brief.
- Lane 5 will have five separately frozen sublanes, with separate verdicts.
- Lane 19 requires a beta-term health test before any queued disc run.
- Other sessions have now landed W1/X1 updates (handoff bfe49ed3c2,
  X1 c36e9a00b7). Re-read their outputs in Tier4; do not duplicate their runs.

No lane is complete merely because its old README was read. Summary rows will
only acquire final labels from executed checks or explicit inaccessible-input
evidence. `SUMMARY.md` will be the end-of-program deliverable; this file is the
live execution record.

## Preserved missing-link leads for the action tier

Before this all-lanes goal arrived, a separate review froze a constant-w
potential-portal branch check at `reviews/missing_links_2026_11_04/` (commit
1a9955b2a9); it has not run. Resume it in the new lane-6 scope only after Tier 1.
Other source-level concerns to test: FN1b/FN6's Gaussian operator is not v3s;
CT14's polarization-conjugate acceleration must be mapped to a screened
background; CQ7's satellite solver carries an unswitched branch caveat.
These are audit leads, not changed verdicts.

## Shared-state safeguards

Other sessions own AZ27-AZ30 and existing uncommitted files. New lane ids start
at AZ31 after checking all-history log and folders. Never edit their folders.
Only the specified status-board files are an authorized shared edit exception.
Commit with explicit paths. Heavy work must use the existing queue; preserve
L1 checkpoints. No downloads, deposits, sending or pushes in this run.
