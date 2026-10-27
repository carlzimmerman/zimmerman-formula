"""Freeze this bounded phase and its exact audited dependencies, including v13."""
from pathlib import Path
import hashlib, json, tarfile, io

ROOT = Path(__file__).resolve().parents[3]
PHASE = Path(__file__).resolve().parent
ARTIFACT = PHASE.parent / 'artifacts/latest_work_2026_10_13_v1.tar.gz'
sha = lambda data: hashlib.sha256(data).hexdigest()

def main():
    audit = json.loads((PHASE / 'audit/results.json').read_text())
    selected = {}
    for rel, expected in audit['source_hashes'].items():
        data = (ROOT / rel).read_bytes()
        assert sha(data) == expected, ('reviewed dependency changed', rel)
        selected[rel] = data
    for path in PHASE.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            selected[str(path.relative_to(ROOT))] = path.read_bytes()
    assert (PHASE / 'audit/SYNTHESIS_REVIEW.json').is_file(), 'final synthesis review required'
    synthesis = json.loads((PHASE / 'audit/SYNTHESIS_REVIEW.json').read_text())
    assert synthesis['accepted'] is True
    assert sha((PHASE / 'RESULT.txt').read_bytes()) == synthesis['report_sha256']
    manifest = {'scope': 'immutable v13 baseline plus reviewed latest-work delta',
                'conditional_statements': 187, 'modules': 22,
                'new_statements': 9, 'new_exact_checks': 29,
                'whole_theory_certified': False,
                'files': {k: sha(v) for k, v in sorted(selected.items())}}
    ARTIFACT.parent.mkdir(exist_ok=True)
    assert not ARTIFACT.exists(), 'immutable archive already exists'
    with tarfile.open(ARTIFACT, 'w:gz') as archive:
        for name, data in sorted(selected.items()):
            item = tarfile.TarInfo(name); item.size = len(data); item.mtime = 0
            archive.addfile(item, io.BytesIO(data))
        data = json.dumps(manifest, indent=2).encode() + b'\n'
        item = tarfile.TarInfo('CHECKPOINT_MANIFEST.json'); item.size = len(data)
        archive.addfile(item, io.BytesIO(data))
    with tarfile.open(ARTIFACT) as archive:
        stored = json.load(archive.extractfile('CHECKPOINT_MANIFEST.json'))
        assert stored == manifest
        assert set(archive.getnames()) == set(selected) | {'CHECKPOINT_MANIFEST.json'}
        for name, expected in stored['files'].items():
            assert sha(archive.extractfile(name).read()) == expected, name
    record = {'archive': str(ARTIFACT.relative_to(ROOT)),
              'sha256': sha(ARTIFACT.read_bytes()), 'members_verified': len(selected)+1,
              'bytes': ARTIFACT.stat().st_size, 'manifest': manifest,
              'all_members_verified': True, 'whole_theory_certified': False}
    (PHASE.parent / 'LATEST_WORK_CHECKPOINT.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k != 'manifest'}, indent=2))

if __name__ == '__main__':
    main()
