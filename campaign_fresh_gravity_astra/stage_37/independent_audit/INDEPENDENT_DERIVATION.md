# FGF050 independent pre-exposure derivation

Reviewer: /root/fgf050_reviewer. No new FGF050 author, coordinator or other
reviewer proof or preview has been read. All task and nine ancestry pins were
verified before ancestry contents were used. This record is frozen before
receiving the new author's pins. Zero mathematical executable computations.

Normalized target: for the exact FGF049 data and equations, estimate on every
putative positive classical continuation covering the full cone to T=B*/omega
both integral sup(-g_x)_+ <= eta omega and integral sup|g| <= Gamma V.
Primary verdict for that actual-family target: **incomplete, with the smallest
missing implication** identified below. The transport identities are exact;
the conditional trace estimates they suggest are not proved for this family.

## 1. Data, units, coefficients, domain

Use physical units and fixed positive C=4pi G_Newton, tau,sigma,J,S0,c,nref,
a_ref, where c is sound speed. Set g=phi_x, p=phi_t, k=chi_x, w=chi_t,
a=a_ref exp chi, B=(sqrt(a^2+4g^2)-a)/2 on g>0,
W(g,a)=integral_0^g B(s,a) ds, Tscale=-W_chi,
U_s=S0(cosh(2chi)-1)/4. The equations are

    n_t+(nv)_x=0,
    D_v v=-c^2(log(n/nref))_x-g,
    tau p_t=B_x-Cn,   g_t=p_x,
    sigma w_t=J k_x+Tscale-U_s',   k_t=w_x, chi_t=w.

The initial n=rho, g=g0, chi=chi0, p=w=0 are the compatible smooth
hydrostatic patch: B(g0,a0)_x=C rho, c^2(log rho)_x=-g0,
J chi0_xx+Tscale(g0,a0)-U_s'(chi0)=0. Only velocity is perturbed:

    v(0,x)=V f((x-x*)/ell), V=v0 N, ell=L/N^3,
    f(y)=(1-y^2)^2 for |y|<1, zero otherwise,
    omega=V/ell=v0 N^4/L.

No smoothing of the C1,1 joins or physical retuning with N occurs. On a
putative classical slab all displayed path identities require only C1 state
variables and smooth coefficients on g>0. Flow-label differentiation justifies
the derivative-source formula without requiring classical second derivatives
of v at the joins.

Retain the explicit FGF049 constants: d_f=8/(3sqrt(3)),
h0=max_K0 rho^(-1/2), hmin=min_K0 rho^(-1/2), A=2 d_f h0,
bstar=d_f hmin, B*=(h0/A)(exp(8A/bstar)-1),
H*=h0+A B*, eta=min(A/2,bstar/2)/H*. For fixed Gamma>0,
S_N=(1+Gamma)V+c max_K0|log(rho/nref)|+c+tau^(-1/2)
+sqrt(J/sigma)+v0, K_t=[x*-R+S_N t,x*+R-S_N t].
Take the FGF049 large-N gates omega>=max|g0|/(c d_f) and
ell+2 S_N T<R, T=B*/omega. Field speeds alone are bounded by
max(tau^(-1/2),sqrt(J/sigma))<S_N; their backward paths stay in this cone
without using the unproved force impulse. Material path containment uses a
separate speed gate (FGF049 derives one conditional on that impulse).
An N-uniform compact chart is not assumed to follow from positive g alone.

## 2. Exact differentiated field paths and signed decomposition

Let b=sqrt(B_g/tau)>0, d=sqrt(J/sigma),
H(g,chi)=integral_{g_*}^g b(s,chi) ds for fixed positive g_*.
Use epsilon in {+1,-1}, R_epsilon=p+epsilon H,
lambda_epsilon=-epsilon b and D_epsilon=partial_t+lambda_epsilon partial_x.
Then, with c0=C/tau,

    D_epsilon R_epsilon=S_epsilon-c0 n,
    S_epsilon=B_chi k/tau+epsilon H_chi w-b H_chi k.       (2.1)

Here S includes full dynamical scale fields. They obey
D_{-d}(w+d k)=D_{+d}(w-d k)=(Tscale-U_s')/sigma, chi_t=w.
In particular no scale force or B_chi term has been set to zero.
Let X_epsilon(s;t,x) solve X'=lambda_epsilon(s,X), X(t)=x. Put

    A_epsilon(s;t,x)=exp(-integral_s^t lambda_epsilon,x(u,X(u)) du),
    I_epsilon(t,x)=integral_0^t A_epsilon(s;t,x)n_x(s,X(s)) ds.

Along each fixed path A'=lambda_x A and A(t)=1. The exact formula is

    xi_epsilon(t,x)=A_epsilon(0) xi_epsilon(0,X_epsilon(0))
           + integral_0^t A_epsilon S_epsilon,x(s,X_epsilon(s)) ds
           - c0 I_epsilon(t,x), xi_epsilon=R_epsilon,x.    (2.2)

This follows either from D_epsilon xi=-lambda_x xi+S_x-c0 n_x,
or by differentiating the integrated R equation in its flow label and
then dividing by the positive flow Jacobian. The latter proof uses only C1
coefficients/sources. S_x is the total derivative, including coefficient
variation in g and chi and k_x,w_x. lambda_x is also the full derivative.
Initial xi_plus=H(g0,chi0)_x and xi_minus=-H(g0,chi0)_x are evaluated at
DIFFERENT feet. Define Hfield as their weighted difference plus the difference
of the two S_x integrals, minus 2 H_chi(t,x)k(t,x). Then exactly

    g_x=[Hfield-c0(I_plus-I_minus)]/(2b).                 (2.3)

The adverse part is [c0(I_plus-I_minus)-Hfield]_+/(2b). This expression
fixes the sign that any feedback estimate must control. It is not the sum
of separate absolute norms, though such a sum supplies a sufficient bound.
No same-point density cancellation has been made. These weights are evaluated
on the actual solution: this is a source decomposition, not a linear
superposition theorem for independent coupled solutions.

## 3. Continuity integration by parts, with every endpoint

On a segment [a,z] of a field path write u=v-lambda (relative velocity),
Dlambda=partial_t+lambda partial_x. Exact continuity gives

    Dlambda n=-u n_x-n v_x.                              (3.1)

When u does not vanish on that CLOSED segment, integration by parts yields

    integral_a^z A n_x ds
      =-[A n/u]_a^z
       +integral_a^z A n[(lambda_x-v_x)/u-Dlambda u/u^2] ds
      =-[A n/u]_a^z-integral_a^z A n D_v u/u^2 ds.         (3.2)

The last equality uses u_x=v_x-lambda_x and D_v=Dlambda+u partial_x.
No Jacobian has been discarded. For the whole nonresonant path, its upper
endpoint is -n(t,x)/u(t,x), and its lower endpoint is
+A(0)rho(X(0))/u(0,X(0)); they do not vanish by conservation of mass.
Every internal subdivision creates its own signed interface traces. One may
only cancel adjacent terms if the same smooth quotient exists on both sides.

The full fluid equation makes explicit a further obstruction:

    D_v u=-c^2 n_x/n-g-D_v lambda,
    integral A n_x =-[A n/u]+integral A[c^2 n_x+n(g+D_v lambda)]/u^2.
                                                               (3.3)

Thus a pressure term proportional to n_x reappears. Pointwise equivalently,

    (u^2-c^2)n_x=-u Dlambda n-n Dlambda u+n(g+D_v lambda). (3.4)

Division by u^2-c^2 requires another gate and introduces acoustic resonance
u=+/-c. Pressure cannot be silently treated as a small fixed coefficient or
removed. D_v lambda also contains actual field/scale gradients. This identity
is not an n_x-free estimate from mass alone.

A globally valid way to keep resonance is a smooth cutoff theta_delta(u),
zero for |u|<=delta and one for |u|>=2delta, with 0<=theta<=1. Extend theta/u
smoothly by zero near u=0. For each whole field path exactly

    I = integral A(1-theta)n_x ds -[A theta n/u]_0^t
        +integral A n[(Dlambda theta)/u-theta D_v u/u^2] ds. (3.5)

The derivative Dlambda theta=theta_delta'(u)Dlambda u is supported in the
transition delta<|u|<2delta and is retained. Formula (3.5) is valid for any
number of speed crossings, without assuming finitely many resonance
components or erasing interface traces. delta is a diagnostic cutoff, not
an N-dependent physical coupling. An estimate must control the residual
resonant integral, cutoff transition integral, two endpoint traces, and the
D_v u integral for BOTH paths, as well as Hfield and b.

## 4. What mass transport gives and what it does not

On a simply connected classical patch continuity permits a local mass
potential m_x=n, m_t=-nv (an additive function of time fixes the gauge).
Then Dlambda m=-(v-lambda)n=-un. If u has a fixed sign along a segment and
|u|>=delta, it follows that

    integral_a^z n(s,X(s)) ds <= |m(z,X(z))-m(a,X(a))|/delta. (4.1)

A finite material tube mass can bound this mass-coordinate difference if the
path lies in that tube. The tube, its containment and its mass must actually
be supplied. For changing relative sign one needs the total variation of m
along the path, not only its range. Recrossings can repeat the same mass.
For a spatial interval [alpha(t),beta(t)] the exact mass law is

    d/dt integral_alpha^beta n dx
       =n(alpha)(v(alpha)-alpha')-n(beta)(v(beta)-beta').   (4.2)

The shrinking K_t mass is not automatically conserved. Even a proved bound
on its mass or on (4.1) does not control endpoint n/u or n_x traces.

This is a real failure of the proposed general mass-only inequality, not
merely an absent proof. In a separate CONTINUITY-ONLY test, take constants
U>b>0 and n_epsilon(t,x)=nbar+(M/epsilon)psi((x-Ut)/epsilon), v=U,
where psi is nonnegative smooth compactly supported with integral one and
psi(0)>0. Relative speeds U+b and U-b are uniformly separated from zero;
the excess mass is exactly M and continuity holds. For constant field paths
lambda_plus=-b, lambda_minus=b and A=1, direct integration gives

    I_plus=[n_epsilon(0,x+bt)-n_epsilon(t,x)]/(U+b),
    I_minus=[n_epsilon(0,x-bt)-n_epsilon(t,x)]/(U-b).      (4.3)

At x=Ut and any fixed positive time away from zero, the two initial bumps
miss the feet for sufficiently small epsilon. Therefore

    I_plus-I_minus=2b M psi(0)/[(U^2-b^2)epsilon]>0.     (4.4)

On a time interval whose interior cone contains this moving peak,
integral sup (I_plus-I_minus)_+ grows like 1/epsilon although mass and
separation are fixed. It has precisely the adverse density-source sign in
(2.3). A finite regular spatial domain suffices; nbar adds finite background
mass there. This family does NOT satisfy the fluid momentum/Q/scale equations,
or the specified FGF049 initial rho. It refutes only a proposed estimate
using continuity, mass and separation alone. It is NOT a counterexample to
coupled compression, nor a frozen-coefficient replacement for the actual
proof. No inference about actual N-growth follows from this independent
inequality test.

For an N-dependent accounting of an attempted sufficient estimate, if both
paths were wholly nonresonant with |u|>=delta_N, A<=J_N, n<=D_N and
|D_v u|<=L_N, (3.2) would give, on each path,

    |I| <= (1+J_N)D_N/delta_N+J_N D_N L_N T/delta_N^2.

Thus the source contribution to the time-integrated absolute gradient is
at most a constant times

    (C/(tau b_min)) [T(1+J_N)D_N/delta_N
                          +J_N D_N L_N T^2/delta_N^2].  (4.5)

T=B*L/(v0 N^4). Even a hypothetical high-speed delta_N~N only makes these
terms O((1+J_N)D_N N^-5+J_N D_N L_N N^-10), in fixed units and fixed
coefficients. There is no supplied full-time bound for D_N,J_N,L_N; the
actual whole-cone delta_N~N premise is false already initially. A bound
O(omega) would still require its coefficient to be at most eta. Formula
(4.5) is preserved as a failed sufficient route, not an asserted growth law.

## 5. Actual resonance, initial edges and exact sufficient gates

At t=0, v is zero at both packet edges, while b0 is positive and bounded on
the compact patch. Hence no |v-lambda|>=constant*V estimate holds on the
whole packet for either field branch. For lambda_minus=+b, v-b0 is negative
at both edges and positive at the center for all sufficiently large N.
By continuity it has at least one zero in EACH half-packet. Using fixed
positive upper/lower bounds on b0, f(y)=b0/V puts those zeros within
1-|y| comparable to V^-1/2 of the edges, i.e. physical distances comparable
to ell V^-1/2=O(N^-7/2). This is an initial-location observation, not a
bound on their future motion, number, widths, or traces. On lambda_plus=-b,
v+b0>=b_min initially, but this is only order one at the edges and positivity
of initial v proves no full-time gate for v+b. On any fixed interior region
where f>=m>0 the initial relative speeds are order V, which alone gives no
future density, acceleration, or crossing bound.

For clarity an exact sufficient quantitative package is as follows. On the
full candidate cone assume b>=b_min>0, sup|g|<=G_N, and set
H_N(t)=sup_Kt |Hfield|. From (3.5) define for each family and each endpoint
(t,x) E_epsilon(t,x) as the sum of the absolute values of its resonant
integral, its two endpoint traces, and the absolute-integral bounds for
its cutoff-transition and D_v u terms. Then |I_epsilon|<=E_epsilon.
It suffices that

    T G_N<=Gamma V,
    (1/(2b_min)) integral_0^T [H_N(t)
                 +(C/tau) sup_Kt(E_plus+E_minus)] dt <= eta omega. (5.1)

These premises are explicit and non-circular as a CONDITIONAL identity-to-
budget implication: they concern named traces and field-state quantities,
not the desired g_x budget itself. They are not asserted to hold, are
stronger than necessary because they discard cancellations, and are not
an actual-family proof. Obtaining them from initial data without assuming
later gradient/density control is the missing step. The weights themselves
involve lambda_x, so bounding J_N by an already-assumed field gradient
estimate would merely move, and could circularly restate, the gap.

A signed estimate for c0(I_plus-I_minus)-Hfield could succeed even if (5.1)
fails; absolute norm failure is not proof that the target signed bound fails.
FGF048 covers only kappa/omega. Its estimates cannot be substituted through
B*/omega, however small their early budget consumption. No Riccati proof is
being recycled as new feedback evidence.

## 6. Controls, energy and scope

For v=0 the exact hydrostatic tuple stays stationary with p=w=0. In (2.1)
S_epsilon-c0 rho=lambda_epsilon R_epsilon,x; in (2.2) the propagated
initial gradient and all source integrals reconstruct the stationary values.
The density term by itself need not vanish: cancellation with field/scale
and transported initial terms is essential. In (3.2), u=-lambda and D_v u
vanishes for stationary fields, so I=-[A rho/u]; indeed A/lambda is constant
along a stationary lambda path because A'=lambda_x A and
lambda'=lambda lambda_x. This checks both signs and variable coefficients.

For a favorable-force sign check, the exact pressure-retaining weighted
fluid gradients y=n^-1/2(v+c log(n/nref))_x and z=n^-1/2(v-c log(n/nref))_x
obey D_{v+c}y=-y^2/(2h)-h g_x and D_{v-c}z=-z^2/(2h)-h g_x, h=n^-1/2.
When g_x>=0 the force reinforces compression; the adverse budget is zero.
The sign in (2.3) agrees: positive I_plus-I_minus alone contributes negative
g_x, but Hfield can reverse the total. This is an exact sign/limiting control,
not the old conditional upper-lifespan theorem.

The complete fixed-reference energy and flux remain

    e=c^2 n(log(n/nref)-1),
    E=nv^2/2+e+n phi+[tau p^2/2+W+sigma w^2/2+J k^2/2+U_s]/C,
    F=nv[v^2/2+c^2 log(n/nref)+phi]-(p B+J w k)/C.

Direct exchanges cancel: matter +np, Q -np-Tscale w/C, scale +Tscale w/C.
Hence E_t+F_x=0 and for moving alpha,beta the exact integral derivative is
F(alpha)-F(beta)+beta'E(beta)-alpha'E(alpha). For K_t the last term is
-S_N(E(beta)+E(alpha)). Both field fluxes are retained. Initial excess
integral rho v^2/2 is O(N^-1), but is not a norm of n_x or g_x and supplies
neither endpoint traces nor chart margins.

All results apply separately to a_ref=9.3619e-11 and 1.1279e-10 m/s^2, each
with its own compatible background and constants. The adopted relation is
a_ref=kappa_vac c_light sqrt(G_Newton rho_Lambda,ref); kappa_vac is not
newly derived. Constant-vacuum histories and separately frozen comparisons
a_ref=a0 E(z), E^2=.315(1+z)^3+.685, are distinct from evolving references,
which require protocol work and are outside the fixed-reference energy law.
Q is distinct from RAR, registered M and filtered MONO. MOND source scaling
is preserved. No physical vacuum, metric/photon/two-DOF completion, criterion
B, calibrated clusters, cosmology, historical novelty or theory closure follows.

## 7. Dependency and obligation record

Dependencies: verified FGF049 supplies the exact domain/budget target; verified
FGF047/048 ancestry supplies only the existing local branch and shorter-time
facts. Equations (2.1)-(3.5), mass law (4.1)-(4.2), generic failed-inequality
example (4.3)-(4.4), and conditional estimate (5.1) are analytic derivations
here. No external theorem or computational experiment is a leaf.

Passed: field path signs; Jacobian weights; initial and terminal terms;
cutoff resonance terms; full scale coefficients; exact C1,1 compatibility;
pressure retained; stationary/favorable-sign controls; moving mass/energy
boundaries; fixed coefficients and both normalization/history distinctions.
Failed: universal mass-plus-separation control of the density-source trace,
with failure strictly scoped to the continuity-only class. Not established:
actual-family full-time trace/cutoff/weight bounds and compact-state gates.
Out of scope: endpoint classification and physical completion.

Strongest safe result: exact two-path representation plus an explicit
continuity integration-by-parts identity and a genuine obstruction to the
mass-only inference. Cheapest discriminating next check: derive a coupled,
signed bound for the resonant residual and endpoint/acceleration terms in
(3.5), with chart/weight bounds, or prove why a particular proposed such bound
fails for the actual data. No unmodified parameter sweep is warranted.

Self-proofreading coverage: this entire record; no LaTeX build needed for
Markdown formulas, no mathematical-token corrections after freeze. Hashes
and JSON validation are administrative checks, not mathematical experiments.
