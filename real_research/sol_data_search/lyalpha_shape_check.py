#!/usr/bin/env python3
"""Reproduce a limited DESI Ly-alpha AP shape check from published summaries.

Input: DESI DR2 Results IV, arXiv:2607.27410v3, Eq. (26);
       Unite, arXiv:2609.05053v2, abstract central CPL values.
No chain samples or unpublished data are used. Run with Python 3 stdlib.
"""

import json
import math

Z = 2.33
DATA = (39.32, 8.600)  # (D_M/r_d, D_H/r_d)
SIGMA = (0.33, 0.066)
RHO = 0.225


def simpson(function, upper, steps):
    assert steps > 0 and steps % 2 == 0
    h = upper / steps
    total = function(0.0) + function(upper)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * function(i * h)
    return total * h / 3


def shape(omega_m, w0, wa, steps=8192):
    """Flat, matter+CPL background; returns (I, 1/E, AP=E*I)."""

    def e(z):
        de = math.exp(3 * (1 + w0 + wa) * math.log1p(z)
                      - 3 * wa * z / (1 + z))
        return math.sqrt(omega_m * (1 + z) ** 3 + (1 - omega_m) * de)

    integral = simpson(lambda z: 1 / e(z), Z, steps)
    return integral, 1 / e(Z), integral * e(Z)


def redshift_slope(omega_m, w0, wa, z_low=2.13, z_high=2.81):
    """Secant d ln H / d ln(1+z), independent of H0 and r_d."""
    def log_e(z):
        de = math.exp(3 * (1 + w0 + wa) * math.log1p(z)
                      - 3 * wa * z / (1 + z))
        return 0.5 * math.log(omega_m * (1 + z) ** 3 + (1 - omega_m) * de)

    return (log_e(z_high) - log_e(z_low)) / math.log((1 + z_high) / (1 + z_low))


def profile_shape(omega_m, w0, wa):
    """Profile q=c/(H0*r_d) from the published correlated distance pair."""
    d_m, d_h = DATA
    s_m, s_h = SIGMA
    determinant = 1 - RHO ** 2

    def inner(a, b):
        return ((a[0] * b[0] / s_m ** 2)
                - RHO * (a[0] * b[1] + a[1] * b[0]) / (s_m * s_h)
                + a[1] * b[1] / s_h ** 2) / determinant

    v_m, v_h, ap = shape(omega_m, w0, wa)
    vector = (v_m, v_h)
    q = inner(vector, DATA) / inner(vector, vector)
    residual = (d_m - q * v_m, d_h - q * v_h)
    chi2 = inner(residual, residual)
    assert chi2 >= -1e-10
    return {
        "omega_m": omega_m, "w0": w0, "wa": wa,
        "ap_dm_over_dh": ap, "q_profiled": q,
        "dm_over_rd_model": q * v_m, "dh_over_rd_model": q * v_h,
        "chi2_profiled_one_shape_dof": max(0.0, chi2),
        "conditional_gaussian_tail_p": math.erfc(math.sqrt(max(0.0, chi2) / 2)),
    }


def main():
    observed_ap = DATA[0] / DATA[1]
    # First-order propagation with the *reported* correlation coefficient.
    fractional_variance = ((SIGMA[0] / DATA[0]) ** 2
                           + (SIGMA[1] / DATA[1]) ** 2
                           - 2 * RHO * SIGMA[0] * SIGMA[1] / (DATA[0] * DATA[1]))
    ap_sigma = observed_ap * math.sqrt(fractional_variance)
    result = {
        "source": {
            "desi": "https://arxiv.org/html/2607.27410v3 (Eq. 26)",
            "unite": "https://arxiv.org/abs/2609.05053v2 (abstract)",
        },
        "desi": {"z": Z, "dm_over_rd": DATA[0], "dh_over_rd": DATA[1],
                 "sigma_dm": SIGMA[0], "sigma_dh": SIGMA[1], "rho": RHO,
                 "ap_dm_over_dh": observed_ap, "ap_sigma_delta_method": ap_sigma},
        "profiles": {
            "unite_cpl_central_fixed": profile_shape(0.305, -0.861, -0.60),
            "lcdm_same_omega_m_fixed": profile_shape(0.305, -1.0, 0.0),
            "desi_lya_lcdm_central_fixed": profile_shape(0.325, -1.0, 0.0),
        },
        "multiredshift_bao": {
            "source": "https://arxiv.org/abs/2607.19619v2",
            "published_fit_n": 1.34,
            "published_sigma_n": 0.16,
            "z_low": 2.13,
            "z_high": 2.81,
            "secant_n_unite_cpl_central": redshift_slope(0.305, -0.861, -0.60),
            "secant_n_lcdm_same_omega_m": redshift_slope(0.305, -1.0, 0.0),
            "scope": "The published n is a three-bin fitted power-law slope; the computed n is only an endpoint secant. They are orientation values, not a matched likelihood. The three-bin BAO and full-shape AP reuse DESI DR2 Ly-alpha data.",
        },
        "quadrature_abs_difference_4096_vs_8192":
            abs(shape(0.305, -0.861, -0.60, 4096)[2]
                - shape(0.305, -0.861, -0.60, 8192)[2]),
        "scope": "Fixed published parameter centers; flat matter+CPL; no radiation, posterior covariance, sample-overlap correction, or action-level prediction. Chi-square is a conditional descriptive shape check, not a new independent significance.",
    }
    assert result["quadrature_abs_difference_4096_vs_8192"] < 1e-9
    assert abs(result["profiles"]["desi_lya_lcdm_central_fixed"]["ap_dm_over_dh"]
               - observed_ap) < 1e-3
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
