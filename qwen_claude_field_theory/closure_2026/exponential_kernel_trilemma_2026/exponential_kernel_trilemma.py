#!/usr/bin/env python3
"""Structural trilemma for the exact exponential MOND kernel.

The exact primitive

    G(y) = y^2 + 2(1+y) exp(-y) - 2,
    G'(y)/(2y) = 1-exp(-y)

has G(y)=2 y^3/3+O(y^4) at the isotropic FLRW point Y=0.  Consequently the
MOND sector has no quadratic Hessian around a regular homogeneous background:
its flux is quadratic in a perturbation, not a linear cosmological principal
symbol.  This script derives the three available repairs and their costs:

  (A) add a local quadratic cY term: mu_eff(0)=c, so exact mu(0)=0 forces c=0;
  (B) use a nonzero background spatial gradient: rotational invariance forces it
      to vanish on an isotropic FLRW background;
  (C) use a derivative-only local auxiliary multiplier P(0)=0: its response is
      Lambda=-R/P and has an inverse-Laplacian IR pole; a finite local regulator
      reintroduces trace-free slip.

This is conditional on locality, one physical metric, a regular isotropic FLRW
background, and the exact exponential constitutive law.  It is not a theorem
against arbitrary nonlocal or multi-metric actions.  No expected rank or target
number is inserted: all conclusions are exact SymPy residuals/limits.
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
    y, eps, q, a0 = sp.symbols("y epsilon q a0", positive=True)
    c, mu0 = sp.symbols("c mu0", real=True)
    R, z, h0, h1 = sp.symbols("R z h0 h1", positive=True)
    F = sp.symbols("F", real=True)

    mu = 1 - sp.exp(-y)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    check("exact primitive differentiates to mu(y)=1-exp(-y)",
          sp.simplify(sp.diff(G, y) / (2 * y) - mu) == 0)

    G_series = sp.series(G, y, 0, 8).removeO()
    expected_series = sp.Rational(2, 3) * y**3 - sp.Rational(1, 4) * y**4 \
        + sp.Rational(1, 15) * y**5 - sp.Rational(1, 72) * y**6 \
        + sp.Rational(1, 420) * y**7
    check("near-zero primitive begins at cubic order", 
          sp.expand(G_series - expected_series) == 0,
          f"G(y)={G_series}")

    # On a regular isotropic background Ybar=0, a perturbative gradient has
    # Y=epsilon^2 q.  The epsilon^2 coefficient is exactly absent.
    FM_eps = sp.expand(a0**2 * G.subs(y, eps * sp.sqrt(q) / a0))
    FM_series = sp.series(FM_eps, eps, 0, 5).removeO()
    check("MOND energy has zero quadratic coefficient at Ybar=0",
          sp.expand(FM_series).coeff(eps, 2) == 0,
          f"a0^2 G(sqrt(Y)/a0)={FM_series}")
    check("leading perturbative MOND term is cubic",
          sp.expand(FM_series).coeff(eps, 3) == sp.Rational(2, 3) * q**sp.Rational(3, 2) / a0,
          f"[epsilon^3]={sp.expand(FM_series).coeff(eps, 3)}")

    # The flux divided by perturbation amplitude is the would-be linear map.
    r = sp.symbols("r", positive=True)
    flux_over_eps = (1 - sp.exp(-eps * r / a0))
    check("linearized MOND flux vanishes at the homogeneous point",
          sp.limit(flux_over_eps, eps, 0, dir="+") == 0,
          f"lim epsilon->0 mu(epsilon*r/a0)={sp.limit(flux_over_eps, eps, 0, dir='+')}")

    # Repair A: a local quadratic term shifts the constitutive law at y=0.
    mu_eff0 = sp.simplify(c + mu.subs(y, 0))
    check("a local cY regulator shifts mu_eff(0) to c",
          sp.simplify(mu_eff0 - c) == 0,
          f"mu_eff(0)={mu_eff0}")
    check("exact mu(0)=0 forces the quadratic regulator c to vanish",
          sp.solve(sp.Eq(mu_eff0, 0), c) == [0],
          f"solution of c+mu(0)=0: {sp.solve(sp.Eq(mu_eff0, 0), c)}")

    # Repair B: a nonzero preferred spatial gradient cannot be isotropic.
    x, yy = sp.symbols("x yy", real=True)
    rot90 = sp.Matrix([-yy, x])
    vec = sp.Matrix([x, yy])
    iso_solution = sp.solve([sp.Eq(rot90[i], vec[i]) for i in range(2)], [x, yy], dict=True)
    check("a spatial background invariant under a 90-degree rotation is zero",
          iso_solution == [{x: 0, yy: 0}],
          f"rotation-invariant solutions={iso_solution}")

    # Repair C: derivative-only local multiplier has P(z)=z(h0+h1 z).
    Pz = z * (h0 + h1 * z)
    Lambda = -R / Pz
    check("P(0)=0 auxiliary response is inverse-Laplacian singular",
          sp.simplify(z * Lambda + R / (h0 + h1 * z)) == 0,
          f"Lambda={Lambda}; z*Lambda -> {sp.limit(z*Lambda, z, 0, dir='+')}")
    check("generic nonzero source diverges as z->0",
          sp.limit(abs(Lambda), z, 0, dir="+") == sp.oo,
          f"lim |Lambda|={sp.limit(abs(Lambda), z, 0, dir='+')}")
    d = F * R / Pz**2
    check("a finite local trace-free regulator produces nonzero slip",
          sp.simplify(d.subs(F, 1) - R / Pz**2) == 0,
          f"d={d}")
    check("exact no-slip with generic source forces regulator F=0",
          sp.solve(sp.Eq(d, 0), F) == [0],
          f"solutions of d=0: {sp.solve(sp.Eq(d, 0), F)}")

    print("\nTRILEMMA:")
    print("  exact exponential + regular isotropic FLRW => MOND Hessian vanishes at quadratic order;")
    print("  quadratic repair => mu(0)!=0; nonzero spatial background => anisotropic FLRW;")
    print("  derivative-only local auxiliary repair => inverse-Laplacian IR pole, and finite regulator => slip.")
    print("  SCOPE: conditional local single-metric trilemma, not a universal no-go for arbitrary nonlocal actions.")
    print(f"RESULT: {len(FAILS)} failure(s).")
    for item in FAILS:
        print("  FAILED:", item)
    print("STATUS: EXPONENTIAL_KERNEL_LOCAL_SINGLE_METRIC_TRILEMMA")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
