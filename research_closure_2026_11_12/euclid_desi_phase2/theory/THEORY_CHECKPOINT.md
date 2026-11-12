# Density portal: principal mixing obstruction and a slow-tail counterexample

Owner: test_feasibility. Parent base: 8db464d4bc. Source bytes: inputs.json.
Status: new analytic checkpoint; no observational fit or all-gate health pass.
Finite symbolic/matrix corroboration completed in run_003; see RESULT.md.
This does not close the full parent-action health gates.

## Contract

Find an explicit changed action that keeps a0^2 proportional to cosmological
dark-energy density without repeating CT7/CT14's scalar/khronon instability.
A sufficient principal-symbol result on a declared background class is partial
progress. It is not a complete cosmology, a local-gravity pass, a derivation of
kappa, or a global hyperbolicity theorem on every field configuration.

Conventions: c=1, signature (-,+,+,+), K=4*pi*G, xi=kappa^2>0,
epsilon=xi/(8*pi). X=-g^{mu nu}partial_mu phi partial_nu phi/2.
E=X+V(phi)>0 is canonical scalar rest-frame energy. It equals the homogeneous
FRW density, but not T_nn for arbitrary spatial gradients in another foliation.
Let n be the unit normal of an independent khronon tau, A_mu=n^nu nabla_nu n_mu,
g=sqrt(A_mu A^mu), a^2=xi*G*E, and x=g/a.

## 1. Existing failures retained, not rediscovered as successes

CT7's potential-only portal a^2=xi G V is locally quiet but does not exactly
track E when the canonical equation of state evolves. Its T_nn portal adds
spatial-gradient energy with the wrong sign and fails scalar gradient health.

The tempting replacement a^2=xi G(X+V) already exists as CT10's C''. CT14-H2
shows why its scalar-only health was misleading: delta g contains
grad(delta Phi-delta sigma_dot), so the scale/acceleration mixing enters the
physical kinetic matrix. For simple mu=x/(1+x), the fixed-polarization Schur
coefficient is

    K_lock=1+epsilon*[h(x)-(1+w)*x^3/(2*(1+x))],
    h=x+x/(1+x)-2 log(1+x).

It becomes negative. Treating delta g as a static constraint changes the sign
of the missing term and repeats CT13's incorrect pass. The time-only portal
E=V+(n.partial phi)^2/2 has the same temporal Hessian and the same mixing on an
aligned homogeneous scalar background; merely deleting the spatial energy
does not remove this particular kinetic failure.

A separate-foliation cuscuton construction already exists as AZC1, with full
constraint health open. It is not claimed as a newly constructed alternative.

## 2. Specified parent action and the general mixing diagnostic

Consider the same Einstein/khronon/scalar architecture with a changed J sector:

    S = integral sqrt(-g) [R/(16*pi*G) + a^2 f(g/a)/K
                          + K_BS(Q_tau)/(2*K) + X-V(phi)]
        - gamma_L/2 integral sqrt(-g) [max(D.P,0)]^2 + S_m[g,matter].

For precision, the P/stiffness expression uses the first-order Legendre
representation of a^2 f/K, not a second copy of that interaction:

    L_J = [P.A-a^2 w(p/a)]/K,  n.P=0,
    p=a f'(x),  w(r)=r*x(r)-f(x(r)),  r=p/a.

The constraint n.P=0 is imposed with a multiplier. The independent normal is
unchanged. K_BS and the sign switch are inherited operators, not a proof that
their global dynamics or caustics are healthy. A concrete V is
V0 exp(-lambda phi/Mpl), V0>0, lambda=1; V0 and the initial condition are inputs.

The static weak-field total Lagrangian is -g^2/(2K)+a^2 f(g/a)/K, giving

    mu(x)=1-f'(x)/x.

Write p(x)=f'(x), d(x)=f''(x), h=2f-xp. On an aligned rolling scalar background,
q=n.partial phi, q^2/E=eta, 0<=eta<=2. On homogeneous FRW only,
eta=1+w for the bare canonical scalar. A local background must satisfy the
eta bound separately; the cosmological value cannot be imposed without solving
its local field equations. Direct differentiation and Legendre
transformation give

    G_phi=1+epsilon*h,
    K_free=1+epsilon*[h-eta*x*h'/2],
    K_lock=K_free-q^2 L_gE^2/L_gg
          =1+epsilon*[h-eta*(p^2/d-x*p)/2].

K_lock is the coefficient at fixed polarization, not a claim obtained by
eliminating the khronon velocity. It is exactly the CT14-sensitive coefficient.

## 3. Why a bounded-charge exponential tail is not a cure

For mu=1-exp(-x),

    f=1-(1+x) exp(-x), p=x exp(-x), d=(1-x) exp(-x).

The charge h=2-(x^2+2x+2)exp(-x) is bounded, but d<0 for x>1.
The clock kinetic curvature therefore changes sign before one can claim a
healthy energy-portal mixing matrix. In the unscreened mu_K=gamma_L=0 PN parent,
eliminating the lapse gives clock kinetic coefficient d/(1-d), which is
negative there. A finite stiffness operator changes the finite-k denominator;
it cannot be ignored or inherited as an automatic repair. Thus this is a
scoped obstruction to the rapid-tail unscreened parent, not a no-go for every
possible extra operator or screened background.

More generally, if mu~x at small x, then p=x(1-mu)>0 somewhere. If p tends to
zero at high x, the mean-value theorem forces p'=d<0 somewhere. Hence a
polarization tail returning to zero is incompatible with nonnegative clock
curvature throughout this unscreened parent class. Convexity plus the Newtonian
limit mu->1 also prevents h being uniformly bounded: h=-x^3 d(f/x^2)/dx and
f/x^2->0 would make bounded h imply bounded f, contradicting positive convex
growth. This does not exclude slower Newtonian tails or changed parent operators.

## 4. Explicit slow-tail kernel and an all-x sufficient condition

Take

    mu_*(x)=1-1/sqrt(1+2x),
    u=sqrt(1+2x),
    f_*(x)=(u^3-3u+2)/6,
    p=x/sqrt(1+2x),
    d=(1+x)/(1+2x)^(3/2)>0,
    h=(u-1)^3*(u+3)/(12u)>=0,
    p^2/d-x*p=x^3/[(1+x)sqrt(1+2x)] = D(x)>0.

It retains mu~x and thus the same leading deep-BTFR coefficient. It is a changed
interpolation choice for this candidate; simple-mu or quadratic-law empirical
passes cannot transfer to it. Its Legendre inverse is explicit:
x(r)=r^2+r sqrt(1+r^2), so the first-order action above is well-defined globally
for p>=0.

The exact ratio controlling K_lock is

    2h/D = (2/3)*(u+3)*(u^2+1)/(u+1)^3
         = (2/3)*[1-2*(u-1)/(u+1)^3].

For u>=1, (u-1)/(u+1)^3 has its maximum 1/27 at u=2. Therefore

    2h/D >= 50/81,
    0<=eta=1+w<=50/81  ==> K_lock>=1 for every x>=0.

This covers w in [-1,-31/81], including ordinary late quintessence with
w=-0.9 or the scalar-dominated lambda=1 exponential attractor w=-2/3. It is
not a bound for every canonical equation of state or every spacelike/misaligned
scalar gradient. For eta=2/3 the same expression eventually becomes negative
at sufficiently large x; for larger kinetic fractions failure remains possible.

## 5. Coupled all-angle kinetic matrix in the truncated principal limit

This retains the khronon velocity. Work in the same frozen static PN principal
reduction as CT14, with a=K=1, wavevector k*n_hat, g along e_z, and aligned
timelike scalar. Let zeta=k delta sigma. Eliminate the nonpropagating lapse and
polarization only after building the quadratic action. The polarization Hessian
is H=diag(H_T,H_T,H_L),

    H_T=x/p=sqrt(1+2x)>1,
    H_L=1/d=(1+2x)^(3/2)/(1+x)>1

for x>0. The active stiffness gives D=H+gamma*k^2*n_hat*n_hat^T, gamma>=0.
The constraint block, up to a harmless Fourier phase rotation, is

    C = [[-k^2, k*n_hat^T], [k*n_hat, -D]].

With Q=n_hat^T D^-1 n_hat, 0<Q<1, so C is negative definite. If B is the
constraint/velocity coupling matrix for (delta phi_dot,zeta_dot), the reduced
physical kinetic matrix is

    K_red=diag(K_lock,0)-B^dagger C^-1 B.

The polarization/scalar entry of B includes -W_pE*q*e_z, and its clock column
is (0,-n_hat). Retaining the canonical lapse/phi_dot coupling changes B, not
the negative-definiteness argument. Thus K_lock>0 suffices for a positive
definite K_red at every finite x>0, k>0 and propagation angle within this
truncated frozen leading-derivative PN block. Finite-k terms omitted from C,
including q^2 lapse^2, potential derivatives, finite mu_K, and remaining
metric/shift constraints can alter the full finite-wavelength system. This is not
the erroneous scalar-only/quasi-static-clock reduction.

For the leading block without the additional lapse/scalar entry, put
b=W_pE*q*e_z, B0=n_hat^T D^-1 b, C0=b^T D^-1 b. Then

    K_red = [[K_lock+C0+B0^2/(1-Q), B0/(1-Q)],
             [B0/(1-Q), Q/(1-Q)]],
    det K_red=[Q*(K_lock+C0)-B0^2]/(1-Q)>0,

by Cauchy-Schwarz Q*C0>=B0^2. This is an explicit coupled matrix, not just a
single positive diagonal entry. Finite mu_K terms, curvature/time evolution,
background mass terms and tensor constraints are outside this principal claim.

The leading spatial/mass matrix is U=diag(G_phi*k^2,rho_tau) in these variables.
For rho_tau>0 it is positive and the frozen conservative principal system has
no growing roots. This is positivity, not metric-cone causality: at gamma=0
and propagation parallel to g, c_fast^2=G_phi/K_lock. For the slow-tail kernel
as x tends to infinity this approaches 2/(2-3*eta)>1 whenever eta>0. The
preferred-foliation causality/strong-coupling gates are therefore still open. At rho_tau=0 the clock zero mode is degenerate. At rho_tau<0,
positive stiffness gives the inherited UV sign failure; switching it off leaves
a negative finite-rate branch, not a universal stability pass. At gamma=0 the
large-k roots have one positive O(k^2) branch and a slow root tending to
rho_tau/K_zeta_zeta. All growth rates and sign-interface behaviour must be
recomputed for this new kernel. x=0 is the separate homogeneous limit, not a
uniform lower kinetic bound obtained by setting x=0 in the above inverse.

## 6. Cosmological tracking, local constancy and the price paid

At g=0, f=x^2/2-x^3/3+..., so scale dependence first enters cubically in the
acceleration perturbation. The homogeneous interaction vanishes. The scalar
therefore remains canonical quintessence on exact FRW, with

    rho_DE=X+V, a^2=xi G rho_DE

exactly on that homogeneous branch. This does not allow phantom crossing,
derive xi, determine cold abundance, or fix the known v3s cosmic growth issues.

The new tail has 1-mu~1/sqrt(2x), hence an unscreened point-source branch has
delta g~sqrt(a*g_N/2). At the Sun's 1-AU acceleration this is approximately
5e-7 m/s^2 rather than the old simple-mu correction of order 1e-10. This is a
severe local-gravity obligation, not a phenomenological success. The physical
acceleration and khronon acceleration are distinct in a screened solution;
therefore neither this unscreened estimate nor the old v3s Solar-System pass
settles the new screened action. Its backgrounds and local precision tests
must be solved again.

Local a constancy is also not inherited. The scalar response coefficient is
G_phi>=1, but h grows as x^(3/2), faster than CT7's h~x. A point-source,
quasi-static scalar response and a full metric/clock background are the next
needed checks. No local-constancy pass is claimed at this checkpoint.

## First unresolved implication and continuation

The original target remains open. The substantive new result is a changed
kernel with a provable all-x/all-angle PN kinetic-positivity condition on a
declared timelike accelerating-background class, plus the rapid-tail clock
obstruction. The first uncertainty is whether a solved screened galaxy/Solar
background for this new kernel remains in that class while preserving an
acceptable force law and a nearly constant scale. Strong-field, nonparallel
gradients, finite-wavelength constraint poles and cosmological matter modes
remain separate obligations. The finite matrix audit corroborates this
algebra; it cannot promote this to an all-gate theory pass.


## 7. Conditional power-tail / rolling-fraction tradeoff

Assume derivative asymptotics f~c*x^n, f'~cn*x^(n-1),
f''~cn(n-1)*x^(n-2), c>0 and 1<n<2. Then

    h~(2-n)*f,
    D=p^2/d-x*p~[n*(2-n)/(n-1)]*f,
    K_lock~1+epsilon*(2-n)*f*[1-eta*n/(2*(n-1))].

Thus eta>2*(n-1)/n eventually gives a negative K_lock; a positive asymptotic
coefficient requires eta<2*(n-1)/n. At equality the subleading terms matter,
so the non-strict inequality is only necessary, not a sufficiency theorem.
Writing 1-mu~x^(-alpha), with the corresponding differentiated asymptotics,
n=2-alpha gives eta<=2*(1-alpha)/(2-alpha). The simple 1/x tail is a limiting
case, not covered by n>1, and its logarithmic subleading terms produce the
separate CT14 failure. For alpha=1/2 the asymptotic threshold is 2/3; the exact
uniform sufficient bound proved above is 50/81. The +1 in K_lock also means
50/81 is not asserted to be the sharp positivity boundary for finite epsilon.

The smooth family mu_alpha=1-(1+x/alpha)^(-alpha) has mu~x and
f''=[1+x*(1/alpha-1)]*(1+x/alpha)^(-alpha-1)>0 for 0<alpha<=1.
This is only a derivative identity and a family to grade later. No all-x Schur,
causality, local, or data claim is made for the rest of that family.

## 8. Internal prior-art and independent-audit scope

Parent's bounded repository-wide search found a related slow polarization
response in sol61_push/CRITICAL_RESPONSE_RESULTS.md,
db/dg=1-1/sqrt(1+12*alpha*g), arising from a cubic polarization potential.
That derivative is not the physical interpolation mu above. The conceptual
slow-tail route is therefore not claimed as globally novel, and repository
search is not a literature novelty proof. The exact 50/81 coupled-portal
bound is the present scoped derivation.

Independent reviewer verify_archive reproduced the general K_lock identity,
slow-kernel 50/81 ratio and negative-C all-angle argument. They found no algebra
flaw in those claims and required the leading-derivative/frozen-limit and
local-eta qualifications now recorded above. Their review does not establish
full covariant or finite-wavelength parent health.
