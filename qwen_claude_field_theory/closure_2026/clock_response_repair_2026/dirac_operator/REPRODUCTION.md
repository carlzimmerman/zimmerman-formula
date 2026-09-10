# Reproduction commands and file inventory

All paths below are relative to `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Only this directory was created by this work; unrelated dirty files were preserved.

## Exact bounded-run commands

The fresh-output directories in these recorded commands already exist. To rerun,
change each output directory and every matching result path consistently.
The commands below are the executed argv (shell-quoted for reproduction).

### Constraint/operator suite (exit 1: unbuilt inverse draft)

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/sample_operator.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/constraint_data.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_checks.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/DiracKernel.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/CoerciveInverse.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_transport/stationary.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_transport/Stationarity.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/finite_evolution/inverse_entropy_clock.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001/checks.json' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001/operator.json' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001/constraints.json' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001/stationary.json' '--timeout' '600' '--max-output-bytes' '8388608' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_checks.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_001/checks.json'
```

### Ellipticity proof suite (exit 0)

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/ellipticity_contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/ellipticity.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/Ellipticity.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity_001' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity_001/checks.json' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity_001/eigenvalues.json' '--timeout' '180' '--max-output-bytes' '1048576' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_ellipticity_001/checks.json'
```

### Actual lapse-source solve (exit 0)

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/lapse_contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/lapse_source.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/constraint_data.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_transport/stationary.py' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_lapse_001' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_lapse_001/lapse.json' '--timeout' '90' '--max-output-bytes' '1048576' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/lapse_source.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/dirac_operator/run_lapse_001/lapse.json'
```

## Exact files created

- `CoerciveInverse.lean`
- `DiracKernel.lean`
- `Ellipticity.lean`
- `LATEST_DOORS_REVIEW.md`
- `README.md`
- `REPRODUCTION.md`
- `constraint_data.py`
- `contract.json`
- `derive.py`
- `ellipticity.py`
- `ellipticity_contract.json`
- `lapse_contract.json`
- `lapse_source.py`
- `run_001/checks.json`
- `run_001/constraints.json`
- `run_001/manifest.json`
- `run_001/operator.json`
- `run_001/stationary.json`
- `run_001/stderr.txt`
- `run_001/stdout.txt`
- `run_checks.py`
- `run_ellipticity.py`
- `run_ellipticity_001/checks.json`
- `run_ellipticity_001/eigenvalues.json`
- `run_ellipticity_001/manifest.json`
- `run_ellipticity_001/stderr.txt`
- `run_ellipticity_001/stdout.txt`
- `run_lapse_001/lapse.json`
- `run_lapse_001/manifest.json`
- `run_lapse_001/stderr.txt`
- `run_lapse_001/stdout.txt`
- `sample_operator.py`

## Evidence distinctions

All three manifests validate, including the honestly failed first suite.
The nine scientific/build rows and their individual statuses are listed in README.md;
raw stdout, stderr and exact child commands are retained. Exploratory builds of
Ellipticity.lean and ellipticity.py also exited zero before the bounded rerun.
The first source-solve execution exited zero before its bounded rerun.
No existing research source was edited. No complete theory or empirical PASS
is implied by these script or Lean exits.

Earlier development errors in derive.py (indentation, Boolean multiplication,
and SymPy bound-variable/substitution normalization) were corrected before the
recorded run. The Hilbert-inverse draft's missing dependency remains unresolved;
its statements have not been elaborated and are not counted as certificates.
