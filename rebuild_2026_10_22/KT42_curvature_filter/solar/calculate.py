#!/usr/bin/env python3
"""Curvature-only Gaussian filter, with its full adjoint in the STF observable."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import time
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import simpson

HERE = Path(__file__).resolve().parent
RB = HERE.parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load('kt42_solar_kt39', RB / 'KT39_power_curvature/cassini/calculate.py')
P = 1.125
ELL_KPC = 3.0
LENGTHS_KPC = [0., .0001, .001, .003, .01, .03, .1, .3, 1.]


def softened_tidal(r, width):
    """H radial/tangential plus t=Htan-Hrad and its first two derivatives."""
    g, gp, gpp, _, tr, trp, trpp = C.base.prior.radial(r, width)
    gt = g / r
    t = gt - gp
    tp = 3 * gp / r - 3 * g / r**2 - trp
    tpp = 3 * gpp / r - 6 * gp / r**2 + 6 * g / r**3 - trpp
    if width > 0:
        mask = r / width < .1
        v = r[mask] / width
        sums = [np.zeros_like(v) for _ in range(3)]
        for k in range(1, 10):
            power = 2*k
            coef = (-1.)**k / (2**k * math.factorial(k) * (2*k+3)) * (-2*k)
            for deriv in range(3):
                if power >= deriv:
                    fac = math.factorial(power)/math.factorial(power-deriv)
                    sums[deriv] += coef * fac * v**(power-deriv)
        for deriv, arr in enumerate((t, tp, tpp)):
            arr[mask] = C.CC * sums[deriv] / width**(3+deriv)
    return gp, gt, t, tp, tpp


def integrands(r, eta, ell, width, nm=128, newtonian=False):
    rr = np.asarray(r)[:, None]
    mu, w = leggauss(nm)
    mu = mu[None, :]
    pol = 3*mu*mu - 1
    g = rr**-2
    hr, ht, _, _, _ = softened_tidal(rr, width)
    _, _, t, tp, tpp = softened_tidal(rr, width)
    s = ell*ell*(hr*hr + 2*ht*ht)
    hh = s**P
    beta = P*ell*ell*s**(P-1)
    x = g*g + eta*eta + 2*g*eta*mu
    x0 = g*g + eta*eta
    if newtonian:
        c = np.zeros_like(x)
        d = np.zeros_like(x)
    else:
        rm, d1, _, _ = C.base.scaled_R(x+hh)
        rm0, d10, _, _ = C.base.scaled_R(x0+hh)
        c = (rm + x/(x+hh)*d1) - (rm0+x0/(x0+hh)*d10)
        d = beta*(x/(x+hh)*d1-x0/(x0+hh)*d10)
    b = (c*(eta*(3*mu-5*mu**3)+g*(1-3*mu*mu))) @ w
    dd = (d*pol) @ w
    qa = 1.5*b/rr[:, 0]
    # T_a acts on the STF Green test: F_a=(t/3)(3mu^2-1).
    kernel = (hr*tpp+ht*(2*tp/rr-6*t/rr**2))[:, 0]
    qb = rr[:, 0]**3 * dd * kernel / 6
    return qa, qb


def quadrupole(eta, ell, width, nr=4000, nm=128, rmin=1e-8, rmax=1e6, newtonian=False):
    uu = np.linspace(math.log(rmin), math.log(rmax), nr)
    r = np.exp(uu)
    qa, qb = np.zeros(nr), np.zeros(nr)
    for first in range(0, nr, 128):
        sl = slice(first, min(nr, first+128))
        qa[sl], qb[sl] = integrands(r[sl], eta, ell, width, nm, newtonian)
    a = float(np.trapz(qa, uu)); b = float(np.trapz(qb, uu))
    asi = float(simpson(qa, x=uu)); bsi = float(simpson(qb, x=uu))
    return dict(q_signed=a+b, q_A=a, q_B=b, q_simpson=asi+bsi,
                trapz_simpson_absolute_difference=abs(a+b-asi-bsi),
                nr=nr, nm=nm, rmin=rmin, rmax=rmax,
                inner_integrand_A=float(qa[0]), inner_integrand_B=float(qb[0]),
                outer_integrand_A=float(qa[-1]), outer_integrand_B=float(qb[-1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    started = time.monotonic()
    prior = json.loads((RB/'KT39_power_curvature/cassini/adaptive_001/results.json').read_text())
    out = dict(power=P, ell_kpc=ELL_KPC, filter_widths_kpc=LENGTHS_KPC,
               convention='q=STF zz Hessian in a0/rM units; Q2=1.5 q a0/rM; exterior point-Sun regular coefficient',
               footings={}, checks={})
    for foot, a0 in C.old.A0.items():
        rm = math.sqrt(C.old.GM/a0); eta = C.old.GEXT/a0
        ell = ELL_KPC*C.KPC/rm
        ff = out['footings'][foot] = dict(a0=a0, eta=eta, rM_m=rm, ell_rM=ell, rows={})
        for length in LENGTHS_KPC:
            width = length*C.KPC/rm
            coarse = C.base.prior.physical(quadrupole(eta, ell, width), a0)
            fine = C.base.prior.physical(quadrupole(eta, ell, width, nr=8000, nm=256, rmin=1e-10, rmax=1e7), a0)
            ff['rows'][str(length)] = dict(base=coarse, fine=fine)
            key = f'{foot}|a{length}'
            out['checks'][key+'|refinement'] = abs(coarse['x_ceiling']-fine['x_ceiling']) < 2e-4
            pref = 1.5*a0/rm/C.old.CEILING
            out['checks'][key+'|radial_rule'] = fine['trapz_simpson_absolute_difference']*pref < 2e-5
            if length == 0:
                expected = prior['footings'][foot]['p1.125|ell3.0']['fine']['q_signed']
                ff['zero_reference_q'] = expected
                out['checks'][key+'|KT39_reproduction'] = abs(fine['q_signed']/expected-1) < 2e-4
            print(foot, 'a_kpc', length, 'ratio', fine['x_ceiling'], 'qA', fine['q_A'], 'qB', fine['q_B'], flush=True)
        test = quadrupole(eta, ell, .001*C.KPC/rm, nr=1000, nm=64, newtonian=True)
        out['checks'][foot+'|Newtonian_exact_zero'] = test['q_signed'] == 0.
    out['zero_external'] = quadrupole(0., 1000., 10., nr=1000, nm=64)
    out['checks']['zero_external_exact_zero'] = out['zero_external']['q_signed'] == 0.
    r = np.array([1e-8, 1e-5, .01, .1, 1., 10.])
    hr, ht, t, tp, tpp = softened_tidal(r, 1.)
    expected = C.CC/3
    out['central_H'] = dict(hr=float(hr[0]), ht=float(ht[0]), expected=expected)
    out['checks']['central_H'] = abs(hr[0]/expected-1)<1e-12 and abs(ht[0]/expected-1)<1e-12
    out['checks']['kernel_point_limit'] = bool(np.allclose(softened_tidal(r, 0.)[4], 36/r**5, rtol=1e-14))
    out['all_checks_pass'] = all(out['checks'].values())
    out['runtime_seconds'] = time.monotonic()-started
    out['outcome'] = 'Finite grid diagnostic. Pending independent adjoint and exterior-source interpretation checks; no universal no-go.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    print('all checks', out['all_checks_pass'], 'seconds', out['runtime_seconds'], flush=True)
    if not out['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
