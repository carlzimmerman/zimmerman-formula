# FGF049: conditional compression with an integrated adverse-feedback budget

Author: /root/fgf049_author, current inherited Codex agent. Proof-only candidate;
independent review pending. The task and all nine listed ancestry hashes matched
BEFORE ancestry text was read. No new stage36 root or reviewer proof was read.
The full unconditional coupled upper-lifespan question remains open. This file
proves a sufficient conditional upper bound and identifies its unsupplied field
estimate. It neither extends FGF048's small kappa nor imports FGF046's endpoint.

## 1. Exact target, equations, and data

Fix positive physical C=4pi G_Newton, tau, sigma, J, S0, c=cs, nref and a_ref.
The sound speed c is NOT the light speed in the adopted vacuum relation.
On the same smooth regular hydrostatic patch U, put g=phi_x, p=phi_t,
k=chi_x, w=chi_t, a=a_ref exp(chi), and retain exactly

    B(g,a)=(sqrt(a^2+4g^2)-a)/2, g>0,
    W(g,a)=integral_0^g B(s,a) ds, T=-W_chi,
    U_s(chi)=S0[cosh(2chi)-1]/4,
    n_t+(nv)_x=0,
    v_t+v v_x+c^2(log(n/nref))_x=-g,
    tau phi_tt=B_x-Cn,
    sigma chi_tt=J chi_xx+T-U_s'(chi).                 (1.1)

In particular B_x=Cn+tau p_t is dynamic. Initial data are n=rho, phi=phi0,
chi=chi0, p=w=0, with hydrostatic B(g0,a0)_x=C rho,
c^2(log rho)_x=-g0 and J chi0_xx+T(g0,a0)-U_s'(chi0)=0.
Here a0(x)=a_ref exp(chi0(x)); this notation does not equate its varying
profile to a physical constant vacuum acceleration.
Choose the inherited K0=[x*-R,x*+R] compactly inside U and fixed L,v0>0.
For integers N with ell=L/N^3<R/2, use EXACTLY

    V=v0 N, omega=V/ell=v0 N^4/L,
    v(0,x)=V f((x-x*)/ell),
    f(y)=(1-y^2)^2 for |y|<1, and 0 otherwise.         (1.2)

The joins are C1,1, not C2. No smoothing, coefficient retuning, pressureless
limit, static field inversion or moving source substitution is made.
Let d_f=8/(3sqrt(3)); f'(1/sqrt(3))=-d_f. On K0 define

    G0=max|g0|, Q0=max|log(rho/nref)|,
    h0=max rho^(-1/2), hmin=min rho^(-1/2),
    A=2 d_f h0, b_*=d_f hmin,
    B_*=(h0/A)[exp(8A/b_*)-1], T_N=B_*/omega,
    H_*=h0+A B_*, eta=min(A/2,b_*/2)/H_*.             (1.3)

A,b_*,H_* have inverse-square-root-density units; B_*,eta are dimensionless.
All constants are independent of N; B_* is deliberately conservative.

## 2. Claim card: the exact conditional theorem

Fix any dimensionless Gamma>0, independent of N, and define

    S_N=(1+Gamma)V+c Q0+c+tau^(-1/2)+sqrt(J/sigma)+v0,
    K_t=[x*-R+S_N t,x*+R-S_N t].                      (2.1)

Take N sufficiently large that

    omega>=G0/(c d_f), ell+2 S_N T_N<R.               (2.2)

These are genuine large-N thresholds since S_N T_N=O(N^-3).
Suppose a positive classical solution of ALL (1.1), with exact data (1.2),
is defined on a neighborhood of the closed cone 0<=t<=T_N, x in K_t.
Here classical means n,v,p,g,w,k,chi are spacetime C1, the potential fields
are C2 and the compatible positive g chart is used. For the contradiction,
spatial C1,1 beyond the initial slice is not additionally required.
Write

    G_N(t)=sup_{K_t}|g(t,x)|,
    K_N(t)=sup_{K_t} max(0,-g_x(t,x)).

The following TWO conditional feedback hypotheses are sufficient:

    (F)  integral_0^T_N G_N(t)dt <= Gamma V,
    (D)  integral_0^T_N K_N(t)dt <= eta omega.        (2.3)

Then such a solution cannot exist through T_N. Thus, IF (F),(D) are proved
for every candidate continuation of the actual constructed branch up to this
time, they give an O(N^-4) upper bound on its positive classical lifespan
covering this physical cone. The implication is proved here; (F),(D) on the
full interval are NOT proved for the actual coupled family.

This is stronger than requiring |g_x|=O(1) or FGF048's O(N^-1) derivative
feedback up to T_N: (D) permits negative g_x as large as a sufficiently small
fixed multiple of omega^2=O(N^8), or sharper time concentration, provided its
integral satisfies the stated budget. Positive g_x is favorable and is not
charged. Smallness refers to eta, not simply to an O(omega) assertion.
Neither (F) nor (D) asserts positive coefficient margins or endpoint type.

## 3. Pressure-retaining identities and domain containment

Put q=log(n/nref), r=v+cq, s=v-cq, alpha=r_x, beta=s_x,
h=n^(-1/2), y=h alpha, zeta=h beta. With D_+/-=partial_t+(v+/-c)partial_x
and D_v=partial_t+v partial_x, direct use of (1.1) gives

    D_+ r=-g, D_- s=-g,
    D_+ alpha=-(alpha+beta)alpha/2-g_x,
    D_- beta=-(alpha+beta)beta/2-g_x,
    D_+ q=-beta, D_- q=-alpha,
    D_+ y=-y^2/(2h)-g_x h,
    D_- zeta=-zeta^2/(2h)-g_x h,
    D_v h=(y+zeta)/4.                                (3.1)

There is no g_t term when differentiating the source spatially. For C1 data
and solutions, obtain the derivative identities by differentiating the
integrated r,s characteristic formula in its initial label, using
J_t=v_x J and J>0. This requires g_x continuous, not second fluid derivatives,
and is valid at the exact polynomial joins. Units are h/time^2 in the last
two gradient equations. The mixed alpha beta term cancels by the density
weight; pressure remains in both families and their speeds.

Initially |r|,|s|<=V+c Q0. Bootstrap |v|+c<S_N on the cone. Every backward
fluid characteristic then stays in earlier K_u. By (F), integration yields

    |r|,|s| <= V+c Q0+integral_0^t G_N(u)du
              <=(1+Gamma)V+c Q0,
    |v|+c <=(1+Gamma)V+c Q0+c<S_N.                   (3.2)

The strict margin excludes first contact on any compact classical slab.
Field speeds are 0,+/-sqrt(B_g/tau),+/-sqrt(J/sigma), and
0<B_g=2g/sqrt(a^2+4g^2)<1. They too have magnitude <S_N, irrespective of
whether a UNIFORM lower margin for B_g is known. Material and vertical
reconstruction paths also stay in the cone. No boundary values or exterior
static-field premise enter these estimates.

For each fixed N the same invariants imply

    |q| <= [(1+Gamma)V+c Q0]/c,
    nref exp(-[(1+Gamma)V+c Q0]/c) <= n
       <= nref exp([(1+Gamma)V+c Q0]/c).             (3.3)

These bounds are exponential in N and do not close field feedback.
The plus characteristic from a_N=x*+ell/sqrt(3) has displacement <=S_N t;
by (2.2), ell+S_N t<R-S_N t. It therefore stays strictly in K_t through
the entire comparison time. Its offset and displacement are O(N^-3),
inside the fixed original physical patch. This is conditional physical-domain
containment under (F), not an extension of the FGF048 time interval.

## 4. The integrated one-sided budget closes the conditional compression

Define M(t)=max(0,sup_{K_t}y,sup_{K_t}zeta), H(t)=sup_{K_t}h.
Hydrostatics gives alpha0=omega f'-g0/c and beta0=omega f'+g0/c.
By (2.2), M(0)<=A omega. Using backward characteristics in (3.1) and
dropping only the nonpositive quadratic terms gives

    M(t)<=A omega+integral_0^t K_N(u)H(u)du,
    H(t)<=h0+(1/2)integral_0^t M(u)du.                (4.1)

Until a first contact M=2A omega, the second line yields
H<=h0+A omega t<=H_*. Then (D) implies

    M(t)<=A omega+H_* eta omega<=1.5 A omega.

This strict improvement excludes that contact. Thus on the whole hypothetical
slab

    H(t)<=h0+A omega t<=H_*, n>=H_*^(-2).             (4.2)

Let w_c=-y along the distinguished plus characteristic. Its initial value is
rho(a_N)^(-1/2)[d_f omega+g0(a_N)/c]>=b_* omega; g0>0 is used here.
Equation (3.1) gives

    w_c' >= w_c^2/(2h)-K_N(t)h.                      (4.3)

An integrated budget is NOT a pointwise bound on the last term; it would be
incorrect simply to replace K_N(t) by its mean. Instead define the future
budget correction, for this hypothetical full slab,

    F_tail(t)=H_* integral_t^T_N K_N(u)du,
    u(t)=w_c(t)-F_tail(t).                            (4.4)

The correction is nonnegative. By (D), u(0)>=b_* omega/2>0. Moreover

    u' >= w_c^2/(2h)+K_N(t)(H_*-h)
        >= w_c^2/(2h).

Starting at u>0 this shows u stays positive and nondecreasing; w_c>=u>0.
Consequently

    u' >= u^2/[2(h0+A omega t)],
    1/u(t)<=2/(b_* omega)
           -[1/(2A omega)]log(1+A omega t/h0).       (4.5)

At T_N, the right side is 2/(b_* omega)-4/(b_* omega)<0, impossible for
finite positive u. Already at

    t_hat=(h0/(A omega))[exp(4A/b_*)-1]<T_N           (4.6)

the upper bound is nonpositive. The future correction is used only in a
contradiction assuming existence through T_N; no field values beyond an
actual earlier endpoint are assumed. This proves the claim in Section 2.

A useful contrapositive: any positive classical continuation through T_N
must violate at least one of (F) or (D). Failure of either inequality is not
itself a singularity, and does not give a stable-solution counterexample.

## 5. Actual feedback: where the presently supplied estimates stop

For explicit field estimates use the fixed nondimensionalization of pinned
FGF048 Section 2 (units L,v0,nref). This paragraph's norms and constants are
in those fixed units; restoring units in the final budgets gives (2.3).
Define b=sqrt(B_g/tau), d=sqrt(J/sigma),

    Hcal(g,chi)=integral_{g_*}^g b(s,chi)ds,
    R_+=p+Hcal, R_-=p-Hcal, Z_+=w+d k, Z_-=w-d k,
    Z=(R_+,R_-,Z_+,Z_-,chi).

On g>0 this is the same smooth field chart as FGF048. Its EXACT equations are

    (partial_t-b partial_x)R_+
      =B_chi k/tau-Cn/tau+Hcal_chi(w-b k),
    (partial_t+b partial_x)R_-
      =B_chi k/tau-Cn/tau-Hcal_chi(w+b k),
    (partial_t-d partial_x)Z_+=(T-U_s')/sigma,
    (partial_t+d partial_x)Z_-=(T-U_s')/sigma,
    chi_t=w.                                        (5.1)

All chi dependence, scale force and gradient energy remain. Write this as
D_i Z_i=H_i^0(Z)-(C/tau)n e_i, with e=(1,1,0,0,0). Differentiating along
characteristics, with xi_i=Z_i,x, yields exactly

    D_i xi_i=-(D_Z lambda_i.Z_x)xi_i
             +D_Z H_i^0.Z_x-(C/tau)e_i n_x.          (5.2)

This is the density source derivative that a frozen-source proof misses.
On any fixed compact chart neighborhood, coefficient bounds L1,P0,G give

    B_f(t)<=B_f(0)+integral_0^t
       [L1 B_f(u)^2+P0 B_f(u)+(C/tau)||n_x(u)||]du,
    ||g_x||<=G B_f,
    ||Z(t)-Z(0)||<=integral_0^t
       [Lambda B_f+F0+(C/tau)||n||]du,               (5.3)

where B_f=max_i||Z_i,x||. Supremum domains must be backward-contained,
with initial variation handled by the same characteristic or fixed-point
PDE integration as in FGF048. These are sufficient absolute estimates,
not necessary conditions for the one-sided budget (D).

In fact the exact inverse derivative is

    2b g_x=xi_+-xi_- -2 Hcal_chi k.                  (5.4)

The identical -Cn_x/tau terms in the two Q source derivatives do not cancel
in their characteristic integrals: lambda_+=-b and lambda_-=+b follow
DIFFERENT paths. Subtracting their PDEs at the same point leaves the spatial
transport term, equivalent to g_t=p_x, not an estimate for g_x. The scale
term 2Hcal_chi k in (5.4) is also present. A cancellation proof would have
to control the two-path density-source difference and these field/scale
terms, with their actual coefficient variation.

The relevant density identities, retaining compression, are

    D_v n=-n v_x,
    D_v n_x=-2v_x n_x-n v_xx,
    D_v q_x=-v_x q_x-v_xx.                            (5.5)

The last two hold in the spatial weak/difference-quotient sense for C1,1
solutions, with v_xx a.e.; no classical f'' is assigned at a join.
As a conservative finite-interval consequence,

    ||n_x(t)|| <= [||rho_x||+
       integral_0^t ||n(u)|| ||v_xx(u)||du]
       exp(2 integral_0^t ||v_x(u)||du).              (5.6)

FGF048 proves, only through kappa/omega with its fixed small dimensionless
kappa (physical kappa ell/V), bounded density, ||v_x||=O(N^4),
Lip(v_x)=O(N^7), q_x=O(N^3), and g_x-g0_x=O(N^-1).
Consequently (F),(D) are easily within their budgets on THAT short interval:
the force impulse and adverse-derivative integral there are O(N^-4),
whereas their allowed totals scale as V=O(N) and omega=O(N^4).
This early consumption leaves a large budget but says nothing about the
remaining interval. There is no supplied bound on the integrals in (5.6),
on the chart displacement in (5.3), or on (5.4) from kappa/omega to B_*/omega.
Near compression, growth of n and n_x is exactly what those estimates must
address. The sign Cn>0 in B_x=Cn+tau p_t is not a sign theorem for g_x:

    B_g g_x=Cn+tau p_t-B_chi k.                      (5.7)

Neither p_t nor the scale contribution has the necessary signed bound.

The FIRST unresolved field input for this conditional route is therefore a
non-circular derivation of (F),(D) on the entire candidate continuation from
(5.1)-(5.5), or a sharper substitute yielding the same weighted-gradient
comparison. Compact field-state control would make (F) easy for large N,
but is itself proved only on the shorter interval. A sufficient stronger
route would control a compact chart and integral_0^T B_f so that (5.3)
implies (D); the current n_x estimate does not close it. We make no claim
that this sufficient absolute route is necessary or that the target is false.

## 6. Continuation gate and endpoint distinctions

The contradiction concerns a full positive classical slab; no endpoint type
is needed for it. To separate other failure mechanisms, fix N and consider
an actual compatible C1/C1,1 branch on a buffered physical domain. Suppose,
up to a finite endpoint t*, its complete state lies in a fixed compact set
with n>=m_n>0 and g>=m_g>0, bounded chi (hence a bounded away from zero),
and its full first spatial derivatives are uniformly bounded. Assume these
bounds on a slightly larger backward-contained domain than the compact
interior on which restart is claimed. Speed/displacement and a positive
spatial buffer must be checked there; an unbuffered cone-tip restart is not
asserted.

These hypotheses imply, for this fixed N, a bound on the C1,1 seminorm.
Here is the actual coupled gate, in fixed nondimensional units. Let
A_f=max(||r_x||,||s_x||), B_f=max_i||Z_i,x||,
H_f=max(Lip r_x,Lip s_x), H_z=max_i Lip Z_i,x.
On the compact state set, the same pair-characteristic differentiation of
(3.1),(5.1) gives finite coefficient constants with

    H_f(t)<=H_f(0)+integral[3A_f H_f+G H_z+G2 B_f^2],
    H_z(t)<=H_z(0)+integral[(3L1 B_f+P)H_z+(P/c)H_f
                            +L2 B_f^3+Q(B_f+A_f/c)^2]. (6.1)

P,Q include the actual density dependence n=exp q on the assumed compact
q range. They need not be independent of N in this endpoint proposition.
These inequalities follow by taking the difference of gradient ODEs on two
characteristics, dividing by their separation, and using the flow Jacobian
rate. They preserve the original Lipschitz joins. Since A_f,B_f are bounded,
(6.1) is linear in H_f+H_z with finite constant forcing; its integrating factor
gives a finite bound through t*. This is the coupled derivation, not a transfer
of the frozen-force continuation theorem.

For the diagonal state U=(r,s,Z), the PDE bounds U_t; differentiating it a.e.
gives (U_i,x)_t=-lambda_i U_i,xx-(D lambda_i.U_x)U_i,x+D H_i.U_x.
The just-derived bound gives a uniform time-Lipschitz C1 trace on the smaller
interior. It remains in the chart and is compatible: chi_x=k, g_t=p_x and
phi_x=g persist as in the pinned construction. The accepted local C1,1
characteristic construction applies to an extension of this trace; uniqueness
on a smaller backward domain supplies a local restart. No N-uniform restart
length is required.

Thus, UNDER these extra state/margin/domain hypotheses, bounded first
derivatives preclude an independent loss of the higher regularity needed
for restart. Outside them, the possibilities remain distinct:

- first derivatives become unbounded;
- a positive density or B_g/g/a coefficient margin is lost, or the state
  escapes the bounded chart (including scale or field amplitude growth);
- restart regularity has not been controlled because the stated gate failed;
- the physical domain or its required buffer is exited.

Section 3 excludes domain exit through T_N conditional on (F) for the specified
cone/characteristic. Equations (3.3),(4.2) bound density for fixed N conditional
on the budgets. They do not bound all field/scale states or g away from zero.
Consequently no unconditional maximal-endpoint classification follows here.
If a constructed branch is independently shown to satisfy the budgets and
all the state/domain gates up to its maximal endpoint, (6.1) would reduce an
earlier nonextendible endpoint to first-derivative breakdown. That is an
additional conditional implication, not this run's actual-family result.

## 7. Full energy, moving boundaries and exact control

For the fixed-reference actual equations set

    e(n)=c^2 n[log(n/nref)-1],
    E=nv^2/2+e(n)+n phi
       +[tau p^2/2+W+sigma w^2/2+J k^2/2+U_s]/C,
    F=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Jwk)/C.       (7.1)

Matter plus interaction has exchange +np. Since W_t=Bp_x-Tw, the Q field
has exchange -np-Tw/C. The scale equation gives +Tw/C. Hence E_t+F_x=0.
The sign of BOTH field fluxes and the full scale energy are essential.
For arbitrary moving endpoints alpha(t),beta(t) inside the solution domain,

    d/dt integral_alpha^beta E dx
       =F(alpha)-F(beta)+beta' E(beta)-alpha' E(alpha). (7.2)

For K_t the last two terms equal -S_N[E(beta)+E(alpha)]. No conservation
of the shrinking-cone integral or positive global energy is asserted.
Initial excess over the hydrostatic datum is exactly rho v^2/2 on the compact
bump, with integral O(V^2 ell)=O(N^-1); this integral does not control n_x,
g_x, compact chart margins or the adverse budget.

With v initially zero, the full hydrostatic tuple is an exact stationary
solution, p=w=0, F=0. The actual field source and full scale balance remain
satisfied. Its weighted-gradient identities agree with (3.1), but it lacks
the large compressive initial w_c>=b_* omega. Thus the contradiction is not
erroneously triggered by this negative control. Local uniqueness identifies
the constructed control with hydrostatics on common physical domains.

## 8. Scope, attempted routes and checkpoint

Carry a_ref=9.3619e-11 and 1.1279e-10 m/s^2 SEPARATELY, with their own
compatible backgrounds, constants and N thresholds. The adopted relation is
a_ref=kappa_vac c_light sqrt(G_Newton rho_Lambda,ref), with kappa_vac adopted,
not derived. A constant-vacuum reference, each separately frozen comparison
a_ref=a0 E(z), E(z)^2=.315(1+z)^3+.685, and an evolving reference are different
histories. Section 7 covers fixed reference only; an evolving reference has
protocol work and is excluded from this conservation claim.

The diagnostic chi adds a degree of freedom. This is not a physical pointwise
vacuum relation, metric/photon/two-DOF completion, criterion B, calibrated
cluster evidence, cosmology or historical novelty. Q is not RAR, registered M
or filtered MONO. No current primary or AS task is promoted by this result.

Executed routes: (i) reconstruct the weighted gradient for actual g(t,x),
leading to the proved integrated-budget theorem; (ii) differentiate actual
field characteristics and density transport, isolating the unclosed source
and chart estimates; (iii) audit static-source sign, two-path cancellation,
energy and higher-regularity shortcuts, preserving their exact failures in
FAILED_ESTIMATES.md. No stable coupled solution counterexample was found or
claimed. The unconditional route remains OPEN, deferred at the explicit
full-interval feedback bound. A useful next attempt must estimate the two
oppositely transported n_x sources in (5.2)-(5.4), or obtain a signed p_t/
scale estimate in (5.7), on the compression horizon; rerunning the short-kappa
bootstrap unchanged would not address it.

Self-audit primary verdict for the actual-family target: CONDITIONAL ON THE
NAMED INPUT (F),(D). Within that conditional statement the proof is complete;
it is not an independent review. Zero mathematical executable computations.
