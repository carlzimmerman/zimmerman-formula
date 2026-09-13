# Qwen Task T03 — Physical DOF / constraint analysis

Work ONLY inside `qwen_claude_field_theory/closure_2026_final/`.

Use the actual equations produced by T01 and T02.

Perform a Dirac-Bergmann / ADM analysis.

Separate:
A. naive local auxiliary system;
B. constrained local system;
C. physical retarded nonlocal functional.

For each, determine:
- canonical variables;
- momenta;
- primary constraints;
- secondary constraints;
- first-class constraints;
- second-class constraints;
- constraint matrix rank;
- multiplier fixing;
- physical phase-space dimension;
- physical propagating modes.

Analyze Minkowski first, then FLRW if feasible.

The mixed Hessian result from the diagnostic script is known and must not be treated as the final answer.

The question is:
Does the apparent negative mode correspond to an independently specifiable physical propagating degree of freedom after the full causal restrictions are imposed?

Outputs:
- `11_dof/T03_dof.py`
- `11_dof/T03_dof.md`

If the proof cannot be completed, give the exact obstruction rather than guessing.
