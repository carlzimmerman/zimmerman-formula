"""Explicit one-shot local runs, no automation."""
import json,pathlib,subprocess,argparse
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
a=argparse.ArgumentParser();a.add_argument('case');a.add_argument('--tag');x=a.parse_args();assert x.tag is None or all(c.isalnum() or c in '_-' for c in x.tag);d=json.loads((P/(x.case+'_contract.json')).read_text());dest=P/(x.tag or x.case);assert not dest.exists();b=d['mathematics']['bounds'];runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(P/(x.case+'_contract.json'))]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT)),'--result',str((dest/'result.json').relative_to(ROOT)),'--result',str((dest/'field.npz').relative_to(ROOT)),'--result',str((dest/'stars.npz').relative_to(ROOT)),'--timeout','290','--max-output-bytes','1048576','--max-cpu-seconds','260','--max-threads','1','--','/usr/bin/python3',str(P/('formation_v4.py' if x.case.endswith('_v4') else ('formation_v3.py' if x.case.endswith('_v3') else ('formation_v2.py' if x.case.endswith('_v2') else 'formation.py')))),'--galaxy',b['galaxy'],'--ne',str(b['ne']),'--dt',str(b['dt']),'--T',str(b['T']),'--out',str(dest)]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
