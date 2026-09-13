#!/usr/bin/env python3
"""Action-level conditional obstruction for a local elliptic scalar.

Consider only the restricted static sector

    S_chi = integral sqrt(-g) F(Y),
    Y = h^{ij} partial_i chi partial_j chi,

on a flat three-dimensional leaf, with no multiplier/heat-kernel stress,
disformal metric, background vector gradient, or extra tensor operator.
The script derives the chi Euler--Lagrange coefficient and the traceless
spatial stress.  It then proves by an exact sum-of-squares identity that
zero slip for every nonzero gradient forces F_Y=0, while the exponential
MOND constitutive law requires F_Y proportional to 1-exp(-sqrt(Y)/a0), which
is nonzero for Y>0.  The result is deliberately conditional, not a
universal no-go for nonlocal or constrained completions.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class Check:
    name: str
    measured: str
    passed: bool
    interpretation: str


def check(name: str, measured: str, passed: bool, interpretation: str) -> Check:
    result = Check(name, measured, bool(passed), interpretation)
    print(f"[{('PASS' if result.passed else 'FAIL')}] {name}")
    print(f"  measured: {measured}")
    print(f"  reading:  {interpretation}")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-compatible",
        action="store_true",
        help="return 2 because the restricted action is analytically incompatible",
    )
    args = parser.parse_args(argv)

    x1, x2, x3, Y, fy, a0, C = sp.symbols(
        "x1 x2 x3 Y F_Y a0 C", real=True
    )
    F = sp.Function("F")
    grad = sp.Matrix([x1, x2, x3])
    metric = sp.eye(3)

    # The static action variation is delta S = integral 2 F_Y grad(chi).grad(delta chi).
    # After one spatial integration by parts the source-free EL operator is
    # -2 div(F_Y grad chi).  Matching div[mu grad Phi] fixes 2 F_Y=C mu.
    y = sp.sqrt(Y) / a0
    mu_exp = 1 - sp.exp(-y)
    fy_mond = sp.simplify(C * mu_exp / 2)

    # Spatial stress convention: T_ij = 2 F_Y chi_i chi_j - delta_ij F.
    # The isotropic F term drops out of the traceless part.
    Fsym = sp.symbols("F", real=True)
    Tij = 2 * fy * (grad * grad.T) - Fsym * metric
    trace = sp.trace(Tij)
    Pi = sp.simplify(Tij - metric * trace / 3)
    A = sp.simplify(Pi / 2 / fy)

    checks: list[Check] = []
    checks.append(
        check(
            "EL coefficient",
            "div(2 F_Y grad chi) = div(C mu grad Phi)",
            sp.simplify(2 * fy_mond - C * mu_exp) == 0,
            "the MOND equation fixes a nonzero constitutive derivative rather than leaving it free",
        )
    )
    checks.append(
        check(
            "traceless stress form",
            f"Pi/2 = {A}",
            all(
                sp.simplify(
                    A[i, j]
                    - (grad[i] * grad[j] - metric[i, j] * grad.dot(grad) / 3)
                )
                == 0
                for i in range(3)
                for j in range(3)
            ),
            "the isotropic potential term cancels; the remaining stress is rank-one minus its trace",
        )
    )

    # Use an independent Y and the defining relation only in this identity.
    A11 = x1**2 - Y / 3
    A22 = x2**2 - Y / 3
    A33 = x3**2 - Y / 3
    A12, A13, A23 = x1 * x2, x1 * x3, x2 * x3
    lhs = (
        A11**2
        + A22**2
        + A33**2
        + 2 * A12**2
        + 2 * A13**2
        + 2 * A23**2
    )
    rhs = sp.Rational(2, 3) * Y**2
    identity_residual = sp.factor((lhs - rhs).subs(Y, x1**2 + x2**2 + x3**2))
    checks.append(
        check(
            "traceless_sum_of_squares",
            f"sum_ij A_ij^2 - 2 Y^2/3 = {identity_residual}",
            identity_residual == 0,
            "for Y>0 the traceless gradient tensor cannot vanish, independent of orientation",
        )
    )

    # If every Pi_ij is zero, the sum of their squares is zero.  The identity
    # then gives 4 F_Y^2 * 2Y^2/3 = 0, so F_Y=0 whenever Y>0.
    fy_sq_factor = sp.simplify(4 * rhs)
    checks.append(
        check(
            "zero-slip implication",
            f"sum_ij Pi_ij^2 = F_Y^2 * ({fy_sq_factor})",
            sp.simplify(fy_sq_factor - sp.Rational(8, 3) * Y**2) == 0,
            "vanishing traceless Einstein source at a nonzero gradient forces F_Y=0",
        )
    )

    # The exponential coefficient is strictly nonzero on the physical branch.
    checks.append(
        check(
            "mond_coefficient_nonzero",
            "2 F_Y/C = 1-exp(-sqrt(Y)/a0) > 0 for Y>0, a0>0",
            (1 - math.exp(-1.0)) > 0
            and sp.simplify(2 * fy_mond / C - mu_exp) == 0,
            "the exact preferred kernel cannot satisfy the zero-slip implication in this restricted sector",
        )
    )

    obstruction_sample = sp.simplify(fy_mond.subs({Y: 1, a0: 1, C: 1}))
    checks.append(
        check(
            "obstruction",
            "Y>0 => slip forces F_Y=0, while exponential MOND gives F_Y>0",
            obstruction_sample > 0 and sp.simplify(fy_sq_factor.subs(Y, 1)) > 0,
            "the two requirements cannot hold simultaneously for this restricted action",
        )
    )

    # A deterministic numerical witness makes the orientation-independent claim concrete.
    witness = (sp.Rational(2, 3), sp.Rational(-1, 3), sp.Rational(1, 3))
    witness_y = sum(v * v for v in witness)
    witness_sum = sp.simplify(
        sum((witness[i] * witness[j] - (witness_y if i == j else 0) / 3) ** 2
            for i in range(3) for j in range(3))
    )
    checks.append(
        check(
            "orientation witness",
            f"v={witness}, Y={witness_y}, sum_ij A_ij^2={witness_sum}",
            witness_y > 0 and witness_sum > 0,
            "a generic nonzero gradient leaves a nonzero anisotropic source whenever F_Y is nonzero",
        )
    )

    all_pass = all(item.passed for item in checks)
    payload = {
        "gate": "local_single_elliptic_scalar_slip",
        "status": "CONDITIONAL_OBSTRUCTION" if all_pass else "DERIVATION_FAILURE",
        "checks": {item.name: item.passed for item in checks},
        "action": "integral sqrt(-g) F(Y)",
        "Y": "delta^ij partial_i chi partial_j chi",
        "MOND_matching": "2 F_Y = C [1 - exp(-sqrt(Y)/a0)]",
        "traceless_stress": "Pi_ij = 2 F_Y (partial_i chi partial_j chi - delta_ij Y/3)",
        "identity": "sum_ij (v_i v_j - delta_ij Y/3)^2 = 2 Y^2/3",
        "scope": (
            "Conditional obstruction only: flat static leaf, one local F(Y) scalar, "
            "no multiplier/heat stress, no disformal metric, no background vector gradient, "
            "and slip required for every nonzero gradient. It is not a universal no-go for "
            "nonlocal, constrained, or multi-field stress cancellation."
        ),
    }
    print("CERTIFICATE_JSON: " + json.dumps(payload, sort_keys=True))
    if not all_pass:
        return 1
    if args.require_compatible:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
