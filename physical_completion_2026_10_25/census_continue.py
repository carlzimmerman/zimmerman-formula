import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from census_halo import CensusHalo
from variable_mass_solver import finish
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=CensusHalo();n=m.n;old=json.loads(Path('physical_completion_2026_10_25/run_census_halo/halo.json').read_text());z=np.r_[np.log(old['mass']),old['v'][n:]];trace=[]
def fg(z):
 mm=np.exp(z[:n]-max(z[:n]));mm*=m.total_mass/sum(mm)
 if min(m.cap(np.r_[mm,z[n:]]))<=1e-8:return 1e100,np.zeros_like(z)
 return m.fg(z)
def cb(z):
 if len(trace)%20==0:dest.with_name('checkpoint.json').write_text(json.dumps(m.report(z),indent=2)+'\n')
 trace.append(m.fg(z)[0])
op=minimize(fg,z,jac=True,method='L-BFGS-B',bounds=[(-60,30)]*n+[(0,1)]*n,callback=cb,options=dict(maxiter=3000,maxls=100,maxcor=30,ftol=1e-15,gtol=1e-10));r=m.report(op.x);dest.with_name('lbfgs.json').write_text(json.dumps(r,indent=2)+'\n');v=np.r_[r['mass'],r['v'][n:]];r=finish(m,v,dest.with_name('final.json'),initial_iterations=0,newton_iterations=200);out={'state':r,'lbfgs_optimizer':{'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)},'energy_trace':trace};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['energy','density_KKT_max','gradient_max','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_mass','free_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
