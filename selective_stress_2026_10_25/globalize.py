"""Species amplitude minimization globalizes the new constitutive model."""
import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.optimize import minimize
from species import Species,solve
from joint import T,RESERVOIR

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--source',default='selective_stress_2026_10_25/run_species_high/results.json');ap.add_argument('--strength',type=float,default=1.);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path(a.source).read_text());old=old['runs'][-1] if 'runs' in old else old
m=Species(scale=old['physical_scale'],delta=0.,h=old['scaled_spacing_kpc'],center=sum(old['fine_band_scaled_kpc'])/2,strength=a.strength)
assert len(old['mass'])==m.n
amp=np.array(old['amplitude']);n=m.n;count=[0];best=[np.inf,None]
def fg(aa):
 aa=T(aa).requires_grad_(True);E=m.amplitude_energy(aa);b=aa[:2*n]*torch.sqrt(RESERVOIR/torch.sum(aa[:2*n]**2));u=m.A@(b[:n]**2);E=E+1e5*torch.sum(torch.relu(u-.9995)**2);g=torch.autograd.grad(E,aa)[0]
 return float(E.detach()),g.detach().numpy()
def cb(aa):
 count[0]+=1
 if count[0]%200==0:
  r=m.areport(aa);r['lbfgs_iterations']=count[0];dest.with_name('lbfgs_checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
op=minimize(fg,amp,jac=True,method='L-BFGS-B',bounds=[(1e-12,None)]*(2*n)+[(0,1)]*n,callback=cb,options=dict(maxiter=12000,maxls=50,maxcor=40,ftol=1e-15,gtol=1e-9))
r=m.areport(op.x);r['lbfgs']={'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)};dest.with_name('lbfgs_end.json').write_text(json.dumps(r,indent=2)+'\n')
assert min(m.cap_amplitude(op.x))>0
r=solve(m,op.x,dest.with_name('equilibrium.json'),maxiter=100);r['lbfgs']={'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)}
dest.write_text(json.dumps({'runs':[r],'source':a.source},indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','n','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','amplitude_projected_gradient','free_exterior_T_fraction','optimizer','lbfgs']},flush=True)
