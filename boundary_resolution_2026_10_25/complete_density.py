import argparse,json
from pathlib import Path
import numpy as np
from density_field import DensityField
from fast_complete import finish
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_density_field/results.json').read_text())['candidate'];m=DensityField(domain=12,beta=2,K=30,charge=0,L=0,eta=0,sigma=.002,eps=.3,hcritical=.1,density_length=1);m.ell2=(2/m.rm)**2;v=np.r_[old['mass'],old['v'][m.n:]];r=finish(m,v,dest.with_name('checkpoint.json'),initial_iterations=0,newton_iterations=100);dest.write_text(json.dumps(r,indent=2)+'\n');print({k:r[k] for k in ['law_endpoint_error_dex','density_KKT_max','gradient_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']})
