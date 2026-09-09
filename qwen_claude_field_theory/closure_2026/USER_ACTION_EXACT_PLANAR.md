# Exact static planar equations: constraint identity

For the metric and clock ansatz in USER_ACTION_BACKGROUND.md, define
U=exp(-2A)phi'^2+xi^2 exp(-4A)[(phi''-A'phi')^2+2B'^2 phi'^2].
The exact static density, up to the EH boundary term, is

L=exp(P-A+2B)[(2B'^2+4P'B')/(16 pi G)+ca P'^2+2b P'phi']
  -exp(P+A+2B)[C+b J(U)].

Direct Euler-Lagrange differentiation with arbitrary differentiable J gives
the exact identity

P' E_P + A' E_A + B' E_B + phi' E_phi - (E_A)' = 0.

The script computes the residual and simplifies it to zero. This is the
spatial coordinate identity associated with delta A=epsilon A'+epsilon';
it is not the full spacetime matter Ward identity or a Dirac classification.
On A=0 and the other three equations, E_A is constant along x, so imposing
it at one point preserves this static constraint for a smooth solution.

After varying and then imposing A=0, derivative orders are:

| equation | P | B | phi |
|---|---|---|---|
| lapse | 2 | 2 | 2 |
| transverse metric | 2 | 2 | 3 |
| scalar | 2 | 3 | 4 |

These mixed orders require simultaneous reduction, including differentiated
metric equations, before an ODE existence or principal-symbol claim. The
printed coefficient block for P'',B'',phi'''' is deliberately not called a
full principal matrix. Next: reduce this constrained system on a regular
branch and construct compatible background data for the intended J.

Command: `python3 qwen_claude_field_theory/closure_2026/user_action_exact_planar.py`
Final exit 0. An intermediate output serialization failed (exit 1) because a
SymPy Integer needed conversion to int; this was corrected and rerun.
Output saved as user_action_exact_planar.json. No empirical test, time
evolution, mode count or full-theory closure is claimed. This scope follows
the Mathbox computation-audit discipline.
