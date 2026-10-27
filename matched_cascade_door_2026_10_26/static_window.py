"""Continuation of the already converged .1pc static branch at .15 and .2pc."""
import argparse,json,sys,time
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,'mechanism_match_2026_10_26')
from matched import Matched
sys.path.insert(0,'nonlinear_transfer_2026_10_25')
from exact_equilibrium import Exact
from three_field_solver import finish
from joint import T,RESERVOIR
torch.set_num_threads(1)

class Static(Exact):
 def __init__(self,length_pc):
  super().__init__(J=30)
  self.obj=Matched(length_kpc=length_pc/1000);m=self.obj.m
  self.L2=(m.c/self.obj.M)**2
  B=np.diag(np.r_[m.w[0],m.w[:-1]+m.w[1:],m.w[-1]])-np.diag(m.w,1)-np.diag(m.w,-1)
  self.chol=torch.linalg.cholesky(T(np.diag(m.vol)+self.L2*B))
  self.weights=T(m.w);self.track=self.obj.M**2*self.obj.lam**2
 def energy(self,z,p):
  E=super().energy(z,p);mass=RESERVOIR*torch.softmax(z,dim=0)
  rho=mass*torch.sin(torch.pi*p[self.n:]/2)**2/self.vol
  t=torch.cholesky_solve((self.vol*rho)[:,None],self.chol)[:,0]
  return E+.5*self.track*(self.L2*torch.sum(self.weights*torch.diff(t)**2)+torch.sum(self.vol*(t-rho)**2))

def run(output):
 dest=Path(output);s=np.load('mechanism_match_2026_10_26/run_newton/state_0.0001.npz');a=s['a'];x=s['alpha'];rows=[];start=time.monotonic()
 for length in [.15,.2]:
  model=Static(length);obj=model.obj;m=obj.m
  mass=np.sum(abs(a)**2,axis=0);theta=np.arctan2(abs(a[0]),abs(a[1]));v=np.r_[mass,x*2/np.pi,theta*2/np.pi]
  et=float(model.energy(T(np.log(mass)),T(v[m.n:])));en=obj.energy(obj.static(a,x));assert abs(et-en)<1e-10
  r=finish(model,v,dest.with_name(f'newton_{length}.json'),initial_iterations=0,newton_iterations=20)
  mass=np.array(r['mass']);x=np.array(r['v'][m.n:2*m.n])*np.pi/2;theta=np.array(r['v'][2*m.n:])*np.pi/2
  a=(np.sqrt(mass)[None,:]*np.array([np.sin(theta),np.cos(theta)])).astype(complex)
  diag=m.diagnostics(a,x,np.zeros(len(m.wr)),np.zeros(len(m.wr)))
  row={k:r.get(k) for k in ['energy','density_KKT_max','gradient_max','cap_slack_min','mass_constraint_error']}
  row.update(length_pc=length,energy_implementation_difference=et-en,diagnostics=diag)
  i=int(np.argmin(abs(m.r*m.rm-3)));rho=abs(a[0,i])**2/m.vol[i];u=m.enclosed(abs(a[0])**2)[i]
  row['local_patch']={'radius_kpc':float(m.r[i]*m.rm),'rho':float(rho),'u':float(u)}
  rows.append(row);np.savez_compressed(dest.with_name(f'state_{length}.npz'),a=a,alpha=x,s=obj.relaxed_s(a),radius_kpc=m.r*m.rm,vol=m.vol)
  dest.write_text(json.dumps({'rows':rows,'runtime_seconds':time.monotonic()-start,'scope':'Finite-grid static continuation; no formation or continuum certificate.'},indent=2)+'\n');print(row,flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);run(ap.parse_args().output)
