# Reproduction commands

Run from `/Users/carlzimmerman/new_physics/zimmerman-formula`.
The bounded orchestrator records each of its 18 exact child command arrays,
working directories, exit codes, source hashes and Lean axiom sets in
`followup_run_001/checks/summary.json`. It caps concurrency at two workers,
numerical library threads at one and each child at 90 seconds.

The complete fresh-evidence invocation used here is:

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' '/Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/followup_contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/principal_gate/principal_gate.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/principal_gate/test_principal.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/principal_gate/first_derivative_variation.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/principal_gate/ResponseGate.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/metric_response/derive_static_metric.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/spherical_branch/derive_spherical.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/spherical_branch/SphericalScaling.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/boosted/derive_boosted.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/boosted/test_boosted.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/pressure/audit_pressure.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mond_braiding_completion/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/verify_followup.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/derive_cone.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/test_cone.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/DisformalCone.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/boosted/tensor_cone.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/nonlinear_clock/derive_nonlinear_clock.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/critical_radial/derive_critical.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/critical_radial/CriticalRadial.lean' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/followup_run_001' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/followup_run_001/checks/summary.json' '--timeout' '300' '--max-output-bytes' '2097152' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/verify_followup.py' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/followup_run_001/checks'
```

For another run, replace all three path arguments containing
`followup_run_001` by an unused directory name, including the result and
child-output paths.

Validation:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/followup_run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Development controls executed before the orchestrated run:

```sh
git status --short --untracked-files=no
git log -5 --oneline
git show --stat --oneline 96512fc6e
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/test_cone.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/derive_cone.py
```

The first unit-test invocation exited 1 with the intended
`action-derived cone implementation missing` assertion before implementation;
its post-implementation run exited 0. The derivation exited 0.
From the pinned `clock_constitutive_construction_2026/lean_formalization_2026`
directory the following development proof command also exited 0:

```sh
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/disformal_cone/DisformalCone.lean
```

Agent-specific runs and exact commands are additionally recorded in
`nonlinear_clock/run_001/manifest.json`, `critical_radial/run_001/manifest.json`
and `critical_radial/lean_run_001/manifest.json`. Source-inspection commands
were read-only. No action histories, published deposits, unrelated user edits,
or earlier evidence directories were overwritten.

Git whitespace checking used
`git -c core.whitespace=-blank-at-eof diff --cached --check`: the single
harmless extra terminal blank line in the already-hashed verification harness
is retained so the executed source remains byte-identical to its evidence.
