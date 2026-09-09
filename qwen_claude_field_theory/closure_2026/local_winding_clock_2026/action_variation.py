"""Exact first-gate variations for the local-winding-clock action.

The calculations are deliberately split into a homogeneous ADM block and a
one-dimensional static weak-field block.  They derive identities from the
displayed action; they do not import a desired rank, PPN value, or DOF count.
"""
from functools import lru_cache

import sympy as sp


def clock_potential(c):
    one_minus = 1 - c
    return one_minus * (
        sp.log(one_minus) ** 2 - 2 * sp.log(one_minus) + 2
    ) - 2


def _euler_lagrange(lagrangian, field, velocity, coordinate):
    return sp.expand(
        sp.diff(sp.diff(lagrangian, velocity), coordinate)
        - sp.diff(lagrangian, field)
    )


@lru_cache(None)
def derive_action():
    t = sp.symbols("t", real=True)
    a, N, Q, lam, chi = (sp.Function(name)(t)
                          for name in ("a", "N", "Q", "lambda", "chi"))
    beta, mc = sp.symbols("beta m_c", real=True)
    adot, Qdot, chidot = sp.diff(a, t), sp.diff(Q, t), sp.diff(chi, t)
    theta = adot / (N * a)
    memory = a ** 3 * lam * (Qdot - N * theta)
    cold = a ** 3 * sp.exp(-beta * Q) * (
        chidot ** 2 / (2 * N) - N * mc ** 2 * chi ** 2 / 2
    )
    total = memory + cold

    memory_lambda = sp.diff(memory, lam)
    memory_equation = Qdot - N * theta
    memory_q_equation = _euler_lagrange(total, Q, Qdot, t)
    memory_q_target = sp.diff(a ** 3 * lam, t) + beta * cold
    cold_scalar_equation = _euler_lagrange(cold, chi, chidot, t)

    y = sp.symbols("y", positive=True)
    mu = 1 - sp.exp(-y)
    primitive = y ** 2 + 2 * (1 + y) * sp.exp(-y) - 2

    return {
        "symbols": {"t": t, "a": a, "N": N, "Q": Q, "lambda": lam,
                    "chi_c": chi, "beta": beta, "m_c": mc},
        "memory_lagrangian": memory,
        "cold_lagrangian": cold,
        "primitive": primitive,
        "mu": mu,
        "primitive_residual": sp.simplify(sp.diff(primitive, y) / (2 * y) - mu),
        "memory_lambda_equation": memory_lambda,
        "memory_target": memory_equation,
        "memory_residual": sp.simplify(memory_lambda / a ** 3 - memory_equation),
        "memory_q_equation": memory_q_equation,
        "memory_q_target": memory_q_target,
        "memory_adjoint_residual": sp.simplify(memory_q_equation - memory_q_target),
        "cold_scalar_equation": cold_scalar_equation,
        "cold_scalar_residual": sp.simplify(
            _euler_lagrange(total, chi, chidot, t) - cold_scalar_equation
        ),
    }


@lru_cache(None)
def static_branch():
    x = sp.symbols("x", real=True)
    m, a0 = sp.symbols("m a0", positive=True)
    Phi = sp.Function("Phi")(x)
    Psi = sp.Function("Psi")(x)
    u = sp.Function("u")(x)
    rho = sp.Function("rho")(x)
    phi_x, psi_x, u_x = sp.diff(Phi, x), sp.diff(Psi, x), sp.diff(u, x)
    density = m * (
        (1 - u ** 2) * phi_x ** 2 + psi_x ** 2
        - 2 * phi_x * psi_x - a0 ** 2 * clock_potential(u ** 2)
    ) - rho * Phi

    e_phi = sp.diff(density, Phi) - sp.diff(sp.diff(density, phi_x), x)
    e_psi = sp.diff(density, Psi) - sp.diff(sp.diff(density, psi_x), x)
    y = phi_x / a0
    mu = 1 - sp.exp(-y)
    slip_substitution = {sp.diff(Psi, x): phi_x}
    e_phi_slip = sp.simplify(e_phi.subs(slip_substitution))
    e_psi_slip = sp.simplify(e_psi.subs(slip_substitution))
    u_branch = sp.sqrt(mu)
    branch_substitution = {
        u: u_branch,
        sp.diff(u, x): sp.diff(u_branch, x),
    }
    e_phi_branch = sp.simplify(
        e_phi_slip.subs(branch_substitution, simultaneous=True)
    )
    mond_equation = 2 * m * sp.diff(mu * phi_x, x) - rho

    return {
        "density": density,
        "lapse_equation": e_phi,
        "conformal_equation": e_psi,
        "lapse_equation_slip": e_phi_slip,
        "lapse_equation_exponential_branch": e_phi_branch,
        "conformal_equation_slip": e_psi_slip,
        "mond_equation": mond_equation,
        "mond_residual": sp.simplify(e_phi_branch - mond_equation),
        "slip_residual": e_psi_slip,
        "measured_G": sp.simplify(1 / (8 * sp.pi * m)),
        "constitutive_law": mu,
        "coordinate": x,
        "fields": {"Phi": Phi, "Psi": Psi, "u": u, "rho": rho},
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
    print(json.dumps(encode({"action": derive_action(), "static": static_branch()}),
                     indent=2))
