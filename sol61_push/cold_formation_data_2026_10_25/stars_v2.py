"""Positive-beta=-1/2 DF cohorts and paired passive stellar response."""
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator
from scipy.integrate import cumulative_trapezoid
from radial_v2 import phi_shell

class Cold:
 def __init__(self,r,dm):
  self.r=r;self.dm=dm;self.mass=float(dm.sum());p=phi_shell(r,dm);self.spline=PchipInterpolator(np.r_[0,r],np.r_[-np.sum(dm/r),p]);self.der=self.spline.derivative()
 def phi(self,q):
  q=np.asarray(q);return np.where(q<=self.r[-1],self.spline(np.minimum(q,self.r[-1])),-self.mass/np.maximum(q,1e-300))
 def g(self,q):
  q=np.asarray(q);return np.where(q<=self.r[-1],self.der(np.minimum(q,self.r[-1])),self.mass/np.maximum(q*q,1e-300))

class Background:
 def __init__(self,q,aa,a0):
  self.q=q;self.aa=np.array(aa);self.a0=a0;grid=np.geomspace(1e-10,1e8,131072);value=cumulative_trapezoid(self.g(grid),grid,initial=0.);self.spline=CubicSpline(np.log(grid),value)
 def gn(self,r):return sum(self.q/len(self.aa)*r/(r*r+a*a)**1.5 for a in self.aa)
 def g(self,r):
  g=self.gn(r);return .5*(g+np.sqrt(g*g+4*self.a0*g))
 def phi(self,r):return self.spline(np.log(np.maximum(r,1e-10)))

def draw(r,dm,bg,a,n=1024,seed=1025):
 rng=np.random.default_rng(seed);cold=Cold(r,dm);grid=np.unique(np.r_[np.geomspace(max(a*1e-5,1e-8),max(a*1e6,1e5),12000),r]);pot=cold.phi(grid)+bg.phi(grid);keep=np.r_[True,np.diff(pot)>1e-14];grid=grid[keep];pot=pot[keep]
 A=(1+(grid/a)**2)**(-2.5)/grid;Ar=-A*(1/grid+5*grid/(a*a+grid*grid));g=cold.g(grid)+bg.g(grid);Ap=Ar/g
 def energy_cdf(rr):
  pp=float(cold.phi(rr)+bg.phi(rr));aa=(1+(rr/a)**2)**(-2.5)/rr;j=int(np.searchsorted(grid,rr,side='right'));E=np.r_[pp,pot[j:]];cdf=np.r_[0.,1-(A[j:]-(pot[j:]-pp)*Ap[j:])/aa];drop=float(max(0,-np.diff(cdf).min()))
  return E,cdf,drop
 maxdrop=0.;moment=[]
 for rr in [a*.5,a,2*a]:
  E,cdf,drop=energy_cdf(rr);maxdrop=max(maxdrop,drop);j=grid>rr;ss=np.r_[rr,grid[j]];nu=(1+(ss/a)**2)**(-2.5);target=4*rr/(1+(rr/a)**2)**(-2.5)*np.trapz(nu*(cold.g(ss)+bg.g(ss))/ss,ss);got=2*np.trapz(1-cdf,E-E[0]);moment.append(abs(got/target-1))
 radii=a/np.sqrt(((np.arange(n)+.5)/n)**(-2/3)-1);speed=np.empty(n)
 for j,rr in enumerate(radii):
  E,cdf,drop=energy_cdf(rr);maxdrop=max(maxdrop,drop)
  if drop>1e-6:raise ValueError('nonpositive DF energy CDF: decrease '+str(drop))
  # Only floating-point-sized reversals removed; substantive failure above is retained.
  cdf=np.maximum.accumulate(cdf);ee=np.interp(rng.random(),cdf,E);speed[j]=np.sqrt(max(0,2*(ee-E[0])))
 dirs=rng.normal(size=(n,3));dirs/=np.linalg.norm(dirs,axis=1)[:,None];tangent=rng.normal(size=(n,3));tangent-=np.sum(tangent*dirs,axis=1)[:,None]*dirs;tangent/=np.linalg.norm(tangent,axis=1)[:,None];four=rng.normal(size=(n,4));mu=four[:,0]/np.linalg.norm(four,axis=1);velocity=speed[:,None]*(mu[:,None]*dirs+np.sqrt(1-mu*mu)[:,None]*tangent)
 return dict(x=radii[:,None]*dirs,v=velocity,direction_mu=mu,cdf_max_decrease=maxdrop,moment_control_relative_error=max(moment),seed=seed)

class Cohort:
 def __init__(self,r,dm,bg,a,n,seed,birth):
  d=draw(r,dm,bg,a,n,seed);self.x=d.pop('x');self.v=d.pop('v');d.pop('direction_mu');self.controls=d;self.xc=self.x.copy();self.vc=self.v.copy();self.birth=birth;self.bg=bg;self.frozen=Cold(r,dm);self.work=np.zeros(n);self.E0=self.energy(self.x,self.v,self.frozen);self.escale=np.sum(self.v*self.v,axis=1)+abs(self.frozen.phi(np.linalg.norm(self.x,axis=1)))+1e-10;self.initial_L=np.cross(self.x,self.v);self.a=a;self.max_ledger=0.;self.max_frozen_drift=0.;self.history=[];self.substep_cap_exceeded=False;self.max_substeps=0
 def energy(self,x,v,cold):
  r=np.linalg.norm(x,axis=1);return .5*np.sum(v*v,axis=1)+cold.phi(r)+self.bg.phi(r)
 def accel(self,x,cold):
  rr=np.linalg.norm(x,axis=1);return -(cold.g(rr)+self.bg.g(rr))[:,None]*x/rr[:,None]
 def advance(self,old,new,dt):
  # Four endpoint work switches, paired with two star substeps in each cold interval.
  rr=np.linalg.norm(self.x,axis=1);rrc=np.linalg.norm(self.xc,axis=1);omega=max(np.max(np.sqrt((old.g(rr)+self.bg.g(rr))/rr)),np.max(np.sqrt((self.frozen.g(rrc)+self.bg.g(rrc))/rrc)));needed=max(2,int(np.ceil(dt*omega/.015)));self.substep_cap_exceeded|=needed>512;nsub=min(512,needed);self.max_substeps=max(self.max_substeps,nsub)
  for k in range(nsub):
   f0=k/nsub;f1=(k+1)/nsub;fm=.5*(f0+f1);h=dt/nsub
   def af(x,f):return (1-f)*self.accel(x,old)+f*self.accel(x,new)
   rr0=np.linalg.norm(self.x,axis=1);self.work+=(fm-f0)*(new.phi(rr0)-old.phi(rr0));self.v+=.5*h*af(self.x,fm);self.x+=h*self.v;self.v+=.5*h*af(self.x,fm);rr1=np.linalg.norm(self.x,axis=1);self.work+=(f1-fm)*(new.phi(rr1)-old.phi(rr1))
   self.vc+=.5*h*self.accel(self.xc,self.frozen);self.xc+=h*self.vc;self.vc+=.5*h*self.accel(self.xc,self.frozen)
  self.max_ledger=max(self.max_ledger,float(np.max(abs(self.energy(self.x,self.v,new)-self.E0-self.work)/self.escale)))
  self.max_frozen_drift=max(self.max_frozen_drift,float(np.max(abs(self.energy(self.xc,self.vc,self.frozen)-self.E0)/self.escale)))
 def diag(self,t,cold):
  def obs(x,v):
   rr=np.linalg.norm(x,axis=1);return dict(r50=float(np.median(rr)),projected_r50=float(np.median(np.linalg.norm(x[:,:2],axis=1))),sigma_los=float(np.std(v[:,2])),orientation_sigma=float(np.sqrt(np.mean(np.sum((v-v.mean(axis=0))**2,axis=1))/3)))
  s=obs(self.x,self.v);control=obs(self.xc,self.vc);row=dict(t=t,birth=self.birth,stars=s,frozen_control=control,paired_r50=s['r50']/control['r50'],paired_sigma_los_ratio=s['sigma_los']/control['sigma_los'],paired_orientation_variance_ratio=(s['orientation_sigma']/control['orientation_sigma'])**2,work_ledger_max_relative=self.max_ledger,substep_cap_exceeded=self.substep_cap_exceeded,max_substeps=self.max_substeps,frozen_energy_max_relative=self.max_frozen_drift,mean_cold_work=float(self.work.mean()),max_L_vector_relative=float(np.max(np.linalg.norm(np.cross(self.x,self.v)-self.initial_L,axis=1))/max(np.max(np.linalg.norm(self.initial_L,axis=1)),1e-30)));self.history.append(row);return row
