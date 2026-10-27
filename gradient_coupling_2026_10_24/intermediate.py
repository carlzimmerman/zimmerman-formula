import argparse,json
from pathlib import Path
import numpy as np
from coupled_model import Coupled,solve,transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[],'checks':[]};old=json.loads(Path('material_interface_2026_10_24/run_continue/results.json').read_text())['runs'][2]
for L,eta in [(5,1),(5,3),(7,1),(7,3)]:
 m=Coupled(n=96,domain=12,beta=2,K=30,charge=0,L=L,eta=eta);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:96]),v[96:]];d=np.cos(np.arange(192));E,g=m.fg(vv);errors=[]
 for dt in [1e-5,3e-6,1e-6]:
  fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);errors.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(errors)<1e-6;out['checks'].append(errors);r=solve(m,v,dest.with_name(f'checkpoint_{L}_{eta}.json'));r['transfer']=info;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['eta','density_stiffness_length_kpc','law_endpoint_error_dex','density_KKT_max','mass_outside50','min_transition_cell_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
