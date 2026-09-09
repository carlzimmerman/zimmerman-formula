#!/usr/bin/env python3
"""On-shell falsification of the ALC acceleration source.

The displayed ALC action contains

    -sigma/2 (g^munu T_,mu T_,nu + 1)

and therefore its sigma Euler--Lagrange equation is the unit-timelike
constraint.  With n_mu=-T_,mu on that shell, the Hessian of T is symmetric and

    a_mu = n^nu nabla_nu n_mu
          = -n^nu nabla_nu nabla_mu T
          = 1/2 nabla_mu(n^nu n_nu) = 0.

The ALC MOND term is a function only of sqrt(a_mu a^mu).  This gate derives
the identity, verifies it in a linear static metric/clock perturbation, and
checks the value and first variation of the exact ALC correction at a=0.
Thus the action as written cannot have both its mimetic equation and a
nonzero static acceleration MOND source.  This is a falsification of this
candidate, not a universal no-go for non-mimetic or non-gradient carriers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def _covariant_identity():
    n0, n1 = sp.symbols("n0 n1", real=True)
    h00, h01, h11 = sp.symbols("H00 H01 H11", real=True)
    # H_mu nu = nabla_mu nabla_nu T is symmetric for a scalar.
    acceleration = sp.Matrix([
        -(n0 * h00 + n1 * h01),
        -(n0 * h01 + n1 * h11),
    ])
    gradient_norm = sp.Matrix([
        -2 * (n0 * h00 + n1 * h01),
        -2 * (n0 * h01 + n1 * h11),
    ])
    residual = sp.simplify(acceleration - gradient_norm / 2)
    return {
        "acceleration": acceleration,
        "half_norm_gradient": gradient_norm / 2,
        "identity_residual": residual,
        "identity_holds": all(item == 0 for item in residual),
    }


def _static_linear_constraint():
    eps = sp.symbols("epsilon", real=True)
    t, x = sp.symbols("t x", real=True)
    lapse = sp.Function("Lapse")(t, x)
    spatial = sp.Function("SpatialPotential")(t, x)
    tau = sp.Function("tau")(t, x)
    # Newtonian-gauge metric: g00=-(1+2 eps Lapse), gxx=1-2 eps Spatial.
    # T=t+eps*tau.  Terms through first order are retained by coefficient
    # extraction, rather than imposing the constraint before variation.
    g00_inv = -1 + 2 * eps * lapse
    gxx_inv = 1 + 2 * eps * spatial
    Tt = 1 + eps * sp.diff(tau, t)
    Tx = eps * sp.diff(tau, x)
    X = sp.expand(g00_inv * Tt**2 + gxx_inv * Tx**2)
    constraint_linear = sp.simplify(sp.expand(X + 1).coeff(eps, 1))
    lapse_norm_linear = sp.simplify(
        sp.expand(sp.sqrt(-X).series(eps, 0, 2).removeO()).coeff(eps, 1)
    )
    # For a hypersurface-orthogonal normal the linear acceleration is minus
    # the spatial gradient of this normalization perturbation in these signs.
    acceleration_x_linear = sp.simplify(-sp.diff(lapse_norm_linear, x))
    on_constraint = {sp.diff(tau, t): lapse}
    return {
        "X_plus_one_linear": constraint_linear,
        "constraint_solution_taudot": sp.solve(sp.Eq(constraint_linear, 0), sp.diff(tau, t))[0],
        "normalization_linear": lapse_norm_linear,
        "acceleration_x_linear": acceleration_x_linear,
        "acceleration_on_constraint": sp.simplify(acceleration_x_linear.subs(on_constraint)),
        "static_constraint_solution": sp.solve(
            sp.Eq(constraint_linear.subs(sp.diff(tau, t), 0), 0), lapse
        ),
        "spatial_potential_does_not_enter_constraint_at_linear_order":
            spatial not in constraint_linear.free_symbols,
    }


def _alc_correction():
    y = sp.symbols("y", nonnegative=True)
    H = sp.simplify(2 * (1 + y) * sp.exp(-y) - 2)
    return {
        "H": H,
        "H_at_zero": sp.simplify(H.subs(y, 0)),
        "H_prime_at_zero": sp.simplify(sp.diff(H, y).subs(y, 0)),
        "H_second_at_zero": sp.simplify(sp.diff(H, y, 2).subs(y, 0)),
        "H_prime": sp.factor(sp.diff(H, y)),
        "static_mond_flux_multiplier": sp.simplify(1 - sp.exp(-y)),
        "on_shell_linear_source": sp.simplify(sp.diff(H, y).subs(y, 0)),
    }


def _projectable_check():
    t, x = sp.symbols("t x", real=True)
    lapse = sp.Function("Lapse")(t)
    # D_x ln N is zero when N is projectable.
    return {
        "lapse": lapse,
        "spatial_acceleration": sp.simplify(sp.diff(sp.log(lapse), x)),
    }


def derive_gate():
    identity = _covariant_identity()
    static = _static_linear_constraint()
    correction = _alc_correction()
    projectable = _projectable_check()
    return {
        "action_fragment": "-sigma/2*(g^munu*d_mu T*d_nu T + 1) - 2*M2*a0^2*H(sqrt(a^2)/a0)",
        "sigma_euler_lagrange": "g^munu*d_mu T*d_nu T + 1 = 0",
        "covariant": identity,
        "static_linear": static,
        "alc_correction": correction,
        "projectable": projectable,
        "status": "DEAD_FOR_ALC_ACTION_AS_WRITTEN",
        "scope": "the displayed mimetic ALC action; excludes non-gradient clocks, removal of the sigma constraint, and different MOND carriers",
    }


def _jsonable(value):
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(v) for v in value]
    if isinstance(value, sp.MatrixBase):
        return [[_jsonable(v) for v in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "mimetic_acceleration_nogo.json")
    args = parser.parse_args(argv)
    result = _jsonable(derive_gate())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
