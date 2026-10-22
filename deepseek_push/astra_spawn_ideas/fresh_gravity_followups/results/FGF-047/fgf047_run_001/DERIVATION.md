# FGF047: direct local evolution of the diagnostic Q/scale/fluid system

Author: /root/fgf047_author. Proof only; no PDE theorem or mathematical
executable computation. All nine task ancestry hashes matched. The FGF046
author text was read immediately before that check; proof development and
all other ancestry reading followed it. No new stage34 author/root/reviewer
proof was read. Primary AS1174/1143/1168 ownership is untouched.

## 1. Exact claim, data and regularity

Fix positive C=4pi G_Newton, tau,sigma,J,S0,cs,nref,a_ref and a regular open
positive-gradient interval U of the inherited hydrostatic solution. Write
c=cs, d=sqrt(J/sigma), a=a_ref exp(chi), and

 B(g,a)=(sqrt(a^2+4g^2)-a)/2,  W(g,a)=integral_0^g B(s,a) ds,
 T(g,a)=-W_chi(g,a),  U_s(chi)=S0[cosh(2chi)-1]/4.             (1)

U_s denotes the scale potential, avoiding confusion with the spatial patch.
On this branch

 B_g=2g/sqrt(a^2+4g^2)>0,
 B_chi=(a^2/sqrt(a^2+4g^2)-a)/2.                             (2)

All these coefficients are smooth for g>0 and finite chi. The background
(rho,phi0,chi0) is smooth on U and obeys

 g0=phi0_x>0, B(g0,a_ref exp chi0)_x=C rho,
 c^2(log rho)_x=-g0, J chi0_xx+T(g0,a_ref exp chi0)-U_s'(chi0)=0. (3)

Choose K0=[x*-R,x*+R] compactly inside U. For fixed finite integer N with
ell=L/N^3<R/2 and V=v0 N, use EXACTLY

 n(0,x)=rho(x), v(0,x)=V f((x-x*)/ell),
 f(y)=(1-y^2)^2 for |y|<1, and 0 otherwise,
 phi(0,x)=phi0(x), chi(0,x)=chi0(x), phi_t(0,x)=chi_t(0,x)=0.   (4)

Here L,v0>0 are the inherited parameters. The polynomial is C1,1, not C2
at its support endpoints. No smoothing or changed initial profile is used.
Its exact norms are ||f||=1, ||f'||=8/(3sqrt(3)), Lip(f')=8.

The claim proved below is a positive-time local solution of

 n_t+(nv)_x=0, v_t+v v_x+c^2(log(n/nref))_x=-phi_x,
 tau phi_tt=(B(phi_x,a))_x-Cn,
 sigma chi_tt=J chi_xx+T(phi_x,a)-U_s'(chi),                 (5)

on a shrinking compact interval inside U. More precisely n,v and
(phi_t,phi_x,chi_t,chi_x,chi) are C1 in spacetime, with first spatial
derivatives locally Lipschitz uniformly in time; phi,chi are C2 there.
The equations hold pointwise, with one-sided initial time derivatives.
The initial traces are exactly (4). Positivity bounds for n,a,g are explicit
box bounds below. Uniqueness and independence of auxiliary extensions hold
on common backward characteristic domains in this classical class (the
competitor need not have Lipschitz first spatial derivatives). No large-N
lifespan power, breakdown theorem, crossing theorem or global wall solution
is part of the claim.

## 2. Full first-order system and characteristic coordinates

Set q=log(n/nref), p=phi_t, g=phi_x, w=chi_t, k=chi_x. Equations (5),
including compatibility, become

 q_t+v q_x+v_x=0, v_t+v v_x+c^2 q_x=-g,
 g_t=p_x, p_t=b(g,chi)^2 g_x+A(g,chi,k,n),
 k_t=w_x, w_t=d^2 k_x+D(g,chi), chi_t=w,                    (6)

where

 b=sqrt(B_g/tau)>0,
 A=B_chi k/tau-Cn/tau,
 D=[T(g,a_ref exp chi)-U_s'(chi)]/sigma.                    (7)

The original field source is B_x=Cn+tau phi_tt; (6) does NOT impose the
static source inversion after the initial slice.

Choose any fixed g_*>0, and define the smooth function

 h(g,chi)=integral_{g_*}^g b(s,chi) ds.                     (8)

The integration interval stays positive. h_g=b, so for every fixed chi the
map g -> h is strictly increasing, with smooth local inverse. Its full state
map is a diffeomorphism onto an open image, since the Jacobian never vanishes.
Use seven coordinates

 r=v+cq, s=v-cq, Rplus=p+h(g,chi), Rminus=p-h(g,chi),
 Zplus=w+d k, Zminus=w-d k, and chi.                       (9)

All state-dependent inverses below are evaluated on this open image.
In particular q=(r-s)/(2c), v=(r+s)/2, p=(Rplus+Rminus)/2,
h=(Rplus-Rminus)/2, w=(Zplus+Zminus)/2, k=(Zplus-Zminus)/(2d).
Direct differentiation, retaining both derivatives of h, gives the diagonal
system

 r_t+(v+c)r_x=-g,      s_t+(v-c)s_x=-g,
 Rplus_t-b Rplus_x=A+h_chi(w-b k),
 Rminus_t+b Rminus_x=A-h_chi(w+b k),
 Zplus_t-d Zplus_x=D,  Zminus_t+d Zminus_x=D,
 chi_t=w.                                                (10)

For example the left side of the Rplus equation is
p_t-b^2 g_x+b(g_t-p_x)+h_chi(chi_t-b chi_x), proving its sign
and every extra source in (10). Treating h as independent of chi would lose
both h_chi w and h_chi b k. The B_chi k/tau source is separate and remains.
All seven right sides in (10) are smooth functions of the seven state
coordinates; none contains a differentiated iterate. Coincident speeds
among v±c,±b,±d,0 cause no denominator: the coordinate Jacobian uses only
c>0,d>0,b>0. No globally constant diagonalization or strict separation of
all seven speeds is assumed.

## 3. The converse and the two gradient constraints

We must not assume chi_x=k while proving it for a solution of (10).
The two Z equations give k_t=w_x and w_t=d^2 k_x+D exactly. Together with
chi_t=w and compatible initial chi_x=k they imply

 chi_x(t,x)=chi0_x(x)+integral_0^t w_x(z,x) dz=k(t,x).        (11)

This only differentiates the time integral of the C1 function w. Before
using (11), subtracting the R equations yields

 b(g_t-p_x)+h_chi chi_t=h_chi w,

hence g_t=p_x already. Adding those equations yields

 p_t=b^2 g_x+A+b h_chi(chi_x-k),                            (12)

whose extra term vanishes by (11). Define

 phi(t,x)=phi_e(x)+integral_0^t p(z,x) dz, phi_e'=g(0,x).    (13)

Then phi_t=p and phi_x=g(0,x)+integral p_x=g. The C1 regularity of p,g
makes phi C2; the same conclusion for chi follows from chi_t=w,chi_x=k.
Thus (12) is precisely the phi equation in (5), and the Z equations give
the chi equation. Adding/subtracting the fluid equations in (10) gives the
two equations for q,v in (6); n=nref exp(q) then gives both fluid equations
in (5). Conversely any solution of (5) with these field derivatives C1
satisfies (10). No compatibility product is discarded without its proof.

## 4. Auxiliary extension and an actual coefficient box

Pick a smooth cutoff zeta, 0<=zeta<=1, supported in U and equal to one on
a neighborhood of K0. Extend q0=log(rho/nref) and chi0 smoothly by taking
zeta times their difference from chosen constants, plus those constants.
Extend g0 by g_e=zeta g0+(1-zeta)g_*; it is globally strictly positive and
constant outside a compact interval. All background extensions have bounded
derivatives of every order. Set k_e=chi_e', p_e=w_e=0, retain the exact
compact velocity (4), and let phi_e be an antiderivative of g_e whose
additive constant makes phi_e=phi0 on K0. Although phi_e can grow linearly
on the auxiliary line, it is not an iteration coordinate; (13) and all local
energy statements are valid on compact intervals. No infinite absolute
background-energy integral is taken. This extension need not solve the
hydrostatic equations outside K0; it is only compatible initial data for
an auxiliary Cauchy construction.

The range of (q_e,v_in,p_e,g_e,w_e,k_e,chi_e) has compact closure. Let
q_- and q_+ be its min/max q, chi_- and chi_+ its min/max chi, and let
0<g_-<=g_+ be its min/max g. Choose a bounded open primitive-state box
containing that range strictly, with the particular bounds

 q_- -1<q<q_+ +1, chi_- -1<chi<chi_+ +1,
 g_-/2<g<2g_+,                                            (14)

and finite strict bounds on v,p,w,k obtained by padding their initial
ranges by any positive constants of the appropriate physical units.
The transformation (9) maps this open box diffeomorphically to an open set.
Its closure is inside the g>0 coordinate chart. On this box (2) gives
positive lower and finite upper bounds for b, and

 nref exp(q_- -1)<n<nref exp(q_+ +1),
 a_ref exp(chi_- -1)<a<a_ref exp(chi_+ +1).                 (15)

These are state bounds to be propagated, not a static assertion about g0.

For dimensionally meaningful estimates select any fixed positive length X,
time Theta, and one positive unit s_i for each physical coordinate in (9).
Write xi=x/X, t_hat=t/Theta, u_i=coordinate_i/s_i. Here chi can have s_i=1.
The transformed system is u_i,t_hat+lambda_i(u)u_i,xi=F_i(u), where lambda
is Theta/X times the physical speed and F_i is Theta/s_i times the physical
right side. Every norm and constant in Sections 5-7 is dimensionless unless
explicitly restored; hence no unlike dimensional quantities are added.
This rescaling is a unit choice, not a changed physical coefficient.

Let Dbox be the image of (14) and the other primitive bounds in these
normalized coordinates, and Kinit the compact closure of the initial u range.
Set

 delta=(1/4) dist_infinity(Kinit, R^7\Dbox)>0.              (16)

The closed 2delta-neighborhood of Kinit is compactly contained in Dbox.
Choose a smooth cutoff equal to one on that neighborhood, compactly supported
in Dbox, and multiply each lambda_i,F_i by it, extending by zero outside.
Existence of this cutoff follows by finitely many balls with closure in
Dbox and the elementary smooth bump function; one may take a product of
one-minus-bumps to cover the compact neighborhood. Denote these globally
smooth bounded coefficient extensions again by lambda,F. They agree with
(10) throughout the neighborhood that the iteration will occupy. Define
finite global constants, in maximum component norm,

 Lambda=max_i ||lambda_i||inf, F0=max_i ||F_i||inf,
 L=max_i ||D lambda_i||, K=max_i ||D^2 lambda_i||,
 P=max_i ||D F_i||, Q=max_i ||D^2 F_i||.                    (17)

Derivative norms are operator norms for l-infinity inputs (linear or
bilinear as appropriate), including all seven components. Cutoff derivatives
are included. Thus they really are Lipschitz and second-derivative bounds
even outside the chart, and require no mean-value segment to stay in Dbox.

## 5. A complete diagonal iteration in the exact C1,1 class

For the exact normalized initial data define

 M0=||u0,xi||inf, H0=max_i Lip_xi(u0,i,xi),
 M=2(M0+1), H=4[H0+K M^3+Q M^2+1],
 T0=min(1, 1/[8(1+LM+P)],
                delta/[2(1+Lambda M+F0)]).                (18)

Every quantity is finite and T0>0 for each fixed N. These are explicit
lifespan dependencies on actual extended initial norms and actual smooth
coefficient norms. No uniformity in N is asserted. In particular the original
velocity derivatives scale as V/ell~N^4 and V/ell^2~N^7, respectively;
neither is silently put into a background constant. Formula (18) has not
been converted into an N^-4 lower bound.

Start u^0(t_hat,xi)=u0(xi). Given u^j, solve by characteristics

 partial_t_hat u_i^{j+1}+lambda_i(u^j)partial_xi u_i^{j+1}=F_i(u^j),
 u_i^{j+1}(0,xi)=u0,i(xi).                                (19)

Here is the underlying construction. If ||u_xi^j||<=M, the velocity a_i
is continuous in time, C1 in space, bounded by Lambda and Lipschitz in
space with constant LM. For any terminal point solve the integral ODE
X(z)=xi-integral_z^t_hat a_i(y,X(y))dy. Its integral map is a contraction
on a sufficiently short subinterval with length times LM<1 (if LM=0,
it is independent of X differences). Iterating the map in the complete
space of continuous curves constructs the flow there; concatenation
constructs it on [0,T0], and bounded speed prevents escape. The same
integral inequality proves uniqueness. Spatial difference quotients converge
to J'=a_i,xi(z,X)J, J(t_hat)=1, by subtracting their integral equations
and using continuity of a_i,xi on compact sets. Thus the flow is C1 in
its label with positive derivative J=exp(integral a_i,xi). Define

 u_i^{j+1}(t_hat,xi)=u0,i(X(0))+
                       integral_0^t_hat F_i(u^j(z,X(z))) dz. (20)

This gives the C1 transport solution, including its time derivative from
(19). The base u^0 is C1. All iterates keep their exact initial traces.

We prove inductively ||u_xi^j||<=M and Lip_xi u_xi^j<=H, uniformly in time.
Differentiating (20) in the label gives the first-derivative equation
D_i p=-a_i,xi p+f_i,xi, where f_i=F_i(u^j). Since
|a_i,xi|<=LM and |f_i,xi|<=PM,

 ||u_xi^{j+1}(t_hat)||<=(M0+t_hat P M)exp(LM t_hat)<M.       (21)

Indeed M0<=M/2, t_hat P<=1/8, and exp(LMt_hat)<=exp(1/8)<4/3,
so the right side is at most (5/8)(4/3)M=5M/6.

For the Lipschitz bound, ||u_xi^j||<=M and Lip u_xi^j<=H imply

 Lip(a_i,xi)<=L H+K M^2,
 Lip(f_i,xi)<=P H+Q M^2.                                  (22)

Compare the first-derivative equations along two characteristics. Their
separation has logarithmic derivative in absolute value at most LM.
Subtract the p equations and divide by that separation. The coefficient
on the quotient is at most 2LM; the inhomogeneous term is bounded by
(LH+KM^2)||p||+PH+QM^2. Multiplication by the scalar integrating factor,
using (21), gives

 Lip u_xi^{j+1}(t_hat)
 <=exp(2LM t_hat)[H0+t_hat((LM+P)H+K M^3+Q M^2)]
 <=(4/3)[H/4+H/8]=H/2<=H.                                (23)

Here t_hat<=1, t_hat(LM+P)<=1/8 and exp(1/4)<4/3. This is a
pair-characteristic Lipschitz estimate: it does not assign classical
second derivatives at the polynomial joins or assume C2 initial velocity.

The PDE also gives ||u_t_hat^{j+1}||<=Lambda M+F0. Its exact initial trace
then yields the important SAME-POINT estimate

 ||u^{j+1}(t_hat,.)-u0(.)||<=t_hat(Lambda M+F0)<delta/2.      (24)

The base also satisfies it. All iterates therefore lie in the chart and
coefficient box; no componentwise initial-range convex-hull assumption is
needed. In particular the cutoff never changes the equations used there.
These estimates prove the induction and global boundedness of the iterates.

## 6. Contraction, derivative limit and local classical solution

Subtract (19) at consecutive stages, using lambda(u^j) as transport speed.
For j>=1, their initial difference vanishes and

 D_i^j(u_i^{j+1}-u_i^j)
  =-[lambda_i(u^j)-lambda_i(u^{j-1})]u_i,xi^j
                      +F_i(u^j)-F_i(u^{j-1}).              (25)

Consequently delta_j=||u^{j+1}-u^j||inf on the whole slab obeys

 delta_j<=T0(LM+P)delta_{j-1}<=delta_{j-1}/8.               (26)

The first difference is finite by (24); hence u^j converges uniformly to u.
To upgrade this to C1, for any component z=u^j-u^l one has Lip(z_xi)<=2H.
For any positive h, integrating z_xi on [xi,xi+h] gives

 |z_xi(xi)|<=2||z||inf/h+Hh,
 ||z_xi||inf<=2sqrt(2H||z||inf).                            (27)

The zero case follows by direct integration. Thus the spatial derivatives
are uniformly Cauchy, continuous, and converge to u_xi by integration in xi.
The limit retains M,H. Equation (19) then gives uniform convergence of
u_t_hat^{j+1} to -lambda(u)u_xi+F(u); integration in time identifies this
continuous limit with u_t_hat. This proves actual C1 convergence to the
classical diagonal solution with exact C1 initial trace.

Estimate (24) passes to the limit, keeping it strictly inside Dbox; therefore
(14)-(15) hold for the evolved fields and g>=g_-/2 is a propagated margin.
Apply the inverse smooth coordinate map, then the exact compatibility proof
of Section 3, to obtain (5). Smooth composition preserves C1 and bounded
spatial Lipschitz derivatives on this compact state set. The physical time
before geometrical localization is Theta T0. Field response is part of this
solution, not an externally prescribed force.

## 7. Physical localization, uniqueness and extension independence

Choose any positive physical speed epsilon and set

 S=(X/Theta)Lambda+epsilon,
 Tphys=min(Theta T0,R/(4S)),
 K_t=[x*-R+St,x*+R-St].                                   (28)

For every constructed iterate and the limit, all seven characteristic speeds
have absolute value at most (X/Theta)Lambda<S. If a backward characteristic
starts in K_t, comparison with the two affine endpoints shows it stays in
K_z at every earlier time z. For instance its distance from the left boundary,
viewed forward, has derivative speed-S<0; equivalently that distance cannot
first become negative when tracing backward. The right boundary is analogous.
Thus every backward curve used to evaluate the physical restriction begins
in K0 and stays inside U. Also the vertical segments used for (11),(13)
remain in K_z since the intervals shrink. At the chosen time the interval
still contains [x*-3R/4,x*+3R/4]. No curve touches the cusp or a wall.

For two solutions of (10) on a common compact cone with coinciding initial
traces, bounded states inside the chart, and bounded first spatial derivatives,
subtract their equations along the first solution's characteristics. On the
compact union of their state images the smooth coefficients have finite
Lipschitz bounds, obtained if necessary by a smooth cutoff as in Section 4.
If Pcomp is the other solution's gradient bound, the maximum difference obeys

 Ddiff(t)<=Ccomp integral_0^t Ddiff(z) dz.                  (29)

All characteristic segments are in the common domain. Iterating this
inequality gives Ddiff(t)<=Dmax(Ccomp t)^m/m! for every integer m; hence
Ddiff=0. This proof uses only C1 classical regularity on that compact domain.
The potentials then agree from their initial values and time derivatives.

In comparing different exterior extensions, choose S larger than BOTH finite
speed bounds and use their smaller positive existence time, shortened also
by the geometrical condition in (28). The same physical initial data on K0
and the same unextended coefficients are present on that common cone, so
(29) proves equality there. The bounds and guaranteed times may depend on
the extension, but the local physical germ does not. The same argument proves
agreement on any larger common backward domain where both solutions exist.
There is no inference that arbitrary extensions share one universal numerical
lifespan or that they are hydrostatic outside the physical patch.

## 8. Full evolving-field energy and exact control

In physical units set e(n)=c^2 n[log(n/nref)-1], p_m=c^2 n, and

 E=nv^2/2+e(n)+n phi
       +[tau p^2/2+W(g,a)+sigma w^2/2+J k^2/2+U_s(chi)]/C,
 F=nv[v^2/2+c^2 log(n/nref)+phi]-(p B+J w k)/C.             (30)

Every term is C1 in the constructed class. The fluid equations give

 partial_t[nv^2/2+e(n)]+partial_x[(nv^2/2+e(n)+p_m)v]=-nv g.

Continuity and compatibility give
partial_t(n phi)+partial_x(nv phi)=n p+nv g. Thus the combined
matter-plus-interaction exchange is +n p. The Q field identity, retaining
W_t=B g_t+W_chi w=B p_x-Tw, is

 partial_t[(tau p^2/2+W)/C]+partial_x[-pB/C]=-n p-Tw/C.      (31)

The scale identity uses k_t=w_x and its full equation:

 partial_t[(sigma w^2/2+Jk^2/2+U_s)/C]
                         +partial_x[-Jwk/C]=Tw/C.          (32)

All three sources cancel exactly, so

 E_t+F_x=0.                                                (33)

Both field fluxes in (30) are necessary. The energy is the diagnostic
fixed-reference action's specified interacting energy; positivity of its
full gravitational density is not claimed. For any C1 moving endpoints
alpha(t),beta(t) inside the physical domain,

 d/dt integral_alpha^beta E dx
 =F(t,alpha)-F(t,beta)+beta' E(t,beta)-alpha' E(t,alpha).    (34)

For K_t the last two terms are -S[E(t,beta)+E(t,alpha)]. Thus local energy
does not assert conservation on a shrinking interval or a wall problem.

For the zero-velocity control, keep exactly the hydrostatic initial fields
and density but set v_in=0. The stationary tuple n=rho,v=0,phi=phi0,
chi=chi0 satisfies ALL of (5) on U by (3). Local uniqueness identifies the
constructed control with it on the common characteristic domain, regardless
of a nonhydrostatic auxiliary exterior. Its total flux is zero and its local
energy is constant in time. This tests the actual scale balance as well as
the fluid and Q source; no force or pressure is removed.

At the initial slice of the nonzero velocity data, p=w=0, p_t=w_t=0 by
(3), and v_t=-v_in v_in', n_t=-(rho v_in)_x. It would be incorrect to
infer that p stays zero: differentiating the Q source once at that slice,
where the derivatives exist, gives tau p_tt=C(rho v_in)_x. This last
identity is only an initial diagnostic, not used in the existence proof;
the proof needs no third field derivative at the velocity joins. The exact
first-order system and (31) already show that the actual dynamic source,
including tau phi_tt, is retained at every constructed time.

## 9. Scope, units and self-review

Run this theorem separately at a_ref=9.3619e-11 and 1.1279e-10 m/s^2,
with each corresponding background and its own norms. The adopted reference
relation is a_ref=kappa c_light sqrt(G_Newton rho_Lambda,ref), with kappa
an input. Constant-vacuum reference and a frozen comparison
 a_ref=a0 E(z), E^2=.315(1+z)^3+.685,
are distinct fixed backgrounds. An evolving H/reference would have explicit
protocol work and is outside (33). Spatially and temporally varying actual
a=a_ref exp chi is an added diagnostic scale degree of freedom; it does not
establish the physical pointwise vacuum relation or two gravitational DOF.
The pressure formula a^2=kappa^2 G_Newton(-p_vac) matches the vacuum relation
only for p_vac=-rho_Lambda c_light^2. It is not the isothermal pressure p_m.

Units before normalization: phi is velocity squared, g and a acceleration,
chi dimensionless, W,T,U_s acceleration squared; tau inverse velocity
squared, sigma velocity squared, J velocity to the fourth. Thus each term
in (30) is an energy density and each field flux has energy flux units.
Sections 5-6 deliberately use fixed normalized coordinates; (28) restores
physical time and characteristic speed.

Proof-audit SELF-REVIEW primary verdict: proved as written for the local
classical construction, compatibility, box propagation, localized uniqueness
and energy identity. This is author self-review, not independent acceptance.

Dependency graph: exact Q smoothness on g>0 -> invertible characteristic
coordinate map with all source terms -> global auxiliary coefficient cutoff
-> elementary characteristic ODE construction -> uniform C1,1 iteration
bounds -> C0 contraction -> derivative interpolation and time-integrated
limit -> box propagation -> compatibility and original equations -> finite
propagation and uniqueness -> extension-independent local germ. Energy and
hydrostatic control are direct algebra using the original equations.
No external PDE theorem or empirical/computational leaf is load-bearing.

| Obligation | Status | Decisive step |
|---|---|---|
| Nine ancestry pins | passed | input_sha256.json; all match task |
| Exact C1,1 profile, no hidden C2 datum | passed | (4), pair-flow estimate (23) |
| Field-dependent coordinate sources | passed | (8)-(12), both h_chi terms |
| Coincident characteristic speeds | passed | coordinate Jacobian only needs c,d,b>0 |
| Density/scale/positive-g box | passed | (14)-(18),(24), actual evolved margin |
| Complete linear and nonlinear construction | passed | (19)-(27) |
| C0 limit upgraded to spacetime C1 | passed | (27) and integrated PDE limit |
| Gradient compatibility and field C2 | passed | (11)-(13) |
| Physical characteristic containment | passed | (28), inward-boundary comparison |
| Local uniqueness and exterior independence | passed | (29), common cones |
| Full energy, both fluxes and exchanges | passed | (30)-(34) |
| Zero-velocity control solves all equations | passed | (3), Section 8 |
| N^-4 lifespan or persistence of breakdown | not addressed | deliberately no such claim |
| Crossing/walls/global existence | out of scope | positive regular patch only |
| Physical vacuum/DOF/MONO/observations | out of scope | diagnostic model only |

Strongest safe statement is the scoped positive-time theorem above for every
fixed admissible finite N. Its constants are conservative, not numerically
evaluated or optimized. No numerical experiment, manufactured test, literature
novelty search, RAR/M transfer, filtered-MONO result, metric/photon completion,
criterion B, cluster calibration, cosmology, stability or theory closure is
claimed. The next discriminating mathematical question, separate from this
closed local construction, is whether the fixed-force compressive mechanism
survives actual evolving Q/scale feedback; it needs new estimates and is not
inherited from FGF046. Independent review of this package remains required.
