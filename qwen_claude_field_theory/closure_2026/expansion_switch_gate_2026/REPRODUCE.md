# Reproduction and audited checkpoint

Run from the repository root. Base revision:
`b7bb6bb3cb0c8241f8470f0ac312daf8d1f15d87`.
Python 3.13.9 / SymPy 1.13.1; independent reviewer used SymPy 1.14.
No installation, observational dataset, fitted simulation or Lean certificate.

## Exact scientific commands executed and exits

```bash
git status --short
git log -6 --format='%h %ad %an %s' --date=iso-strict
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/adm_principal.py
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/expansion_switch.py --require-two-tensor
OPENBLAS_NUM_THREADS=1 python -B qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/cuscuton_screen.py --require-two-tensor
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/gate1_constitutive_2026 -v
OPENBLAS_NUM_THREADS=1 python -B -m unittest discover -s qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026 -v
git diff --check
```

| Run | Exit | Meaning |
|---|---:|---|
| Raw ADM derivation | 0 | Nine variational/identity residuals vanish |
| New combined unit suite | 0 | 22 tests pass, including exceptional strata and signed controls |
| Expansion-switch physical acceptance | **2** | Rejected in the specified local static principal sector |
| Bare-cuscuton physical acceptance | **2** | Added lapse potential breaks the seed's constraint mechanism |
| Prior FLRW suite | 0 | 10 tests pass |
| Prior constitutive suite | 0 | 8 tests pass |
| Prior cluster audit suite | 0 | 9 tests pass; no claim of a new empirical test |
| Final provenance run, run_002 | 0 | Computation completed, NOT a theory PASS |
| run_002 manifest/hash validation | 0 | Current inputs and outputs match the recorded run |
| Whitespace check | 0 | No whitespace errors |

There are **49 passing unit tests**, while both new physical acceptance gates
fail. This distinction is intentional. No rank, determinant, PPN value or
gravitational count is supplied as an expected input to a derivation.
Hand-computed expected results occur in regression tests, not in construction
of the canonical matrices.

Development tests ran before implementation and failed for the named missing
features (exit 1). A real adapter error then collected residual dictionary
keys rather than values; the unchanged identity test caught it and the adapter
was corrected. Later missing-limit, separate-evidence, and general-F tests
also failed first, then passed. No physical sign or rank was changed to make
an acceptance test pass.

## Recorded runs

`run_002/manifest.json` is the final version-2 evidence record. It contains
the exact launched argv, resolved paths, commit/dirty state, software,
input hashes before and after, execution status, duration and output hashes.
The runner used timeout=60 seconds, max-output-bytes=1048576 and cooperative
numerical-library max-threads=1. No hard memory/CPU/affinity cap was requested.

The portable equivalent below uses AUDIT_SCRIPTS for the installed Mathbox
computation-audit `scripts` directory. The resolved invocation is recorded in
the tool history; the scientific child command and file inputs are recorded
in the manifest. A reproduction must use a **fresh** run directory, replacing
all three occurrences of run_002. Existing results are never overwritten.

```bash
OPENBLAS_NUM_THREADS=1 python -B "$AUDIT_SCRIPTS/run_experiment.py" \
  --root . \
  --contract qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/contract.json \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/adm_principal.py \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/expansion_switch.py \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/test_expansion_switch.py \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/cuscuton_screen.py \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/test_cuscuton_screen.py \
  --input qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/DECISION.md \
  --input qwen_claude_field_theory/closure_2026/vcdm_flrw_gate_2026/vcdm_flrw.py \
  --output qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/run_002 \
  --result qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/run_002/result.json \
  --timeout 60 --max-output-bytes 1048576 --max-threads 1 -- \
  python -B qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/expansion_switch.py \
  --output qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/run_002/result.json
OPENBLAS_NUM_THREADS=1 python -B "$AUDIT_SCRIPTS/validate_manifest.py" \
  qwen_claude_field_theory/closure_2026/expansion_switch_gate_2026/run_002/manifest.json --root .
```

`run_001` is retained as a **superseded** development snapshot. It completed
successfully before the final independent review tightened the domain and
matter/Schur-complement qualifications. Its pinned report and code hashes
therefore do not match current inputs; do not use it as a freshness certificate.
The final run preserves the same derived signs and ranks with the corrected
scope. Its replacement was a new run, not an edited manifest.

## Review and non-claims

The Mathbox computation audit required action construction, fixed controls,
actual Poisson differentiation, exceptional-mode handling and immutable run
provenance. Independent proof review reconstructed the static canonical block
and general-F restriction, then required three scope corrections: a product
domain for F(s,K); fixed canonical matter in the lapse-complement calculation;
and strong degeneracy as an affine-lapse research target, not a universal
necessity. These corrections are incorporated in DECISION.md and run_002.
Mathematical proofreading of the new report checked definitions, signs and
equation/prose consistency; it supplied no additional proof certificate.

The full nonlinear metric-plus-clock system is not counted here. A local
principal scalar is a rejection of the intended regular galactic branch,
not a theorem that every MOND action is impossible. No new PPN values, data
fit or observational prediction is certified. The complete-theory goal remains
OPEN; the specific expansion-switch repair is DEAD for that target branch.

## Exact new-file inventory

All 16 files below are confined to this new directory:

- `adm_principal.py`
- `expansion_switch.py`
- `test_expansion_switch.py`
- `cuscuton_screen.py`
- `test_cuscuton_screen.py`
- `DECISION.md`
- `REPRODUCE.md`
- `contract.json`
- `run_001/manifest.json`
- `run_001/result.json`
- `run_001/stdout.txt`
- `run_001/stderr.txt`
- `run_002/manifest.json`
- `run_002/result.json`
- `run_002/stdout.txt`
- `run_002/stderr.txt`

The two stderr files are empty and hashed. No prior action, prior result,
empirical artifact, or unrelated dirty working-tree file was changed.
