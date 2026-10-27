# Qwen Task T04 — Metric variation and MOND closure

Work ONLY inside `qwen_claude_field_theory/closure_2026_final/`.

Use T01/T02 results; do not invent a separate weak-field theory.

Derive the weak-field metric equation from the repaired action:

S = S_m + c^3/(16 pi G) ∫ sqrt(-g) [R - 2 Lambda - (a0^2/c^4) M[g]].

Required:
1. linearize the metric;
2. keep the chain-rule variation through M[g];
3. derive the quasistatic scalar equation;
4. show precisely whether the coefficient is 1 - 2F'(Z);
5. substitute Z=4 y^2;
6. derive mu(y)=1-exp(-y);
7. derive the spherical relation mu(g/a0) g = GM/r^2;
8. derive deep MOND and v^4=GMa0;
9. derive the high-acceleration corrections.

Do not start from the desired Poisson equation.

Outputs:
- `06_newtonian/T04_metric_weakfield.py`
- `06_newtonian/T04_metric_weakfield.md`
