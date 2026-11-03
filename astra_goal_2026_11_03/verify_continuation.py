"""Read-only verification of all AZ evidence; writes one report in this tree."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
validator=Path(sys.argv[1]);checks=[]
def check(name,ok,detail=''):checks.append({'name':name,'passed':bool(ok),'detail':detail})
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
lanes=sorted(HERE.glob('P*/AZ*'));check('17 frozen lanes',len(lanes)==17)
for lane in lanes:
 r=json.loads((lane/'results.json').read_text());m=json.loads((lane/'manifest.json').read_text())
 check(lane.name+' labels',r['label'] in ['PASS','FAIL','NO VERDICT','NOT EVALUABLE'] and set(r['footings'])=={'canonical','alt'})
 check(lane.name+' disclaimer',r.get('disclaimer')=='κ = ½ FITTED; not theory closed')
 bad=sum(not c['passed'] for c in r['checks']) if 'checks' in r else sum(not v for d in r['footings'].values() for v in d['checks'].values())
 expected=4 if lane.name.startswith('AZ9_') else 1 if lane.name.startswith('AZ17_') else 0
 check(lane.name+' preserved control outcomes',bad==expected,f'{bad} failed controls; expected {expected}')
 run=subprocess.run([sys.executable,str(validator),str(lane/'manifest.json'),'--root',str(ROOT)],capture_output=True,text=True)
 check(lane.name+' manifest validation',run.returncode==0,(run.stdout+run.stderr).strip())
 unchanged=True
 for a in m['input_artifacts']:
  unchanged &= hashlib.sha256((ROOT/a['path']).read_bytes()).hexdigest()==a['sha256']==a['sha256_after']
 for a in m['outputs']:unchanged &= hashlib.sha256((ROOT/a['path']).read_bytes()).hexdigest()==a['sha256']
 check(lane.name+' current hashes',unchanged)
 cp=git('log','--reverse','--format=%H','--',str((lane/'CRITERIA.md').relative_to(ROOT))).splitlines()[0]
 sp=git('log','--reverse','--format=%H','--',str((lane/'run.py').relative_to(ROOT))).splitlines()[0]
 check(lane.name+' criteria before script commit',cp!=sp and subprocess.run(['git','merge-base','--is-ancestor',cp,sp],cwd=ROOT).returncode==0)
 check(lane.name+' criteria ancestor of recorded run',subprocess.run(['git','merge-base','--is-ancestor',cp,m['repository']['commit']],cwd=ROOT).returncode==0)
for n in range(1,7):
 p=HERE/f'P{n}/STATUS.md';check(f'P{n} status',(p.is_file() and 'κ = ½ FITTED; not theory closed' in p.read_text()))
v=json.loads((HERE/'coverage.json').read_text())
for c in v['candidates']:
 check(c['candidate']+' all rows',len(c['requirement_rows'])==12 and len(c['rq3_expanded_rows'])==99 and len(c['rq3_grouped_rows'])==96)
 for rows,key in [('requirement_rows','requirements_both_count'),('rq3_expanded_rows','rq3_expanded_both_count'),('rq3_grouped_rows','rq3_grouped_both_count')]:
  count=sum(x['both_footings_credited'] for x in c[rows].values());check(c['candidate']+' '+key,c[key]==count==0)
foreign=[]
for rev in git('log','--format=%H','--','astra_goal_2026_11_03').splitlines():
 for p in git('diff-tree','--no-commit-id','--name-only','-r',rev).splitlines():
  if not p.startswith('astra_goal_2026_11_03/'):foreign.append((rev,p))
check('local commits scoped',not foreign,str(foreign))
private=[]
for p in HERE.rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:
  try:s=p.read_text()
  except UnicodeDecodeError:continue
  if ('/'+'Users'+'/') in s or ('/'+'home'+'/') in s:private.append(str(p.relative_to(HERE)))
check('no private home paths',not private,str(private))
report={'disclaimer':'κ = ½ FITTED; not theory closed','evidence_revision':git('rev-parse','HEAD'),'scope':'Read-only artifact, hash, chronology, preserved-control and coverage audit. Not an independent proof review or scientific closure. No computations rerun or archived manifests rewritten.','checks':checks,'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks)}
(HERE/'FINAL_VERIFICATION.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'passed':report['passed'],'failed':report['failed'],'failures':[c for c in checks if not c['passed']]},indent=2))
raise SystemExit(bool(report['failed']))
