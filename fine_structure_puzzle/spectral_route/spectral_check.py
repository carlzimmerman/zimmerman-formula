#!/usr/bin/env python3
"""FSP-S: charge-normalized dispersive subtraction and induced-boundary checks.

Command and finite mathematical contract are in contract.json. No measured
alpha, mass, Planck scale, or fitted number is an input. m=1 sets units.
"""
import argparse
import json
from pathlib import Path

import mpmath as mp


def compute(dps, mutate=False):
    mp.mp.dps = dps
    C = 1 / (12 * mp.pi**2)
    checks = []
    def check(name, condition, residual=None):
        item = {"name": name, "passed": bool(condition)}
        if residual is not None:
            item["residual"] = mp.nstr(residual, 25)
        checks.append(item)

    def spectral_subtraction(r):
        # s=4/(1-v^2), rho=C*(1+2/s)*sqrt(1-4/s).
        r2 = r*r
        sign = -1 if mutate else 1
        return sign * C * mp.quad(
            lambda v: r2 * (3-v*v)*v*v/(4+r2*(1-v*v)), [0, 1])

    def feynman_subtraction(r):
        return mp.quad(lambda x: x*(1-x)*mp.log1p(r*r*x*(1-x)),
                       [0, mp.mpf('0.5'), 1])/(2*mp.pi**2)

    grid = ['0', '0.1', '1', '10', '100', '1000']
    rows = []
    for raw in grid:
        r = mp.mpf(raw)
        p = spectral_subtraction(r)
        f = feynman_subtraction(r)
        err = abs(p-f)
        check('dispersion_equals_Feynman_Q_over_m='+raw, err < mp.mpf('1e-40'), err)
        check('screening_nonnegative_Q_over_m='+raw, p >= 0)
        rows.append({'Q_over_m': raw, 'P': mp.nstr(p, 35),
                     'Feynman_P': mp.nstr(f, 35), 'absolute_error': mp.nstr(err, 10)})

    rsmall = mp.mpf('1e-6')
    low_ratio = spectral_subtraction(rsmall)/(rsmall*rsmall)/(1/(60*mp.pi**2))
    check('small_Q_coefficient_1_over_60_pi_squared', abs(low_ratio-1) < mp.mpf('1e-12'), low_ratio-1)
    rlarge = mp.mpf(1000)
    # dP/dln(Q^2), computed from a derivative of the independent x integral.
    adler = mp.quad(lambda x: (rlarge*rlarge*x*x*(1-x)**2)/
                    (1+rlarge*rlarge*x*(1-x)), [0, mp.mpf('0.5'), 1])/(2*mp.pi**2)
    check('UV_log_slope_1_over_12_pi_squared', abs(adler/C-1) < mp.mpf('1e-4'), adler/C-1)

    cutoff_rows = []
    for rawR in ['100', '10000', '100000000']:
        R = mp.mpf(rawR)
        vmax = mp.sqrt(1-4/(R*R))
        closed_bracket = vmax**3/3-2*vmax+2*mp.atanh(vmax)
        closed = C*closed_bracket
        upper = mp.log(R*R/4)
        def rho_log(t):
            return C*(1+mp.exp(-t)/2)*mp.sqrt(1-mp.exp(-t))
        direct = mp.quad(rho_log, [0, upper])
        err = abs(closed-direct)
        check('finite_band_integral_R='+rawR, err < mp.mpf('1e-40'), err)
        asym_error = closed_bracket-(mp.log(R*R)-mp.mpf(5)/3)
        check('finite_band_asymptotic_bound_R='+rawR, 0 < asym_error < 4/R**4, asym_error)
        for rawc in ['0', '1', '10']:
            c = mp.mpf(rawc)
            # All these have identical rho, charge lattice Z, and anomalies=0.
            # These are background-matter response kernels, not a claim of
            # isospectral fully interacting QED at different couplings.
            sampled_K = []
            for rawQ in ['0', '1', '10', '100']:
                Q2 = mp.mpf(rawQ)**2
                K = c + mp.quad(lambda t: rho_log(t)*(4*mp.exp(t))/
                                (4*mp.exp(t)+Q2), [0, upper])
                sampled_K.append(K)
                check('positive_band_K_R='+rawR+'_c='+rawc+'_Q='+rawQ, K > 0)
            check('contact_shift_c='+rawc+'_R='+rawR,
                  abs((c+direct)-direct-c) < mp.mpf('1e-40'))
            cutoff_rows.append({'Lambda_over_m': rawR, 'local_coefficient_c': rawc,
                'alpha_inverse_at_zero': mp.nstr(4*mp.pi*(c+direct), 35),
                'K_at_Q_over_m_0_1_10_100': [mp.nstr(k, 25) for k in sampled_K]})

    return {'decimal_precision': dps, 'checks': checks,
            'passed': all(c['passed'] for c in checks),
            'dispersion_rows': rows, 'cutoff_counterfamily': cutoff_rows,
            'anomalies_of_one_vectorlike_Dirac': {'sum_left_Weyl_q': 0, 'sum_left_Weyl_q_cubed': 0}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--mutate-spectral-sign', action='store_true')
    args = parser.parse_args()
    # The closed cutoff formula loses ~16 digits at Lambda/m=1e8 because
    # vmax differs from one by ~2e-16; retain >40 accurate digits after that.
    runs = [compute(dps, args.mutate_spectral_sign) for dps in (70, 100)]
    stable = all(abs(mp.mpf(a['P'])-mp.mpf(b['P'])) < mp.mpf('1e-33')
                 for a, b in zip(runs[0]['dispersion_rows'], runs[1]['dispersion_rows']))
    result = {'claim_id': 'FSP-S-DISPERSION-001', 'measured_alpha_used': False,
              'mutation': args.mutate_spectral_sign, 'precision_stable_33_digits': stable,
              'runs': runs, 'passed': stable and all(r['passed'] for r in runs)}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'passed': result['passed'], 'mutation': result['mutation'],
                      'checks_per_precision': len(runs[0]['checks']),
                      'precision_stable_33_digits': stable,
                      'failed_checks': [c['name'] for c in runs[0]['checks'] if not c['passed']]}))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
