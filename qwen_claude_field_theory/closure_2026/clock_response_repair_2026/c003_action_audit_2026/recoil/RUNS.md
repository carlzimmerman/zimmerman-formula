# Recoil audit execution record

The successful result directories are `numeric_run_002` and `lean_run_003`. Their runner manifests are the authoritative argv, UTC timing, environment, input-hash, and output-hash records. Both were additionally validated with `validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula`; both returned exit 0 and `valid evidence record; mathematical interpretation requires review`.

The assigned base was `1f0306787590840947e8e22cadfcabb9e162bb8d`. A concurrent unrelated commit moved the shared checkout to `5a87447af258ec132f6cedb5170dc8dd4c03f038` before execution; the runner records that actual HEAD, with dirty state true. `git diff 1f0306787590840947e8e22cadfcabb9e162bb8d -- fable_independent_2026/L189_clock_frame_kicks.py fable_independent_2026/L189_results.json` returned no difference, exit 0. No Fable/Hermes inputs were edited and this agent made no Git commit.

| Run | Child/runner exit | Elapsed seconds | Result |
|---|---:|---:|---|
| `numeric_run_001` | 1/1 | 1.362770 | Failed strict massive-grid comparison because computing `gamma^2-1` loses precision at `beta=1e-8` |
| `numeric_run_002` | 0/0 | 1.804806 | Passed after algebraically identical stable `gamma^2 beta^2` radicand; original precision and tolerances preserved |
| `lean_run_001` | 1/1 | 10.334221 | Umbrella Mathlib.Tactic imports unavailable cached asymptotics module |
| `lean_run_002` | 1/1 | 21.464735 | Narrow tactic imports load, but missing explicit real-number import prevents elaboration |
| `lean_run_003` | 0/0 | 13.800682 | Five theorems check after Mathlib.Data.Real.Basic import and autoImplicit=false |

The failed records retain the actual logs and former source hashes. Their input files were then repaired, so they are historical failed attempts rather than current fresh evidence. They should not be mistaken for the successful final certificates.

The small numerical cancellation diagnostic used `mpmath` at 80 digits and returned an error of `1.41015e-73` for the cancellation-prone root, versus `1.05422e-81` after using the algebraically equivalent stable root, exit 0. It motivated the implementation fix rather than relaxing a tolerance.

An initial environment probe `lake env lean --version` in `fable_independent_2026/lean_2026` could not resolve its missing dependency manifest: Reservoir/curl failed with code 6; the shell probe ended with exit 1. No package or manifest appeared there (`git status --short -- fable_independent_2026/lean_2026` was empty). Subsequent certification uses the existing local compiled package directory and raw Lean, so it performs no network operation or Lake write.

## Reproduce into fresh output directories

From the repository root, set the following task-specific shell variables. Replace the output suffixes with fresh names if they already exist; the runner refuses to overwrite an evidence directory.

```bash
recoil_root=/Users/carlzimmerman/new_physics/zimmerman-formula
recoil_base=qwen_claude_field_theory/closure_2026/clock_response_repair_2026/c003_action_audit_2026/recoil
recoil_runner=/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py
python3 "$recoil_runner" --root "$recoil_root" --contract "$recoil_root/$recoil_base/numeric_contract.json" \
  --input fable_independent_2026/L189_results.json \
  --input fable_independent_2026/L189_clock_frame_kicks.py \
  --input "$recoil_base/recoil_audit.py" \
  --output "$recoil_base/numeric_run_fresh" --result "$recoil_base/numeric_run_fresh/results.json" \
  --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- \
  python3 "$recoil_base/recoil_audit.py" --result "$recoil_base/numeric_run_fresh/results.json"
python3 "$recoil_runner" --root "$recoil_root" --contract "$recoil_root/$recoil_base/lean_contract.json" \
  --input "$recoil_base/RecoilAccounting.lean" --input "$recoil_base/check_lean.py" \
  --output "$recoil_base/lean_run_fresh" --result "$recoil_base/lean_run_fresh/results.json" \
  --timeout 200 --max-output-bytes 1048576 --max-threads 1 -- \
  python3 "$recoil_base/check_lean.py" --result "$recoil_base/lean_run_fresh/results.json"
```

Numerical precision: 80 decimal digits; no RNG. The caps are 60/200 seconds and 1 MiB log output; conventional numerical thread limits request one thread and may be ignored by libraries. No memory, CPU-time, or affinity cap was requested for these small algebra runs. Python 3.9.6, SymPy 1.14.0, mpmath 1.3.0, Lean 4.34.0-rc2; hardware reported by runner is macOS 26.5.2, arm64.

Lean uses the absolute binary and colon-separated LEAN_PATH recorded in its result, importing only existing compiled package directories under `clock_constitutive_construction_2026/lean_formalization_2026/.lake/packages`. Its one harmless linter warning concerns the stylistic use of `<;>` instead of `;`; it reports no proof error. All five `#print axioms` results contain only `propext`, `Classical.choice`, and `Quot.sound`.

## SHA-256 of final scientific inputs and outputs

```text
09f630707350fe84f723218c2cf34563803e07304ca03ff55117e40f409dbb87  recoil_audit.py
f112f347f864d27ff5e3f1d185ef0b1baaf34b618d6f6093537dbb01d66e31c7  RecoilAccounting.lean
496f7191e0946c15dc42a1d6aac01fab36579cdff28c84943016aba863030993  check_lean.py
14b427ff13c2a6aaa1df64cbe04348ffc18890b0f2a841b910aa4e6508605716  numeric_run_002/results.json
37f6669ef303f054c57a7235978f1f3c1cc8c8c7182a5b7d29fdb25423add1cc  lean_run_003/results.json
```

`shasum -a 256` verified these five hashes, exit 0. The full manifests also pin the original L189 inputs and raw log files.

## Mathematical proofreading self-review

Scope: `RECOIL_AUDIT.md`, `SOURCE_CHECK.md`, and `RUNS.md`, plus the stated theorem signatures in `RecoilAccounting.lean`. Equations were checked for consistent mass/energy units, physical branches, finite versus infinite Poisson support, and local symbol definitions. Routine edits: none required after creation. Mathematical-token changes during proofreading: none. Unresolved issues are the physical inputs explicitly labeled incomplete in the report; no full classical/quantum theory or observational result is certified.
