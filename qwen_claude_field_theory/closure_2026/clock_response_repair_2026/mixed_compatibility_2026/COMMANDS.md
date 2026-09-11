# Executed scientific commands

Working directory: repository root unless the command changes it. These are
actual subprocess argv from recorded runs, not an invented reproduction plan.
The bounded runner settings and pinned inputs are in each run's manifest.
Historical probe revisions are identified in REPORT.md; replaying them with
current source is not claimed byte-identical. Exit 0 is not a physics PASS.

## attribution_001

Execution exit 0; 40.451121 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/attribution.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/attribution_001/result.json'
```

## collocated_001

Execution exit 0; 26.34631 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/collocated_probe.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/collocated_001/result.json'
```

## evolution_001

Execution exit 0; 286.00429 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/collocated_probe.py' '--evolve' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/evolution_001/result.json'
```

## integrated_001

Execution exit 0; 25.371727 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/integrated_probe.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/integrated_001/result.json'
```

## lean_attempt_001

Execution exit 1; 1.622605 seconds.

```sh
'/bin/bash' '-c' 'cd qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/ClockCompatibility.lean'
```

## origin_001

Execution exit 0; 19.638593 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/origin_profiles.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/origin_001/result.json'
```

## spline_001

Execution exit 0; 0.263639 seconds.

```sh
'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/spline_obstruction.py' '--result-file' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/spline_001/result.json'
```

## spline_lean_001

Execution exit 0; 1.62276 seconds.

```sh
'/bin/bash' '-c' 'cd qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026/SplineJetObstruction.lean'
```

## Fresh regression verification

Both commands executed from the repository root, exit 0. The first passed
4 tests (0.233 seconds), the second 17 tests (224.993 seconds).

```sh
python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/mixed_compatibility_2026 -p 'test_*.py' -v
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026 -p 'test_*.py' -v
```

Manifest validation was executed for every directory listed above, using
validate_manifest.py with --root .; exact findings are in validation.json.
Earlier direct Lean invocations produced the same success/failure outcomes
as their subsequently recorded runs. Developmental missing-module and nodal
polynomial regression failures are described in REPORT.md, not represented as
final-source failures.
