# Acceleration-only khronon candidate: full 3-D slip gate

The direct primordial-clock action is

\[
 S=\int\sqrt{-g}\left[\frac{M^2}{2}(R-2\Lambda)-2M^2a_0^2H(Z)\right]+S_m,
 \qquad H(Z)=2(1+Z)e^{-Z}-2,
\]

with (Z=\sqrt{a_\mu a^\mu}/a_0).  Its independent weak-static potential
variation does produce the exact exponential AQUAL flux because

\[
H'(y)/y=2\mu(y)-2,
\qquad \mu(y)=1-e^{-y}.
\]

However, the full three-dimensional Hilbert variation on a constant-gradient
patch was missing from the earlier one-dimensional check.  On
(Phi=Psi), with (v_i=\partial_i\Phi), direct differentiation gives

\[
 \left.\frac{\partial L_{EH}}{\partial h^{ij}}\right|_{TF}
 =-2M^2(v_iv_j)_{TF},
\]

\[
 \left.\frac{\partial L_{acc}}{\partial h^{ij}}\right|_{TF}
 =-M^2\frac{H'(y)}{y}(v_iv_j)_{TF},
\]

and therefore

\[
 \boxed{\;T^{TF}_{ij}=-2M^2\mu(y)(v_iv_j)_{TF}\;}.
\]

The Lean certificate proves this coefficient is nonzero for every (y>0).
Thus the action has the desired static MOND flux, FLRW (H\ne0) branch, and
luminal tensor diagnostic, but it cannot simultaneously give exact
(Phi=\Psi) for generic galaxy gradients.  A one-dimensional variation could
not test the transverse traceless equation.

The ADM jet also shows why the clock cannot simply be called an auxiliary:
the lapse has no time velocity but enters through spatial (D_iN), producing a
nonlinear elliptic lapse constraint on the MOND branch.  The full khronon Dirac
count and preferred-frame parameters still require a separate covariant gate;
the candidate is already obstructed by the 3-D slip equation.

This is scoped to the explicit local acceleration-only action.  A successful
theory would need a new covariant stress-compensating mechanism and a complete
Dirac/Ward/PPN/FLRW/stability derivation from that enlarged action.

## Reproduction

```sh
python3 -B qwen_claude_field_theory/closure_2026/khronon_acceleration_mond_2026/khronon_acceleration_mond_gate.py
python3 -B qwen_claude_field_theory/closure_2026/khronon_acceleration_mond_2026/run_lean_khronon_acceleration.py
```
