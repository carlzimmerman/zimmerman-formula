"""Read-only evidence validation and documentary source inventory for vectors leaf."""
import sys,json,hashlib,math
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
sys.path.insert(0,'/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts')
from validate_manifest import validate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[];corrections=[];input_union={};bad=[]
for p in sorted(HERE.glob('run_*/manifest.json')):
 obj=json.loads(p.read_text());errors=validate(obj,root=ROOT,manifest_path=p);run=p.parent.name;entry=dict(run=run,manifest=str(p.relative_to(ROOT)),manifest_sha256=sha(p),status=obj['run']['status'],validation_errors=errors,command=obj['command'],software_record=obj['environment']['software']);metric=p.parent/'metrics.json';result=p.parent/'result.json'
 if metric.exists():entry['observed_resources']=json.loads(metric.read_text())
 if result.exists():
  data=json.loads(result.read_text());entry['result_sha256']=sha(result);entry['checks']=data.get('checks');entry['partial']=data.get('partial',False)
  def finite(v):
   if isinstance(v,float):return math.isfinite(v)
   if isinstance(v,dict):return all(finite(a) for a in v.values())
   if isinstance(v,list):return all(finite(a) for a in v)
   return True
  entry['result_all_numbers_finite']=finite(data)
 if errors:bad.append(dict(run=run,errors=errors))
 soft={a['name']:a['version'] for a in obj['environment']['software']}
 if soft.get('runner-python')=='3.13.9' and soft.get('Python')=='3.9.6':corrections.append(run)
 for a in obj['repository']['input_artifacts']:
  input_union[a['path']]=a['sha256']
 records.append(entry)
critical=['transport_v3.py','rates_v2.py','gauge_basis_v1.py','run_table003/result.json','coulomb/elastic_builder_v3.py','coulomb/scalar_factory_v3.py','coulomb/template_v2.py','coulomb/cold_split.py','coulomb/cold_split_v2.py','coulomb/photino_opacity.py','DERIVATION.md','STATUS.md','SOURCES.md','ENVIRONMENT_ERRATUM.md']
provenance=dict(claim_id='CC11_VECTOR_TRANSPORT_COLD_COULOMB_SCOPED_HANDOFF',frozen_at_UTC=datetime.now(timezone.utc).isoformat(),owned_scope=str(HERE.relative_to(ROOT)),all_manifests_valid=not bad,manifest_count=len(records),unexpected_validation_errors=bad,records=records,critical_artifacts=[dict(path=str((HERE/p).relative_to(ROOT)),sha256=sha(HERE/p)) for p in critical],unique_input_paths=len(input_union),per_job_environment_correction=dict(affected_runs=corrections,actual_interpreter='Miniconda Python3.13.9',actual_numpy='1.26.4',actual_scipy='1.14.1',explanation='Old launch.py copied historical contract strings; see ENVIRONMENT_ERRATUM.md. No root3.9 jobs are changed. launch_v2/v3 detect actual per-job versions.'),preferred=dict(vector_factory='transport_v3.py',vector_coefficients='rates_v2.py',vector_table='run_table003/result.json',portable_selfelastic=['coulomb/elastic_builder_v3.py','coulomb/scalar_factory_v3.py','coulomb/template_v2.py'],cold_comparison=['run_cold_split001/result.json','run_cold_split002/result.json'],opacity='run_opacity001/result.json',portability=['run_portable313001/result.json','run_portable39001/result.json']),non_claims=['No newglobalcandidateviability','No oldlate/newwarmendpointsplice','Conditionaloldlatevacuum4Psourceandtreecascade, notnewloop/occupiedmediumcompletion','ColdSc0selfelastic is partialspeciescoverage; actualunknownoldlightbath is not invented','Rawfinitewidth/modelenergyresidualisdistinctfromaccountedledgerclosure'])
(HERE/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps(dict(manifests=len(records),valid=not bad,errors=bad,software_erratum_runs=len(corrections))))
assert not bad,bad
