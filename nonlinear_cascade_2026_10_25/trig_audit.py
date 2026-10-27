import argparse,json
from pathlib import Path
import numpy as np
from fine_material import FineMaterial
from trig_dg import TrigDG
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();s=np.load('nonlinear_cascade_2026_10_25/run_fine_birth/state.npz');a=s['a'];x=s['alpha'];p=s['carrier_p'];chi=s['chi'];pi=s['pi'];rows=[];m=TrigDG(material_h_kpc=.125,wave_R_kpc=10000.);parts=m.vacuum_parts(a,chi);delta=.3*np.sin(m.r);m.endpoint0=x;G=m.carrier_force(x+delta/2,parts)[0];err=m.alpha_energy(x+delta,parts)-m.alpha_energy(x,parts)-G@delta;m.endpoint0=None;assert abs(err)<1e-10
for method in [FineMaterial,TrigDG]:
 m=method(material_h_kpc=.125,wave_R_kpc=10000.);E0=m.full_energy(a,x,p,chi,pi)
 for h in [1e-6,.0001,.001,.0025]:
  an,xn,pn,cn,vn,sink,qs,info=m.full_step(a,x,p,chi,pi,h/m.tdyn);rows.append({'method':method.__name__,'h_Myr':h,'energy_defect':float(m.full_energy(an,xn,pn,cn,vn)+sink-E0),'carrier_residual':info['carrier_root_residual'],'joint_residual':info['fixed_point_error'],'mass_error':float(abs(np.sum(abs(an)**2)-np.sum(abs(a)**2)))})
out={'fixed_density_carrier_discrete_gradient_identity_error':float(err),'rows':rows,'scope':'Exact trigonometric potential divided difference at fixed midpoint material fields, tested in coupled model. Density-dependent inertia and material potential still midpoint approximations; no assertion of exact full energy conservation or spectral convergence.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
