# Qwen Task T01 — Complete action-level definition

Work ONLY inside `qwen_claude_field_theory/closure_2026_final/`.

Do one task. Do not orchestrate the whole project. Do not modify the frozen candidate.

Goal: derive an explicit mathematical definition of the active repaired nonlocal candidate:

S = S_m + c^3/(16 pi G) ∫ sqrt(-g) [ R - 2 Lambda - (a0^2/c^4) M[g] ]

U_mu = -∇_mu T,   g^{mu nu}∇_mu T ∇_nu T = -1

Box Phi = R_mu nu U^mu U^nu   (retarded solution)

Z = (4 c^4/a0^2) ∇_mu Phi ∇^mu Phi

∇_mu[U^mu (M + F_epsilon(Z))] = 0

Tasks:
1. State metric signature and curvature conventions.
2. Write a complete constrained auxiliary representation, if possible.
3. State every field and multiplier.
4. Derive each Euler-Lagrange equation.
5. Show exactly how the retarded boundary condition is imposed.
6. Explain whether a single-copy variational action gives a retarded or advanced response, and whether an in-in/doubled construction is required.
7. Derive the first variation with respect to g^{mu nu}, including all indirect dependencies through T, U, Phi, Z, and M.
8. Do not claim ghost-freedom.
9. Do not simplify away boundary terms without showing why they vanish.
10. If exact closure fails, identify the exact missing equation.

Outputs:
- `01_action/T01_action.py`
- `01_action/T01_action.md`

At the end print only:
PASS / PARTIAL / FAIL and the single most important unresolved equation.
