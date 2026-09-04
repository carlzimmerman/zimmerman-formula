#!/usr/bin/env python3
"""Independent 3-D orbit checks of the exponential-AQUAL EFD clock laws.

This file intentionally does not import the analytic production module.  It
integrates the force of the unexpanded anisotropic point potential and extracts
frequencies or successive-node angles directly from trajectories.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class FrequencyAudit:
    eta: float
    q: float
    measured_azimuthal_frequency: float
    measured_vertical_frequency: float
    measured_ratio: float
    predicted_ratio: float
    relative_error: float
    zero_crossings: int


@dataclass(frozen=True)
class NodeAudit:
    eta: float
    epsilon: float
    eccentricity: float
    inclination: float
    argument_of_periapsis: float
    first_periapsis_node_shift: float
    first_order_initial_node_shift: float
    first_step_relative_difference: float
    first_radial_period: float


def _parameters(eta: float) -> tuple[float, float, float]:
    eta = float(eta)
    if not math.isfinite(eta) or eta <= 0.0:
        raise ValueError("the numerical orbit audit requires eta > 0")
    mu = -math.expm1(-eta)
    L = eta * math.exp(-eta) / mu
    return mu, L, 1.0 + L


def measure_frequency_ratio(eta: float, cycles: int = 14, amplitude: float = 2.0e-5) -> FrequencyAudit:
    """Measure nu_z/Omega_phi from a small vertical 3-D perturbation."""
    _, _, q = _parameters(eta)
    if cycles < 4 or not 0.0 < amplitude < 1.0e-2:
        raise ValueError("use cycles >= 4 and 0 < amplitude < 1e-2")
    root_q = math.sqrt(q)
    omega_estimate = math.sqrt(1.0 / root_q)
    period_estimate = 2.0 * math.pi / omega_estimate
    initial = np.array([1.0, 0.0, amplitude, 0.0, omega_estimate, 0.0], dtype=float)

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        x, y, z, vx, vy, vz = state
        denominator_squared = z * z + q * (x * x + y * y)
        denominator_cubed = denominator_squared**1.5
        acceleration = -np.array([q * x, q * y, z], dtype=float) / denominator_cubed
        return np.array([vx, vy, vz, *acceleration], dtype=float)

    def z_crossing(_time: float, state: np.ndarray) -> float:
        return float(state[2])

    z_crossing.direction = 0
    z_crossing.terminal = False
    end_time = cycles * period_estimate
    sample_times = np.linspace(0.0, end_time, cycles * 800 + 1)
    solution = solve_ivp(
        rhs,
        (0.0, end_time),
        initial,
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-14,
        max_step=period_estimate / 250.0,
        t_eval=sample_times,
        events=z_crossing,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    azimuth = np.unwrap(np.arctan2(solution.y[1], solution.y[0]))
    omega_measured = float(np.polyfit(solution.t, azimuth, 1)[0])
    crossings = np.asarray(solution.t_events[0], dtype=float)
    if crossings.size < 6:
        raise RuntimeError("too few vertical zero crossings")
    half_period = float(np.mean(np.diff(crossings)))
    nu_measured = math.pi / half_period
    measured_ratio = nu_measured / omega_measured
    predicted_ratio = 1.0 / root_q
    return FrequencyAudit(
        eta=float(eta),
        q=q,
        measured_azimuthal_frequency=omega_measured,
        measured_vertical_frequency=nu_measured,
        measured_ratio=measured_ratio,
        predicted_ratio=predicted_ratio,
        relative_error=abs(measured_ratio / predicted_ratio - 1.0),
        zero_crossings=int(crossings.size),
    )


def _rotation_z(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def _rotation_x(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def _node_longitude(state: np.ndarray) -> float:
    angular_momentum = np.cross(state[:3], state[3:])
    node = np.cross(np.array([0.0, 0.0, 1.0]), angular_momentum)
    return math.atan2(float(node[1]), float(node[0]))


def _principal_angle(angle: float) -> float:
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def measure_node_advance(
    eta: float,
    eccentricity: float,
    inclination: float,
    argument_of_periapsis: float,
    *,
    rtol: float = 2.0e-12,
    atol: float = 2.0e-14,
    max_step: float = 0.03,
) -> NodeAudit:
    """Measure the first-periapsis node step in the unexpanded EFD potential."""
    _, L, q = _parameters(eta)
    eccentricity = float(eccentricity)
    inclination = float(inclination)
    argument_of_periapsis = float(argument_of_periapsis)
    if not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity must satisfy 0 <= e < 1")
    if not 0.0 < rtol < 1.0e-3 or not 0.0 < atol < rtol or not 0.0 < max_step < 1.0:
        raise ValueError("invalid solver tolerance or step cap")
    epsilon = L / q
    # Units: the Kepler part of the anisotropic potential has k_e=1 and a=1.
    semimajor_axis = 1.0
    radius_periapsis = semimajor_axis * (1.0 - eccentricity)
    speed_periapsis = math.sqrt((1.0 + eccentricity) / (semimajor_axis * (1.0 - eccentricity)))
    rotation = _rotation_z(0.0) @ _rotation_x(inclination) @ _rotation_z(argument_of_periapsis)
    position = rotation @ np.array([radius_periapsis, 0.0, 0.0])
    velocity = rotation @ np.array([0.0, speed_periapsis, 0.0])
    initial = np.concatenate((position, velocity))

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        x, y, z, vx, vy, vz = state
        denominator_squared = x * x + y * y + (1.0 - epsilon) * z * z
        denominator_cubed = denominator_squared**1.5
        acceleration = -np.array([x, y, (1.0 - epsilon) * z]) / denominator_cubed
        return np.array([vx, vy, vz, *acceleration], dtype=float)

    def periapsis(_time: float, state: np.ndarray) -> float:
        return float(np.dot(state[:3], state[3:]))

    periapsis.direction = 1
    periapsis.terminal = False
    solution = solve_ivp(
        rhs,
        (0.0, 20.0 * math.pi),
        initial,
        method="DOP853",
        rtol=rtol,
        atol=atol,
        max_step=max_step,
        events=periapsis,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    events = [
        (float(time), state)
        for time, state in zip(solution.t_events[0], solution.y_events[0])
        if time > 1.0e-5
    ]
    if not events:
        raise RuntimeError("no post-initial periapsis found")
    first_time, first_state = events[0]
    measured = _principal_angle(_node_longitude(first_state) - _node_longitude(initial))
    s = math.sqrt(1.0 - eccentricity * eccentricity)
    alpha = eccentricity / (1.0 + s)
    predicted = (
        math.pi
        * epsilon
        * math.cos(inclination)
        / s
        * (1.0 - alpha * alpha * math.cos(2.0 * argument_of_periapsis))
    )
    return NodeAudit(
        eta=float(eta),
        epsilon=epsilon,
        eccentricity=eccentricity,
        inclination=inclination,
        argument_of_periapsis=argument_of_periapsis,
        first_periapsis_node_shift=measured,
        first_order_initial_node_shift=predicted,
        first_step_relative_difference=(
            abs(measured / predicted - 1.0) if predicted != 0.0 else abs(measured)
        ),
        first_radial_period=first_time,
    )


def run_independent_audit() -> dict[str, object]:
    """Run the deterministic trajectory suite and return its certificate."""
    geometry = dict(eccentricity=0.3, inclination=math.radians(20.0), argument_of_periapsis=math.radians(40.0))
    frequency = measure_frequency_ratio(eta=1.0)
    controlled = measure_node_advance(eta=6.0, **geometry)
    controlled_refined = measure_node_advance(
        eta=6.0,
        rtol=5.0e-13,
        atol=5.0e-15,
        max_step=0.015,
        **geometry,
    )
    frozen = measure_node_advance(eta=2.47812944, **geometry)
    checks = {
        "direct_frequency_ratio": frequency.relative_error < 2.5e-5,
        "controlled_first_order_node": controlled.first_step_relative_difference < 0.01,
        "unexpanded_shift_is_prograde": (
            controlled.first_periapsis_node_shift > 0.0
            and frozen.first_periapsis_node_shift > 0.0
        ),
        "sampled_stronger_anisotropy_has_larger_first_step_difference": (
            frozen.first_step_relative_difference > controlled.first_step_relative_difference
        ),
        "node_step_size_convergence": abs(
            controlled_refined.first_periapsis_node_shift
            - controlled.first_periapsis_node_shift
        ) < 2.0e-10,
        "frozen_unexpanded_case_resolved_not_certified_first_order": (
            math.isfinite(frozen.first_step_relative_difference)
            and 0.0 < frozen.first_periapsis_node_shift < math.pi
        ),
    }
    return {
        "status": (
            "PASS_NONRELATIVISTIC_EFD_ORBIT_AUDIT"
            if all(checks.values())
            else "FAIL_NONRELATIVISTIC_EFD_ORBIT_AUDIT"
        ),
        "checks": checks,
        "frequency_audit": asdict(frequency),
        "node_audits": {
            "eta_6": asdict(controlled),
            "eta_6_refined": asdict(controlled_refined),
            "eta_2p47812944": asdict(frozen),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_independent_audit()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
