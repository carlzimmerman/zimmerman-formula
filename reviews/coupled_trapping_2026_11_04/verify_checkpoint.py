"""Read-only science provenance checks; writes only this phase's inventory.

Does not rerun experiments and does not certify their physical interpretation.
Historical input differences are accepted only if exact original bytes exist.
"""
import ast,collections,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
VALIDATOR=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
 files=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='VERIFICATION.json']
 by_hash=collections.defaultdict(list)
 for p in files:by_hash[sha(p)].append(str(p.relative_to(ROOT)))
 parsed_py=parsed_json=0
 for p in files:
  if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));parsed_py+=1
  if p.suffix=='.json':json.loads(p.read_text());parsed_json+=1
 records=[];differences=[];unrecovered=[];bad_outputs=[];statuses=collections.Counter()
 for p in sorted(HERE.rglob('manifest.json')):
  m=json.loads(p.read_text());statuses[m['run']['status']]+=1
  actual=[]
  for item in m.get('input_artifacts',[]):
   q=ROOT/item['path'];got=sha(q) if q.is_file() else None
   if got!=item['sha256']:
    archives=by_hash.get(item['sha256'],[])
    record=dict(manifest=str(p.relative_to(ROOT)),status=m['run']['status'],input=item['path'],original_sha256=item['sha256'],exact_original_archives=archives)
    differences.append(record);actual.append(record)
    if not archives:unrecovered.append(record)
  for item in m.get('outputs',[]):
   q=ROOT/item['path']
   if not q.is_file() or sha(q)!=item['sha256']:
    bad_outputs.append(dict(manifest=str(p.relative_to(ROOT)),output=item['path']))
  check=subprocess.run([sys.executable,str(VALIDATOR),str(p),'--root',str(ROOT)],capture_output=True,text=True)
  # Validator differences are expected for archived original source bytes;
  # any additional malformed record must remain an explicit verification failure.
  records.append(dict(path=str(p.relative_to(ROOT)),status=m['run']['status'],validator_exit=check.returncode,validator_output=(check.stdout+check.stderr).strip(),archived_input_differences=len(actual)))
 bad_validation=[r for r in records if r['validator_exit'] and not r['archived_input_differences']]
 prior=ROOT/'reviews/gravity_completion_2026_11_03'
 pins=json.loads((prior/'VERIFICATION.json').read_text())
 prior_differences=[x['path'] for x in pins['artifact_inventory'] if sha(prior/x['path'])!=x['sha256']]
 head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
 inventory=[dict(path=str(p.relative_to(HERE)),sha256=sha(p),bytes=p.stat().st_size) for p in sorted(files)]
 result=dict(checkpoint='CT09',verified_utc=datetime.now(timezone.utc).isoformat(),assessment_head=head,
  base_revision='285353a57bc1c21662c5565830bbc97ac5b0f7f9',python_sources_parsed=parsed_py,json_files_parsed=parsed_json,
  run_status_counts=dict(statuses),manifest_records=records,changed_input_records=differences,
  all_historical_originals_exactly_recovered=not unrecovered,unrecovered_originals=unrecovered,
  changed_output_records=bad_outputs,
  unexpected_validator_failures=bad_validation,prior_TP06_artifacts_rechecked=len(pins['artifact_inventory']),prior_TP06_differences=prior_differences,
  interpretation_guards=['Runner completed does not certify physics.','Two completed kinetic records with wrong phase-splitter pole are explicitly excluded in kinetics/RUN_INDEX.json.','Preferred late finite-width trajectory is an NWA-early/BW-late hybrid, not the timed-out full BW run.','Momentum trajectory convergence and physical statistical/delayed-parent collision action remain open.'],
  inventory=inventory,scope='Provenance/parse audit, not experiment rerun or physical proof. Scientific limitations are in README, HANDOFF and the independent reviews.')
 (HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ('checkpoint','assessment_head','python_sources_parsed','json_files_parsed','run_status_counts','all_historical_originals_exactly_recovered','unexpected_validator_failures','prior_TP06_artifacts_rechecked','prior_TP06_differences')},indent=2))
 assert not unrecovered and not bad_validation and not bad_outputs and not prior_differences

if __name__=='__main__':main()
