# Candidate finite-regularity local evolution and continuation

Research derivation, awaiting independent audit. Scope: periodic plane symmetry,
constant V,a0, native on branch, compact r>0,Q>1,cap<1,h>0,R>0,1-2gammaD>0.
No postbreak solution or three-dimensional theorem is claimed.

## Gauge and closed system

Use x in R/Z and
 ds²=-r^-2 dτ²+ell(τ)²(dx+w dτ)²+exp(2beta)dy_perp².
 n=r(∂τ-w∂x), e=ell^-1∂x,
 ell'/ell=mean(K/r), w_x=mean(K/r)-K/r, mean(w)=0.
Then div_2 n=K and the actual commutator is
 [n,e]=-e(log r)n-Ke, including off the constraint surface.

Unknown U=(r,A,P,beta,B,E,a,K), plus positive ell. Use the PF08 clock equations
for lower fields and the algebraically expanded a,K equations: replace er,eA,
eP,eB in eS and ec² by ra,Wp/r,D-2PE,(K-B)E, respectively. Do not replace eK.
The native spatial inverse for u,v is exactly the corrected PF08 curved inverse,
with its er forcing set to ra. This specifies an off-constraint evolution.

In τ coordinates the spatial matrix is -w I plus a 2x2 a,K block
 (r ell)^-1 [[0,c²],[1,0]]. The other six speeds equal -w. A smooth symmetrizer
is identity on those six fields and diag(1,c²) on a,K. A smooth left-eigenvector
matrix exists even with the repeated advective speed: choose the coordinate
vectors for the six advected fields and the two eigenvectors of the 2x2 block.
It depends smoothly on r,A only; all eigenvector inverses stay bounded locally.

The source is a locally Lipschitz algebraic function of U and z=(u,v), including
Wpp(P), plus the scalar ell equation. No source depends on U_x after expansion.
The shift w is an order-minus-one functional of K/r. This is a quasilinear
hyperbolic system with a spatial inverse in its lower-order terms.

## Spatial inverse estimates off the constraint surface

At compatible initial data the weighted coercivity proof makes the periodic
first-order operator invertible. Write it in x coordinates as
 T_U z = z_x-M(U,ell)z=f(U,ell).
Here coefficients depend locally Lipschitz on U; f is algebraic, including
terms linear in a,K. Cusp Wpp(P) is locally Lipschitz inside the cap.
The initial inverse maps Lp to W1,p, 1<=p<=infinity, with fixed finite constants:
solve the fundamental-matrix boundary problem, whose monodromy minus identity
is invertible. This also proves surjectivity, not just kernel exclusion.

For U in a small C0 neighborhood of the compatible initial U0 and ell near ell0,
Neumann inversion of T_U T_U0^-1 supplies uniform inverse estimates. Thus no
identity e beta=E is assumed to prove invertibility for off-constraint iterates.
The neighborhood is on the compact lower fields: a,K enter forcing, not M.
For bounded U:
 ||z||W1,infinity <= C_R,
 ||z1-z2||H1 <= C_R (||U1-U2||L2+|ell1-ell2|).
The latter follows from T1(z1-z2)=(M1-M2)z2+f1-f2, pointwise Lipschitz
coefficients, z2 bounded, and the L2-to-H1 inverse bound. Similarly the inverse
is locally Lipschitz in C0 and shift differences are bounded in H1 by the L2
state difference. Constants may depend on the initial operator and compact set.

## Approximation construction and uniform estimates

Take periodic W1,infinity initial U0 and ell0>0 in the invertible neighborhood.
Approximate initial data by smooth convolutions and the locally Lipschitz native
source/coefficient functions by smooth functions. Keep the smooth principal
matrix unchanged; approximate Wpp and any nonsmooth algebraic source with
uniform local Lipschitz constants and uniform convergence on the compact set.
These are proof approximants, not physical regularizers or postshock laws.
They need not preserve constraints at finite approximation index.

For each smooth approximant, local smooth solutions follow by freezing the
hyperbolic coefficients and spatial inverse, solving the linear hyperbolic
system, and iterating. Smooth composition plus first-order inverse bounds gives
the high Sobolev estimates for this step; the L2 difference estimate below gives
contraction on a shorter interval. This interval may initially depend on the
smoothing index. The following independent estimates extend it uniformly.

Let V=U_x. Differentiate the smooth approximate equation:
 V_τ+C V_x = -(∂x C)V+∂x F.
The coefficient derivative has ||∂x C||infinity<=C_R(1+||V||infinity).
The spatial inverse equation itself, not differentiation of its inverse, gives
z_x=M z+f and hence ||z_x||infinity<=C_R. Consequently
 ||∂x F||infinity<=C_R(1+||V||infinity), uniformly in smoothing index.
The smooth left eigenvectors L depend only on r,A. Along each characteristic,
(∂τ+lambda_i∂x)L has bound C_R(1+||V||infinity), since U_τ is bounded by
C_R(1+||V||infinity). No second source derivative is used. Thus the maximum of
|L V| obeys an upper inequality
 m'<=C_R(1+m)^2.
A corresponding state estimate ||U_τ||infinity<=C_R(1+m) keeps U in the
invertible/domain neighborhood for a positive uniform time. ell has the scalar
ODE bound from bounded K/r. Smooth high norms can be continued over this time:
for each fixed smoothing index their energy inequalities have bounded first
coefficient derivatives and smooth-source higher constants. The latter need
not be uniform in the index. The required first-derivative bounds are uniform.

For two approximants use the symmetrizer for one solution and subtract equations.
Their difference satisfies an L2 energy inequality
 d/dτ (||delta U||L2²+|delta ell|²)
 <=C_R,m (||delta U||L2²+|delta ell|²)+C_R eta²,
where eta is the uniform coefficient/source approximation error. The term
(C1-C2)U2,x is bounded using the uniform Lipschitz state bound, the local Lipschitz
pointwise principal coefficients and the shift H1 estimate. Source differences
use the inverse H1 estimate above. Symmetrizer time/space derivatives are bounded
by uniform first state derivatives. This proves a Cauchy sequence in CτL2.
Uniform W1,infinity and time-Lipschitz bounds give a uniformly convergent
subsequence and a joint Lipschitz limit. The limit satisfies the exact native
expanded system almost everywhere, with the exact spatial inverse at each time.
No mollification is retained. The same L2 inequality without eta proves
uniqueness and L2 continuous dependence within bounded Lipschitz classes.

The conclusion is a local W1,infinity strong solution of the EXPANDED system.
The native equations follow only after the separate residual propagation proof.
No C-infinity or high-Sobolev regularity across generic P zeros is asserted.

## Continuation once constraints propagate

On the constraint surface, r_x=ell r a, A_x=ell Wp/r,
P_x=ell(D-2PE), beta_x=ell E, B_x=ell(K-B)E,
E_x=ell[KB+(B²-3E²)/2-rho/(2M)]. Thus derivatives of the six lower fields are
bounded by compact U values, irrespective of a_x,K_x. Also w_x is bounded by
K/r and ell'/ell by its mean. The two characteristic eigenvectors and speeds
therefore have first derivatives controlled by compact U, not by a_x,K_x.

The differentiated a,K sources contain at most linear a_x,K_x terms with
bounded coefficients: all other field derivatives above and z_x are bounded;
Wpp(P) has bounded a.e derivative times bounded P_x. Therefore the maximum of
(a_x,K_x) in characteristic eigencomponents obeys
 m'<=C_R(1+m),
with no derivative-cusp singularity. This can be justified for the Lipschitz
limit by difference quotients or characteristic integral equations, using the
bounded a.e derivative of the native locally Lipschitz source. The lower field
derivatives remain controlled by the propagated constraints.

Consequently a solution can be continued across a finite time while compact
state/domain/length bounds and |a|+|K| remain bounded. For a quantitative
extension one also needs uniform inverse bounds along the solution; on the
constraint surface these follow from the existing curved coercivity theorem.
This is the continuation input needed by the localized-packet Riccati argument.

## Sources and evidence boundary

The smooth symmetric-hyperbolic construction/energy method was compared with
Ian Tice, Quasilinear symmetric hyperbolic systems (2017), Theorems2.4.1–2.4.2,
https://www.math.cmu.edu/~iantice/notes/quasilinear_hyperbolic_systems.pdf .
That theorem is NOT directly invoked for the native cusp or nonlocal source.
The uniform first-derivative and inverse estimates above are additional internal
obligations. A prior Oxford chapter access failed; no claim relies on it.

Self-derived candidate proof. Independent review must check approximation
construction, derivative estimate for the repeated-speed block, inverse mapping,
constraint equivalence, and the Lipschitz continuation step before this is used
as an unconditional native breakdown theorem.
