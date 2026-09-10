#!/usr/bin/env python3
"""Literal lapse variation of the rotated-MMG constraint candidate.

The proposed first-order action writes ``-N C_perp`` while simultaneously
defining ``u = log(N) - log(h)/6`` and putting ``D_i[mu(|Du|) D^i u]`` in
``C_perp``.  Consequently N is not a pure Lagrange multiplier.  This gate
derives the extra Euler term and evaluates it on a local affine vacuum
branch.  It is a conditional action-consistency check, not a universal
no-go theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def derive() -> dict:
    x, k, beta = sp.symbols("x k beta", positive=True)
    eps = sp.Function("eps")(x)
    u = sp.Function("u")(x)
    lam = sp.symbols("Y", positive=True)

    # Work on the positive-gradient branch Y=beta*u' with flat, fixed h.
    # beta=c^2/(2*a0)>0.  This is enough for an action-level counterexample.
    Y = beta * sp.diff(u, x)
    mu = 1 - sp.exp(-Y)
    mu_Y = sp.diff(1 - sp.exp(-lam), lam).subs(lam, Y)
    constitutive_tangent = sp.simplify(mu + Y * mu_Y)
    advertised_Q = sp.diff(mu * sp.diff(u, x), x)

    # Direct first variation under u -> u + eps*epsilon, N=exp(u).
    # The derivative of mu*u' is A*epsilon' with A=mu+Y*mu_Y.
    u_var = u + eps * sp.Symbol("delta")
    # Use a named variation parameter so SymPy differentiates through all
    # spatial derivatives, then set it to zero.
    d = sp.symbols("d")
    u_var = u + d * eps
    Y_var = beta * sp.diff(u_var, x)
    Q_var = sp.diff((1 - sp.exp(-Y_var)) * sp.diff(u_var, x), x)
    delta_Q = sp.simplify(sp.diff(Q_var, d).subs(d, 0))
    expected_delta_Q = sp.diff(constitutive_tangent * sp.diff(eps, x), x)

    N = sp.exp(u)
    # The literal action piece is -N*Q.  Integrating the variation by parts
    # gives delta I = -int N*E_literal*epsilon + boundary.
    delta_lagrangian = sp.simplify(-N * eps * advertised_Q - N * delta_Q)
    literal_residual = sp.simplify(
        advertised_Q
        + sp.exp(-u) * sp.diff(N * sp.diff(u, x) * constitutive_tangent, x)
    )
    boundary_term = -N * constitutive_tangent * sp.diff(eps, x) + N * sp.diff(u, x) * constitutive_tangent * eps
    variation_identity = sp.simplify(
        delta_lagrangian + N * literal_residual * eps - sp.diff(boundary_term, x)
    )

    # A local affine positive-gradient vacuum witness.  The advertised Q
    # vanishes, while the literal lapse Euler term is positive and nonzero.
    Y_aff = beta * k
    mu_aff = sp.simplify(1 - sp.exp(-Y_aff))
    tangent_aff = sp.simplify(mu_aff + Y_aff * sp.exp(-Y_aff))
    Q_affine = sp.simplify(sp.diff(mu_aff * k, x))
    extra_affine = sp.simplify(
        sp.exp(-k * x) * sp.diff(sp.exp(k * x) * k * tangent_aff, x)
    )
    positive_factor = sp.simplify(extra_affine / (k**2 * sp.exp(-Y_aff)))
    positive_factor_target = sp.simplify(sp.exp(Y_aff) + Y_aff - 1)
    # Take the limit in the independent dimensionless field variable rather
    # than asking SymPy to use the composite expression beta*k as a limit
    # symbol.
    high_field_extra = sp.simplify(
        sp.limit((1 + (lam - 1) * sp.exp(-lam)), lam, sp.oo)
    )

    # A compact smooth-branch control avoids relying only on affine boundary
    # data: the action mismatch is already visible in the pointwise formula.
    checks = {
        "exact_exponential_mu": sp.simplify(mu - (1 - sp.exp(-Y))) == 0,
        "constitutive_linearization_derived": sp.simplify(delta_Q - expected_delta_Q) == 0,
        "literal_variation_identity_with_boundary": variation_identity == 0,
        "advertised_affine_constraint_vacuum": Q_affine == 0,
        "affine_extra_term_is_symbolically_nonzero": extra_affine != 0,
        "affine_extra_factorization_exact": sp.simplify(
            positive_factor - positive_factor_target
        ) == 0,
        "newtonian_limit_extra_term_nonzero": high_field_extra == 1,
    }

    # The last positivity step is analytic rather than an oracle: for Y>0,
    # e^Y+Y-1 = (e^Y-1)+Y > 0.  The script records this certificate and does
    # not replace it by a hard-coded sign/rank.
    result = {
        "candidate": "rotated_mmg_literal_lapse_variation",
        "checks": {name: bool(value) for name, value in checks.items()},
        "symbols": {"Y": "beta*u'", "beta": "c^2/(2*a0)>0"},
        "advertised_constraint": str(advertised_Q),
        "constitutive_tangent": str(constitutive_tangent),
        "derived_delta_Q": str(delta_Q),
        "literal_lapse_euler_residual": str(literal_residual),
        "variation_identity": str(variation_identity),
        "affine": {
            "u": "k*x",
            "N": "exp(k*x)",
            "Y": str(Y_aff),
            "advertised_Q": str(Q_affine),
            "extra_term": str(extra_affine),
            "extra_over_k2_exp_minus_Y": str(positive_factor),
            "positive_factor": str(positive_factor_target),
            "analytic_positivity_certificate": "exp(Y)+Y-1=(exp(Y)-1)+Y>0 for Y>0",
            "high_field_extra_over_k2": str(high_field_extra),
        },
        "derived_equation": (
            "Q + N^{-1} D_j[N (D_i u) A^{ij}] + matter = 0, "
            "A^{ij}=mu h^{ij}+(mu_Y/Y)D^i u D^j u"
        ),
        "scope": (
            "Flat fixed-h positive-gradient branch of the literal rotated-MMG "
            "first-order action. If u is instead declared independent of N, "
            "the defining relation u=log(N)-log(h)/6 is absent and must be "
            "added as a new constraint; its Dirac algebra is not analyzed here."
        ),
        "status": "OBSTRUCTION_TO_ADVERTISED_LAPSE_MULTIPLIER",
    }
    return result


def write_outputs(result: dict, output: Path) -> None:
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "rmmg_lapse_variation_results.json")
    parser.add_argument(
        "--require-advertised-lapse-constraint",
        action="store_true",
        help="Return 2 because the literal action does not yield the advertised constraint.",
    )
    args = parser.parse_args()
    result = derive()
    write_outputs(result, args.output)
    for index, (name, passed) in enumerate(result["checks"].items(), 1):
        print(f"[{index}] {'ok' if passed else 'FAIL'} {name}")
    print("Advertised Q:", result["advertised_constraint"])
    print("Literal lapse residual:", result["literal_lapse_euler_residual"])
    print("Affine extra term:", result["affine"]["extra_term"])
    print("Scope:", result["scope"])
    if not all(result["checks"].values()):
        return 1
    if args.require_advertised_lapse_constraint:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
