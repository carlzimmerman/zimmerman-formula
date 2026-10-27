# FGF047 independent construction, before new-author exposure

Reviewer /root/fgf047_reviewer. This is an independent derivation from task,
common contract and pinned OLD ancestry, not an audit verdict. No new stage34
proof, result or mathematical preview has been read. The metadata receipt pins
this immutable text and its inputs. Old source text was initially read before
checking the task's nine expected hashes; all nine subsequently matched before
this derivation was written. This ordering defect is disclosed, not concealed.

## 1. Exact domain and equations

Fix c=cs>0, C=4pi G_Newton>0, tau,sigma,J,S0,a_ref,nref>0.
Use one smooth inherited hydrostatic background (rho,phi0,chi0) on an open
positive-gradient patch U, with g0=phi0_x>0. Work on K0=[x*-R,x*+R]
compactly inside U, with a buffer to the crossing and all physical walls.
Initial n=rho, phi=phi0, chi=chi0, p=phi_t=0, h=chi_t=0 and exactly
v=V f((x-x*)/ell), V=v0 N, ell=L/N^3, f=(1-y^2)^2 for |y|<1 and
zero elsewhere. Fix a finite N with ell<R/2. This velocity is C1,1 and need
not be C2; ||f'||=8/(3sqrt(3)), Lip f'=8. Its first-gradient norm scales
N^4 and Lipschitz-gradient norm N^7; neither is replaced by a background bound.

The actual equations are the four task equations, with a=a_ref exp chi,
B(g,a)=(sqrt(a^2+4g^2)-a)/2, g=phi_x>0. Put A=B_g=2g/sqrt(a^2+4g^2),
D=B_chi=a^2/[2sqrt(a^2+4g^2)]-a/2, b=sqrt(A/tau)>0, d=sqrt(J/sigma)>0.
The exact primitive and scale source are
W=g sqrt(a^2+4g^2)/4+a^2 asinh(2g/a)/8-ag/2,
T=-W_chi=ag/2-a^2 asinh(2g/a)/4, U=S0(cosh(2chi)-1)/4.
In particular T_g=-B_chi. All coefficients are smooth on g>0, finite chi.
The dynamic source remains B_x=Cn+tau p_t throughout.

## 2. Characteristic variables and all induced terms

Let q=log(n/nref), r=v+cq, s=v-cq, p=phi_t, h=chi_t, k=chi_x.
The first-order original equations, after imposing the gradient constraint,
are
r_t+(v+c)r_x=-g, s_t+(v-c)s_x=-g,
p_t-b^2 g_x=D k/tau-Cn/tau, g_t-p_x=0,
h_t-d^2 k_x=(T-U')/sigma, k_t-h_x=0, chi_t=h.
Phi is reconstructed afterward and is not required in these coefficients.

Choose any fixed g_star>0 and define H(g,chi)=integral_{g_star}^g b(z,chi) dz.
Here H_g=b>0, but H_chi is generally nonzero. Define
u=p+H, w=p-H, alpha=h+d k, beta=h-d k, and state
y=(r,s,u,w,alpha,beta,chi). Its diagonal equations are

r_t+(v+c)r_x=-g,
s_t+(v-c)s_x=-g,
u_t-b u_x=F+H_chi(h-b k),
w_t+b w_x=F-H_chi(h+b k),
alpha_t-d alpha_x=L,
beta_t+d beta_x=L,
chi_t=h,

where F=D k/tau-Cn/tau and L=(T-U')/sigma.
Recover v=(r+s)/2, q=(r-s)/(2c), n=nref exp q,
p=(u+w)/2, H=(u-w)/2, h=(alpha+beta)/2, k=(alpha-beta)/(2d).
Invert H at fixed chi to recover g. The inverse exists on an open coordinate
image because H_g=b>0. On any compact g>0 box it and all needed derivatives
are bounded. Equal speeds in different rows cause no problem: the displayed
coordinates provide independent coordinates even when b=d or v+c=b, etc.
There is no assumption of separated families or globally constant eigenvectors.

The source formula cannot discard either H_chi h or H_chi b k. Directly,
(p+H)_t-b(p+H)_x=(p_t-b^2g_x)+H_chi(h-b chi_x)
after g_t=p_x. This gives the displayed source when chi_x=k.

## 3. Compatibility and converse, without assuming iteration compatibility

Solve the diagonal system first, allowing its iterates to violate constraints.
The resulting C1 solution satisfies k_t=h_x by subtracting its two scale rows.
Since chi(t,x)=chi0(x)+integral_0^t h(z,x) dz,
chi_x-k=chi0_x-k0=0 for compatible initial data. No uncontrolled mixed
second derivative is required: differentiate the integral using continuous h_x.
Before using this identity the scalar rows give exactly

g_t-p_x=H_chi(chi_x-k),
p_t-b^2g_x=F+b H_chi(chi_x-k).

They therefore reduce to the desired first-order field pair. Set
phi(t,x)=phi0(x)+integral_0^t p(z,x) dz. Then phi_t=p and
phi_x=g0+integral_0^t p_x dz=g, again by compatibility initially.
Consequently phi,chi are C2 in spacetime because their first derivatives
(p,g) and (h,k) are C1. The reconstructed n,v are C1 and satisfy both fluid
equations by adding/subtracting their rows. The field source equation follows
from b^2=A/tau and B_x=A g_x+D k, with all terms retained.

## 4. Auxiliary data and fixed compact box

Extend g0 to a positive smooth bounded function on R, constant outside a
compact interval, by a cutoff convex combination with a positive constant.
Extend chi0 and q0 smoothly and boundedly by the same elementary cutoff
procedure; set k0=chi0_x, p0=h0=0 and leave the exact compact velocity
unchanged. The extensions agree on a neighborhood of K0. If a global initial
phi is desired, integrate the extended g0 and choose the physical integration
constant; its possible linear growth is harmless because phi is absent from
the state coefficients. It need not be falsely claimed bounded.

The initial y0 then belongs to C_b^{1,1}(R), with compact range in the valid
coordinate domain. Choose a closed physical box containing the extended
initial range strictly inside it, with, for example,
g between gmin/2 and 2gmax+gmin, q in [qmin-1,qmax+1], chi in
[chimin-1,chimax+1], and finite buffered bounds on v,p,h,k. All extrema here
are those of the chosen extended initial data; gmin>0. The initial physical
image in diagonal coordinates is compact and strictly interior to this box's
coordinate image. Choose epsilon>0 such that its closed 2epsilon-neighborhood
is inside that image. Use a smooth cutoff equal to one on that neighborhood,
supported compactly inside the valid image, to extend each characteristic
speed lambda_i(y) and source F_i(y) to globally bounded smooth functions on
R^7. They agree with the actual system whenever ||y-y0(x)||<=epsilon.
This extension only concerns state space and is not a physical exterior model.

To avoid adding quantities of unlike dimensions, perform the following norm
estimates after fixing arbitrary positive length/time/state reference units
and expressing all equations and coordinates in those units. Transforming back
multiplies the lifespan by the reference time. All constants below are thus
dimensionless numerical values of actual rescaled norms and coefficients.
No claim that their size is independent of N is made.

## 5. Direct diagonal transport construction with quantitative time

Use maximum component norms and their induced operator norms (including row
sums). Let L0 bound all extended speeds, L1 their first derivatives, L2
their second derivatives, and F0,F1,F2 the analogous source bounds. Define
P0=||y0_x||, Q0=Lip(y0_x), P=2(P0+1), Q=4(Q0+1),
A1=F1+L1 P, D2=(F2+L2 P)P^2, E0=F0+L0 P.
One sufficient positive time is

T0=min(1,1/[16(A1+1)],Q/[16(D2+1)],epsilon/[4(E0+1)]).

The actual extended norms are finite for each fixed N. Dependence on P0,Q0,
all coefficient bounds and the positive-state margin is explicit. This formula
does not assume or assert an N^-4 lower time.

Start y^0(t,x)=y0(x). Solve recursively
(y_i^{m+1})_t+lambda_i(y^m)(y_i^{m+1})_x=F_i(y^m),
y_i^{m+1}(0,x)=y0_i(x).
For each row construct terminal characteristics by successive approximation
of X'=lambda_i(y^m(t,X)). The Lipschitz constant in x is at most L1 P.
On short pieces the integral map contracts; bounded speed prevents escape,
so concatenation gives the flow on the whole time interval. Its label
Jacobian solves J'=lambda_x J and equals the corresponding exponential;
this follows directly by difference quotients of the integral equation.
Integrating the source along that flow constructs y^{m+1} as C1, with the
prescribed exact trace. This is a proof of the needed linear transport step,
not an appeal to a PDE existence theorem.

Assume ||y_x^m||<=P and Lip_x(y_x^m)<=Q. Differentiating the characteristic
formula gives
||y_x^{m+1}(t)|| <= (P0+t F1 P) exp(L1 P t).
Since T0 A1<=1/16, the right side is at most
(P/2+P/16)exp(1/16)<P. For the derivative Lipschitz seminorm, compare its
ODE along two characteristics and divide the difference by their separation.
The separation has logarithmic derivative bounded by L1 P. This yields

Lip_x(y_x^{m+1}(t))
 <=exp(2L1Pt)[Q0+t((F1+L1P)Q+(F2+L2P)P^2)]
 <=exp(1/8)[Q/4+Q/16+Q/16]<Q.

To verify the forcing constants, Lip_x(lambda_x)<=L1 Q+L2 P^2 and
Lip_x(F_x)<=F1 Q+F2 P^2; the former multiplies an output gradient <=P.
These inequalities require only Lipschitz first derivatives, not continuous
second derivatives, and therefore include the actual polynomial joins.
The elementary bound exp(z)<=1/(1-z), 0<=z<1, verifies both strict margins.
The starting iterate satisfies the same bounds, so induction closes.

The equations give ||y_t^{m+1}||<=E0. As every iterate has initial trace y0,
||y^{m+1}(t)-y0||<=t E0<=epsilon/4. The entire construction remains inside
the state region where the extended coefficients equal the original ones.
Thus the use of globally extended coefficients is removed, rather than merely
asserting that positivity follows from the old static background.

## 6. Contraction and actual C1 limit

Subtract consecutive transport equations using lambda(y^m). Their common
initial data cancel, and the source is bounded by
(F1+L1P)||y^m-y^{m-1}||. Thus
||y^{m+1}-y^m|| <=T0 A1 ||y^m-y^{m-1}|| <=(1/16)||y^m-y^{m-1}||.
The first difference is finite, so the series converges uniformly. To recover
spatial derivatives, for a scalar difference z with Lip(z_x)<=2Q,
|z_x(x)|<=2||z||/h+Qh for every h>0. Optimization gives
||z_x||<=2sqrt(2Q||z||). Hence the gradients converge uniformly, and the
integral identity in x identifies their continuous limit with y_x. The PDE
right sides -lambda(y^m)y_x^{m+1}+F(y^m) converge uniformly; integrating in t
identifies the continuous time derivative of the limit. We obtain y in C1
with uniformly Lipschitz spatial gradients, exact initial trace and pointwise
original diagonal equations. Section 3 now supplies compatibility, actual
field equations and phi,chi in C2. Their derivatives need not have a further
continuous spatial derivative beyond the stated class.

The finite compact physical box gives, for the entire proved interval,
g>=gmin/2>0, n>=nref exp(qmin-1)>0,
a>=a_ref exp(chimin-1)>0, and finite upper bounds for each. It follows that
B_g and b have strictly positive lower bounds on that box. These margins are
propagated by the iteration's actual time-drift estimate, not static balance.

## 7. Local domain, uniqueness and extension independence

Use S=L0+1 in the fixed units and set T=min(T0,R/[2S]). On
K_t=[x*-R+St,x*+R-St], every backward characteristic of the constructed
state stays inside earlier K_z because its speed has absolute value <S.
The zero-speed reconstruction integrals also stay inside earlier slices.
The physical conclusion is for 0<=t<=T on this cone; it avoids cusp/walls.

For two C1 solutions whose states lie in a common compact valid coordinate
region, subtract the diagonal systems and integrate along the first one's
characteristics. A finite coefficient Lipschitz bound and finite gradients
of the second solution give D(t)<=K integral_0^t D(z)dz when initial data
coincide and all backward curves remain in the common cone. Repeated
integration bounds D(t) by Dmax(Kt)^j/j! for every j, proving D=0. Coincident
speeds are immaterial to this scalar-row argument. Different auxiliary spatial
extensions therefore yield the same solution on any common contained cone,
using a speed that bounds both solutions. In particular they define the same
local physical germ. Phi's integration constant and trace are fixed, so it
also agrees. No claim that every extension provides the same guaranteed time
or an arbitrarily large common cone is needed.

## 8. Full evolving energy and hydrostatic control

Let e(n)=c^2 n(log(n/nref)-1), Pmat=c^2 n. Define
E=nv^2/2+e(n)+n phi+
 [tau p^2/2+W(g,a)+sigma h^2/2+J k^2/2+U(chi)]/C,
Fenergy=nv[v^2/2+c^2 log(n/nref)+phi]-(p B+J h k)/C.
The matter plus interaction balance is
(nv^2/2+e+n phi)_t+[nv(v^2/2+c^2 log(n/nref)+phi)]_x=n p.
The Q-field balance is
[(tau p^2/2+W)/C]_t+[-pB/C]_x=-np-T h/C.
The scale balance is
[(sigma h^2/2+Jk^2/2+U)/C]_t+[-Jhk/C]_x=T h/C.
Thus E_t+(Fenergy)_x=0 pointwise in the constructed class. Both field fluxes
and both exchanges are necessary. For moving endpoints l(t),r(t),
d/dt integral_l^r E=Fenergy(l)-Fenergy(r)+r'E(r)-l'E(l).
No conserved cone energy or missing boundary work is asserted.

With v_in=0, the actual hydrostatic fields and n=rho,v=0 are an exact
stationary solution: B_x=C rho, J chi_xx+T-U'=0 and pressure balance.
Local uniqueness identifies the constructed control with that stationary
solution on the physical cone; an auxiliary extension need not be an exact
hydrostatic solution outside it.

## 9. Scope and remaining questions

This independently supplies a direct local construction for all fixed finite
N satisfying the support gate, the complete derivative limit, exact coupling,
state margins, compatibility, local domain and full energy. It neither assumes
nor proves fixed-force breakdown persistence, an N^-4 lower bound, crossing
well-posedness, endpoint classification, global existence or post-breakdown
selection. Both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 are separate positive
fixed backgrounds. Constant-vacuum and frozen-H reference families remain
separate from evolving H. The spatially varying diagnostic scale does not
establish the pointwise physical vacuum relation, two gravitational degrees
of freedom, metric/photon coupling, RAR/M/filtered MONO transfer, criterion B,
cluster calibration, cosmology, novelty or theory closure.

Proof-only. No mathematical executable commands, numerical experiment, external
existence theorem, network use, service, installation or commit. Metadata
hashing and file reads/writes are administrative. No failed mathematical route
was used to support this construction. Final proof audit will be a separate
artifact pinned to the final new-author bytes after this freeze.
