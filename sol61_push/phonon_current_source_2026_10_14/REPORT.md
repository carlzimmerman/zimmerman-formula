# Cold production through a harmonic target's transverse current

2026-10-14. Base branch checkpoint: 848bf43520505471a5135d9e6e5d8f24e2dccfc0.

The transverse current of a bound charged site lifts the zero-momentum scalar
production node of the static charge channel. This is a concrete additional
production mechanism in the stipulated scalar-photon theory. Its calculated
cold-pair yield remains negligible for the assigned benchmark. The calculation
neither establishes the particles nor provides a real target or capture method.

## Model and scope

Retain the local interaction -g R F_munu F^munu/4, g=2.93129374869688e-15/eV,
M_R approximately 2 MeV, daughter mass 1 MeV, pair excess 2e-9 eV, and
Br(R -> phi anti-phi)=1/2 from the ordinary-lepton source branch. The source
mass is rounded to 2 MeV in smooth kinematic factors; the tiny pair excess is
retained separately in the daughter acceptance. This is a narrow on-shell
source calculation, not a full finite-width integration.

The target consists of independent isotropic harmonic charged sites, initially
in their ground states, with M=200 GeV, Z=82, and assigned oscillator energies
Omega=0.01, 0.03, 0.1 eV. The macroscopic support takes momentum with negligible
center-of-mass recoil energy. Internal oscillator excitation energy is retained.
There is no measured crystal dispersion, temperature distribution, form factor,
spatial coherence geometry or attenuation model. Local inelastic final states
at distinct sites are orthogonal, so their probabilities add. Elastic Bragg
coherence is outside this calculation and was audited separately.

Use site column 3e25/m^2, photon flux 1e8/s, Gaussian energy RMS 5000 eV,
center M_R+10 eV, and require BOTH daughters to have laboratory kinetic energy
at most 1e-8 eV. These are assigned inputs, not demonstrated apparatus parameters.

## Charge and current matrix elements

In natural units, the nonrelativistic one-site operators are

    rho(Q) = exp(i Q.x),
    j(Q) = {p_operator, exp(i Q.x)}/(2M).

For H=p_operator^2/(2M)+M Omega^2 x^2/2, their commutator obeys
[H,rho]=Q.j. Thus Delta*rho_f0=Q.j_f0, where Delta is the internal excitation
energy. Including j is essential; substituting a charge response alone misses
transverse final states.

Choose an oscillator axis along Q and define eta=Q^2/(2M Omega).
For n longitudinal quanta and no transverse excitation,

    rho_n = exp(-eta/2) (i sqrt(eta))^n/sqrt(n!),
    Delta_L = n Omega,
    j_L = (Delta_L/Q) rho_n Qhat.

For n longitudinal quanta plus one quantum along either transverse unit vector e_a,

    rho_f0 = 0,
    Delta_T = (n+1) Omega,
    j_T = i sqrt(Omega/(2M)) rho_n e_a.

Both channels contain w_n=|rho_n|^2=exp(-eta) eta^n/n!, but are distinct final
states and do not interfere. At fixed Q, sum_n w_n=1 and mean excitation in the
longitudinal sector is eta Omega=Q^2/(2M). Here it is approximately 10 eV.
This identity does not justify multiplying an elastic cross section by 1-f:
energy transfer, photon spectrum and current contraction differ by final state.

## Scalar-photon contraction and rate

Take k=(omega,0,0,omega), outgoing mediator energy E=sqrt(M_R^2+P^2), and
u=P_z/P. Define the spatial transfer Q=k_vec-P_vec,

    Q^2 = omega^2+P^2-2 omega P u,
    Q_T^2 = P^2(1-u^2),
    q=(Delta,Q),  t=Delta^2-Q^2,
    omega=E+Delta.

Q^2 denotes a spatial norm throughout; t is a Minkowski invariant. With
metric (+---), the heavy-site normalized amplitude is

    Mcal = (2M g Z e/t) [(k.q)(epsilon.j)-(k.j)(epsilon.q)].

For the conserved longitudinal current, its contraction divided by t reduces
to -omega (epsilon_vec.Q)/Q^2 times rho_n. The polarization average gives

    average |M_L|^2 = 2 M^2 g^2 Z^2 e^2 omega^2 Q_T^2/(Q^2)^2 * w_n.

For the two orthogonal transverse final states, project
(k.q) epsilon_vec+(epsilon_vec.Q) k_vec perpendicular to Q. The summed and
polarization-averaged squared projection is

    (k.q)^2 - omega^2 Q_T^2 t/(2Q^2).

Consequently

    average |M_T|^2 = 2M Omega g^2 Z^2 e^2 omega^2/t^2
                     * [(E-Pu)^2-Q_T^2 t/(2Q^2)] * w_n.

At P=0 the longitudinal amplitude vanishes, but the transverse numerator is
E^2>0. The oscillator's transverse excitation supplies the current matrix
element. It costs energy Omega in addition to the n longitudinal quanta;
there is no energy-free recoil assumption for internal modes.

In the heavy anchored-site approximation,

    d sigma/d^3P = average |Mcal|^2
                  *delta(omega-E-Delta)/(64 pi^2 M^2 omega E).

Integrating incident photon energy has unit Jacobian. The rate is

    N_column (hbar c)^2 Br_phi integral d^3P A(P)
    * sum_n S(E+Delta) [kernel_L + kernel_T],

where each channel uses its own Delta, Q, t, eta, and

    kernel_L = alpha g^2 Z^2/(8pi) * (omega/E) Q_T^2/(Q^2)^2 * w_n,
    kernel_T = alpha g^2 Z^2 Omega/(8pi M) * (omega/E)
               * [(E-Pu)^2-Q_T^2 t/(2Q^2)]/t^2 * w_n.

The sum above is shorthand for separate channel sums, not evaluation at a
shared excitation energy. The assumed scalar isotropic decay yields

    r=sqrt(2m Kstar), b=sqrt(2m Kcut),
    A(P)=min(1,max(0,(b^2-r^2-P^2/4)/(P r))).

A(0)=1 by continuity. Quadrature splits at P=2(b-r) and ends at
P=2sqrt(b^2-r^2). Nonzero amplitude at P=0 does not confer finite probability
on that single point; the phase-space volume still shrinks as P^3.

## Numerical result

| Omega (eV) | Longitudinal pairs/s | Transverse pairs/s | Total pairs/s | Transverse / longitudinal |
|---|---:|---:|---:|---:|
| 0.01 | 5.566e-42 | 5.015e-41 | 5.572e-41 | 9.01 |
| 0.03 | 5.566e-42 | 1.505e-40 | 1.560e-40 | 27.03 |
| 0.10 | 5.566e-42 | 5.015e-40 | 5.071e-40 | 90.11 |

The inclusive longitudinal rate recovers the previous small-momentum
stationary-target rate, even though a coherent zero-excitation amplitude is
exponentially small. These are different final-state selections. This result
shows why the coherent elastic suppression alone cannot exclude inclusive
production. The transverse sector enhances this benchmark but falls far short
of a useful source, even before any collection losses.

A separate leading small-P calculation gives, with S evaluated near M_R+10 eV,

    rate_L = N_column (hbar c)^2 Br S alpha g^2 Z^2/(3 M_R^4)
             * integral P^4 A(P) dP,
    rate_T = N_column (hbar c)^2 Br S alpha g^2 Z^2 Omega/(8pi M M_R^2)
             * integral A(P) d^3P.

These reproduce both integrated rates within 1e-4 relative tolerance. The
transverse result depends on the ground-state velocity variance Omega/(2M),
not a coherent N^2 gain. Extrapolating Omega to arbitrarily large values would
invalidate the assigned nonrelativistic material model and is not a route
established by these three cases.

## Evidence and next discriminating step

129 bounded checks pass: explicit four-vector contractions, continuity, photon
Ward algebra, independent oscillator matrix exponentiation at eta=0.1,1,5,
fixed-Q Poisson normalization/mean, 12-to-24-node quadrature refinement,
100 extra oscillator levels, and separate leading asymptotic rate formulas.
The oscillator matrix has 100 levels and checks final levels 0 through 11;
it verifies the matrix-element formula at bounded eta, while production sums
use its analytic log-Poisson expression up to the documented cutoff. The Ward
check is an algebraic consistency check, not an independent physical test.

The run manifest records inputs and execution. CurrentNode.lean proves only
conditional zero-momentum numerator positivity and excitation-energy algebra.
It does NOT certify the scattering normalization, oscillator model, numerical
integrals, physical existence, confinement or experimental viability.

The prior turn explained existing results without adding evidence. This turn
adds the previously missing transverse current and changes the next research
question: a candidate target must supply a quantitatively larger measured
transverse dynamic response at momentum near 2 MeV and its associated energy
transfer. A generic claim of lattice coherence or phonons is insufficient.
Other possibilities require a new explicit source interaction or a verified
cooling/capture stage; none is established here. The overall goal remains open.

Reproduce from the repository root:

    python3 sol61_push/phonon_current_source_2026_10_14/check.py /tmp/phonon_current_results.json

Related model provenance: ../ordinary_lepton_source_2026_10_13/REPORT.md;
static-target normalization: ../cold_primakoff_target_2026_10_14/REPORT.md;
coherent versus inclusive distinction: ../collective_recoil_audit_2026_10_14/REPORT.md.
The present harmonic-current derivation is supplied explicitly above and does
not claim that those references describe a measured target with these properties.
