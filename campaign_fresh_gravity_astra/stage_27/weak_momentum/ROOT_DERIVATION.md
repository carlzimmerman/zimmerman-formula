# Force-product obstruction and combined weak momentum

2026-09-30 21:31 UTC pass. Root proof frozen before new author/reviewer proof
or formula previews. Inherit the fixed-reference Q diagnostic action; no new
numerical run or imported mechanism. Constants C=4piG, cs²,tau,sigma,J,S0>0
are fixed. The background Q crossing is the reviewed short fixed-wall solution,
with density rho>0, mass M and fixed potential/scale wall values.

Write n for current density, j=n v for matter momentum/current, g=phi_x,
u=phi_t, k=chi_x, w=chi_t, a=a_ref exp chi. The Q constitutive functions are
B(g,a)=sgn(g)(sqrt(a²+4g²)-a)/2, W(s,a)=int_0^s b(v,a)dv,
T=-W_chi, U=S0(cosh(2chi)-1)/4, and pressure p=cs² n.
The smooth equations inherited from the action are

n_t+j_x=0,
j_t+(j²/n+cs²n)_x=-n g,
tau u_t-B_x=-C n,
sigma w_t-J k_x+U'-T=0.                                  (1)

The smooth matter equation requires a meaningful velocity, e.g. n>0. For a
finite-energy candidate at vacuum define j²/n as zero if j=n=0, infinity if
n=0,j!=0. No smooth vacuum evolution is assumed. The actual dynamic MOND
source is B_x=Cn+tau u_t, not B_x=Cn on arbitrary comparison states.

## Exact finite-energy state with nonintegrable separate force

Choose an interior point x0 away from the background cusp and a fixed length
L0 whose neighborhood is strictly inside I. Let y=(x-x0)/L0. Take a smooth
nonnegative cutoff f equal to1 near zero, supported in that neighborhood.
Define a normalized probability density F_p(x)=Z_p^-1 f(y)|y|^(-p),
Z_p=int_I f(y)|y|^(-p)dx, p=3/4. Then F_p>=0, integral F_p=1 and
F_p log F_p is integrable. Values at the single point x0 can be assigned
arbitrarily; all statements concern almost-everywhere functions.

For any 0<epsilon<1 set n=(1-epsilon)rho+epsilon M F_p. This is positive,
fixed-mass and finite entropy. Let q=1/3, H>0 have acceleration units, and
let b0 be a fixed smooth nonnegative unit-integral bump with disjoint support.
Set c_q=int f(y)|y|^(-q)dx, and

h(x)=H[f(y)|y|^(-q)-c_q b0(x)],
psi(x)=int_left^x h(s)ds, eta=0, j=u=w=0.                 (2)

The derivative h has integral zero and belongs to L2 because 2q<1, so psi
is H1_0 and bounded. Actual g=g_background+h has finite Q field energy,
using 0<=W(s,a)<=s²/2 and bounded background scale. Scale gradient and U
are unchanged and finite. Internal entropy is finite, and n(phi_background+psi)
is integrable because the potential is bounded and n is L1. Kinetic energy
is zero. Thus every term in the exact energy and every required wall datum
is valid; no unmentioned density-gradient energy rejects this state.

Near x0, n*g has a positive leading coefficient times |y|^(-p-q), with
p+q=13/12>1. The bounded background g and disjoint correcting bump cannot
cancel it. Thus n phi_x is NOT locally integrable, even as a signed integral
with finite positive part. This is a state-domain counterexample, not a
nonlinear solution or proof of dynamical ill-posedness. Defining an extension
by renormalization would require an extra rule; no such rule is assumed.

The obstruction persists arbitrarily close in exact excess energy to the
background. Convexity in density gives D(n||rho)<=epsilon D(M F_p||rho).
On eta=0 the global Q tangent remainder is at most h²/2 because 0<=A<=1.
After exact background first-variation cancellation, the remaining interaction
is (n-rho)psi, whose integral is bounded by a fixed constant times epsilon H.
Therefore DeltaE is bounded above by O(epsilon)+O(epsilon H)+O(H²), and
is nonnegative by FGF039 on the selected short patch. Taking epsilon,H to
zero through positive values gives DeltaE->0, while the product is nonintegrable
for every member. It is not merely a pathology at an inaccessible large energy.
All amplitudes use fixed physical reference units; p,q are fixed, not scanned.

## Smooth momentum identity with full field and scale terms

First perform all product differentiation for smooth solutions of (1). The
chain rule W_x=B g_x-T k gives

B_x g = (B g-W)_x-T k.

Consequently the dynamic source implies

C n g = (B g-W+tau u²/2)_x-(tau u g)_t-T k,              (3)

using g_t=u_x. The scale equation gives T=sigma w_t-J k_x+U', and hence

-T k=-(sigma w k)_t+(sigma w²/2+J k²/2-U)_x.             (4)

Combining (3),(4) with the matter momentum equation yields

P_t+F_x=0,                                               (5)
P=j-(tau u g+sigma w k)/C,
F=j²/n+cs²n+[B g-W+tau u²/2+sigma w²/2+J k²/2-U]/C.

The MINUS sign of the field momentum densities and the PLUS signs of both
kinetic stresses are essential. For a right-moving positive-energy free
wave, u and g have opposite signs, so -tau u g has the correct positive
momentum sign. The scale potential appears with -U in the stress. All terms
have momentum-per-volume or stress units appropriate to this 1D area-normalized
model. The interaction n phi disappears through the source relation, rather
than being dropped from the original energy.

For smooth fields (with products well-defined), (5) and the two field equations
recover the separate conservative Euler momentum equation by reversing the
algebra. Mass conservation is a separate equation. This is smooth equivalence;
it is NOT multiplication of rough distributions or a proof of weak equivalence.

## Integrable coefficients for a candidate weak formulation

On a bounded time slab (0,T) and finite I, impose measurable representatives
with n>=0, fixed finite mass a.e. in time, j²/n in L1(space-time), and
u,g,w,k in L2(space-time). Require the derivative identities u=phi_t,g=phi_x,
w=chi_t,k=chi_x distributionally, and a bounded chi (for example retained
quarter-cap relative to the fixed bounded background). These are genuine
spacetime hypotheses: finite energy at each time without an integrable bound
in time does not suffice. Uniform finite-energy norms on a finite time slab
are one sufficient way to supply them. Relative-energy cancellation alone
is not being used to infer every unweighted norm.

Then j is L1 by Cauchy-Schwarz using integral n=M T and integral j²/n<infinity.
Each u g,w k belongs to L1. For Q, 0<=B g-W<=g²: monotonicity gives W<=b(s)s,
and b(s)<=s. Thus P,F in (5) are L1, including the kinetic, pressure and scale
terms. U and U' are bounded under the chi cap. Also B is L2 since |B|<=|g|.
For the scale source, T_s=s b_s-b=a b/sqrt(a²+4s²), between0 and a/2;
T(0)=0 gives 0<=T<=a|g|/2. Hence T is L2 when a is uniformly bounded.

Every term in the following distributional system is therefore meaningful:

n_t+j_x=0,
tau u_t-B_x+C n=0,
sigma w_t-J k_x+U'-T=0,
P_t+F_x=0, with the derivative identities above.            (6)

For example, the last equation means int(P zeta_t+F zeta_x)=0 for every
smooth compactly supported spacetime test zeta. The field equations mean
int[-tau u zeta_t+B zeta_x+C n zeta]=0 and
int[-sigma w zeta_t+J k zeta_x+(U'-T)zeta]=0. No term n*g or product of a
distributional acceleration with a gradient is formed in (6).

This is a meaningful CANDIDATE weak conservative system inherited by smooth
solutions. It is not automatically a solution obtained from (2), nor does
integrability prove existence, uniqueness, conservation of energy, weak-limit
closure, or equivalence to a separately written forced matter equation.
In particular weak convergence of finite-energy approximants does not by
itself identify quadratic or constitutive products in P and F. Defect terms
or stronger compactness may be needed; neither is resolved in this pass.

## Boundary balance and the unresolved evolution gate

At smooth walls, integrating (5) gives d/dt int P=F(left)-F(right). Fixed
phi and chi boundary values imply u=w=0 there if smooth, and impermeability
sets j=0. These conditions do NOT set the remaining pressure and field stresses
to zero or equal. The walls can exchange momentum. No conserved global total
momentum is inferred from impermeability and static Dirichlet values alone.

For the rough system, P,F merely in L1 do not automatically possess pointwise
wall or initial traces. Local compact-support testing needs no wall trace.
A global initial-boundary balance requires separately supplied/justified normal
flux and momentum traces (or regularity that gives them) and the prescribed
boundary data. This is distinct from the previously derived smooth energy
flux identity and is not repaired by declaring the integrated momentum constant.

Thus the separated Euler force density fails to be an L1-defined term on
the energy class, even at arbitrarily small energy, while combined momentum
coefficients admit an L1 spacetime formulation under explicit additional time
bounds. Neither the failure nor the candidate repair closes nonlinear evolution.
A bounded next question is whether energy bounds plus chosen approximation
constraints suffice to identify these nonlinear fluxes in a weak limit;
energy-space membership alone does not supply that theorem.

Both a0=9.3619e-11 and1.1279e-10 m/s² label separate positive reference
backgrounds. Constant vacuum reference, frozen a0 E(z) with
E²=.315(1+z)^3+.685, and actual evolving-H branches remain distinct. This pass
uses fixed reference; prescribed time dependence retains its work/reservoir
obligation. Spatially responsive scale is an added diagnostic premise. All
source bookkeeping is Q MOND, not Newtonian discrepancy, RAR, M or filtered
MONO. No metric/photon/DOF, covariant physical conservation, calibrated evidence,
imported mechanism, historical novelty or full theory closure follows.
