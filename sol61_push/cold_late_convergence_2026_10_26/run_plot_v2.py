"""Rerender the sealed numerical analysis with readable scientific labels."""
import json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1];dest=P/'figure_002';assert not dest.exists();contract=P/'plot2_contract.json';assert not contract.exists();d=json.loads((P/'plot_contract.json').read_text());d['claim_id']='CCT022_PLOT_LAYOUT_V2';d['mathematics']['assertion_tested']='Same sealed numerical data; label/caption/empty-legend presentation correction only';d['execution_artifacts']=sorted(set(d['execution_artifacts']+[str((P/f).relative_to(ROOT)) for f in ['plot_v2.py','run_plot_v2.py','VISUAL_QA.md']]));version=subprocess.check_output(['/usr/bin/python3','-c','import matplotlib; print(matplotlib.__version__)'],text=True).strip();d['software']=[x for x in d['software'] if x['name']!='matplotlib']+[dict(name='matplotlib',version=version)];contract.write_text(json.dumps(d,indent=2));runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in ['result.json','later_collapse.png']:cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout','240','--max-cpu-seconds','220','--max-threads','1','--max-output-bytes','1048576','--','/usr/bin/python3',str(P/'plot_v2.py'),'--out',str(dest)];raise SystemExit(subprocess.call(cmd,cwd=ROOT))
