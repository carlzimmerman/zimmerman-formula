# IN PROGRESS — FA1 record completion

Retired sector, adopts nothing. Kappa = 1/2 FITTED; not theory closed.
Original I1, I2 and I6 records remain untouched. No new action is
established by this audit. PREPARATION_PLAN.md was committed alone before
the audit script. Subsequent frozen substudies and their limited conclusions
are recorded below; the full nonlinear Bullet computation is still pending.

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

## A missing inference in the I2-P exclusion

FROZEN_KINEMATICS.md (e3fe114390) was committed alone before this focused
audit. The implication from a projected velocity gradient to a positive
vorticity floor FAILS: a pure symmetric-strain field has the same projected
velocity map as a rotating field but zero curl. Its unit gradient-normal
four-velocity also has exactly zero projected relativistic vorticity.
KINEMATIC_FINDING.md gives the explicit witness, derivation and limits.

kinematics.py passes23/23 known-answer, circulation and1/0.5kpc derivative
checks; both footings give F=1 for the irrotational witness. The separate
mutation confuses full strain with rotation and fails four checks, exit1.
Main and mutation outputs repeat byte-identically. covariant_witness.py
passes4/4 exact symbolic checks, including a nonzero rigid-rotation control.
This invalidates that stated lower-bound inference, not the observed
gradient, actual cluster rotation, or every independent failure of I2.
The old G-P-CL exclusion is not established by that gradient alone.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python kinematics.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python kinematics.py --mutate
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python covariant_witness.py

Run these from this lane directory with NumPy and SymPy available. The
mutation command must exit1. No observational or field-equation solve is
substituted by these kinematic identity checks.

## Fifteen shear keys: NOT EVALUABLE from the audited inputs

FROZEN_SHEAR_INPUTS.md (a3b7195720) fixes the input gate before this report.
shear_inputs.json lists all15 BA1 key names for both selectors and both
footings (60 rows). Every value is null, with its missing inputs named.
The label concerns the audited input chain, not a physical failure or a
proof that no usable product exists elsewhere. The Bullet3D task remains
open; this input report does not satisfy that computation.

The distinction in the distance chain matters: F1 uses measured BAO ratios
with an HRD/h absolute calibration, plus an explicit LCDM reference-distance
conversion for catalogue masses/radii. It is not uniformly a Planck18
calculation. This audit has not authenticated a complete native calibration
and gas-profile reconstruction. The inspected eRASS1 table has integrated
aperture quantities and derived MGAS500/R500, while X2 supplies a parametric
radial shape and taper. These are not by themselves raw radial gas evidence.

I1 also leaves its non-decreasing selector function unspecified; necessary
threshold support alone does not fix15 shear amplitudes. I2's old
system-level reading specifies a conditional uniform1.5-times-law extra
mass, but the chain supplies no per-cluster mean-flow constraints. KT is
not a mean-flow measurement. A common single-gradient proxy is inadequate
for the independently demonstrated kinematic reason above. No new F,
velocity field or cosmic normalization has been fitted to fill these gaps.

The isolated BA1 key function reproduces an independent15-name list and
the constant synthetic ratios/slopes:21/21 input checks pass. The mutation
accepts missing evidence and fails both incomplete-input controls,19/21,
expected exit1. Main and mutation outputs repeat byte-identically. This is
an input gate, so it has no graded PDE/N-body resolution number. No old
driver or top-level bootstrap was executed.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python shear_inputs.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python shear_inputs.py --mutate

Run from this directory with NumPy/Astropy. Missing external product needs
are recorded in NEEDS_OWNER. Native calibration and selector completion
would require new frozen physical criteria before these keys can be graded.

## Bullet3D preparation

FROZEN_BULLET.md (7cd8cf3ed7) now fixes the full3D equation, signed source,
physical epsilon,64/128/256 ladder, doubled-box check, ellipticity/residual
gates, known answers, mutation and queue contract before implementation.
The signed source is everywhere positive: the negative correction is bounded
by8262/8575 of its common-centre positive component. No clipping is applied.
All24 source/normalization checks pass, including paired mass quadratures;
the selector-sign mutation fails two known answers, exit1. Outputs repeat
exactly. BULLET_NORMALIZATION.md gives the derivation and scope. The3D
solver, field convergence and conditional Bullet readings remain pending.

The full3D physical-coordinate derivative module passes21/21 analytic
checks on N8/N16 stretched grids, including mixed Hessian components,
both-footing quadratic operators, the principal ellipticity matrix and
finite-difference Jacobian products. The maximum relative quadratic-operator
error is2.55e-13; the maximum Jacobian comparison error is1.09e-9 against
the frozen1e-8 line. Expanded-box central spacing is independently checked.
The separate selector-sign mutation fails five checks (16/21, exit1).
Both outputs repeat byte-identically with warnings treated as errors.
These are operator checks, not a nonlinear solution or field-convergence
result. Grids above N16 are guarded for heavyq execution.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python check_grid3d.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python check_grid3d.py --mutate

Run from this directory with NumPy/SciPy available. Next: spherical boundary
quadrature, a bounded nonlinear pilot, interruption/resume validation and
resource measurement before queued known-answer and Bullet ladders.
