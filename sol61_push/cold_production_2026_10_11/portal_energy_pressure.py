"""Energy-constrained bound on the portal pressure functional under rearrangement."""
from fractions import Fraction as F
from pathlib import Path
import json,math
import numpy as np
p=Path(__file__).parent
sample=json.loads((p/'portal_intensity_run/results.json').read_text())['rows'][0]
portal=json.loads((p/'nonlinear_portal_run/results.json').read_text())
params=json.loads((p/'repulsive_envelope_run/results.json').read_text())['parameters']
z=np.array(sample['normalized_intensity_samples']);checks=[]
def check(n,b):checks.append(dict(name=n,passed=bool(b)))
for t in [F(0),F(1,10),F(1,3),F(3,4),F(99,100)]:
 x=2*t/(1-t*t);u=2*t*t/(1-t*t);d=x-u;p0=2*t*t/(1+t*t)
 check('exact pressure-deficit identity',p0==d*d/(d*d-2*d+2))
 fprime=2*d*(2-d)/(d*d-2*d+2)**2
 fsecond=4*(1-d)*(2+2*d-d*d)/(d*d-2*d+2)**3
 check('monotone convex deficit function',0<=d<1 and fprime>=0 and fsecond>0)
Hratio=portal['softened']['Astar_over_m2']/2
gap_coefficient=params['u']**2/(2*Hratio)
sourceF=sample['final']['source_fraction']/sample['final']['charge']
rows=[]
for x in [.1,1.,10.]:
 v=x*z;r=np.hypot(1,v);U=float(np.mean(v*v/(r+1)));P=float(np.mean(v*v/(r*(r+1))))
 deficit=x-U
 bound=lambda E:(max(0.,x-E)**2/(max(0.,x-E)**2-2*max(0.,x-E)+2))
 check('sample satisfies Jensen portal bound',P>=bound(U)-1e-12)
 E=U+gap_coefficient*sourceF*x
 check('sample satisfies conservative chemical-budget bound',P>=bound(E)-1e-12)
 uniformU=math.hypot(1,x)-1;uniformP=1-1/math.hypot(1,x);release=U-uniformU
 check('convex energy decreases on homogenization',release>=0)
 rows.append(dict(mean_x=x,initial_U_over_AstarS0=U,initial_portal_pressure_over_AstarS0=P,
   initial_source_gap_over_AstarS0=gap_coefficient*sourceF*x,
   declared_total_excess_budget_over_AstarS0=E,
   portal_pressure_lower_bound_over_AstarS0=bound(E),
   released_interaction_energy_on_uniformization_over_AstarS0=release,
   uniform_portal_pressure_over_AstarS0=uniformP,
   uniform_pressure_with_release_in_kinetic_energy_over_AstarS0=uniformP+2*release/3))
out=dict(all_pass=all(v['passed'] for v in checks),checks=checks,rows=rows,
 source_charge_fraction_used=sourceF,chemical_gap_per_unit_mean_x_over_AstarS0=gap_coefficient,
 non_claims=['Bound is for portal pressure functional, not total instantaneous stress or sound speed',
 'Illustrative excess budgets assume rescaled sample and retained source fraction, not evolved cosmology',
 'No gravity, boundary energy exchange or time-dependent mean volume in the fixed-box bound',
 'No formation, selected density or baryonic acceleration law'])
(p/'portal_energy_pressure_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
