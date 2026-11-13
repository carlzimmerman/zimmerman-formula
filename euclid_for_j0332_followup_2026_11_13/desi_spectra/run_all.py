from pathlib import Path
import json,subprocess,sys,concurrent.futures
P=Path(__file__).resolve().parent;ROOT=P.parents[1];runner=Path('/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py');validator=runner.with_name('validate_manifest.py');venv='/private/tmp/forj0332-fit-venv/bin/python'
def one(d):
 rel=lambda f:str(f.relative_to(ROOT));c=json.loads((d/'bounded_contract.json').read_text());cmd=['python3',str(runner),'--root',str(ROOT),'--contract',rel(d/'bounded_contract.json')]
 for f in c['execution_artifacts']:cmd+=['--input',f]
 cmd+=['--output',rel(d/'run_01'),'--result',rel(d/'run_01/result.json'),'--timeout','30','--max-output-bytes','100000','--max-threads','1','--',venv,rel(d/'search.py'),rel(d/'run_01')];subprocess.run(cmd,cwd=ROOT,check=True);subprocess.run(['python3',str(validator),str(d/'run_01/manifest.json'),'--root',str(ROOT)],check=True);r=json.loads((d/'run_01/result.json').read_text());return {'target':d.name,'candidates':r['candidates'],'strongest':r['strongest_diagnostic_peaks'][:1],'null_passing_realizations':r['null_passing_realizations']}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(one,sorted(P.glob('EUCL-*'))))
(P/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
