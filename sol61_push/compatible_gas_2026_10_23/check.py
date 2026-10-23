import json,sys
import numpy as np
from gas import Gas,rates
m=Gas(n=64,fmol=0,xe=0);y=m.initial();t=m.ti
# Perturb inward mesh velocity so viscous pressure is active.
y[m.sl[3]]=-3*m.Hi*m.edge*(1-m.edge/m.R)
k,d,_=m.eval(t,y)
checks=[]
for eps in [1e-7,3e-8,1e-8]:
 ep=m.eval(t+eps,y+eps*k)[1]['energy'];em=m.eval(t-eps,y-eps*k)[1]['energy']
 fd=(ep-em)/(2*eps);target=k[-2]+k[-1];checks.append(dict(eps=eps,derivative=fd,target=target,relative=abs(fd-target)/max(abs(target),1e-30)))
# Individual gas gravity+pressure force = minus energy gradient at fixed u entropy.
frozen=m.eval(t,y,True);fdchecks=[]
for j in [0,8,31,60]:
 eps=m.dx*1e-5;yp=y.copy();ym=y.copy();yp[m.sl[2]][j]+=eps;ym[m.sl[2]][j]-=eps
 vol=m.gasgrid(y[m.sl[2]])[1]
 for yy in [yp,ym]:yy[m.sl[8]]*= (vol/m.gasgrid(yy[m.sl[2]])[1])**(m.gamma-1)
 # Switch viscosity off to compare conservative force.
 old=m.visc;m.visc=0;ff=m.eval(t,y,True)[0][m.sl[3]][j]*m.mnode[j]
 grad=(m.eval(t,yp,True)[1]['energy']-m.eval(t,ym,True)[1]['energy'])/(2*eps);m.visc=old
 fdchecks.append(dict(j=j,force=ff,negative_gradient=-grad,relative=abs(ff+grad)/max(abs(ff),1e-20)))
ns=np.array([1e-8,1e2,1e4,1e8,1e14]);low,lte,L=rates(np.full(5,500.),ns)
r=dict(energy_derivative=checks,force_derivative=fdchecks,cooling=dict(density=ns.tolist(),per_molecule=L.tolist(),LTE=lte.tolist(),low_density_ratio=float(L[0]/(ns[0]*low[0])),high_density_ratio=float(L[-1]/lte[-1])),pass_energy=min(c['relative'] for c in checks)<1e-6,pass_force=max(c['relative'] for c in fdchecks)<1e-5)
open(sys.argv[1],'w').write(json.dumps(r,indent=2,default=lambda x:x.item()));print(json.dumps(r,indent=2,default=lambda x:x.item()))
