#!/usr/bin/env python3
"""Rerun handoff scripts without allowing their writes to reach original lanes.

This is a reproduction harness, not an independent physics implementation.
Each job gets a fresh copied lane and reads other inputs through a mirror.
Outputs, input access hashes, return code, and structural JSON differences are
retained. A nonzero status is never interpreted as a scientific falsification
without examining the named check. Numerical comparison tolerances are reporting
thresholds only: rtol=1e-8, atol=1e-10, not altered acceptance gates.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CLASS_SITE = os.environ.get('HANDOFF_DEPS', '/private/tmp/handoff-classy-20260927/site')


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def compare(a, b, path=''):
    differences = []
    if any(k in path.lower().split('/')[-1] for k in ('runtime', 'elapsed', 'seconds', 'timestamp')):
        return differences
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(a.keys() | b.keys()):
            if k not in a or k not in b:
                differences.append([path+'/'+k, 'missing key'])
            else:
                differences += compare(a[k], b[k], path+'/'+k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            differences.append([path, 'length', len(a), len(b)])
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                differences += compare(x, y, path+'/'+str(i))
    elif isinstance(a, (int, float)) and not isinstance(a, bool) and isinstance(b, (int, float)) and not isinstance(b, bool):
        import math
        if not (a == b or (math.isnan(a) and math.isnan(b)) or abs(a-b) <= 1e-10 + 1e-8*abs(a)):
            differences.append([path, a, b])
    elif a != b:
        differences.append([path, a, b])
    return differences


def mirror_tree(dst, lane):
    parts = Path(lane).parts
    def build(src, target, rest):
        target.mkdir(parents=True)
        for p in src.iterdir():
            q = target / p.name
            if p.name == rest[0]:
                if len(rest) == 1:
                    shutil.copytree(p, q, ignore=shutil.ignore_patterns('__pycache__'))
                else:
                    build(p, q, rest[1:])
            else:
                q.symlink_to(p, target_is_directory=p.is_dir())
    build(ROOT, dst, parts)


WRAPPER = r'''
import hashlib,json,os,runpy,sys
from pathlib import Path
script, mirror, record, writable = map(Path,sys.argv[1:5])
reads={}; recording=False
def audit(event,args):
 global recording
 if recording or event!='open': return
 filename,mode,flags=args
 if not isinstance(filename,(str,bytes,os.PathLike)): return
 p=Path(filename).absolute()
 write=(isinstance(mode,str) and any(c in mode for c in 'wax+')) or (isinstance(flags,int) and flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
 if write:
  resolved=p.resolve()
  # Temporary CLASS builds and ordinary OS null device are allowed.
  if not (resolved.is_relative_to(writable.resolve()) or str(resolved).startswith('/private/tmp/') or str(resolved).startswith('/private/var/folders/') or str(resolved)=='/dev/null'):
   raise PermissionError('reproduction blocked write outside output scope: '+str(p))
 else:
  try:
   if p.is_file() and (str(p).startswith(str(mirror)) or '/zimmerman-formula/' in str(p)):
    recording=True
    reads[str(p)]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'resolved':str(p.resolve())}
  finally: recording=False
sys.addaudithook(audit)
sys.path.insert(0,str(script.parent))
try:
 runpy.run_path(str(script),run_name='__main__')
finally:
 recording=True
 for name,row in reads.items():
  p=Path(name)
  row['sha256_after']=hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
 record.write_text(json.dumps(reads,indent=2))
'''


def run(relative, mutation, timeout, tag, patch_xr28):
    source = ROOT / relative
    label = source.stem + ('_mutate' if mutation else '_main') + tag
    out = HERE/'reproduction'/label
    out.mkdir(parents=True, exist_ok=False)
    # Git pathspecs inside a mirror nested in the real checkout inherit that
    # nested prefix even with GIT_WORK_TREE set. An external scratch root has
    # no such prefix; source provenance queries then address the real checkout.
    mirror = Path(tempfile.mkdtemp(prefix='handoff-repro-'))/'mirror'
    mirror_tree(mirror, source.parent.relative_to(ROOT))
    script = mirror/relative
    patch_record=None
    if patch_xr28:
        common=script.parent/'XR28_common.py'
        old=common.read_text()
        substitutions=[('(0.43 * k * s / h)', '(0.43 * k * s)'),
                       ('q = k * th * th / ge', 'q = (k / h) * th * th / ge')]
        new=old
        for before_text,after_text in substitutions:
            assert new.count(before_text)==1, 'Ambiguous transfer-function correction'
            new=new.replace(before_text,after_text)
        common.write_text(new)
        shutil.copy2(common,out/'XR28_common_corrected.py')
        patch_record={'source':'real_research/cross_thread_review_2026_09_26/XR28_common.py',
                      'old_sha256':hashlib.sha256(old.encode()).hexdigest(),
                      'new_sha256':hashlib.sha256(new.encode()).hexdigest(),
                      'substitutions':substitutions,
                      'basis':'FP24 fix_block: physical k in Mpc^-1 requires k/h in q and no /h in k*s.'}
        (out/'patch.json').write_text(json.dumps(patch_record,indent=2))
    # Remove old target results, keeping dependency inputs. Never report a stale
    # result copied from the source tree as output of this execution.
    for pattern in (source.stem+'*.out', source.stem+'*_results*.json'):
        for old in script.parent.glob(pattern):
            old.unlink()
    wrapper = out/'execute.py'
    wrapper.write_text(WRAPPER)
    access = out/'inputs_accessed.json'
    env = dict(os.environ, MUTATE=str(int(mutation)), PYTHONPATH=CLASS_SITE,
               GIT_DIR=str(ROOT/'.git'), GIT_WORK_TREE=str(ROOT),
               PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    argv = [sys.executable, str(wrapper), str(script), str(mirror), str(access), str(out)]
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    t = time.monotonic()
    before = digest(source)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    with (out/'stdout.txt').open('w') as stdout, (out/'stderr.txt').open('w') as stderr:
        process = subprocess.Popen(argv,cwd=mirror,env=env,stdout=stdout,stderr=stderr,start_new_session=True)
        (out/'RUNNING.json').write_text(json.dumps({'pid':process.pid,'command':argv,'started_at':started}))
        try:
            rc=process.wait(timeout=timeout); status='completed' if rc==0 else 'failed'
        except subprocess.TimeoutExpired:
            import signal
            os.killpg(process.pid,signal.SIGTERM)
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL);process.wait()
            rc=process.returncode;status='timeout'
    elapsed = time.monotonic()-t
    (out/'RUNNING.json').unlink()
    outputs=[]; diffs={}
    for pattern in (source.stem+'*.out',source.stem+'*_results*.json'):
        for p in script.parent.glob(pattern):
            target=out/p.name;shutil.copy2(p,target)
            outputs.append(target)
            baseline=source.parent/p.name
            if p.suffix=='.json' and baseline.exists():
                diffs[p.name]=compare(json.loads(baseline.read_text()),json.loads(p.read_text()))
    (out/'comparison.json').write_text(json.dumps(diffs,indent=2,allow_nan=True))
    outputs += [out/'stdout.txt',out/'stderr.txt',out/'comparison.json']
    if patch_record: outputs += [out/'patch.json',out/'XR28_common_corrected.py']
    if access.exists(): outputs.append(access)
    summary={'script':relative,'mutation':mutation,'status':status,'exit_code':rc,'runtime_s':elapsed,
             'mirror':str(mirror),
             'patch':patch_record,
             'source_sha256_before':before,'source_sha256_after':digest(source),
             'differences':{k:len(v) for k,v in diffs.items()}}
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    outputs.append(out/'summary.json')
    manifest={
      'schema_version':1,'claim_id':'HR01_'+label,
      'repository':{'commit':commit,'dirty':True},'command':argv,
      'environment':{'software':['Python '+sys.version.split()[0],
        'numpy '+__import__('numpy').__version__, 'scipy '+__import__('scipy').__version__,
        'CLASS 3.3.4.0 local vanilla build', 'dependency path '+CLASS_SITE], 'hardware':os.uname().machine},
      'mathematics':{'assertion_tested':'Reproduce named finite checks in '+relative+(' with deliberate mutation' if mutation else ''),
        'coefficient_domain':'IEEE-754 float64; symbolic operations where source explicitly uses them',
        'conventions':'Original script conventions and both original acceleration footings; original source unchanged; any scratch correction recorded in patch.json',
        'inputs':[relative,'Source dependency reads and before/after hashes in inputs_accessed.json'],
        'bounds':{'wall_seconds':timeout,'parameter_grid':'Unmodified original source grid'},
        'non_claims':['Reproduction does not independently validate the physical surrogate or prove a covariant action.']},
      'randomness':{'used':bool(__import__('re').findall(r'default_rng\((\d+)\)',source.read_text())), 'generator':'numpy default_rng; PCG64; source-local literal seeds (imported defaults remain source-defined)', 'seed':[int(x) for x in __import__('re').findall(r'default_rng\((\d+)\)',source.read_text())] or None},
      'run':{'started_at':started,'runtime_seconds':elapsed,'exit_status':rc},
      'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':digest(p)} for p in outputs],
      'checks':[{'name':'original script unchanged','passed':before==digest(source)}, {'name':'process completed within bound','passed':status!='timeout'}],
      'result':'Execution '+status+'; compare named scientific checks in raw output. '+json.dumps(summary['differences']),
      'residual_risks':['Version-1 manifest limitations; supplemental input access hashes record Python file reads but cannot capture all C-library reads or subprocess git-show inputs.',
        'Numerical thread environment caps are cooperative; original source may override them.',
        'Each job starts from original lane outputs, so reproduces original dependencies rather than silently substituting prior reruns.']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    # Scratch mirror is disposable execution state, never a scientific output.
    # Leave it available during the task; do not commit it.
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('scripts',nargs='+')
    parser.add_argument('--timeout',type=int,default=2400)
    parser.add_argument('--mode',choices=['pair','main','mutate'],default='pair')
    parser.add_argument('--tag',default='')
    parser.add_argument('--patch-xr28-spectrum',action='store_true')
    args=parser.parse_args()
    for name in args.scripts:
        for mutation in ([True,False] if args.mode=='pair' else [args.mode=='mutate']):
            run(name,mutation,args.timeout,args.tag,args.patch_xr28_spectrum)
