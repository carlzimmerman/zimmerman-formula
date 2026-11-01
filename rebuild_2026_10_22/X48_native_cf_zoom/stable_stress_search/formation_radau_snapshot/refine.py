import json,numpy as np
import collapse,material
p=material.MaterialParameters(rho_q=1,G=1,a0=np.sqrt(8*np.pi),tau=.5)
r=collapse.simulate(collapse.SphericalCollapse(64,p),t_end=1.2,samples=121,rtol=2e-8,atol=1e-10,method='Radau',wall_seconds=25)
open('n64_refined/result.json','w').write(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['status','t_reached','elapsed_seconds','rhs_calls','max_relative_energy_error','peak_sampled_5pct_density']}))
