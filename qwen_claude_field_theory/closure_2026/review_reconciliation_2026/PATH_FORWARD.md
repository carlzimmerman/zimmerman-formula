# Same-action closure: reconciliation and implementation plan

> **For agentic workers:** Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` when implementation is authorized. This handoff does not authorize editing frozen preregistrations or changing the theory silently.

**Goal:** Resolve disputed claims reproducibly, then construct or falsify one explicit relativistic action against the original gravity requirements.

**Architecture:** One action is authoritative; every reduced equation must retain a derivation back to it. Cheap algebraic and variational gates precede parameter scans and expensive dynamics. Failed gates exclude only the stated branch and assumptions.

**Tech stack:** Existing Python, NumPy, SciPy and SymPy; exact symbolic checks where possible; numerical residual and convergence checks elsewhere.

**Spec:** The user's original requirements, restated below. The latest candidate is documented in `../THE_ACTION_2026-09-05.md`; it is an object to test, not a certificate.

**Reviewed baseline:** `06a698432236e6f7f65917aba9852705beb0de36`, 2026-09-08. Existing unrelated dirty files are excluded from this handoff.

## Trust is not an acceptance criterion

There is no evidence here establishing that another model deliberately lied. There is evidence of code/claim mismatches and an overstatement by this reviewer. A result is accepted because its hypotheses, calculation and residuals survive independent checking, not because Claude/Fable or OpenAI/Astra endorsed it.

**Reviewer correction, preserved explicitly:** g04k's literal force implementation is not unbounded at external-field cancellation. The `max(s, 1e-30)` denominator bounds its multiplier, and the multiplier tends to zero at exact cancellation. The earlier literal-divergence claim is withdrawn. The actual criticism is loss of the intended physical acceleration cap and strong cancellation sensitivity. No claim is made here about how often trajectories enter that region or how much it changes the aperture masses.

## Global constraints

- The target remains `mu(y) = 1 - exp(-y)`, with `y = |grad Phi|/a0`, unless the user explicitly changes it. The saturated RAR carrier is a differently named variant, not the same law.
- Require exactly two propagating gravitational degrees of freedom, both tensor polarizations, with no gravitational scalar. Any allowed genuine matter/clock mode must be separately identified, counted and shown healthy; auxiliary fields cannot hide extra propagation.
- Derive Phi and Psi separately, ordinary minimally coupled matter conservation, measured Newton's constant, beta/gamma/alpha1/alpha2/alpha3, tensor speed and positive energy from the same theory.
- Require an expanding FLRW solution, controlled homogeneous and zero-field sectors, and no ghost, gradient instability, pathological strong coupling or unacceptable physical instantaneous/superluminal channel.
- Treat `a0 = (c/2) sqrt(G rho_DE)` as input until derived. Constant a0 is allowed. Do not spend the first repair cycle trying to derive the coefficient 1/2.
- Never input desired constraint ranks, degrees of freedom or PPN values into certification logic. Compute equations and invariants first, then compare with independently stated requirements.
- Preserve original source files, published records, hashes and preregistrations in this handoff. Corrections to them require an explicit subsequent change with an audit trail.

## What this commit actually delivers

- [x] A corrected statement of the reviewer error.
- [x] A replayable diagnostic using selected functions from the current source, without running their large top-level scans: `REPRODUCE.md`.
- [x] Machine-readable output and input hashes: `results.json` and `manifest.json`.
- [x] This ordered handoff. It is not a repaired theory, a new no-go theorem, or a replacement preregistration.

The replay distinguishes a successfully executed audit from a successfully validated physical claim. Its exit status can be zero while measured equation residuals contradict a claimed solution. Check the reported quantities, not just the process status.

## Gate 0: adjudicate the inexpensive disputes first

**Files:** Read `REPRODUCE.md`, `results.json`, `manifest.json` here. Original source paths are recorded in the results. Corrections below are proposed work, not changes already made.

**Consumes:** The pinned source and its literal functions. **Produces:** Source-specific findings, each with a residual/invariant and an explicit non-claim.

- [ ] Reproduce the force example and the numerical-floor correction. Do not repeat the withdrawn literal-divergence statement.
- [ ] Evaluate k04's returned q against its original flux equation, not just successive-iterate changes. Report failure to converge separately from a physical branch ending.
- [ ] Check the replacement kernel's external-field inversion against `s + Delta(s) = g_external/a0`. Do not reuse the original exponential conversion after changing the kernel.
- [ ] Reconcile the manuscript's BTFR sign with its defined statistic and plotting code. Published/preregistered changes must be explicit amendments, not silent overwrites.
- [ ] Classify the remaining review findings separately: established algebra/code discrepancy; conditional physical implication; numerical proxy; or not independently verified.

**Exit criterion:** Both author and reviewer can obtain the same measured quantities from the same source. Agreement on interpretation is not required. Disagreement means provide a smaller countercheck, not another authority claim.

## Gate 1: define a valid constitutive action before repairing predictions

**Proposed new files, only after implementation authorization:** `constitutive_gate.py`, `CONSTITUTIVE_DECISION.md`, with independently failing/working control tests.

**Consumes:** One explicitly selected action and branch, with units, matter metric, boundaries, field domains and differentiability assumptions. **Produces:** A well-defined primitive or constrained variational problem and its actual Euler-Lagrange equations.

For the current regular single-scalar carrier, test the exact implication

    g_phi = a0 Delta(s),  Y = a0^2 Delta(s)^2,  J_Y(Y(s)) = s/Delta(s).

If Delta is exactly constant on a nontrivial interval, Y is constant while the demanded derivative varies: this cannot define a differentiable, single-valued J(Y). Boundedness alone also does not force a maximum at finite s. Neither observation excludes an explicitly defined nonsmooth/constrained action.

- [ ] Attempt a literal regular-J reconstruction first; test two distinct source values on the plateau. If it fails, label that regular representation invalid.
- [ ] If retaining the plateau is chosen, specify an actual convex constraint/dual formulation, its allowed variations, multipliers and boundary terms. Derive the constitutive graph rather than clipping the solution. Then count any added modes at Gate 2.
- [ ] Keep the original exponential-law target distinct. A repair that only realizes the saturated RAR variant does not satisfy that target, even if internally consistent.
- [ ] If the carrier route cannot meet the target, the next architectural candidate is the elliptic phantom-density route, but it starts from a new explicit action and receives no inherited PASS results.

**Elliptic-route first obstacle:** On a compact boundaryless slice, integrating `Delta_h chi = 4 pi G rho` gives zero on the left and nonzero total matter on the right. A zero-mean projection, background equation or boundary flux must follow from the action and boundary conditions. Manually deleting k=0 is not a cosmological completion.

**Exit criterion:** An action defines every branch being used. If that requires a materially different action, present the choice before implementing downstream repairs. No larger infall run is justified before this gate.

## Gate 2: vary everything and close the constraint algorithm

**Proposed outputs:** `full_action_variation.py`, `dirac_closure.py`, and a constraint ledger tied to a source hash.

**Consumes:** Gate 1's explicit action, including all auxiliary/clock/four-form and boundary terms. **Produces:** Full field equations; canonical variables; constraints and preservation equations; Poisson-bracket operators and sector-specific counts.

- [ ] Vary the metric, scalar, clock, auxiliary and multiplier fields before fixing gauges or inserting background equations. Keep ordinary matter variation separate.
- [ ] Derive primary constraints from the velocity Hessian/Legendre map. Preserve each constraint until it determines a multiplier or produces a new independent constraint; continue until closure.
- [ ] Compute brackets, their null directions and differential-operator kernels. A sampled finite matrix rank alone is not a continuum proof.
- [ ] Separate k=0, k!=0, boundary modes and the y=0 limit. Count physical phase space only after first-/second-class classification and gauge handling.
- [ ] For a four-form extension, differentiate at fixed original independent fields and specify the flux/boundary ensemble. The sign of L_qq alone does not establish a propagating ghost. A q=0 kink requires an explicit variational completion.

**Exit criterion:** A derived constraint count and matter Ward identity, not a target count embedded in assertions. Otherwise stop and report the smallest missing preservation equation or branch obstruction.

## Gate 3: derive physical predictions from that same action

**Proposed outputs:** `weak_field_gate.py` and a derived-equation-to-solver mapping.

**Consumes:** Gate 2's field equations and matter metric. **Produces:** Independent Phi and Psi equations, the actual MOND law, lensing and PPN limits, and a source-derived numerical force operator.

- [ ] Derive Newtonian/deep-MOND limits and the measured G. In spherical symmetry verify the original exponential relation by forward substitution, not by fitting another kernel.
- [ ] Derive beta, gamma and all preferred-frame parameters. Static Phi=Psi is not a substitute for the moving-source PPN calculation.
- [ ] Derive the full coherence operator's variation. A Helmholtz-filter proxy does not inherit exact equivalence to a nonlinear action.
- [ ] Solve external-field boundary conditions with the selected kernel's own inverse. For an irrotational quasistatic metric force, test curl, field-equation residuals and boundary convergence.

**Exit criterion:** Prediction and solver use the same equations. Recompute Solar-System and binary numbers before proposing any amendment. Check current observational bounds against primary sources at execution time.

## Gate 4: expanding cosmology and physical stability

**Proposed outputs:** `cosmology_stability_gate.py`, background and perturbation residuals, mode and characteristic analysis.

**Consumes:** The same action and constraint reduction. **Produces:** Expanding FLRW backgrounds and scalar/vector/tensor perturbations with their physical kinetic and gradient matrices.

- [ ] Solve the background, including homogeneous auxiliaries and conserved charges, without forcing H=0 to remove modes.
- [ ] Solve coupled perturbations together. Define `r = (2-K_B)^2/(c_2 |K_2|)`. Do not use the single-feedback approximation `1-r` as an exact cancellation at r=1; the previously checked prescribed-metric branch gives `1/(1+r)` instead. That countercheck is not itself a complete FLRW solution.
- [ ] Derive tensor speed/energy, scalar poles, vector structure, strong-coupling behavior and the approach to y=0. Distinguish gauge/constraint instantaneous equations from physical signal channels.
- [ ] Evolve source histories when the boost changes growth. An assumed matter-era response coefficient is not automatically valid in that changed solution.

**Exit criterion:** An actual healthy expanding branch in stated regimes. No inference of global stability from one secant derivative, one wavenumber or one fixed-metric reduction.

## Gate 5: then confront galaxies, clusters and the dark sector

**Proposed outputs:** Converged action-derived dynamics and a likelihood/provenance report; reuse the corrected `../cluster_measurement_audit_2026/` data handling.

**Consumes:** The derived force, cosmological initial spectra and one parameter set. **Produces:** Testable predictions with systematics, not a stitched collection of different models.

- [ ] Verify homogeneous-background recovery and conservation controls before galaxy capture. Use consistent baryon assembly and compare controls at matched baryonic mass.
- [ ] Refine timestep, force resolution, particle count, domain and seeds. A minimum timestep must not overrule an accuracy ceiling. Begin small; authorize a large run only when its discriminating purpose is named.
- [ ] For a relic/wave component, use its actual initial power suppression and dynamics. Random velocities alone do not reconstruct erased correlations. Stationary scattering does not measure bound capture.
- [ ] An upper bound exceeding a tolerance does not prove the true mass exceeds it. A no-go needs a justified lower bound or a demonstrated exhaustive argument under explicit assumptions.
- [ ] Compare cluster pressure/baryon/lensing observables with their uncertainties. Do not infer measurement error merely because a model misses them, or infer universal failure from one toy profile.

**Exit criterion:** Either one consistently tested theory, or a scoped falsification identifying the first unavoidable obstruction. Only then assess novelty against primary literature and formulate a genuinely discriminating new prediction.

## Next assignment for Fable or any other worker

Run the replay unchanged, acknowledge or refute each discrepancy with an equation-level counterexample, then tackle Gate 1 only. Return the explicit variational definition or the precise obstruction. Do not start another particle scan, claim a new universal no-go, or reuse downstream PASS labels while the action-to-equation link is unresolved.

**Current status: OPEN.** Some implementations and proof implications fail their stated checks; neither the full framework nor all possible completions have been adjudicated.
