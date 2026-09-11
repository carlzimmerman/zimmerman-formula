# Conditional small-source exponential-MOND obstruction

Base: `62a6ee68703f8c89e6bbf66eb1a69b114dc18a83`.
The Lean proof establishes the finite inequalities below. The source-to-force
bound is an explicit hypothesis and is not obtained from a PDE by this file.

For real accelerations define

\[
F_{a_0}(g)=\bigl(1-e^{-g/a_0}\bigr)g.
\]

Let \(a_0,n,C,\varepsilon>0\), and suppose
\(0\le g\le C\varepsilon\). The exact exponential tangent inequality
\(1-e^{-x}\le x\), supplied by mathlib's `Real.add_one_le_exp`, gives

\[
0\le F_{a_0}(g)
\le \frac{g^2}{a_0}
\le \frac{C^2\varepsilon^2}{a_0},
\qquad
0\le \frac{F_{a_0}(g)}{\varepsilon n}
\le \frac{C^2\varepsilon}{a_0n}.
\]

In particular,

\[
0<\varepsilon<\frac{a_0n}{C^2}
\quad\Longrightarrow\quad
F_{a_0}(g)<\varepsilon n,
\]

so the exact constitutive equality with \(g_N=\varepsilon n\) cannot hold
in that range. The proof uses the exponential function itself, not a
truncated Taylor series. Choosing a positive \(C\) is no loss for an
identically zero response: any positive linear upper bound then suffices.

For a family \(g(\varepsilon)\), if the same positive constants \(a_0,n,C\)
and the assumed bound hold for every sufficiently small positive
\(\varepsilon\), the normalized quantity tends to zero by the squeeze
theorem. The Lean file proves the displayed quantitative inequalities; a
separate `Tendsto` declaration is not included. A statement that \(g\) is
smooth alone would be insufficient: the requisite vanishing source-induced
force at zero source, together with the local bound, must also be justified.

## Checked declarations

Source: `lean/SmallSourceObstruction.lean`, namespace
`ConditionalSmallSource`.

| Declaration | Content |
| --- | --- |
| `exponential_upper` | Exact inequality \(1-e^{-x}\le x\). |
| `mondForce_nonneg` | Nonnegative \(F_{a_0}(g)\) for \(a_0>0,g\ge0\). |
| `mondForce_le_quadratic` | \(F_{a_0}(g)\le g^2/a_0\) for \(g\ge0\). |
| `conditional_quadratic_bound` | Consequence of the input bound \(g\le C\varepsilon\). |
| `conditional_normalized_bound` | Nonnegative ratio bounded by \(C^2\varepsilon/(a_0n)\). |
| `conditional_force_lt_source` | Strict inequality below the explicit positive threshold. |
| `conditional_not_exact_mond` | Exclusion of the exact constitutive equality there. |

## Verification

The existing dependency environment was used without installation or changes.
Runtime: Lean 4.34.0-rc2, `arm64-apple-darwin24.6.0`, compiler commit
`6a10ac8c22beadecabdbb0919c2b50214762f91d`; the existing mathlib pin is
`v4.34.0-rc2`.
Working directory:

```text
/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026
```

Executed command:

```sh
lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_infall_2026/lean/SmallSourceObstruction.lean
```

Final exit status: **0**, without warnings. All seven `#print axioms` outputs
list only `propext`, `Classical.choice`, and `Quot.sound`. The source has no
`sorry` or added axioms. There is one Lean source in this package, and it was
executed. The first development compilation exited 1 because `field_simp`
had already closed a goal before an unnecessary `ring` command; removing
that command changed no statement. An unused-hypothesis binding warning was
also removed without changing its type or the theorem assumptions.

## Exact scope and remaining implication

This is a conditional algebraic obstruction to an exact constitutive law on
a regular small-source branch. It does not derive existence, analyticity,
invertibility, or a uniform response bound for the constrained field equations.
It assumes that \(g\) is the nonnegative force quantity to which the proposed
law applies and that \(n>0\) is fixed at the comparison point. Neither its
physical interpretation nor the relevant Newton-constant calibration is
supplied by this file.

An application must establish a common solution branch, boundary and initial
data, a positive fixed \(a_0\), and a \(C\) independent of source amplitude
on a common positive interval. The statement does not exclude a singular or
nonperturbative branch, source-dependent boundary data, or limits in which
the domain, observation time, comparison radius, or coefficients change.
It is not a global no-go theorem, an evolved galaxy solution, or a claim about
the first-principles selection of the clock action.

Mathbox proof-audit guided the separation between the theorem and its PDE
hypothesis. Computation-audit guided the bounded Lean execution, and
proofread-math self-review covered the new source comments and this report.
No mathematical-token correction was needed in that proofreading pass.
