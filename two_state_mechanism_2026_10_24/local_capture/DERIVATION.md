# Local conversion, independent transport, and conserved work

This is a Newtonian effective-model construction and finite synthetic test.
It is not a derived microscopic interaction. The final reversible branch is
`capture_v4.py`; the distinct dissipative branch is `capture_radiative.py`.
Earlier versions and their estimator/encounter-rate limitations are retained.

## 1. Individual state and motion

Each positive-mass packet has its own three-dimensional position and velocity.
A medium packet is either F or T; its mass is unchanged by conversion. There
is no common phase variable, common radius, or forced common velocity. Baryons
remain a separate species. Labels F and T select field charge, not galaxy type.

With X=sum(mi xi)/Mtot and Ri=sqrt(|xi-X|²+epsilon²), a compact smooth radial
shell kernel Si(r)=S(r/Ri) represents each packet in the polarization monopole.
The ordinary gravitational energy uses actual three-dimensional separations:

    Ug = -G sum_{i<j} mi mj / sqrt(|xi-xj|²+epsilon²),
    MT(r) = sum_{i in T} mi Si(r),
    z(r) = G MT(r)/(a0 r²),
    UT = (a0²/G) integral r² [-log(1-z)-z] dr,
    H = sum mi |vi|²/2 + Ug + UT + Q.

Require z<1. The numerical domain includes an infinite-radius field tail.
This is a 3D transport model with a spherical-average tether field; it is NOT
a full 3D polarization solution. Softening and finite packet self-energy must
be taken seriously when interpreting resolution dependence.

Differentiating UT includes the dependence of X on every position. If ai is
the direct positional gradient at fixed X, then

    grad_i UT = ai - (mi/Mtot) sum_j aj.

Only T packets have an individual ai. All particles share the compensating
center reaction in this monopole approximation. The gradients sum to zero;
rotational invariance makes total torque zero. Two equal-position, equal-mass
packets in different states have different accelerations, which is explicitly
tested. Thus F and T can segregate dynamically. The center term is a limitation
of this collective field representation, not an omitted force in the energy.

## 2. A finite local reaction pays its full field cost

Choose a nearby baryon partner with a compact, position-based neighbor kernel.
Change one medium packet's state at fixed positions and calculate

    Delta = UT(after) - UT(before).

Ug is unchanged. Use the full finite difference, not an initial chemical
potential held fixed through a large conversion. Define the unit pair normal
n=(xi-xj)/|xi-xj|, reduced mass mu=mi mj/(mi+mj), incoming normal relative
velocity vn<0 and K=mu vn²/2. For an energetically allowed reversible event,

    vn' = +sqrt(vn² - 2 Delta/mu),
    J = mu (vn'-vn) n,
    vi' = vi + J/mi,   vj' = vj - J/mj.

Tangential relative velocity and center-of-mass velocity are unchanged.
Therefore Delta K=-Delta, Delta P=0 and Delta L=(xi-xj) cross J=0 exactly.
F->T uses collision kinetic energy; T->F returns stored field energy to motion.
There is no global work pump, conversion reward or prescribed phase fraction.

## 3. A local activation barrier and the sampling measure

The hypothetical transition-state barrier is

    B=beta Cpair |Delta|,
    K >= max(Delta,0)+B.

Cpair averages the local circulation statistic before and after the proposed
nonradiative impulse. Under reversal of all velocities and the state switch,
Cpair and B are unchanged. Reverse kinetic energy is K-Delta, so its barrier
condition is algebraically identical to the forward condition. This checks
reversibility of the allowed reaction, not a microscopic origin for beta.

The local circulation estimate fits baryon velocities to an affine field.
It uses curl squared relative to residual dispersion/h², with isotropic ridge
regularization and conservative subtraction of estimated curl noise. The
chosen final subtraction is four times the noise expectation, calibrated on
a fresh finite Gaussian sample. This estimates resolved ordered circulation;
it is neither a temperature classifier nor exact microscopic vorticity.
Velocity boosts and coordinate rotations leave it invariant.

The final hazard carries incoming normal collision flux:

    gamma=10 sqrt(G rho_b) |vn|/sqrt(G M_b,neighbors/h).

The reference speed, density, partner probabilities and h depend on positions
only. If a and b are incoming/outgoing speed magnitudes, db/da=a/b, so a da
=b db. A speed-independent encounter rate would not supply this factor; the
earlier runs with that rate are exploratory. The Poisson probability is
1-exp(-gamma dt). Finite dt, one candidate per packet per interval, omitted
internal degeneracies and modeled cross sections prevent a claim of complete
microscopic detailed balance. The half-interval control tests one discretization.

## 4. Radiative capture as a separate physical assumption

Reversible excitation need not trap a T packet below its release barrier.
In the radiative branch, cross the same activation threshold first, then use
an outgoing normal restitution e=.3 for F->T:

    Kout=e²(K-Delta),
    Qrad=(1-e²)(K-Delta)>=0.

The central impulse now removes Delta+Qrad from pair kinetic energy. Add Qrad
to the receiver, yielding Delta H=0. T->F remains nonradiative. This models a
cold radiation receiver with no incoming absorption. It is intentionally
irreversible, and cannot be described as the time reverse of a closed two-
body event. Zero net radiative momentum is an isotropic Newtonian closure;
relativistic recoil and gravitating radiation energy are not simulated.

Both branches also allow baryon-baryon central collisions with restitution
.5. Their kinetic loss enters Q, conserving total energy while permitting
dissipative baryonic assembly. A no-baryon-cooling control is included.

## 5. Claims that need separate tests

All numerical masses/scales receive the same law, coefficients, and initial
rotation/flattening families. Rotation and shape are initial conditions, not
object labels selecting a state. Rates use actual local baryon moments.

Total-energy conservation during transport is approximate to the controlled
Hamiltonian integration error; collision bookkeeping is algebraically exact.
There is no after-the-fact energy rescaling or projection. Fixed-state step
subdivision is allowed; state changes outside the field domain are rejected.

Snapshot-bound free mass uses current Newtonian potential and kinetic energy.
It does not establish asymptotic retention, especially with the common center
reaction and an evolving potential. Global T fraction, inner T fraction and
the actual monopole acceleration residual are reported separately. A small
global T fraction alone cannot rule out an inner T-dominated region. The
acceleration comparison is diagnostic, not a force imposed by the integrator.

Real dwarf/cluster mass sufficiency, disk morphology, nonspherical field
completion, microscopic cross sections, stochastic/continuum convergence and
long-term survival are further obligations. Finite successful conservation
checks do not establish them.
