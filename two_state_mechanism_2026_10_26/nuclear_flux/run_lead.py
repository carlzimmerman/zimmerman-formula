"""Re-match archived nuclear grids to coupled asymptotic lattice modes."""
import argparse,json
from pathlib import Path
import numpy as np
from electronic import states,overlap
from lead import scattering_lead
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();src=Path(a.input)
d=json.loads((src/'results.json').read_text());settings=d['settings'];g=np.load(src/'grid.npz');V=g['V'];O=g['O'];R=g['R'];n=V.shape[1];h=settings['h'];basis=settings['basis']
prev=states(R[-2],basis);last=states(R[-1],basis);next_=states(R[-1]+h,basis)
recheck=overlap(prev,last)[:n,:n];assert np.max(abs(recheck-O[-1]))<1e-7
link=overlap(last,next_)[:n,:n];signs=np.sign(np.diag(link));assert np.all(signs!=0);link=link*signs
rows=[]
for E in [-.62,-.60,-.58]:
 r=scattering_lead(V,O,E,h,link)
 assert r['unitarity']<1e-7 and r['reciprocity']<1e-7
 rows.append(dict(energy=E,probabilities=(abs(r['S'])**2).tolist(),unitarity_error=r['unitarity'],reciprocity_error=r['reciprocity'],mode_weights=r['mode_weights'],mode_angles=r['mode_angles'],mode_residual=r['mode_residual']))
 print(E,rows[-1]['probabilities'],flush=True)
Path(a.output).write_text(json.dumps(dict(input=str(src),settings=settings,retained_states=n,rows=rows,physical_DR_rates_derived=False,scope='Coupled stationary lead for finite-basis neutral radial scattering; modes not full rovibrational product states'),indent=2)+'\n')
