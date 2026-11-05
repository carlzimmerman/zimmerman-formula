#!/usr/bin/env python3
"""Live SIGTERM/resume, idempotence and row-chunk pairs on8x8 raw pilots."""
import argparse,json,signal,subprocess,sys,time
from pathlib import Path
import raw_cube as R
import io_beam as B
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='raw_verified');a=ap.parse_args()
base=R.HERE/a.tag
if base.exists():raise RuntimeError('Use a fresh tag')
base.mkdir();checks=[]
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
def cmd(tag,weight='NA',rows=32,extra=()):return [sys.executable,'-W','error',str(R.HERE/'raw_cube.py'),'--weight',weight,'--binning','8','--row-chunk',str(rows),'--tag',tag,*extra]
def run(tag,weight='NA',rows=32,extra=()):
    with (base/f'{tag.split("/")[-1]}_{weight}_{rows}.log').open('a') as log:return subprocess.run(cmd(tag,weight,rows,extra),stdout=log,stderr=subprocess.STDOUT,timeout=120).returncode
def directory(tag,weight='NA',rows=32):return R.HERE/tag/f'{weight}_bin8_rows{rows}'
for weight in ['NA','R']:
    for rows in [32,64]:
        code=run(a.tag+'/baseline',weight,rows);check(f'{weight}_{rows}_complete',code==0)
    p=[directory(a.tag+'/baseline',weight,r)/'raw_manifest.json' for r in [32,64]]
    x,y=[json.loads(f.read_text()) for f in p]
    check(weight+'_row_pair_scientific',x['scientific']==y['scientific'])
    check(weight+'_row_pair_array_hashes',x['output_hashes']==y['output_hashes'])
tag=a.tag+'/interrupted';out=directory(tag);signalled=False;cursor=None
with (base/'interrupt.log').open('w') as log:
    child=subprocess.Popen(cmd(tag),stdout=log,stderr=subprocess.STDOUT)
    deadline=time.monotonic()+60
    while child.poll() is None and time.monotonic()<deadline:
        p=out/'checkpoint.json'
        if p.exists():
            v=json.loads(p.read_text());cursor=len(v['planes'])
            if cursor>=1 and child.poll() is None and not (out/'raw_manifest.json').exists():
                child.send_signal(signal.SIGTERM);signalled=True;break
        time.sleep(.005)
    code=child.wait(timeout=60)
check('live_SIGTERM_checkpoint_exit75',signalled and code==75,dict(cursor_at_signal=cursor,exit_code=code))
check('resume_completes',run(tag,extra=['--resume'])==0)
reference=directory(a.tag+'/baseline')/'raw_manifest.json';actual=out/'raw_manifest.json'
check('resumed_manifest_byte_identical',reference.read_bytes()==actual.read_bytes())
saved=actual.read_bytes();check('complete_resume_idempotent',run(tag,extra=['--resume'])==0 and actual.read_bytes()==saved)
obj=json.loads(saved);first=next(iter(obj['identity']['hashes']));obj['identity']['hashes'][first]='deliberately stale'
actual.write_text(json.dumps(obj));code=run(tag,extra=['--resume']);actual.write_bytes(saved)
check('stale_identity_rejected',code!=0)
result=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
            source_hashes={p.name:R.sha(p) for p in [Path(__file__),Path(R.__file__),Path(B.__file__),R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md']},
            scope='Raw8x8 preparation only; masks/full fits not tested; kappa=1/2 FITTED; not theory closed')
B.atomic(R.HERE/'raw_resume_checks.json',result);print(json.dumps(result,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
