# Direct optical preparation of a confined pair below the mediator threshold

2026-10-14. Parent checkpoint: f4f066860260eea18bb94fb79108860d90ad54b2.

The conditional material wall admits a different loading mechanism: drive a
confined carrier–anticarrier pair through a VIRTUAL mediator at total energy
below the free mediator mass. This avoids requiring a propagating mediator to
decay before leaving the chamber. A one-pair calculation gives a nonzero matrix
element and a leading 1% creation-probability timescale of 10.5 ms at the assigned
optical intensity. It is not a demonstrated loading efficiency or a complete
manufacturing protocol: the wall, particle model, optical access and omitted
loss/many-pair channels still need validation.

## Same wall, a cavity chosen for the energy ordering

Retain m=1 eV, M_R=2m+delta, delta=2e-9 eV, mu=0.002 eV,
lambda=1e-6 and g=1e-20/eV. Use the preceding matched Coulomb-only barrier
U=4.9704148e-7 eV, including all its stated material-matching limitations.

Choose a vacuum sphere of radius a=2 cm, surrounded by material extending to
infinity for the spectral reference problem. This differs from the earlier
1 cm sphere: the larger radius lowers the two-particle ground energy below
delta. A real finite shell gives metastable states and needs its own leakage
calculation. The hypothetical mediator is taken to propagate freely through
this geometry; its wall-dependent mass corrections are not supplied.

Write the normalized carrier ground mode as psi(r)=u(r)/(sqrt(4pi)r), with
integral |u|^2 dr=1. Its interior sine and exterior exponential satisfy

    x cot x = -sqrt(z0^2-x^2),
    z0=a sqrt(2mU), E0=x^2/(2ma^2)

in natural units. The result is E0=4.71008e-10 eV per carrier. Both charges
see the same barrier. The distinguishable pair mode has spatial conversion
profile rho(r)=psi(r)^2. It is created from the initially empty carrier sector.

## Couple the pair to the mediator continuum

Nonrelativistic reduction of -mu R|phi|^2 gives

    H_conversion = h integral d^3x [b a^dagger c^dagger + h.c.],
    h=mu/(2m sqrt(2M_R))=5e-4 eV^(-1/2).

Here a and c denote the carrier and anticarrier fields, not the cavity radius;
b is the neutral mediator field. Its free Hamiltonian relative to the pair
rest mass is H_R=delta-laplacian/(2M_R). The normalization independently
reproduces the earlier vacuum width Gamma_phi=mu^2 beta/(16pi M_R).

Project onto one ground pair while retaining the spatial mediator continuum.
The pair's nonresonant contact energy is

    D = [lambda-mu^2/(4M_R^2)]/m^2 * integral |psi|^4 d^3x.

The subtraction is the leading short-range t-channel exchange; the near-pole
s-channel is treated separately through the continuum resolvent below. This
prevents treating all exchange as a local static quartic. Derivative corrections
to that short-range approximation and other carrier modes are omitted.

The one-pair self-energy and its dressed energy obey

    Sigma(E)=h^2 <rho|(E-H_R)^(-1)|rho>,
    E=2E0+D+Sigma(E),
    Z_pair=1/[1-Sigma'(E)].

For E<delta the denominator has no real momentum zero, so this free-mediator
channel has no on-shell imaginary part. The self-energy is real and negative.
That closes conversion of the isolated pair into one escaping REAL mediator;
it does not close annihilation into photons, pump-assisted processes or every
possible medium excitation.

The computed values are

    dressed pair excess E = 9.41899e-10 eV,
    Sigma(E) = -1.17130e-13 eV,
    delta-E = 1.05810e-9 eV,
    Z_pair = 0.99991047.

The virtual mediator component has probability about 8.95e-5. Its characteristic
spatial decay length is (hbar c)/sqrt(2M_R(delta-E))=3.033 mm. This is not the
free mediator's decay flight distance. The contact contribution is about
4.70e-22 eV and does not set the reported energy shift.

## Drive the same confined state with photons

Retain the leading matched, counterpropagating optical normalization
F0=g u_peak/sqrt(2M_R), with each traveling wave's assigned peak intensity
1e12 W/m^2. In the spherical vacuum region take the transverse source envelope
exp[-r_perp^2/(2L_t^2)], L_t=1 mm, and zero source in the surrounding material.
The optical Rayleigh range is much larger than the chamber, so axial envelope
variation is neglected. The sphere's detailed optical boundary, mirrors and
pump access are NOT solved by prescribing this field. No open hole can simply
be ignored when calculating carrier leakage.

Only the source's spherical component couples to the ground pair. Its angular
average is

    F_bar(r)=F0 Daws(t)/t, t=r/(sqrt(2)L_t),

with limiting value F0 at r=0; Daws is Dawson's integral. The dressed pair
creation matrix element is

    Omega = sqrt(Z_pair) h <rho|(E-H_R)^(-1)|F>.

Both the self-energy and this source overlap are computed in the same spherical
geometry with the same carrier ground mode. This replaces multiplying a free
mediator production rate by an assumed capture fraction.

The result is

    |Omega| = 6.2816e-15 eV,
    |Omega|/hbar = 9.5435 per second.

Tune the total photon energy to 2m+E, rather than M_R. On resonance and at small
transition probability, starting from vacuum,

    P_one_pair(t) = |Omega t/hbar|^2 + higher-order terms.

The leading expression reaches 0.01 at t=0.01048 s. This is a perturbative
single-channel timescale, not a guaranteed pair count per pulse or a steady
production rate. Continued driving can reconvert pairs to the optical field;
many-pair stimulation, energy shifts and photon losses require evolution of a
larger system. No high-probability pulse or macroscopic inventory is inferred.

The virtual-response memory scale hbar/(delta-E) is about 0.62 microseconds,
much shorter than that timescale. Smooth turn-on and turn-off could separate
those scales. An abrupt drive would contain frequencies above the mediator
threshold; this static calculation does not bound that transient loss. Actual
pump linewidth and detuning must also be controlled, and the hypothetical
particle mass is not known experimentally for tuning.

## Numerical method and formal scope

For each trial E below threshold, solve the radial resolvent using the
half-line Green function

    G(r,s)=[exp(-kappa|r-s|)-exp(-kappa(r+s))]/(2kappa),
    kappa=sqrt(2M_R(delta-E)).

The script uses dimensionless radius r/a. Independent boundary-value solutions
with a regular origin and decaying exterior give the source and pair response.
The derivative discontinuity in the Green kernel is avoided in the main
integration; direct Green integrals at selected radii check the solutions.
The optical source is solved inside the sphere and continued exponentially,
rather than forcing a discontinuous right-hand side through a smooth solver.

Twelve bounded checks pass: ground-mode normalization, two BVP refinements,
the dressed-energy equation, four source Green comparisons, residue derivative
refinement, two pair Green comparisons and vacuum-width normalization. Ground
mode tails are retained for 25 exterior decay lengths, and quadrature uses
320 nodes per radial region. These controls verify this projected model, not
convergence over all carrier-pair channels.

ClosedChannel.lean proves only that E<delta and positive mediator mass imply
E differs from delta+p^2/(2M_R) for every real p, via a positive denominator.
It does not prove the computed bound spectrum, source matrix element, complete
resolvent theory, physical particles, or experimental loading. Compiler logs
record its actual formal scope. This is self-reviewed research.

## Preparation status

There is now a conditional amplitude for optical creation INTO a confined mode,
with the dominant one-real-mediator escape channel energetically closed. The
chain uses the same declared photon/cubic interactions and the conditional
Coulomb wall; it does not first assume a trapped carrier population.

The original objective is still not fully achieved. In particular, the complete
material scalar charge and experimental admissibility are unresolved; an optical
boundary that transmits pump energy while retaining carriers has not been
constructed in the model; finite-shell leakage, two-photon annihilation,
other pair modes and driven many-pair dynamics remain to be calculated. The
identity with the repo's cosmological cold component also remains unproved.

Reproduce:

    python3 sol61_push/confined_virtual_pair_2026_10_14/check.py /tmp/confined_pair_results.json

The run manifest pins the corrected material-wall input and executable source.
The next computation should test optical access and finite-shell retention in
one common material geometry, followed by a controlled finite-pulse evolution.
