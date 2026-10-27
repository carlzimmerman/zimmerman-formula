import argparse,json
from pathlib import Path
import numpy as np
from fine_cc import FineCC
from elliptic_precondition import EllipticPreconditioned
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[];states=[]
for cls in [FineCC,EllipticPreconditioned]:
 m=cls(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,c,pi,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n);E0=m.full_energy(a,x,p,c,pi);an,xn,pn,cn,vn,sink,qs,info=m.full_step(a,x,p,c,pi,.0025/m.tdyn);states.append(an);rows.append({'method':cls.__name__,'residual_evaluations':info['residual_evaluations'],'Newton_iterations':info['iterations'],'runtime_seconds':info['root_runtime_seconds'],'root_residual':info['fixed_point_error'],'energy_defect':m.full_energy(an,xn,pn,cn,vn)+sink-E0})
out={'checks':rows,'state_difference':float(np.max(abs(states[0]-states[1]))),'scope':'Same forces and root tolerance; diagonal1+eta preconditions Newton linear solve only. A runtime result is solver evidence, not new physical damping or formation.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
