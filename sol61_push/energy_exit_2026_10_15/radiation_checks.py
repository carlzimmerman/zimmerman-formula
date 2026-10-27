"""Conserved-source scalar radiation; prescribed breathing-source comparison."""
import json
from pathlib import Path
import sympy as s
import mpmath as mp
mp.mp.dps=60
z=s.symbols('z',positive=True)
F=3*(s.sin(z)-z*s.cos(z))/z**3
B=s.simplify(z*s.diff(F,z))
series=s.series(B,z,0,7).removeO()
checks={}
checks['constant_charge_cancels']=s.limit(B,z,0)==0
checks['finite_size_amplitude']=s.simplify(series-(-z*z/5+z**4/70-z**6/2520))==0
checks['source_power_series']=s.series(B*B,z,0,7).removeO()==z**4/25-z**6/175
M,R,O,e,alpha,G,cf=s.symbols('M R O e alpha G cf',positive=True)
power=alpha*G*M*M*e*e*O*O*(O*R/cf)**4/(50*cf)
E=3*M*R*R*e*e*O*O/10
checks['damping_scale']=s.simplify(E/power-15*cf*R*R/(alpha*G*M*(O*R/cf)**4))==0
v=s.symbols('v',positive=True)
checks['virial_time_ratio']=s.simplify((E/power*O).subs(G*M,v*v*R).subs(O,v/R)-15/alpha*(cf/v)**5)==0
rows=[]
for zv in ['.001','.01','.1','1']:
 zz=mp.mpf(zv)
 # Independent radial integral: delta rho contains the moving boundary.
 # For rho=3M/(4piR^3), R->R(1+e), delta Q/M/e = -9 int_0^1 t^2 sinc(zt)dt+3 sinc(z).
 integ=-9*mp.quad(lambda t:t*t*mp.sin(zz*t)/(zz*t) if t else mp.mpf(0),[0,1])+3*mp.sin(zz)/zz
 formula=3*((zz*zz-3)*mp.sin(zz)+3*zz*mp.cos(zz))/zz**3
 assert abs(integ-formula)<mp.mpf('1e-50')
 rows.append(dict(z=float(zz),radiative_charge_amplitude_per_eM=float(formula),
                  leading_approximation=float(-zz*zz/5),quadrature_error=float(abs(integ-formula))))
c=299792458.; vel=200000.
result=dict(checks={k:bool(v) for k,v in checks.items()},quadratures=rows,
 example=dict(assigned_velocity_km_s=200,assigned_alpha=1,damping_to_dynamical_time=15*(c/vel)**5),
 nonclaims=['Prescribed uniform-sphere breathing comparison','No universal monopole theorem for varying scalar charges',
 'No full mediator completion','No astrophysical likelihood'])
Path(__file__).with_name('radiation_run_v1').joinpath('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
assert all(checks.values())
