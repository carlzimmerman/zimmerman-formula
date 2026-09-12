# Independent vertex and Lean review

2026-09-12. Reviewed `vertices/vertices.py`, `vertices/test_vertices.py` and
`VarianceClosure.lean` independently of their implementation. No source edits.

**Verdict: implementation and finite assertion verified in the stated range.**
No critical coefficient, sign or Fourier-normalization defect was found.
The result is a bare fixed-metric, fixed-clock interaction calculation and
seven real-algebra lemmas; it does not establish nonlinear stabilization.

## Action and Fourier checks

Writing \(v=\dot\sigma\), \(p=k^2/a^2\), the invariant perturbation used in
`vertices.py:32–35` is
\(\Delta X=2Q\epsilon v\cos kx+\epsilon^2(v^2\cos^2kx-p\sigma^2\sin^2kx)\).
Independent expansion gives the period-averaged quartic density

\[
a^3\left[
\frac{P_{XX}}{16}(3v^4-2p\sigma^2v^2+3p^2\sigma^4)
+\frac{Q^2P_{XXX}}4(3v^4-p\sigma^2v^2)
+\frac{Q^4P_{XXXX}}4v^4
+\frac{3sW_{YY}}{16}p^2\sigma^4\right],
\]

agreeing with lines 46–49. These are derivatives at physical \(X=Q^2,Y=0\),
not at the coefficient reference \(\bar q^2\). The constant-gamma
\(X\Box\chi\) term is at most cubic in \(\chi\) on fixed geometry, so it
contributes no additional **bare scalar quartic**. Its constraint-mediated
effects are outside this assertion.

At \(v=0\), the spatial Euler contribution is
\(\tfrac32(P_{XX}+sW_{YY})\sigma^3k^4a^{-4}
[\cos kx-\cos3kx]\), under \(E=-\partial_x(\partial L/\partial\chi_x)\).
This agrees with the direct variation at lines 54–67. Integration by parts
gives the third cosine coefficient \(-6\langle F\sin3x\rangle\), for flux
\(F=2(sW_Y-P_X)\chi_x\); the numerical normalization at lines 104–106 is
therefore correct. This is the **spatial contribution**, not a claim to have
varied the complete time-dependent scalar equation at finite amplitude.

The exact single-mode moments are
\(\langle Y^2\rangle=3\langle Y\rangle^2/2\). Consequently replacing
\(\langle W(Y)\rangle\) by \(W(\langle Y\rangle)\) misses
\(W_{YY}\langle Y\rangle^2/4\) at quartic order. Those factors agree with
lines 50–66.

The five tests pass. The strongest orthogonal check is the **full nonlinear
constitutive flux**, evaluated at \(X=Q^2-Y\) using the unchanged model and
then Fourier-projected, against the separately derived small-amplitude
coefficient. It is not a test that merely reevaluates the cubic formula.
The direct polynomial expansion versus expected quartic formula also checks
all velocity terms. The wrapper counting six symbolic checks and the
zero-amplitude check are bookkeeping/elementary controls; their count adds no
independent evidence.

At the archived physical state \(Q=0.9078321505772312\), \(a=1\):

- \(P_{XX}=0.6301409907160642\), \(sW_{YY}=-0.06242275469149993\).
- \(C=P_{XX}+sW_{YY}=0.5677182360245643\), so the third-harmonic target is
  \(-3C/2=-0.8515773540368464\).
- For amplitudes `0.01`, `0.003`, `0.001`, relative errors from the full flux
  are `0.00138264997`, `0.000124560528`, `0.0000138412630`.
- The largest 1024-versus-4096-point quadrature difference is `1.525e-11`;
  the linear-flux control is `2.498e-16`; the selected jets exactly match the
  archived values in floating arithmetic.

Thus retaining \(P\) reverses the isolated \(W\) spatial-vertex sign at this
sample. It does not determine the reduced Hamiltonian sign, a kinetic ghost,
the net constrained third harmonic, a saturation amplitude, or an attractor.

## Lean scope

All seven lemmas compile. Their displayed axioms are only `propext`,
`Classical.choice` and `Quot.sound`; no additional mathematical assumption was
introduced as an axiom.

The two-coordinate closure theorem is valid for its quantified unrestricted
real states and positive weight: a variance-only rate exists for every
\((x,y)\) iff the velocity coupling `b` vanishes. Applying that statement to
admissible constrained initial data remains a separate obligation. The
moment-rate and acceleration statements prove algebraic consequences of the
functions **defined** at lines 57–59; they do not derive those functions from
the action or differentiate a stochastic process inside Lean.

In particular, `homogeneous_rate_preserves_stationary_ray` at lines 92–95
quantifies over a **scalar map** `rate : ℝ → ℝ`, given its homogeneity law.
It does not formalize matrices, covariance positivity, the equation
\(\dot\Sigma=A\Sigma+\Sigma A^T\), its solutions, or asymptotic attraction.
The preceding covariance-language comment is an intended application, not
the formal theorem's type. Documentation must retain that distinction.

## Independent execution record

From the repository root:

```text
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/vertices -p test_vertices.py -v
```

Exit 0; five tests in 0.407 seconds. A separate read-only import printed
`snapshot()`, `flux_controls()` and `linear_flux_third()` without calling the
script's file-writing CLI. Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4 and
SymPy 1.14.0. Deterministic quadratures; no random seed or stochastic sampling.

From `qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`:

```text
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/VarianceClosure.lean
```

Exit 0, approximately 1.97 seconds. SHA-256 hashes before and after these
checks were unchanged:

```text
vertices.py: df9206c3285f8f2e3a9aa0989ba04599bf5ad8e6ddef65922015a212b801c626
test_vertices.py: 7ba237f8d65368d0caa11836b9f59f6a0312840aaa845f95e2012ac035849ee8
VarianceClosure.lean: 69eaa60e9d8e98f5286e3051b85d122a85df3ac509ecb0ba181373d70714924f
```

The symbolic identities cover formal jets; the numerical sign and convergence
claim cover one specified archived state, three amplitudes and two quadrature
sizes. No interval-certified numerical assertion or full nonlinear
constraint reduction is claimed. Used proof-audit, computation-audit and
proofread-math self-review; only this review report was added.
