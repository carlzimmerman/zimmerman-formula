import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('stage',choices=['cs','interface','pressure01','pressure03','pressure05','pressure1','relaxation','relaxed_pressure']);p.add_argument('new_output_name');p.add_argument('--runner',required=True);a=p.parse_args()
base=Path(__file__).resolve().parent;root=base.parents[2]
if '/' in a.new_output_name or a.new_output_name in ('','.','..'):raise ValueError('new direct-child name required')
out=base/a.new_output_name
if out.exists():raise FileExistsError(out)
routes={'cs':('cs_contract.json','check_cs.py',[]),'interface':('interface_contract.json','check_interface.py',[]),
        'pressure01':('pressure_01_contract.json','scan_pressure.py',['.01']),
        'pressure03':('pressure_03_contract.json','scan_pressure.py',['.03']),
        'pressure05':('pressure_05_contract.json','scan_pressure.py',['.05']),
        'pressure1':('pressure_1_contract.json','scan_pressure.py',['.1']),
        'relaxation':('relaxation_contract.json','check_relaxation.py',[]),
        'relaxed_pressure':('relaxed_pressure_contract.json','scan_relaxed_pressure.py',[])}
cname,script,extras=routes[a.stage];c=json.loads((base/cname).read_text());rel=lambda v:str(v.relative_to(root))
cmd=[sys.executable,a.runner,'--root',str(root),'--contract',rel(base/cname)]
for v in c['execution_artifacts']:cmd+=['--input',v]
cmd+=['--output',rel(out),'--result',rel(out/'result.json'),'--timeout','180','--max-cpu-seconds','170','--max-threads','1','--max-output-bytes','1048576','--',sys.executable,rel(base/script),rel(out/'result.json')]+extras
raise SystemExit(subprocess.run(cmd,cwd=root).returncode)
