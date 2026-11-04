"""Authorized bounded continuation; write a fresh contract before execution."""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[3]
OWN=Path('reviews/weak_completion_2026_11_04/energy')
def main(branch,number,prior):
 h={'coarse':'.0001','fine':'.00005'}[branch];name='run_fresh_'+branch+str(number).zfill(3);base=json.loads((ROOT/OWN/('contract_fresh_'+branch+'_v3.json')).read_text());base['execution_artifacts']=list(dict.fromkeys(base['execution_artifacts']+[prior,str(Path(prior).parent/'manifest.json')]));base['mathematics']['inputs'].append('Exact matched-energy prefix '+prior+'; old energy/work is retained, not reset.');contract=OWN/('contract_'+name+'.json');(ROOT/contract).write_text(json.dumps(base,indent=2)+'\n');cmd=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root',str(ROOT),'--contract',str(contract)]
 for f in base['execution_artifacts']:cmd+=['--input',f]
 cmd+=['--output',str(OWN/name),'--result',str(OWN/name/'result.json'),'--timeout','240','--max-cpu-seconds','235','--max-threads','1','--max-output-bytes','1048576','--','python3',str(OWN/'fresh_history_v4.py'),str(OWN/name/'result.json'),prior,'0.0021690179772784167',h,'8'];raise SystemExit(subprocess.run(cmd,cwd=ROOT).returncode)
if __name__=='__main__':main(*sys.argv[1:])
