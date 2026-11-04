# Review of the October 30 to November 3 research

The most useful next step is to make the current filtered-gravity proposal a
single conserving field equation and test whether its narrow empirical window
survives. The recent calculations motivate spatial response beyond a local
interpolating function, but the implemented source-only filter fails a necessary
variational reciprocity test. Its variable-width successor also changes the
operator between Solar System and galaxy calculations. Those are concrete
obstacles that another scan of width formulas would not address.

This review found no completed common theory, no derivation of kappa=1/2, and
no reason to reverse the recorded retirement of route E. It did find reusable
results, several correctable inference defects, and a specific next calculation.
The new contribution here is an independently reviewed reciprocity obstruction
and bounded diagnostic checks, not a claim of new fundamental physics.

## Scope and provenance

The committed interval is pinned from
`4cba03defe795a2f8e40bc181d8bd7c1a5362752` to
`c8b2586bb1921cff3bcb75feae827233ce62db8b`: 783 commits, 5,665 changed paths,
and 856 changed Markdown files. It starts at midnight October 30, New York
time. The initial checkpoint includes KT28's frozen criteria but no KT28 result.
There are 230 changed top-level rebuild lane READMEs in the path inventory.

The review used a complete path/history inventory, a headline-level pass over
those 230 lanes, deeper domain reviews, and selected independent mathematical
checks. It is **not a line-by-line certification or rerun of all 5,665 files**.
The empirical reviewer read 53 lane summaries and inspected selected code;
the core/cosmology reviewer inventoried 916 scoped artifacts and the closure
hierarchy; the particle reviewer inventoried 764 changed paths across eight
families and inspected their principal dependencies. The coordinator also read
the untracked compatibility, field-response, dynamical-response, and ER2 records.
Exact depth and omissions are in the three domain reports.

Another 6,284 untracked paths had modification times in the window, predominantly
external data and generated outputs. They are inventoried separately. Modification
time is not proof of creation date or authorship. Older untracked Yang–Mills C2
material was inspected because its current status files refer to it.

The shared checkout was dirty and advanced during review. Read evidence is
hashed; the late changes were publication/brief/frozen-plan commits rather than
new results used to establish the findings below. Existing research code,
results, seals, owner decisions, jobs, and Git state were not changed by this
review. New files are confined to this review directory; delegated scratch
checks were originally written under `/private/tmp` and archived here.

See [inventory](inventory.json), [commit history](commit_history.txt),
[lane summary inventory](lane_summaries.json), and
[critical input hashes](critical_source_pins.json). The summary inventory is
discovery material: several historical headlines are superseded by amendments.

## What the current programme actually is

The [November 1 owner decision](../../rebuild_2026_10_22/OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md)
retires route E, native N, N with response, the basin split, and their core
rules. The flagship is the a0 law and its unresolved failures. The subsequent
exceptions permit the specified one-field nonlinear-well investigation and
HF1's fermion experiment; they do not reinstate the retired sector or the
separate SU(5) particle programme.

The November 1 compatibility matrix is useful historical synthesis, but it
cannot be treated as the current programme's authorization or evidence that
PN28, X48, and the galaxy law are one model. Their stress, state, and scale
assumptions differ. The archived recommendation to combine their strengths
remains a matching problem, not a physical mechanism already constructed.

## Findings that change the next decision

### 1. The present filtered force lacks its reciprocal variation

[KT14's solve](../../rebuild_2026_10_22/KT14_filtered_phantom_mw/kt14.py)
implements, for Gaussian smoothing S,

    Phi[rho] = Phi_N[rho] + Phi_ph[S rho].

The derivative of the QUMOND phantom potential with respect to its source is
a symmetric operator B. The derivative of the implemented composite map is
N+B S; its adjoint is N+S B. These differ on a nonuniform background. A twice
differentiable static interaction energy with ordinary universal matter
coupling requires symmetry.

The [full derivation](FILTER_RECIPROCITY.md) provides an analytic counterexample
using positive density and mass-preserving perturbations in a planar periodic
external-field problem. The independent two-mode calculation gives reciprocal
cross responses 0.0017058629 and 0.0035575464; the mismatch is resolved at
64–4096 quadrature points. This is not a percentage error estimate for any
galaxy. A separate reviewer obtained a nonzero internal-force diagnostic for
the same source-only architecture; ordinary QUMOND and the completed controls
vanished within numerical error.

Varying the explicit candidate energy

    U_new[rho] = U_N[rho] + U_ph[S rho]

instead gives

    Phi_new[rho] = Phi_N[rho] + S* Phi_ph[S rho].

The outer adjoint is required by that construction. This is established
variational reasoning applied to the current implementation, not a novel
general principle. The older
[FRIED_CHICKEN_SPEC](../../qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md)
already includes outer S* with a different nu_mono kernel. Its action checks
cannot validate KT14's different equation. CFG653's failed high-pass model is
also a different operator.

**Consequence:** KT17/KT25 retain their recorded phenomenological screen results,
but these cannot be promoted to a conserving theory. The completed equation
must earn its own scores. The obstruction is scoped to the stated static map
and standard matter coupling; it does not exclude every nonlocal or dynamical
completion.

### 2. The local-width screens do not test one common operator

[KT27](../../rebuild_2026_10_22/KT27_local_rule_alt_grade/kt27.py), lines 20–26,
uses a fixed-width Gaussian enclosed-mass formula evaluated at xi(r) for Cassini.
Lines 45–62 instead smooth a density with the output-row width and then integrate
it for dwarfs; SPARC follows that density route. For a point source,

    d[M F(r/xi(r))]/dr = 4 pi r^2 rho_sm(r) [1-r xi'(r)/xi(r)].

Thus the two constructions disagree when xi varies. The constant-width
reproduction control cannot detect this mismatch. In addition, KT27 reports
SPARC smoothed-mass ratios 0.36–1.13, median 0.81, and KT26 uses one Milky Way
width derived from the observed circular speed and slope. Those are useful
screens, but not a single self-consistent local field solution.

For a genuinely state-dependent filter, the energy variation involves the
adjoint of the full derivative of rho -> S[rho]rho, including width derivatives.
Choosing another local scalar for xi without deriving that variation leaves
the same structural issue open. KT28 was criteria-only at the pinned checkpoint;
this review assigns it no empirical result.

### 3. One large reported rejection probability is miscalibrated

[RQ3 acceptance.py](../../rebuild_2026_10_22/RQ3_acceptance_v2/acceptance.py),
lines 179–180 and 314–319, converts lensing chi-square into
Z=(chi-square-56)/sqrt(112), then uses a two-sided Gaussian tail. This is a
moment-normal approximation far into a non-Gaussian tail.

| Footing | Stored chi-square | Gaussian probability used | Chi-square survival for the assumed 56 degrees of freedom |
|---|---:|---:|---:|
| canonical | 154.14858 | 1.7901e-20 | 4.1642e-11 |
| alternative | 124.99569 | 7.0551e-11 | 3.5166e-7 |

The exact integer-degree gamma-series calculation independently reproduces
these corrected probabilities. Bonferroni remains valid under arbitrary
correlation **only when its input probabilities are valid**. It does not fix
this marginal-tail error. The covariance and effective degrees of freedom also
need their own justification; this arithmetic accepts the script's 56.

**Consequence:** recompute affected probability summaries before quoting their
significance. This does not turn the law into an accepted model: the corrected
lensing tails are still small, and other failures remain. The script's overall
FAIL label is also based on row labels, not solely this probability.

### 4. AN1's principal Gaussian “runaway” check rejects exact dust behavior

The original AN1 force interpolation used enclosed mass proportional to r
inside the central cell, where uniform density requires r^3. At half a cell
that gives four times the correct force. The v3 solver corrects this and
reproduces the dust-sphere reference z=1.3617. The historical “all 68 fold”
headline is superseded by
[README_V3](../../rebuild_2026_10_22/AN1_aest_nonlinear_dust/README_V3.md):
61 folds, five no-collapse cases, two oscillating cases, zero settled cases,
formally NO VERDICT because K11 fails.

However, an independent exact-dust shell calculation at K11's own compression
event gives deviations 0.908393 at N=300 and 0.540161 at N=1200. AN1's saved
values are 0.908083 and 0.540619. The large apparent failure is almost exactly
the expected differential focusing of a Gaussian peak. Requiring near-homology
with a universal 0.02 threshold is inappropriate for that initial profile.

**Consequence:** revise the diagnostic against the correct analytic reference,
with an explicit post-result amendment, before using it to judge the solver.
Do not silently convert NO VERDICT to PASS: the top-hat residual 0.03696,
reduced-action validity, absent settled baryon profile, and other obligations
remain. The independent calculation diagnoses one bad check; it does not prove
that a physical halo forms.

### 5. AN2's capture test can pass in an unperturbed background

The fixed physical R500 test compares total enclosed field mass against a
phantom-mass need. At z=20 and R=1350 kpc, the homogeneous background alone
gives Md/Mph=5.235 canonical and 4.622 alternative, with zero excess field mass.
It therefore passes without a formed well. The current AN2 report already flags
this trivial early trigger; the independent arithmetic corroborates it.

AN2's 16–18% spherical lag and failed checks still prevent a physical verdict.
The existing sphere-lag diagnostic must be reconciled before any duplicate
run. A meaningful well test needs background-subtracted excess, a formed
baryonic profile, and persistence/binding under the actual equations.

AN1's stated finite-Q0 diagnostic also uses flow speed v in the contract but
circular speed sqrt(g r) in code. These are inequivalent near turnaround.
A full finite-Q0 continuation must derive its approximation conditions from
the current, rather than treating that proxy as a validity certificate.

### 6. Several smaller claims need tighter interpretation

- **HF1:** hard-clipping an isothermal density to a constant phase-space cap
  while holding sigma spatially constant violates Jeans equilibrium on a
  saturated interval: d(rho sigma^2)/dr=0, whereas -rho g is nonzero. The
  [solver](../../rebuild_2026_10_22/HF1_hybrid_fermion/hf1_fermion.py) is a capped
  density prescription there, not a stationary fermion distribution. This
  limits the capped-disc interpretation; the uncapped cluster failure and
  independent CMB failures are not repaired. Five primary masses fail and one
  is unconverged; that is not a continuous-family exclusion theorem.
- **KT3:** the displayed positive-delta attractor is checked against an assumed
  reduced ODE, not derived from a kinetic action. With conventional positive
  scalar kinetic energy and KT2's potential sign, the leading force for
  delta=1-chi has the opposite sign. This is a conditional fixed-background
  finding; full constrained gravitational backreaction has not been audited.
  The algebraic elimination and unfixed normalization conclusions survive.
- **KU2:** its UNIVERSAL label means no detected matched slow/fast residual
  difference under the chosen model-selection procedure. It is not an
  equivalence test or proof that kappa is universal. Its absolute mass
  calibration and environment caveats remain material.
- **NP2:** finite derivative/admissibility checks do not establish global
  admissibility, and rejection of a fitted smooth rule is not exclusion of
  every function of the same variables. The successful flexible fits to the
  first gates are useful evidence that a universal algebraic impossibility
  has not been demonstrated.

## Work worth retaining

| Programme | What survives this review | What it does not establish |
|---|---|---|
| a0 law and normalization | A useful empirical target; KT23's ladder-distance sample is compatible with one-half under its chosen kernel | A forced value of kappa, a universal law across all systems, or the DE normalization |
| KT spatial filtering | The implemented map can change vertical relative to radial response; KT25's canonical near-pass is a concrete diagnostic target | A conserving action; a robust Milky Way pass at the star-count thick fraction; one operator across scales |
| Formula and residual searches | Extensive scoped failures, scrambled controls, and evidence of sample-identity confounding | Exhaustion of all physical functions, states, histories, or actions |
| Native collapse and route E | Reproducible profile/response information and a serious contraction/observational tension | A reason to reinstate the retired sector or combine its passes with another parent's equations |
| X48 entropy transport | Finite formed-core examples and conditional energy/prefix-preservation estimates | Mesh-uniform seeding, unconditional all-time floor, or a physical core normalization; work remains parked |
| FR01 and DR01 | Dense-state energy-saddle evidence; restricted dilute screens; a conserving finite quadrupole response | Stable dense-core formation or retained monopole regulation; linear work is not contraction suppression |
| TP01–04 | Substantial finite spectrum, matching, current, and named loss-channel calculations | A produced gravity-compatible relic, complete inclusive lifetime, or a derived vacuum scale |
| TP05 | Correct checked leading tadpole/cubic relations and a scoped canonical-tilt obstruction | A full stable SUGRA vacuum, neutral spectrum, modulus stabilization, or solved production |
| Yang–Mills C2 | Restricted cactus and finite-cluster results with a checked semiclassical source application | Full cubic conditional propagation, volume-uniform control, or a continuum mass gap |

The current TP summaries are notably careful about these limits. For example,
the old MeV point's leading-gravity force exceeds its maximum restoring force
by about 30.3; the lower ~26 keV branch remains unfinished. The old MeV
benchmark's raw vacuum mismatch of roughly 10^74 and stipulated relic
distribution are already
disclosed. Repeating its rigid lifetime calculation would not solve those gaps.

## A concrete way forward

**First priority: an action-consistent spatial response.** The first bounded
test is the outer-adjoint completion of the actual KT simple-nu low-pass map,
with the parameters frozen at the existing candidate values. Verify reciprocity
and force balance, then test the existing Milky Way near-pass cells and Cassini
with the same operator. Initially this is a diagnostic with a declared fixed
width for each boundary problem; it is not yet a universal system-mass law.
If the window disappears, record that outcome before inventing another width.

If it survives, the next obligation is a single definition of the filter on a
host plus satellite plus compact source, independent of how the source is
labelled or split. A variational state-dependent operator must include its full
derivative. The scale and any new coefficients remain inputs until derived.
Then confront the complete vertical profile, host/Fornax response, SPARC, and
the untouched cluster/merger requirements. A galaxy-filter pass would still
leave the cosmological and cluster programme open.

An adjacent established framework is generalized QUMOND, which permits spatial
derivative dependence at the action level. Its existence supports this type of
construction, not any specific filter or empirical success. See Milgrom,
[arXiv:2305.01589v2, sections II and III](https://arxiv.org/html/2305.01589v2),
and the original [QUMOND action, equation 3](https://arxiv.org/html/0911.5464v2).
Both primary versions were authenticated and the relevant equations inspected.
No global novelty claim is made.

**Second priority: a valid nonlinear-well test of the authorized one-field
model.** Calibrate the Gaussian and top-hat checks against their own analytic
solutions, reconcile AN2's existing lag diagnosis, and use an excess/bound
mass criterion. First check the full constrained kinetic and characteristic
matrices on the intended occupied states, retaining the existing health
obstructions. Only an admissible regime warrants a controlled finite-Q0
initial-value problem with the relevant validity terms retained.
More shapes in the same unvalidated reduced engine cannot settle that question.

**Third priority: falsification with a calibrated measurement pipeline.** Fix
the chi-square tail calculation and audit the affected marginal probabilities.
For a completed gravity candidate, freeze one parameterization and jointly
test the Milky Way radial and vertical profiles and a vector host/dwarf setup.
Use held-out systems or observations for confirmation: a newly frozen threshold
on repeatedly inspected data is still a post-hoc screen. This can reject a
candidate without requiring a new large simulation campaign.

The [next-step specification](NEXT_STEP.md) makes the first route concrete.
The review executed the mathematical consistency checks; it did not run the
new completed operator through the full observational pipeline or silently
change any existing verdict.

## Evidence package

- [Reciprocity proof and independent review](FILTER_RECIPROCITY.md),
  [bounded result](reciprocity_run/result.json), and
  [validated manifest](reciprocity_run/manifest.json).
- [Gravity and empirical detail](gravity/REPORT.md), including the independent
  momentum and probability checks.
- [Cosmology and core detail](cosmology/REPORT.md), including the exact-dust
  benchmark and homogeneous-background counterexample.
- [Particle and Yang–Mills detail](particle/REPORT.md), including five tiny
  independent symbolic checks and the audited dependency boundaries.
- [Final verification record](VERIFICATION.json) and
  [archive provenance](ARCHIVE_PROVENANCE.json).

The durable result is a more reliable decision boundary: there is a precise
conserving equation to test next, and several negative/positive diagnostics
must be interpreted more narrowly. Neither constitutes a completed theory.
