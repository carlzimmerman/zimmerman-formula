import json,argparse
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();p=Path(__file__).parent;out=[]
for r in json.loads((p/'run_amplitude/results.json').read_text())['runs']:
 rad=np.array(r['r']);mass=np.array(r['mass']);R=r['interpolated_crossings_kpc'][-1];edges=[0.]
 for rr in rad:edges.append(2*rr-edges[-1])
 M50=float(np.interp(50**3,np.array(edges)**3,np.r_[0,np.cumsum(mass)]));sel=(rad>50)&(rad<R);err=np.log10(np.array(r['g_total'])/r['g_law']);ee=np.r_[err[(rad>=1.5)&(rad<=50)],np.interp(50,rad,err),np.interp(1.5,rad,err)]
 out.append(dict(L=r['density_stiffness_length_kpc'],boundary_kpc=R,law_error_dex=float(max(abs(ee))),law_error_fraction=float(max(abs(10**ee-1))),M_inside50_volume_reconstruction=M50,M_outside50=5.364-M50,required_M_inside50=4.801579345912336,minimum_cell_mass_between50_and_boundary=float(min(mass[sel])),r_at_minimum_cell_mass=float(rad[sel][np.argmin(mass[sel])]),exterior_mass=r['explicit_exterior_mass'],exterior_T_fraction=r['explicit_exterior_T_fraction'],density_KKT=r['density_KKT_max'],optimizer=r['optimizer'],qualification='No successful joint law/support/restoration claim. Positive numerical tails do not establish a populated transition.'))
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
