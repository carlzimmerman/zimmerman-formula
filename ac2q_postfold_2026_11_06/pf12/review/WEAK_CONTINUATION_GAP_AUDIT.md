# Independent audit: the weak-continuation gap

**Verdict: the mathematical gap identified is correct; two scope/wording
clarifications are recommended.** Reviewed `pf12/WEAK_CONTINUATION_GAP.md`,
SHA256 `4d6fdc904938256fe941cb75532a8a93c1b1e107921f591eff51ffaea04bbe4e`.
Independent delegated audit, 2026-11-06.

A periodic first-order spatial system with bounded measurable
coefficients and the stated quantitative inverse/coercivity can solve
finite-measure forcing in a BV response class. This linear fact does not
give that forcing its native nonlinear meaning. At jumps of r or the
clock direction, differentiating smooth constraints creates products of
derivative measures with discontinuous coefficients. A classical chain
rule cannot choose those products or prove that the resulting equations
are equivalent to the original scalar, polarization and Einstein
divergence equations. A specified weak formulation, correct native jump
relations and constraint propagation are therefore additional obligations.

The reviewed prebreak construction and trace estimates supply terminal
data, not a family of native approximants existing after the strong
endpoint. The distinction between extending a spatial inverse and
constructing postbreak evolution is valid. No general entropy theorem
for this constrained nonlocal system is imported by the existing work.

Two wording clarifications preserve the exact mathematical scope:

- The shock compatibility sentence should specify a regular nontrivial
  **small acoustic shock in the stated low-u neighborhood**. The audited
  corner result is not a theorem excluding every BV jump or every shock.
- Replace "the failure ... proves none exists or is nonunique" with
  "the failure ... proves neither existence nor nonuniqueness of any such
  continuation." The former wording can be read as a nonexistence claim,
  contrary to the surrounding, correctly restricted discussion.

Continuous non-Lipschitz candidates, diffuse limits and irregular layers
are neither constructed nor excluded by failure of the naive BV-inverse
argument. The file's final statement that complete postbreak predictivity
has not been established is supported by the audited implication gap.

Coordinator follow-up: applied both wording corrections exactly; no new
mathematical claim was added. Revised input SHA256:
`96d42d84b5543f92abd0d8abd1636be053a82874ea3bc82275098680b3847f38`. The earlier hash identifies the reviewed pre-correction file.
