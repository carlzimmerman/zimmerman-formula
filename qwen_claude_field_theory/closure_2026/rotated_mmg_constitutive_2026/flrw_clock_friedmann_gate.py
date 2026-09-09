"""Minisuperspace Friedmann gate for the evolving DBI clock branch.

Use chi=dot(T)^2 and K(chi)=-A*sqrt(1-chi^2/L^2), 0<chi<L.  The homogeneous
shift current is J=a^3 K_chi sqrt(chi).  Writing z=chi/L gives a^3
z^(3/2)/sqrt(1-z^2)=constant.  The stress tensor is

    rho=A(1+z^2)/sqrt(1-z^2),   p=-A*sqrt(1-z^2),
    w=-(1-z^2)/(1+z^2).

This gate proves the exact continuity identity and constructs a positive-H
Friedmann witness on a finite expanding interval.  It is the concrete
cosmological branch to use in the later full metric/Dirac calculation.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


A, Ld, z = sp.symbols("A Ld z", positive=True)
chi = Ld * z
K = sp.simplify(-A * sp.sqrt(1 - chi**2 / Ld**2))
K_chi = sp.simplify(sp.diff(-A * sp.sqrt(1 - sp.symbols("q")**2 / Ld**2), sp.symbols("q")).subs(sp.symbols("q"), chi))
rho = sp.simplify(2 * chi * K_chi - K)
p = sp.simplify(K)
w = sp.simplify(p / rho)

current_shape = sp.simplify(z ** sp.Rational(3, 2) / sp.sqrt(1 - z**2))
dcurrent_dz = sp.simplify(sp.diff(current_shape, z))
dz_dln_a = sp.simplify(-3 * current_shape / dcurrent_dz)
drho_dz = sp.simplify(sp.diff(rho, z))
continuity_residual = sp.simplify(drho_dz * dz_dln_a + 3 * (rho + p))

# Derive the same rho and p directly from a homogeneous lapse/scale-factor
# minisuperspace action, rather than inserting the perfect-fluid formulas.
N, qdot, aa = sp.symbols("N qdot aa", positive=True)
chi_N = qdot**2 / N**2
K_N = -A * sp.sqrt(1 - chi_N**2 / Ld**2)
L_mini = N * aa**3 * K_N
rho_from_lapse = sp.simplify(
    -sp.diff(L_mini, N).subs({N: 1, qdot: sp.sqrt(Ld * z)}) / aa**3
)
p_from_scale = sp.simplify(
    sp.diff(L_mini, aa).subs({N: 1, qdot: sp.sqrt(Ld * z)}) / (3 * aa**2)
)


def bisect_root(target: float, tol: float = 1e-13) -> float:
    lo, hi = 0.0, 1.0 - 1e-14
    for _ in range(240):
        mid = 0.5 * (lo + hi)
        value = mid ** 1.5 / np.sqrt(1.0 - mid**2)
        if value < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


A_value = 1.0
Ld_value = 2.0
z_at_a1 = 0.5922633671067405
current_at_a1 = z_at_a1**1.5 / np.sqrt(1.0 - z_at_a1**2)
a_values = np.geomspace(0.02, 100.0, 96)
rows = []
for aval in a_values:
    zval = bisect_root(current_at_a1 / aval**3)
    rhoval = float(rho.subs({A: A_value, Ld: Ld_value, z: zval}).evalf())
    pval = float(p.subs({A: A_value, Ld: Ld_value, z: zval}).evalf())
    wval = pval / rhoval
    rows.append({"a": float(aval), "z": zval, "rho": rhoval, "p": pval, "w": wval, "rho_a3": rhoval * aval**3})

rho_values = np.array([row["rho"] for row in rows])
w_values = np.array([row["w"] for row in rows])
rho_a3 = np.array([row["rho_a3"] for row in rows])

# Positive expanding Friedmann witness in dimensionless units.  The clock
# density is normalized at a=1 and a positive Lambda component is included.
rho_ref = float(rho.subs({A: A_value, Ld: Ld_value, z: z_at_a1}).evalf())
omega_lambda = 0.7
omega_clock = 0.3
H_values = np.sqrt(omega_lambda + omega_clock * rho_values / rho_ref)
ln_a = np.log(a_values)
cosmic_time_span = float(np.trapz(1.0 / H_values, ln_a))

# Dust and de Sitter asymptotic checks use interior points to avoid finite-
# precision saturation at z=1.
early = np.where(a_values < 0.12)[0]
late = np.where(a_values > 20.0)[0]
early_rho_a3_spread = float((np.max(rho_a3[early]) - np.min(rho_a3[early])) / np.mean(rho_a3[early]))
late_rho_spread = float((np.max(rho_values[late]) - np.min(rho_values[late])) / np.mean(rho_values[late]))

results = {
    "K_chi": str(K_chi),
    "rho": str(rho),
    "pressure": str(p),
    "equation_of_state": str(w),
    "current_shape": str(current_shape),
    "dcurrent_dz": str(dcurrent_dz),
    "dz_dln_a": str(dz_dln_a),
    "continuity_residual": str(continuity_residual),
    "continuity_identity_exact": continuity_residual == 0,
    "rho_from_lapse_variation": str(rho_from_lapse),
    "pressure_from_scale_variation": str(p_from_scale),
    "lapse_variation_matches_rho": sp.simplify(rho_from_lapse - rho) == 0,
    "scale_variation_matches_pressure": sp.simplify(p_from_scale - p) == 0,
    "a_interval": [0.02, 100.0],
    "number_of_FLRW_samples": len(rows),
    "early_dust_rho_a3_relative_spread": early_rho_a3_spread,
    "late_vacuum_rho_relative_spread": late_rho_spread,
    "w_min": float(np.min(w_values)),
    "w_max": float(np.max(w_values)),
    "positive_H_witness": bool(np.all(H_values > 0)),
    "H_min": float(np.min(H_values)),
    "H_max": float(np.max(H_values)),
    "finite_positive_cosmic_time_span": bool(cosmic_time_span > 0 and np.isfinite(cosmic_time_span)),
    "cosmic_time_span_dimensionless": cosmic_time_span,
    "status": "OPEN: unified clock dust-to-vacuum FLRW minisuperspace branch constructed; full metric stress perturbations, Dirac closure and PPN remain required.",
}

print(json.dumps(results, indent=2, sort_keys=True))
out = Path(__file__).parent / "run_001" / "flrw_clock_friedmann_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert results["continuity_identity_exact"]
assert results["lapse_variation_matches_rho"]
assert results["scale_variation_matches_pressure"]
assert results["positive_H_witness"]
assert results["finite_positive_cosmic_time_span"]
assert -1 < results["w_min"] < results["w_max"] < 0
assert early_rho_a3_spread < 0.01
assert late_rho_spread < 0.01
