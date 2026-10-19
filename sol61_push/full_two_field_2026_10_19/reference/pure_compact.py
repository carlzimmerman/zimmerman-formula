"""Independent compact pure-X references for finite-time radial tests."""
import json
import sys
from pathlib import Path
import numpy as np
from pure_reference_refined import solve

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
rows=[]
for central in [.02,.03,.05]:
    sol,r,y,row=solve(central,radius=120,tol=2e-9)
    rows.append(row)
    print(json.dumps(row),flush=True)
    if row['success'] and row['field_min']>=-1e-9:
        np.savez(out/f'pureX_h{central:.3f}.npz',r=r,h=y[0],hp=y[1],
                 mass_G=y[2],logalpha=y[3],omega_X=row['frequency'],central=central,
                 source_mass=1.,four_pi_G=1.)
(out/'results.json').write_text(json.dumps({'rows':rows,'non_claim':'No stability or mixed-branch assertion.'},indent=2)+'\n')
