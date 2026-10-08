"""Sharp state inequality and independently selected response, not cosmology.

The universal proof is in REPORT.md. This script verifies exact constituents
and bounded, independent quadratures. The response rule is an explicit input.
"""
import argparse
import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar
import sympy as S

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
ap.add_argument('--mutate', action='store_true')
args = ap.parse_args()
checks = []


def check(name, ok, detail=''):
    checks.append(dict(name=name, passed=bool(ok), detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + str(detail), flush=True)


r, beta, z, t, lam = S.symbols('r beta z t lambda', positive=True)
pdf = 4*beta**3*r**2*S.exp(-2*beta*r)
moments = {}
for k, expected in [(0, 1), (-1, beta), (1, 3/(2*beta)), (2, 3/beta**2)]:
    moments[k] = S.integrate(pdf*r**k, (r, 0, S.oo))
    check('Optimizer moment '+str(k), S.simplify(moments[k]-expected) == 0, moments[k])
K = S.integrate(pdf*beta**2, (r, 0, S.oo))
check('Sharp bound saturated by optimizer', moments[-1]**2 <= (S.Rational(99, 100) if args.mutate else 1)*K,
      'q^2=beta^2=K; mutated bound is deliberately too strong')
psi = S.sqrt(beta**3/S.pi)*S.exp(-beta*r)
lap = S.diff(r*r*S.diff(psi, r), r)/r**2
check('Optimizer Coulomb equation', S.simplify(-lap-2*beta/r*psi+beta**2*psi) == 0)
check('No point delta flux', S.limit(r*r*S.diff(psi, r), r, 0) == 0)

# Direct angular-averaged radial integration, before simplifying its answer.
p = 4*t*t*S.exp(-2*t)
U = S.integrate(p*(z+t*t/(3*z)), (t, 0, z)) + S.integrate(p*(t+z*z/(3*t)), (t, z, S.oo))
F = z-S.Rational(3, 2)+1/z-(S.Rational(1, 2)+1/z)*S.exp(-2*z)
check('Selected response closed form', S.simplify(U-S.Rational(3, 2)-F) == 0)
check('Deep susceptibility', S.limit(F/z**2, z, 0) == S.Rational(1, 3))
check('High field offset', S.limit(z-F, z, S.oo) == S.Rational(3, 2))
check('High field next term', S.limit(z*(F-z+S.Rational(3, 2)), z, S.oo) == 1)
check('Origin expansion distinguishes P2', S.simplify(S.limit((F-z**2/3)/z**4, z, 0)+S.Rational(1, 15)) == 0)

# Positive angular representation: derivatives of A(g,R)-R in each branch.
gg, rr = S.symbols('g R', positive=True)
Ainside = gg+rr**2/(3*gg)-rr
Aoutside = gg**2/(3*rr)
check('Angular branch matching value', S.simplify((Ainside-Aoutside).subs(gg, rr)) == 0)
check('Angular branch matching derivative', S.simplify(S.diff(Ainside-Aoutside, gg).subs(gg, rr)) == 0)
check('Angular inner second derivative', S.simplify(S.diff(Ainside, gg, 2)-2*rr**2/(3*gg**3)) == 0)
check('Angular outer second derivative', S.simplify(S.diff(Aoutside, gg, 2)-2/(3*rr)) == 0)

# P2 moments from beta integrals, independently of the prior implementation.
h = S.symbols('h', positive=True)
def p2moment(k):
    a, b = S.Rational(k+3, 2), S.Rational(4-k, 2)
    return S.simplify(S.Rational(15, 4)*h**k*S.gamma(a)*S.gamma(b)/S.gamma(a+b))
q2 = p2moment(-1)
k2 = S.simplify(S.Rational(49*15, 16)/h**2*S.gamma(S.Rational(5, 2))*S.gamma(3)/S.gamma(S.Rational(11, 2)))
check('P2 normalization', p2moment(0) == 1)
check('P2 exact energy excess', S.simplify(k2/q2**2) == S.Rational(28, 27), k2/q2**2)
a0 = 3/beta
check('Optimizer plateau equals a0 over two', S.simplify(moments[1]-a0/2) == 0)
check('Operator dictionary optimizer', S.simplify(lam/K/a0**2) == lam/9)
check('Operator dictionary P2', S.simplify(lam/k2/(3/q2)**2) == 3*lam/28)
check('Variance dictionary optimizer', S.simplify(2*lam*moments[2]/a0**2) == 2*lam/3)

# Finite H1 gamma family, all at q=1; tests the square identity independently.
gamma_rows = []
for kk in (2.5, 3., 4., 6., 10.):
    bb = (kk-1)/2
    norm = (2*bb)**kk/math.gamma(kk)
    def radial(rrr):
        return norm*rrr**(kk-1)*math.exp(-2*bb*rrr)
    def slope(rrr):
        return (kk-3)/(2*rrr)-bb
    knum = quad(lambda v:radial(v)*slope(v)**2, 0, math.inf, epsabs=1e-10)[0]
    sq = quad(lambda v:radial(v)*(slope(v)+1)**2, 0, math.inf, epsabs=1e-10)[0]
    kexact = (kk-1)**2/(4*(kk-2))
    check('Gamma square identity k='+str(kk), abs(knum-1-sq) < 1e-9 and abs(knum-kexact) < 1e-9,
          dict(K=knum, square=sq))
    gamma_rows.append(dict(shape=kk, K=knum, square=sq))

mp.mp.dps = 45
def response(g):
    zz = 3*mp.mpf(float(g))  # a0=1, beta=3
    return float((zz-mp.mpf('1.5')+1/zz-(mp.mpf('.5')+1/zz)*mp.exp(-2*zz))/3)

quadratures = []
for gval in (.001, .01, .1, 1., 10., 100.):
    # A(g,R)-R avoids subtracting two close expectations.
    radial = lambda v:108*v*v*math.exp(-6*v)
    inside = quad(lambda v:radial(v)*(gval+v*v/(3*gval)-v), 0, gval, epsabs=1e-14, epsrel=1e-11)[0]
    outside = quad(lambda v:radial(v)*gval*gval/(3*v), gval, math.inf, epsabs=1e-14, epsrel=1e-11)[0]
    measured = inside+outside
    rel = abs(measured/response(gval)-1)
    check('Direct response quadrature g='+str(gval), rel < 1e-8, rel)
    quadratures.append(dict(g=gval, response=measured, relative_error=rel))

def compare(logb):
    b = math.exp(logb)
    p2 = math.sqrt(b*b+b)
    selected = brentq(lambda g:response(g)-b, b, b+1., xtol=1e-15, rtol=1e-14)
    return dict(b=b, g_P2=p2, g_selected=selected, relative_excess=selected/p2-1)

grid = [compare(v) for v in np.linspace(math.log(1e-8), math.log(1e8), 161)]
imax = max(range(len(grid)), key=lambda i:grid[i]['relative_excess'])
lo, hi = math.log(grid[imax-1]['b']), math.log(grid[imax+1]['b'])
opt = minimize_scalar(lambda v:-compare(v)['relative_excess'], bounds=(lo, hi), method='bounded')
peak = compare(opt.x)
check('Bounded force comparison within two percent', max(abs(x['relative_excess']) for x in grid) < .02 and abs(peak['relative_excess']) < .02,
      peak)

# Direct P2/optimizer overlap at q=1, not an assumed closeness theorem.
hh = 1.5
psip = lambda v:math.sqrt(15*hh**4/(8*math.pi))*(v*v+hh*hh)**(-1.75)
psic = lambda v:math.exp(-v)/math.sqrt(math.pi)
overlap = quad(lambda v:4*math.pi*v*v*psip(v)*psic(v), 0, math.inf, epsabs=1e-12)[0]
check('Normalized state overlap admissible', 0 < overlap < 1, overlap)
result = dict(checks=checks, gamma_rows=gamma_rows, quadratures=quadratures, comparison=grid, refined_peak=peak,
              state_overlap=overlap, P2_energy_ratio='28/27', operator_bound='lambda/9',
              mutation=args.mutate, non_claims=['No global certified force maximum','No physical vacuum dictionary derivation','No covariant completion','No data fit'])
Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
passed = sum(x['passed'] for x in checks)
print(str(passed)+'/'+str(len(checks))+' checks passed', flush=True)
raise SystemExit(0 if passed == len(checks) else 1)
