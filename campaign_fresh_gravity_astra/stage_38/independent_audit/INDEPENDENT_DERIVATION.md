# FGF051 independent pre-exposure derivation

Actor: /root/fgf051_reviewer. No new FGF051 author, coordinator, or other
reviewer proof, preview, or proposed verdict has been read. This independent
reconstruction uses the task, framework/result contract, ten hash-verified
ancestry pins, and the additionally hash-verified original FGF047 construction.
It is proof-only: zero mathematical executable computations, numerical
experiments, external services, or literature mechanisms. Hashing is metadata.

Primary verdict on the proposed scoped local theorem: **proved as written for
the bounded edge-domain claim formulated below**. This is a pre-exposure
independent derivation, not yet a verdict on an unseen author proof. The
full-cone feedback and actual compression endpoint remain incomplete.

## 1. Claim card and fixed units

Fix all positive physical parameters and a smooth compatible hydrostatic
background on a fixed open interval, with n=rho>0 and g0=phi0_x>0. Fix
x*, L, v0 and c_s>0. For all sufficiently large integers N, keep the exact
C1,1 velocity V f((x-x*)/ell), V=v0 N, ell=L N^-3, with f=(1-y^2)^2
inside its support and zero outside. Density and both fields equal the
background initially and both field time derivatives vanish. There are fixed
constants D>A>0, S>0, k>0, independent of N, such that each edge has an
actual compatible classical coupled solution on

  0<=theta<=k/P,  |X-X_e|<=D/P-S theta,
  X=(x-x*)/L, theta=v0 t/L, P=N^(7/2), X_e=+/-N^-3,

and this domain contains the fixed inner interval |X-X_e|<=A/P throughout.
The solution is C1 in its first-order variables, with uniformly bounded
spatial derivative Lipschitz seminorm at each fixed N; phi,chi are C2.
The initial v=b0 and v=b0+c roots on both packet halves are in these inner
intervals. Quantitative estimates below hold on both domains and at every
fixed B*>0 through theta_N=B* N^-4 for sufficiently large N.

The system uses the physical Q law B=(sqrt(a^2+4g^2)-a)/2,
a=a_ref exp chi, W=integral_0^g B(s,a)ds, T=-W_chi,
U_s=S0(cosh(2chi)-1)/4. It is

  n_t+(nv)_x=0, v_t+v v_x+c_s^2(log(n/nref))_x=-g,
  tau p_t=B_x-Cn, g_t=p_x,
  sigma w_t=J k_x+T-U_s', k_t=w_x, chi_t=w,

with p=phi_t, k=chi_x, w=chi_t, C=4 pi G. The dynamic source
B_x=Cn+tau phi_tt is retained. No static inversion replaces it.

Use the fixed units of FGF048: velocity v0, density nref, potential v0^2,
g and a in v0^2/L, p in v0^3/L, w in v0/L, k in 1/L. Below all equations
and constants use these dimensionless units, with q=log(n/nref), c=c_s/v0.
The dimensionless fixed coefficients are tau v0^2, sigma/v0^2, J/v0^4,
C nref L^2/v0^2, a_ref L/v0^2 and S0 L^2/v0^4. Symbols are reused only
after this fixed unit choice; no physical coefficient is retuned with N.

## 2. Exact profile, roots, and local auxiliary extension

For either edge define the inward distance d>=0 and zeta=P d (dimensionless
space). For 0<=d<=ell=N^-3, exactly

  v_in=zeta^2(2-zeta/sqrt(N))^2,
  |v_in,X|=4P zeta (1-zeta/sqrt(N))(2-zeta/sqrt(N)).

On |X-X_e|<=D/P and sufficiently large N this gives |v|<=4D^2,
|v_X|<=8D P. The outside half has v=0. The global exact polynomial bound
Lip(v_X)<=8N^7=8P^2 also holds across the C1 joins. There is no classical
v_XX value at a join, and none is assigned. These are estimates on the
original packet, not on a rounded join.

Let b0=sqrt(B_g(g0,chi0)/tau)>0. On the fixed background neighborhood choose
bmax>=sup b0 and choose A>0 with A^2>bmax+c+1. For N large enough that
A/sqrt(N)<=1, v at inward distance A/P is at least A^2; at the edge it
is zero. Hence each half has a v=b0 root and a v=b0+c root at distance
strictly between 0 and A/P. Moreover v is increasing from each edge to the
center, so outside these edge intervals but inside the packet v>=A^2.
Thus every initial root of these two equations in the packet is captured.
This proves inclusion, not just asymptotic root locations.

Other nonnegative acoustic thresholds b0-c and c-b0 are also <=bmax+c,
so their positive-velocity packet roots are included. One cannot claim that
all initial acoustic coincidences everywhere are captured: at v=0 outside
the support, b0=c would produce additional coincidences. No assumption
excluding that equality was supplied. No future resonance localization is
proved here. The required v=b0 and v=b0+c inclusions do not need it.

Choose D>A+2, then a fixed smooth scalar cutoff eta=1 on [-D,D] and
eta=0 outside [-2D,2D]. For each edge take the auxiliary initial velocity
v_e,N(X)=eta(P(X-X_e)) v_in,N(X), with the EXACT original packet in the
product. For N sufficiently large the cutoff sees only that edge, and

  ||v_e,N||<=16D^2=:Vloc,
  ||(v_e,N)_X||<=C_D P,
  Lip((v_e,N)_X)<=C_D P^2.

Product differentiation gives these bounds: each cutoff derivative supplies
P, while v,v_X,v_XX on the cutoff support are O(1),O(P),O(P^2). The edge
join remains exactly C1,1. This modification is an auxiliary extension of
local initial data only; it is not asserted to be the whole physical packet.
Extend q0,g0,chi0 once smoothly on the line as in FGF047, g0 bounded strictly
positive, k0=chi0_X and p0=w0=0. Extension norms are fixed independently of N.
The initial data agree with the actual whole packet on |X-X_e|<=D/P.
The proof of physical irrelevance of the auxiliary cutoff is in Section 6.

## 3. Actual diagonal equations and block estimates

Let d_s=sqrt(J/sigma), b=sqrt(B_g/tau), and h_g=b with
h(g,chi)=integral_gstar^g b(s,chi)ds. Set

  r=v+cq, s=v-cq, R+=p+h, R-=p-h,
  Z+=w+d_s k, Z-=w-d_s k, z=(R+,R-,Z+,Z-,chi).

On a fixed compact field chart g>0 all inverse maps and two derivatives are
bounded, with b,d_s,c bounded away from zero. All scale terms are present:

  D_(v+c) r=-g, D_(v-c) s=-g,
  D_(-b) R+=A+h_chi(w-bk),
  D_(+b) R-=A-h_chi(w+bk), A=B_chi k/tau-C exp(q)/tau,
  D_(-d_s) Z+=D_s, D_(+d_s) Z-=D_s,
  chi_t=w, D_s=(T-U_s')/sigma.

Consequently field speeds depend only on z and field sources H_i only on
(q,z), never on v or derivatives. Choose fixed smooth coefficient extensions
for the field chart and q box, agreeing on a compact neighborhood of all
initial field ranges. They provide finite bounds Lambda,F,G,G2,L1,L2,K1,K2
for |lambda|,|H|,|Dg|,|D2g|,|Dlambda|,|D2lambda|,|DH|,|D2H|.
The fluid speeds remain v+/-c. The pinned FGF047 fixed-N construction applies
to these compatible C1,1 data; only starts/restarts are taken from it.

Put A_f=max(||r_X||,||s_X||), B_f=max_i||z_i,X||. Differentiating along
actual characteristics gives

  A_f <= A_f(0)+int(A_f^2+G B_f),
  B_f <= B_f(0)+int[L1 B_f^2+K1(B_f+A_f/c)].                 (3.1)

These use |v_X|<=A_f, |q_X|<=A_f/c. Also

  D_v q=-v_X,
  ||z(t)-z0||<=int(Lambda B_f+F),
  |v|<=Vloc+c||q0||+gbar t.                                (3.2)

The last bound follows separately from both fluid invariants, whose initial
amplitudes are fixed on the auxiliary line. There is no pressure omission or
N-dependent sound speed. Let A_f(0)<=a0 P, B_f(0)<=B0. Choose fixed a>a0+1,
beta>B0+1 and then k>0 sufficiently small that, on theta<=k/P,

  k(a^2+G beta)<(a-a0)/2,
  k[L1 beta^2+K1(beta+a/c)]<(beta-B0)/2,
  ak<1/2,
  k(Lambda beta+F)<delta/2,
  k<=1.

Here delta is a fixed chart margin, and reducing k is harmless. Bootstrap
A_f<aP, B_f<beta, q within one of its initial range, z within delta of z0.
The inequalities strictly improve all four bounds. In particular

  A_f<=aP, B_f<=beta,
  qmin-1/2<=q<=qmax+1/2, |z-z0|<=delta/2,
  |v|<=Vloc+c||q0||+gbar.

Therefore a single fixed S larger than this last expression plus c and
all field speed bounds controls all actual local characteristics. This
speed bound is derived from the real momentum equations on the constructed
solution; it is not an imposed boundary condition suppressing the core.

## 4. Higher norm and full endpoint restart

Set Hf=max(Lip(r_X),Lip(s_X)), Hz=max_i Lip(z_i,X). Pair-characteristic
first-derivative difference quotients, or a.e. differentiation, yield

  Hf <= Hf0+int[3A_f Hf+G Hz+G2 B_f^2],
  Hz <= Hz0+int[(3L1 B_f+K1)Hz+(K1/c)Hf
                     +L2 B_f^3+K2(B_f+A_f/c)^2].           (4.1)

The factor 3 accounts for the speed derivative, its derivative, and spatial
separation of characteristics. Linear dependence on the higher norm is
critical; a generic cubic seven-variable bound loses this structure.
Initial Hf+Hz<=C0 P^2. The strict bootstrap gives

  Hf+Hz <= C0 P^2+int[E P(Hf+Hz)+D P^2],
  Hf+Hz <=(C0 P^2+D P^2 theta) exp(E P theta)<=C_H P^2.      (4.2)

Every constant is independent of N. This retains the initial N^7 seminorm
without using it to shorten the lifespan to N^-7.

For each fixed N the PDE bounds U_theta and, a.e.,

  (U_X)_theta=-lambda(U)U_XX-(Dlambda.U_X)U_X+DF.U_X.

The right side is uniformly finite because the actual speed, first gradient,
and Lipschitz first gradient are bounded. Distributional integration and the
continuous spatial representatives make U and U_X uniformly Cauchy as an
endpoint theta*<=k/P is approached. The trace is C1,1, retains the strict
chart and positive-state margins, and has finite amplitude. FGF047 restarts
it; its local uniqueness glues the branches. A restart length depending on
fixed N suffices. This rules out failure to reach k/P without requiring a
uniform restart length. Thus the bootstrap belongs to an actual solution on
the stated interval, not merely to a putative one.

Compatibility is also present at endpoint traces: the scale equations give
k_t=w_X and chi_t=w, hence chi_X=k. Subtracting R equations yields
b(g_t-p_X)+h_chi chi_t=h_chi w, so g_t=p_X; adding yields
p_t=b^2 g_X+A+b h_chi(chi_X-k), whose last term is now zero. Reconstructing
phi=phi0+int p gives phi_X=g,phi_t=p and C2 potentials. These identities
survive uniform C1 limits and the exact compatible restart.

## 5. Feedback on the actual interval and comparison time

The preceding proof already yields n between fixed positive constants,
|n_X|<=C P, bounded field gradients, positive g and a, and g_t=p_X.
A sharper evolving estimate follows from the real continuity equation:

  D_v q_X=-v_X q_X-v_XX,
  ||q_X(theta)||<=[||q0_X||+C_H P^2 theta] exp(aP theta).    (5.1)

Since n is bounded, the same bound controls n_X. Repeating only the field
higher-norm inequality with (5.1) in the quadratic source term gives, for
0<=theta<=k/P,

  Hz(theta)<=C(1+P^2 theta).                               (5.2)

Indeed (1+P^2 theta)^2<=C P^2 on that interval, Hf<=C_H P^2,
and the scalar coefficient multiplying Hz is fixed. No field mode is dropped.
From g-g0=int p_X and Lip(p_X)<=Hz one obtains

  |g-g0|<=beta theta,
  |g_X-g0_X|<=C(theta+P^2 theta^2).                        (5.3)

For the prescribed theta_N=B* N^-4, we have theta_N<=k/P when
sqrt(N)>=B*/k. Hence on the protected inner domains throughout comparison,

  |n_X|<=C(1+N^3), |z_X|<=beta,
  Hf<=C N^7, Hz<=C(1+N^3),
  |g-g0|<=C N^-4, |g_X-g0_X|<=C N^-1.                     (5.4)

Write M0=max over the initial edge neighborhoods of (-g0_X)_+, bounded by
a fixed background constant. Nested-domain vertical segments stay inside the
larger domain, so all integrations used in (5.3) are legitimate. The actual
adverse feedback, taking the supremum only on the union of the inner patches,
satisfies

  int_0^theta_N sup(-g_X)_+
    <=M0 theta_N+C(theta_N^2+P^2 theta_N^3)
    <=M0 B* N^-4+C_B N^-5.                               (5.5)

This is the strongest bound proved here without extra background sign:
background adverse contribution O(N^-4), generated excess O(N^-5).
If g0_X>=0 on these neighborhoods, only the O(N^-5) term is charged.
The force impulse is <=gbar B* N^-4. In physical units multiply (5.5)
by v0/L and the impulse by v0; spatial field-gradient deviations in (5.4)
get factor v0^2/L^2. These are far smaller than an O(N^4) adverse budget
and O(N) impulse allowance, but only for the local suprema actually bounded.
No whole-cone replacement is permitted.

One can investigate hydrostatic subtraction to improve the lower-order
O(theta) term in (5.3), but it is not needed for (5.5) and is not claimed
here. Formal initial-time jets do not replace these actual-time estimates.

## 6. Buffer, matching, and exterior independence

Reduce k further so S k<(D-A)/2. Then the affine cones

  K_e(theta)=[X_e-D/P+S theta, X_e+D/P-S theta]

contain a neighborhood of the fixed inner intervals of radius A/P through
k/P. Every backward characteristic of the constructed solution stays inside
K_e at earlier times because its speed has magnitude <S; vertical segments
also stay inside. Distinct edge cones are disjoint for large N since
D/P << N^-3. On the shorter comparison time the lost width S B* N^-4
is smaller by N^-1/2 than the original buffer. Paths launched at the
initial resonance points move at most S theta and remain protected by the
additional buffer through a further harmless reduction of k. This is
protection of those starting points and their locally defined paths; it is
not a statement about all newly formed speed intersections.

Matching to a whole-packet classical branch deserves a sharper argument
than using its crude O(N) speed. Let U be this bounded-speed local solution
and V any C1 whole-packet branch defined on the entire cone under comparison,
in the same positive field chart. They have the same initial trace on the
base. Subtract along U's characteristics:

  D_lambda(U)(U_i-V_i)=F_i(U)-F_i(V)
                          +(lambda_i(V)-lambda_i(U)) V_i,X.

The compact competitor range and its finite first derivatives give a finite
C_N on each closed common time interval. All integration curves stay inside
the cone by U's speed alone. Thus

  Ddiff(theta)<=C_N int_0^theta Ddiff(s) ds,

and iteration or scalar integration gives Ddiff=0. This argument needs NO
uniform bound on the competitor's speeds and does not use its O(N) bound
as the cone slope. It does need the competitor to be defined and C1 on the
whole common cone. It proves equality only through its existing interval;
the local construction does not extend its fast core or prove whole-packet
existence to comparison time. Before any whole-packet breakdown, exterior
high-speed data cannot alter this smooth local restriction: the asymmetric
uniqueness estimate explicitly handles that concern instead of deleting
incoming data. A different auxiliary extension has the same restriction
whenever its solution is defined on this cone. Beyond loss of classical
regularity or for a competitor not defined on the needed domain there is
no asserted comparison.

## 7. Energy, controls, branches, failures, and remaining gap

In physical units the full fixed-reference energy and flux are

  e=c_s^2 n(log(n/nref)-1),
  E=nv^2/2+e+n phi+[tau p^2/2+W+sigma w^2/2+Jk^2/2+U_s]/C,
  F=nv[v^2/2+c_s^2 log(n/nref)+phi]-(pB+Jwk)/C.

Matter plus interaction gives +np, Q gives -np-Tw/C, and scale gives +Tw/C.
Therefore E_t+F_x=0. For moving endpoints alpha,beta,

  d/dt int_alpha^beta E=F(alpha)-F(beta)+beta'E(beta)-alpha'E(alpha).

The edge cones have both endpoint energy terms with inward physical speed
v0 S; neither can be discarded. No positive conserved shrinking-cone norm
is inferred. The unchanged zero-velocity hydrostatic tuple solves every
fluid and field equation, with p=w=0 and full flux zero. Uniqueness makes the
constructed restriction equal to this control. Hydrostatics outside an
auxiliary cutoff are not required for this local check.

Repeat separately for a_ref=9.3619e-11 and 1.1279e-10 m/s^2 with their own
compatible backgrounds. Constant vacuum and every separately frozen
 a_ref=a0 E(z), E(z)^2=.315(1+z)^3+.685,
are distinct fixed-reference choices. There is no uniformity claimed over
unbounded z. Evolving references have explicit work -T d(log a_ref)/dt /C
and extra characteristic-chart time terms; they are excluded from this
fixed-reference result. The adopted vacuum relation and its p=-rho c_light^2
qualification remain assumptions, not derived physical completion.

Failed routes identified and excluded: (i) using the global O(N) speed to
shrink the narrow patch would lose its buffer on the comparison interval;
the bounded auxiliary evolution plus asymmetric uniqueness repairs that
argument without changing the data inside the cone; (ii) using H~N^7 as a
first-gradient lifespan control gives a spurious shorter time; (iii) calling
all initial acoustic resonances edge-localized ignores possible b0=c in
the exterior; (iv) local estimates cannot bound the full-cone supremum;
(v) replacing the old kappa by B* without the new spatial construction is
invalid. These are estimate/scope failures, not counterexamples to compression.
The corrected FGF050 ancillary identity has not been reused uncorrected.

Dependency graph: exact packet scaling -> bounded local auxiliary data ->
pinned fixed-N construction + real block inequalities -> strict state bounds
and linear C1,1 continuation -> bounded local speed -> buffered cones ->
asymmetric local uniqueness -> matching on common existing classical domains.
Continuity/field higher norms then imply the actual feedback estimate (5.5).
Every load-bearing external-looking leaf is the verified internal FGF047
construction, not an unverified literature theorem.

Obligations passed: profile and initial required roots; genuine fixed buffer;
all field/scale/pressure terms; compact chart; N^-7/2 local existence; full
higher-norm endpoint and compatible restart; positive density/scale/g bounds;
local speed and conditional-on-existing-branch comparison; adverse bound;
energy and exact hydrostatic control; separate fixed normalizations/histories.
Not addressed: fast-core existence through B* N^-4, every future resonance,
interface coverage beyond these cones, full-cone gradient supremum and actual
compression endpoint. Out of scope: Q-to-RAR/M/MONO transfer, physical
vacuum/metric/photon/two-DOF completion, criterion B, observations, cosmology,
novelty or closure. Cheapest next check is the raw new author proof against
these obligations after this file and its metadata are frozen.
