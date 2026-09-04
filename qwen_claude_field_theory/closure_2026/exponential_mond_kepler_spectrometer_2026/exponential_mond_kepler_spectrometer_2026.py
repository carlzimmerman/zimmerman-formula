#!/usr/bin/env python3
"""Exact-exponential MOND Kepler spectrometer and curvature/clock audit.

This module starts with the frozen weak-static action of the HPI-Delta
candidate, varies Phi and Psi independently, derives the spherical exterior
law, derives the epicyclic clock from a test-particle Lagrangian, and derives
the weak-field curvature tensors from the metric perturbation.  The inverse
map uses the real W_{-1} branch of Lambert W; W_0 is the spurious y=0 root.

The calculation is deliberately bounded.  It is a prediction of the positive-
field weak-static branch, not a resurrection of the HPI-Delta relativistic
candidate, whose exact regular-center branch is already excluded elsewhere in
this repository.
"""

from __future__ import annotations

import json
import math
from typing import Any

import mpmath as mp
import sympy as sp
from scipy.optimize import minimize_scalar


def derive_action_and_flux(
    eh_psi_gradient_coefficient: sp.Expr = sp.Integer(1),
) -> dict[str, Any]:
    """Vary the radial weak-static action before imposing no slip.

    We work on the attractive branch Phi'(r)>0, so y=Phi'/a0.  The omitted
    common angular factor 4*pi and M_Pl^2 normalization do not affect the
    Euler equations.
    """

    r, a0, G = sp.symbols("r a_0 G", positive=True)
    rho = sp.Function("rho", positive=True)(r)
    Phi = sp.Function("Phi")(r)
    Psi = sp.Function("Psi")(r)
    y_symbol = sp.symbols("y", positive=True)
    F = 2 * ((1 + y_symbol) * sp.exp(-y_symbol) - 1)
    primitive = sp.expand(y_symbol**2 + F)
    mu = sp.simplify(sp.diff(primitive, y_symbol) / (2 * y_symbol))

    gp = sp.diff(Phi, r)
    hp = sp.diff(Psi, r)
    y_radial = gp / a0
    B = sp.sympify(eh_psi_gradient_coefficient)
    lagrangian = r**2 * (
        -2 * gp * hp
        + B * hp**2
        - a0**2 * F.subs(y_symbol, y_radial)
        - 8 * sp.pi * G * rho * Phi
    )

    euler_phi = sp.simplify(
        sp.diff(lagrangian, Phi) - sp.diff(sp.diff(lagrangian, gp), r)
    )
    euler_psi = sp.simplify(
        sp.diff(lagrangian, Psi) - sp.diff(sp.diff(lagrangian, hp), r)
    )
    expected_phi = sp.simplify(
        2 * sp.diff(r**2 * (hp - sp.exp(-y_radial) * gp), r)
        - 8 * sp.pi * G * rho * r**2
    )
    expected_psi = sp.simplify(2 * sp.diff(r**2 * (gp - B * hp), r))

    # The isolated regular solution of d[r^2(Phi'-B Psi')]/dr=0.
    slip_ratio = sp.simplify(1 / B)
    effective_mu = sp.simplify(slip_ratio - sp.exp(-y_symbol))

    slip_substitutions = {
        hp: slip_ratio * gp,
        sp.diff(Psi, (r, 2)): slip_ratio * sp.diff(Phi, (r, 2)),
    }
    euler_phi_on_slip = sp.simplify(euler_phi.subs(slip_substitutions) / 2)
    expected_flux = sp.simplify(
        sp.diff(r**2 * effective_mu.subs(y_symbol, y_radial) * gp, r)
        - 4 * sp.pi * G * rho * r**2
    )

    return {
        "r": r,
        "a0": a0,
        "G": G,
        "rho": rho,
        "Phi": Phi,
        "Psi": Psi,
        "y": y_symbol,
        "F": F,
        "primitive": primitive,
        "primitive_at_zero": sp.simplify(primitive.subs(y_symbol, 0)),
        "mu": mu,
        "lagrangian": lagrangian,
        "euler_phi": euler_phi,
        "euler_psi": euler_psi,
        "phi_euler_residual": sp.simplify(euler_phi - expected_phi),
        "psi_euler_residual": sp.simplify(euler_psi - expected_psi),
        "slip_ratio": slip_ratio,
        "effective_mu": effective_mu,
        "phi_mond_residual": sp.simplify(euler_phi_on_slip - expected_flux),
    }


def _linearized_riemann(
    spatial_sign: int,
) -> tuple[list[list[list[list[sp.Expr]]]], dict[str, sp.Symbol]]:
    """Build R_abcd^(1) from second derivatives of h_ab in Cartesian axes."""

    if spatial_sign not in (-1, 1):
        raise ValueError("spatial_sign must be -1 (physical) or +1 (mutation)")
    p_phi, t_phi, p_psi, t_psi = sp.symbols(
        "p_Phi t_Phi p_Psi t_Psi", real=True
    )
    H_phi = sp.diag(p_phi, t_phi, t_phi)
    H_psi = sp.diag(p_psi, t_psi, t_psi)
    n = 4

    # ddh[metric index a][metric index b][derivative c][derivative d].
    ddh = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)]
             for _ in range(n)] for _ in range(n)]
    for i in range(3):
        for j in range(3):
            ddh[0][0][i + 1][j + 1] = -2 * H_phi[i, j]
    for i in range(3):
        for j in range(3):
            if i == j:
                for a in range(3):
                    for b in range(3):
                        ddh[i + 1][j + 1][a + 1][b + 1] = (
                            2 * spatial_sign * H_psi[a, b]
                        )

    riemann = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)]
                for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    riemann[a][b][c][d] = sp.simplify(
                        (
                            ddh[a][d][b][c]
                            + ddh[b][c][a][d]
                            - ddh[a][c][b][d]
                            - ddh[b][d][a][c]
                        )
                        / 2
                    )
    return riemann, {
        "p_phi": p_phi,
        "t_phi": t_phi,
        "p_psi": p_psi,
        "t_psi": t_psi,
    }


def derive_curvature_from_metric(spatial_sign: int = -1) -> dict[str, Any]:
    """Contract the generated weak-field Riemann tensor.

    Returned R and K are respectively c^2 R and c^4 K when p and t carry
    physical-potential units.  Phi and Psi remain independent until the final
    no-slip substitution.
    """

    riemann, symbols = _linearized_riemann(spatial_sign)
    eta = sp.diag(-1, 1, 1, 1)
    n = 4
    ricci = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    for b in range(n):
        for d in range(n):
            ricci[b][d] = sp.simplify(
                sum(
                    eta[a, c] * riemann[a][b][c][d]
                    for a in range(n)
                    for c in range(n)
                )
            )
    scalar = sp.simplify(
        sum(eta[b, d] * ricci[b][d] for b in range(n) for d in range(n))
    )

    kretschmann = sp.Integer(0)
    nonzero = 0
    entries: list[tuple[int, int, int, int, sp.Expr]] = []
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    value = riemann[a][b][c][d]
                    if value != 0:
                        nonzero += 1
                        entries.append((a, b, c, d, value))
    # eta is diagonal, so raising all indices only supplies the four signs.
    for a, b, c, d, value in entries:
        kretschmann += (
            eta[a, a] * eta[b, b] * eta[c, c] * eta[d, d] * value**2
        )
    kretschmann = sp.simplify(kretschmann)

    p, t = sp.symbols("p t", real=True)
    noslip = {
        symbols["p_phi"]: p,
        symbols["t_phi"]: t,
        symbols["p_psi"]: p,
        symbols["t_psi"]: t,
    }
    return {
        **symbols,
        "p": p,
        "t": t,
        "R_general": scalar,
        "K_general": kretschmann,
        "R_noslip": sp.simplify(scalar.subs(noslip)),
        "K_noslip": sp.simplify(kretschmann.subs(noslip)),
        "nonzero_riemann_components": nonzero,
    }


def derive_orbit_and_clock_relations() -> dict[str, Any]:
    """Derive the radial epicycle and eliminate Phi' and Phi''."""

    r, ell = sp.symbols("r ell", positive=True)
    Phi = sp.Function("Phi")(r)
    effective_potential = Phi + ell**2 / (2 * r**2)
    circular_ell2 = sp.simplify(r**3 * sp.diff(Phi, r))
    kappa_raw = sp.diff(effective_potential, r, 2)
    kappa_on_circle = sp.simplify(kappa_raw.subs(ell**2, circular_ell2))

    p, t = sp.symbols("p t", real=True)
    replacements = {
        sp.diff(Phi, (r, 2)): p,
        sp.diff(Phi, r): r * t,
    }
    derived_kappa2 = sp.simplify(kappa_on_circle.subs(replacements))
    derived_Omega2 = t

    # Independent clock symbols are introduced only for the elimination step.
    # The two identities above prove how they map back to the potential.
    Omega2, kappa2 = sp.symbols("Omega2 kappa2", positive=True)

    curvature = derive_curvature_from_metric()
    R_clock = sp.simplify(
        curvature["R_noslip"].subs({curvature["p"]: kappa2 - 3 * Omega2,
                                        curvature["t"]: Omega2})
    )
    K_clock = sp.simplify(
        curvature["K_noslip"].subs({curvature["p"]: kappa2 - 3 * Omega2,
                                        curvature["t"]: Omega2})
    )
    return {
        "r": r,
        "ell": ell,
        "effective_potential": effective_potential,
        "circular_ell2": circular_ell2,
        "kappa_raw": kappa_raw,
        "kappa_on_circle": kappa_on_circle,
        "p": p,
        "t": t,
        "derived_Omega2": derived_Omega2,
        "derived_kappa2": derived_kappa2,
        "Omega2": Omega2,
        "kappa2": kappa2,
        "R_clock": R_clock,
        "K_clock": K_clock,
    }


def derive_exponential_transition() -> dict[str, sp.Expr]:
    """Differentiate the exterior flux and derive the clock/curvature map."""

    y = sp.symbols("y", positive=True)
    mu = 1 - sp.exp(-y)
    L = sp.simplify(y * sp.diff(mu, y) / mu)

    # d ln(mu*g)/d ln r=-2 and d ln(mu)/d ln g=L.
    slope = sp.simplify(-2 / (1 + L))
    q = sp.simplify(3 + slope)  # kappa^2/Omega^2
    R_over_Omega2 = sp.simplify(2 * (q - 1))
    K_over_Omega4 = sp.factor(4 * (3 * q**2 - 14 * q + 23))
    return {
        "y": y,
        "mu": mu,
        "L": L,
        "log_g_slope": slope,
        "q": q,
        "R_over_Omega2": R_over_Omega2,
        "K_over_Omega4": K_over_Omega4,
    }


def curvature_fingerprints() -> dict[str, dict[str, int]]:
    """Evaluate generated clock identities in three diagnostic limits."""

    q = sp.symbols("q", real=True)
    R = sp.expand(2 * (q - 1))
    K = sp.expand(4 * (3 * q**2 - 14 * q + 23))
    regimes = {
        "newton": sp.Integer(1),
        "deep_mond": sp.Integer(2),
        # g~sqrt(r) gives Phi''/(Phi'/r)=1/2, hence q=1/2+3.
        "regular_center": sp.Rational(7, 2),
    }
    return {
        name: {
            "R_over_Omega2": int(R.subs(q, value)),
            "K_over_Omega4": int(K.subs(q, value)),
        }
        for name, value in regimes.items()
    }


def _auto_dps_for_y(y: mp.mpf, base_dps: int) -> int:
    """Digits needed to resolve q away from its y=0 and y=infinity limits."""

    with mp.workdps(max(base_dps, 50)):
        if y <= 1:
            required = int(mp.ceil(max(mp.mpf(0), -mp.log10(y)))) + 60
        else:
            # q-1 is asymptotic to 2*y*exp(-y); this conservative bound is
            # intentionally a few digits larger than its negative log10.
            required = int(mp.ceil(y / mp.log(10))) + 60
    effective = max(base_dps, required)
    if effective > 2000:
        raise ValueError(
            "endpoint separation requires more than 2000 decimal digits; "
            "use an asymptotic representation instead of a finite q"
        )
    return effective


def clock_ratio_from_y(y: Any, dps: int = 80) -> mp.mpf:
    """Return q=kappa^2/Omega^2 for a positive exterior field y=g/a0."""

    yy = mp.mpf(y)
    if yy <= 0:
        raise ValueError("the positive-field exterior branch requires y>0")
    effective_dps = _auto_dps_for_y(yy, dps)
    with mp.workdps(effective_dps):
        yy = mp.mpf(y)
        L = yy / mp.expm1(yy)
        return +(1 + 3 * L) / (1 + L)


def y_from_clock_ratio(q: Any, branch: int = -1, dps: int = 80) -> mp.mpf:
    """Invert q using Lambert W.

    For 1<q<2, L=(q-1)/(3-q) lies in (0,1).  W_0(-L exp(-L))=-L
    gives the endpoint y=0 for every L and is therefore extraneous.  W_{-1}
    gives the unique physical y>0.
    """

    if branch not in (-1, 0):
        raise ValueError("only the real Lambert branches -1 and 0 are relevant")
    input_bits = q._mpf_[3] if isinstance(q, mp.mpf) else 0
    input_digits = int(math.ceil(input_bits * math.log10(2))) + 20
    preliminary_dps = max(dps, input_digits)
    with mp.workdps(preliminary_dps):
        qq = mp.mpf(q)
        if not (1 < qq < 2):
            raise ValueError("exact exponential exterior prediction requires 1<q<2")
        lower_distance = qq - 1
        upper_distance = 2 - qq
        endpoint_distance = min(lower_distance, upper_distance)
        endpoint_digits = int(mp.ceil(-mp.log10(endpoint_distance)))
        # Near q=2, L approaches 1 and -L*exp(-L) approaches -1/e
        # quadratically.  Resolving W_{-1} away from the branch point therefore
        # needs roughly twice the endpoint digits.  Near q=1 there is no such
        # quadratic coalescence.
        required_dps = (
            2 * endpoint_digits + 80
            if upper_distance < lower_distance
            else endpoint_digits + 60
        )
    effective_dps = max(preliminary_dps, required_dps)
    if effective_dps > 2000:
        raise ValueError(
            "endpoint separation requires more than 2000 decimal digits; "
            "the supplied finite q is not a practical inverse representation"
        )
    with mp.workdps(effective_dps):
        qq = mp.mpf(q)
        L = (qq - 1) / (3 - qq)
        w = mp.lambertw(-L * mp.exp(-L), branch)
        if abs(mp.im(w)) > mp.mpf(10) ** (-(effective_dps // 2)):
            raise ArithmeticError("Lambert inversion left the real branch")
        return +(-L - mp.re(w))


def infer_mass_and_a0(
    radius: Any,
    omega: Any,
    kappa: Any,
    *,
    G: Any = 6.67430e-11,
    dps: int = 80,
) -> dict[str, mp.mpf]:
    """Infer (a0,M) from radius and the two local orbital clocks."""

    input_bits = max(
        value._mpf_[3] if isinstance(value, mp.mpf) else 0
        for value in (radius, omega, kappa, G)
    )
    input_digits = int(math.ceil(input_bits * math.log10(2))) + 20
    working_dps = max(dps, input_digits)
    with mp.workdps(working_dps):
        r = mp.mpf(radius)
        Om = mp.mpf(omega)
        kap = mp.mpf(kappa)
        GG = mp.mpf(G)
        if min(r, Om, kap, GG) <= 0:
            raise ValueError("radius, frequencies, and G must be positive")
        q = (kap / Om) ** 2
        y = y_from_clock_ratio(q, dps=working_dps)
        a0 = r * Om**2 / y
        mu = -mp.expm1(-y)
        mass = r**3 * Om**2 * mu / GG
        return {"q": +q, "y": +y, "a0": +a0, "mass": +mass, "mu": +mu}


def fractional_condition_number(y: Any, dps: int = 80) -> float:
    """Return |d ln y / d ln q| for the inverse clock map."""

    with mp.workdps(dps):
        yy = mp.mpf(y)
        if yy <= 0:
            raise ValueError("y must be positive")
        em1 = mp.expm1(yy)
        L = yy / em1
        dL = (em1 - yy * mp.exp(yy)) / em1**2
        q = (1 + 3 * L) / (1 + L)
        dq = 2 * dL / (1 + L) ** 2
        return float(abs(q / (yy * dq)))


def find_best_conditioned_acceleration() -> dict[str, Any]:
    """Numerically locate the least ill-conditioned positive-field radius."""

    grid_points = 4001
    grid_logs = [-12.0 + 24.0 * i / (grid_points - 1) for i in range(grid_points)]
    grid_values = [
        fractional_condition_number(math.exp(log_y), dps=60)
        for log_y in grid_logs
    ]
    grid_index = min(range(grid_points), key=grid_values.__getitem__)
    result = minimize_scalar(
        lambda log_y: fractional_condition_number(math.exp(log_y), dps=60),
        bounds=(-12.0, 12.0),
        method="bounded",
        options={"xatol": 1e-13},
    )
    if not result.success:
        raise RuntimeError(f"conditioning minimization failed: {result.message}")
    y = math.exp(float(result.x))
    q = float(clock_ratio_from_y(y))
    return {
        "y": y,
        "q": q,
        "kappa_over_omega": math.sqrt(q),
        "fractional_condition": float(result.fun),
        "optimizer_evaluations": int(result.nfev),
        "bounded_log_y_interval": [-12.0, 12.0],
        "grid_points": grid_points,
        "grid_best_y": math.exp(grid_logs[grid_index]),
        "optimizer_no_worse_than_grid": bool(result.fun <= grid_values[grid_index]),
    }


def build_results() -> dict[str, Any]:
    """Run all live derivations and return a JSON-serializable result ledger."""

    action = derive_action_and_flux()
    geometry = derive_curvature_from_metric()
    clocks = derive_orbit_and_clock_relations()
    transition = derive_exponential_transition()
    optimum = find_best_conditioned_acceleration()
    y = transition["y"]
    L = transition["L"]
    inverse_residual = abs(y_from_clock_ratio(clock_ratio_from_y(1)) - 1)
    certificates = {
        "phi_variation": action["phi_euler_residual"] == 0,
        "psi_variation": action["psi_euler_residual"] == 0,
        "mond_reduction": action["phi_mond_residual"] == 0,
        "curvature_R_clock": sp.simplify(
            clocks["R_clock"] - 2 * (clocks["kappa2"] - clocks["Omega2"])
        ) == 0,
        "curvature_K_clock": sp.simplify(
            clocks["K_clock"]
            - 4
            * (
                3 * clocks["kappa2"] ** 2
                - 14 * clocks["kappa2"] * clocks["Omega2"]
                + 23 * clocks["Omega2"] ** 2
            )
        ) == 0,
        "exponential_q": sp.simplify(
            transition["q"] - (1 + 3 * L) / (1 + L)
        ) == 0,
        "lambert_inverse_y_1": inverse_residual < mp.mpf("1e-60"),
        "conditioning_optimizer_beats_grid": optimum["optimizer_no_worse_than_grid"],
    }
    passed = all(certificates.values())
    return {
        "status": (
            "PASS_BOUNDED_WEAK_STATIC_PREDICTION_NOT_RELATIVISTIC_CLOSURE"
            if passed
            else "FAIL_BOUNDED_WEAK_STATIC_PREDICTION"
        ),
        "action": {
            "primitive": str(action["primitive"]),
            "mu": str(action["mu"]),
            "phi_variation_residual": str(action["phi_euler_residual"]),
            "psi_variation_residual": str(action["psi_euler_residual"]),
            "mond_reduction_residual": str(action["phi_mond_residual"]),
            "slip_ratio": str(action["slip_ratio"]),
        },
        "geometry": {
            "general_R": str(geometry["R_general"]),
            "general_K": str(geometry["K_general"]),
            "noslip_c2R": str(geometry["R_noslip"]),
            "noslip_c4K": str(geometry["K_noslip"]),
            "generated_nonzero_riemann_components": geometry[
                "nonzero_riemann_components"
            ],
            "clock_c2R": str(clocks["R_clock"]),
            "clock_c4K": str(clocks["K_clock"]),
        },
        "exponential_exterior": {
            "L": str(L),
            "q_kappa2_over_omega2": str(transition["q"]),
            "c2R_over_omega2": str(transition["R_over_Omega2"]),
            "c4K_over_omega4": str(transition["K_over_Omega4"]),
            "inverse_y": "-L - LambertW(-L*exp(-L), -1)",
            "inverse_L_from_q": "(q - 1)/(3 - q)",
            "domain": "y>0, 1<q<2",
            "inverse_numeric_residual_y_1": float(inverse_residual),
        },
        "fingerprints": curvature_fingerprints(),
        "best_fractional_conditioning": optimum,
        "certificates": certificates,
        "nonclaims": [
            "not a new relativistic completion",
            "not a repair of the HPI-Delta regular-center obstruction",
            "not a disk-galaxy formula; spherical exterior only",
            "not a global novelty proof",
            "this module is the circular limit; finite-e correction is audited separately",
        ],
    }


def main() -> int:
    results = build_results()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
