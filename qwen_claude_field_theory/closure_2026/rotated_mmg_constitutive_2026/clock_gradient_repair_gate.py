"""Test the minimal healthy clock-gradient repair of the covariant branch.

The acceleration constitutive operator alone gives an omega^2 k^2 clock
principal term and hence c_s^2=0.  Add an explicitly counted k-essence clock
sector K(X)=-A*sqrt(1-X^2/L^2).  Its quadratic coefficients are K_X>0 and
Sigma=K_X+2 X K_XX>0.  The combined scalar symbol is

  P = (Sigma + lambda_parallel*kx^2
                 + lambda_perp*(ky^2+kz^2))*omega^2 - K_X*k^2.

This gate checks the repaired scalar is healthy and subluminal on a finite
scan, while making explicit that it is a propagating clock scalar rather than
an auxiliary mode.  It does not certify the metric Dirac algebra or PPN.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


X, A, Ld = sp.symbols("X A Ld", positive=True)
K = -A * sp.sqrt(1 - X**2 / Ld**2)
K_X = sp.simplify(sp.diff(K, X))
Sigma = sp.simplify(K_X + 2 * X * sp.diff(K_X, X))
c_s0_sq = sp.simplify(K_X / Sigma)

y, kx, ky, kz, omega = sp.symbols("y kx ky kz omega", positive=True)
lambda_perp = 1 - sp.exp(-y)
lambda_parallel = 1 + (y - 1) * sp.exp(-y)
k2 = kx**2 + ky**2 + kz**2
clock_accel_k = lambda_parallel * kx**2 + lambda_perp * (ky**2 + kz**2)
combined_symbol = sp.expand((Sigma + clock_accel_k) * omega**2 - K_X * k2)

f_kx = sp.lambdify((X, A, Ld), K_X, "numpy")
f_sigma = sp.lambdify((X, A, Ld), Sigma, "numpy")
f_cs0 = sp.lambdify((X, A, Ld), c_s0_sq, "numpy")
f_lp = sp.lambdify(y, lambda_parallel, "numpy")
f_lt = sp.lambdify(y, lambda_perp, "numpy")

xs = np.linspace(1e-3, 0.95, 64)
ys = np.geomspace(1e-8, 8.0, 80)
ks = np.geomspace(1e-4, 20.0, 40)
angles = np.linspace(0.0, np.pi / 2.0, 16)

kx_vals = f_kx(xs, 1.0, 1.0)
sigma_vals = f_sigma(xs, 1.0, 1.0)
cs_vals = f_cs0(xs, 1.0, 1.0)

dispersion = []
for yy in ys:
    lp = float(f_lp(yy))
    lt = float(f_lt(yy))
    for kk in ks:
        for theta in angles:
            kxx = kk * np.cos(theta)
            kyy = kk * np.sin(theta)
            ka = lp * kxx**2 + lt * kyy**2
            # Use the minimum clock-sector Sigma over the scan for a
            # conservative positivity check; A=Ld=1 is the witness scale.
            sig = float(np.min(sigma_vals))
            kx_min = float(np.min(kx_vals))
            c2 = kx_min / (sig + ka)
            dispersion.append(c2)

results = {
    "K_X": str(K_X),
    "Sigma": str(Sigma),
    "clock_sound_speed_squared": str(c_s0_sq),
    "combined_principal_symbol": str(combined_symbol),
    "positive_K_X_scan": bool(np.all(kx_vals > 0)),
    "positive_Sigma_scan": bool(np.all(sigma_vals > 0)),
    "positive_clock_c_s2_scan": bool(np.all(cs_vals > 0)),
    "subluminal_clock_c_s2_scan": bool(np.all(cs_vals < 1)),
    "combined_positive_frequency_coefficient": bool(np.all(np.asarray(dispersion) > 0)),
    "combined_subluminal_scan": bool(np.all(np.asarray(dispersion) < 1)),
    "combined_min_c_s2": float(np.min(dispersion)),
    "combined_max_c_s2": float(np.max(dispersion)),
    "acceleration_sector_at_y0": str(clock_accel_k.subs(y, 0)),
    "explicit_propagating_clock": True,
    "status": "OPEN: healthy clock-gradient repair found on finite scan; it adds one explicit propagating clock scalar, so full metric Dirac/PPN/Ward/FLRW closure remains mandatory.",
}

print(json.dumps(results, indent=2, sort_keys=True))
out = Path(__file__).parent / "run_001" / "clock_gradient_repair_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert results["positive_K_X_scan"]
assert results["positive_Sigma_scan"]
assert results["positive_clock_c_s2_scan"]
assert results["subluminal_clock_c_s2_scan"]
assert results["combined_positive_frequency_coefficient"]
assert results["combined_subluminal_scan"]
assert results["acceleration_sector_at_y0"] == "0"
