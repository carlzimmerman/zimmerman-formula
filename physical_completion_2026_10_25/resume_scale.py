import argparse,json
from pathlib import Path
from physical_model_checked import Physical
from fast_complete import finish
from surface_checked import transfer_species
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('physical_completion_2026_10_25/run_screen_checked/base_2.0_fixed_entropy.json').read_text());out={'runs':[]}
for thermal in ['fixed_entropy','virial_scaled']:
 m=Physical(scale=2,thermal=thermal,canonical=True,h=.125);v,info=transfer_species(m,old);r=finish(m,v,dest.with_name(thermal+'.json'),initial_iterations=100,newton_iterations=120);r['transfer']=info;out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','thermal_policy','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
