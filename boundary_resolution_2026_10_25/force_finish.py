import argparse,json
from pathlib import Path
import numpy as np
from critical import Critical
from fast_finish import finish
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);r=json.loads(Path('boundary_resolution_2026_10_25/run_critical/base_0.1.json').read_text());m=Critical(domain=12,beta=2,K=30,charge=0,L=1,eta=0,sigma=.002,eps=.3,hcritical=.1);m.ell2=(2/m.rm)**2;v=np.r_[r['mass'],r['v'][m.n:]];out=finish(m,v,dest.with_name('checkpoint.json'));dest.write_text(json.dumps(out,indent=2)+'\n');print({k:out[k] for k in ['law_endpoint_error_dex','density_KKT_max','gradient_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']})
