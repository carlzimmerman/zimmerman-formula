# Executed medium-emission checks

The original scientific run, `run_001`, completed with child exit 0 and runner exit 0. There were no failed scientific runs. The complete version-2 manifest includes actual HEAD, dirty state, UTC timing, execution-input hashes before and after, raw log hashes, and result hash. The `validate_manifest.py` command below also returned exit 0 at that source revision: `valid evidence record; mathematical interpretation requires review`.

Executed from `/Users/carlzimmerman/new_physics/zimmerman-formula`:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/contract.json \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/audit.py \
  --input qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/MediumEmission.lean \
  --output qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/run_001 \
  --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/run_001/results.json \
  --timeout 150 --max-output-bytes 1048576 --max-threads 1 -- \
  python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/audit.py \
  --result qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/run_001/results.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py \
  qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/medium_emission/run_001/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

To reproduce, replace `run_001` with a fresh directory name; the runner deliberately refuses to overwrite it. Existing Lean 4.34.0-rc2 and compiled Mathlib are used through the exact binary and LEAN_PATH recorded in `results.json`. Python 3.9.6 and SymPy 1.14.0 perform exact rational/radical checks. The displayed numerical approximations use 25 or 30 digits; pass/fail uses exact expressions. No RNG, network fetch, or external physical source was used. Bounds: 45 support-grid cases, four cold constructions, four symbolic identities, six Lean lemmas, wall timeout 150 seconds and 1 MiB output, cooperative one-thread setting; no hard memory or CPU-affinity cap.

The SHA-256 command returned exit 0 with:

```text
2b936b30df8dfc33d9ee995be7c1cd442b8db8d71c12ca8f2ea0d71048af2f38  audit.py
dfda270c1a10a8f1039c840d8c039f2627d5bfd557d5e67aeaffed3450f99af0  MediumEmission.lean
b5a542e451fc9bd3fa5dfd400621d24f8ae81b74b8e9a19f2be168ac50048665  run_001/results.json
```

All ordinary Lean foundational dependencies are explicitly printed in the result; no `sorryAx` or newly asserted axiom occurs. Existing compiled Mathlib's complete binary dependency closure is trusted rather than independently hashed. The proofs certify the displayed conditional algebra only.

Proofreading scope: new `REPORT.md`, theorem signatures, and this command record. No mathematical-token corrections were required during the final conservative self-review. The physical assumptions and missing action interaction remain explicit unresolved obligations, not typographical issues.

## Coordinator's post-review rerun

The display-precision comment in `audit.py` was corrected from 50 digits to
30 digits; no executable mathematics changed. The same bounded command was
executed again with each `run_001` path replaced by `run_002`, and exited 0.
`run_002/manifest.json` is the current-source evidence record and contains its
exact argv and hashes. The hash block above and `run_001` remain historical
records of the earlier commented source; they are not claimed to match the
current source. The report was also clarified: release-free emission may
jump below the emission threshold, not merely approach it continuously.
