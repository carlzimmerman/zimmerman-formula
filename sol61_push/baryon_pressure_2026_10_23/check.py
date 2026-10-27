import argparse,json
from pathlib import Path
import numpy as np
from gas import Radial
from thermal import Thermal
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();checks=[];details={}
def ck(n,e,t):checks.append(dict(name=n,value=float(e),tolerance=t,passed=bool(e<t)))
for gamma in [1.,5/3]:
 Radial.gamma=gamma;m=Radial(128,.05);x=m.x0.copy();f,U,W,d=m.gas_terms(x,1);pred=-m.mb[40]*f[40];scan=[]
 for step in [1e-6,1e-7,1e-8]:
  xp=x.copy();xm=x.copy();xp[40]+=step;xm[40]-=step;fd=(m.gas_terms(xp,1)[1]-m.gas_terms(xm,1)[1])/(2*step);scan.append(float(abs(fd-pred)/max(abs(pred),1e-30)))
 ck('gas_force_gamma_'+str(gamma),scan[-1],1e-5);eps=1e-5;A=10;terms=m.gas_terms(x,A);fd=(m.gas_terms(x,A*np.exp(eps))[1]-m.gas_terms(x,A*np.exp(-eps))[1])/(2*eps);ck('thermal_work_gamma_'+str(gamma),abs(fd-terms[2])/max(abs(terms[2]),1e-30),1e-6)
 ck('null_pressure_gamma_'+str(gamma),np.max(abs(m.gas_terms(m.r,1)[0])),1e-8);details[str(gamma)]=dict(force_step_scan=scan)
t=Thermal();t2=Thermal(nodes=8193);z=np.array([1100,500,200,100,30,10]);table=[]
for zz in z:
 A=1101/(1+zz);T,b=t.at(A);table.append(dict(z=int(zz),T=T,beta=b));
ck('thermal_interpolation',max(abs(t.at(1101/(1+zz))[0]/t2.at(1101/(1+zz))[0]-1) for zz in z),1e-7)
zero=Thermal(xe=0);ck('adiabatic_background',max(abs(zero.at(A)[0]/(2.725*1101/A**2)-1) for A in [1,3,10,100]),1e-7)
Path(a.output).write_text(json.dumps(dict(checks=checks,details=details,temperature_table=table),indent=2)+'\n')
