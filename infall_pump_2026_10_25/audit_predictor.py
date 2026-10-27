"""Compare exact-root trajectories; a predictor must not change the equations."""
import argparse,json,time
from pathlib import Path
import numpy as np
from predicted_phi_collocated import FourthOrder as Predicted
from autodiff_phi_collocated import FourthOrder as Plain
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[];states=[]
for cls in [Plain,Predicted]:
 m=cls(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);s=np.load('infall_pump_2026_10_25/run_components_time/state.npz');a,x,p,c,v=[s[k].copy() for k in ['a','alpha','carrier_p','chi','pi']];E0=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);sink=qs=0.;trace=[];start=time.monotonic()
 for j in range(20):
  tic=time.monotonic();an,xn,pn,cn,vn,ds,dq,info=m.full_step(a,x,p,c,v,.0025/m.tdyn);trace.append({'step':j,'seconds':time.monotonic()-tic,'iterations':info['iterations'],'residual':info['fixed_point_error']})
  if info['fixed_point_error']>1e-9 or info.get('substep_failed',False):break
  a,x,p,c,v=an,xn,pn,cn,vn;sink+=ds;qs+=dq
 states.append([a,x,p,c,v]);rows.append({'method':cls.__module__,'runtime_seconds':time.monotonic()-start,'energy_defect':m.full_energy(a,x,p,c,v)+sink-E0,'charge_defect':m.charge(a,v)+qs-Q0,'trace':trace})
out={'cases':rows,'endpoint_max_differences':[float(np.max(abs(x-y))) for x,y in zip(*states)],'interpretation':'Only Newton initial guesses change; every accepted substep solves the same full equations.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
