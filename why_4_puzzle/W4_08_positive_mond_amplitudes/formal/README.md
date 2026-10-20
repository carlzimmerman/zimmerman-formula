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

All printed critical theorem axioms are exactly
`[propext, Classical.choice, Quot.sound]`. There are no proof admissions or
custom axioms in the successful modules. Their statements quantify
arbitrary ordered fields except the real scale/gap module. The stress
module represents r by r>=0 and r^2=1+d^2 and proves its uniqueness.
No irrational/transcendental gap theorem is silently assumed.

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
