"""Independent exact density, inverse, offset and dilation checks; fixed background only."""
from pathlib import Path
import sympy as s
import json,hashlib
r,R,M,a,G,y,q,rho,B,w2,lam=s.symbols('r R M a G y q rho B w2 lam',positive=True)
total=M*s.sqrt(1+a*r*r/(G*M))
density=s.diff(total,r)/(4*s.pi*r*r)
expected=a*M/(4*s.pi*G*r*total)
yq=(q*q+q*s.sqrt(q*q+4))/2
F=(1+y)**s.Rational(3,2)/(1+y/2)
Fprime=s.sqrt(1+y)*(y+4)/(y+2)**2
sigma=s.eye(3)*lam-s.eye(3)*(3*lam)/3
meanr2=s.integrate(r**4,(r,0,R))/s.integrate(r**2,(r,0,R))
checks={
'density_from_enclosed_mass':s.simplify(density-expected)==0,
'inverse_positive_root_squared_relation':s.simplify(yq*yq-q*q*(1+yq))==0,
'density_map_derivative':s.simplify(s.diff(y/s.sqrt(1+y),y)-(1+y/2)/(1+y)**s.Rational(3,2))==0,
'constitutive_derivative_monotonic_factor':s.simplify(s.diff(F,y)-Fprime)==0,
'uniform_sphere_mean_radius_squared':s.simplify(meanr2-3*R**2/5)==0,
'dilation_shear_zero':sigma==s.zeros(3),
'kinetic_per_volume':s.expand(rho*meanr2+9*B*w2-((s.Rational(3,5))*rho*R**2+9*B*w2))==0,
}
root=Path(__file__).resolve().parents[1]
files=[root/'constitutive/EQUATION_OF_STATE.md',root/'constitutive/eos_audit.py',Path(__file__)]
res={'checks':checks,'sources':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'scope':'Exact fixed-background identities only; free sphere dilation admissibility is a boundary-condition hypothesis.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
assert all(checks.values())
