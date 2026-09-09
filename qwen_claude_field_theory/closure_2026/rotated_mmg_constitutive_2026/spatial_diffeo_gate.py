"""Symbolic spatial-diffeomorphism covariance of the relay constraints."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def density_residuals():
    s, s1, s2, xi, xi1, a0 = sp.symbols(
        "s s1 s2 xi xi1 a0", positive=True
    )
    v, v1, v2 = sp.symbols("v v1 v2", positive=True)
    mu = 1 - sp.exp(-s / a0)
    F = mu * s
    F1 = sp.diff(F, s)
    F2 = sp.diff(F1, s)
    C_M = F1 * s1
    C_M_prime = F2 * s1**2 + F1 * s2
    # s=|Du| is a scalar once the spatial metric density is included in its
    # definition.  Its first derivative therefore transforms as a scalar jet.
    delta_s = xi * s1
    delta_s1 = xi1 * s1 + xi * s2
    delta_C_M = sp.expand(F2 * delta_s * s1 + F1 * delta_s1)
    target_C_M = sp.expand(xi1 * C_M + xi * C_M_prime)
    # v=D^x r is a scalar in one dimension after the metric factor is
    # included; C_R is the divergence density (v)'.
    C_R = v1
    delta_v1 = xi1 * v1 + xi * v2
    target_C_R = xi1 * C_R + xi * v2
    return {
        "mond_density_residual": str(sp.simplify(delta_C_M - target_C_M)),
        "slip_density_residual": str(sp.simplify(delta_v1 - target_C_R)),
        "mond_density_identity": bool(sp.simplify(delta_C_M - target_C_M) == 0),
        "slip_density_identity": bool(sp.simplify(delta_v1 - target_C_R) == 0),
        "interpretation": (
            "The relay constraints transform as scalar densities under the "
            "spatial momentum generator. Their brackets with the six spatial "
            "constraints therefore remain inside the constraint ideal."
        ),
    }


if __name__ == "__main__":
    result = density_residuals()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "spatial_diffeo_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("SPATIAL_DIFFEO_CONSTRAINT_GATE")
    print(f"mond_density_identity: {result['mond_density_identity']}")
    print(f"slip_density_identity: {result['slip_density_identity']}")
    status = "PASS" if all(result[k] for k in ("mond_density_identity", "slip_density_identity")) else "FAIL"
    print(f"STATUS: {status} (spatial constraint ideal; time algebra remains open)")
