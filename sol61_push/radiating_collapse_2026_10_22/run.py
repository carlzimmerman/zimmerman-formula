import argparse,json,time
from pathlib import Path
import numpy as np
from model import Model,evolve
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--n',type=int,default=256);p.add_argument('--ns',type=int,default=128);p.add_argument('--dt',type=float,default=.001);p.add_argument('--end',type=float,default=30);p.add_argument('--mass',type=float,default=1);p.add_argument('--spin',type=float,default=.02);p.add_argument('--lam',type=float,default=1);p.add_argument('--gap',type=float,default=.5);a=p.parse_args();m=Model(n=a.n,ns=a.ns,mass_ratio=a.mass,spin=a.spin,lam=a.lam,gap=a.gap);checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
r=m.r0;w,z,st=m.static(r);E,grad=m.potential(r,w,z,True)
for i,name in enumerate(['shell','polarization','phase']):
 Y=[r.copy(),w.copy(),z.copy()];direction=np.cos(np.arange(len(Y[i]))*.73);hh=1e-6;Y[i]+=hh*direction;ep=m.potential(*Y);Y[i]-=2*hh*direction;em=m.potential(*Y);fd=(ep-em)/(2*hh);exact=np.dot(grad[i],direction)
 ck('energy_force_'+name,abs(fd-exact)<2e-7*max(1,abs(exact)),dict(fd=fd,exact=exact))
ck('deposition_mass',abs(np.dot(m.dep(r)[0],m.vol)/sum(m.mi)-1)<1e-12,sum(m.mi))
result=evolve(m,dt=a.dt,end=a.end);result['parameters']=vars(a);result['checks']=checks
ck('static_field_residual',result['static']['gradient_max']<2e-5,result['static'])
ck('energy_balance',result['max_relative_energy_error']<.01,result['max_relative_energy_error'])
ck('positive_fields',all(x['min_z']>0 and x['max_w']<1 for x in result['rows']),'field domain')
ck('absorber_nonnegative',all(x['removed']>=0 for x in result['rows']),result['rows'][-1]['removed'])
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print('final',result['rows'][-1],flush=True);raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
