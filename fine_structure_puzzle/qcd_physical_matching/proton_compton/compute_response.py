#!/usr/bin/env python3
"""Exact native-unit proton Compton stencil; not a complete mass derivative."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import pi, sqrt
from pathlib import Path


def encoded(x):
    return {"exact": str(x), "decimal": float(x)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    ipath = Path(args.inputs)
    inputs = json.loads(ipath.read_text())
    rows = inputs["rows"]
    n2 = [sum(n*n for n in row["n"]) for row in rows]
    s = [F(row["S1"]) for row in rows]
    sigma = [F(row["sigma"]) for row in rows]
    assert all(n2[i] < n2[i+1] for i in range(len(n2)-1))
    weights = [F(n2[1]-n2[0], 2)]
    weights += [F(n2[i+1]-n2[i-1], 2) for i in range(1, len(n2)-1)]
    weights += [F(n2[-1]-n2[-2], 2)]
    # Orthogonal implementations: segment integral and nodal weighted sum.
    segment_sum = sum(F(n2[i+1]-n2[i], 2)*(s[i]+s[i+1]) for i in range(len(n2)-1))
    weighted_sum = sum(w*y for w, y in zip(weights, s))
    assert segment_sum == weighted_sum
    # Hand-computable quadrature invariants, independent of the data.
    assert sum(weights) == n2[-1]-n2[0]
    assert sum(w*n for w, n in zip(weights, n2)) == F(n2[-1]**2-n2[0]**2, 2)
    NL = inputs["ensemble"]["N_L"]
    aM = F(inputs["ensemble"]["aM"])
    aM_sigma = F(inputs["ensemble"]["aM_sigma"])
    coefficient = -F(3, 16*NL*NL)/aM**2
    answer = coefficient*weighted_sum
    # Check the pi cancellation by the original Cottingham kernel in native units.
    kernel_float = -3/(64*pi*pi)*((2*pi/NL)**2)*float(weighted_sum)/float(aM*aM)
    assert abs(kernel_float-float(answer)) < 1e-16
    # Any PSD covariance obeys |cov_ij| <= sigma_i sigma_j.
    errors = [abs(w)*sd for w, sd in zip(weights, sigma)]
    sigma_upper = abs(coefficient)*sum(errors)
    sigma_lower = abs(coefficient)*max(F(0), 2*max(errors)-sum(errors))
    # Independent errors are an illustration only, not a source-supported error bar.
    sigma_diag_example = abs(float(coefficient))*sqrt(sum(float(x)**2 for x in errors))
    q = [F(x) for x in inputs["charges"]]
    trq, trq2 = sum(q), sum(x*x for x in q)
    assert trq == 0 and trq2 == F(2, 3)
    # Diagonal equal-propagator determinant algebra: single-current factors cancel,
    # but the two-current insertion on the same sea loop carries sum Q_f^2.
    determinant = {
        "one_current_sea_factor": encoded(trq),
        "two_separate_sea_loops_factor": encoded(trq**2),
        "two_currents_same_sea_loop_factor": encoded(trq2),
        "proton_minus_neutron_same_loop_factor_at_isospin": encoded(trq2-trq2),
        "proton_plus_neutron_same_loop_factor_at_isospin": encoded(trq2+trq2)
    }
    result = {
        "assertion_tested": "Exact weighted connected proton subtraction stencil and SU(3) sea-charge factors, for the six supplied Table III central values.",
        "inputs_sha256": hashlib.sha256(ipath.read_bytes()).hexdigest(),
        "n_squared": n2,
        "weights_in_n_squared": [encoded(w) for w in weights],
        "weighted_S1_sum": encoded(weighted_sum),
        "fractional_response_e2_stencil": encoded(answer),
        "fractional_response_alpha_stencil": 4*pi*float(answer),
        "conditional_covariance_sigma_lower_bound": encoded(sigma_lower),
        "conditional_covariance_sigma_upper_bound": encoded(sigma_upper),
        "diagonal_covariance_sigma_example_not_inferred": sigma_diag_example,
        "aM_first_order_fractional_sensitivity": encoded(2*aM_sigma/aM),
        "sea_charge_algebra": determinant,
        "checks": {"segment_vs_nodal": True, "constant_and_linear_integrands": True, "native_Cottingham_normalization": True, "SU3_charge_traces": True},
        "non_claims": [
            "No complete physical individual proton derivative.",
            "No bound on interpolation error or contribution outside window.",
            "No all-sea/continuum/physical-mass extrapolation or counterterm evaluation.",
            "No alpha input, alpha root, vacuum coefficient, or R(alpha) determination."
        ]
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"fractional_e2_stencil": encoded(answer), "conditional_sigma_ceiling": encoded(sigma_upper), "all_checks": True}))


if __name__ == "__main__":
    main()
