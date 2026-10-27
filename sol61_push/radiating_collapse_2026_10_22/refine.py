import argparse,json
from pathlib import Path
from model_flux import Model,evolve
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();rows=[];checks=[]
for label,kw,dt,end in [('ultrafine',dict(n=1024,ns=512,spin=.02),.00025,30),('mass4_fine',dict(n=512,ns=256,spin=.02,mass_ratio=4),.0005,30),('mass4_strong_fine',dict(n=512,ns=256,spin=.02,mass_ratio=4,lam=100,gap=.2),.0005,120)]:
 try:
  r=evolve(Model(**kw),dt=dt,end=end);r.update(label=label,settings=kw);rows.append(r);ok=r['max_relative_energy_error']<.01;v=dict(balance=r['max_relative_energy_error'],last=r['rows'][-1]);print(label,ok,v,flush=True)
 except Exception as ex:ok=False;v=repr(ex);rows.append(dict(label=label,error=v,settings=kw))
 checks.append(dict(name=label,passed=bool(ok),value=str(v)))
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(rows=rows,checks=checks),indent=2)+'\n');raise SystemExit(0 if all(r['passed'] for r in checks) else 1)
