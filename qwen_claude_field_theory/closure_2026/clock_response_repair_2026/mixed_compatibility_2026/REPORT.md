# Mixed clock compatibility: localized progress, no convergence closure

Base `38cb06700`, 2026-09-11. Full same-action relativistic MOND status: **OPEN**.
No physical coefficient, production solver, matter coupling, or MOND kernel
was changed. This is a numerical-consistency investigation of the existing
clock sector, not a completed galactic MOND action. Carl Zimmerman's
primordial-clock direction motivates the work; no new priority claim is made.

## Decision

Do **not** enable the experimental clock-rate method in production. Fresh
129/257/513-point evolution improves the reported momentum residual, but
the full-domain angular-curvature tangency error grows by **1.3781** on the
last refinement. Late-time force and dust-depletion claims remain unvalidated.

The useful exact result is a mismatch between the two interpolation spaces.
It rules out generic **exact** compatibility in those spaces, not convergent
approximation and not a physical gravity theory. Two associated algebra
implications compile in Lean. A separate real-analysis proof draft failed
at dependency import and is explicitly unverified.

## What was tested

Write u=chi_r. The continuum kinematic identity is

\[
u_t=(NQ)_r,\qquad (u_t)_r=Q N_{rr}+2N_rQ_r+NQ_{rr}.
\]

The action-derived evolution uses the right-hand jets, while the differentiated
radial constraint projection uses derivatives of interpolated time-rate data.
These need not commute at finite resolution.

1. `attribution.py` changes only the mixed u_r time-jet in the tangent-linear
   constraint ODE. It integrates unmodified, substituted and sign-reversed
   forcing branches together. The sign-response discrepancy is below 1e-9
   (observed about 3e-15). At 513 points the radial-curvature error falls from
   4.181e-6 to 9.909e-7 under substitution and rises to 8.034e-6 under reversal.
   This identifies a substantial contribution, **not** an integrable repair.
2. `integrated_jet.py` integrates an even source spline exactly cell by cell.
   Reinterpolation into the projection's odd spline space loses that identity;
   the fixed-state probe does not repair fine-grid tangency.
3. `collocated_jet.py` solves for a primitive directly in that odd space.
   The initial nodal construction was ill-conditioned: about 1.32e9 at 513
   points. Its unchanged polynomial test failed (7.19e-11 error versus 3e-12
   tolerance). Center-plus-midpoint collocation reduced the measured condition
   to 978.95 and passed that test. The nonlinear test was changed to reflect
   the explicitly changed collocation contract, not to loosen a tolerance.
4. `collocated_probe.py --evolve` evolves fresh initial data, then independently
   differentiates the constraints. It does not merely retest old trajectories.

The numerical library thread cap is cooperative. All three fresh evolutions
use amplitude .02, width .3, outer radius 3, gamma 1e-6, dt .00025, final t .02,
and the same action/background/outer lapse condition as the baseline.

## Fresh results

Tangency norms include the origin and all sampled r<2.8. The separate snapshot
momentum norm retains the existing solver mask, which excludes two inner grid
cells; it is **not** a full-origin residual norm.

| Points | Angular h tangency | Radial k tangency | Snapshot momentum | Clock-rate identity defect |
|---:|---:|---:|---:|---:|
| 129 | 2.4071e-6 | 1.6686e-5 | 8.7386e-7 | 9.5129e-8 |
| 257 | 3.2279e-7 | 5.4797e-6 | 3.3586e-7 | 1.5297e-8 |
| 513 | 4.4483e-7 | 5.0344e-6 | 1.9789e-7 | 6.4476e-9 |

At 257 and 513 the h maximum is the first positive node and the k maximum is
at 5 grid spacings. Outside r=.1, k error falls from 1.0651e-6 to 2.6718e-7.
The midpoint linear-system residual is 4.34e-16/7.10e-16, while the nodal mixed
jet defect is 5.4112e-6/4.9106e-6. A tiny collocation residual is therefore not
a field-equation certificate. The remaining error is concentrated in a
shrinking inner region; these runs do not establish its asymptotic fate.

## Exact interpolation-space obstruction

Let z=r^2 and represent u_t=r G(z), with G piecewise cubic and C2. Then

\[
D(z)=(u_t)_r=G+2zG',\qquad D''=5G''+2zG'''.
\]

If the separately interpolated target D is also C2, at every positive knot
z_j continuity of G'' and D'' implies

\[
2z_j[G''']=0\quad\Longrightarrow\quad [G''']=0.
\]

Thus adjacent cubic pieces have equal derivatives through order three and
are the same polynomial. Across connected positive knots G must be one cubic.
Generic piecewise cubic targets cannot satisfy this exact matching condition.
This is a local spline regularity fact, not a novelty claim or a no-go against
approximate numerical convergence.

`spline_obstruction.py` derives the join matrix from polynomial differentiation,
computes determinant 24 z_j, generic rank 4 and rank 3 at z_j=0, and exhibits
the C2 join with coefficient jump (0,0,0,1), whose D'' jump is 12 z_j.
No determinant or rank is inserted as an expected output. The zero-knot case
is kept distinct; it is not a gravitational constraint-rank calculation.

`SplineJetObstruction.lean` verifies third-jet continuity and coefficient-jump
uniqueness under the displayed algebraic hypotheses. Both compile, with only
propext, Classical.choice and Quot.sound reported. The spline/differentiation
bridge is checked in SymPy, not formalized in Lean.

`ClockCompatibility.lean` attempts the stronger interval estimate
|u_t-(NQ)_r| <= r epsilon from a uniform derivative-defect bound and equal center
values. Its import fails because the local cache supplies conflicting
Asymptotics.IsEquivalent declarations. No theorem in that draft is certified;
the proof bodies were not reached. No shared dependency cache was modified.

## Follow-through: common-product diagnostic

`origin_profiles.py` compares the action target with two derivatives of a
single background-subtracted even spline of NQ, then measures the error added
by resampling its first derivative into the odd spline space. These are
fixed-state comparisons, not a new evolution prescription.

At 257/513, resampling errors have maxima 1.203e-5/1.099e-5, at 5/4 grid
spacings. Outside r=.1 the shared-second-derivative versus action discrepancy
decreases from 8.983e-6 to 2.257e-6. Thus simply computing a shared product
derivative and resampling it is not a demonstrated fix. The raw first ten
nodes and both radial norms are retained in `origin_001/result.json`.

**Next calculation:** construct a derivative-compatible pair of spatial
representations for the lapse/product and clock gradient, retaining regular
center conditions and the same action equations. Test manufactured nonpolynomial
fields and the first eight evolved grid cells before another fresh evolution.
Do not tune coefficient functions, remove the center from acceptance norms,
or interpret a passing collocation solve as repaired dynamics.

## Verification and provenance

- Fresh evolution, component attribution, two fixed-state primitive probes,
  origin comparison, symbolic join calculation: execution exit 0. The fresh
  global-convergence acceptance condition nevertheless **fails**.
- Four primitive regression tests: exit 0, 4/4 passed.
- Relevant unchanged production suite: exit 0, 17/17 passed, 224.993 seconds.
- `SplineJetObstruction.lean`: exit 0, two checked algebra implications.
- `ClockCompatibility.lean`: exit 1, dependency-import failure, unverified.

Each experiment directory has actual argv, environment, bounds, input/output
hashes and exit status in its manifest. `integrated_001` and `collocated_001`
are historical input revisions: subsequent changes added common probe metrics
and generic evolution dispatch. Their pinned source hashes differ from the
final files; do not cite them as current-source certificates. Their numeric
outputs are retained as historical experiments. The decisive `evolution_001`,
`origin_001`, `spline_001` and `spline_lean_001` pin final inputs.

See `COMMANDS.md` for executed scientific commands and `validation.json` for
manifest checks, including expected historical-source and failed-run findings.
Only this experimental directory and the parent checkpoint link are intended
for this commit. Independent review agreed that global convergence is not
repaired. No empirical data, new force law, full Dirac chain, PPN certification,
cosmological spectrum or complete-theory proof was produced by this checkpoint.
