# Execution and exit-status record

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
For readability B below is
`qwen_claude_field_theory/closure_2026/clock_response_repair_2026`, and N is
`B/nonlinear_clock_response_2026`. Expand these path abbreviations in commands.
Every bounded run's manifest records its **exact expanded command argv**, input
hashes, resource limits, timestamps, exit status and captured output.

## Inspection and preservation

`git status --short`, `git status --short --untracked-files=no`, and
`git log -5 --oneline`: exit 0. The observed base was `1be42350b`; the preceding
L196 output-only commit was `53b1869f5`. Existing tracked modification
`fable_independent_2026/FINDINGS.md` and unrelated untracked work were preserved.
Targeted `rg --files` and `sed` reads inspected current scientific sources,
tests, same-action inputs, and new independent results. No old coefficient
functions or archived runs were edited.

## Scientific scripts, tests and formal certificate

| Execution | Exit | Evidence |
|---|---:|---|
| `python3 N/action/run_checks.py --result-file N/action/run_001/result.json` under bounded runner | 0 | Full S2/S3/S4 generator, five tests, exact covariant/ADM and S2 checks, finite-amplitude/contour controls |
| `python3 N/action/run_initial_checks.py --result-file N/action/run_002/result.json` under bounded runner | 0 | Mean/2k initial response and its regression |
| `python3 -B -m unittest discover -s N/action -p 'test_*.py'` coordinator rerun | 0 | Six tests, 11.199 s |
| `python3 -B -m unittest discover -s N/clock -p 'test_*.py'` coordinator rerun | 0 | Eight tests |
| `python3 N/clock/clock_response.py --run-tests --output N/clock/run_002/result.json` under bounded runner | 0 | Eight tests, fourteen existing covariant checks, symbolic derivations and implicit-root controls; exact argv in manifest |
| `python3 -B N/review/derive_audit.py` direct | 0 | 32 exact identities plus independent stationary root |
| `python3 -B N/run_certificates.py` | 0 | New bounded independent review and Lean runs, each validated against current inputs |

`run_certificates.py` executes:

```bash
python3 -B N/review/derive_audit.py --output N/review/run_001/result.json
```

and, from the existing
`qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026`
directory:

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_clock_response_2026/ClockElimination.lean
```

Direct and bounded Lean compilation: exit **0**. Ten conditional lemmas;
axiom output contains only `propext`, `Classical.choice`, `Quot.sound`.
This is not a formal covariant field-equation or Dirac certificate.

Canonical v2 manifests:

- `action/run_001/manifest.json`
- `action/run_002/manifest.json`
- `clock/run_002/manifest.json`
- `review/run_001/manifest.json`
- `lean_001/manifest.json`
- `regression/run_001/manifest.json`

All six were checked with this exact validator invocation after expanding
MANIFEST to the corresponding repository-relative path:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Each exit was **0**. A valid manifest certifies a bounded execution record,
not its physical interpretation. Earlier `clock/exploratory_*/result.json`
and `clock/run_001/result.json` are retained development outputs, not the
canonical certified record. `clock/run_002` supersedes them without overwriting.

## Existing regressions, freshly rerun

`regression/run_regressions.py --output N/regression/run_001/result.json`
ran under the bounded runner with four concurrent subprocesses, one
cooperative numerical thread per subprocess, and project-read auditing.
All **92 existing tests and four additional checks exited 0**, no timeouts.
The parent runtime was 9.681 s. The exact per-job argv, cwd, logs, input-read
inventory, counts and exit statuses are in `regression/run_001/result.json`.

| Directory under B | Tests |
|---|---:|
| `variance_closure_2026/geometry` | 8 |
| `variance_closure_2026/evolution` | 4 |
| `variance_closure_2026/vertices` | 5 |
| `cosmological_bridge_2026` | 35 |
| `inhomogeneous_charge_2026/exterior` | 5 |
| `inhomogeneous_charge_2026/current` | 9 |
| `inhomogeneous_charge_2026/constraints` | 5 |
| `inhomogeneous_charge_2026/tracking` | 5 |
| `finite_gradient_metric_2026` (root test files only) | 4 |
| `finite_gradient_metric_2026/cubic` | 6 |
| `finite_gradient_background_2026` | 6 |

The extra existing checks were `mond_braiding_completion/derive.py`,
`mond_braiding_completion/CubicRelations.lean`, `dirac_operator/ellipticity.py`,
and `dirac_operator/lapse_source.py`, all exit 0. Their new output files are
under `regression/run_001`, not overwritten into old result paths.
Counting the fourteen new unit tests gives 106 unit tests across the stated
scopes, not 106 newly solved physics requirements.

The independent reviewer also reran the new initial-response test (exit 0),
recomputed the clock current identity with arbitrary lapse/shift (zero
symbolic residual), and checked the spatial residual on 65 rather than 512
points. This additional review is described in REPORT.md; it is not another
complete-theory formalization.

## Integration

Only N is eligible for this checkpoint commit. Integration commands are
`git add -N -- N`, `git diff --check -- N`, an exact-path-only
`git commit --only -m MESSAGE -- N`, and `git push origin HEAD:main`.
Actual commit/push outcomes are supplied in the final handoff rather than
being predeclared here. No broad staging, force push, reset, or concurrent-file
cleanup is authorized by this record.

Before integration a concurrent commit `d28d97ba1` appeared, committing
Claude's L197/L198 work and the previously dirty FINDINGS.md. It was left
untouched. `git show --stat --oneline d28d97ba1` and targeted L198 source/result
reads exited 0. The companion DF2 note records a limited read-only audit;
L198 was not rerun or promoted to same-action evidence. All six new manifests
still validated against current source hashes after this concurrent commit.
