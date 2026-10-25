"""One explicit bounded cold-first run. No schedules or overwrite."""
import argparse,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];ap=argparse.ArgumentParser();ap.add_argument('case');ap.add_argument('--tag');x=ap.parse_args();assert all(c.isalnum() or c in '_-' for c in (x.tag or x.case));dest=P/(x.tag or x.case);assert not dest.exists();d=json.loads((P/(x.case+'_contract.json')).read_text());b=d['mathematics']['bounds'];runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(P/(x.case+'_contract.json'))]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in ['result.json','field.npz','stars.npz']:cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout','600','--max-output-bytes','1048576','--max-cpu-seconds','550','--max-threads','1','--','/usr/bin/python3',str(P/'evolve_energetic.py'),'--galaxy',b['galaxy'],'--ne',str(b['ne']),'--tol',str(b['tol']),'--T',str(b['T']),'--out',str(dest)]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
