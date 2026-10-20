# Protected five-dimensional gauge cubic: operator and source audit

2026-10-20. Criteria: `FROZEN_CRITERIA.md`, criteria-only commit2591280c8;
continuation base9a9ab4032. This is an analytic audit, not a new healthy
microscopic selector. Exact primary versions and normalization qualifications
are in `SOURCES_GAUGE.md`. No level, flux, radius, coupling or vacuum offset
is chosen using the target. No new code or Lean is needed for this decision.

## 1. What the protected cubic actually multiplies

Use signature(-++++) and one Abelian Coulomb coordinate sigma in a regular
positive chamber. The source-compatible component convention is

    P(sigma)=m0 sigma^2/2+c sigma^3/6,
    t(sigma)=P''=m0+c sigma,
    L5=t[-F_MN F^MN/4-(partial sigma)^2/2+Y^2/2+Fauxbar Faux]
       +(c/24)epsilon^{MNPQR}A_M F_NP F_QR.

Here Y=D+partial5 sigma. The last component term is
`(c/6) integral A wedge F wedge F` in differential-form notation. These are
Dudas--Gherghetta--Groot Nibbelink Eqs(43)--(45). Its c is a component
normalization; it must not be identified numerically with IMS's integer
coefficient without translating the charge basis and action prefactors.

Seiberg Eqs(2.2)--(2.3) identify the same cubic prepotential with
sigma(partial sigma)^2, sigma F^2 and A wedge F wedge F. IMS Eq(2.22) gives
the exact piecewise-cubic Coulomb prepotential, including vector/hypermultiplet
one-loop thresholds. The protected statement concerns the two-derivative
Coulomb action within its chambers. It is not an exact finite-field
constitutive action, a sigma^3 potential, or a theorem fixing all higher
derivative operators. Charged states integrated out in that action become
massless on the corresponding chamber walls.

For static pure electric A=A0(x)dt,

    F=dA0 wedge dt=-dt wedge dA0,    F wedge F=0.

The CS term and its bulk gauge variation vanish on this sector. At a fixed
regular sigma0 with t0>0, the local electric Lagrangian is t0 E^2/2 and
Gauss is div(t0 E)=rho. This conditional fixed-modulus statement is not
the full scalar equation: for t'=c nonzero, an electric field generally
sources sigma. The scalar has its own kinetic term; it is not an auxiliary.
At F=0, constant sigma and Y=Faux=0, the displayed action has exactly zero
vacuum energy throughout the Coulomb branch.

Even at m0=0, c>0, sigma>0, the scalar coordinate change

    chi=(2/3)sqrt(c) sigma^(3/2)

gives the ordinary kinetic term -(partial chi)^2/2 and P=3chi^2/8. This
does not turn P into a derivative cubic. At sigma=0, t=0: the Abelian
photon kinetic coefficient vanishes and the integrated-out charged states
cannot be kept heavy. This is a failure of this controlled low-energy
description; it is not a proof that the full interacting fixed point is a
ghost theory.

## 2. A real electric cubic from radial relaxation

There is a constructive operator workaround once a new potential is added.
After an untwisted circle reduction of circumference ell, write the
four-dimensional dielectric T=C sigma with C=ell c>0. Add

    V(sigma)=kappa sigma^3,       kappa>0, sigma>0.

In a local adiabatic electrostatic approximation, dropping the retained
scalar gradient only for this algebraic minimization,

    Lstatic=C sigma E^2/2-kappa sigma^3,
    sigma=sqrt(C/(6kappa)) |E|,
    Leff=C_E |E|^3,
    C_E=C^(3/2)/(3sqrt(6kappa))>0.

This is not obtained by evaluating the CS term. It is dielectric relaxation
against an added potential. The fixed-displacement Hamiltonian checks the
ensemble and the sign independently:

    H(D,sigma)=D^2/(2C sigma)+kappa sigma^3,
    D^2=6C kappa sigma^4,
    H_min=4 kappa^(1/4)|D|^(3/2)/(6^(3/4) C^(3/4)),
    H_sigma_sigma=D^2/(C sigma^3)+6kappa sigma>0.

The stationary point is the unique global minimum for D nonzero and
sigma>0. These facts are necessary local energy checks, not a demonstration
of the full microscopic spectrum, derivative expansion or source map.
The existing `../current_interactions/CurrentEnergy.lean` already proves the
same rational-polynomial gap/global-minimum algebra: substitute
Q=sigma, lambda=3kappa and n^2=2D^2/C. Its formal statement does not derive
this dielectric action, its Gauss law or any force normalization.

The scalar gradient term C sigma(partial sigma)^2/2 remains in the action.
In the canonical real coordinate chi=(2/3)sqrt(C)sigma^(3/2), this added
potential is 9kappa chi^2/(4C). Its canonical vacuum mass squared is
9kappa/(2C). Slow variation relative to that mass can justify a local
radial approximation in a suitable nonzero-field region. It does not
restore a nonzero photon kinetic term at the zero-field vacuum, or keep
the Coulomb-branch charged thresholds heavy as sigma tends to zero.
The zero-field vacuum of this construction is sigma=0, V0=0, T0=0.

One explicit four-dimensional N=1 local diagnostic shows where the added
potential could live. Let Z=sigma+ia and choose

    Re f(Z)=C sigma,
    K=C(Z+Zbar)^3/24,        K_ZZbar=C sigma/2,
    W=y Z^3/3.

On a=0, the rigid F-term potential is

    V=|W_Z|^2/K_ZZbar=(2|y|^2/C)sigma^3,
    kappa=2|y|^2/C.

The a=0 slice is stationary for the potential and for a pure electric
field. This demonstrates the algebra, not a globally completed compactified
model. Untwisted five-dimensional N=1 reduction preserves four-dimensional
N=2; this added superpotential breaks that protection to N=1. Its coefficient
y is a new interaction and is not set by the gauge CS level. Moreover a is
a periodic Wilson line in a genuine compact gauge theory; a polynomial in
Z requires a global large-gauge-consistent completion. Holomorphic
nonrenormalization of a chosen coupling would not determine its value.
No authenticated source here supplies an independent equation for y,
the radius, and a positive vacuum scale simultaneously.

## 3. Positive FI energy changes the infrared response

For an ordinary auxiliary source zeta Y, the vector action gives

    Laux=T Y^2/2+zeta Y,
    Y=-zeta/T,              V_FI=zeta^2/(2T)>0.

This explicit one-field diagnostic does not assume that an arbitrary bulk
FI term has a UV completion for every five-dimensional non-Abelian fixed
point. The source's brane FI analysis also leaves its coefficient and
compensating moduli explicit.

With T=C sigma and no added cubic potential, fixed-E stationarity would
require

    dLstatic/dsigma=C E^2/2+zeta^2/(2C sigma^2)=0.

There is no finite positive solution for zeta nonzero. Equivalently
H=(D^2+zeta^2)/(2C sigma) runs toward large sigma. FI by itself neither
stabilizes the critical vacuum nor generates the desired electric cubic.

With both kappa sigma^3 and FI, the vacuum is at

    sigma0^4=zeta^2/(6C kappa),
    epsilon=V(sigma0)=4kappa sigma0^3>0,
    T0=C sigma0>0.

This is the rigid matter potential at its own minimum; minimal Einstein
coupling would make it gravitate, but a supersymmetric gravitational
completion with this potential and its retained spectrum has not been
derived here.

The algebraic finite-field branch is exactly

    sigma(E)^2=[C E^2+sqrt(C^2 E^4+24kappa zeta^2/C)]/(12kappa).

Its weak-field expansion is

    Leff=-epsilon+(C sigma0/2)E^2
         +C^2 E^4/(96kappa sigma0)+O(E^6).

Thus this uplift gives a quadratic infrared response. The electric cubic
is approached at larger E, where the FI contribution becomes negligible.
This is the opposite order from the required infrared cubic and ultraviolet
quadratic. Adding an ordinary m0 E^2/2 to the zero-FI example likewise makes
the quadratic dominate smaller E and the cubic dominate larger E. The
prepotential action does not supply the required high-field saturation.

For clarity, this FI+cubic algebra does have a parameter-independent but
inapplicable cross-regime combination. If one labels its low-field
coefficient C2=C sigma0/2 and high-field coefficient C3=C_E, then

    epsilon C3^2/C2^3=16/27.

Those coefficients have the wrong ultraviolet/infrared assignment and
are static electric Lagrangian coefficients. The electric Hamiltonian
H(E)=E dot partial_E Leff-Leff has high-field cubic coefficient 2C_E;
its corresponding cross-regime energy combination would instead be
64/27. Neither is the operational ratio R or a partial normalization
proof for 128pi/9.
An arbitrary constant offset can supply positive energy without this
crossover, but it introduces no equation selecting that offset.

## 4. The electric force has the wrong sign for universal attraction

Define an electric potential V with E=-grad V, source term -rho_q V and
test potential energy qV. For Leff=C_E|E|^3, in n>=2 spatial dimensions,

    D=3C_E |E|E,             div D=rho_q,
    E_r=sign(Q)sqrt(|Q|/(3C_E Omega_(n-1))) r^(-(n-1)/2).

In the original five-dimensional bulk n=4 and E falls as r^(-3/2).
Only after reduction to three large spatial dimensions does it fall as
1/r. The test force is qE; sources and tests with like charge repel.
A charge proportional to positive inertial mass therefore gives universal
repulsion, not gravitational MOND attraction. Changing the name or sign
of V changes the source and force together. Changing the kinetic sign
or making the charge imaginary does not supply a healthy repair.

For comparison a healthy attractive scalar static Lagrangian
-C3|grad Phi|^3-alpha rho_m Phi gives
3C3 div(|grad Phi|grad Phi)=alpha rho_m and force -alpha grad Phi.
The opposite static gradient sign is physically consequential. A mixed
gravitational, scalar or dipolar realization would need its own action,
source equation and retained-mode audit; it is not supplied by CS
quantization. KK momentum is also not a universal mass charge:
p5=2pi n/ell whereas m4^2=m5^2+p5^2, including neutral massive states.

Even without the added potential, a scalar-electric BPS-shaped ansatz
E=+/-grad sigma on the source-free m0=0 branch gives
div(c sigma grad sigma)=(c/2)Delta(sigma^2)=0. Radially,
sigma^2=sigma_infinity^2+constant/r^(n-2) for n>2. For n=3 and
sigma_infinity=0 its electric magnitude falls as r^(-3/2), not 1/r.
This additional profile is not the dielectric-potential construction.

## 5. What flux, compactification and gravity protection add

Magnetic components can activate the CS Gauss term. In four spatial
dimensions its source is a spatial F wedge F density, whose integral can
be quantized under the required bundle/boundary hypotheses. That fixes
an integrated topological charge. It does not impose a local isotropic
constitutive relation D proportional to |E|E. Nonzero magnetic fields
also carry the positive Maxwell energy and generally non-vacuum stress.
This is distinct from the prior 2+1-dimensional CS-Higgs obstruction,
where Gauss directly ties charge to B and the charged covariant gradient
prevents a homogeneous nonzero-B matter minimum.

For circle-invariant fields A=A4+a dy and F=F4+da wedge dy, the CS
reduction is locally an axion a F4 wedge F4 interaction plus a boundary
term. In a trivial patch,

    A wedge F wedge F=[3a F4 wedge F4-2d(a A4 wedge F4)] wedge dy.

For constant a the bulk term is itself locally a total derivative;
global bundles/boundaries must be retained when computing a theta term.
The pure electric sector still has F4 wedge F4=0. With a magnetic
background an axion can couple to E dot B. For example, a regular
massive axion with quadratic operator m_a^2-T Delta gives upon elimination
a term proportional to (E dot B)(m_a^2-T Delta)^(-1)(E dot B), quadratic
and anisotropic in E at fixed B. A massless axion instead makes this
elimination nonlocal. Neither calculation supplies the missing universal
attractive electric cubic or a stress-free positive vacuum.

There is a genuine stronger normalization example: minimal ungauged
five-dimensional supergravity fixes the relative Einstein, Maxwell and
CS coefficients. In Gauntlett et al.'s convention its Eq(2.2) is

    d star F+(2/sqrt(3))F wedge F=0.

Pure electrostatics again removes the CS term and leaves the Maxwell
operator. At F=0 the same equations give Ricci-flat vacuum, not positive
vacuum energy. This is an explicit protected normalization with the
wrong operator, even when the gauge coefficient is tied to Newton's
coefficient and no separate Coulomb scalar is present. The cited theory
is ungauged; this is not a no-go theorem for every gauged supergravity.

In an unwarped rigid-model circle reduction, separately adding
M5^3 R5/2 gives M4^2=ell M5^3. Neither the rigid cubic-prepotential theorem
nor CS charge quantization fixes this coefficient or ell. Minimal
supergravity illustrates why tying them is insufficient by itself.

## 6. Scope and remaining open possibility

The protected two-derivative prepotential by itself fails the electric
operator map and has zero Coulomb-vacuum energy. Radial relaxation with
a new cubic potential truly produces the electric magnitude, but has
no regular nonzero-kinetic zero-field photon vacuum, no demonstrated
protected potential/uplift relation, no required ultraviolet quadratic
branch, and the wrong force sign for universal same-sign charges.
The explicit FI repair supplies positive energy while losing the
infrared cubic. The minimal gravitational normalization does not repair
these operator facts. None yields a physical equation forcing R=128pi/9.

This closes the stated source-backed action and explicit continuations,
not every interacting SCFT, gauging, compactification or emergent-gravity
construction. A surviving new continuation would need to derive an
attractive universal source map and full finite-field action, show a
healthy same-state positive-vacuum spectrum and actual UV force law,
and provide an independent equation fixing its operational ratio.
The Coulomb prepotential alone supplies none of those missing equations.
