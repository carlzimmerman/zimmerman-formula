"""Read-only science-record verification plus one regenerated inventory.

A historical source may differ from its original path only if exact original
bytes remain in an archived file. Successful-run inputs are never silently
reinterpreted using the active implementation.
"""
import ast,collections,datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 files=sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='VERIFICATION.json');hashes={p:sha(p) for p in files};byhash=collections.defaultdict(list)
 for p,h in hashes.items():byhash[h].append(str(p.relative_to(ROOT)))
 syntax=[]
 for p in files:
  try:
   if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
   elif p.suffix=='.json':json.loads(p.read_text())
  except Exception as e:syntax.append(dict(path=str(p.relative_to(ROOT)),error=str(e)))
 manifests=[];differences=[];lost=[];badoutputs=[];states=collections.Counter()
 for p in files:
  if p.name!='manifest.json':continue
  r=json.loads(p.read_text());status=r['run']['status'];states[status]+=1
  v=subprocess.run(['python3',str(VALIDATOR),str(p),'--root',str(ROOT)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  manifests.append(dict(path=str(p.relative_to(ROOT)),status=status,validator_exit=v.returncode,validator_output=v.stdout.strip()))
  for a in r.get('input_artifacts',[])+r.get('execution_artifacts',[]):
   if not isinstance(a,dict) or 'sha256' not in a:continue
   q=Path(a['path']);q=q if q.is_absolute() else ROOT/q
   current=sha(q) if q.is_file() else None
   if current!=a['sha256']:
    row=dict(manifest=str(p.relative_to(ROOT)),original_path=a['path'],expected=a['sha256'],current=current,exact_archives=byhash[a['sha256']]);differences.append(row)
    if not row['exact_archives']:lost.append(row)
  for a in r.get('outputs',[]):
   if not isinstance(a,dict) or 'sha256' not in a:continue
   q=Path(a['path']);q=q if q.is_absolute() else ROOT/q
   if not q.is_file() or sha(q)!=a['sha256']:badoutputs.append(dict(manifest=str(p.relative_to(ROOT)),path=a['path']))
 historical_failures=[];unexpected=[]
 diff_manifests={r['manifest'] for r in differences}
 for item in manifests:
  if not item['validator_exit']:continue
  messages=item['validator_output'].removeprefix('invalid manifest: ').split('; ')
  archived=item['path'] in diff_manifests and all(x.startswith('input changed since the run: ') for x in messages) and not any(x['manifest']==item['path'] for x in lost)
  (historical_failures if archived else unexpected).append(item)
 prior=[]
 for dirname,key in [('coupled_trapping_2026_11_04','inventory'),('gravity_completion_2026_11_03','artifact_inventory')]:
  parent=ROOT/'reviews'/dirname;certificate=parent/'VERIFICATION.json';published=subprocess.check_output(['git','show','370cb35bc08d13f2a8c0dfa9adee161e1665ead2:'+str(certificate.relative_to(ROOT))],cwd=ROOT);certificate_unchanged=hashlib.sha256(published).hexdigest()==sha(certificate);v=json.loads(certificate.read_text());diff=[]
  for item in v[key]:
   q=parent/item['path']
   if not q.is_file() or sha(q)!=item['sha256']:diff.append(item['path'])
  prior.append(dict(root=str(parent.relative_to(ROOT)),pins_checked=len(v[key]),inventory_certificate_matches_published_commit=certificate_unchanged,differences=diff))
 report=dict(checkpoint='CC10',assessment_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Record integrity and syntax, not independent physical validation.',base_revision='fd417eea045a0b6259b8efff5e20ca62a2e14f7e',published_physics_ancestry='370cb35bc08d13f2a8c0dfa9adee161e1665ead2',python_sources_parsed=sum(p.suffix=='.py' for p in files),json_files_parsed=sum(p.suffix=='.json' for p in files),syntax_errors=syntax,run_status_counts=dict(states),manifest_records=manifests,historical_source_differences=differences,archived_historical_validator_differences=historical_failures,unexpected_validator_failures=unexpected,unrecovered_originals=lost,changed_outputs=badoutputs,prior_checkpoints=prior,validator_sha256=sha(VALIDATOR),inventory=[dict(path=str(p.relative_to(BASE)),sha256=hashes[p],bytes=p.stat().st_size) for p in files])
 (BASE/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('python_sources_parsed','json_files_parsed','run_status_counts','syntax_errors','unrecovered_originals','changed_outputs','prior_checkpoints')},indent=2));print('validator_failures',sum(r['validator_exit']!=0 for r in manifests));assert not syntax and not lost and not badoutputs and not unexpected and not any(r['differences'] or not r['inventory_certificate_matches_published_commit'] for r in prior)
if __name__=='__main__':main()
