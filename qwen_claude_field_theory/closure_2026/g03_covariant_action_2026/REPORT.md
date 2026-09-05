# G03: explicit action started; causal feasibility remains OPEN

2026-09-04. Work began at HEAD `4362cc405`; a concurrent attribution-only
commit advanced HEAD to `7a4413989`. All files produced by this task are
inside this study directory. Existing dirty work, Fable's files, original
outputs and manifests were preserved. No commit, push or publication was
performed.

**Primary mathematical verdict: incomplete, with the smallest missing
implication being the full constrained physical response of the specified
clock/metric action. G03 OPEN.** The static algebra and finite variation
checks pass in their stated domains. A healthy relativistic completion,
the original T-A target, and a universal obstruction are not established.

## What was constructed

`ACTION.md` defines one action C-H, including its metric, dynamical clock,
auxiliary scalar, auxiliary heat coordinate, both multiplier fields,
cosmological constant, minimally coupled matter and temporal boundary
terms. It fixes the leaf topology and heat-kernel domain. It is a classical
fundamental trial action, with no hidden cutoff or derivative expansion.
Its gravitational modification is

    2|D U-a|^2 + 2 alpha^2 q(|D W_b|^2/alpha^2)
    + integral_0^(xi^2/2) dz L(partial_z W-Delta_h W)
    + lambda_0(W_0-U),     alpha=a0/c^2.

The Einstein-Hilbert term is also retained. U and ln N are independently
varied covariant quantities, not assigned metric potentials. Their weak
static reduction derives u=c^2 U as the Newtonian potential and
Phi=c^2 ln N as the minimally coupled physical potential. Eliminating the
independent spatial metric potential at the leading weak order gives
exactly the T-B static functional with its two filters. The matching domain
is flat periodic zero-mean perturbations, with an appropriate subtracted
homogeneous background. The R^3 isolated infrared limit has not been
proved. Phi=Psi beyond the leading static order remains unproved.

This construction does not introduce an unspecified S_aux. W_0=U,
W_b=S U, the terminal multiplier equation and the weighted adjoint are
derived explicitly. In the full action the adjoint is N^-1 S N for
measure N sqrt(h); only the leading flat static equation uses S*=S.
The heat coordinate is not physical time. Eliminating its endpoint data
does not establish the physical mode count of the clock/metric system.

## Corrections to the reviewed handoff

1. **The f31c result is host-specific.** Scaling the full coupled Y
   quadratic sector gives a reference drag suppression. The Hessian-squared
   and trace operators fail the desired suppression. This does not prove
   that every covariant T-B completion must implement that reference
   replacement. f31c constructs its reference through a quadratic
   replacement; it is not an action-derived new covariant operator. Its
   large-XI2 table still has a nonzero alpha1 contribution (-0.80036 in
   one reference row), so suppressed drag is not alpha1=0. No f31c PPN
   number has been imported into C-H. The script/output were inspected;
   the 209-second pipeline was not rerun.
2. **G02b is a bounded nonlinear-machinery cross-check of a linear
   identity.** Its per-background ratios agree with the identity within
   about 1.43% canonical and 0.58% alternate. Pooling backgrounds would
   be wrong. It does not prove an exact nonlinear identity, and the
   spherical-host physical-to-Newtonian conversion remains an input.
   The division-free identity is (15A+5B)Q2+2BD=0. No ratio is asserted
   at D=0.
3. **The G00 contract misidentifies a kernel comparison.** The 0.073 dex
   value in f21 compares T-R/nu_RAR to T-Q/nu_muexp. It is not a
   T-A-versus-T-Q spherical difference: those share the exact spherical
   algebraic law. Also, T-B tends to T-Q at xi=0 for general sources;
   only the additional equivalence to T-A is spherical.
4. **Some G02 PASS labels exceed what their checks implement.** B3
   evaluates an explicitly assigned sigma-squared formula; B4 subtracts
   an identical constant vector from itself. They are algebraic sanity
   checks, not independent demonstrations of solver behavior. The new
   action-variation tests independently detect the missing outer filter.
   S2 tests Helmholtz floor >= Gaussian floor; the alternate floors are
   equal, not strictly higher. Its description of a constant central
   Helmholtz sunward force does not follow from this double-filter check.
   Planetary g_r is the monopole, not the complete directional acceleration.
   G1 is a two-wavenumber transfer calculation, not a solved Galactic disk.
5. **G02b discards imported failures.** Its executed G02 prefix creates
   FAILS, then G02b resets its own FAILS. A G02b rc=0 alone cannot
   authenticate the imported checks. Both programs were therefore run
   separately, with their real return codes.

These corrections are recorded here rather than editing shared handoff
documents during concurrent work. G02's observational ceilings remain
inherited conditional inputs, not a newly authenticated ephemeris fit.
G02's small-xi Gaussian NaNs remain unresolved; its nonempty surviving
window does not depend on labeling those unresolved points successful.

## Reproduction and executable evidence

`reproduce_handoff.py` copies the unchanged producer scripts into a private
snapshot before executing them because G02 writes its manifest next to
its source. It also runs the ten parent-action tests in a private fixture,
including their CLI output check. All original source/output/manifest
hashes remained unchanged.

| Command, from repository root | Actual result |
|---|---|
| `python3 qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/reproduce_handoff.py` | G02 rc=0, 53.1 s; G02b rc=0, 11.0 s; initial parent fixture packaging failure, rc=1 |
| same command with `--parent-only`, first repair | rc=1; a second fixture path dependency was missing |
| same command with `--parent-only`, final repair | rc=0; parent 10/10 in 2.8 s, originals unchanged |
| `python3 qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/g03_action_gate.py` | 13/13 finite/symbolic checks; rc=0; G03 explicitly OPEN |
| same command with `--require-closed-g03` | Actual rc=2, with 13/13 checks passing and outstanding obligations retained; this is a gate status, not a numerical test failure |

The two parent failures were environmental packaging errors, first the
missing copied CONTRACT.md and then the original producer's relative
f29/f30 provenance paths. The final private fixture preserves the producer's
layout and copies those read-only dependencies. No physics, tolerance or
pre-existing script was changed. Both failed logs and nested run histories
are retained. The final wrapper can now reproduce all three suites in one
call; the already successful G02/G02b runs were not repeated for the
parent-only packaging repair.

G02 again found Gaussian tabulated floors 0.02 pc canonical / 0.03 pc
alternate, and Helmholtz 0.03 pc in both. These are conditional surviving
grid points of the inherited checks, not continuum confidence boundaries.
G02b returned canonical Q2/D about 1.0931 versus analytical 1.1089 and
alternate about 0.6137 versus 0.6102. The dimensionless y values differ:
2.47812944 canonical and 2.05691994 alternate, for the stated spherical
host input g_obs=2.32e-10 m s^-2.

The new diagnostics use exact SymPy algebra and deterministic float64
finite-volume rings of 9, 15 and 23 vertices with nonconstant intrinsic
metric and lapse. The rings are distinct curved-leaf surrogates, not a
3D continuum mesh-convergence sequence. A central difference step 2e-5
is compared to independent action derivatives and a matrix-exponential
Frechet derivative. Numerical tolerances are checks, not interval proofs.

- Nonlinear U first-variation errors are <=5.60e-11; removing the outer
  filter produces errors 0.0262–0.0783 in the same test directions.
- Full metric-variation errors are <=3.63e-11; freezing the heat operator
  produces errors 0.0207–0.0327.
- The weighted adjoint and diffusion endpoint transport are verified on
  nonconstant lapse and metric. The tests also verify DC gain and the
  intrinsic Laplacian's weighted symmetry.
- Symbolic checks establish the inverse primitive, leading static
  reduction, unsmoothed source coefficient and FLRW extrinsic-curvature
  correction to a projected Hessian.
- The central division-free identity is checked separately at both a0
  backgrounds. This does not replace the G02b finite result.

## The early obstruction and remaining causal question

A direct attempt to drive an unconstrained wave with S rho has a strictly
positive retarded Green function outside the metric light cone. The exact
convolution and an explicit spacelike evaluation are in ACTION.md and the
code. **That scalar-wave realization FAILS.** It is not a theorem against
all covariant or constrained completions of a static spatial filter.

C-H instead puts the heat filter into a varied foliation/constraint
sector. Its inexpensive scalar ADM principal-block calculation exposes
another specific issue: after conserved sources are included, the
advertised static lapse depends on an undetermined spatial function F(k).
The shift constraint alone ties the changing spatial metric potential to
the ordinary source, while the static modification can reside in F.
The full physical Bardeen potential must include the shift; its explicit
lapse dependence cancels in this truncated calculation. Thus treating
the lapse alone as an instantaneously measurable signal would be an
invalid acausality argument.

In the same frozen-background approximation the clock decoupling
coefficient 2C/(1+C) is positive transversely and negative longitudinally
at both inherited backgrounds: at k xi=0.4 its values are approximately
0.1448/-0.2076 canonical and 0.2221/-0.2258 alternate. These are flags
requiring the full coupled constraints. They are not physical ghost
eigenvalues. No rank, DOF integer, PPN coefficient or success label was
hard-coded as a result.

The spatial-filter wave counterexample justifies examining a constraint
realization rather than immediately adding a propagating filter field.
The resulting C-H action is the one explicit alternative pursued within
this gate. It has not yet demonstrated that its constraint realization
works. No additional speculative action family is offered here.

## Obligation matrix and next calculation

| Obligation | Status and dependency |
|---|---|
| Explicit action, fields, units, signs, heat and cap conditions | Defined on closed-leaf domain in ACTION.md |
| Leading weak static T-B functional | Symbolically and finitely checked; periodic zero-mean domain |
| Outer adjoint, metric-dependent filter variation | Finite checks pass; full spacetime equations not completed |
| Genuine clock rather than fixed background structure | Varied normalized scalar specified; its complete equation remains to be reduced |
| Physical causality | OPEN; naive scalar-wave realization fails, full constrained C-H channel unresolved |
| Allowed initial data and extra physical modes | OPEN; F(k) diagnostic identifies the issue rather than hiding it |
| k=0, y=0, C=0 and isolated infrared limit | Defined where possible at action level; branch analysis OPEN |
| Phi=Psi, Ward identity, tensors, PPN, FLRW, observations | Leading static slip and matter identity described; full common-action gates unproved |
| Strict T-A closure | Ineligible: this is T-B |

The smallest next calculation is to vary C-H fully and obtain its
constrained retarded curvature response on an actual nonzero external
background, retaining heat-kernel stress, clock variation and source
conservation. It must decide whether F(k) is constrained, physical frozen
data, or an inconsistent static branch, and whether R_0i0j has spacelike
response. This precedes a large Dirac count or PPN calculation. A
verified obstruction on that full channel would stop this candidate;
the present truncated evidence cannot do so by itself.

## Literature and scope of attribution

Milgrom, *Generalizations of quasilinear MOND (QUMOND)*,
[arXiv:2305.01589v2](https://arxiv.org/html/2305.01589v2), revised
4 October 2023, section II.B (HTML II.2), equation (6), was checked on
2026-09-04. It explicitly allows nonlocal functionals of the Newtonian
potential in a generalized QUMOND action. Its psi is our u, phi is our
Phi, and the present static specialization has
P[u]=|grad u|^2/a0^2+q(|grad S u|^2/a0^2). The action architecture is
therefore known after notation translation. This source does not
establish a healthy covariant clock/heat completion or the present causal
diagnostics. No novelty claim is made for them.

An exact-ID local cache lookup found no configured cache. The versioned
primary source was read in the web reader; no source was retained and
no root cache or ignore rule was created across the scope fence.

## Files and interpretation

Authored files: ACTION.md, REPORT.md, g03_action_gate.py and
reproduce_handoff.py. Generated outputs: results.json,
computation_manifest.json, handoff_reproduction.json, and the private
handoff_reproduction/ snapshots, raw logs and parent CLI artifacts.
The manifest records exact source hashes, versions, current commit, dirty
state, arithmetic conventions, bounds, output hash and actual exit code.
Its file_inventory.json lists every study artifact with its content hash
(excluding the inventory and manifest themselves to avoid circular hashes).
The Mathbox manifest validator returned rc=0. Both authored Python files
compiled in memory; an earlier bytecode-cache check hit the machine's
out-of-scope default cache path and was replaced by this no-write check.
The closure-folder diff whitespace check returned rc=0.

Mathbox computation audit guided the finite contracts and provenance;
proof audit restricted the two obstruction claims to their actual
assumptions; literature check corrected attribution. A conservative
mathematical self-review covers the two new documents and the displayed
code equations, not unrelated repository prose. Full G03 remains OPEN.
