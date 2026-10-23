import json,subprocess
from pathlib import Path
b=Path('sol61_push/kinetic_support_2026_10_23');names=['dynamic32','dynamic48','dynamic64','particles48','timestep32','dilation32','dilation48','box72','long_equilibrium','long_dilation','family','refinement','spectrum_v2','growth_v2','virial'];files=[str(b/'analyze.py')]+[str(b/n/'result.json') for n in names];c=json.loads((b/'family_contract.json').read_text());c['claim_id']='KS_ANALYSIS';c['execution_artifacts']=files;c['mathematics']['assertion_tested']='Finite profile, lifetime and convergence comparisons';c['software'].append({'name':'Matplotlib','version':'3.9.4'});p=b/'analysis_contract.json';assert not p.exists();p.write_text(json.dumps(c,indent=2));o=b/'analysis'
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(p),'--output',str(o),'--result',str(o/'result.json'),'--result',str(o/'summary.png'),'--timeout','60','--max-threads','1']
for f in files:cmd+=['--input',f]
subprocess.run(cmd+['--','python3',str(b/'analyze.py'),str(o/'result.json')],check=True)
