import argparse,json
from pathlib import Path
import numpy as np
from surface_model import Surface,solve,transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('material_interface_2026_10_24/run_continue/results.json').read_text())['runs'][2];out={'runs':[],'checks':[]}
for L,sigma in [(1,.003),(1,.01),(1,.03),(3,.01)]:
 m=Surface(domain=12,beta=2,K=30,charge=0,L=L,eta=3,sigma=sigma,spacing=2);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(vv);err=[]
 for dt in [3e-6,1e-6,3e-7]:
  fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(err)<1e-6;out['checks'].append(err);r=solve(m,v,dest.with_name(f'checkpoint_{L}_{sigma}.json'),maxiter=2000);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['density_stiffness_length_kpc','surface_tension','n','law_endpoint_error_dex','density_KKT_max','mass_outside50','min_transition_cell_mass','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
