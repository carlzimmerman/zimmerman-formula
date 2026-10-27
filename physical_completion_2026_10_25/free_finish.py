import argparse,json
from pathlib import Path
import numpy as np
from free_formation import FreeVacuum
from fast_projected import finish
from surface_checked import transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=FreeVacuum();old=json.loads(Path('physical_completion_2026_10_25/run_free_lbfgs/final.json').read_text());v=np.r_[old['mass'],old['v'][m.n:]];formed=finish(m,v,dest.with_name('formed.json'),initial_iterations=0,newton_iterations=160);out={'formed':formed};dest.write_text(json.dumps(out,indent=2)+'\n');print('FORMED',{k:formed.get(k) for k in ['energy','density_KKT_max','gradient_max','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
old=json.loads(Path('physical_completion_2026_10_25/run_vacuum/prepared.json').read_text());v,info=transfer_species(m,old);prepared=finish(m,v,dest.with_name('prepared.json'),initial_iterations=0,newton_iterations=80);out['prepared']=prepared;out['formation_radius_difference_kpc']=formed['scaled_boundary_kpc']-prepared['scaled_boundary_kpc'];out['formation_energy_difference']=formed['energy']-prepared['energy'];out['released_energy_Eunit']=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text())['energy']-formed['energy'];dest.write_text(json.dumps(out,indent=2)+'\n');print('MATCH',out['formation_radius_difference_kpc'],out['formation_energy_difference'],flush=True)
