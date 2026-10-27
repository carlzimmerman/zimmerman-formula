"""Supplement, not replacement, for the preserved failed check record."""
import argparse,json
from pathlib import Path
import numpy as np
from radial_v2 import Radial
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args()
m=Radial(128,.03);P,c,_=m.static(m.x0);x=m.x0.copy();zero=np.zeros_like(x);z=np.zeros_like(P)
s=m.evaluate(x,x,P,c,1,zero,zero,z,zero);j=40;pred=-m.mc[j]*s[0][j];scan=[]
for step in [1e-6,1e-7,1e-8,1e-9,3e-10]:
 xp=x.copy();xm=x.copy();xp[j]+=step;xm[j]-=step
 fd=(m.evaluate(xp,x,P,c,1,zero,zero,z,zero)[4]-m.evaluate(xm,x,P,c,1,zero,zero,z,zero)[4])/(2*step)
 scan.append(dict(step=step,finite_difference=fd,prediction=pred,relative_error=abs(fd-pred)/abs(pred)))
u=Radial(128,0);zz=np.zeros_like(u.edge);z=np.zeros_like(u.r)
rc,_,_=u.dep(u.r,u.mc);rb,_,_=u.dep(u.r,u.mb)
s=u.evaluate(u.r,u.r,zz,np.ones_like(z),1,z,z,zz,z)
null=dict(relative_density_roundoff=max(np.max(abs(rc/(u.mc.sum()/u.vol.sum())-1)),np.max(abs(rb/(u.mb.sum()/u.vol.sum())-1))),force_maxima=[float(np.max(abs(v))) for v in s[:4]])
checks=[dict(name='force_step_scan_at_1e-9',passed=scan[3]['relative_error']<1e-5,value=scan[3]['relative_error']),dict(name='uniform_density_roundoff',passed=null['relative_density_roundoff']<1e-13,value=null['relative_density_roundoff']),dict(name='null_absolute_original_threshold',passed=max(null['force_maxima'])<1e-7,value=max(null['force_maxima']))]
early=Radial(256,.03*1101/4401,4400);pe,ce,re=early.static(early.x0)
Path(a.output).write_text(json.dumps(dict(checks=checks,force_scan=scan,null=null,early_equilibrium=dict(Pmax=float(max(abs(pe))),chi_min=float(min(ce)),chi_max=float(max(ce)),residual=re)),indent=2)+'\n')
