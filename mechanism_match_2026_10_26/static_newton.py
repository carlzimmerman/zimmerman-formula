"""Force-based Newton refinement, independently using Torch inherited energy."""
import argparse,json,sys,time
from pathlib import Path
import numpy as np,torch
from matched import Matched
sys.path.insert(0,'nonlinear_transfer_2026_10_25')
from exact_equilibrium import Exact
from three_field_solver import finish
from joint import T,RESERVOIR
torch.set_num_threads(1)

class ParentStatic(Exact):
 def __init__(self,length):
  super().__init__(J=30)
  self.obj=Matched(length_kpc=length);m=self.obj.m;assert self.n==m.n
  L2=(m.c/self.obj.M)**2
  B=np.diag(np.r_[m.w[0],m.w[:-1]+m.w[1:],m.w[-1]])-np.diag(m.w,1)-np.diag(m.w,-1)
  self.chol=torch.linalg.cholesky(T(np.diag(m.vol)+L2*B))
  self.weights=T(m.w);self.L2=L2;self.track=self.obj.M**2*self.obj.lam**2
 def energy(self,z,p):
  E=super().energy(z,p);mass=RESERVOIR*torch.softmax(z,dim=0)
  rho=mass*torch.sin(torch.pi*p[self.n:]/2)**2/self.vol
  t=torch.cholesky_solve((self.vol*rho)[:,None],self.chol)[:,0]
  return E+.5*self.track*(self.L2*torch.sum(self.weights*torch.diff(t)**2)+torch.sum(self.vol*(t-rho)**2))

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();dest=Path(args.output);rows=[];start=time.monotonic()
prior=np.load('mechanism_match_2026_10_26/run_static/states.npz')
for length in [.00001,.0001,.001]:
 model=ParentStatic(length);obj=model.obj;m=obj.m
 if length==.001:a=prior['a_0.001'];x=prior['carrier_0.001']
 else:a=obj.reference['a'];x=obj.reference['alpha']
 mass=np.sum(abs(a)**2,axis=0);theta=np.arctan2(abs(a[0]),abs(a[1]));v=np.r_[mass,x*2/np.pi,theta*2/np.pi]
 E_torch=float(model.energy(T(np.log(mass)),T(v[m.n:])));E_numpy=obj.energy(obj.static(a,x));assert abs(E_torch-E_numpy)<1e-10
 r=finish(model,v,dest.with_name(f'newton_{length}.json'),initial_iterations=0,newton_iterations=20)
 mass=np.array(r['mass']);x=np.array(r['v'][m.n:2*m.n])*np.pi/2;theta=np.array(r['v'][2*m.n:])*np.pi/2
 aa=np.sqrt(mass)[None,:]*np.array([np.sin(theta),np.cos(theta)]);aa=aa.astype(complex)
 diag=m.diagnostics(aa,x,np.zeros(len(m.wr)),np.zeros(len(m.wr)))
 row={k:r.get(k) for k in ['energy','density_KKT_max','gradient_max','optimizer','cap_slack_min','mass_constraint_error']}
 row.update(length_kpc=length,energy_implementation_difference=E_torch-E_numpy,diagnostics=diag)
 rows.append(row);np.savez_compressed(dest.with_name(f'state_{length}.npz'),a=aa,alpha=x,s=obj.relaxed_s(aa))
 dest.write_text(json.dumps({'rows':rows,'wall_seconds':time.monotonic()-start,'status':'partial' if length!=.001 else 'completed',
 'non_claim':'Finite-grid static stationary points; not formation, continuum convergence or global minimum.'},indent=2)+'\n')
 print(row,flush=True)
