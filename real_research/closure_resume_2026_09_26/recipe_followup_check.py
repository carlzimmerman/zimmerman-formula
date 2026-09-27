#!/usr/bin/env python3
"""Exact frozen CHK scalar reduction; bounded witness, not full gravity closure."""
import json
import math
from pathlib import Path
import sympy as s

checks = {}

def exact(name, residual):
    value = s.factor(s.simplify(residual))
    checks[name] = {"residual": str(value), "passed": value == 0}
    assert value == 0, (name, value)

k, C, B, A, w = s.symbols('k C B A w', real=True)
p, f, v, u, d = s.symbols('p f v u d', real=True)
T = -s.I*w
E = [4*k**2*p-4*k**2*f-T*(-12*T*p+4*k**2*v-6*B*(3*T*p-k**2*v)),
     -4*k**2*p-4*k**2*(u-f)+2*A*k**2*f,
     4*k**2*T*p+2*B*k**2*(3*T*p-k**2*v),
     4*k**2*(u-f)+4*k**2*C*u]
M = s.Matrix([[s.diff(e, z) for z in [p, f, v, u]] for e in E])
den, num = A+(A+2)*C, 2-A*(1+C)
exact('independent_Fourier_determinant', M.det()-64*k**8*(B*num*k**2-(2+3*B)*den*w**2))
L = (-6*d**2+4*k**2*v*d+2*k**2*p**2-4*k**2*f*p
     +2*k**2*(u-f)**2+2*k**2*C*u**2-B*(3*d-k**2*v)**2+A*k**2*f**2)
sol = s.solve([s.diff(L, z) for z in [f, v, u]], [f, v, u], dict=True)[0]
exact('independent_realtime_reduction', L.subs(sol)-(2*(2+3*B)/B*d**2-2*k**2*num/den*p**2))
speed = B*num/((2+3*B)*den)
exact('speed_monotonicity', s.diff(speed, C)+4*B/((2+3*B)*den**2))
causal_C = (B-A-2*A*B)/(A+2+2*A*B+3*B)
exact('unit_speed_boundary', speed.subs(C, causal_C)-1)
x = s.symbols('x', positive=True)
phantom = (x-1)/(s.exp(x)+x-1)
exact('exponential_threshold', 2*phantom/(1-phantom)-2*(x-1)*s.exp(-x))
exact('threshold_derivative', s.diff(2*(x-1)*s.exp(-x), x)-2*(2-x)*s.exp(-x))
exact('phantom_derivative', s.diff(phantom, x)-s.exp(x)*(2-x)/(s.exp(x)+x-1)**2)
av, bv = s.Rational(3, 10), s.Rational(1, 100)
cv_min, cv_max = -s.Rational(1, 8), s.Integer(5)
exact('rational_witness_kinetic', (2*(2+3*B)/B).subs(B, bv)-406)
exact('rational_witness_min_D', den.subs({A: av, C: cv_min})-s.Rational(1, 80))
exact('rational_witness_min_N', num.subs({A: av, C: cv_max})-s.Rational(1, 5))
exact('rational_witness_max_speed', speed.subs({A: av, B: bv, C: cv_min})-s.Rational(139, 203))
exact('rational_witness_min_speed', speed.subs({A: av, B: bv, C: cv_max})-s.Rational(1, 11977))
ctrl = speed.subs({A: 0, B: bv, C: cv_min})
assert ctrl < 0
checks['zero_alpha_negative_response_control'] = {'speed_squared': str(ctrl), 'passed': bool(ctrl < 0)}
d2 = 1/(math.exp(2)+1)
rows = []
for aa in [9.624047966926507e-14, 1e-9, 3.2e-9]:
    kk = math.sqrt(math.log((aa+2)*d2/aa))
    rows.append({'alpha': aa, 'kcrit_xi': kk, 'Lcrit_over_xi': 2*math.pi/kk})
result = {'result': 'exact symbolic block identities and rational bounded witness verified',
          'checks': checks, 'threshold_table_float64': rows,
          'all_negative_branch_alpha_threshold_float64': 2/math.exp(2),
          'scope': 'k>0, B>0, D!=0, frozen principal block; real rational/exponential identities',
          'non_claims': ['No full canonical count or covariant action-to-block theorem',
                         'No exact static MOND/PPN compatibility of the finite-alpha witness',
                         'No nonlinear stability or observational fit']}
dest = Path(__file__).parent/'recipe_followup_run'/'results.json'
dest.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
