# PF04–PF05: coupled metric junctions and native layers

Base 59cbc01d7c; criteria f53b83d55a. New results below are restricted statements,
not a proof that AC2q must form a singularity from smooth data.

## Exact plane-symmetric reduction

Take ds^2=e^(2alpha)(-dt^2+dx^2)+e^(2beta)(dy^2+dz^2). Define rapidity theta,
n=e^-alpha(cosh theta,sinh theta,0,0), e=e^-alpha(sinh theta,cosh theta,0,0),
and P^mu=P e^mu. Direct four-dimensional contractions give

    D.P=e^-alpha[sinh theta(P_t+2P beta_t)
                   +cosh theta(P_x+2P beta_x)],
    P.A=P e^-alpha[cosh theta theta_t+sinh theta theta_x
                   +sinh theta alpha_t+cosh theta alpha_x].

The scalar curvature is

    R=e^-2alpha[-2 Box alpha-4 Box beta-6(partial beta)^2],

with Box=-partial_t^2+partial_x^2 and Minkowski contraction. After integration
by parts, the Einstein density per unit transverse coordinate area is

    L_G=Mpl^2 e^(2beta)[2 partial alpha.partial beta+(partial beta)^2].

The matter density, modulo the covariant divergence from P.A, is

    L_m=e^(2alpha+2beta) F(D,X,P,phi),
    F=-D+X-V-W-gamma/2{max(D+2X,0)^2-(2X)^2}.

The omitted conformal-gauge Einstein constraints are still necessary for an
actual solution. Our junction exclusions use only necessary reduced variations;
adding the missing constraints cannot rescue a corner already excluded by them.

## The metric cannot supply the regular corner's missing impulse

Consider a stationary timelike interface with stationary alpha,beta,P profiles
and phi=s t+psi(x), fixed finite s>0 and gamma>0; continuous alpha,beta,phi,P,
a uniformly nondegenerate metric, bounded one-sided derivatives and bounded
potential sources, without an added
surface action or an unresolved concentration defect. Let phi=s t+psi(x),
v=-psi'/s, C=(1-v^2)^-1/2, B=2X=e^-2alpha s^2(1-v^2), and
D=e^-alpha C(P'+2P beta'). On either branch set the normal conjugate fluxes
pi_i=partial L/partial i'. On the on-branch,

    pi_P=-e^(alpha+2beta) C[1+gamma(D+B)],
    pi_alpha=2 Mpl^2 e^(2beta) beta',
    pi_beta=2 Mpl^2 e^(2beta)(alpha'+beta')+2P pi_P.

The last identity holds on the off-branch too. It is the native metric coupling
that was absent from the flat calculation. The variational corner conditions
require these fluxes to be continuous. Since P and pi_P are continuous, they
imply [beta']=0 and [alpha']=0. The metric jump matrix has determinant
-4 Mpl^4 e^(4beta), which is nonzero. Thus an ordinary metric derivative jump
cannot independently absorb the mismatch while satisfying the native equations.

Set ell=P'+2P beta'. The total spatial Hamiltonian is the gravitational one
plus v L_m,v+ell L_m,ell-L_m: the 2P beta' pi_P terms cancel exactly.
The gravitational contribution is continuous, and all metric coefficients are
common at the interface. With s_local=e^-alpha s, the remaining matter corner
is precisely PF02's local problem. Its strict-convexity obstruction therefore
extends to this coupled regular planar class for 0<gamma*s_local^2<1/3 and
same-sign nonzero through-flow velocities. Stationarity of the interface alone
is insufficient: for evolving fields D also contains
e^-alpha C v(P_t+2P beta_t). That tangential contribution is absent from the
stationary-profile reduction and must not be silently dropped. This is stronger than a fixed-metric
argument, but still not a theorem about every singular weak spacetime.

## The negative-divergence loophole must be checked, not ignored

The positive-part square penalizes large positive D+2X. It does NOT directly
penalize a large negative divergence. A proposed negative polarization sheet
therefore cannot be rejected by citing the stiffness square alone.

For a stationary thin layer with uniformly bounded metric first derivatives,
bounded explicit potential derivatives, bounded temporal variation of currents,
a uniformly nondegenerate metric, fixed finite s>0 and gamma>0, and fixed
limiting endpoints strictly inside the positive-charge branch, normal field fluxes stay
bounded across a layer of vanishing thickness. Write

    A=-pi_P/e^(alpha+2beta)=C[1+gamma max(D+B,0)].

To leading order across a continuous regular metric, A has a common limit >1, with a uniform gap A>=1+delta for some delta>0.
Merely positive endpoint charge for each layer width, tending to zero in the
limit, would not suffice.
On the positive branch this bounds q_+=max(D+B,0); thus P' is bounded if X and
other fields remain bounded. On the off-branch C=A, so

    |v|=sqrt(1-A^-2)>0.

The scalar normal current on that branch is

    pi_phi = e^(alpha+2beta) v C^3(P'+2P beta')/s
               +e^(2beta) s v(1+2gamma B).

The coefficient of P' is nonzero. A delta contribution to P' would create a
normal delta current and hence a delta-prime in its divergence, without a source
to cancel it. Equivalently the bounded normal current solves algebraically for
a bounded P'. Thus a quasi-stationary negative sheet cannot provide the missing
stress under these uniform bounds. The v=0 exception requires A=1 and cannot
match the strictly on-branch endpoints. Uniform timelike separation and finite
s are essential; no bound is claimed as X approaches zero.

This reasoning does not cover a rapidly time-dependent layer: time derivatives
of currents can then balance large spatial derivatives. It also does not cover
unbounded metric gradients, an approach to the hold-law cap, or an oscillatory
weak limit. Those are physical/mathematical dependencies, not suppressed terms.

For compact interior endpoint P values, a finite excursion to the cap and back
requires finite positive variation on at least one leg. If metric derivatives
and X stay bounded, Cauchy–Schwarz makes the positive stiffness integral grow
at least as excursion^2/layer_width. This excludes such an excursion only for
families with a uniformly bounded positive stiffness integral. Finite signed
total action alone is not that bound; gravitational/matter cancellations must
not be used to assert coercivity without proof.

## A hidden tensor wave is not automatically a carrier in this symmetry

Allow transverse anisotropy h: g_yy=e^(2beta+2h), g_zz=e^(2beta-2h).
The four-dimensional reduction adds -Mpl^2 e^(2beta)(partial h)^2 to L_G.
D, X and W in the x-polarized planar sector do not depend on h. Its equation is

    partial_t(e^(2beta) h_t)-partial_x(e^(2beta) h_x)=0.

For a regular positive coefficient e^(2beta), zero tensor data remain zero by
the usual wave-energy uniqueness argument. Scalar plane-symmetric data therefore
do not have an independent sourced tensor channel that can simply be assigned
the lost shock energy. Singular coefficients, nonzero tensor data, and loss of
uniqueness at the interface are outside this statement.

## Checks and retained failure

metric_junction.py/main001 failed one comparison because its left side still
used d=P' while its right side used ell=d+2P beta'. The v2 comparison substitutes
the same variable on both sides; equations and criteria are unchanged. main002
passes 10/10 identities. Removing 2P beta' breaks the current-coupling identities;
changing the Einstein transverse coefficient breaks the curvature-compatible
junction identities. layers001 passes 9/9 algebraic checks. These counts support
the displayed algebra; the uniform-bound arguments are separate internal proofs.
No universal weak-solution uniqueness or full smooth-data breakdown is claimed.
