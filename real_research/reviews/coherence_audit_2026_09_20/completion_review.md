# Independent bounded review of the carrier completion

Date: 2026-09-20. Base commit: `3aaed026d55f65b38733316cb63c432290a339e1`.
This review independently read the raw `carrier_action/check_carrier.py`,
`carrier_bounds/check_bounds.py`, `carrier_bounds/KineticSchur.lean`, and the
Sep19 ADM builder before reading the carrier report. Source files were not changed.

**Normalized claim.** On X>0, Y>=0, with A>1 and positive rho0, X0, Yd,
the stated p(X,Y) defines a conserved, positive-density homogeneous carrier,
whose switch has no quadratic contribution along any homogeneous rolling X,
and whose coupled homogeneous quadratic velocity Hessian is positive when it
maps to the stated ADM core.

**Primary verdict: correct only after a stated restriction.** The constitutive
and homogeneous statements are correct. The positive reduced velocity Hessian
is also correct for the explicit ADM action with intrinsic spatial healing,
or with xi=0. It does not extend to the older projected-spacetime-Hessian
healing term on expanding FRW. None of these statements proves finite-Y
stability, halo phenomenology, a cutoff, or novelty.

## Stress, currents, and constitutive identities

Use signature (-+++), a separate clock tau with T=-grad(tau)^2>0,
n_a=-tau_a/sqrt(T), Q=n^a phi_a, and s_a=phi_a+Q n_a. Direct differentiation gives

    delta Y / delta g^{ab} = s_a s_b,
    T_ab = p g_ab + 2 p_X chi_a chi_b - 2 p_Y s_a s_b.

A conserved carrier current is j_chi^a=p_X grad^a chi. The variational currents
from the carrier alone, with the common normalization retained, are

    Pi_chi^a = -2 p_X grad^a chi,
    Pi_phi^a = 2 p_Y s^a,
    Pi_tau^a = -2 p_Y Q s^a/sqrt(T).

The scalar and clock equations include the other sectors' contributions.
The carrier stress alone is generally not separately conserved at finite Y.
For the perfect-fluid part tau_ab=2p_X chi_a chi_b+p g_ab, the chi equation gives
nabla^a tau_ab=p_Y nabla_b Y, agreeing with the stated exchange identity.

Write r=X/X0. Then

    p_X = rho0 r^m/(2X),
    p_XX = (m-1) p_X/X,
    rho = rho0[(2m-1)r^m+1]/(2m) > 0,
    K_chi = p_X+2X p_XX = (2m-1)p_X > 0,
    c_chi^2 = 1/(2m-1),
    p = (rho-rho0)/(2m-1).

The last equation is a fixed-Y affine constitutive identity. The temporal
Hessian on a homogeneous carrier background is 2K_chi. In the fixed-clock
rest frame even a spatial carrier gradient leaves the bare chi time Hessian
2p_X+4 chi_dot^2 p_XX positive, because m>1. These are bare carrier statements,
not a substitute for eliminating the metric and clock constraints.

For s_bar=0, Y=O(epsilon^2). Since

    m(Y)-m(0) = -(A-1)Y^2/(8Yd^2)+O(Y^4),

p(X,Y)-p(X,0)=O(epsilon^4), uniformly in a compact positive-X neighborhood.
The conclusion holds for an arbitrary finite rolling X_bar(t)>0. At X_bar=X0
the leading mixed correction is even higher order because p and p_X at X0
are independent of m. No direct quadratic switch coupling has been omitted.

The conserved homogeneous charge gives, on either fixed sign branch of chi_dot,

    X(a)=X0 a^(-6/A),
    rho(a)=rho0[A a^(-3(1+1/A))+1]/(A+1),
    p(a)=rho0[a^(-3(1+1/A))-1]/(A+1),

with X(1)=X0. Both charge conservation and continuity follow exactly. This
solves the carrier on FRW; H(a) must still solve the gravitational equations
with this density and any other stated components. K_chi>0 is pointwise on
X>0, not a uniform lower bound as X approaches zero in the far-future limit.

## Independent ADM reconstruction of the velocity core

For h_ij=a^2 exp(-2Phi) delta_ij, N=1+Psi, v=Phi_dot,
u=delta_chi_dot, C=chi_bar_dot, b=c2, and r_b=2+3b, retain the scalar shift
through sigma. Expanding K_ij K^ij-(1+b)K^2 gives, after removing the common a^3,

    -3 r_b(v+H Psi)^2 - 2 r_b(v+H Psi)sigma - b sigma^2.

The exact matter expansion N p((C+epsilon u)^2/N^2) contributes
K_chi(u-C Psi)^2 to this block, for arbitrary p_bar, p_X, p_XX and C(t).
Eliminating sigma gives Akin=2(2+3b)/b. The phi-constant auxiliary scalar block,
with intrinsic spatial healing, is

    (k/a)^2 [alpha Psi^2 + 2d Psi P - d(beta+xi^2 k^2/a^2)P^2].

For d!=0 and beta+xi^2 k^2/a^2!=0 its elimination gives
alpha_eff=alpha+d/(beta+xi^2 k^2/a^2). Thus the submitted core follows with
Bkin=K_chi and E=alpha_eff k^2/a^2. Sufficient sign assumptions are
b>0, d>0, 0<alpha<2, beta=d/(2-alpha), xi^2>=0, k!=0, a>0.
At xi=0, alpha_eff=2 exactly.

For D=Akin H^2+Bkin C^2+E, the reduced Hessian divided by a^3 is

    (2/D) [[Akin(Bkin C^2+E), Akin Bkin H C],
           [Akin Bkin H C, Bkin(Akin H^2+E)]].

Its determinant is 4 Akin Bkin E/D>0, and its first principal minor is positive.
The physical determinant including a^3 is a^6 times this expression.
The algebra and sign argument are correct; k=0 is excluded and gives E=0.

Configuration-dependent sources in the lapse or shift equations, including
terms linear in a velocity, generate velocity-configuration or configuration
terms after elimination. They do not change this Hessian because the relevant
quadratic auxiliary block is already retained. Time derivatives of Bkin or C
matter in the evolution equations, not in this instantaneous Hessian.
Background equations are needed for a consistent perturbation problem, but
no on-shell cancellation was needed for the displayed velocity core.

### Material distinction between two healing operators

`real_research/clock_2026/clock_action_build.py:302-305` uses
(h^{mu nu} nabla_mu nabla_nu phi)^2. The Sep19
`frw_repair/adm_unitary.py:37` instead uses intrinsic spatial healing.
These operators differ by the extrinsic-curvature term:

    h^{mu nu} nabla_mu nabla_nu phi = Delta_h phi - K Q.

Even when phi_bar is constant, on FRW their linearizations differ:

    delta(h^{mu nu} nabla_mu nabla_nu phi)
      = a^(-2) Delta P - 3H P_dot.

The older operator contributes

    -a^3 d xi^2 [k^2 P/a^2 + 3H P_dot]^2.

For d>0 and H xi!=0 this gives the additional negative Hessian entry
-18 a^3 d xi^2 H^2 for P_dot. On the stated cold phi-constant background there
is no compensating bare phi kinetic term; the lapse/shift blocks do not mix
with P_dot at this order. P is then dynamical, and the auxiliary elimination
is invalid. In that specified cold action this is a negative kinetic direction.
Therefore explicitly use intrinsic healing, set xi=0, or restrict to H=0;
do not import the alpha_eff formula into the older FRW builder for xi!=0.

## Finite-Y obstruction and exact scope

The chain-rule identity and the submitted exact witness are correct:

    p_Y+2Y p_YY = p_m(m_Y+2Y m_YY)+2Y p_mm m_Y^2.

For A=9, Yd=rho0=1, y=sqrt(15), z=1/3, m=3,

    p_Y = -sqrt(15)/288,
    p_Y+2Y p_YY = sqrt(15)(7+10e)/4608 > 0.

Thus the transverse and longitudinal pressure curvatures can have different
signs. In a fixed-clock, fixed-metric scalar spatial-energy block for -J(Y)+p,
positive energy requires J_Y-p_Y>0 and
J_Y+2YJ_YY-p_Y-2Yp_YY>0. This restricted block does not settle constrained
coupled stability or establish that the witness lies on a halo solution.

A stronger domain warning follows directly. At any fixed finite Y>0, m_Y!=0.
As z=log(X/X0) tends to positive infinity,

    p_Y+2Yp_YY ~ rho0 Y m_Y^2 exp(mz) z^2/m -> +infinity.

Consequently no X-independent J(Y), with finite derivatives at that Y, can
keep this restricted longitudinal spatial-energy coefficient positive over
the entire unbounded X>0 domain. This does not exclude a bounded physical
branch, but any global positivity claim needs an additional restriction or
an altered constitutive design.

## Obligation matrix and evidence

| Obligation | Status |
|---|---|
| Stress and normalized-clock variation | Passed by direct chain rule |
| Constitutive positivity, affine EOS, charge trajectory | Passed under stated domain |
| No quadratic switch term on arbitrary rolling homogeneous X | Passed |
| Schur determinant and positive kinetic minors | Passed for Akin,Bkin,E>0 |
| Mapping for intrinsic healing or xi=0 | Passed for the displayed ADM action |
| Same mapping for older projected Hessian with H xi!=0 | Failed; extra negative P kinetic term |
| Full finite-Y reduced principal symbol and constraints | Not addressed |
| Halo solution, observable cosmology, strong-coupling cutoff, novelty | Not addressed |

The dependency chain is constitutive differentiation -> homogeneous current
and perturbative order; independently ADM expansion -> auxiliary elimination
-> positive kinetic minors. Neither branch supplies the finite-Y spatial
principal symbol or a background solution of the full inhomogeneous equations.
There are no external-theorem leaves in these checks.

A read-only Python 3/SymPy 1.14.0 inline calculation independently expanded
N p(X), the ADM extrinsic-curvature block, and its shift reduction; all three
residuals were exactly zero. It independently recomputed the finite-Y witness
and checked the three diagonal components of the normalized-projector metric
variation. The off-diagonal statement follows from the displayed tensor chain
rule. Lean was read but not rerun in this review. No full builder, cosmological
integration, or nonlinear halo solve was run.

The strongest safe result is a coherent conserved homogeneous carrier plus a
positive two-field quadratic velocity Hessian in the stated intrinsic-healing
ADM theory. The next discriminating calculation is the full finite-Y reduced
principal symbol, with a precise physically reached X,Y domain and the chosen
healing operator fixed. A positive temporal Hessian alone is insufficient.
