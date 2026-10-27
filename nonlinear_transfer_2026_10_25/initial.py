"""Actual initial data, not a prescribed subsequent density history."""
import json
from pathlib import Path
import numpy as np,torch
from live import Live

def initial(m,case):
 p=Path('physical_completion_2026_10_25/run_free_formation/all_F.json' if case=='allF_seed' else 'physical_completion_2026_10_25/run_free_finish/formed.json');data=json.loads(p.read_text());mass=np.array(data['mass']);chi=np.zeros(len(m.wr));pi=chi.copy()
 if case=='allF_seed':
  x=torch.zeros(m.n,dtype=torch.float64,requires_grad=True);z=torch.tensor(np.log(mass),dtype=torch.float64);H=torch.autograd.functional.hessian(lambda x:m.m.energy(z,x),x).detach().numpy();sv=np.sqrt(m.vol);ev,vec=np.linalg.eigh(H/(sv[:,None]*sv[None,:]));seed=np.abs(vec[:,0]/sv);seed*=.02/max(seed);theta=np.pi*seed/2;a=np.array([np.sqrt(mass)*np.sin(theta),np.sqrt(mass)*np.cos(theta)],dtype=complex);alpha=theta;meta={'seed_original_locked_phase_eigenvalue':float(ev[0]),'seed_max_original_phase':.02}
 else:
  qt=np.array(data['q']);mt=mass*qt;mf=mass-mt
  if case=='dilated':
   rr=m.edges*m.rm;shifted=m.edges*(1+.2*np.exp(-(rr/200)**4));assert min(np.diff(shifted))>0
   mt=np.diff(np.interp(m.edges,shifted,np.r_[0,np.cumsum(mt)]));mf=np.diff(np.interp(m.edges,shifted,np.r_[0,np.cumsum(mf)]))
  a=np.array([np.sqrt(np.maximum(mt,0)),np.sqrt(np.maximum(mf,0))],dtype=complex);alpha=np.arctan2(abs(a[0]),abs(a[1]));meta={'core_radius_dilation':1.2 if case=='dilated' else 1.,'outer_grid_unchanged':True}
 alpha,res,it=m.minimize_alpha(a,chi,alpha,maxit=300);meta.update(initial_alpha_residual=res,initial_alpha_iterations=it)
 return a,alpha,chi,pi,meta
