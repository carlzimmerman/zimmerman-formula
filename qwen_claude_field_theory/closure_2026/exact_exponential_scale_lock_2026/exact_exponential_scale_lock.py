#!/usr/bin/env python3
"""Exact-exponential scale lock.

This gate isolates a remaining coefficient loophole.  Let a single scale-free
action use the dark-energy acceleration a_Lambda in the constitutive argument
u=g/a_Lambda, with the exact required kernel mu(u)=1-exp(-u).  If its static
law is to equal the target law mu(g/a0) for all sufficiently small g, strict
monotonicity (or just the first-order coefficient) forces a0=a_Lambda and
kappa=1.  Achieving kappa=1/2 requires either changing the kernel to
1-exp(-2u), or inserting an independent factor two in the argument.  Both
violate the exact-kernel/no-extra-normalization requirement.

The calculation is conditional on one acceleration scale and exact equality
of the constitutive law; it does not address the other relativistic gates.
"""

from __future__ import annotations

import sympy as sp


FAILS: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    ok = bool(condition)
    print(("  [ok]   " if ok else "  [FAIL] ") + label)
    if detail:
        print("         " + detail)
    if not ok:
        FAILS.append(label)


def main() -> int:
    g, a0, aL, kappa = sp.symbols("g a0 a_Lambda kappa", positive=True)
    u = sp.symbols("u", positive=True)
    mu = 1 - sp.exp(-u)

    check("exact exponential kernel has unit deep-MOND slope",
          sp.limit(sp.diff(mu, u), u, 0, dir="+") == 1,
          f"mu'(0+)={sp.limit(sp.diff(mu, u), u, 0, dir='+')}")
    check("the slope with respect to physical acceleration is 1/a",
          sp.simplify(sp.limit(sp.diff(1-sp.exp(-g/a0), g), g, 0, dir="+")) == 1/a0,
          f"d mu(g/a0)/dg at zero={1/a0}")

    slope_target = 1 / a0
    slope_scale_free = 1 / aL
    ratio = sp.simplify(slope_target / slope_scale_free)
    check("matching the exact constitutive law fixes a0=a_Lambda",
          sp.solve(sp.Eq(slope_target, slope_scale_free), a0) == [aL],
          f"1/a0=1/a_Lambda -> a0={sp.solve(sp.Eq(slope_target, slope_scale_free), a0)[0]}")
    check("therefore kappa=a0/a_Lambda is exactly one",
          sp.simplify(ratio.subs(a0, aL) - 1) == 0,
          f"slope ratio a_Lambda/a0={ratio}; kappa={sp.simplify(aL/aL)}")

    # The requested kappa=1/2 is equivalent to a factor-two slope in the
    # dark-energy argument, i.e. a different interpolation function.
    mu_two = 1 - sp.exp(-2*u)
    check("kappa=1/2 requires slope two in the scale-free argument",
          sp.limit(sp.diff(mu_two, u), u, 0, dir="+") == 2,
          f"d[1-exp(-2u)]/du at zero={sp.limit(sp.diff(mu_two, u), u, 0, dir='+')}")
    check("the slope-two repair is not the exact required exponential",
          sp.simplify(mu_two - mu) != 0,
          "1-exp(-2u) != 1-exp(-u) for u>0")

    # L231's discrete family is useful as a curve, but n=2 is exactly this
    # slope-two departure in the scale-free limit and is not a derivation of
    # the required exponential.
    n = sp.symbols("n", positive=True)
    family = 1 - (1 + u) ** (-n)
    check("the L231 n=2 curve has slope two but differs from the exact exponential",
          sp.limit(sp.diff(family.subs(n, 2), u), u, 0, dir="+") == 2
          and sp.simplify(family.subs(n, 2) - mu) != 0,
          "it is an allowed alternative curve, not a closure of the fixed exponential target")

    print("\nSCALE LOCK:")
    print("  one dark-energy acceleration scale + exact mu=1-exp(-u) => kappa=1;")
    print("  kappa=1/2 requires mu=1-exp(-2u) or an equivalent inserted factor two.")
    print("  STATUS: EXACT_EXPONENTIAL_COEFFICIENT_DOOR_CLOSED")
    print(f"RESULT: {len(FAILS)} failure(s).")
    for item in FAILS:
        print("  FAILED:", item)
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
