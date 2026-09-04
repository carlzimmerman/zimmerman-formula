#!/usr/bin/env python3
"""Independent numerical audit of the exponential-AQUAL EFD flyby laws.

This file intentionally does not import the analytic module.  It compares a
separately written closed expression with direct improper quadrature of the
force, checks the scattering-map Jacobian by finite differences, and measures
the breakdown of the straight-line approximation by integrating curved
trajectories in the unexpanded EFD Green potential.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp


SEED = 20260904


def random_unit(rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=3)
    return vector / np.linalg.norm(vector)


def matrix_from_axis(q: float, axis: np.ndarray) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    return q * np.eye(3) - (q - 1.0) * np.outer(axis, axis)


def independent_closed_impulse(
    coupling: float,
    v_inf: float,
    A: np.ndarray,
    direction: np.ndarray,
    impact: np.ndarray,
) -> np.ndarray:
    trajectory_quadratic = float(direction @ A @ direction)
    cross_term = float(direction @ A @ impact)
    schur_distance = float(
        impact @ A @ impact - cross_term**2 / trajectory_quadratic
    )
    shifted = impact - direction * cross_term / trajectory_quadratic
    return (
        -2.0
        * coupling
        * (A @ shifted)
        / (v_inf * math.sqrt(trajectory_quadratic) * schur_distance)
    )


def quadrature_impulse(
    coupling: float,
    v_inf: float,
    A: np.ndarray,
    direction: np.ndarray,
    impact: np.ndarray,
) -> np.ndarray:
    timescale = np.linalg.norm(impact) / v_inf

    def scaled_acceleration(u: float) -> np.ndarray:
        position = impact + v_inf * timescale * u * direction
        quadratic = float(position @ A @ position)
        return -coupling * (A @ position) * timescale / quadratic**1.5

    return np.array(
        [
            quad(
                lambda u, component=component: scaled_acceleration(u)[component],
                -np.inf,
                np.inf,
                epsabs=2.0e-12,
                epsrel=2.0e-12,
                limit=300,
            )[0]
            for component in range(3)
        ]
    )


def random_quadrature_audit(cases: int = 96) -> dict:
    rng = np.random.default_rng(SEED)
    relative_errors = []
    transverse_errors = []
    for _ in range(cases):
        q = rng.uniform(1.0001, 1.9999)
        axis = random_unit(rng)
        direction = random_unit(rng)
        trial = random_unit(rng)
        impact = trial - direction * float(direction @ trial)
        if np.linalg.norm(impact) < 0.1:
            trial = np.roll(direction, 1)
            impact = trial - direction * float(direction @ trial)
        impact *= rng.uniform(0.4, 2.5) / np.linalg.norm(impact)
        coupling = rng.uniform(0.3, 2.0)
        v_inf = rng.uniform(0.5, 2.5)
        A = matrix_from_axis(q, axis)
        closed = independent_closed_impulse(coupling, v_inf, A, direction, impact)
        integrated = quadrature_impulse(coupling, v_inf, A, direction, impact)
        relative_errors.append(float(np.linalg.norm(closed - integrated) / np.linalg.norm(closed)))
        transverse_errors.append(float(abs(direction @ closed) / np.linalg.norm(closed)))
    return {
        "cases": cases,
        "seed": SEED,
        "maximum_relative_error": max(relative_errors),
        "median_relative_error": float(np.median(relative_errors)),
        "maximum_transversality_error": max(transverse_errors),
    }


def mutation_audit() -> dict:
    """Ensure common algebra mistakes are visible in a non-principal geometry."""
    q = 1.83
    axis = np.array([0.2, -0.3, 0.9327379053088815])
    axis /= np.linalg.norm(axis)
    direction = np.array([0.48, -0.36, 0.8])
    direction /= np.linalg.norm(direction)
    impact = np.array([1.11, 0.77, -0.32])
    impact -= direction * float(direction @ impact)
    A = matrix_from_axis(q, axis)
    coupling, v_inf = 0.91, 1.27
    reference = quadrature_impulse(coupling, v_inf, A, direction, impact)

    a = float(direction @ A @ direction)
    d = float(direction @ A @ impact)
    c = float(impact @ A @ impact)
    D = c - d**2 / a
    correct = independent_closed_impulse(coupling, v_inf, A, direction, impact)
    mutations = {
        "drop_shift": -2 * coupling * (A @ impact) / (v_inf * math.sqrt(a) * D),
        "drop_schur_term": -2
        * coupling
        * (A @ (impact - direction * d / a))
        / (v_inf * math.sqrt(a) * c),
        "drop_sqrt_a": -2
        * coupling
        * (A @ (impact - direction * d / a))
        / (v_inf * D),
        "wrong_sign": -correct,
    }
    errors = {
        name: float(np.linalg.norm(value - reference) / np.linalg.norm(reference))
        for name, value in mutations.items()
    }
    return {
        "correct_relative_error": float(np.linalg.norm(correct - reference) / np.linalg.norm(reference)),
        "mutation_relative_errors": errors,
    }


def scattering_map_jacobian_audit(cases: int = 24) -> dict:
    rng = np.random.default_rng(SEED + 1)
    relative_errors = []
    for _ in range(cases):
        a = rng.uniform(1.01, 1.99)
        q = rng.uniform(a, 2.0)
        B = np.diag([q, q / a])
        ell = rng.uniform(0.2, 1.7)
        impact = rng.uniform(-2.0, 2.0, size=2)
        if np.linalg.norm(impact) < 0.3:
            impact[0] += 0.7

        def deflection(vector: np.ndarray) -> np.ndarray:
            return -ell * (B @ vector) / float(vector @ B @ vector)

        step = 2.0e-6 * max(1.0, np.linalg.norm(impact))
        jacobian = np.column_stack(
            [
                (
                    deflection(impact + step * np.eye(2)[index])
                    - deflection(impact - step * np.eye(2)[index])
                )
                / (2.0 * step)
                for index in range(2)
            ]
        )
        theta = deflection(impact)
        numerical = abs(float(np.linalg.det(np.linalg.inv(jacobian))))
        closed = ell**2 / (
            float(np.linalg.det(B))
            * float(theta @ np.linalg.inv(B) @ theta) ** 2
        )
        relative_errors.append(abs(numerical / closed - 1.0))
    return {
        "cases": cases,
        "seed": SEED + 1,
        "maximum_relative_error": max(relative_errors),
        "median_relative_error": float(np.median(relative_errors)),
    }


def integrate_curved_trajectory(
    h: float,
    A: np.ndarray,
    direction: np.ndarray,
    impact: np.ndarray,
    cutoff: float = 30000.0,
) -> tuple[np.ndarray, float, float, int]:
    """Integrate dimensionless r''=-h A r/(r.A.r)^(3/2)."""

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        position = state[:3]
        quadratic = float(position @ A @ position)
        acceleration = -h * (A @ position) / quadratic**1.5
        return np.concatenate((state[3:], acceleration))

    initial = np.concatenate((impact - cutoff * direction, direction))
    solution = solve_ivp(
        rhs,
        (-cutoff, cutoff),
        initial,
        method="DOP853",
        rtol=3.0e-12,
        atol=3.0e-13,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    final = solution.y[:, -1]

    def energy(state: np.ndarray) -> float:
        return 0.5 * float(state[3:] @ state[3:]) - h / math.sqrt(
            float(state[:3] @ A @ state[:3])
        )

    initial_lz = float(np.cross(initial[:3], initial[3:])[2])
    final_lz = float(np.cross(final[:3], final[3:])[2])
    return (
        final[3:] - direction,
        abs(energy(final) - energy(initial)),
        abs(final_lz - initial_lz),
        solution.nfev,
    )


def curved_path_grid_audit() -> dict:
    h = 0.002
    rows = []
    max_energy_drift = 0.0
    max_lz_drift = 0.0
    for q in (1.1, 1.5, 1.99):
        A = np.diag([q, q, 1.0])
        for theta_degrees in (0, 15, 30, 45, 60, 75, 90):
            theta = math.radians(theta_degrees)
            direction = np.array([math.sin(theta), 0.0, math.cos(theta)])
            e_phi = np.array([0.0, 1.0, 0.0])
            e_theta = np.array([math.cos(theta), 0.0, -math.sin(theta)])
            for phi_degrees in (0, 15, 30, 45, 60, 75, 90):
                phi = math.radians(phi_degrees)
                impact = math.cos(phi) * e_phi + math.sin(phi) * e_theta
                born = independent_closed_impulse(h, 1.0, A, direction, impact)
                curved, energy_drift, lz_drift, evaluations = integrate_curved_trajectory(
                    h, A, direction, impact
                )
                transverse = curved - direction * float(direction @ curved)
                relative_error = float(np.linalg.norm(transverse - born) / np.linalg.norm(born))
                max_energy_drift = max(max_energy_drift, energy_drift)
                max_lz_drift = max(max_lz_drift, lz_drift)
                rows.append(
                    {
                        "q": q,
                        "theta_degrees": theta_degrees,
                        "phi_degrees": phi_degrees,
                        "relative_transverse_born_error": relative_error,
                        "function_evaluations": evaluations,
                    }
                )
    rows.sort(key=lambda row: row["relative_transverse_born_error"], reverse=True)
    worst = rows[0]

    # A second h value at the worst grid geometry tests the observed order,
    # rather than merely accumulating another same-regime success.
    q = float(worst["q"])
    theta = math.radians(float(worst["theta_degrees"]))
    phi = math.radians(float(worst["phi_degrees"]))
    direction = np.array([math.sin(theta), 0.0, math.cos(theta)])
    impact = math.cos(phi) * np.array([0.0, 1.0, 0.0]) + math.sin(phi) * np.array(
        [math.cos(theta), 0.0, -math.sin(theta)]
    )
    A = np.diag([q, q, 1.0])
    half_h = h / 2.0
    half_born = independent_closed_impulse(half_h, 1.0, A, direction, impact)
    half_curved, half_energy, half_lz, half_evaluations = integrate_curved_trajectory(
        half_h, A, direction, impact
    )
    half_transverse = half_curved - direction * float(direction @ half_curved)
    half_error = float(np.linalg.norm(half_transverse - half_born) / np.linalg.norm(half_born))

    return {
        "grid": {
            "q_values": [1.1, 1.5, 1.99],
            "theta_degrees": [0, 15, 30, 45, 60, 75, 90],
            "impact_azimuth_degrees": [0, 15, 30, 45, 60, 75, 90],
            "cases": len(rows),
            "born_parameter_h": h,
            "finite_cutoff_in_impact_parameters": 30000.0,
        },
        "maximum_relative_transverse_error": float(worst["relative_transverse_born_error"]),
        "median_relative_transverse_error": float(
            np.median([row["relative_transverse_born_error"] for row in rows])
        ),
        "worst_case": worst,
        "half_h_worst_case_relative_error": half_error,
        "half_h_to_full_h_error_ratio": half_error
        / float(worst["relative_transverse_born_error"]),
        "half_h_function_evaluations": half_evaluations,
        "maximum_energy_drift": max(max_energy_drift, half_energy),
        "maximum_axial_angular_momentum_drift": max(max_lz_drift, half_lz),
        "interpretation": (
            "finite grid evidence only; generic relative post-Born error is first order in h, "
            "while symmetry planes can cancel that term"
        ),
    }


def equatorial_exact_control() -> dict:
    q = 1.7
    h = 0.04
    A = np.diag([q, q, 1.0])
    direction = np.array([1.0, 0.0, 0.0])
    impact = np.array([0.0, 1.0, 0.0])
    curved, energy_drift, lz_drift, evaluations = integrate_curved_trajectory(
        h, A, direction, impact, cutoff=50000.0
    )
    effective_h = h / math.sqrt(q)
    exact_angle = 2.0 * math.atan(effective_h)
    exact_transverse_velocity = -2.0 * effective_h / (1.0 + effective_h**2)
    measured_angle = math.atan2(-curved[1], 1.0 + curved[0])
    return {
        "q": q,
        "h": h,
        "effective_equatorial_h": effective_h,
        "exact_deflection_angle": exact_angle,
        "measured_deflection_angle": measured_angle,
        "relative_angle_error": abs(measured_angle / exact_angle - 1.0),
        "exact_transverse_velocity_change": exact_transverse_velocity,
        "measured_transverse_velocity_change": float(curved[1]),
        "relative_transverse_error": float(abs(curved[1] / exact_transverse_velocity - 1.0)),
        "energy_drift": energy_drift,
        "axial_angular_momentum_drift": lz_drift,
        "function_evaluations": evaluations,
    }


def efd_regime_examples() -> dict:
    """Exhibit finite examples satisfying both EFD and weak-Born controls."""
    rng = np.random.default_rng(SEED + 2)
    rows = []
    for eta in (0.1, 0.5, 1.0, 2.47812944):
        mu = -math.expm1(-eta)
        q = 1.0 + eta * math.exp(-eta) / mu
        gm = 1.0
        a0 = 1.0
        g_external = eta * a0
        impact_norm = 50.0 * math.sqrt(gm / a0) / eta
        axis = np.array([0.0, 0.0, 1.0])
        direction = random_unit(rng)
        trial = random_unit(rng)
        impact = trial - direction * float(direction @ trial)
        impact *= impact_norm / np.linalg.norm(impact)
        A = matrix_from_axis(q, axis)
        coupling = gm / mu
        # Maximize the internal field along a broad straight-path interval.
        samples = np.linspace(-5.0, 5.0, 20001)
        accelerations = []
        for scaled_time in samples:
            position = impact + impact_norm * scaled_time * direction
            quadratic = float(position @ A @ position)
            accelerations.append(np.linalg.norm(coupling * (A @ position) / quadratic**1.5))
        max_efd_ratio = float(max(accelerations) / g_external)
        target_h = 0.002
        v_inf = math.sqrt(coupling / (impact_norm * target_h))
        rows.append(
            {
                "eta": eta,
                "mu_e": mu,
                "q": q,
                "impact_over_deep_efd_radius": 50.0,
                "maximum_internal_to_external_acceleration": max_efd_ratio,
                "born_parameter": coupling / (impact_norm * v_inf**2),
                "dimensionless_v_inf": v_inf,
            }
        )
    return {
        "rows": rows,
        "maximum_internal_to_external_acceleration": max(
            row["maximum_internal_to_external_acceleration"] for row in rows
        ),
        "note": (
            "These exhibit a nonempty joint regime; they do not bound nonlinear AQUAL errors "
            "for untested physical encounters."
        ),
    }


def run_audit() -> dict:
    quadrature = random_quadrature_audit()
    mutations = mutation_audit()
    jacobian = scattering_map_jacobian_audit()
    curved = curved_path_grid_audit()
    equatorial = equatorial_exact_control()
    regimes = efd_regime_examples()
    checks = {
        "random_quadrature_matches_closed_impulse": quadrature["maximum_relative_error"] < 2.0e-11,
        "random_impulses_are_transverse": quadrature["maximum_transversality_error"] < 2.0e-13,
        "correct_formula_beats_mutations": mutations["correct_relative_error"] < 2.0e-11
        and min(mutations["mutation_relative_errors"].values()) > 1.0e-3,
        "finite_difference_cross_section_jacobian": jacobian["maximum_relative_error"] < 2.0e-8,
        "declared_h_grid_stays_below_one_percent": curved["maximum_relative_transverse_error"] < 0.01,
        "worst_case_error_decreases_when_h_is_halved": 0.35
        < curved["half_h_to_full_h_error_ratio"]
        < 0.65,
        "curved_integration_conserves_energy": curved["maximum_energy_drift"] < 1.0e-10,
        "curved_integration_conserves_axial_angular_momentum": curved[
            "maximum_axial_angular_momentum_drift"
        ]
        < 1.0e-10,
        "equatorial_full_orbit_matches_exact_hyperbola": bool(
            equatorial["relative_angle_error"] < 5.0e-6
            and equatorial["relative_transverse_error"] < 5.0e-6
        ),
        "simultaneous_efd_and_born_examples_exist": regimes[
            "maximum_internal_to_external_acceleration"
        ]
        < 0.001,
    }
    passed = all(checks.values())
    return {
        "schema_version": 1,
        "status": "PASS_INDEPENDENT_NUMERICAL_AUDIT" if passed else "FAIL_INDEPENDENT_NUMERICAL_AUDIT",
        "checks": checks,
        "quadrature": quadrature,
        "mutation_audit": mutations,
        "cross_section_jacobian": jacobian,
        "curved_path_grid": curved,
        "equatorial_exact_control": equatorial,
        "efd_regime_examples": regimes,
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "non_claims": [
            "The 147-case grid is not a uniform theorem over all orientations or Born parameters.",
            "Post-Born integration is exact only within the linearized EFD Green potential.",
            "The exhibited EFD examples do not certify any particular astronomical encounter.",
            "Numerical agreement does not establish global novelty or a relativistic completion.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_audit()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
