# FGF034: constrained equilibrium response on fixed physical walls

2026-09-30. Exact conditional proof, derived without reading stage20 root or
independent-auditor work. No numerical experiment is used. This is the inherited
Q scalar/scale/fluid diagnostic wall model, not a physical metric completion.

## 1. Precisely fixed objects and the base gate

Fix the physical interval [0,D], D>0, total mass per transverse area M>0,
C=4piG, cs²>0, J>0, S0>0, and all positive physical kinetic coefficients.
Fix both endpoint values of phi and chi. No endpoint field-flux value is
additionally held fixed. Fluid walls are impermeable; their densities and
pressures need not be fixed along the branch. Let a=a_c exp(chi+lambda).
Use Q g=sqrt(B²+aB), with inverse B=b(g,a), on g=phi'>0.
Write A=b_g>0, q=−b_chi=gA−B, T=−W_chi, d=T_chi=2T−gq,
U=S0[cosh(2chi)−1]/4, and m=U''−d. T_g=q.

Assume ONE actual base local equilibrium (phi0,chi0,rho0,lambda0), smooth
on the closed interval, with phi0'>=gmin>0 and rho0>=rhomin>0. C2 fields
with bounded higher smooth constitutive compositions suffice for the estimates
below; taking smooth data is an explicit convenient regularity hypothesis.
Assume its exact fixed-mass full Q0 is bounded and coercive on H1_0 triples,
using fixed positive reference-unit scalings for position and each field:

 Q0[u]=integral {cs² r²/rho0+2r psi
    +(A psi'²−2q eta psi'+J eta'²+m eta²)/C} dx,
 r=−(rho0 xi)', u=(xi,psi,eta),
 Q0[u]>=c0 ||u||_(H1)^2, c0>0.                       (1)

This is the reviewed FGF033 gate, not an inference from mere strict positivity.
A matching reviewed FGF030 fixed-reference slab may be the base; its induced
M and wall values are then frozen ONCE. The FGF030 IVP family itself does not
already supply the constrained continuation proved here. No V or simultaneous
global driver equilibrium is assumed to construct this local branch.

## 2. Exact density elimination and its domain

Hydrostatic equilibrium says cs² log(rho/rho_*)+phi=h, spatially constant.
With mass fixed to M, this is equivalent to

 rho[phi](x)=M exp[−phi(x)/cs²]/Z[phi],
 Z[phi]=integral_0^D exp[−phi(s)/cs²] ds.              (2)

Thus density is not frozen. Its derivative in a potential direction psi is

 r_psi=−rho/cs² (psi−<psi>rho),
 <psi>rho=(1/M) integral rho psi dx,  integral r_psi=0. (3)

The derivative of the normalizing denominator is essential. Dropping the
weighted mean changes the mass constraint and the operator below.

At the base the map xi -> r=−(rho0 xi)' is a bounded bijection
H1_0(0,D) -> L2_0(0,D), where L2_0 has zero ordinary integral. Its inverse is

 xi(x)=−[1/rho0(x)] integral_0^x r(s)ds.              (4)

Both endpoints vanish exactly because integral r=0; rho0 positive and W1,infinity
make the inverse bounded. If integral r is nonzero, the right trace is
−(integral r)/rho0(D), so it cannot represent an impermeable-wall perturbation.
This establishes the displacement/density correspondence rather than assuming it.

## 3. Nonlinear map and actual inverse gate

Use affine field spaces phi=phi0+v, chi=chi0+w, with
Y=(H2(0,D) intersect H1_0(0,D))², and target Zspace=L2(0,D)².
Use fixed unit weights in these product norms. In one dimension H2 embeds
continuously into C1; choose an open neighborhood where phi'>gmin/2.
Define the nonlinear residual, including its normalization (2), by

 F1(phi,chi,lambda)=rho[phi]−(1/C) partial_x b(phi',a_c exp(chi+lambda)),
 F2(phi,chi,lambda)=[−J chi''+U'(chi)−T(phi',a_c exp(chi+lambda))]/C. (5)

F=0 is exactly the static field/scale system with hydrostatic fluid and fixed
mass. Smooth constitutive functions on g>0,a>0, the H1 algebra property in
one dimension, and the positive denominator Z[phi] imply this map is C1
from the stated open Y neighborhood times R into Zspace. More explicitly,
its differentiated flux is a smooth coefficient of (phi',chi,lambda) times
phi'' plus another smooth coefficient times chi'; H2 perturbations control
those coefficients uniformly and the second derivatives in L2. The exponential
and its integral denominator are continuously differentiable there. Thus no
unsupported Nemytskii map on bare H1 is being used.

At the base its field derivative is

 Lred(psi,eta)=(r_psi−(A psi'−q eta)'/C,
                        [−J eta''+m eta−q psi']/C).  (6)

Its weak symmetric form on H1_0 pairs is

 Qred[psi,eta]=integral(A psi'²−2q eta psi'+J eta'²+m eta²)/C
                  −(1/cs²) integral rho0(psi−<psi>rho0)². (7)

Indeed minimize the fluid part of Q0 over r in L2_0. Its Euler equation is
cs²r/rho0+psi=constant, uniquely giving (3). The minimized value is the
negative weighted variance in (7), and (4) realizes the minimizer by an
admissible xi_psi. Therefore

 Qred[psi,eta]=Q0[xi_psi,psi,eta]
               >=c0 (||psi||_H1²+||eta||_H1²).       (8)

The reduced form is bounded and coercive on H1_0 pairs. This verifies the
nonlocal derivative's positivity; it is not a frozen-fluid approximation.

For any L2 pair f, the bounded coercive form has a unique H1_0 weak solution
with norm controlled by ||f||_L2. This can be formulated directly as the
unique minimizer of Qred[y]/2−<f,y>; coercivity gives bounded minimizing
sequences and weak lower semicontinuity, strict convexity gives uniqueness.
The second equation of (6) then gives eta'' in L2. The first gives
(A psi'−q eta)' in L2. Since A is bounded below and A,q are W1,infinity,
psi' is H1 and psi is H2. These equations give

 ||psi||_H2+||eta||_H2 <= Cbase ||f||_L2,              (9)

using the preceding H1 estimate, bounded coefficients and fixed D. Hence
Lred:Y -> Zspace is a bounded isomorphism, with an actual H2 inverse.
Uniqueness is already supplied by (8); no extra independent boundary
conditions or discarded Dirichlet compatibility term are introduced.

Now write y=(v,w) and consider y -> y−Lred^(-1)F(phi0+v,chi0+w,lambda).
Its y derivative vanishes at (0,lambda0). Continuous differentiability makes
its derivative norm at most1/2 on a sufficiently small ball; taking lambda
sufficiently near lambda0 also makes the center displacement at most half
the ball radius. The map is then a self-map and contraction, giving a unique
nearby solution. Its derivative operator remains invertible by the same
small-operator bound; taking difference quotients in F=0 gives a continuous
lambda derivative. This supplies a local C1 equilibrium branch in Y with
fixed walls, mass, physical coefficients and D. Neighborhood size is not
computed. Positivity of phi' persists by H2 -> C1, and density is positive
by (2), with a uniform positive lower bound after shrinking the neighborhood.

## 4. Full susceptibility and the global margin

Let a0(u,v) be the symmetric polarization of the ORIGINAL full Q0, not its
reduced field form, and define

 ell[v]=−(1/C) integral(q psi_v'+d eta_v) dx,
 a0(z,v)=ell[v] for every v in H1_0 triples,
 beta=ell[z]=Q0[z]>=0.                               (10)

Coercivity supplies unique z. Since ell has no fluid component, its fluid
Euler equation makes z's density component the exact minimizer (3) associated
with psi_z. Thus the reduced solution lifts to the full displacement space.

Differentiating (5) with respect to lambda at fixed fields gives
F_lambda=(q'/C,−d/C). Its pairing with zero-trace field variations is exactly
ell. Differentiating the actual branch and using (3),(4) therefore gives

 u_lambda=(xi_lambda,phi_lambda,chi_lambda)=−z.        (11)

There is no field endpoint term: phi_lambda and chi_lambda have zero traces.
Define, along this local constrained branch only,

 R(lambda)=(1/C) integral T(partial_x phi(x;lambda),
                                      a_c exp(chi(x;lambda)+lambda))dx.

Its derivative is unambiguously

 R'=(1/C) integral[d+q (partial_lambda phi)'
                             +d partial_lambda chi]dx
    =(1/C) integral d dx−ell[u_lambda]
    =(1/C) integral T_chi dx+beta.                   (12)

The explicit-reference derivative is NOT the total branch derivative. The
response contribution beta is nonnegative, but the explicit integral d may
have either sign; no assertion R'>0 is inferred from beta>=0 alone.

If an independently specified single V has an ACTUAL intersection V'=R at
some point on this branch whose matched form is coercive, FGF033 gives

 Delta=V''−integral d/C−beta=V''−R'.                  (13)

Delta>0 is the positive full-form criterion with positive kinetics, Delta=0
has the neutral linear mode, and Delta<0 has its one negative direction.
No such V or intersection is supplied here. A zero margin alone does not
establish a fold, hysteresis, nonlinear stability or cosmological tracking.
The same statements apply pointwise on a sufficiently small branch where
coercivity persists: the coefficients and rho depend continuously in the
norms controlling the form, so a strict base margin remains positive locally.

## 5. Why the old IVP derivative is not this response

The FGF030 left-IVP family holds left data and length fixed while reference
changes; its right phi/chi values and total mass M(lambda) are induced and
vary. At fixed D its hydrostatic density derivative is instead

 r=r_psi+rho M'/M,                                   (14)

with the mean in (3) formed using that family's density and mass. Its integral
is M', not zero. Formula (4) would give xi(D)=−M'/rho(D), generally nonzero.
Moreover psi(D)=partial_lambda phi(D) and eta(D)=partial_lambda chi(D) are
generally nonzero. Thus the family derivative lies outside the fixed-domain
triple space used in (10); substituting it for −z is unjustified.

The explicit boundary/mass work can also be seen without a displacement.
For any smooth local equilibrium family on fixed [0,D], let Epot be the
original static fluid+field energy per area and h=e'(rho)+phi, constant in x.
Its first derivative is

 Epot'=h M'+[B psi/C+J chi' eta/C]_0^D−R.            (15)

The bulk Euler terms cancel on equilibrium. This follows directly by varying
integral[e(rho)+rho phi+(W+J chi'²/2+U)/C]; integration by parts produces
the displayed field boundary work and the mass multiplier term. For the
constrained branch, M'=psi|walls=eta|walls=0, so Epot'=−R. For the old IVP
family these terms cannot be discarded. Differentiating (15) again retains
their derivatives, obstructing substitution of its energy curvature for
−R' of the constrained branch. No moving-wall term is needed here because
D is fixed; a moving D would introduce yet another endpoint contribution.

The same distinction appears in MOND source balance:
B(D)−B(0)=C M. The constrained branch has delta B(D)−delta B(0)=0;
the old family has that difference equal to C M'. Neither requires each
endpoint flux itself to be fixed. If evolved dynamically, the source law is
P_x=C rho+tau phi_tt, with P=b(|phi_x|,a) sign(phi_x), not the static formula.

## 6. Controls, reference bookkeeping and remaining gap

- Dropping the normalization derivative in (3) loses zero-integral density
  and changes both the nonlinear inverse gate and beta.
- Formally ell=0 gives z=0 and R'=integral d/C; beta is a response correction,
  not an extra independently fitted coefficient.
- The full positive Q0 gate is essential; invertibility or nonlinear branch
  continuation at a zero or negative mode is not proved by this argument.
- Imposing zero endpoint flux in addition to fixed phi is a different
  overconstrained problem; it is not part of the theorem.
- The old IVP derivative fails the declared mass/wall domain unless its
  induced derivatives happen separately to vanish; this is a domain control,
  not evidence that the old IVP computation was erroneous.

Keep a_c=9.3619e-11 m/s² and the alternative reference 1.1279e-10 as distinct
choices (lambda0=0 or log of their ratio); frozen H comparisons add log E(z),
E²=.315(1+z)^3+.685, with physical coefficients and units unchanged. The local
neighborhood around one base does not prove a connected branch between these
reference choices. Constant vacuum is a separate physical hypothesis; an
actual time-dependent H trajectory is not this static lambda continuation.
The actual a=a_c exp(chi+lambda) remains a diagnostic varying scale and does
not establish a literal pointwise constant-vacuum identity.

No RAR or registered M action is invented from the Q proof. No acceleration
or missing mass is estimated; source balance is explicitly the MOND Q flux.
The operative filtered-MONO/physical metric/photon problem, local covariant
sector, empirical calibration and nonlinear/global closure remain open.
The next substantive gate is an independently justified V and an actual
intersection, rather than a fitted desired slope or another formal response
calculation. This proof provides a conditional local susceptibility theorem,
not that missing physical potential or a global branch diagram.
