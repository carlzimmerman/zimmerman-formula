"""Execute one explicitly selected bounded case into a fresh directory."""
import argparse,json,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('case',choices=['screen','temporal','Draco','Sextans','analysis','audit']);ap.add_argument('tag');a=ap.parse_args();dest=P/a.tag;assert dest.parent==P and not dest.exists();contract=P/(a.case+'_contract.json');d=json.loads(contract.read_text());outputs=['result.json'];wall=240;cpu=220
if a.case in ['Draco','Sextans']:
 b=d['mathematics']['bounds'];script=P.parent/'cold_pre_stellar_settling_2026_10_25/continue_gated.py';extra=['--galaxy',a.case,'--ne','8192','--tol','1.25e-8','--T','8','--wall','1800','--resume',str(ROOT/b['parent'])];outputs+=['field.npz','stars.npz'];wall=2100;cpu=1950
else:
 script=P/({'screen':'refinement_screen.py','temporal':'temporal_probe.py','analysis':'analyze.py','audit':'verify_late.py'}[a.case]);extra=[]
 if a.case=='screen':outputs+=['transfers.npz']
 if a.case=='temporal':outputs+=['temporal_fields.npz'];wall=480;cpu=450
runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT))]
for f in outputs:cmd+=['--result',str((dest/f).relative_to(ROOT))]
cmd+=['--timeout',str(wall),'--max-output-bytes','1048576','--max-cpu-seconds',str(cpu),'--max-threads','1','--','/usr/bin/python3',str(script),'--out',str(dest)]+extra
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
