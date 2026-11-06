# One interaction chain for baryons, vacuum phase, and material production

## Result

An explicit two-field model does connect all three processes: baryonic density
triggers a scalar condensate, its energy changes the phase stress, and its
motion creates particles of a second field. The same model also shows why a
final phase pressure does not uniquely determine the created material. Slow
and fast formation with identical endpoint phases produce different particle
occupations. No universal pool mass or MOND coefficient follows.

This is new conditional physics work after BARYON_PHASE_RESULT.md, not an
adopted action. All couplings below remain visible; none was calibrated to 1/2.
Frozen contract: SHARED_INTERACTION_CONTRACT.md, commits 60263a84e2 and
4b2c94656f. Interpretation uses natural units c=hbar=1 unless stated otherwise.

## 1. A concrete interaction

Take canonical real scalar fields sigma and chi with

    L = -(partial sigma)^2/2 -(partial chi)^2/2
        -V0 -ms^2 sigma^2/2 -lambda sigma^4/4
        -(m0^2+g^2 sigma^2) chi^2/2,

and baryonic rest masses multiplied by

    A(sigma)=1-alpha sigma^2/2.

Here ms^2, m0^2, lambda, alpha and g^2 are positive. The expression for A is
an effective small-field coupling, used only while A>0 and preferably
alpha sigma^2 much less than one. A globally valid completion is not supplied.
Einstein gravity and the baryonic action are understood as additional terms;
this calculation first takes a local weak-gravity background.

For baryons of conserved reference mass density rho_b, with negligible chi
occupation, the local energy density at fixed rho_b is

    f = rho_b + V0 +(ms^2-alpha rho_b) sigma^2/2
                       +lambda sigma^4/4.

The term -alpha rho_b sigma^2/2 makes dense matter favor the nonzero phase:

    sigma_eq^2 = (alpha rho_b-ms^2)/lambda, if alpha rho_b>ms^2;
    sigma_eq=0 otherwise.

The nonzero branch has curvature 2(alpha rho_b-ms^2)>0. This is local field
stability at fixed density, not full fluid or gravitational stability.

A finite object must also overcome gradient energy. For an ideal top-hat
baryonic sphere of radius R, the linear zero-mode threshold matches
sigma proportional to sin(k r)/r inside to exp(-ms r)/r outside, with

    k^2=alpha rho_b-ms^2,
    k cot(k R)=-ms.

The first threshold lies in pi/2<kR<pi for ms>0. Thus density alone is not
sufficient: object size matters. The local minimum is a bulk approximation
for regions large compared with the scalar healing length.

## 2. Derive the pressure without confusing binding energy with vacuum

On the condensed branch the combined energy density is

    f_min = rho_b+V0 -(alpha rho_b-ms^2)^2/(4 lambda).

However the scalar's own potential energy increase is positive:

    Delta U_sigma = (alpha^2 rho_b^2-ms^4)/(4 lambda).

The lowering of the combined energy includes a negative baryonic interaction
energy. It cannot all be relabeled a freely adjustable cosmological vacuum.
For conserved baryon number and a locally relaxed scalar, volume variation
requires P=rho_b df_min/d rho_b-f_min, giving

    P_total = -V0 +(ms^4-alpha^2 rho_b^2)/(4 lambda),
    dP_total/d rho_b = -alpha^2 rho_b/(2 lambda).

Here pressureless reference baryons have been used. Their own gas pressure,
stellar dispersion, gradients and gravity were not included in this local
formula. The induced contribution has negative compressibility. For an
otherwise pressureless responsive fluid in the long-wavelength local limit,
it is destabilizing; for stars, a collisionless analysis is needed. It is not
a positive isothermal pool pressure that can be substituted into the earlier
critical-sphere formula. Ordinary positive pressure or dispersion could help
stabilize it, but would introduce physical state information.

The stellar force from this coupling is -grad ln A. At weak coupling it is
alpha sigma grad sigma, attractive when sigma decreases outward. Outside the
baryons the small-field solution is sigma=C exp(-ms r)/r, hence

    a_sigma,r = -alpha C^2 exp(-2 ms r) [ms/r^2+1/r^3].

It is not a MOND 1/r acceleration. Even for ms r much less than one, this
quadratic coupling gives acceleration proportional to 1/r^3. This statement
concerns the direct scalar force; gravitational attraction from produced chi
particles would need their actual distribution and stresses.

## 3. The same phase motion can create actual particles

The coupling g^2 sigma^2 chi^2/2 makes the chi mass

    m_chi^2(t)=m0^2+g^2 sigma(t)^2.

For a homogeneous patch, each chi momentum mode satisfies

    u_k'' + omega_k(t)^2 u_k=0,
    omega_k^2=k^2+m_chi^2(t).

A static final condensate does not itself create a continuing flux. Starting
from an initial vacuum, matching an ideal instantaneous frequency change gives

    A_k=(sqrt(omega_f/omega_i)+sqrt(omega_i/omega_f))/2,
    B_k=(sqrt(omega_f/omega_i)-sqrt(omega_i/omega_f))/2,
    N_k=|B_k|^2=(omega_f-omega_i)^2/(4 omega_f omega_i).

These follow by continuity of u and u'; |A|^2-|B|^2=1. In a sufficiently slow,
smooth, gapped transition the positive-frequency mode evolves adiabatically
and particle production tends to zero. In a mode decomposition its mixing is
controlled by dot(omega)/(2 omega) with a rapidly oscillating phase. Thus
endpoint masses alone do not specify the material abundance.

We tested smooth transitions

    omega^2(t)=1 + 3[1+tanh(t/tau)]/2

with the same endpoints omega_i=1, omega_f=2. These are dimensionless mode
fixtures, not observed galaxy parameters. DOP853 integrations on [-12tau,12tau]
at two tolerances give:

| Transition duration tau | Final occupation per mode |
| --- | ---: |
| Ideal sudden matching | 0.125 exactly |
| 0.05 | 0.122715045321 |
| 0.5 | 0.0283924583592 |
| 5 | Consistent with negligible production; direct projection about 2.3e-14 |

The smallest number is not claimed accurate to its displayed relative digits.
The meaningful finite result is strong suppression compared with the fast
case. Both histories have the same final phase energy and baryon density.

The initial energy-based estimator returned about -1.46e-12 in the slow case
because it subtracts the vacuum half-quantum and amplifies normalization error.
That is numerical cancellation, not negative particles. A separately retained
implementation uses the nonnegative final-frequency projection

    N=|sqrt(omega_f/2) u - i u'/sqrt(2 omega_f)|^2.

It is cross-checked against the energy estimator using the Wronskian error.
Original and corrected evidence are preserved with separate scripts and hashes.

## 4. What is required to turn production into pool mass?

For these real scalar particles, in a homogeneous volume the number and energy
would be integrals of N_k over momentum. In particular

    n_chi = integral d^3k/(2pi)^3 N_k,
    rho_chi = integral d^3k/(2pi)^3 omega_f N_k.

Only if populated momenta satisfy k much less than m_chi does this behave as
cold matter with rho_chi approximately m_chi n_chi. An instantaneous mass jump
has N_k proportional to k^-4 at high k: its particle-number UV integral
converges, but its energy integral diverges logarithmically. A smooth physical
transition, rather than an arbitrary cutoff, must specify the spectrum.

For a finite evolving galaxy, gradients, transport, escape/binding, initial
occupation, and the spacetime-dependent sigma profile must be included.
Produced particles have no thermalizing self-interaction in the displayed
model; an isothermal halo does not follow automatically. In a locally static
weak potential, binding requires kinetic energy below the appropriate escape
energy. This condition is additional to merely producing particles.

Backreaction adds g^2 <chi^2> sigma to sigma's equation. When appreciable, it
changes both the phase and its stress. Prescribing a transition externally is
a test of history dependence, not a self-consistent production history.
Energy comes from the changing scalar/baryon configuration; it is not free
creation from a static gravitational field. A coupled cosmological/galactic
initial-value calculation would be necessary to predict a yield for this model.

## 5. Why no 1/2 follows from this interaction

At fixed local geometry, adding a constant to V0 changes neither the phase
minimum, the direct scalar force nor the mode-production equations. It does
change the outside vacuum density rho_DE (V0/c^2 in SI units). The parameters
alpha, lambda, ms, m0 and g also remain independent. Therefore this local
model supplies no identity that fixes the abundance and response relative to
c sqrt(G rho_DE). Full gravity makes V0 affect cosmic history; the local
argument does not exclude a special cosmological attractor, but no such
attractor or coefficient has been established here.

Even fixing all couplings and both endpoint phases leaves production sensitive
to formation history. Shared interactions alone do not imply universal final
abundance. Conversely, finding a chosen history/coupling that matches 1/2
would be a fit, not the requested derivation. No MOND normalization or rotation
curve is claimed from the computations above.

## Evidence and continuation

The original script passes 30 checks. Its sign-reversed Bogoliubov control
fails exactly field and derivative continuity. The projection implementation
passes 36 checks, including independent occupation/energy/Wronskian identities.
All three manifests are validated. The finite-size threshold and analytic
pressure/force interpretation have been self-reviewed; no independent review,
renormalized quantum effective potential, or complete dynamical health proof
is claimed. Tree-level phase minima require produced stress and quantum
corrections to be small, or else a new coupled calculation.

Related precedent, checked at abstract level only:
[Chen, Suyama and Yokoyama, Spontaneous scalarization: asymmetron as dark matter](https://arxiv.org/abs/1508.01384)
studies a massive matter-scalarization dark-sector model. This is adjacent
prior art, not a validation of this toy action or a novelty claim.

Disposition: a concrete shared interaction chain is established conditionally;
endpoint-only mass selection is refuted for this construction. Positive cold
pool pressure, a stable galaxy distribution, and normalization are unresolved.
A coupled formation study remains open, but requires an actual baryon history,
initial quantum state and coupling choices. A numerical scan cannot eliminate
those inputs. A genuinely new selector would need to relate the vacuum offset,
couplings and formation history through additional physical structure; the
river/pool analogy alone provides no such relation. This is not a universal
impossibility claim for all pool models.
