import argparse,json,time
from pathlib import Path
import numpy as np
from warm_homotopy import WarmHomotopy
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=WarmHomotopy(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,c,pi,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n);E0=m.full_energy(a,x,p,c,pi);Q0=m.charge(a,pi);sink=qs=0.;rows=[];accepted=0
for k in range(10):
 an,xn,pn,cn,vn,ds,dq,info=m.full_step(a,x,p,c,pi,.0025/m.tdyn);rows.append({'step':k+1,'runtime_seconds':info['root_runtime_seconds'],'evaluations':info['residual_evaluations'],'root_residual':info['fixed_point_error'],'carrier_residual':info['carrier_root_residual'],'homotopy_stages':len(info['coupling_homotopy_stages'])})
 if info['fixed_point_error']>1e-9:
  rows[-1]['accepted']=False;break
 rows[-1]['accepted']=True;accepted+=1;a,x,p,c,pi=an,xn,pn,cn,vn;sink+=ds;qs+=dq
out={'checks':rows,'final_time_Myr':.0025*accepted,'energy_ledger_error':float(m.full_energy(a,x,p,c,pi)+sink-E0),'shift_charge_error':float(m.charge(a,pi)+qs-Q0),'mass':float(np.sum(abs(a)**2)),'scope':'Same complete refined CC step; coupling continuation and previous accepted root used only as nonlinear initial guesses. No changed physical coupling or timestep acceptance. Nonconverged trial ends test.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
