# Stress audit commands and exits

Working directory: /Users/carlzimmerman/new_physics/zimmerman-formula.

The fresh bounded run executes exactly:

~~~bash
/bin/bash -c 'python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026 -p "test_*.py" -v && python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/stress_audit.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/run_002/result.json'
~~~

Exit0. Five unit tests passed in0.230seconds. All ten metric variations, both invariant identities, and39 numerical consistency checks passed. The complete bounded job took1.843717seconds. The scientific nonzero-pressure verdict is conditional on its computed boolean; all20 evaluated cases pass that nonzero-pressure test.

The command was wrapped by the installed computation-audit run_experiment.py, using this directory's contract.json, the seven execution_artifacts listed there as --input, fresh output run_002, and declared result run_002/result.json. Enforced limits: timeout120seconds, per-process CPU100seconds, maximum log2MiB; cooperative numerical-library thread cap1. Full executed argv, hashes and resource details are in run_002/manifest.json.

~~~bash
python3.11 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_stress_audit_2026/run_002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
~~~

Exit0; input freshness and output hashes verified. Use a new run directory when reproducing the bounded experiment.

Historical run_001 also exited0. Its later verdict-output correction makes its original source path stale. The old source is preserved at run_001/source_at_run.py with SHA256 matching its original manifest; the manifest itself was not edited. It is historical evidence, not current-input-fresh evidence. No source change affects the current run_002.

The first tool submission failed JavaScript parsing before any file was written or experiment launched; it produced no scientific run. The subsequent patch and unit tests succeeded.
