# Radiation persists, but the joint galaxy-formation test still fails

The original objective remains OPEN. Starting from the accepted unseeded state,
we now evolve the full backreacting system to **12.8825 Myr**, find radiation
beyond the first pulse, and demonstrate a local restoring response of the moving
boundary. Inward transport occurs, but repairs only **0.03356%** of the initial
50-kpc mass deficit. Galaxy-law error is still **17.36125%**. A populated density
trough develops. These are partial results, not a successful formation mechanism.

All new work is in this directory; prior manifested inputs remain unchanged.
No modes, cooling force, target-density force or material boundary were supplied.
The original initial state has chi=pi=carrier_p=0. Continuations load every
accepted field and momentum, rather than resetting or replacing them.

## Joint measurements at the final accepted state

| Test | Result at 12.8825 Myr | What it establishes |
|---|---:|---|
| Galaxy law | 17.361245% error; initially 17.368389% | Fails the <1% target |
| Inward mass gain inside 50 kpc | 0.000287785 Mb | Only 0.03356% of the initial deficit repaired |
| Initial missing mass inside 50 kpc | 0.857611689 Mb | Conversion-front relabeling cannot replace this mass |
| Inward mass rate at 50 kpc | 4.46374e-5 Mb/Myr | Actual total-mass current, not boundary speed |
| Boundary | One crossing at 66.625975 kpc | Finite and moving |
| Local live restoring response | omega_probe^2=5.10170 /Myr^2 at ±0.01 kpc; 5.10341 at ±0.005 | Restoring acceleration for the specified mass/charge-preserving family |
| Transition population | Minimum density 0.0006842905 | Populated during tested interval |
| Density rebound | 1.182644; trough at 64.8125 kpc | Monotonic profile lost; no strong gap-free formation claim |
| Free outer reservoir, r>1.2R | T fraction 3.10063e-12 | No appreciable conversion in this finite window |
| Outgoing characteristic energy, r>500 kpc | 1.358068e-5 Eunit | Actual escaping radial modes |
| Net material-to-field work | 0.005098083 Eunit | Most transferred energy remains in the field |
| Outgoing / net field work | 0.266388% | Finite-time efficiency, not a universal rate |

Mb=6e10 solar masses and Eunit=3.2572137002e51 J. The 50-kpc requirement comes
from the inherited galaxy law and exact baryonic acceleration; the separate
energy-derived equilibrium used in transport projections is not a fitted law
profile. Moving and fixed outer-radius diagnostics are distinct. No long-time
reservoir, nonradial or cosmological-population conclusion follows.

The joined global energy defect is 1.8911e-10 Eunit and charge defect
-1.1420e-10. Numerical defects are reported, never assigned to radiation. All
accepted steps solve the complete coupled equations under residual, cap and
energy guards. The far absorber has not been reached. Full raw values and
accepted durations are in run_assessment/results.json.

## A continuing source, not just the original pulse

Outgoing packet energies in successive retarded two-Myr windows are:

| Retarded interval (Myr) | Outgoing energy (Eunit) |
|---|---:|
| 0--2 | 3.12534e-6 |
| 2--4 | 2.11549e-6 |
| 4--6 | 3.92430e-6 |
| 6--8 | 6.08102e-7 |
| 8--10 | 3.60669e-6 |

Thus radiation persists well beyond the initial packet. This does not establish
steady emission on a redistribution timescale or an asymptotic cooling rate.
These are characteristic energies in the source-free exterior, with reactive
energy separated, not total wave energy or uncorrected finite-radius flux.

The integrated source obeys Qm_dot=sum S_i, where
Qm=sum(g1 mTi+g2 mTi^2/Vi). In the compact radial limit, the outgoing waveform
is u=-Qm_dot/c^2 and power is Qm_ddot^2/c^3 in dimensionless units. The full
finite-source retarded integral predicts the final measured waveform to
**0.3085% relative L2 error**, without fitting its normalization. The earlier
5.7-Myr check gives 0.2261%. This directly ties the radiation to the actual
infall/conversion history with reciprocal work retained.

RADIATION_TRANSPORT_DERIVATION.md gives the source, conservation and retarded
force/work derivation. The fixed initial composition mismatch identified in the
previous phase is not reintroduced. Preparation losses remain excluded.

## What prevents the observed radiation from repairing the outer deficit

The complete current-acceleration budget at 50 kpc shows a nearly cancelling
force balance. At 9.765 Myr, gravity contributes +4.80787e-5 Mb/Myr^2 and
response -4.46028e-5: about 92.77% cancellation. Scalar-phase backreaction is
-2.30270e-8, only about 0.66% of the remaining net acceleration. Strong scalar
drag is therefore not what holds this particular outer current small.

The emitting source is concentrated in the core: 97.9% of its absolute weight
lies inside 10 kpc at 9.765 Myr, while the dominant law deficit is near 50 kpc.
An exact frozen-profile linear audit makes the mismatch quantitative. In the
positive common-transport kinetic metric, only 0.057321% of the transport tangent
toward the energy-derived equilibrium lies in the leading monopole's bright
direction. That bright component carries just 0.003586% of the required inward
50-kpc current. The source functional agrees with an independent phase
perturbation to 5.03e-13 relative error.

This is NOT a radiation-efficiency bound, a statement that 99.94% of matter can
never radiate, or a no-go theorem. Initially dark transport can mix into emitting
modes through the Hamiltonian. That spatial/compositional transfer remains the
unresolved dependency. Simple finite-size retardation does not repair the direct
projection in the tested family: the bright fraction decreases across the
sampled 0--1000-rad/Myr range. TRANSPORT_COUPLING.md derives the operator and
states every restriction; nine cutoff/floor checks test tail sensitivity.

## Moving-boundary restoration with density free

At 5.7 Myr, paired ±0.01-kpc composition/carrier perturbations preserve total
density in every initial cell and global shift charge, while leaving material
phases, chi and pi unchanged. All fields and densities are then released. The
probes return across the unperturbed moving boundary and overshoot during the
next 0.5 Myr. The final odd displacement is -0.524377 of its initial value;
with the time-step ceiling halved it is -0.524391. The largest difference of the
sampled normalized response curves is 0.3665% of the initial displacement.

Independent full-force directional derivatives verify restoring acceleration
at 5.7, 12.135 and 12.8825 Myr, under displacement and derivative-step refinement.
The final-state local response remains positive, as tabulated above. The finite
response experiment starts at 5.7 Myr; the later checks are instantaneous.
These results establish local restoration for this family, not asymptotic
stability, arbitrary-perturbation stability, or a fully formed galaxy. The probes
are response diagnostics, not parent populations used to drive formation.

## Numerical checks and tested limits

The first two new continuations use a 0.0025-Myr ceiling, reach 9.765 and
12.135 Myr and have zero rejected steps. Their wall-bounded partial status is
not a physical failure or a completed planned 20-Myr evolution. One-step
qualification of larger steps at 12.135 Myr succeeds, but longer guarded runs
shrink their steps again. They reach 12.8825 and 12.65 Myr; this is not a
production speedup or a uniform time-halving test. At their common endpoint,
law errors differ by 2.39e-8 percentage points and radii by 2.81e-6 kpc;
wave energies differ by 1.17e-7 Eunit. Fast phase convergence is not proved.

The independent continuous Hamiltonian field used for the force budget agrees
with energy directional differences to about 1e-8 relative. Mass-current
acceleration is independently checked at three derivative scales. The radial
source/characteristic calculation and all existing work/charge ledgers provide
separate checks on the emitting mechanism.

The 2-kpc exterior has a discrete scalar frequency ceiling of 306.60 rad/Myr.
It cannot certify escape of arbitrary roughly 500-rad/Myr carrier waves. Present
inner-annulus windowed content above 300 rad/Myr is about 6e-6, so this limitation
does not explain the measured slow radiation. A future fast-cascade claim must
refine the exterior. Neither a unique three-dimensional completion nor the
microscopic origin of g2 is supplied. The benchmark begins already mixed;
exact all-F birth is still a separate invariant-subspace problem.

See HANDOFF.md for the exact accepted state and unresolved next obligation,
ROUTES.md for route outcomes, PROOF_AUDIT.md for author self-review, and
MANIFEST_AUDIT.json for actual provenance validation. The joint objective is
not marked complete.
