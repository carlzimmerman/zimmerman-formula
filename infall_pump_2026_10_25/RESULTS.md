# Infall generates radiation; the joint formation goal remains open

The component question has a positive answer: infall generates a genuine
outgoing radial pulse from initially zero scalar fields under the full
backreacting action. The pulse is weak and transient. The galaxy law has not
formed, and restoration of the moving nonlinear boundary is unestablished.
This is a synthetic radial benchmark, not new population validation against
observed galaxies.

## Causal mechanism and false-positive control

The positive covariant spatial energy, finite carrier, density-dependent
current and all density/scalar companion forces are retained. See
PUMP_DERIVATION.md, ORIGINAL_VARIABLES.md and QUIET_PUMP_DERIVATION.md.
The inherited g2=171.68027319658 is phenomenological; its microscopic origin
and a unique relativistic completion remain unresolved.

Simply dilating the species profiles leaves an internal chemical-potential
mismatch. At 2 Myr the full unprepared run exports net 500-kpc flux
2.07407e-5 Eunit. A conservative diagnostic with all material hopping removed
exports 2.20332e-5 despite having no mass transport. This falsifies the early
signal as a clean infall-pump demonstration. The diagnostic is not a proposed
physical model or a reason to remove gradients.

Preparing composition and carrier stationarity at the same displaced total
density gives h_s=mu(r)a_s with a common local mu. Initially real material and
chi=pi=p_alpha=0 have no relative-composition kick. Spatially varying mu still
drives infall. At the initial instant,

    a_dot = -i mu a / sigma,
    a_ddot = -mu^2 a / sigma^2 - [T_kin,mu]a / sigma^2,
    rho_ddot = div(rho grad(mu)).

The commutator supplies additive transport forcing. Infall changes density and
preferred composition; the finite carrier and relative phases respond, and
compression/conversion currents source the scalar with reciprocal material
forces. This does not assume a homogeneous oscillator populates itself from zero.
The quiet 2-Myr flux is only 2.09613e-10. A time-independent common support
U=-mu makes the same control stationary within tolerance. Physical infall has
U=0 and freely evolving density and boundary.

## Authoritative smooth, quiet run

run_smooth_prepare starts from a positive C4 smooth continuum density based on
the energy-derived equilibrium, conservatively dilates it, then prepares internal
composition/carrier stationarity. No target-law density is fitted. The preparation
energy decrease, 0.00215126 Eunit, is excluded from physical work and radiation.
This tests already mixed infall, not exact all-F classical birth.

run_smooth_infall evolves every material cell, phase, carrier, scalar and
momentum for 5.7 Myr. Material spacing is 0.125 kpc through 320 kpc; the scalar
exterior extends to 10 Mpc. Fixed 0.0025-Myr steps give 2280 accepted steps and
zero rejections. Eunit=3.2572137002e51 J.

| Joint diagnostic | Measured result | Interpretation |
|---|---:|---|
| Galaxy-law error | Initial 17.368389%; final 17.366986% | Fails <1% target |
| Transition | Minimum density 0.000600245; rebound diagnostic 1 | Filled in tested interval |
| Boundary | One crossing, R=66.854353 kpc | Finite; live restoration unestablished |
| Exterior T fraction, r>1.2R | 2.65653e-13 | No appreciable conversion in tested interval |
| Total mass | 5.364000000000011 Mb | Constraint conserved |
| Maximum absolute energy defect | 1.03917e-13 Eunit | Far below radiation signal |
| Maximum charge / mass defects | 1.81899e-11 / 1.59872e-14 | Audited conservation |

The exterior diagnostic follows the moving boundary. The distinct fixed
r>70-kpc T fraction decreases from 2.17829e-6 to 1.70209e-6 and includes the
initial dilated transition fringe. Neither diagnostic proves unlimited-time
nonconversion of the reservoir.

## Actual energy source and escaping modes

run_smooth_assessment independently decomposes the Hamiltonian. During free
evolution gravitational energy decreases by 0.00502723 Eunit while
density-gradient energy INCREASES by 7.87880e-5. Material flow gains 0.00175003;
the scalar gains 0.00104706. All component changes sum to 1.01252e-13.
The pulse is not burning a preloaded density-gradient packet. Compression work
is +0.001084663 and conversion work -0.0000376051, with backreaction included.

Far flux includes reactive field energy. In the source-free annulus beyond
500 kpc the calibrated outgoing/incoming characteristic decomposition gives:

| Quantity | Eunit |
|---|---:|
| Outgoing characteristic energy | 5.26093816e-6 |
| Incoming characteristic energy | 9.02674241e-14 |
| Reactive boundary energy | 2.16871193e-6 |
| Positive finite-grid correction | 8.52769690e-11 |

The exact discrete decomposition closes to 1.30e-21. Outgoing energy is only
0.50245% of net material-to-field work. Most work remains in the field.
The distant absorber has received zero energy because the wave has not reached
it. See OUTGOING_CHARACTERISTICS.md for the identity and gauge convention.

The finite-annulus packet RMS frequency is 1.678 rad/Myr and weighted duration
0.461 Myr. FFT resolution is 1.103 rad/Myr and the peak occupies its first bin.
No resolved coherent parent frequency, fast material occupation, sustained
cooling rate or noncollinear cascade is established. Exact spherical data cannot
test angular transfer. A real pulse is narrower evidence than a sustained pump.

## Boundary force and redistribution

The static equilibrium retains its fully relaxed radial stiffness:
k_R=0.00041127513 Eunit/kpc^2, F_R=-k_R delta R. At zero momenta the CC
phase/current sector adds positive quadratic squares and decouples from the
static real-amplitude sector. run_restoring_phase audits this addition;
RESTORING_FORCE_INHERITANCE.md states the finite-grid hypotheses. This is
local equilibrium restoration, not live nonlinear or nonradial restoration.

At the smooth final state Rdot=-0.0197654 kpc/Myr splits into transport
-0.0238140 and conversion +0.00404863. Independent continuity and crossing
derivatives agree. Finite radius or inward speed is not a restoring-force test.
Paired live perturbations remain necessary.

The earlier mass audit finds 0.857603 Mb missing inside 50 kpc. Conversion
cancels from total-mass continuity: boundary relabeling cannot fix this deficit.
The initial-acceleration redistribution scale is about 704 Myr, not a forecast
or bound. The 5.7-Myr trajectory neither reaches that scale nor rules out later
formation. It does rule out claiming that the first pulse has formed the law.

## Verification limits

Selected early unprepared observables agree under time-step halving (flux
relative difference 3.5e-5) and material-grid halving (5.8e-4). These do not
certify the complete smooth trajectory or its spectrum. Later quiet runs and C4
smooth data give comparable outgoing energies near 5.25e-6; their unequal
adaptive endpoints do not establish phase convergence. Frozen-carrier curvature
is positive and flow remains below the tested local energetic threshold;
neither supplies full coupled stability.

ROUTES.md records failed alternatives. EVIDENCE_ERRATA.md separates corrections
and withdrawn runs. MANIFEST_AUDIT.json records actual reproducibility checks.
A process exit, a conserved trajectory and a component result never substitute
for the original joint galaxy-formation target, which remains OPEN.
