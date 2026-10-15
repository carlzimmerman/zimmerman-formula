# Counted nonrelativistic lift, finite inventory and a global minimum of the gamma-zero S2 reduction

VC3-DL-001, 15 October 2026. The explicit finite-inventory equilibrium and global
minimum proved below belong to the **gamma-zero reduction** of the frozen S2
functional. The actual frozen stiffness is nonzero. For that case this work
derives its density stiffness and a conditional positive-energy theorem, but
does not assert that the gamma-zero profile solves its equations. The model is
nonrelativistic and electrostatic; no healthy Lorentz vacuum or radiation sector
is inferred.

This adds counted density/current dynamics, the gravitational cancellation,
physical nonnegative-density constraints and a free-support variational
inequality. The earlier reciprocal-medium work established local principal
health for a different varied-frame action; it did not supply these nonzero
spatial-gradient terms or this finite-inventory global energetic result.
Original W and gamma conventions are pinned in `inputs/S2_CANONICAL.md`; the
previous exact Legendre dictionary is pinned separately. No canonical equation,
frozen gate, abundance or measured parameter is changed.

## 1. Sources, admissible fields and the exact reduced potential

Let kappa=4 pi G, zeta=sqrt(kappa), and use one particle species of rest mass
m_*>0 and charge q_*=zeta m_*. Its counted mass density is rho=m_* n>=0,
physical mass current is j=rho v, and electric charge/current are zeta(rho,j).
There is no reference subtraction or conversion source in this construction.
Neutral baryons have a fixed mass distribution and Newtonian potential Phi_b;
they do not enter the dark charge current. Field stress, kinetic energy and
internal energy are omitted from Newtonian gravity's source at this order.

Put D=zeta P, so electric Gauss is precisely

    div P=rho,       rho_t+div j=0.

A vacuum region has rho=0, not necessarily P=0. In particular any compact
positive stock of mass M has total flux integral P dot dS=M; its spherical
exterior has P=M rhat/(4 pi r^2). No uncounted compensating charge is introduced.

Use full space with vanishing work/energy flux at infinity, or boundary
conditions supplying every integration-by-parts term. For the statements below,
P is square integrable, div P is a nonnegative integrable density with fixed
integral M, the displayed energies are finite, and kappa|P|<a0 almost everywhere.
For gamma>0 also require grad P square integrable. The admissible domain is
convex. The explicit point-source profile below is weak at its cusped origin;
that point of measure zero is not a claimed smooth relativistic core.

Decompose P=P_L+P_T by the full-space orthogonal Helmholtz decomposition,
with div P_T=0 and curl P_L=0. The dark Newtonian potential solves
Delta Phi_c=kappa rho, hence grad Phi_c=kappa P_L. Its self-energy is

    (1/2) integral rho Phi_c = -(kappa/2) integral |P_L|^2.

The reciprocal constitutive Hamiltonian satisfies the exact identity

    H(zeta P)=kappa |P|^2/2+W(kappa|P|),
    W(u)=[-a0^2 log(1-u/a0)-a0 u-u^2/2]/kappa,
    kappa W'(u)=u^2/(a0-u).

Electric energy plus rest-mass gravity therefore reduce to

    V[P]=integral {kappa |P_T|^2/2 + W(kappa|P|)
                   +gamma |grad P|^2/2 - grad Phi_b dot P}.       (1)

The external term is exactly integral rho Phi_b after integration by parts.
For point baryons their divergent fixed self-energy is excluded; it is not a
dynamical contribution to (1). The stiffness is the same
`gamma=kappa L*^2/2` in S2, counted once. This is the gravitational cancellation
at the assigned critical charge/mass ratio; it fails for a general charge/mass
ratio or extra uncharged gravitating matter.

For a given rho, P_T is an instantaneous electrostatic auxiliary variable:
minimize (1) subject to div P=rho. Where a minimizer exists, introduce lambda
with

    V_P = kappa P_T + kappa W'(kappa|P|) P_hat
          -gamma Delta P-grad Phi_b = -grad lambda.              (2)

This supplies the curl-free effective electric field condition. Equivalently
lambda=Phi_b+Phi_c+zeta phi with the electrostatic potential convention
E_eff=-grad phi. At gamma>0 the effective constitutive electric field includes
`-(gamma/zeta) Delta P`; it is not the derivative-free Le relation alone.
Existence and regularity of this auxiliary solution for every evolving density
are not assumed as a theorem.

## 2. Counted current dynamics and its Hamiltonian

It is incorrect in a general three-dimensional fluid to infer j=-P_t solely
from the two divergence equations. They imply only

    div(j+P_t)=0.

For a regular spherical radial flow with no point source, the integration
constant in r^2(j_r+P_t,r) vanishes, and j_r=-P_t,r does follow. In that restricted
sector the ordinary kinetic term is integral |P_t|^2/(2 rho). For a general
current, preserve j as an independent physical variable instead.

One local fluid lift of the reduced field potential is the first-order action

    S=integral dt [ integral { |j|^2/(2 rho)
            +theta(rho_t+div j)
            +rho alpha beta_t +alpha j dot grad beta
            +lambda(div P-rho)} -V[P] ].                         (3)

The Clebsch pair permits local vortical flow; a single patch does not assert a
global Clebsch chart on every flow topology. Varying j gives
v=grad theta-alpha grad beta. Varying theta, alpha, beta gives conservation of
rho and advection of the two labels. Variation of rho and these identities give

    rho_t+div(rho v)=0,
    v_t+(v dot grad)v=-grad lambda,                               (4)

together with Gauss and (2). Eliminating j in (3) produces the canonical kinetic
Hamiltonian, with physical total energy

    H=integral |j|^2/(2 rho)+V[P],    div P=rho.                   (5)

The kinetic perspective is nonnegative: it equals zero at (rho,j)=(0,0), and is
infinite if rho=0 but j is nonzero. A perturbation calculation dividing by rho
is restricted to occupied matter. Continuity conserves the counted stock and
preserves positivity for a regular material flow. Dust caustics and global
well-posedness are not resolved by this action.

For sufficiently regular closed solutions, the Euler/continuity equations give
`dK/dt=-integral lambda rho_t`, while (2) gives
`dV/dt=integral lambda rho_t`; hence H is conserved. This is an actual fluid
Hamiltonian and current constraint, not a time-derivative term added to a
static density by identification.

The collisionless alternative uses a nonnegative phase-space mass density
f(x,v), rho=integral f dv, j=integral v f dv. Its Hamiltonian is
`integral f |v|^2/2 dx dv+V[P]`, with the same field constraint. Its first
variation has one-particle energy |v|^2/2+lambda, yielding

    f_t+v dot grad_x f-grad lambda dot grad_v f=0.                 (6)

Equation (6) preserves positivity and the counted inventory along a regular
phase flow and conserves the displayed energy by phase-space integration by
parts. Its kinetic energy is at least integral |j|^2/(2 rho); equality holds for
a monokinetic flow. It accommodates a solenoidal physical current independently
of P_t. The cold equilibrium below is f0=rho0 delta(v), a stationary weak
phase-space measure; no smooth finite-dispersion equilibrium is claimed.

All these equations define a nonrelativistic instantaneous electrostatic lift.
They do not introduce propagating transverse gauge radiation or a current-free
Lorentz vacuum. In particular using P in the exterior is not an extension of
the carrier-defined U at zero density.

## 3. Convexity and the stiffness already supplied by S2

For 0<u<a0,

    W'(u)=u^2/[kappa(a0-u)],
    W''(u)=u(2a0-u)/[kappa(a0-u)^2].

The Hessian of W(kappa|P|) has radial and transverse eigenvalues

    h_rad=kappa u(2a0-u)/(a0-u)^2,
    h_tan=kappa u/(a0-u),                                       (7)

both positive. The function is globally strictly convex on |kappa P|<a0,
including its continuous zero-field value, although its Hessian vanishes at
P=0. The P_T and gamma terms add nonnegative quadratic forms; the external
baryon term is linear. Thus V is strictly convex on its convex admissible
domain. This yields energetic conclusions, not automatic coercivity in every
physical norm, a uniform spectral gap, or a relativistic characteristic cone.

With the stated boundary terms vanishing, the exact Hodge identity is

    integral |grad P|^2
      =integral {(div P)^2+|curl P|^2}.                           (8)

For radial/longitudinal P, curl P=0 and div P=rho, so the existing stiffness is
exactly the density energy gamma rho^2/2. Its effective barotropic pressure and
specific enthalpy are

    pressure_eff=gamma rho^2/2,
    enthalpy_eff=gamma rho,
    cs,NR^2=gamma rho.                                         (9)

No second arbitrary EOS or additional copy of this energy is added. Nonradial
configurations retain the positive curl contribution; P need not be curl free
in a nonlinear electrostatic solution. The interpretation is an effective
mean-field density stiffness, not a microscopic thermodynamic derivation.
At large gamma rho the nonrelativistic approximation itself needs checking.
A point baryon source is singular and (9) alone does not establish a finite
central density. A regular baryon core allows a regular local expansion, but
is an additional source choice requiring its own solution.

At a positive-density static solution, (4) requires lambda to be constant on
each connected resting occupied region. A spherically radial bulk then obeys

    gamma rho' = u^2/(a0-u)-gb,
    u=G m(r)/r^2,     m'=4 pi r^2 rho.                           (10)

Equation (10), not the gamma-zero algebraic law, is the finite-stiffness
free-boundary problem. In particular the gamma-zero profile has nonconstant
rho and does not solve (10) at gamma>0.

## 4. An explicit finite-stock equilibrium of the gamma-zero reduction

Let gamma=0, Phi_b=-G Mb/r with fixed Mb>0, and total carrier mass M=s Mb>0.
Set rM=sqrt(G Mb/a0), y=r/rM, and

    m_can(r)=Mb [sqrt(1+4 y^2)-1]/2,
    R=rM sqrt[s(s+1)],
    m0(r)=min{m_can(r),M},
    P0=m0(r) rhat/(4 pi r^2),     rho0=m0'/(4 pi r^2).           (11)

Thus the interior density is

    rho0=Mb/[2 pi rM^2 r sqrt(1+4y^2)]  for 0<r<R,

and it is zero for r>R. Its total mass and charge are finite and exactly M and
zeta M. P0 is continuous at R and has the nonzero Coulomb-flux exterior. There
is a density step but no surface mass/charge delta; the field normal flux does
not jump. The central density is cusped as 1/r, not a regular core. All terms
in (1) are finite after excluding the fixed baryon self-energy. The constitutive
argument approaches its capacity only at the singular point r=0; it remains
strictly inside the domain for every finite r>0.

Write u0=G m0/r^2 and

    F(r)=u0^2/(a0-u0)-G Mb/r^2,
    lambda0(r)=integral_r^infinity F(t) dt.                       (12)

Inside R, the canonical algebra gives F=0. Outside, let B=G Mb and A=G M=sB.
Then

    F(r)=A^2/[r^2(a0 r^2-A)]-B/r^2
        = B[(s^2+s)B-a0 r^2]/[r^2(a0 r^2-sB)] <0  (r>R).     (13)

Both denominators are positive because u0(R)=a0/(s+1)<a0. Therefore

    lambda0=mu<0 inside R,
    lambda0>mu outside R,     lambda0 increases to zero at infinity. (14)

The integrable exterior formula is also explicit. With ell=sqrt(A/a0),

    lambda0(r)= A/ell artanh(ell/r)-(A+B)/r  for r>=R,
    mu=lambda0(R).

It is the conservative effective particle potential; a particle of this same
critical charge/mass ratio needs at least -mu of additional specific energy to
escape from rest. No irreversible untethering, capture, frictional relaxation
or S4 reaction law is derived by this statement.

## 5. The free-support inequality and all-angle energetic minimum

P0 is longitudinal and satisfies the full field stationarity equation

    V_P[P0]=F(r) rhat=-grad lambda0.

For any other finite-energy admissible P with **any angular dependence**, rho=
div P>=0 and the same total mass M, convexity and integration by parts give

    V[P]-V[P0] >= integral V_P[P0] dot (P-P0)
               = integral lambda0 (rho-rho0)
               = integral (lambda0-mu) rho >=0.                  (15)

The last step uses (14), rho>=0, and lambda0=mu wherever rho0>0. This is the
outside-vacuum KKT inequality; the interior force equation alone would not have
sufficed. Boundary terms vanish with the declared decay, and lambda0 is finite
at the origin. Strict convexity makes P0 the unique finite-energy constrained
minimizer, modulo equality almost everywhere, among the stated admissible
fields. It is not merely a radial minimizer or an arbitrarily cut profile.

More precisely the exact relative energy is

    H-H0 = K + B_V(P,P0)+integral (lambda0-mu) rho,                (16)

where B_V=V[P]-V[P0]-integral V_P[P0] dot(P-P0) is nonnegative. Equation (16)
also holds with the nonnegative collisionless kinetic energy. It permits changes
of occupied support within the same inventory/domain; the added material in
an exterior empty region pays the nonnegative obstacle term. It does not divide
by the vacuum density.

For smooth tangent variations in occupied material with finite quadratic
energy, the bulk Hamiltonian is

    H2 = (1/2) integral |delta j|^2/rho0
         +(kappa/2) integral |delta P_T|^2
         +(1/2) integral deltaP dot Hess[W(kappa|P0|)] deltaP,
    delta rho=div deltaP,    delta rho_t+div delta j=0.           (17)

These terms are nonnegative in every angular sector. Material/free-boundary
variations are controlled most safely by the exact inequality (16), not by
extending 1/rho0 through vacuum. This is a global constrained **energetic**
minimum and, for existing closed solutions, a conserved relative-energy
control. It is not a proof of global smooth evolution, decay, a norm-independent
nonlinear stability theorem, a mode gap, or a relativistic halo solution.

For gamma>0 the same convex relative-energy argument holds at an actual
solution of (2),(4) with the required outside inequality lambda>=mu; its
quadratic form adds gamma integral |grad deltaP|^2/2. Existence, its free boundary
and its outside inequality must be proved for that solution. Substituting (11)
into the nonzero-gamma action cannot establish them.

## 6. The same finite-inventory theorem for an extended spherical baryon source

The point baryon is not essential to the gamma-zero minimum. Let B_b(r) be any
fixed nonnegative, nondecreasing enclosed baryon mass, with finite nonzero total
mass and a potential normalized to zero at infinity. At radii B_b>0 define

    m_can(r)=[sqrt(B_b(r)^2+4 a0 r^2 B_b(r)/G)-B_b(r)]/2.

It solves `m_can^2+B_b m_can=(a0/G)r^2 B_b`. Differentiating this relation yields

    (2m_can+B_b)m_can'
        =2(a0/G) r B_b+(m_can^2/B_b) B_b' >=0.

Set m_can=0 in any central interval with B_b=0. Thereafter it increases and
ultimately diverges linearly with r. Every finite M>0 therefore has a unique
outer crossing R with m_can(R)=M; clamping m0=min(m_can,M) gives a nonnegative
finite cold stock. Formulae (12),(14)--(16) are unchanged, with
`gb=G B_b(r)/r^2`. In the exterior,

    [u0^2/(a0-u0)]/gb
       =G M^2/[B_b(r)(a0 r^2-G M)].

This equals one at R and strictly decreases afterwards: both positive
factors in the denominator are nondecreasing and the second strictly increases.
Thus the same outside inequality holds, including variations of the occupied
support and arbitrary angular dependence of the cold perturbation. This is an
exact family of gamma-zero energetic minima for a prescribed physical baryon
profile; it introduces no neutral support stock or new dark equation of state.

For a regular positive central baryon density B_b is proportional to r^3;
then m_can is proportional to r^(5/2), so the cold density is proportional to
r^(-1/2). The point-source singularity is removed, but a smooth finite-density
cold core is still not proved in this gamma-zero limit. A finite-gamma core
requires its own equation (10) and boundary conditions.

## 7. Closure status and reproducibility

What is closed here is the counted nonrelativistic current lift and an explicit
finite-inventory global minimum for its gamma-zero canonical reduction. The
specified S2 stiffness supplies a fixed effective density energy rather than a
new fitted pressure input. Its actual finite-gamma equilibrium remains a
separate ODE/variational problem, and the relativistic material/vacuum interface
and dynamical baryon source remain open. The prescribed Mb, critical q/m,
constitutive W, supplied mass ratio and L* are inputs, not derived constants.

Exact algebra and bounded implementation checks are in `check_lift.py`, its
contract and recorded run. The universal variational conclusion is proved in
(12)--(16); a finite computation or count of passed checks does not replace it.
No data rescore, new empirical pass, asymptotic-attractor claim or full-theory
closure is made.
