"""A parameter-free deep-MOND action-angle invariant.

The exact logarithmic deep-MOND orbit quadratures give
T_r = F(e) R / v_inf and ell = J(e) R v_inf, with
v_inf^4 = G M_b a0.  This script derives the cancellation symbolically and
evaluates the invariant from the repository's independent quadrature code.
It is a conditional weak-static prediction, not a relativistic closure.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "hpi_delta_eccentric_kepler_2026" / "hpi_delta_eccentric_kepler_2026.py"
spec = importlib.util.spec_from_file_location("hpi_delta", SOURCE)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load quadrature source: {SOURCE}")
hpi = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = hpi
spec.loader.exec_module(hpi)

F, J, R, v, S = sp.symbols("F J R v S", positive=True)
T_r = F * R / v
ell = J * R * v
invariant = sp.factor(T_r * S / ell)
invariant_after_scale = sp.simplify(invariant.subs(S, v**2))

F1, F2, J1, J2 = sp.symbols("F1 F2 J1 J2", positive=True)
pair_ratio = sp.factor(
    ((F1 * R / v) * (J2 * R * v)) / ((F2 * R / v) * (J1 * R * v))
)
pair_target = F1 * J2 / (F2 * J1)

eccentricities = (0.1, 0.3, 0.6, 0.9)
rows = []
for e in eccentricities:
    data = hpi.deep_log_orbit(e)
    f_value = float(data["radial_period_scaled"])
    j_value = math.sqrt(float(data["j_squared"]))
    rows.append(
        {
            "eccentricity": e,
            "F": f_value,
            "J": j_value,
            "A_of_e": f_value / j_value,
        }
    )

checks = {
    "single_orbit_cancellation": sp.simplify(invariant_after_scale - F / J) == 0,
    "two_orbit_cancellation": sp.simplify(pair_ratio - pair_target) == 0,
    "quadrature_rows_finite": all(math.isfinite(row["A_of_e"]) for row in rows),
}

results = {
    "symbolic_invariant": str(invariant),
    "invariant_after_vinf4_relation": str(invariant_after_scale),
    "pair_ratio": str(pair_ratio),
    "pair_target": str(pair_target),
    "rows": rows,
    "checks": checks,
    "prediction": (
        "For two deep-MOND orbits around one source, "
        "T_r1*ell2/(T_r2*ell1)=A(e1)/A(e2), independent of M_b, a0, R."
    ),
    "status": "OPEN: conditional weak-static action-angle prediction; relativistic closure remains unresolved.",
}

print(json.dumps(results, indent=2, sort_keys=True))
out = ROOT / "run_001" / "action_angle_invariant_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
assert all(checks.values())
