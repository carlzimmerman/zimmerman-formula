# Reproduce the bounded checks

Run from the repository root. The stored runs used Python 3.9.6, SymPy 1.14.0
and, for regular-core shell quadrature, mpmath 1.3.0. Each stored manifest
records its own command, software, input/output hashes, resource limits and
actual exit status. The analytic proofs carry the uniform statements.

## Re-run without modifying stored evidence

Choose fresh output paths; for example:

```bash
python3 sol61_push/ambient_support_round2_2026_10_15/action/check_neutral_support.py /tmp/as2-action-recheck.json
python3 sol61_push/ambient_support_round2_2026_10_15/self_gravity/check_self_gravity.py /tmp/as2-gravity-recheck.json
python3 sol61_push/ambient_support_round2_2026_10_15/regular_core/check_regular_core_v2.py /tmp/as2-core-recheck.json
python3 sol61_push/ambient_support_round2_2026_10_15/patch/check_patch.py /tmp/as2-patch-recheck.json
```

Expected authoritative counts: action 36 exact; self-gravity 56 exact;
regular core v2 19 exact plus 3 potential quadratures and 7 gate samples;
patch 15 exact plus 12 blend controls. The patch blend controls use 50-digit
SymPy numerical evaluation; they are not additional exact sign proofs. Core
gate samples also use numerical comparison of exact radical formulas. Do not overwrite the recorded run
folders. The regular-core original script/run_v1 is preserved as a valid
17-check predecessor; v2 adds two independent normalization controls.

For the bounded-run command with time/thread caps, use each lane's
computation contract and the command fields of its manifest. The original
mathbox runner was
`/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/run_experiment.py`.
Its companion `validate_manifest.py` validates schema and hashes against
`--root /Users/carlzimmerman/new_physics/zimmerman-formula`.
A fresh checkout need not have that plugin to run the scripts or the portable
hash check below. The contracts record the actual resource caps; single-thread
environment limits are cooperative, not a process sandbox or memory ceiling.

## Portable input/output integrity check

```python
from pathlib import Path
import hashlib, json
root = Path.cwd()
packet = root / 'sol61_push/ambient_support_round2_2026_10_15'
for manifest in sorted(packet.rglob('manifest.json')):
    record = json.loads(manifest.read_text())
    if record.get('schema_version') != 2:
        continue
    assert record['run']['status'] == 'completed'
    assert record['run']['exit_status'] == 0
    for item in record['input_artifacts'] + record['outputs']:
        actual = hashlib.sha256((root / item['path']).read_bytes()).hexdigest()
        assert actual == item['sha256'], (manifest, item['path'])
    print('hashes match:', manifest.relative_to(root))
```

This portable check is integrity verification, not a proof validator. Review
`regular_core/PROOF.md`, `stability/PLUMMER_CHECK.md`, `joint_audit/REPORT.md`
and `patch/AUDIT.md` together for assumptions, normalization audits and limits.
The pinned source snapshot manifest distinguishes originally tracked files
from local source reports copied for reproducibility.
