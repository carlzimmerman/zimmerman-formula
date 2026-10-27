import json,argparse
from pathlib import Path
import numpy as np
from model import Model,evolve
p=argparse.ArgumentParser();p.add_argument('--output');args=p.parse_args();m=Model(n=16,np_side=6,mass_ratio=2);x=m.x0.copy();P,c,st=m.static(x);E,ax,aP,ac,h,d=m.evaluate(x,P,c);checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=float(v)))
rho,flat,der=m.deposit(x);ck('mass_deposition',abs(rho.sum()*m.vol-m.mass)<1e-12,rho.sum()*m.vol-m.mass)
ck('constant_interpolant_derivative',np.max(abs(der.sum(axis=1)))<1e-12,np.max(abs(der.sum(axis=1))))
eps=1e-5;xx=x.copy();xx[23,1]+=eps;yy=x.copy();yy[23,1]-=eps;fd=(m.evaluate(xx,P,c)[0]-m.evaluate(yy,P,c)[0])/(2*eps);ck('particle_energy_force',abs(fd+m.m*ax[23,1])<1e-8,abs(fd+m.m*ax[23,1]))
q=np.sin(np.arange(P.size)).reshape(P.shape);q/=np.linalg.norm(q);fd=(m.evaluate(x,P+eps*q,c)[0]-m.evaluate(x,P-eps*q,c)[0])/(2*eps);an=-m.vol*m.eta*np.sum(aP*q);ck('P_energy_force',abs(fd-an)<1e-8,abs(fd-an))
z=np.cos(np.arange(c.size)).reshape(c.shape);z/=np.linalg.norm(z);fd=(m.evaluate(x,P,c+eps*z)[0]-m.evaluate(x,P,c-eps*z)[0])/(2*eps);an=-m.vol*m.b*np.sum(ac*z);ck('chi_energy_force',abs(fd-an)<1e-8,abs(fd-an))
Pv=q*.1;cv=z*.1;pabs=np.sqrt(np.sum(P*P,axis=0));dot=-h*m.div(Pv)-.5*h*h*cv+np.sum(P/(1-pabs)*Pv,axis=0)+m.a*(c-1)*cv+m.d*np.sum(m.grad(c)*m.grad(cv),axis=0)+m.eta*np.sum(Pv*aP,axis=0)+m.b*cv*ac
err=abs(m.vol*np.sum(m.mask*dot)+m.flux(Pv,cv,h,c).sum());ck('local_signed_field_flux_identity',err<1e-10,err)
runs=[evolve(m,dt=.003,end=.9),evolve(m,dt=.0015,end=.9),evolve(m,dt=.003,end=.9,frozen=True)]
for i,r in enumerate(runs):ck('energy_'+str(i),r['max_energy_error']<1e-3,r['max_energy_error'])
Path(args.output).write_text(json.dumps(dict(checks=checks,runs=runs),indent=2)+'\n')
