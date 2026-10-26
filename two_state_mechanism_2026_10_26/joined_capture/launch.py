import sys,json,subprocess
from pathlib import Path
b=Path('two_state_mechanism_2026_10_26/joined_capture');label,script,*args=sys.argv[1:];c=json.loads((b.parent/'nuclear_flux/ry2_h10_contract.json').read_text());ins=[str(b/x) for x in ['DESIGN.md','qmap.py','run_map.py','fourth.py','run_fourth.py','launch.py']]+[str(b.parent/'nuclear_flux'/x) for x in ['electronic.py','lead.py']]+[str(x) for x in sorted((b/'inputs').iterdir())]+[str(b.parent/'nuclear_flux'/d/'kernel.npz') for d in ['run_kernel','run_kernel_R3','run_kernel_R4']]
c['claim_id']='JOINED_CAPTURE_'+label.upper();c['execution_artifacts']=ins;c['mathematics'].update(assertion_tested='Signed Q embedding and optical identity, or fourth-order neutral nuclear convergence diagnostic',inputs=ins,bounds=dict(script=script,args=args),non_claims=['No full electron+nuclear rate','No photon trajectory','No galaxy separation test','Fixed-axis and approximate stationary exterior'])
p=b/(label+'_contract.json');assert not p.exists();p.write_text(json.dumps(c,indent=2)+'\n');r=b/('run_'+label)
a=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root','.','--contract',str(p)]
for x in ins:a+=['--input',x]
a+=['--output',str(r),'--result',str(r/'results.json'),'--timeout','1800','--max-threads','1','--','python3',str(b/script),'--output',str(r/'results.json'),*args];subprocess.run(a,check=True)
