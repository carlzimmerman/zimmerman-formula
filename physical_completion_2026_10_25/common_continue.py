import argparse,json
from pathlib import Path
import numpy as np
from common_family import family
from fast_projected import finish
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=family(1.);old=json.loads(Path('physical_completion_2026_10_25/run_common_family/scale_1.0.json').read_text());v=np.r_[old['mass'],old['v'][m.n:]];r=finish(m,v,dest.with_name('state.json'),initial_iterations=0,newton_iterations=160);out={'state':r};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['energy','density_KKT_max','gradient_max','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
