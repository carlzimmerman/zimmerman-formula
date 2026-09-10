#!/usr/bin/env python3
"""Exact current/stress checks for +gamma X Box(chi); no global-health claim.

Run from any directory: python3 -B <this-file>
Prints JSON to stdout; writes no files. Signature -+++; K=+div(n).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sympy as s


def derive():
    t, x = s.symbols("t x", real=True)
    gamma = s.symbols("gamma", real=True)
    a, lapse, chi, tau = [s.Function(v)(t) for v in ("a", "N", "chi", "tau")]
    Q = s.diff(chi, t) / lapse
    H = s.diff(a, t) / (lapse * a)
    Qdot = s.diff(Q, t) / lapse
    X = Q**2
    box = -s.diff(a**3 * Q, t) / (lapse * a**3)
    raw = gamma * lapse * a**3 * X * box
    boundary = -gamma * a**3 * Q**3 / 3
    reduced = -2 * gamma * a**2 * s.diff(a, t) * Q**3
    checks = {"raw_cubic_minus_boundary_equals_reduced": s.simplify(raw - s.diff(boundary, t) - reduced) == 0}

    def euler(L, field):
        return s.diff(L, field) - s.diff(s.diff(L, s.diff(field, t)), t)

    rho3 = s.simplify(-euler(reduced, lapse) / a**3)
    p3 = s.simplify(euler(reduced, a) / (3 * lapse * a**2))
    j3 = s.simplify(s.diff(reduced, s.diff(chi, t)) / a**3)
    checks.update({
        "lapse_variation_rho3": s.simplify(rho3 + 6 * gamma * H * Q**3) == 0,
        "scale_variation_p3": s.simplify(p3 - 2 * gamma * Q**2 * Qdot) == 0,
        "velocity_variation_current3": s.simplify(j3 + 6 * gamma * H * Q**2) == 0,
        "cubic_energy_current_identity": s.simplify(s.diff(rho3, t) / lapse + 3 * H * (rho3 + p3) - Q * (s.diff(j3, t) / lapse + 3 * H * j3)) == 0,
    })

    # Arbitrary P(X,tau), W(0,tau), V(tau), with increasing homogeneous tau.
    P = s.Function("P")
    W0, V = s.Function("W0"), s.Function("V")
    L = lapse * a**3 * (P(X, tau) - V(tau)) + a**3 * s.diff(tau, t) * W0(tau) + reduced
    rho = s.simplify(-euler(L, lapse) / a**3)
    pressure = s.simplify(euler(L, a) / (3 * lapse * a**2))
    current = s.simplify(s.diff(L, s.diff(chi, t)) / a**3)
    E_tau = s.simplify(euler(L, tau) / (lapse * a**3))
    Xvar, tvar = s.symbols("Xvar tvar")
    PX = s.diff(P(Xvar, tvar), Xvar).subs({Xvar: X, tvar: tau})
    Pt = s.diff(P(Xvar, tvar), tvar).subs({Xvar: X, tvar: tau})
    Vt = s.diff(V(tau), tau)
    stau = s.diff(tau, t) / lapse
    checks.update({
        "total_rho": s.simplify(rho - (2 * X * PX - P(X, tau) + V(tau) - 6 * gamma * H * Q**3)) == 0,
        "total_pressure": s.simplify(pressure - (P(X, tau) - V(tau) + stau * W0(tau) + 2 * gamma * Q**2 * Qdot)) == 0,
        "total_current": s.simplify(current - (2 * Q * PX - 6 * gamma * H * Q**2)) == 0,
        "homogeneous_clock_euler": s.simplify(E_tau - (Pt - Vt - 3 * H * W0(tau))) == 0,
        "full_off_shell_energy_identity": s.simplify(s.diff(rho, t) / lapse + 3 * H * (rho + pressure) - Q * (s.diff(current, t) / lapse + 3 * H * current) + stau * E_tau) == 0,
    })

    # Independent 1+1 flat-coordinate specialization of the covariant tensor.
    # This checks the formula, not arbitrary curved 3+1 backgrounds.
    f = s.Function("f")(t, x)
    coords = [t, x]
    metric = s.diag(-1, 1)
    u = s.Matrix([s.diff(f, z) for z in coords])
    up = metric * u
    Xflat = -(u.T * metric * u)[0]
    Bflat = sum(metric[i, i] * s.diff(f, coords[i], 2) for i in range(2))
    dX = s.Matrix([s.diff(Xflat, z) for z in coords])
    J = -2 * gamma * Bflat * up - gamma * metric * dX
    E = -sum(s.diff(J[i], coords[i]) for i in range(2))
    T = s.Matrix(2, 2, lambda i, j: 2 * gamma * Bflat * u[i] * u[j] + gamma * (u[i] * dX[j] + u[j] * dX[i]) - gamma * metric[i, j] * (up.T * dX)[0])
    Hessnorm = sum(metric[i, i] * metric[j, j] * s.diff(f, coords[i], coords[j])**2 for i in range(2) for j in range(2))
    checks["flat_current_second_derivative_form"] = s.simplify(E - 2 * gamma * (Bflat**2 - Hessnorm)) == 0
    for nu in range(2):
        divergence = sum(metric[mu, mu] * s.diff(T[mu, nu], coords[mu]) for mu in range(2))
        checks[f"flat_stress_ward_component_{nu}"] = s.simplify(divergence - E * u[nu]) == 0

    return {"checks": checks, "passed": all(checks.values()), "formulas": {
        "J_definition": "delta S / delta chi = -sqrt(-g) divergence(J)",
        "J_chi": "-2 P_X grad^mu chi + 2 sqrt(Xtau) W_Y h^{mu nu} grad_nu chi - 2 gamma Box(chi) grad^mu chi - gamma grad^mu X",
        "T3_munu": "2 gamma Box(chi) chi_mu chi_nu + gamma (chi_mu d_nu X + chi_nu d_mu X) - gamma g_munu grad(chi).grad(X)",
        "rho3": "-6 gamma H Q^3", "p3": "2 gamma Q^2 Qdot", "J3": "-6 gamma H Q^2",
        "off_shell_balance": "rhodot+3H(rho+p) = Q*(Jdot+3H*J) - sqrt(Xtau)*E_tau",
        "E_tau_FLRW": "P_tau - V_tau - 3H*W(0,tau)",
    }, "scope": "Exact symbolic homogeneous variations with arbitrary lapse and functions; 1+1 flat-coordinate current/stress Ward checks. Covariant derivation is in REPORT.md. No nonlinear Dirac/stability/phenomenology certificate."}


if __name__ == "__main__":
    result = derive()
    source = Path(__file__).resolve()
    root = next(p for p in source.parents if (p / ".git").exists())
    result["provenance"] = {
        "base": "86dbf3b3c667fbe0674ff56fa2c54177a070aaaf",
        "current_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "python": platform.python_version(), "sympy": s.__version__,
        "arithmetic": "exact symbolic", "randomness": "none",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
