"""Homogeneous FLRW variation for the local cumulative-winding clock."""

from functools import lru_cache

import sympy as sp


def _euler_lagrange(lagrangian, field, velocity, coordinate):
    return sp.expand(
        sp.diff(sp.diff(lagrangian, velocity), coordinate)
        - sp.diff(lagrangian, field)
    )


@lru_cache(None)
def flrw_report():
    t = sp.symbols("t", real=True)
    m, Lambda, beta, mc = sp.symbols(
        "m Lambda beta m_c", positive=True
    )
    a_ref, Q0, lambda0 = sp.symbols(
        "a_ref Q0 lambda0", positive=True
    )
    a = sp.Function("a_f")(t)
    N = sp.Function("N_f")(t)
    Q = sp.Function("Q_f")(t)
    lam = sp.Function("lambda_f")(t)
    chi = sp.Function("chi_f")(t)
    adot, Qdot, chidot = sp.diff(a, t), sp.diff(Q, t), sp.diff(chi, t)

    # Einstein-Hilbert minisuperspace after the standard boundary-term
    # subtraction, plus the signed winding memory and canonical cold scalar.
    # The lapse is retained as a field until after all variations are formed.
    L_grav = -3 * m * a * adot ** 2 / N - m * Lambda * N * a ** 3
    L_mem = a ** 3 * lam * (Qdot - adot / a)
    L_cold = a ** 3 * sp.exp(-beta * Q) * (
        chidot ** 2 / (2 * N) - N * mc ** 2 * chi ** 2 / 2
    )
    L_total = L_grav + L_mem + L_cold

    lapse_equation = sp.simplify(sp.diff(L_total, N))
    scale_equation = _euler_lagrange(L_total, a, adot, t)
    memory_equation = sp.simplify(
        _euler_lagrange(L_total, Q, Qdot, t)
    )
    multiplier_equation = sp.simplify(sp.diff(L_total, lam))
    cold_scalar_equation = _euler_lagrange(L_total, chi, chidot, t)

    H = sp.sqrt(Lambda / 3)
    a_sol = a_ref * sp.exp(Q0 + H * t)
    N_sol = sp.Integer(1)
    Q_sol = Q0 + H * t
    lam_sol = lambda0 * sp.exp(-3 * H * t)
    chi_sol = sp.Integer(0)
    solution = {
        a: a_sol,
        N: N_sol,
        Q: Q_sol,
        lam: lam_sol,
        chi: chi_sol,
        sp.diff(a, t): sp.diff(a_sol, t),
        sp.diff(a, t, 2): sp.diff(a_sol, t, 2),
        sp.diff(N, t): sp.Integer(0),
        sp.diff(Q, t): sp.diff(Q_sol, t),
        sp.diff(Q, t, 2): sp.Integer(0),
        sp.diff(lam, t): sp.diff(lam_sol, t),
        sp.diff(chi, t): sp.Integer(0),
        sp.diff(chi, t, 2): sp.Integer(0),
    }
    equation_residuals = {
        "lapse": sp.simplify(lapse_equation.subs(solution)),
        "scale": sp.simplify(scale_equation.subs(solution)),
        "memory": sp.simplify(memory_equation.subs(solution)),
        "multiplier": sp.simplify(multiplier_equation.subs(solution)),
        "cold_scalar": sp.simplify(cold_scalar_equation.subs(solution)),
    }
    memory_integral_residual = sp.simplify(
        (Q - sp.log(a / a_ref)).subs(solution)
    )

    return {
        "time": t,
        "m": m,
        "Lambda": Lambda,
        "beta": beta,
        "m_c": mc,
        "lagrangian": L_total,
        "lapse_equation": lapse_equation,
        "scale_equation": scale_equation,
        "memory_equation": memory_equation,
        "multiplier_equation": multiplier_equation,
        "cold_scalar_equation": cold_scalar_equation,
        "expanding_solution": {
            "a": a_sol,
            "N": N_sol,
            "Q": Q_sol,
            "lambda": lam_sol,
            "chi_c": chi_sol,
            "H": H,
            "equation_residuals": equation_residuals,
        },
        "memory_integral_residual": memory_integral_residual,
        "cold_kinetic_coefficient": sp.exp(-beta) / 2,
    }


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


if __name__ == "__main__":
    import json

    print(json.dumps(encode(flrw_report()), indent=2))
