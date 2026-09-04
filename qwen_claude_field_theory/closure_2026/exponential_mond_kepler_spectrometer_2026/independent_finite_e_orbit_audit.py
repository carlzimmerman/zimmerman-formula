#!/usr/bin/env python3
"""Production-independent nonlinear-orbit audit of the finite-e null.

The force is obtained by bracketing the implicit exponential-MOND equation at
every ODE evaluation.  This file imports none of the symbolic/production
finite-e module.  It measures turning radii and apsidal angles directly, then
tests the independently reimplemented O(e^2) clock and guiding-radius
corrections over an amplitude ladder.
"""

from __future__ import annotations

import json
import math
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


GM_TRUE = 1.0
A0_TRUE = 1.0
SAMPLED_Y = (0.1, 1.0, 3.0, 7.0)
APO_OFFSETS = (0.003, 0.01, 0.03)


def solve_field(radius: float) -> float:
    target = GM_TRUE / (A0_TRUE * radius**2)

    def residual(y: float) -> float:
        return y * (-math.expm1(-y)) - target

    upper = max(1.0, target + 1.0)
    while residual(upper) < 0:
        upper *= 2
    return brentq(residual, 0.0, upper, xtol=1e-14, rtol=1e-14)


def transition(y: float) -> dict[str, float]:
    L = y / math.expm1(y)
    q = (1 + 3 * L) / (1 + L)
    s = q - 3
    D = 4 * L * (y + L - 1) / (1 + L) ** 3
    E = -8 * L / (1 + L) ** 5 * (
        L**3
        + 3 * L**2 * y
        - 5 * L**2
        + 2 * L * y**2
        - 6 * L * y
        + 5 * L
        - y**2
        + 3 * y
        - 1
    )
    u3 = D + s**2 - s - 12
    u4 = E + 3 * (s - 1) * D + (s - 2) * (s**2 - s) + 60
    Ce = u4 / (8 * q) - 5 * u3**2 / (24 * q**2) - 3 - u3 / q
    return {"q": q, "u3": u3, "u4": u4, "Ce": Ce}


def invert_ratio(q_measured: float, eccentricity: float, finite_e: bool) -> float:
    def residual(log_y: float) -> float:
        y = math.exp(log_y)
        state = transition(y)
        correction = 1 + state["Ce"] * eccentricity**2 if finite_e else 1
        return state["q"] * correction - q_measured

    return math.exp(brentq(residual, -14.0, 6.0, xtol=5e-15, rtol=1e-14))


def audit_orbit(y_target: float, apo_offset: float) -> dict[str, Any]:
    mu = -math.expm1(-y_target)
    guiding_radius = math.sqrt(GM_TRUE / (A0_TRUE * y_target * mu))
    omega0 = math.sqrt(A0_TRUE * y_target / guiding_radius)
    angular_momentum = math.sqrt(A0_TRUE * y_target * guiding_radius**3)
    circular_period = 2 * math.pi / omega0

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        radius, radial_velocity, _azimuth = state
        return (
            radial_velocity,
            angular_momentum**2 / radius**3 - A0_TRUE * solve_field(float(radius)),
            angular_momentum / radius**2,
        )

    def maximum(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    def minimum(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    maximum.direction = -1  # type: ignore[attr-defined]
    maximum.terminal = False  # type: ignore[attr-defined]
    minimum.direction = 1  # type: ignore[attr-defined]
    minimum.terminal = False  # type: ignore[attr-defined]
    solution = solve_ivp(
        equations,
        (0.0, 14 * circular_period),
        (guiding_radius * (1 + apo_offset), 0.0, 0.0),
        method="DOP853",
        rtol=2e-12,
        atol=2e-14,
        max_step=circular_period / 120,
        events=(maximum, minimum),
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    maxima = solution.y_events[0]
    maximum_times = solution.t_events[0]
    maxima = maxima[maximum_times > 1e-8 / omega0]
    minima = solution.y_events[1]
    if len(maxima) < 8 or len(minima) < 8:
        raise RuntimeError("too few turning points for a fundamental-frequency audit")

    apoapsis = float(np.median(maxima[:, 0]))
    periapsis = float(np.median(minima[:, 0]))
    mean_turning_radius = (apoapsis + periapsis) / 2
    eccentricity = (apoapsis - periapsis) / (apoapsis + periapsis)
    apsidal_angle = float(np.median(np.diff(maxima[:, 2])))
    q_e = (2 * math.pi / apsidal_angle) ** 2

    exact = transition(y_target)
    measured_Ce = (q_e / exact["q"] - 1) / eccentricity**2

    recovered_y = invert_ratio(q_e, eccentricity, finite_e=True)
    recovered = transition(recovered_y)
    corrected_guiding_radius = mean_turning_radius * (
        1 + recovered["u3"] * eccentricity**2 / (6 * recovered["q"])
    )
    corrected_X = recovered_y * (-math.expm1(-recovered_y))
    corrected_null = corrected_guiding_radius**2 * corrected_X

    uncorrected_y = invert_ratio(q_e, 0.0, finite_e=False)
    uncorrected_X = uncorrected_y * (-math.expm1(-uncorrected_y))
    uncorrected_null = mean_turning_radius**2 * uncorrected_X

    return {
        "y_target": y_target,
        "apo_offset": apo_offset,
        "measured_e": eccentricity,
        "turning_mean_radius": mean_turning_radius,
        "apsidal_angle": apsidal_angle,
        "q0": exact["q"],
        "q_e": q_e,
        "Ce_symbolic": exact["Ce"],
        "Ce_measured": measured_Ce,
        "relative_Ce_error": (measured_Ce - exact["Ce"]) / exact["Ce"],
        "recovered_y": recovered_y,
        "relative_y_error": recovered_y / y_target - 1,
        "corrected_null": corrected_null,
        "absolute_corrected_null": abs(corrected_null - GM_TRUE / A0_TRUE),
        "uncorrected_null": uncorrected_null,
        "absolute_uncorrected_null": abs(uncorrected_null - GM_TRUE / A0_TRUE),
        "maxima_used": len(maxima),
        "minima_used": len(minima),
        "ode_evaluations": solution.nfev,
    }


def audit_logarithmic_limit(eccentricity: float = 0.03) -> dict[str, float | int]:
    """Measure the exact deep-MOND log-potential apsidal ratio.

    This is an all-orders-in-e limiting orbit, not data generated from the
    truncated production formula.  At fixed dimensionless angular momentum
    ell=1, equality of the two turning-point energies gives R analytically.
    """

    if not 0 < eccentricity < 1:
        raise ValueError("logarithmic-limit eccentricity must satisfy 0<e<1")
    log_ratio = math.log((1 + eccentricity) / (1 - eccentricity))
    mean_radius = math.sqrt(
        2 * eccentricity / ((1 - eccentricity**2) ** 2 * log_ratio)
    )
    periapsis = mean_radius * (1 - eccentricity)
    apoapsis = mean_radius * (1 + eccentricity)
    angular_momentum = 1.0

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        radius, radial_velocity, _azimuth = state
        return (
            radial_velocity,
            angular_momentum**2 / radius**3 - 1 / radius,
            angular_momentum / radius**2,
        )

    def maximum(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    maximum.direction = -1  # type: ignore[attr-defined]
    maximum.terminal = False  # type: ignore[attr-defined]
    solution = solve_ivp(
        equations,
        (0.0, 20 * math.pi),
        (apoapsis, 0.0, 0.0),
        method="DOP853",
        rtol=5e-13,
        atol=5e-15,
        max_step=2 * math.pi / 300,
        events=maximum,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    event_times = solution.t_events[0]
    maxima = solution.y_events[0][event_times > 1e-8]
    if len(maxima) < 8:
        raise RuntimeError("too few log-potential apoapses")
    apsidal_angle = float(np.median(np.diff(maxima[:, 2])))
    q_e = (2 * math.pi / apsidal_angle) ** 2
    truncated_endpoint = 2 * (1 + eccentricity**2 / 6)
    return {
        "eccentricity": eccentricity,
        "mean_radius": mean_radius,
        "apsidal_angle": apsidal_angle,
        "q_e": q_e,
        "truncated_q_endpoint": truncated_endpoint,
        "endpoint_excess": q_e - truncated_endpoint,
        "maxima_used": len(maxima),
        "ode_evaluations": solution.nfev,
    }


def audit_grid() -> dict[str, Any]:
    rows = [audit_orbit(y, offset) for offset in APO_OFFSETS for y in SAMPLED_Y]
    summaries = {}
    for offset in APO_OFFSETS:
        selected = [row for row in rows if row["apo_offset"] == offset]
        summaries[str(offset)] = {
            "max_relative_Ce_error": max(
                abs(row["relative_Ce_error"]) for row in selected
            ),
            "max_relative_y_error": max(
                abs(row["relative_y_error"]) for row in selected
            ),
            "max_absolute_corrected_null": max(
                row["absolute_corrected_null"] for row in selected
            ),
            "max_absolute_uncorrected_null": max(
                row["absolute_uncorrected_null"] for row in selected
            ),
        }
    exact_logarithmic_limit = audit_logarithmic_limit()
    passed = (
        summaries["0.003"]["max_relative_Ce_error"] < 4e-5
        and summaries["0.003"]["max_absolute_corrected_null"] < 2e-8
        and summaries["0.01"]["max_absolute_corrected_null"] < 3e-7
        and summaries["0.03"]["max_absolute_corrected_null"] < 3e-5
        and summaries["0.03"]["max_absolute_corrected_null"]
        < summaries["0.03"]["max_absolute_uncorrected_null"] / 20
        and exact_logarithmic_limit["endpoint_excess"] > 1e-7
    )
    return {
        "status": "PASS" if passed else "FAIL",
        "units": "GM_true=a0_true=1",
        "sampled_y": list(SAMPLED_Y),
        "apo_offsets": list(APO_OFFSETS),
        "by_apo_offset": summaries,
        "exact_logarithmic_limit": exact_logarithmic_limit,
        "orbits": rows,
    }


def main() -> int:
    results = audit_grid()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
