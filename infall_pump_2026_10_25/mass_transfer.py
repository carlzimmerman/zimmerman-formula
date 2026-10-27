"""Locate the law deficit and distinguish mass flux from phase-front motion."""
import argparse,json
from pathlib import Path
import numpy as np
from live_collocated import Collocated
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rows=[]
initial_dd=None
for name in ['initial_dilated','run_components_time','run_infall']:
 if name=='initial_dilated':a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');p=np.zeros(m.n);time=0.
 else:
  root=Path('infall_pump_2026_10_25')/name;s=np.load(root/'state.npz');a,x,p,c,v=[s[k] for k in ['a','alpha','carrier_p','chi','pi']];time=json.loads((root/'results.json').read_text())['completed_time_Myr']
 mass=np.sum(abs(a)**2,axis=0);rho=mass/m.vol;q=abs(a[0])**2/mass;U=m.geometry(a,c)[3];psi=a/np.sqrt(m.vol);jt=m.k/m.sigma*m.w*np.imag(np.conj(psi[0,:-1])*U*psi[0,1:]);jf=m.k/m.sigma*m.w*np.imag(np.conj(psi[1,:-1])*psi[1,1:]);j=jt+jf;md=np.r_[-j[0],j[:-1]-j[1:],j[-1]];Md=(np.cumsum(md)-.5*md)/m.tdyn
 rr=m.r*m.rm;gt=m.gb+m.enclosed(mass);law=(m.gb+np.sqrt(m.gb*m.gb+4*m.gb))/2;target=(law-m.gb)*m.r**2;actual=m.enclosed(mass)*m.r**2;deficit=target-actual;errors=law/gt-1;sel=(rr>=1.5)&(rr<=50);ii=np.flatnonzero(sel)[np.argmax(errors[sel])]
 if name=='initial_dilated':
  mu=m.pot(a,x,True)[1];extra=m.transfer(a,x,c)[0];mu[0]+=extra
  def H(aa):
   hh=(m.kd+mu)*aa+m.J*m.alignment(aa,x,c);hh[0,:-1]+=m.ko*U*aa[0,1:];hh[0,1:]+=m.ko*np.conj(U)*aa[0,:-1];hh[1,:-1]+=m.ko*aa[1,1:];hh[1,1:]+=m.ko*aa[1,:-1];return hh
  ad=-1j*H(a)/m.sigma;add=-1j*H(ad)/m.sigma;massdd=np.sum(2*abs(ad)**2+2*np.real(np.conj(a)*add),axis=0);initial_dd=(np.cumsum(massdd)-.5*massdd)/m.tdyn**2
 samples=[]
 for R in [1.5,3,10,30,50]:
  dm=float(np.interp(R,rr,deficit));rate=float(np.interp(R,rr,Md));acc=float(np.interp(R,rr,initial_dd));samples.append({'radius_kpc':R,'required_enclosed_mass_increase_Mb':dm,'actual_enclosed_mass_inflow_Mb_Myr':rate,'initial_enclosed_mass_acceleration_Mb_Myr2':acc,'initial_acceleration_characteristic_Myr':float(np.sqrt(2*dm/acc)) if dm>0 and acc>0 else None})
 rows.append({'case':name,'time_Myr':time,'worst_sampled_law_deficit_radius_kpc':float(rr[ii]),'samples':samples})
Path(args.output).write_text(json.dumps({'cases':rows,'meaning':'Conversion cancels from total-mass continuity exactly. Characteristic times extrapolate only initial acceleration; they are neither a nonlinear forecast nor a rigorous lower bound. The observational test includes the50kpc endpoint even when it lies between cells.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
