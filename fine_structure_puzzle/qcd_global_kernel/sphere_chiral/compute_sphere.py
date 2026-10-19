#!/usr/bin/env python3
"""FSP-008: finite global S4 pion-determinant calculation; no empirical input."""
import hashlib
import json
import math
import pathlib
import sys
import time

import mpmath as mp
import sympy as sp

mp.mp.dps = 50
START = time.monotonic()
MAX_TERMS = 1000
SPLIT = mp.mpf('0.025')


def dec_integral(z, xi=0):
    """Exact resummed expression for integral e^-zx B_xi(x) dx."""
    z, xi = mp.mpf(z), mp.mpf(xi)
    w = z + 12 * xi
    assert z > 0 and w > 0
    nu = mp.sqrt(mp.mpf(9) / 4 - w)
    psi_sum = mp.digamma(mp.mpf(3) / 2 + nu) + mp.digamma(mp.mpf(3) / 2 - nu)
    k2 = mp.mpf(29) / 90 - 4 * xi + 12 * xi**2
    value = (w - 2) / 6 * (psi_sum - mp.log(z)) + mp.mpf(2) / 9 - 2 * xi - k2 / z
    assert abs(mp.im(value)) < mp.mpf('1e-45')
    return mp.re(value)


def psi(z, xi=0):
    return mp.mpf(z) * dec_integral(z, xi)


def get_heat_coefficients():
    """Independent half-integer spectral Euler--Maclaurin coefficients."""
    x = sp.Symbol('x')
    s = sp.Rational(1, 2) / x**2 - sp.Rational(1, 8) / x
    for k in range(15):
        z3 = (sp.Rational(2)**(-3 - 2*k) - 1) * sp.zeta(-3 - 2*k)
        z1 = (sp.Rational(2)**(-1 - 2*k) - 1) * sp.zeta(-1 - 2*k)
        s += (-x)**k / sp.factorial(k) * (z3 - z1 / 4)
    series = sp.series(sp.exp(9*x/4) * s / 3, x, 0, 14).removeO().expand()
    coeff = {j: series.coeff(x, j) for j in range(-2, 14)}
    assert [coeff[j] for j in range(-2, 4)] == [
        sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(29, 90),
        sp.Rational(37, 189), sp.Rational(149, 1890), sp.Rational(179, 10395)]
    return coeff


EXACT_COEFF = get_heat_coefficients()
COEFF = {j: mp.mpf(int(c.p)) / int(c.q) for j, c in EXACT_COEFF.items()}


def shifted_coeff(j, xi):
    return mp.fsum(COEFF[k] * (-12*xi)**(j-k) / mp.factorial(j-k)
                   for k in range(-2, j+1))


def heat_b(x, xi):
    """Direct harmonic sum, independent of digamma implementation."""
    n = int(mp.ceil(mp.sqrt(140/x))) + 4
    assert n <= MAX_TERMS
    value = mp.fsum(mp.mpf((l+1)*(l+2)*(2*l+3)) / 6 * mp.exp(-x*l*(l+3))
                    for l in range(n+1)) * mp.exp(-12*xi*x)
    return (value - 1/(6*x*x) - (mp.mpf(1)/3-2*xi)/x
            - mp.mpf(29)/90 + 4*xi - 12*xi*xi)


def heat_integral(z, xi=0, split=SPLIT, order=10, w_action=False):
    """Independent proper-time quadrature; short early segment asymptotic."""
    z, xi = mp.mpf(z), mp.mpf(xi)
    if w_action:
        low = mp.fsum(shifted_coeff(j, xi) * mp.gammainc(j, 0, z*split) / z**j
                      for j in range(1, order+1))
    else:
        low = mp.fsum(shifted_coeff(j, xi) * mp.gammainc(j+1, 0, z*split) / z**(j+1)
                      for j in range(1, order+1))
    def integrand(x):
        q = mp.exp(-z*x) * heat_b(x, xi)
        return q/x if w_action else q
    high = mp.quad(integrand, [split, mp.mpf('.1'), mp.mpf('.5'), 1, 4, 16, mp.inf])
    return -(low+high)/2 if w_action else low+high


def spectral_bracket(z, xi=0, n=1000):
    """Positive S(w) partial sum + analytic integral bound on its tail.

    l>=n: term <= (l+3)^3/(3*l^6). For decreasing l^-p,
    sum_(l=n)^infinity l^-p <= integral_(n-1)^infinity x^-p dx.
    Bound is intentionally conservative; no interval-library claim.
    """
    z, xi = mp.mpf(z), mp.mpf(xi)
    w = z+12*xi
    partial = mp.fsum(mp.mpf(2*l+3)/(6*(l+1)*(l+2)*(l*(l+3)+w)) for l in range(n))
    tail = mp.fsum(mp.mpf(c)/(3*(p-1)*(n-1)**(p-1))
                   for c, p in [(1, 3), (9, 4), (27, 5), (27, 6)])
    base = (w-2)*(1-2*mp.euler-mp.log(z))/6+mp.mpf(2)/9-2*xi
    base -= (mp.mpf(29)/90-4*xi+12*xi*xi)/z
    lo = base+(w-2)**2*partial
    hi = lo+(w-2)**2*tail
    exact = dec_integral(z, xi)
    assert lo-mp.mpf('1e-45') <= exact <= hi+mp.mpf('1e-45')
    return {'lower': fmt(lo), 'upper': fmt(hi), 'digamma': fmt(exact), 'n': n}


def fmt(x):
    return mp.nstr(x, 32)


def verify_exact_charge():
    xi, C, F, M, k = sp.symbols('xi C F M k', nonzero=True)
    k3 = sp.Rational(37, 189)-sp.Rational(58, 15)*xi+24*xi**2-48*xi**3
    from_shift = sum(EXACT_COEFF[j]*(-12*xi)**(1-j)/sp.factorial(1-j)
                     for j in range(-2, 2))
    assert sp.expand(k3-from_shift) == 0
    assert k3.subs(xi, sp.Rational(1, 6)) == -sp.Rational(4, 945)
    deriv = sp.Rational(3, 16) * (sp.diff(k3, xi).subs(xi, 0)*(-2*k)/M**2
                                 - k3.subs(xi, 0)*2*C/(F**2*M**4))
    target = sp.Rational(3, 16)*(sp.Rational(116, 15)*k/M**2
                                - sp.Rational(74, 189)*C/(F**2*M**4))
    assert sp.factor(deriv-target) == 0
    assert sp.Rational(3, 32)*k3.subs(xi, 0) == sp.Rational(37, 2016)
    return {'k3_xi': str(k3), 'pi2_times_charge_derivative_rho_over_H6': str(target)}


def main(output):
    heat_checks = []
    for z in [mp.mpf('.25'), 1, 4, 16, 64]:
        for xi in [mp.mpf(0), mp.mpf('.02'), mp.mpf(1)/6]:
            h = heat_integral(z, xi)
            v = dec_integral(z, xi)
            err = abs(h-v)
            assert err < mp.mpf('3e-21')
            heat_checks.append({'z': fmt(z), 'xi': fmt(xi), 'heat': fmt(h),
                                'digamma': fmt(v), 'absolute_difference': fmt(err)})
    stability = []
    for z, xi in [(mp.mpf('.25'), mp.mpf(0)), (mp.mpf(16), mp.mpf('.02'))]:
        values = [heat_integral(z, xi, split=mp.mpf('.02'), order=12),
                  heat_integral(z, xi, split=mp.mpf('.03'), order=10)]
        err = abs(values[0]-values[1])
        assert err < mp.mpf('3e-21')
        stability.append({'z': fmt(z), 'xi': fmt(xi), 'difference': fmt(err)})
    w_checks = []
    for z in [1, 4, 16]:
        wa = heat_integral(z, w_action=True)
        upper = mp.mpf(4096)
        integral = mp.quad(lambda v: dec_integral(v), [z, 64, 256, 1024, upper])
        tail = mp.fsum(COEFF[j]*mp.factorial(j-1)/upper**j for j in range(1, 11))
        wb = -(integral+tail)/2
        assert abs(wa-wb) < mp.mpf('1e-20')
        w_checks.append({'z': fmt(z), 'proper_time_W': fmt(wa),
                         'integrated_spectral_W': fmt(wb),
                         'absolute_difference': fmt(abs(wa-wb))})
    # Finite differences use direct W heat integrals and hold M,xi fixed.
    metric_checks = []
    dh = mp.mpf('1e-6')
    for z, xi in [(1, 0), (16, mp.mpf('.02'))]:
        wp = heat_integral(mp.mpf(z)*mp.exp(-2*dh), xi, w_action=True)
        wm = heat_integral(mp.mpf(z)*mp.exp(2*dh), xi, w_action=True)
        minus_DW = -(wp-wm)/(2*dh)
        expected = mp.mpf(z)*dec_integral(z, xi)
        assert abs(minus_DW-expected) < mp.mpf('2e-12')
        metric_checks.append({'z': str(z), 'xi': fmt(xi), 'minus_DW': fmt(minus_DW),
                              'zI': fmt(expected), 'absolute_difference': fmt(abs(minus_DW-expected))})
    spectral = [spectral_bracket(z, xi) for z in [1, 4, 16, 64]
                for xi in [0, mp.mpf('.02')]]
    radius = []
    for z in [mp.mpf('.25'), 1, 4, 16, 64, 256, 1024, 4096]:
        val = psi(z)
        radius.append({'z': fmt(z), 'H_over_M': fmt(1/mp.sqrt(z)), 'Psi': fmt(val),
                       'rho_over_H4_one_pion': fmt(3*val/(32*mp.pi**2)),
                       'ratio_to_leading_H6': fmt(z*val/(mp.mpf(37)/189))})
    charge = []
    z = mp.mpf(16)
    for y in [mp.mpf(0), mp.mpf('.1'), mp.mpf('.25'), mp.mpf('.5'), 1, 2]:
        ratio = (psi(z)+2*psi(z*(1+y)))/(3*psi(z))
        charge.append({'z': '16', 'y': fmt(y), 'finite_radius_mass_ratio': fmt(ratio),
                       'leading_H6_mass_ratio': fmt((1+2/(1+y))/3)})
    derivative_checks = []
    dy = mp.mpf('1e-8')
    for z in [1, 16, 256]:
        analytic = 2*z*mp.diff(lambda t: psi(t), mp.mpf(z))
        numeric = (2*psi(z*(1+dy))-2*psi(z*(1-dy)))/(2*dy)
        assert abs(analytic-numeric) < mp.mpf('2e-16')
        derivative_checks.append({'z': str(z), 'd_sumPsi_dy_at0': fmt(analytic),
                                  'finite_difference': fmt(numeric),
                                  'absolute_difference': fmt(abs(analytic-numeric))})
    result = {
        'claim': 'FSP008_GLOBAL_PION_DETERMINANT_COMPONENT',
        'status': 'finite assertions passed; conditional numerical interpretation',
        'versions': {'python': sys.version.split()[0], 'mpmath': mp.__version__, 'sympy': sp.__version__},
        'exact_heat_coefficients': {str(j): str(c) for j, c in EXACT_COEFF.items()},
        'exact_charge': verify_exact_charge(),
        'heat_comparisons': heat_checks,
        'max_heat_difference': fmt(max(mp.mpf(v['absolute_difference']) for v in heat_checks)),
        'small_segment_stability': stability,
        'W_reconstruction_checks': w_checks,
        'fixed_parameter_metric_checks': metric_checks,
        'positive_spectral_brackets': spectral,
        'radius_grid_one_real_pion': radius,
        'finite_charge_mass_component': charge,
        'charge_derivative_checks': derivative_checks,
        'zero_mode': {'included': True, 'Gaussian_minimal_limit_Psi_z_to_0': '61/90',
                      'massless_chiral_QCD_interpretation': 'not asserted; Gaussian zero mode singular'},
        'empirical_inputs': [],
        'full_QCD_ratio_calculated': False,
        'alpha_calculated': False,
        'numerical_limits': {'decimal_precision': mp.mp.dps, 'maximum_harmonic_cap': MAX_TERMS,
                             'heat_tail_exponent_cut': 140, 'small_x_split': str(SPLIT),
                             'small_x_series_order': 10, 'W_integral_upper': 4096,
                             'W_tail_asymptotic_order': 10, 'interval_certification': False},
        'runtime_seconds': time.monotonic()-START
    }
    pathlib.Path(output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'heat_cases': len(heat_checks),
                      'max_heat_difference': result['max_heat_difference'],
                      'W_cases': len(w_checks), 'metric_cases': len(metric_checks),
                      'spectral_brackets': len(spectral), 'charge_cases': len(charge)}))


if __name__ == '__main__':
    main(sys.argv[1])
