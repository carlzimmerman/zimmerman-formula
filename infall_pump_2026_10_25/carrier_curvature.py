"""Instantaneous finite-carrier curvature, not a complete coupled stability proof."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from live_collocated import Collocated
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Collocated(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);rows=[]
for name in ['initial_dilated','run_infall','run_time_half','run_rest_control']:
 if name=='initial_dilated':a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');time=0.
 else:
  root=Path('infall_pump_2026_10_25')/name;s=np.load(root/'state.npz');a,x,c,v=[s[k] for k in ['a','alpha','chi','pi']];time=json.loads((root/'results.json').read_text())['completed_time_Myr']
 parts=m.vacuum_parts(a,c);force,diag,off,scale=m.carrier_force(x,parts);Z=m.Z(a);d=diag/Z;e=off/np.sqrt(Z[1:]*Z[:-1]);vals,vecs=eigh_tridiagonal(d,e,select='i',select_range=(0,3),lapack_driver='stebz',tol=1e-7)
 modes=[]
 for lam,z in zip(vals,vecs.T):
  Az=d*z;Az[:-1]+=e*z[1:];Az[1:]+=e*z[:-1];weights=z*z
  modes.append({'lambda_dimensionless':float(lam),'omega_squared_Myr_inverse2':float(lam/m.tdyn**2),'growth_time_Myr_if_frozen_negative':float(m.tdyn/np.sqrt(-lam)) if lam<0 else None,'weighted_radius_kpc':float(weights@(m.r*m.rm)),'eigen_residual_scaled':float(np.linalg.norm(Az-lam*z)/max(np.linalg.norm(Az),abs(lam),1.))})
 rows.append({'case':name,'time_Myr':time,'minimum_four_carrier_modes':modes,'local_min_diagonal_curvature_Myr_inverse2':float(np.min(d)/m.tdyn**2),'max_alpha':float(np.max(x)),'min_alpha':float(np.min(x))})
Path(args.output).write_text(json.dumps({'cases':rows,'scope':'Carrier displacement Hessian at frozen actual material/scalar state, with finite Z and spatial stiffness. A negative value is an instantaneous saddle in this subspace; it is not a full nonstationary coupled Floquet instability or a proof of mode growth.'},indent=2)+'\n');print(json.dumps(rows,indent=2))
