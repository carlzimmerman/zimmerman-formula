# Lean audit for the 2026-09-26 closure resume

**Target:** the explicitly quantified real-algebra, matrix, norm, finite-sum,
and derivative statements in the eight files below, under exactly their Lean
hypotheses. This is a source-level mathematical certificate bundle. It is not
a certificate that a single relativistic action yields those hypotheses, that
observational gates pass, or that the full gravity theory is closed.

**Primary verdict: proved as written, for these 70 formal statements only.**
All eight source files compile with exit code 0. Every theorem's axiom list is
contained in `{propext, Classical.choice, Quot.sound}`; accepted evidence has
no `sorryAx` and the inspected source has no admitted proofs or custom axiom
declarations. The exact final source hashes, compiler exits and theorem-level
axiom inventory are recorded in `lean_logs/manifest.json`.

## Claim cards and scope

| Source | Formal claim class | Inputs not derived by Lean |
|---|---|---|
| `DE_vacuum_gate_certificates.lean` | Sixteen real identities/inequalities: edge law, positive gate window and logarithmic exponent interval, monotonicity, scale normalization, four-form algebra | The edge model, empirical floor/cap values, positive cosmological factors, physical four-form energy and normalization |
| `L357_L361_vacuum_gate_certificates.lean` | Seven claims: vacuum-fraction identity, exponential determinant identity, threshold obstruction/window, real-power and NFW monotonicity, subtraction of two linear screened equations | Background/foliation interpretation, tensor dynamics, screened equations, boundary conditions and physical screening |
| `L353_kernel_invisible_certificates.lean` | Six claims: symmetric matrix response, asymmetric counterexample, scalar source subtraction, given static-block elimination, force-ratio arithmetic | Action-to-Hessian reduction, physical invertibility/uniqueness, field equations, coupling interpretation |
| `L340_chk_certificates.lean` | Four claims: static-block consequences, mode-root sign, sufficient inertia lower bound, bound for a supplied PPN expression | Scalar-block derivation, energy/Krein signature, physical range/normalization of the supplied PPN formula, nonlinear health |
| `I27_kick_escape.lean` | Five claims: norm lower bound and positive post-kick energy, supplied numerical escape bounds, monotone density trigger and shutoff inequality | Potential and escape-speed model, velocity bounds, physical decay process and subsequent time evolution |
| `I28_selection_inflates_retention.lean` | Four claims: filtered finite-sum inequalities and exact decimal comparison | Selection by retained fraction, rather than an arbitrary density mask; positive aggregate denominators when interpreting a ratio; correspondence to actual simulation statistics |
| `XC1_strong_coupling_certificates.lean` | Twelve claims: completing a kinetic square, inertia bounds, annihilating quadratic form, power-law branch comparison, supplied strong-coupling and vacuum-scale identities, exponential filter bound and cubic coefficient algebra | Full interaction expansion, physical cutoff/power counting, literature formula identification, filter metric/foliation vertices and numerical acceptance windows |
| `ClosureResume20260926.lean` | Local-gate algebra and constructive witnesses, exact four-constraint feasibility, exponential-kernel differentiation and chain-rule sign consequence | Physical realizability of the local scalar witnesses, empirical floor/cap reduction, kernel/action identification, and a differentiable local response when interpreting the constitutive derivative |

The scalar results are over `ℝ`; the screened subtraction is over an arbitrary
real module and a linear endomorphism; the kick vectors are Euclidean `ℝ³`;
the selection theorem uses an arbitrary finite set with nonnegative baseline
weights. Positivity and nonzero-denominator assumptions remain explicit.

## New exact exponential calculation

For dimensionless `x`, define

\[
t(x)=x(1-e^{-x}),\qquad h(x)=xe^{-x}.
\]

Lean checks actual `HasDerivAt` proofs, not supplied derivative identities:

\[
t'(x)=1+(x-1)e^{-x}>0\quad(x>1),\qquad
h'(x)=(1-x)e^{-x}.
\]

For any `response : ℝ → ℝ` differentiable at `t(x)`, with derivative `C`,
and satisfying `response(t(y))=h(y)` in a neighborhood of `x`, the chain rule
and uniqueness of derivatives give

\[
C=\frac{h'(x)}{t'(x)}
 =\frac{1-x}{e^x+x-1}<0\quad(x>1).
\]

At `x=2` this is exactly `−1/(exp(2)+1)`. The differentiability and local
matching hypotheses specify the response being differentiated. They do not
assume the derivative's value or sign. The unconditional derivative and slope
lemmas establish the sign independently of the response-existence question.

This contradicts a requirement `0<C` on that exact branch. It does not rule
out every nonzero-`alpha_c` or filtered configuration, a different kernel, or a
different action. See the raw-block discussion in `recipe_audit.md`. The
physics bridge from the frozen exponential field equation to this spherical
parametrization assumes the no-extra-central-flux reduction described there.

## New local-gate and window certificates

The local linear gate is explicitly defined as

\[
G(R,K,\Lambda)=\frac{27\Lambda R}{4K^4}.
\]

For positive `Λ` and nonzero `K`, Lean proves strict increase with `R`, the
`K⁻⁴` rescaling identity, and nonnegative on/off witnesses at fixed `Λ,K`
for every positive threshold `cut`:

\[
R_{off}=0,\qquad R_{on}=\frac{4\,cut\,K^4}{27\Lambda}.
\]

Thus the constant vacuum scale does not make this environment-dependent gate
constant. The separate vacuum-only obstruction says only that one response
value cannot be simultaneously above a larger lower bound and below a smaller
upper bound. It does not rule out the current curvature/expansion gate.
Existence of real scalar witnesses does not prove that a gravitational solution
realizes them. The expression follows the note's `c=1` convention, and its
omitted positive present-day vacuum-fraction normalization can be absorbed
into the cut. The certificate deliberately excludes `K=0` from this reading.

For positive weights `aK,aS,aF,aL` and `XS>0`, Lean proves

\[
\begin{aligned}
&\exists x>0:\quad xa_K\le X_K,\quad X_S\le xa_S,\quad
xa_F\le X_F,\quad X_L\le xa_L\\
&\quad\Longleftrightarrow\quad
\max(X_S/a_S,X_L/a_L)\le\min(X_K/a_K,X_F/a_F).
\end{aligned}
\]

The reverse direction constructs `x=max(XS/aS,XL/aL)`; it does not assume a
passing parameter exists. A rational example with `x=2` passes, while a second
example with incompatible bounds is proved empty. Those are algebraic
nonvacuity fixtures, not empirical parameter fits. In particular, this theorem
does not prove the forest monotonicity assumption in DE2 or replace its
numerical tests. The original three-constraint `window_iff` and
`window_p_interval` already contain nontrivial derivations; they are not just
relabelings of their conclusions.

## Dependency and obligation audit

The dependency graph is: explicit definitions and input hypotheses → Mathlib
algebra/calculus/order/norm theorems → the recorded Lean declarations. The
separate physical dependency graph is: proposed action and physical state →
field equations/reduced block → identification of the Lean variables and
hypotheses → formal consequence → numerical or observational interpretation.
Only the last algebraic/calculus step of that physical chain is certified here.

| Obligation | Status | Evidence/limit |
|---|---|---|
| Exact statements type-check | Passed for all eight files / 70 theorems | Fresh compiler exits in the manifest, including the final new-file derivative proof |
| Axiom provenance | Recorded per theorem | `#print axioms` output; permitted set is `propext`, `Classical.choice`, `Quot.sound` |
| Conclusion substituted as a hypothesis | Passed on inspected statements | Existing field/root equations are input models; derived formulas are not assumed; the new chain-rule theorem derives `C` |
| Denominator and boundary handling | Passed within formal scope | Positivity/nonzero hypotheses in statements; singular boundaries not silently included |
| Nonvacuity | Passed for new scalar/window fixtures; limited elsewhere | Explicit on/off and feasible-window witnesses; response existence and gravitational solution existence are not asserted |
| Finite statistic → retention ratio | Conditional | Need positive selected and total baseline sums and the same selection predicate |
| Physical action → scalar block/response | Not addressed | No common-action reduction is formalized in this bundle |
| External PPN formula attribution | Not addressed | Lean proves a bound on the supplied expression, not its identification with a published PPN parameter |
| Cosmological and halo numerical checks | Out of scope | No data-fitting or simulation gate is established by these Lean files |

Four interpretation limits require particular care:

1. `tt_mode_trace_free` proves `exp(h) exp(−h)=1`. It does not by itself prove
   tensor propagation speed `c_T=1`, nor the gate's full variation about a
   tensor-perturbed background.
2. `response_symmetric` proves symmetry of `BᵀH⁻¹B` assuming symmetry of `H`.
   Mathlib's matrix inverse is totalized, so the theorem remains an algebraic
   identity for singular `H`; a unique physical inverse response requires the
   additional invertibility and constraint-reduction argument. The asymmetric
   matrix counterexample excludes this symmetric static response class, not
   every conceivable Lagrangian.
3. `mode_sign` assumes the reduced root equation. With positive `c2` and
   nonzero `k`, its hypotheses exclude `C=0` automatically. It does not establish
   a positive energy norm, a degree-of-freedom count, or nonlinear health.
4. `milky_way_interior_empties` proves positive instantaneous daughter energy
   under the supplied speed/potential bounds. It does not establish a retained
   fraction after self-consistent time evolution. `selection_inflates_retention`
   is a cross-product inequality even if the selected baseline sum vanishes;
   interpreting it as an inequality of ratios needs positive denominators.

## Reproduction and provenance

Run each command from
`/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026`:

```sh
lake env lean DE_vacuum_gate_certificates.lean
lake env lean L357_L361_vacuum_gate_certificates.lean
lake env lean L353_kernel_invisible_certificates.lean
lake env lean L340_chk_certificates.lean
lake env lean I27_kick_escape.lean
lake env lean I28_selection_inflates_retention.lean
lake env lean XC1_strong_coupling_certificates.lean
lake env lean ClosureResume20260926.lean
```

Three existing files lacked axiom commands. Their unchanged full source was
copied into `lean_logs/*_axioms.lean`, with one `#print axioms` per theorem
appended, and those copies were compiled with the same Lake environment.
The manifest records their exact commands, source hashes and exits as well.
Existing files and build configuration were not edited.

Toolchain: Lean `4.34.0-rc2`, commit
`6a10ac8c22beadecabdbb0919c2b50214762f91d`, arm64 macOS; Lake
`5.0.0-src+6a10ac8`; Mathlib commit
`85e3a25e006c35636f0e53b0e9296caca2685bc0`. Repository base:
`4e16ccf585f6fcc775a2f9d62ac30d329212e0af`. Another task advanced HEAD during
review to `03524d209b7ca0c3900f47ccf5dfe42f9187d7c3`, adding the XC1 certificate
and strong-coupling updates. The newly landed XC1 certificate was separately
read, compiled and axiom-audited. The six earlier source hashes were rechecked
without change. The workspace contained existing
uncommitted research; source SHA-256 values, rather than HEAD alone, identify
the exact certificate inputs. `lean_logs/manifest.json` records full hashes,
compiler commands/exits, and every theorem's axiom list.

Run `python3 real_research/closure_resume_2026_09_26/lean_logs/verify_manifest.py`
from the repository root to validate recorded compiler exits, all source/log
hashes and the theorem-by-theorem axiom inventory. This validates the evidence;
the Lean commands above reproduce the proofs themselves.

An initial path preflight failed before the new source existed; its diagnostic
is preserved separately. The first actual gate/window compile passed with one
redundant-tactic warning; that tactic was removed. Later compilation evidence
is tied to the final source hash, so intermediate drafts are not the certificate.
Two intermediate derivative drafts failed to elaborate and are kept as
development logs; their compiler-generated `sorryAx` diagnostics are excluded
from accepted evidence. The final derivative proof compiles without errors.
One harmless tactic-sequencing style warning remains in the accepted new-file
log. It does not introduce an axiom or change the proven statement.

The final mathematical proofreading pass covered only the new Lean source and
this report. It checked notation, inequalities, quantifier scope, theorem names,
and the distinction between the formal statements and their physical reading.
No substantive mathematical-token correction was needed in that final pass.

The strongest safe conclusion is a formal certification of the stated
conditional mathematical consequences. The missing scientific implication is
the action/state/observable bridge, including consistent assembly of the gate,
kernel and carrier sectors. The cheapest next check is to derive the exact
chosen kernel's scalar block from one frozen action and identify each formal
variable and assumption before promoting any component-level result to closure.
