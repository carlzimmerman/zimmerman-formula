"""Resolve the stalled derived-entropy state with a changed globalizer."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from thermal_branch_checked import Thermal
from three_field_solver import finish
from joint import RESERVOIR
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('selective_stress_2026_10_25/run_thermal_branch_checked/results.json').read_text())['runs'][-1];m=Thermal(scale=old['physical_scale'],K=old['K']);n=m.n;z=np.array(old['v']);trace=[]
def actual(z):
 mass=np.exp(z[:n]-max(z[:n]));mass*=RESERVOIR/sum(mass);return np.r_[mass,z[n:]]
def fg(z):
 if min(m.cap(actual(z)))<=1e-8:return 1e100,np.zeros_like(z)
 return m.fg(z)
def cb(z):
 trace.append(m.fg(z)[0])
 if len(trace)%200==0:dest.with_name('lbfgs_checkpoint.json').write_text(json.dumps(m.report(z),indent=2)+'\n')
op=minimize(fg,z,jac=True,method='L-BFGS-B',bounds=[(-60,30)]*n+[(0,1)]*(2*n),callback=cb,options=dict(maxiter=10000,maxls=100,maxcor=30,ftol=1e-15,gtol=1e-10));r=m.report(op.x);dest.with_name('lbfgs.json').write_text(json.dumps(r,indent=2)+'\n');r=finish(m,actual(op.x),dest.with_name('final.json'),initial_iterations=0,newton_iterations=120);out={'state':r,'energy_trace':trace,'lbfgs_optimizer':{'success':bool(op.success),'message':str(op.message),'iterations':int(op.nit)}};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['K','energy','density_KKT_max','gradient_max','maximum_fractional_law_error_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
