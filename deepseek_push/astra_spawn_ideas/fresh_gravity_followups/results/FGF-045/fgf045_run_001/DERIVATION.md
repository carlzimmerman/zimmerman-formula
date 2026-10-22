# FGF045: a localized conditional C1 lifespan obstruction for actual isothermal momentum

Proof-only author derivation, /root/fgf045_author. No new stage32 root or
reviewer files were read. All eight task ancestry hashes matched before use.
This is the task's fixed-potential diagnostic, not coupled field evolution.

## 1. Claim card, background and unchanged data

Fix one inherited signed-Q background, with C=4piG,
B0_x=C rho, g0=phi0_x=sgn(B0)sqrt(B0^2+a|B0|),
a=a_ref exp(chi0), and c_s^2 rho_x=-rho g0. Choose the prescribed regular
positive-side x*, and a closed interval K0=[x*-R,x*+R] in an open regular
neighborhood U whose closure avoids the crossing and physical walls. Shrink
R if necessary, but do not move x* or change the data. On U, rho>0 and
g0,rho are smooth; in particular the constants below are finite. The
regularity at the excluded zero-flux crossing is not used. Set c=c_s>0 in
this derivation only; the vacuum relation's light speed is denoted c_light.

For fixed dimensional L,v0>0 and dimensionless positive integer N, retain
exactly

 ell=L/N^3, V=v0 N, omega=V/ell=v0 N^4/L,
 f(y)=(1-y^2)^2 for |y|<1, and f(y)=0 otherwise,
 n(0,x)=rho(x), v(0,x)=V f((x-x*)/ell).                 (1)

No smoothing or replacement profile is made. f is C1,1 with jumps in f''
at +/-1, not C2. The maximal derivative magnitude is

 d=max |f'|=8/(3 sqrt(3)),  f'(1/sqrt(3))=-d.           (2)

The equations to be satisfied are the actual two fluid equations

 n_t+(nv)_x=0,
 v_t+v v_x+c^2(log n)_x=-g0(x).                         (3)

Quantified conclusion: constants B>0 and N0, depending only on the fixed
background, U,R,L,v0,c and a positive density reference n_ref, are defined
below. For every N>=N0 there is no positive-density C1 solution of (3) with
(1) on [0,B/omega] x U. The proof uses only a shrinking characteristic domain
strictly inside K0, and bounds the relevant characteristic displacement by
O(N^-3). Thus the same conclusion holds whenever a proposed evolution covers
that domain and its initial interval. No positive N-independent time slab
on U can support all sufficiently large N.

This is an a priori nonexistence-through-time / conditional lifespan upper
bound. No local existence, uniqueness, maximal-solution continuation theorem,
or post-breakdown solution is supplied. In particular it is not an assertion
that the initial state fails to have any short-time classical evolution.

## 2. Exact characteristic identities, including pressure

Let q=log(n/n_ref), r=v+cq, s=v-cq, and D0=partial_t+v partial_x,
D+=partial_t+(v+c)partial_x, D-=partial_t+(v-c)partial_x. From (3),

 D0 q=-v_x,   D0 v=-c^2 q_x-g0,
 D+ r=-g0,    D- s=-g0.                                (4)

The sound speeds +/-c arise from the retained pressure; they have not been
set to zero. Put alpha=r_x, beta=s_x, so v_x=(alpha+beta)/2. Then

 D+ alpha=-(alpha+beta)alpha/2-g0',
 D- beta =-(alpha+beta)beta /2-g0',
 D+ q=-beta,  D- q=-alpha.                             (5)

These identities hold along characteristics for C1 solutions without assuming
second spatial derivatives. To justify the first, let X_+(t,a) be the C1
flow of v+c and J=partial_a X_+. Differentiating the integrated first equation
in (4) gives
alpha(t,X_+)J=alpha(0,a)-integral_0^t g0'(X_+)J du,
while J_t=v_x(t,X_+)J. Division and differentiation in time yield (5).
The minus equation is identical with s and X_-. Local flow uniqueness follows
from the assumed C1 velocity; this does not construct the unknown PDE solution.

The raw mixed product alpha beta has no fixed favorable sign. It cancels
exactly after a density weight. Define

 h=n^(-1/2)>0, y=h alpha, z=h beta.

Since D+ h=h beta/2 and D- h=h alpha/2, (5) gives

 D+ y=-y^2/(2h)-g0' h,
 D- z=-z^2/(2h)-g0' h,
 D0 h=(y+z)/4.                                        (6)

Here h has units inverse square root of mass density, y,z have units h/time,
and g0' has units 1/time^2. In particular both terms in each weighted gradient
equation have units h/time^2. Formula (6) is exact, not a limiting pressureless
equation. All force terms remain present, with no assumption that g0'>=0.

## 3. A local characteristic cone with no wall or invariant-support premise

All maxima in this paragraph are on K0. Define

 G0=max |g0|, G1=max |g0'|, Q0=max |log(rho/n_ref)|,
 h0=max rho^(-1/2), hmin=min rho^(-1/2)>0.

G0 and G1 are force bounds, not the gravitational constant G in C=4piG.
Fix any physical comparison time tau>0, independent of N. Set

 S_N=V+c Q0+G0 tau+2c,
 K_t=[x*-R+S_N t, x*+R-S_N t].                          (7)

For t<=tau and before K_t becomes empty, the Riemann equations imply in this
cone

 |r|,|s|<=V+c Q0+G0 t,
 |v|+c<=V+c Q0+G0 t+c < S_N.                           (8)

For completeness this is a bootstrap, not an assumed speed bound: initially
the bound |v|+c<S_N is strict. As long as it holds, every backward +/-
characteristic from K_t remains in the earlier K_u, because the lateral
boundaries move inward at the faster speed S_N. Integrating (4) gives (8),
with at least c strict margin for t<=tau. A first loss of the speed bound is
therefore impossible on any compact positive-C1 existence slab. The same
backward-cone containment holds for material characteristics of speed v.
Thus the estimates below depend solely on the initial data in K0. No signal
from a crossing, a wall, or the exterior of K0 is used.

These bounds also imply, for each fixed N,

 |q|<= (V+c Q0+G0 tau)/c,
 n_ref exp[-(V+c Q0+G0 tau)/c] <= n
 <= n_ref exp[(V+c Q0+G0 tau)/c].                       (9)

The lower bound will be improved below. The upper bound need not be uniform
in N. A solution is not assumed stationary outside the original bump, and
its later support need not remain in (x*-ell,x*+ell).

## 4. Upper weighted-gradient envelope bounds inverse density

Initially, hydrostatic balance implies q_x=-g0/c^2, hence

 alpha0=omega f'((x-x*)/ell)-g0/c,
 beta0 =omega f'((x-x*)/ell)+g0/c.                     (10)

Take fixed positive constants

 A=2d h0,   b=d hmin,
 B=(h0/A)[exp(8A/b)-1],   T_N=B/omega,
 Hstar=h0+A B.                                       (11)

B is dimensionless, A,b have units h, and Hstar has units h. These constants
are deliberately conservative and finite; no sharp lifespan coefficient is
claimed. Set N0 sufficiently large that for all N>=N0,

 omega >= G0/(c d),
 T_N<=tau,
 ell+2 S_N T_N<R,
 G1 Hstar B < A omega^2,
 b omega > 2 sqrt(G1) Hstar.                         (12)

If G1=0, the last two inequalities are automatic (the last right side is 0).
All five requirements hold for sufficiently large N: omega grows as N^4,
S_N as N, and ell+2 S_N T_N=O(N^-3). Thus (12) is a genuine asymptotic
threshold with dimensional constants, not a numeric parameter scan.

Define at each time in the cone

 M(t)=max(0, sup_{K_t} y(t,.), sup_{K_t} z(t,.)),
 H(t)=sup_{K_t} h(t,.).

Equation (10) and the first threshold give M(0)<=A omega. Dropping only the
nonpositive quadratic terms from (6), and integrating backward characteristics
within the cone, gives exact inequalities

 M(t)<=A omega+G1 integral_0^t H(u) du,
 H(t)<=h0+(1/2) integral_0^t M(u) du.                 (13)

In particular on every positive-C1 existence slab through t<=T_N,

 M(t)<2A omega,       H(t)<=h0+A omega t<=Hstar.       (14)

A first-contact proof is enough: before M first reaches 2A omega the second
inequality of (13) gives H<=h0+A omega t; the first then gives
M<=A omega+G1 Hstar B/omega<2A omega, contradicting that contact.
The extrema are continuous on the compact moving interval for a C1 solution,
so this bootstrap has no missing supremum attainment assumption. The force
may raise the positive gradients, but its integrated contribution is controlled
by the fourth threshold. In particular

 n(t,x)>=1/(h0+A omega t)^2>=Hstar^(-2)>0             (15)

uniformly in N on the comparison cone. No density assumption was inserted to
get the Riccati coefficient. Large positive gradients in the other half of
the bump are included in M, rather than being excluded by an invariant-support
or purely compressive-patch assertion.

## 5. A closed compression inequality and the contradiction

Start a plus characteristic at a_N=x*+ell/sqrt(3). It lies strictly in K0.
Using (8), its displacement from a_N by any t<=T_N is at most S_N t.
The third threshold in (12) ensures

 |X_+(t,a_N)-x*| <=ell+S_N t < R-S_N t,              (16)

so this specific characteristic remains in K_t throughout every claimed
existence interval up to T_N. This is stronger than merely assuming it never
reaches a wall. The chosen characteristic displacement and its initial offset are O(N^-3);
the cone has fixed width up to an O(N^-3) shrinkage.

Along this characteristic write w=-y. The positive-side condition g0>0 and
(2),(10) imply

 w(0)=rho(a_N)^(-1/2)[d omega+g0(a_N)/c]>=b omega.     (17)

From (6), (14), and |g0'|<=G1,

 w' >= w^2/(2h)-G1 h.

Whenever w>=b omega, the final threshold gives w>2 sqrt(G1)Hstar>=
2 sqrt(G1)h. Consequently

 w' >= w^2/(4h) >= w^2/[4(h0+A omega t)] >0.         (18)

A first-exit argument preserves w>=w(0)>=b omega: it cannot exit downward
while its derivative is positive at and above the proposed threshold. Thus
(18) is a closed scalar compression inequality with pressure, density and
force coefficients controlled on the same characteristic domain.

As long as a finite positive-C1 solution exists there, w is finite positive,
so integrating its reciprocal gives

 1/w(t) <= 1/w(0)
    -[1/(4A omega)] log(1+A omega t/h0).              (19)

At t=T_N the logarithm is 8A/b, so the right hand side is at most
1/(b omega)-2/(b omega)=-1/(b omega)<0, an impossibility.
Indeed it is already nonpositive by

 t_hat=(h0/(A omega))[exp(4A/b)-1] < T_N.             (20)

The chosen T_N provides a strict contradiction margin and leaves every
bootstrap proved on a larger comparison slab. Hence no solution in the
claim card persists through T_N. If a particular classical branch continues
up to the reciprocal-comparison obstruction, (19) forces its negative weighted
characteristic gradient to be unbounded. Since (9),(15) bound density above
and away from zero for fixed N, divergence of y entails divergence of at least
one of v_x or q_x (and therefore of v_x or n_x).

Interpretation is deliberately conditional: the proof rules out a full
positive-C1 slab and bounds the lifespan of any such branch covering the cone.
It does not prove existence of a maximal branch or a continuation criterion.
If a separately justified maximal classical solution stops earlier, this proof
alone does not identify its first stopping mechanism. Vacuum or infinite
density cannot develop as a limit inside the controlled cone while the displayed
C1 estimates hold, but a general classification of every possible earlier
continuation failure is not claimed. In particular failure of a sufficient
estimate has not been substituted for a singularity proof; the contradiction
here is the impossible negative reciprocal of a finite positive w.

## 6. Exact fixed-potential fluid energy, independent of existence

Use e(n)=c^2 n[log(n/n_ref)-1], p=ne'(n)-e(n)=c^2n. Then any positive-C1
solution of (3), wherever it exists, obeys

 E=nv^2/2+e(n)+n phi0,
 F=nv[v^2/2+c^2 log(n/n_ref)+phi0],
 E_t+F_x=0.                                          (21)

To check this without suppressed terms, kinetic energy satisfies
K_t+(vK)_x=-v p_x-nv g0, internal energy satisfies
e_t+(ve)_x=-p v_x, and interaction energy satisfies
(n phi0)_t+(nv phi0)_x=nv g0. Adding gives (21).
Both pressure work and force work cancel with their actual partner terms.
The external potential is time independent. No field equation was invoked.

Hydrostatics makes mu=c^2 log(rho/n_ref)+phi0 constant on the connected
background interval. Subtract the static background energy and mu(n-rho):

 Erel_density=nv^2/2+c^2[n log(n/rho)-n+rho],
 Frel=nv[v^2/2+c^2 log(n/rho)],
 (Erel_density)_t+(Frel)_x=0.                         (22)

On a fixed interval [a,b], d integral E/dt=-[F]_a^b, and similarly for (22).
For a moving local interval, Reynolds boundary terms must also be retained;
there is no conserved energy claim on K_t. On a full finite fluid interval,
IF a compatible smooth solution with impermeable stationary walls v(a)=v(b)=0
exists, both mass and energy fluxes vanish and

 integral Erel_density(t) dx
 =integral rho v(0)^2/2 dx=O(V^2 ell)=O(N^-1).         (23)

This is a conditional identity, not a global wall-existence theorem. The initial
bump is zero near the walls and hydrostatics gives v_t(0)=0 there, satisfying
the first compatibility condition; higher regularity/traces needed by any
stronger global theorem have not been supplied. Local analysis used no wall
conditions or no-incoming-flow assumption.

At t=0 the actual momentum equation gives v_t=-v v_x, because the background
pressure gradient exactly balances g0. In the derivative of integrated kinetic
energy, the continuity contribution integral rho v^2 v_x is canceled by
integral rho v v_t=-integral rho v^2 v_x. The first variation of internal plus
potential energy is mu integral n_t=0 for zero mass flux. Thus Erel'(0)=0 for
an actual smooth solution. The strictly positive Erel'(0) of FGF044 belonged
to its prescribed stationary velocity, and is not inherited by (3).

The zero-velocity control v=0,n=rho solves both equations exactly, has constant
energy and zero currents, and obeys alpha=-g0/c, beta=g0/c. Its identities (5)
and (6) are consistent with c^2(log rho)'=-g0, without requiring constant
rho or constant g0. This control has no large negative initial w~omega and
does not satisfy the compression trigger (17).

## 7. Field residual, dimensions, branches and exact exclusions

Holding the fields fixed still gives Rphi=-B0_x+C n=C(n-rho) and Rchi=0 in
the inherited diagnostic equations. An actual solution of the two fluid
equations therefore remains a residual ansatz for the dynamically coupled
system. No estimate for this field residual beyond its exact formula is
claimed here. Fluid energy conservation in a fixed potential neither removes
that source residual nor proves conservation laws for an exact coupled state.

Physical L,ell are lengths; v0,V,c are velocities; omega is inverse time;
T_N=B L/(v0 N^4) has units time. The sound speed c here is not c_light in the
adopted vacuum scale a_ref=kappa c_light sqrt(G rho_Lambda,ref). Kappa is
adopted. Run the conditional statement separately for a_ref=9.3619e-11 and
1.1279e-10 m/s^2; no normalization is fitted or selected. Their backgrounds
may give different constants R,G0,G1,h0,hmin,A,b,B,N0. Q remains the signed
constitutive relation stated in Section 1. No Newtonian missing mass or empirical
source mass is substituted for its MOND flux requirement.

Constant-vacuum reference is the primary fixed family. A frozen comparison
a_ref=a0 E(z), E(z)^2=.315(1+z)^3+.685, is a separate fixed-reference family.
An evolving-H reference changes the physical model and requires separate work
and reservoir accounting; it is not solved here. Spatial chi0 response remains
the inherited diagnostic premise and does not derive the pointwise constant-
vacuum identity for a(x). There is no transfer to exact coupled gravity,
RAR/R/M/filtered MONO, a physical scale reservoir, metric/photon dynamics,
degree counting, observational closure, historical novelty, or global stability.

The remaining analytic implication, if needed, is a direct local C1 existence
and continuation construction for these exact C1,1 data, so the a priori
obstruction can be attached to a constructed maximal fluid branch. It must be
a separate claim; the present bound already excludes an N-independent
positive-C1 lifespan on the stipulated fixed regular neighborhood.
