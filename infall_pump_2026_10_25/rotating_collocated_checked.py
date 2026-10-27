"""Same full CC action; extend scalar collocation to the fine material region.

This reduces sparse Jacobian coloring conflicts, not the scalar degrees of
freedom. Material remains unchanged and the absorber is outside all matter.
"""
import numpy as np
from rotating_phi_checked import ContinuedSparse as SparseMidpoint
class Collocated(SparseMidpoint):
 def __init__(self,**kw):
  super().__init__(**kw)
  R=kw.get('wave_R_kpc',10000.);h=kw.get('wave_h_kpc',2.)
  self.wr=np.r_[self.r[self.r*self.rm<320.],np.arange(320.,R+h*.1,h)/self.rm]
  ed=np.r_[0.,.5*(self.wr[1:]+self.wr[:-1]),self.wr[-1]+.5*(self.wr[-1]-self.wr[-2])]
  self.wvol=np.diff(ed**3)/3;self.ww=ed[1:-1]**2/np.diff(self.wr);self.wdiag=np.r_[self.ww[0],self.ww[:-1]+self.ww[1:],self.ww[-1]]
  self.gamma=30*self.c/(2000/self.rm)*np.clip((self.wr-(R-2000)/self.rm)/(2000/self.rm),0,1)**2
  self.ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);self.frac=np.clip((self.r-self.wr[self.ids])/(self.wr[self.ids+1]-self.wr[self.ids]),0,1);self.wcache={}

class FourthOrder(Collocated):
 """Fourth order Hamiltonian triple midpoint; positive absorber half steps."""
 def full_step(self,a,x,p,chi,pi,dt):
  gamma=self.gamma.copy();vold=pi.copy();pi=pi*np.exp(-gamma*dt/2)
  sink=float(.5*self.wvol@(vold*vold-pi*pi));qs=float(self.wvol@(vold-pi));self.gamma=np.zeros_like(gamma)
  coeff=1/(2-2**(1/3));infos=[];work=bulkwork=convwork=farflux=farwork=0.;mincap=1.
  edge=int(np.argmin(abs((self.wr[:-1]+self.wr[1:])/2-500/self.rm)))
  try:
   for fraction in [coeff,1-2*coeff,coeff]:
    aa,xx,pp,cc,vv,ds,dq,info=super().full_step(a,x,p,chi,pi,dt*fraction)
    cap=float(np.min(.9997-self.enclosed(abs(aa[0])**2)));mincap=min(mincap,cap)
    if info['fixed_point_error']>1e-9 or cap<=0:
     info['substep_failed']=True;return aa,xx,pp,cc,vv,sink,qs,info
    vm=(pi+vv)/2;cm=(chi+cc)/2
    farflux+=float(-dt*fraction*self.c**2*self.ww[edge]*(cm[edge+1]-cm[edge])*(vm[edge+1]+vm[edge])/2)
    dep=np.bincount(self.ids,weights=(1-self.frac)*info['source_cell'],minlength=len(vm))+np.bincount(self.ids+1,weights=self.frac*info['source_cell'],minlength=len(vm))
    farwork+=float(-dt*fraction*dep[edge+1:]@vm[edge+1:])
    work+=float(-dt*fraction*info['source_cell']@self.true_chi_m(vm));bulkwork+=float(-dt*fraction*info['source_bulk']@self.true_chi_m(vm));convwork+=float(-dt*fraction*info['source_conversion']@self.true_chi_m(vm));infos.append(info);a,x,p,chi,pi=aa,xx,pp,cc,vv
  finally:self.gamma=gamma
  vold=pi.copy();pi=pi*np.exp(-gamma*dt/2);sink+=float(.5*self.wvol@(vold*vold-pi*pi));qs+=float(self.wvol@(vold-pi));self.energy_chi=chi
  info=infos[-1].copy();info.update(iterations=sum(i['iterations'] for i in infos),fixed_point_error=max(i['fixed_point_error'] for i in infos),carrier_root_residual=max(i['carrier_root_residual'] for i in infos),root_runtime_seconds=sum(i['root_runtime_seconds'] for i in infos),minimum_substep_cap_slack=mincap,integrated_far_flux=farflux,integrated_far_work=farwork,integrated_work=work,integrated_bulk_work=bulkwork,integrated_conversion_work=convwork,substep_root_histories=[i['root_history'] for i in infos])
  return a,x,p,chi,pi,sink,qs,info

class RotatingFourth(FourthOrder):
 def full_step(self,a,x,p,chi,pi,dt):
  self.rho_coupling=None;self.chi_override=None
  mu=self.pot(a,x,True)[1];u=self.enclosed(abs(a[0])**2);omega=p/self.Z(a)
  mu[0]-=(2/np.pi)**2*self.ell2/self.c**2*self.transpose(.5*self.vol*omega**2*self.f(u)[3]);extra,source,bulk,conv,U,rate=self.transfer(a,x,chi);mu[0]+=extra
  Ha=(self.kd+mu)*a+self.J*self.alignment(a,x,chi);Ha[0,:-1]+=self.ko*U*a[0,1:];Ha[0,1:]+=self.ko*np.conj(U)*a[0,:-1];Ha[1,:-1]+=self.ko*a[1,1:];Ha[1,1:]+=self.ko*a[1,:-1]
  total=np.sqrt(np.sum(abs(a)**2,axis=0));mask=abs(a)>1e-4*total;freq=np.zeros_like(a.real);freq[mask]=np.real(np.conj(a[mask])*Ha[mask])/(self.sigma*abs(a[mask])**2)
  self.rotation_frequency=freq
  try:
   result=super().full_step(a,x,p,chi,pi,dt);result[-1]['max_reference_phase_step']=float(np.max(abs(freq))*abs(dt));return result
  finally:self.rotation_frequency=np.zeros_like(freq)
