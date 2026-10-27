import argparse,json
from pathlib import Path
import numpy as np
from fine_material import FineMaterial
from momentum import Momentum
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();s=np.load('nonlinear_cascade_2026_10_25/run_fine_infall/state.npz');a=s['a'];x=s['alpha'];p=s['carrier_p'];chi=s['chi'];pi=s['pi'];rows=[]
for method in [FineMaterial,Momentum]:
 m=method(material_h_kpc=.125,wave_R_kpc=10000.);E0=m.full_energy(a,x,p,chi,pi)
 for h in [3e-7,1e-6,1e-5,.0001,.001]:
  an,xn,pn,cn,vn,sink,qs,info=m.full_step(a,x,p,chi,pi,h/m.tdyn);E1=m.full_energy(an,xn,pn,cn,vn);rows.append({'method':method.__name__,'step_Myr':h,'energy_defect':E1+sink-E0,'mass_error':float(abs(np.sum(abs(an)**2)-np.sum(abs(a)**2))),'carrier_residual':info['carrier_root_residual'],'joint_residual':info['fixed_point_error'],'carrier_energy':float(.5*np.sum(pn*pn/m.Z(an)))})
out={'rows':rows,'scope':'Same Hamiltonian and midpoint equations at identical stalled fine-grid state; direct momentum removes subtract-angle/divide-step cancellation. No physical damping or energy projection.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
