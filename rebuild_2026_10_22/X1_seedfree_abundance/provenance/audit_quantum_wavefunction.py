"""Convergence of persistent full complex state in the four-coordinate cell."""
from pathlib import Path
import sys,json
import numpy as np
from quantum_wavefunction import CellWavefunction
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
rows=[];states={}
for n,dt in [(24,.02),(32,.04),(32,.02),(32,.01),(40,.02)]:
 model=CellWavefunction(n,12.);initial=model.initial_x_excitation();d0=model.diagnostics(initial)
 psi=model.evolve(initial,dt,round(2/dt));d=model.diagnostics(psi)
 row=dict(n=n,dt=dt,initial=d0,final=d,relative_energy_drift=abs(d['energy']/d0['energy']-1));rows.append(row)
 if n==32:states[dt]=psi
 if n==24:
  matrix=psi.reshape(n*n,n*n);rho=matrix@matrix.conj().T
  row['Phi_reduced_purity']=float(np.sum(abs(rho)**2))
 print(json.dumps(row),flush=True)
model=CellWavefunction(32,12.);back=model.evolve(states[.02],-.02,100)
inverse_error=float(np.linalg.norm(back-model.initial_x_excitation()))
e1=float(np.linalg.norm(states[.04]-states[.02]));e2=float(np.linalg.norm(states[.02]-states[.01]))
free=CellWavefunction(32,12.,g=0.,lam=0.);p0=free.initial_x_excitation();pf=free.evolve(p0,.002,100)
free_error=float(np.linalg.norm(pf-p0*np.exp(-.2j*(free.mass.sum()/2+free.mass[2]))))
# Compare observables at the SAME dt; separate grid error from time error.
spatial=[rows[i] for i in [0,2,4]]
spatial_errors=[float(np.max(abs(np.array(spatial[i]['final']['bare_occupations'])-np.array(spatial[i+1]['final']['bare_occupations'])))) for i in range(2)]
checks=dict(unitarity=all(abs(r['final']['norm']-1)<1e-11 for r in rows),inverse=inverse_error<1e-11,second_order=3.5<e1/e2<4.5,free_analytic=free_error<1e-5,energy=all(r['relative_energy_drift']<1e-4 for r in rows),field_grid=spatial_errors[-1]<1e-6,boundary=all(r['final']['boundary_probability']<1e-9 for r in rows))
np.save(O/'persistent_state_n32_dt001.npy',states[.01])
out=dict(checks={k:bool(v) for k,v in checks.items()},all_pass=bool(all(checks.values())),rows=rows,timestep_state_differences=[e1,e2],timestep_ratio=e1/e2,spatial_occupation_differences=spatial_errors,inverse_state_error=inverse_error,free_analytic_state_error=free_error,scope='One-cell quantum mechanics, four real coordinates, original polynomial potential, mPhi=1. Explicit free one-X-oscillator benchmark state, NOT the actual high-H source. FFT conjugate momenta are configuration momenta, not spatial particle momenta. Full wavefunction propagated without Gaussian replacement or separate rate terms. No bath, spatial momentum convergence, renormalized field theory, or abundance.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2));sys.exit(0 if out['all_pass'] else 1)
