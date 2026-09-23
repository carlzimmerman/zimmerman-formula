"""Exact constitutive checks and fresh Lean compilation; no cosmology fit."""
from pathlib import Path
import json
import subprocess
import sys
import sympy as S

here = Path(__file__).resolve().parent
root = here.parents[3]
out = Path(sys.argv[1]).resolve()
assert out.is_relative_to(here)
checks = {}

def check(name, residual):
    value = S.simplify(residual)
    assert value == 0, (name, value)
    checks[name] = str(value)

y, lam, t, u, v, r, G, a0, C = S.symbols('y lam t u v r G a0 C', positive=True)
mu = 1-(1+lam*y)**-2
primitive = y*y-2/lam**2*(S.log(1+lam*y)+1/(1+lam*y)-1)
check('action_primitive_derivative', S.diff(primitive,y)/(2*y)-mu)
check('deep_slope', S.limit(mu/y,y,0)-2*lam)
check('newtonian_limit', S.limit(mu,y,S.oo)-1)
check('transverse_positive_factor', mu-(lam*y)*(lam*y+2)/(1+lam*y)**2)
check('longitudinal_positive_factor', mu+y*S.diff(mu,y)-(lam*y)*((lam*y)**2+3*lam*y+4)/(1+lam*y)**3)
f=lambda q:q*(1-(1+q)**-2)
poly=u*u*v*v+2*u*u*v+u*u+2*u*v*v+5*u*v+2*u+v*v+2*v
check('flux_difference', f(v)-f(u)-(v-u)*poly/((1+u)**2*(1+v)**2))
check('flux_derivative', S.diff(f(t),t)-t*(t*t+3*t+4)/(1+t)**3)
check('flux_lower_bound_gap', f(t)-(t-1)-(t*t+t+1)/(1+t)**2)
check('effective_exterior_density', S.diff(r*r*(C/r),r)/(4*S.pi*G*r*r)-C/(4*S.pi*G*r*r))
check('total_inferred_mass', r*r*(C/r)/G-C*r/G)
p=S.symbols('p0:3',real=True)
norm=S.sqrt(sum(q*q for q in p))
energy=norm**3/(12*S.pi*G*a0)
for i in range(3):
    check('deep_action_gradient_'+str(i),S.diff(energy,p[i])-norm*p[i]/(4*S.pi*G*a0))

lean = here/'BaryonResponse.lean'
compiled = subprocess.run(['lake','env','lean',str(lean)],cwd=root/'fable_independent_2026/lean_2026',capture_output=True,text=True)
(out/'lean.txt').write_text(compiled.stdout+compiled.stderr)
assert compiled.returncode == 0, compiled.stdout+compiled.stderr
assert 'sorryAx' not in compiled.stdout and 'warning:' not in compiled.stdout
assert compiled.stdout.count('depends on axioms:') == 9
result={'exact_checks':checks,'exact_check_count':len(checks),'lean_named_theorems':9,
        'lean_exit_code':compiled.returncode,'scope':'Constitutive identities; all-real Lean algebra, monotonicity and IVT existence. Static spherical response only; no observational or cosmological certificate.'}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
