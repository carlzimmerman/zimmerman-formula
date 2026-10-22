# FGF048: uniform short time for the actual coupled diagnostic system

Author: `/root/fgf048_author`, current Codex agent (model identifier not exposed
in this child context). Proof-only author candidate; independent review pending.
No new stage35 root or reviewer proof has been read. The fixed-N construction
used below is the hash-pinned, accepted FGF047 proof, not an assumed uniform
existence theorem. Eight task ancestry pins and the task hash matched; old
FGF047 text was read just before checking its ancestry hashes. No mathematical
executable computation, external theorem, numerical sample or literature lookup
is used.

## 1. Claim and fixed data

Fix the same positive physical coefficients C=4pi G_Newton, tau, sigma, J,
S0, cs, nref and a_ref. On the same smooth hydrostatic positive-gradient patch
U, the background (rho,phi0,chi0) obeys, with g0=phi0_x>0,

    B(g0,a_ref exp chi0)_x=C rho,
    cs^2 (log rho)_x=-g0,
    J chi0_xx+T(g0,a_ref exp chi0)-U_s'(chi0)=0.

Here U_s(chi)=S0[cosh(2chi)-1]/4, and EXACTLY

    B(g,a)=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=integral_0^g B(s,a) ds,  T=-W_chi,  a=a_ref exp chi.

Choose K0=[x*-R,x*+R] compactly inside U, and fixed L,v0>0. For every
integer N>=1 with ell=L/N^3<R/2, prescribe exactly

    n=rho, phi=phi0, chi=chi0, phi_t=chi_t=0,
    v=V f((x-x*)/ell), V=v0 N,
    f(y)=(1-y^2)^2 (|y|<1), and f(y)=0 (|y|>=1).

The original C1,1 joins are retained: ||f||=1, ||f'||=8/(3sqrt(3)),
Lip(f')=8. We prove that some fixed kappa>0, independent of N, gives an
actual classical solution through

    T_N=kappa ell/V=(kappa L/v0)N^-4.

It has positive density, scale and g bounds independent of N on a quantitatively
contained physical cone including [x*-R/2,x*+R/2] for the whole interval.
Matter and first field derivatives are spacetime C1, uniformly C1,1 in space
for each N; phi and chi are C2. The actual four equations are

    n_t+(nv)_x=0,
    v_t+v v_x+cs^2(log(n/nref))_x=-phi_x,
    tau phi_tt=B_x-Cn,
    sigma chi_tt=J chi_xx+T-U_s'(chi).

We also obtain constants independent of N such that

    sup |g-g0| <= C_g N^-4,
    sup |g_x-g0_x| <= C_dx N^-1.

Explicit definitions and sharper time-dependent bounds appear below. These
are lower-time and feedback estimates, not a shock, upper-lifespan, endpoint,
post-shock, crossing or global theorem.

## 2. Fixed units, extension and exact diagonal structure

To avoid adding unlike dimensional quantities, use X=(x-x*)/L,
theta=v0 t/L, velocity unit v0, potential unit v0^2, density unit nref,
acceleration unit v0^2/L, p=phi_t unit v0^3/L, w=chi_t unit v0/L, and
k=chi_x unit 1/L. Suppress hats until Section 8. Thus V=N, ell=N^-3 and
the requested time is kappa N^-4. The fixed dimensionless coefficients are

    c=cs/v0, tau_hat=tau v0^2, sigma_hat=sigma/v0^2,
    J_hat=J/v0^4, C_hat=C nref L^2/v0^2,
    a_ref_hat=a_ref L/v0^2, S0_hat=S0 L^2/v0^4.

The equations keep their displayed form after using these coefficients and
n=exp q, q=log(n_physical/nref). No physical coefficient depends on N.
In the rest of the proof tau,sigma,J,C,a_ref,S0 mean these fixed numerical
coefficients; R means R_physical/L. Norms below are dimensionless.

Use one N-independent smooth extension to the line: extend q0,chi0 by cutoffs
to constants, and g0 by a positive convex cutoff to a positive constant.
The extension agrees with the background on a neighborhood of K0, has all
background derivatives bounded, and has 0<m<=g0<=M. Put k0=chi0_x,
p0=w0=0 and retain the exact compact velocity. Take phi0 to be the compatible
antiderivative of g0. Exterior hydrostatics are neither needed nor asserted.
No infinite absolute background-energy integral is used.

Set d=sqrt(J/sigma), b=sqrt(B_g/tau), and choose fixed g_*>0. Define

    h(g,chi)=integral_{g_*}^g b(s,chi) ds,
    r=v+cq, s=v-cq,
    Rplus=p+h, Rminus=p-h,
    Zplus=w+d k, Zminus=w-d k,
    z=(Rplus,Rminus,Zplus,Zminus,chi).

Since B_g=2g/sqrt(a^2+4g^2)>0, the field chart z is a smooth invertible
chart for (p,g,w,k,chi) on g>0. Its inverse uses b>0 and d>0, both bounded
away from zero on the fixed compact field set used below. The fluid inverse
uses the fixed physical c>0; no c/N inverse is introduced.

Write A=B_chi k/tau-C exp(q)/tau and D=(T-U_s')/sigma. The EXACT system is

    r_t+(v+c)r_x=-g(z),   s_t+(v-c)s_x=-g(z),
    Rplus_t-b Rplus_x=A+h_chi(w-b k),
    Rminus_t+b Rminus_x=A-h_chi(w+b k),
    Zplus_t-d Zplus_x=D, Zminus_t+d Zminus_x=D,
    chi_t=w.                                                   (2.1)

Thus the five field equations have the structural form

    z_i,t+lambda_i(z)z_i,x=H_i(q,z).                            (2.2)

Crucially, lambda_i and H_i do not depend on v or on derivatives. All
chi-dependent terms in (2.1) remain. The fluid characteristic speeds are
linear in (r,s), while field speeds depend on z alone.

The accepted fixed-N construction supplies a local C1/C1,1 solution of this
system for each N and arbitrary compatible C1,1 restart data in this chart.
For completeness, its construction freezes the previous characteristic speeds
and sources, integrates the resulting linear transport equations, proves a
C0 contraction and uniform Lipschitz bounds for spatial derivatives, and uses
||u_x-v_x|| <= 2 sqrt(2H||u-v||) to obtain the C1 limit. Its time is positive
for each fixed data set. We use that construction only for local starts and
restarts; all uniformity is derived below.

## 3. Fixed coefficient neighborhood and estimates

The extended initial field range K=closure{z0(x)} is compact in its chart.
Choose delta>0 so the closed 2delta-neighborhood of K lies strictly in the
chart and its primitive image has

    m/2 <= g <= 2M,
    chi_min-1 <= chi <= chi_max+1,

and bounded p,w,k. Here chi_min/max refer to the extended initial background.
Let q_- and q_+ be the extrema of q0. Coefficients can be smoothly extended
by cutoffs outside a neighborhood of

    q_- -1 <= q <= q_+ +1,   dist(z,K)<=2delta.

Take cutoffs equal to one on this set. Their extended derivatives have global
bounds, so coefficient differences need not be estimated along a line segment
leaving the chart. All constants below are fixed, independent of N. Let

    Lambda >= max_i |lambda_i|,
    F >= max_i |H_i|,
    G >= ||D_z g||, G2 >= ||D_z^2 g||,
    L1 >= max_i ||D_z lambda_i||,
    L2 >= max_i ||D_z^2 lambda_i||,
    P >= max_i ||D_(q,z) H_i||,
    Q >= max_i ||D_(q,z)^2 H_i||.

These norms are max-component induced linear/bilinear norms. Include the
smooth extended g in G,G2, and let gbar be its absolute bound on the physical
coefficient neighborhood. We need only actual equations inside that neighborhood.

Let A(t)=max(||r_x||,||s_x||), Bf(t)=max_i||z_i,x||, and B0=Bf(0).
The fluid derivative equations and differentiated field characteristics give

    A(t) <= A0+integral_0^t [A^2+G Bf] du,
    Bf(t) <= B0+integral_0^t [L1 Bf^2+P(Bf+A/c)] du.           (3.1)

Indeed |v_x|<=A and |q_x|<=A/c. The second inequality follows from
D_i z_i,x=-(Dlambda_i.z_x)z_i,x+H_i,q q_x+D_z H_i.z_x.
These equations follow by differentiating the C1 characteristic formula;
no second spatial derivative is needed here.

In addition the exact fluid identity and the field PDE imply

    (partial_t+v partial_x)q=-v_x,
    ||z(t,.)-z0(.)|| <= integral_0^t [Lambda Bf+F]du.          (3.2)

The first controls q along the actual fluid trajectories and not through a
rectangular box in r,s. The auxiliary line has no spatial boundary, and the
finite fixed-N speed bound below makes those trajectories legitimate.

## 4. Explicit N-independent small time and strict bootstrap

Put P_N=N^4, and define fixed constants

    a0=8/(3sqrt(3))+c||q0_x||,
    a=2(a0+1),
    beta=2(B0+1+P a/c),
    Q0=||q0||,
    s0=1+c Q0+gbar+c+Lambda+1.

For N>=1, A0<=a0 P_N. Choose any positive kappa no larger than

    min{1,
        1/(2a),
        (a-a0)/(2(a^2+G beta+1)),
        (beta-B0)/(2(L1 beta^2+P beta+P a/c+1)),
        delta/(2(Lambda beta+F+1)),
        R/(4s0)}.                                           (4.1)

Every denominator is positive and finite. None involves N, a rescaled sound
speed, a field cutoff depending on v, or an initial C1,1 seminorm.

On a local branch bootstrap A<a P_N, Bf<beta,
q_- -1<q<q_+ +1 and ||z-z0||<delta. For t<=kappa/P_N, (3.1) gives

    A(t) <= [a0+kappa(a^2+G beta)]P_N < a P_N,
    Bf(t) <= B0+kappa(L1 beta^2+P beta+P a/c) < beta.          (4.2)

These are strict improvements; in using G beta/P_N<=G beta P_N we used
P_N>=1 only. Equations (3.2) give the stronger margins

    q_- -1/2 <= q(t,x) <= q_+ +1/2,
    ||z(t,.)-z0(.)|| <= delta/2.                             (4.3)

Every fluid trajectory begins on the initial line, so (4.3) follows from
integral A<=a kappa<=1/2, without any exponential-in-N density bound.
The invariant source equations also give

    |r|,|s| <= N+c Q0+gbar t,
    |v| <= N+c Q0+gbar       (t<=1).                         (4.4)

Thus every characteristic speed is strictly less than

    S_N=N+c Q0+gbar+c+Lambda+1 <= s0 N.                     (4.5)

The bootstrap inequalities control a genuine local solution; they do not
assert it already exists until the desired endpoint. Section 5 closes that
logical gap by constructing traces and restarts.

## 5. Exact C1,1 propagation and continuation, not an assumed gate

Write Hf=max{Lip(r_x),Lip(s_x)}, Hz=max_i Lip(z_i,x), Htot=Hf+Hz.
On any existing bootstrap interval, comparing derivative equations along two
characteristics gives the integral inequalities

    Hf(t) <= Hf(0)+integral[3A Hf+G Hz+G2 Bf^2],
    Hz(t) <= Hz(0)+integral[(3L1 Bf+P)Hz+(P/c)Hf
                             +L2 Bf^3+Q(Bf+A/c)^2].        (5.1)

For the first line, the differentiated speed is v_x and its Lipschitz
seminorm is bounded by Hf. The two transport contributions give 2A Hf
and the differentiated speed contribution gives A Hf. The force composition
has seminorm at most G Hz+G2 Bf^2. For the second line, the corresponding
three speed terms are bounded by 3L1 Bf Hz+L2 Bf^3, and the source
composition gives P(Hz+Hf/c)+Q(Bf+A/c)^2.

These statements can equivalently be obtained by a.e. differentiation of
Lipschitz spatial gradients. More explicitly, the flow Jacobian is positive
and solves J_t=lambda_x J; subtract the two first-gradient ODEs and divide
by the separation of their characteristics. Its logarithmic rate contributes
the second transport term. Integration bounds the spatial difference quotient,
so (5.1) holds for the original Lipschitz gradients even at the polynomial
joins. We do not assign a classical f'' there or smooth the initial data.

With A<=a N^4 and Bf<=beta, fix E,D>0 satisfying, for every N>=1,

    3A+G+3L1 Bf+P+P/c <= E N^4,
    G2 Bf^2+L2 Bf^3+Q(Bf+A/c)^2 <= D N^8.

For example, the same sums with A replaced by a and Bf by beta define
suitable E,D (enlarging to a positive number if needed). The exact initial
profile gives Htot(0)<=h0 N^7 for fixed

    h0=8+c Lip(q0_x)+Hz(0).

Iterating the integral inequality in (5.1), or its scalar integrating factor,
therefore yields, for t<=kappa N^-4,

    Htot(t) <= [h0 N^7+D N^8 t] exp(E N^4 t)
             <= C_H N^7,
    C_H=(h0+D kappa)exp(E kappa).                            (5.2)

Here N^4<=N^7. This is precisely where the large initial N^7 seminorm is
retained without shortening the N^-4 time. The generic, undifferentiated
seven-component cubic bound would obscure this block structure.

For EACH fixed N, the strict state margins (4.3), amplitude bound (4.4),
first-gradient bounds (4.2) and finite Lipschitz bound (5.2) are a sufficient
restart gate. To prove it directly, suppose an endpoint t*<=kappa N^-4
were approached through this branch. The PDE bounds U_t uniformly, where
U=(r,s,z), and its spatial derivative, interpreted a.e., is

    (U_i,x)_t=-lambda_i U_i,xx
               -(Dlambda_i.U_x)U_i,x+D F_i.U_x.             (5.3)

All terms in (5.3) have finite bounds for this fixed N. Spatial gradients
are therefore uniformly Lipschitz in time in the L-infinity norm: integrate
(5.3) distributionally, and use their continuous spatial representatives.
The states and gradients have uniform limits at t*. Integration in x shows
that the limiting state has the limiting first derivative, which retains the
Lipschitz seminorm in (5.2). The trace stays strictly inside the chart and
q-neighborhood by (4.3). Its amplitude is finite by (4.4).

Apply the pinned FGF047 characteristic construction to this exact C1,1 trace.
It produces a positive restart interval (depending on this fixed N is allowed).
Local uniqueness, proved by the same characteristic difference inequality,
glues it to the old solution. Gradient compatibility persists by Section 7.
Thus no such finite endpoint prevents extension. Taking the union of local
intervals and applying the strict improvements proves existence through
kappa N^-4, and indeed a short interval beyond it for each fixed N.

This argument derives rather than assumes the higher norm and the trace. It
does not infer uniform existence from fixed-N existence alone, does not require
a uniform individual restart length, and does not classify arbitrary maximal
endpoints beyond the controlled interval.

## 6. A spatial derivative estimate for the force feedback

A first estimate already follows from g_t=p_x and
p=(Rplus+Rminus)/2:

    ||g(t,.)-g0|| <= beta t.                                (6.1)

This is valid on the entire auxiliary line and hence on the physical domain.
It also gives positive g directly when combined with the fixed margins in
Section 3. It is conservative; initial p_x=0 is not used to claim a formal
second-order Taylor bound.

We can improve the spatial derivative estimate beyond the crude O(1) bound.
Differentiate q_t+v q_x=-v_x along the fluid flow, in the same Lipschitz
sense as (5.1):

    D_v q_x=-v_x q_x-v_xx.

The bound |v_xx|<=Hf a.e. and (5.2) imply

    ||q_x(t)|| <= [||q0_x||+C_H N^7 t] exp(a N^4 t)
                <= C_q N^3,
    C_q=(||q0_x||+C_H kappa)exp(a kappa).                   (6.2)

Now repeat ONLY the field line of (5.1), using (6.2) instead of the crude
A/c inside the quadratic source term. The linear Hf/c term is unchanged.
Define fixed nonnegative constants

    E_z=3L1 beta+P,
    D_z=(P/c)C_H+L2 beta^3+Q(beta+C_q)^2.

For N>=1, the field inequality becomes

    Hz(t) <= Hz(0)+integral_0^t [E_z Hz+D_z N^7]du,
    Hz(t) <= [Hz(0)+D_z N^7 t]exp(E_z t).                   (6.3)

In fact q_x^2=O(N^6), which is bounded by N^7 here. Since p is the average
of two field coordinates, Lip(p_x)<=Hz. Differentiating
 g(t)-g0=integral_0^t p_x(u)du
in the weak spatial sense and then using continuity of g_x-g0_x gives

    ||g_x(t)-g0_x||
      <= exp(E_z kappa)[Hz(0)t+(D_z/2)N^7 t^2].             (6.4)

The weak derivative bound applies a.e. and therefore everywhere to the
continuous representative. This step requires no classical p_xx at the joins.
At t<=kappa N^-4, (6.4) is at most

    exp(E_z kappa)[Hz(0)kappa+(D_z/2)kappa^2] N^-1.          (6.5)

This is an actual feedback estimate on a proved interval, not a Taylor jet.
We claim neither optimality of N^-4 in (6.1) nor of N^-1 in (6.5).

## 7. Constraints, physical domain, uniqueness and positive states

The scale pair implies k_t=w_x; chi_t=w then propagates chi_x=k. Subtracting
the two R equations gives b(g_t-p_x)+h_chi chi_t=h_chi w, hence g_t=p_x.
Adding gives

    p_t=b^2 g_x+A+b h_chi(chi_x-k).

The last term vanishes by the already proved scale constraint. Reconstruct
phi=phi0+integral p dt. Then phi_x=g and phi_t=p, and the exact source is

    B_x=C exp(q)+tau phi_tt.

It is not a static MOND inversion. The smooth inverse chart and C1 limit give
the regularity stated in Section 1. These identities also hold at restart
traces, so the construction never drops compatibility.

Define, in the dimensionless coordinates,

    K_t=[-R+S_N t, R-S_N t].                                (7.1)

Every backward characteristic and every vertical reconstruction segment from
K_t stays in K_u at earlier u. This follows from the strict speed bound (4.5)
and the inward slopes of its endpoints. The last constraint in (4.1) gives
S_N t<=s0 kappa N^-3<=R/4. Thus K_t contains [-3R/4,3R/4] and in particular
the fixed central [-R/2,R/2]; it stays within the same original regular patch.
The initial support is in [-R/2,R/2] by the specified ell<R/2 condition.
No wall or zero-gradient crossing enters any footprint.

The propagated positive-state bounds on this physical cone are

    nref exp(q_- -1/2) <= n_physical <= nref exp(q_+ +1/2),
    a_ref exp(chi_min-1) <= a <= a_ref exp(chi_max+1),
    m/2 <= g_dimensionless <= 2M.                          (7.2)

They are independent of N and hold on an explicitly contained domain.
Constants can be conservative because they come from one fixed extension.

For two C1 solutions on a common backward domain, subtract their diagonal
systems along the first solution's characteristics. On their compact state
ranges, with their finite first-gradient bounds, the difference satisfies
D(t)<=C integral_0^t D(u)du when its initial trace vanishes. Iteration gives
D(t)<=Dmax(Ct)^j/j! and hence zero. Thus the physical solution is independent
of exterior choices on every common backward domain. Comparing two fixed
extensions gives the quantitative common horizon min(kappa_1,kappa_2)N^-4
with speed max(S_N,1,S_N,2) and the corresponding explicit R/4 containment
gate. We do not claim one numerical kappa works for every unbounded choice
of arbitrary exterior norms. One fixed extension supplies the asserted
N-independent physical existence time; uniqueness makes its physical germ
intrinsic. There is no lateral boundary data assumption.

## 8. Physical feedback constants and local energy

Restoring units, let beta,C_dx_dimless denote the constants in (6.1),(6.5).
For 0<=t<=T_N, on the physical domain,

    ||g(t)-g0|| <= (v0^3/L^2) beta t
                 <= (v0^2/L) beta kappa N^-4,
    ||partial_x(g-g0)||
      <= (v0^2/L^2)exp(E_z kappa)
             [Hz(0)kappa+(D_z/2)kappa^2]N^-1.              (8.1)

Thus C_g=(v0^2/L)beta kappa and the displayed acceleration-gradient
coefficient is C_dx. The strictly positive gradient of the potential means
g=phi_x>0, and (7.2) preserves it uniformly. If the phrase instead refers
to a separately assumed positive derivative g0_x>=mu>0 on a compact
subdomain, (8.1) preserves that additional margin for N>2C_dx/mu there;
we do not presume such a background derivative margin from g0>0 alone.

The full physical local energy is

    e(n)=cs^2 n[log(n/nref)-1],
    E=nv^2/2+e(n)+n phi
       +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U_s]/C,
    F=nv[v^2/2+cs^2 log(n/nref)+phi]-(pB+Jwk)/C.

The actual fluid exchange after adding n phi is +np. The Q field exchange
is -np-Tw/C since W_t=Bp_x-Tw. The scale exchange is +Tw/C. Therefore
E_t+F_x=0 pointwise in the proved regularity, including both field fluxes.
For moving endpoints alpha,beta inside the domain,

    d/dt integral_alpha^beta E
       =F(alpha)-F(beta)+beta' E(beta)-alpha' E(alpha).

For (7.1) the endpoint contribution is -S_N[E(beta)+E(alpha)] in matching
units. No conserved shrinking-cone integral or global positive energy is
claimed. Initial excess energy is only kinetic and is O(V^2 ell)=O(N^-1)
on the compact support; this small integral was not used for regularity.

Set the initial velocity to zero as the negative control. The original
hydrostatic tuple satisfies all four equations, with p=w=0, unchanged chi
balance, and zero full flux. Local uniqueness identifies our restriction
with that stationary tuple on every common backward domain. Nonhydrostatic
exterior extensions do not change this control inside its causal footprint.

## 9. Framework, failed estimates, and author review

The entire proof is repeated separately for a_ref=9.3619e-11 and
1.1279e-10 m/s^2, with their own fixed backgrounds and constants. Both are
positive; no equality of backgrounds or constants is assumed. If desired,
taking the smaller of their two kappas produces a common positive time
coefficient for this finite pair. Constant vacuum and a separately frozen
reference a0 E(z), E(z)^2=.315(1+z)^3+.685, are separate histories. The proof
applies at any individually fixed positive reference with its own compatible
background. Evolving H/reference protocols introduce the pinned FGF032 work
term and are not covered by this fixed-reference conservation result.

The following unsuccessful estimates are preserved in FAILED_ESTIMATES.md:
the old same-point full-state cutoff bound, a rectangular invariant bound
for density, pressureless diagonal-inverse reasoning, and a generic cubic
higher-gradient bound. Their failures are failures of estimates, not
counterexamples to existence. The successful substitute is the actual
triangular coefficient structure together with density transport and the
linear higher-norm restart estimate.

Author proof-audit verdict: **proved as written for the bounded local claim**,
subject to independent review. Dependency chain: pinned fixed-N construction
and exact characteristic chart -> strict blockwise gradient/state bounds ->
C1,1 propagation -> trace/restart -> uniform horizon -> feedback and domain
bounds. All external leaves are pinned internal proofs; no literature theorem
or finite sample is promoted to a universal assertion. The proof does not
transfer the old fixed-force compression endpoint or upper-lifespan theorem.

Q remains distinct from RAR, registered M, and filtered MONO. This diagnostic
scale field is an added dynamical degree of freedom, not a physical vacuum
completion, metric/photon coupling, two-gravitational-DOF result, criterion B,
calibrated cluster evidence, historical novelty, cosmology or theory closure.
AS1486/1562/759 and AS1174/1143/1168 are other targets; no claims transfer.
