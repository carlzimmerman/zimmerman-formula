"""Exact quadratic elimination and conditional de Sitter cone identities."""
import argparse
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
B, delta, k, H, beta = s.symbols('B delta k H beta', positive=True)
S = 3*B+2
xi = 1+delta
v, shift, z, n, p = s.symbols('v shift z n p', real=True)
checks = {}
def check(name, expression):
    remainder = s.simplify(expression)
    checks[name] = remainder == 0
    if not checks[name]:
        raise AssertionError((name, remainder))

# Units M²/2, local spatial Fourier wave number k, v=dot(zeta).
K = -3*S*v**2-2*S*v*k**2*shift-B*k**4*shift**2
shift_star = -S*v/(B*k**2)
check('shift_stationarity', s.diff(K,shift).subs(shift,shift_star))
alpha = 2*S/B
check('positive_kinetic_reduction', K.subs(shift,shift_star)-alpha*v**2)
Lp = 4*p*k*n-2*xi*p**2
p_star = k*n/xi
check('polarization_stationarity', s.diff(Lp,p).subs(p,p_star))
eta = 2/xi
check('acceleration_coefficient', Lp.subs(p,p_star)-eta*k**2*n**2)
gradient = k**2*(2*z**2+4*n*z+eta*n**2)
n_star = -xi*z
check('lapse_stationarity', s.diff(gradient,n).subs(n,n_star))
check('negative_gradient_reduction', gradient.subs(n,n_star)+2*delta*k**2*z**2)
cs2 = delta*B/S
check('scalar_speed',2*delta/alpha-cs2)
Cbare = 3*beta**2/4
check('acceleration_radius_curvature', (beta/(4*H))**2*(3*H**2)-Cbare/4)
delta_equal = S*beta**2/(16*B)
check('cone_radius_equals_acceleration_radius', cs2.subs(delta,delta_equal)/H**2-(beta/(4*H))**2)
check('target_equal_radius_gap', delta_equal.subs(beta**2,128*s.pi/3)-8*s.pi*S/(3*B))
# Effective radial cone metric in the chosen homogeneous preferred foliation.
r, speed = s.symbols('r speed', positive=True)
geff = s.Matrix([[H**2*r**2-speed**2,-H*r],[-H*r,1]])
check('effective_metric_determinant',geff.det()+speed**2)
ray = H*r-speed
check('inward_characteristic_null',(s.Matrix([1,ray]).T*geff*s.Matrix([1,ray]))[0])
check('cone_stationary_radius',ray.subs(r,speed/H))
check('preferred_clock_killing_contraction', (s.Matrix([-1,0]).dot(s.Matrix([1,0])))+1)

result = {'scope':'Local high-wave-number quadratic scalar sector; conditional constant-speed cone extrapolation, not full causal health',
          'checks':checks,'passed':len(checks),
          'scalar_speed_squared':str(cs2),
          'target_equal_radius_gap_infimum':float(8*s.pi),
          'target_scalar_speed':float(s.sqrt(8*s.pi/3)),
          'non_claims':['No complete de Sitter perturbation spectrum',
                        'No universal causal bound for the full constrained theory',
                        'No coefficient selection or source-to-observation dictionary']}
Path(args.output).parent.mkdir(parents=True,exist_ok=True)
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':len(checks),'scope':result['scope']}))
