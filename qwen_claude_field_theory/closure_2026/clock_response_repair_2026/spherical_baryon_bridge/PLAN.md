# Spherical baryon bridge implementation plan

> For agentic workers: use the Mathbox research/computation protocols and disjoint
> agent tasks; preserve the live working tree. This is an executed research plan,
> not a claim that its open mathematical steps have been proved.

**Goal:** derive and test baryon-sourced response of the SAME cubic clock action,
then use it to construct the nonlinear matched-source calculation.
**Base:** `776cc413d`; parent physical definitions in
`../cubic_background_completion/README.md`; target in `../../FRIED_CHICKEN_SPEC.md`.
**Architecture:** exact spherical ADM variation in `action/`; independent sourced
finite-wave reduction and initial-value calculation in this directory. The latter
is a prerequisite/linear benchmark, NOT a substitute for the nonlinear target.
**Stack:** SymPy exact algebra, SciPy independent integrators, Lean for established
algebraic bridges. No observations fitted; no local a0 introduced.

## Contract and scientific decision

Retain P(X,tau), clock density and time current; do not replace P by F(Y).
Keep all spherical metric variations before radial gauge specialization.
Use a conserved O(epsilon) comoving dust source on the baryon-free background:
L_source=-C*n/2 for each real Fourier mode, C=a^3 delta-rho constant.
Its motion induced by the metric enters stress at O(epsilon^2), which this
linear benchmark does not compute. No arbitrary time switch or independent
scalar-charge fitting. Derive both physical potentials including shift evolution.

## Tasks and tests

- [x] Action agent: `action/derive.py`, `action/REPORT.md`: exact spherical lapse,
  shift, radial/angular metric and chi Euler equations; scalar improvement current;
  independent FLRW, Minkowski and gamma=0 reductions. Execute before reporting.
- [x] Primary: `test_source.py` first. Check raw sourced auxiliary Euler residuals,
  source conservation, zero-source regression, and correct canonical forcing.
  The first run must fail because the source implementation is absent.
- [x] Primary: `source.py`: derive source reduction from the existing varied
  quadratic action. Interface `derive()` returns exact source and metric maps,
  original background symbols and checks; no expected PPN/DOF values inserted.
- [x] Primary: `response.py`: solve shared u=udot=0 initial clock data with
  DOP853/Radau; reconstruct Phi=n+dot(beta), Psi=-z-H*beta separately;
  check derivative refinement and constraints before interpreting source response.
- [x] Reconcile with spherical action, record actual commands/exits and limits,
  run prior source/current/background regressions. Formalize only an actual new
  identity, not the desired force law as a premise masquerading as a derivation.
- [x] Add and vary dynamical dust in `action/matter.py`, including radial motion,
  normal-vs-rest density, and source conservation before caustics.

Executed checkpoint: ten aggregate jobs exit 0, manifest valid, 401.377 seconds.
See RESULTS.md. These completed implementation tasks are not full goal closure.

## Rulings

The previous question turn yielded source-method evidence, but no new gravity
calculation. This turn must execute the next source calculation.
Constraint-only data do not determine Phi: beta-dot requires evolution. Therefore
the first numerical benchmark is time-dependent linear response alongside full
spherical equations. Nonlinear matched solutions and a common primordial-data
selection remain required even if this benchmark passes.

No test of a linearized model establishes a universal nonlinear no-go. A
small-source obstruction additionally requires a controlled differentiable
source-to-solution map and fixed domain/time/boundary data. No success flag means
the full theory is closed. The full goal remains OPEN.
