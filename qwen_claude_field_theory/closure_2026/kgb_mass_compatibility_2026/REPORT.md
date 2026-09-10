# Common-mass preservation and an action-derived conformal clock extension

2026-09-10. Initial code base `9a088d45c9c3349de154446aeee4500a84f31c9a`;
concurrent Fable commit reviewed: `3b41b064a` (L119). Unrelated work preserved.

**Status: OPEN, not a completed theory. No dark-matter particles are introduced.**
The physical clock is a real scalar field, not an auxiliary field being omitted
from a degree count. A local scalar principal test is not a full Dirac count.
The broader goal remains one universal action, not a different fitted action for
each galaxy. No empirical fit, new observed law, or globally novel theory is
claimed by this checkpoint.

Carl Zimmerman's physical inputs are retained: the exponential MOND law, the
primordial-clock direction, the no-particle-dark-matter restriction, and the
fitted acceleration-scale relation. The coefficient 1/2 is still fitted; the
Lean results below do not derive it. The derivative-conformal action class is
known in the literature, as documented in `extension/SOURCES.md`. The work here
is the explicit inverse, its compatibility tests, and its independently audited
implementation. Mathbox computation/proof audits guided the separate evidence
and scope statements; mathematical proofreading covered this report.
The desired a0-Lambda relation remains an input/target: this local inverse has
not identified a matching cosmological vacuum energy for its reconstructed P.

## 1. Actual progress beyond the previous two-mass construction

The old KGB action is `sqrt(-g)[m R/2+P(X)-G(X) box(phi)]`. Its two-mass inverse
forced P_X and P_XX; independent higher jets are not adjustable health knobs.
`triple_seed.py` now solves two further compatibility conditions by changing
the second and third initial accelerations. A selected three-mass seed is:

```
epsilon = (1e-6, 2e-6, 1.5e-6), X=.5, P=0, b=.25
y = (.1, .21527977962234623, .1437148859287078)
P_X = 11557.20329234368
P_XX = 35292030149.17402
G_X = -55.16072193548242
G_XX = 12766762.122112215
```

All three share the displayed jets and pass the local scalar energy/cone
tests at this point. The 40-attempt initial grid found 17 equation roots and
4 healthy roots (not a complete root classification; duplicate roots possible).
The actual fitting Jacobian is evaluated, not assigned an expected rank.

**Next preservation fails.** At b=.25 the next scaled directional residual is
about 5.89331469. Evolving the actual equations to `t=(X-.5)/epsilon_1=.05`
gives a relative h=G_X/P_X mismatch about `1.35675e-4`. Using the FIRST halo's
G_X and G_XX in every halo's stress, rather than giving the third another action,
produces a third-halo normalized metric residual about `6.76625e-5`; the first
two remain below `2.1e-15`. Half-step runs check numerical reproducibility.
Positive coefficients of an off-shell third profile do not certify a solution.

`structure/STRUCTURE.md` gives the exact preservation hierarchy. With
`F_i=a_i+kappa b_i`, `kappa=P_X`, `A_i=a_i-a_1`, `B_i=b_i-b_1`, define

```
K_i=A_i B_2-A_2 B_i,
Q_i=(c_i-c_1)B_2-(c_2-c_1)B_i,
c_i=D_kappa a_i+kappa D_kappa b_i.
```

On the stated regular chart,

```
D_kappa K_i=Q_i+(D_kappa B_2/B_2)K_i.
```

Solving K=Q=0 at a point is insufficient: Q must itself be preserved. When h
and h_X match, the mismatch in G_XXX is `P_X Delta(h_XX)`; a common freely chosen
P_XXX cancels and cannot repair it. These algebraic implications are partially
formalized in `CompatibilityAlgebra.lean`, with the field-theory bridge stated
outside Lean. This is not a universal no-go for all branches or disjoint X ranges.

## 2. A distinct explicit action, varied rather than a phantom stress ansatz

The new physical-metric action is

\[
S=\int d^4x\sqrt{-g}\left[F(X)R+
\frac{3F_X(X)^2}{2F(X)}\nabla_\mu X\nabla^\mu X+
P(X)-G(X)\Box\phi\right]+S_m[g,\psi],
\qquad X=-\tfrac12\nabla_\mu\phi\nabla^\mu\phi.
\]

The implemented first case is `F=(1+sigma X)/2`, sigma>0, m=c=a0=|q|=1.
F is the entire Ricci coefficient. A constant vacuum term may be included in
P but is not selected by the galaxy inverse. We do not graft an earlier model's
FLRW solution onto these newly reconstructed functions.

Introduce independent chi and `lambda(X-chi)` only to vary the F sector. Put
`K=3F_X^2/(2F)`. Its equations give

\[
\chi=X,\qquad \lambda=E_\chi=F_XR-K_X(\nabla X)^2-2K\Box X,
\]
\[
E^{F}_{\mu\nu}=F G_{\mu\nu}+(g_{\mu\nu}\Box-\nabla_\mu\nabla_\nu)F
+K X_\mu X_\nu-\tfrac12g_{\mu\nu}K(\nabla X)^2
-\tfrac12E_\chi\phi_\mu\phi_\nu.
\]

The metric equation is `2 E^F=T_KGB+T_m`; the scalar equation is

\[
\nabla_\mu J^\mu_{\rm total}=0,\qquad
J^\mu_{\rm total}=(P_X+E_\chi-G_X\Box\phi)\nabla^\mu\phi
-G_X\nabla^\mu X.
\]

All signs and factors were independently checked using covariant variation and
the static reduced action before imposing the radial gauge. The mixed equation
is `E^r_t=-q J^r_total/2`; a static vacuum exterior with q!=0 therefore requires
TOTAL current zero, not the old KGB current separately. Full derivations are in
`structure/DERIVATIVE_CURVATURE_VARIATION.md` and `extension/REPORT.md`.

Ordinary matter conservation follows separately from its physical minimal
coupling: on the ordinary-matter equations, a diffeomorphism generated by xi
gives `delta S_m=integral sqrt(-g) T^{mu nu} nabla_mu xi_nu`. Integration by
parts for compactly supported xi gives `nabla_mu T_m^{mu nu}=0`. This does not
require matter-plus-clock conservation to be substituted for baryon conservation.
It assumes a diffeomorphism-invariant ordinary matter action and matter on shell;
no nonmetric baryonic force is added here.

## 3. Static construction and what the target does NOT establish

Use `ds^2=-A dt^2+B dr^2+r^2 dOmega^2`, `phi=-t+psi(r)`,
`g=A'/(2A)`, `p=psi'`, `U=p^2/B=1/A-2X`, `z=X'`. Impose the target exterior

\[
\mu(y)=1-e^{-y},\quad r=\frac{\epsilon}{\sqrt{y\mu(y)}},\quad
g=\frac{y}{1-2ry},\quad B=1+2rg.
\]

This is the prior Schwarzschild-like relativistic completion of the prescribed
spherical law. In the weak field g approaches y. The mass parameter epsilon is
NOT independently matched to an interior baryonic source here. The full
nonspherical MOND PDE, measured Newton constant, and mass-normalization map are
not derived by imposing this exterior. The numerical profile is a construction
target, not an empirical prediction or an independent confirmation of MOND.

The independently varied radial equation gives

\[
P=\frac{2F_Xz(g+2/r)+Kz^2}{B}.
\]

The metric components give `Phi'=g` and `Psi'=(B-1)/(2r)` at leading metric
order. Substitute the independently derived B equation to evaluate the spatial
potential. If the conformal sector is ALSO perturbative, with `rF'/F` and
`r^2P/F` of the same weak-field order as rg, this simplifies to

\[
\Phi'=g,\qquad
\Psi'=g+\frac{F'}F-\frac{rP}{4F}+O(\text{higher weak-field orders}).
\]

In that simultaneous expansion, leading no-slip requires `P=4F'/r`, the leading
part of the displayed exact radial condition for B=1+2rg. This simplification
must not be used when large auxiliary-sector terms cancel in the exact radial
equation; the long outward run below approaches such a regime. The B profile
is imposed in this inverse; its field
equations are then checked. It is not a derivation that arbitrary sourced
solutions dynamically select that branch. Equality of these leading gradients
with matched boundary constants is not a full PPN gamma calculation. Beta and
the preferred-frame parameters remain uncomputed for these functions.

## 4. New solvable inverse and a removable fold

The pressure chart solves radial preservation, total current and density for
`X'',P_X,G_X`; it first eliminates X'' and solves an actual 2x2 linear system.
P_XX and G_XX are total derivatives along the resulting radial trajectory, not
inputs chosen to pass stability. A separate implementation retains z as a state
and solves the original 3x3 system directly. See `gradient_inverse.py` and the
exact system in `structure/test_conformal_inverse_structure.py`.

Let f=F_X, a=g+2/r. The independently COMPUTED determinants are

\[
\det M_2=\frac{2z(2X+U)}{pr\,[a+3fz/(2F)]},\qquad
\boxed{\det M_3=\frac{4fz(2X+U)}{Bpr}}.
\]

The pressure fold `a+3fz/(2F)=0` is removable by the z-state formulation.
In particular `Z=U/X-rg=0` is not a singularity of this new inverse. These are
radial ODE inversion matrices, **not Poisson-bracket matrices or DOF counts**.
The second quadratic root is not eliminated by insisting on a positive square
root. A direct fold control solves the full equations; it is not claimed healthy.

There is also a genuine conditional obstruction: for finite coefficients,
f!=0, F!=0, regular B,p,r and a!=0, setting z=0 first forces P=0; preservation
forces z'=0; the density equation then forces rho_geom=0. But the target has

\[
\rho_{\rm geom}=\frac{4y^2e^{-y}}
 {r(1-e^{-y}+ye^{-y})}>0\quad(y>0,r>0).
\]

Therefore a smooth solution of this fixed no-slip inverse cannot reach z=X'=0
at finite positive y. This means the radial gradient of the CLOCK NORM X, not
the radial field gradient p. It does not exclude the other P=0 root
`z=-4Fa/(3f)`, singular coefficients, another metric branch, or another theory.
`ConformalInverseAlgebra.lean` proves the conditional determinant nonvanishing,
matrix invertibility, zero-density implication and exponential-density positivity.
The explicit matrix identity and variation-to-algebra bridge remain SymPy/prose,
not silently assumed to be a fully formalized field theory.

The angular metric component is directly assembled from the variation, but the
independent audit proves it is algebraically dependent on the three solved
equations. Its small residual is an implementation cross-check, NOT a fourth
independent physics gate. The precise residual combination is in the structure
audit; no extra physical evidence is counted twice.

## 5. Stability tested from this action and its actual background

For C=2F=1+sigma X, chi=X/C, the regular conformal map has `C-X C_X=1`.
The action maps to Einstein-frame KGB with the derivatives in
`extension/EF_PRINCIPAL.md`; the scalar Hessian is transformed too. Reusing the
old physical-frame principal unchanged would be wrong. The helper evaluates
the original coupled scalar/metric principal, including Ricci elimination.

Under that regular vacuum equivalence the known class has the luminal tensor
structure, with positive Ricci coefficient F. This is not a full new nonlinear
Dirac analysis or a certificate for the matter-containing transformed system.
An Einstein-frame static quadratic-energy test is also not a proof of a bounded
physical-frame nonlinear Hamiltonian. Strong coupling and boundary data remain.

The 320-point scan has 110 points passing the stated EF energy/strict-cone test.
All metric residuals in that scan are below `4.7e-10`; independent high-precision
checks distinguish floating-point cancellation from an equation defect.
These are many DIFFERENT initial local inverse data, not one global theory.

For one selected branch `(epsilon,y0,sigma,b,d)=(1e-6,.1,.1,.25,1.5)`,

```
P=-2926.54065677, X'=-.150000307531
principal C00=3.83965958898e10, C11=-8579.4779184,
C22=-28280.8013003, C01=19422368.7919
```

`conformal_flow.py` evolves X,U,P,G together and stops at an energy/cone boundary.
The inward run reaches C22=0 at `y=0.14041695259`, before the requested y=1.
Pressure and gradient formulations and half-step runs agree on this boundary.
The boundary is not a healthy endpoint just because rounding leaves a tiny
negative C22. The first 18 attempted decade continuations are bounded tests of
selected seeds, not a parameter-space no-go. Full results and accepted-step
counts are in the suite output. New P/G functions are not chosen at each step.

The sigma=.1 branch survives the first outward decade. Immediately extending
the SAME action toward y=1e-5 finds a further EF boundary at
`y=0.00014074400653`, checked with half steps. Thus this selected construction
has a substantial bounded deep-MOND exterior interval; its inward instability
still prevents continuation through the transition to Newtonian accelerations.
The sigma=1 comparison reaches an outward boundary already near y=.0989707.
These are not a y=0 treatment, common-mass solutions, or empirical validations.

## 6. Concurrent L119: useful direction, unsupported health certification

Read and run the actual code from `3b41b064a`, not just its six PASS labels.
The elliptic-field direction remains worth testing. Three implications in its
health claim are not established by the computations it runs:

1. A spatial-gradient lapse Hessian is not a lapse time-kinetic Hessian.
2. A lapse multiplying a Hamiltonian linearly does not alone make the resulting
   constraint first class. Our explicit L=`qdot^2/2-Nq` counterexample derives
   primary p_N=0, then q=0, p_q=0, N=0, then fixes the multiplier. Its actual
   antisymmetric bracket matrix is nonsingular, with computed rank4, no
   first-class constraints and zero DOF. Nothing about that example's rank is
   passed as a preassigned answer to the calculation.
3. For its displayed F(p,s)+W(gs^2), unchanged H_p does not imply unchanged
   H_p H_s. The missing term is
   `2 g^(3/2) p s^2 W'(g s^2)/sqrt(p^2-mg)`.
   Taking W(u)=u, (p,s,g,m)=(2,1,1,1) gives `4/sqrt(3)`, not zero.

`l119_scope.py` computes these results. The single-field expression in L119
does not itself represent a completed separate-field constraint algebra either;
that full system must be supplied. No claim is made that every elliptic MOND
architecture fails. L119's passing derivative identities do not certify its
stated health gates.

## 7. Exact next calculation, not a claim that the finish line was reached

Continue in gradient variables and test **one universal F,P,G**, not individual
local jets: first preserve common action derivatives for different masses over
an interval while retaining actual EF energy/cone conditions. Affine F is a
restricted first family; the fold is now accessible without a fake singularity.
If non-affine F is introduced, derive its extra terms rather than importing this
affine inverse. In either case, impose physical source and common cosmological
boundary data before identifying epsilon with baryon mass.

The remaining full-theory gates are still open: complete primary/secondary and
higher Dirac preservation and Poisson matrix (k=0 separate); measured G and
interior/nonspherical MOND sourcing; beta/gamma/alpha PPN; FLRW and its scalar,
vector and tensor perturbations for THESE functions; physical-frame constrained
energy, strong coupling and y=0; empirical clusters/binaries/CMB constraints;
and any first-principles a0-Lambda coefficient. Lean algebra is not a proof that
an untested theory is a law of nature. Neither the selected instability nor the
compatibility failure is promoted to a universal impossibility result.

## Reproduction and evidence

Run `python3 -B qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/run_suite.py`
from the repository. It emits exact argv, working directories and exit statuses
for every important test and runs the previous closure suite afterward.
`audit_contract.json` and `run_002/manifest.json` record explicit inputs, hashes,
software, resource limits and bounded output. Individual independent audits have
their own manifests. `EXECUTION.md` records final verification and development
failures. A zero suite exit is a reproducibility result, not gravity closure.
The initial full `run_001` exposed a test-runner import collision after physics
tests modified sys.path. Its failed record is retained; the test now loads its
runner by explicit filename. That test-only revision supersedes its old hash.
