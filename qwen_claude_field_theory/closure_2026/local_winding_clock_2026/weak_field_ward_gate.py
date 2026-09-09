"""Weak-field and matter-Ward calculations for the same winding-clock action."""

from functools import lru_cache

import sympy as sp

from action_variation import clock_potential


@lru_cache(None)
def weak_field_report():
    """Vary the two static metric potentials before selecting the baryon branch."""
    x = sp.symbols("x", real=True)
    m, a0 = sp.symbols("m a0", positive=True)
    rho_b, rho_c_phi, rho_c_psi = sp.symbols(
        "rho_b rho_c_phi rho_c_psi", real=True
    )
    Phi = sp.Function("Phi_w")(x)
    Psi = sp.Function("Psi_w")(x)
    u = sp.Function("u_w")(x)
    phi_x, psi_x = sp.diff(Phi, x), sp.diff(Psi, x)
    density = m * (
        (1 - u ** 2) * phi_x ** 2
        + psi_x ** 2
        - 2 * phi_x * psi_x
        - a0 ** 2 * clock_potential(u ** 2)
    ) - rho_b * Phi - rho_c_phi * Phi - rho_c_psi * Psi

    phi_equation = sp.expand(
        sp.diff(density, Phi) - sp.diff(sp.diff(density, phi_x), x)
    )
    psi_equation = sp.expand(
        sp.diff(density, Psi) - sp.diff(sp.diff(density, psi_x), x)
    )

    y = phi_x / a0
    mu = 1 - sp.exp(-y)
    slip = {sp.diff(Psi, x): phi_x}
    branch = {
        u: sp.sqrt(mu),
        sp.diff(u, x): sp.diff(sp.sqrt(mu), x),
    }
    phi_slip = sp.simplify(phi_equation.subs(slip))
    phi_branch = sp.simplify(phi_slip.subs(branch, simultaneous=True))
    baryon_only = {rho_c_phi: 0, rho_c_psi: 0}
    mond_equation = 2 * m * sp.diff(mu * phi_x, x) - rho_b
    mond_residual = sp.simplify(
        phi_branch.subs(baryon_only) - mond_equation
    )
    cold_source_term = sp.simplify(phi_equation - phi_equation.subs(rho_c_phi, 0))

    return {
        "coordinate": x,
        "m": m,
        "a0": a0,
        "rho_b": rho_b,
        "rho_c_phi": rho_c_phi,
        "rho_c_psi": rho_c_psi,
        "phi_equation": phi_equation,
        "psi_equation": psi_equation,
        "phi_equation_slip": phi_slip,
        "phi_equation_exponential_branch": phi_branch,
        "mond_equation": mond_equation,
        "mond_residual": mond_residual,
        "cold_source_term": cold_source_term,
        "constitutive_law": mu,
        "measured_G": sp.simplify(1 / (8 * sp.pi * m)),
    }


def _on_shell_second_derivative(equation, field, coordinate):
    second = sp.diff(field, coordinate, 2)
    solutions = sp.solve(sp.Eq(equation, 0), second, dict=True)
    if not solutions:
        raise ValueError("matter equation did not determine its second derivative")
    return solutions[0][second]


@lru_cache(None)
def ward_report():
    """Derive the baryon Ward identity and the cold/Q exchange identity.

    A one-dimensional time-dependent scalar representative is enough to check
    the variational identity.  The baryon scalar has no Q prefactor, whereas
    the cold scalar is weighted by exp(-beta Q), exposing the exchange term.
    """
    t = sp.symbols("t", real=True)
    beta, mc = sp.symbols("beta m_c", real=True)
    psi = sp.Function("psi_b")(t)
    Q = sp.Function("Q_w")(t)
    chi = sp.Function("chi_c_w")(t)
    V = sp.Function("V_b")
    psidot, Qdot, chidot = sp.diff(psi, t), sp.diff(Q, t), sp.diff(chi, t)

    L_b = psidot ** 2 / 2 - V(psi)
    E_b = sp.diff(sp.diff(L_b, psidot), t) - sp.diff(L_b, psi)
    T_b = sp.simplify(psidot * sp.diff(L_b, psidot) - L_b)
    baryon_ward = sp.simplify(sp.diff(T_b, t) - E_b * psidot)
    psi_ddot_on_shell = _on_shell_second_derivative(E_b, psi, t)
    baryon_on_shell = sp.simplify(
        sp.diff(T_b, t).subs(sp.diff(psi, t, 2), psi_ddot_on_shell)
    )

    f = sp.exp(-beta * Q)
    L0_c = chidot ** 2 / 2 - mc ** 2 * chi ** 2 / 2
    L_c = f * L0_c
    E_Q_c = sp.simplify(-sp.diff(L_c, Q))
    E_chi = sp.diff(sp.diff(L_c, chidot), t) - sp.diff(L_c, chi)
    T_c = sp.simplify(chidot * sp.diff(L_c, chidot) - L_c)
    cold_ward = sp.simplify(sp.diff(T_c, t) - E_Q_c * Qdot - E_chi * chidot)
    chi_ddot_on_shell = _on_shell_second_derivative(E_chi, chi, t)
    cold_exchange = sp.simplify(
        sp.diff(T_c, t).subs(sp.diff(chi, t, 2), chi_ddot_on_shell)
    )

    return {
        "baryon_eom": E_b,
        "baryon_stress_representative": T_b,
        "baryon_ward_residual": baryon_ward,
        "baryon_divergence_on_shell": baryon_on_shell,
        "cold_eom": E_chi,
        "q_equation_source_term": E_Q_c,
        "cold_ward_residual": cold_ward,
        "cold_exchange_residual": cold_exchange,
        "beta": beta,
        "mc": mc,
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

    print(json.dumps(encode({
        "weak_field": weak_field_report(),
        "ward": ward_report(),
    }), indent=2))
