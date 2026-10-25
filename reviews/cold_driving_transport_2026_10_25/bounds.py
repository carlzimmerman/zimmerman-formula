"""Post-run analytic checks; no fitted parameters or observed merger counts."""
import json,math
from pathlib import Path
import sympy as s
x=s.symbols('x')
assert s.expand(10*x**4-24*x**2+14+8*(x-1)-2*(x-1)**2*(5*x*x+10*x+3))==0
p=Path(__file__).resolve().parent
rows=json.load(open('reviews/cold_local_production_2026_10_25/run/result.json'))['rows']
counts=[math.ceil(math.log(1/r['ratio_produced_required'])/math.log(3)) for r in rows]
f=json.loads((p/'run/result.json').read_text())['summary']['sudden_fraction_range']
r=dict(algebraic_factorization_verified=True,optimistic_factor_three_cycle_counts=[min(counts),max(counts)],uniform_donor_volume_ratio=[1/f[1],1/f[0]],uniform_donor_radius_R500=[(.001+.999/z)**(1/3) for z in f[::-1]])
(p/'bounds_result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
