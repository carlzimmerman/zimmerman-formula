# Commands and observed exit statuses

All paths below are relative to the repository root unless absolute.
The canonical run's exact executable paths, argv, cwd, exits and timings are
in [run_001/suite.json](run_001/suite.json); full stdout/stderr and hashes are
in [run_001/manifest.json](run_001/manifest.json). No credentials are recorded.

## Canonical bounded run

Executed exactly (exit 0):
```bash
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/contract.json' '--output' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001' '--timeout' '240' '--max-output-bytes' '2097152' '--max-threads' '1' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/solver.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/test_solver.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/study.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/test_study.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_suite.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/data/inputs.json' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/data/SOURCES.md' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/profile.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/test_profile.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/run_checks.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/contract.json' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/bridge/audit_solver.py' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/bridge/REPORT.md' '--input' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/bridge/NUMERICAL_REVIEW.md' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/exact_exponential_aqual_efe_kepler_2026.py' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/independent_orbit_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/symbolic_action_audit.py' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/test_exact_exponential_aqual_efe_kepler_2026.py' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/calculation_results.json' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/orbit_audit_results.json' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/symbolic_action_results.json' '--input' 'qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/computation_manifest.json' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/study.json' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/suite.json' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/unit_static.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/unit_static.stderr.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/unit_stellar.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/unit_stellar.stderr.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/existing_efe.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/existing_efe.stderr.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/stellar_reference.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/stellar_reference.stderr.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/independent_audit.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/independent_audit.stderr.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/nonlinear_study.stdout.txt' '--result' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/nonlinear_study.stderr.txt' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_suite.py' '--output' 'qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001'
```

The wrapper executed, with the resolved Python binary recorded in suite.json:

| Command | Exit | Result |
|---|---:|---|
| `python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026 -p 'test_*.py' -v` | 0 | 8 tests |
| `python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar -p test_profile.py -v` | 0 | 5 tests |
| `python3 -B qwen_claude_field_theory/closure_2026/exact_exponential_aqual_efe_kepler_2026/test_exact_exponential_aqual_efe_kepler_2026.py` | 0 | 17 existing regressions |
| `python3 -B qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/stellar/run_checks.py` | 0 | reference grids 1025, 2049, 4097 |
| `python3 -B qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/bridge/audit_solver.py` | 0 | ten audit checks |
| `python3 -B qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/study.py --output qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/study.json` | 0 | 13 PDE cases; symbolic and numerical checks |

Manifest verification, exit 0:
```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Development history, not hidden or counted as successes

Before the canonical run, `python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026 -p 'test_*.py'`
failed on primitive finite differentiation near y=0.003. Independent
high-precision comparison located floating-point subtraction in the direct
primitive, not a changed constitutive law. A series evaluation repaired it.
Subsequent tests exited 0.

A new sixth solver test then failed for eta=1e-5, external/a0=0.5:
the source-relative residual stalled near 6.47e-7. The solver was changed to
store the internal potential and assemble the analytically background-subtracted
flux. The same strict test then passed; no tolerance was relaxed.
The independent review reproduces the corrected residual and exact action
differentiation. Earlier exploratory study output had a false convergence
flag and was not accepted as the canonical result.

The first independent audit script failed while serializing a NumPy bool;
plain-bool conversion repaired the output. The entire audit was rerun, exit 0.
The final archived source was independently inspected and executed.

An exploratory complete study after both arithmetic repairs exited 0 in a
fresh mktemp directory before the reproducible canonical run above. No earlier
committed scientific outputs were overwritten.

The staged whitespace check then reported four extra blank EOF lines. After
removing them (including the wrapper's final blank line), the first archive
was moved intact into a fresh `/private/tmp/df2-preformat.*` directory using
`mktemp -d` and a scoped `mv`. The identical bounded command above was rerun
in a fresh `run_001` so its hashes pin the final source, rather than editing
the generated manifest. Both complete suite invocations exited 0.

## Reproduction without the optional provenance tool

Use a new output directory every time:
```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/run_suite.py --output qwen_claude_field_theory/closure_2026/df2_fixed_a0_2026/rerun_002
```

This reproduction example is not an additional claimed run. It produces the
same six subprocess logs and study JSON, but not the optional bounded-run
manifest unless invoked through the recorded audit runner.
