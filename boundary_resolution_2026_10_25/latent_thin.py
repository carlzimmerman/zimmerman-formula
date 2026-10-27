import argparse,json
from pathlib import Path
import numpy as np
from latent_stiff import LatentStiff
from fast_complete import finish
from surface_checked import transfer_species
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_stiff/base_0.25.json').read_text());out={'runs':[]}
 for beta in [4,8]:
  ell=3*np.sqrt(2/beta);m=LatentStiff(domain=12,beta=beta,K=30,charge=0,L=0,eta=0,sigma=0,eps=.3,h=.25,volume_cost=.001,material_length=.25);m.ell2=(ell/m.rm)**2;v,info=transfer_species(m,old);r=finish(m,v,dest.with_name(f'base_{beta}.json'),initial_iterations=100,newton_iterations=60);r['transfer']=info;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['beta','ell_kpc','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
