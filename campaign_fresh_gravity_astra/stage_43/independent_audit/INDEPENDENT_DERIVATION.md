# FGF056 independent reconstruction: the buffered fixed-domain endpoint

Reviewer `/root/fgf056_reviewer`. Written before exposure to any new FGF056
worker proof, result, preview, or stage43 coordinator argument. All thirteen
task ancestry pins were checked against actual bytes before use. The task
hash is in input_pins.json. This is an analytic argument, with zero mathematical
executable computations. Hash checks are administrative, not proof experiments.

## Claim card and dependencies

Fix the complete autonomous Q/scale/isothermal-fluid system and a smooth
positive compatible hydrostatic background on a fixed open physical patch.
Fix all positive coefficients, both physical units, V,cs,Vmax independently
of the packet width epsilon. In the sufficient cell

    Vmax > 7.5 cs,  7.5 cs < V < Vmax,
    7.5 < B < Bcap < V/cs,

there is, for sufficiently small epsilon, a unique intrinsic whole-packet
classical germ on a fixed buffered patch, with exact unsmoothed C1,1 packet
v=V(1-y^2)^2 for |y|<1, zero elsewhere, y=(x-x*)/epsilon. All initial
fields and density are the background. Its maximal time T_e satisfies

    kappa epsilon/V <= T_e <= B epsilon/V < Bcap epsilon/V.

On that germ, density remains between fixed positive finite bounds, the fields
remain in a positive compact chart, and |v|<Vmax. If D_e is the supremum of
all first spatial derivatives in the full diagonal chart on the fixed active
patch, then limsup_(t upward T_e) D_e(t)=infinity. No individual divergent
component, shock type, weak continuation, sharp constant or physical realization
is identified. The statement is local and extension-independent in the whole-
packet buffered sense defined below, not a theorem about arbitrary boundaries.

Provisional verdict: **proved as written** for this precise conditional claim,
with inherited local construction and parent cone estimates as pinned internal
inputs. Independent adversarial comparison is still required. The new links
are the known-H support comparison, enlarged common cone, fixed-domain union,
and actual endpoint trace/restart. The parent corrected matter scope is retained.

Internal dependency graph: FGF055 exact equations/chart and fresh local lower
construction -> lower branch on fixed physical cone -> known-H comparison and
outer patching -> intrinsic unique union. Separately, enlarged version of the
FGF055 amplitude cone + known-H support -> bounds on the entire union -> parent
capacity upper bound. Bounded full first gradients -> coupled difference-
quotient bounds -> actual C1,1 trace -> compatible restart -> contradiction.
FGF053 supplies a checked pattern, not its obsolete exact inner collars;
FGF048 supplies the explicit local characteristic construction. There is no
external theorem, numerical simulation, literature mechanism or empirical leaf.

## 1. Equations and fixed units

Use fixed L,u>0: X=(x-x*)/L, t=u t_phys/L, e=epsilon/L, V=Vphys/u,
c=cs/u, n=nphys/nref, phi=phiphys/u^2. Suppress the resulting coefficient
hats exactly as in the pinned FGF055 independent derivation. All constants
below can depend on the fixed physical coefficients and background, including
arbitrarily large but finite field speeds; none is uniform in a coefficient
limit. Set q=log n, g=phi_X>0, p=phi_t, k=chi_X, w=chi_t,
a=a_ref exp chi, C>0, and

    Q=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=integral_0^g Q(s,a) ds, T=-W_chi,
    U(chi)=S0(cosh(2chi)-1)/4.

The full equations are

    q_t+v q_X+v_X=0,   v_t+v v_X+c^2 q_X=-g,
    g_t=p_X,          tau p_t=Q_g g_X+Q_chi k-C exp q,
    k_t=w_X,          sigma w_t=J k_X+T-U',  chi_t=w.       (1)

The background H obeys v=p=w=0,

    (Q0)_X=C rho,  c^2(log rho)_X=-g0,
    J chi0_XX+T0-U'(chi0)=0.                               (2)

With b=sqrt(Q_g/tau)>0, d=sqrt(J/sigma), h_g=b, write

    r=v+cq, s=v-cq,
    R+=p+h, R-=p-h, Z+=w+d k, Z-=w-d k,
    z=(R+,R-,Z+,Z-,chi), Ufull=(r,s,z).

The exact diagonal equations are U_i,t+lambda_i(U)U_i,X=F_i(U), namely
D_(v+c)r=D_(v-c)s=-g,

    D_-b R+=Q_chi k/tau-Cn/tau+h_chi(w-bk),
    D_+b R-=Q_chi k/tau-Cn/tau-h_chi(w+bk),
    D_-d Z+=D_+d Z-=(T-U')/sigma,  chi_t=w.              (3)

No speed separation or division by differences of characteristic speeds is
required. These equations retain the actual density and all scale terms.
Compatibility follows from k_t=w_X and chi_t=w, which preserve chi_X=k.
The R difference gives g_t=p_X; its sum gives the p equation plus
b h_chi(chi_X-k), which vanishes. Integrating p in time from the original
potential gauge gives phi_X=g. These same calculations apply at the restart.

## 2. Fixed domains and the support comparison that is actually proved

Choose [-R,R] with an open neighborhood compactly inside the background patch.
The background has strict density/g/chart margins there. Choose a fixed

    S_H > max_(|X|<=R) { c, b(H(X)), d, 0 }.

Define Theta_cap=Bcap e/V and take e small enough that
r_cap=e+S_H Theta_cap<R/8. Put J=(-R,R), J0=[-R/2,R/2]. An admissible
segment through T<Theta_cap is a positive C1 solution in first-order variables
on [0,T]xJ, spatially C1,1 uniformly on compact time slabs, with the exact
initial data and potential gauge, and equal to H on |X|>=R/2. Potentials
are compatible and classical. This is an outer matching condition, distant
from the dynamical endpoints +/-2e; its independence is justified below.

For any such existing segment define D=Ufull-H in the diagonal chart. Along
KNOWN background characteristics, the exact subtraction is

    D_i,t+lambda_i(H)D_i,X
      =F_i(U)-F_i(H)+[lambda_i(H)-lambda_i(U)] U_i,X.    (4)

The coefficient difference times the UNKNOWN solution gradient is retained.
On each compact existing time prefix the state ranges are compact and positive
and U_X is bounded. Smoothness thus gives a finite Lipschitz bound for the
right side by C_prefix max_j|D_j|. This bound need not be uniform near an
endpoint and is used only to prove equality on that prefix. Smooth chart
coefficient extensions near the compact ranges, or finite covers and pairwise
Lipschitz constants, avoid assuming that every straight segment stays in the
chart.

On the right region e+S_H t<=X<=R/2, a backward H characteristic either
reaches t=0 with X>=e or first hits X=R/2. It cannot cross the inner line
backward because its speed is <S_H. In the first case D=0 initially; in the
second case D=0 on the prescribed outer overlap. The left region is identical
with signs reversed. The integral inequality

    sup_exterior |D|(t) <= C_prefix integral_0^t sup_exterior |D|(s) ds

implies D=0 there (iterate the inequality or use its elementary exponential
bound). Together with the outer overlap this proves, on each prefix,

    Ufull(t,X)=H(X) whenever |X|>=e+S_H t.              (5)

This is a support bound proved using known-H paths, not an a priori upper
speed bound on the unknown fields or fluid. In particular it is valid even
when actual interior speeds exceed S_H. The constants multiplying D in (4)
may be large; zero data still imply zero difference. Positivity and smoothness
are required on the existing prefix, not beyond it.

At any exterior point satisfying (5) at time t, the same fixed X lies exterior
at every earlier time; p=0 there. Hence phi(t,X)=phi0(X), including its
constant, and chi=chi0. This verifies potential matching, not merely equality
of g. The whole perturbation lies inside (-R/8,R/8) through Theta_cap; there
are wide unused stationary overlaps around +/-R/2.

To see that the admissible class is nonempty and not a imposed wall solution,
use the parent local construction on a wider fixed physical cone
[-R+Slo t,R-Slo t], with Slo bounding its actual short-time speeds and also
Slo>S_H. On its right exterior region bounded by e+S_H t and R-Slo t,
known-H backward characteristics cannot leave through either moving boundary;
all start in background initial data. Equation (4) proves H there without
any boundary prescription. Similarly on the left. For sufficiently small e,
the cone through the parent lower time contains J0 and fixed surrounding
buffers. Restrict to J0 and patch to H outside J0 on J; the two solutions
agree on open neighborhoods of the joins, including both potential constants.
This gives an admissible segment through kappa e/V. Auxiliary extensions
outside the physical patch have been discarded.

Two admissible segments agree on every common prefix: compare along one
solution's actual characteristics inside J0, stopping at the initial line
or first lateral contact, where both solutions equal H. The difference
source contains the other's bounded first gradients. The same zero-data
integral inequality proves equality. Gauges then match by p and the initial
potential. Thus overlaps form one intrinsic branch. Any alternate auxiliary
construction on a neighborhood containing these buffers patches in the same
way and belongs to this branch. No claim is made about a continuation that
abandons part of the packet or its physical dependence neighborhood.

## 3. Enlarging the parent cone to cover the entire perturbation

A literal use of the parent cone with final radius 3e does not suffice:
e+S_H Theta_cap may exceed 3e for fast fields. This is an essential changed
geometric step. Choose a central chart ball about z*=z0(0), and one fixed

    S > max(Vmax+c, sup_central_chart b, d, S_H, 1),
    K=3+(S+S_H)Bcap/V,
    C_e(t)=[-K e+S t,K e-S t].                         (6)

At Theta_cap the radius is 3e+S_H Theta_cap, so at every earlier time
C_e(t) contains the support interval [-e-S_H t,e+S_H t], the fixed mass
interval [-2e,2e], and a positive e buffer. For e small, K e<R/4, so the
entire cone is inside J0. This alteration only increases the fixed K in the
parent inequalities; every constant remains independent of e.

For completeness, bootstrap the central chart and |v|<Vmax on this cone.
Every backward actual characteristic is contained since S exceeds all its
bootstrap speeds. With q*=log rho(0), Q1=sup|q0_X| and Gbar the chart force
bound, centered acoustic invariants give

    -D0 e <= v +/- c(q-q*) <= V+D0 e,
    D0=c Q1 K+Gbar Bcap/V,
    -D0 e<=v<=V+D0 e,
    exp(q*-V/(2c)-1)<=n<=exp(q*+V/(2c)+1)              (7)

for D0 e<=c. Subtract the varying background z0(X) along actual field paths:

    D_lambda(z)(z_i-z0_i)
      =H_i(n,z)-H_i(rho,z0)
       +[lambda_i(z0)-lambda_i(z)]z0_i,X.             (8)

This uses only known background derivatives. With the actual n bound in (7),
finite source Lipschitz constants yield A_z(t)<=Dn t exp(Lz t)<=Cf e.
Then |z-z*|<zeta/2 and -D0 e<=v<=V+D0 e<Vmax for small e, strictly closing
the first-exit bootstrap on every existing prefix. Neither (7) nor (8) assumes
solution gradient control near the endpoint.

Outside C_e(t), (5) gives the VARYING H(X), because the perturbation support
is contained in C_e(t). Consequently the entire admissible domain has fixed
positive density bounds, positive g and a margins, bounded fields and speed
strictly below Vmax. These global bounds are the union of the cone bounds
and the compact background range on J. The assertion |z-z*|=O(e) holds only
on a shrinking central region. There is no global O(e) displacement from the
single central state on the fixed patch.

Choose c<a_ext<V/Bcap. The parent exterior acoustic wedges
C_e(t) intersect {+/-X>=e+a_ext t} are still nonempty, and include +/-2e.
The exact centered equations

    D_(v+c)[v+c(q-q0)]=-(g-g0)+(g0/c)v,
    D_(v-c)[v-c(q-q0)]=-(g-g0)-(g0/c)v

give |v|+|n-rho|=O(e^2) there by the same strict wedge-speed bootstrap.
They do not imply interior density/kinetic-stress smallness. Throughout the
shrinking core the field differences and mf,Sf-Sf0 are O(e); ONLY on those
wedges, including +/-2e, are nv^2=O(e^4) and c^2(n-rho)=O(e^2).

The parent lower construction used a fixed physical cone containing all
C_e(t) for t<=kappa e/V: choose e so K e plus its finite short-time speed
allowance fits inside the original background patch. Patching occurs much
farther out. Thus this is genuinely the same solution and cone used by the
upper bound, not a match of time scales from unrelated domains.

## 4. Upper horizon and maximal union

Let A=-2e,D=2e, ell=4e,j=nv,M=int_A^D n,P=int_A^D nv,
I=int_A^D(X-A)n, Delta=ell M-I. Exact integration gives

    M'=j(A)-j(D),
    P'=-[nv^2+c^2 n]_A^D-int_A^D ng,
    I'=P-ell j(D),
    Delta'=ell j(A)-P.

Using hydrostatics, define
Rm=[nv^2+c^2(n-rho)]_A^D+int_A^D(ng-rho g0). Then

    Delta(T)=Delta0-P0 T+int_0^T(T-t)Rm(t)dt
                            +ell int_0^T j(A,t)dt.    (9)

The parent actual bounds give Rm=O(e), the weighted error O(e^3), and
left influx error O(e^4). The separately audited conditional refinement can
improve the dynamical weighted error to O(e^4), but is unnecessary here and
does not remove the O(e^3) initial Taylor error. Direct initial integration is

    Delta0=8 rho* e^2+O(e^3),
    P0=(16/15)rho* V e+O(Ve^2).

At T=B e/V, Delta/e^2=rho*(8-16B/15)+O(e)<0 for small e, contradicting
positive n. No admissible segment extends through that closed time.

Let T_e be the supremum of all admissible segment lengths below Theta_cap.
Nonemptiness gives T_e>=kappa e/V. Uniqueness identifies their overlaps;
the union exists on [0,T_e)xJ and every compact prefix lies in an admissible
segment. If T_e>B e/V, that union includes a forbidden closed slab. Hence

    kappa e/V <= T_e <= B e/V < Theta_cap.             (10)

The bookkeeping cap is inactive. The active support is strictly interior
to the fixed patch and outer stationary overlaps are unused. A continuation
on the physical neighborhood that retains this whole packet can be patched
into the admissible class by (4)-(5); therefore an auxiliary extension or
artificial wall cannot alone terminate this germ. Shrinking or widening a
fixed patch while retaining these buffers yields the same overlapping germ
and the same inactive maximal time by uniqueness and local patching.

## 5. Bounded combined first gradients imply full higher seminorm bounds

Define D_e(t)=max_i ||U_i,X(t)||_(J0) in the complete diagonal chart. Outside
the support the derivatives equal H_X, so there is no uncontrolled exterior
part. Suppose limsup_(t upward T_e)D_e(t)<infinity. Combining the limsup
bound with regularity on earlier compact slabs gives D_e<=M1 for all t<T_e.
The global amplitude bounds of Section 3 give a fixed compact coefficient
range; all coefficient derivatives through order two are bounded there.
Here constants are finite for the fixed e and may depend on M1.

Take Scont from the Section 3 amplitude range, independently of e and of
the hypothetical M1, larger than every speed on that range and S_H. The cones [-3R/4+Scont t,3R/4-Scont t] contain J0 through
Theta_cap after a further small-e choice; alternatively begin their estimate
on a fixed earlier slab with equivalent buffers. Outside the shrinking support
the solution is H, and these cones avoid all lateral data in the seminorm proof.

Let Af=max(||r_X||,||s_X||), Bf=max_i||z_i,X||,
Hf=max(Lip r_X,Lip s_X), Hz=max_i Lip z_i,X. Differentiating (3) once gives

    D_(v+c)r_X=-v_X r_X-g_X,
    D_(v-c)s_X=-v_X s_X-g_X,
    D_i z_i,X=-(D_z lambda_i.z_X)z_i,X
                    +H_i,q q_X+D_z H_i.z_X.           (11)

In particular -C exp(q)q_X/tau and derivatives of all scale terms are present.
Compare these equations on two same-family characteristic paths. The spatial
flow separation obeys J'=lambda_X J. Dividing differences by that separation,
using smooth coefficient composition and q_X=(r_X-s_X)/(2c), yields finite
constants G,G2,L1,L2,P1,P2 with

    Hf(t)<=Hf(0)+int[3Af Hf+G Hz+G2 Bf^2],
    Hz(t)<=Hz(0)+int[(3L1 Bf+P1)Hz+(P1/c)Hf
                        +L2 Bf^3+P2(Bf+Af/c)^2].     (12)

The initial seminorm is finite and includes 8V/e^2 from the EXACT packet
joins. No classical second derivative at the join is asserted. Difference
quotients, equivalently weak derivatives of spatially Lipschitz gradients,
justify (12) on each compact admissible prefix. Same-family flows preserve
order, and all intervening spatial intervals are contained in the earlier
cone sections. Bounded Af,Bf reduce (12) to a coupled linear integral bound:

    Hf+Hz <= [Hf(0)+Hz(0)+C2 t] exp(C1 t).             (13)

Thus both higher seminorms are uniformly bounded through the approached
endpoint. This is not a hypothesis that the second derivatives were initially
continuous, and not an inference from the bound on only the fluid gradient.

## 6. Actual endpoint trace, potential constants and restart of this germ

On a fixed interval containing J0 with unused outer room, the PDE bounds U_t.
Its distributional spatial derivative gives

    (U_i,X)_t=-lambda_i U_i,XX
       -(D_U lambda_i.U_X)U_i,X+D_U F_i.U_X.           (14)

Every term is bounded a.e. by Section 5. Integrating (14) in time proves
||U_X(t)-U_X(s)||_infinity<=C|t-s|; continuity in X extends the a.e. bound
to every point. The same estimate for U follows directly from the PDE.
Hence U and U_X have genuine uniform endpoint limits U*,V*. Integrating
in X shows V*=(U*)_X, and (13) passes to the limit: U* is C1,1. The PDE
expression for U_t converges to F(U*)-lambda(U*)U*_X, supplying the time
C1 trace needed for classical gluing. There is no merely subsequential or
weak trace in this argument.

The global strict state margins survive this trace. Constraint chi_X=k
passes by C1 convergence. Define phi*=phi0+int_0^(T_e)p dt on the inner
interval; the integral and its first spatial derivative converge uniformly,
so phi*_X=g*. Both outer overlaps have p=0 for all earlier times, hence
phi*=phi0 there on BOTH sides. In particular the integral of g*-g0 over the
whole perturbation is zero; this is a compatibility consequence, not an
extra imposed constraint. chi*=chi0 on the overlaps as well. Smooth inversion
of the chart gives the primitive C1,1 traces with compatible gradients.

By (5) the trace equals H outside |X|<=r*=e+S_H T_e<R/8. Extend it using
H on the fixed surrounding patch. Farther out a compatible positive smooth
extension of the background suffices: extend q,g,chi, keep g>0, put k=chi_X,
and obtain phi by an antiderivative that matches its existing inner value.
The two checked potential constants guarantee simultaneous matching to the
same phi0 on both nearby exterior sides. Set v=p=w=0 outside the patched
perturbation. No cutoff touches the exact packet trace or its C1,1 joins.

Apply the pinned explicit local characteristic iteration to these actual
C1,1 data: extend coefficients outside the compact range, freeze speeds and
sources, integrate, choose a positive time with strict chart margin and C0
contraction, use the uniform gradient-Lipschitz bounds plus interpolation
to obtain a C1 solution. This construction accepts the trace just established;
it does not presume a smooth solution at T_e. Compatibility follows from
Section 1 and the preserved gauge.

Restrict the restart duration delta so its fixed physical dependence cone
contains J0 with an open overlap, delta<Theta_cap-T_e, and its bounded speeds
do not consume the fixed outer room. Known-H comparison from the restart
slice now proves equality to H for |X|>=r*+S_H(t-T_e). Since this is exactly
e+S_H t, the restarted patch satisfies the original support bound and is H
around +/-R/2. Patch it to H on J. The resulting solution agrees in U,U_X
at T_e; its U_t agrees by the PDE trace, and the potential derivatives agree
by compatibility. It is C1,1 on the appended compact slab and classical
across the join. Uniqueness identifies every overlap with the original branch.
Thus it is an admissible extension of the SAME germ beyond T_e, contradiction.

It follows that limsup_(t upward T_e)D_e(t)=infinity. Smooth chart inversion
on the compact range makes this equivalent to a full primitive gradient
limsup for v,q,p,g,w,k,chi (or n in place of q). No particular component is
selected. chi_X=k itself remains amplitude-bounded. No exact divergence
rate, actual limit, shock, or distributional continuation is established.

## 7. Conservation bookkeeping on inner, outer and moving domains

Direct differentiation of (1) gives the local identities

    (nv)_t+(nv^2+c^2 n)_X=-ng,
    mf_t+Sf_X=ng,
    mf=-(tau p g+sigma w k)/C,
    Sf=[gQ-W+tau p^2/2+sigma w^2/2+Jk^2/2-U]/C.       (15)

The field sign follows from (gQ-W)_X=g Q_X+T k; its T k term cancels the
scale exchange in mf_t. Therefore at the INNER endpoints A,D, which remain
dynamical,

    d_t int_A^D(nv+mf)=-[nv^2+c^2(n-rho)+Sf-Sf0]_A^D.

Neither mf nor boundary field stress is set to zero. As specified earlier,
only field quantities are O(e) throughout the shrinking core; the small
matter stresses are endpoint/wedge estimates. These identities agree with
the variable-mass capacity calculation (9).

For autonomous reference a_ref, define

    E=nv^2/2+c^2 n(log n-1)+n phi
        +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U]/C,
    F=nv[v^2/2+c^2 log n+phi]-(pQ+Jwk)/C.

Matter plus interaction exchanges +np, Q exchanges -np-Tw/C, and scale
exchanges +Tw/C, so E_t+F_X=0. On [A,D], d_t int E=F(A)-F(D), generally
nonzero with both field fluxes retained. On fixed J0 the outer endpoints
are truly H by (5), hence j=F=0 and c^2 rho+Sf0 is spatially constant:
whole-patch mass, total momentum and energy are conserved there. This outer
conservation is not transferred to the inner interval.

For ANY local law h_t+f_X=s and moving alpha,beta, direct differentiation is

    d_t int_alpha^beta h=int s+f(alpha)-f(beta)
                           +beta' h(beta)-alpha' h(alpha).

Thus shrinking cones retain their boundary-motion terms, including
-S(E(beta)+E(alpha)) for the symmetric cone. Even a moving endpoint lying
in H can contribute this geometric term. No energy coercivity is used.

## 8. Controls, failed shortcuts and scope

V=0 is handled separately without dividing by V: H is an exact smooth
solution, all currents vanish and no positive initial-momentum contradiction
exists. Arbitrary fixed finite field speeds are allowed but the small-e
threshold and constants depend on them. No infinite-speed limit is proved.
Both a_ref=9.3619e-11 and 1.1279e-10 m/s^2 are distinct parameter choices
with their own compatible backgrounds. The adopted vacuum normalization
is not derived. Constant vacuum and separately frozen a0 E(z),
E(z)^2=.315(1+z)^3+.685, are separate autonomous cases. Evolving-reference
work/reservoir terms are not supplied, so evolving-reference claims are excluded.
Q, RAR, registered M and operative filteredMONO remain distinct. The actual
MOND source Q_X=C n+tau phi_tt is retained; no Newtonian missing-mass
replacement or observational discrepancy estimate occurs in this proof.

Failed shortcuts rejected explicitly: (i) known-H speed is not an assumed
unknown speed cap; the unknown-gradient term in (4) cannot be deleted;
(ii) the literal radius-3e parent cone cannot cover arbitrary fast-field
support; (iii) +/-2e cannot be patched to H; (iv) bounded amplitudes alone
do not supply C1 endpoint traces; (v) merely gluing g does not check both
potential constants; (vi) central O(e) field displacement cannot be asserted
on a fixed patch; (vii) initial core kinetic stress is O(1), not O(e^4).
No counterexample was found to the scoped repaired construction, and no
numerical experiment was performed.

Obligation matrix: domain/support comparison, lower/upper common branch,
full-domain source bounds, inactive cap, exact joins, higher seminorms,
actual endpoint traces, both potential constants, compatible extension,
restart/uniqueness, complete fluxes and V=0 are passed by the arguments above.
Physical realization, metric/photon coupling, criterion B, two gravitational
DOF, cosmology, calibrated cluster inference and historical novelty are OUT
OF SCOPE. This settles only the named finite-V diagnostic continuation gate
if independently accepted. Stop this endpoint chain here; the outstanding
physical-sector and calibrated-data gates remain separate and unchanged.
