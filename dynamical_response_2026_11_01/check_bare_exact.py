"""No-Krylov actual-halo free-response check; bounded runner only."""
import json,sys
from pathlib import Path
import numpy as np
from background import Background
from response_v2 import assemble,pulse_integral

def main():
    root=Path(__file__).resolve().parent;rows=[]
    for state in ('baseline','compact'):
        bg=Background(state)
        V,sg,nu,b,bc,diag=assemble(bg,64,1024,24,10)
        reference=json.loads((root/(state+'_bare_001/result.json')).read_text())
        amp=.001*bg.original_psi;T=20/bg.omega_dyn
        for saved in reference['cases']:
            omega=saved['forcing_omega']
            final=amp*nu*b*pulse_integral(nu,np.array([T]),omega,T)[:,0]
            energy=float(np.vdot(final,final).real/4)
            angular=float(.5*np.sum(abs(final)**2/nu))
            rows.append(dict(state=state,pattern_ratio=saved['pattern_ratio'],
                             direct_spectral_energy=energy,direct_spectral_angular=angular,
                             energy_relative_error=abs(saved['final_energy']/energy-1),
                             angular_relative_error=abs(saved['canonical_angular_momentum']/angular-1)))
    passed=all(max(r['energy_relative_error'],r['angular_relative_error'])<2e-6 for r in rows)
    out=Path(sys.argv[1]);out.write_text(json.dumps(dict(cases=rows,passed=passed),indent=2)+'\n')
    print(json.dumps(dict(passed=passed,max_error=max(max(r['energy_relative_error'],r['angular_relative_error'])for r in rows))))
    if not passed:raise SystemExit(1)
if __name__=='__main__':main()
