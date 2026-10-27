import argparse,json
from pathlib import Path
import numpy as np
from latent_verify import model,hessian
from fast_complete import finish
from surface_checked import transfer_species
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_verify/base_0.125.json').read_text());out={'runs':[]}
 for h,domain in [(.0625,12),(.125,18)]:
  m=model(h,domain);v,info=transfer_species(m,old);r=finish(m,v,dest.with_name(f'base_{h}_{domain}.json'),initial_iterations=0,newton_iterations=50);r.update(stage='domain_mesh_check',transfer=info,hessian=hessian(m,r));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['n','R_kpc','fine_spacing_kpc','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer','hessian']},flush=True)
