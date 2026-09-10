#!/usr/bin/env python3
"""Restricted clock kinematics on a frozen accelerated static metric.

2026-09-10: physical health/dispersion claims withdrawn. This script omits
lapse/shift fluctuations, the complete acceleration action, and its constraints.
The metric N=exp(k*x),g_xx=1 is curved, not flat Rindler spacetime.

The covariant CAM action is supplemented by a pure cuscuton clock term
  S_tau = ∫sqrt(-g)[C_tau sqrt(X_tau)-V(tau)].
On this static patch this term supplies a spatial stiffness but no
clock kinetic term.  The acceleration-locked MOND sector supplies the
clock's mixed spatial-time kinetic term after the leaf constraint is solved.
This gate derives that statement from the normal and Christoffel definitions.
It is a local principal check, not the full nonlinear tau Dirac algebra.
"""

import json
import sympy as sp


def derive_clock_symbol():
    eps, t, x = sp.symbols("eps t x", real=True)
    k, a0, M2, Ctau = sp.symbols("k a0 M2 Ctau", positive=True)
    pi = sp.Function("pi")(t, x)
    N0 = sp.exp(k * x)
    g = sp.diag(-N0**2, 1)
    gi = g.inv()
    tau_t = 1 + eps * sp.diff(pi, t)
    tau_x = eps * sp.diff(pi, x)
    X = sp.simplify(-gi[0, 0] * tau_t**2 - gi[1, 1] * tau_x**2)
    sqrtX = sp.series(sp.sqrt(X), eps, 0, 3).removeO()
    n_cov = sp.Matrix([-tau_t / sqrtX, -tau_x / sqrtX])
    n_con = sp.simplify(gi * n_cov)

    Gamma = [[[sp.Integer(0) for _ in range(2)] for _ in range(2)]
              for _ in range(2)]
    coords = (t, x)
    for lam in range(2):
        for mu in range(2):
            for nu in range(2):
                Gamma[lam][mu][nu] = sp.simplify(sum(
                    gi[lam, sig] * (
                        sp.diff(g[sig, nu], coords[mu])
                        + sp.diff(g[sig, mu], coords[nu])
                        - sp.diff(g[mu, nu], coords[sig])
                    ) / 2 for sig in range(2)
                ))

    a_x = sum(
        n_con[nu] * (
            sp.diff(n_cov[1], coords[nu])
            - sum(Gamma[lam][nu][1] * n_cov[lam] for lam in range(2))
        ) for nu in range(2)
    )
    a_x_series = sp.series(sp.expand(a_x), eps, 0, 2).removeO()
    delta_a = sp.simplify(sp.diff(a_x_series, eps).subs(eps, 0))

    cuscuton_density = sp.series(N0 * sqrtX, eps, 0, 3).removeO()
    cuscuton_quad = sp.simplify(sp.expand(cuscuton_density).coeff(eps, 2))

    y = sp.symbols("y", positive=True)
    Q = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    Qpp = sp.simplify(sp.diff(Q, y, 2))
    return {
        "X_series": X,
        "normal_covariant": n_cov,
        "normal_contravariant": n_con,
        "acceleration_series": a_x_series,
        "delta_acceleration": delta_a,
        "cuscuton_density_series": cuscuton_density,
        "cuscuton_quadratic": cuscuton_quad,
        "Q_second_derivative": Qpp,
        "symbols": {"eps": eps, "pi": pi, "k": k, "a0": a0,
                    "M2": M2, "Ctau": Ctau, "y": y, "N0": N0},
    }


def main():
    data = derive_clock_symbol()
    failures = []

    def check(name, ok, detail=""):
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" +
              (f" ({detail})" if detail else ""))
        if not ok:
            failures.append(name)

    sy = data["symbols"]
    pi = sy["pi"]
    x = sp.symbols("x", real=True)
    expected_delta_a = -sp.diff(pi, sp.symbols("t", real=True), x)
    # Symbols with the same assumptions are equal; obtain the actual
    # coordinates from the derivative expression for a robust comparison.
    t = next(v for v in data["delta_acceleration"].free_symbols
             if str(v) == "t")
    x = next(v for v in data["delta_acceleration"].free_symbols
             if str(v) == "x")
    expected_delta_a = -sp.diff(pi, t, x)
    check("clock normalization is expanded from X_tau",
          str(data["X_series"]).find("eps") >= 0)
    check("frozen static metric acceleration perturbation is derived",
          sp.simplify(data["delta_acceleration"] - expected_delta_a) == 0,
          f"delta a_x={data['delta_acceleration']}")
    check("pure cuscuton has no pi-dot-squared term",
          not data["cuscuton_quadratic"].has(sp.diff(pi, t)),
          f"L_tau^(2)={data['cuscuton_quadratic']}")
    check("cuscuton supplies a negative spatial-gradient term",
          sp.simplify(data["cuscuton_quadratic"] /
                      (sp.exp(2 * sy["k"] * x) * sp.diff(pi, x)**2)
                      + sp.Rational(1, 2)) == 0)

    y0 = sp.symbols("y0", positive=True)
    qpp0 = sp.simplify(data["Q_second_derivative"].subs(sy["y"], y0))
    qpp_expected = 2 * (1 + (y0 - 1) * sp.exp(-y0))
    check("exponential constitutive stiffness is derived",
          sp.simplify(qpp0 - qpp_expected) == 0,
          f"Q''={qpp0}")
    # e^y+y-1 > 0 for y>0, so Q''=2e^-y(e^y+y-1)>0.
    check("exponential stiffness is positive at the four tested values",
          all(float(qpp0.subs(y0, value)) > 0
              for value in (sp.Rational(1, 100), 1, 2, 10)))

    payload = {
        "status": "FROZEN_METRIC_KINEMATICS_ONLY_HEALTH_CLAIMS_WITHDRAWN",
        "checks": {"count": 6, "passed": 6 - len(failures)},
        "derived": {k: str(v) for k, v in data.items()
                    if k != "symbols"},
        "scope": "Frozen metric kinematics; no physical dispersion or mode count computed.",
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
