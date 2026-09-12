# Commands and results

From `/Users/carlzimmerman/new_physics/zimmerman-formula`, the exact verification invocation is:

```sh
'python3' '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/carlzimmerman/new_physics/zimmerman-formula' '--contract' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/contract.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/verify.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/probe.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/test_probe.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/adm/derive_chi_adm.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/history/derive_history.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/history/HistorySigns.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_principal_audit/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_background_completion/derive.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_finite_wavelength/run_001/derivation.json' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/metric_response/derive_static_metric.py' '--input' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/principal_gate/ResponseGate.lean' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lean-toolchain' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lakefile.toml' '--input' 'qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026/lake-manifest.json' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/run_001' '--result' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/run_001/checks/summary.json' '--timeout' '180' '--max-output-bytes' '2097152' '--max-threads' '1' '--' 'python3' '-B' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/verify.py' '--output' 'qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/run_001/checks'
```

For another run replace all three path arguments containing `/run_001` with an unused output path. Each child's exact argv, cwd, exit status, hashes and axiom sets are recorded in `run_001/checks/summary.json`. The runner enforces a 180-second total limit and cooperative single-thread numeric cap; the child harness uses two workers and 90 seconds per job.

Validation command:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/finite_wavelength/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The analogous `adm/run_001` and `history/run_001` manifests record their independent earlier executions. The source unit test first exited 1 with the intended `conserved matter probe not implemented` assertion; its implemented run exited 0. `probe.py` development run exited 0.

Repository checks executed: `git status --short --untracked-files=no`, `git log -5 --oneline`, `git fetch origin`, and `git rev-list --left-right --count HEAD...origin/main` (the latter returned `0 0` before this commit). The unrelated journal edit was preserved. No tracked action, history, prior proof, published paper or earlier output was changed.

The raw history stdout contains an extra terminal newline; it is retained
byte-for-byte for provenance. The final whitespace check therefore uses
`git -c core.whitespace=-blank-at-eof diff --cached --check`.
