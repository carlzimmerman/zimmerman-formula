"""Verify this checkpoint's recorded evidence without modifying research inputs."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    snapshots = json.loads((HERE / 'snapshot_index.json').read_text())
    aliases = {}
    for item in snapshots:
        path = HERE / item['snapshot']
        assert digest(path) == item['sha256'], str(path)
        aliases[item['original']] = path
    index = json.loads((HERE / 'canonical_runs.json').read_text())
    counts = []
    for item in index['runs']:
        manifest_path = ROOT / item['manifest']
        manifest = json.loads(manifest_path.read_text())
        assert manifest['run']['status'] == 'completed', str(manifest_path)
        assert manifest['run']['exit_status'] == 0
        for artifact in manifest['input_artifacts']:
            path = ROOT / artifact['path']
            if not path.is_file():
                path = aliases[artifact['path']]
            assert digest(path) == artifact['sha256'], str(path)
            assert artifact['sha256_after'] == artifact['sha256']
        for artifact in manifest['outputs']:
            path = ROOT / artifact['path']
            assert digest(path) == artifact['sha256'], str(path)
        result = json.loads((manifest_path.parent / 'results.json').read_text())
        checks = result['checks']
        assert len(checks) == item['checks'], str(manifest_path)
        assert all(c.get('ok', c.get('passed', False)) is True for c in checks)
        counts.append(len(checks))
    assert sum(counts) == index['total_checks'] == 888
    assert len(counts) == 16
    print('Verified 16 recorded runs, 888 passing checks, and declared artifact hashes.')
    print('This validates evidence integrity, not physical theory closure.')


if __name__ == '__main__':
    verify()
