#!/usr/bin/env python3
"""Bounded numerical checks of independently derived n=1 TF formulas.

This is not a formation simulation or an SP ground-state solver. The regular
Helmholtz ODE, moment quadrature and analytic boundary formula are deliberately
different checks of the same fixed TF static response.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq
from scipy.special import spherical_jn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    inp = json.loads(Path(args.inputs).read_text())
    pi = math.pi
    cshape = (15.0-pi*pi)/(3.0*pi*pi)
    k2 = 1.5*cshape
    rows = []
    for ell in inp["ode"]["l_values"]:
        double_fac = math.prod(range(1, 2*ell+2, 2))
        for rtol in inp["ode"]["rtols"]:
            x0 = inp["ode"]["x_start"]
            # H=x^ell y, y(0)=1, from its regular power series.
            a = 2.0*(2*ell+3)
            b = 8.0*(2*ell+3)*(2*ell+5)
            y0 = 1-x0*x0/a+x0**4/b
            yp0 = -2*x0/a+4*x0**3/b

            def rhs(x, y):
                return [y[1], -(2*ell+2)*y[1]/x-y[0]]

            sol = solve_ivp(rhs, (x0, pi), [y0, yp0], method="DOP853",
                            rtol=rtol, atol=rtol*1e-2,
                            max_step=inp["ode"]["max_step"])
            assert sol.success
            y, yp = sol.y[:, -1]
            beta = ell+pi*yp/y
            response = (ell-beta)/(ell+1+beta)
            exact_beta = pi*spherical_jn(ell, pi, derivative=True)/spherical_jn(ell, pi)
            exact_response = (ell-exact_beta)/(ell+1+exact_beta)
            norm_exact = double_fac*spherical_jn(ell, pi)/pi**ell
            error = abs(response-exact_response)
            assert error < 2e-8
            assert abs(y-norm_exact) < 2e-9
            rows.append({"ell": ell, "rtol": rtol, "nfev": sol.nfev,
                         "beta": float(beta), "B_over_a_R_2lplus1": float(response),
                         "absolute_response_error": float(error),
                         "regular_y_error": float(abs(y-norm_exact))})
    # With G=R=E=1, K=2/pi and A=5/2, delta rho=-A*j2(pi*r)/(2K).
    moment, err = quad(lambda r: r**4*spherical_jn(2, pi*r), 0, 1,
                       epsabs=1e-13, epsrel=1e-13)
    qzz = -(8*pi/15)*(2.5/(2*(2/pi)))*moment
    assert abs(qzz+cshape) < 1e-13
    j1root = brentq(lambda x: spherical_jn(1, x), pi+1e-6, 1.5*pi)
    assert j1root > pi
    # Translation zero: pi*j0(pi)=sin(pi), with the exact value zero
    # established analytically, not by this floating residual.
    translation_residual = pi*spherical_jn(0, pi)
    units = inp["unit_inputs_SI"]
    hbar, c, ev, grav = (units["hbar_J_s"], units["c_m_s"],
                         units["eV_J"], units["G_m3_kg_s2"])
    mass = inp["benchmark"]["mass_MeV_c2"]*1e6*ev/c**2
    lam = inp["benchmark"]["lambda_rep"]
    g2si = lam*hbar**3/(2*mass**2*c)
    keos = g2si/(2*mass**2)
    radius = math.sqrt(pi*keos/(2*grav))
    scat = mass*g2si/(4*pi*hbar**2)
    crossover = hbar**2/(grav*mass**2*radius)
    weak_grav_mass = radius*c**2/grav
    diluteness_mass = 4*radius**3*mass/(pi*scat**3)
    comparisons = []
    for length_pc in inp["declared_comparison_lengths_pc"]:
        length = length_pc*units["parsec_m"]
        # Define k=1/L; replacing L by wavelength inserts the declared 2pi.
        comparisons.append({"L_pc": length_pc, "k_definition": "k=1/L",
                            "R_over_L": radius/length,
                            "max_ratio_4piG_chi_at_f_equal_1": cshape*(radius/length)**2})
    result = {
        "assertion_tested": "Regular n=1 TF static tidal boundary ODE for ell=2,3,4 at three tolerances agrees with spherical-Bessel formula; direct quadrupole moment agrees with C; benchmark conversions and long-wavelength factors computed.",
        "software": {"numpy": np.__version__, "scipy": scipy.__version__},
        "C_lambda_GRminus5": cshape, "k2_apsidal": k2,
        "required_f_times_kR_squared_for_4piG_chi_equal_1": 1/cshape,
        "ode_checks": rows,
        "independent_moment_check": {"Qzz_over_E_G_R5": qzz,
                                     "abs_error": abs(qzz+cshape),
                                     "quadrature_reported_error": err},
        "stability_checks": {"first_positive_j1_zero": j1root,
                             "minimum_density_Hessian_gap_factor": 1-(pi/j1root)**2,
                             "translation_denominator_float_residual": translation_residual},
        "benchmark_SI": {"particle_mass_kg": mass, "g2_J_m3": g2si,
                         "K_EOS_m5_kg_s2": keos, "R_TF_m": radius,
                         "R_TF_pc": radius/units["parsec_m"],
                         "scattering_length_m": scat,
                         "M_QTF_scale_kg": crossover,
                         "M_compactness_equal_1_scale_kg": weak_grav_mass,
                         "M_central_na3_equal_1_scale_kg": diluteness_mass,
                         "lambda_T_kg_m2_s2": cshape*radius**5/grav},
        "declared_length_comparisons": comparisons,
        "status": "finite checks passed; no formation, SP-profile or phase-classification claim"
    }
    out = Path(args.result)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "C": cshape,
                      "R_TF_m": radius, "worst_ODE_abs_error": max(r["absolute_response_error"] for r in rows),
                      "moment_abs_error": abs(qzz+cshape)}))


if __name__ == "__main__":
    main()
