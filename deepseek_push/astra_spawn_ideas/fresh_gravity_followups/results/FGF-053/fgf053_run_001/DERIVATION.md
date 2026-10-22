# FGF053: a buffered maximal classical germ and its first-gradient obstruction

Author `/root/fgf053_author`, run `fgf053_run_001`. One bounded proof-only pass.
All twelve task ancestry pins and the task hash were checked before ancestry
source use. This is an author candidate requiring separate review. No new
stage40 coordinator/reviewer proof or preview was read. Zero mathematical
executable computations; hash verification is metadata, not a machine proof.

## 1. Exact system, units, and claim

Fix the task's positive physical coefficients, smooth compatible hydrostatic
background on U, and positive L,v0,nref, independently of N. Use the fixed
FGF048 units X=(x-x*)/L, t=v0 t_physical/L, n=n_physical/nref,
v=v_physical/v0, g=g_physical L/v0^2. Field derivatives and all coefficients
have the corresponding FGF048 units; all norms below are dimensionless.
In particular c=cs/v0>0 is sound speed, not light speed. Suppress hats.
Put q=log n, p=phi_t, g=phi_X, w=chi_t, k=chi_X, a=a_ref exp chi, and

    B=(sqrt(a^2+4g^2)-a)/2, W(g,a)=integral_0^g B(s,a) ds,
    Tscale=-W_chi, U_s(chi)=S0[cosh(2chi)-1]/4.

The full equations are

    q_t+v q_X+v_X=0, v_t+v v_X+c^2 q_X=-g,
    g_t=p_X, tau p_t=B_g g_X+B_chi k-C exp q,
    k_t=w_X, sigma w_t=J k_X+Tscale-U_s', chi_t=w.       (1)

The background H has v=p=w=0, n=rho>0, g=g0>0 and

    (B0)_X=C rho, c^2(log rho)_X=-g0,
    J(chi0)_XX+Tscale(g0,chi0)-U_s'(chi0)=0.

Initial fields/density are H and v=N f(X/ell), ell=N^-3, where
f(y)=(1-y^2)^2 on |y|<1 and zero elsewhere. Exactly C1,1 joins are
retained. No smoothing, pressure deletion or static replacement of (1).

Claim: for every fixed B_dagger>15/8 and all sufficiently large N, there is
an extension-independent maximal positive classical whole-core germ with

    kappa N^-4 <= T_N <= B_dagger N^-4,                  (2)

where kappa>0 is independent of N. On its branch the full field state stays
in a fixed compact positive chart; n has finite positive bounds for each
fixed N. For U=(r,s,z) defined below, the particular norm

    D_N(t)=max{||r_X||_I,||s_X||_I,max_i ||z_i,X||_I}

satisfies

    limsup_(t upward T_N) D_N(t)=infinity.               (3)

I and the germ, including the meaning of maximality, are constructed in
Sections 3–4. All claims concern this local autonomous diagnostic and its
inherited source-pinned existence/edge theorems. They do not classify a shock,
prove a weak continuation, or assert physical theory failure.

## 2. The exact chart and characteristic equations

Set b=sqrt(B_g/tau)>0, d=sqrt(J/sigma)>0,
h(g,chi)=integral_(g_*)^g b(s,chi) ds with fixed g_*>0, and

    r=v+cq, s=v-cq,
    R_+=p+h, R_-=p-h, Z_+=w+d k, Z_-=w-d k,
    z=(R_+,R_-,Z_+,Z_-,chi).

The inverse is smooth for g>0: h_g=b, p=(R_++R_-)/2,
w=(Z_++Z_-)/2 and k=(Z_+-Z_-)/(2d). Write
A=B_chi k/tau-C exp(q)/tau and D=(Tscale-U_s')/sigma. Then EXACTLY

    D_(v+c) r=-g, D_(v-c) s=-g,
    D_(-b) R_+=A+h_chi(w-bk),
    D_(+b) R_-=A-h_chi(w+bk),
    D_(-d) Z_+=D, D_(+d) Z_-=D, chi_t=w.               (4)

Thus z_i,t+lambda_i(z)z_i,X=H_i(q,z). Both scale terms and both h_chi
terms remain; H_i depends on density through exp q. There is no v in the
field speeds or sources, and no division by differences of family speeds.
The inverse characteristic system implies (1) for compatible data: from Z
we get k_t=w_X, from chi_t=w we propagate chi_X=k; subtraction of the R
relations gives g_t=p_X, while addition gives

    p_t=b^2 g_X+A+b h_chi(chi_X-k).

The final term therefore vanishes. Given phi at a time slice, reconstruct
phi(t,X)=phi(slice,X)+integral p(u,X)du; then phi_X=g. This verifies
actual dynamic Q and scale compatibility, including at a restart.

## 3. Fixed spatial buffers and exact exterior collars

Choose [-R,R] compactly inside U in these units, with room for a slightly
larger open neighborhood. Fix a bookkeeping constant B0>B_dagger and
Theta0=B0 N^-4. Use FGF052 Section 2's edge constants R_i,S,k_edge,
d_e=R_i/2 and r_e=R_i/4 (d_e is unrelated to scale speed d), and put

    h_N=N^-7/2,
    A_N=-ell-d_e h_N, D_N=ell+d_e h_N, I=[A_N,D_N].

For N large, the exact hydrostatic exterior cones centered at A_N,D_N have
initial half-width r_e h_N and shrink at speed S. The conditions

    B0 N^-1/2 <= k_edge, S B0 N^-1/2 < r_e/2          (5)

ensure they contain the fixed collars

    C_A={|X-A_N|<r_e h_N/2}, C_D={|X-D_N|<r_e h_N/2}

for all 0<=t<=Theta0. These open collars lie outside the packet initially.
Their equality to H is a PDE uniqueness statement, not a claim that high
initial fluid speed cannot move a packet. Here the pinned FGF052 proof,
using FGF051's known edge branches, supplies that equality on any existing
positive classical whole branch covering these common cones.

For clarity, comparison does not assume a speed bound on the unknown branch.
Use the known edge branch's characteristic curves (speed <S) and subtract
(4). The coefficient difference multiplies the other solution's bounded
first derivative on each compact existing slab. The resulting inequality
sup|difference|(t)<=C integral_0^t sup|difference|(u)du, with zero initial
difference, proves equality by iteration. The edge branch itself equals H
by the same argument. No core existence is imported from edge existence.
Positivity needed for the chart is maintained in these collars by equality
to H. The result includes all first derivatives and phi=phi0, since p=0.

A classical core restriction through any T<Theta0 can now be glued to H
outside I on the fixed interval J=(-R,R): use the core inside I and H
outside. The two definitions agree on OPEN collars, so this is an actual
classical solution, not a boundary-value approximation. It solves (1) on J;
its potentials also glue, since both endpoint values equal phi0,chi0.
Artificial extensions used to construct a Cauchy solution are discarded.
The gluing does not require the background to be globally hydrostatic on R.

## 4. Definition, uniqueness and the actual maximal germ

An admissible segment of length T<Theta0 is a solution on [0,T] x J,
C1 in all first-order variables, C2 in phi,chi, positive n,g, with the exact
initial data. It is spatially C1,1 locally uniformly on every compact time
slab, equals H outside I, and on fixed collars of radius r_e h_N/4 at A_N,D_N.
It has the initial potential gauge phi0. Equivalent descriptions are core
restrictions with the exact stationary collars, patched as in Section 3.
The larger radius r_e h_N/2 follows for every such segment from the edge
comparison; this extra margin is reserved for restart.

Any two admissible segments coincide. Along characteristics of the first
solution inside I, stop at the initial line or the first lateral contact.
The two solutions coincide at each such starting contact (both are H on
lateral collars). Smooth coefficient difference bounds on the compact union
of their state ranges and the finite gradient bound of the second solution
give sup_I|difference|(t)<=C integral_0^t sup_I|difference|(u)du.
Iterate this integral inequality to obtain zero. On J\I both are already H.
Potential equality follows from equal p and equal initial gauge. This also
proves uniqueness against a C1 competitor; C1,1 is not used in this comparison.

FGF048 constructs the exact data through kappa N^-4 on a contained physical
cone with fixed outer buffers. For N large this cone contains I and both
edge cones. Its restriction agrees with H in the collars by Section 3.
Patching it to H therefore gives an admissible segment of that SAME length,
with precisely the same equations and regularity as used by the upper proof.
Shrink kappa once if necessary so kappa<B_dagger. This is an actual lower
branch, not a claimed existence interval obtained just by matching exponents.

Let T_N be the supremum of lengths of admissible segments, bounded above by
Theta0 for definition only. Uniqueness identifies every overlap; the union
is a single solution on [0,T_N) x J. Every compact slab below T_N lies in
one such segment and inherits its regularity. There is no arbitrary choice
of an auxiliary extension or a selected maximal chain in this definition.

FGF052 with its accepted ROOT_TRANSFER_BOOTSTRAP excludes an admissible
segment through B_dagger N^-4. If T_N>B_dagger N^-4, the union would contain
such a closed slab. Consequently T_N<=B_dagger N^-4<Theta0. The bookkeeping
cap is strictly inactive. The interval J has fixed spatial size, the core
I lies in its center, and collars have fixed positive width for each fixed N.
A loss of this definition is not a cone tip reaching an artificial wall.

It also cannot result solely from a bad auxiliary exterior: any continuation
of the same germ defined on a neighborhood of the core and its edge cones
has the same H collars by Section 3 and patches to an admissible segment.
Conversely an admissible segment is itself such a local physical continuation.
Different auxiliary extensions, background neighborhoods containing these
buffers, or bookkeeping horizons yield the same overlapping germ by uniqueness;
whenever their bookkeeping caps are inactive they have the same maximal time.
No assertion is made about a continuation defined only at an isolated point
while abandoning part of the whole packet.

## 5. Actual field margins and fixed-N fluid amplitudes

Here is the source mechanism, included to specify its domain and to avoid
mistaking the original FGF052 author's conditional verdict for the later
accepted theorem. Work on any admissible slab t<T_N. Near z*=z0(0), choose
a fixed compact smooth chart neighborhood K, and a delta-ball whose doubled
ball stays in g>0 with bounded chi,p,w,k. Bootstrap |z-z*|<delta on I.
There |g|<=Gbar, |lambda_Q|<=Lambda, the regular parts of both Q sources
are bounded by Hbar, and scale sources by Zbar. Initial and lateral data
are within C0 ell of z*, since the background is fixed smooth.

Let Q0 bound |log rho| on the fixed background neighborhood, and suppose
Theta0<=1. Both acoustic equations in (4), stopped at initial or first
lateral contact, give r,s>=-L0, L0=cQ0+Gbar. Since initial velocity is
nonnegative, no N enters this lower bound. On the actual set v<=Lambda+1,

    |q|<= (Lambda+1+L0)/c, n<=Ncut=exp((Lambda+1+L0)/c).

Exact stationary boundaries imply M=int_I n=int_I rho=O(ell). The mass
primitive m(t,X)=int_(A_N)^X n satisfies m_X=n, m_t=-nv, 0<=m<=M.
Along either Q path of speed lambda in I,

    d m/dt=-(v-lambda)n.

Split the WHOLE path into H={v>Lambda+1} and L={v<=Lambda+1}. On H,
v-lambda>1; on L, n<=Ncut and |v-lambda|<=Ccut for a fixed Ccut.
One signed integration, not one charge per crossing, gives

    integral_path n dt <= M+(Ccut+1)Ncut t.             (6)

Integrating the two actual Q equations, both scale equations and chi_t=w
from their initial/lateral contacts yields

    sup_I |z(t)-z*| <= C1 ell+C2 t.                     (7)

Vertical paths for chi stay in I. For large N and t<=Theta0, (7)<delta/2,
so a first-exit argument strictly closes the field bootstrap on every existing
slab, regardless of its derivatives. Thus g>=g_min>0, a>=a_min>0 and
all p,g,w,k,chi have fixed finite bounds on the core. Outside I they equal
the fixed smooth H. All margins hold up to the approached endpoint by
continuity of the bounding inequalities; existence at that endpoint has
not been assumed.

Now also use the UPPER acoustic bounds. Initial r,s<=N+cQ0 and lateral
r,s<=cQ0; the force bound gives on the core

    |r|,|s|<=K_N:=N+cQ0+Gbar Theta0,
    |v|<=K_N, |q|<=K_N/c,
    exp(-K_N/c)<=n<=exp(K_N/c).                         (8)

These are fixed-N bounds, generally exponential in N. They are NOT uniform
density estimates. They include all first lateral contacts, where the data
are exactly hydrostatic, and all initial contacts. Outside I use H's bounds.

Let Lambda_outer bound all field speeds on K and on H over [-R,R]. Choose
S_N strictly larger than K_N+c, Lambda_outer, and all background sound
speeds, with S_N=O(N). For large N, S_N Theta0<R/8 and I and its collars
lie in [-R/4,R/4]. The backward-contained cones

    K_t=[-R+S_N t,R-S_N t]

therefore contain the fixed restart interval [-R/2,R/2] with a positive outer
buffer through Theta0. Every fluid, field and vertical characteristic used
for the estimates below stays in earlier K_u. This explicitly removes outer
boundary contact from the higher-norm proof. The solution is H on K_t\I.

## 6. Bounded first gradients propagate the complete C1,1 seminorm

Suppose, toward a contradiction, limsup_(t upward T_N) D_N(t)<infinity.
Compact earlier slabs then give a bound D_N(t)<=M1 on all [0,T_N).
Outside I, the derivatives are those of H. By (7)–(8) the complete state
range is compact for this fixed N, with all chart and density margins.
Smooth cutoffs outside a larger coefficient neighborhood give genuine finite
coefficient derivative bounds without assuming line segments stay in the chart.

On K_t set A=max(||r_X||,||s_X||), Bf=max_i||z_i,X||,
Hf=max(Lip r_X,Lip s_X), Hz=max_i Lip z_i,X. For H_i(q,z), lambda_i(z)
and g(z), take bounds P,Q on first/second source derivatives, L1,L2 on
first/second field speed derivatives, and G,G2 on first/second derivatives
of g. P,Q INCLUDE exp(q), all scale terms and their derivatives, and may
depend on N. The actual gradient equations are

    D_(v+c) r_X=-v_X r_X-g_X,
    D_(v-c) s_X=-v_X s_X-g_X,
    D_i z_i,X=-(D_z lambda_i.z_X)z_i,X
                      +H_i,q q_X+D_z H_i.z_X.         (9)

In particular the Q density derivative -C exp(q)q_X/tau remains in (9).
There is no purported cancellation between density sources on different paths.

Compare (9) along two characteristics of the same family and divide their
gradient difference by the spatial separation. That separation's logarithmic
rate is bounded by A for the fluid or L1 Bf for a field. The two transport
terms and differentiated velocity coefficient give 3A Hf. Composition of
g_X gives G Hz+G2 Bf^2. For fields the three speed terms give
3L1 Bf Hz+L2 Bf^3, while the complete source gives
P(Hz+Hf/c)+Q(Bf+A/c)^2. Thus, on backward-contained K_t,

    Hf(t)<=Hf(0)+integral_0^t [3A Hf+G Hz+G2 Bf^2]du,
    Hz(t)<=Hz(0)+integral_0^t [(3L1 Bf+P)Hz+(P/c)Hf
                              +L2 Bf^3+Q(Bf+A/c)^2]du. (10)

Two terminal points in K_t have backward paths in earlier K_u; their
intervening segments also lie there because K_u is an interval. This
justifies the spatial Lipschitz coefficient estimates. Positive flow Jacobians
follow from J'=lambda_X J. The inequalities are difference-quotient estimates,
valid at the original joins, not a classical f'' assertion. Equivalently one
may integrate the a.e. weak equations for Lipschitz gradients. They first
hold on each compact admissible slab, where C1,1 is already supplied; their
uniform bound prevents loss of that regularity at the supremum time.

Since A,Bf are bounded, (10) yields finite constants E_N,F_N with

    Hf(t)+Hz(t)<=[Hf(0)+Hz(0)+F_N t] exp(E_N t) <= H_N. (11)

No N-uniform bound or continuation length is claimed here. The initial
finite seminorm contains the exact 8N^7 velocity contribution.

## 7. Actual endpoint trace, compatible gluing and restart

On the fixed interval J1=[-R/2,R/2], all state first derivatives are bounded
and their spatial Lipschitz seminorms are bounded by (11). The diagonal PDE
bounds U_t uniformly. In distributions, and a.e. in space,

    (U_i,X)_t=-lambda_i U_i,XX
              -(D_U lambda_i.U_X)U_i,X+D_U F_i.U_X.    (12)

Every term is uniformly bounded for this fixed N. Distributional integration
of (12) implies ||U_X(t)-U_X(s)||_infinity<=C_N|t-s|: first it holds for
a.e. spatial representative, then for all spatial points by continuity.
Similarly ||U(t)-U(s)||<=C_N|t-s|. Thus U and U_X have actual uniform
limits U*,V* on J1 as t upward T_N. Integration along spatial segments shows
V*=(U*)_X. Passing (11) through the limit proves U* is C1,1. Passing the
PDE expression for U_t shows its uniform limit is F(U*)-lambda(U*)V*.
This supplies the time derivative needed for classical gluing at T_N.

Smooth inversion gives compatible primitive C1,1 traces with n*>0,g*>0
and bounded chi*. Since chi_X=k on every earlier slice, C1 convergence
gives chi*_X=k*. Set phi*=phi0+integral_0^(T_N) p dt on J1. The integral
converges with its spatial derivative, phi*_X=g*, and p* is its time-velocity
trace. In fact phi* is spatial C2,1 because g* is C1,1; the spacetime
potential after restart will be C2. The traces on the larger collars C_A,C_D
are EXACTLY H, including phi*=phi0 and chi*=chi0. Both boundary potential
constants match; merely gluing g without checking these constants would not
have sufficed.

Extend the trace to the auxiliary line as follows. On J1 use the exact trace.
Outside I it equals H, so in the surrounding fixed background region use H;
farther out use the compatible smooth positive background extension of FGF047.
Extend q,g,chi smoothly there, using a positive convex cutoff for g; take
k=chi_X, p=w=v=0 off the core. This yields bounded compatible C1,1 initial
coordinates, with positive g and finite q. Choose the potential antiderivative
to match phi* on J1; since phi*=phi0 at both collars and phi*_X=g*, it
matches the same background potential on both neighboring sides. No cutoff
is applied to the exact core or joins.

Apply the explicit FGF047 construction to this trace, not a named general
continuation theorem: extend the smooth coefficients outside the trace's
compact chart, freeze successive characteristic speeds/sources, solve the
linear transport equations, and choose a time with C0 contraction factor
at most 1/8 and strict chart margin. Its derivative estimates give a common
finite Lipschitz bound; the elementary interpolation inequality
||u_X-v_X||<=2 sqrt(2H||u-v||) gives the C1 limit. Equations (4) and the
compatibility calculation of Section 2 then reconstruct ALL of (1), n and
the potentials on a positive restart interval. These are the pinned explicit
FGF047 steps; no smooth trace beyond T_N was assumed to apply them.

At restart the trace equals H on collars of radius r_e h_N/2. Restrict the
restart duration so its finite speeds cannot consume more than r_e h_N/4
of either collar, and so its physical cone contains J1's inner core. The
same characteristic uniqueness argument with H gives exact H on collars
of radius r_e h_N/4 during this restart. Patch its core to H on J exactly
as before. Choose the duration also less than Theta0-T_N, which is positive
by Section 4. The resulting combined solution is classical across T_N:
U,U_X agree there, U_t agrees by its PDE limit, and potential first and
second derivatives agree by compatibility. It is C1,1 uniformly on the
new compact slab, positive and admissible. Reapplying the original known
edge comparison even recovers the larger collars if needed.

For uniqueness after a restart, subtract two classical solutions with these
traces, stop characteristics at initial/lateral contacts, and use the same
zero-initial-difference integral inequality as in Section 4. If restarted
slightly before T_N this also identifies the overlap with the existing branch.
Thus the appended solution extends the SAME germ and contradicts maximality.
The assumed bounded first-gradient limsup is impossible; (3) follows.

## 8. Lifespan, norm interpretation, controls and limits

Restore physical time in (2):

    kappa (L/v0)N^-4 <= T_N,physical
                         <= B_dagger (L/v0)N^-4.

For each B_dagger>15/8 the sufficiently-large-N threshold may depend on it,
the fixed coefficients and the chosen background. No equality statement at
15/8, sharp constant, or attained upper horizon is claimed. The source proof
bounds the actual integrated field momentum by M(Gbar+G0)t^2/2; the initial
ratios P0/(MN)->8/15 and capacity/(M ell)->1 give its upper obstruction.
Pressure boundary stress is included there. FGF049's adverse-gradient budget
is still unproved; it was bypassed, not solved.

On the fixed-N compact state set, the smooth chart and inverse have bounded
Jacobians. Consequently (3) is equivalent, up to finite fixed-N constants,
to divergence of the limsup of the complete primitive spatial gradient norm
max(||v_X||,||q_X||,||p_X||,||g_X||,||w_X||,||k_X||,||chi_X||) on I.
Density derivatives can replace q_X because n has both fixed-N bounds.
Since chi_X=k already has a field-amplitude bound, it is not separately a
required divergent component. No particular fluid or field component is
identified. Fixed-N n bounds rule out vacuum or infinite density as the
sole endpoint mechanism; (7) rules out g=0/chart exit or field-amplitude
escape. The result is a bounded-amplitude, full-first-gradient obstruction.
It is a limsup statement only, not a claimed limit or a shock classification.

The full autonomous energy is retained. In the present fixed units set

    e(n)=c^2 n(log n-1),
    E=nv^2/2+e(n)+n phi
           +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U_s]/C,
    F=nv[v^2/2+c^2 log n+phi]-(pB+Jwk)/C.

Matter plus interaction has exchange +np; Q contributes -np-Tscale w/C;
scale contributes +Tscale w/C, so E_t+F_X=0. Both field fluxes remain.
At the fixed hydrostatic endpoints F=0; moving-cone integrals additionally
have boundary-motion terms and are not called conserved. No positive-energy
coercivity is used to prove (7) or (11).

With zero initial velocity, H is an exact solution of every equation,
including dynamic Q and scale. Its p,w,v and flux vanish, its momentum is
zero, and the positive-P0 upper contradiction does not apply. It need not
break down; the continuation argument correctly restarts it. This is the
exact negative control.

The adopted vacuum relation is a_ref=kappa_vac c_light sqrt(G rho_Lambda),
with kappa_vac adopted, not derived. Carry a_ref=9.3619e-11 and
1.1279e-10 m/s^2 separately, each with its compatible background and its
own constants. Constant vacuum and each separately frozen a0 E(z),
E(z)^2=.315(1+z)^3+.685, are distinct fixed-reference cases. An evolving
reference is EXCLUDED: autonomous source/boundary and protocol-work claims
have not been proved for it. The diagnostic chi degree of freedom does not
establish the physical pointwise scale-vacuum relation. Q, RAR, registered M
and filtered MONO are distinct; MOND scaling was never replaced by Newtonian
missing mass. No metric/photon, vacuum/two-DOF, criterion B, calibration,
cosmological, historical novelty or physical closure claim follows. The
high-N nonrelativistic family has no verified observational velocity window.

No missing implication was identified within this scoped author derivation.
Independent review must check the collar-patching equivalence and endpoint
restart, which are the new steps. Shock type, weak evolution, physical
completion and FGF049's different gate remain separate unproved questions.
