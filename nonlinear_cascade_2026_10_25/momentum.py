"""Same implicit midpoint equations, solve scaled carrier momentum directly."""
import numpy as np
from scipy.linalg import solve_banded
from fine_material import FineMaterial
class Momentum(FineMaterial):
 def carrier_mid(self,a,chi,x0,p0,dt,guess):
  Z=self.Z(a);rootZ=np.sqrt(Z);parts=self.vacuum_parts(a,chi);y=np.zeros(self.n);coef=dt/(2*rootZ);res=np.inf
  for it in range(40):
   x=x0+coef*y;G,hd,off,scale=self.carrier_force(x,parts);R=y-p0/rootZ+coef*G;dg=1+coef*coef*hd;od=coef[:-1]*coef[1:]*off;weight=1+coef*coef*scale;merit=np.sum(R*R/weight);ab=np.zeros((3,self.n));ab[0,1:]=od;ab[1]=dg;ab[2,:-1]=od
   try:dy=solve_banded((1,1),ab,-R,check_finite=False)
   except np.linalg.LinAlgError:break
   res=float(np.max(abs((R/coef)/(scale+4*Z/dt**2))))
   if res<1e-12 and np.max(abs(dy))<1e-12:break
   rate=1.
   for ls in range(20):
    yn=y+rate*dy;Gn=self.carrier_force(x0+coef*yn,parts)[0];Rn=yn-p0/rootZ+coef*Gn
    if np.sum(Rn*Rn/weight)<=merit+1e-30:break
    rate*=.5
   y=yn
  self.last_mid_alpha=x0+coef*y;self.last_carrier_displacement=coef*y
  return self.last_mid_alpha,y*rootZ,float(res)
 def full_step(self,a0,x0,p0,chi0,pi0,dt):
  a1=a0.copy();chi1=chi0.copy();xm=x0.copy();maxres=0.;err=np.inf
  for it in range(45):
   amid=(a0+a1)/2;cmid=(chi0+chi1)/2;xm,pm,res=self.carrier_mid(amid,cmid,x0,p0,dt,xm);maxres=max(maxres,res);mu=self.pot(amid,xm,True)[1];u=self.enclosed(abs(amid[0])**2);angular_rate=pm/self.Z(amid);mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*angular_rate**2*self.f(u)[3]);an=self.material_cn(a0,mu,xm,cmid,dt);am=(a0+an)/2;align=self.alignment(am,xm,cmid);rate=2*self.J/self.sigma*np.imag(np.conj(am[0])*align[0]);cn,pn,sink,qs=self.wave_source(chi0,pi0,rate,dt)
   err=max(float(np.max(abs(an-a1))),float(np.max(abs(cn-chi1)))*max(self.g,1)/self.sigma)
   a1=an;chi1=cn
   if err<2e-12 and res<1e-9:break
  # Final midpoint p is the kinematically consistent canonical momentum.
  return a1,x0+dt*pm/self.Z(amid),2*pm-p0,chi1,pn,sink,qs,{'iterations':it+1,'fixed_point_error':err,'carrier_root_residual':res,'max_carrier_trial_residual':maxres}

