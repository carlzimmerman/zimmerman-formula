"""Diagnostic mass-current labels and passive stars; labels never source gravity."""
import json,numpy as np
from scipy.interpolate import CubicSpline
from field_tools import harmonics,Potential
class Wave:
 def __init__(self,v,r,w,lm,eta):self.s=CubicSpline(r,v/(np.sqrt(w)*r)[:,None],axis=0);self.lm=lm;self.eta=eta
 def values(self,x):
  d,mu,Y,dY,er,et,ep=harmonics(self.lm,x);q=self.s(d);dq=self.s(d,1);psi=np.sum(q*Y,axis=1);dr=np.sum(dq*Y,axis=1);dt=np.sum(q*dY,axis=1)/d;dp=np.sum(q*Y*1j*np.array([m for l,m in self.lm]),axis=1)/(d*np.sqrt(1-mu*mu));grad=dr[:,None]*er+dt[:,None]*et+dp[:,None]*ep;return psi,grad
class Tracker:
 def __init__(self,ang,r,w,eta,name,dt,M,R,V,substeps,previous):
  self.ang=ang;self.r=r;self.w=w;self.eta=eta;self.name=name;self.dt=dt;self.M=M;self.R=R;self.V=V;self.substeps=substeps;self.previous=previous;self.rows=[];self.positions=[];self.weights_history=[];self.node_flag_count=0;self.outside_weight=0.;self.source='j/rho reconstruction; no angular-projection source correction';self.stellar_mass=previous['stellar_mass']/M;self.a0=9.3603e-11*3.085677581491367e10*R/(V*V)
 def before_sink(self,v):pass
 def initialize(self,t,v):
  self.t=t;self.birth=t;self.prev=v.copy();self.center=np.array(self.previous['center']);self.bulk=np.array(self.previous['bulk']);rng=np.random.default_rng(11011);va=self.ang.field.forward(v);wm=self.ang.field.w;nf=self.ang.field.nphi;mu=self.ang.field.mu;weights=abs(va)**2*wm[None,:,None]*(2*np.pi/nf)/2;maskparts=[]
  for side in range(2):
   phi=np.arange(nf)*np.pi/nf+side*np.pi;unit=np.stack(np.broadcast_arrays(np.sqrt(1-mu[:,None]**2)*np.cos(phi)[None,:],np.sqrt(1-mu[:,None]**2)*np.sin(phi)[None,:],mu[:,None]),axis=-1);maskparts.append(np.linalg.norm(self.r[:,None,None,None]*unit[None,:,:,:]-self.center,axis=-1)<1)
  full=np.concatenate([weights.ravel(),weights.ravel()]);mask=np.concatenate([z.ravel() for z in maskparts]);self.N=512;points=[];ww=[]
  for pp in [full,full*mask]:
   ix=rng.choice(len(pp),size=self.N,p=pp/pp.sum());side,idx=np.divmod(ix,weights.size);ir,jk=np.divmod(idx,len(mu)*nf);it,ip=np.divmod(jk,nf);phi=np.pi*ip/nf+side*np.pi;mm=mu[it];points.append(self.r[ir,None]*np.c_[np.sqrt(1-mm*mm)*np.cos(phi),np.sqrt(1-mm*mm)*np.sin(phi),mm]);ww.extend([pp.sum()/self.N]*self.N)
  self.x=np.concatenate(points);self.weights=np.array(ww);self.initial_tag_mass=float(np.sum(self.weights[self.N:]));self.initial_global_mass=float(np.sum(self.weights[:self.N]));self.active=np.ones(len(self.x),bool)
  # Same deterministic circular probe construction as CCT-010.
  rng=np.random.default_rng(1010);N=128;u=rng.normal(size=(N//2,3));u/=np.linalg.norm(u,axis=1)[:,None];u=np.r_[u,-u];vv=rng.normal(size=(N//2,3));vv=np.r_[vv,-vv];tan=vv-u*np.sum(vv*u,axis=1)[:,None];tan/=np.linalg.norm(tan,axis=1)[:,None];ff=((np.arange(N//2)+.5)/(N//2))*27/(10**1.5);rr=(ff**(-2/3)-1)**(-.5);rr=np.r_[rr,rr];self.scales=[1.] if self.name!='Sextans' else [434.24183348/self.R,794.188604/self.R];rad=rr*np.resize(self.scales,N);self.sx=self.center+rad[:,None]*u;acc=-self.cold_force(t,self.sx)+self.baryon_acc(self.sx);vc=np.sqrt(rad*np.maximum(-np.sum(acc*u,axis=1),0));self.sv=self.bulk+vc[:,None]*tan
 def cold_force(self,t,x):
  ts=self.previous['times'];co=self.previous['coeff'];j=np.clip(np.searchsorted(ts,t)-1,0,len(ts)-2);f=np.clip((t-ts[j])/(ts[j+1]-ts[j]),0,1);return Potential(self.r,(1-f)*co[j]+f*co[j+1],self.ang.density.lm).evaluate(x,True)
 def baryon_acc(self,x):
  d=x-x.mean(axis=0);rad=np.maximum(np.linalg.norm(d,axis=1),1e-10);gn=sum(self.stellar_mass/len(self.scales)*rad/(rad*rad+a*a)**1.5 for a in self.scales);gb=.5*(gn+np.sqrt(gn*gn+4*self.a0*gn));return -gb[:,None]*d/rad[:,None]
 def after_sink(self,v):
  # Align a spatially constant phase, which leaves all densities/currents invariant.
  vv=v*np.exp(-1j*np.angle(np.vdot(self.prev,v)));a=Wave(self.prev,self.r,self.w,self.ang.field.lm,self.eta);b=Wave(vv,self.r,self.w,self.ang.field.lm,self.eta)
  def velocity(x,f):
   ps0,g0=a.values(x);ps1,g1=b.values(x);psi=(1-f)*ps0+f*ps1;grad=(1-f)*g0+f*g1;small=abs(psi)**2<1e-20;self.node_flag_count+=int(small.sum());return self.eta*np.imag(psi.conj()[:,None]*grad)/np.maximum(abs(psi)**2,1e-300)[:,None]
  ds=self.dt/self.substeps
  for k in range(self.substeps):
   ix=np.flatnonzero(self.active);x=self.x[ix];f=k/self.substeps;v0=velocity(x,f);mid=x+ds*v0/2
   # A trajectory leaving the represented radial domain is censored and reported.
   outside=np.linalg.norm(mid,axis=1)>=self.r[-1];ids=ix[outside];self.outside_weight+=float(self.weights[ids].sum());self.active[ids]=False;self.weights[ids]=0.;ix=ix[~outside];x=x[~outside];mid=mid[~outside];vel=velocity(mid,f+.5/self.substeps);self.x[ix]=x+ds*vel;rad=np.linalg.norm(mid,axis=1);self.weights[ix]*=np.exp(-2*ds*(np.maximum(rad-16,0)/12)**4)
  # Full inertial passive-star kick/drift/kick; baryonic source is rigid and no cold backreaction.
  t=self.t;acc=-self.cold_force(t,self.sx)+self.baryon_acc(self.sx);self.sv+=self.dt*acc/2;self.sx+=self.dt*self.sv;acc=-self.cold_force(t+self.dt,self.sx)+self.baryon_acc(self.sx);self.sv+=self.dt*acc/2;self.t+=self.dt;self.prev=v.copy()
 def record(self,t,v):
  if not self.rows:self.initialize(t,v)
  xs=self.sx.mean(axis=0);vs=self.sv.mean(axis=0);ix=slice(self.N,None);ww=self.weights[ix];xx=self.x[ix];ct=np.average(xx,weights=ww,axis=0);dist=np.linalg.norm(xx-ct,axis=1);order=np.argsort(dist);cdf=np.cumsum(ww[order]);r50=float(np.interp(.5*ww.sum(),cdf,dist[order]));near=np.linalg.norm(xx-xs,axis=1)<1;inside=float(ww[near].sum());rad=np.geomspace(.2,20,32);shell=np.sum(abs(v)**2,axis=1);fieldcdf=np.interp(rad,self.r,np.cumsum(shell),left=0,right=shell.sum())/shell.sum();gcdf=np.array([np.sum(self.weights[:self.N][np.linalg.norm(self.x[:self.N],axis=1)<rr]) for rr in rad])/np.sum(self.weights[:self.N]);srad=np.linalg.norm(self.sx-xs,axis=1)
  row=dict(t=t,tagged_mass_Msun=float(ww.sum()*self.M),tagged_mass_within_Rstar_of_stars_Msun=inside*self.M,retained_near_stars_fraction=inside/self.initial_tag_mass,tagged_COM_pc=(ct*self.R).tolist(),stellar_COM_pc=(xs*self.R).tolist(),material_stellar_COM_separation_pc=float(np.linalg.norm(ct-xs)*self.R),tagged_r50_pc=r50*self.R,stellar_r50_pc=float(np.median(srad)*self.R),stellar_sigma_1d_kms=float(np.sqrt(np.mean((self.sv-vs)**2))*self.V),whole_cloud_radial_CDF_max_error=float(np.max(abs(gcdf-fieldcdf))),node_flag_evaluations=self.node_flag_count,censored_weight_Msun=self.outside_weight*self.M);self.rows.append(row);self.positions.append(self.x.copy());self.weights_history.append(self.weights.copy());print(self.name,'labels',round(t,2),round(row['retained_near_stars_fraction'],4),round(row['whole_cloud_radial_CDF_max_error'],4),flush=True)
 def save(self,path):
  np.savez_compressed(str(path)+'_labels.npz',positions=self.positions,weights=self.weights_history,stellar_positions=self.sx,stellar_velocities=self.sv)
  open(str(path)+'_labels.json','w').write(json.dumps(dict(scope='diagnostic continuum-current labels, not particles or extra gravity; finite angular local-source defect is separately audited and limits material inference',substeps=self.substeps,N_per_label_group=self.N,initial_tag_mass_Msun=self.initial_tag_mass*self.M,history=self.rows),indent=2)+'\n')
