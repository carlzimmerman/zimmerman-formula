# Qwen Task T02 — Causal adjoint / nonlocal variation

Work ONLY inside `qwen_claude_field_theory/closure_2026_final/`.

Assume T01 exists. Do not redesign the theory.

Determine the correct causal variation of the retarded nonlocal functional.

Given:
Box Phi = J[g,T],  J = R_mu nu U^mu U^nu

and
∇_mu[U^mu(M+F(Z))]=0,

derive the adjoint equations needed to calculate δM/δg.

Required:
1. Distinguish retarded physical response from advanced adjoint response.
2. Track all boundary terms.
3. Determine whether a single-copy action can generate the desired causal equation.
4. If not, construct the minimal doubled/in-in schematic and identify physical equations.
5. State the allowed initial data.
6. Determine whether auxiliary fields are independent dynamical data or fixed functionals of the metric.
7. Derive an explicit formula or algorithm for δM/δg.

Do not claim that a mixed auxiliary Hessian proves a physical ghost.
Do not claim that boundary conditions automatically remove a ghost.

Outputs:
- `10_causality/T02_causal_adjoint.py`
- `10_causality/T02_causal_adjoint.md`
