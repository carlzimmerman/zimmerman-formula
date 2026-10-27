"""Late actual-state root, energy and charge checks for a phase-exact frame."""
import argparse,json,time
from pathlib import Path
import numpy as np
from rotating_collocated import RotatingFourth
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=RotatingFourth(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);s=np.load('infall_pump_2026_10_25/run_quiet_long_time/state.npz');a,x,p,c,v=[s[k] for k in ['a','alpha','carrier_p','chi','pi']];E0=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);M0=np.sum(abs(a)**2);rows=[]
for h in [.02,.005,.00125]:
 start=time.monotonic();r=m.full_step(a,x,p,c,v,h/m.tdyn);aa,xx,pp,cc,vv,ds,dq,info=r;row={'h_Myr':h,'seconds':time.monotonic()-start,'energy_defect':m.full_energy(aa,xx,pp,cc,vv)+ds-E0,'mass_defect':float(np.sum(abs(aa)**2)-M0),'charge_defect':m.charge(aa,vv)+dq-Q0,**{k:z for k,z in info.items() if not k.startswith('source_')}};rows.append(row);print(row,flush=True)
Path(args.output).write_text(json.dumps({'cases':rows,'scope':'Same continuous action; one frequency frozen across all3 symmetric composition stages. Actual physical endpoint arrays, no parent population or physical force added. Convergence against ordinary small steps still required.'},indent=2)+'\n')
