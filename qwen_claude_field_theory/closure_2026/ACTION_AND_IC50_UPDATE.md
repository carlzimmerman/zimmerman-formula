# Submitted action and IC50: separate evidence

The action Carl submitted matches section 2 of
`fable_independent_2026/THE_COMPLETE_THEORY_2026-09-08.md`. That file defines
n as the normalized gradient of tau, Q=n.grad(phi), V as its orthogonal
gradient, and Y=V.V. It explicitly reports four modes. Its claim that all
four are healthy has not been independently certified here. This action is
different from the IC49/IC50 action; their successes cannot be combined.

## Static action gate

Subsequent correction: `USER_ACTION_CONNECTION.md` shows that connection
terms contribute at quadratic order about a fixed nonzero scalar gradient.
The following truncation does not justify zero slip or the full physical
response on that background. Its algebraic variation remains reproducible.

For a static clock at rest and Q0=0, a leading planar weak-field reduction,
with ca=c1+c4 and b=2-K_B in the submitted normalization, is

L=(Psi'^2-2 Phi'Psi')/(8 pi G)+ca Phi'^2+2b Phi'phi'
  -b J(phi'^2+xi^2 phi''^2)-rho Phi.

This reduction assumes a regular weak-field expansion and retains the
nonlinear scalar constitutive function. It is not a full relativistic
variation on arbitrary backgrounds. Its Euler-Lagrange equations give

Psi''/(4 pi G)-2ca Phi''-2b phi''=rho,
Phi''-Psi''=0,
Phi''=(J'(B)phi')'-xi^2(J'(B)phi'')'',
B=phi'^2+xi^2 phi''^2.

Appropriate boundary conditions are needed to remove the affine integration
modes in Phi-Psi. For the independently checked specialization J(B)=j B,
the scalar equation contains -j xi^2 phi''''. The higher-derivative operator
therefore survives even in this simple limit. This is not a general no-go:
the remaining task is to solve the coupled system for the intended J and
derive its physical-metric response. Assigning a MOND kernel to J alone is
not a derivation of the requested exact physical-metric AQUAL equation.

Command (repository root):
`python3 qwen_claude_field_theory/closure_2026/user_action_static_gate.py`
Exit 0; checks include direct affine-J variation and the GR limit.
Output: `user_action_static_gate.json`. No PPN or DOF values are assigned.

## IC50 longer evolution

Two seven-node runs reach dimensionless time 2e-6, ten times IC49's interval,
at dt=4e-8 and 2e-8. Both complete. The inactive interior activation maximum
stays below -1.76950e-4; active interior minimum stays above 1.76983e-4.
Maximum reaction magnitude is below 5.14e-10, and momentum residual below
1.84e-14. These are sampled interior tests, not interval bounds between nodes.
Activation uses the stored initial interface threshold, whose normalization
roundoff is separately recorded. No condition on the sign of the unrestricted
Lagrange multiplier is inferred. Finiteness of that multiplier at vanishing
activation remains unproved.

Command (repository root):
`python3 qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ic50_branch_evolution.py`
Exit 0. Output: `integrable_clock_construction_2026/ic50_results.json`.
Finite Taylor endpoint data, unresolved continuum convergence, and the
absence of a global/full-theory certificate remain limitations.

Both candidates remain OPEN. Mathbox computation-audit scope is maintained:
each result applies only to its stated action, approximation and tested range.
