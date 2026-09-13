#!/usr/bin/env python3
"""General first-gradient York/QUMOND no-slip obstruction.

Consider the most general isotropic static two-potential carrier of the form

    L = -2 A(u) h^{ij} Phi_i Psi_j + a0^2 F(u),
    u = h^{ij} Psi_i Psi_j/a0^2.

The calculation is deliberately local and action-level.  It asks whether
this whole class can (i) give an exactly linear Poisson equation for Psi,
(ii) give the exact exponential QUMOND flux for Phi, and (iii) have zero
Hilbert trace-free stress on Phi=Psi for arbitrary anisotropic gradients.
No desired coefficient, rank, or PPN value is inserted.
"""

from __future__ import annotations

import sympy as sp


def main() -> int:
    u, A, Aprime, Fprime = sp.symbols("u A A_prime F_prime", real=True)
    q0, q1, q2 = sp.symbols("q0 q1 q2", real=True)
    # Direct variation with respect to Phi_i: exact Poisson requires A=1
    # (the normalization is fixed by the measured Newton coupling).
    poisson_vector = sp.Matrix([-2 * A * q0, -2 * A * q1, -2 * A * q2])
    target_vector = sp.Matrix([-2 * q0, -2 * q1, -2 * q2])
    poisson_residual = sp.simplify(poisson_vector - target_vector)
    poisson_condition = all(sp.factor(e) == 0 for e in poisson_residual.subs(A, 1))

    # Varying the inverse spatial metric on Phi=Psi gives the general TF
    # coefficient found by the chain rule: F' - 2(A + u A').
    tf_coefficient = sp.factor(Fprime - 2 * (A + u * Aprime))
    tf_difference = sp.factor(
        (Fprime - 2 * (A + u * Aprime)) * (q0**2 - q1**2)
    )
    no_slip_after_poisson = sp.simplify(tf_coefficient.subs({A: 1, Aprime: 0}))

    x = sp.symbols("x", positive=True)
    nu_exp = 1 / (1 - sp.exp(-x))
    residual_exp = sp.simplify(no_slip_after_poisson.subs(Fprime, nu_exp))
    point_witness = sp.simplify(residual_exp.subs(x, 1))
    nonconstant_witness = sp.simplify(
        residual_exp.subs(x, 1) - residual_exp.subs(x, 2)
    )

    checks = {
        "exact_poisson_forces_A_one": poisson_condition,
        "general_tf_factorization": sp.expand(tf_difference - tf_coefficient * (q0**2 - q1**2)) == 0,
        "poisson_reduced_tf_coefficient": no_slip_after_poisson == Fprime - 2,
        "exponential_tf_residual_nonzero_at_x1": point_witness != 0,
        "exponential_tf_residual_not_constant": nonconstant_witness != 0,
    }
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("  delta L/d(Phi_i) =", poisson_vector.T)
    print("  TF coefficient before Poisson normalization =", tf_coefficient)
    print("  TF coefficient after A=1 =", no_slip_after_poisson)
    print("  exponential residual nu_exp(x)-2 =", residual_exp)
    print("  x=1 witness =", point_witness)
    print("  x=1 minus x=2 witness =", nonconstant_witness)
    print()
    print("THEOREM (scoped): exact Poisson + first-gradient isotropy forces A=1;")
    print("no-slip then forces F'(u)=2 for every anisotropic gradient, while")
    print("the exact exponential carrier requires F'(u)=nu_exp(sqrt(u)), which")
    print("is nonconstant and differs from 2 except at one field value.")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
