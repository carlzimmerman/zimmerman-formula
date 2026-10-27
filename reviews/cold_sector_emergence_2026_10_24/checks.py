"""Bounded checks of the point-baryon square-root-law halo; not formation dynamics."""
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import sympy as sp

r = sp.symbols('r', positive=True)
rho = 1/(4*sp.pi*r*sp.sqrt(1+r*r))
g = sp.sqrt(1+r*r)/r**2
P = 1/(8*sp.pi*r*r)
u = sp.simplify(P/rho)
phi = sp.asinh(r)-sp.sqrt(1+r*r)/r
h = sp.factor(sp.diff(sp.diff(rho,r)/g,r)/g)
lum = sp.simplify(-4*sp.pi*rho*r**3*sp.sqrt(u)*sp.diff(u,r))
identities = {
    'potential': sp.simplify(sp.diff(phi,r)-g),
    'poisson': sp.simplify(sp.diff(r*r*g,r)/(4*sp.pi*r*r)-rho),
    'jeans': sp.simplify(sp.diff(P,r)+rho*g),
    'density_convexity': sp.simplify(h-r**5/(sp.pi*(1+r*r)**sp.Rational(7,2))),
    'conductive_luminosity': sp.simplify(lum-sp.sqrt(2)/(4*sp.sqrt(r)*(1+r*r)**sp.Rational(3,4))),
    'luminosity_derivative': sp.simplify(sp.diff(lum,r)+sp.sqrt(2)*(4*r*r+1)/(8*r**sp.Rational(3,2)*(1+r*r)**sp.Rational(7,4))),
}
assert all(v == 0 for v in identities.values())

def potential(x):
    return math.asinh(x)-math.hypot(1,x)/x

def distribution(x0, xmax=1e10):
    """Abel inversion at E=Phi(x0), integrating radius x=x0 exp(t^2)."""
    E = potential(x0)
    def integrand(t):
        x = x0*math.exp(t*t)
        gg = math.hypot(1,x)/(x*x)
        hh = x**5/(math.pi*(1+x*x)**3.5)
        delta = potential(x)-E
        if t < 1e-5:
            delta = math.hypot(1,x0)/x0*t*t
        if t == 0:
            return 2*(x0**5/(math.pi*(1+x0*x0)**3.5))*math.sqrt(math.hypot(1,x0)/x0)
        return hh*gg*2*t*x/math.sqrt(delta)
    val, err = quad(integrand, 0, math.sqrt(math.log(xmax/x0)), epsabs=1e-13, epsrel=2e-9)
    return val/(math.sqrt(8)*math.pi**2), err/(math.sqrt(8)*math.pi**2)

samples = []
for x in [0.03, 0.1, 0.3, 1., 3., 10., 100.]:
    f, err = distribution(x)
    fshort, _ = distribution(x, 1e8)
    assert f > 0
    assert abs(f-fshort)/f < 1e-6
    samples.append(dict(radius=x, energy=potential(x), f=f, quadrature_error=err,
                        cutoff_relative_change=abs(f-fshort)/f))

reconstruction = []
for x in [0.1, 1., 10.]:
    base = potential(x)
    def integrand(t):
        energy = base+t*t
        logroot = brentq(lambda lx: potential(math.exp(lx))-energy,
                         math.log(x)-1e-10, max(40., energy+3.))
        f, _ = distribution(math.exp(logroot), 1e30)
        return 8*math.pi*math.sqrt(2)*f*t*t
    value, error = quad(integrand, 0, math.sqrt(25), epsabs=1e-10, epsrel=2e-6)
    expected = 1/(4*math.pi*x*math.hypot(1,x))
    relative = abs(value/expected-1)
    assert relative < 2e-5
    reconstruction.append(dict(radius=x, density=value, expected=expected, relative_error=relative))

# Finite mass accounting, independently reconstructing the proposed acceleration.
mass_checks = []
for mb in [0.1, 1., 10.]:
    for mc in [0.1, 1., 10.]:
        for R in [0.3, 1., 3.]:
            a = mc*(mc+2*mb)/(mb*R*R)  # G=1
            recovered = mb*(math.sqrt(1+a*R*R/mb)-1)
            assert math.isclose(mc, recovered, rel_tol=2e-12)
            mass_checks.append([mb,mc,R,a])

result = dict(symbolic_identities={k:str(v) for k,v in identities.items()},
              phase_space_samples=samples, density_reconstruction=reconstruction,
              finite_mass_cases=len(mass_checks),
              non_claims=['No formation attractor', 'No stability theorem',
                          'Infinite-mass idealization', 'No finite-halo completion',
                          'No derivation of a0 or kappa', 'Point baryons only'])
out=Path('reviews/cold_sector_emergence_2026_10_24/run/result.json')
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
