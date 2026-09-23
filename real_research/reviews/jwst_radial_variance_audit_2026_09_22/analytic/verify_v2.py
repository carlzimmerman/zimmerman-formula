"""Exact finite algebra/enclosure audit; stopping proof is in THEOREM.md."""
import json
from fractions import Fraction as Q
from pathlib import Path
import sympy as S

def exact(expr):
    return S.cancel(S.expand(expr))


HERE = Path(__file__).resolve().parent
s, z = S.symbols('s z', real=True)
a, A = S.symbols('a A', positive=True)
c = S.Rational(20, 9)
k = A/(a+s)
F = A/2*S.log((a+1)/(a+s))
k1 = A/(a+1)
offset = k1**2/11
b = -2*F-S.Rational(2, 3)*s*k
J = A**2*(S.log((a+1)/(a+s))+a/(a+1)-a/(a+s))
a0 = offset+(c-1)*(1-s)+F**2+J/3
U = a0+b*z+c*z**2
m = F-z


def L(poly):
    p = S.Poly(poly, z)
    if p.degree() > 2:
        raise ValueError('Only the explicitly derived angular moments are implemented')
    angular = p.nth(0)+p.nth(2)*(S.Rational(3, 10)*s+z**2/10)
    return 2*z*S.diff(poly, s)+S.diff(poly, z)+k*(angular-poly)


def log_part(x, n):
    lo = 2*sum((x**(2*j+1)/Q(2*j+1) for j in range(n)), Q(0))
    return lo, lo+2*x**(2*n+1)/(Q(2*n+1)*(1-x*x))


def enclosure(n):
    l2, u2 = log_part(Q(1, 3), n)
    lr, ur = log_part(Q(1, 129), n)
    return 6*l2+lr, 6*u2+ur


residual = S.factor(exact(L(U)+2*m))
boundary = exact(U.subs(s, 1)-z**2)
square = S.Rational(11, 9)*(z-3*k1/11)**2
checks = {
    'F_derivative': exact(S.diff(F, s)+k/2) == 0,
    'J_derivative': exact(S.diff(J, s)+s*k**2) == 0,
    'a0_derivative': exact(S.diff(a0, s)-(1-c+k*b/2)) == 0,
    'first_moment_generator': exact(L(m)+1) == 0,
    'first_moment_boundary': exact(m.subs(s, 1)+z) == 0,
    'generator_residual': exact(residual+4*A*a*z**2/(3*(a+s)**2)) == 0,
    'boundary_square': exact(boundary-square) == 0,
    'offset_derivative_zero': exact(L(U-offset)-L(U)) == 0,
}
# Symbolic identities above plus a,A>0, s>=0, z real prove the residual sign.
# Negative fixture tests the same boundary minimum formula, not a mode boolean.
negative_boundary = exact((boundary-offset).subs(z, 3*k1/11))
checks['negative_boundary_value'] = exact(negative_boundary+offset) == 0
checks['negative_boundary_is_negative'] = bool(negative_boundary.is_negative)

rows = []
for n in (16, 20):
    lo, hi = enclosure(n)
    Au = 8/lo
    # Every term is bounded individually by positive rational bounds.
    upper = Q(16)+Q(11, 9)+(Au*Q(64, 65))**2/11+Au**2/3*(hi-Q(64, 65))
    vertex_hi = Q(3, 11)*Au*Q(64, 65)
    checks[f'log_interval_{n}'] = Q(4) < lo < hi < Q(5)
    checks[f'positive_integral_factor_{n}'] = lo > Q(64, 65)
    checks[f'central_upper_{n}'] = upper < Q(1073, 50) < Q(112, 5)
    checks[f'negative_vertex_in_domain_{n}'] = 0 < vertex_hi < 1
    rows.append({'N':n, 'log65_lower':str(lo), 'log65_upper':str(hi),
        'central_upper_rational':str(upper), 'central_upper_display':float(upper),
        'certified_simple_central_bound':'1073/50', 'certified_variance_bound':'273/50'})

central = exact(a0.subs({s:0, a:S.Rational(1, 64), A:8/S.log(65)}))
target = 16+S.Rational(11, 9)+(S.Rational(512, 65)/S.log(65))**2/11+64/(3*S.log(65)**2)*(S.log(65)-S.Rational(64, 65))
checks['central_expression'] = exact(central-target) == 0
checks = {key:bool(value) for key,value in checks.items()}
result = {'checks':checks, 'all_checks_pass':all(checks.values()),
    'residual':str(residual), 'boundary_square':str(square),
    'negative_boundary_minimum':str(negative_boundary), 'central_exact':str(central),
    'central_display':str(S.N(central, 20)), 'enclosures':rows,
    'interpretation':'Algebra and rational arithmetic support the separate model-conditional stopping proof. No novelty or observational certification.'}
(HERE/'certified_v2/result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'checks':checks, 'central_display':result['central_display'], 'residual':str(residual)}))
