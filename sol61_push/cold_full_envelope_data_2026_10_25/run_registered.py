"""Run one authored contract in a NEW local output directory. No scheduler."""
import argparse,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1]
REGISTRY={'fit':('fit_contract_v2.json','fit_v2.py'),'core':('core_contract.json','core_floor.py'),'fraction':('core_fraction_contract.json','core_fraction.py'),'response':('response_contract_v2.json','response_v2.py'),'hst':('hst_contract_v2.json','hst_check.py'),'verify':('verification_contract.json','verify.py')}
p=argparse.ArgumentParser();p.add_argument('case',choices=REGISTRY);p.add_argument('new_tag');a=p.parse_args();assert a.new_tag and all(c.isalnum() or c in '_-' for c in a.new_tag);dest=P/a.new_tag;assert not dest.exists();contract,script=REGISTRY[a.case];d=json.loads((P/contract).read_text());runner='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py';cmd=['/opt/homebrew/bin/python3',runner,'--root',str(ROOT),'--contract',str(P/contract)]
for f in d['execution_artifacts']:cmd+=['--input',f]
cmd+=['--output',str(dest.relative_to(ROOT)),'--result',str((dest/'result.json').relative_to(ROOT)),'--timeout','600','--max-output-bytes','1048576','--max-cpu-seconds','550','--max-threads','1','--','/usr/bin/python3',str(P/script),'--out',str(dest)]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
