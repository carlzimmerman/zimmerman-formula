"""Constituent checks for the H1 direct-energy obstruction; proof in report."""
import argparse
import json
from pathlib import Path
import sympy as s

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
checks = []
def check(name, ok, detail=''):
    checks.append(dict(name=name, passed=bool(ok), detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail), flush=True)

g, r, amplitude, beta = s.symbols('g r amplitude beta', positive=True)
actual = g+r*r/(3*g)-r
quadratic = g*g/(3*r)
defect = (g-r)**3/(3*g*r)
check('Angular remainder factorization', s.factor(quadratic-actual-defect) == 0)
derivative = s.factor(s.diff(defect, g))
check('Remainder derivative', s.factor(derivative-(g-r)**2*(2*g+r)/(3*g*g*r)) == 0)
t = s.symbols('t', nonnegative=True)
factor = s.factor((derivative*r/g).subs(r, t*g))
check('Derivative normalized factor', factor == (t-1)**2*(t+2)/3, factor)
# On 0 <= t <= 1, this factor lies in [0, 2/3] since its derivative is t^2-1.
check('Derivative factor monotonic', s.simplify(s.diff(factor, t)-(t*t-1)) == 0)
check('Derivative factor endpoints', factor.subs(t, 0) == s.Rational(2, 3) and factor.subs(t, 1) == 0)

# Radial divergence in R^3: div(rhat)=2/r and div(rhat/r)=1/r^2.
check('Coulomb square divergence', s.diff(r*r, r)/r**2 == 2/r)
check('Hardy square divergence', s.diff(r*r/r, r)/r**2 == 1/r**2)
q, K, J, a = s.symbols('q K J a', positive=True)
check('Sharp square optimizer', s.expand((K+a*a-2*a*q).subs(a,q)) == K-q*q)
check('Hardy square coefficient', K+J/4-J/2 == K-J/4)

# Critical singular density |psi|^2 = amplitude^2/r near origin.
critical_pdf = 4*s.pi*amplitude**2*r
critical_D = s.integrate(defect*critical_pdf, (r, 0, g))
check('Critical cubic remainder', s.simplify(critical_D-s.pi*amplitude**2*g**3/3) == 0, critical_D)
critical_psi = amplitude/s.sqrt(r)
kinetic_density = s.simplify(4*s.pi*r*r*s.diff(critical_psi,r)**2)
check('Critical state has logarithmic gradient divergence', kinetic_density == s.pi*amplitude**2/r, kinetic_density)
energy_cubic = -critical_D/g**3
check('Subtracted critical direct energy has negative cubic', energy_cubic > 0 if args.mutate else energy_cubic < 0,
      energy_cubic)

# Optimizer's exact direct energy has a quartic, not cubic, first remainder.
z = beta*g
energy = (z-s.Rational(3,2)+1/z-(s.Rational(1,2)+1/z)*s.exp(-2*z))/beta
check('Optimizer direct energy quadratic', s.limit(energy/g**2,g,0) == beta/3)
check('Optimizer direct energy no cubic', s.limit((energy-beta*g*g/3)/g**3,g,0) == 0)
check('Optimizer subtracted energy quartic negative', s.limit((energy-beta*g*g/3)/g**4,g,0) == -beta**3/15)
check('Optimizer direct flux linear', s.limit(s.diff(energy,g)/g,g,0) == 2*beta/3)
result = dict(checks=checks, mutation=args.mutate,
              scope='Fixed isotropic normalized H1 state; direct mean-norm field-energy functional, optionally subtracting its quadratic term.',
              non_claims=['Not an obstruction to all response prescriptions','Not a theorem for source-dependent states or extra operators'])
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
passed=sum(c['passed'] for c in checks)
print(str(passed)+'/'+str(len(checks))+' checks passed',flush=True)
raise SystemExit(0 if passed == len(checks) else 1)
