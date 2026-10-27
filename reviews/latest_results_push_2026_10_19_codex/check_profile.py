"""Bounded numerical cross-check of an analytic projected Jeans discriminator.

No observational data or kinetic confinement simulations are used.
Run through the documented computation-audit contract.
"""
import argparse
import json
import math
from pathlib import Path

from scipy.integrate import quad


def closed(y):
    if y == 0:
        return 1.0
    return 1.5 * (1 + y*y) * (2/3 + y*y - y*(1+y*y)*math.atan(1/y))


def projected(y):
    # Direct LOS projection of the integrated isotropic Jeans equation.
    # r^2 = y^2 + z^2; Plummer scale a=1 and V_x^2=1.
    denom = quad(lambda z: (1+y*y+z*z)**(-2.5), 0, math.inf,
                 epsabs=2e-12, epsrel=2e-12)[0]
    numer = quad(lambda z: (1+y*y+z*z)**(-2.5)
                 * (z*z/(y*y+z*z) if y*y+z*z else 1),
                 0, math.inf, epsabs=2e-12, epsrel=2e-12)[0]
    return numer / denom


def compact(y):
    # A second, compact-domain quadrature, used in the all-aperture integral.
    if y == 0:
        return 1.0
    q2 = y*y / (1+y*y)
    return 1.5 * quad(lambda u: (1-u*u)*u*u/(q2+(1-q2)*u*u),
                      0, 1, epsabs=2e-12, epsrel=2e-12)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    ap.add_argument('--mutate', action='store_true')
    args = ap.parse_args()
    grid = [0, .01, .1, .25, .5, 1, 2, 5, 10]
    rows = []
    checks = []
    for y in grid:
        fc = closed(y) * (1.2 if args.mutate else 1)
        fp, fs = projected(y), compact(y)
        err = max(abs(fc-fp), abs(fp-fs))
        rows.append(dict(R_over_a=y, closed=fc, direct_projection=fp,
                         compact_projection=fs, max_abs_error=err))
        checks.append(err < 2e-8)
    global_value, global_error = quad(
        lambda y: 2*y/(1+y*y)**2 * compact(y), 0, math.inf,
        epsabs=2e-10, epsrel=2e-10)
    checks += [abs(global_value-1/3) < 2e-9,
               abs(projected(1)-(5-1.5*math.pi)) < 2e-10,
               abs(compact(1e5)-.2) < 2e-9,
               abs(projected(0)-1) < 2e-10]
    result = dict(
        assertion_tested='The closed Plummer/isotropic logarithmic-force projection equals two numerical integrals on nine named radii; its whole-tracer moment equals 1/3 and its endpoint limits agree',
        mutate=args.mutate, grid=rows, whole_tracer_moment=global_value,
        quadrature_error_estimate=global_error,
        checks=len(checks), passed=sum(checks), all_passed=all(checks),
        non_claims=['No observation is fitted', 'No isotropy-independent resolved-profile prediction',
                    'No finite-mass or finite-core physical realization',
                    'No numerical experiment on the analytic confinement program'])
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['mutate','whole_tracer_moment','checks','passed','all_passed']}))
    if not all(checks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
