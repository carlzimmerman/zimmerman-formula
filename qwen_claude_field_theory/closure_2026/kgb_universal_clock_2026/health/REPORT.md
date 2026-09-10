# Exact common-curvature interval for local EF pencils

This is a complete algebraic interval reduction **conditional on the supplied
pencil and strict local cone criterion**. It is not a common-action existence
proof, a physical-frame cosmological certificate, or a complete Hamiltonian
analysis. The actual-background controls below introduce no dark-matter
particles and retain the explicit clock field.

Requested base: `1e8f58095a44e27b9cff0a467737e30eef414601`. No old files,
index, commits or branches are modified. Computation-audit supplies the bounded
run contract; proof-audit checks the exceptional sectors; proofread-math covers
this new derivation. No external theorem or novelty claim is needed.

## 1. Exact scalar interval

For one local EF principal matrix write

\[
 M^{ab}=\begin{pmatrix}K&b&0&0\\b&R&0&0\\0&0&T&0\\0&0&0&T\end{pmatrix},
 \quad K=K_0+A j,\qquad T=\beta(K-I),
 \quad R<0,\quad\beta>0.
\]

All coefficients except the one common curvature control \(j=F_{XX}\) are
fixed real numbers. In particular, \(A\), \(b\), \(R\), \(I\), and \(\beta\)
are not independent tunable functions within this test. Set \(c=|b|\).
The assumed local diagnostic is strict positive static quadratic energy and
strict positivity on the EF metric null cone:

\[
 K<I,\qquad
 q_K(t)=K+\beta(K-I)-2ct+[R-\beta(K-I)]t^2>0
 \quad\text{for every }0\le t\le1.
\]

Here \(t\) is the absolute radial component of a unit spatial direction, not
time. With \(R<0\), these inequalities already imply the other usual local
checks: \(T<0\), \(K>0\), and \(K>c\). Specifically, \(q_K(1)>0\) gives
\(K>2c-R>c\). This does not derive a full constrained-gravity Hamiltonian.

Define

\[
 D(t)=1+\beta(1-t^2)\ge1,\qquad
 L(t)=\frac{\beta I(1-t^2)+2ct-Rt^2}{D(t)}.
\]

The exact identity \(q_K(t)=D(t)[K-L(t)]\), together with continuity on the
compact interval, proves

\[
 \boxed{\quad K\in(L_*,I),\qquad L_*:=\max_{0\le t\le1}L(t).\quad}
\]

Both endpoints are excluded. Equality at the lower endpoint puts at least one
null direction on the scalar characteristic cone; equality at the upper
endpoint makes the angular spatial coefficient vanish.

## 2. Complete maximum, including exceptional sectors

Let \(S=\beta I+(1+\beta)R\). Direct differentiation yields

\[
 \frac12D(t)^2L'(t)
 =\beta c t^2-S t+(1+\beta)c=:f(t).
\]

The endpoints are \(L(0)=\beta I/(1+\beta)\) and \(L(1)=2c-R\).

- If \(c>0\) and \(S\le c(1+2\beta)\), the maximum is at \(t=1\).
  Indeed,
  \(f(t)=c(1-t)[1+\beta(1-t)]+[c(1+2\beta)-S]t\ge0\).
  The threshold equality is included; its stationary point is the endpoint.
- If \(c>0\) and \(S>c(1+2\beta)\), then \(f(0)>0>f(1)\).
  Its positive leading coefficient and root product \((1+\beta)/\beta>1\)
  imply exactly one root in \((0,1)\), a strict maximum of \(L\):

  \[
  t_* = \frac{S-\sqrt{S^2-4\beta(1+\beta)c^2}}{2\beta c}
  =\frac{2c(1+\beta)}{S+\sqrt{S^2-4\beta(1+\beta)c^2}}.
  \]

  Use \(L_*=L(t_*)\). The discriminant is strictly positive in this sector.
  The implementation uses the second expression to reduce cancellation.
- If \(c=0\), then \(L'=-2St/D^2\). For \(S>0\), use \(t=0\);
  for \(S<0\), use \(t=1\); for \(S=0\), the function is constant and
  either endpoint gives the same value. There is no division by \(c\).

The cases \(\beta\le0\) or \(R\ge0\) are outside this reduction and are
rejected, not silently interpreted as a no-go for other physical sectors.
Nonfinite or numerically unorderable coefficients are likewise unsupported.

As a useful cross-check, \(L_*<I\) iff \(I+R-2c>0\).
Necessity follows from \(L(1)<I\). Conversely, writing this last positive gap
as \(g\),
\(q_I(t)=g+(1-t)[2c-R(1+t)]\ge g>0\), so
\(I-L(t)\ge g/(1+\beta)>0\) uniformly. Individual feasibility alone does
**not** imply that two pencils share a feasible \(j\).

## 3. One common curvature, not separate per-halo choices

For pencil \(i\), let \(L_i\) be the exact maximum above. If \(L_i\ge I_i\),
its curvature set is empty. Otherwise:

\[
 J_i=\begin{cases}
 ((L_i-K_{0i})/A_i,(I_i-K_{0i})/A_i),&A_i>0,\\
 ((I_i-K_{0i})/A_i,(L_i-K_{0i})/A_i),&A_i<0,\\
 \mathbb R,&A_i=0\text{ and }L_i<K_{0i}<I_i,\\
 \varnothing,&A_i=0\text{ otherwise}.
 \end{cases}
\]

Intersect these open intervals. Two finite nonempty intervals have a common
control iff \(\max(\ell_1,\ell_2)<\min(u_1,u_2)\); their touching endpoints
are not allowed. A midpoint is a single witness for both. No curvature is
retuned separately for a halo. For example, the individually feasible sets
\((1,2)\) and \((0,1)\) have no shared strict control.

`common_interval.py` exposes `Pencil(K0,A,I,R,b,beta,label='')`,
`lower_bound`, `pencil_interval`, `common_interval`, and independent
`direct_health`. Passing exact SymPy numeric inputs and `sqrt=sympy.sqrt`
retains radical endpoints; ordinary floating inputs give a conditional
numerical evaluation, not interval-arithmetic certification of input errors.
Near an endpoint, recompute the actual coefficients at higher precision.
Empty families and invalid hypotheses raise; empty mathematical intersections
return `status='empty', witness=None`.

## 4. Actual inverse-derived controls and limitations

`actual_pencils.py` evaluates the committed non-affine inverse, including its
total-derived \(P_{XX},G_{XX}\), at two local backgrounds:

\[
 \epsilon=(10^{-6},2\times10^{-6}),\quad y=.1,\quad X=.5,
 \quad F=.525,\quad F_X=.05,\quad b_{\rm scale}=.25,
 \quad d_{\rm scale}=1.5.
\]

It constructs \(I=K_0-T_0/\beta\), \(\beta=U/(2X)\), and the inverse-derived
slope

\[
 A=\frac{4CXG_Xz}{C_X\Delta^2p},\qquad
 C=2F,\quad\Delta=C-XC_X,\quad p=\sqrt{BU},\quad z=X'.
\]

This relation is checked against the original coupled principal at
\(j=\pm|F_X|/\epsilon\), not assumed from arbitrary assigned coefficients.
For these floating controls, the two intervals are approximately

\[
 (-85222.81611696,490361.94199729),\qquad
 (-42593.56586896,245180.40282272).
\]

The common midpoint \(j=101293.41847688\) passes both directly recomputed
principal diagnostics. Correlation residuals are below \(7\times10^{-16}\);
the metric residuals at that same control are below \(2.6\times10^{-16}\).
Both lower maxima happen to be in the endpoint-one sector. An independent
exact interior fixture has \((I,R,c,\beta)=(10,-1,1,1)\),
\(t_*=4-\sqrt{14}\), and \(L_*=7-\sqrt{14}/2\).

The two actual controls do **not** share \(P,P_X,G_X\) at the same \(X\).
They therefore validate the two-pencil interval machinery, not a universal
action. The root construction must first impose common-action compatibility;
the same routine can then test its actual pair without introducing any new
freedom. A common interval only supplies a necessary local vacuum EF gate.
It neither preserves the matching surface radially nor handles baryonic
interiors, global boundary data, FLRW matter perturbations, physical-frame
observational constraints, or CMB spectra. The invertible conformal-map and
regular-background premises remain required upstream.

## Reproduction

From the repository root, run

```text
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/test_common_interval.py
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/actual_pencils.py
```

Nine tests cover exact differentiation/factorization, all maximizing sectors,
positive/negative/zero slopes, open/touching intervals, invalid inputs, 324
fixed-\(j\) comparisons to an independent quadratic minimizer, and the actual
two-background controls. `CommonInterval.lean` compiles three conditional
real-algebra lemmas: polynomial factorization, the strict-bound implication,
and the exact common-open-interval criterion. The radical maximum itself is
proved above and checked in SymPy, not certified in Lean.

`run_health.py` records the tests, the actual control pair, and the Lean
command in `run_001/results.json`. The bounded manifest pins code, report,
imported inverse/principal sources, and Lean dependency declarations. A valid
manifest records provenance; it is not a physics theorem.
