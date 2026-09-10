#!/usr/bin/env python3
"""Audit the four-form promotion of the MOND scale used by the framework.

This is an explicit parameterization of the otherwise constant a0 in the
envelope Hamiltonian. A four-form flux q has no local wave operator; varying
its three-form potential gives a conserved conjugate quantity. The algebraic
sector is P(q)=Z*q**2/2, epsilon=q*P_q-P(q)+b*beta**2*q**2, and
a0=beta*c*sqrt(G)*|q|. Hence
 a0^2=kappa^2*G*epsilon, kappa^2=2*beta^2/(Z+2*b*beta^2).

The coefficient kappa=1/2 is not derived: the gate solves the parameter
condition required for that value and reports it as an input calibration.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def derive():
    q, Z, b, beta, G, c = sp.symbols("q Z b beta G c", positive=True)
    P = Z * q**2 / 2
    legendre_energy = sp.simplify(q * sp.diff(P, q) - P)
    epsilon = sp.simplify(legendre_energy + b * beta**2 * q**2)
    a0_sq = sp.simplify(beta**2 * c**2 * G * q**2)
    denominator = sp.simplify(Z + 2 * b * beta**2)
    kappa_sq = sp.simplify(2 * beta**2 / denominator)
    relation_residual = sp.simplify(a0_sq - kappa_sq * c**2 * G * epsilon)

    z_over_beta_sq_for_half = sp.solve(sp.Eq(kappa_sq, sp.Rational(1, 4)), Z)[0] / beta**2
    calibration_residual = sp.simplify(z_over_beta_sq_for_half - (8 - 2 * b))
    numerical_kappa = float(sp.sqrt(kappa_sq.subs({Z: 7.96, b: 0.02, beta: 1.0})))

    # A top-form potential gives dJ=0. Derive the Euler operator for the
    # one-dimensional representative L=P(dot A), rather than asserting it.
    t = sp.symbols("t")
    A = sp.Function("A")(t)
    qA = sp.diff(A, t)
    Pfun = sp.Function("P")
    topform_lagrangian = Pfun(qA)
    topform_euler = sp.simplify(
        sp.diff(topform_lagrangian, A)
        - sp.diff(sp.diff(topform_lagrangian, sp.diff(A, t)), t)
    )
    topform_target = sp.simplify(
        -sp.diff(sp.diff(Pfun(sp.symbols("q")), sp.symbols("q")).subs(sp.symbols("q"), qA), t)
    )
    topform_residual = sp.simplify(topform_euler - topform_target)

    checks = {
        "positive_legendre_energy": sp.simplify(legendre_energy.subs({Z: 1, q: 1}) > 0),
        "a0_energy_relation_derived": relation_residual == 0,
        "half_kappa_condition_solved": calibration_residual == 0,
        "half_kappa_numeric_witness": abs(numerical_kappa - 0.5) < 5e-3,
        "fourform_euler_equation_derived": topform_residual == 0,
    }
    result = {
        "candidate": "rmmg_envelope_fourform_a0_promotion",
        "definitions": {
            "P(q)": str(P),
            "legendre_energy_qPq_minus_P": str(legendre_energy),
            "epsilon(q)": str(epsilon),
            "a0_squared": str(a0_sq),
            "kappa_squared": str(kappa_sq),
            "rho_DE_relation": "epsilon=rho_DE*c^2",
        },
        "derived": {
            "a0_squared_minus_kappa_squared_G_epsilon": str(relation_residual),
            "Z_over_beta_squared_for_kappa_half": str(z_over_beta_sq_for_half),
            "kappa_half_condition": "Z/beta^2 = 8 - 2*b",
            "numeric_witness_b_002_Z_796": numerical_kappa,
            "fourform_euler_form": "dJ=0 for J=P_q + (MOND-sector q derivative)",
            "topform_euler_operator": str(topform_euler),
            "topform_conservation_residual": str(topform_residual),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
        "status": "A0_PROMOTION_ALIGNED_BUT_KAPPA_FITTED",
        "scope": "Algebraic four-form normalization only; coupled flux selection, metric/clock Dirac closure, PPN, FLRW and stability remain open.",
        "non_claims": [
            "kappa=1/2 is derived",
            "rho_DE is dynamically selected",
            "the four-form has been fully canonically reduced in the coupled theory",
        ],
    }
    out = Path(__file__).parent / "run_001"
    out.mkdir(exist_ok=True)
    (out / "fourform_a0_promotion_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert all(checks.values())
    return result


if __name__ == "__main__":
    derive()
