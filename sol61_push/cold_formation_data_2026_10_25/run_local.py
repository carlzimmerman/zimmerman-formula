"""Run one explicit analysis/audit contract, never overwrite prior evidence."""
import argparse,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];ap=argparse.ArgumentParser();ap.add_argument('case',choices=['analysis','audit']);ap.add_argument('tag');x=ap.parse_args();assert x.tag and all(c.isalnum() or c in '_-' for c in x.tag);dest=P/x.tag;assert not dest.exists();d=json.loads((P/(x.case+'_contract.json')).read_text());runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(P/(x.case+'_contract.json'))]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT)),'--result',str((dest/'result.json').relative_to(ROOT)),'--timeout','240','--max-output-bytes','1048576','--max-cpu-seconds','220','--max-threads','1','--','/usr/bin/python3',str(P/('analyze.py' if x.case=='analysis' else 'verify.py')),'--out',str(dest)]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
