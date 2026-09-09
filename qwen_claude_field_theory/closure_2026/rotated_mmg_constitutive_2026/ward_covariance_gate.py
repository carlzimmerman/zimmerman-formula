"""Explicit time-diffeomorphism residual of the ADM relay term.

The relay is spatially covariant by construction.  This gate checks the
stronger four-dimensional Ward requirement before a clock/Stueckelberg
completion is asserted.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def derive_residual():
    x, t, a0 = sp.symbols("x t a0", positive=True)
    slope = sp.symbols("slope", positive=True)
    xi = sp.Function("xi")(t, x)
    # A space-dependent time diffeomorphism shifts the ADM lapse potential by
    # delta u = d_t xi on a flat background.  Choose u_x=slope>0 locally.
    y = slope / a0
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    dG_d_slope = sp.simplify(sp.diff(G, slope))
    delta_u_x = sp.diff(xi, t, x)
    delta_L = sp.simplify(dG_d_slope * delta_u_x)
    witness = sp.simplify(delta_L.subs({sp.diff(xi, t, x): 1, slope: a0}))
    return {
        "delta_u": "d_t xi(t,x)",
        "delta_grad_u": "d_x d_t xi(t,x)",
        "delta_constitutive_density": str(delta_L),
        "unit_slope_witness": str(witness),
        "residual_nonzero": bool(witness != 0),
        "interpretation": (
            "The ADM relay is not by itself a 4D scalar action: a "
            "space-dependent time diffeomorphism produces a nonzero "
            "constitutive residual. A covariant clock/Stueckelberg completion "
            "must cancel this term before the ordinary matter Ward identity "
            "can be claimed."
        ),
    }


if __name__ == "__main__":
    result = derive_residual()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "ward_covariance_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("WARD_COVARIANCE_GATE")
    print(f"residual: {result['unit_slope_witness']}")
    print(f"nonzero: {result['residual_nonzero']}")
    print("STATUS: OPEN (Stueckelberg/covariant completion required)")
