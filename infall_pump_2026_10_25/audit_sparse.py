import argparse,json,time
from pathlib import Path
import numpy as np
from sparse_midpoint import SparseMidpoint
from fine_cc import FineCC
from fine_initial import fine_initial

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
config=dict(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
m=SparseMidpoint(**config);m.audit_jacobian=True
a,x,chi,pi,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n)
E0=m.full_energy(a,x,p,chi,pi);M0=np.sum(abs(a)**2);Q0=m.charge(a,pi)
out=[]
for h in [.00001,.0025,.02]:
 start=time.monotonic();r=m.full_step(a,x,p,chi,pi,h/m.tdyn);an,xn,pn,cn,pin,ds,dq,info=r
 E=m.full_energy(an,xn,pn,cn,pin)
 row={'h_Myr':h,'seconds':time.monotonic()-start,'energy_defect':E+ds-E0,'mass_defect':float(np.sum(abs(an)**2)-M0),'charge_defect':m.charge(an,pin)+dq-Q0,**{k:v for k,v in info.items() if not k.startswith('source_')}}
 if h==.00001:
  old=FineCC(**config);rr=old.full_step(a,x,p,chi,pi,h/old.tdyn)
  row['old_root_residual']=rr[-1]['fixed_point_error'];row['old_state_max_differences']=[float(np.max(abs(v-w))) for v,w in zip(r[:5],rr[:5])]
 out.append(row);print(row,flush=True)
Path(args.output).write_text(json.dumps({'config':config,'initial':meta,'cases':out},indent=2)+'\n')
