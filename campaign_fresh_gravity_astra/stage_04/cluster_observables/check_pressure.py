"""Execute the next pressure-gradient test when genuine bounds become available.

Input JSON: {"A644": {"radius_kpc": 1331, "lower": ..., "upper": ...,
 "quantity": "new_over_original_thermal_pressure_gradient",
 "independent_provenance": "...", "same_angular_aperture_and_distance": true,
 "uniform_density_normalization_validated": true}, "ZW1215": {...}}

No observation values are supplied or manufactured by this script.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('pressure_bounds',type=Path)
ap.add_argument('--requirements',type=Path,default=Path(__file__).parent/'run_002/closure_requirements.csv')
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args()
obs=json.loads(a.pressure_bounds.read_text())
result=[]
for row in csv.DictReader(a.requirements.open()):
    if row['name'] not in obs:
        continue
    value=obs[row['name']]
    assert value['independent_provenance'].strip()
    assert value['quantity']=='new_over_original_thermal_pressure_gradient'
    assert value['same_angular_aperture_and_distance'] is True
    assert value['uniform_density_normalization_validated'] is True
    assert abs(float(value['radius_kpc'])-float(row['radius_kpc']))<1e-8
    lo,hi=float(value['lower']),float(value['upper'])
    assert 0<lo<=hi
    rlo,rhi=float(row['pressure_gradient_ratio_box_low']),float(row['pressure_gradient_ratio_box_high'])
    result.append(dict(name=row['name'],footing=row['footing'],scaling=row['scaling'],kernel=row['kernel'],
                       interval_intersection_nonempty=max(lo,rlo)<=min(hi,rhi),
                       inference='Conditional interval compatibility, not a confidence level'))
if not result:
    raise ValueError('No supported cluster measurement supplied')
payload={'input_hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (a.pressure_bounds,a.requirements)},
         'results':result,'warning':'Provenance assertions in the input must be independently audited before physical interpretation.'}
a.out.write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
