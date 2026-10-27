import argparse,json
from pathlib import Path
import numpy as np
from model import Model,evolve
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);a=pa.parse_args();rows=[];checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v,flush=True)
def run(label,kwargs,dt=.001,end=30):
 try:
  m=Model(**kwargs);r=evolve(m,dt=dt,end=end);r['label']=label;r['settings']=kwargs;rows.append(r)
  ck(label,r['max_relative_energy_error']<.01 and r['static']['gradient_max']<2e-5,dict(balance=r['max_relative_energy_error'],absorbed_fraction=r['rows'][-1]['removed']/abs(r['initial_energy']),mass=r['mass'],inner2=r['rows'][-1]['masses'][3],maxradius=r['rows'][-1]['max_r']))
 except Exception as ex:ck(label,False,repr(ex));rows.append(dict(label=label,settings=kwargs,error=repr(ex)))
for mass in [.5,1,2,4]:
 for spin in [0,.02,.05]:run('baseline_%g_%g'%(mass,spin),dict(mass_ratio=mass,spin=spin))
run('half_step',dict(mass_ratio=1,spin=.02),dt=.0005)
run('fine_grid',dict(mass_ratio=1,spin=.02,n=512,ns=256),dt=.0005)
run('larger_box',dict(mass_ratio=1,spin=.02,n=384,L=24,sponge_start=16))
for lam in [10,100]:
 for gap in [.5,.2]:run('phase_%g_%g'%(lam,gap),dict(mass_ratio=1,spin=.02,lam=lam,gap=gap),end=60)
# Static initialization noise with frozen material: field-only dynamics.
m=Model(spin=.02);r=m.r0.copy();v=np.zeros(m.ns);w,z,stat=m.static(r);wp=np.zeros_like(w);zp=np.zeros_like(z);E0=m.energy(r,v,w,wp,z,zp);loss=0.;dt=.001
_,aw,az=m.accel(r,w,z)
for step in range(30000):
 wp,zp,d=m.damp(wp,zp,dt/2);loss+=d;wp+=dt/2*aw;zp+=dt/2*az;w+=dt*wp;z+=dt*zp;_,aw,az=m.accel(r,w,z);wp+=dt/2*aw;zp+=dt/2*az;wp,zp,d=m.damp(wp,zp,dt/2);loss+=d
Ef=m.energy(r,v,w,wp,z,zp);control=dict(initial=E0,final=Ef,absorbed=loss,balance=Ef+loss-E0)
ck('frozen_source_control',abs(Ef+loss-E0)/abs(E0)<1e-6,control)
ck('coverage',len(rows)==19,len(rows))
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(dict(checks=checks,rows=rows,frozen_control=control),indent=2)+'\n');raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
