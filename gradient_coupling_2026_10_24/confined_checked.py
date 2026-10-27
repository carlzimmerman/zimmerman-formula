import argparse,json
from pathlib import Path
import numpy as np
from coupled_model import Coupled,solve,transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('gradient_coupling_2026_10_24/run_continue/results.json').read_text())['runs'][0];out={'runs':[],'checks':[]}
for charge in [.003,.03,.3]:
 m=Coupled(n=96,domain=12,beta=2,K=30,charge=charge,L=5,eta=3);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,old);vv=np.r_[np.log(v[:96]),v[96:]];d=np.sin(np.arange(192));E,g=m.fg(vv);err=[]
 for dt in [3e-6,1e-6,3e-7]:
  fd=(m.fg(vv+dt*d)[0]-m.fg(vv-dt*d)[0])/(2*dt);err.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(err)<1e-6;out['checks'].append(err);r=solve(m,v,dest.with_name(f'checkpoint_{charge}.json'),maxiter=2000);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['charge','law_endpoint_error_dex','density_KKT_max','mass_outside50','min_transition_cell_mass','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
