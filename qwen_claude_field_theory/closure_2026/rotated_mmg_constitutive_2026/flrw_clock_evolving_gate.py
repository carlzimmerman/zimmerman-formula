"""Constructive FLRW branch with an evolving shift-symmetric clock speed.

The failed T=t specialization is not the whole shift-symmetric theory.  Let
chi=dot(T)^2 and use K(chi)=-A*sqrt(1-chi^2/L^2), 0<chi<L.  The homogeneous
clock equation is

    d_t[a^3 K_chi(chi) dot(T)] = 0.

For a conserved nonzero current J=C/a^3, the implicit equation for
z=chi/L is z^3/(1-z^2)=L*(C/(A*a^3))^2.  Its left side is strictly increasing
on (0,1), so every a>0 has a unique healthy root.  This script solves that
root by deterministic bisection on an expanding de Sitter test background and
checks K_chi>0, Sigma>0 and 0<c_s^2<1.  It is a constructive existence
witness for the evolving-clock branch, not a full Friedmann/metric proof.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


chi, A, Ld = sp.symbols("chi A Ld", positive=True)
K = -A * sp.sqrt(1 - chi**2 / Ld**2)
K_chi = sp.simplify(sp.diff(K, chi))
Sigma = sp.simplify(K_chi + 2 * chi * sp.diff(K_chi, chi))
c_s2 = sp.simplify(K_chi / Sigma)

z = sp.symbols("z", positive=True)
charge_shape = sp.simplify(z**3 / (1 - z**2))
charge_shape_derivative = sp.simplify(sp.diff(charge_shape, z))


def bisect_root(target: float, tol: float = 1e-13) -> float:
    """Unique root z in (0,1) of z^3/(1-z^2)=target."""

    lo, hi = 0.0, 1.0 - 1e-14
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        value = mid**3 / (1.0 - mid**2)
        if value < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


A_value = 1.0
Ld_value = 2.0
C_value = 0.4
a_values = np.geomspace(0.2, 8.0, 32)
rows = []
for aval in a_values:
    target = Ld_value * (C_value / (A_value * aval**3)) ** 2
    zval = bisect_root(target)
    chival = Ld_value * zval
    kx = float(K_chi.subs({A: A_value, Ld: Ld_value, chi: chival}).evalf())
    sig = float(Sigma.subs({A: A_value, Ld: Ld_value, chi: chival}).evalf())
    cs = float(c_s2.subs({A: A_value, Ld: Ld_value, chi: chival}).evalf())
    # The conserved current in the positive-chi convention is
    # A*sqrt(chi)*K_chi; its product with a^3 is the fixed C witness.
    current = aval**3 * np.sqrt(chival) * kx
    rows.append({"a": float(aval), "z": float(zval), "chi": float(chival), "K_chi": kx, "Sigma": sig, "c_s2": cs, "a3_current": current})

currents = np.array([row["a3_current"] for row in rows])
cs_values = np.array([row["c_s2"] for row in rows])
kx_values = np.array([row["K_chi"] for row in rows])
sigma_values = np.array([row["Sigma"] for row in rows])

results = {
    "K_chi": str(K_chi),
    "Sigma": str(Sigma),
    "clock_sound_speed_squared": str(c_s2),
    "charge_shape": str(charge_shape),
    "charge_shape_derivative": str(charge_shape_derivative),
    "charge_shape_strictly_increasing_on_0_1": bool(sp.simplify(charge_shape_derivative - z**2 * (3 - z**2) / (1 - z**2) ** 2) == 0),
    "expanding_background": "H=constant>0 de Sitter test; a in [0.2,8]",
    "unique_root_scan": len(rows),
    "positive_K_chi_scan": bool(np.all(kx_values > 0)),
    "positive_Sigma_scan": bool(np.all(sigma_values > 0)),
    "positive_clock_c_s2_scan": bool(np.all(cs_values > 0)),
    "subluminal_clock_c_s2_scan": bool(np.all(cs_values < 1)),
    "relative_current_spread": float((np.max(currents) - np.min(currents)) / np.mean(currents)),
    "current_target": C_value,
    "status": "OPEN: evolving-dotT shift-symmetric clock gives a healthy homogeneous FLRW witness; full metric stress, Friedmann solution, PPN and Dirac closure remain required.",
}

print(json.dumps(results, indent=2, sort_keys=True))
out = Path(__file__).parent / "run_001" / "flrw_clock_evolving_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert results["charge_shape_strictly_increasing_on_0_1"]
assert results["positive_K_chi_scan"]
assert results["positive_Sigma_scan"]
assert results["positive_clock_c_s2_scan"]
assert results["subluminal_clock_c_s2_scan"]
assert results["relative_current_spread"] < 1e-10
