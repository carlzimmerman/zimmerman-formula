import argparse,json
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();rows=json.loads(Path('gradient_coupling_2026_10_24/run_continue/results.json').read_text())['runs'];out=[]
for r in rows:
 if r['stage']!='base':continue
 rad=np.array(r['r']);mass=np.array(r['mass']);R=r['interpolated_crossings_kpc'][-1];ed=[0.]
 for rr in rad:ed.append(2*rr-ed[-1])
 rho=mass/(np.diff(np.array(ed)**3)/3)
 for fac in [1,1.2,1.5]:
  z=rho[(rad>15)&(rad<fac*R)];out.append(dict(n=r['n'],radius_cut_factor=fac,density_rebound=float(max(z/np.minimum.accumulate(z))),minimum_density=float(min(z)),boundary_kpc=R))
Path(a.output).write_text(json.dumps({'finding':'The original eligibility cut at q=.5 misses part of the coarse-grid cavity; full interface support fails already on coarse grid.','rows':out},indent=2)+'\n');print(json.dumps(out,indent=2))
