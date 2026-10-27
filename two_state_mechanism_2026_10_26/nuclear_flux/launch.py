"""Generate a new bounded contract before execution; refuse output reuse."""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('label');p.add_argument('--basis',default='aug-cc-pvdz');p.add_argument('--h',default='.1');p.add_argument('--end',default='30');p.add_argument('--retain',default='4,16,42');a=p.parse_args()
b=Path(__file__).resolve().parent;root=b.parents[1];rel=b.relative_to(root);run=rel/('run_'+a.label);assert not (root/run).exists()
inputs=[str(rel/x) for x in ['electronic.py','flux.py','run_grid.py','DESIGN.md']]
c=json.loads((root/'two_state_mechanism_2026_10_26/continuum/nuclear_contract.json').read_text());c['claim_id']='NEUTRAL_NUCLEAR_FLUX_'+a.label.upper();c['mathematics']['assertion_tested']='Finite-basis neutral radial scattering, flux and reciprocity; not electron recombination';c['mathematics']['inputs']=inputs;c['execution_artifacts']=inputs;c['mathematics']['bounds']=vars(a);c['mathematics']['non_claims']=['No electron capture kernel','No physical DR rate','No DR product branching','No galaxy population test','Ideal diagonal asymptotic lead approximation']
contract=rel/(a.label+'_contract.json');assert not(root/contract).exists();(root/contract).write_text(json.dumps(c,indent=2)+'\n')
args=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(root),'--contract',str(contract)]
for x in inputs:args+=['--input',x]
args+=['--output',str(run),'--result',str(run/'results.json'),'--result',str(run/'grid.npz'),'--timeout','1800','--max-threads','1','--','python3',str(rel/'run_grid.py'),'--output',str(run/'results.json'),'--basis',a.basis,'--h',a.h,'--end',a.end,'--retain',a.retain]
subprocess.run(args,cwd=root,check=True)
