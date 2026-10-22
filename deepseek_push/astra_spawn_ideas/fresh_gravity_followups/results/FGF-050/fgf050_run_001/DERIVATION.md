# FGF050: exact two-path source and the remaining trace obstruction

Author: /root/fgf050_author. Bounded proof-only candidate, independent review
pending. Primary actual-family verdict: **incomplete, with the smallest missing
implication identified below**. The exact identities are the scoped result;
the full feedback budgets and endpoint classification are not proved.

## 1. Quantifiers, data, units, and the horizon

Fix C=4 pi G_Newton, tau,sigma,J,S0,c=cs,nref,L,v0,a_ref>0 independently of N.
Here c is sound speed, not light speed. Use physical coordinates throughout.
Let g=phi_x>0, p=phi_t, k=chi_x, w=chi_t, a=a_ref exp(chi), and

    B=(sqrt(a^2+4g^2)-a)/2, W(g,a)=integral_0^g B(s,a) ds,
    T=-W_chi, U_s=S0[cosh(2chi)-1]/4,
    n_t+(nv)_x=0,
    v_t+v v_x+c^2(log(n/nref))_x=-g,
    tau p_t=B_x-Cn, g_t=p_x,
    sigma w_t=J k_x+T-U_s', k_t=w_x, chi_t=w.             (1)

The initial n=rho, g=g0, chi=chi0, p=w=0 form the inherited regular
hydrostatic patch: B(g0,a_ref exp chi0)_x=C rho,
c^2(log rho)_x=-g0, J chi0_xx+T(g0,chi0)-U_s'(chi0)=0.
The unchanged velocity is V f((x-x*)/ell), V=v0 N, ell=L/N^3,
omega=V/ell, f(y)=(1-y^2)^2 on |y|<1 and zero otherwise. It is C1,1;
no smoothing or extra classical second derivative at a join is used.

For clarity the FGF049 constants are repeated, but its conditional Riccati
proof is not rerun. On K0=[x*-R,x*+R], set

    d_f=8/(3 sqrt(3)), h0=max rho^(-1/2), hmin=min rho^(-1/2),
    A=2 d_f h0, b_*=d_f hmin,
    B_*=(h0/A)[exp(8A/b_*)-1], H_*=h0+A B_*,
    eta=min(A/2,b_*/2)/H_*, T_N=B_*/omega,
    Q0=max|log(rho/nref)|, G0=max|g0|,
    S_N=(1+Gamma)V+c Q0+c+tau^(-1/2)+sqrt(J/sigma)+v0,
    K_t=[x*-R+S_N t,x*+R-S_N t].                         (2)

Gamma>0 is fixed; ell<R/2, omega>=G0/(c d_f) and
ell+2 S_N T_N<R are the original large-N gates. b_* is NOT field speed b.
The target is integral_0^T_N sup_Kt(-g_x)_+ dt<=eta omega and
integral_0^T_N sup_Kt|g| dt<=Gamma V.

Every identity below is quantified over any putative positive classical
continuation on a neighborhood of the closed cone through T_N. It does not
assert existence through that time. C1 state variables and C2 potentials
suffice for the characteristic identities. A compact field chart independent
of N, a uniform first-gradient bound, and a full-time fluid-speed bound are
extra gates when explicitly invoked, not consequences of classical existence.
Field paths are automatically backward contained since b<tau^(-1/2)<S_N.
Material paths used below require |v|<S_N or a separately buffered domain.
FGF049 derives that speed gate under its still-unproved force budget.

## 2. Exact transported source representation, including Jacobians

Set b=sqrt(B_g/tau)>0, H(g,chi)=integral_gstar^g b(s,chi) ds, gstar>0 fixed,
and R_+=p+H, R_-=p-H. Write epsilon=+1,-1, and define

    lambda_epsilon=-epsilon b,
    F_epsilon=B_chi k/tau+epsilon H_chi w-b H_chi k,
    D_epsilon=partial_t+lambda_epsilon partial_x,
    D_epsilon R_epsilon=F_epsilon-(C/tau)n.             (3)

All scale dependence remains. In particular F_epsilon is a function of the
field states (g,chi,k,w); its spatial derivative includes their actual
spatial derivatives. No frozen coefficient or hydrostatic source is used.
For each terminal (t,x), let X_epsilon(s;t,x) solve X'=lambda_epsilon(s,X),
X(t;t,x)=x. Its terminal-label Jacobian is

    j_epsilon(s;t,x)=partial_x X_epsilon(s;t,x)
       =exp[-integral_s^t lambda_epsilon,x(u,X(u)) du]>0,
    j_epsilon(t)=1, d_s j_epsilon=lambda_epsilon,x j_epsilon.  (4)

Differentiate the integrated state formula in terminal x. This uses only C1
coefficients/solutions and gives, with every integrand evaluated on its OWN X,

    xi_epsilon(t,x)=E_epsilon(t,x)-(C/tau) I_epsilon(t,x),
    E_epsilon=j_epsilon(0) R_epsilon,0'(X_epsilon(0))
                 +integral_0^t j_epsilon F_epsilon,x(s,X_epsilon) ds,
    I_epsilon=integral_0^t j_epsilon n_x(s,X_epsilon) ds.        (5)

Thus the exact signed physical gradient is

    g_x = [E_+-E_--2 H_chi(t,x) k(t,x)]/[2b(t,x)]
          -(C/[2 tau b(t,x)]) [I_+-I_-].                     (6)

The weights (4) contain field self-interaction; (5) retains initial positions,
initial derivatives and differentiated scale/field sources. The endpoint
scale correction in (6) cannot be omitted. Splitting into E and I is an exact
algebraic accounting along the actual nonlinear solution, not linear
superposition: E, j, b and the paths themselves depend on the coupled source.

Equivalently D_epsilon xi_epsilon=-lambda_epsilon,x xi_epsilon+
F_epsilon,x-(C/tau)n_x. The integrating factor from s to t is exactly j(s),
which independently checks the sign in (4)-(5). Same-point subtraction would
lose these weights and transported arguments.

## 3. Continuity integration by parts on a separated segment

Suppress epsilon and terminal labels temporarily. Put r=v-lambda along X.
On any closed segment [a,d] where r is nonzero, continuity gives

    D_lambda n=-r n_x-n v_x.

Using j'=lambda_x j, ordinary integration by parts yields

    integral_a^d j n_x ds
      =-[j n/r]_a^d
        +integral_a^d j n[(lambda_x-v_x)/r-D_lambda r/r^2] ds
      =-[j n/r]_a^d-integral_a^d j n D_v r/r^2 ds.            (7)

The second equality uses D_v r=D_lambda r+r r_x and r_x=v_x-lambda_x.
Units agree: both sides are density times time/length. Formula (7) is exact
without a lower bound uniform in N, but an estimate of its RHS needs one.
The field's material acceleration is NOT zero:

    D_v lambda=lambda_g(p_x+v g_x)+lambda_chi(w+v k),
    D_v r=-g-c^2 n_x/n-D_v lambda.                          (8)

Consequently (7), with pressure retained, becomes

    integral_a^d j(1-c^2/r^2)n_x ds
      =-[j n/r]_a^d+integral_a^d j n(g+D_v lambda)/r^2 ds.   (9)

This does not solve for the unweighted integral: r varies, and pressure has
returned a weighted n_x integral. A lower bound for |r| alone is insufficient
to bound the original source by density mass. Formally dividing the integrand
by 1-c^2/r^2 would also require control near r=+/-c, i.e. the fluid acoustic
speeds meeting the field speed, and creates new coefficient derivatives.
No such division is made in this proof.

If BOTH paths stay separated from r=0 on the WHOLE interval, the terminal
pieces of I_+-I_- can be combined exactly because j_+(t)=j_-(t)=1:

    -n/(v+b)+n/(v-b)=2b n/(v^2-b^2).                       (10)

Their contribution to (6) is -C n/[tau(v^2-b^2)]. This is adverse when
|v|>b and favorable when |v|<b. Initial traces, the two acceleration
integrals and all E/scale terms are still present; (10) is not a sign theorem
for the total g_x. At v^2=b^2 the separated formula is unavailable.

## 4. An exact global cutoff formula that does not divide at resonance

Fix dimensionless delta>0, and choose a smooth even theta_N(r) taking values
in [0,1], zero for |r|<=delta V, one for |r|>=2 delta V,
|theta_N'|<=Ctheta/(delta V). All quotients with theta_N or theta_N' are
extended by zero near r=0. This is an analytic partition of the identity;
it changes neither equations nor physical coefficients. Set theta=theta_N(r).
Repeating (7) with the weight theta gives

    I_epsilon=J_epsilon+P_epsilon+L_epsilon,
    J_epsilon=-[j theta n/r]_0^t
       +integral_0^t j n[D_lambda theta/r
                         +theta(g+D_v lambda)/r^2] ds,
    P_epsilon=integral_0^t j theta c^2 n_x/r^2 ds,
    L_epsilon=integral_0^t j(1-theta)n_x ds.                 (11)

This is valid across ALL speed resonances. Inserting the difference of (11)
into (6) is the requested exact two-path density-source representation.
D_lambda theta=theta_N'(r)D_lambda r is a transition term supported where
delta V<|r|<2 delta V. It is NOT controlled just because theta has compact
transition support. In fact

    D_lambda r=-g-c^2 n_x/n-D_v lambda-r(v_x-lambda_x),      (12)

so its pressure and compression content is retained explicitly. Combining
those pressure contributions in (11) would yield the exact residual weight
1-theta+c^2(theta/r^2-theta_N'/r) multiplying j n_x; no hidden removal of
n_x is obtained. The uncombined (11) makes the three outstanding terms clear.
The globally smooth cutoff avoids a tacit finite bound on the number of
crossings. Segmentwise use of (7) instead must retain every entry/exit trace.

The high-speed gain in P is only c^2/(delta V)^2=O(N^-2). It multiplies an
unknown signed density-gradient trace; it is not by itself a small result.
The low-speed L term covers the exterior and edges as well as possible later
resonance regions. They cannot be deleted on the grounds that the initial
velocity is positive in the packet interior.

Indeed initially r_+=V f+b0 and r_-=V f-b0, where b0(x)>0 is the actual
background field speed. At both joins v=0. For sufficiently large N the
packet center has v>b0, while the edges have v<b0; continuity therefore
forces at least one r_-=0 crossing on EACH half of the initial packet.
There is no uniform lower bound for |v-lambda_-| even at t=0. Positive r_+
at t=0 gives no full-time gate or O(V) lower bound at the joins. No later
sign or separation is inferred from these initial observations.

## 5. What mass transport actually controls

Assume material paths in the causal footprint reach the initial patch, with
a C1 inverse material label A_m(t,x), A_m(0,x)=x. Its Jacobian is positive.
Continuity is equivalently

    n(t,x)=rho(A_m) partial_x A_m,
    D_lambda A_m=-r n/rho(A_m).

Let M0'(a)=rho(a), with any fixed additive constant. Then

    d_s M0(A_m(s,X(s)))=-r(s,X(s)) n(s,X(s)).               (13)

On an interval of fixed sign r, this proves the exact swept-mass identity

    integral_a^d n |r| ds
      =|M0(A_m(d,X(d)))-M0(A_m(a,X(a)))|.                  (14)

This is useful: on a fully separated fast segment |r|>=delta V and bounded
j, certain undifferentiated density integrals gain inverse powers of V.
But (14) controls an integral along one path, not n at an endpoint, n_x,
or a supremum over distinct terminal x at every t. Summing separated pieces
counts material-label crossings with multiplicity. No bound for that
multiplicity follows from mass conservation when r can change sign.
The transition term in (11) is exactly where that proposed shortcut fails.

There is also a direct two-path mass identity. For s<t, the left path
X_-(s;t,x) lies below the right path X_+(s;t,x), since their backward vector
fields point apart and b>0. With M(s)=integral_Xminus^Xplus n(s,y)dy,

    M'(s)=-r_+(s)n(s,X_+(s))+r_-(s)n(s,X_-(s)),
    integral_0^t [r_+ n_+-r_- n_-] ds=M(0), M(t)=0.        (15)

Reynolds transport and continuity prove (15). It controls a flux difference;
there are no terminal-label Jacobians times n_x in (15). Differentiating it
in terminal x reintroduces density traces and derivatives of r. Positivity
of M does not control its spatial derivative. Equations (13)-(15) therefore
do not supply the missing estimate for (6).

A simple functional obstruction makes the failed implication precise. In a
fixed interior interval choose a nonnegative smooth bump psi with integral
one and define n_epsilon=nbg+m epsilon^(-1)psi((x-xc)/epsilon), nbg,m>0.
Its excess mass is m, yet its peak grows as epsilon^(-1) and its gradient as
epsilon^(-2). Thus no bound for sup n or sup|n_x| in terms of that mass alone
exists. This is ONLY a counterexample to a functional mass-to-trace inequality,
not a solution of (1), not the prescribed initial family, and not a
counterexample to coupled compression. Actual dynamics could enforce a
stronger trace estimate; that is precisely the unresolved implication.

## 6. Full-time accounting, sufficient extra gates, and N dependence

Let Ecal=(E_+-E_--2H_chi k)/(2b). Formula (6) is signed, so the sharp
remaining goal is to control (-Ecal+(C/(2 tau b))(I_+-I_-))_+ in time.
For a transparent SUFFICIENT absolute estimate, suppose b>=bmin>0 throughout
the full cone, with bmin independent of N. Define

    A_E=integral_0^T_N sup_Kt (-Ecal)_+ dt,
    A_Q=integral_0^T_N sup_Kt (|Q_+|+|Q_-|) dt,
           Q=J,P,L as in (11).

Then the proved implication is only

    integral sup(-g_x)_+ <= A_E+[C/(2 tau bmin)](A_J+A_P+A_L). (16)

These explicitly stronger premises suffice: a fixed compact field chart with
|g|<=gmax and b>=bmin, A_E<=eta omega/2, and
A_J+A_P+A_L<=eta tau bmin omega/C. For sufficiently large N,
gmax B_*/omega<=Gamma V also supplies the force impulse. The chart and trace
premises have NOT been obtained from the actual data on this full horizon.
They are named quantitative gates, not conclusions or a replacement theorem.
The signed difference in (6) might need less than these absolute gates.

To see exactly what the fast-region improvement buys, also assume j<=jmax
uniformly on all paths. Put Mx(s)=sup_Ks |n_x(s,.)|. Backward containment gives

    A_P <= [2 jmax c^2/(delta^2 V^2)]
               integral_0^T_N (T_N-s) Mx(s) ds.            (17)

It improves the plain gradient bound by O(N^-2), but the integral on the RHS
has no supplied full-time bound. To make (17) o(omega) one sufficient input
is integral (T_N-s)Mx(s)ds=o(omega V^2)=o(N^6), in fixed physical units.
Neither classical finiteness for each N nor mass yields this N-uniform gate.
For the fully fast paired terminal term (10), a bound instead requires
integral sup n/(v^2-b^2), whose crude fast estimate is O(V^-2) integral sup n.
Again a sufficient scale is integral sup n=o(omega V^2); mass does not give it.
Endpoint estimates taken separately lose the additional paired O(1/V) gain.

A_J additionally retains initial j rho/r, transition D_lambda theta, actual
D_v lambda and their transport weights. Bounding j itself requires the
integrated lambda_x along field paths; bounded field states alone do not
bound these Jacobians. A_L has no fast-speed gain. The FGF048 bound for Mx,
the chart and gradients holds only through kappa/omega; it is not extended.
The exponential-in-N density amplitude allowed by fluid invariant bounds
under force impulse is not offset by O(N^-2) or T_N=O(N^-4). Those loose
bounds demonstrate an estimate failure, not actual exponential growth.

The narrowed next implication is a signed two-path estimate controlling
(11), especially its low-speed/transition density trace and pressure remainder,
with quantitative chart/Jacobian control on the full B_*/omega cone. A proof
of a uniform fast-core speed alone would leave A_L, crossing traces and the
field/scale terms unresolved. No repeated unmodified sweep is proposed.

## 7. Controls, energy, and scope

Zero velocity control: the exact hydrostatic tuple with p=w=v=0 is stationary
and satisfies all of (1). Then lambda_epsilon R_epsilon,0'=F_epsilon-(C/tau)rho;
differentiating its integrated characteristic formula gives (5) exactly and
(6) returns g0_x. In (7), r=-lambda and D_v r=partial_t r=0, so
integral j rho_x=-[j rho/r], providing an independent endpoint-sign check.
For the cutoff identity, D_lambda theta terms account for spatial variation
of b and of theta. No spurious zero-source or zero-scale assertion is made.

Favorable-gradient limiting check: if g_x>=0 on a candidate cone, its adverse
budget is exactly zero. The physical pressure-retaining fluid identities,
with h=n^(-1/2), y=h(v+c log(n/nref))_x and D_+=partial_t+(v+c)partial_x,
include D_+ y=-y^2/(2h)-h g_x. Thus positive g_x helps compression and is
correctly uncharged; no conclusion about its actual sign is inferred.
At t=0, I_+=I_-=0 and (6) reduces to the chain-rule identity for g0_x.

For fixed reference, keep the complete energy and both field fluxes:

    e=c^2 n[log(n/nref)-1],
    E=nv^2/2+e+n phi+[tau p^2/2+W+sigma w^2/2+J k^2/2+U_s]/C,
    F=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Jwk)/C,
    E_t+F_x=0.

Matter/interaction exchange is +np; Q exchange is -np-Tw/C because
W_t=Bp_x-Tw; scale exchange is +Tw/C. For moving endpoints alpha,beta,
d/dt integral_alpha^beta E=F(alpha)-F(beta)+beta'E(beta)-alpha'E(alpha).
On K_t the boundary term is -S_N[E(beta)+E(alpha)]. The initial excess energy
is exactly integral rho v^2/2=O(V^2 ell)=O(N^-1); it does not bound n_x,
g_x, or the trace/Jacobian gates. No positive conserved cone norm is claimed.

Treat a_ref=9.3619e-11 and 1.1279e-10 m/s^2 separately, with their own
compatible backgrounds, B_*,eta and other fixed constants. The adopted
vacuum relation a_ref=kappa_vac c_light sqrt(G_Newton rho_Lambda,ref) is not
newly derived. The pressure form a_ref^2=kappa_vac^2 G_Newton(-p_vac)
equals that vacuum relation only when p_vac=-rho_Lambda,ref c_light^2;
p_vac is unrelated to the field variable p=phi_t. Constant vacuum and individually frozen a_ref=a0 E(z),
E(z)^2=.315(1+z)^3+.685, are distinct histories; each fixed choice fits (1).
If a_ref evolves, let alpha_ref=d(log a_ref)/dt. The same written field
potential contributes explicit protocol work -T alpha_ref/C to E_t+F_x
(and any additional externally varied coefficients would have their own work).
Equations (3)-(11) here concern fixed reference; an evolving-reference chart
also acquires H's explicit-time terms and is not silently covered.

The actual MOND source B_x=Cn+tau phi_tt is retained, with no replacement by
Newtonian missing mass and no N-dependent physical retuning. Q: F=sqrt(B^2+aB)
is distinct from RAR: F=B/[1-exp(-sqrt(B/a))], registered M and filtered MONO.
No identity here establishes a physical vacuum completion, metric/photon or
two-gravitational-DOF completion, criterion B, calibrated clusters, cosmology,
historical novelty or theory closure. Failure to close (16) is not a
counterexample to compression, and conditional budgets would still not
classify the actual maximal endpoint without separate continuation gates.
