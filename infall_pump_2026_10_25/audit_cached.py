import argparse,json,time
from pathlib import Path
import numpy as np
from cached_collocated import Collocated,FourthOrder
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
rows=[]
for cls,h,steps in [(Collocated,.0025,12),(FourthOrder,.02,6)]:
 m=cls(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n)
 E0=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);M0=np.sum(abs(a)**2);sink=qs=0.;case=[];t=0
 for i in range(steps):
  start=time.monotonic();r=m.full_step(a,x,p,c,v,h/m.tdyn);an,xn,pn,cn,vn,ds,dq,info=r
  E=m.full_energy(an,xn,pn,cn,vn);row={'step':i,'h_Myr':h,'seconds':time.monotonic()-start,'energy_defect':float(E+sink+ds-E0),'mass_defect':float(np.sum(abs(an)**2)-M0),'charge_defect':m.charge(an,vn)+qs+dq-Q0,**{k:v for k,v in info.items() if not k.startswith('source_')}};case.append(row);print(cls.__name__,row,flush=True)
  if info['fixed_point_error']>1e-9:break
  a,x,p,c,v=an,xn,pn,cn,vn;sink+=ds;qs+=dq;t+=h
 rows.append({'method':cls.__name__,'completed_time_Myr':t,'trace':case,'final':m.diagnostics(a,x,c,v)})
Path(args.output).write_text(json.dumps({'cases':rows},indent=2)+'\n')
