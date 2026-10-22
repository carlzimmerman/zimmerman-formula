# FGF052: protected traces, interval momentum, and the unresolved transfer budget

Author: `/root/fgf052_author`; run `fgf052_run_001`. Proof-only. The task
and all ten ancestry hashes were verified before ancestry text was used.
This derivation uses the checked FGF051 local theorem, its original equations,
and elementary differentiation/integration. No new stage39 coordinator or
reviewer proof, preview, or result was read. It is an author candidate,
not independently accepted evidence. No mathematical executable computation
was performed; SHA verification is metadata only.

## 1. Claim and fixed physical conventions

Fix the positive coefficients C=4 pi G_Newton, tau,sigma,J,S0,cs,nref,L,v0,
a_ref, and a smooth compatible hydrostatic background rho,g0,chi0 on a fixed
neighborhood of x*, with rho,g0>0. None depends on N. Work throughout in
physical units, per unit transverse area in this one-dimensional diagnostic.
Let g=phi_x, p=phi_t, k=chi_x, w=chi_t, a=a_ref exp(chi), and

    B(g,a)=(sqrt(a^2+4g^2)-a)/2,
    W(g,a)=integral_0^g B(s,a) ds, T=-W_chi,
    U(chi)=S0[cosh(2chi)-1]/4.

The equations, with fixed reference a_ref, are

    n_t+(nv)_x=0,
    v_t+v v_x+cs^2(log(n/nref))_x=-g,
    tau p_t=B_x-Cn,                 g_t=p_x,
    sigma w_t=J k_x+T-U',           k_t=w_x, chi_t=w.       (1)

The compatible hydrostatic equations are

    (B0)_x=C rho, cs^2 rho_x=-rho g0,
    J (k0)_x+T0-U'(chi0)=0, k0=(chi0)_x.                  (2)

Keep the EXACT initial data n=rho, phi=phi0, chi=chi0, p=w=0 and

    v=V f((x-x*)/ell), V=v0 N, ell=L N^-3,
    f(y)=(1-y^2)^2 for |y|<1, f=0 for |y|>=1.              (3)

These are C1,1 joins and are never smoothed. Pressure and every coupling
remain in (1). All results about the entire interval below are conditional
on an existing compatible classical whole-packet branch in the positive
chart n>0,g>0 on the common domain. The field a is positive by definition.
This positive-chart restriction is the one used by FGF051's comparison
chart; no assertion about continuation through g=0 is made. The regularity
C1 for first-order variables and C2 for potentials suffices for the balances.

For every fixed B_dagger>0 and sufficiently large N, the two fixed interval
endpoints constructed below have EXACT stationary hydrostatic traces through
T_N=B_dagger ell/V, on the actual local solutions. Any existing positive
whole branch agrees at those traces. On that branch mass is conserved and
full momentum is conserved, while matter momentum is generally not.
A finite-interval first-moment identity yields a conditional obstruction to
existence through T_N under the exact signed transfer criterion (18).
Its convenient fractional form has limiting coefficient
15/[8(1-eta)] for fixed 0<=eta<1. The transfer criterion is NOT proved for
actual whole-packet evolution. The unconditional energy estimate proved in
Section 7 is a factor N too weak to supply it. This is the scoped result.

## 2. Exact exterior traces from the checked local theorem

Use the constants R_i,R_o,S,k_edge of the pinned FGF051 theorem, where
all physical local speeds have magnitude <v0 S and the fixed strips
|x-x_e|<=L R_i N^-7/2 persist on the constructed edge solutions, for
x_-=x*-ell, x_+=x*+ell. Write h=L N^-7/2 and choose fixed

    d=R_i/2, r=R_i/4,
    a_N=x_--d h, b_N=x_++d h,
    R_N=ell+d h, D_N=b_N-a_N=2R_N.                        (4)

The initial intervals [a_N-rh,a_N+rh] and [b_N-rh,b_N+rh]
are strictly outside the original velocity support: their nearest distances
from it are (d-r)h=rh. They lie strictly inside the protected edge strips
since d+r=3R_i/4<R_i. Consider the shrinking exterior cones

    E_a(t)=[a_N-rh+v0 S t,a_N+rh-v0 S t],
    E_b(t)=[b_N-rh+v0 S t,b_N+rh-v0 S t].                 (5)

For fixed B_dagger, take N large enough that

    B_dagger N^-1/2<=k_edge,
    S B_dagger N^-1/2<r/2,                               (6)

and the initial strips lie in the background neighborhood. Then (5) exists
through T_N, remains in the fixed protected strips, and contains a fixed
neighborhood of each endpoint of radius rh/2. It also remains outside the
original support, although coincidence with the stationary solution below
comes from initial agreement and uniqueness, not from that geometric fact.

The exact stationary hydrostatic tuple H=(rho,0,g0,0,chi0,k0,0), with its
potentials phi0,chi0, solves all of (1), by (2). On E_a(0), E_b(0) it
agrees with the actual edge data. To prove equality, use FGF051's diagonal
variables U and stationary variables H in that same positive chart. Along
an actual edge characteristic of family i,

    D_i^U(U_i-H_i)=F_i(U)-F_i(H)
                  -[lambda_i(U)-lambda_i(H)] H_i,x.     (7)

All such backward paths stay in (5) because their speeds are <v0 S.
The stationary background derivatives and the coefficient derivatives are
bounded on the compact ranges. Taking the supremum on the nested cones gives
D(t)<=K integral_0^t D(s)ds with D(0)=0, and iterating gives D=0.
Thus the actual edge solution is exactly H throughout both exterior cones.
Its potentials also agree: p=w=0 and their initial values agree. This
proves derivatives as well as values in open endpoint neighborhoods.

FGF051's one-sided comparison identifies any existing whole classical
positive branch with the local edge solution on common cones. Its proof
does not require a speed bound on the competing branch before comparison:
the coefficient difference multiplies that branch's finite first derivative.
It is applied only on compact intervals on which that branch exists, never
to construct a core solution. Therefore, for such a branch,

    (n,v,g,p,chi,k,w,phi)|_{a_N,b_N}
       =(rho,0,g0,0,chi0,k0,0,phi0)|_{a_N,b_N}.            (8)

For solutions given on open time intervals the statement holds on every
compact common time interval; no endpoint extension is inferred. B_dagger
is new and is not FGF049's B_* or FGF048's kappa.

## 3. Local momentum balances and the interaction signs

Put pi=cs^2 n. Multiplying fluid momentum by n and using continuity gives

    (nv)_t+(nv^2+pi)_x=-ng.                              (9)

Define physical field momentum densities and stresses by

    m_Q=-tau p g/C,      S_Q=(tau p^2/2+gB-W)/C,
    m_chi=-sigma w k/C,  S_chi=(sigma w^2/2+J k^2/2-U)/C.

The signs follow directly from (1). In particular W_x=B g_x-T k, hence
(gB-W)_x=g B_x+T k, and

    (m_Q)_t+(S_Q)_x=ng+T k/C,
    (m_chi)_t+(S_chi)_x=-T k/C.                          (10)

The Q equation uses B_x=Cn+tau p_t, not a static source substitution.
The scale stress has MINUS U. The Q momentum has MINUS tau p g.
The scale interaction cancels between the two equations in (10); the
matter/field force cancels only after adding (9). Consequently

    (nv+m_Q+m_chi)_t+(nv^2+cs^2 n+S_Q+S_chi)_x=0.         (11)

There is no additional n phi stress missing from (11): (9)-(10) are direct
identities for the actual equations and already cancel their force exchange.
The n phi interaction appears explicitly in the energy density below.

Fix [a,b]=[a_N,b_N], use [F]_a^b=F(b)-F(a), and define

    M(t)=int_a^b n dx, I(t)=int_a^b (x-a)n dx,
    P(t)=int_a^b nv dx, Q(t)=int_a^b m_Q dx,
    K(t)=int_a^b m_chi dx, F(t)=Q(t)+K(t).

Here K is scale momentum, not kinetic energy. Before inserting traces,

    M'=-[nv]_a^b,
    I'=-[(x-a)nv]_a^b+P,
    P'=-[nv^2+cs^2 n]_a^b-int_a^b ng dx,
    Q'=-[S_Q]_a^b+int_a^b ng dx+int_a^b T k/C dx,
    K'=-[S_chi]_a^b-int_a^b T k/C dx,
    (P+F)'=-[nv^2+cs^2 n+S_Q+S_chi]_a^b.                (12)

These display both stresses, pressure and both exchange terms separately.

For the stationary background, (10) says
(S_Q0+S_chi0)_x=rho g0 while (cs^2 rho)_x=-rho g0.
Thus the TOTAL hydrostatic stress cs^2 rho+S_Q0+S_chi0 is constant in x.
Its equality at a,b cancels the boundary term of total momentum. The
individual pressure and field stress differences generally do not vanish.
Using (8) and the hydrostatic pressure integral gives precisely

    M(t)=M0, I'=P, P+F=P0,
    P'=-A(t), F'=A(t), F(0)=0,
    A(t)=int_a^b [n(t,x)g(t,x)-rho(x)g0(x)] dx.            (13)

For example [cs^2 rho]_a^b=-int rho g0 is generally negative, not zero.
Replacing it by zero would incorrectly fail even the stationary control.
Equation (13) is the actual matter-transfer identity and does not state
that P is conserved.

## 4. Exact profile integrals, interval width, and controlled errors

Let rho*=rho(x*), rho*'=rho_x(x*) and H2=sup|rho_xx| on a fixed
background neighborhood. Taylor's formula gives a pointwise remainder
bounded by H2 z^2/2 for z=x-x*. All following estimates are uniform in N
once the interval is in that neighborhood.

Integrating the exact polynomials term by term gives

    int_-1^1 f dy=2(1-2/3+1/5)=16/15,
    int_-1^1 y f dy=0,
    int_-1^1 y^2 f dy=2(1/3-2/5+1/7)=16/105,
    int_-1^1 f^2 dy=2(1-4/3+6/5-4/7+1/9)=256/315,
    int_-1^1 y^2 f^2 dy
       =2(1/3-4/5+6/7-4/9+1/11)=256/3465.               (14)

There are no numerical quadratures or rounded coefficients here. Because the
velocity is zero outside the packet, the endpoint extensions contribute
to M0 and the moment capacity, but not to P0 or the kinetic excess E_kin,0.
Writing Delta0=int_a^b (b-x)rho dx=M0 D_N-I0, one obtains

    D_N=2ell(1+d N^-1/2),
    M0=2rho* R_N+e_M,        |e_M|<=H2 R_N^3/3,
    Delta0=2rho* R_N^2-(2/3)rho*' R_N^3+e_D,
                             |e_D|<=H2 R_N^4/3,
    P0=(16/15)rho* ell V+e_P,
                             |e_P|<=(8/105)H2 ell^3 V,
    E_kin,0=(128/315)rho* ell V^2+e_E,
                             |e_E|<=(64/3465)H2 ell^3 V^2.             (15)

For instance the error in Delta0 uses
(H2/2)int_-R^R (R-z)z^2 dz=H2 R^4/3. Its rho*' term is
rho*'int(R-z)z dz=-(2/3)rho*'R^3. Odd profile terms cancel
exactly in P0 and E_kin,0. This records the effect of varying rho and of
the chosen exterior endpoints separately. In particular, P0>0 for large N,

    P0/(M0 V) -> 8/15,
    Delta0/(P0 ell/V) -> 15/8.                           (16)

The leading correction in the second ratio includes
(1+d N^-1/2)^2 from the interval width; its remaining relative background
error is O(ell). All dimensional constants in these O terms depend only on
the fixed background, L and the chosen edge constants, not on N.

## 5. Exact conditional moment criterion

Positive density on the whole finite interval implies 0<I(t)<M0 D_N.
Integrating (13) twice yields the exact identities

    I(T)=I0+P0 T-J(T),
    J(T)=int_0^T F(s) ds
        =int_0^T (T-s) A(s) ds
        =-(1/C)int_0^T int_a^b (tau p g+sigma w k) dx ds. (17)

Thus any such branch existing through T must satisfy STRICTLY
J(T)>P0 T-Delta0. The weakest signed sufficient obstruction expressed
only through this moment identity is the threshold

    J(T)<=P0 T-Delta0.                                  (18)

Under (18), (17) contradicts strict positivity. No absolute-value bound,
pointwise gradient bound, or matter-momentum conservation is needed.
This threshold is sufficient and necessary for the contradiction produced
by this particular upper moment bound; it is not asserted to classify
existence of the PDE.

A convenient stronger sufficient hypothesis, for a fixed 0<=eta<1, is

    int_0^T (T-s) int_a^b (ng-rho g0) dx ds <=eta P0 T.    (19)

It is identical to the corresponding signed field-momentum bound
int_0^T F<=eta P0T. Bounding the integral of F_+ or |F| by eta P0T
also suffices, but is stronger. For every fixed

    B_dagger>15/[8(1-eta)], T=T_N=B_dagger ell/V,          (20)

(15)-(16) imply (1-eta)P0T>Delta0 for all sufficiently large N.
Equations (19)-(20) then preclude existence of a positive classical branch
through T_N. A finite-N fully explicit alternative to the limit in (20) is

    (1-eta)B_dagger[(16/15)rho* ell^2-(8/105)H2 ell^4]
       >=2rho*R_N^2+(2/3)|rho*'|R_N^3+H2 R_N^4/3,

with the positive bracket required; this implies the exact threshold.
The time unit ell/V=(L/v0)N^-4 is retained. P0 has units mass per area
 times velocity, J has units mass per area times length, and both sides
of (18) have those same units. A and P' are forces per transverse area.
No upper bound on the actual maximal lifespan follows until a sufficient
transfer estimate is proved on the branch, or uniformly as its endpoint
is approached. If a branch is defined only for t<T_N, a criterion only
at T_N cannot by itself assign its endpoint or provide a continuation.

## 6. Full energy and the stationary control

Define e(n)=cs^2 n[log(n/nref)-1]. The energy and flux are

    E=nv^2/2+e(n)+n phi
        +[tau p^2/2+W+sigma w^2/2+J k^2/2+U]/C,
    F_E=nv[v^2/2+cs^2 log(n/nref)+phi]-(pB+Jwk)/C.

The fluid kinetic/internal balance has source -nvg. Adding n phi leaves
+np. The Q energy balance has source -np-Tw/C, since W_t=B p_x-Tw.
The scale energy balance has source +Tw/C. Therefore

    E_t+(F_E)_x=0, d/dt int_a^b E=-[F_E]_a^b=0.          (21)

The last equality uses EXACTLY v=p=w=0 at both endpoints. Full energy is
conserved on this fixed interval; this differs from an energy on a shrinking
edge cone, where Reynolds terms would remain. Neither e nor n phi is
silently dropped in using (21).

As a negative control, replace the entire initial velocity by zero. The
stationary tuple solves every equation by (2), has all three momenta zero,
constant mass and moment, and zero energy flux. Its separate force and
pressure boundary terms cancel in P'; its Q and scale stress/exchange
terms cancel in (12); A=F=J=0. Its full stress is constant and its
energy is stationary. P0=0, so the positive-momentum hypothesis and the
fractional criterion cannot yield a contradiction for this control.

## 7. Attempted actual transfer bound and its precise shortfall

We now derive, rather than assume, what the conserved energy controls on
an existing positive-chart branch. Let phi_min=min(phi0(a),phi0(b)),
chi_bd=max(|chi0(a)|,|chi0(b)|) and E_N=int_a^b E(0). Because g>0
and the endpoint values of phi are fixed by (8), phi>=phi_min on [a,b].
Also e(n)>=-cs^2 nref pointwise, W(g,a)>=0 for g>=0, and U>=0.
Consequently the NONNEGATIVE quantity

    H_N=E_N+cs^2 nref D_N-M0 phi_min                      (22)

bounds each positive kinetic/field contribution in (21), and their sum:

    int_a^b [nv^2/2+(tau p^2/2+W+sigma w^2/2
                                  +J k^2/2+U)/C] <=H_N.

The hydrostatic initial integrand is smooth and bounded, and the potential
gauge cancels between E_N and M0 phi_min. Thus
H_N=E_kin,0+O(D_N)=O(N^-1), with leading positive coefficient
(128/315)rho* L v0^2. This energy upper bound needs no density supremum.

The scale gradient and fixed endpoint give, by the integral Cauchy-Schwarz
inequality,

    |chi(t,x)|<=chi_bd+sqrt(2 C D_N H_N/J),
    a(t,x)<=A_N:=a_ref exp[chi_bd+sqrt(2 C D_N H_N/J)].     (23)

In particular A_N is bounded independently of N; the displayed increment
is O(N^-2). For s>=0, B(s,a)>=s-a/2. Integrating and using
ag/2<=g^2/4+a^2/4 gives

    W(g,a)>=g^2/4-a^2/4,
    int g^2 <=4 C H_N+A_N^2 D_N,
    int p^2 <=2 C H_N/tau.                              (24)

All of these apply to actual energy on the branch, not to a separately
assumed positive perturbation energy. They explicitly account for the
interaction and internal energy terms that are not sign definite.
Cauchy-Schwarz now gives

    |Q(t)| <=sqrt(2 tau H_N/C)*sqrt(4 C H_N+A_N^2 D_N),
    |K(t)| <=sqrt(sigma/J) H_N,
    |F(t)| <=[sqrt(8tau)+sqrt(sigma/J)]H_N
                +A_N sqrt(2tau D_N H_N/C)=:F_bound,N.    (25)

For the scale inequality, apply 2|ab|<=a^2+b^2 to
sqrt(sigma)w and sqrt(J)k in their integrated energy; the coefficient
sqrt(sigma/J) has units inverse speed. The Q coefficient sqrt(tau)
also has units inverse speed, as follows from tau phi_tt=B_x-Cn.
Thus (25) has the correct momentum units. Because H_N=O(N^-1),
D_N=O(N^-3), and A_N=O(1), (25) supplies F_bound,N=O(N^-1).
It proves the actual but insufficient transfer estimate

    J(T_N)<=int_0^T_N |F(s)| ds<=T_N F_bound,N=O(N^-5).   (26)

The target eta P0 T_N is O(N^-6), since P0=O(N^-2).
The leading term of F_bound,N/P0 grows proportionally to N, with fixed
positive coefficients. Hence this estimate cannot certify any fixed
eta<1 as N grows. This is an algebraic scaling obstruction to this
particular energy estimate, not a counterexample to the dynamics, and not
a proof that no sharper actual estimate exists.

In exact terms the unresolved quantity is the SIGNED spacetime field
momentum

    -(1/C)int_0^T_N int_a^b (tau phi_t phi_x
                                      +sigma chi_t chi_x) dx dt,       (27)

equivalently the weighted force excess in (19), at scale O(N^-6).
There is zero initial field momentum, but (13) only says F'=A; it
provides no smallness until the correlated force int n g is controlled.
Mass/positivity fixes int n and the endpoint difference fixes int g,
while (24) gives an L2 bound on g. Those facts alone do not bound int n g
at the scale required. Density-weighted or dynamical information is missing.
The isothermal energy has also been retained and can bound an entropy,
but no entropy-to-force inequality at the required scale was derived here.
A generic arbitrary-state example would not be an actual solution and is
not used as a counterexample. Nor is any adverse-gradient supremum asserted
bounded by mass. Local edge bounds leave the core part of (27) uncovered.

One discriminating continuation is to estimate the signed core contribution
to (27), using p(0)=w(0)=0 and the actual source equations, with the target
O(P0T_N) constant strictly below 1-Delta0/(P0T_N). It must gain one factor
N over (26), or establish a favorable sign; repeating (25) cannot do so.
This run stops with that specific unresolved transfer implication.

## 8. Framework histories and exclusions

Repeat the theorem separately for a_ref=9.3619e-11 and 1.1279e-10 m/s^2,
using each normalization's compatible hydrostatic background and fixed
constants. The input relation is a_ref=kappa_vac c_light
sqrt(G_Newton rho_Lambda,ref), with kappa_vac adopted, not derived.
Its pressure version a_ref^2=kappa_vac^2 G_Newton(-p_vac) agrees only
when p_vac=-rho_Lambda,ref c_light^2. A diagnostic dynamic chi does not
prove a physical pointwise scale-vacuum completion.

Constant vacuum and the separately FROZEN reference a_ref=a0 E(z),
E(z)^2=.315(1+z)^3+.685, are distinct branch choices. Each fixed positive
reference admits this autonomous conditional argument with its own compatible
background. No uniform result over unbounded z is asserted. If a_ref instead
evolves, alpha_ref=d(log a_ref)/dt produces protocol work

    E_t+(F_E)_x=-T alpha_ref/C.

The spatial momentum identities (9)-(11) still have no explicit spatial
reference source when a_ref depends only on time, but the stationary tuple
need not remain a solution, so (8), (13), (21)-(26) cannot silently be
reused. Such evolving protocols require a separate boundary/work analysis.

The dynamic MOND source is B_x=Cn+tau phi_tt throughout; no Newtonian
missing-mass source replaces it. The acceleration is the Q branch
F_acc=sqrt(B^2+aB), distinct from RAR
F_acc=B/[1-exp(-sqrt(B/a))], registered M and filtered MONO.
This argument supplies no endpoint shock classification, solution past
breakdown, global or full-cone existence, physical metric/photon or
vacuum/two-DOF completion, criterion B, calibrated empirical prediction,
cosmology, historical novelty, or theory closure. It does not close FGF049's
full-cone gradient gate. No literature mechanism or external claim was used.
