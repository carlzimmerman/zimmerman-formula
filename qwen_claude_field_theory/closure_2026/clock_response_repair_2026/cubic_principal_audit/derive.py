#!/usr/bin/env python3
"""Action-derived scalar high-frequency principal coefficients; no DOF theorem.

derive() returns (facts, ctx), preserving exact SymPy expressions for reuse.
No files are written; run this file to print checks and provenance as JSON.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sympy as s


def derive():
    gamma, q, H, qdot, M2 = s.symbols("gamma q H qdot M2", real=True)
    C0, S0, d, B0, A, U = s.symbols("C0 S0 d B0 A U", real=True)
    PX0, PXX0, W00 = s.symbols("PX0 PXX0 W00", real=True)
    eps, sd, sx, td, tx = s.symbols("eps sigmad sigmax taud taux", real=True)
    X = (q + eps * sd)**2 - eps**2 * sx**2
    Xtau = (1 + eps * td)**2 - eps**2 * tx**2
    Q = ((1 + eps * td) * (q + eps * sd) - eps**2 * tx * sx) / s.sqrt(Xtau)
    Y = s.series(Q**2 - X, eps, 0, 3).removeO().expand()
    DX = X - q**2
    PXgamma = PX0 + 3 * gamma * q * H
    Wgamma = W00 - 2 * gamma * q**2 * qdot
    density = PXgamma * DX + PXX0 * DX**2 / 2 + s.sqrt(Xtau) * (Wgamma + d * Y)
    matter2 = s.expand(s.series(density, eps, 0, 3).removeO().coeff(eps, 2))

    # Derive the cubic quadratic term before freezing q and a: exact FLRW
    # Box(chi)=-chi_ddot-3H chi_dot+a^-2 Delta chi on the fixed metric.
    t = s.symbols("t", real=True)
    at, qt, vt, wx = [s.Function(n)(t) for n in ("a", "q", "sigmad", "sigmax")]
    ht = s.diff(at, t) / at
    qdt = s.diff(qt, t)
    # First integrate sigmad Delta sigma spatially. wx_dot=partial_x sigmad.
    cubic_raw_after_spatial_ibp = gamma * at**3 * (
        -(qdt + 3 * ht * qt) * (vt**2 - wx**2 / at**2)
        - 2 * qt * vt * s.diff(vt, t) - 6 * ht * qt * vt**2
        - 2 * qt * s.diff(wx, t) * wx / at**2)
    cubic_boundary = -gamma * at**3 * qt * vt**2 - gamma * at * qt * wx**2
    cubic_reduced = gamma * at**3 * (-6 * ht * qt * vt**2 + 2 * (qdt + 2 * ht * qt) * wx**2 / at**2)
    checks = {"FLRW_cubic_quadratic_boundary_identity": s.simplify(cubic_raw_after_spatial_ibp - s.diff(cubic_boundary, t) - cubic_reduced) == 0}
    cubic2 = gamma * (-6 * H * q * sd**2 + 2 * (qdot + 2 * H * q) * sx**2)
    total2 = s.expand(matter2 + cubic2)
    kinetic_fixed = s.diff(total2, sd, 2)
    spatial_matrix = -s.hessian(total2, [tx, sx])
    substitutions = {PX0: C0 + d, PXX0: (B0 - 2 * (C0 + d)) / (4 * q**2), W00: S0 + 2 * q**2 * d}
    Kfixed = s.simplify(kinetic_fixed.subs(substitutions))
    spatial_matrix = s.simplify(spatial_matrix.subs(substitutions))
    tau_stiffness = S0 - 2 * gamma * q**2 * qdot
    Cgamma = C0 - gamma * (q * H + 2 * qdot)
    tau_solution = s.solve(s.diff(total2, tx), tx)[0]
    spatial_schur = s.simplify((spatial_matrix[1, 1] - spatial_matrix[1, 0]**2 / spatial_matrix[0, 0]))
    checks.update({
        "projected_gradient_from_action": s.simplify(Y - eps**2 * (sx - q * tx)**2) == 0,
        "no_fixed_metric_tau_time_kinetic": s.diff(total2, td, 2) == 0 and s.diff(total2, td, sd) == 0,
        "fixed_metric_kinetic": s.simplify(Kfixed - (B0 - 6 * gamma * q * H)) == 0,
        "tau_spatial_hessian": s.simplify(spatial_matrix[0, 0] - tau_stiffness) == 0,
        "tau_chi_spatial_hessian": s.simplify(spatial_matrix[0, 1] - 2 * q * d) == 0,
        "chi_spatial_hessian": s.simplify(spatial_matrix[1, 1] - 2 * Cgamma) == 0,
        "tau_schur_from_euler_solution": s.simplify(-s.diff(total2.subs(tx, tau_solution), sx, 2).subs(substitutions) - spatial_schur) == 0,
    })

    # Independently linearize the exact covariant cubic stress. Only its
    # second perturbation derivatives source the order-two metric principal.
    xs = s.symbols("x y z", real=True)
    coords = [t, *xs]
    sigma = s.Function("sigma")(*coords)
    eta = s.diag(-1, 1, 1, 1)
    field = q * t + eps * sigma
    u = s.Matrix([s.diff(field, v) for v in coords])
    up = eta * u
    xf = -(u.T * up)[0]
    bx = sum(eta[i, i] * s.diff(field, coords[i], 2) for i in range(4))
    dx = s.Matrix([s.diff(xf, v) for v in coords])
    stress = s.Matrix(4, 4, lambda i, j: 2 * gamma * bx * u[i] * u[j] + gamma * (u[i] * dx[j] + u[j] * dx[i]) - gamma * eta[i, j] * (up.T * dx)[0])
    Tlin = s.simplify(stress.diff(eps).subs(eps, 0))
    lap = sum(s.diff(sigma, v, 2) for v in xs)
    sdd = s.diff(sigma, t, 2)
    checks["metric_source_00"] = s.simplify(Tlin[0, 0] - 2 * gamma * q**2 * lap) == 0
    for i in range(1, 4):
        checks[f"metric_source_0{i}"] = s.simplify(Tlin[0, i] - 2 * gamma * q**2 * s.diff(sigma, t, coords[i])) == 0
        for j in range(1, 4):
            checks[f"metric_source_{i}{j}"] = s.simplify(Tlin[i, j] - 2 * gamma * q**2 * eta[i, j] * sdd) == 0
    trace = sum(eta[i, i] * Tlin[i, i] for i in range(4))
    R00 = s.simplify((Tlin[0, 0] + trace / 2) / M2)
    curvature_feedback = s.expand(-2 * gamma * q**2 * R00)
    checks["trace_reversed_Einstein_00"] = s.simplify(R00 - gamma * q**2 * (lap + 3 * sdd) / M2) == 0
    delta_K = s.simplify(-curvature_feedback.coeff(sdd))
    delta_G = s.simplify(curvature_feedback.coeff(s.diff(sigma, xs[0], 2)))
    kinetic = s.factor(Kfixed + delta_K)
    restoring = s.factor(spatial_schur + delta_G)
    checks["metric_kinetic_feedback"] = s.simplify(delta_K - 6 * gamma**2 * q**4 / M2) == 0
    checks["metric_gradient_feedback"] = s.simplify(delta_G + 2 * gamma**2 * q**4 / M2) == 0

    # Orthogonal check: full local metric/scalar velocity Hessian at Y=0.
    ki = s.symbols("K1 K2 K3 K12 K13 K23", real=True)
    Qvar = s.symbols("Qvar", real=True)
    Ktrace = sum(ki[:3])
    Kl2 = sum(v**2 for v in ki[:3]) + 2 * sum(v**2 for v in ki[3:])
    velocity_density = M2 * (Kl2 - Ktrace**2) / 2 + PXgamma * (Qvar**2 - q**2) + PXX0 * (Qvar**2 - q**2)**2 / 2 - s.Rational(2, 3) * gamma * Qvar**3 * Ktrace
    hessian = s.hessian(velocity_density, [*ki, Qvar]).subs({ki[0]: H, ki[1]: H, ki[2]: H, ki[3]: 0, ki[4]: 0, ki[5]: 0, Qvar: q})
    velocity_schur = s.simplify((hessian[6, 6] - (hessian[6, :6] * hessian[:6, :6].inv() * hessian[:6, 6])[0]).subs(substitutions))
    checks["velocity_hessian_independent_kinetic_check"] = s.simplify(velocity_schur - kinetic) == 0
    dust_C = 2 * q**2 * d**2 / S0
    dust_restoring = s.factor(restoring.subs(C0, dust_C))
    checks["original_dust_control"] = s.simplify(dust_restoring.subs(gamma, 0)) == 0
    dust_slope = s.factor(s.diff(dust_restoring, gamma).subs(gamma, 0))
    profile_subs = {d: A * U / (2 * q * (q * A + U)), S0: U**2 / (q * A + U)}
    profile_slope = s.factor(dust_slope.subs(profile_subs))
    facts = {"checks": checks, "passed": all(checks.values()),
             "scope": "Order-two high-frequency principal scalar equations on homogeneous FLRW after scalar metric principal elimination and elliptic tau Schur, Sgamma != 0. No finite-wavelength stability or nonlinear Dirac count.",
             "expressions": {"kinetic": str(kinetic), "restoring": str(restoring), "tau_stiffness": str(tau_stiffness), "spatial_matrix_before_metric": str(spatial_matrix), "dust_restoring": str(dust_restoring), "dust_first_gamma_derivative": str(dust_slope), "profile_first_gamma_derivative": str(profile_slope)}}
    ctx = dict(gamma=gamma, q=q, H=H, qdot=qdot, M2=M2, C0=C0, S0=S0, d=d, B0=B0, A=A, U=U,
               kinetic=kinetic, restoring=restoring, tau_stiffness=tau_stiffness,
               Cgamma=Cgamma, speed_squared=s.factor(restoring / kinetic),
               dust_restoring=dust_restoring, dust_first_gamma_derivative=dust_slope,
               profile_first_gamma_derivative=profile_slope)
    return facts, ctx


if __name__ == "__main__":
    facts, ctx = derive()
    source = Path(__file__).resolve()
    root = next(p for p in source.parents if (p / ".git").exists())
    facts["provenance"] = {"python": platform.python_version(), "sympy": s.__version__,
        "current_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "arithmetic": "exact symbolic", "randomness": "none"}
    print(json.dumps(facts, indent=2, sort_keys=True))
    raise SystemExit(0 if facts["passed"] else 1)
