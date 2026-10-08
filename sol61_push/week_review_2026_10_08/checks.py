"""Exact halo/vacuum separation and full mu_n pressure checks.

Run with --output FILE, optionally --mutate (deliberately wrong pressure).
Own calculations only; does not import or modify historical campaign scripts.
Numerical convention GM = G = s = 1. Boundary P(infinity)=0.
"""
import argparse
import json
import math
import platform

import scipy
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
parser.add_argument('--mutate', action='store_true')
args = parser.parse_args()
checks = []


def check(name, ok, value=None):
    checks.append(dict(name=name, passed=bool(ok), value=str(value)))
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + str(value))


r, C, G, A, R, Pedge = S.symbols('r C G A R Pedge', positive=True)
half = S.Rational(51, 100) if args.mutate else S.Rational(1, 2)
rho = C / (4*S.pi*G*r**2)
g = C/r
P = half*C*rho
check('Log branch Poisson', S.simplify(S.diff(r*r*g, r)/r**2 - 4*S.pi*G*rho) == 0)
check('Log branch hydrostatic pressure', S.simplify(S.diff(P, r)+rho*g) == 0,
      S.simplify(S.diff(P, r)+rho*g))
Pfinite = C*rho/2 - C*rho.subs(r, R)/2 + Pedge
check('Finite log halo equilibrium', S.simplify(S.diff(Pfinite, r)+rho*g) == 0)
check('Finite log halo boundary', S.simplify(Pfinite.subs(r, R)-Pedge) == 0)
hfinite = S.simplify(Pfinite.subs(Pedge, 0)/(rho*C))
check('Finite log halo half correction', S.simplify(hfinite-(1-r**2/R**2)/2) == 0, hfinite)

# A different positive barotropic self-gravitating power law, 0 < r < R.
rho1 = A/r
g1 = 2*S.pi*G*A
P1 = 2*S.pi*G*A**2*S.log(R/r)
check('Gamma one Poisson', S.simplify(S.diff(r*r*g1, r)/r**2-4*S.pi*G*rho1) == 0)
check('Gamma one hydrostatic barotrope', S.simplify(S.diff(P1, r)+rho1*g1) == 0)
check('Gamma one positive compressibility', S.simplify(S.diff(P1, r)/S.diff(rho1, r)-2*S.pi*G*A*r) == 0)

# Countermodel to identification of the halo half with the vacuum coefficient.
# c=G=rho_L=s=1, n=3, a0=1/3, Mb=3 => C=sqrt(G Mb a0)=1.
n = S.Integer(3)
a0 = 1/n
kvac = a0
khalo = half
check('n three halo amplitude', S.sqrt(3*a0) == 1)
check('n three distinct ratios', khalo != kvac, [khalo, kvac])
area_lambda = S.pi/a0**2 * (8*S.pi)
check('n three violates desired normalization', S.simplify(area_lambda-32*S.pi**2) != 0, area_lambda)

# Exact point-mass P2 equilibrium; previously present in CFG9/CFG44.
M, acc = S.symbols('M a0', positive=True)
gt = S.sqrt((G*M/r**2)**2 + acc*G*M/r**2)
rhoc = S.simplify(S.diff(r*r*gt, r)/(4*S.pi*G*r*r))
Pp2 = acc*M/(8*S.pi*r*r)
check('P2 hydrostatics', S.simplify(S.diff(Pp2, r)+rhoc*gt) == 0)
check('P2 local pressure half', S.simplify(Pp2-rhoc*r*gt/2) == 0)
Pp2finite = Pp2-Pp2.subs(r, R)+Pedge
check('P2 finite boundary correction', S.simplify(Pp2finite.subs(Pedge, 0)/(rhoc*r*gt)-(1-r*r/R**2)/2) == 0)

# Full mu2 = 1-(1+u)^-2, NOT the P2 quadrature kernel.
u = S.symbols('u', positive=True)
mu2 = 1-(1+u)**-2
d = S.simplify(u*S.diff(mu2, u)/mu2)
I2 = 4*S.log(1+u/2)-2*S.log(1+u)
check('mu2 pressure primitive', S.simplify(S.diff(I2, u)-u*u*S.diff(mu2, u)/mu2) == 0)
check('mu2 pressure origin', I2.subs(u, 0) == 0)
h2 = S.simplify((1+d)/(2*u*u*d)*I2)
check('mu2 deep half', S.limit(h2, u, 0) == S.Rational(1, 2))
check('mu2 at one differs from half', abs(float(h2.subs(u, 1))-.5) > .02, h2.subs(u, 1))
check('mu2 high field asymptote', S.limit(h2-S.log(u)/2+S.log(2), u, S.oo) == 0)
r2 = 1/S.sqrt(u*mu2)
rho2 = d/(2*S.pi*r2**3*mu2*(1+d))
check('mu2 exact hydrostatic chain rule', S.simplify(S.diff(I2/(4*S.pi), u)+rho2*u*S.diff(r2, u)) == 0)


def mu(v, nn):
    return -math.expm1(-nn*math.log1p(v))


def dd(v, nn):
    return v*nn*(1+v)**(-nn-1)/mu(v, nn)


def field(rr, nn):
    b = rr**-2
    hi = max(1.0, b+1.0)
    while hi*mu(hi, nn) < b:
        hi *= 2
    return brentq(lambda v: v*mu(v, nn)-b, 0, hi, xtol=1e-30, rtol=1e-13)


def density(rr, nn):
    v = field(rr, nn)
    dv = dd(v, nn)
    return dv/(2*math.pi*rr**3*mu(v, nn)*(1+dv))


rows = []
for nn in (1, 2, 3):
    for uu in (.01, .1, 1., 10., 100.):
        rr = 1/math.sqrt(uu*mu(uu, nn))
        # Direct radial pressure integral; implicit g(r) solved independently.
        prad, err = quad(lambda ell: density(math.exp(ell), nn)*field(math.exp(ell), nn)*math.exp(ell),
                         math.log(rr), math.log(rr)+25, epsabs=1e-13, epsrel=1e-10, limit=150)
        integ = quad(lambda v: v*dd(v, nn), 0, uu, epsabs=1e-13, epsrel=1e-11)[0]
        pu = integ/(4*math.pi)
        hh = prad/(density(rr, nn)*rr*uu)
        rel = abs(prad/pu-1)
        check('Radial versus field pressure n=%s u=%s' % (nn, uu), rel < 2e-8, rel)
        if nn == 2:
            exact_h = float(h2.subs(u, uu))
            check('mu2 closed form u=%s' % uu, abs(hh-exact_h) < 2e-9, hh)
        rows.append(dict(n=nn, u=uu, r=rr, halo_pressure_ratio=hh,
                         vacuum_ratio_if_s_equals_c_sqrt_Grho=1/nn,
                         relative_quadrature_error=rel, quad_error_estimate=err))

result = dict(checks=checks, rows=rows, mutation=args.mutate,
              versions=dict(python=platform.python_version(), sympy=S.__version__, scipy=scipy.__version__),
              statement='Local Newtonian hydrostatics does not select the vacuum coefficient. No cosmological or stability closure claimed.')
with open(args.output, 'w') as f:
    json.dump(result, f, indent=2)
passed = sum(x['passed'] for x in checks)
print('%s/%s checks passed' % (passed, len(checks)))
raise SystemExit(0 if passed == len(checks) else 1)
