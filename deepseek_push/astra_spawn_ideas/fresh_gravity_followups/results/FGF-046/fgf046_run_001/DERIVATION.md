# FGF046: direct local construction for the unchanged C1,1 fluid data

Author /root/fgf046_author; proof only. The eight FGF046 ancestry hashes were
checked and matched before the proof was developed (source text was initially
read before that hash check). The corrected FGF045 scope is the premise.
No new stage33 root or reviewer proof was read. No PDE existence theorem,
shock theorem, or external literature mechanism is used below.

## 1. Claim card and fixed equations

Fix one inherited signed-Q background on an open regular positive-side interval
U, strictly away from the crossing and walls. Write C=4pi G_Newton,
B0_x=C rho, g0=phi0_x=sgn(B0)sqrt(B0^2+a|B0|), a=a_ref exp(chi0),
and c^2(log rho)_x=-g0, with c=c_s>0. The symbol c_light will denote the light
speed in the scale relation. Here rho>0 and g0,rho,phi0 are smooth on U.
Choose K0=[x*-R,x*+R] compactly inside U, with the stipulated center x*.
For fixed L,v0>0 and every integer N with ell=L/N^3<R/2, take EXACTLY

 v_in(x)=V f((x-x*)/ell), V=v0 N,
 f(y)=(1-y^2)^2 on |y|<1, zero otherwise; n_in=rho.             (1)

The desired equations are

 n_t+(nv)_x=0,
 v_t+v v_x+c^2(log(n/n_ref))_x=-g0(x), n_ref>0.                (2)

There is a positive time T_N explicitly specified below and a positive C1
solution on the shrinking interval K_t. Its spatial derivatives are Lipschitz
uniformly on this slab, although they need not have continuous second
spatial derivatives. The initial traces are (1). The solution is unique among
positive C1 solutions on a common compact characteristic domain with these
traces, and its restriction is independent of auxiliary exterior extensions.
For fixed background and parameters the guaranteed time is bounded below by
c_* N^-4 for all sufficiently large N, for an explicitly definable c_*>0.
This is a lower bound, not a sharp lifespan assertion.

We also prove a sufficient interior continuation gate retaining a uniform
Lipschitz bound for the spatial gradients. We DO NOT remove this higher norm
or identify every earliest endpoint as first-gradient blowup.

## 2. Exact invariants, auxiliary extension, and actual initial norms

Put q=log(n/n_ref), r=v+cq, s=v-cq, v=(r+s)/2. Direct substitution in
(2) gives, equivalently for positive C1 functions,

 r_t+(v+c)r_x=-g0,       s_t+(v-c)s_x=-g0.                     (3)

Conversely set n=n_ref exp((r-s)/(2c)). Adding and subtracting (3) gives
v_t+v v_x+c^2 q_x=-g0 and q_t+v q_x+v_x=0, proving BOTH (2).

Choose once a smooth cutoff zeta supported compactly in U and equal to one
on a neighborhood of K0. Extend q_e=zeta log(rho/n_ref) and g_e=zeta g0
by zero to R. These are bounded smooth functions with bounded derivatives.
The initial velocity (1) itself is already a compact C1,1 function on R;
it is neither mollified nor replaced. Set r_in=v_in+cq_e, s_in=v_in-cq_e.
The extension is only a device for constructing a local solution; Section 6
removes all dependence on it. No values from a crossing or wall are used.

For a pair u=(r,s), use the maximum of component sup norms. Define actual
extended norms and force bounds

 A0=||u_in||_infinity,
 M0=||partial_x u_in||_infinity,
 H0=max(Lip(r_in'),Lip(s_in')),
 Gj=||partial_x^j g_e||_infinity, j=0,1,2.                    (4)

They are finite. Writing d_f=8/(3 sqrt(3)), the unchanged polynomial has
||f||=1, ||f'||=d_f, Lip(f')=8, since f''=-4+12y^2 inside and f'=0
outside, continuously at the joins. Consequently

 A0<=V+c||q_e||,
 M0<=d_f V/ell+c||q_e'||,
 H0<=8 V/ell^2+c||q_e''||.                                  (5)

In particular H0 can grow as N^7, not N^4. It is not treated as a bounded
background constant. For an explicit sufficient time, the right sides of
(5) may replace the exact norms (4) everywhere below.

Choose any fixed positive time tau and length d. Set

 A=A0+tau G0,
 M=2(M0+tau G1+tau^-1),
 H=4(H0+tau G2+(tau d)^-1),
 T_lin=min(tau,1/(8M)).                                    (6)

A has units speed, M inverse time, H inverse length-time. The harmless floors
avoid division by zero. No large-N argument is needed for positivity of T_lin.
Notice the time restriction involves M, while H is a genuine finite bound
which will control the derivative convergence.

## 3. Linear transport construction and iteration bounds

The complete ambient space is C_b([0,T]xR;R^2), with uniform norm. The
iterates additionally lie in C^1([0,T]xR) with uniform bounds

 ||u^k||<=A, ||u_x^k||<=M, sup_t Lip_x(u_x^k(t,.))<=H.         (7)

Their initial trace is u_in. Begin u^0(t,x)=u_in(x). Given u^k, put
v^k=(r^k+s^k)/2 and solve the two LINEAR transport equations

 partial_t u_i^{k+1}+a_i^k partial_x u_i^{k+1}=-g_e,
 a_+^k=v^k+c, a_-^k=v^k-c,
 u_i^{k+1}(0,x)=u_in,i(x).                                 (8)

Here is the construction rather than an imported linear PDE theorem. For
terminal (t,x), let X_i^k(z;t,x) solve X'=a_i^k(z,X), X(t)=x. The integral
map for this ODE is a contraction on every subinterval of length <1/M;
its iterates converge uniformly because |a_x|<=M. The bound |a|<=A+c
prevents escape to infinity in finite time. Concatenation constructs the
flow on [0,T], and the same Lipschitz estimate proves uniqueness. Difference
quotients of its integral equation converge to the solution of
J'=a_x(z,X)J, J(t)=1, so J=exp(integral_t^z a_x). Uniform continuity of
a_x on compact sets justifies this passage; the exponential bound is global.
The integral formula

 u_i^{k+1}(t,x)=u_in,i(X_i^k(0;t,x))
                   -integral_0^t g_e(X_i^k(z;t,x)) dz         (9)

therefore gives a C1 function and exactly (8). This requires only C1 spatial
initial data and C1 coefficients, including at the polynomial joins.

For p=partial_x u_i^{k+1}, differentiation in the characteristic label gives

 D_i^k p=-(v_x^k)p-g_e',
 ||p(t)||<= (M0+t G1) exp(Mt).                              (10)

For clarity the Lipschitz estimate does not assume classical second
derivatives of the data. Compare (10) along two characteristics X,Y. Their
distance obeys |(log|X-Y|)'|<=M. Divide the difference of their p equations
by |X-Y|: the coefficient on the quotient is bounded above by 2M, while
the inhomogeneous term is at most H||p||+G2, since v_x^k is H-Lipschitz.
Scalar integration yields

 Lip_x p(t)<=exp(2Mt)[H0+t(H sup_{z<=t}||p(z)||+G2)].         (11)

This argument uses only absolutely continuous scalar equations and the
Lipschitz property. It proves (11) directly, without smoothing the initial
polynomial or postulating a bounded classical second derivative.

Now assume (7) for u^k and take T<=T_lin. Formula (9) bounds amplitudes by
A0+TG0<=A. Since MT<=1/8,

 ||u_x^{k+1}||<2(M0+tau G1)<=M,
 Lip_x(u_x^{k+1})
 <=exp(1/4)[H0+tau G2+THM]
 <=(4/3)[H/4+H/8]=H/2<=H.                                 (12)

The strict numerical estimate exp(1/4)<4/3 follows, for example, from
exp(x)<=1/(1-x) for 0<=x<1, by comparing its power series termwise.
Thus all iterates stay in (7). The starting function satisfies the bounds.
Their time derivatives also obey

 ||u_t^{k+1}||<= (A+c)M+G0.                                (13)

## 4. Contraction, recovery of C1, initial trace, and positivity

For k>=1, subtract the k+1 and k equations, transporting the difference
with a_i^k. Their common initial data cancel and

 D_i^k(u_i^{k+1}-u_i^k)
       =-(v^k-v^{k-1}) partial_x u_i^k.

Consequently, writing delta_k=||u^{k+1}-u^k||,

 delta_k<=TM delta_{k-1}<=delta_{k-1}/8.                    (14)

The finite first difference starts a convergent geometric series. Hence
u^k converges uniformly on the entire slab to a continuous bounded pair u.
Contraction in C0 alone would not be enough; here is the missing derivative
step explicitly. If h is any component of u^k-u^j, then Lip(h_x)<=2H.
For every a>0, integration over [x,x+a] gives

 |h_x(x)|<=2||h||/a+H a.

When ||h||>0 choose a=sqrt(2||h||/H). Thus

 ||h_x||<=2 sqrt(2H||h||),                                (15)

and the zero case follows directly. This is uniform in t. Therefore u_x^k
is uniformly Cauchy. Integration in x identifies its continuous limit with
u_x. The limit inherits ||u_x||<=M and Lip_x(u_x)<=H, including at t=0.
Finally (8) gives u_t^{k+1}=-a^k u_x^{k+1}-g_e. The right sides converge
uniformly to -a(u)u_x-g_e. Integrating in t shows that u_t exists, is
continuous, and equals that limit. This proves u is C1 in both variables,
not merely a continuous or weak solution. One-sided time derivatives are
understood at the initial and final slices. Initial traces and their spatial
derivatives agree exactly with the C1,1 initial functions, because every
iterate has that trace.

Use Section 2 to reconstruct (n,v). Since |r|,|s|<=A,

 n_ref exp(-A/c)<=n(t,x)<=n_ref exp(A/c).                    (16)

Both are finite and strictly positive for every fixed N; uniformity in N is
not asserted. The exponential chain rule proves n,v are C1 with spatially
Lipschitz first derivatives, and both original equations hold pointwise.
The actual initial acceleration is v_t(0)=-v_in v_in', because the exact
hydrostatic density balances g0 on K0. No stationary velocity was prescribed.

## 5. Explicit physical patch and lower lifespan

Let Q_K=max_K0 |log(rho/n_ref)| and G_K=max_K0 |g0|, and use the SAME
physical cone speed as the FGF045 author proof,

 S_N=V+c Q_K+G_K tau+2c,
 K_t=[x*-R+S_N t,x*+R-S_N t],
 T_N=min(T_lin,R/(4S_N)).                                 (17)

For t<=T_N this cone contains [x*-3R/4,x*+3R/4]. On any interval where
|v|+c<S_N there, all backward +/- and material characteristics stay in
K_z for earlier z: its endpoints move inward faster than those speeds.
Integrating (3) along such curves gives

 |r|,|s|<=V+c Q_K+G_K t,
 |v|+c<=V+c Q_K+G_K tau+c<S_N.                             (18)

Initially the strict inequality holds. A first-contact argument on the
compact cone shows it cannot fail; the a priori bound has a margin c.
This validates backward containment and (18) for the whole constructed
slab. It uses no information outside K0 and no stationary-support assumption.

For a quantitative asymptotic lower bound define the N-independent positive
constants

 m_bar=2[d_f v0/L+c||q_e'||+tau G1+tau^-1],
 s_bar=v0+c Q_K+G_K tau+2c,
 c_*=min(tau,1/(8 m_bar),R/(4 s_bar)).                     (19)

For N>=1, M<=m_bar N^4 and S_N<=s_bar N, so T_N>=c_* N^-4,
provided the support gate ell<R/2 holds. If one uses the upper bounds (5)
instead of actual norms, the same inequality is immediate. The units of
c_* are time and N is dimensionless. The coefficient depends on the chosen
fixed regular patch and its cutoff, not on N. H grows as N^7 but remains
finite for each N; its appearance in (15) affects the convergence constants,
not the contraction ratio or the proven time power. This does not claim a
uniform C1,1 norm over the family.

## 6. Uniqueness and independence of auxiliary extensions

Let u and tilde u be two positive C1 solutions after invariant conversion,
with identical data on K0 and the same physical g0. On a common compact
cone whose backward characteristics lie inside their domains, transport the
difference using u's characteristics:

 D_i(u_i-tilde u_i)=-(v-tilde v) partial_x tilde u_i.

A finite bound P for |partial_x tilde u| on that compact slab yields
D(t)<=P integral_0^t D(z) dz for the supremum difference on K_t. Iterating
this inequality gives D(t)<=D_max(Pt)^k/k! for every k, hence D=0.
This proof needs only positive C1 solutions with finite compact-slab bounds,
not a C1,1 hypothesis on the competitor. The same proof applies to a cone
started at any later slice.

Every auxiliary extension construction agrees with the physical initial
r,s,g0 on K0 and satisfies the intrinsic speed bootstrap (18). Two such
solutions therefore agree on their common K_t existence interval. If an
extension with a shorter guaranteed time is chosen, this only shortens the
comparison interval; it does not supply distinct physical data. Thus the
constructed physical germ and all its locally unique continuations depend
only on the given initial data and force in the regular patch. The extension
was smooth only for q_e and g_e; the velocity profile was kept exactly C1,1.

## 7. Sufficient interior continuation gate, with its higher norm retained

Here is an explicit gate, not an assertion that its failure is a shock.
Suppose a constructed solution is defined for t0<=t<t_*<infinity on an open
neighborhood of a closed interval I compactly inside U. Fix a smaller closed
interval J inside the interior of I. Suppose uniformly for these times and
x in I that

 0<n_-<=n<=n_+<infinity, |v|<=V_*,
 max(|r_x|,|s_x|)<=P_*<infinity,
 max(Lip_I r_x,Lip_I s_x)<=K_*<infinity.                    (20)

The finite constants n_-,n_+,V_*,P_*,K_* are actual required bounds. The
spatial force and its first two derivatives stay bounded on the regular
neighborhood. Equivalently, suitable positive-density bounds and bounded
C1,1 spatial norms of n,v suffice, by the logarithm chain rule. We do not
assume (20) automatically from a first-gradient bound.

Set A_*=V_*+c max(|log(n_-/n_ref)|,|log(n_+/n_ref)|).
Equation (3) implies |u_t|<=(A_*+c)P_*+G_K0 on I, with G_K0 the
force bound there. Spatial gradients have continuous characteristic-label
equations D_i p=-v_x p-g0'. Their right sides are bounded by P_*^2+G_K1.
On a smaller fixed interval I' containing J with positive margin inside I,
short backward characteristics stay in I. Comparing p(t+h,x) first with
p(t,X(t;t+h,x)) and then with p(t,x) gives

 |p(t+h,x)-p(t,x)|
 <=[P_*^2+G_K1+K_*(A_*+c)] |h|.                          (21)

For sufficiently short h this is uniform on I'; subdividing time intervals
proves the Cauchy property as t approaches t_*. Thus u and u_x have uniform
limits on I', giving a C1,1 spatial trace u_* with the same bounds.
The limiting spatial derivative is identified by integrating over spatial
segments, just as in Section 4. The PDE right side also has a continuous
limit, so u_t extends continuously to this slice.

For an explicit restart choose a fixed smooth cutoff theta supported in the
interior of I', equal to one on a neighborhood J_delta of J whose margin is
delta>0. Extend theta u_* by zero to R. With Cj=||theta^(j)|| and
0<=theta<=1 its initial bounds are

 A0,new<=A_*,
 M0,new<=P_*+C1 A_*,
 H0,new<=K_*+2C1 P_*+C2 A_*.                              (22)

Use an auxiliary smooth force extension agreeing with g0 on I', and its
bounds G0,new,G1,new,G2,new. Equations (6)-(16), with these inputs, give a
new solution through t_* for a time at least

 delta_t=min(tau,1/(8M_new),
             delta/[2(A_*+tau G0,new+c)]),
 M_new=2(P_*+C1 A_*+tau G1,new+tau^-1).                   (23)

This is strictly positive. The finite H_new constructed from (22) is needed
for the new iteration and C1 limit. The last gate prevents a characteristic
from J leaving J_delta during the restart. At t_* the traces and PDE time
derivatives coincide, so adjoining the old and new solutions gives a C1
solution on a neighborhood of {t_*}xJ. Its spatial derivatives remain
locally Lipschitz. Uniqueness on smaller characteristic cones makes this
extension independent of restart choices. No external boundary data are
prescribed or inferred.

For endpoints of a shrinking cone the gate applies to any interior compact
J and a buffered interval I contained in the earlier cone for times close
to t_*. It does not automatically extend a lateral boundary or provide one
uniform neighborhood covering an entire open domain. A positive geometrical
buffer is part of the gate. In particular we have not proved that K_* stays
bounded solely from P_*; omitting K_* from an endpoint classification would
be an additional, unsupported implication in this package.

## 8. Applying the pinned conditional obstruction, and exact scope

The construction supplies an actual locally unique positive C1 branch for
the exact data used in FGF045, on the same cone for a positive initial time.
For N satisfying the additional explicit large-N gates of the pinned FGF045
author proof, every continuation of THIS branch that covers its stipulated
cone is subject to that proof: no positive C1 continuation covers the entire
cone through B/omega, omega=v0 N^4/L. Its pressure-retaining weighted
characteristic identities apply to our C1 class, including the non-C2 joins.
Thus the lower existence scale c_*N^-4 and the conditional upper obstruction
B L/(v0 N^4) concern the same actual initial branch and same physical patch.
Their constants are conservative; no sharp time is computed.

This does not assert existence of a solution all the way to the upper time,
a shock, a post-breakdown entropy solution, or first-gradient divergence at
every earlier endpoint. A continuation failing earlier may fail a condition
of the sufficient gate, including K_* or its spatial buffer. Proving that
bounded lower norms control K_* on a needed moving patch would be a separate
analytic improvement, not an inference from the obstruction. The root FGF045
CORRECTION remains respected.

## 9. Energy identity in the constructed class and hydrostatic control

Let e(n)=c^2 n[log(n/n_ref)-1], p=c^2 n and

 E=nv^2/2+e(n)+n phi0,
 F=nv[v^2/2+c^2 log(n/n_ref)+phi0].                        (24)

All these functions are C1. Multiply the actual momentum equation by nv
and use actual continuity. Kinetic energy K=nv^2/2 obeys
K_t+(vK)_x=-v p_x-nv g0; internal energy obeys
e_t+(ve)_x=-p v_x; interaction energy obeys
(n phi0)_t+(nv phi0)_x=nv g0. Addition gives

 E_t+F_x=0.                                                (25)

Hydrostatic balance makes mu=c^2 log(rho/n_ref)+phi0 constant. Subtracting
the background and mu(n-rho) gives the nonnegative relative energy density
and its corresponding flux

 E_rel=nv^2/2+c^2[n log(n/rho)-n+rho],
 F_rel=nv[v^2/2+c^2 log(n/rho)],
 (E_rel)_t+(F_rel)_x=0.                                   (26)

For any C1 moving interval [a(t),b(t)] lying in the constructed domain,

 d/dt integral_a^b E dx
   =F(t,a)-F(t,b)+b'(t)E(t,b)-a'(t)E(t,a),                (27)

and the identical formula holds for E_rel,F_rel. In particular the shrinking
cone has the additional terms -S_N[E(t,b)+E(t,a)]; there is no assertion
that energy on that cone is conserved. A fixed interval retains -[F]_a^b.
No global wall solution is constructed. Conditional zero-flux conservation
on a separate compatible fixed-wall solution is not needed here.

At the initial slice v_t=-v v_x, which removes FGF044's stationary-velocity
energy defect. Choosing v_in=0 instead, n=rho and v=0 solves (2) exactly on
the regular patch for all times; the local uniqueness proof identifies this
with the constructed local control. It has zero relative energy and flux.
Its hydrostatic force/pressure balance, not a removed pressure or force,
accounts for the control. It does not satisfy the large compressive trigger.

## 10. Dimensions, scales, branches, and remaining physical obligations

The fixed fields still have Rphi=C(n-rho), C=4pi G_Newton, and Rchi=0.
This generally nonzero source residual is not canceled by solving the two fluid
equations. No coupled-gravity evolution or residual norm estimate follows.
All force bounds use Gj, never G_Newton. The norms in (4)-(6) have the units
stated there; H0~v0 N^7/L^2 while M0~v0 N^4/L. T_N is a physical time.

Run this entire local theorem separately for a_ref=9.3619e-11 and
1.1279e-10 m/s^2, with the corresponding regular signed-Q background and
its own constants. The adopted relation is a=kappa c_light sqrt(G_Newton
rho_Lambda), with kappa an input. Constant vacuum gives constant reference
scale. A frozen-H comparison a_ref=a0 E(z), E^2=.315(1+z)^3+.685 is a
separate fixed reference, not an evolving-H solution. Time-dependent fields
would require new forcing and energy accounting; (25) uses phi0_t=0.
The pressure relation a^2=kappa^2 G_Newton(-p) equals the vacuum relation
only for p=-rho_Lambda c_light^2. No such equation of state for this fluid
is inserted: its retained pressure is p=c_s^2 n.

Signed Q is never replaced by Newtonian missing mass or by R, M, RAR, or
filtered MONO. No physical scale reservoir, metric/photon dynamics, degrees
of freedom, instrument independence, observational fit, novelty, global
stability, or theory closure is asserted. The unbounded diagnostic speed
sequence is not a claim of physically admissible relativistic flow.

## 11. Proof-audit self-review

Primary verdict: proved as written for the scoped local construction and
higher-norm sufficient continuation gate. This is author self-review, not
an independent referee judgment or promotion.

Dependency graph: exact transformation (2)<->(3) -> elementary ODE flow
construction -> uniform amplitude/C1/Lipschitz bounds -> C0 contraction ->
interpolation recovers C1 -> positivity and both equations -> cone containment
and uniqueness remove extension dependence -> trace/restart proves the
specified continuation gate. Separate algebra gives energy and control.
Only the final upper-obstruction corollary imports a prior local theorem,
namely the exact pinned FGF045 proof with its corrected scope.

| Obligation | Status | Decisive locator |
|---|---|---|
| Unchanged C1,1 polynomial, actual norm scaling | passed | (1),(5) |
| Pressure, force, positive density retained | passed | (3),(16), converse derivation |
| Linear existence is constructed | passed | ODE integral contraction and (9) |
| No hidden C2 requirement | passed | pair-characteristic quotient (11) |
| Uniform iteration closes | passed | (10)-(14) |
| C0 convergence upgraded to C1 in both variables | passed | (15), time-integrated limit |
| Initial traces and both original equations | passed | Section 4 |
| Explicit positive time with actual norms | passed | (6),(17),(19) |
| Patch and extension independence | passed | (18), Section 6 |
| Buffered interior continuation retaining H | passed | (20)-(23) |
| Energy boundary terms and hydrostatic control | passed | (24)-(27) |
| Same-branch conditional upper obstruction | passed subject to pinned FGF045 gates | Section 8 |
| First-gradient-only endpoint classification | not addressed | K_* retained |
| Coupled field evolution, evolving-H closure | out of scope | Section 10 |

No mathematical executable computation was used. Metadata hashing and JSON
validation are not numerical PDE tests. No failed mathematical route is being
reported as a refutation. The smallest remaining analytic improvement would
be a direct estimate controlling the Lipschitz gradient norm from specified
lower norms on a buffered moving cone, if first-gradient endpoint
classification is desired. It is not required for the theorem proved here.
