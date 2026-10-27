"""Discriminating linear counterexample before any long global split run."""
import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[]
for eta in [0.,.1,1.,100.]:
 for dt in [.1,1.,10.]:
  b=np.sqrt(eta);LC=np.array([[0.,0.,0.],[0.,0.,-b],[0.,0.,0.]]);LD=np.array([[0.,1.,0.],[-1.,0.,0.],[0.,b,0.]]);I=np.eye(3);C=I+dt/2*LC;D=np.linalg.solve(I-dt/2*LD,I+dt/2*LD);S=C@D@C;h=dt/2;pred=(1-(1+2*eta)*h*h)/(1+h*h);actual=(np.trace(S)-1)/2;L=LC+LD;mid=np.linalg.solve(I-dt/2*L,I+dt/2*L)
  rows.append({'eta':eta,'dt_times_bare_frequency':dt,'predicted_cos_fast':pred,'matrix_cos_fast':float(actual),'split_spectral_radius':float(max(abs(np.linalg.eigvals(S)))),'joint_midpoint_spectral_radius':float(max(abs(np.linalg.eigvals(mid)))),'within_predicted_linear_stability':bool(eta*h*h<=1)})
out={'cases':rows,'derivation':'Cayley free-wave plus symmetric exact transport kicks: cos(theta_eff)=[1-(1+2eta)h^2]/(1+h^2), h=omega_bare*dt/2. Stability requires eta*h^2<=1. Joint midpoint of the positive coupled quadratic system is stable for every dt. Thus exact component flows alone do not solve strong near-field stiffness.','decision':'Do not launch a long global split run unchanged. Exact edge lemma survives; transport and the scalar near field must be solved together or appropriately preconditioned.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert all(abs(z['matrix_cos_fast']-z['predicted_cos_fast'])<1e-10 for z in rows)
assert all(z['joint_midpoint_spectral_radius']<1+1e-10 for z in rows)
