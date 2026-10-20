# Lean checkpoint for the why-4 microscopic problem

2026-10-20. **The original goal remains open.** The kernel-checked results
below prove exact necessary obstructions and classical coefficient/cone
implications. They do not derive xi=1/4 from a healthy microscopic theory.
The frozen scope is committed as 63afb2ca2. The earlier W4-08 result and
registry checkpoints are 4131def0e and 58ae06c36.
The reviewed formal/physical checkpoint is f77a0cd8d; registry rows
K673-K678 record its separate stress, scale, vector, pressure, BMB and
formal scopes. None is a determinate normalization candidate.

## What Lean now verifies

| Module | Exact scope |
|---|---|
| [PairedBandStress.lean](PairedBandStress.lean) | Every positive paired band has rho/2<rho+p_parallel<rho. Nonempty finite positive sums plus arbitrary vacuum offsets and extra sectors with nonnegative directional null stress cannot form a vacuum. The required compensating null stress is more negative than half the total band energy. |
| [AmplitudeBridge.lean](AmplitudeBridge.lean) | The source-coefficient definitions imply xi=8Omega/(9R); for Omega=4P, xi=1/4 iff R=128P/9. Common factors cancel. A target match in the reduced band formula imposes u=(96P-1)/(96P+2). P is any positive ordered-field element, not an asserted selecting law. |
| [ScaleGap.lean](ScaleGap.lean) | The stated stationary scale/gap Hessian with positive energy requires a strict lower bound on running curvature when that Hessian is positive definite. A single-log positive-energy stationary point has negative radial curvature. The differentiated potential dictionary is explicit analytic input. |
| [GaugeCones.lean](GaugeCones.lean) | Exact discriminant/root bounds, the refined cone identity, and the fully substituted principal coefficients of the temporal-vector action put every existing root in (0,1]. The microscopic/PDE interpretation of the polynomial is an explicit input. |
| [CurrentEnergy.lean](current_interactions/CurrentEnergy.lean) | Exact Legendre identity with the full canonical charge, an empty neutral amplitude minimum, and a unique global minimum of the charged sextic energy. Current and Gauss dictionaries remain analytic inputs. |
| [FluxComparison.lean](current_interactions/FluxComparison.lean) | The compact flux trial's jet cancellation and quartic energy, plus the quartic-versus-cubic bound. Admissibility, integration and the physical variational infimum remain analytic inputs. |
| [ChiralFold.lean](protected_auxiliaries/ChiralFold.lean) | Exact auxiliary fold identities and all-root timelike bounds imply negative coefficients; nominal Taylor arithmetic is distinguished from a physical force ratio. Component dictionaries, mode interpretation and asymptotics remain analytic inputs. |
| [ClockTilt.lean](clock_flux/ClockTilt.lean) | Complete-square and frequency signs for a retained clock tilt; positive static stiffness and conditional fixed-clock amplitude arithmetic. Physical mode, force and vacuum dictionaries remain analytic inputs. |
| [GravitySelection.lean](gravity_constraints/GravitySelection.lean) | Conditional de Sitter lapse/shift and redshift-boundary algebra, positive reduced kinetic coefficient, amplitude deformation and tensor-plus-scalar force identities, an inferred-density target's PPN bound, and finite-k polynomial signs. Covariant/PDE, source, density and actual-pi dictionaries remain analytic inputs. |

The original four modules' printed critical theorem axioms are exactly
`[propext, Classical.choice, Quot.sound]`. There are no proof admissions or
custom axioms in the successful modules. Their statements quantify
arbitrary ordered fields except the real scale/gap module. The stress
module represents r by r>=0 and r^2=1+d^2 and proves its uniqueness.
No irrational/transcendental gap theorem is silently assumed.
The two new current modules add nine printed critical theorems, using
only subsets of those same standard axioms. Their evidence and controls
are checked separately in [current_interactions](current_interactions/README.md).
The [protected-auxiliary continuation](protected_auxiliaries/README.md)
adds six critical theorem prints and true/two false controls. That
checkpoint had seven partial modules using only standard axioms, not a complete
microscopic normalization proof.
The [clock/flux continuation](clock_flux/README.md) adds seven critical
theorem prints and true/two false controls, bringing the total to eight
partial modules. Earlier checkpoints retain their original scopes.
The [gravitational-constraint continuation](gravity_constraints/README.md)
adds fourteen critical theorem prints and true/three false controls,
bringing the total to nine partial modules. These are exact algebraic
results under displayed hypotheses, not a microscopic selector.

The rational control has A=L=1,d=3/4,r=5/4, giving rho=17/32 and
N=3/8. The normal control compiles. Reversing N makes the unchanged lower
bound false; a vacuum offset of 7 leaves N unchanged and cannot make it
zero. Both separate mutant files reduce to `False` and exit 1. Their
failures are expected tests, not proof modules to import.

The actual-Real.pi adapter [PiBridge.lean](PiBridge.lean) is **not yet
kernel verified**: importing its analysis dependency exceeds the current
1024 MiB process cap. Its failed runs are preserved. The generic P bridge
is verified; do not describe the unverified adapter as a completed build.
Even a passing adapter would supply an equivalence, not a physical selector.

## New physical progress

[MICROSCOPIC_CONTINUATION.md](MICROSCOPIC_CONTINUATION.md) derives a
preferred-frame temporal-vector completion of the constrained MOND
response. It avoids the scalar-regulator tachyon, has a nonnegative
constrained classical energy, and admits positive local quadratic energy
and submetric principal cones on positive-Y, A=0 backgrounds. A regular
spherical source has a unique positive decaying radial branch with the
MOND asymptotic force. These analytic statements were independently
reconstructed, but the full field-theory/PDE proof is not formalized here.

The same action still leaves

    R=8epsilon0/(9gamma b^3),  xi=4pi gamma b^3/epsilon0

free. Its zero-field constraint degenerates. A microscopic gauge-invariant
source/current sector, gravitating clock, regular protected quantum vacuum
and independent amplitude relation remain missing. A pressure integral or
positive classical Hamiltonian alone does not establish them.

[REGULAR_PRESSURE_PARENT.md](REGULAR_PRESSURE_PARENT.md) pushes this
further: a charged sextic scalar gives a regular classical pressure
sector and the derived vector relation mV^2=gamma Y/2. Its exact Gauss
law still requires a regular compensating current. A conditional BMB
large-N pressure coefficient fixes neither that current nor positive
same-state vacuum energy.

[NEUTRAL_CURRENT_TEST.md](NEUTRAL_CURRENT_TEST.md) tests two regular
oppositely charged condensates. Their exact dilute Gauss equation removes
the apparent branch; a regular finite-density neutral clock generically
retains quadratic infrared stiffness. A restricted variational argument
also excludes positive cubic energy from amplitude-only relaxation with
an affine gradient energy and gradient-independent charge constraints.
Derivative-current completions remain outside that result.
Its reviewed evidence is committed as 3a26d1eb9 and registered as K679.

The [regular-current continuation](current_interactions/RESULT.md) goes
beyond the amplitude-only restriction. A polynomial current interaction
changes the canonical charge but leaves the neutral vacuum empty; a
Jacobian current supplies charge under local neutrality but permits a
cheaper electric-flux trial for compact profiles. CS flux attachment and
the specified zero-flux axion model supply no three-dimensional MOND
normalization or positive vacuum relation. Boundary/topological sectors
and protected auxiliary completions remain open obligations.

The [protected-auxiliary test](protected_auxiliaries/RESULT.md) constructs
a supersymmetric chiral fold with calculated positive rigid vacuum energy
and a positive static cubic correction. Its small-timelike critical
branches disappear; every remaining real branch has a decoupled scalar
ghost. The response also retains quadratic infrared stiffness. Ordinary
Born-Infeld/FI calculates a displayed vacuum/nonlinearity relation, but
no MOND cubic; its diagnostic portal gives a quartic correction. The
minimal vector convexity and specified portal tests are explicitly
restricted. Generalized/multiple auxiliary sectors and a regular clock
remain constructive openings; none has supplied the missing selector.

[Clock projection and flux](clock_flux/RESULT.md) now produce actual
static MOND branches with Newtonian crossovers. The new chiral branch
also has positive rigid vacuum energy, with conditional R=4096/1125;
its simple dynamical unit-clock completion has a retained tilt tachyon.
A top-form's positive same-form vacuum flux instead cuts off its MOND
infrared law. Branch selection, full clock/metric constraints and an
independent gravitating normalization remain open.

[Physical gravitational constraints](gravity_constraints/RESULT.md)
resolve a loophole in the earlier fixed-metric clock test: pure BM at
lambda=1 on its actual de Sitter vacuum retains a positive-kinetic scalar
with no quadratic restoring force. This does not establish full health.
An explicit deformation preserves the vacuum and all homogeneous
quadratic constraints while changing the MOND cubic. The rational
prototype's finite-k instability also has a conditional weak-gravity
continuation, subject to a regular constraint reduction and validity
window. Its universal conformal matter coupling gives a free scalar
force fraction; forcing the inferred-density target would imply a local
unscreened gamma below 1/2. None of these constraints selects the target.

[Protected normalization](protected_normalization/RESULT.md) tests a
five-dimensional exact gauge prepotential, the actual de Sitter sphere
determinant with smooth source profiles and a universal disformal metric.
A real radial electric cubic has the wrong universal force sign and
critical-vacuum/UV problems; the tested quantum responses are analytic or
logarithmic; a gamma=1 metric leaves the physical scalar charge free.
These are analytic results, with cross-reviews and exact source pins.
No extra Lean module is claimed: the existing charged-energy theorem
already covers the radial Hamiltonian's algebra, and the physical selector
is still missing. The module count remains nine.

## Verification and reproduction

Installed pin: Lean 4.34.0-rc2, mathlib commit
85e3a25e006c35636f0e53b0e9296caca2685bc0. The existing library at
`fable_independent_2026/lean_2026` is read-only. No reserved KAPPA_LOGIC/p63
file was changed. No dependencies were downloaded and no broad lake build
was run. [verify.py](verify.py) uses one worker, 1024 MiB Lean memory,
30 seconds CPU and 45 seconds wall time for each module. Final runs take
about 1-5 seconds each.

Run from the repository root, choosing fresh evidence-directory names:

```sh
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py PairedBandStress.lean runs/local_stress
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py AmplitudeBridge.lean runs/local_amplitude
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py ScaleGap.lean runs/local_scale
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py GaugeCones.lean runs/local_cones
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py controls/Normal.lean runs/local_control
```

After the stress module, run controls/ReversedStress.lean and
controls/VacuumOffset.lean separately with fresh output names; both must
exit 1 with an unsolved `False` goal. Compiled objects stay in ignored
`build/`. Source/object stamps prevent stale local objects from being
used silently. Exact input/dependency hashes, commands, log hashes,
resources and results are in each run manifest.

See [REVIEW.md](REVIEW.md) for the scope audit, [SOURCES.md](SOURCES.md)
for external leaves, and [GOAL_STATUS.md](GOAL_STATUS.md) for the unchanged
completion requirements and the next physical implication.
