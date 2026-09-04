#!/usr/bin/env python3
"""Independent nonlinear-orbit audit of the Kepler spectrometer.

No production functions are imported.  In units GM=a0=1, the script solves
the implicit exponential-MOND force equation at every ODE evaluation,
integrates slightly eccentric orbits, measures successive radial maxima, and
compares that measured clock ratio with both a finite-difference force slope
and the symbolic transition law.  It then feeds the measured ratio—not the
analytic one—through the W_{-1} inverse and reconstructs GM and a0.
"""

from __future__ import annotations

import json
import math
from typing import Any

import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


GM_TRUE = 1.0
A0_TRUE = 1.0


def solve_field(radius: float) -> float:
    """Solve y(1-exp(-y))=GM/(a0 r^2), with no analytic force inversion."""

    target = GM_TRUE / (A0_TRUE * radius**2)

    def residual(y: float) -> float:
        return y * (-math.expm1(-y)) - target

    upper = max(1.0, target + 1.0)
    while residual(upper) < 0:
        upper *= 2.0
    return brentq(residual, 0.0, upper, xtol=1e-14, rtol=1e-14)


def invert_measured_ratio(q: float) -> float:
    if not (1.0 < q < 2.0):
        raise ValueError("measured ratio is outside the exterior model domain")
    with mp.workdps(50):
        qq = mp.mpf(q)
        L = (qq - 1) / (3 - qq)
        return float(-L - mp.lambertw(-L * mp.exp(-L), -1).real)


def audit_orbit(y_target: float, radial_amplitude: float = 1e-5) -> dict[str, Any]:
    mu = -math.expm1(-y_target)
    radius = math.sqrt(GM_TRUE / (A0_TRUE * y_target * mu))
    y_circle = solve_field(radius)
    g_circle = A0_TRUE * y_circle
    omega = math.sqrt(g_circle / radius)
    angular_momentum = math.sqrt(g_circle * radius**3)
    circular_period = 2 * math.pi / omega

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        r, radial_velocity, _theta = state
        acceleration = A0_TRUE * solve_field(float(r))
        return (
            radial_velocity,
            angular_momentum**2 / r**3 - acceleration,
            angular_momentum / r**2,
        )

    def radial_maximum(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    radial_maximum.direction = -1  # type: ignore[attr-defined]
    radial_maximum.terminal = False  # type: ignore[attr-defined]
    solution = solve_ivp(
        equations,
        (0.0, 20.0 * circular_period),
        (radius * (1 + radial_amplitude), 0.0, 0.0),
        rtol=2e-11,
        atol=2e-13,
        max_step=circular_period / 100.0,
        events=radial_maximum,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    maxima = solution.t_events[0]
    maxima = maxima[maxima > 1e-8 / omega]
    if len(maxima) < 8:
        raise RuntimeError("too few radial maxima to measure the epicycle")
    radial_periods = np.diff(maxima)
    kappa_measured = 2 * math.pi / float(np.median(radial_periods))
    q_orbit = (kappa_measured / omega) ** 2

    # Five-point derivative of the independently root-solved force.
    h = radius * 1e-4
    samples = [A0_TRUE * solve_field(radius + j * h) for j in (-2, -1, 1, 2)]
    dg_dr = (samples[0] - 8 * samples[1] + 8 * samples[2] - samples[3]) / (12 * h)
    q_finite_difference = (dg_dr + 3 * g_circle / radius) / (g_circle / radius)

    L = y_target / math.expm1(y_target)
    q_symbolic = (1 + 3 * L) / (1 + L)

    y_inferred = invert_measured_ratio(q_orbit)
    a0_inferred = radius * omega**2 / y_inferred
    mu_inferred = -math.expm1(-y_inferred)
    gm_inferred = radius**3 * omega**2 * mu_inferred

    return {
        "y_target": y_target,
        "radius_GM_a0_units": radius,
        "events_used": len(maxima),
        "ode_evaluations": solution.nfev,
        "q_symbolic": q_symbolic,
        "q_finite_difference": q_finite_difference,
        "q_direct_orbit": q_orbit,
        "relative_q_error_orbit": (q_orbit - q_symbolic) / q_symbolic,
        "relative_q_error_finite_difference": (
            q_finite_difference - q_symbolic
        ) / q_symbolic,
        "a0_inferred_from_orbit": a0_inferred,
        "GM_inferred_from_orbit": gm_inferred,
        "relative_a0_error": a0_inferred / A0_TRUE - 1,
        "relative_GM_error": gm_inferred / GM_TRUE - 1,
    }


def main() -> int:
    rows = [audit_orbit(y) for y in (0.1, 0.25, 1.0, 3.0, 7.0)]
    max_q_error = max(abs(row["relative_q_error_orbit"]) for row in rows)
    max_fd_error = max(abs(row["relative_q_error_finite_difference"]) for row in rows)
    max_a0_error = max(abs(row["relative_a0_error"]) for row in rows)
    max_gm_error = max(abs(row["relative_GM_error"]) for row in rows)
    results = {
        "status": "PASS"
        if max_q_error < 5e-8
        and max_fd_error < 5e-8
        and max_a0_error < 2e-6
        and max_gm_error < 2e-6
        else "FAIL",
        "units": "GM_true=a0_true=1",
        "radial_fractional_amplitude": 1e-5,
        "max_relative_q_error_direct_orbit": max_q_error,
        "max_relative_q_error_finite_difference": max_fd_error,
        "max_relative_a0_recovery_error": max_a0_error,
        "max_relative_GM_recovery_error": max_gm_error,
        "orbits": rows,
    }
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
