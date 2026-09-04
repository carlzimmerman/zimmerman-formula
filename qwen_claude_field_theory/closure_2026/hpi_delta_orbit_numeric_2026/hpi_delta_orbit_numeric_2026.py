#!/usr/bin/env python3
"""Numerical audit of the exponential-MOND near-circular orbit law."""

from __future__ import annotations

import json
import math
import platform
import sys

import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sp


def _require_positive_finite(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be positive and finite, got {value!r}")


def derive_symbolic_orbit_law() -> dict[str, object]:
    """Derive the local epicycle law from the differentiated flux equation."""

    y = sp.symbols("y", positive=True, finite=True)
    mass_log_slope, log_g_slope = sp.symbols("m s", real=True)
    mu = 1 - sp.exp(-y)
    log_mu_slope = sp.factor(y * sp.diff(mu, y) / mu)
    expected_log_mu_slope = y / (sp.exp(y) - 1)

    # d ln(mu*g)/d ln(r) = d ln(M_b/r^2)/d ln(r).
    slope_equation = sp.Eq(
        (1 + log_mu_slope) * log_g_slope,
        mass_log_slope - 2,
    )
    derived_log_g_slope = sp.solve(slope_equation, log_g_slope)[0]

    # Linearizing r_ddot=l^2/r^3-g(r) gives kappa^2=g'+3g/r.
    general_ratio = sp.factor(3 + derived_log_g_slope)
    general_closed_form = (
        (1 + mass_log_slope) * (sp.exp(y) - 1) + 3 * y
    ) / (sp.exp(y) - 1 + y)
    exterior_ratio = sp.factor(general_ratio.subs(mass_log_slope, 0))
    exterior_closed_form = (sp.exp(y) - 1 + 3 * y) / (
        sp.exp(y) - 1 + y
    )
    precession = 2 * sp.pi * (1 / sp.sqrt(exterior_ratio) - 1)
    return {
        "symbols": {"y": y, "mass_log_slope": mass_log_slope},
        "mu": mu,
        "log_mu_slope": log_mu_slope,
        "log_mu_slope_residual": sp.simplify(
            log_mu_slope - expected_log_mu_slope
        ),
        "slope_equation": slope_equation,
        "derived_log_g_slope": derived_log_g_slope,
        "mass_slope_equation_residual": sp.simplify(
            (1 + log_mu_slope) * derived_log_g_slope
            - (mass_log_slope - 2)
        ),
        "general_ratio": general_ratio,
        "general_closed_form": general_closed_form,
        "general_closed_form_residual": sp.simplify(
            general_ratio - general_closed_form
        ),
        "exterior_ratio": exterior_ratio,
        "exterior_closed_form": exterior_closed_form,
        "exterior_closed_form_residual": sp.simplify(
            exterior_ratio - exterior_closed_form
        ),
        "precession": precession,
        "deep_exterior_ratio": sp.limit(exterior_ratio, y, 0, dir="+"),
        "newtonian_exterior_ratio": sp.limit(exterior_ratio, y, sp.oo),
        "deep_precession": sp.simplify(sp.limit(precession, y, 0, dir="+")),
        "newtonian_precession": sp.limit(precession, y, sp.oo),
    }


def mu_exponential(y: float) -> float:
    """Return ``1-exp(-y)`` without cancellation at small positive ``y``."""

    return -math.expm1(-y)


def analytic_kappa2_over_omega2(
    y: float, *, mass_log_slope: float = 0.0
) -> float:
    """Return kappa^2/Omega^2 for local enclosed-mass slope ``m``.

    Here ``m=d ln(M_b(<r))/d ln(r)``.  The exterior point-mass result is
    the default ``m=0`` branch.
    """

    mu = mu_exponential(y)
    logarithmic_mu_slope = y * math.exp(-y) / mu
    return (
        1.0 + mass_log_slope + 3.0 * logarithmic_mu_slope
    ) / (1.0 + logarithmic_mu_slope)


def analytic_kappa_over_omega(
    y: float, *, mass_log_slope: float = 0.0
) -> float:
    return math.sqrt(
        analytic_kappa2_over_omega2(y, mass_log_slope=mass_log_slope)
    )


def solve_exterior_acceleration(
    radius: float, *, gm: float = 1.0, a0: float = 1.0
) -> float:
    """Solve ``mu(g/a0) g = GM/r^2`` on its unique positive branch."""

    _require_positive_finite("radius", radius)
    _require_positive_finite("gm", gm)
    _require_positive_finite("a0", a0)
    source = gm / (a0 * radius**2)

    def residual(y: float) -> float:
        return y * mu_exponential(y) - source

    upper = source + math.sqrt(source) + 1.0
    y = brentq(
        residual,
        0.0,
        upper,
        xtol=5.0e-15,
        rtol=4.0 * np.finfo(float).eps,
        maxiter=100,
    )
    return a0 * y


def circular_orbit_from_y(
    y: float, *, gm: float = 1.0, a0: float = 1.0
) -> dict[str, float]:
    _require_positive_finite("y", y)
    _require_positive_finite("gm", gm)
    _require_positive_finite("a0", a0)
    acceleration = a0 * y
    radius = math.sqrt(gm / (a0 * y * mu_exponential(y)))
    omega = math.sqrt(acceleration / radius)
    return {
        "radius": radius,
        "acceleration": acceleration,
        "omega": omega,
        "angular_momentum": math.sqrt(acceleration * radius**3),
        "azimuthal_period": 2.0 * math.pi / omega,
    }


def integrate_near_circular_orbit(
    y: float,
    *,
    epsilon: float = 1.0e-4,
    requested_radial_cycles: int = 5,
    method: str = "DOP853",
    rtol: float = 2.0e-11,
    atol: float = 2.0e-13,
    gm: float = 1.0,
    a0: float = 1.0,
) -> dict[str, object]:
    """Integrate a slightly eccentric orbit and measure successive pericenters.

    The nonlinear ODE uses only the implicit exterior force law.  The analytic
    epicycle formula is not used to compute the event-to-event angle.
    """

    _require_positive_finite("y", y)
    _require_positive_finite("epsilon", epsilon)
    if epsilon >= 0.05:
        raise ValueError("epsilon must be below 0.05 for a near-circular audit")
    if requested_radial_cycles < 3:
        raise ValueError("requested_radial_cycles must be at least 3")
    _require_positive_finite("rtol", rtol)
    _require_positive_finite("atol", atol)

    reference = circular_orbit_from_y(y, gm=gm, a0=a0)
    radius0 = float(reference["radius"])
    angular_momentum = float(reference["angular_momentum"])
    azimuthal_period = float(reference["azimuthal_period"])

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        radius, radial_velocity, _theta = state
        acceleration = solve_exterior_acceleration(radius, gm=gm, a0=a0)
        return (
            radial_velocity,
            angular_momentum**2 / radius**3 - acceleration,
            angular_momentum / radius**2,
        )

    def pericenter_event(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    pericenter_event.direction = 1.0
    pericenter_event.terminal = False

    initial_state = (radius0 * (1.0 - epsilon), 0.0, 0.0)
    final_time = (requested_radial_cycles + 1.5) * azimuthal_period
    solution = solve_ivp(
        equations,
        (0.0, final_time),
        initial_state,
        method=method,
        events=pericenter_event,
        rtol=rtol,
        atol=atol,
        max_step=azimuthal_period / 100.0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    event_times = solution.t_events[0]
    event_states = solution.y_events[0]
    keep = event_times > azimuthal_period * 1.0e-8
    event_times = event_times[keep]
    event_states = event_states[keep]
    if len(event_times) < 2:
        raise RuntimeError("fewer than two post-initial pericenters were found")

    radial_periods = np.diff(event_times)
    apsidal_angles = np.diff(event_states[:, 2])
    mean_radial_period = float(np.mean(radial_periods))
    mean_apsidal_angle = float(np.mean(apsidal_angles))
    measured_ratio = 2.0 * math.pi / mean_apsidal_angle
    predicted_ratio = analytic_kappa_over_omega(y)

    force_residuals = []
    for radius in solution.y[0]:
        acceleration = solve_exterior_acceleration(radius, gm=gm, a0=a0)
        force_residuals.append(
            acceleration * mu_exponential(acceleration / a0) - gm / radius**2
        )

    return {
        "y": y,
        "epsilon": epsilon,
        "method": method,
        "radius": radius0,
        "omega": reference["omega"],
        "predicted_kappa_over_omega": predicted_ratio,
        "measured_kappa_over_omega": measured_ratio,
        "relative_frequency_error": measured_ratio / predicted_ratio - 1.0,
        "mean_radial_period": mean_radial_period,
        "mean_azimuth_per_radial_cycle": mean_apsidal_angle,
        "predicted_precession_degrees": math.degrees(
            2.0 * math.pi * (1.0 / predicted_ratio - 1.0)
        ),
        "measured_precession_degrees": math.degrees(
            mean_apsidal_angle - 2.0 * math.pi
        ),
        "measured_cycles": len(radial_periods),
        "max_force_residual": max(abs(value) for value in force_residuals),
        "nfev": solution.nfev,
    }


def run_epsilon_convergence(
    y: float,
    *,
    epsilons: tuple[float, ...],
    requested_radial_cycles: int = 5,
) -> list[dict[str, object]]:
    """Measure approach of the nonlinear orbit to the epicyclic limit."""

    rows = []
    for epsilon in epsilons:
        measurement = integrate_near_circular_orbit(
            y,
            epsilon=epsilon,
            requested_radial_cycles=requested_radial_cycles,
        )
        rows.append(
            {
                **measurement,
                "absolute_relative_frequency_error": abs(
                    float(measurement["relative_frequency_error"])
                ),
            }
        )
    return rows


def compare_integrators(
    y: float,
    *,
    epsilon: float,
    requested_radial_cycles: int,
    methods: tuple[str, ...],
) -> dict[str, object]:
    """Repeat one event measurement with independent solve_ivp methods."""

    if len(methods) < 2:
        raise ValueError("at least two integrators are required")
    measurements = {}
    for method in methods:
        result = integrate_near_circular_orbit(
            y,
            epsilon=epsilon,
            requested_radial_cycles=requested_radial_cycles,
            method=method,
            rtol=1.0e-10,
            atol=1.0e-12,
        )
        measurements[method] = float(result["measured_kappa_over_omega"])
    values = list(measurements.values())
    fractional_disagreement = (max(values) - min(values)) / float(np.mean(values))
    return {
        "measurements": measurements,
        "fractional_disagreement": fractional_disagreement,
    }


def run_no_constitutive_slope_mutation(
    y: float,
    *,
    epsilon: float,
    requested_radial_cycles: int,
) -> dict[str, object]:
    """Test the wrong Newtonian ``kappa=Omega`` formula against MOND events."""

    measurement = integrate_near_circular_orbit(
        y,
        epsilon=epsilon,
        requested_radial_cycles=requested_radial_cycles,
    )
    measured_ratio = float(measurement["measured_kappa_over_omega"])
    correct_ratio = analytic_kappa_over_omega(y)
    mutated_ratio = 1.0
    correct_error = abs(measured_ratio / correct_ratio - 1.0)
    mutated_error = abs(measured_ratio / mutated_ratio - 1.0)
    survival_tolerance = max(1.0e-6, 10.0 * correct_error)
    return {
        "measured_kappa_over_omega": measured_ratio,
        "correct_kappa_over_omega": correct_ratio,
        "mutated_kappa_over_omega": mutated_ratio,
        "correct_relative_error": correct_error,
        "mutated_relative_error": mutated_error,
        "survival_tolerance": survival_tolerance,
        "mutation_survives": mutated_error <= survival_tolerance,
    }


def run_full_audit() -> dict[str, object]:
    """Run the fixed, deterministic finite computation contract."""

    symbolic = derive_symbolic_orbit_law()
    grid_y = (0.01, 0.1, 1.0, 5.0, 10.0)
    grid = [
        integrate_near_circular_orbit(
            y,
            epsilon=1.0e-4,
            requested_radial_cycles=7,
            method="DOP853",
            rtol=2.0e-11,
            atol=2.0e-13,
        )
        for y in grid_y
    ]
    convergence = run_epsilon_convergence(
        1.0,
        epsilons=(1.0e-2, 1.0e-3, 1.0e-4),
        requested_radial_cycles=5,
    )
    integrators = compare_integrators(
        1.0,
        epsilon=1.0e-3,
        requested_radial_cycles=5,
        methods=("DOP853", "RK45"),
    )
    mutation = run_no_constitutive_slope_mutation(
        0.1,
        epsilon=1.0e-4,
        requested_radial_cycles=5,
    )

    max_grid_relative_error = max(
        abs(float(row["relative_frequency_error"])) for row in grid
    )
    max_grid_force_residual = max(
        float(row["max_force_residual"]) for row in grid
    )
    convergence_errors = [
        float(row["absolute_relative_frequency_error"])
        for row in convergence
    ]
    checks = {
        "symbolic_derivation_residuals_zero": all(
            symbolic[name] == 0
            for name in (
                "log_mu_slope_residual",
                "mass_slope_equation_residual",
                "general_closed_form_residual",
                "exterior_closed_form_residual",
            )
        ),
        "five_nonlinear_orbits_match_linear_law": max_grid_relative_error
        < 2.0e-7,
        "implicit_force_residual_small": max_grid_force_residual < 3.0e-12,
        "epsilon_to_zero_convergence": (
            convergence_errors[0] > 50.0 * convergence_errors[1]
            and convergence_errors[1] > 50.0 * convergence_errors[2]
            and convergence_errors[2] < 2.0e-8
        ),
        "independent_integrators_agree": float(
            integrators["fractional_disagreement"]
        )
        < 2.0e-8,
        "no_constitutive_slope_mutation_rejected": (
            not bool(mutation["mutation_survives"])
            and float(mutation["mutated_relative_error"]) > 0.2
        ),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "symbolic": symbolic,
        "grid": grid,
        "convergence": convergence,
        "integrators": integrators,
        "mutation": mutation,
        "max_grid_relative_error": max_grid_relative_error,
        "max_grid_force_residual": max_grid_force_residual,
        "contract": {
            "claim": (
                "Conditional on the exact isolated spherical exponential-MOND "
                "flux law, the exterior near-circular apsidal formula follows."
            ),
            "surrogate": (
                "Solve the implicit force and integrate nonlinear central-force "
                "orbits; measure successive pericenter times and angles."
            ),
            "units": "G*M=a0=1 (dimensionless rescaling)",
            "grid_y": grid_y,
            "epsilon": 1.0e-4,
            "algorithm": "solve_ivp DOP853 with brentq force inversion",
            "failure_meaning": (
                "A discrepancy refutes the formula or exposes the implementation; "
                "agreement is bounded numerical corroboration, not a theorem."
            ),
        },
        "scope": {
            "proves_novelty": False,
            "proves_full_relativistic_theory": False,
            "exterior_constant_mass_only": True,
            "includes_exact_y_zero": False,
            "includes_finite_eccentricity_theorem": False,
            "includes_external_field_effect": False,
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sp.__version__,
            "randomness": "none",
        },
    }


def main() -> int:
    audit = run_full_audit()
    print("=" * 88)
    print("HPI-DELTA EXPONENTIAL-MOND EXTERIOR ORBIT AUDIT")
    print("=" * 88)
    print("Analytic exterior (M_b constant):")
    print("  kappa^2/Omega^2 = (exp(y)-1+3*y)/(exp(y)-1+y)")
    print(
        "  Delta_varpi = 2*pi*"
        "(sqrt((exp(y)-1+y)/(exp(y)-1+3*y))-1)"
    )
    print("Extended spherical mass profile:")
    print(
        "  kappa^2/Omega^2 = "
        "((1+m)*(exp(y)-1)+3*y)/(exp(y)-1+y), "
        "m=d ln(M_b(<r))/d ln(r)"
    )
    print("Convention: Delta_varpi is relative to 2*pi per radial period.")
    print()
    print("Nonlinear pericenter-event measurements (G*M=a0=1, epsilon=1e-4):")
    print(
        "       y          r0      predicted       measured       rel.error   "
        "precession[deg]  cycles"
    )
    for row in audit["grid"]:
        print(
            f"{float(row['y']):8.3g} "
            f"{float(row['radius']):11.6g} "
            f"{float(row['predicted_kappa_over_omega']):14.10f} "
            f"{float(row['measured_kappa_over_omega']):14.10f} "
            f"{float(row['relative_frequency_error']): .3e} "
            f"{float(row['measured_precession_degrees']):16.9f} "
            f"{int(row['measured_cycles']):7d}"
        )

    print()
    print("Epsilon-to-zero convergence at y=1:")
    for row in audit["convergence"]:
        print(
            f"  epsilon={float(row['epsilon']):.0e}  "
            f"absolute relative error="
            f"{float(row['absolute_relative_frequency_error']):.3e}"
        )
    integrators = audit["integrators"]
    print()
    print("Integrator comparison at y=1, epsilon=1e-3:")
    for method, value in integrators["measurements"].items():
        print(f"  {method}: kappa/Omega={float(value):.12f}")
    print(
        "  fractional disagreement="
        f"{float(integrators['fractional_disagreement']):.3e}"
    )

    mutation = audit["mutation"]
    print()
    print("Mutation control (drop constitutive slope, falsely set kappa/Omega=1):")
    print(
        "  correct relative error="
        f"{float(mutation['correct_relative_error']):.3e}"
    )
    print(
        "  mutated relative error="
        f"{float(mutation['mutated_relative_error']):.3e}"
    )
    print(f"  mutation survives: {bool(mutation['mutation_survives'])}")

    print()
    print("Checks:")
    for name, passed in audit["checks"].items():
        print(f"  [{'PASS' if passed else 'FAIL'}] {name}")

    passed = bool(audit["passed"])
    status = "PASS_BOUNDED" if passed else "FAIL"
    print()
    if passed:
        print("VERDICT: PASS (BOUNDED NUMERICAL VALIDATION)")
    else:
        print("VERDICT: FAIL")
    print(
        "NON-CLAIMS: no novelty proof, no full relativistic closure proof, "
        "no exact-y=0 test, and no finite-eccentricity theorem."
    )
    certificate = {
        "status": status,
        "grid_points": len(audit["grid"]),
        "max_grid_relative_error": audit["max_grid_relative_error"],
        "max_grid_force_residual": audit["max_grid_force_residual"],
        "mutation_survives": bool(mutation["mutation_survives"]),
        "proves_novelty": bool(audit["scope"]["proves_novelty"]),
        "proves_full_relativistic_theory": bool(
            audit["scope"]["proves_full_relativistic_theory"]
        ),
    }
    print("CERTIFICATE_JSON: " + json.dumps(certificate, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
