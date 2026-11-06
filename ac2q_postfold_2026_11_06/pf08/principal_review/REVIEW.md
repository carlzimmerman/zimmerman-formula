# Independent PF08 audit: principal genuine nonlinearity versus native breakdown

**Primary verdict: incomplete, with the smallest missing implication being
a differentiated, constraint-compatible error estimate transferring the
frozen principal Riccati mechanism to the finite-K coupled evolution.**
The proposed fixed-A derivatives and genuine-nonlinearity factor are
correct. They do not by themselves prove breakdown of the native system.
An exactly frozen-A nonconstant simple wave is not even an exact finite-K
solution, as shown below. No full-action counterexample or avoidance
theorem is established by this review either.

Base d7aba1da7f. Scope: independently derive the proposed principal model,
identify the first uncertain transfer step, and inspect singular selection
claims. No solver changes or evolution experiments. Input hashes and seven
exact algebra checks are in `check_result.json`; `CONTRACT.md` preceded
their execution.

## 1. Fixed-A principal calculation

Take gamma>0 and

    H(r,A)=r^2/2-V-W+(Ar-1-gamma r^2)^2/(2gamma).

For partial derivatives in r, A is held fixed. Constant/frozen V and W do
not enter these derivatives. At the homogeneous matter state D=0,

    A0=(1+gamma r0^2)/r0,
    H_r=r0,
    H_rr=1+(1/r0-gamma r0)^2/gamma,
    H_rrr=-6(1/r0-gamma r0).

All three formulas pass direct differentiation. In the source-free frozen
flat k-essence subsystem, write

    phi_t=r cosh(theta), phi_x=-r sinh(theta), v=tanh(theta).

The compatibility and scalar equations are

    e(r)+r n(theta)=0,
    H_rr n(r)+H_r e(theta)=0,

where n=cosh(theta)partial_t+sinh(theta)partial_x and
e=sinh(theta)partial_t+cosh(theta)partial_x. At rest they become

    r_t+(H_r/H_rr)theta_x=0,
    theta_t+r_x/r=0.

Thus c^2=H_r/(r H_rr), lambda_+=(v+c)/(1+vc), and the plus right
eigenvector satisfies dtheta/dr=+1/(r c). The proposed sign is correct.
At v=0, along that eigenvector,

    d lambda_+/dr=c_r+(1-c^2)/(r c)=G/(2r c),
    G=3(1-c^2)-H_r H_rrr/H_rr^2.

At general v the same bracket is multiplied by
(1-v^2)/(1+vc)^2, so its sign is unchanged in the timelike domain.

With z=gamma r0^2,

    c0^2=z/(1-z+z^2),
    G0=3(1-c0^2)+6(1-z)/H_rr(r0,A0)^2.

For 0<z<1, both terms are nonnegative and the second is strictly positive.
Hence the principal characteristic is genuinely nonlinear. At z=1 this
specific test gives c=1 and G=0, so the strict range matters.

For a sufficiently small simple-wave state interval around such a point,
hyperbolicity and positive directional speed derivative persist. The
source-free scalar simple-wave equation consequently has the usual exact
gradient characteristic law wdot=-lambda'(u)w^2 and a compressive datum
breaks in that **frozen subsystem**. Nonconstant explicit potentials would
already add sources; freezing the metric also excludes Einstein evolution.

## 2. Fixed A is not differentiation along the homogeneous family

The curve A0(r)=1/r+gamma r consists of different homogeneous backgrounds.
Its derivative is gamma-1/r^2. Along this curve,

    d[H_r(r,A0(r))]/dr=1,

whereas the fixed-A partial derivative is H_rr, generally much larger.
Replacing the partial derivatives by total derivatives along A0(r) changes
the principal model and would give the wrong result for this calculation.
The genuine-nonlinearity derivative above is explicitly at fixed A.

Conversely, treating fixed A as an exact solution restriction fails at
finite K. The exact polarization equation is

    r e(A)=W_P.

If A is exactly constant, the strict hold law forces P=0. Then D=0 and
the algebraic auxiliary equation requires Ar=1+gamma r^2. For fixed A,
r can take only the isolated roots of this equation; a connected smooth
profile cannot be a nonconstant r simple wave. This is a direct obstruction
to embedding the frozen-A wave as an exact native solution. It does not
rule out a justified high-frequency asymptotic transfer.

## 3. What finite K actually changes, already in flat matter

Keep the exact auxiliary constraints, still omitting gravity and explicit
potential sources for this diagnostic. Let

    D=(Ar-1-gamma r^2)/gamma,
    D_r=(A-2gamma r)/gamma, D_A=r/gamma.

The equations include

    e(P)=D,
    e(A)=W_P/r,
    e(r)+r n(theta)=0.

The scalar equation from the auxiliary action is

    H_rr n(r)+H_r e(theta)+r D_r n(A)+(W_P/r)n(P)=0.

To obtain this, the topological scalar-current divergence is
n(P)e(A)-e(P)n(A). Combining it with n(H_r) uses
H_rA-D=r D_r. In particular the corrections contain n(A) and n(P);
they are not simply bounded algebraic source values supplied for free.

The commutator [n,e]=(n theta)n-(e theta)e gives exact differentiated
constraints

    e(nA)=(W_PP/r)nP-(W_P/r^2)nr-(n theta)nA+(e theta)W_P/r,
    e(nP)=D_r nr+(r/gamma)nA-(n theta)nP+(e theta)D.

These already exhibit the issue: estimates for the auxiliary time
derivatives couple to the steep fluid gradients. Curved geometry and
transverse expansion add further coefficients and source terms.

In curved planar geometry, the exact scalar equation is

    R n(r)+(h_A-D)n(A)+(W_P/r)(n(P)+2P n(beta))
        +h(div_2 n+2n(beta))=S_phi,
    h=H_r, R=H_rr, h_A-D=r(A-2gamma r)/gamma,

where div_2 is the base two-dimensional metric divergence and S_phi is
the controlled explicit scalar source. The topological divergence
divided by E is exactly

    (nP+2P n(beta))e(A)-(eP+2P e(beta))n(A).

Use e(A)=W_P/r and e(P)+2P e(beta)=D to obtain the displayed equation.
Thus the proposed full-frame source structure is correct without dropping
auxiliary time derivatives. Clock compatibility adds the spin connection
to n(theta)=-e(log r), as required for a nonconstant frame.

### Exact homogeneous linear control

At P=0, theta=0, r=r0, A=A0, with W_PP(0)=K>0, linearization gives

    partial_x delta A=(K/r0)delta P,
    partial_x delta P=D_r delta r+(r0/gamma)delta A.

For Fourier wavenumber k,

    delta A=-(K D_r/r0)/(k^2+K/gamma) delta r.

Eliminating its time derivative from the scalar equation gives the
effective kinetic coefficient and exact flat-subsystem linear sound ratio

    Keff(k)=H_rr-K D_r^2/(k^2+K/gamma),
    c^2(k)=(k^2+K/gamma)/(H_rr k^2+K/gamma).

The high-frequency limit is 1/H_rr, exactly the frozen-A principal result
at D=0. The zero-frequency ratio is 1. Thus the high-frequency claim has
a concrete linear basis, but the low modes are not small corrections.
Nonlinear products can generate precisely those low modes. This linear
calculation is a frozen-flat matter control, not the full gravitational
dispersion or a nonlinear shock theorem.

## 4. The first missing transfer estimate

One needs a well-posed constrained evolution and a compact state domain
with uniform hyperbolicity, clock/cap/branch margins, and controlled metric
coefficients. In adapted characteristic variables, a sufficient route
would establish an exact gradient equation of the form

    D_+ w=-a w^2+R,  a>=a0>0,
    |R|<=eta w^2+C1|w|+C0, eta<a0,

uniformly in the high-frequency family up to the claimed breaking time.
Opposite-family gradients, auxiliary inverse-operator terms, and metric
terms must all be included in R and bounded with constants independent
of the compression scale. If w starts negative enough, the displayed
inequality implies wdot<=-c w^2 and hence finite-time gradient blowup,
provided the amplitude/domain/constraint bounds survive to that time.

The reviewed material does not establish this inequality. The first
specific missing step is a differentiated estimate for the nonlinear
clock-slice inverse solving for A,P and their temporal derivatives,
including the generated low modes and coefficient gradients. A bound on
e(A) or on A,P amplitudes alone is not that estimate. Gravity also requires
constraint-compatible initial data and estimates that its contribution
does not cancel the Riccati term or destroy the assumed compact domain.

There is useful structure for the gravitational part: on branch and on
a compact frame-clock domain the auxiliary Hilbert stress is algebraic
and bounded independently of matter gradients. A regular 1+1 wave-gauge
estimate can therefore plausibly control metric first derivatives for a
uniform short time from uniformly controlled initial metric data, without
differentiating matter stress. This observation does not itself construct
the constrained initial data or prove the needed matter-gradient estimate.

The constant-coefficient multiplier (k^2+K/gamma)^(-1) provides two powers
of high-frequency suppression at the linear level. It does not justify
commuting arbitrary derivatives through variable-coefficient nonlinear
constraints with constants independent of the growing gradient. That is
the earliest unproved implication, before any appeal to a shock theorem.

### Why bounded source amplitude alone is insufficient

A concrete counterexample to that proposed *inference*, not to AC2q, is
forced Burgers:

    u_t+u u_x=F_k(x),
    u=k^(-1/2)sin(kx), F_k=sin(kx)cos(kx).

This is an exact stationary smooth solution with uniformly bounded source
amplitude and arbitrarily steep compressive slope of size sqrt(k).
F_k,x is order k and cancels the order-k Riccati term. Thus genuine
nonlinearity plus bounded sources does not imply formation. The native
constraints must supply the stronger differentiated bounds, rather than
being called lower order solely from amplitude estimates.

No such native cancellation has been constructed here. Equally, no native
estimate excluding it has been proved. This is why the correct verdict
remains incomplete rather than breakdown or avoidance.

## 5. Does the auxiliary system select singular continuations?

The Q>=1 minimization and KKT complementarity uniquely encode the local
switch relation for given smooth D and r. They are constitutive/domain
conditions, not an entropy or vanishing-regularization rule for scalar
shocks and surface measures. The topological canonical formulation is an
exact reformulation of the original action; it adds no physical selection
mechanism merely by introducing A and Pi.

Native necessary conditions remain: field equations, metric constraints,
clock/domain restrictions, switch complementarity, and the appropriate
charge/stress balances. The previous regular-corner obstruction shows
that some naive finite-state continuations cannot satisfy them. It does
not show that all singular limits are absent or identify a unique one.

To establish intrinsic admissibility one would need, for example, a
well-defined singular solution class with existence and uniqueness, or
a proved unique limit of the native smooth evolution within a controlled
compactness framework. Neither follows from the local auxiliary
minimization. No claim of actual nonuniqueness is made without distinct
valid solutions; the selection question is unresolved.

## Obligation matrix

| Implication | Status |
| --- | --- |
| Fixed-A derivatives and sound speed | passed |
| Eigenvector sign and G formula | passed |
| G>0 for 0<gamma r0^2<1 | passed |
| Principal compressive simple-wave breaking | passed for the source-free frozen subsystem |
| Exact finite-K embedding with constant A | refuted by the polarization constraint |
| High-frequency linear approach to the principal speed | passed for the frozen-flat matter subsystem |
| Nonlinear differentiated estimate uniform to breaking | not established |
| Full coupled smooth-data breakdown or avoidance | not established |
| Intrinsic singular admissibility/uniqueness from auxiliary variables | not established |

Independent audit provenance: delegated review, 2026-11-06. Seven symbolic
identities pass via `python ac2q_postfold_2026_11_06/pf08/principal_review/check.py`.
These checks certify the displayed algebra only. No external theorem was
imported and no numerical experiment was treated as a formation proof.
