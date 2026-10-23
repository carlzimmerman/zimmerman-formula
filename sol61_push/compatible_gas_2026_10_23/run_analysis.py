from pathlib import Path
import json,subprocess
b=Path('sol61_push/compatible_gas_2026_10_23');names=['crossing_base','crossing_time','crossing_fine','ultra','no_molecules','fewer_molecules','late','small','smooth'];files=[str(b/x) for x in ['radial_base.py','gas_v4.py','analyze.py','CONTRACT.md']]+[str(b/n/'result.json') for n in names if (b/n/'result.json').exists()]
c=json.loads((b/'crossing_fine_contract.json').read_text());c['claim_id']='CG_ANALYSIS';c['execution_artifacts']=files;c['mathematics']['inputs']=names;c['mathematics']['assertion_tested']='Endpoint comparisons and profile/resolution diagnostics, not a binding certificate';c['software'].append({'name':'Matplotlib','version':'3.9.4'});c['mathematics']['bounds']={'timeout_seconds':60};(b/'analysis_contract.json').write_text(json.dumps(c,indent=2))
cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(Path.cwd()),'--contract',str(b/'analysis_contract.json'),'--output',str(b/'analysis'),'--result',str(b/'analysis'/'result.json'),'--result',str(b/'profiles.png'),'--timeout','60','--max-threads','1']
for f in files:cmd+=['--input',f]
cmd+=['--','python3',str(b/'analyze.py'),str(b/'analysis'/'result.json')];subprocess.run(cmd,check=True)
