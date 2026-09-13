# Conditional local-scalar slip obstruction

**Status: conditional obstruction, not a universal no-go.** This gate tests the
smallest local elliptic auxiliary sector that is often proposed for a
phantom-density MOND construction:

\[
 S_\chi=\int d^4x\,\sqrt{-g}\,F(Y),\qquad
 Y=h^{ij}\partial_i\chi\,\partial_j\chi,
\]

on a flat three-dimensional static leaf. The test holds the foliation fixed
and excludes multiplier/heat-kernel stress, a disformal matter metric, a
background vector gradient, and extra tensor operators. The full covariant
action problem is therefore **not** represented by this sector.

## Derivation from the action

Varying \(\chi\) gives, after one spatial integration by parts,

\[
 \delta S_\chi=-2\int d^4x\,\sqrt{-g}\,
 D_i(F_YD^i\chi)\,\delta\chi,
 \qquad
 E_\chi=-2D_i(F_YD^i\chi).
\]

Consequently a target equation

\[
 D_i\!\left[\mu(|\nabla\Phi|/a_0)D^i\Phi\right]=C\,\rho_b
\]

requires, up to the nonzero normalization \(C\),

\[
 2F_Y=C\,\mu(\sqrt{Y}/a_0),
 \qquad
 \mu(y)=1-e^{-y}.
\]

For \(Y>0\) and \(a_0>0\), this constitutive derivative is nonzero.

The spatial metric variation gives (up to the overall stress-tensor sign
convention)

\[
 T_{ij}=2F_Y\,\partial_i\chi\partial_j\chi-\delta_{ij}F,
\]

so the traceless source in the weak-field spatial Einstein equation is

\[
 \Pi_{ij}=2F_Y\left(v_iv_j-\frac{Y}{3}\delta_{ij}\right),
 \qquad v_i=\partial_i\chi.
\]

The isotropic \(F\) term cancels exactly. Direct algebra gives

\[
 \sum_{i,j}\left(v_iv_j-\frac{Y}{3}\delta_{ij}\right)^2
 =\frac{2}{3}Y^2,
 \qquad Y=v_1^2+v_2^2+v_3^2.
\]

Hence

\[
 \sum_{i,j}\Pi_{ij}^2=\frac{8}{3}F_Y^2Y^2.
\]

If \(\Phi=\Psi\) is required pointwise for every nonzero static gradient,
the traceless Einstein equation requires \(\Pi_{ij}=0\) for all \(i,j\).
For \(Y>0\), the identity then forces \(F_Y=0\), contradicting the
nonzero exponential-MOND coefficient. The contradiction is exact and does
not depend on the gradient orientation.

This is the useful architectural result:

> A single local \(F(Y)\) elliptic scalar cannot both carry the exponential
> MOND constitutive flux and give zero gravitational slip for arbitrary
> nonzero static gradients unless another sector cancels its anisotropic
> stress.

The required cancellation is precisely the part that must be derived, not
assumed, in a viable nonlocal/elliptic construction. It could come from a
multiplier, heat-kernel stress, a constrained vector, or another metric
operator; adding such a sector changes the theorem's hypotheses and requires
a fresh Dirac and Ward analysis.

## Executable and Lean evidence

`scalar_slip_gate.py` derives the Euler coefficient, stress tensor, exact
sum-of-squares identity, and a numerical orientation witness with SymPy. The
ordinary command exits 0 only when all derivation checks pass and reports
`CONDITIONAL_OBSTRUCTION`. `--require-compatible` deliberately exits 2,
because compatibility is falsified in this restricted sector.

`AnisotropicSlip.lean` proves the algebraic identity, the implication from
vanishing traceless stress to \(F_Y=0\), and incompatibility with any nonzero
MOND matching coefficient. The compiler reports only the standard Lean
foundational axioms (`propext`, `Classical.choice`, `Quot.sound`); there is no
`sorry` and no custom physics axiom. The action variation and the weak-field
Einstein equation remain documented assumptions outside Lean.

## Reproduction

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/scalar_slip_gate_2026/test_scalar_slip_gate.py
python3 -B qwen_claude_field_theory/closure_2026/scalar_slip_gate_2026/scalar_slip_gate.py
lake env lean qwen_claude_field_theory/closure_2026/scalar_slip_gate_2026/AnisotropicSlip.lean \
  # run from qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026
```

The local-scalar door is therefore **closed under the displayed hypotheses**;
the full theory remains **OPEN**. The next unavoidable calculation is the
full metric variation of a proposed stress-cancelling multiplier/heat sector,
including its constraints and boundary data, followed by the nonlinear
finite-mass spherical branch. No coefficient reconstruction is justified by
this result.
