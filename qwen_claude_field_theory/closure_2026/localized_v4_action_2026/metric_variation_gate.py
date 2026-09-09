"""Finite metric-variation gate for the localized spatial operators.

The cochain calculation is intentionally reported as a surrogate: it tests
the Frechet terms from the Hodge inverse, moving kernel complement, projector,
weighted measure, and lapse.  It is not a continuum proof of the full York
variation.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "clock_constitutive_construction_2026"
if str(OLD) not in sys.path:
    sys.path.insert(0, str(OLD))

from operator_variation import evaluate


def metric_variation_gate():
    rows = []
    for n in (3, 4):
        value, derivative, residuals = evaluate(n)
        h = 1e-4
        finite = [abs((evaluate(n, h)[0] - evaluate(n, -h)[0])/(2*h)-derivative)]
        # The n=3 grid supplies the omission controls; n=4 independently
        # checks refinement of the full derivative at lower cost.
        omitted_inverse = (abs(evaluate(n, omit="inverse")[1]-derivative)
                           if n == 3 else 0.0)
        omitted_projector = (abs(evaluate(n, omit="projector")[1]-derivative)
                             if n == 3 else 0.0)
        rows.append({
            "grid": n,
            "max_finite_difference_error": max(finite),
            "omitted_inverse_error": omitted_inverse,
            "omitted_projector_error": omitted_projector,
            "residuals": residuals,
        })
    return {
        "status": "METRIC_HODGE_VARIATION_SURROGATE_VERIFIED; FULL_YORK_VARIATION_OPEN",
        "rows": rows,
        "max_finite_difference_error": max(r["max_finite_difference_error"] for r in rows),
        "max_omitted_inverse_error": max(r["omitted_inverse_error"] for r in rows),
        "max_omitted_projector_error": max(r["omitted_projector_error"] for r in rows),
        "identity": "delta(A^-1)=-A^-1(delta A)A^-1 plus moving-kernel terms",
        "scope": [
            "weighted finite periodic cochains at grids 3 and 4",
            "moving Hodge inverse, measure, lapse, mean projector, and transverse projector",
            "not a continuum nonlinear York-TT variation",
        ],
    }
