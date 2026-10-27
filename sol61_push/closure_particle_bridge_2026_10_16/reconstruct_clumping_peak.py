"""Reverse the saved fine-grid reversible trajectory to its recorded peak.
Independent reversibility/energy check; does not change original evolution.
"""
import json,sys,math
from pathlib import Path
import numpy as np
out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent;r=base/'nonlinear_charge_clumping_run_001'
d=json.loads((r/'results.json').read_text());row=d['runs'][-1];target=max(row['samples'],key=lambda s:s['peak_I_over_initial'])
state=np.load(r/'final_N512_dt0.005.npz');psi=state['psi'].copy();vel=state['psi_dot'].copy();chi=state['chi'].copy();cv=state['chi_dot'].copy();x=state['x'];dx=float(x[1]-x[0]);dt=-row['dt'];steps=round((row['end_time']-target['t'])/abs(dt));M=10.;L=1.9;a=20.;mu=-3.75
lap=lambda q:(np.roll(q,1)-2*q+np.roll(q,-1))/dx**2
def acc():
 ii=abs(psi)**2;return lap(psi)-(1+2*L*ii+a*chi)*psi,lap(chi)-(M*M*chi+mu*chi**2+chi**3+a*ii)
af,ac=acc()
for step in range(steps):
 vel+=.5*dt*af;cv+=.5*dt*ac;psi+=dt*vel;chi+=dt*cv;af,ac=acc();vel+=.5*dt*af;cv+=.5*dt*ac
peak=float(np.max(abs(psi)**2)/row['initial_I']);charge=float(dx*np.sum(2*np.imag(np.conj(psi)*vel)))
checks=[{'name':'reverse reconstructed peak matches recorded forward sample','passed':abs(peak/target['peak_I_over_initial']-1)<1e-8},{'name':'reverse reconstructed charge matches recorded forward sample','passed':abs(charge/target['charge']-1)<1e-10}]
assert all(c['passed'] for c in checks)
np.savez_compressed(out/'reconstructed_peak.npz',x=x,psi=psi,psi_dot=vel,chi=chi,chi_dot=cv)
result={'peak_time':target['t'],'peak_I_over_initial':peak,'peak_density_relative_std':target['density_relative_std'],'target_forward_sample':target,'checks':checks,'scope':'Reverse reconstruction of saved deterministic reversible trajectory; no new initial condition or forward formation claim'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
