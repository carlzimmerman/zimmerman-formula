# XC2 independent mathematical audit — 2026-09-26

**Normalized claim.** For the C-H/K action on smooth compact connected closed
leaves, with any smooth positive lapse, XC2 claims that (a) every listed kernel
with `C_min > -1` gives a strictly convex auxiliary energy and exactly one leaf
solution; (b) heat filtering removes the MOND sector from the full nonlinear
principal symbol; and (c) its zero-field behavior is Lipschitz at generic zeros
and Osgood-controlled at the remaining planar zeros. Thus only the nonlinear
khronometric strong-hyperbolicity question is said to remain.

**Primary verdict: refuted, with an admissible counterexample.** The weighted
convexity implication (a) is false for both requested nonmonotone branches,
`nu_RAR` and exact `mu_exp(x)=1-exp(-x)`, on the stated domain. The universal
zero-field conclusion (c) is also false: the admitted homogeneous background
has an amplitude response proportional to the square root of the perturbation,
including after the outer heat filter. This does **not** refute nonlinear
wellposedness itself; it refutes XC2's claimed reduction to only one remaining
question. The full-symbol conclusion (b) is incomplete.

This review uses direct reconstruction from ACTION.md, not its dashboard or
the lane's PASS flags. The existing weighted counterexample was located in
`real_research/closure_doors_2026_09_26/auxiliary/weighted_heat_check.py` and
`auxiliary/run2/results.json`; it is credited as prior work and independently
corroborated here. The specific XC2 overclaim remains in the inspected source.

## Sources and claim locators

Observed base commit: `f3b848273e635b81bc328882db0ffb4206d86e45`, with unrelated
dirty/untracked work. The computation manifest pins hashes before/after its
run because the repository is actively changing. No source/result file outside
this review directory was edited or executed; no commit was made. No applicable
AGENTS.md or `.mathbox` ledger was found in the inspected paths.

- `real_research/extra_crispy_2026/XC2_wellposedness_scoping.py`: normalized
  claims at 8–44, B3 at 191–196, B4 at 276–279, B5 at 316–319, B6 at 332–336,
  B7 at 377–382, final scope at 384–391.
- `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md`:
  domain 24–34; filter measure 71–84; original exact exponential kernel 86–93;
  action 95–106; weighted adjoint and elimination 134–164; metric heat
  variation 217–228.
- `real_research/g03_audit_2026/L340_filtered_khronon_completion.py`:
  candidate action 8–16; monotone branch 102–134; explicit zero-gradient
  singularity caveat 60–63.
- Prior weighted evidence: `real_research/closure_doors_2026_09_26/auxiliary/weighted_heat_check.py`
  26–61 and `auxiliary/run2/results.json`.

## Reconstruction and dependency graph

Write `dV=dvol_h`, `a=D ln N`, `b=xi^2/2>0`, and `S=exp(b Delta_h)`,
self-adjoint in `L2(dV)`, not generally in `L2(N dV)`. Eliminating W and L
gives the genuine fixed-(h,N) functional

```
E(U) = integral N [2 |DU-a|^2 + Q(DSU)] dV,
Q(p) = 2 alpha_M^2 q(|p|^2/alpha_M^2).
```

At `p != 0`, let `y=|p|/alpha_M`, `h(y)=y(nu(y)-1)`, and `e=p/|p|`.
Direct differentiation, without a polynomial proxy, gives

```
DQ(p) = 4 (nu(y)-1) p,
D2Q(p) = 4 C(p),
C(p) = C_T I + (C_L-C_T) e tensor e,
C_T = h(y)/y,  C_L = h'(y).

delta2 E(U)[v,v] / 4
  = ||Dv||_N^2 + integral N <DSv, C(DSU) DSv> dV.
```

The unweighted Hessian operator is
`4[-div(N D) + S(-div(N C D))S]`. Multiplying by `N^-1` expresses the
gradient/Hessian in the weighted Hilbert space. ACTION.md 148–155 already
states `S^dagger_N=N^-1 S N`.

The dependency chain is:

1. Action and heat endpoint equations -> this weighted energy: **passed**.
2. Differentiating Q away from zero -> eigenvalues `4 C_T`, `4 C_L`: **passed**.
3. Spectral heat definition -> **unweighted** Dirichlet contraction: **passed**.
4. Unweighted contraction -> claimed contraction with independent weight N:
   **failed**.
5. Weighted second-variation lower bound -> strong convexity -> unique
   minimizer: **conditional** on a valid bound and the functional setting.
6. Fixed-(h,N) U-Hessian smoothing -> full metric/clock reduced principal
   symbol: **not established**.
7. Quadrature for one simple-zero profile and one translation direction ->
   regularity for all filtered configurations -> evolution uniqueness:
   **failed at the first extension; later implication not established**.
8. Decoupled scalar cone -> full nonlinear strong hyperbolicity:
   **not established**, as XC2 partly acknowledges.

## Finding 1: the lapse weight invalidates B3 for both target branches

XC2 B2, 128–165, diagonalizes the Laplace–Beltrami operator and proves
`||DSv||_dV <= ||Dv||_dV`. Its random matrix experiment represents this same
metric Dirichlet form. There is no independent lapse N in that proof.
Nevertheless, 19–21 and 191–196 apply the statement in the N-weighted norm.

The previously recorded exact counterexample is already enough to break that
implication. On a flat circle, or T3 with two spectator coordinates, take

```
N(x) = 1 + (4/5) cos(9x) > 0,
v(x) = sin x - sin(10x)/50.
```

Fourier orthogonality gives

```
||D S_b v||_N^2 / pi
 = exp(-2b) + exp(-200b)/25 - (4/25) exp(-101b).
```

Its value at zero is `22/25`, and its derivative there is `154/25 > 0`.
The weighted heat energy increases. This example stays inside ACTION.md's
closed smooth domain and uses a positive smooth lapse.

The failure is substantive for the actual kernels, not just for the estimate.
For the exponential branch use the distinct physical acceleration variable
`x=g/a0`, source `y=x(1-exp(-x))`, and

```
C_L = (1-x)/(exp(x)+x-1),
min C_L = -1/(exp(2)+1) > -1, attained at x=2.
```

For RAR, using the source variable y directly,

```
h_RAR(y) = y/(exp(sqrt(y))-1),
C_L = 1/(exp(sqrt(y))-1)
      - sqrt(y) exp(sqrt(y))/(2(exp(sqrt(y))-1)^2).
```

In particular `C_L(6)<0`. These are different laws; no conversion of the
RAR source argument to the exponential physical-acceleration argument is made.

A rigorous counterexample family can be read directly from the second
variation. Set `b=0.02`, `v=sin x-sin(10x)/10`, and choose `U` so
`DSU=y0 cos x`, with `y0=2(1-exp(-2))` for the exponential branch, or `y0=6`
for RAR. Choose

```
N_A = exp(-A) + exp(A(cos x-1)),  A -> infinity.
```

At x=0, `Dv=0`, `DSv=exp(-b)-exp(-100b) != 0`, and `C_L(y0)<0`.
The weighted negative term is order `A^(-1/2)` by concentration near zero;
the positive local-gradient term is order `A^(-5/2)`, since
`Dv=(99/2)x^2+O(x^4)`. The positive floor contributes only `O(exp(-A))`;
the square-root constitutive singularities at the zeros of cos x are
integrable and do not change this conclusion. Thus `delta2 E<0` for all
sufficiently large A. Every individual `N_A` is smooth and strictly positive.

The independently implemented adaptive quadrature also checks the prior
finite exponential witness `N=1e-8+exp(1000(cos x-1))`, and the analogous RAR
witness, with refinement. The exponential value is approximately
`-0.02522828924`, and the RAR value is `-0.005240714245`. Tightening quadrature
tolerances from `1e-8` to `1e-10` changes these values by about `3.2e-11` and
`1.4e-11`, respectively. These numerical values corroborate the continuum
concentration argument; quadrature error estimates are not interval certificates.

**What survives.** A correct elementary estimate is

```
||DSv||_N^2 <= (Nmax/Nmin) ||Dv||_N^2,
delta2 E >= 4[1 + min(0,Cmin)(Nmax/Nmin)] ||Dv||_N^2.
```

Thus the exponential branch has a sufficient uniform-convexity condition
`Nmax/Nmin < exp(2)+1`. For constant lapse, XC2's original bound is valid.
For a genuinely monotone law with `C_T,C_L>=0`, including the intended
continuous nu_mono law, the second term is nonnegative for every positive N:
no weighted heat contraction is needed. Changing S to a lapse-adapted filter
would change the action and is a separate candidate, as the prior work notes.

Negative off-shell curvature of E refutes global convexity; it does not by
itself prove multiple stationary solutions or a physical ghost on shell.

## Finding 2: B7 omits an admitted zero background and degenerate isolated zeros

The local leading deep-MOND flux is
`F(p)=|p|^(-1/2)p`, with `F(0)=0`. Both target branches have this same
leading behavior; their subleading terms differ. Heat filtering is linear.
It neither prevents `U=constant` nor makes every smooth field transverse to
zero. At `U=0`, choose `v=sin x` on flat T3. Then

```
DS(epsilon v) = epsilon exp(-b) cos x e_1,
F(DS(epsilon v)) = sqrt(epsilon) F(DSv),  epsilon>0.
```

Therefore the flux difference divided by epsilon diverges as
`epsilon^(-1/2)`. Nor can it satisfy the claimed Osgood modulus
`epsilon sqrt(log(1/epsilon))`. This is also a counterexample for the actual
outer-filtered nonlinear term: the first sine Fourier coefficient of
`-S div F(DS(epsilon v))` is

```
sqrt(epsilon) exp(-3b/2) (1/pi) integral_0^(2pi) |cos x|^(3/2) dx > 0.
```

The outer heat filter preserves this nonzero mode and the square-root
amplitude scaling. The higher order terms of exact RAR and exact mu_exp do
not cancel it. Thus no ordinary bounded linear tangent exists at this
homogeneous zero background. ACTION.md 90–93 already explicitly warns that
the composite is C1 but not C2; L340 63 retains the cosmological singularity.

Even the blanket wording “isolated zeros” requires a nondegeneracy condition.
For an admissible finite Fourier polynomial take

```
W_b(x1,x2,x3) = [(1-cos x1)+(1-cos x2)+(1-cos x3)]^3,
U = S^(-1) W_b,
```

where the last expression is harmless on this finite Fourier support. Its
gradient has only finitely many zeros on T3, hence isolated zeros, and near
the origin `DW_b=(3/4)|x|^4 x+O(|x|^7)`. Perturb with
`v=exp(b) sin x1`, so `DSv=cos x1 e_1`. On a ball of radius proportional to
`epsilon^(1/5)`, the unperturbed gradient is at most a small multiple of
epsilon while the perturbation is comparable to epsilon. The flux change
is bounded below by a constant times `sqrt(epsilon)` on a fixed fraction of
that ball. Consequently its L2 norm is at least
`c epsilon^(1/2+3/10)=c epsilon^(4/5)`. The quotient by epsilon diverges,
even though the zero is isolated and the field lies exactly in the heat range.

The quadratures at XC2 340–380 only test `p=x` in one dimension and the
nondegenerate identity map `p=(x,y[,z])` in dimensions two and three, under
one rigid translation direction. Their asymptotics are compatible with
those model profiles; they do not establish a Banach-space Lipschitz estimate
for arbitrary variations, uniformity along an evolution, or a differential
inequality to which Osgood's theorem can be applied. In three dimensions a
codimension-two zero is a line, not an isolated point.

This does not prove dynamical nonuniqueness. Convex/monotone methods can
sometimes control nonsmooth equations without classical linearization.
The missing task is an actual estimate for the full evolved variables and
the chosen function spaces, including homogeneous and degenerate zero sets.

## Finding 3: B5 checks one block, not the claimed full principal symbol

At a fixed smooth (h,N) and a background where the constitutive coefficient
defines a suitable bounded operator, the U-U correction
`S[-div(N C D)]S` is spatially smoothing. This is the correct restricted
content of the test. The code at 289–319 actually omits the lapse N from
`mond_lin` and tests only three Fourier cutoffs on one clamped grid background
(`r=max(|DSU|,1e-14)`, line 291).

Full variation also differentiates the heat operator with respect to the
metric and clock. Such variation is not an exponentially smoothing operator
in its metric input. For example, on a circle let

```
h_epsilon = exp(2 epsilon cos(mx)) dx^2,  U=sin x.
delta Delta U = ((m+2)/2) sin((m+1)x)
                + ((m-2)/2) sin((m-1)x).
```

Using ACTION.md's own Duhamel formula, the coefficient for k=m+1 in
`delta S U` is

```
((m+2)/2) [exp(-b)-exp(-b k^2)]/(k^2-1)
  ~ exp(-b)/(2m).
```

The same example embeds into a product T3 metric. This polynomial tail does
not alone disprove that the **full reduced correction** is lower order; it
shows that B5's particular exponential-decay argument cannot establish that
claim for metric/clock variations. The full mixed symbol, constraints,
gauge reduction and differentiability must actually be derived. At the
homogeneous zero field, Finding 2 prevents the proposed ordinary tangent
of the U equation used by B5 in the first place. A different nonlinear
reduction could have a smoother solution map; this review does not exclude
that possibility. Setting `U=ln N` nulls the local square in the action,
but the full auxiliary equation generally does not set `U=ln N`; nor does
that substitution null the q term.

## Other scope and implementation checks

| Obligation | Result | Reason |
|---|---|---|
| B1 away from p=0 | Passed | Direct chain rule gives the quoted eigenvalues. |
| B2 unweighted | Passed | Spectral contraction is correct on the stated closed leaf. |
| B3 arbitrary lapse, nonmonotone branches | Failed | Prior exact weighted counterexample and actual-kernel negative Hessians. |
| Monotone branch convexity | Passed under continuous-kernel/domain assumptions | `C>=0` and the local square give strong convexity modulo constants. |
| Existence | Correct with explicit hypotheses, not supplied by “strict convexity” alone | For smooth positive N and smooth compact h, coercivity/Poincare and weak compactness give a minimizer for these nonnegative q laws. Heat smoothing makes the q term continuous along a bounded weak H1 subsequence. |
| Uniqueness for all listed kernels | Not established | Negative Hessian blocks the claimed proof; it is not itself a multiple-solution witness. |
| B4 solves the stated lapse problem | Failed as written | Lines 221–223 rescale phi and its gradient, then independently set `Nlap=exp(0.3 phi/max|phi|)`. Lines 232–234 still use `Dphi`, which generally is not `D ln Nlap`. |
| B4 lowest Hessian mode | Limited | Lines 204,247–249 add 50 on whole Nyquist lines, although only the four Cartesian combinations of zero/Nyquist component frequencies, including the constant, have zero total spectral gradient. The reported eigenvalue belongs to this modified operator. |
| B5 smoothing of the fixed-background U block | Correct under stated regularity | Not a derivation of the mixed system; coefficient is singular at zero and numerically clamped. |
| B6 decoupled nonzero-k cone | Passed, with alpha_c>0 and c_2>0 | The operator `Delta(alpha_c partial_t^2-c_2 Delta)` has the stated nonzero-k roots. Spatial zero modes, gauge and metric mixing are not fixed by this calculation. |
| B6 cited collapse/hyperbolicity theorems | Conditional / not authenticated in this review | No exact theorem/hypothesis check was performed; those citations are not used to support any audit conclusion. |
| B7 model-profile quadrature | Computationally limited | The model results are plausible; their extension to all heat-smoothed fields is explicitly false. |

The convex monotone branch also permits a more precise safe leaf statement:
on a fixed smooth compact connected leaf, smooth positive N, and fixed b>0,
the intended continuous q with `Q>=0`, convex Q and C1 first variation has
a unique H1 minimizer modulo constants. The heat-smoothed nonlinear forcing
and elliptic equation then give spatial smoothness for smooth h,N. This is
a leafwise result, not differentiability of the solution map in all evolved
variables or a physical-time Cauchy theorem.

## Strongest safe conclusion and next check

XC2 supplies correct local Hessian algebra, an unweighted heat contraction,
and finite illustrations. The genuinely monotone candidate has a viable
fixed-background convex auxiliary problem. The RAR and exact exponential
branches require a lapse bound or a separate nonconvex solvability argument.
The zero-field and full mixed principal-symbol questions remain open beyond
the particular nondegenerate frozen configurations tested here.

The cheapest decisive continuation is to state the desired evolution norm
and prove a solution-difference estimate at the homogeneous zero background
for the full reduced equations. In parallel, any claimed full-symbol
reduction must retain `delta S` and the weighted adjoint before eliminating
the constraints. Repeating the present generic-zero quadratures or random
minimizations does not address those implications.

The independent computation is `independent_checks.py`; its contract,
runner manifest, results and logs record arithmetic, bounds, inputs and
non-claims. It imports none of the audited scripts and writes only inside
this review directory.

## Completed computation record

- `run1/manifest.json` records a 60-second timeout in the initial general
  symbolic trigonometric integration; no scientific output was produced.
  The exact original script is preserved as `run1/script_snapshot.py`, whose
  SHA-256 `1fb47a3b02948f63dc6c52c768efc52ede92ae5b327c68daa3038064bb5f5bcd`
  matches that run's declared input. The current source has intentionally
  changed, so this historical failed run is not fresh evidence for it.
- `run2/manifest.json` records the revised exact finite Fourier convolution,
  completed at base commit `f3b848273e635b81bc328882db0ffb4206d86e45` in
  2.442489 seconds, exit code 0. All declared inputs were unchanged during
  that run, and `run2/stderr.txt` is empty.
- Arithmetic: SymPy exact rationals and Fourier products; Python 3.9.6,
  NumPy 1.26.2, SciPy 1.11.4, SymPy 1.14.0; deterministic adaptive
  quadrature/root-finding; no randomness. A 60-second wall cap and 1 MiB log
  cap were enforced; the single numerical-library thread setting is cooperative.
- The independent result preserves the prior weighted-energy derivative
  `154/25`, reproduces the weighted ratio `106.9352789001`, shows the two
  actual-kernel negative Hessians, and confirms the exact square-root
  homogeneous scaling and the mixed metric derivative's `1/m` tail.
- Fresh validation command, completed successfully:

```
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py real_research/peer_review_2026_09_26/xc2/run2/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The runner's exact argv is stored in the manifest. The validator reported
`valid evidence record; mathematical interpretation requires review`.
Final self-proofreading covered this report's equations, variables and source
locators; no mathematical claim is authenticated merely by manifest validation.
