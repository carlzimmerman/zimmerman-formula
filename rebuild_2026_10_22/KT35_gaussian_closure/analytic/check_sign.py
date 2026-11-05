#!/usr/bin/env python3
"""Finite checks for the separately documented analytic sign argument."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss, legval
from scipy.integrate import quad, simpson
from scipy.special import gammainc


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    mixture = []
    for h in np.logspace(-3, 3, 19):
        rec, err = quad(lambda u: 2/(math.pi*h)*math.atan(
            h*math.sqrt(1-u*u)/(2*u*u)), 0, 1, epsabs=1e-11,
            epsrel=1e-11, limit=200)
        exact = 1/(h*(math.sqrt(.25+1/h)+.5))
        mixture.append(dict(h=float(h), relative_error=rec/exact-1,
                            quadrature_error_estimate=err))
    mu, w = leggauss(400)
    max_angular_error = 0.
    signs = []
    for eta in [2.050919377652051, 2.478553037829984]:
        for g in [.01, .1, .5, 1., 3., 5., 10., 100.]:
            for t in [.01, .1, 1., 10., 100.]:
                hh = g*g+eta*eta+t
                cc = .5*(hh+math.sqrt(hh*hh-4*g*g*eta*eta))
                zz = g*eta/cc
                coeff = [2*(-zz)**ell/((2*ell+1)*math.sqrt(cc)) for ell in range(4)]
                kernel = 1/np.sqrt(hh+2*g*eta*mu)
                for ell in range(4):
                    numeric = float((kernel*legval(mu, [0.]*ell+[1.]))@w)
                    max_angular_error = max(max_angular_error, abs(numeric-coeff[ell]))
                b = -2*(g*coeff[2]+eta*coeff[3])
                c = 2*(g*coeff[2]+eta*(3*coeff[3]+2*coeff[1])/5)
                signs.extend([3*b < 0, 3*b+5*c < 0])
    bounds = {}
    for footing, a0, width in [('canonical', 9.3603e-11, .32), ('alt', 1.1312e-10, .47)]:
        eta = 2.32e-10/a0
        r = np.exp(np.linspace(math.log(1e-5), math.log(1e3), 12000))
        g = gammainc(1.5, .5*(r/width)**2)/r**2
        tt = gammainc(2.5, .5*(r/width)**2)
        h = np.hypot(1/r**2, eta)
        app = (3*h+10)/(4*h**4.5*(h+4)**1.5)
        integrand = 16/35*eta*eta*tt*g**3/r*app
        qcut = 5.2e-27/(1.5*a0/math.sqrt((6.6743e-11*1.98892e30)/a0))
        bounds[footing] = dict(epsilon_upper=width, supplementary_bound_integral=float(
            simpson(integrand, x=np.log(r))), required_q_magnitude=qcut,
            sufficient=False, certified_numerical_integral=False)
    result = dict(outcome='finite floating checks only; analytic theorem is separately self-reviewed',
                  mixture=mixture, kernel_grid_count=len(signs)//2,
                  max_angular_absolute_error=max_angular_error,
                  all_tested_endpoint_signs_negative=all(signs), unsuccessful_bound=bounds)
    result['all_checks_pass'] = bool(all(signs) and max_angular_error < 1e-10 and max(
        abs(row['relative_error']) for row in mixture) < 1e-8)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'mixture'}, indent=2))
    if not result['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
