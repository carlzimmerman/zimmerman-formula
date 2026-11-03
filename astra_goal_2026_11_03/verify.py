"""Verify the AZ reporting phase without reading or writing other lane outputs.
Usage: python3 astra_goal_2026_11_03/verify.py PATH_TO_MANIFEST_VALIDATOR
"""
import hashlib,json,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
validator=Path(sys.argv[1]);checks=[];runs=[]
def check(name,ok,detail=''):
    checks.append({'name':name,'passed':bool(ok),'detail':detail})
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
lanes=sorted(HERE.glob('P*/AZ*'))
check('eleven lanes',len(lanes)==11,str(len(lanes)))
for lane in lanes:
    script=lane/'run.py';result=lane/'results.json';old=result.read_bytes()
    run=subprocess.run([sys.executable,str(script.relative_to(ROOT))],cwd=ROOT,env=env,capture_output=True,text=True,timeout=30)
    check(lane.name+' execution',run.returncode==0,run.stderr[:200])
    check(lane.name+' deterministic results',old==result.read_bytes())
    r=json.loads(result.read_text());expected_bad=4 if lane.name.startswith('AZ9_') else 0
    if 'checks' in r:bad=sum(not c['passed'] for c in r['checks'])
    else:bad=sum(not v for d in r['footings'].values() for v in d['checks'].values())
    check(lane.name+' control outcomes',bad==expected_bad,f'failed checks {bad}; expected {expected_bad}')
    check(lane.name+' both footings',set(r['footings'])=={'canonical','alt'})
    validate=subprocess.run([sys.executable,str(validator),str((lane/'manifest.json').relative_to(ROOT)),'--root','.'],cwd=ROOT,capture_output=True,text=True)
    check(lane.name+' manifest',validate.returncode==0,validate.stdout.strip() or validate.stderr.strip())
    cp=git('log','--reverse','--format=%H','--',str((lane/'CRITERIA.md').relative_to(ROOT))).splitlines()[0]
    sp=git('log','--reverse','--format=%H','--',str(script.relative_to(ROOT))).splitlines()[0]
    ancestry=subprocess.run(['git','merge-base','--is-ancestor',cp,sp],cwd=ROOT).returncode==0
    check(lane.name+' criteria before committed script',cp!=sp and ancestry,f'criteria {cp}; script {sp}')
    runs.append({'lane':lane.name,'label':r['label'],'result_sha256':hashlib.sha256(result.read_bytes()).hexdigest()})
for p in range(1,7):check(f'P{p} STATUS exists',(HERE/f'P{p}/STATUS.md').is_file())
coverage=json.loads((HERE/'coverage.json').read_text())
for c in coverage['candidates']:
    check(c['candidate']+' coverage shape',len(c['requirement_rows'])==12 and len(c['rq3_expanded_rows'])==99 and len(c['rq3_grouped_rows'])==96)
    check(c['candidate']+' counts',c['requirements_both_count']==0 and c['rq3_expanded_both_count']==0 and c['rq3_grouped_both_count']==0)
check('summary and owner needs',(HERE/'SUMMARY.md').is_file() and (HERE/'NEEDS_OWNER.md').is_file())
private=[]
for p in HERE.rglob('*'):
    if p.is_file() and '__pycache__' not in p.parts:
        try:s=p.read_text()
        except UnicodeDecodeError:continue
        # Avoid embedding any user's actual name or home prefix in this source.
        if ('/'+'Users'+'/') in s or ('/'+'home'+'/') in s:private.append(str(p.relative_to(HERE)))
check('no home paths in artifacts',not private,','.join(private))
commits=git('log','--format=%H','--',str(HERE.relative_to(ROOT))).splitlines()
foreign=[]
for rev in commits:
    paths=git('diff-tree','--no-commit-id','--name-only','-r',rev).splitlines()
    foreign.extend((rev,p) for p in paths if not p.startswith('astra_goal_2026_11_03/'))
check('all goal commits scoped to allowed directory',not foreign,str(foreign))
report={'disclaimer':'κ = ½ FITTED; not theory closed','scope':'artifact/provenance verification; not scientific closure','evidence_revision':git('rev-parse','HEAD'),'validator_sha256':hashlib.sha256(validator.read_bytes()).hexdigest(),'runs':runs,'checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(HERE/'VERIFICATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(bool(report['failed']))
