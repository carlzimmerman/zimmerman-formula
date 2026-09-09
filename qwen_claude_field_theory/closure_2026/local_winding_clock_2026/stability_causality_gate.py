"""Principal-symbol stress test for the local winding and cold sectors.

This is intentionally a bounded quadratic test around a fixed FLRW patch.  It
asks the sharp question the reduced action can answer without guessing the
full IC1 ADM perturbations: does the Q-lambda multiplier carry a k-dependent
hyperbolic principal symbol?  The answer is computed from the action and is
kept separate from the healthy canonical cold scalar.
"""

from functools import lru_cache

import sympy as sp


@lru_cache(None)
def stability_report():
    t, x = sp.symbols("t x", real=True)
    omega, k = sp.symbols("omega k", real=True)
    f = sp.symbols("f_Q", positive=True)
    q = sp.Function("delta_Q")(t, x)
    ell = sp.Function("delta_lambda")(t, x)
    sigma = sp.Function("delta_Theta")(t, x)
    cold = sp.Function("delta_chi")(t, x)
    qdot, elldot = sp.diff(q, t), sp.diff(ell, t)

    # Principal quadratic memory piece after imposing the background winding
    # equation.  sigma is the independent expansion perturbation; setting it
    # to zero isolates the clock sector on a fixed metric patch.
    L_mem = ell * (qdot - sigma)
    E_q = sp.diff(sp.diff(L_mem, qdot), t) - sp.diff(L_mem, q)
    E_ell = sp.diff(L_mem, ell)
    velocity_hessian = sp.hessian(L_mem, (qdot, elldot))
    memory_velocity_hessian_rank = int(velocity_hessian.rank())
    spatial_gradient_coefficient = sp.simplify(
        sp.diff(L_mem, sp.diff(q, x))
    )

    qh, lh, sh, ch = sp.symbols("q_hat lambda_hat sigma_hat chi_hat")
    iomega = sp.I * omega
    fourier_substitution = {
        q: qh,
        ell: lh,
        sigma: 0,
        sp.diff(q, t): iomega * qh,
        sp.diff(ell, t): iomega * lh,
    }
    memory_equations_fourier = [
        sp.expand(E_ell.xreplace(fourier_substitution)),
        sp.expand(E_q.xreplace(fourier_substitution)),
    ]
    memory_matrix = sp.Matrix([
        [sp.diff(eq, variable) for variable in (qh, lh)]
        for eq in memory_equations_fourier
    ])
    memory_determinant = sp.factor(memory_matrix.det())

    # A canonical cold scalar has the usual spatial gradient.  Its symbol is
    # generated from the Euler derivative rather than written down directly.
    cold_dot, cold_x = sp.diff(cold, t), sp.diff(cold, x)
    L_cold = f * (cold_dot ** 2 - cold_x ** 2) / 2
    E_cold = (
        sp.diff(sp.diff(L_cold, cold_dot), t)
        + sp.diff(sp.diff(L_cold, cold_x), x)
        - sp.diff(L_cold, cold)
    )
    cold_fourier = sp.expand(E_cold.xreplace({
        cold: ch,
        sp.diff(cold, t, 2): -omega ** 2 * ch,
        sp.diff(cold, x, 2): -k ** 2 * ch,
    }))
    cold_characteristic = sp.factor(cold_fourier.coeff(ch))
    cold_velocity_hessian = sp.diff(L_cold, cold_dot, cold_dot)

    return {
        "mode": "fixed_FLRW_principal_patch",
        "omega": omega,
        "k": k,
        "memory_equations": (E_q, E_ell),
        "memory_matrix": memory_matrix,
        "memory_characteristic_determinant": memory_determinant,
        "memory_velocity_hessian": velocity_hessian,
        "memory_velocity_hessian_rank": memory_velocity_hessian_rank,
        "memory_spatial_gradient_coefficient": spatial_gradient_coefficient,
        "zero_gradient_flag": spatial_gradient_coefficient == 0,
        "cold_euler_equation": E_cold,
        "cold_characteristic_determinant": cold_characteristic,
        "cold_kinetic_coefficient": sp.simplify(cold_velocity_hessian / 2),
        "interpretation": (
            "The Q-lambda block has a k-independent zero-frequency principal "
            "symbol and vanishing velocity Hessian; this is a strong-coupling "
            "risk, not a healthy propagating scalar."
        ),
    }


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[encode(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(encode(stability_report()), indent=2))
