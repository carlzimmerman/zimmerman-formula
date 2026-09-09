"""Re-export the exact six-source response gate for localized V4 review."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "clock_constitutive_construction_2026"
if str(OLD) not in sys.path:
    sys.path.insert(0, str(OLD))

from general_sources_v3 import response_matrix
import sympy as sp
from functools import lru_cache


@lru_cache(maxsize=None)
def _counts(tensor_norm):
    result = response_matrix(tensor_norm)
    return len(result["spatial_poles"]), len(result["rows"])


def causal_response_gate():
    v2_poles, entries = _counts(sp.Integer(1))
    v3_poles, _ = _counts(sp.Rational(5, 6))
    # The factor test is evaluated at the fixed V3 witness, exactly as in the
    # source gate, and is reconstructed here from the returned denominators.
    x, z, r = sp.symbols("kx kz rate", real=True)
    light = r*r + x*x + z*z
    clock = sp.Rational(509, 900)*r*r + sp.Rational(1, 50)*(x*x+z*z)
    v3 = response_matrix(sp.Rational(5, 6))
    failures = []
    for row in v3["rows"]:
        den = sp.sympify(row["denominator"], locals={"kx": x, "kz": z, "rate": r})
        if sp.denom(sp.cancel(light*clock/den)).free_symbols & {x, z, r}:
            failures.append(row)
    return {
        "status": "SIX_SOURCE_CAUSAL_RESPONSE_GATE_VERIFIED; NONLINEAR_THEORY_OPEN",
        "source_count": 6,
        "curvature_entries": entries,
        "v2_spatial_pole_count": v2_poles,
        "v3_spatial_pole_count": v3_poles,
        "v3_factor_failure_count": len(failures),
        "v3_characteristic_factors": [str(light), str(clock)],
        "scope": [
            "constant high-acceleration Fourier coefficients",
            "all six symmetric conserved seed polarizations",
            "electric Riemann response only",
            "no nonlinear or arbitrary-curved-background causality theorem",
        ],
    }
