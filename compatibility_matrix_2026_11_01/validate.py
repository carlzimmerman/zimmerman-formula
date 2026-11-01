"""Validate CM01 documentary integrity; this does not rerun or certify physics."""
import hashlib,json,re,sys
from datetime import datetime,timezone
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parent
failures=[];checks=0

def check(ok,message):
 global checks
 checks+=1
 if not ok:failures.append(message)
def read(name):return json.loads((P/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
required={'id','name','family','parent','status','result','obstruction','scope','requirements','nonrepeat','next_new_step','sources','aliases'}
statuses={'scoped_obstruction','finite_failure','fitted_partial','conditional_positive','open','in_progress','owner_closed','inconclusive','data_audit','corrected'}
fragments=[r for name in ['foundational','observational','audit','coordinator']for r in read(name+'_rows.json')]
combined=read('lane_matrix.json');rows=combined['rows'];requirements=combined['requirements']
check(rows==fragments,'Assembled rows differ from source fragments')
check(len({r['id']for r in rows})==len(rows),'Duplicate lane IDs')
check(set(requirements)=={f'C{i:02d}'for i in range(1,13)},'Common obligations differ from contract')
sources=read('sources.json');by_source={r['id']:r for r in sources}
area_sources=[r for p in sorted((P/'inputs').glob('*/SOURCES.json'))for r in json.loads(p.read_text())]
check(sources==area_sources,'Combined source index differs from area indexes')
check(len(by_source)==len(sources),'Duplicate source capture IDs')
for r in rows:
 i=r['id'];check(required<=set(r),f'{i}: incomplete schema')
 check(r['status']in statuses,f'{i}: invalid status')
 check(bool(r['requirements'])and set(r['requirements'])<=set(requirements),f'{i}: missing/unknown obligation')
 check(bool(r['sources'])and set(r['sources'])<=set(by_source),f'{i}: missing/unknown evidence')
 check(all(isinstance(r[k],str)and bool(r[k].strip())for k in required-{'requirements','sources','aliases'}),f'{i}: empty textual judgment')
 check(isinstance(r['aliases'],list),f'{i}: aliases not list')
check(sum(r.get('coverage_level')=='index_summary_only'for r in rows)==11,'Summary-family coverage count changed')
drift=[]
for s in sources:
 p=P/s['snapshot_path']
 check(p.is_file()and not p.is_symlink(),f'{s["id"]}: missing/nonregular capture')
 if p.is_file():
  check(sha(p)==s['sha256'],f'{s["id"]}: snapshot hash mismatch')
  check(p.stat().st_size==s['bytes'],f'{s["id"]}: snapshot byte mismatch')
 original=ROOT/s['source_path']
 current=sha(original)if original.is_file()else None
 if current!=s['sha256']:drift.append({'id':s['id'],'source_path':s['source_path'],'captured_sha256':s['sha256'],'current_sha256':current})
a=read('architecture_matrix.json');ids={r['id']for r in rows}
check(a['requirements']==requirements,'Architecture obligation definitions differ')
check(len({r['id']for r in a['architectures']})==len(a['architectures']),'Duplicate architecture ID')
for r in a['architectures']:
 check(set(r['cells'])==set(requirements),f'{r["id"]}: incomplete cells')
 check(set(r['evidence'])<=ids and bool(r['evidence']),f'{r["id"]}: invalid architecture evidence')
 for k,c in r['cells'].items():
  check(c['status']in a['cell_statuses'],f'{r["id"]}/{k}: invalid cell status')
  check(bool(c['note'])and bool(c['evidence'])and set(c['evidence'])<=ids,f'{r["id"]}/{k}: missing/invalid cell support')
 if r['id']=='A09':check(all(c['status']=='open'for c in r['cells'].values()),'Unbuilt integration target inherits a pass')
# Every claim has a visible row and an explicit non-repetition entry.
lanes=(P/'LANE_MATRIX.md').read_text();nonrepeat=(P/'NON_REPETITION.md').read_text()
for r in rows:
 check(f'## {r["id"]}\n'in lanes,f'{r["id"]}: missing rendered lane')
 check(f'[{r["id"]}]'in nonrepeat,f'{r["id"]}: missing non-repetition row')
# Check package-authored Markdown links. Captured source reports retain their original relative contexts.
link_count=0
for p in P.glob('*.md'):
 for target in re.findall(r'\[[^\]]*\]\(([^)\n]+)\)',p.read_text()):
  if re.match(r'[a-z]+:',target):continue
  filename,_,anchor=target.partition('#')
  dest=(p.parent/filename).resolve()if filename else p
  link_count+=1;check(dest.is_file(),f'{p.name}: missing link {target}')
  if anchor and dest==P/'LANE_MATRIX.md':check(anchor in {x.lower()for x in ids},f'{p.name}: unknown lane anchor {target}')
# Optional independent review manifest freezes the inspected semantic artifacts.
review_manifest=P/'REVIEWED_FILES.json'
check((P/'REVIEW.md').is_file(),'Independent review missing')
check(review_manifest.is_file(),'Independent review hashes missing')
if review_manifest.exists():
 for r in read('REVIEWED_FILES.json'):
  check((P/r['path']).is_file()and sha(P/r['path'])==r['sha256'],f'Reviewed file changed: {r["path"]}')
for p in P.rglob('*'):
 if p.is_symlink():check(False,f'Unexpected symlink: {p.relative_to(P)}')
report={'scope':'Documentary schema, references, rendered coverage, immutable source hashes and review hashes; not science replication or physical success',
 'utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'failures':failures,'passed':not failures,
 'lane_records':len(rows),'architecture_records':len(a['architectures']),'source_captures':len(sources),'local_links_checked':link_count,
 'current_source_drift':drift,'drift_policy':'Immutable captures are authoritative for CM01. Drift is disclosed, not silently refreshed or called a failure of the captured evidence.',
 'command':'python3 compatibility_matrix_2026_11_01/validate.py'}
(P/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k]for k in ('checks','passed','failures','lane_records','architecture_records','source_captures','local_links_checked')}))
print(json.dumps({'current_source_drift_count':len(drift),'paths':[r['source_path']for r in drift]}))
sys.exit(bool(failures))
