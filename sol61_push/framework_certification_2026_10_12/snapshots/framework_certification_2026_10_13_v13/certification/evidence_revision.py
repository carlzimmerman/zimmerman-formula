"""Resolve explicitly reviewed historical primary inputs without refreshing their premises."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
REGISTRY = HERE / 'nonspherical_audit/HISTORICAL_PRIMARY_DISPOSITION.json'

def dispositions():
    return json.loads(REGISTRY.read_text())['records'] if REGISTRY.exists() else []

def resolve_evidence(path, expected):
    live = ROOT / path
    if sha(live) == expected:
        return live, False
    for rec in dispositions():
        if rec['source'] == path and rec['recorded_historical_sha256'] == expected:
            old = ROOT / rec['historical_copy']
            current_copy = ROOT / rec['current_copy']
            assert sha(old) == expected, 'Historical primary copy changed'
            assert sha(live) == sha(current_copy) == rec['current_sha256'], 'Unreviewed primary revision'
            assert (ROOT / rec['reviewed_in']).is_file(), 'Missing revision review'
            return old, True
    raise AssertionError('Unreviewed evidence change: ' + path)

def validate_record(manifest, validator, allow_reconstruction=True):
    obj = json.loads(manifest.read_text())
    affected = []
    reviewed = {(r['source'], r['recorded_historical_sha256']) for r in dispositions()}
    for artifact in obj.get('input_artifacts', []) if allow_reconstruction else []:
        if (artifact['path'], artifact['sha256_after']) in reviewed:
            _, old = resolve_evidence(artifact['path'], artifact['sha256_after'])
            if old:
                affected.append(artifact['path'])
    if not affected:
        result = subprocess.run([sys.executable, str(validator), str(manifest), '--root', str(ROOT)], capture_output=True, text=True)
        return result, []
    # Reconstruct only the exact artifact tree required by this unchanged v2 manifest.
    # Copy files: symlinks would escape the validator's project-root check.
    assert obj['schema_version'] == 2
    with tempfile.TemporaryDirectory(prefix='framework-evidence-validation-') as directory:
        stage = Path(directory)
        for artifact in obj['input_artifacts']:
            path = artifact['path']
            source, _ = resolve_evidence(path, artifact['sha256_after'])
            target = stage / path
            assert not Path(path).is_absolute() and target.resolve().is_relative_to(stage.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        for artifact in obj['outputs']:
            path = artifact['path']; target = stage / path
            assert not Path(path).is_absolute() and target.resolve().is_relative_to(stage.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        staged_manifest = stage / manifest.relative_to(ROOT)
        staged_manifest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(manifest, staged_manifest)
        result = subprocess.run([sys.executable, str(validator), str(staged_manifest), '--root', str(stage)], capture_output=True, text=True)
    return result, affected
