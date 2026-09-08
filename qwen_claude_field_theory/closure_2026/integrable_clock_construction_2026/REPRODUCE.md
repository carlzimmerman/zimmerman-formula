# Reproduce IC-1 construction checkpoint

Run from the repository root. Runtime: Python 3.13.9 (Anaconda), SymPy 1.13.1,
NumPy 1.26.4. No network or empirical data are used by these calculations.

## Exact scientific commands executed

```bash
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py --require-full-closure
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/lapse_braiding_gate_2026 -p 'test_*.py' -v
git diff --check
```

| Check | Observed result | Exit |
| --- | --- | --- |
| New computation tests, final run | 9 passed | 0 |
| Construction derivation (recorded runner below) | Exact residuals zero; computed rank6 kinetic block, rank4 homogeneous constraints; OPEN | 0 |
| Full-goal reporting gate | Missing proof obligations retained; **not a certificate** | 2 |
| Relevant existing lapse/primary closure tests | 32 passed | 0 |
| Patch whitespace | Clean | 0 |

Development test-first runs failed intentionally before implementation: five
missing derivation tests, then two missing family/spatial functions, then one
missing Ward function. Each exited1; the implemented final suite exits0.
These were missing-code checks, not physical counterexamples. An intermediate
six-test and an eight-test suite also passed. All newly created scientific
scripts were executed.

## Pinned run

This exact argv was executed using the installed computation-audit runner:

```bash
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/contract.json --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/ACTION.md --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py --input qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/test_integrable_clock.py --output qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/run_001 --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- python -B qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/integrable_clock.py
python -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/integrable_clock_construction_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Both exited0. The manifest pins the actual base commit, dirty-state observation,
input hashes, command, software, limits and stdout/stderr. Use a **new output
directory** for a new recorded run; do not overwrite run_001. On another machine,
resolve its installed runner and project-root paths before reproducing.
Library thread caps are cooperative, not a hardware-resource guarantee.

Read-only independent review of module SHA256
`c6a5b227aed84fa53829659327ef986c2fc813a4888455515da52d651322cce3`
recomputed the primary bracket and homogeneous PB determinant relation and
reran tests/default CLI/reporting gate: exits0/0/2. No blocker was found within
the report's deliberately limited claims; full-field obligations remain open.

## Files in this checkpoint

New: ACTION.md, REPORT.md, REPRODUCE.md, contract.json, integrable_clock.py,
test_integrable_clock.py, run_001/manifest.json, run_001/stdout.txt,
run_001/stderr.txt. Existing file changed: ../CRISPY_FRIED_CHICKEN_RECIPE.md
(current-candidate link only). No prior scientific code or dirty G03 work changed.

The strongest result is the exact canonical integrability identity plus an
expanding, regular, positive-homogeneous-kinetic branch of the same action.
Full theory: **OPEN**. Next calculation: inhomogeneous scalar reduction and
the secondary functional constraint operator on that exact background.
