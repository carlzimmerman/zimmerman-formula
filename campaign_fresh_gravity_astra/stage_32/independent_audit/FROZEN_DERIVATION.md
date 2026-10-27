# FGF045 independent derivation, frozen before author/new-root exposure

This is a proof-only derivation from the task and pinned old ancestry. No new
FGF045 author or stage-32 root proof, result, preview or conclusion was read.
No literature theorem, numerical experiment, or existence theorem is imported.

## Claim card and domain

Write c=cs>0, q=n/nref with fixed density nref>0, and g=phi0_x.
On a fixed closed regular interval U=[a,b] on the positive side of the signed-Q
crossing, g is C1, rho is positive and smooth, and c²(log rho)_x=-g.
Let G0=sup_U |g| and G=sup_U |g'|. They are finite, independent of N; G need
not be positive and no sign of g' is assumed. Both a0 background choices are
handled separately with their own constants.

The exact initial data are n=rho and v=V f((x-x*)/ell), with V=v0 N,
ell=L/N³, f(y)=(1-y²)² for |y|<1 and zero otherwise. f is C1,1, not C2 at
its endpoints. Fix x* strictly inside U and take N large enough for the whole
initial support to lie inside U. The conclusion below is conditional on an
actual positive-density C1 solution of the stated fluid equations; it rules
out any such solution covering the specified characteristic neighborhood up
to a time t_N=O(N^-4). It does not construct a solution or a maximal extension.

## Characteristics, exact gradients and density weight

Define R=v+c log q, S=v-c log q, Dplus=partial_t+(v+c)partial_x,
Dminus=partial_t+(v-c)partial_x, alpha=R_x, beta=S_x. Direct substitution gives

 Dplus R=-g, Dminus S=-g,
 Dplus alpha=-(alpha+beta)alpha/2-g',
 Dminus beta=-(alpha+beta)beta/2-g'.                       (1)

Also Dplus log q=-beta and Dminus log q=-alpha. Hence, with
r=q^-1/2, y=r alpha, z=r beta,

 Dplus y=-y²/(2r)-g' r,
 Dminus z=-z²/(2r)-g' r,
 (partial_t+v partial_x)r=(y+z)/4.                       (2)

Pressure remains in the two characteristic speeds, initial alpha,beta and
weight cancellation. Equations (2) are not pressureless dynamics.

No C2 solution is needed to justify (1). For the C1 characteristic flow X,
its label Jacobian J obeys J_t=v_x(t,X)J. Differentiate the integrated identity
R(t,X)=R(0,label)-integral g(X)dt with respect to its label. This yields an
ODE for alpha(t,X)J and therefore the stated continuous-gradient ODE. The
same argument applies to S. The C1,1 endpoints do not create distributions.

## Local characteristic domain

Let H0=sup_U |c log(rho/nref)|, fix any small physical time t0>0, and choose
M_N=V+H0+c+G0 t0+epsilon_v, with fixed epsilon_v>0 in velocity units. Consider
D_N={0<=t<=t0, a+M_N t<=x<=b-M_N t}. The initial invariant bounds and (1)
give |R|,|S|<=V+H0+G0t, thus |v|+c<M_N, on this domain by the usual first-exit
characteristic argument: backwards curves stay in D_N and meet its initial
base, never a side. The strict margin closes the speed bootstrap. Material
curves also have this property. This is a local domain-of-dependence statement,
not a claim that the initial support remains invariant.

A plus-characteristic starting at x_c=x*+ell/sqrt(3) remains inside D_N
provided 2M_Nt is smaller than dist(x_c,{a,b}). Since our t_N=O(N^-4) and
M_N=O(N), its whole domain stays within U for all sufficiently large N.
No crossing cusp, physical wall, wall datum or incoming-wall assumption enters.

## Closed envelopes including arbitrary bounded force derivative

Let R0=max_U sqrt(nref/rho)>0 and
Y0=max(0,sup_U y(0),sup_U z(0)). For large N, Y0>0.
On D_N, define nonnegative comparison envelopes Rbar,Ybar by

 Rbar'=Ybar/2, Ybar'=G Rbar, Rbar(0)=R0, Ybar(0)=Y0.       (3)

Then r<=Rbar and y,z<=Ybar. Indeed (2) gives Dplus y<=G r,
Dminus z<=G r and material r_t<=(y+z)/4; their integrated characteristic
inequalities and a strict-envelope/first-crossing argument close simultaneously.
This bounds the positive parts only; it does not assume compression is bounded.
For k=sqrt(G/2),

 Rbar(t)=R0 cosh(kt)+Y0 sinh(kt)/(2k),                    (4)

using the continuous k=0 limit. Choose t0 small enough that cosh(kt)<=2 and
sinh(kt)/(kt)<=2 on [0,t0]. Then the simpler bound

 r<=B_N(t):=2R0+Y0 t,   n>=nref/[B_N(t)]²                (5)

holds. The invariant bounds separately give finite upper and lower density
bounds for each fixed N; (5) supplies the useful N-uniform lower bound on
our N^-4 interval. No source sign or external density hypothesis was added.

## Compression and conditional lifespan contradiction

At x_c, f'=-8/(3sqrt(3)). Put A_N=8v0 N4/(3sqrt(3)L). Hydrostatics gives
alpha(0,x_c)=-A_N-g(x_c)/c. Thus w0=-y(0,x_c)>0 and w0 is asymptotic to
A_N sqrt(nref/rho(x*)). Likewise Y0 has this same leading asymptotic, because
the positive maximum of f' is equal in magnitude and background factors vary
by O(ell) across the initial patch. In particular Y0/w0 tends to one and lies
between 1/2 and 2 for all sufficiently large N.

Along that plus-characteristic write w=-y. Equation (2) and (5) give

 w'>=w²/(2B_N(t))-G B_N(t),
 w(t)>=w0-G integral_0^t B_N(s)ds.                       (6)

Define the explicit dimensional time

 t_N=(2R0/Y0)[exp(4Y0/w0)-1].                            (7)

It is positive and O(L/(v0 N4)), with constants depending on the fixed
background/density normalization. Choose N large enough for localization,
t_N<=t0, and G integral_0^t_N B_N(s)ds<=w0/8. These are explicit sufficient
large-N gates: the last left side is O(N^-4), its right side O(N4).
Then w>=7w0/8, so in particular w>=w0/2 throughout hypothetical survival.
For h=1/w,

 h'<=-1/[2B_N(t)]+4G B_N(t)/w0².

But integral_0^t_N [2B_N(t)]^-1 dt=2/w0 by (7). Therefore

 0<h(t_N)<=1/w0-2/w0+1/(2w0)=-1/(2w0),                  (8)

a contradiction. Every density coefficient and force term used in this bound
has been controlled. No N-independent positive-density C1 evolution exists
on a fixed neighborhood containing the resulting characteristic cone for all N.

Precise qualification: this is a conditional upper bound on classical
survival, not local existence or a continuation theorem. If a positive C1
solution is present until the Riccati obstruction, its weighted compression
cannot remain finite. Bounds (5) and the finite-N invariant bound exclude
vacuum and unbounded density on this time slab. Any claim about the endpoint
of a *maximal* solution additionally needs a local existence/continuation
argument; failure of that unproved gate must not be called a proven singularity.

## Exact fluid energy and stationary control

For e(n)=c² n[log(n/nref)-1], define
E=nv²/2+e(n)+n phi0 and F=nv[v²/2+c²log(n/nref)+phi0].
Multiplying the exact momentum equation by nv, using exact continuity and
e'(n)n-e(n)=c²n gives E_t+F_x=0. The force term -nv g is canceled by the
fixed-potential contribution (n phi0)_t+(nv phi0)_x=nv g. Thus d integral E/dt
=-[F] at fixed boundaries, conditionally conserved under appropriate zero flux.
We assert no global-wall solution or boundary compatibility beyond that identity.
Hydrostatics makes mu=c²log(rho/nref)+phi0 constant, so at equal total mass
integral(E-E_background)=integral[nv²/2+c²(n log(n/rho)-n+rho)].
Its conservation is conditional on an actual smooth fluid solution and zero
mass/energy flux, not an existence certificate.

With v=0,n=rho, both fluid PDEs hold and energy flux is exactly zero. Freezing
the old MOND fields nevertheless leaves source residual C(n-rho) for changing
density. Exact forced fluid momentum does not repair that field source residual.

## Units and exclusions

N,q,r,f are dimensionless; L,ell are lengths; v0,V,c velocities; y,z,Y0,w0
are inverse times; g' and G are inverse times squared. All times in (7) have
physical units. Density normalization cancels between ratios/constants and is
not a free physical prediction. No empirical/source mass conversion is made.
The adopted a=kappa c_light sqrt(G_Newton rho_Lambda) and separate backgrounds
9.3619e-11 and 1.1279e-10 m/s² are retained. Constant vacuum and fixed/frozen-H
references give separate static backgrounds; evolving H is not solved. No
transfer to coupled gravity, RAR/M/filtered MONO, physical reservoir, metric,
photons, degree count, observations, novelty or theory closure is asserted.

## Provenance and unsuccessful routes

The first considered unweighted gradients retain the mixed alpha beta term,
so compression alone does not close. Invariant density bounds alone scale
exponentially in N and do not justify N^-4. A constant lower coefficient plus
a short-time density envelope can produce a circular insufficient lifespan
estimate; integrating the variable coefficient in (6) avoids that failure.
These were analytic discarded estimates, not computations or counterexamples.
All eight task ancestry hashes were checked and matched before freezing.
Administrative note: source texts were initially opened before the separate
hash-check command; no hash mismatch was found and no premise changed.
