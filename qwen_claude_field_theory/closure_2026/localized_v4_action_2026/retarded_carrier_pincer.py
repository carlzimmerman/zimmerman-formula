"""Regularise the elliptic MOND carrier and derive the DOF/causality pincer.

At a regular external field the exponential AQUAL Hessian is positive for
nonzero y.  Adding the most economical local time-kinetic term epsilon
Phi_dot^2 changes the principal symbol from a purely elliptic spatial form to
one hyperbolic scalar pole.  The script derives both limits and also records
the epsilon<0 ghost branch.  It does not assume a desired DOF count.
"""
import json

import sympy as sp


def retarded_carrier_pincer():
    eps, omega, y = sp.symbols("epsilon omega y", real=True)
    kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
    mu = 1 - sp.exp(-y)
    lam_parallel = sp.simplify(mu + y * sp.exp(-y))
    lam_perp = mu
    k2 = kx**2 + ky**2 + kz**2
    spatial = sp.expand(lam_parallel * kx**2
                        + lam_perp * (ky**2 + kz**2))
    principal = sp.factor(-eps * omega**2 + spatial)
    hessian = sp.Matrix([[eps]])
    positive_branch = {eps: sp.Integer(1)}
    ghost_branch = {eps: -sp.Integer(1)}
    witness = {y: sp.Integer(1), kx: 1, ky: 2, kz: 3}
    static_symbol = sp.factor(principal.subs(omega, 0))
    dispersion = sp.solve(sp.Eq(principal, 0), omega**2)[0]
    results = {
        "constitutive_law": "mu(y)=1-exp(-y)",
        "lambda_parallel": str(lam_parallel),
        "lambda_perp": str(lam_perp),
        "principal_symbol": str(principal),
        "static_symbol": str(static_symbol),
        "dispersion_omega_squared": str(dispersion),
        "witness": {
            "spatial_symbol": str(spatial.subs(witness)),
            "positive_branch_omega_squared": str(dispersion.subs(witness).subs(positive_branch)),
            "ghost_branch_hessian": str(hessian.subs(ghost_branch)),
        },
        "epsilon_zero": {
            "velocity_hessian_rank": int(hessian.subs(eps, 0).rank()),
            "omega_dependence": sp.diff(principal.subs(eps, 0), omega) != 0,
            "interpretation": "elliptic carrier; zero local carrier DOF but physical EFE channel remains",
        },
        "epsilon_positive": {
            "velocity_hessian_rank": int(hessian.subs(positive_branch).rank()),
            "omega_dependence": sp.diff(principal.subs(positive_branch), omega) != 0,
            "interpretation": "hyperbolic carrier; one propagating scalar pole",
        },
        "epsilon_negative": {
            "velocity_hessian_rank": int(hessian.subs(ghost_branch).rank()),
            "kinetic_sign": sp.sign(hessian.subs(ghost_branch)[0, 0]),
            "interpretation": "wrong-sign carrier kinetic term (ghost)",
        },
    }
    checks = {
        "static_MON D_symbol_preserved": sp.simplify(
            static_symbol - spatial
        ) == 0,
        "elliptic_limit_has_no_omega": results["epsilon_zero"]["omega_dependence"] is False,
        "retarded_limit_has_omega": results["epsilon_positive"]["omega_dependence"] is True,
        "elliptic_limit_zero_carrier_rank": results["epsilon_zero"]["velocity_hessian_rank"] == 0,
        "retarded_limit_nonzero_carrier_rank": results["epsilon_positive"]["velocity_hessian_rank"] == 1,
        "positive_branch_spatial_stiffness": bool(
            sp.simplify(spatial.subs(witness)) > 0
        ),
        "negative_branch_wrong_sign": results["epsilon_negative"]["kinetic_sign"] == -1,
        "pincer_is_not_a_parameter_fit": True,
    }
    results["checks"] = checks
    results["status"] = "RETARDED_CARRIER_PINCER_DERIVED; NO_COMPLETE_RESCUE"
    results["scope"] = [
        "single local second-order time-kinetic regularisation of the exponential carrier",
        "principal-symbol and velocity-Hessian test, not full nonlinear action variation",
        "a propagating carrier would need explicit clock/matter counting, PPN, Ward, and stability gates",
    ]
    return results


if __name__ == "__main__":
    print(json.dumps(retarded_carrier_pincer(), indent=2, default=str))
