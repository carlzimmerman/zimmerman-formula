import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from free_formation import FreeVacuum
from fast_projected import finish
from joint import RESERVOIR
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=FreeVacuum();n=m.n;old=json.loads(Path('physical_completion_2026_10_25/run_free_continue/formed.json').read_text());start=np.r_[np.log(old['mass']),old['v'][n:]];trace=[];count=[0];reject=[0]
def actual(z):
 mass=np.exp(z[:n]-max(z[:n]));mass*=RESERVOIR/sum(mass);return np.r_[mass,z[n:]]
def fg(z):
 v=actual(z)
 if min(m.cap(v))<=1e-8:
  reject[0]+=1;return 1e100,np.zeros_like(z)
 return m.fg(z)
def cb(z):
 count[0]+=1;E,g=m.fg(z);cap=min(m.cap(actual(z)));assert cap>0;trace.append({'iteration':count[0],'energy':E,'cap':float(cap),'gradient':float(max(abs(g)))})
 if count[0]%100==0:
  r=m.report(z);r['iterations']=count[0];dest.with_name('lbfgs_checkpoint.json').write_text(json.dumps(r,indent=2)+'\n')
op=minimize(fg,start,jac=True,method='L-BFGS-B',bounds=[(-60,30)]*n+[(0,1)]*n,callback=cb,options=dict(maxiter=8000,maxls=100,maxcor=30,ftol=1e-15,gtol=1e-10));r=m.report(op.x);r.update(optimizer={'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)},trace=trace,rejected_infeasible_evaluations=reject[0]);dest.with_name('lbfgs.json').write_text(json.dumps(r,indent=2)+'\n');out={'lbfgs':r};dest.write_text(json.dumps(out,indent=2)+'\n');print('LBFGS',{k:r.get(k) for k in ['energy','gradient_max','scaled_law_error_bound_percent','scaled_boundary_kpc','optimizer']},flush=True)
if min(m.cap(actual(op.x)))>0:
 final=finish(m,actual(op.x),dest.with_name('final.json'),initial_iterations=0,newton_iterations=100);out['final']=final;out['released_energy_Eunit']=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text())['energy']-final['energy'];dest.write_text(json.dumps(out,indent=2)+'\n');print('FINAL',{k:final.get(k) for k in ['energy','density_KKT_max','gradient_max','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
