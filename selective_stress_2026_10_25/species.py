"""Same selective energy in independent species amplitudes; no angle singularity."""
import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from scipy.optimize import minimize
from selective import Selective
from two_field_refine import transfer
from joint import T,RESERVOIR

class Species(Selective):
 def amplitude_energy(self,a):
  n=self.n;b=a[:2*n];b=b*torch.sqrt(RESERVOIR/torch.sum(b*b));t=b[:n];f=b[n:];x=a[2*n:];mt=t*t;mf=f*f;mass=mt+mf;theta=torch.pi*x/2
  u=self.A@mt;w,F=self.functions(u);s=torch.sin(torch.pi*x)**2/torch.pi**2
  E=torch.sum(self.vol*(w+self.beta*.95*s*F))+torch.sum(self.tw*self.functions(mt.sum()*self.tt**2)[0]/self.tt**4)
  ff=self.functions((u[1:]+u[:-1])/2)[1];weight=self.rf**2/self.dr;dx=x[1:]-x[:-1]
  E=E+.5*torch.sum(weight*(self.ell2*ff+(self.vacuum_length/self.rm)**2)*dx**2)
  k=self.strength*(self.material_length/self.rm)**2;aF=f/torch.sqrt(self.vol);aT=t/torch.sqrt(self.vol)
  E=E+.5*k*torch.sum(weight*((aF[1:]-aF[:-1])**2+self.delta*(aT[1:]-aT[:-1])**2))
  gd=self.A@mass;gb=self.r/(self.r**2+self.b**2)**1.5
  E=E-torch.sum(self.vol*(.5*gd**2+gb*gd))-.5*RESERVOIR**2/self.R-RESERVOIR/np.sqrt(self.R**2+self.b**2)
  E=E+1.5*self.K*torch.sum(self.vol*(mf/self.vol)**(5/3))
  return E+torch.sum(self.volume_cost*self.vol*torch.sin(theta)**2-self.eps*mt+self.J*(t*torch.cos(theta)-f*torch.sin(theta))**2)
 def afg(self,a):
  aa=T(a).requires_grad_(True);E=self.amplitude_energy(aa);g=torch.autograd.grad(E,aa)[0]
  return float(E.detach()),g.detach().numpy()
 def unpack(self,a):
  n=self.n;b=a[:2*n]*np.sqrt(RESERVOIR/sum(a[:2*n]**2));mt=b[:n]**2;mf=b[n:]**2;mass=mt+mf
  return np.r_[mass,a[2*n:],2/np.pi*np.arctan2(b[:n],b[n:])]
 def cap_amplitude(self,a):return self.cap(self.unpack(a))
 def areport(self,a):
  n=self.n;v=self.unpack(a);r=self.report(np.r_[np.log(v[:n]),v[n:]]);E,g=self.afg(a);b=a[:2*n];mu=g[:2*n]/(2*np.maximum(b,1e-30));occupied=b*b>1e-7;proj=mu.copy();proj[(~occupied)&(mu>0)]=0
  pg=g.copy();x=a[2*n:];pg[2*n:][((x<1e-8)&(g[2*n:]>0))|((x>1-1e-8)&(g[2*n:]<0))]=0
  r.update(amplitude=a.tolist(),density_KKT_max=float(max(abs(proj))),amplitude_projected_gradient=float(max(abs(pg))),mass_constraint_error=float(abs(sum(v[:n])-RESERVOIR)),cap_slack_min=float(min(self.cap(v))),energy=E)
  return r

def solve(m,a,path,maxiter=100):
 n=m.n;path=Path(path);a[:2*n]*=np.sqrt(RESERVOIR/sum(a[:2*n]**2));trace=[]
 for it in range(maxiter):
  r=m.areport(a);E,g=m.afg(a)
  if r['density_KKT_max']<1e-6 and r['amplitude_projected_gradient']<1e-8:break
  im=np.where((a[:2*n]>1e-8)|(g[:2*n]<0))[0];ix=np.where(((a[2*n:]>1e-10)|(g[2*n:]<0))&((a[2*n:]<1-1e-10)|(g[2*n:]>0)))[0]+2*n
  P=np.zeros((3*n,len(im)-1));P[im]=null_space(a[im][None,:]);Z=np.c_[P,np.eye(3*n)[:,ix]]
  H=torch.autograd.functional.hessian(m.amplitude_energy,T(a)).detach().numpy();hh=Z.T@H@Z;gg=Z.T@g
  scale=1/np.sqrt(np.maximum(abs(np.diag(hh)),1e-8));hs=scale[:,None]*hh*scale[None,:];mine=float(np.linalg.eigvalsh(hs)[0]);shift=max(0,-mine+.02)
  d=-Z@(scale*np.linalg.solve(hs+shift*np.eye(len(gg)),scale*gg))
  d[:2*n][(a[:2*n]<=1e-8)&(d[:2*n]<0)]=0;d[2*n:][(a[2*n:]<=1e-8)&(d[2*n:]<0)]=0;d[2*n:][(a[2*n:]>=1-1e-8)&(d[2*n:]>0)]=0
  alpha=1.;neg=d<0;pos=(d>0)&(np.arange(3*n)>=2*n)
  if any(neg):alpha=min(alpha,.95*min(a[neg]/(-d[neg])))
  if any(pos):alpha=min(alpha,.95*min((1-a[pos])/d[pos]))
  accepted=False
  for k in range(40):
   aa=a+alpha*d;aa[:2*n]*=np.sqrt(RESERVOIR/sum(aa[:2*n]**2))
   if min(m.cap_amplitude(aa))>0 and m.afg(aa)[0]<=E+1e-4*alpha*g@d+1e-14:accepted=True;break
   alpha*=.5
  trace.append(dict(iteration=it,minimum_scaled_H=mine,shift=shift,alpha=float(alpha),accepted=accepted,KKT=r['density_KKT_max'],gradient=r['amplitude_projected_gradient'],energy=E))
  if not accepted or alpha<1e-13:break
  a=aa;r=m.areport(a);r.update(trace=trace,status='checkpoint');path.write_text(json.dumps(r,indent=2)+'\n')
 r=m.areport(a);r.update(trace=trace,optimizer=dict(success=bool(r['density_KKT_max']<1e-5 and r['amplitude_projected_gradient']<1e-7),iterations=len(trace),message='Constrained species-amplitude Newton with physical species KKT'))
 path.write_text(json.dumps(r,indent=2)+'\n');return r

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--scale',type=float,default=2.);ap.add_argument('--delta',type=float,default=0.);ap.add_argument('--h',type=float,default=.5);ap.add_argument('--source');ap.add_argument('--strength',type=float,default=1.);a=ap.parse_args();dest=Path(a.output)
 source=a.source or f'physical_completion_2026_10_25/run_purification_{a.scale}/results.json';old=json.loads(Path(source).read_text());old=old['runs'][-1] if 'runs' in old else old
 m=Species(scale=a.scale,delta=a.delta,h=a.h,center=old['scaled_boundary_kpc'],strength=a.strength);v=transfer(m,old);q=np.sin(np.pi*v[2*m.n:]/2)**2
 amp=np.r_[np.sqrt(v[:m.n]*q),np.sqrt(v[:m.n]*(1-q)),v[m.n:2*m.n]];amp[:2*m.n]=np.maximum(amp[:2*m.n],1e-10)
 # Orthogonal implementation and directional derivative checks at an interior state.
 vv=v.copy();vv[m.n:]=.05+.9*vv[m.n:];qq=np.sin(np.pi*vv[2*m.n:]/2)**2;aa=np.r_[np.sqrt(vv[:m.n]*qq),np.sqrt(vv[:m.n]*(1-qq)),vv[m.n:2*m.n]]
 equivalence=abs(m.afg(aa)[0]-m.fg(np.r_[np.log(vv[:m.n]),vv[m.n:]])[0]);assert equivalence<1e-11
 d=.01*np.sin(np.arange(3*m.n)+.7);E,g=m.afg(aa);errs=[]
 for dt in [1e-6,3e-7]:
  fd=(m.afg(aa+dt*d)[0]-m.afg(aa-dt*d)[0])/(2*dt);errs.append(float(abs(fd-g@d)/max(1,abs(fd))))
 assert max(errs)<1e-7
 r=solve(m,amp,dest.with_name('equilibrium.json'),maxiter=100);out={'runs':[r],'energy_equivalence_error':equivalence,'gradient_errors':errs,'source':source,'non_claim':'Effective static constitutive test, not microscopic derivation or physical formation'};dest.write_text(json.dumps(out,indent=2)+'\n')
 print({k:r.get(k) for k in ['physical_scale','stress_ratio_T_to_F','stress_strength','n','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','amplitude_projected_gradient','free_exterior_T_fraction','edge_mass_fraction','optimizer']},flush=True)
