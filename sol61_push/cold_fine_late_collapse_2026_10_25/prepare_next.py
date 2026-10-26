"""Prepare, but never execute, a fresh bounded continuation contract."""
import argparse, hashlib, json, re, shlex, sys
from pathlib import Path

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('galaxy', choices=['Draco', 'Sextans'])
ap.add_argument('tag')
ap.add_argument('--check-only', action='store_true')
a = ap.parse_args()
assert re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', a.tag)
dest = P / a.tag
contract = P / (a.tag + '_contract.json')
assert not dest.exists() and not contract.exists()
parent = P / (a.galaxy + '_fine_late')
pd = json.loads((parent / 'result.json').read_text())
assert pd['status'] == 'wall stop' and pd['birth_time'] is None
assert pd['ne'] == 8192 and pd['local_tolerance'] == 1.25e-8
assert pd['inputs_before'] == pd['inputs_after']
sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
for f, h in pd['inputs_before'].items():
    assert sha(ROOT / f) == h
for f, h in pd['raw_sha256'].items():
    assert sha(parent / f) == h
for k, lim in dict(mass=1e-8, energy=1e-4, phase=.05, boundary=1e-4).items():
    assert pd['maxima'][k] <= lim
files = {str(f.relative_to(ROOT)) for f in [Path(__file__).resolve(), P/'NEXT.md']}
seen = set()
def include_manifest(path):
    if path in seen:
        return
    seen.add(path)
    files.add(str(path.relative_to(ROOT)))
    m = json.loads(path.read_text())
    assert m['run']['status'] == 'completed' and m['run']['exit_status'] == 0
    for x in m['input_artifacts'] + m['outputs']:
        f = ROOT / x['path']
        assert sha(f) == x['sha256']
        if 'sha256_after' in x:
            assert x['sha256_after'] == x['sha256']
        files.add(x['path'])
        if f.name == 'manifest.json':
            include_manifest(f)
include_manifest(parent/'manifest.json')
d = json.loads((P/(a.galaxy+'_contract.json')).read_text())
d['claim_id'] = 'CCT021_NEXT_' + a.tag.upper()
d['mathematics']['bounds'].update(parent=str(parent.relative_to(ROOT)), wall_seconds=1800)
d['mathematics']['assertion_tested'] = 'Next explicit bounded original-history fine segment, preserving original gates and first birth'
d['execution_artifacts'] = sorted(files)
payload = json.dumps(d, indent=2)
runner = '/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
cmd = ['/opt/homebrew/bin/python3', runner, '--root', str(ROOT), '--contract', str(contract)]
for f in d['execution_artifacts']:
    cmd += ['--input', f]
cmd += ['--output', str(dest.relative_to(ROOT))]
for f in ['result.json', 'field.npz', 'stars.npz']:
    cmd += ['--result', str((dest/f).relative_to(ROOT))]
cmd += ['--timeout','2100','--max-output-bytes','1048576','--max-cpu-seconds','1950','--max-threads','1','--', '/usr/bin/python3', str(P.parent/'cold_pre_stellar_settling_2026_10_25/continue_gated.py'), '--galaxy', a.galaxy, '--ne','8192','--tol','1.25e-8','--T','8','--wall','1800','--out',str(dest),'--resume',str(parent)]
if not a.check_only:
    with contract.open('x') as f:
        f.write(payload)
print(json.dumps(dict(galaxy=a.galaxy, parent_T=pd['t'], check_only=a.check_only, launched=False, contract=str(contract), contract_sha256=hashlib.sha256(payload.encode()).hexdigest(), artifacts=len(files), command=shlex.join(cmd)), indent=2))
