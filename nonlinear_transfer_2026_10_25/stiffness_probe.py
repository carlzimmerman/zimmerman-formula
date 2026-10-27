import argparse,json
from pathlib import Path
import numpy as np
from full import Full
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();m=Full();s=np.load('nonlinear_transfer_2026_10_25/run_adaptive_dilated/state.npz');a=s['a'];x=s['alpha'];p=s['carrier_p'];chi=s['chi'];pi=s['pi'];E0=m.full_energy(a,x,p,chi,pi);out={'trial_steps':[]}
for h in [.005/2**i for i in range(18)]:
 an,xn,pn,cn,vn,ds,dq,info=m.full_step(a,x,p,chi,pi,h/m.tdyn);E1=m.full_energy(an,xn,pn,cn,vn);out['trial_steps'].append({'h_Myr':h,'energy_defect':E1+ds-E0,**info})
Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
