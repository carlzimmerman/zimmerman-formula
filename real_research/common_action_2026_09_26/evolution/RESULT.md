# CD26-4 evolution: a constructive regularity repair, with its remaining boundary

This audit begins at `ecffd2af3623ff3e32318234fd51e1fac50b9126` with the dirty CD26-2/3 work retained. It advances one part of the common-action problem: the proposed **convex-composition gate** can repair source regularity at active MOND zeros while preserving strong convexity of the auxiliary solve on a fixed compact leaf. It does not establish global coupled evolution. A second constructive repair, the measured-G-normalized alpha sector, also removes the old frozen-block sign crossing. Full lapse/metric/carrier mixing and a coercive continuation estimate remain separate obligations.

The calculation deliberately distinguishes three claims: positivity of a principal or kinetic block on a specified state class; local well-posedness of a coupled constrained evolution; and continuation for all time while remaining in that class. None follows merely from a positive static auxiliary Hessian.

The latest continuation is [CP_AND_CARRIER.md](CP_AND_CARRIER.md): it retains the weighted-gate transition failure, derives its compensated lapse-independent repair, and audits canonical carrier mixing. The fixed-background estimates below are retained with their explicit gate version; the continuation translates them to the current CP candidate.

## 1. What XC3, XC5 and the outer-filter result actually establish

XC3 derives the filter's foliation variations in a static-background decoupling limit. Its noncommuting heat derivative is relevant, but its static suppression and finite weak-field scans do not bound the complete moving-background metric/clock system. Its own mutation restores first-order foliation couplings when the background moves.

XC5 supplies a genuinely useful fixed-lapse result. On a compact connected leaf, for fixed positive lapse N, metric h and heat operator S, the energy

    E(U) = ∫N [2|DU−a|² + 2 alpha_M² q(|DSU|²/alpha_M²)],
    a = D ln N,

is strongly convex modulo constants for the monotone phantom law. No ordinary finite Hessian exists at an open zero-gradient region; convexity and monotonicity still make sense there. Geometric heat need not contract the N-weighted norm. Uniform estimates in a family of lapses require N_min>0, N_max<infinity and geometry bounds, not merely pointwise N>0.

The earlier outer-filter result makes the physical force spatially smooth for suitable integrable inputs. Its ungated source-to-force map still scales as sqrt(source amplitude) at an open zero. Position regularity and source-data regularity are different.

## 2. The inverse direction is already better behaved

Divide E by four and define

    J_norm(p) = alpha_M² q(|p|²/alpha_M²)/2,
    H = mean-zero H¹,  ||u||_H² = ∫N|Du|².

The auxiliary equation is a resolvent equation

    u + B(u) = f,

in the Dirichlet Hilbert space, where B is the gradient of a convex functional. The prescribed f is the Riesz representative of the linear source functional; in this auxiliary problem it is associated with the fixed metric/lapse data. For two solutions,

    ||du||_H² <= <df,du>_H,
    ||du||_H <= ||df||_H.

Moreover, writing dr=df−du, monotonicity gives <du,dr>>=0 and hence

    ||du||_H² + ||dr||_H² <= ||df||_H².

These statements do not require a bounded constitutive derivative at zero. Existence uses coercivity, weak lower semicontinuity and a fixed mean; uniqueness is strict convexity. This is not a proof about the joint lapse/metric/transport equations.

The scalar control is exact. For gamma>0 and f>=0,

    u + gamma sqrt(u) = f,
    u(f) = [(sqrt(gamma²+4f)−gamma)/2]²,
    du/df = 1−gamma/sqrt(gamma²+4f) in [0,1).

By contrast, the forward map f(u)=u+gamma sqrt(u) is not Lipschitz at u=0. In the ordinary static QUMOND direction, matter first fixes a Newtonian auxiliary field and the physical potential is a forward constitutive response. A Lipschitz inverse in prescribed lapse data therefore cannot be relabeled a Lipschitz matter-to-force result.

## 3. The exact finite-alpha clock block has an upper condition

An independent determinant calculation of L340's source-free four-variable scalar block, keeping alpha_c=a>0 and c2=b>0, gives

    cs² = b[2−a(1+C)] / [(2+3b)(a+(a+2)C)].

For C>=0 the denominator is positive. Positivity also requires

    a(1+C)<2.

The often-used approximation b/[C(2+3b)] sets a=0 first. It is not uniform when C grows. In fact C→infinity at fixed a>0 gives the negative limit

    −ab/[(2+3b)(a+2)].

The numerical rational control a=10^−9,b=.01,C=3×10^9 is negative; C=1 is positive. This checks the algebra, not the existence of a completed physical background.

**Admissibility matters.** A constant tiny-gradient background has zero Laplacian and is gate-off for a positive-density, same-field gate. At an active isolated zero the pointwise coefficient diverges but the relevant heat-sandwiched operator can be bounded. It would therefore be incorrect to turn the frozen constant-C crossing into a no-go for the newly gated action. The legitimate requirement is an upper estimate for the actual constrained operator, including gate terms and mixing. A static positive Hessian supplies a lower bound, not that upper bound.

### The revised alpha sector removes this old crossing

The action agent's new construction defines cN=1−alpha/2 and changes the pre-elimination auxiliary terms to

    alpha|a−DZ|² +4a·DZ−2|DZ|²−4cN DZ·DU+cN G.

For the carrier-free nonzero modes, the Z equation gives DZ=a−DU. Direct substitution, rather than an assumed coefficient replacement, yields

    alpha|a|²+2cN|DU−a|²+cN G.

The old action is recovered only if these coefficient changes are undone. For the new action, keeping the Einstein and c2 kinetic terms unchanged, the independently recomputed scalar matrix gives

    phi=psi+cN U,  phi=(1+C)U,
    L_red = 2(2+3c2)/c2 psi_dot²
             −2(2−alpha)/(2C+alpha) k²psi²,
    cs² = c2(2−alpha)/[(2+3c2)(alpha+2C)].

Thus the reduced kinetic and spatial quadratic forms are positive for every **finite** C>=0, c2>0 and0<alpha<2. The effective acceleration coefficient is

    alpha_eff=(alpha+2C)/(1+C),
    0<alpha_eff<2,  2−alpha_eff=(2−alpha)/(1+C).

This removes the old finite-alpha numerator instability while retaining a positive inertia floor as C→0. The determinant, stationary Z equation, exact substitution and reduced quadratic action are independently checked. The companion calculation fixes the measured local normalization G_N=G/cN; that normalization is not an extra empirical fit here.

For0<=C<=Gamma, the repaired frozen block has the positive lower speed bound

    cs² >= c2(2−alpha)/[(2+3c2)(alpha+2Gamma)].

The upper estimate Gamma below can supply such a bound on the declared fixed-background energy class. C→infinity still degenerates this bound; one may not ignore that endpoint. The convex gate handles active zeros through a bounded integrated operator rather than assigning an infinite constant C to a homogeneous mode. These results remain carrier-free, reduced-host statements. They do not certify the complete projected-Z constraint algebra or mixing with the moving carrier, lapse and geometry. In the fixed-lapse energy estimates below, the repaired host's auxiliary energy is simply cN E_new; divide by cN>0 to use the displayed normalization.

## 4. Heat averaging controls a transverse singularity

On a fixed flat compact leaf let S be the positive self-adjoint Markov heat operator. For a scalar nonnegative coefficient C, Jensen's inequality gives

    ∫ C|Sv|² <= ∫ C S(|v|²) = ∫(SC)|v|²,
    ||S M_C S||_(L²→L²) <= ||SC||_infinity.

One can first truncate C and pass monotonically to an integrable singular coefficient. Matrix coefficients are controlled by their largest eigenvalue. The bound uses a heat average, not ess sup C. In the N-weighted Dirichlet norm an elementary comparison adds kappa_N=N_max/N_min. The exact two-site Markov control has raw coefficient maximum100, operator norm62.5 and heat-average bound75.

For a one-dimensional transverse zero embedded in three dimensions, g=gamma x1 e1 with gamma>0, the leading deep-MOND coefficient is sqrt(a0/(gamma |x1|)) in physical acceleration units. Its Gaussian heat average at the zero is exactly

    [Gamma(1/4)/(2^(1/4)sqrt(pi))] sqrt[a0/(gamma xi)]
      = 1.72007997... sqrt[a0/(gamma xi)].

The Gaussian uses variance xi², corresponding to S=exp(xi² Delta/2). The convolution of the even decreasing power and Gaussian is maximal at the zero. Three independent quadrature widths verify the closed form after a change of variable removes the integrable singularity. This is a controlled transverse-zero model, not a universal value for an inhomogeneous galaxy.

The nu_mono coefficient admits a global majorant. Put d=delta h_peak, y_peak>0. For h_RAR(y)=y/(exp(sqrt(y))−1), write h_RAR=sqrt(y) F(sqrt(y)) with 0<F<=1 and F'<=0. Consequently h_RAR'<=1/(2sqrt(y)). From

    h_mono' = max(h_RAR', d/(y+y_peak)),  h_mono(0)=0,

one obtains

    h_mono(y) <= sqrt(y)+d log(1+y/y_peak),
    C_T <= y^(-1/2)+d/y_peak,
    C_L <= (1/2)y^(-1/2)+d/y_peak.

Thus the transverse singularity plus a finite constant controls both eigenvalues. Strict positivity alone would not provide this upper estimate.

## 5. Why a generic multiplicative gate is insufficient

Multiplying a convex energy by a positive state-dependent gate does not preserve convexity when that gate is varied. The bounded, increasing logistic function

    f_K(u)=1/[1+exp(−K(u−1))/3]

has values in(0,1). Nevertheless

    E(u)=u²/2+(2/3)f_K(u)u^(3/2),  u>0,
    E''(1)=11/8+3K/8−K²/16,

which equals−69/8 at K=16. This is a noninheritance counterexample, not a claim that a specific completed gate necessarily has this Hessian.

## 6. The new convex-composition gate repairs that objection

The current construction instead proposes

    W = S_h U,
    sigma = J(DW)+ell Delta_N W−theta,
    E_new(U) = ∫N [2|DU−a|²+G(sigma)],
    Delta_N W = N^−1 div(N DW),

with ell,theta>0, J(p)=2 alpha_M² q(|p|²/alpha_M²), and G convex and nondecreasing. G'=0 for sigma<=0 and G'=1 for sigma>=delta>0. Thus J has Hessian eigenvalues4C_T,4C_L. This normalization matters in any comparison with the finite-alpha clock block.

At fixed N,h, Delta_N S is affine in U. For v=delta U,

    delta²[G(sigma)]
      = G' Hess_J[DSv,DSv]
        +G''[DJ·DSv+ell Delta_N Sv]² >=0.

Therefore delta²E_new>=4||Dv||_N² wherever the second variation is interpreted; convexity itself extends to zero gradient without differentiating the singular pointwise tangent. This is a genuinely new action ingredient. The old phenomenological gate's numerical passes are not inherited.

The proposed C4 ramp uses t=sigma/delta and

    G'=35t^4−84t^5+70t^6−20t^7,  0<t<1,
    d(G')/dt=140t³(1−t)³>=0.

Its integral across the unit transition is1/2, and its first three endpoint derivatives vanish. The checked chain rule applies to this ramp. On a closed leaf, ∫N Delta_N W=0, so the affine Laplacian term is a boundary term on a fully-on plateau. The plateau also leaves the genuine constant offset−theta−delta/2 in G; its lapse/gravitational effect must not be discarded.

### Active zeros are transverse by construction

Where J(DW)<=theta/2 and G'>0,

    Delta_N W > theta/(2ell).

At DW=0 the drift a·DW vanishes, so Delta_N W=Delta W. Near the zero, a uniform bound on |a| and the condition |a·DW|<=theta/(4ell) imply

    Delta W > theta/(4ell).

At least one component derivative of g=DW is then bounded away from zero. This excludes an open active zero region. The argument holds at every point along interpolation between fields because the gate is evaluated on each interpolant; one need not posit that an independently chosen transverse-state class is convex.

### Bounded-energy fixed-background source regularity

On a fixed flat compact leaf, heat smoothing gives

    ||D^m(DSU)||_infinity <= C_m(xi)||DU||_2,   m=0,1,2.

Since G>=0, an energy bound gives

    ||DU||_N <= sqrt(E_new/2)+||a||_N.

Thus on any fixed energy ball the filtered gradient has uniform derivative bounds. The active-zero trace bound gives a finite uniform atlas of transverse charts. In each chart one component of g is monotone with derivative at least a fixed positive constant. Fubini then bounds the active sublevel volume by

    volume{G'>0, |g|<r} <= C r    for sufficiently small r.

The constants depend on the energy ball, geometry, xi,theta,ell and lapse bounds. Layer-cake integration gives a uniform integral of G'|g|^(−1/2). The heat kernel and its derivatives are bounded on the compact leaf, so the singular contribution is a bounded bilinear form after both heat factors. Away from small |g| all constitutive derivatives are bounded.

The remaining G'' term is also controlled. On a flat leaf write a=DlnN. Then

    DJ·DSv+ell Delta_N Sv = (DJ+ell a)·DSv+ell Delta Sv.

If M_G=||G''||_infinity, L_J=||DJ||_infinity and A=||a||_infinity, its quadratic form is bounded by

    2 kappa_N M_G [(L_J+ell A)²+ell²/(e xi²)] ||Dv||_N²,

using sup_(k>=0) k² exp(−xi²k²)=1/(e xi²). Including the J-Hessian yields, after dividing by the base factor4, the conditional bound

    Gamma <= kappa_N { ||S(G' C_max)||_infinity
                 +(M_G/2)[(L_J+ell A)²+ell²/(e xi²)] }.

Integrating the bounded Hessian along straight paths shows that **the forward auxiliary Euler map is locally Lipschitz from H¹ modulo constants to its dual on bounded sets**, for fixed N,h and this new gate. The existing strong-monotonicity argument controls its inverse. The integral proof can be justified by smoothing J at zero, using the uniform active sublevel bound, then taking the limit. It does not assert a pointwise finite J-Hessian at the zero.

This is the constructive advance over the old outer-filter result. It is not yet a coupled Cauchy theorem. In particular, metric/clock changes alter S, Delta_N, the volume form and all mixed variations. A bound Gamma sufficient for the scalar constrained block cannot be assumed to diagonalize the full variable-coefficient system.

## 7. Positive lapse on a slice is not an all-time bound

The separate spectral-lapse construction solves

    (-4b Delta−A)y=0,  N=y²>0.

Its ground-state factorization and positive root are useful slice statements. A positive eigenfunction on a connected compact leaf follows under the specified elliptic spectral conditions, but uniform positivity in time requires bounds on geometry, coefficients and normalized spectral inverses.

The exact family y=exp(epsilon cos x), A=−4b y''/y has arbitrarily large lapse contrast exp(4|epsilon|). Its constrained Hamiltonian integrand is a total derivative,

    A y²−4b(y')² = −4b(yy')',

so the integrated constraint energy is zero for every epsilon. A bound on that zero Hamiltonian cannot by itself bound lapse contrast. With mean N normalized to1, N_min=exp(−2epsilon)/I0(2epsilon) tends to zero and N_max grows. Overall clock relabeling does not change the contrast. The same issue appears in trying to infer a quantitative timelike margin solely from the clock's derivative invariants; the clock chart and lapse bounds must be part of a propagated admissible state class.

The new action uses a different lapse equation, so the spectral example is a warning about coercivity, not an asserted counterexample solution of the new common action. Likewise the carrier phase-gradient counterexample from the transport route concerns identifying that phase with a clock; it must not be silently transferred to an independent khronon field.

## 8. What is now available and what still closes the evolution argument

Available analytically: strong auxiliary monotonicity, the correct inverse direction, the old finite-alpha upper condition and its explicitly changed-action repair, the heat-average singular-coefficient bound, and a convex same-field gate that gives local source regularity on fixed-background energy balls.

Still required for a global result: a fully reduced coupled principal/constraint system; a propagated state class with positive lapse, nondegenerate geometry and controlled clock gradients; and a coercive conserved energy or continuation inequality that bounds that class and the actual constrained Hessian. The gravitational Hamiltonian constraint is not automatically that coercive energy. Additional regularity estimates are needed for the time-dependent heat operator and matter stress. Local positive carrier coefficients, a bounded carrier potential and particle-free field transport help, but do not supply these missing gravitational estimates.

The bounded checks and small Lean file certify their displayed algebraic bridges only. No arbitrary-data nonsingular evolution, full-action stability, full field count, observational fit or all-time PDE theorem is claimed.

## Quantitative fixed-leaf hypothesis sheet

For the regularity claim in section6, take T^d of side2pi with normalized measure, fixed 0<N_min<=N<=N_max, ||DlnN||_infinity<=A, and fixed xi,ell,theta,delta>0. Fix the mean of U. Assume the stated nu_mono primitive and the C4 convex ramp, and E_new(U)<=E0. No parameter tends to zero in this assertion. Let

    R = N_min^(-1/2)[sqrt(E0/2)+||DlnN||_N],
    C_m(xi)² = sum_(k!=0) |k|^(2m) exp(−xi²|k|²),
    ||D^m g||_infinity <= C_m R,  g=DSU, m=0,1,2.

Choose eta>0 small enough that sup_(|p|<=eta) J(p)<=theta/2 and A eta<=theta/(4ell); the second restriction is unnecessary when A=0. Set tau=theta/(4ell). At every active point with |g|<eta, tr(Dg)>tau, so some partial_i g_i>tau/d. With M2=C_2 R, take a patch radius no larger than

    r0 = min(pi/8, tau/[4d sqrt(d)(1+M2)]).

On a suitably smaller coordinate box around that point the same derivative stays at least tau/(2d). A maximal separated cover has at most a fixed constant times(2pi/r0)^d boxes. Fubini bounds the sublevel length in the distinguished coordinate by4d r/tau, so for0<r<eta

    mu{G'>0, |g|<r} <= C_cover r,

where C_cover depends only on d,tau,r0 and the fixed volume/normalization. Thus

    ∫G' |g|^(-1/2) dmu <= Vol/sqrt(eta)+2 C_cover sqrt(eta).

For K_xi=sum_k exp(−xi²|k|²/2), the heat kernel obeys ||K_S||_infinity<=K_xi, and consequently

    ||S(G' C_max)||_infinity
       <= K_xi {sqrt(alpha_M)[Vol/sqrt(eta)+2C_cover sqrt(eta)]
                       +(delta_kernel h_peak/y_peak)Vol}.

Here delta_kernel denotes nu_mono's phantom-slope parameter, not the gate width delta. This deliberately coarse bound is finite and uniform on the stated energy ball; the exact linear-zero Gaussian result is much sharper when applicable. J's derivative is bounded on |p|<=C_0R, and the ramp has bounded G'', supplying the other term in Gamma. Because E_new is convex, every straight interpolant between two fields in the same energy sublevel remains in it. These estimates therefore justify the path-integrated local Lipschitz statement on that sublevel. They supply no control when the lapse, geometry, heat width or energy leave the declared bounds.
