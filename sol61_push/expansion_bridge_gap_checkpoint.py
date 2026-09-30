"""Exact algebra checks for the scoped gapped-cubic checkpoint; no source BVP."""
import json
import sympy as s

P, gap, a0, beta, H, S, M, N, a, adot = s.symbols(
    'P gap a0 beta H S M N a adot', positive=True)
checks = {}
def check(name, expression):
    checks[name] = s.simplify(expression) == 0
    assert checks[name], (name, s.simplify(expression))

b = P*s.sqrt(P**2+gap**2)/a0
check('monotone_flux_derivative', s.diff(b,P)-(2*P**2+gap**2)/(a0*s.sqrt(P**2+gap**2)))
check('infrared_force_ratio', s.limit((P+b)/b,P,0)-(1+a0/gap))
check('zero_gap_mond_flux', s.limit(b,gap,0)-P**2/a0)
C = 2*M**2/(3*a0)
W = M**2*P**2+C*((P**2+gap**2)**s.Rational(3,2)-gap**3)
check('polarization_force', s.diff(W,P)/(2*M**2)-P-b)
A = s.Rational(3,2)*M**2*S
B = beta*M**2*gap**3/3
L = -A*a*adot**2/N-B*N**2*a**4/adot
constraint = s.diff(L,N).subs(adot,N*a*H)/(a**3)
check('homogeneous_lapse',constraint-(A*H**2-2*B/H))
# At constant H and N=1, d/dt is H*a*d/da after substituting adot=H*a.
dL_dadot = s.diff(L,adot).subs({N:1,adot:H*a})
scale_euler = s.diff(L,a).subs({N:1,adot:H*a})-H*a*s.diff(dL_dadot,a)
check('constant_H_scale_equation',scale_euler-3*a**2*(A*H**2-2*B/H))
check('vacuum_H_cubed', (A*H**2-2*B/H).subs(gap**3,9*S*H**3/(4*beta)))
check('joint_gap_coefficient', ((beta*gap/(2*H))**3).subs(gap**3,9*S*H**3/(4*beta))-(3*S/8)*(3*beta**2/4))
print(json.dumps({'scope':'exact algebra only; no full dynamics or observational matching',
                  'checks':checks,'passed':len(checks),
                  'target_gap_ratio_lower_bound':float((24*s.pi)**s.Rational(1,3))},indent=2))
