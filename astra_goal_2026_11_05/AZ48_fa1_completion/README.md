# IN PROGRESS — FA1 record completion, input audit only

Retired sector, adopts nothing. Kappa = 1/2 FITTED; not theory closed.
Existing I1, I2 and I6 failures stand. No new action or physical grade is
established by this audit. PREPARATION_PLAN.md was committed alone before
the audit script; physical criteria and computations are still pending.

audit_inputs.py records43 CFG713 lens identifiers separately for both
footings, with identical rosters. All43 match entries in the local Auger
catalogue. That table has dispersion and morphology columns but no resolved
rotation measure; the inspected ATLAS3D Faber–Jackson table also lacks one.
Every per-lens rotation measurement and class remains explicitly unknown.
These unknowns cannot be filled using morphology, dispersion or model mass.

The bounded local search inspected11 SLACS-containing tex/tsv/csv/txt files
under real_research/data and the sibling external-data directory. Its two
files with rotation-term matches were manually inspected: Etherington's
lens-modelling section describes relative orientation of light profiles;
Auger's manuscript contains a commented rotating-package import and a
wavelength-dependent effective-radius formula. None supplies a measured
rotation class. This search excludes PDFs, archives, other extensions and
other roots; it is not a proof that no relevant local or published product
exists. Exact paths, hashes, coverage and line references are in
input_audit.json. The missing per-lens kinematic product is in NEEDS_OWNER.

Source inspection also finds explicit Planck18 angular distances in CFG713,
and DA_lcdm, fixed cosmic-normalization constants and derived gas masses in
X30's chain. None of those drivers was executed. The requested15 selector
shear keys require a native-input audit and new execution; dimensionless
selector algebra alone will not satisfy that requirement. X2's parametric
gas profile and the exact source locations are recorded for that work.

The Bullet input is the inherited six-component Plummer prescription,
including a negative component used in its gas-profile construction. That
component is recorded, not silently removed. Total-density positivity,
native calibration, boundary conditions and a genuinely3D nonlinear solver
remain to be established before grading. The existing I6 solver explicitly
uses axisymmetry; it is not a Bullet3D solution.

All21 parser/source-presence audit checks pass. Independent identifier and
header fixtures pass11/11; the separate mutate/false_rotation_evidence.json
rejects the deliberate substitution of a dispersion column for measured
rotation evidence. These are input-handling controls, not observational
or field-equation tests. No physical numerical convergence claim is made.
The audit, fixture report and separate mutation output repeat byte-identically.

    python3 astra_goal_2026_11_05/AZ48_fa1_completion/audit_inputs.py
    python3 astra_goal_2026_11_05/AZ48_fa1_completion/check_audit.py

Next: complete the native shear-input trace, freeze evaluable selector
criteria, and derive/freeze the3D nonlinear solve and its known-answer,
mutation, restart and convergence tests before any heavyq submission.
