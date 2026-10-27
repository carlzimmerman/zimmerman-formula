import argparse,json
from pathlib import Path
from model_flux import Model,evolve
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();rows=[];checks=[]
def run(label,settings,end=30,dt=.001):
 try:
  r=evolve(Model(**settings),dt=dt,end=end);r['label']=label;r['settings']=settings;rows.append(r);good=r['max_relative_energy_error']<.01
  msg=dict(balance=r['max_relative_energy_error'],absorbed=r['rows'][-1]['removed'],flux6=r['rows'][-1]['flux6'],m2=r['rows'][-1]['masses'][3],maxr=r['rows'][-1]['max_r'])
 except Exception as e:good=False;msg=repr(e);rows.append(dict(label=label,error=repr(e),settings=settings))
 checks.append(dict(name=label,passed=bool(good),value=str(msg)));print(label,good,msg,flush=True)
run('flux_standard',dict(spin=.02))
run('flux_large_box',dict(spin=.02,L=24,n=384,sponge_start=16))
run('flux_fine',dict(spin=.02,n=512,ns=256),dt=.0005)
for m in [.5,1,2,4]:run('long_%g'%m,dict(spin=.02,mass_ratio=m,lam=100,gap=.2),end=120)
run('strong_fine',dict(spin=.02,mass_ratio=1,lam=100,gap=.2,n=512,ns=256),end=60,dt=.0005)
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(rows=rows,checks=checks),indent=2)+'\n');raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
