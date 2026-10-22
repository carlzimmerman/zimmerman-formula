"""Administrative validation only; no mathematical computation."""
from pathlib import Path
import hashlib,json,datetime
root=Path(__file__).resolve().parents[6]
run=Path(__file__).resolve().parent
result=json.loads((run/'result.json').read_text())
contract=json.loads((root/'deepseek_push/astra_spawn_ideas/fresh_gravity_followups/RESULT_CONTRACT.json').read_text())
assert set(contract['required_fields']) <= set(result)
checks=[]
for kind in ['input_sha256','artifacts_sha256']:
 for p,h in result[kind].items():
  actual=hashlib.sha256((root/p).read_bytes()).hexdigest()
  assert actual==h,(kind,p,h,actual)
  checks.append({'kind':kind,'path':p,'matched':True})
assert result['task_id']=='FGF-050'
assert result['mathematical_executable_computations']==0
assert result['acceptance_state']=='unreviewed'
assert result['actual_family_budgets']=='not established'
report={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'administrative_only':True,'required_fields_present':True,'hash_checks':checks,'status':'pass'}
(run/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'pass','input_hashes':len(result['input_sha256']),'artifact_hashes':len(result['artifacts_sha256']),'mathematical_executable_computations':0}))
