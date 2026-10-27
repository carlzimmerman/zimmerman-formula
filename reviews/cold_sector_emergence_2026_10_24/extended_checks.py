"""Finite curvature screen for exact algebraic-law halos around Plummer baryons."""
import json
from pathlib import Path
import numpy as np
import sympy as s

r,A=s.symbols('r A',positive=True)
b=A*r/(1+r*r)**s.Rational(3,2)
# Rationalization avoids subtracting nearly equal fields in the baryon-dominated regime.
g=s.sqrt(b*b+b)
gc=b/(g+b)
rho=(s.diff(gc,r)+2*gc/r)/(4*s.pi)
dr=s.diff(rho,r)
h=(s.diff(dr,r)*g-dr*s.diff(g,r))/g**3
fn=s.lambdify((r,A),(rho,dr,h),'numpy',cse=True)
x=np.geomspace(1e-4,1e4,1601)
rows=[]
for a in np.geomspace(1e-4,1e4,17):
    density,slope,convexity=fn(x,a)
    assert np.all(np.isfinite(density)) and np.all(np.isfinite(convexity))
    rows.append({'A':float(a),'positive_density':bool(np.all(density>0)),
                 'decreasing_density':bool(np.all(slope<0)),
                 'positive_phi_curvature':bool(np.all(convexity>0)),
                 'negative_curvature_count':int(np.count_nonzero(convexity<0)),
                 'minimum_curvature':float(np.min(convexity))})
data={'domain':'G=a0=Plummer radius=1; A=baryonic mass; r>0',
      'A_count':17,'radius_count':1601,'rows':rows,
      'interpretation':'Positive d2rho/dPhi2 everywhere would suffice for positive Abel inversion. Finite sampling cannot prove everywhere positivity. Negative values would not by themselves prove f<0.',
      'non_claims':['No time evolution','No finite-mass halo','No universal sign theorem','No precision certification near cancellation']}
Path('reviews/cold_sector_emergence_2026_10_24/extended_run/result.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
