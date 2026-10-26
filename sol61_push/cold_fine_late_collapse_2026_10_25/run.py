"""Explicit finite continuation, new output directory only."""
import argparse,json,pathlib,subprocess
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];OLD=P.parent/'cold_pre_stellar_settling_2026_10_25';ap=argparse.ArgumentParser();ap.add_argument('galaxy',choices=['Draco','Sextans']);x=ap.parse_args();dest=P/(x.galaxy+'_fine_late');assert not dest.exists();contract=P/(x.galaxy+'_contract.json');d=json.loads(contract.read_text());b=d['mathematics']['bounds'];runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in ['result.json','field.npz','stars.npz']:cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout','2100','--max-output-bytes','1048576','--max-cpu-seconds','1950','--max-threads','1','--','/usr/bin/python3',str(OLD/'continue_gated.py'),'--galaxy',b['galaxy'],'--ne',str(b['ne']),'--tol',str(b['tol']),'--T',str(b['T']),'--wall',str(b['wall_seconds']),'--out',str(dest),'--resume',str(ROOT/b['parent'])]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
