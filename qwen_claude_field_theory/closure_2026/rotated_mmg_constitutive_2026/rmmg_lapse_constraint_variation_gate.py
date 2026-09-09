"""Action-level lapse variation check for the rotated-MMG constraint.

The candidate defines u=log(N) (holding h fixed on the local affine test) and
also places N in front of C=Dx(mu(|Dx u|) Dx u).  Those two appearances are
not independent in an Euler--Lagrange variation.  This gate computes the
higher-derivative Euler operator of the displayed term -N*C directly, then
evaluates the affine witness N=exp(k*x), k>0.  It does not insert the result
by hand and does not infer a nonlinear no-go beyond this action/branch.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


x, k = sp.symbols("x k", positive=True)
N = sp.Function("N")(x)

# At fixed h and a0=1, u_x=N_x/N on the positive-slope affine branch.
u_x = sp.diff(N, x) / N
mu = 1 - sp.exp(-u_x)
advertised_constraint = sp.diff(mu * u_x, x)
lagrangian = sp.simplify(-N * advertised_constraint)

# L contains N_xx, so use the second-derivative Euler operator.
N1 = sp.diff(N, x)
N2 = sp.diff(N, x, 2)
euler_lapse = sp.simplify(
    sp.diff(lagrangian, N)
    - sp.diff(sp.diff(lagrangian, N1), x)
    + sp.diff(sp.diff(lagrangian, N2), x, 2)
)

N_affine = sp.exp(k * x)
affine_substitutions = {
    N: N_affine,
    sp.diff(N, x): sp.diff(N_affine, x),
    sp.diff(N, x, 2): sp.diff(N_affine, x, 2),
    sp.diff(N, x, 3): sp.diff(N_affine, x, 3),
    sp.diff(N, x, 4): sp.diff(N_affine, x, 4),
}

constraint_affine = sp.simplify(advertised_constraint.subs(affine_substitutions))
euler_affine = sp.factor(euler_lapse.subs(affine_substitutions))
expected_affine = sp.factor(-k**2 * (1 + (k - 1) * sp.exp(-k)))

checks = {
    "advertised_constraint_vanishes_on_affine": constraint_affine == 0,
    "euler_residual_derived": sp.simplify(euler_affine - expected_affine) == 0,
    "unit_slope_residual_nonzero": sp.simplify(euler_affine.subs(k, 1) + 1) == 0,
    "unit_slope_constraint_still_zero": sp.simplify(constraint_affine.subs(k, 1)) == 0,
}

results = {
    "mu": str(mu),
    "advertised_constraint": str(advertised_constraint),
    "lagrangian": str(lagrangian),
    "euler_lapse": str(euler_lapse),
    "affine_constraint": str(constraint_affine),
    "affine_euler_residual": str(euler_affine),
    "expected_affine_residual": str(expected_affine),
    "unit_slope_euler_residual": str(sp.simplify(euler_affine.subs(k, 1))),
    "checks": checks,
    "status": (
        "OBSTRUCTION: because u=log(N) occurs inside the N-weighted constraint, "
        "the actual lapse Euler equation contains a nonzero affine residual; "
        "the advertised MOND constraint is not the lapse equation of this action."
    ),
}

print(json.dumps(results, indent=2, sort_keys=True))
out = Path(__file__).parent / "run_001" / "rmmg_lapse_constraint_variation_results.json"
out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")

assert all(checks.values())
