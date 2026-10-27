# Manual execution order

Run these in separate Claude/Qwen invocations if necessary:

1. `python3 scripts/01_constitutive_check.py`
2. `python3 scripts/02_c2_regulator.py`
3. `python3 scripts/03_auxiliary_hessian.py`
4. `python3 scripts/04_transport_solution.py`
5. `python3 scripts/05_active_normalization.py`
6. Give Qwen ONLY `qwen_tasks/T01_action_variation.md`.
7. Review T01 output.
8. Give Qwen ONLY `qwen_tasks/T02_causal_adjoint.md`.
9. Review T02 output.
10. Give Qwen ONLY `qwen_tasks/T03_dof.md`.
11. Review T03 output.
12. Give Qwen ONLY `qwen_tasks/T04_metric_weakfield.md`.
13. Run the new scripts/tests individually.

Do NOT launch a giant all-in-one autonomous loop until T01-T04 are stable.

If Qwen crashes, restart from the last completed task. Do not rerun the whole project.
