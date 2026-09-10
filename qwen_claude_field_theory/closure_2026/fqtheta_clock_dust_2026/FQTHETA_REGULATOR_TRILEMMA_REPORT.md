# F(Q)Theta regulator trilemma (2026-09-09)

The exact action-derived principal scalar sector reduces, after the displayed
constraints are solved, to

\[
 L=\Omega p\dot z+\frac{k^2}{2}(U_{pp}p^2+U_{zz}z^2),\qquad
 \Omega=U_{nz}k^2/Q_0 .
\]

Direct variation gives

\[
 K_{\rm red}=-\frac{U_{nz}^2 k^2}{2Q_0^2U_{pp}},\qquad
 \omega^2=\frac{Q_0^2U_{pp}U_{zz}}{U_{nz}^2},\qquad
 \det\omega_{ab}=\Omega^2 .
\]

The Lean certificate proves the sign alternatives without inserting a desired
rank or determinant.  For the exponential constitutive branch,

\[
 U_{pp}\propto A(y),\qquad A(y)=1+(y-1)e^{-y}>0\quad(y>0).
\]

Hence a nonzero mixed sector (`U_nz != 0`) is a ghost (`K_red < 0`). Flipping
the stiffness to `U_pp < 0` makes `omega^2 < 0` whenever `U_zz > 0`, i.e. a
gradient instability. Setting `U_nz = 0` makes the symplectic determinant zero
and is a rank-changing/strong-coupling branch rather than a regular closure.

Adding an independent `eps*p_dot^2/2` term is not an auxiliary repair: direct
Euler--Lagrange variation contains `-eps*p_ddot`. Together with the `z`
equation, eliminating `z` gives the second-order equation

\[
 \left(\frac{\Omega^2}{k^2U_{zz}}-\epsilon\right)\ddot p+k^2U_{pp}p=0,
\]

for generic nonzero coefficient. The clock/auxiliary field is therefore
dynamical and must be counted and re-audited in the full covariant theory.

This closes the regulator options for the displayed mixed F(Q)Theta
architecture, not all possible relativistic MOND actions. A genuinely new
action must evade at least one premise of this trilemma while re-deriving the
metric, Ward, PPN, FLRW, tensor-speed, and stability gates from that same
action.

## Reproduction

```sh
python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/fqtheta_regulator_trilemma_gate.py
python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/run_lean_regulator_trilemma.py
```
