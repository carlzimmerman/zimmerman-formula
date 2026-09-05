# First-principles relativistic MOND: closure roadmap for Fable

**Date:** 2026-09-04. **Inspected HEAD:** `4fed8bfa6`.
**Goal:** construct one explicit theory satisfying the full specification, or
prove a sharply scoped incompatibility; neither outcome is guaranteed.
**Architecture:** freeze the observable equation first, apply inexpensive
static falsification tests, then derive every sector from one covariant
action. A result from a different action cannot fill a missing gate.
**Tools:** SymPy, numerical linear algebra, independently checked PDE solvers,
versioned observational inputs, and explicit analytical arguments.
**Spec:** the user's thirteen-requirement full-theory target, restated below.

This is a research roadmap, not a claim that the unknown action has been
constructed. Proposed scripts below do not yet exist. The current change is
documentation only. For implementation, follow the repository's computation
audit and test-first workflow; use task-by-task review rather than a single
unreviewable omnibus script. All new calculation files belong under
`qwen_claude_field_theory/closure_2026/`, respecting its scope fence.

## 1. Fable's immediate assignment

Do these in order, with a small independent review after each result:

1. **G00: freeze the target and audit the current evidence.** Distinguish
   exact exponential AQUAL, exact-inverse QUMOND, the empirical RAR kernel,
   and the double-filter extension. Inspect the latest f31/f31b/f31c results
   before claiming any preferred-frame screening. Do not rerun a long
   symbolic pipeline merely to regenerate already authenticated output.
2. **G01: close the cheap obstructions for the strict target.** Audit the
   exact-AQUAL Cassini boundary-value problem and the positive-density
   zero-force center. The existing evidence is adverse but its numerical
   and regularity qualifications must survive into the verdict.
3. **G02: for the screened extension, compute its actual external-field
   response.** Start with the Fourier benchmark derived below, then solve
   the nonlinear Sun-plus-external-field problem with the exact inverse
   exponential kernel, both filters, and unsmoothed baryonic gravity.
   Extract the monopole and quadrupole, not just a point-source force.
4. **G03/G04: only if that survives, supply a complete covariant action and
   vary the metric-dependent filter and clock as well as the auxiliary
   fields.** A schematic `S_aux` is not a deliverable. Do not identify u or
   Phi with a metric scalar without deriving the identification.

In parallel with G02, a second worker can finish the narrow audit of the
existing f31c operator comparison. That work is a host-specific diagnostic,
not permission to import its PPN values into the double-filter action.
The full Dirac calculation starts only once the action is fixed.

**First handoff from Fable:** exact action/target ID, one runnable diagnostic,
its tests and command, raw numerical or symbolic result, and PASS/FAIL/OPEN
with assumptions. A failed gate is a useful result; do not conceal it or
silently switch theories. No further speculative ansatz list is needed.

## 2. Non-negotiable target and the necessary fork

Use one physical metric for baryons, photons and laboratory clocks. On the
specified weak static branch, the original target is

\[
 \nabla\!\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]=4\pi G_N\rho_b.
\]

The same theory must supply two propagating gravitational tensor modes,
independently derived Phi=Psi, acceptable beta/gamma/alpha1/alpha2/alpha3,
ordinary matter covariant conservation, luminal healthy tensors, no hidden
auxiliary propagator, controlled scalar/vector sectors, expanding viable
FLRW, controlled k=0 and zero-field limits, and measured Newton/GR recovery.
Any genuine matter/clock mode is separately counted and tested in the
coupled system; changing a scalar's name does not remove its physics.

The explicit reference targets are N_grav=2, Phi=Psi, gamma_PPN=1,
beta_PPN approximately 1, alpha1=alpha2=alpha3=0, nabla_mu T_m^(mu nu)=0
and c_T=c. Record exact theoretical identities separately from observational
agreement within a stated confidence interval. Where the user's specification
allows observational tolerance, report that tolerance; never label an
approximate bound as an exact identity or silently weaken an exact requirement.

The two research tracks are **not two halves of one solution**:

| Track | Observable equation | Eligible to close original target? |
|---|---|---|
| A: strict target | Exact exponential AQUAL for general sources in its stated domain | Yes, if all other gates and empirical tests pass |
| B: screened extension | An action-derived modification with an additional length xi | Not if it changes that required equation; an explicit revised specification is needed |

Track B is authorized for investigation, but that does not authorize calling
it closure of Track A. It can become a useful alternative theory or a
falsification result. Recovering the spherical relation at xi=0 does not
prove general-source AQUAL, since its current parent is QUMOND.

Freeze a0 as an input initially. Preserve the optional relation

\[
 a_0=\frac{c}{2}\sqrt{G\rho_\Lambda}
     =c^2\sqrt{\Lambda/(32\pi)},\qquad
 \rho_\Lambda=\Lambda c^2/(8\pi G),
\]

where rho_Lambda is a mass-equivalent density. This is not a derivation of
the coefficient. Audit which measured/bare/cosmological G occurs before
identifying them. Report canonical a0=9.3619e-11 and alternate 1.1279e-10
m/s^2 where inherited comparisons require both. A varying a0 or xi is a new
coupling/field whose equations and degrees of freedom must be included.

## 3. What the inspected repository actually establishes

| Evidence | Safe use in this roadmap |
|---|---|
| `smoothed_onset_action_2026/REPORT.md`, commit `4fed8bfa6` | A static action, required outer adjoint filter, finite reciprocity checks, conditional sixth-power onset; no covariant theory or data validation |
| `aqual_solar_gate_2026/REPORT.md`, commit `5b0c721d0` | Exact AQUAL Q2 around 2.10e-26 s^-2, roughly four times the adopted Cassini upper endpoint; 13/14 numerical cases complete, strict iteration gate still OPEN |
| `exact_exponential_aqual_q2_2026/REPORT.md` | Earlier direct AQUAL calculation for cross-checking; its numerical error estimate is not automatically a certified continuum bound |
| `slipless_exact_mond_center_nogo_2026/REPORT.md` | Center regularity obstruction under the stated exact-law/metric assumptions; inspect uniform validity of the weak-field expansion before claiming an exact-metric theorem |
| `hunt_2026/f29_coherence_length_law.py` | Gaussian phantom calculation using the RAR kernel; not the exact inverse exponential action now under test |
| `hunt_2026/f30_ppn_screening_door.py` | Gaussian/Helmholtz core distinction; absence of a static 1/r scalar potential is not a PPN proof |
| `hunt_2026/f31_ppn_k4_alpha1.out` and `f31b_ppn_k4_split.out`, commit `5807a46b9` | Recorded operator-specific suppression hypotheses fail; some final prose contradicts the calculated failures |
| `hunt_2026/f31c_ppn_k4_operators.py/.out` | Untracked work at inspection; output stops after operator construction, so no completed verdict is available |

Older STANDING/RESUME_HERE entries contain obsolete kernels, withdrawn
claims and later corrections. Use them as an index, not as certification.
In particular, a finite scan of a kernel family is not a theorem about every
one-argument kernel. No claimed MMG/AeST/no-go result transfers without its
exact hypotheses and action matching the current candidate.

## 4. The available static action and first new benchmark

The concrete Track B starting point, in nonrelativistic units, is

\[
 I=\int dt\,d^3x\left\{\mathcal L_{m,\rm kin}-\rho_b\Phi
 -\frac{2\nabla\Phi\cdot\nabla u-|\nabla u|^2
 -a_0^2q(|\nabla S_\xi u|^2/a_0^2)}{8\pi G}\right\},
 \quad S_\xi=e^{\xi^2\Delta/2}.
\]

With s=y(1-exp(-y)), define

\[
 \nu(s)=y/s,\quad \mathcal G(y)=y^2+2(1+y)e^{-y}-2,
 \quad q(s^2)=2sy-\mathcal G(y)-s^2.
\]

Then q'(s^2)=nu(s)-1, and variation yields

\[
 \Delta u=4\pi G\rho_b,\qquad
 \Delta\Phi=4\pi G\rho_b+S_\xi^*\nabla\cdot
 [\{\nu(|\nabla S_\xi u|/a_0)-1\}\nabla S_\xi u].
\]

On flat isolated space S*=S. The filter on the output is compulsory.
The known parent action is [Milgrom's QUMOND, equations (3)-(6)](https://arxiv.org/pdf/0911.5464v2),
not a new invention of two-potential gravity. The filter modification and
its consequences require their own attribution and novelty audit.

### A cheap external-field calculation Fable can start immediately

Linearize this action about a constant nonzero filtered Newtonian gradient
a0 s_e ehat. Let sigma(k)=exp(-xi^2 k^2/2). Derive, independently of this
display, the source response

\[
 \delta\Phi(\mathbf k)=-\frac{4\pi G\,\delta\rho_b(\mathbf k)}{k^2}
 \left[1+\sigma(k)^2\left\{\nu_e-1+s_e\nu'_e
                  (\hat{\mathbf k}\cdot\hat{\mathbf e})^2\right\}\right].
\]

Test the longitudinal tangent d(y-s)/ds=1/[mu+y mu']-1 and transverse
tangent nu-1; finite-difference both. Two Gaussian filters give sigma^2,
not sigma. Test xi=0, kxi>>1, rotated wavevectors, and constant-background
subtraction. These are benchmarks for the new solver, not PPN parameters.

The external Newtonian field and physical measured Galactic field must be
matched through the candidate's Galactic solution; do not assume the
spherical algebraic conversion is exact in a nonspherical galaxy. Start
with a controlled input-field scan and label that uncertainty explicitly.

For isolated compact sources the same action gives

\[
 r_{\rm eq}^6\sim\frac{81}{4}\frac{GM_b\xi^4}{a_0},\qquad
 R\ll r_{\rm eq}\ll\xi,\quad GM_b/(a_0\xi^2)\to0.
\]

Do not use this asymptote for galaxies at xi=0.05–0.1 pc. At those lengths,
epsilon<=1e-4 corresponds to M<=0.000168–0.000672 solar masses. An external
field can eliminate the isolated mass exponent. Finite source structure and
comparable-mass binaries need new derivations, not insertion of total mass
into a test-particle formula.

## 5. Dependency order

```text
G00 freeze target, conventions, evidence
  ├─ Track A: G01 exact-AQUAL external-field + center gate
  └─ Track B: G02 double-filter external-field + source gate
          ↓ only a surviving, explicitly identified target continues
G03 complete covariant action and domain
          ↓
G04 full variations, Ward identities, static matching
          ├─ G05 ADM/Legendre → G06 full Dirac closure
          ├─ G07 homogeneous equations and k=0 compatibility
          └─ G08 independent weak metric potentials and measured G
                    ↓ combine compatible branches/parameters
G09 reduced perturbations, strong coupling, GW
G10 moving sources, full PPN or direct finite-scale observables
G11 initial/boundary problem, causality, zero-field matching
G12 cosmological perturbations and structure formation
G13 independent empirical prediction and novelty audit
G14 same-action closure package OR scoped no-go proof
```

Background FLRW equations may be checked early alongside the Hamiltonian
work because H=0 is an inexpensive decisive failure. Perturbative health
and cosmological observations require the completed constraints. Passing
one diagram branch cannot compensate for failure on another.

## 6. Full computation and derivation list

Each gate below produces a derivation, executable computation, behavior
tests, source hashes and a report. New gate files should live in a fresh
`closure_2026/fable_closure_roadmap_2026/` folder, with the stated basenames.
Do not create empty files or PASS certificates in advance.

### G00 — Freeze and authenticate (`g00_contract.md`, `g00_provenance.py`)

- [ ] Record action ID, complete couplings/free functions, field list,
  physical metric, boundary/initial data, units, signs and approximation
  domain; explicitly label strict target or screened extension.
- [ ] Hash authoritative input scripts and compare cached objects with their
  producing source, versions and assumptions. Inspect real return codes.
- [ ] Reproduce the ten onset tests and the eight nearby existing tests
  listed below; these are regression checks, not full-theory gates.
- [ ] Reconcile f31 numerical failures with its unconditional verdict prose;
  compare trace-Laplacian, Hessian-squared and coherent-stiffening operators
  only after deriving each from its own action. Mark partial f31c OPEN.

**Stop condition:** no unambiguous target or no reproducible provenance.
Do not spend further algebra on a statement that changes between files.

### G01 — Strict-law cheap falsification (`g01_strict_aqual.py`)

- [ ] Re-derive mu, its exact primitive, Newtonian and deep-MOND limits,
  spherical first integral and measured-G normalization.
- [ ] Solve the exact nonlinear AQUAL Sun/external-field problem with
  physical inner/outer data. Reuse the corrected multipole extractor.
  Resolve the 1e-11 iteration issue or independently bound the observable
  with a different discretization; never turn an exhausted cap into PASS.
- [ ] Verify signed quadrupole convention, boundary, mesh, precision and
  zero-saddle sensitivities. Compare a published same-kernel benchmark and
  the current observational likelihood, not a QUMOND substitute.
- [ ] At rho(r)=rho0+O(r^2), derive g^2~(4pi G_N a0 rho0/3)r and
  Phi'/r~r^(-1/2). Determine weak-solution existence, tidal observables,
  curvature and validity of the weak-field expansion into that center.
- [ ] If a relativistic boundary layer cures the center, calculate its
  thickness and matching and state exactly where universal AQUAL stops
  applying; a regulator/floor is not the original exact law.

**Fail implication:** identical physical static equations, source and
boundary conditions cannot be rescued merely by changing the covariant
carrier. An observational exclusion remains conditional on data/model
assumptions; it is not a universal mathematical no-go.

### G02 — Screened static falsification (`g02_filtered_efe.py`)

- [ ] Derive and test the Fourier response in section 4 from the action.
- [ ] Implement the full nonlinear axisymmetric source/external-field
  problem: solve u, apply S, calculate the vector phantom flux, apply S*,
  solve Phi. Match the nondecaying external background separately.
- [ ] Use Gaussian convolution with its actual width convention; extend
  the domain or add analytic tails. Demonstrate continuum/boundary
  convergence with a second representation of the filtering operation.
- [ ] Compute signed Q2, radial anomalous acceleration and tidal tensor
  over planetary radii. A constant sunward magnitude is not a constant
  vector acceleration and does not cancel from relative orbital motion.
- [ ] Scan one universal xi across Solar-System, nonspherical galactic and
  finite compact-source problems, with the two stated a0 inputs and
  environmental uncertainty. Do not reuse f29's RAR-based floors.
- [ ] For two finite bodies derive forces by varying both positions in the
  same action; test total momentum, mass-ratio limits and internal structure.
  Recalculate whether any observable onset law survives these conditions.

**Fail implication:** discard this static prescription/parameter region.
Do not start its costly covariant completion after a decisive static failure.

### G03 — Supply an actual covariant action (`g03_action.py`)

- [ ] Write every term in S_EH+S_aux+S_m, including boundary terms and all
  auxiliary/clock kinetic, gradient, multiplier and normalization terms.
  Specify whether the theory is fundamental or an EFT with a cutoff.
- [ ] If using a clock tau, derive n_mu=-partial_mu tau/sqrt(-partial tau^2)
  and the induced projector/connection; if using an independent unit vector,
  vary its normalization multiplier and transverse components separately.
- [ ] Define the intrinsic leaf Laplacian, its domain, measure and inverse
  or heat kernel. A projected spacetime Hessian is not automatically the
  intrinsic Laplace-Beltrami operator; compute extrinsic-curvature terms.
- [ ] Identify covariant quantities whose limit is u/Phi; potentials from
  a gauge-fixed static calculation are not automatically spacetime scalars.
- [ ] State all free initial and boundary data. A localization by auxiliary
  diffusion coordinate or rational filter approximation defines a new
  system until equivalence and extra-mode counting are demonstrated.
- [ ] Perform an early causal-feasibility screen: identify which physical
  source/response channel the spatial filter modifies and how the proposed
  dynamical completion could avoid a prohibited instantaneous signal. A
  decisive obstruction here stops expensive ADM/PPN work; an unresolved
  channel remains OPEN until the full G11 initial-value analysis.

**Stop condition:** unresolved schematic operators, hidden boundary data,
or a fixed preferred structure claimed to be a dynamical covariant field.

### G04 — Vary everything and derive conservation (`g04_variation_ward.py`)

- [ ] Derive metric, clock/vector, auxiliary, multiplier and matter
  Euler-Lagrange equations before gauge fixing or symmetry reduction.
- [ ] Include variation of the smoothing operator, its integration measure
  and adjoint. For S=exp(A), A=xi^2 Delta_h/2, evaluate
  delta S=integral_0^1 exp[(1-s)A](delta A)exp[sA] ds; verify by
  finite differences on a discretized curved leaf. Vary xi if it is a field.
- [ ] Derive the full Noether identity off shell. Separately derive the
  matter diffeomorphism identity from S_m alone and show that its matter
  equations imply nabla_mu T_m^(mu nu)=0, with no auxiliary source term.
- [ ] Vary photons and massive matter against the same metric. If an
  auxiliary term depends explicitly on baryon density/current/T_m, derive
  the altered matter equation instead of appealing only to total conservation.
- [ ] Reduce these equations to the target static law, retaining stresses
  from the filter and clock. Verify the action, not a postulated density,
  produces the modified source.

**Fail implication:** missing adjoint/metric terms, nonmetric baryon forces,
or incorrect static limit prevents closure of that action.

### G05 — ADM and Legendre map (`g05_hamiltonian.py`)

- [ ] Decompose the full action into lapse N, shift N^i, h_ij, all auxiliary
  and matter variables, keeping boundary terms and spatial derivatives of
  lapse. Introduce independent variables for higher time derivatives if needed.
- [ ] Calculate every momentum and the complete velocity Hessian, including
  metric-clock-matter mixing. Solve the Legendre map only on justified strata.
- [ ] Derive primary constraints from its null directions and construct the
  canonical and total Hamiltonians. A vanishing lapse-only minor is not
  degeneracy of the full map; a quadratic flat-space Hessian is not enough.
- [ ] Check covariant and gauge-fixed reductions against each other without
  deleting equations by imposing the gauge inside the original action.

**Deliverable:** explicit phase-space coordinates, symplectic form, momenta,
primary-constraint functions, H_c and H_T; not an expected DOF integer.

### G06 — Full Dirac-Bergmann closure (`g06_dirac.py`)

- [ ] For every constraint C_a, compute dot C_a=partial_t C_a+{C_a,H_T}.
  Find all secondary, tertiary and higher constraints, or determined
  multipliers, continuing until preservation adds nothing independent.
- [ ] Calculate the full Poisson-bracket operator matrix on the actual
  constraint surface. Check functional independence, null vectors,
  boundary terms and reducibility; use smeared constraints in the continuum.
- [ ] Classify first/second class by the complete algebra and construct the
  gauge generators. Verify the physical interpretation of every gauge symmetry.
- [ ] Compute N_phys=(dim phase space-2 N_FC-N_SC)/2, then identify which
  physical modes are tensors, vectors, clock/matter or hidden auxiliaries.
  Never subtract a scalar merely because it is labelled matter.
- [ ] Repeat rank and closure at generic field configurations, k!=0,
  homogeneous k=0, zero field, FLRW, high acceleration and exceptional
  coupling surfaces. Explain rank changes and physical boundary modes.
- [ ] Use exact symbolic/minor tests and independent numeric ranks with
  tolerance/precision studies; numeric rank alone is not a field-theory proof.

**Fail implication:** an extra physical gravitational mode, a lost equation,
inconsistent preservation or unaccounted rank bifurcation defeats the count.
Removing it by imposing K=0/H=0 is not an acceptable cosmological solution.

### G07 — Homogeneous background first (`g07_flrw.py`)

- [ ] Substitute FLRW only after deriving the full equations. Independently
  vary the homogeneous action while retaining the lapse until its variation.
- [ ] Derive the Friedmann, acceleration, clock/current and matter equations;
  verify their Noether redundancy and the mapping to the k=0 constraints.
- [ ] For any Delta_h chi=source equation, integrate over the spatial domain:
  a compact leaf without boundary requires zero mean source. Homogeneous
  noncompact solutions need explicit admissible boundary/asymptotic data.
  Do not remove positive mean matter by silently subtracting it.
- [ ] Find an expanding H!=0 branch through radiation, matter and late-time
  acceleration, with finite fields and derived G_cosm/G_N. Integrate it
  numerically and test constraint drift and early-time singularities.

**Fail implication:** no expanding source-compatible branch ends the candidate.
Fitting one H(z) curve alone does not establish viable cosmology.

### G08 — Independent weak-field metric and measured G (`g08_metric.py`)

- [ ] Expand the physical metric in independently varied Phi, Psi and shift;
  use the 00, 0i, spatial trace and traceless spatial field equations.
- [ ] Solve auxiliary and metric equations together, including boundary and
  homogeneous modes. Derive Phi and Psi separately; calculate slip and the
  lensing potential Phi+Psi for spherical and nonspherical sources.
- [ ] Determine G_N from an actual laboratory/Solar-System source-response
  or two-body experiment in the candidate, including environmental and
  scale dependence. Relate it to the bare EH coupling and G_cosm.
- [ ] Derive the high-acceleration GR branch, not only mu->1. Check residual
  auxiliary stress and local position dependence; verify spherical BTFR
  with the measured G_N and test nonspherical deviations from the target.

**Fail implication:** unequal physical potentials, wrong source normalization
or an observable extra force fails the corresponding target, even if MOND fits.

### G09 — Reduced perturbations, GW and strong coupling (`g09_modes.py`)

- [ ] Use the completed constraints to reduce scalar/vector/tensor quadratic
  actions on Minkowski, the galactic external-field branch and FLRW.
- [ ] Calculate kinetic and gradient matrices and dispersion relations,
  eigenvectors and pole residues for arbitrary wavevector orientations.
  Account for mixing and constraints before diagnosing a kinetic sign.
- [ ] Verify exactly two physical tensor polarizations, positive tensor
  kinetic energy, and their propagation speed relative to the photon metric.
  Derive c_T across the relevant backgrounds/frequencies, not just one point.
- [ ] Inspect auxiliary propagators and source-to-source exchange amplitudes
  for hidden poles. Count a pole absent only at omega=0 as unresolved.
- [ ] Derive cubic interactions, and quartic terms where cubic terms vanish;
  canonically normalize and estimate the strong-coupling scale relative to
  every wavelength/frequency at which the theory is being used.
- [ ] Test perturbative stability beyond isolated sample points; characterize
  the allowed parameter domain and its boundary. Check EFT cutoff validity
  for xi*k values used in screening, rather than extrapolating a truncation.

**Fail implication:** ghost, uncontrolled strong coupling, gradient pathology
or prohibited propagator on the required branch is a failure, not a tuning hint.

### G10 — Full PPN and finite-scale observations (`g10_ppn.py`)

- [ ] Set a consistent PN counting and coordinate gauge. Solve g00 through
  O(c^-4), g0i through O(c^-3), gij through O(c^-2), with matter pressure,
  internal energy, velocities and preferred-frame velocity retained.
- [ ] Match the complete independent PPN potential basis. Derive beta,
  gamma, alpha1, alpha2 and alpha3; test other nonzero PPN coefficients too.
  Static Phi=Psi does not determine nonlinear beta or preferred-frame terms.
- [ ] Calculate boosted finite-source solutions and match near/far regions.
  If operators introduce length-dependent response, derive real-space
  observables; a coefficient alpha1(k) is not automatically a constant PPN alpha1.
- [ ] Compute Shapiro delay, bending, perihelion/node precession, lunar and
  preferred-frame effects with measured G_N. Compare current primary-source
  likelihoods and their assumptions; do not equate k=1/AU with an ephemeris fit.
- [ ] Check extended self-gravitating bodies: sensitivities, strong-equivalence
  violations, scalar/vector radiation and binary-pulsar losses when relevant.

**Fail implication:** absent static 1/r terms or suppressed scalar amplitudes
do not by themselves clear this gate; cancellations need full metric evidence.

### G11 — Causality and controlled singular limits (`g11_initial_value.py`)

- [ ] Specify a well-posed initial-boundary problem, characteristic structure
  and constraint propagation. Separate gauge ellipticity from measurable
  instantaneous influence by computing response between physical sources.
- [ ] Compare causal cones/front propagation with the physical light cone;
  address superluminal channels and radiation/Cherenkov implications within
  the EFT's actual validity range, not its extrapolated UV polynomial.
- [ ] For a nonlocal kernel, define the inverse and boundary/time prescription.
  An ordinary single-history action does not become retarded merely by
  replacing a symmetric inverse after variation; show the correct variational
  formulation and all additional data if such a prescription is used.
- [ ] Analyze the order of omega->0, k->0, y->0 and GR-limit operations;
  distinguish mathematical regulators from physical new couplings. Establish
  existence, uniqueness in the claimed class and continuous dependence where
  required, or explicitly restrict the prediction's domain.
- [ ] Treat zero-field saddles and smooth positive-density centers: weak
  solutions may exist despite loss of uniform ellipticity, but tidal
  observables, matching, constraint ranks and the perturbative cutoff still
  need a controlled limit. Do not elevate a finite grid to a universal proof.

**Fail implication:** an unacceptable physical instantaneous channel or an
uncontrolled limit blocks full closure even if every static plot looks healthy.

### G12 — Cosmological perturbations and observables (`g12_cosmology.py`)

- [ ] Derive gauge-invariant scalar/vector/tensor perturbation equations on
  the surviving FLRW branch with the same matter content and parameter set.
- [ ] Calculate growing/decaying modes, effective gravitational coupling,
  slip, Jeans/sound horizons, lensing and ISW response; verify the k->0
  treatment agrees with G06/G07 and does not invent a missing global mode.
- [ ] Implement the derived system in a verified Boltzmann/structure pipeline,
  reproducing its GR limit first. Compare expansion, BBN, CMB, BAO, growth,
  weak lensing and cluster mass accounting with declared datasets and priors.
- [ ] If the dark/clock sector supplies matter-like density, count and evolve
  that density explicitly. Do not claim baryons-only cosmology while using
  an unreported conserved dark charge or extra fitted matter component.
- [ ] Only after constant-a0 viability, derive or test any a0(z)/dark-energy
  relation from the same equations; include its feedback into all local gates.

**Fail implication:** healthy local modes and an expanding background alone
are insufficient if the required cosmology fails.

### G13 — A genuinely discriminating prediction (`g13_prediction.py`)

- [ ] Derive at most two observables not used to choose the action or fix
  its parameters. Identify which are unique consequences and which are
  known MOND limits/dimensional restatements.
- [ ] For the sixth-power candidate, first establish that systems exist in
  its compact, isolated, small-epsilon regime. Use the full curve outside
  the asymptotic domain, with finite-source and external-field corrections.
- [ ] Compare against rival kernels and ordinary gravity using the same
  observational forward model, masses, distances, inclinations, selection,
  uncertainties and nuisance priors. Split training/held-out systems by
  object, not by correlated radial points from one galaxy.
- [ ] Predeclare the estimator, thresholds, exclusions and failure rule;
  preserve existing preregistrations. Publish adverse residuals and sensitivity
  to modelling choices. A fit score alone is not evidence for relativistic closure.
- [ ] Search primary literature and citation chains for the precise action,
  equation and prediction; distinguish new derivation, formal corollary and
  independently new empirical content. Record search limits, not a priority claim.

**Success here:** an independently testable, supported prediction with honest
attribution. Calling it “Kepler-grade” still requires exceptional empirical
reach and durability, not an impressive exponent or a passing script.

### G14 — Closure package or restricted no-go (`g14_certificate.py`)

- [ ] Freeze one action hash, parameter domain and boundary/initial-data
  prescription. Every gate must point to that same object or an explicitly
  derived limit with a justified overlap domain.
- [ ] Produce an obligation matrix for every requirement in section 2,
  with a derivation, executable test, external source and error/scope statement.
  Compute the conjunction of gates from their actual results; missing gates
  are OPEN and cannot be represented by prefilled constants.
- [ ] Have an independent reviewer reproduce the central calculations and
  attempt counterexamples at rank-changing and observational boundaries.
- [ ] If a gate fails, prove the narrowest obstruction: quantified action
  class, regularity, locality/nonlocality, coupling, boundary conditions and
  exceptional modes. An excluded ansatz is not “no relativistic MOND.”
- [ ] If proposing a genuine new no-go, close each logical implication
  analytically or with an appropriate certified computation, check known
  counterexamples and audit novelty separately from correctness.

**Final labels:** DEAD for the specified falsified candidate/assumption class;
OPEN for missing calculations or unresolved validity; ACTUALLY CLOSED only
for one explicit action meeting all stated requirements in its declared domain.
No roadmap can promise that an ACTUALLY CLOSED candidate exists.

## 7. Efficiency and reproducibility contract

- Work on the first unpassed dependency, not whichever calculation produces
  the prettiest formula. Spend large symbolic/PDE budgets only to resolve a
  named alternative or uncertainty that can change the next decision.
- Each gate gets a short written mathematical contract and a test capable
  of failing under a relevant mutation: omitted adjoint/metric variation,
  wrong inverse kernel, sign/normalization error, dropped zero mode or rank.
- Save exact constraints/matrices before reducing them to ranks. Record
  dimensions, precision, singular values and rank tolerances; never hard-code
  expected determinants, PPN values or DOF counts into the producer.
- Reuse authenticated expressions and independent benchmarks. A cache key
  must include action hash, background, operator definition and conventions.
  Do not reuse an untracked pickle just because its filename looks familiar.
- Run every new script. Record exact command, environment, source/output
  hashes, elapsed time, seed, tested range and exit code. Separate mathematical
  failure, code defect, timeout and inconclusive numerical error.
- Keep boundary data and global modes explicit. A source-dependent boundary
  adjustment made solely to restore PASS is a change of model.
- Commit a small reviewed gate at a time. Preserve unrelated concurrent
  changes and all failures. Stage only reviewed files, inspect the resulting
  commit and all outgoing commits, then push the intended branch; never
  force-push over another worker or rewrite their work to make a clean tree.

## 8. Existing commands and sources

These are actual existing regression commands, not proposed executables:

```bash
python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/smoothed_onset_action_2026 -v
python3 qwen_claude_field_theory/closure_2026/elliptic_phantom_action_gate_2026/test_elliptic_phantom_action_gate_2026.py
python3 -m unittest discover -s hunt_2026/exact_mu_cassini_2026 -q
```

They cover 10 + 2 + 6 tests in the preceding verified study, not the unrun
roadmap gates. The first command regenerates the onset manifest/results;
do not accidentally stage provenance-only regeneration into another change.
The full AQUAL Solar gate intentionally retains a nonzero exit until its
strict numerical requirement is actually resolved.

Primary references inspected or identified for workers, checked 2026-09-04:

- [Milgrom, QUMOND, arXiv:0911.5464v2](https://arxiv.org/pdf/0911.5464v2),
  equations (3)-(6): the known two-potential action and its field equations.
- [Will, arXiv:1403.7377v1](https://arxiv.org/abs/1403.7377v1): starting
  reference for the PPN dictionary; verify its full definitions before
  matching and obtain current experimental bounds separately.
- [GW170817/GRB170817A, arXiv:1710.05834v2](https://arxiv.org/abs/1710.05834v2):
  primary multimessenger speed comparison; do not substitute it for a
  candidate's propagation derivation or ignore emission-time assumptions.
- [Park et al., arXiv:2602.17884v1](https://arxiv.org/html/2602.17884v1):
  Cassini likelihood/conventions already used in the repository; recalculate
  the model observable and uncertainty instead of copying a scalar ceiling.

The source pointers support established formalism or observational inputs,
not novelty or survival of this candidate. No numerical theory gate was
newly executed merely by writing this roadmap.

## 9. Roadmap validation, not theory certification

The current task inspected git status, recent commits, the listed source
files/reports and the remote main reference. An independent read-only review
checked coverage, the Fourier benchmark and the strict/extension distinction.
The manuscript was self-reviewed for dimensions, signs, notation, dependency
order and exact-versus-approximate claims. `git diff --check` returned 0.
No existing theory implementation or preregistration was modified.

Two algebraic identities in the proposed external-field benchmark were
checked with SymPy (exit 0) using the following reproducible command:

```bash
python3 -c 'import sympy as s; y=s.symbols("y",positive=True); mu=1-s.exp(-y); x=y*mu; lam=s.diff(x,y); nu=y/x; dnuds=s.diff(nu,y)/lam; longitudinal=s.simplify(nu-1+x*dnuds); assert s.simplify(longitudinal-(1/lam-1))==0; k,xi=s.symbols("k xi",real=True); assert s.simplify(s.exp(-xi**2*k**2/2)**2-s.exp(-xi**2*k**2))==0; print("Two exact benchmark identities verified; no full external-field solve performed.")'
```

This is not execution of G02, a new data analysis, or verification of a
covariant action. All fifteen roadmap gates remain future obligations or
require their existing evidence to be audited against the frozen action.
