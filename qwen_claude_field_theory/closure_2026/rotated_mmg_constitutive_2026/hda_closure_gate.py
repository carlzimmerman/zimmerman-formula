"""Hamiltonian-constraint bracket gate for the local constitutive pair.

This is an exact 1+1-dimensional principal calculation.  It does not claim
to be a no-go for theories with additional constrained fields; it identifies
the term those fields must cancel.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def derive_bracket():
    s, p, a0, A = sp.symbols("s p a0 A", positive=True)
    A_of_s = sp.Function("A")(s)
    mu = 1 - sp.exp(-s / a0)
    W_prime = mu * s
    # For H[N]=integral N[ A(s)p^2/2 + W(s) ], s=u',
    # {H[N],H[M]} has smear factor (N M'-M N') times p*A*B,
    # B=A'(s)p^2/2+W'(s).
    B = sp.diff(A_of_s, s) * p**2 / 2 + W_prime
    coefficient = sp.expand(p * A_of_s * B)
    target = p * s  # standard spatial diffeomorphism D=p*u'
    residual = sp.factor(coefficient - target)
    p3_coefficient = sp.simplify(sp.diff(residual, p, 3) / 6)
    p_linear_residual = sp.simplify(sp.diff(residual, p).subs(p, 0))
    # The only way to remove the p-linear residual pointwise is A=1/mu.
    A_match = 1 / mu
    cubic_match = sp.simplify(
        (sp.diff(A_match, s) * A_match / 2).subs(s, a0)
    )
    return {
        "mu": str(mu),
        "bracket_residual": str(residual),
        "p3_coefficient": str(p3_coefficient),
        "p_linear_residual": str(p_linear_residual),
        "A_required_by_p_linear_term": "1/(1-exp(-s/a0))",
        "cubic_coefficient_for_A_equal_1_over_mu_at_s_eq_a0": str(cubic_match),
        "cubic_witness_nonzero": bool(sp.simplify(cubic_match) != 0),
        "mu_derivative_at_a0": str(sp.diff(mu, s).subs(s, a0)),
        "interpretation": (
            "With only this canonical pair, standard spatial-diffeomorphism "
            "closure requires A'=0 and A*mu=1. Since mu' > 0, these are "
            "incompatible. Extra constrained fields could cancel the p^3 term."
        ),
    }


if __name__ == "__main__":
    result = derive_bracket()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "hda_closure_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("HDA_CONSTITUTIVE_BRACKET_GATE")
    print(f"p3_coefficient: {result['p3_coefficient']}")
    print(f"A_required: {result['A_required_by_p_linear_term']}")
    print(f"cubic_witness_nonzero: {result['cubic_witness_nonzero']}")
    print("STATUS: CONDITIONAL OBSTRUCTION (additional constrained cancellation is required)")
