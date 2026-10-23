import json,sys,numpy as np
from gas_v2 import Gas,rates
m=Gas(64,fmol=0,xe=0,visc=0);y=m.initial();t=m.ti
# Stable finite difference of the quadratic gravitational functional.
def rho_phi(yy):
 xc=yy[m.sl[0]];rb=m.gasgrid(yy[m.sl[2]])[2];dr=m.dep(xc,m.mc)[0]+rb-m.J;g=np.cumsum(dr*m.vol)[:-1]/m.edge**2
 phi=np.r_[-np.cumsum((g*m.dx)[::-1])[::-1],0.];phi-=np.sum(phi*m.vol)/np.sum(m.vol);return dr,phi
checks=[]
for j in [0,8,31,60]:
 for step in [1e-3,3e-4,1e-4]:
  eps=m.dx*step;yp=y.copy();ym=y.copy();yp[m.sl[2]][j]+=eps;ym[m.sl[2]][j]-=eps
  v=m.gasgrid(y[m.sl[2]])[1];vp=m.gasgrid(yp[m.sl[2]])[1];vm=m.gasgrid(ym[m.sl[2]])[1]
  rp,pp=rho_phi(yp);rm,pm=rho_phi(ym);deltaG=.5*np.sum(m.vol*(rp-rm)*(pp+pm))
  um=y[m.sl[8]]*(v/vm)**(m.gamma-1);deltaU=np.sum(m.mgas*um*np.expm1(-(m.gamma-1)*np.log(vp/vm)))
  f=m.eval(t,y,True)[0][m.sl[3]][j]*m.mnode[j];grad=(deltaG+deltaU)/(2*eps)
  checks.append(dict(j=j,step=step,force=f,negative_gradient=-grad,relative=abs(f+grad)/abs(f)))
# Closed spherical gas pressure/viscosity exercise, frozen background, no gravity.
def gas_rhs(yy):
 b,p,u=np.split(yy,[m.n-1,2*(m.n-1)]);faces,v,rb=m.gasgrid(b);rho=m.mgas/v;vel=np.r_[0,p,0];theta=np.diff(faces**2*vel)/v;dv=np.diff(vel);q=rho*2*np.where(theta<0,np.maximum(-dv,0),0)**2;press=(m.gamma-1)*rho*u+q
 return np.r_[p,b*b*np.diff(-press)/m.mnode,-press/rho*theta]
def energy(yy):
 b,p,u=np.split(yy,[m.n-1,2*(m.n-1)]);return .5*np.sum(m.mnode*p*p)+np.sum(m.mgas*u)
def integrate(dt):
 yy=np.r_[m.edge,-.3*np.sin(np.pi*m.edge/m.R),np.where(m.r<m.R*.5,.01,.001)];E=energy(yy);s0=yy[-m.n:]*m.vol**(m.gamma-1);mn=1e99
 for i in range(round(.08/dt)):
  k=gas_rhs(yy);k2=gas_rhs(yy+dt*k/2);k3=gas_rhs(yy+dt*k2/2);k4=gas_rhs(yy+dt*k3);yy+=dt*(k+2*k2+2*k3+k4)/6;mn=min(mn,min(yy[-m.n:]));m.gasgrid(yy[:m.n-1])
 sf=yy[-m.n:]*m.gasgrid(yy[:m.n-1])[1]**(m.gamma-1)
 return dict(dt=dt,relative_energy_error=abs(energy(yy)-E)/E,min_internal=mn,min_entropy_ratio=float(min(sf/s0)),max_entropy_ratio=float(max(sf/s0)))
shock=[integrate(dt) for dt in [.0002,.0001,.00005]]
r=dict(force_gradient=checks,pass_force=all(min(c['relative'] for c in checks if c['j']==j)<1e-5 for j in [0,8,31,60]),closed_compressive_gas=shock,pass_gas=all(a['relative_energy_error']<1e-5 and a['min_internal']>0 and a['min_entropy_ratio']>1-1e-8 for a in shock))
open(sys.argv[1],'w').write(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
