# DP1: what the radial law fixes, and what dynamics still require

Date: 2026-09-27. Scientific parent: AFG-008. This lane derives directly
from Q and R in the campaign contract. No literature was searched, no named
mechanism imported, and no historical novelty is claimed. The latest STANDING
was consulted only to retain its warnings about nonzero curl, failed static
hosts, and incomplete relativistic/cosmological extensions. This construction
does not supersede those empirical exclusions.

## Claim and conventions

Let a>0 be a constant acceleration. Q is F(B)=sqrt(B²+aB); R is
F(B)=B/[1-exp(-sqrt(B/a))], B>0. Let b(g)=F^{-1}(g), extended by b(0)=0,
mu(g)=b(g)/g for g>0. Gradients have the **opposite sign** to physical
accelerations: b_N=grad Phi_N, g_vector=grad phi, acceleration=-g_vector.
G>0; Phi and phi have units of speed squared. Boundary data must be specified.

The exact conclusions below are conditional mathematical statements about
explicit field classes, not a claim of a complete gravity theory. Both registered
a values are 9.3619e-11 and 1.1279e-10 m/s². The dimensionless conclusions are
independent of the normalization. We do not change to the M interpolation.

## 1. An exact integrability condition and a vacuum counterexample

Put nu(B)=F(B)/B. For a C² Newtonian potential on a simply connected open set
with |b_N|>0,

    curl[nu(B)b_N] = nu'(B) grad B cross b_N.                 (1)

Consequently direct vector rescaling is conservative if and only if this
right-hand side vanishes everywhere. The simply connected hypothesis is needed
for the global converse; zero curl is locally sufficient. For Q and R, nu'<0
at every finite B>0, so the condition is exactly grad B parallel to b_N.
Spherical symmetry guarantees it; generic nonspherical fields do not.

This fails already in a source-free tidal patch. Take length L>0,

    Phi_N = a/(2L) (x²+2y²-3z²),
    p = (L/sqrt(5), L/sqrt(5), 0).

Here Laplacian Phi_N=0, B(p)=a and
(grad B cross b_N)_z=-2a²/(5L). Writing u=B/a, (1) is

    (curl g_vector)_z = -(2a/5L) d nu/du at u=1
                      = a/(5 sqrt(2)L)             [Q]
                      = a exp(-1)/(5L(1-exp(-1))²) [R].     (2)

Both are strictly positive. There is a nonzero circulation around arbitrarily
small rectangles containing p. The harmonic polynomial is a **local vacuum
witness**, not an isolated finite-mass boundary condition. A global isolated
counterexample is unnecessary for refuting the asserted local identity.

## 2. A conservative extension exists, after a new constitutive assumption

**New assumptions:** one scalar potential, local rotation-invariant dependence
on its first spatial gradient, universal source term rho phi, and a Gauss law
for the constitutive flux. Define

    W(g;a) = integral_0^g b(s;a) ds,
    E_static[phi] = integral [W(|grad phi|;a)/(4 pi G)+rho phi] d³x.

Variation at fixed Dirichlet boundary values gives

    div[mu(|grad phi|) grad phi] = 4 pi G rho.              (3)

For a regular spherical solution, integration fixes b(g)=GM(<r)/r²=B, hence
g=F(B). A central point mass requires its separately prescribed flux. Generally
(3) fixes divergence, not the vector identity mu grad phi=grad Phi_N: their
difference is a divergence-free vector field determined by geometry/boundary
data. Equation (2) proves why this distinction cannot be dropped.

The spatial Hessian A of W at g>0 has eigenvalues

    lambda_perp = mu(g) = b(g)/g,
    lambda_parallel = b'(g) = 1/F'(B).                    (4)

Both are positive. Thus W is strictly convex as a function of grad phi and the
linearized static operator is elliptic wherever g>0. At g=0 both eigenvalues
vanish: this is degenerate ellipticity, not uniform ellipticity.

There is also a bounded-domain existence/uniqueness result. For a bounded
Lipschitz domain, rho in L² and prescribed boundary values with an H¹
extension, E_static on that affine H¹ class has a unique weak minimizer. Indeed
W(g) grows quadratically at large g since b(g)/g tends to 1, giving
W(g)>=c0 g²-C0 for some positive c0,C0. Poincare and Cauchy-Schwarz bound the
linear source term, yielding coercivity. Convexity gives weak lower
semicontinuity; the direct method gives a minimizer; strict convexity of the
gradient energy and fixed Dirichlet data give uniqueness. This does not assert
classical smoothness at critical points, existence on an infinite domain, or
that observed nonspherical galaxies obey (3).

The construction is unique **within the stated first-gradient single-scalar
constitutive class**, up to an additive constant in W: spherical recovery for
all positive B fixes W'(g)=b(g). It is not unique among all conservative
extensions, nonlocal fields, extra fields, higher derivatives or couplings.

For Q the primitive is explicitly

    b(g) = (sqrt(a²+4g²)-a)/2,
    W_Q(g) = g sqrt(a²+4g²)/4
             + a² asinh(2g/a)/8 - ag/2.                   (5)

Its deep limit is g³/(3a). R has the same deep limit and an unambiguous positive
quadrature primitive. No vacuum-energy normalization follows from its additive
constant: the nonrelativistic equations only see derivatives of W.

## 3. A family with time evolution and exact conservation laws

**Additional new assumption:** a preferred inertial time and a constant K>0,
which the static law does not determine. Consider the nonrelativistic action

    S_K = integral dt d³x [K phi_t²/(8 pi G c²)
                          - W(|grad phi|)/(4 pi G) - rho phi]
          + S_matter,kinetic.

Use smooth mass-conserving matter, with the same coupling giving acceleration
-grad phi. Then

    K phi_tt/c² - div(mu grad phi) = -4 pi G rho.          (6)

This is an explicit time-dependent theory in the preferred frame, not a
relativistic completion. All K have exactly the same time-independent field
equation and exactly the same spherical Q/R relation.

For a smooth solution with vanishing boundary flux, time and spatial translation
invariance yield conserved total energy and momentum. The field energy and
energy flux are

    e_f = [K phi_t²/(2c²)+W]/(4 pi G),
    S_f = -phi_t mu grad phi/(4 pi G),
    partial_t e_f + div S_f = -rho phi_t.

Matter kinetic energy obeys its usual work law. Adding the interaction energy
rho phi and its advective flux cancels -rho phi_t, using
rho_t+div(rho v)=0. Thus total energy includes matter kinetic energy, rho phi,
and e_f. It need not be bounded below for self-attracting point particles; the
positive *field perturbation* result below is not a nonlinear matter-stability
claim.

For clarity, the compensating field momentum is

    (p_f)_i = -K phi_t partial_i phi/(4 pi G c²),
    (T_f)_ji = [mu partial_j phi partial_i phi
                 + delta_ji (K phi_t²/(2c²)-W)]/(4 pi G).

Direct differentiation of (6) gives
partial_t (p_f)_i + partial_j (T_f)_ji = +rho partial_i phi,
which cancels the matter force density -rho partial_i phi. These identities
require a constant a and K and accounting for boundary/source fluxes; a
prescribed fixed source alone is an external energy/momentum reservoir.

Linearize around a static source-free uniform gradient g0>0. For angle theta
between wave vector and that gradient,

    omega² = (c²/K) |k|²
             [lambda_perp sin² theta + lambda_parallel cos² theta]. (7)

The quadratic field energy is positive for every nonconstant mode and K>0.
This is local strict hyperbolicity plus positive quadratic energy on the
specified background. It proves neither global smooth evolution nor stability
of a cosmological or self-gravitating matter background. At g0=0 the spatial
principal part vanishes and the strict-hyperbolicity statement ceases to apply.

For both Q and R, lambda_parallel>lambda_perp. If we **add** the requirement
that all these characteristic speeds be <=c, the necessary and sufficient
constant-K condition is K >= sup_(B>0) lambda_parallel(B).

For Q, using u=B/a,

    lambda_perp = sqrt(u/(u+1)),
    lambda_parallel = 2 sqrt(u²+u)/(2u+1) < 1.

Hence the exact sharp constant bound is K>=1. For R, writing t=sqrt(B/a),

    lambda_perp = 1-exp(-t),
    lambda_parallel = (1-exp(-t))²/[1-exp(-t)(1+t/2)].      (8)

It is positive and <2, since F'(B)>1/2 is equivalent to
2 sinh(t)>t. Thus K=2 is an analytically sufficient bound for R, independent
of any numerical maximization. K=1 fails for sufficiently large t, because
lambda_parallel>1 iff t>2(1-exp(-t)); the positive equality root is about
1.59. The numerical supremum and its location are reported as finite numerical
evidence, not certified global optimization. Both K=2 and K=8 are conservative,
locally stable, <=c examples on every nonzero uniform-gradient background.
Their propagation times for the same mode differ by exactly a factor of two,
despite identical static Q/R curves. Arbitrarily large K gives arbitrarily
long response times. The static response has zero derivative with respect to K:
no collection of static radial measurements can identify it in this family.

The missing input is at least one independent positive kinetic coefficient
even in this tightly restricted class. If local gradient-dependent kinetic
coefficients K(g)>0 are admitted, the missing input is a positive **function**;
it remains absent from every exactly static field equation and sets the
quadratic time coefficient on each static background. Higher powers of phi_t
add further invisible nonlinear dynamical data. No value of kappa or a replaces
these missing inputs. A measured response time or wave speed, and a choice of
which time/frame is physical, are independent information.

## 4. The minimal Lorentz-invariant scalar choice is a sharper conditional test

Restrict instead to a local one-scalar first-derivative Lorentz-invariant action
with flat metric light speed c,

    S = -1/(4 pi G) integral P(X) dt d³x + S_source,
    X = |grad phi|² - phi_t²/c².

On static spacelike backgrounds, matching the same constitutive law fixes
P(X)=W(sqrt(X)) for X>0, up to a constant. Expanding directly about constant
spacelike grad phi gives time coefficient 2P'(X)=mu and spatial coefficients
(4). Therefore

    c_perp²/c² = 1,
    c_parallel²/c² = lambda_parallel/mu
                   = d log B / d log g.                 (9)

In Q, this ratio is 2(u+1)/(2u+1). In R it is

    [1 - t/(2(exp(t)-1))]^{-1}.

Both are strictly between 1 and 2 for every finite positive B, tending to 2
in the deep limit and 1 in the Newtonian limit. Thus the first-derivative
Lorentz-invariant one-scalar class cannot simultaneously implement either
static law and have every characteristic inside the chosen metric light cone
on those backgrounds. It remains hyperbolic there; this is **not** a proof of
generic acausality, ghost instability, or a no-go for relativistic gravity.
Extra fields, other matter light cones, derivative terms or other couplings lie
outside the theorem. The coupling used here does not supply a lensing metric.

Moreover, static radial data determine P only at X>0. They do not specify its
timelike X<0 branch, needed even to discuss a homogeneous time-dependent scalar
background. W~g³/(3a) entails P~X^(3/2)/(3a) near X=0+, so the spacelike branch
itself loses a nonzero quadratic kinetic coefficient at X=0. A regular timelike
continuation and a cosmological solution do not follow from the radial fit.

## 5. Vacuum normalization versus the separate H(z) prescription

For a=kappa c sqrt(G rho_Lambda), fixed vacuum rho_Lambda makes a constant and
the preceding time-translation conservation identities apply. Neither kappa
nor its two observed normalizations determine K, a metric coupling, or a
timelike kinetic branch.

Replacing this with externally prescribed a(t)=a(0)E(z(t)) is a distinct model.
It explicitly breaks time translation in this action. The local balance gets
the additional source

    partial_t e_total + div S_total
       = (partial W/partial a)_g a_dot/(4 pi G).          (10)

For either Q or R, F_a>0, so b_a=-F_a/F_B<0 and W_a<0. Thus this exchange is
nonzero wherever a_dot and g are nonzero. In the deep regime,
W=g³/(3a), W_a a_dot=-(a_dot/a)W. With the registered illustrative
E²=0.315(1+z)³+0.685 and z_dot=-(1+z)H,

    a_dot/a = -3 H Omega_m(z)/2.

Consequently the deep field-energy injection term is +3H Omega_m(z)W/(8 pi G).
This is the explicit missing reservoir/exchange term of the prescribed-time
toy action; it is not an FLRW energy-conservation derivation. Promoting the
vacuum/scale to a dynamical field could supply the reservoir, but then its
equation, energy and coupling must be given. Merely inserting H(z) does not.

## Verification, dependency graph and remaining implication

Dependency graph: frozen Q/R equations -> F monotonicity -> inverse b -> W and
Hessian -> conditional static existence and spherical recovery. Separately,
new K action -> conservation identities and principal symbol. Additional
Lorentz-invariant P(X) restriction -> K=mu -> metric-light-cone conflict.
New externally prescribed a(t) -> explicit exchange term. No empirical or
external theorem source is a hidden leaf in the algebraic statements.

`check_dynamics.py` tests the analytic derivatives against central differences;
the exact vacuum curl against shrinking-loop quadrature; W_Q against independent
inverse-function quadrature; positivity and limiting cases over a stated grid;
the numerical R maximum; two finite-difference wave evolutions with K=2,8 and
their conserved discrete quadratic energy; both dimensional normalizations;
and the separate E(z) energy-exchange coefficient. Its finite output supports
the implementation, while the universal inequalities above have their own
algebraic proofs. Run provenance pins actual inputs, code, limits and outputs.

Self-review obligation status: integrability **passed** with explicit simply
connected/local distinction; radial recovery **passed conditionally** on the
new constitutive assumptions and flux boundary condition; static existence
**passed** for the bounded-domain weak formulation; conservation **passed
conditionally** for smooth matter/fields with stated boundary treatment;
linear stability **passed** only for the specified nonzero-gradient fixed
background; global evolution, lensing, Solar-System compatibility, cosmology
and observational calibration **not addressed**. No independent agent audit
was performed within this lane.

Primary proof-audit verdict for "the radial laws determine a physical dynamical
completion": **incomplete, with the smallest missing implication**. Even one
kinetic coefficient K is not identifiable from the exact static predictions;
its selection requires a new principle or dynamical observable. The survivor
is a conditional conservative, preferred-frame local field family with a
proved spatial construction and a tested linear evolution, not a replacement
empirical theory. The next discriminating calculation is to specify a physical
time/metric coupling and K, then compute a source-response observable; adding
more scalar radial fits cannot select that missing dynamics.
