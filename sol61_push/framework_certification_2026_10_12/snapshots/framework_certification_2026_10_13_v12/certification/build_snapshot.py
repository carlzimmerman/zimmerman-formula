"""Freeze a local research checkpoint; no publication or Git mutation."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from zoneinfo import ZoneInfo
from evidence_revision import resolve_evidence, dispositions

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
name=sys.argv[1]
if not name.replace('_','').isalnum():
    raise ValueError('Use an alphanumeric snapshot name')
destination=HERE/'snapshots'/name
artifact=HERE/'artifacts'/(name+'.tar.gz')
if destination.exists() or artifact.exists():
    raise ValueError('Existing checkpoints are immutable; choose a new name')
sources={}
versions={}
def add_source(path, expected):
    source, historical = resolve_evidence(path, expected)
    versions[(path, expected)] = {'path': path, 'sha256': expected,
        'copy': str(source.relative_to(ROOT)), 'historical_primary_context': historical}
    old = sources.get(path)
    if old is not None and old != expected:
        # Both revisions must independently resolve through the exact reviewed disposition.
        resolve_evidence(path, old)
        live_sha = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if live_sha not in {old, expected}:
            raise ValueError('Competing unreviewed source snapshots: ' + path)
        sources[path] = live_sha
    else:
        sources[path] = expected
for record in ['assumptions/assumption_register.json','assumptions/closure_gate_graph.json']:
    data=json.loads((HERE/record).read_text())
    for entry in data['source_snapshots']:
        add_source(entry['path'], entry['sha256'])
for path in ['CITATION.cff','LICENSE.md','fable_independent_2026/lean_2026/lean-toolchain',
             'fable_independent_2026/lean_2026/lakefile.toml',
             'fable_independent_2026/lean_2026/lake-manifest.json',
             'sol61_push/hamiltonian_drift_2026_10_12/HANDOFF.md',
             'sol61_push/hamiltonian_drift_2026_10_12/REPORT.md',
             'sol61_push/kinetic_receiver_lift_2026_10_12/FROZEN_CRITERIA.txt',
             'sol61_push/kinetic_receiver_lift_2026_10_12/DERIVATION.txt',
             'sol61_push/kinetic_receiver_lift_2026_10_12/LOCAL_DERIVATION.txt',
             'sol61_push/kinetic_receiver_lift_2026_10_12/LOCAL_RESULT.txt',
             'sol61_push/kinetic_receiver_lift_2026_10_12/LOCAL_CRITERIA.txt',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_checks.py',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_control.py',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_run/manifest.json',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_run/results.json',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_control_run/manifest.json',
             'sol61_push/kinetic_receiver_lift_2026_10_12/local_control_run/results.json']:
    source=ROOT/path
    if source.is_file():add_source(path, hashlib.sha256(source.read_bytes()).hexdigest())
for rel in ['HANDOFF.txt', 'interaction_admission/RESULT.txt',
            'interaction_admission/FROZEN_CRITERIA.txt', 'interaction_admission/checks.py',
            'interaction_admission/INPUTS.json', 'interaction_admission/run/manifest.json',
            'interaction_admission/run/results.json']:
    path = 'sol61_push/kinetic_receiver_lift_2026_10_12/' + rel
    source = ROOT / path
    if not source.is_file():
        raise ValueError('Missing reviewed interaction admission source: ' + path)
    add_source(path, hashlib.sha256(source.read_bytes()).hexdigest())
spatial_root = ROOT / 'sol61_push/carrier_spatial_transport_2026_10_13'
for source in spatial_root.rglob('*'):
    if source.is_file() and '__pycache__' not in source.parts:
        if source.is_symlink():
            raise ValueError('No live symlinks in spatial evidence')
        path = str(source.relative_to(ROOT))
        add_source(path, hashlib.sha256(source.read_bytes()).hexdigest())
# Retain exact original-path primary sources of the prospective join audit.
for review in list((HERE / 'shared_phase_audit').glob('*.json')) + list((HERE / 'gravitational_work_audit').glob('*.json')) + list((HERE / 'minimal_metric_audit').glob('*.json')) + list((HERE / 'metric_uniqueness_audit').glob('*.json')) + list((HERE / 'metric_coordination').glob('*.json')) + list((HERE / 'nonspherical_audit').glob('*.json')):
    data = json.loads(review.read_text())
    if not isinstance(data, dict):
        continue
    for path, expected in data.get('source_sha256', data.get('source_hashes', {})).items():
        if path.startswith('sol61_push/framework_certification_2026_10_12/'):
            continue
        add_source(path, expected)
for path,sha in sources.items():
    resolve_evidence(path, sha)
destination.mkdir(parents=True)
for path in sorted(HERE.rglob('*')):
    rel=path.relative_to(HERE)
    if any(x in {'snapshots','artifacts','__pycache__'} for x in rel.parts):continue
    if path.is_file():
        if path.is_symlink():raise ValueError('No live symlinks in snapshot')
        target=destination/'certification'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,target)
for path in sorted(sources):
    target=destination/'evidence_inputs'/path
    target.parent.mkdir(parents=True,exist_ok=True)
    source, _ = resolve_evidence(path, sources[path])
    shutil.copyfile(source,target)
# Preserve every reviewed source version with its exact original identity.
for record in versions.values():
    if record['historical_primary_context']:
        target=destination/'evidence_versions'/record['sha256']/record['path']
        target.parent.mkdir(parents=True,exist_ok=True)
        source, historical = resolve_evidence(record['path'], record['sha256'])
        assert historical
        shutil.copyfile(source,target)
(destination/'SOURCE_VERSIONS.json').write_text(json.dumps(list(versions.values()),indent=2)+'\n')
entries=[]
for file in sorted(destination.rglob('*')):
    if file.is_file():
        entries.append({'path':str(file.relative_to(destination)),
                        'bytes':file.stat().st_size,
                        'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
now=datetime.now(timezone.utc)
current_state=json.loads((HERE/'STATE.json').read_text())
current_inventory=json.loads((HERE/'CERTIFIED_CLAIMS.json').read_text())
if current_state['checkpoint']!=current_inventory['checkpoint']:
    raise ValueError('State and certificate inventory name must agree')
record={'checkpoint':current_state['checkpoint'],'snapshot_name':name,
        'created_utc':now.isoformat(),'created_user_timezone':now.astimezone(ZoneInfo('America/New_York')).isoformat(),
        'observed_git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'original_designated_base_git':'8cef73ea7d01e20f1d08f435ad621b739f8eb3cc',
        'whole_theory_certified':False,'files':entries,
        'scope':'Local content-hashed research record; no public timestamp, digital signature or priority guarantee. Installed Lean/Mathlib dependencies are pinned but not bundled.'}
(destination/'CHECKPOINT_MANIFEST.json').write_text(json.dumps(record,indent=2)+'\n')
artifact.parent.mkdir(exist_ok=True)
with tarfile.open(artifact,'w:gz') as archive:
    archive.add(destination,arcname=name)
archive_sha=hashlib.sha256(artifact.read_bytes()).hexdigest()
artifact.with_suffix(artifact.suffix+'.sha256').write_text(archive_sha+'  '+artifact.name+'\n')
# Verify every member by its recorded bytes after the archive is created.
with tarfile.open(artifact,'r:gz') as archive:
    for entry in entries:
        stream=archive.extractfile(name+'/'+entry['path'])
        if stream is None or hashlib.sha256(stream.read()).hexdigest()!=entry['sha256']:
            raise ValueError('Archive member mismatch')
print(json.dumps({'archive':str(artifact),'sha256':archive_sha,'files':len(entries),'bytes':artifact.stat().st_size,'all_member_hashes_verified':True}))
