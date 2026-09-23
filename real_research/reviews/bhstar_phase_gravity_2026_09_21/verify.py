#!/usr/bin/env python3
"""Finite checks of the conditional phase-gravity law. No observed time series.

Run: python3 verify.py OUTPUT_DIRECTORY
Requires numpy, scipy, sympy. All mock inputs are deterministic.
"""
import json
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import simpson
from scipy.optimize import brentq
import sympy as sp

G = 6.67430e-11
C = 299792458.0
AU = 149597870700.0
MSUN = 1.98847e30
YEAR = 31557600.0
MP = 1.67262192369e-27
SIGMA = 5.670374419e-8
MU_H = 1.4
CHECKS = []


def check(name, condition, **details):
    record = dict(name=name, passed=bool(condition), **details)
    CHECKS.append(record)
    if not condition:
        raise AssertionError(json.dumps(record))


def exact_checks():
    A, R, q, acc, c, kap, sig, T, mass, grav = sp.symbols(
        'A R q acc c kap sig T mass grav', positive=True)
    g = A/q**2 + R*acc
    check('phase invariant', sp.simplify(q**2*(g-R*acc)-A) == 0)
    x1, x2, x3 = sp.symbols('x1 x2 x3')
    determinant = sp.Matrix([[1, x, A+R*x] for x in (x1, x2, x3)]).det()
    check('three-epoch determinant', sp.expand(determinant) == 0)
    check('two-epoch radius recovery', sp.cancel(
        ((A+R*x1)-(A+R*x2))/(x1-x2)-R) == 0)
    check('corrected Eddington factor', sp.simplify(
        kap*sig*T**4/(c*(g-R*acc))-kap*sig*T**4*q**2/(c*A)) == 0)
    qinv, qinv2, speed2 = sp.symbols('qinv qinv2 speed2', positive=True)
    mean_g = A*qinv2
    mean_gq = A*qinv-R*speed2
    check('cycle-moment inverse', sp.simplify(
        ((mean_g/qinv2)*qinv-mean_gq)/speed2-R) == 0)
    eps, om, phase = sp.symbols('eps om phase', real=True)
    wave = 1+eps*sp.cos(phase)
    qdd = -eps*om**2*sp.cos(phase)
    gmax = (grav*mass/(R**2*wave**2)+R*qdd).subs(phase, 0)
    check('turning-point mass identity', sp.simplify(
        gmax*R**2*(1+eps)**2/grav -
        (mass-eps*om**2*R**3*(1+eps)**2/grav)) == 0)
    s = sp.symbols('s')
    for j in range(6):
        w = s**2*(1-s)**2*(2*s-1)**j
        check('weight endpoints %d' % j,
              all(sp.diff(w, s, k).subs(s, endpoint) == 0
                  for k in (0, 1) for endpoint in (0, 1)))


def waveform(t, period, variant):
    """Analytic q, q', q'', normalized to q(0)=1."""
    if variant == 0:
        modes = [(1, .08, 0.0)]
    elif variant == 1:
        modes = [(1, .08, .2), (2, .017, .7)]
    else:
        modes = [(1, .07, -.3), (2, .012, .8), (3, .005, .1)]
    om = 2*math.pi/period
    q = np.ones_like(t)
    dq = np.zeros_like(t)
    ddq = np.zeros_like(t)
    norm = 1+sum(a*math.sin(p) for k, a, p in modes)
    for k, a, phase in modes:
        q += a*np.sin(k*om*t+phase)
        dq += a*k*om*np.cos(k*om*t+phase)
        ddq -= a*(k*om)**2*np.sin(k*om*t+phase)
    return q/norm, dq/norm, ddq/norm, modes


def weak_fit(t, q, g):
    span = t[-1]-t[0]
    s = (t-t[0])/span
    p = Polynomial([0, 1])
    rows, rhs = [], []
    for j in range(6):
        w = p**2*(1-p)**2*(2*p-1)**j
        rows.append([simpson(q**-2*w(s), x=s),
                     simpson(q*w.deriv(2)(s), x=s)])
        rhs.append(simpson(g*w(s), x=s))
    design, rhs = np.asarray(rows), np.asarray(rhs)
    coef, _, rank, singular = np.linalg.lstsq(design, rhs, rcond=None)
    fitted_A, fitted_R = coef[0], coef[1]*span**2
    residual = np.linalg.norm(rhs-design@coef)/np.linalg.norm(rhs)
    return dict(A=float(fitted_A), R=float(fitted_R),
                M=float(fitted_A*fitted_R**2/G), rank=int(rank),
                condition=float(singular[0]/singular[-1]),
                relative_residual=float(residual))


def recovery_tests():
    rows = []
    cases = [(1e4, 100, 30), (1e5, 941, 100), (2e6, 2000, 32)]
    for m_sun, r_au, p_year in cases:
        M, R, P = m_sun*MSUN, r_au*AU, p_year*YEAR
        A = G*M/R**2
        for variant in range(3):
            for fraction in (.65, 1.0):
                errors = []
                fits = []
                for n in (257, 513, 1025):
                    t = np.linspace(.13*P, (.13+fraction)*P, n)
                    q, dq, ddq, _ = waveform(t, P, variant)
                    g = A/q**2+R*ddq
                    check('mock positive g %s' % (len(rows),), np.min(g) > 0)
                    fit = weak_fit(t, q, g)
                    error = max(abs(fit['A']/A-1), abs(fit['R']/R-1),
                                abs(fit['M']/M-1))
                    errors.append(error)
                    fits.append(fit)
                check('weak inversion grid convergence %d' % len(rows),
                      errors[-1] < 2e-5 and errors[-1] < errors[0]/100,
                      errors=errors)
                check('weak design identifiable %d' % len(rows),
                      fits[-1]['rank'] == 2 and fits[-1]['condition'] < 1e5)
                # Orthogonal check using analytic acceleration at each epoch.
                slope, intercept = np.polyfit(q*q*ddq*P**2, g*q*q, 1)
                direct_R = slope*P**2
                check('direct versus integral inversion %d' % len(rows),
                      abs(direct_R/R-1) < 1e-10 and abs(intercept/A-1) < 1e-10)
                rows.append(dict(mass_solar=m_sun, radius_au=r_au,
                                 period_rest_year=p_year, waveform=variant,
                                 observed_cycle_fraction=fraction,
                                 grid_errors=errors, final_fit=fits[-1]))
    return rows


def cycle_tests():
    R, M, P = 941*AU, 1e5*MSUN, 100*YEAR
    A = G*M/R**2
    records = []
    for variant in range(3):
        n = 4096
        t = np.arange(n)*P/n
        q, dq, ddq, modes = waveform(t, P, variant)
        g = A/q**2+R*ddq
        a = np.mean(g)/np.mean(q**-2)
        r = (a*np.mean(q**-1)-np.mean(g*q))/np.mean(dq*dq)
        check('cycle moment inversion %d' % variant,
              abs(a/A-1) < 1e-12 and abs(r/R-1) < 1e-10)
        loop = float(np.mean(g*dq)*P/(A*.1))
        check('cycle signed-area null %d' % variant, abs(loop) < 1e-12)
        Q, H = np.fft.fft(q)/n, np.fft.fft(g-a/q**2)/n
        radii = []
        for k, _, _ in modes:
            rk = -H[k]/((k*2*math.pi/P)**2*Q[k])
            check('harmonic radius %d:%d' % (variant, k),
                  abs(rk/R-1) < 1e-10)
            radii.append(dict(k=k, radius_au=float(rk.real/AU),
                              imaginary_fraction=float(rk.imag/R)))
        # A different normalization of q must preserve the physical mass.
        scaled = weak_fit(np.linspace(0, P, 1025),
                          waveform(np.linspace(0, P, 1025), P, variant)[0]*2.7,
                          A/waveform(np.linspace(0, P, 1025), P, variant)[0]**2 +
                          R*waveform(np.linspace(0, P, 1025), P, variant)[2])
        check('radius normalization covariance %d' % variant,
              abs(scaled['R']/(R/2.7)-1) < 2e-5 and abs(scaled['M']/M-1) < 2e-5)
        records.append(dict(waveform=variant, harmonic_radii=radii,
                            recovered_mass_solar=a*r*r/G/MSUN))
    return records


def adversarial_tests():
    R, M, P = 941*AU, 1e5*MSUN, 100*YEAR
    A = G*M/R**2
    t = np.linspace(0, P, 2049)
    q, dq, ddq, _ = waveform(t, P, 1)
    g = A/q**2+R*ddq
    # Rest/observer time must not be silently interchanged.
    z = 4.3
    wrong = weak_fit(t*(1+z), q, g)
    check('time-frame error recovered, not hidden',
          abs(wrong['R']/R/(1+z)**2-1) < 2e-6 and
          abs(wrong['M']/M/(1+z)**4-1) < 2e-6)
    # A known extra acceleration outside the two fitted columns must be visible.
    extra = .15*A*np.sin(6*math.pi*t/P+.37)
    bad = weak_fit(t, q, g+extra)
    baseline = weak_fit(t, q, g)
    check('unmodelled acceleration rejected',
          bad['relative_residual'] > 1e4*baseline['relative_residual'] and
          bad['relative_residual'] > 1e-6,
          relative_residual=bad['relative_residual'],
          baseline_residual=baseline['relative_residual'])
    # An error in the span of the model is NOT detected: required limitation.
    hidden = weak_fit(t, q, g+.2*A/q**2+.3*R*ddq)
    check('absorbable systematic evades null',
          hidden['relative_residual'] < 1e-7 and
          abs(hidden['A']/(1.2*A)-1) < 1e-6 and
          abs(hidden['R']/(1.3*R)-1) < 1e-6)
    constant = weak_fit(t, np.ones_like(t), np.full_like(t, A))
    # Exact continuum rank is 1. Quadrature can generate a tiny false column.
    check('constant-radius limit ill-conditioned', constant['condition'] > 1e8)
    # Constant flux magnification cancels; unequal image magnifications do not.
    temperatures = 4662*(1+.025*np.sin(2*math.pi*t/P+.2))
    flux = q*q*(temperatures/temperatures[0])**4
    q_from_flux = np.sqrt(flux/flux[0])*(temperatures[0]/temperatures)**2
    check('relative bolometric radius recovered',
          np.max(abs(q_from_flux-q/q[0])) < 1e-14)
    common = np.sqrt((37*flux)/(37*flux[0]))*(temperatures[0]/temperatures)**2
    check('common magnification cancels', np.max(abs(common-q_from_flux)) < 1e-14)
    drift = 1+.1*np.sin(2*math.pi*t/P)
    wrong_q = np.sqrt(drift*flux/flux[0])*(temperatures[0]/temperatures)**2
    check('variable magnification does not cancel', np.max(abs(wrong_q-q_from_flux)) > .04)
    return dict(observer_time_radius_bias=wrong['R']/R,
                observer_time_mass_bias=wrong['M']/M,
                extra_acceleration_fit=bad, undetectably_biased_fit=hidden,
                constant_radius_condition=constant['condition'])


def numerical_implications():
    # Published stack summaries are inputs, not independent time samples.
    stacks = [('median', -2.2, 941), ('luminous', -2.5, 1989),
              ('intermediate', -1.9, 900), ('faint', -2.5, 747)]
    density_rows = []
    a_dense = C/2*math.sqrt(G*MU_H*MP*1e10*1e6)
    for label, logg, r_au in stacks:
        g_static = 10**logg/100
        nmax = 4*g_static*g_static/(C*C*G*MU_H*MP)/1e6
        radius_ratio = math.sqrt(g_static/a_dense)
        # Independent recomputation via the mass and transition radius.
        M = g_static*(r_au*AU)**2/G
        transition = math.sqrt(G*M/a_dense)
        check('density geometry cancellation '+label,
              abs(transition/(r_au*AU)-radius_ratio) < 1e-14)
        density_rows.append(dict(stack=label, logg_cgs=logg,
                                 nmax_cm3=nmax, radius_ratio_at_n1e10=radius_ratio))
    floors = []
    for r_au in (941, 2000):
        for p_yr in (30, 32, 100):
            eps = .1
            floor = 4*math.pi**2*eps*(1+eps)**2*(r_au*AU)**3/(G*(p_yr*YEAR)**2)
            max_R = r_au*AU*(1+eps)
            dd_R = -eps*r_au*AU*(2*math.pi/(p_yr*YEAR))**2
            check('mass floor equality %s %s' % (r_au, p_yr),
                  abs(G*floor/max_R**2+dd_R) < 1e-16)
            floors.append(dict(mean_radius_au=r_au, assumed_period_rest_yr=p_yr,
                               assumed_fractional_radius_amplitude=eps,
                               mass_floor_solar=floor/MSUN))
    R, P, M = 941*AU, 32*YEAR, 1e4*MSUN
    emax = brentq(lambda e: 4*math.pi**2*e*(1+e)**2*R**3/(G*P**2)-M, 0, 1)
    check('low mass amplitude ceiling', .01 < emax < .015)
    return dict(static_density_ceiling=density_rows, illustrative_mass_floors=floors,
                maximum_sinusoidal_radius_amplitude_for_1e4Msun_941AU_32yr=emax,
                observational_fit_performed=False)


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: verify.py OUTPUT_DIRECTORY')
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    exact_checks()
    result = dict(claim='Conditional photospheric phase-gravity law',
                  status='synthetic and exact checks; no observational validation',
                  weak_inversions=recovery_tests(), cycle_tests=cycle_tests(),
                  adversarial=adversarial_tests(), implications=numerical_implications())
    result['checks'] = CHECKS
    result['all_passed'] = all(c['passed'] for c in CHECKS)
    result['software'] = dict(python=sys.version, numpy=np.__version__, sympy=sp.__version__)
    (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(checks=len(CHECKS), passed=result['all_passed'],
                         weak_inversion_cases=len(result['weak_inversions']),
                         max_final_recovery_error=max(r['grid_errors'][-1]
                             for r in result['weak_inversions']),
                         amplitude_limit=result['implications'][
                             'maximum_sinusoidal_radius_amplitude_for_1e4Msun_941AU_32yr'],
                         extra_acceleration_residual=result['adversarial'][
                             'extra_acceleration_fit']['relative_residual']), indent=2))


if __name__ == '__main__':
    main()
