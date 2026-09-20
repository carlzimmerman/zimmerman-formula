# From conditional particle-free theorems to a defensible physical result

Date: 2026-09-20. Audit starting revision:
`97023676ec3ae94174391b2bc23484e49e9f1484`.
Scope: the auxiliary action, orbital-shape theorem and field–orbit reciprocity
packages linked below. This document does not audit every new cosmology/BH*
commit or promise that nature will validate the proposed theory.

**Primary verdict: conditional on named physical inputs.** There is a proved
mathematical prediction to test. A new empirically established law, unique
physical normalization and global novelty have not been established.

## What is already closed, and what is not

| Claim | Present evidence | Remaining premise or gap |
| --- | --- | --- |
| The specified auxiliary action has the rational static response | Symbolic action variation and Lean auxiliary elimination | The action and field domain are physical model choices; the full variational bridge is not formalized in Lean |
| `kappa=1/(2 lambda)`; equal weight gives `1/2` | Conditional theorem and explicit counterfamily | Independent selection of `lambda=1` remains open; it may instead be declared a fixed model postulate |
| Exterior orbital slope fixes baryonic mass fraction; quarter-slope ratio is `4/3` | Lean calculus and real algebra plus exact/numerical checks | Isolated spherical source, ordinary circular test-body motion, specified full rational response, constant enclosed mass |
| `E²(1-2 beta)=2` for the local action class | Lean conditional compatibility theorem; independent symbolic constitutive/Green-function checks | The Green-function identification is a Lean premise; matched physical acceleration and external-field-dominated limit are required |
| A real population obeys either relation | No test in these packages | Suitable measurements, controlled geometry/projection and an independently fixed analysis |
| This is original enough for a new physical-discovery claim | Bounded literature checks only | Existing MOND overlap must be resolved; proof formalization does not establish priority |
| The full theory is cosmologically stable and observationally viable | Outside these packages | Covariant dynamics, constraint-preserving cosmological evolution and actual data likelihoods |

The strongest current paper claim is a **conditional theorem and reproducible
test construction for a specified particle-free action**, with credit for the
known MOND machinery. A preprint or Zenodo deposit can document that exact work;
it cannot by itself establish novelty, observational success or priority over
earlier literature. No publication is being performed by this roadmap.

## Dependency map and evidence boundary

`chosen action + auxiliary domain -> stationary response -> static field equation`
`-> isolated spherical flux + circular motion -> orbital theorem`
`-> geometry/projection model + independent baryonic inputs -> observable prediction`
`-> frozen likelihood + suitable data -> empirical result`.

The first line combines symbolic variation with Lean elimination. The orbital
calculus in the second line is formalized. The last two arrows are **open**.
The field–orbit test has a separate symbolic/external-source bridge from the
constitutive Jacobian to the 3D Green function; its final compatibility algebra
is formalized. None of these chains inserts a dark-matter particle.

Sources of truth:

- [Action and normalization](../kappa_unit_response_2026_09_20/README.md), with
  `UnitResponse.lean` and `run/manifest.json`.
- [Orbital theorem](../orbital_shape_law_2026_09_20/README.md), especially
  `OrbitalShape.lean` theorems `rational_exterior_shape` and `quarter_slope_iff`.
- [Field–orbit theorem](../field_orbit_reciprocity_2026_09_20/README.md), especially
  `Reciprocity.lean` theorems `action_class_reciprocity` and `no_response_retuning`.
- `claim_register.json` records the bounded claim statuses and outstanding gates.

Lean's absence of `sorry` proves that the stated propositions follow from their
premises and library axioms. It does not establish physical premises. The number
of certified lemmas is not a measure of physical evidence.

## First priority: determine whether the orbital test is usable

**Deliverable:** `validation_work/orbital_admissibility.csv` and
`validation_work/geometry_report.md`, under this directory. These files do not
exist yet; they are the first work package, not completed evidence.

- [ ] Inventory independent mass, distance, inclination, spatial geometry,
  environment and kinematics for candidate systems; record raw-source versions
  and hashes, uncertainties, missing fields and rejection reasons.
- [ ] Use the existing `real_research/data/sparc_data/*_rotmod.dat` and
  `real_research/data/sparc_master_clean.csv` as **disk benchmarks**. SPARC is a
  disk-galaxy catalog; membership does not satisfy the spherical theorem.
  Preserve signed source-column conventions: the inspected NGC7814 file contains
  negative gas entries. Verify their documented meaning before constructing
  baryonic accelerations; do not silently square away signs.
- [ ] Assess compact-source/spherical-exterior candidates without selecting on
  whether their inferred ratio resembles `4/3`. The true criterion is whether
  their geometry and enclosed-mass gradient permit the intended error budget.
- [ ] If no suitable exterior population exists, record that outcome and move
  to full disk forward modeling. Do not relabel disk enclosed mass as the
  spherical Newtonian field or manufacture a test sample.

**Pass condition:** at least one specified observable and candidate population
with independent baryonic information, a documented geometry model and an error
budget demonstrably smaller than the competing predictions' separation.
**Stop condition:** unidentifiable baryonic normalization, no applicable radial
range, or geometry corrections as large as the proposed distinguishing signal.
This stop would reject the instrument, not the theory.

## Second priority: calculate the geometry error before looking for agreement

**Deliverable:** `validation_work/geometry_solver_validation.json` with raw
residuals and convergence tables; reuse a repo solver only after auditing its
actual operator, boundary condition and kernel. Candidate starting points are
`qwen_claude_field_theory/theory_2026/aqual_solver_2026.py` and
`real_research/reviews/mi_aqual_solve_framework_kernel_2026.py`; neither is
endorsed as validated by this document.

- [ ] Recover the analytic isolated spherical flux and the linearized
  external-field Green function with the selected solver.
- [ ] Use the Newtonian limit as an independent geometry benchmark and check
  integrated source flux, field-equation residuals and boundary sensitivity.
- [ ] Compare grid spacings `h`, `h/2`, `h/4` and outer boundaries `R`, `2R`.
  Do not accept merely a solver's internal convergence flag. Require observable
  changes to be below the allocated numerical-error budget at every comparison.
- [ ] For extended spherical sources, include
  `m=d ln Mb(<r)/d ln r`. The exact replacement is
  `beta=1/2+(m-2)(1+q)/(2(1+q+2q²))`, `q=sqrt(1-f_b)`.
  At `f_b=3/4`, this is `beta=-1/4+3m/8`, not `-1/4`.
- [ ] For disks, solve the actual non-spherical field equation with the chosen
  density, thickness and boundary field. For externally affected systems, vary
  field strength, direction and tides across their independently allowed ranges.
  Choose the simulation grid to cover the candidate sample, not convenient
  parameter values at which the theorem happens to fit.

**Pass condition:** quantified corrections and numerical errors are sufficiently
small or modeled in the likelihood to distinguish the registered alternatives.
Changing the full response is a new model version requiring a new test; it is
not a harmless uncertainty adjustment.

## Third priority: freeze a measurement that can actually fail

**Deliverables:** `validation_work/protocol.json`, a provenance-pinned mock
generator, a fit/recovery script and a held-out result. Freeze sample rules,
mass priors, response functions, nuisance treatment, selection model, comparison
statistic and decision rule before opening the held-out result.

- [ ] Fit the measured velocity/photometric data jointly. Infer the latent
  rotation curve and its slope with covariance; do not choose the radius where
  a noisy finite difference happens to cross `-1/4` and then treat that radius
  as independently selected.
- [ ] Carry shared distance, inclination, mass-to-light, gas, aperture and
  noncircular-motion errors. Estimate systematic uncertainties from observations
  or validated simulations; writing percentages into a budget is not evidence
  that those percentages are achievable.
- [ ] Generate mocks from the rational, simple and standard responses, with
  identical geometry/noise/nuisance machinery. Test bias and uncertainty coverage
  under each model and under deliberately violated geometry assumptions.
- [ ] Separate any data used to choose response parameters or selection rules
  from the final validation data. Report all registered comparisons and failures.
  Include correlations between radial bins and between systems where applicable.
- [ ] Compare the full likelihoods or a predeclared residual distribution;
  do not translate a raw percentage difference into a sigma count without a
  sampling distribution, covariance and nuisance treatment.

**Pass condition:** an unbiased, calibrated estimator with sufficient sensitivity
in the actual sample, followed by a held-out result and independent reanalysis.
A null, rejection or inconclusive result is a legitimate outcome.

## Concrete precision arithmetic: why the experimental step matters

Let `D=Mdyn/Mb`. At the rational quarter-slope point,

\[
D=4/3,\qquad \frac{dD}{d\beta}=\frac{128}{45},\qquad
\left.\frac{dD}{dm}\right|_{\beta=-1/4,m=0}=-\frac{16}{15}.
\]

The closest of the two listed comparison values is `sqrt(3/2)`, a difference
of about **0.1086** in D. In an ideal Gaussian comparison of two fixed predictions,
three-standard-deviation separation would require an effective uncertainty
below **0.0362**, about **2.71%** of `4/3`. If slope error were the only error,
its standard deviation would need to be below about **0.0127**.

These are planning ceilings, not a forecast for an existing survey. For the
local residual `R_D=D_obs-D_pred(beta_obs)`, first-order propagation gives

\[
\operatorname{Var}(R_D)=\sigma_D^2+
(128/45)^2\sigma_\beta^2-2(128/45)\operatorname{Cov}(D,\beta),
\]

with the other modeled nuisances carried jointly. A small omitted enclosed-mass
gradient `m=0.03` alone shifts D by approximately `-0.032` at fixed quarter slope:
already comparable to that ideal precision ceiling.

The independent field–orbit comparison is harder: distinguishing the deep-limit
force ratios `sqrt(2)` and `4/3` in the same idealized three-sigma sense requires
an effective error below **0.0270** in E, about **1.91%** of `sqrt(2)`, even before
uncertain beta, finite-field and projection effects. Projected binary velocities
are not E without a validated dynamical population model. This route is secondary
until such an observable estimator exists.

`precision_budget.py` reproduces the exact derivatives and planning numbers.
Its output labels all these restrictions explicitly; it is not fitted evidence.

## Finish the physical and novelty arguments separately

- [ ] Choose a clear paper scope. A fixed equal-weight action is a legitimate
  model postulate; a first-principles prediction of the normalization additionally
  requires a reason to exclude the explicit variable-weight action family.
  A new physical derivation must distinguish lambda=1 from lambda=2 while keeping
  the independently defined scale fixed. Re-expressing an assumed or measured
  equality as an injective map is not an independent selection mechanism.
- [ ] Reconstruct the covariant-to-static reduction and matter coupling if the
  paper claims relativistic completion. Establish metric slip before predicting
  lensing from an inferred Poisson density. Static ellipticity does not prove
  absence of dynamical ghosts or cosmological stability.
- [ ] Obtain an independent proof/physics audit of the explicit assumptions and
  statement, not just a second successful compilation. Formalize the 3D
  Green-function bridge if claiming the entire reciprocity chain is Lean-proved.
- [ ] Compare the exact statements with prior AQUAL/TeVeS interpolation work,
  external-field solutions and orbital-slope diagnostics. Record versions and
  equation-level overlap; classify the contribution as a new statement, new
  proof/formalization, new test or rediscovery according to what survives.
- [ ] For a technical note, publish the theorem's actual scope, reproducible
  source/data, exact commit, failures and open gates. For a claimed physical
  discovery, additionally require the successful independent empirical test.

## What to do next, literally

Start with the **orbital admissibility and geometry report**, not another scalar
coefficient identity or a full-cosmology claim. Its first conclusion should be
whether an observable population can distinguish the 4/3 response after realistic
geometry and covariance. If it can, execute the frozen test. If it cannot, the
next useful output is the full disk prediction or a documented infeasibility
result—not a more confident headline.

Primary sources checked for the scope of this plan:

- [Lelli, McGaugh & Schombert, SPARC, arXiv:1606.09251v1](https://arxiv.org/abs/1606.09251v1):
  the catalog is a set of disk-galaxy mass models and rotation curves.
- [Banik & Zhao, arXiv:1509.08457v3](https://arxiv.org/html/1509.08457v3),
  sections 2–3: the external-field solutions used by the reciprocity package.
- [Chae & Milgrom, arXiv:2201.02109](https://arxiv.org/abs/2201.02109):
  a relevant numerical external-field/disk study identified for the solver
  comparison; its detailed implementation has not been audited here.

This is a self-review, not an independent referee report. Publication or a
successful scientific outcome is not guaranteed by the work plan.
