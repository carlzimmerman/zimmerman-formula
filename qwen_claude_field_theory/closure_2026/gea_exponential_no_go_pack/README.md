# GEA Exponential-MOND No-Go / Next-Gate Package

This package records a reproducible audit of the standard generalized Einstein–æther (GEA) single-function MOND construction for the target interpolation

\[
\mu(y)=1-e^{-y},\qquad y=|\nabla\Psi|/a_0.
\]

## Status

**Claim supported by this package:** Under the standard GEA weak-field reconstruction, assuming a finite nonzero \(F_{\mathcal K}(0)\), imposing the MOND deep-MOND normalization \(\mu(0)=0\) and the luminal tensor-speed condition \(c_{13}\simeq0\) forces the effective coupling combination

\[
\bar c_4-\bar c_1=2,
\]

and hence, with \(\epsilon=\bar c_{14}>0\),

\[
\bar c_1=-1+\epsilon/2.
\]

In the observational regime \(\epsilon\ll1\), this makes the Einstein–æther spin-1 mode have negative squared speed,

\[
c_V^2\simeq\bar c_1/\bar c_{14}<0,
\]

using the standard Minkowski spin-1 speed formula.

This is a **conditional no-go for the stated standard single-function realization**, not a no-go theorem for every possible covariant MOND theory, every multi-function æther theory, or every theory with additional fields/operators.

## Reproduction

Run:

```bash
python3 scripts/verify_no_go.py
```

The script performs symbolic algebra for the coupling identities, evaluates the exact vector-speed expression at \(c_{13}=0\), checks the sign conditions, and verifies the AQUAL primitive for the exponential interpolation.

## Files

- `NO_GO.md` — manuscript-ready derivation and scope statement.
- `ASSUMPTIONS.md` — explicit assumptions and logical dependencies.
- `REFERENCES.md` — primary/reference literature used for the audit.
- `scripts/verify_no_go.py` — SymPy reproducibility check.
- `next_gate/QWEN_NEXT_GATE.md` — tightly scoped task for searching for a two-function completion.
- `next_gate/RESEARCH_PROTOCOL.md` — falsification protocol for candidate two-function models.

## Suggested repository location

Drop this directory into:

```text
qwen_claude_field_theory/closure_2026/gea_exponential_no_go/
```

Do not overwrite the prior candidate. Treat this package as a **negative-result branch / closure record**.
