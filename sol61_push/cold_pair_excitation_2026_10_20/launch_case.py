"""Execute a predeclared local case through the bounded provenance runner."""
from pathlib import Path
import sys,json,subprocess
p=Path(__file__).resolve().parent;root=p.parents[1]
name=sys.argv[1];case=p/(name+'_case.json');contract=p/(name+'_contract.json');out=p/(name+'_run_001')
c=json.loads(contract.read_text());s=json.loads(case.read_text())
run='/Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py'
argv=['python3',run,'--root',str(root),'--contract',str(contract.relative_to(root)),
      '--output',str(out.relative_to(root)),'--timeout','180','--max-cpu-seconds','120',
      '--max-threads','1','--max-output-bytes','1048576']
for x in c['execution_artifacts']:argv+=['--input',x]
results=[out/'results.json']
if s['kind']=='preflight':
    for x in ['gaussian_1.0','gaussian_0.5']:results+=[out/x/'solver_stdout.txt']
    evolutions=s['evolutions']
else:evolutions={'evolution':s['evolution']}
for tag,v in evolutions.items():
    d=out/tag;results += [d/'log.jsonl',d/'solver_stdout.txt',d/'enclosed_energy.jsonl']
    times=list(range(0,int(v['T'])+1,int(v['snapshot_interval'])))
    if times[-1]!=v['T']:times.append(v['T'])
    results += [d/f'snap_t{round(t*1000):09d}.bin' for t in times]
for x in results:argv+=['--result',str(x.relative_to(root))]
argv+=['--','python3',str((p/'pair_driver_v2.py').relative_to(root)),str(case.relative_to(root)),str(out.relative_to(root))]
r=subprocess.run(argv,cwd=root);raise SystemExit(r.returncode)
