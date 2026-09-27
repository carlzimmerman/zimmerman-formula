#!/usr/bin/env python3
"""Independent scoped checks; no import or execution of audited lane scripts.

Rechecks the already-recorded weighted counterexample using Fourier algebra
and adaptive quadrature, and tests XC2's zero-field/mixed-filter inferences.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy.integrate as integrate
import scipy.optimize as optimize
import sympy as sp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    results = {}

    # Independent Fourier product integration of the pre-existing example.
    a, d, t = sp.symbols("a d t", real=True)
    lapse_modes = {0: sp.Integer(1), 9: sp.Rational(2, 5), -9: sp.Rational(2, 5)}
    derivative_modes = {1: a/2, -1: a/2, 10: -d/10, -10: -d/10}
    # Integral/pi is twice the exact constant coefficient of the product.
    exact_energy = sp.expand(2*sum(nv*vk*vl for n,nv in lapse_modes.items()
                                 for k,vk in derivative_modes.items()
                                 for l,vl in derivative_modes.items() if n+k+l == 0))
    assert sp.simplify(exact_energy - (a*a+d*d/25-sp.Rational(4,25)*a*d)) == 0
    heat_energy = exact_energy.subs({a: sp.exp(-t), d: sp.exp(-100*t)})
    growth = sp.diff(heat_energy, t).subs(t, 0)
    assert growth == sp.Rational(154,25)
    results["prior_weighted_counterexample_independent_fourier_integration"] = {
        "formula_over_pi": str(exact_energy), "derivative_at_b0_over_pi": str(growth),
        "b0_energy_over_pi": float(heat_energy.subs(t,0)),
        "b0p001_energy_over_pi": float(heat_energy.subs(t,sp.Rational(1,1000))),
        "prior_source": "real_research/closure_doors_2026_09_26/auxiliary/weighted_heat_check.py:26-34",
    }

    # Same old exponential witness, but independent scalar inversion/adaptive
    # quadrature instead of a uniform mesh and vectorized bisection.
    b = 0.02
    lapse = lambda z: 1e-8 + math.exp(1000*(math.cos(z)-1))
    vp = lambda z: math.cos(z)-math.cos(10*z)
    svp = lambda z: math.exp(-b)*math.cos(z)-math.exp(-100*b)*math.cos(10*z)
    source_exp = 2*(-math.expm1(-2))
    def cl_exp(s):
        y = optimize.brentq(lambda y: y*(-math.expm1(-y))-s, 0, 2, xtol=1e-14)
        return (1-y)/(math.expm1(y)+y)
    def cl_rar(s):
        z = math.sqrt(s)
        ezm = math.expm1(z)
        return 1/ezm - z*math.exp(z)/(2*ezm*ezm)
    rows = []
    for tol in (1e-8, 1e-10):
        def integral(fun):
            value, error = integrate.quad(fun, 0, math.pi, points=[math.pi/2],
                                          epsabs=tol, epsrel=tol, limit=500)
            return 2*value, 2*error
        unfiltered, ue = integral(lambda z: lapse(z)*vp(z)**2)
        filtered, fe = integral(lambda z: lapse(z)*svp(z)**2)
        h_exp, err_exp = integral(lambda z: 4*lapse(z)*(vp(z)**2+cl_exp(abs(source_exp*math.cos(z)))*svp(z)**2))
        h_rar, err_rar = integral(lambda z: 4*lapse(z)*(vp(z)**2+cl_rar(abs(6*math.cos(z)))*svp(z)**2))
        assert h_exp < -0.025 and h_rar < -0.005
        rows.append({"absolute_relative_tolerance": tol, "unfiltered": unfiltered,
                     "filtered": filtered, "weighted_ratio": filtered/unfiltered,
                     "mu_exp_second_variation": h_exp, "mu_exp_quad_error_estimate": err_exp,
                     "nu_RAR_second_variation": h_rar, "nu_RAR_quad_error_estimate": err_rar})
    results["weighted_hessian_branches"] = rows

    # At U=0 the exact deep-MOND leading flux is homogeneous of degree 1/2.
    # Evaluate its surviving first harmonic after the outer heat/divergence.
    harmonic = 4*integrate.quad(lambda z: math.cos(z)**1.5, 0, math.pi/2,
                              epsabs=1e-12, epsrel=1e-12)[0]/math.pi
    epsilons = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
    zero_rows = []
    for eps in epsilons:
        amplitude = harmonic*math.exp(-1.5*b)*math.sqrt(eps)
        zero_rows.append({"epsilon": eps, "outer_operator_sin1_coefficient": amplitude,
                          "coefficient_over_epsilon": amplitude/eps,
                          "coefficient_over_claimed_osgood_modulus": amplitude/(eps*math.sqrt(math.log(1/eps)))})
    assert zero_rows[-1]["coefficient_over_epsilon"] > 9000*zero_rows[0]["coefficient_over_epsilon"]
    results["homogeneous_zero_leading_flux"] = {"b": b, "first_harmonic_constant": harmonic, "rows": zero_rows,
        "interpretation": "Exact epsilon^(1/2) homogeneity; quadrature evaluates only a positive prefactor."}

    # Duhamel derivative for h=e^(2 eps cos(mx)) dx^2, U=sin x.
    # Independent coefficients show metric-input variation is not exponentially
    # smoothing. They do NOT determine the full coupled principal symbol.
    mixed = []
    for m in (4, 16, 64, 256, 1024):
        k = m+1
        coefficient = ((m+2)/2)*(math.exp(-b)-math.exp(-b*k*k))/(k*k-1)
        mixed.append({"metric_frequency_m": m, "delta_S_U_sin_mplus1": coefficient,
                      "m_times_coefficient": m*coefficient})
    assert abs(mixed[-1]["m_times_coefficient"]-math.exp(-b)/2) < 1e-12
    results["mixed_metric_heat_variation"] = {"rows": mixed, "limit_m_times_coefficient": math.exp(-b)/2}

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
