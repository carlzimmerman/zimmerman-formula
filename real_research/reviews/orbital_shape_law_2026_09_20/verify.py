#!/usr/bin/env python3
"""Exact shape identities, independent forward-orbit checks, and Lean compile.
No observations, particle species, or fitted parameters are used.
"""
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.optimize import brentq
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else HERE / 'run'
OUT.mkdir(exist_ok=True)
checks = []

def zero(name, expression):
    residual = S.simplify(expression)
    assert residual == 0, (name, residual)
    checks.append(name)

x, q, r, b, K = S.symbols('x q r b K', positive=True)
mu = 1 - 1/(1+x)**2
A = S.factor(x*S.diff(mu,x)/mu)
zero('response_elasticity', A - 2/((1+x)*(2+x)))
Aq = 2*q**2/(1+q)
zero('eliminate_acceleration_scale', A.subs(x, 1/q-1)-Aq)
beta = S.Rational(1,2)-(1+q)/(1+q+2*q**2)
zero('spherical_exterior_slope', (1+Aq)*(2*beta-1)+2)
zero('quarter_slope_value', beta.subs(q,S.Rational(1,2))+S.Rational(1,4))
zero('quarter_slope_unique_factor', (beta+S.Rational(1,4)) -
     (2*q-1)*(3*q+1)/(4*(1+q+2*q**2)))
zero('quarter_mass_ratio', (1/(1-q*q)).subs(q,S.Rational(1,2))-S.Rational(4,3))
zero('quarter_epicyclic_ratio', (2+2*beta).subs(q,S.Rational(1,2))-S.Rational(3,2))
zero('newtonian_slope_limit', beta.subs(q,0)+S.Rational(1,2))
zero('deep_slope_limit', beta.subs(q,1))
zero('unique_radius_for_point_mass', (S.sqrt(4*K/(3*b)))**2*(b*S.Rational(3,4))-K)

# Differentiation of the actual implicit spherical equation; the orbital
# slope is not inserted into this calculation.
g = S.Function('g')(r)
mug = 1 - 1/(1+g/b)**2
flux = r*r*g*mug
dg_solution = S.solve(S.diff(flux,r),S.diff(g,r))[0]
orbital_beta = S.factor((1+r*dg_solution/g)/2)
zero('differentiate_implicit_flux', orbital_beta.subs(g,b*(1/q-1))-beta)

# Enclosed baryonic mass M(r) may vary: m=dlogM/dlogr.
m = S.symbols('m', real=True)
beta_extended = S.Rational(1,2)+(m-2)*(1+q)/(2*(1+q+2*q*q))
zero('extended_spherical_source', (1+Aq)*(2*beta_extended-1)-(m-2))

# Real negative controls: other standard kernels do not predict 4/3.
simple = x/(1+x)
standard = x/S.sqrt(1+x*x)
As = S.simplify(x*S.diff(simple,x)/simple)
Ast = S.simplify(x*S.diff(standard,x)/standard)
zero('simple_quarter_slope_elasticity',As.subs(x,2)-S.Rational(1,3))
zero('simple_quarter_mass_ratio',1/simple.subs(x,2)-S.Rational(3,2))
zero('standard_quarter_slope_elasticity',Ast.subs(x,S.sqrt(2))-S.Rational(1,3))
zero('standard_quarter_mass_ratio',1/standard.subs(x,S.sqrt(2))-S.sqrt(S.Rational(3,2)))

# Same p(0)=0, p'(0)=1 and saturation, different completion. This disproves
# any claim that the finite-acceleration shape result follows from count alone.
mu_exp = 1-S.exp(-2*x)
A_exp = S.simplify(x*S.diff(mu_exp,x)/mu_exp)
zero('exponential_same_deep_slope',S.diff(mu_exp,x).subs(x,0)-2)
Ae = A_exp.subs(x,S.log(2))  # mu=3/4
beta_exp = S.simplify((Ae-1)/(2*(1+Ae)))
assert abs(float(beta_exp)+0.25) > 0.05

# Independent root solutions at perturbed radii, then numerical log slopes.
# K=GM=1 in arbitrary consistent units; changing b tests scale cancellation.
numeric = []
for bv in [0.2,2.0,20.0]:
    for xv in np.geomspace(0.01,100.0,31):
        muv = xv*(xv+2)/(1+xv)**2
        rv = math.sqrt(1/(bv*xv*muv))
        def velocity(radius):
            def equation(logg):
                gv = math.exp(logg)
                z = gv/bv
                return 2*math.log(radius)+logg+math.log(z*(z+2)/(1+z)**2)
            gv = math.exp(brentq(equation,-60,60,xtol=1e-13))
            return math.sqrt(radius*gv)
        h = 1e-4
        vplus, vminus = velocity(rv*math.exp(h)), velocity(rv*math.exp(-h))
        beta_fd = (math.log(vplus)-math.log(vminus))/(2*h)
        qv = 1/(1+xv)
        predicted = 0.5-(1+qv)/(1+qv+2*qv*qv)
        error = abs(beta_fd-predicted)
        assert error < 2e-8, (bv,xv,error)
        numeric.append({'b':bv,'x':float(xv),'slope_fd':beta_fd,
                        'slope_predicted':predicted,'absolute_error':error})

lean = subprocess.run(['lake','env','lean',str(HERE/'OrbitalShape.lean')],
    cwd=ROOT/'fable_independent_2026/lean_2026',capture_output=True,text=True)
(OUT/'lean.txt').write_text(lean.stdout+lean.stderr)
assert lean.returncode == 0, lean.stdout+lean.stderr
assert 'sorryAx' not in lean.stdout and 'warning:' not in lean.stdout
assert lean.stdout.count('depends on axioms:') == 13
result = {'status':'conditional theorem and bounded numerical checks passed',
    'exact_checks':checks,'exact_check_count':len(checks),
    'numerical_checks':numeric,'numerical_check_count':len(numeric),
    'maximum_absolute_slope_error':max(n['absolute_error'] for n in numeric),
    'lean_theorems':13,'lean_exit_code':lean.returncode,
    'quarter_slope_mass_ratios':{'specified_rational':4/3,'simple':1.5,
                               'standard':math.sqrt(1.5)},
    'same_boundary_different_completion_slope_at_f_3_4':float(beta_exp),
    'non_claims':['No observational confirmation','No global novelty established',
        'No disk or external-field applicability without further calculation',
        'No normalization selection','Not independent of response completion',
        'Action variation and physical identification remain upstream of this Lean file']}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='numerical_checks'},indent=2))
