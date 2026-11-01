"""Launch one authored experiment with its frozen contract into a new output folder."""
import argparse,json,subprocess,sys
from pathlib import Path

p=argparse.ArgumentParser();p.add_argument('stage',choices=['diagnostic','blocks','pressure','exact_gap','density']);p.add_argument('new_output_name');p.add_argument('--runner',required=True)
args=p.parse_args();root=Path(__file__).resolve().parents[3];base=Path(__file__).resolve().parent
if '/' in args.new_output_name or args.new_output_name in ('','.','..'):raise ValueError('Use a new direct child folder name')
out=base/args.new_output_name
if out.exists():raise FileExistsError(out)
routes={'diagnostic':('diagnostic_contract.json','spectrum.py',[]),
        'blocks':('block_contract.json','block_spectrum.py',[]),
        'pressure':('pressure_contract.json','pressure_scan.py',[]),
        'exact_gap':('gap_contract.json','exact_and_gap.py',['run_pressure/result.json']),
        'density':('density_contract.json','density_reach.py',['run_exact_gap/result.json'])}
contract,script,extra=routes[args.stage];c=json.loads((base/contract).read_text())
rel=lambda v:str(v.relative_to(root))
cmd=[sys.executable,args.runner,'--root',str(root),'--contract',rel(base/contract)]
for v in c['execution_artifacts']:cmd+=['--input',v]
cmd+=['--output',rel(out),'--result',rel(out/'result.json'),'--timeout','180','--max-cpu-seconds','170','--max-threads','1','--max-output-bytes','1048576','--',sys.executable,rel(base/script),rel(out/'result.json')]
cmd += [rel(base/e) for e in extra]
raise SystemExit(subprocess.run(cmd,cwd=root).returncode)
