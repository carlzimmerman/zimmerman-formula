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
  points and729 local MW cells. Original anchors reproduced;123 small-gate
  pairs completed:107 pass, points91/92,104–111 and117–122 have T2
  nonconvergence on both footings (maximum7.17% versus1%). Targeted Andromeda IX replay8/8
  reproduces those failures; no tolerance changed. At canonical p=.35,L_MW=1.5 the
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
  nonlinear grid and execution of the sample-size scan remain pending;
  not queued before light-tier work. Physical-footprint pilot0.154GB,
  prepared1GB queue estimate in QUEUE_PLAN.md; no submission yet.
  Population-statistics module now passes13/13 analytic/seeded checks,
  with byte-identical rerun. Calibration10/10 and full4032-case synthetic
  grader7/7 checks pass; production report0/4032, no power verdict yet.
- Tier3 lane12: AZ46 preliminary diagnosis executed under plan e282c8c2dc.
  Reproduces old mass3.0346e7 and drift20.8492 exactly; all4 I/O/recovery
  checks pass. Natural versus published robust mass differs10.44%; full
  gap to Oh's table remains unidentified. Same-profile analytical drift
  gives18.8803, not a new grade. Robust beam differs and must be fixed in
  a new engine. Missing published products recorded in NEEDS_OWNER.
  New physical criteria e3d557204a freeze the full beam-aware cube redo;
  beam/raw-reader implementation started: raw I/O4/4 passes, beam16/18;
  robust6arcsec minor-axis moments miss2% at5/9 quadrature (6.30/5.33%).
  Wrong-beam mutation bites; failures repeat exactly. Row-chunked V profile
  checks7/7 pass, original photometry recovered exactly,442MB peak RSS.
  Raw8x8 stage now has16/16 reader and13/13 restart checks; full cubes
  are queue-guarded. A1 corrects FELO spectral WCS before fits (old linear
  axis differs0.06208km/s). Mask fixtures10/10 and complete8x8 preparation
  checks19/19 pass; own masks/noise, shared gas map, exact resume/repeat.
  Preparation physical footprint0.141GB. Forward checks14/16: direct
  positive convolution reduces edge-normalization error3.64e-10 to1.64e-12,
  still above the unchanged1e-12 line; retain both failed tests. Dense
  fitting implementation14/14 checks, including fixed physical30arcsec
  pressure smoothing and ungraded stationary-fit pilot; both check suites
  repeat byte-identically. Individual fit worker restart/identity checks12/12
  pass twice, live SIGTERM/resume and fresh results byte-identical; ungraded
  budget2 pilot remains status0. Fit physical footprint0.285GB (RSS0.905GB).
  Paired native-noise checks23/23, separate uncorrelated mutation bites.
  All eight pilot mock constructions62/62 twice, exact full-manifest repeats;
  live noise interruption/resume exact. Mock-input fit integrity12/12 and
  updated worker restart12/12 pass. Full grid orchestration, production
  scaling, queue and fit-based mock/local-cube verdicts remain pending.
- Tier3 lane13: AZ47 IN PROGRESS. Measurement protocol75abae6f8b,
  criteria774bb8db44 and pre-result wording amendment b06499a5dc.
  Four train clusters yield rank3 empirical covariance, scatter.067-.106dex;
  all10 measurement checks pass. All400 archived stage2 candidates regraded
  as a pilot,824/824 checks and byte-identical rerun. Stable conditional
  G3 passes L1/L2:11/26 canonical,9/24 alt; scrambled sets all0 under
  full covariance, though diagonal inflation accepts many. Full retained-
  hit census/pairs still pending; calibrated population inference NO VERDICT.
  Streaming contract44/44 passes, including live interruption/resume. First
  complete L1 canonical real set:4,816,238 rows,37,525 conditional flags,
  28,125 stable;168seconds,127MB. The1000-row chunk attempt exceeds180s
  and must resume through heavyq. Canonical L1 control full pair agrees:
  3,297,394 rows,two stable conditional passes (mutation zero). Full
  Eight independent full chunk2000 repeats now match byte-for-byte;
  six chunk pairs pass. Two L1 real chunk1000 remainders require heavyq.
  Census-auditor mutation fixtures8/8 pass.
- Tier3 lane14: AZ48 IN PROGRESS, preparation plan716ca50b84. Local input
  audit21/21, parser/control fixtures11/11. All43 CFG713 lenses match the
  catalogue, but no rotation evidence in the inspected tables;11-file
  bounded text search supplies no measured classes. Missing kinematics
  recorded in NEEDS_OWNER. X30/CFG713 cosmology dependencies and signed
  Bullet components recorded; native shear trace, physical criteria and
  genuine3D nonlinear solve remain pending. Retired sector, adopts nothing.
  Focused I2-P audit finds the projected-gradient-to-vorticity lower bound
  invalid: an irrotational strain witness has the same projected map.
  Frozen e3fe114390;23/23 kinematic checks, separate mutation fails four,
  exact covariant normal-field check4/4. This challenges that inference only,
  not the actual cluster flow or I2-R's separate elliptical constraint.
- Tiers4-5: pending in brief order.
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
