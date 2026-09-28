"""Read-only structural/source-freshness audit. No scientific certification."""
from pathlib import Path
import json,hashlib,re,collections,sys
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def validate():
 errors=[]
 m=json.loads((BASE/'manifest.json').read_text());tasks=m['tasks']
 ss=json.loads((BASE/'sources.json').read_text())['sources'];sources={s['source_id']:s for s in ss}
 def check(ok,msg):
  if not ok:errors.append(msg)
 check(len(tasks)==2500,'Expected 2500 records')
 check(len(ss)==100 and len(sources)==100,'Expected 100 unique sources')
 required='id year source_id title principle math measurement_input deliverable steps controls first_principles closure_bridge new_information overlap_handling continuation depends_on priority kind path task_sha256 source_record_sha256 scientific_fingerprint'.split()
 srequired='source_id year title authors_or_collaboration primary_url identifier report_date date_precision date_basis version observation_epoch measurement data_access verification source_locator overlap_family search_queries checked_on'.split()
 ids={t['id'] for t in tasks}; old=json.loads((BASE.parent/'manifest.json').read_text())
 oldids={t['id'] for t in old['tasks']}
 for key in ['id','title','scientific_fingerprint','task_sha256']:
  vals=[t[key] for t in tasks];check(len(set(vals))==2500,f'Duplicate {key}')
 for year in range(2017,2027):
  yy=[t for t in tasks if t['year']==year]
  check(len(yy)==250,f'{year}: task count')
  check({t['id'] for t in yy}=={f'MY{year}-{i:03d}' for i in range(1,251)},f'{year}: ID sequence')
  check(len([s for s in ss if s['year']==year])>=10,f'{year}: too few source anchors')
 listed=set();words=[]
 for s in ss:
  for k in srequired:check(bool(s.get(k)),f"{s['source_id']}: missing {k}")
  check(str(s['report_date']).startswith(str(s['year'])),f"{s['source_id']}: year/date mismatch")
  check(s['report_date']<='2026-09-27',f"{s['source_id']}: beyond cutoff")
  check(s['date_precision'] in ['day','month','year'],f"{s['source_id']}: date precision")
  check(s['primary_url'].startswith('https://'),f"{s['source_id']}: primary URL")
  check(canonical({k:v for k,v in s.items() if k!='record_sha256'})==s['record_sha256'],f"{s['source_id']}: source record hash")
 for t in tasks:
  ident=t['id']
  for k in required:check(k in t,f'{ident}: missing {k}')
  for k in ['title','principle','math','measurement_input','deliverable','first_principles','closure_bridge','new_information','overlap_handling']:check(bool(t[k].strip()),f'{ident}: empty {k}')
  check(4<=len(t['steps'])<=6,f'{ident}: step count')
  check(len(t['controls'])>=2 and 'negative' in t['controls'][0].lower(),f'{ident}: negative control')
  check(len(t['continuation'])==3,f'{ident}: continuation count')
  check(t['priority'] in ['P0','P1','P2'],f'{ident}: priority')
  check(t['kind'] in ['derivation','inference','computation','audit'],f'{ident}: kind')
  check(t['source_id'] in sources,f'{ident}: unknown source')
  check(sources[t['source_id']]['year']==t['year'],f'{ident}: wrong source year')
  check(t['source_record_sha256']==sources[t['source_id']]['record_sha256'],f'{ident}: source hash mismatch')
  for dep in t['depends_on']:check(dep in ids|oldids,f'{ident}: unknown dependency {dep}')
  p=BASE/t['path'];listed.add(p.resolve());check(p.is_file(),f'{ident}: missing file')
  if not p.is_file():continue
  check(sha(p)==t['task_sha256'],f'{ident}: stale task hash')
  txt=p.read_text();words.append(len(txt.split()))
  for needle in ['a0=(c/2)*sqrt(G_N*rho_Lambda)','9.3619e-11','1.1279e-10','criterion **B**','filtered MONO','First-principles obligation','Finding-driven continuation','Pinned local base']:
   check(needle in txt,f'{ident}: missing {needle}')
  for target in re.findall(r'\]\(([^)]+)\)',txt):
   if target.startswith(('https://','http://','#')):continue
   check((p.parent/target.split('#')[0]).exists(),f'{ident}: broken local link {target}')
 actual={p.resolve() for p in BASE.glob('20??/MY*.md')}
 check(actual==listed,'Task file set differs from manifest')
 pinned=json.loads((BASE/'FRAMEWORK_SOURCES.json').read_text())['sources']
 for p,h in pinned.items():check((ROOT/p).is_file() and sha(ROOT/p)==h,f'Stale local base: {p}')
 # Dependencies within this namespace must be acyclic.
 graph={t['id']:[x for x in t['depends_on'] if x in ids] for t in tasks};vis=set();active=set()
 def visit(n):
  if n in active:errors.append('Dependency cycle at '+n);return
  if n in vis:return
  active.add(n)
  for d in graph[n]:visit(d)
  active.remove(n);vis.add(n)
 for n in graph:visit(n)
 result={'passed':not errors,'task_records':len(tasks),'task_files':len(actual),'source_anchors':len(ss),'years':{str(y):sum(t['year']==y for t in tasks) for y in range(2017,2027)},'local_sources_checked':len(pinned),'word_counts':{'min':min(words),'median':sorted(words)[len(words)//2],'max':max(words)},'errors':errors,'limits':'Structural and freshness validation only. Does not certify semantic novelty, source conclusions, future scientific results or closure.'}
 return result
if __name__=='__main__':
 r=validate();print(json.dumps(r,indent=2));sys.exit(0 if r['passed'] else 1)
