# Same-action closure: shared nonlinear data and an analytic causal obstruction

2026-09-06. Continuation of `METRIC_STATIC_BACKGROUND.md`; no kernel change,
new fit, empirical dataset, or claim of historical novelty.

**Result:** two gaps in the earlier initial-curvature calculation are narrowed
substantially. We construct exactly shared nonlinear gravitational constraint
data for two positive-energy matter states, and solve their common first
multiplier-preservation problem. An analytic small-slab argument proves a
nonzero exterior curvature coefficient without relying on a numerical rank.

**Status:** the candidate remains **OPEN as a complete nonlinear theory**, with
a conditional no-go for its regular finite-speed branch. The condition is
not cosmetic: higher boundary compatibility and coupled smooth evolution have
not been established. A passing algebra test is not a passing gravity theory.

## 1. Claim and assumptions

Keep the same explicit Hamiltonian, with c=1 and the common gravitational
normalization absorbed into the matter fields:

\[
H=\int_\Sigma\!\left[N\mathcal H_{GR}+N^i\mathcal H_i
-2N\sqrt h\,a_0^2F(a^2/a_0^2)
+\lambda(\pi-\sqrt h\,\bar\pi)\right]d^3x+H_m,
\]
\[
\mathcal H_{GR}=\frac{\pi^{ij}\pi_{ij}-\pi^2/2}{\sqrt h}
-\sqrt h(R^{(3)}-2\Lambda),\qquad
F(z)=2[1-(1+\sqrt z)e^{-\sqrt z}],
\]
\[
a_i=D_i\log N,\qquad \bar\pi=\frac{\int\pi}{\int\sqrt h}.
\]

The already varied static equations are imported from
`metric_static_background.py`, not replaced by phenomenological equations.
Their weak-field constitutive function is the user-requested exponential
AQUAL law. The original repository's other interpolation prescriptions are
not silently identified with it.

The restricted setting is a finite slab times a transverse torus,
\(\Sigma=[-L,L]\times T^2\), with zero shift and the Dirichlet gravitational
boundary completion specified in the preceding report. Use a smooth static
vacuum background
\(ds^2=-N_0(z)^2dt^2+dz^2+A_0(z)^2(dx^2+dy^2)\), normalized to
\(N_0(0)=A_0(0)=1\), on the positive-field branch. Put

\[
y_0=(\partial_z\log N_0)(0)/a_0>0,\qquad
\chi=(1-y_0)e^{-y_0}\ne0,\qquad m=1-\chi>0.
\]

The background must exist with a real constrained seed; not every arbitrary
choice of y0 and Lambda meets this condition. Small enough L is understood.
The coefficient m is the *longitudinal ellipticity eigenvalue*, not the
interpolation function \(\mu(y_0)\).

**Conditional no-go statement.** Suppose this boundary theory admits the
shared matter/gravity data constructed below for both amplitude families
in a neighborhood of epsilon=0, with common compatible wall data. Assume
plane-symmetric coupled evolutions, sufficiently smooth in time and C² in
matter amplitude in a topology controlling the time/spatial derivatives
used in the curvature and twice-differentiated constraints. In particular,
the differentiations used below must commute. Suppose physical curvature
has a finite domain of dependence. These properties cannot all
hold: the same equations force a nonzero initial curvature difference in a
region where the full canonical initial data of the pair agree.

This excludes the conjunction of regular admissibility and finite-speed
evolution under these assumptions, not every possible completion or every
MOND action. The symmetry condition would follow from uniqueness and
symmetry-preserving boundary dynamics, but these are not proved here.
In particular, an admissibility restriction could invalidate
the premise rather than produce the same causal counterexample.

## 2. Derive the shared matter sources

Use three minimally coupled canonical KG fields with masses 1,2,3 in the
dimensionless calculation; these are explicitly counted ordinary matter,
not auxiliary gravitational scalars. Their action is

\[
S_m=-\frac12\int\sqrt{-g}\sum_i
[(\partial\phi_i)^2+m_i^2\phi_i^2]d^4x.
\]

Let \(r=(1,1/2,1/3), v=(1,1,1), U=(1,-2,1)\). On any common spatial
geometry prescribe

\[
\phi_\pm=\epsilon r,\qquad
\Pi_\pm:=p_{\phi,\pm}/\sqrt h=\epsilon(v\pm U\sigma(z/L)).
\]

Here \(\sigma\in C_c^\infty((-1/3,1/3))\) is even, nonnegative and nonzero;
its physical support after composition with z/L is |z|<L/3.
Direct evaluation of the KG stress gives, for *each* state,

\[
\rho=3\epsilon^2(1+\sigma^2),\qquad
p=3\epsilon^2\sigma^2,\qquad S=3p=9\epsilon^2\sigma^2,
\qquad J_i=0.
\]

The two states also have the same first stress derivatives. In the normal
derivative convention \(K=\nabla_\mu n^\mu\), at the initial spatially
constant phi,

\[
\partial_n\rho=-K\epsilon^2(3+6\sigma^2),\quad
\partial_n S=-3K\epsilon^2(3+6\sigma^2)-36\epsilon^2.
\]

These identities are computed from KG, including the mass matrix. The
matter Ward identity remains
\(\nabla_\mu T^{\mu\nu}=\sum_i(\Box\phi_i-m_i^2\phi_i)\nabla^\nu\phi_i\).
No prescribed nonconserved stress is used. A model admitting only a more
restricted matter sector is outside this particular test's assumptions.

## 3. Exact common nonlinear gravitational constraint data

Set \(h_\epsilon=e^{2Q}h_0\), \(N_\epsilon=N_0e^V\),
\(\pi^{ij}=0\), with Q=V=0 at both walls. Thus the momentum and
mean-subtracted trace constraints hold, including \(\bar\pi=0\).
Do not infer that the geometry remains static.

With the ungauged variational derivatives E_N,E_A,E_B from the static
action, define

\[
E_\ell=E_N/(A^2B),\qquad
E_\tau=(AE_A+BE_B)/(NA^2B).
\]

Solve the lapse constraint and first preservation of the trace constraint:

\[
E_\ell=\rho,\qquad E_\tau+S=2d/N_\epsilon,
\qquad d=\dot{\bar\pi},
\]
\[
\int_{-L}^{L}A_0^2(e^{3Q}-1)\,dz=0.
\]

The homogeneous d is an unknown solved together with the two initial
shooting slopes; it is not set to zero. Fixing the initial volume selects
one family of data, rather than eliminating homogeneous cosmological
evolution. All nonlinear exponentials and background derivatives are
retained. The code checks all twelve entries of the linearization against
the preceding independently constructed variational operator.

**Existence argument.** At epsilon=0, Q=V=d=0 is the vacuum solution.
At a fixed sufficiently small L the three-dimensional endpoint-and-volume
Jacobian is invertible by section 5. The nonlinear spatial equations have
an invertible highest-derivative matrix near that vacuum. They therefore
give a smooth first-order shooting system. Its solution and endpoint map
depend smoothly on the slopes, d and epsilon squared. Local inversion of
this finite-dimensional endpoint map gives exact common solutions for
sufficiently small epsilon. Positivity of N,A,y follows by continuity.
Precisely, for a fixed regular seed there is L0>0 such that for every
0<L<L0 there is epsilon0(L)>0 with this construction for
|epsilon|<epsilon0(L). No uniform epsilon0 or explicit certified L0 is
claimed. This is an existence statement for the constraints, not a theorem of
coupled time evolution. Numerical values at specified finite epsilons are
floating-point checks, not interval-certified realizations of its bounds.

## 4. Preserve the constraints at fixed canonical matter momenta

A common-data shooting derivative holds normal matter velocities fixed.
That is **not** the Poisson variation. Let
\(\dot h=2w h\), \(\dot N=Nv\) at gravitational pi=0, and put
\(X=\sum_i\Pi_i^2=\epsilon^2(3+6\sigma^2)\).
At fixed canonical p_phi, a conformal change gives

\[
\delta\rho=-3Xw,\qquad \delta S=-9Xw.
\]

The script obtains these terms by differentiating \(\Pi^2\mapsto e^{-6w}\Pi^2\).
If \(\mathcal L_\ell,\mathcal L_\tau\) are the gravitational linearizations
on the *nonlinear* common geometry, the true first-preservation equations are

\[
\mathcal L_\ell[w,v]+3Xw=0,
\]
\[
\mathcal L_\tau[w,v]-9Xw+\frac{2d}{N}v
=36N\epsilon^2+\frac{2\dot d}{N},\qquad
\int\sqrt{h_\epsilon}\,w=0.
\]

Use w=v=0 at both walls. The free canonical KG time flow contributes
\(\dot\rho=0,\dot S=-36N\epsilon^2\); that is the source of the RHS,
not a chosen multiplier. The solution supplies common
\(\lambda_{\rm eff}=2w\), \(\dot N=Nv\), and \(\dot d\) for both states.
Gravitational momentum terms in these scalar constraints are quadratic,
so their first time derivatives vanish at pi=bar pi=0 even though pi_dot
need not vanish.

The code integrates the three homogeneous columns, computes the actual
boundary matrix and singular values, and solves for their weights. It
checks differential residuals using dense-output finite differences and
compares two independent integrators. It also tests the fixed-p derivative
directly against finite differences of the nonlinear constraints.

**Dirac interpretation and limit.** On the mean-free conformal sector,
p_N and the trace generator produce precisely lapse and volume-preserving
conformal variations. Consequently their weak Poisson pairing with the
lapse and projected-trace equations is this J, up to invertible density
normalizations and a sign. Projection creates no omitted term: its
variation acting on the on-shell spatial constant 2d is zero.
At epsilon=0 the boundary inverse in section 5 applies. The additional
fixed-p terms and the changed volume weight are smooth small perturbations
at fixed L, so the local inverse persists for small epsilon.

With suitable adjoint domains the scalar pairing has block form
\(\bigl(\begin{smallmatrix}0&J\\-J^*&K_*\end{smallmatrix}\bigr)\)
weakly; if J and its adjoint are invertible, its kernel is zero independently
of the uncomputed block K_*. This explains why these preservation equations
locally fix the effective multiplier and lapse velocity instead of imposing
a new local KG restriction. It is **not** an evaluation of the entire
nonlinear functional Poisson matrix, nor a first/second-class count for
the full three-dimensional theory. The subsequent canonical constraint
fixing lambda would pair with mean-free p_lambda; the spatially constant
lambda is a spectator gauge variable because the integrated trace
constraint vanishes identically. Do not count that constant as second class.

## 5. Analytic inverse and exterior tail

Return to the leading order-epsilon-squared *difference* experiment of
`metric_initial_response.py`. Delta denotes half the difference with that
overall amplitude removed. The independently derived KG jets give
\(\delta\ddot\rho=0\), \(\delta\ddot S=-24N_0^2\sigma\).
Write \(\delta\ddot h=2w h_0\), \(\delta\ddot N=N_0v\) and
\(c=\delta\bar\pi'''\). All common order-epsilon-squared initial-data
and first-multiplier corrections cancel from this leading difference.

Set z=Lx, w=L²W, v=L²V. The exact variational operator has the small-L limit

\[
-4(W''+\chi V'')=0,\qquad
-4(W''+V'')=24\sigma+2c,
\]

with W=V=0 at x=±1 and \(\int_{-1}^1W=0\). Primes here mean x derivatives.
Integrating the three homogeneous shooting columns (initial slopes a,b
and c) gives the computed endpoint-and-mean matrix

\[
M_0=\begin{pmatrix}
2&0&\chi/m\\
0&2&-1/m\\
2&0&2\chi/(3m)
\end{pmatrix},\qquad
\boxed{\det M_0=-\frac{4\chi}{3m}\ne0.}
\]

This matrix is derived from the action's highest-derivative coefficients;
its determinant and the rank-two degeneration at chi=0 are calculated.
The point y0=1 has chi=0 but is **not** the whole GR theory: the radial
leading operator alone degenerates there. The y0=0 limit also has m=0.
Neither exceptional sector is certified by this argument.

Let \(P=(-\partial_x^2_D)^{-1}\sigma\),
\(M=\int_{-1}^1(1-s^2)\sigma(s)ds\), and
\(M_s=\int_{-1}^1\sigma(s)ds\). The Dirichlet Green kernel gives
\(\int P=M/2\). Solving the mean condition gives, exactly,

\[
c=-9M,\qquad
V=\frac{6P-\frac94M(1-x^2)}m,\qquad W=-\chi V.
\]

For even sigma and x>1/3, P=(1-x)M_s/2. Since M>=8M_s/9>0,

\[
W(3/4)=\frac{\chi(63M-48M_s)}{64m},\qquad
\boxed{|W(3/4)|\ge\frac{|\chi|M_s}{8m}>0.}
\]

This is an exterior value of W itself, not merely an exterior derivative.
The full initial-curvature identity, computed from the time derivatives of
the connection in the preceding script, is

\[
\delta R_{\mu\nu}n^\mu n^\nu=-3w/N_0^2.
\]

Thus the observable is curvature, not an instantaneous gauge lapse.

**Lift to the variable-coefficient problem.** The vacuum background is
smooth around z=0. On x in [-1,1], N0(Lx),A0(Lx) converge uniformly to one;
the highest-derivative coefficients converge to the displayed invertible
matrix, while the lower derivative terms acquire factors L or L². The
weighted mean and forcing likewise converge. After solving for the highest
derivatives, the first-order integral equations for each homogeneous column
and the particular solution have uniformly bounded coefficients. Subtract
their limiting integral equations and iterate the resulting integral bound;
the exponential series bounds the difference by a constant times the
coefficient difference. Hence the columns and endpoint matrix converge
uniformly. Nonzero det M0 gives a bounded inverse for all sufficiently
small L, and the forced solution converges uniformly as well. The strict
exterior bound survives, for example with half its limiting magnitude.

This proves existence of a small-L family with a nonzero curvature tail;
it does not specify an interval-certified numerical threshold L0. Similarly,
for fixed small L, smooth amplitude dependence makes the nonzero leading
epsilon² difference survive at sufficiently small nonzero epsilon. Finite
domain of dependence would instead require exactly equal curvature in
the exterior, including the initial slice. This is the contradiction in
the conditional statement of section 1.

## 6. Boundary contract and remaining work

The constructed KG pair does not obey time-independent homogeneous
Dirichlet or Neumann wall data: at the walls sigma=0 but phi_dot=N epsilon v
is nonzero, and its normal spatial derivative generally is too. Shared
time-dependent matter boundary values with the required corner jets must
be specified, or another explicit compatible wall formulation supplied.
At higher common gravitational orders, pi_dot need not vanish; its terms
must be included in the wall multiplier jets. The *difference* second-jet
wall conditions used above remain homogeneous because initial pi_dot agrees.

The next unavoidable calculation is that higher shared wall/coupled
compatibility problem, or a boundary-independent version of the same
counterexample. Failure there must be reported as an admissibility failure,
not silently assumed away. No full nonlinear Dirac count, PPN beta/alpha_i,
global FLRW perturbation certificate, or zero-field strong-coupling control
is obtained here. The framework input Lambda=32 pi a0² is allowed in one
numerical case, not derived. The result is not an empirical exclusion or a
new observed Kepler law.

## 7. Reproduction and exact changes

Five new files; no previously published audit artifact modified:

- `metric_shared_data.py`
- `test_metric_shared_data.py`
- `metric_shared_data_results.json`
- `metric_shared_data_manifest.json`
- `METRIC_SHARED_DATA.md` (this report)

From the repository root, the important commands are:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_metric_shared_data.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_shared_data.py --output qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_shared_data_results.json
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_initial_response.py --require-local-initial-curvature
python3 -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/2.2.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/g03_global_kernel_bridge_2026/metric_shared_data_manifest.json
git diff --check
```

The red-first runs exited 1 for missing implementations/fields. Completed
new tests: seven pass, exit 0. Relevant suite: 69 pass, exit 0. The new
standalone audit exits 0 for its seven mathematical consistency checks.
The existing **physical causal gate exits 2**, correctly rejecting locality
in its tested response problem. This failure is not relabeled a PASS.
Manifest validation and whitespace checks are recorded with their actual
statuses in the manifest after running them.

Four numerical shared-data cases use (y0,Lambda/a0²,L,epsilon) equal to
(0.5,0,0.02,0.02), (0.5,0,0.02,0.01),
(10.5,32pi,0.002,0.05), (10.5,32pi,0.002,0.025).
Maximum normalized nonlinear constraint residual is below 9.4e-10;
the independently integrated common-preservation boundary matrices all
have computed rank three. Detailed unrounded outputs, tolerances and
residuals are in the JSON. This is deterministic floating-point evidence,
not a universal proof from four samples.

The latest inspected repository commit, `ebc6b0570`, withdraws the separate
g03o/g03q dust-collapse window as unconverged. Nothing here relies on that
window or upgrades its status. Unrelated working-tree changes are preserved.
No commit or push is performed by this continuation.

Proof audit: the assumptions above were retained after independent review
of the source signs, fixed-canonical variation, scaling and boundary caveat.
Math proofreading covers this new report only; no earlier mathematical
tokens were changed. No external theorem or novelty search was required
for the explicit finite-dimensional argument; no novelty priority asserted.
