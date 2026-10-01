# SD1: a positive dynamical scale, its necessary backreaction, and a stable local survivor

2026-09-27. Parent: DP1 stage-three scalar derivation. No earlier evidence is
modified. This is a new conditional two-field model derived from the Q/R
constitutive functions, not a uniquely selected theory or a relativistic
completion. No literature mechanism is imported and no novelty is claimed.

## 1. Explicit assumptions and scale equation

Retain b(g;a)=F^{-1}(g;a), W(g;a)=integral_0^g b(s;a) ds from DP1, with
Q: F=sqrt(B²+aB) and R: F=B/[1-exp(-sqrt(B/a))]. The acceleration is
-grad phi, and g=|grad phi|. Add a dimensionless scalar chi and set

    a = a_ref exp(chi) > 0.

The independently registered reference values are 9.3619e-11 and
1.1279e-10 m/s². Positivity of a is built into this parametrization, not derived.
Assume constants K,J,v_chi>0 and a time-independent potential U(chi). The action is

    S = integral { [K phi_t²/(2c²) - W(g;a_ref exp chi)
                    + J chi_t²/(2 v_chi²) - J |grad chi|²/2 - U(chi)]/(4 pi G)
                   - rho phi } dt d³x + S_matter,kinetic.                 (1)

J has units acceleration² length²; U has units acceleration². K is dimensionless.
This is a local preferred-frame nonrelativistic model with one extra field.
Its kinetic normalization, stiffness, potential, boundary conditions and frame
are added assumptions. No cosmological or photon metric is specified.

Define the positive gravitational drive on chi

    T(g,a) = -W_chi = -a W_a = g b(g;a) - 2 W(g;a),
    q(g,a) = T_g = g lambda - B,
    lambda = b_g = 1/F_B,  B=b(g;a),  mu=B/g.                            (2)

The homogeneity W=a² w(g/a) gives these identities directly. For Q and R,
F_a>0 and F_B>0, so b_a<0 and W_a<0: T>0 for g>0. The strict decrease of
F(B)/B also gives q>0. Additionally

    b_chi = -q,  T_chi|g = 2T-gq.                                      (3)

The two Euler-Lagrange equations are

    K phi_tt/c² - div(mu grad phi) = -4 pi G rho,
    J chi_tt/v_chi² - J Laplacian chi + U'(chi) = T(g,a).                (4)

Thus the reservoir repairs the missing exchange only by responding to the
gravitational field. Its reaction cannot consistently be discarded.

## 2. Exchange and momentum balance close within the assumed action

Let e_phi=[K phi_t²/(2c²)+W]/(4 pi G) and
S_phi=-phi_t mu grad phi/(4 pi G). Then

    partial_t e_phi + div S_phi = -rho phi_t - T chi_t/(4 pi G).

Let e_chi=J[chi_t²/v_chi²+|grad chi|²]/(8 pi G)+U/(4 pi G) and
S_chi=-J chi_t grad chi/(4 pi G). Its balance is

    partial_t e_chi + div S_chi = +T chi_t/(4 pi G).                     (5)

Adding (5), then the matter kinetic and interaction energies as in DP1,
cancels the exchange.
Boundary fluxes still matter. This is conservation of the specified action,
not an assertion of globally bounded self-gravitating matter energy.

For momentum, DP1's phi stress now obeys

    partial_t p_phi,i + partial_j T_phi,ji
       = rho partial_i phi + T partial_i chi/(4 pi G).

The chi momentum and stress are

    p_chi,i = -J chi_t partial_i chi/(4 pi G v_chi²),
    T_chi,ji = [J partial_j chi partial_i chi
                 + delta_ji(J chi_t²/(2v_chi²)-J|grad chi|²/2-U)]/(4 pi G).

Equation (4) gives their divergence as -T partial_i chi/(4 pi G). Thus the
internal momentum exchange also cancels, leaving the usual matter force pair.

## 3. Uniform-scale obstruction

For a static spatially uniform chi_c with no extra tuned source, (4) requires

    U'(chi_c) = T(g(x), a_ref exp chi_c) at every x.                     (6)

The left side is constant and T_g=q>0 at every g>0. Hence (6) is impossible
on a region containing two distinct field magnitudes. The exceptional case
is constant |grad phi|, including zero. This is an exact conditional no-go for
the uniform static scale in action (1), independent of how large finite J is.
A tailored spatial source equal to the residual, a rigid nondynamical limit,
or a change of coupling can evade it only by changing the stated model.

Spherical symmetry gives the exact flux relation even for variable chi:

    b(g(r); a(r)) = GM(<r)/r² = B(r),
    g(r) = F(B(r); a_ref exp chi(r)),
    -J(chi''+2chi'/r)+U'(chi) = T(F(B(r);a(r)),a(r)).                    (7)

This retains MOND in the entire source/force calculation. It also demonstrates
why the newly supplied scale equation changes the old fixed-a radial prediction.

## 4. An explicit potential with a useful stability theorem

Choose the following new, nonunique stabilizing potential, with S0>0:

    U(chi) = S0 [cosh(2chi)-1]/4,
    U' = S0 sinh(2chi)/2,  U''=S0 cosh(2chi).                          (8)

It has positive curvature, a unique zero-field minimum at chi=0, and obeys
U''-2U'=S0 exp(-2chi)>0. This identity motivates the choice; neither the radial
law nor the vacuum normalization derives it.

For any fixed B0>0 there is a unique **homogeneous equilibrium at fixed flux**
chi0>0 solving U'=T(F(B0,a),a). To see this, divide both sides by a².
The left side is S0[1-exp(-4chi)]/(4 a_ref²), strictly increasing for chi>=0.
The right side is a dimensionless positive function of B0/a, strictly
increasing in B0/a because

    partial_B [T(F(B,a),a)] = g - B/lambda = q/lambda > 0.

It therefore strictly decreases with chi and tends to zero as chi tends to
infinity. At chi=0 the left side is zero and the right side positive, proving
existence and uniqueness by continuity. No negative chi can solve it since
U'<0 while T>0. This is not a global uniqueness theorem for (7).

Consider the exact source-free background phi0=g0 n dot x, chi=chi0 constant,
with U'(chi0)=T(g0,a0) and g0>0. Its field quadratic potential has coefficients

    A = mu I + (lambda-mu) n n^T,
    m = U''-T_chi|g = U''-2T+g0 q,
    mixed energy = -q eta (n dot grad psi),                            (9)

where psi=delta phi and eta=delta chi. At equilibrium,

    M = m-q²/lambda
      = S0 exp(-2chi0) + B0 q/lambda > 0.                            (10)

For any wave-vector direction, writing
Lambda(theta)=mu sin²(theta)+lambda cos²(theta),
q² cos²(theta)/Lambda(theta)<=q²/lambda. Thus (10) is a sufficient and here
strict bound on the Schur complement of the full static quadratic form.
With K>0 and J/v_chi²>0, both coupled field modes have positive squared
frequencies for every nonzero wave vector. The dispersion is

    [Lambda k²-K omega²/c²]
    [J k²+m-J omega²/v_chi²] - q² k² cos²(theta) = 0.                 (11)

The spatially constant phi shift is a zero mode; the homogeneous chi oscillator
has positive mass. This establishes linear **field** stability on the given
background, not self-gravitating matter stability, nonlinear global evolution,
or cosmological stability. At zero gravitational gradient the DP1 degeneracy
remains. High-frequency characteristic speeds approach c sqrt(Lambda/K) and
v_chi; the mixing is lower differential order. K=2 and v_chi<=c retain the
earlier sufficient metric-speed bound, without making the model relativistic.

## 5. Finite-scale susceptibility is determined once the new coefficients are supplied

For a one-dimensional static perturbation parallel to n, let delta B be the
perturbation of the constitutive flux. The linearized equations are

    delta B = lambda delta g - q eta,
    (-J partial_x² + m) eta = q delta g.

Eliminating delta g yields

    eta(k) = q delta B(k) / [lambda (M+J k²)],
    delta g(k)/delta B(k)
       = (1/lambda) [1+q²/(lambda(M+J k²))].                        (12)

The response length is sqrt(J/M). The scale's response increases the force
susceptibility; it vanishes as k tends to infinity at fixed J. A massive or
very stiff scale suppresses the correction. For a general direction the
corresponding Schur factor uses Lambda and cos(theta) as in (11).

Near the reference state at weak backreaction, chi approximately equals
(-J Laplacian+S0)^(-1) T(g_fixed,a_ref). At fixed baryonic B,

    delta g/g approximately alpha(B/a_ref) chi,
    alpha_Q = a_ref/[2(B+a_ref)],
    alpha_R = t/[2(exp(t)-1)], t=sqrt(B/a_ref).                       (13)

Both approach 1/2 in the deep regime. A tolerance epsilon on fractional force
change therefore requires about |chi|<2epsilon there. For an almost uniform
source patch with scale long compared with sqrt(J/S0), chi approximately
T/S0 and one needs S0 approximately greater than T/(2epsilon). This is a
leading-order design condition, not an observational bound or a derived value
of S0. The finite spherical solves below evaluate the full equations instead.

For a spherical region with chi=0 at the outer boundary and regular center,
any smooth solution of (7) has chi>=0: a negative interior minimum would give
-J Laplacian chi+U'(chi)<0, contradicting T>=0. Where the source drives the
scale, the response is positive. Therefore this model predicts an environmental
increase of a and of the force compared with the fixed-reference law.

## 6. The vacuum relation is a real additional obstruction, not a label for chi

The reference parameter may be set to the core value
a_ref=kappa c sqrt(G rho_Lambda,ref), with either registered normalization.
If rho_Lambda is an exactly constant vacuum and the core relation must hold
pointwise for the **actual local** a, it forces chi=0 everywhere. Equation (6)
then rules out this local reservoir around a varying gravitational field.
Accordingly the surviving two-field construction requires an extra physical
interpretation: chi changes an effective local acceleration scale around the
vacuum-set reference. This is a modification of the literal universal constant-a
reading, not a derivation from it.

One might instead demand rho_Lambda(x)=rho_Lambda,ref exp(2chi). That declaration
does not make the added canonical scalar a vacuum. Its gradients and kinetic
energy have non-vacuum stresses, and its potential (8) is not this density.
Even in a static homogeneous zero-gradient limit, identifying its potential
energy U/(4 pi G) with rho_Lambda c² forces

    U(chi) = [4 pi a_ref²/kappa²] exp(2chi).                         (14)

But a stationary homogeneous vacuum then requires U'=0, whereas (14) has
U'=2U>0 at every finite chi and positive vacuum density. Thus the simplest
identification with the scale field's own potential cannot produce a static
positive vacuum. Adding a constant background energy to (8) leaves its equation
unchanged but does not repair equality (14) over a range of chi. An additional
sector or different coupling is required; none is covertly supplied here.

## 7. The separate prescribed H history is still not selected

If one demands a(t)=a_ref E(z(t)), then chi_H=log E is a proposed trajectory,
not a solution derived from (1). In the zero-field homogeneous limit it must
satisfy J chi_H,tt/v_chi²+U'(chi_H)=0. On the registered illustrative history
E²=0.315(1+z)³+0.685 and z_dot=-(1+z)H,

    chi_H,t = -3 H Omega_m/2,
    chi_H,tt = (9/2)H² Omega_m(1-Omega_m/2)>0.                      (15)

At z>=0, chi_H>=0 and U'>=0, so the required source
J chi_H,tt/v_chi²+U' is strictly positive. This history is not a homogeneous
zero-field solution of the new action. It could be externally driven only by
restoring a source whose energy exchange must also be accounted for.
Equation (15) is a check against the prescribed E(z), not an FLRW field
calculation. A cosmological action would add metric dynamics and change this
question; no Hubble-friction term was silently inserted into (1).

## Verification contract and limits

`check_scale.py` performs deterministic binary64 checks of T and its derivatives
using independent quadrature/finite differences, verifies the strict uniform
scale obstruction at unequal fields, compares the coupled-mode eigenvalues to
the Schur identity, tests (12) against nonlinear one-dimensional boundary-value
solutions, and solves (7) on a declared finite spherical domain at both
normalizations. It checks a local manufactured scale energy balance directly,
and keeps the core-vacuum and prescribed-H branches separate. Parameters are
illustrative declared inputs, not fits to observations. Output and actual input
hashes are recorded by the computation-audit runner.

The precise earned survivor is an energy-exchanging positive scale with a
stable coupled local field background and a calculable susceptibility. The
precise failed target is an exactly uniform static dynamical scale around a
varying field within this action, and—under the stated identification—a static
positive vacuum furnished by the scale field's own exponential potential.
The remaining physical decision is whether an environmental effective scale
is allowed at all by the core claim. If it is, independently constrain S0,J,
v_chi and K and test (12)/(13) across source sizes; if it is not, this reservoir
class is excluded and an alternate exchange coupling is required. No new
scalar radial fitting can by itself settle that dynamical decision.
