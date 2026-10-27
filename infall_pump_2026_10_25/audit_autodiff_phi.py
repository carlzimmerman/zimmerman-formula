import argparse,json,time
from pathlib import Path
import numpy as np
from autodiff_phi_collocated import FourthOrder
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
m=FourthOrder(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
s=np.load('infall_pump_2026_10_25/run_time_half/state.npz');a,x,p,c,v=[s[k] for k in ['a','alpha','carrier_p','chi','pi']]
E0=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);M0=np.sum(abs(a)**2);rows=[]
for h in [.005,.0025]:
 start=time.monotonic();r=m.full_step(a,x,p,c,v,h/m.tdyn);aa,xx,pp,cc,vv,ds,dq,info=r;E=m.full_energy(aa,xx,pp,cc,vv)
 row={'h_Myr':h,'seconds':time.monotonic()-start,'energy_defect':E+ds-E0,'mass_defect':float(np.sum(abs(aa)**2)-M0),'charge_defect':m.charge(aa,vv)+dq-Q0,**{k:v for k,v in info.items() if not k.startswith('source_')}};rows.append(row);print(row,flush=True)
Path(args.output).write_text(json.dumps({'input_time_Myr':4.816249999999945,'cases':rows},indent=2)+'\n')
