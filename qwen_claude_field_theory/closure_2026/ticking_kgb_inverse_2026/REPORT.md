# Ticking KGB: constructive halo, same-action cosmology, and the universal-MOND gate

Date: 2026-09-10. Base commit: `e5dd47b08625e2444f3df7b0bce3421b7204d467`.
Unrelated dirty/untracked work was preserved.

## Decision

A ticking scalar evades the purely static scalar stress obstruction and gives
an explicit positive-density flat-rotation solution with healthy, subluminal
local scalar characteristics. The SAME action admits an expanding FLRW branch.
However, its fixed power selects one flat speed, not the mass-dependent BTFR.
Reconstructing the exact exponential transition with zero radial pressure
fails both the sampled scalar-health test and a two-mass action-compatibility
test. Neither construction is the requested complete gravity theory.

The new constructive tool is the general inverse identity below, which retains
nonzero radial pressure. The next action must satisfy its cross-mass
compatibility equations and stability simultaneously. The broader route is
**OPEN**, not certified. The two worked restricted constructions fail the full
target. A script exiting zero means its calculation ran, not that physics passed.

## 1. Same covariant action and actual variation

Use c=1, signature (-+++), m=(8 pi G_b)^(-1)>0, with G_b the bare
Einstein coupling. Its identification with a measured Newton constant is not
established for the full scalar theory:

\[
 S=\int d^4x\sqrt{-g}\,[mR/2+P(X)-G(X)\Box\phi]+S_m[g,\psi],
 \qquad X=-\tfrac12\nabla_\mu\phi\nabla^\mu\phi .
\]

The worked solutions set Lambda=0. Adding a cosmological constant is a new
background/stability problem, not already covered. This is the known KGB class;
see [sources and credit](SOURCES.md).

For ds²=-A dt²+B dr²+R(r)² dOmega² and phi=q t+psi(r), p=psi',
integration by parts gives the radial scalar Lagrangian

\[
 L_r=\sqrt{AB}R^2[P(X)+G_X X'p/B],\qquad
 X=q^2/(2A)-p^2/(2B).
\]

The script varies A, B, R and p with independent derivative jets. It also
varies the off-diagonal metric g_tr BEFORE setting it to zero; otherwise an
energy-flux equation could be lost. The resulting current and identities are

\[
 J^r=P_Xp/B+G_X\,X A'/(AB)-2G_Xp^2R'/(B^2R),
 \quad (\sqrt{AB}R^2J^r)'=0,
 \quad T^r{}_t=qJ^r,\quad p_r=P+pJ^r .
\]

On the static, zero-flux ticking branch q!=0, J^r=0, the independent metric
variations reduce to

\[
 p_r=P,\qquad \rho=2XG_X X'/p-P,\qquad p_t=P+G_XpX'/B,
 \qquad {p_t-p_r\over\rho+p_r}={p^2\over2BX}.
\]

For q=0, the full varied tensor has rho+p_t=0. It does NOT do so for q!=0.
Thus the repository's static-scalar result is not a ticking-scalar no-go.
This does not invalidate its stated static assumptions.

The covariant equations behind the principal calculation are

\[
 mG_{\mu\nu}=T^{(m)}_{\mu\nu}+T^{(\phi)}_{\mu\nu},\quad
 \nabla_\mu J^\mu=0,\quad
 J^\mu=(P_X-G_X\Box\phi)\nabla^\mu\phi-G_X\nabla^\mu X,
\]
\[
 T^{(\phi)}_{\mu\nu}=(P_X-G_X\Box\phi)\phi_\mu\phi_\nu+Pg_{\mu\nu}
 -G_X(X_\mu\phi_\nu+\phi_\mu X_\nu)
 +g_{\mu\nu}G_X\nabla X\cdot\nabla\phi.
\]

Ordinary matter is separately minimally coupled. Under a compactly supported
diffeomorphism its on-shell variation is
0=delta S_m=int sqrt(-g) T_m^(mu nu) nabla_mu xi_nu
=-int sqrt(-g) xi_nu nabla_mu T_m^(mu nu).
Consequently nabla_mu T_m^(mu nu)=0, assuming the ordinary matter equations
and no diffeomorphism anomaly. This is not just conservation of a combined
effective fluid. A complete canonical/Dirac derivation has NOT been supplied.

## 2. Local inverse with radial pressure retained

For the stress required by a prescribed Einstein geometry, set

\[
 b_*={p_t-p_r\over\rho+p_r}>0,\quad
 X={q^2\over2A(1+b_*)},\quad
 p^2={Bq^2b_*\over A(1+b_*)},\quad
 P(X(r))=p_r(r),\quad G_X(X(r))={p(\rho+p_r)\over2XX'}.
\]

Exclude X'=0, p=0, rho+p_r=0, require A,B,X>0 and a monotone X interval.
Then the remaining current equation reduces exactly to radial stress
conservation:

\[
 {BX'\over p}J^r=p_r'+{A'\over2A}(\rho+p_r)
                  +{2R'\over R}(p_r-p_t)=0.
\]

The last equality follows for an Einstein-required stress by the Bianchi
identity. The substitution and stress identities are checked symbolically.
This constructs functions along ONE profile. Universality requires BOTH
P and G_X to agree wherever different profiles have the same X; integration
constants and boundary conditions must also be compatible. A branchwise
inverse is not a predictive universal theory.

## 3. Exact constructive example

Take P=0, G(X)=-g_* X^n, g_*>0 and

\[
 A=A_0(r/r_0)^{2w},\quad B=1+2w,\quad
 X={q^2\over A(2+w)},\quad p=\sqrt{BwX},\quad
 n={1-w\over2w},\quad 0<w<1.
\]

The coefficient required by the Einstein equations is

\[
 g_*={m\sqrt w\over2\sqrt{1+2w}\,n r_0 X_0^{n+1/2}},
 \qquad X_0={q^2\over A_0(2+w)}.
\]

Thus this is an explicit action, not an unspecified stress ansatz. The code
sets reference units A_0=r_0=|q|=1 and differentiates the metric to construct
the Christoffel symbols, Ricci tensor and Einstein tensor independently:

\[
 \rho={2mw\over(1+2w)r^2}>0,\qquad p_r=0,\qquad p_t={w\rho\over2}.
\]

All three Einstein residuals and the current vanish. The local circular speed
satisfies v_circ²/c²=w. This is a local exterior power-law halo, not a regular
center, asymptotically flat spacetime, or a cosmologically matched solution.

The weak-field potentials are independently read after converting areal to
isotropic radius, r proportional to R_iso^(1/sqrt(B)):

\[
 \Phi={w\over\sqrt B}\log(R_{iso}/R_*)+O(\Phi^2),\qquad
 \Psi=(1-1/\sqrt B)\log(R_{iso}/R_*)+O(\Psi^2).
\]

Their logarithmic slope ratio is 2/(sqrt(1+2w)+1)=1-w/2+O(w²).
It gives no slip at leading order in small w, not exact nonlinear equality
and not a Solar-System gamma_PPN derivation. No PPN parameter is assigned.

For characteristics, expand div J, use Einstein's trace-reversed equation
to eliminate R_mu_nu phi^mu phi^nu, and differentiate the resulting scalar
equation with respect to the Hessian of phi. Off-diagonal symmetric-Hessian
entries receive the required factor 1/2. The canonical-scalar limit P=X,G=0
independently returns diag(1,-1,-1,-1). On the halo, at the reference radius,
the derived matrix is

\[
 C={m(w+2)\over2(2w+1)}\operatorname{diag}(w+2,-3w,-3w^2,-3w^2),
 \quad c_r^2={3w\over w+2},\quad c_\perp^2={3w^2\over w+2}.
\]

Time kinetic energy has the canonical positive sign and the scalar cone is
subluminal for 0<w<1; Lean proves the displayed rational inequalities.
This is a local principal-symbol result. Global hyperbolicity, interaction
strong coupling and matching through a center are not thereby certified.

## 4. Expanding branch from that same power action

For q=dot(phi)=-Q<0, X=Q²/2 and flat FLRW, the nonzero Friedmann root is
H=2qXG_X/m>0. The shift charge is J=6HXG_X, and dot(J)+3HJ=0 yields

\[
 w_{cos}={p\over\rho}={1\over4n+1},\quad
 a(t)\propto t^{(4n+1)/(3(2n+1))},\quad
 c_{cos}^2={16n+7\over3(4n+1)^2}.
\]

The kinetic coefficient is 6(4n+1)X²G_X²/m>0. Friedmann, spatial Einstein
and charge-conservation residuals vanish. Lean proves 0<c_cos²<1 for n>=1,
a sufficient range covering small galactic w. This branch is approximately
dustlike for n large; it is NOT accelerated dark energy. No radiation era,
recombination, Lambda extension or observed cosmological fit has been tested.

## 5. Where the construction fails the requested MOND theory

**Fixed power:** n fixes w=1/(2n+1). A fixed action therefore cannot produce
different flat speeds on this branch for distinct baryonic masses. Lean
proves that imposing w_i²=K M_i with common K>0 and common n forces M_1=M_2.
This is a conditional obstruction to this branch, not all KGB solutions.

**Exact exponential inverse:** use mu=1-exp(-y), r=epsilon/sqrt(y mu),
epsilon=sqrt(G_b M a0)/c²; dimensionless a0=m=|q|=1. Here G_b M labels the
prescribed Newtonian profile; an actual baryonic-source matching calculation
has not been performed. Choose the relativistic
embedding B=(1-2ry)^(-1), (log A)'=2yB. Its Newtonian mu->1 limit has the
Schwarzschild form. Its weak-field acceleration is the requested y; no
all-orders coordinate-acceleration identity is assumed. Einstein gives

\[
 \rho={4my^2e^{-y}\over r[\mu+ye^{-y}]},\quad p_r=0,
 \quad p_t={ryB\over2}\rho .
\]

The inverse then supplies G_X and G_XX by differentiation, not by a chosen
interpolation of the principal matrix. At epsilon=10^-6 and 2*10^-6,
y={0.02,0.1,0.5,1,2,5,10,20}, all 16 metric/current-stress checks have relative
residual below 10^-35 in 50-digit arithmetic. The tested principal-health
conditions hold at y<=1 but fail at all sampled y>=2. For example, epsilon=
2*10^-6, y=10 gives C00 approximately -9.9680*10^10: the scalar time coefficient
has the wrong sign; the radial hyperbolicity discriminant also fails. Good
field-equation residuals do not rescue the perturbations.

**Same-action test:** fix q=-1 and A(y=0.02)=1 separately for the two masses.
Integrate A and find the common X in the overlapping intervals by 140
bisections. At X approximately 0.500003218095919564435,

| epsilon | y at common X | reconstructed G_X |
|---|---:|---:|
| 10^-6 | 0.6708320079630 | -756.0083792903 |
| 2*10^-6 | 0.1294092748338 | -124.2056790989 |

The values differ by a ratio approximately 0.1642914054, with X-matching error
below 10^-45. This numerically rejects universality of THIS zero-pressure
embedding with THESE normalizations. Boundary freedom, radial pressure,
other metric completions and other action classes are not excluded.

## 6. Remaining closure requirements and next calculation

The target is not attained: exact universal MOND/AQUAL and BTFR fail in the
worked examples; full nonlinear Dirac closure, a separately classified healthy
clock degree of freedom, vector/tensor perturbation derivations, measured
Newton constant, full PPN, k=0 and zero-field strong coupling, and cosmological
matching remain unproved. A known second-order action class is not a substitute
for the requested constraint calculation. An extra scalar is present in this
route; it is not an elliptic auxiliary and must be explicitly accepted/countable
as the allowed genuine clock, never silently called two total modes.

No value of kappa, a0 or the a0–Lambda relation has been derived, and no
empirical data was fitted. The flat halo alone is not a new Kepler-grade law.

The next unavoidable calculation is a JOINT two-function P(X),G(X) construction
for multiple baryonic masses using section 2, retaining small radial pressure.
Require equality of both reconstructed functions at shared X and healthy
principal matrices before fitting anything to galaxy data. If no such branch
exists in a specified functional family, retain that scope in the conclusion.
Do not repair one mass or one speed by assigning separate action parameters.

## Reproduction and evidence

From this directory: `python3 -B run_suite.py`. It prints exact argv, working
directories and exit statuses for all nested commands. The suite runs the
symbolic action, the exponential inverse, nine new tests, three Lean theorems,
and the previous 40 closure regression tests. `kgb_inverse.py --require-closure`
must exit 2 (not closed); this is kept distinct from test execution failures.

The authoritative bounded run under `run_002/` records raw stdout/stderr, command, environment,
resource caps, base revision, dirty state and before/after input hashes.
`audit_contract.json` states bounds and non-claims. Numerical angular sampling
is 361 directions, not a universal numerical proof. Lean proves only its
explicit conditional algebraic statements, not the field equations or a law
of nature. The source and report were self-reviewed for notation and scope.
`run_001/` predates the bare-versus-measured-coupling clarification; its raw
outputs are retained, but its report input hash is superseded by `run_002/`.
