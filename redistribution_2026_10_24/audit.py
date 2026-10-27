import json,argparse
from pathlib import Path
import numpy as np
from global_density import Global,transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);p=Path(__file__).parent;out={'log_mass_gradient_checks':[],'states':[]};old=json.loads(Path('material_interface_2026_10_24/run_continue/results.json').read_text())['runs'][2]
for L in [1,3,10]:
 m=Global(n=96,domain=12,beta=2,K=30,charge=0,L=L);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:96]),v[96:]];d=np.r_[np.cos(np.arange(96)),np.zeros(96)];E,g=m.fg(vv);err=[]
 for eps in [1e-4,1e-5,1e-6]:
  fd=(m.fg(vv+eps*d)[0]-m.fg(vv-eps*d)[0])/(2*eps);err.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(err)<1e-6;out['log_mass_gradient_checks'].append(dict(L=L,errors=err))
for directory in ['run_screen','run_binding','run_global']:
 rows=json.loads((p/directory/'results.json').read_text())['runs']
 for r in rows:
  rad=np.array(r['r']);mass=np.array(r['mass']);q=np.array(r['q']);edges=[0.]
  for rr in rad:edges.append(2*rr-edges[-1])
  M50=float(np.interp(50**3,np.array(edges)**3,np.r_[0,np.cumsum(mass)]));err=np.log10(np.array(r['g_total'])/r['g_law']);ii=(rad>=1.5)&(rad<=50);errors=np.r_[err[ii],np.interp(50,rad,err),np.interp(1.5,rad,err)]
  out['states'].append(dict(source=directory,L=r.get('density_stiffness_length_kpc'),epsilon=r.get('binding_epsilon'),R=r['interpolated_crossings_kpc'],law_error_dex=float(max(abs(errors))),law_error_fraction=float(max(abs(10**errors-1))),M_inside50_volume_reconstruction=M50,M_outside50=5.364-M50,required_M_inside50=4.801579345912336,density_KKT=r['density_KKT_max'],empty_cells=r['empty_transition_cells'],exterior_T_fraction=r['explicit_exterior_T_fraction'],exterior_mass=r['explicit_exterior_mass'],optimizer=r['optimizer']))
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
