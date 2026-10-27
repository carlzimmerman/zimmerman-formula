"""Complete cubic CC modes coupled reciprocally to an actual outgoing scalar.

Only a local weak-mode truncation: no galaxy or interface is represented.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg.lapack import dgttrf,dgttrs
from scipy.optimize import root
from fine_material import PhysicalFull
from vertex import equal_resonance
from cc_vertex import cc_vertex

class Model:
 def __init__(self,q=80.,wave_h_kpc=2.,omit_inertia=False,g2_override=None):
  m=PhysicalFull();s=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');a=s['a'];i=np.argmin(abs(m.r*m.rm-3));self.rho=abs(a[0,i])**2/m.vol[i];self.u=m.enclosed(abs(a[0])**2)[i];self.c=m.c;self.tdyn=m.tdyn;self.rm=m.rm;self.g=171.68027319658083 if g2_override is None else g2_override;self.eta=self.g*self.g*self.rho**3/self.c**2;self.R=4*np.pi/q;vol=self.R**3/3;ks=equal_resonance(q,self.rho,self.u,m.k);v=cc_vertex(*ks,self.rho,self.u,m.k,vol,self.eta);self.om=v['omega'];self.A=v['A'];self.V=v['V']-(v['nonlinear_inertia'] if omit_inertia else 0);self.N=.05**2*self.rho**2*vol/(64*self.A[0]**2);self.qcoef=2*self.g*self.A**2;self.qcoef[2]=0.;self.q=q
  ed=np.r_[np.linspace(0,2*self.R,65),np.geomspace(2*self.R,30/m.rm,65)[1:],np.arange(30+wave_h_kpc,6000+wave_h_kpc*.1,wave_h_kpc)/m.rm];self.r=(ed[1:]+ed[:-1])/2;self.vol=np.diff(ed**3)/3;self.w=((self.r[1:]+self.r[:-1])/2)**2/np.diff(self.r);self.diag=np.r_[self.w[0],self.w[:-1]+self.w[1:],self.w[-1]];self.profile=np.exp(-(self.r/self.R)**4);self.profile/=self.vol@self.profile;self.gamma=30*self.c/(2000/m.rm)*np.clip((self.r-4000/m.rm)/(2000/m.rm),0,1)**2;self.cache={}
 def charge(self,z):return float(self.N*np.sum(self.qcoef*(abs(z[0])**2+abs(z[1])**2+2*np.real(z[0]*z[1]))))
 def energy(self,z,chi,pi):
  mat=self.N*np.sum(self.om*abs(z)**2)+2*self.N**1.5*np.real(self.V*np.sum(z[:,0]*z[:,1]*np.conj(z[:,2])));wave=.5*(self.vol@(pi*pi)+self.c**2*(self.w@np.diff(chi)**2));return float(mat+wave)
 def wave(self,chi,pi,dQ,dt):
  if dt not in self.cache:
   lu=dgttrf((-dt*dt*self.c**2/4*self.w/self.vol[1:]).copy(),(1+dt*dt*self.c**2/4*self.diag/self.vol).copy(),(-dt*dt*self.c**2/4*self.w/self.vol[:-1]).copy());self.cache[dt]=lu
  lap=-self.diag*chi;lap[:-1]+=self.w*chi[1:];lap[1:]+=self.w*chi[:-1];rhs=pi+dt*self.c**2/2*lap/self.vol-dQ*self.profile/2;v,info=dgttrs(*self.cache[dt][:-1],np.asfortranarray(rhs[:,None]));assert info==0;v=v[:,0];return chi+dt*v,2*v-pi,v
 def midpoint(self,z0,c0,p0,dt):
  Q0=self.charge(z0);fac=1j*dt*self.om/2;pred=((1-fac)/(1+fac))*z0;last=None
  def fun(y):
   nonlocal last
   z=y[:6].reshape(2,3)+1j*y[6:].reshape(2,3);zm=(z+z0)/2;cn,pn,pm=self.wave(c0,p0,self.charge(z)-Q0,dt);avg=self.vol@(self.profile*pm);G=np.zeros((2,3),complex)
   for k in range(2):
    b=zm[k];G[k]=np.sqrt(self.N)*np.array([np.conj(self.V)*np.conj(b[1])*b[2],np.conj(self.V)*np.conj(b[0])*b[2],self.V*b[0]*b[1]])
   G-=avg*self.qcoef*(zm+np.conj(zm[::-1]));an=((1-fac)*z0-1j*dt*G)/(1+fac);r=z-an;last=(z,cn,pn);return np.r_[r.real.ravel(),r.imag.ravel()]
  y=np.r_[pred.real.ravel(),pred.imag.ravel()];sol=root(fun,y,method='hybr',options={'xtol':1e-10,'maxfev':250});res=float(np.max(abs(fun(sol.x))));return *last,res
 def step(self,z,c,p,dt):
  factor=np.exp(-self.gamma*dt/2);pnew=p*factor;sink=float(.5*(self.vol@(p*p-pnew*pnew)));charge=float(self.vol@(p-pnew));p=pnew;w1=1/(2-2**(1/3));w0=1-2*w1;res=0.
  for frac in [w1,w0,w1]:z,c,p,r=self.midpoint(z,c,p,frac*dt);res=max(res,r)
  pnew=p*factor;sink+=float(.5*(self.vol@(p*p-pnew*pnew)));charge+=float(self.vol@(p-pnew));return z,c,pnew,sink,charge,res

def run(cfg,out):
 m=Model(cfg['q'],cfg.get('wave_h_kpc',2.),cfg.get('omit_inertia',False),cfg.get('g2_override'));z=np.array([[1.,1.,0.],[1.,1.,0.]],complex);chi=np.zeros(len(m.r));pi=chi.copy();E0=m.energy(z,chi,pi);Q0=m.vol@pi+m.charge(z);sink=qs=0.;t=0.;h=cfg['dt_Myr'];trace=[];maxE=maxQ=maxroot=0.;accept=reject=0;start=time.monotonic();status='completed';nextsample=0.;maxdaughter=0.;det=int(np.argmin(abs(m.r*m.rm-500)));detector=[]
 while t<cfg['duration_Myr']-1e-9:
  if time.monotonic()-start>cfg.get('wall_seconds',240):status='wall_limit_partial';break
  h=min(h,cfg['duration_Myr']-t);an,cn,pn,ds,dq,res=m.step(z,chi,pi,h/m.tdyn);En=m.energy(an,cn,pn);defect=En+ds-m.energy(z,chi,pi);tol=cfg.get('local_energy_relative',1e-8)*E0*h/cfg['dt_Myr']
  if res>1e-9 or abs(defect)>tol or not np.isfinite(En):
   h/=2;reject+=1
   if h<1e-6:status='minimum_step_failure';break
   continue
  z,chi,pi=an,cn,pn;t+=h;detector.append([t,chi[det],pi[det]]);sink+=ds;qs+=dq;accept+=1;maxE=max(maxE,abs(En+sink-E0)/E0);maxQ=max(maxQ,abs(m.vol@pi+m.charge(z)+qs-Q0));maxroot=max(maxroot,res);daughter=float(m.N*m.om[2]*np.sum(abs(z[:,2])**2)/E0);maxdaughter=max(maxdaughter,daughter)
  if t>=nextsample:trace.append({'time_Myr':t,'escaped_fraction':sink/E0,'daughter_energy_fraction':daughter,'total_energy_plus_escape_relative_error':(En+sink-E0)/E0,'mode_norms':abs(z).tolist()});nextsample=t+.1
  if abs(defect)<tol/32:h=min(cfg['dt_Myr'],1.25*h)
 out=Path(out);result={'config':cfg,'status':status,'completed_time_Myr':t,'runtime_seconds':time.monotonic()-start,'accepted_steps':accept,'rejected_steps':reject,'rhoT':float(m.rho),'uT':float(m.u),'g2':m.g,'eta_local':float(m.eta),'q':m.q,'vertex':{'real':float(m.V.real),'imag':float(m.V.imag)},'frequencies_per_Myr':(m.om/m.tdyn).tolist(),'initial_material_energy_Eunit':E0,'density_perturbation_bound':.05,'patch_radius_kpc':m.R*m.rm,'escaped_fraction':sink/E0,'max_daughter_energy_fraction':maxdaughter,'max_relative_total_energy_error':maxE,'max_shift_charge_error':maxQ,'max_root_residual':maxroot,'trace':trace,'scope':'Local cubic CC conservative matter modes plus exact reciprocal radial scalar bath and outgoing absorber; zero supplied field energy, free pump depletion. Not the full nonlinear density action, not actual infall occupations, no interface/outer phase/galaxy law test. Material modal truncation omits other quartic and nonresonant interactions.'};out.write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(out.with_name('detector.npz'),data=np.array(detector),radius=float(m.r[det]),c=m.c,tdyn=m.tdyn);np.savez_compressed(out.with_name('state.npz'),z=z,chi=chi,pi=pi);print({k:v for k,v in result.items() if k!='trace'})
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();run({'q':80.,'dt_Myr':.005,'duration_Myr':150.,'wall_seconds':240,'wave_h_kpc':2.},args.output)
