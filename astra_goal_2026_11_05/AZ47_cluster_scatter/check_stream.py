#!/usr/bin/env python3
"""Fresh bounded prefix, chunk-pair and real SIGTERM/resume verification."""
import argparse,hashlib,json,signal,sqlite3,subprocess,sys,time
from pathlib import Path
import g3 as G
ap=argparse.ArgumentParser();ap.add_argument('--tag',default='stream_final_contract');args=ap.parse_args()
base=G.HERE/args.tag
if base.exists():raise RuntimeError('Use a fresh --tag')
base.mkdir()
common=[sys.executable,str(G.HERE/'stream.py'),'--foot','canonical','--mode','real','--level','L1']
def run(tag,chunk,limit,extra=()):
    cmd=common+['--tag',tag,'--chunk',str(chunk),'--max-chunks',str(limit),*extra]
    with (base/(tag.split('/')[-1]+f'_{chunk}_{limit}.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=60)
    return r.returncode
def directory(tag,chunk):return G.HERE/tag/'L1_canonical_real'/f'chunk{chunk}'
tag1=args.tag+'/baseline';tag2=args.tag+'/interrupted';tag3=args.tag+'/repeat'
assert run(tag1,1000,20,['--verify-templates'])==0
assert run(tag1,1000,20)==75
assert run(tag1,2000,10)==75
assert run(tag3,1000,20)==75
cmd=common+['--tag',tag2,'--chunk','1000','--max-chunks','20']
with (base/'interrupt.log').open('w') as log:
    child=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT);interrupted=False;cursor=None
    deadline=time.time()+30
    while child.poll() is None and time.time()<deadline:
        dbpath=directory(tag2,1000)/'checkpoint.sqlite'
        if dbpath.exists():
            try:
                with sqlite3.connect(dbpath,timeout=.01) as db:
                    rec=db.execute('SELECT data FROM state WHERE id=1').fetchone()
                if rec:
                    cursor=json.loads(rec[0])['rows']
                    if cursor>=1000 and child.poll() is None:child.send_signal(signal.SIGTERM);interrupted=True;break
            except sqlite3.OperationalError:pass
        time.sleep(.005)
    code=child.wait(timeout=30)
if not interrupted or code!=75:raise RuntimeError('No verified live interruption')
with sqlite3.connect(directory(tag2,1000)/'checkpoint.sqlite') as db:rows=json.loads(db.execute('SELECT data FROM state WHERE id=1').fetchone()[0])['rows']
remaining=(20000-rows)//1000
assert 0<remaining<=20
assert run(tag2,1000,remaining,['--resume'])==75
checks=[]
def check(name,passed,value=None):checks.append(dict(name=name,passed=bool(passed),value=value))
check('SIGTERM_live_exit75',interrupted and code==75,dict(cursor_when_signalled=cursor,rows_after_checkpoint=rows))
for mode in ['main','mutate']:
    files=[directory(t,c)/mode/'result.json' for t,c in [(tag1,1000),(tag1,2000),(tag2,1000),(tag3,1000)]]
    a,b,c,d=[json.loads(p.read_text()) for p in files]
    for key in ['rows','unique_valid_formulas','unique_covariance_err','unique_stable_covariance_err']:
        check(mode+'_chunk_'+key,a['scientific'][key]==b['scientific'][key],a['scientific'][key])
    for key,value in a['scientific']['statistics'].items():
        other=b['scientific']['statistics'][key]
        ok=(value==other) if not isinstance(value,float) else abs(value-other)<=1e-10*max(abs(value),1e-300)
        check(mode+'_statistics_'+key,ok,None)
    check(mode+'_resume_byte_identical',files[0].read_bytes()==files[2].read_bytes())
    check(mode+'_repeat_byte_identical',files[0].read_bytes()==files[3].read_bytes())
tc=json.loads((directory(tag1,1000)/'template_checks.json').read_text())
check('all_template_decodings',all(c['passed'] for c in tc['checks']),len(tc['checks']))
G.atomic(G.HERE/'stream_contract.json',dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
                                         stream_sha256=hashlib.sha256((G.HERE/'stream.py').read_bytes()).hexdigest(),
                                         scope='20,000-row prefix only; no completed census or physical verdict'))
print('stream checks',sum(c['passed'] for c in checks),'/',len(checks));raise SystemExit(int(not all(c['passed'] for c in checks)))
