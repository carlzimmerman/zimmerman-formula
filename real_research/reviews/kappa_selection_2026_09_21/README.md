# Can the present action force κ = 1/2?

**Requested goal: not achieved. Primary verdict: incomplete, with the missing physical selection of λ = 1.** The stronger claim that the specified static conditions already imply the half is refuted by an explicit counterexample. This is a self-review with fresh Lean compilation, not an independent scientific review.

The work here proves a precise obstruction and a useful reformulation of the next task. It does not establish that every particle-free theory must leave κ free. Existing conditional half theorems remain correct under their stated assumptions.

## Exact result: the entire static action has one effective acceleration scale

Use the existing auxiliary action, with independently fixed s>0, λ>0, g=|∇Φ|, 0<q₁,q₂≤1 and U(q)=q²/2−2q+log q+3/2. Its gravitational density, before the fixed factor −1/(8πG), is

\[
\begin{aligned}
D_{s,\lambda}
&=s^2\left[\left(\frac gs\right)^2(1-q_1q_2)
          +\frac{U(q_1)+U(q_2)}{\lambda^2}\right]\\
&=g^2(1-q_1q_2)+\left(\frac{s}{\lambda}\right)^2[U(q_1)+U(q_2)]\\
&=g^2(1-q_1q_2)+4a_0^2[U(q_1)+U(q_2)],
\qquad a_0=\frac{s}{2\lambda}.
\end{aligned}
\]

Thus **the full static functional depends on s and λ only through s/λ**, not merely its deep asymptote. The unchanged baryonic source term does not break this identity. This algebraic statement even holds for arbitrary U.

After auxiliary elimination, let x=g/a₀. Then

\[
\mu_\lambda(g/s)=1-\left(1+\frac{g}{2a_0}\right)^{-2}
                 =1-(1+x/2)^{-2}.
\]

Every λ gives exactly the same curve in x. Lean proves equality of these functions and, consequently, equivalence of **any predicate of the normalized curve alone** at any two nonzero weights. A normalized RAR shape, its slopes, or arbitrarily accurate normalized shape measurements therefore cannot choose λ within this family.

This is not a claim that s can be changed in a fixed-vacuum physical comparison. At the same independently known s, different λ give different dimensional a₀ and different forces at fixed g. Measuring a₀ against that external s constrains λ empirically. It does not derive the exact number λ=1 from a principle.

## Fixed-s counterexample and channel counting

The existing stationary solution is q₁=q₂=1/(1+λy), with y=g/s. For every λ>0 it has the same domain, channel-exchange symmetry, zero response at zero drive and unit saturation. Its static principal coefficients at y>0 are

\[
\mu_\lambda=\frac{\lambda y(\lambda y+2)}{(1+\lambda y)^2}>0,
\qquad
\mu_\lambda+y\mu'_\lambda
=\frac{\lambda y[(\lambda y)^2+3\lambda y+4]}{(1+\lambda y)^3}>0.
\]

In particular λ=2 obeys these conditions, yet at fixed s gives **κ=1/4**. The new Lean existential counterexample includes bounded response and both positive principal coefficients. Saturation and their identification with the variation of the action are separately checked symbolically; the existing auxiliary existence/uniqueness theorems are freshly recompiled.

For N channels with common response pλ(y)=λy/(1+λy), Lean proves the exact derivative

\[
\left.\frac{d}{dy}\left[1-(1-p_\lambda(y))^N\right]\right|_{y=0}
=N\lambda.
\]

For N>0, deep matching therefore gives κ=1/(Nλ). Counting two channels fixes N=2 and leaves λ untouched. In `deepseek_push/lean/PD21_law_of_nature.lean`, `Framework.hprinciple` supplies `kappa = 1/count` as a premise; `hcount` supplies two. PD08 explicitly assigns `p = Y + c2 * Y**2`, inserting unit slope. Neither closes this missing implication.

High-acceleration matching supplies no extra independent coefficient in this family: the deep slope is 2λ, the coefficient of 1−μ at order y⁻² is λ⁻², and their product (2λ)²λ⁻²=4 for every λ≠0. Fixing a particular tail amplitude in s-units would require a separately justified physical constraint.

## Additional attempted selector: vary λ itself

Treating a coupling as a variable changes the variational problem. Even if one tries that extension, the current density does not select an interior unit weight. On the stationary auxiliary branch,

\[
\partial_\lambda\overline W_\lambda(y)
=-\frac{4}{\lambda^3}U\!\left(\frac1{1+\lambda y}\right).
\]

Since U(1)=0 and U′(q)=(1−q)²/q>0 for 0<q<1, U(q)<0 there. For every λ,y>0 the displayed derivative is positive. At λ=y=1 it is 4 log 2−5/2>0. SymPy checks the derivative identity; Lean proves this strict positive value using a certified logarithm inequality. Thus even this simplest stationarity proposal fails at λ=1. A new potential or coupling could change the result, but its minimum and numerical coefficient would need an independent justification.

This pointwise result is not an analysis of all spacetime-dependent λ fields, their kinetic terms, or arbitrary global constraints.

## Evidence and route outcomes

| Route or obligation | Result | Evidence |
|---|---|---|
| Normalized force-law shape selects λ | Fails within this family: exact function equality | `normalized_response_exact`, `no_normalized_shape_selector` |
| Entire static action distinguishes s and λ independently | Fails: only s/λ enters | `action_depends_on_ratio`, `action_at_fixed_a0` |
| Static positivity/bounds force the half | Fails at λ=2, same s | `static_conditions_do_not_force_half` plus explicit symbolic action checks |
| Channel count alone fixes susceptibility | Fails: derivative is Nλ | `channel_count_slope`; inspected PD21/PD08 premises |
| Promoting the bare coefficient selects one | Fails: nonzero variation at λ=y=1 | Symbolic derivative identity, `unit_weight_variation_positive` |
| Independently justified vacuum-to-response coupling | Missing | No such numerical selection equation supplied by these routes |
| Complete covariant stability and observational adequacy | Not addressed | Static counterexample only |

`Selection.lean` contains **13 compiled theorems**, with ordinary Lean foundational axioms only. `verify.py` runs **28 exact symbolic checks** and recompiles **14 existing UnitResponse theorems**. The action-to-field-equation and logarithmic derivative bridges are explicitly symbolic/analytic checks; they are not silently claimed as full Lean formalizations of gravitational variational calculus.

`run/result.json`, `run/lean.txt`, `run/upstream_lean.txt` and `run/manifest.json` record the successful bounded run, hashes, versions and theorem names. The installed Lean kernel and compiled libraries remain part of the trusted computational environment. No observational data were fitted, no model API calls were used, and no worldwide novelty claim is made.

## What would actually finish the requested proof?

The smallest missing implication is still **an independent physical equation fixing the relative response coefficient at the independently fixed vacuum scale**. To advance beyond this result, a proposal must specify the new symmetry, interaction, boundary condition or microscopic field dynamics, derive its selection equation, and show that λ=1 satisfies it while λ=2 fails. A λ-independent property of the normalized static curve cannot do this, by the theorem above. An observed intercept can test the half, but finite measurement precision cannot prove exact equality.

The original goal remains open. The mathematical conclusion of this attempt is that these particular existing routes do not force it; further algebra or additional Lean certificates of the same premises cannot supply the missing physical input.

Reproduce the check into a fresh directory under this folder:

```bash
/opt/homebrew/Caskroom/miniconda/base/bin/python3 -B \
  real_research/reviews/kappa_selection_2026_09_21/verify.py \
  real_research/reviews/kappa_selection_2026_09_21/recheck
```

The full provenance-producing command is recorded in `run/manifest.json`; `contract.json` fixes its scope. The autoresearch loop and older research files were left unchanged.
