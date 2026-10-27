"""Independent small Fourier identities and saved-run accounting; no evolution."""
import json
from pathlib import Path
import numpy as np
from scipy.fft import fftn,ifftn,fftfreq

b=Path(__file__).parent
N=16;L=8.;dx=L/N;x=np.arange(N)*dx
X,Y,Z=np.meshgrid(x,x,x,indexing='ij',sparse=True)
k=2*np.pi*fftfreq(N,d=dx);kx,ky,kz=np.meshgrid(k,k,k,indexing='ij',sparse=True)
k2=kx*kx+ky*ky+kz*kz
rho=np.broadcast_to(1+.1*np.cos(2*np.pi*X/L)+.2*np.cos(4*np.pi*Y/L),(N,N,N)).copy()
rh=fftn(rho);kernel=np.zeros_like(k2);np.divide(-4*np.pi,k2,out=kernel,where=k2!=0)
target=4*np.pi*(rho-rho.mean())
lap=ifftn(-k2*kernel*rh).real
poisson_error=float(np.max(abs(lap-target)))
mutated_error=float(np.max(abs(-lap-target)))
eta=.7;dt=.06
wave=np.broadcast_to(np.exp(2j*np.pi*X/L),(N,N,N)).copy()
evolved=ifftn(fftn(wave)*np.exp(-.5j*eta*k2*dt))
expected=wave*np.exp(-.5j*eta*(2*np.pi/L)**2*dt)
plane_error=float(np.max(abs(evolved-expected)))
checks={'poisson_equation':poisson_error<1e-12,
        'poisson_sign_mutation_bites':mutated_error>.1,
        'free_plane_wave_dispersion':plane_error<1e-12,
        'unitary_step_preserves_mass':bool(abs(np.sum(abs(evolved)**2)-np.sum(abs(wave)**2))<1e-10)}
mass_residual={}
for tag in ['spin48','zero48','reverse48','spin64','halfstep48','pad64L32']:
    d=json.loads((b/'transport_runs'/(tag+'.json')).read_text())
    residual=abs(d['initial']['mass']-d['final']['mass']-d['removed']['mass'])
    mass_residual[tag]=residual
checks['six_mass_ledgers']=max(mass_residual.values())<1e-10
s=json.loads((b/'transport_summary.json').read_text())
checks['parity_control']=s['parity_gate']
checks['time_and_grid_control']=all(v['gate'] for c in s['controls'].values() for v in c.values())
# Preserve the failures: these assertions do not convert failed transport into a pass.
checks['all_failed_contraction_preserved']=all(not d['gates']['contraction_1p5'] for d in s['runs'].values())
checks['base_spin_ledger_failure_preserved']=not s['runs']['spin48']['gates']['spin_ledger']
checks['padded_spin_ledger_pass']=s['runs']['pad64L32']['gates']['spin_ledger']
assert all(checks.values()),checks
result={'checks':checks,'poisson_max_error':poisson_error,'wrong_sign_max_error':mutated_error,
        'plane_wave_max_error':plane_error,'mass_residuals':mass_residual,
        'scope':'small spectral identities and saved-run bookkeeping, not isolated boundary or four-dwarf verification'}
(b/'transport_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
