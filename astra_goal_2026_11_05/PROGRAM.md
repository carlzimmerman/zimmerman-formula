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
- Tier 1 lane 4: AZ34 calculationsc869c20b96. Six switched-action claims
  regraded. Radiation/physical causality NO VERDICT; leaf existence/regularity
  UNDECIDED. Matter-shell identity PASS; off-shell-zero wording corrected.
  Coupling estimates and60 BH convergence pairs PASS within reduced scope.
  Inverted-switch control bites. Original global-quadrature failures retained;
  separately frozen mapped diagnostic passes. Board27/27 integration checks,
  37/37 selftest mutants caught; both explicit board mutants exit1.
- Tier 1 is complete to scoped labels, not full dynamical health.
- Tier 2 lane 5(a): AZ35 complete to NO VERDICT on full nonlinear
  well-posedness. New exact derivative-loss diagnostic in density/velocity
  variables, with a frozen polarization-variable repair; principal-only
  caustic verified, not promoted to a full-action counterexample. Main18/18,
  mutant15/18, all numerical convergence/known-answer checks pass.
- Tier 2 lane 5(b): AZ36 complete to NO VERDICT on full nonspherical
  PN signs. Exact conditional radial UV kinetic/gradient signs derived
  without a PN expansion, including lapse/shift and matter cancellation.
  Main26/28 retains two float64 misses; mutant24/28 additionally fails
  gradient signs. Separately frozen stable-offset diagnostic passes.
- Tier 2 lane 5(c): AZ37 complete to NO VERDICT on the selected moving
  Sun. Exact conditional v3s GR/geodesic branch verified; all tested
  incoming ray families focus downstream outside the Sun. Main87/87,
  flat-profile mutant69/103; charged-background response36/36 with paired
  ODE solves and independent convolution. Nonlinear Galactic matching open.
- Tier 2 lane 5(d): AZ38 NOT EVALUABLE for a realistic interior: no
  authenticated local model found in the recorded inventory. Model S
  acquisition recorded in NEEDS_OWNER, no payload downloaded. Exact
  Green-integral engine validated on two analytic fixtures, main21/21,
  mutant15/21,256/512 convergence; fixtures are not called a realistic Sun.
- Tier 2 lane 5(e): AZ39 NO VERDICT for full charged-background
  causality. Conditional GR-branch conserved-source tidal response
  derived, including a nonzero delayed TT signal and zero early response.
  Main29/29, deliberately instantaneous mutant25/29, exact integrals and
  16/32 quadrature agree. C8's elliptic-to-signal inference remains unproved.
- Tier 2 lane6: AZ40 NO VERDICT on a complete healthy density-tie
  action. Universal algebraic insertion reproduces CT14's negative
  coefficient; exact constant-w potential-portal branch and restricted
  clock-retaining kinetic positivity verified. Main32/32, three mutants
  21/32,30/32,25/32. No kappa-derivation reopen condition is met.
- Tier 2 lane7: AZ41 NO VERDICT on a complete covariant FN6 mechanism.
  Native power-law stiffness asymptotic obstruction and rational-versus-
  Gaussian operator mismatch derived; main28/28, mutant24/28. No candidate
  is transferred to the five observational engines; new-mechanism T0-T4
  and Q2 NOT EVALUABLE, tensor speed UNDECIDED. Finite-radius/non-power
  mechanisms and their full own-equation observable solves remain open.
- Tier 2 lane8: AZ42 NOT EVALUABLE, no verified healthy carrier. The
  brief's explicit one-paragraph fallback is recorded; no prediction is
  sealed and no artificial numerical test is substituted for that decision.
- Tier3 lane9: AZ43 IN PROGRESS. Criteria096759f915 freeze143 parameter
  points and729 local MW cells. Original anchors reproduced; twenty-three
  small-gate resolution pairs pass. At canonical p=.35,L_MW=1.5 the
  full local MW pair has15 coarse passes,10 fine passes,10 stable and
  five flips retained as unresolved. Alt now has77 stable passes at that
  parameter point; full grid pending.
- Tier3 lane10: AZ44 NO VERDICT on fully validated FN4e stage0;
  conditional STOP: NOT ENOUGH POWER. Fisher upper4.3678/5.2785,
  log-a0 error lower.4785/.4353dex. Mathematical controls11/11 and
  convergence/repeatability13/13 pass. Rotation count drops41.2%, failing
  frozen>50%; provisional area980.3 versus777deg2 also misses. Full
  isolated/native-geometry forecast not supplied; no stage1 authorization.
- Tier3 lane11: AZ45 IN PROGRESS, criteria616d7954c8. Explicit synthetic
  population avoids FN3's Planck15 mass conversion and retired Native
  background. Known answers56/56, flat forward pairs24/24, interrupted
  resume byte-identical. One canonical mutation pair misses0.01dex
  convergence (change0.02906); retained as UNRESOLVED. Full4032-case
  nonlinear grid, queue footprint declaration, population grader and
  sample-size scan remain pending; not queued before light-tier work.
- Tier3 lane12: AZ46 preliminary diagnosis executed under plan e282c8c2dc.
  Reproduces old mass3.0346e7 and drift20.8492 exactly; all4 I/O/recovery
  checks pass. Natural versus published robust mass differs10.44%; full
  gap to Oh's table remains unidentified. Same-profile analytical drift
  gives18.8803, not a new grade. Robust beam differs and must be fixed in
  a new engine. Missing published products recorded in NEEDS_OWNER.
  New physical criteria and independent cube redo remain pending.
- Tier3 lanes13-14 and Tiers4-5: pending in brief order.
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
1a9955b2a9). AZ40 now executes it with its original criteria preserved,
and extends it with a restricted static kinetic check; full health is open.
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
