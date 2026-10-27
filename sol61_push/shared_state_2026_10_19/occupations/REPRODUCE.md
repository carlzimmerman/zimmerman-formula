# Reproduction and evidence status

All paths below are relative to
`/Users/carlzimmerman/new_physics/zimmerman-formula` unless absolute.
The source note and program are frozen at the hashes in `run_001/manifest.json`.

`run_001` completed on 2026-10-19 in 0.252 seconds. The mathematical code
reports **198 checks passed**: 51 oscillator/thermal/pulse checks, 21 checks
on complete microcanonical shells, 73 exact finite quantum-model controls,
and 53 cutoff/thermal TLS quadrature controls. The process used a 45-second
wall cap, 30-second per-process CPU cap, 1-MiB combined-log cap and one
numerical-library thread. No memory or CPU-affinity cap was requested.
Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4 were recorded.

The largest matrix has dimension four; all quadratures are one-dimensional.
There are no stochastic samples, formation simulations, heavy jobs,
manuscript/action changes or external writes. Successful finite tests
verify the listed algebra controls, not an original-model shared medium.

Validate the existing evidence without rerunning:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/shared_state_2026_10_19/occupations/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

This command was executed and reported
`valid evidence record (run status: completed)`; stderr from the scientific
run is empty. The manifest pins before/after code, source-note and original
input hashes, the exact command, dirty repository state and outputs. The
repository was already concurrently dirty. Observed initial HEAD was
`3ac0427149a2108afa8f102df4d82da33b9060c4`; the pin/run HEAD was
`aa0d1a83d15c1fe2a0c9d32f189bdbbff49dd19a`. Byte hashes, rather than
the changing shared HEAD, identify the exact reviewed inputs.

For an authorized fresh rerun, the following constructs the same runner
command from the contract's explicit dependency list. `run_002` must not
already exist; use another fresh directory name if it does.

```bash
python3 - <<'PY'
import json, pathlib, subprocess
root = pathlib.Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
lane = 'sol61_push/shared_state_2026_10_19/occupations/'
contract = json.loads((root / (lane + 'contract.json')).read_text())
runner = '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
output = lane + 'run_002'
result = output + '/checks.json'
argv = ['python3', runner, '--root', str(root), '--contract', lane + 'contract.json']
for artifact in contract['execution_artifacts']:
    argv.extend(['--input', artifact])
argv.extend(['--output', output, '--result', result, '--timeout', '45',
             '--max-output-bytes', '1048576', '--max-cpu-seconds', '30',
             '--max-threads', '1', '--', 'python3',
             lane + 'check_occupations.py', '--output', result])
subprocess.run(argv, cwd=root, check=True)
PY
```

## Interpretation and review provenance

Outcome: **implementation and finite assertion verified in the stated range**.
The universal analytic theorem is supported by the explicit contour-resolvent
proof in `OCCUPATIONS.md`, not by four-state numerical agreement. The finite
TLS example is deliberately an imposed diagnostic spectrum. Its error
certificate is `0.0010999587534367746` on the stated force interval; that
establishes a mathematically viable approximation, not physical spectrum
selection. The six thermal TLS examples have susceptibilities strictly
between zero and their ground-state value, as (17) requires.

The author performed analytic self-review of (1)–(17), source checking,
implementation inspection and manifest validation. The final proofreading
pass covered the new mathematical note and sibling finite-k review:
routine edits none; mathematical-token changes none; unresolved typographical
issues none. An independent parent review is recorded separately if supplied.
`FINITE_K_REVIEW.md` is this lane's independent focused review of the parent's
physical finite-k static response, with exact artifact hashes and scope.

The primary source consulted was Gardiner and Morgan,
`arXiv:cond-mat/0610623v2`, version header 29 January 2007, checked directly
on arXiv on 2026-10-19. Equations (98)–(101) and Section V.3 were extracted
only to check the finite-number/bosonic-algebra caveat. No exact finite-N
Bose law is inferred from that source, and no novelty claim is made.

The physical task remains open: state inventories/energy, formation,
source-carrying actual modes of the selected phase, their nonlinear
continuation or local saturators, and gravitational normalization have not
all been supplied by this lane. The finite gapped branch restriction does
not exclude critical/continuum/infinite-state alternatives.
