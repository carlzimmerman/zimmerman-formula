import json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];dest=P/'figure_001';assert not dest.exists();contract=P/'plot_contract.json';d=json.loads(contract.read_text());runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in ['result.json','later_collapse.png']:cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout','240','--max-output-bytes','1048576','--max-cpu-seconds','220','--max-threads','1','--','/usr/bin/python3',str(P/'plot_late.py'),'--out',str(dest)];raise SystemExit(subprocess.call(cmd,cwd=ROOT))
