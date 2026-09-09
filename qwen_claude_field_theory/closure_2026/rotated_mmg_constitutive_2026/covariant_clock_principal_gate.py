"""Principal-symbol gate for the covariant clock/Stueckelberg completion.

For T=t+pi on a locally flat background, the unit-clock acceleration obeys
delta a_i = -d_i d_t pi at linear order.  An acceleration-only constitutive
term therefore supplies a quadratic principal symbol proportional to
omega^2 k_i K_ij k_j, but no omega^0 spatial-gradient term.  This script
derives the constitutive Jacobian from the exact exponential kernel and
checks the resulting zero-speed/ellipticity limits without hard-coded ranks.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


y, a0, omega, kx, ky, kz = sp.symbols("y a0 omega kx ky kz", positive=True)
mu = 1 - sp.exp(-y)
G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2

# Jacobian of f_i(a)=mu(|a|/a0) a_i.  The transverse and longitudinal
# eigenvalues are obtained by differentiating the exact constitutive law.
lambda_perp = sp.simplify(mu)
lambda_parallel = sp.simplify(mu + y * sp.diff(mu, y))

kernel_identity = sp.simplify(sp.diff(G, y) / (2 * y) - mu)
parallel_identity = sp.simplify(lambda_parallel - (1 + (y - 1) * sp.exp(-y)))

# A local acceleration background selects x.  The clock perturbation has
# delta a_i=-d_i d_t pi, so the highest-derivative polynomial is
# P = omega^2 [lambda_parallel*kx^2 + lambda_perp*(ky^2+kz^2)].
principal = sp.expand(
    omega**2 * (lambda_parallel * kx**2 + lambda_perp * (ky**2 + kz**2))
)
spatial_gradient_coefficient = sp.simplify(principal.subs(omega, 0))
clock_speed_numerator = spatial_gradient_coefficient

eigen_det = sp.simplify(lambda_perp**2 * lambda_parallel)
small_y_perp = sp.limit(lambda_perp / y, y, 0, dir="+")
small_y_parallel = sp.limit(lambda_parallel / y, y, 0, dir="+")

sample = {y: sp.Integer(1), kx: sp.Integer(1), ky: sp.Integer(2), kz: sp.Integer(0)}
sample_principal_over_omega2 = sp.simplify(principal.subs(sample) / omega**2)

results = {
    "kernel_identity": kernel_identity == 0,
    "parallel_eigenvalue_identity": parallel_identity == 0,
    "lambda_perp": str(lambda_perp),
    "lambda_parallel": str(lambda_parallel),
    "principal_symbol": str(principal),
    "omega_zero_spatial_gradient": spatial_gradient_coefficient == 0,
    "clock_speed_numerator": str(clock_speed_numerator),
    "elliptic_determinant": str(eigen_det),
    "ellipticity_lost_at_y0": sp.simplify(eigen_det.subs(y, 0)) == 0,
    "small_y_lambda_perp_over_y": str(small_y_perp),
    "small_y_lambda_parallel_over_y": str(small_y_parallel),
    "sample_y1_principal_over_omega2": str(sample_principal_over_omega2),
    "status": "OBSTRUCTION: acceleration-only covariant clock has c_s^2=0 at the principal-symbol level; a healthy completion needs an additional clock-gradient operator or a demonstrated second-class gauge removal.",
}

print(json.dumps(results, indent=2, sort_keys=True))

out = Path(__file__).parent / "run_001" / "covariant_clock_principal_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert results["kernel_identity"]
assert results["parallel_eigenvalue_identity"]
assert results["omega_zero_spatial_gradient"]
assert results["ellipticity_lost_at_y0"]
assert small_y_perp == 1
assert small_y_parallel == 2
