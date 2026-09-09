# Connection terms require a new metric elimination

For a static clock normal to zero-shift slices with spatial metric
h_ij=exp(-2 Psi) delta_ij and phi=phi(x), direct Christoffel construction gives

q^{ik}q^{jl} nabla_i V_j nabla_k V_l
=exp(4 Psi)[(phi''+Psi' phi')^2+2(Psi' phi')^2].

For phi=s0*x+epsilon*f and Psi=epsilon*p, its quadratic term is
(f''+s0*p')^2+2*s0^2*p'^2. The operator vanishes on the flat constant-gradient
background itself, so its quadratic contribution to -b J(Y+xi^2 H) is
-b J'(s0^2) xi^2 times this expression. Measure corrections start at cubic
order for this operator contribution. Here b=2-K_B.

Its independently computed Euler-Lagrange contributions are

E_p=2b J' xi^2 s0 (f'''+3s0*p''),
E_f=-2b J' xi^2 (f''''+s0*p''').

Thus replacing the covariant contraction by phi''^2 omits metric terms at
quadratic order on this background. The earlier two-field Fourier elimination
does not establish the response of the full submitted action. This correction
neither proves nor disproves cancellation in the complete system. The missing
calculation is the full quadratic action, including the remaining J(Y),
measure, lapse and clock contributions, before eliminating metric variables.
Background equations and any supporting source must also be specified.

The exact contraction is checked directly from the metric's Christoffel
symbols. A zero-background-gradient control recovers f''^2. Command:

`python3 qwen_claude_field_theory/closure_2026/user_action_connection_gate.py`

Exit 0. All expressions are printed by the script; no numerical fits, PPN
values or mode counts are assigned. This is a static sector calculation,
not full relativistic closure. The earlier IC50 evolution uses a different
action and is unaffected. Mathbox computation-audit discipline requires
limiting the prior response claim after this omitted-term check.
