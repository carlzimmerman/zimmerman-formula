# MS1 result: coupled matter is the missing stability test

**Conditional result established by the written derivation and bounded checks:**
the accepted positive-energy scalar sector develops an attractive growing
mode when responsive barotropic matter is included in the specified
supported, mean-subtracted constant-background problem. This is a
potential-energy instability, not a negative-kinetic-energy ghost or a
high-frequency ill-posedness for cs²>0.

For directional constitutive eigenvalue L>0 and vphi²=c² L/K, the exact
longitudinal dispersion is

    (omega²−cs² k²)(omega²−vphi² k²)
       −4 pi G rho0 c² k²/K = 0.

There is one growing branch precisely when

    0<k²<kJ²=4 pi G rho0/(cs² L).

The threshold cannot constrain K. Rates can. Within this homogeneous model,

    k_peak/kJ = sqrt(cs vphi)/(cs+vphi),
    gamma_max = sqrt(4 pi G rho0/L)/(1+cs/vphi).

These formulas exhibit a finite, K-sensitive maximum growth rate. At fixed k
inside the unstable band, increasing K decreases growth. At high k both
branches have real limiting propagation speeds cs and vphi. The pressureless
boundary case has bounded high-k growth, whereas a deliberately negative cs²
control has unbounded growth proportional to k. These are distinct failure
mechanisms.

The raw proof, exact energy signs, full branch solutions, assumptions and
K-inversion formulas are in `DERIVATION.md`. This is a newly derived lane
result awaiting independent coordinator review; the numerical program does
not replace that review.

## Background restriction is essential

Uniform nonzero density and constant nonzero scalar gradient do not solve
the original unsupplemented static field-plus-fluid equations. The exact
calculation explicitly subtracts rho0 from the scalar source and supports
the fluid with a fixed acceleration cancelling the background force. The
affine field plus periodic zero-mean perturbations is an exact equilibrium
of that modified problem. It is not presented as an isolated galaxy,
cluster or cosmological background.

A stronger new restriction follows in a genuine isothermal hydrostatic slab:
its equilibrium equations imply kJ² Lrho Lg=1 exactly. Consequently every
nominally unstable k<kJ has k min(Lrho,Lg)<1. Such a slab has no simultaneously
slowly varying density-and-field local unstable window. This does not settle
its global stability; it requires solving the finite-domain coupled modes.
Four positive-gradient equilibrium samples are provided as inputs for that
next calculation, without claiming their perturbation spectra.

Applying the dispersion locally to a genuinely balanced inhomogeneous source
requires controlled wavelength, background-gradient, tidal and timescale
separation. There is no guarantee that the unstable band fits inside such a
patch. An accelerated-frame symmetry is not assumed for the preferred-frame
action. This caveat prevents a field-only stability claim from being replaced
by an equally unsupported universal collapse claim.

## Computation and decisive controls

Accepted evidence: `run_003/results.json` and `run_003/manifest.json`.
The standalone script imports no parent implementation and runs:

* 672 Q/R cases across B/a in {1e-4,.01,1,100}, three propagation angles,
  K in {2,8}, cs in {.001,.2} (c=1), and seven k/kJ values from .01 to 100.
  The analytic two-branch roots are compared to eigenvalues of the four
  first-order density/velocity/potential/field-velocity equations.
* 96 independent bounded one-dimensional maximizations of growth, checked
  against the exact peak location and maximum.
* Eight direct ODE evolutions covering Q/R, K=2/8, growing k/kJ=.5 and
  stable k/kJ=2. The density trajectory is checked against the derived modal
  cosh/cos evolution; the coupled quadratic energy is checked independently.
* Pressureless, negative-compressibility and coincident-principal-speed
  controls, plus monotonic suppression of growth with increasing K.
* Four genuine hydrostatic slab backgrounds, with independent first-integral
  quadrature and the exact background-length identity checked on 401 points each.
* Eight synthetic dimensional cases carrying both registered a normalizations,
  Q/R and vacuum versus a frozen E(3) scale comparison separately.

All checks passed. The largest scaled companion-eigenvalue error is
3.67e-15, the largest direct-trajectory error is 3.00e-15, and the largest
scaled energy drift is 2.21e-16. These are finite binary64 residuals under
the declared scaling, not certified error bounds. The companion comparison
is normalized by the largest branch scale, while the direct evolutions
separately test the slow/growing branch in the stated representative cases.

For an explicit falsification of the field-only stability proxy, take
Q, B/a=.1, parallel propagation, cs=.2, c=1, 4 pi G rho0=1,
K=2 and k=.5kJ. The field-only omega² is +3.125, whereas the coupled lower
branch is −0.9388585833. Direct responsive-fluid evolution grows accordingly.
With K=8 the same threshold persists, but the coupled lower branch becomes
−0.5834047632. Freezing matter therefore misses an actual negative direction
of the declared coupled model.

## Dynamic identifiability is not a measurement

Given calibrated L, cs and k, measuring both branches determines K from their
frequency-squared sum. A single branch additionally requires rho0. Static
equilibrium, a static response and the instability threshold carry no K.
The derived formulas specify observations that could constrain K; no such
dynamic dataset is fitted here.

The dimensional examples use deliberately chosen rho0=1e-21 kg/m³,
cs=100 km/s and B0=1e-12 m/s², with no source association. At k=.5kJ,
changing K from 2 to 8 changes the synthetic growth rate by only 6.56e-6
to 1.59e-5 fractionally across the eight cases. The slow mode is almost
quasistatic despite the scalar propagation speed halving. This demonstrates
conditioning: a dynamic rate can formally identify K yet be a very weak
practical constraint when nuisance maps and fluid properties are uncertain.
The frozen H-scale comparison contains no expansion or scale-field equation.

## Provenance and preserved history

Frozen Git base is `eccd1c0e59459b5ec1acf2e916fb7a05a7f67971`; the shared
checkout is dirty and campaign evidence is identified by file hashes.
`read_files_sha256.json` records the actual original sources read. The live
AUTORESEARCH view was copied at dispatch so future coordinator updates do not
invalidate a historical computation input. The accepted version-2 manifest
pins code, derivation, contracts and parent inputs before and after execution,
and records software, limits, runtime, commands and output hashes.

There were no failed computational checks in this lane. `run_001` succeeded
before the exact maximum-growth result was added; `run_002` also succeeded
before the balanced-slab obstruction was added. Their original scripts,
derivations and contracts are retained as `accepted_run001_*` and
`accepted_run002_*`. `run_003` is the current accepted evidence. Earlier run
input hashes can be matched to archived versions; they must not be mistaken
for hashes of current files. The accepted run_003 manifest validates against
current inputs and outputs.
All writes are confined to `stage_04/matter_stability/`; no parent artifact
was edited and no commit was made.

Final self-review checked the Fourier signs, pressure/scalar coupling,
kinetic versus potential signs, equality cases, dimensions, the noncommuting
limits, root cancellation, Q/R distinction and physical-scope language.
The mathematical proof and its physical background assumptions remain
separate from the finite checks.

## First remaining implication and executable follow-up

Independently audit the recorded balanced finite slabs and solve their coupled
perturbations with explicit boundaries. That must decide whether a physical
finite-domain unstable mode exists; the exact slab identity already rules out
the naive locally homogeneous unstable-window interpretation in this class. The exact next equations, finite input ranges and
decisive controls are in `FOLLOWUP_TASKS.md`, prepared for the coordinator's
small-model queue. This lane does not dispatch those tasks or edit the queue.
