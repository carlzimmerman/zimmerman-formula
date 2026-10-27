import sys,json,argparse
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'material_interface_2026_10_24'))
from carrier_checked import Carrier
from joint import law,RESERVOIR
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();m=Carrier();r=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text());rad=np.array(r['r']);mass=np.array(r['mass']);R=r['interpolated_crossings_kpc'][-1];external=sum(mass[rad>1.2*R])
def required(R):
 x=R/m.rm;gb=x/(x*x+m.b*m.b)**1.5;return float(x*x*(law(gb)-gb))
out=dict(total_mass_Mb=RESERVOIR,required_at_50_Mb=required(50),outside_50_max_Mb=RESERVOIR-required(50),required_at_existing_boundary_Mb=required(R),existing_boundary_kpc=R,existing_exterior_mass_Mb=float(external),minimum_mass_to_relocate_from_existing_exterior_Mb=float(external-(RESERVOIR-required(50))),maximum_law_radius_with_no_exterior_kpc=brentq(lambda R:required(R)-RESERVOIR,1,100),maximum_law_radius_if_existing_exterior_mass_retained_kpc=brentq(lambda R:required(R)-(RESERVOIR-external),1,100),claim='Necessary mass constraints, not an exclusion of a relocated boundary and redistributed free reservoir.')
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
