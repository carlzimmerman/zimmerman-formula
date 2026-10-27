import argparse,json
from pathlib import Path
import numpy as np,torch
from physical_model import Physical
from fast_complete import finish
from surface_checked import transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_verify/base_0.25.json').read_text());out={'runs':[],'checks':[]}
for scale,thermal in [(1.,'fixed_entropy'),(.5,'fixed_entropy'),(2.,'fixed_entropy')]:
 m=Physical(scale=scale,thermal=thermal,canonical=True);source=dict(old,r=(np.array(old['r'])*scale).tolist());v,info=transfer_species(m,source);z=np.r_[np.log(v[:m.n]),v[m.n:]];d=np.cos(np.arange(2*m.n));E,g=m.fg(z);errors=[]
 for dt in [1e-6,3e-7,1e-7]:
  fd=(m.fg(z+dt*d)[0]-m.fg(z-dt*d)[0])/(2*dt);errors.append(abs(fd-g@d)/max(1,abs(fd)))
 assert max(errors)<1e-6;out['checks'].append(errors);r=finish(m,v,dest.with_name(f'base_{scale}_{thermal}.json'),initial_iterations=0,newton_iterations=80);r['transfer']=info;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','thermal_policy','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
