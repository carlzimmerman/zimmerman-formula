"""Executable Dirac analysis for the homogeneous local-winding block.

The purpose of this module is deliberately modest and auditable: it computes
the canonical momenta, carries the primary constraints through their
preservation equations, and forms the actual Poisson-bracket matrix.  The
minisuperspace block is not a substitute for the full ADM field-theory
analysis; it is a falsifiable gate which makes any hidden ``lambda`` or
clock-memory mode visible before a more expensive perturbative calculation.
"""

from functools import lru_cache

import sympy as sp


def _poisson(f, g, coordinates, momenta):
    """Canonical Poisson bracket in the displayed finite-dimensional block."""
    return sp.expand(sum(
        sp.diff(f, q) * sp.diff(g, p)
        - sp.diff(f, p) * sp.diff(g, q)
        for q, p in zip(coordinates, momenta)
    ))


def _hamiltonian(coordinates, momenta, k_value):
    a, N, Q, lam, chi = coordinates
    pa, pN, pQ, pl, pchi = momenta
    m, Lam, beta, mc = sp.symbols("m Lambda beta m_c", positive=True)
    k = sp.symbols("k", nonnegative=True)
    # Legendre transform of the FRW Einstein-Hilbert block plus
    # a^3 lambda (dot Q - N Theta) and the conformally weighted cold scalar.
    # k^2 chi^2 is the Fourier-space spatial-gradient contribution.
    F = (
        -(pa + a ** 2 * lam) ** 2 / (12 * m * a)
        + m * Lam * a ** 3
        + sp.exp(beta * Q) * pchi ** 2 / (2 * a ** 3)
        + a ** 3 * mc ** 2 * chi ** 2 / 2
        + a * k ** 2 * chi ** 2 / 2
    )
    hamiltonian = N * F
    if k_value == "k_zero":
        hamiltonian = hamiltonian.subs(k, 0)
    elif k_value != "k_nonzero":
        raise ValueError("mode must be 'k_nonzero' or 'k_zero'")
    return sp.factor(hamiltonian), {"m": m, "Lambda": Lam,
                                  "beta": beta, "m_c": mc, "k": k}


def _absolute_winding_control():
    """Negative control: smooth |Theta| spends a velocity Hessian direction."""
    a, N, lam, adot, Qdot, epsw = sp.symbols(
        "a N lambda adot Qdot epsilon_w", positive=True
    )
    theta = adot / (N * a)
    smooth_abs = sp.sqrt(theta ** 2 + epsw ** 2) - epsw
    lagrangian = a ** 3 * lam * (Qdot - N * smooth_abs)
    hessian = sp.hessian(lagrangian, (adot, Qdot))
    # A concrete regular point is used only to evaluate the rank returned by
    # SymPy; no rank is inserted by hand.
    witness = {a: 1, N: 1, lam: 1, adot: 1, epsw: 1}
    rank = int(hessian.subs(witness).rank())
    return {
        "mode": "absolute_control",
        "epsilon_w": epsw,
        "velocity_hessian": hessian,
        "velocity_hessian_rank": rank,
        "regular_point": witness,
    }


@lru_cache(None)
def dirac_report(mode="k_nonzero"):
    """Return the computed constraints and their closure for one Fourier sector.

    ``k_nonzero`` retains a symbolic nonzero wave number.  ``k_zero`` sets it
    to zero only after the same Hamiltonian and constraint construction, so
    homogeneous degeneracies cannot be silently identified with local ones.
    """
    coordinates = sp.symbols("a N Q lambda chi", positive=True)
    # Order is chosen to keep the canonical pairs explicit.
    a, N, Q, lam, chi = coordinates
    momenta = sp.symbols("p_a p_N p_Q p_lambda p_chi", real=True)
    pa, pN, pQ, pl, pchi = momenta
    hamiltonian, parameters = _hamiltonian(coordinates, momenta, mode)

    primary = [pN, pl, pQ - a ** 3 * lam]
    primary_names = ["p_N", "p_lambda", "C_Q"]

    secondary = [sp.factor(_poisson(c, hamiltonian, coordinates, momenta))
                 for c in primary]
    secondary_names = ["C_N", "C_lambda", "C_Qadjoint"]

    # Preservation has the form dot C_i = {C_i,H_c} + B_ij u_j.
    bracket_secondary_primary = sp.Matrix([
        [_poisson(s, p, coordinates, momenta) for p in primary]
        for s in secondary
    ])
    drift = sp.Matrix([
        _poisson(s, hamiltonian, coordinates, momenta) for s in secondary
    ])
    # Solve with the actual bracket matrix.  If the matrix is singular this
    # raises, exposing an unresolved tertiary-constraint branch.
    multipliers = -bracket_secondary_primary.inv() * drift
    preservation = bracket_secondary_primary * multipliers + drift
    preservation = [sp.factor(sp.simplify(x)) for x in preservation]

    constraints = primary + secondary
    poisson_matrix = sp.Matrix([
        [_poisson(c_i, c_j, coordinates, momenta) for c_j in constraints]
        for c_i in constraints
    ])
    poisson_matrix = poisson_matrix.applyfunc(lambda x: sp.factor(x))
    rank = int(poisson_matrix.rank())
    total_constraints = len(constraints)
    first_class = total_constraints - rank
    second_class = rank
    phase_space_dimension = 2 * len(coordinates) - 2 * first_class - second_class

    return {
        "mode": mode,
        "coordinates": coordinates,
        "momenta": momenta,
        "hamiltonian": hamiltonian,
        "parameters": parameters,
        "primary_names": primary_names,
        "primary_constraints": primary,
        "secondary_names": secondary_names,
        "secondary_constraints": secondary,
        "preservation_matrix": bracket_secondary_primary,
        "preservation_drift": drift,
        "multiplier_solution": multipliers,
        "preservation_residuals": preservation,
        "constraints": constraints,
        "poisson_matrix": poisson_matrix,
        "rank": rank,
        "first_class": first_class,
        "second_class": second_class,
        "phase_space_dimension": phase_space_dimension,
        "absolute_winding_control": _absolute_winding_control(),
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

    print(json.dumps(encode({
        mode: dirac_report(mode) for mode in ("k_nonzero", "k_zero")
    }), indent=2))
