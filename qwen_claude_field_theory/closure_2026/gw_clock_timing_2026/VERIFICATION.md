# Verification and change record

## Scope and files

Only new research files were added under these two directories:

```
qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/
qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/
```

The first contains REPORT.md, this record, timing_audit.py, verify.py,
TimingIdentities.lean, ReviewedClaudeTime.lean, contract.json, run_001
provenance/results, and verification_001/verification_002 per-command logs/summary.

The second contains README.md and:

```
boosted/
  REPORT.md
  derive_boosted.py, result.json
  test_boosted.py
  check_archived_jets.py, archived_jets.json
  tensor_cone.py, tensor_result.json, tensor_result_v2.json
  clock_lapse.py, clock_lapse_result.json
  ClockGeometry.lean
health/
  REPORT.md, contract.json, audit_health.py, HealthSign.lean
  run_001/{manifest.json,stdout.txt,stderr.txt}
  pressure/
    REPORT.md, contract.json, audit_pressure.py, PressureIdentity.lean
    run_001/{manifest.json,stdout.txt,stderr.txt}
    run_002/{manifest.json,stdout.txt,stderr.txt}
  turning/
    REPORT.md, contract.json, audit_turning.py, TurningBound.lean
    run_001/{manifest.json,stdout.txt,stderr.txt}
```

The first pressure run and first tensor output are preserved historical
checkpoints. Current evidence is pressure/run_002 and tensor_result_v2.json.
Do not validate old source hashes against revised code as if they were a fresh
run. No existing theory coefficients or other agents' files were modified.

## Fresh consolidated execution

From the repository root:

```sh
python3 -B qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/verify.py --output qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/verification_001
PYTHONOPTIMIZE=1 python3 -B qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/verify.py --output qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/verification_002
```

Both exited **0**. All **14 research child commands** returned exit 0 and passed their
verification conditions in each run. `verification_002/summary.json` records the exact
expanded argv, working directory, source hashes before/after, compiler axiom
sets and duration for every child. It is the authoritative command inventory.
Reruns require a new output directory; old logs are never overwritten.
The second run follows independent review: it explicitly disables child
Python optimization and tests both an enabled assertion and an intentionally
false assertion, even with optimization enabled in the parent environment.
The negative-control child exits 1 as required; it is not a failed scientific
test. This prevents inherited optimization from silently dropping checks.
The summary pins entry-script hashes, not the entire import/dependency tree;
separate computation manifests supply the declared mathematical input hashes.

| Child | Result |
|---|---|
| timing_audit.py | 16 symbolic checks; 50/90-digit arithmetic checks; exit 0 |
| boosted/derive_boosted.py | 21 exact checks; exit 0 |
| boosted/test_boosted.py | independent inversion, zero-mode, boost and source controls; exit 0 |
| boosted/check_archived_jets.py | six archived jets re-evaluated; exit 0 |
| boosted/tensor_cone.py | 13 computed action/cone checks; exit 0 |
| boosted/clock_lapse.py | 8 connection/clock checks; exit 0 |
| health/audit_health.py | 19 checks; exit 0 |
| health/pressure/audit_pressure.py | 29 checks; exit 0 |
| existing mond_braiding_completion/derive.py | previous same-action radial/cubic closure regression; exit 0 |
| TimingIdentities.lean | 5 conditional theorems; exit 0 |
| ReviewedClaudeTime.lean | 3 original Claude statements/proofs isolated; exit 0 |
| boosted/ClockGeometry.lean | 5 geometric theorems; exit 0 |
| health/HealthSign.lean | 3 sign theorems; exit 0 |
| health/pressure/PressureIdentity.lean | 2 corrected pressure identities; exit 0 |

There are 15 new small Lean theorems and 3 checked existing theorem excerpts.
All printed axiom sets contain only `propext`, `Classical.choice`, `Quot.sound`.
No full covariant action variation or empirical law is formalized by them.
The verification driver explicitly requires compiler exit 0, nonempty axiom
output, allowed axioms, and unchanged source hashes. Only two processes run
concurrently, with 90-second per-command timeouts and numerical thread caps.

The final additional turning-point audit ran after that suite:

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/closure_front_2026/health/turning/audit_turning.py
```

Exit **0**, 16 checks. Its `TurningBound.lean` was compiled with
`lake env lean` and its absolute source path from the same pinned Lean
directory: exit **0**, three theorems, only the same standard axiom set.
Its own report gives the exact independent runner/validator commands and
`health/turning/run_001` contains their provenance. Including this follow-up,
**18 new small Lean theorems** and **3 original excerpts** were checked.

Software: Python 3.9.6, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4,
mpmath 1.3.0; Lean 4.34.0-rc2 in the existing pinned Mathlib project at
`clock_constitutive_construction_2026/lean_formalization_2026`.

## Timing computation provenance

The independent bounded timing run and manifest validation also exited 0:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/carlzimmerman/new_physics/zimmerman-formula --contract qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/contract.json --input qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/timing_audit.py --output qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/run_001 --result qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/run_001/results.json --timeout 90 --max-output-bytes 1048576 --max-cpu-seconds 60 --max-threads 1 -- python3 -B qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/timing_audit.py --output qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/run_001/results.json
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/gw_clock_timing_2026/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Health and pressure reports give their additional exact runner/validator
commands. The repository contains unrelated concurrent changes, recorded in
the manifests; a passing local check does not certify those changes.

## Important unsuccessful build attempts

The entire existing `fable_independent_2026/lean_2026/Mondlean.lean` was **not**
successfully rebuilt in this investigation:

1. `lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026/Mondlean.lean`
   from the pinned closure Lean project: exit **1**, import environment
   conflict involving `Asymptotics.IsEquivalent` in Mathlib modules. This is
   a dependency/build failure, not a refutation of the new algebra.
2. `lake env lean Mondlean.lean` from its own `fable_independent_2026/lean_2026`
   directory: exit **1**, missing local dependency materialization and blocked
   Reservoir lookup (`curl` code 6). No dependencies were installed or repaired.

The three new statements/proofs were therefore isolated, without changing
their premises or mathematical content, as ReviewedClaudeTime.lean. Their
successful compilation verifies those implications, not the 114-theorem
parent module. This limitation must not be hidden behind the successful
focused suite.

## Scientific verdict

Clock geometry and homogeneous equal tensor/photon cones: derived under
stated assumptions. Proposed L206 cubic pressure correction: refuted for the
canonical tracked branch. L207/L208 window: not a certified search gate.
Full relativistic MOND theory, global wave transport, scalar health, PPN,
CMB/galaxy/cluster closure and origin of time: **OPEN**.

Next calculation: the complete coupled retarded response on an on-shell
inhomogeneous background of the same frozen action, with the physical metric
and source response derived rather than assigned.
