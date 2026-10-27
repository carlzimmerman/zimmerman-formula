import argparse,json,time
from pathlib import Path
import numpy as np
from original_collocated import Collocated,FourthOrder
from live_collocated import FourthOrder as Previous
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[]
m=FourthOrder(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
for mode in ['initial','late']:
 if mode=='initial':a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n)
 else:
  state=np.load('infall_pump_2026_10_25/run_time_half/state.npz');a,x,p,c,v=[state[k] for k in ['a','alpha','carrier_p','chi','pi']];rho=abs(a[0])**2/m.vol;a[0]*=np.exp(1j*(m.g+2*m.g2*rho)*m.true_chi_m(c)/m.sigma)
 E0=m.full_energy(a,x,p,c,v);Q0=m.charge(a,v);M0=np.sum(abs(a)**2)
 for h in ([.00001,.01] if mode=='initial' else [.005,.02]):
  start=time.monotonic();r=m.full_step(a,x,p,c,v,h/m.tdyn);aa,xx,pp,cc,vv,ds,dq,info=r;E=m.full_energy(aa,xx,pp,cc,vv);row={'mode':mode,'h_Myr':h,'seconds':time.monotonic()-start,'energy_defect':E+ds-E0,'mass_defect':float(np.sum(abs(aa)**2)-M0),'charge_defect':m.charge(aa,vv)+dq-Q0,**{k:v for k,v in info.items() if not k.startswith('source_')}}
  if mode=='initial' and h==.00001:
   old=Previous(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rr=old.full_step(a,x,p,c,v,h/old.tdyn);olda=rr[0].copy();oldrho=abs(olda[0])**2/m.vol;olda[0]*=np.exp(1j*(m.g+2*m.g2*oldrho)*old.true_chi_m(rr[3])/m.sigma);row['physical_amplitude_difference_from_old']=float(np.max(abs(aa-olda)));row['old_energy']=old.full_energy(rr[0],rr[1],rr[2],rr[3],rr[4]);row['new_energy']=E
  rows.append(row);print(row,flush=True)
Path(args.output).write_text(json.dumps({'cases':rows,'interpretation':'Same continuous action, different consistent discretization. Small-step agreement is necessary; full force audit and time refinement remain required.'},indent=2)+'\n')
