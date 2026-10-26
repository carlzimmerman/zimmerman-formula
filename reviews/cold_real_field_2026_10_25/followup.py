import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
source=Path(__file__).with_name('evolve_followup.cpp');binary=out/'evolve';subprocess.run(['clang++','-O3','-std=c++17',str(source),'-o',str(binary)],check=True)
cases=[('base',0,.5,3,60,.05,.005,False),('time',0,.5,3,60,.05,.0025,False),('space_time',0,.5,3,60,.025,.0025,False),('boundary',0,.5,3,80,.05,.005,False),('larger_seed',0,1.2,3,60,.05,.005,False),('restored',60,.8,3,60,.05,.005,False),('incoming_small',0,.1,3,60,.05,.005,True),('incoming_large',0,.2,3,60,.05,.005,True)]
rows=[]
for name,d,amp,width,R,dx,dt,incoming in cases:
 stem=out/name;cmd=[str(binary),str(stem),str(d),str(amp),str(width),str(R),str(dx),str(dt),'1000','0']
 if incoming:cmd+=['incoming']
 subprocess.run(cmd,check=True);r=json.load(open(str(stem)+'.json'));r.update(name=name,d=d,amplitude=amp,R=R,dx=dx,dt=dt,incoming=incoming);rows.append(r)
reference=rows[0]['late_core_mean'];agreement={r['name']:abs(r['late_core_mean']/reference-1) for r in rows[1:4]}
result=dict(scope='Finite-time nonlinear localization and prepared-pulse focusing; not abundance prediction',rows=rows,refinement_relative_changes=agreement,retention_converged_within_5_percent=all(x<.05 for x in agreement.values()))
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
