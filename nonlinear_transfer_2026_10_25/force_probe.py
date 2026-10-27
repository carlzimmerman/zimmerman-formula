import argparse,json
from pathlib import Path
import numpy as np
from full import Full
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();m=Full();out={'states':[]}
for path in ['nonlinear_transfer_2026_10_25/run_equilibrium/state.npz','nonlinear_transfer_2026_10_25/run_adaptive_dilated/state.npz']:
 s=np.load(path);a=s['a'];x=s['alpha'];chi=s['chi'];d=.1*a*(np.sin(np.arange(m.n))+.3j*np.cos(np.arange(m.n)))[None,:];E,mu=m.pot(a,x,True);exact=2*np.real(np.sum(mu*np.conj(a)*d));errs=[]
 for h in [1e-4,1e-5,1e-6]:
  fd=(m.pot(a+h*d,x)-m.pot(a-h*d,x))/(2*h);errs.append({'h':h,'fd':float(fd),'analytic':float(exact),'relative_error':float(abs(fd-exact)/max(abs(fd),1e-20))})
 direction=np.sin(np.arange(m.n))*.1;parts=m.vacuum_parts(a,chi);grad=m.carrier_force(x,parts)[0];h=1e-5
 def Ealpha(t):return m.energy(a,t,chi,np.zeros(len(chi)))
 fda=(Ealpha(x+h*direction)-Ealpha(x-h*direction))/(2*h);ga=float(grad@direction)
 item={'state':path,'potential_force_checks':errs,'carrier_full_energy_fd':float(fda),'carrier_force':ga,'carrier_relative_error':float(abs(fda-ga)/max(abs(fda),1e-20))};out['states'].append(item)
Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(out,flush=True)
