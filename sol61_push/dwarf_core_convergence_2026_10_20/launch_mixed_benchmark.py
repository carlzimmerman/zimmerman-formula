"""Frozen bounded record for a candidate, not production admission."""
import json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;REL=HERE.relative_to(ROOT)
SKILL=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit')
files=['benchmark_mixed_gravity.py','launch_mixed_benchmark.py','mixed_gravity.py','mixed_gravity.mm','mixed_gravity.dylib','test_mixed_gravity.py','metal_gravity.py','metal_gravity.mm','metal_gravity.dylib','fast_gravity.py','fast_gravity.c','fast_gravity.dylib','run_q08_iso_c/final.npz']
inputs=[str(REL/f) for f in files];out=REL/'mixed_validation_run_001'
contract=dict(claim_id='COMPENSATED_MIXED_CANDIDATE',mathematics=dict(assertion_tested='Candidate full3D compensated mixed direct Plummer force; empirical forceL2<5e-7,max<2e-6,phi/U<5e-7; normalized force/torque<1e-8 in declared samples',coefficient_domain='FP32pair arithmetic, raw3f/DSdisplacements andDSsums; native CPU/DS references',conventions='pc,Msun,Myr; all ordered off-diagonal pairs; unchanged Plummer law',inputs=['seed19876','actualq08endpoint'],bounds=dict(N=[1024,8192,32768,65536,262144],wall_seconds=100),non_claims=['Not original1e-11DSadmission','No physicalprofile/core/trajectory convergence result']),execution_artifacts=inputs,software=[dict(name='simulationPython',version='3.9.6')],randomness=dict(used=True,generator='PCG64',seed=19876))
p=HERE/'contracts/mixed_validation_001.json';p.write_text(json.dumps(contract,indent=2)+'\n')
cmd=['/opt/homebrew/bin/python3.12',str(SKILL/'scripts/run_experiment.py'),'--root',str(ROOT),'--contract',str(p),'--output',str(out),'--timeout','100','--max-cpu-seconds','400','--max-threads','4']
for f in inputs:cmd+=['--input',f]
cmd+=['--result',str(out/'benchmark.json'),'--','nice','-n','19','/usr/bin/python3',str(REL/'benchmark_mixed_gravity.py'),'--output',str(out/'benchmark.json')]
raise SystemExit(subprocess.call(cmd))
