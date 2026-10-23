"""Independent charge-generator check on the saved propagated wavefunction."""
from pathlib import Path
import sys,json
import numpy as np
from scipy.fft import fft,ifft
from quantum_wavefunction import CellWavefunction
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True);m=CellWavefunction(32,12.)
psi=np.load(P/'quantum_wavefunction_run/persistent_state_n32_dt001.npy')
def charge(p):
 k=2*np.pi*np.fft.fftfreq(m.n,d=m.length/m.n);der=[]
 for axis in range(4):
  shape=[1]*4;shape[axis]=m.n
  der.append(ifft(fft(p,axis=axis,norm='ortho')*k.reshape(shape),axis=axis,norm='ortho'))
 f,h,x,y=m.fields
 return f*der[1]-h*der[0]+2*(x*der[3]-y*der[2])
rows=[]
for name,p in [('initial',m.initial_x_excitation()),('evolved',psi)]:
 q=charge(p);rows.append(dict(name=name,Q_real=float(np.vdot(p,q).real),Q_imag=float(np.vdot(p,q).imag),Q2=float(np.vdot(q,q).real)))
error=abs(rows[1]['Q2']-rows[0]['Q2']);checks=dict(expected_charge_variance=abs(rows[0]['Q2']-4)<1e-9,charge_conservation=error<1e-9,neutral_expectation=all(abs(r['Q_real'])<1e-10 for r in rows))
out=dict(checks=checks,all_pass=bool(all(checks.values())),rows=rows,Q2_drift=error,scope='Single-cell global U(1) charge only; mean-neutral superposition of X charges +/-2. Not a measured inverse scattering rate or cosmological quantum state.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
