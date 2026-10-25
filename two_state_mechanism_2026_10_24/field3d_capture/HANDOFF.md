# FIELD3D-CAPTURE-2026-10-24 checkpoint

User asked to replace the spherical-average tether field with full 3D, resolve
local capture, conserve energy, and test disk T formation with dwarf/cluster F
retention without type switches. Implemented a conservative quasistatic 3D
longitudinal field and fixed physical encounter support. Literal spatial locality
and temporal subdivision are implemented; continuum local-density resolution and
a selective physical mechanism remain OPEN. Do not claim the full research goal
is achieved.

Final sources: field_exact_self.py (inherits Gaussian primitives from field.py),
simulate.py, run_exact_self.py. Field3D without exact self subtraction is the
historical initial evaluator. It is full 3D too, but has avoidable single-packet
mesh self-force. Preserve its runs as numerical history.

The full vector field is curl-free Coulomb u of Gaussian T density. Energy is
integral [-log(1-|u|/a0)-|u|/a0]. This is NOT a minimizer over arbitrary vector
fields constrained only by divergence. Keep that distinction in any continuation.
Analytic all-space quadratic and isolated nonlinear self terms; finite Cartesian
quadrature only for nonlinear interference; analytic gradients. Finite-box and
mesh symmetry errors are measured, not projected away. Multi-source saturation
is sampled, not rigorously certified between nodes.

Universal illustrative capture support0.1kpc, normal-flux coefficient1cm²/g in
units, radiative restitution .3, local baryon cooling restitution .5. The old
expanding-neighbor circulation barrier is removed. Capture means F->T state
conversion, not a derived permanent molecular bond. The incoming-normal flux
normalization is not directly an empirical total scattering cross section.

Final evidence: 30 completed formation trajectories (2 initial dynamical times,
seed11, N64 or128), two completed initially seeded-T transport controls, and
invariant checks. Formation suites scan_exact16, refinement_exact8,
interval_exact4, encounter_exact2. Do not pool original quadrature runs with them.
All jobs ended; all 12 manifest records validated against current inputs. Analysis
stderr is only font-cache construction. No unresolved tool process or pending job.

Final result: max global T1.5625%; bound free98.4375–100%; 11 attempts,4 captures
across final formation runs. Largest normalized energy drift7.17923e-6. Best RAR
RMS0.186814dex; best max residual0.629352dex. No joint target success. One rotating
round large input has1/64 T; a rotating flattened N128 input has1/128 T. Inner
fractions50% and25% mean one packet out of two/four, not resolved dominance.
Step-refined counts differ; one seed and few events cannot establish selective
formation or statistical convergence.

Local support samples are mostly empty. A smooth initial-density estimate gives
N>=~5.75e12 for32 expected central neighbors in the cluster-size case, illustrating
why brute-force packet doubling is not the way to resolve this collision term.
This estimate is not a rigorous probability bound for stratified radial shells,
not a condition for a single binary collision, and not a late-time density bound.
Temporal encounter resolution does not imply local-density resolution.

Next meaningful routes: adaptive continuum/kinetic collision representation;
statistically controlled rare-event treatment; field/packet smoothing convergence;
and a physically motivated durable binding/transition interaction with reciprocal
energy and angular-momentum transfer. The isotropic local binary law has no direct
sensitivity to circulation coherence at fixed local isotropic velocity statistics.
Additional couplings require derivation, not a galaxy-type switch. Solving the
unconstrained nonlinear polarization PDE is a separate untested closure choice.

No commits, manuscript edits, external publishing, or observational fit. The
report, derivation and audit calibrate every claim. Current research outcome is
numerical prototype + failed finite formation target + unresolved continuum
sampling, not a universal no-go theorem or validation of the Zenodo paper.
