import sys,json,subprocess
from pathlib import Path
b=Path('two_state_mechanism_2026_10_26/nuclear_flux');label,basis,h,end=sys.argv[1:];ins=[str(b/x) for x in ['run_stream.py','lead.py','electronic.py','DESIGN.md']];c=json.loads((b/'ry2_h10_contract.json').read_text());c['claim_id']='STREAMED_COUPLED_NUCLEAR_'+label.upper();c['mathematics']['inputs']=ins;c['execution_artifacts']=ins;c['mathematics']['bounds']=dict(basis=basis,h=float(h),end=float(end),energy=[-.62,-.6,-.58]);c['mathematics']['assertion_tested']='Neutral radial propagation with coupled lead; stream memory without changing operator';p=b/(label+'_contract.json');assert not p.exists();p.write_text(json.dumps(c,indent=2)+'\n');r=b/('run_'+label)
a=['python3','/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py','--root','.','--contract',str(p)]
for x in ins:a+=['--input',x]
a+=['--output',str(r),'--result',str(r/'results.json'),'--timeout','1800','--max-threads','1','--','python3',str(b/'run_stream.py'),'--basis',basis,'--h',h,'--end',end,'--output',str(r/'results.json')];subprocess.run(a,check=True)
