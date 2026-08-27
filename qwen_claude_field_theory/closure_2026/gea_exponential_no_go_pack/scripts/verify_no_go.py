#!/usr/bin/env python3
"""Symbolic verification of the conditional GEA no-go algebra."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    eps, c13 = sp.symbols("eps c13", real=True)
    c1, c3, c4, c14 = sp.symbols("c1 c3 c4 c14", real=True)
    F0 = sp.symbols("F0", nonzero=True, finite=True)

    # Effective couplings bar{c_i} = F_K(0) c_i.
    b1, b3, b4 = sp.symbols("b1 b3 b4", real=True)

    # Exact exponential deep-MOND normalization:
    # mu(0) = 0 = 1 - (bar{c4} - bar{c1})/2.
    mond_eq = sp.Eq(b4 - b1, sp.Integer(2))
    c14_eq = sp.Eq(b4 + b1, eps)
    sol = sp.solve([mond_eq, c14_eq], [b1, b4], dict=True)[0]

    assert sp.simplify(sol[b1] - (-1 + eps / 2)) == 0
    assert sp.simplify(sol[b4] - (1 + eps / 2)) == 0

    print("[PASS] MOND normalization + c14 definition")
    print("       bar_c1 =", sol[b1])
    print("       bar_c4 =", sol[b4])

    # Standard spin-1 speed formula.
    s1_sq = (2 * c1 - c13 * (2 * c1 - c13)) / (
        2 * c14 * (1 - c13)
    )

    # At c13 = 0, s1^2 = c1/c14.
    reduced = sp.simplify(s1_sq.subs(c13, 0))
    assert sp.simplify(reduced - c1 / c14) == 0
    print("[PASS] c13 -> 0 spin-1 speed reduction")
    print("       cV^2 =", reduced)

    # Common rescaling cancels in c1/c14.
    ratio_bar = sp.simplify((F0 * c1) / (F0 * c14))
    assert sp.simplify(ratio_bar - c1 / c14) == 0
    print("[PASS] F_K(0) rescaling cancels from c1/c14")

    # Substitute c1 -> bar_c1, c14 -> eps in the c13=0 ratio.
    cv_eff = sp.simplify(sol[b1] / eps)
    assert sp.simplify(cv_eff - (-1 + eps / 2) / eps) == 0
    print("[PASS] effective vector-speed expression")
    print("       cV^2 =", cv_eff)

    # Prove negativity for 0 < eps < 2 by inspecting the numerator.
    numerator = sp.factor(sp.together(cv_eff).as_numer_denom()[0])
    denominator = sp.factor(sp.together(cv_eff).as_numer_denom()[1])
    print("       numerator   =", numerator)
    print("       denominator =", denominator)

    # AQUAL primitive for mu(y) = 1-exp(-y).
    y = sp.symbols("y", nonnegative=True)
    F = y**2 / 2 + (y + 1) * sp.exp(-y) - 1
    mu = 1 - sp.exp(-y)
    check = sp.simplify(sp.diff(F, y) - y * mu)
    assert check == 0
    print("[PASS] AQUAL primitive: F'(y) = y mu(y)")

    # Explicit numeric sanity check in the small-positive-epsilon regime.
    for val in [1e-1, 1e-2, 1e-4, 1e-6]:
        cv = float(cv_eff.subs(eps, val))
        assert cv < 0.0
        print(f"[PASS] eps={val:g}: cV^2={cv:.6g} < 0")

    print("\nConditional conclusion:")
    print("  For 0 < eps < 2, cV^2 = (-1 + eps/2)/eps < 0.")
    print("  The observational regime eps << 1 lies inside this interval.")


if __name__ == "__main__":
    main()
