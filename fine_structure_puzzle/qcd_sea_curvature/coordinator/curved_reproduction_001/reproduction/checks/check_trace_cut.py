#!/usr/bin/env python3
"""Bounded, dependency-free checks of the pion trace cut; no physical fit inputs.

Run from the repository root:
  python3 fine_structure_puzzle/qcd_sea_curvature/curved_response/checks/check_trace_cut.py
"""
from fractions import Fraction as F
from pathlib import Path
import json
import math


def simpson(fun, lo=0.0, hi=1.0, n=32768):
    assert n % 2 == 0
    h = (hi - lo) / n
    value = fun(lo) + fun(hi)
    value += 4 * math.fsum(fun(lo + h * k) for k in range(1, n, 2))
    value += 2 * math.fsum(fun(lo + h * k) for k in range(2, n, 2))
    return value * h / 3


def moment_polynomial(c):
    return c*c/F(6) + c/F(15) + F(1, 105)


def cutoff_moment(c, xmax):
    t = math.sqrt(1 - 4/xmax)
    a = 2*c + 1
    return (a*a*t**3/3 - 2*a*t**5/5 + t**7/7)/8


def spectral_kernel(z, c):
    return simpson(lambda t: .5*t*t*(2*c + 1 - t*t)**2 /
                   (4 + z*(1 - t*t)))


def feynman_remainder(z, c):
    # From 1/2 Tr log after phi -> exp(-sigma) chi, with all local
    # source polynomials through Q^4 explicitly removed.
    ell = simpson(lambda x: math.log1p(z*x*(1-x)))
    p1 = 2/3
    p2 = -1/15 - 2*c/3
    return ((2-c*z)**2*ell - p1*z - p2*z*z) / z**3


def main():
    exact = moment_polynomial(F(1))
    assert exact == F(17, 70)
    # Two independent polynomial decompositions of the same moment.
    poly_from_beta = (9*F(1,3) - 6*F(1,5) + F(1,7))/8
    poly_from_loop = 4*F(1,420) + 4*F(1,60) + F(1,6)
    assert exact == poly_from_beta == poly_from_loop
    assert exact/F(32) == F(17, 2240)
    assert exact/(F(32)*72) == F(17, 161280)
    # General improvement c=1-6 xi. k15 gives c=1+12 e^2 k15^r.
    deriv_c_at_one = F(1,3) + F(1,15)
    k15_prefactor = 2*12*deriv_c_at_one/F(32)
    mass_prefactor = -2*2*exact/F(32)
    assert k15_prefactor == F(3,10)
    assert mass_prefactor == -F(17,560)

    grid = []
    max_abs_error = 0.0
    for c in [-.5, 0., 1., 2.]:
        for z in [.1, 1., 4., 16., 64.]:
            a = spectral_kernel(z, c)
            b = feynman_remainder(z, c)
            err = abs(a-b)
            max_abs_error = max(max_abs_error, err)
            assert err < 2e-11, (z, c, a, b, err)
            assert a >= 0
            grid.append(dict(z=z, c=c, spectral=a, feynman=b,
                             absolute_error=err))
    # Endpoint cutoff formula checked against a direct spectral quadrature.
    cutoffs = []
    for xmax in [5., 9., 16., 25., 100.]:
        tmax = math.sqrt(1-4/xmax)
        v = cutoff_moment(1., xmax)
        independent = simpson(lambda t: t*t*(3-t*t)**2/8, hi=tmax)
        assert abs(v-independent) < 1e-13
        cutoffs.append(dict(smax_over_M2=xmax,
                            moment_without_1_over_32pi2M2=v,
                            fraction_of_full_LO_loop=v/float(exact)))
    charge_scenarios = []
    for y in [F(0), F(1,100), F(1,10), F(1,2), F(1), F(2)]:
        # y = 2 e^2 C/(F^2 M^2); no measured alpha or masses inserted.
        relative = (1 + 2/(1+y))/3
        charge_scenarios.append(dict(y=str(y), moment_ratio=str(relative),
                                     decimal=float(relative)))
    result = {
        'status': 'all bounded checks passed',
        'physical_calibration': 'none; dimensionless symbolic/scenario inputs only',
        'simpson_intervals': 32768,
        'assertion_tested': 'Exact moment coefficients and 20 dimensionless dispersion/Feynman kernel comparisons',
        'moment_I_1': str(exact),
        'per_real_pion_M3_coefficient_without_1_over_pi2M2': str(exact/F(32)),
        'per_real_pion_RDeltaR_coefficient_without_1_over_pi2M2': str(exact/(F(32)*72)),
        'k15_M3_slope_coefficient_without_1_over_pi2M2': str(k15_prefactor),
        'mass_M3_slope_coefficient_without_C_over_pi2F2M4': str(mass_prefactor),
        'maximum_absolute_kernel_difference': max_abs_error,
        'kernel_grid': grid,
        'cutoff_moments': cutoffs,
        'matched_charge_mass_scenarios': charge_scenarios,
        'non_claims': [
            'Not a measurement of QCD, of alpha, of A_rho, or of R=A_rho/m_p^3',
            'LO pion amplitude does not fix the high-energy QCD spectral tail',
            'The matched mass-shift contribution omits photon radiative and independent curvature-LEC contributions',
            'A flat quadratic curvature response does not determine the curved-sphere one-point vacuum stress'
        ]
    }
    out = Path(__file__).resolve().parents[1]/'checks'/'RESULTS.json'
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
                      ('kernel_grid','cutoff_moments','matched_charge_mass_scenarios','non_claims')}, indent=2))


if __name__ == '__main__':
    main()
