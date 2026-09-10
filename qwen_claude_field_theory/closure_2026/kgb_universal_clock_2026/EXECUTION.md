# Verified execution checkpoint

The main bounded run completed at repository HEAD
`d0db626c4035117798922587fa5a9edc1e9fb40d` on 2026-09-10, in 17.981059 s.
The root result is `run_001/results.json`; the source-pinned record is
`run_001/manifest.json`. All pinned inputs remained unchanged.

## Important exits and results

| Case | Exit | Measured outcome |
|---|---:|---|
| Root implementation/regression tests | 0 | 17 tests |
| Fixed-f bounded search | 0 | 0 initial matches / 36 starts |
| Free-f bounded search | 0 | 0 initial matches / 27 starts |
| Pressure-reduced search | 0 | 14 initial matches / 27 starts; repeated starts, not 14 independent theories |
| Three initial data at 50/80 digits | 0 | Six evaluations; next-preservation residual nonzero |
| Eight prescribed continuation targets | 0 | Seven initial matches, each with nonzero next obstruction; eighth solver trial leaves required chart |
| Strict next-preservation acceptance | **2** | Physics gate rejects the evaluated seeds |
| Independent structural checks | 0 | 11 Python tests; 8 conditional Lean theorems; 60/80-digit independent seed |
| Common curvature intervals | 0 | 9 Python tests; 3 conditional Lean lemmas |
| Independent matched-seed health audit | 0 | 5 tests; three 80-digit five-equation refinements |
| Previous action/flow/health regressions | 0 | 10 tests |
| Previous varied-action algebra | 0 | 14 tests |
| Previous EF dictionary | 0 | 10 tests |
| Previous cosmology | 0 | 8 tests |
| Existing power-law counterclaim regression | 0 | 9 tests |
| Main manifest validation | 0 | Input and output hashes validated |

Total: **93 Python tests**, including **42 new** and **51 previous** tests;
**11 new conditional Lean theorems** compile. Physics remains **OPEN**.
The strict exit 2 is expected because the new matched seeds do not satisfy
the next shared-action condition. It is not converted into a physical PASS.

The later L125 review is recorded separately under `latest_review/` and is
not silently included in these counts or this earlier manifest.

That subsequent bounded review also completed (exit 0): **four additional
tests and three additional Lean lemmas** pass. It reran the nine existing
L123 tests and Claude's actual L125 script (exit 0, seven literal PASS labels).
Those seven labels do not establish the claimed physical no-go; the exact
scale-counterexample refutes its displayed implication. Both root and
independent lane reproduced this review. Its commands and outcomes are in
`latest_review/run_001/results.json`, with a separate validated manifest.
Combined unique total: **97 Python tests and 14 conditional Lean lemmas**;
repeat executions are not counted as additional distinct tests.

Final CLI smoke check (after the frozen research runs), exit 0:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/signed_search.py --max-nfev 1
```

This exercised all 18 starting cases with only one evaluation per optimizer;
none was already matched. It is **not** an optimization study or additional
parameter-space exclusion. The earlier health-search report's unexecuted
broad search remains unperformed at its intended convergence budget; this
later smoke check only verifies the standalone entry point. The helper itself
was already executed through the five focused tests and independent seed audit.

## Exact commands

Every scientific subprocess's complete argv, working directory, exit code,
stdout and stderr is in `run_001/results.json`. The structure wrapper's
commands appear in its retained stdout; the health wrapper records its Lean
argv and compiler output. Independent subpackage manifests retain their own
commands. The top-level frozen command was:

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/audit_contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain' '--input' 'qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/joint_static.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_joint_action_2026/third_mass.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/conformal_dictionary.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/conformal_inverse.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/extension/conformal_extension.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/extension/ef_principal.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/structure/test_derivative_curvature_variation.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_mass_compatibility_2026/triple_seed.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/controlled_flow.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/cosmology/cosmology_checks.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/cosmology/run_cosmology.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/cosmology/test_cosmology.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/curvature_window.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/dictionary/general_ef.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/dictionary/test_general.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/l123_review/test_power_law_counterclaim.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/nonaffine_inverse.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/quadratic_flow.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/run_suite.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/run_supplement.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/test_controlled_flow.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/test_curvature_window.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/test_nonaffine.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/test_quadratic_flow.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/variation/test_nonaffine_variation.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_shared_pressure_2026/shared_pressure.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/continue_seeds.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/CommonInterval.lean' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/actual_pencils.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/common_interval.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/run_health.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health/test_common_interval.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/matched_seed_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/run_matched_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/signed_search.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/health_search/test_signed_search.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/high_precision_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/reduced_match.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_suite.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/SharedControlAlgebra.lean' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/check_next_preservation.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/closed_inverse.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/run_checks.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/structure/test_shared_preservation.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/test_high_precision_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/test_reduced_match.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/test_universal_seed.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/test_w_match.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/universal_seed.py' '--input' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/w_match.py' '--input' 'qwen_claude_field_theory/closure_2026/ticking_kgb_inverse_2026/kgb_inverse.py' '--output' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_001' '--result' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_001/results.json' '--timeout' '450' '--max-output-bytes' '4194304' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_suite.py' '--result-file' 'qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_001/results.json'
```

Validation command, from the repository root:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

For a fresh bounded run choose a **new** output directory and matching result
file instead of overwriting this evidence. For direct computation only:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_universal_clock_2026/run_suite.py
```

Development failures and their regression fixes are retained in
`DEVELOPMENT_NOTES.md`; they are not evidence of physical exclusions.
