import argparse,json,time
from pathlib import Path
import numpy as np
from krylov_checked import Krylov
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();s=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');out={'runs':[]}
for eta in [0.,.01,1.]:
 m=Krylov(eta=eta);a=s['a'].copy();x=s['alpha'].copy();chi=np.zeros(len(m.wr));pi=chi.copy();p=np.zeros(m.n);E0=m.full_energy(a,x,p,chi,pi);Q0=m.charge(a,pi);M0=float(sum(np.sum(abs(a)**2,axis=0)));dt=.001/m.tdyn;an,xn,pn,cn,vn,ds,qs,info=m.full_step(a,x,p,chi,pi,dt);ans={'eta':eta,'calibration':m.calibration,'dt_Myr':.001,'energy_error':float(m.full_energy(an,xn,pn,cn,vn)+ds-E0),'charge_error':float(m.charge(an,vn)+qs-Q0),'mass_error':float(np.sum(abs(an)**2)-M0),**{k:v for k,v in info.items() if not k.startswith('source_')}};out['runs'].append(ans);Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(ans,flush=True)
