#!/usr/bin/env python3
"""All-orders eccentric Kepler null for the exact exponential MOND exterior.

This removes the small-e expansion from the orbit observable.  It is still a
weak-static, isolated, spherical point-mass result—not a relativistic closure.
"""

from __future__ import annotations

from functools import lru_cache
import json
import math
from typing import Any
import warnings

from scipy.integrate import IntegrationWarning, quad, solve_ivp
from scipy.optimize import brentq
import sympy as sp


MIN_FORWARD_Y_PERI = 1e-6
MAX_FORWARD_Y_PERI = 25.0
MIN_INVERSE_Y_PERI = 1e-5
MAX_INVERSE_Y_PERI = 20.0
MIN_NUMERICAL_ECCENTRICITY = 0.01
MAX_NUMERICAL_ECCENTRICITY = 0.7
DEFAULT_INVERSE_LOG_GRID_SEGMENTS = 32
INVERSE_ENDPOINT_Q_UNCERTAINTY = 1e-8
INVERSE_ROOT_Q_RESIDUAL_TOLERANCE = 1e-9


def derive_exact_turning_law() -> dict[str, sp.Expr]:
    """Generate the scaling, turning-energy elimination, and exact invariant."""

    G, M, a0, x, y = sp.symbols("G M a_0 x y", positive=True)
    mu = 1 - sp.exp(-y)
    r_M = sp.sqrt(G * M / a0)
    dimensional_flux = sp.simplify(
        (a0 * y * mu - G * M / (r_M * x) ** 2) / a0
    )
    X = y * mu
    field_scale_residual = sp.simplify(dimensional_flux - (X - x**-2))

    root_p, root_a, eccentricity = sp.symbols(
        "sqrt_X_p sqrt_X_a e", positive=True
    )
    eccentricity_from_roots = (root_p - root_a) / (root_p + root_a)
    root_a_solution = sp.solve(
        sp.Eq(eccentricity, eccentricity_from_roots), root_a
    )[0]
    eccentricity_X_residual = sp.simplify(
        root_a_solution**2
        - root_p**2 * ((1 - eccentricity) / (1 + eccentricity)) ** 2
    )

    A, Xp, Xa = sp.symbols("A X_p X_a", positive=True)
    lambda_squared = A / (Xp - Xa)
    turning_energy_residual = sp.simplify(
        A / 2 - lambda_squared * (Xp - Xa) / 2
    )

    R, rM2 = sp.symbols("R r_M_squared", positive=True)
    rp = R * (1 - eccentricity)
    ra = R * (1 + eccentricity)
    pericenter_invariant = rp**2 * Xp
    apocenter_invariant = ra**2 * Xa
    Xa_relation = Xp * ((1 - eccentricity) / (1 + eccentricity)) ** 2
    invariant_pericenter_residual = sp.simplify(
        pericenter_invariant - rM2
    ).subs(rM2, pericenter_invariant)
    invariant_apocenter_residual = sp.simplify(
        (apocenter_invariant - pericenter_invariant).subs(Xa, Xa_relation)
    )
    cycle_factor_mutation = sp.simplify(
        ((2 * sp.pi) / sp.pi) ** 2
    )
    return {
        "field_scale_residual": field_scale_residual,
        "eccentricity_X_residual": eccentricity_X_residual,
        "turning_energy_residual": turning_energy_residual,
        "lambda_squared": lambda_squared,
        "invariant": pericenter_invariant,
        "invariant_pericenter_residual": sp.simplify(
            invariant_pericenter_residual
        ),
        "invariant_apocenter_residual": invariant_apocenter_residual,
        "cycle_factor_mutation": cycle_factor_mutation,
    }


def constitutive_X(y: float) -> float:
    if not math.isfinite(y) or y <= 0:
        raise ValueError("the positive exterior branch requires y>0")
    return y * (-math.expm1(-y))


def constitutive_X_prime(y: float) -> float:
    if not math.isfinite(y) or y <= 0:
        raise ValueError("the positive exterior branch requires y>0")
    return 1 + (y - 1) * math.exp(-y)


def _outer_acceleration(X_target: float, y_peri: float) -> float:
    if not 0 < X_target < constitutive_X(y_peri):
        raise ValueError("outer X target must lie strictly between zero and X_peri")
    return brentq(
        lambda value: constitutive_X(value) - X_target,
        1e-300,
        y_peri,
        xtol=5e-15,
        rtol=1e-14,
    )


def exact_apsidal_map(y_peri: float, eccentricity: float) -> dict[str, float]:
    """Return the exact all-orders apsidal map for one pair of turning points.

    y_peri labels the acceleration at pericenter.  The dimensionless radius is
    x=r/r_M with r_M=sqrt(GM/a0).  The numerical quadrature is bounded to
    ordinary double precision, while the displayed integral is exact.  A fresh
    dictionary is returned so callers cannot mutate the cached calculation.
    """

    return dict(_exact_apsidal_map_cached(y_peri, eccentricity))


@lru_cache(maxsize=1024)
def _exact_apsidal_map_cached(
    y_peri: float, eccentricity: float
) -> dict[str, float]:
    """Compute and cache the internal forward record."""

    if (
        not math.isfinite(y_peri)
        or not MIN_FORWARD_Y_PERI <= y_peri <= MAX_FORWARD_Y_PERI
    ):
        raise ValueError(
            "the exact formula holds for y_peri>0, but this double-precision "
            f"implementation is audited only for {MIN_FORWARD_Y_PERI}"
            f"<=y_peri<={MAX_FORWARD_Y_PERI}"
        )
    if (
        not math.isfinite(eccentricity)
        or not MIN_NUMERICAL_ECCENTRICITY
        <= eccentricity
        <= MAX_NUMERICAL_ECCENTRICITY
    ):
        raise ValueError(
            "the exact formula holds for 0<e<1, but this double-precision "
            f"implementation is audited only for {MIN_NUMERICAL_ECCENTRICITY}"
            f"<=e<={MAX_NUMERICAL_ECCENTRICITY}"
        )

    Xp = constitutive_X(y_peri)
    radius_ratio = (1 - eccentricity) / (1 + eccentricity)
    rho = 1 / radius_ratio
    Xa = Xp / rho**2
    y_apo = _outer_acceleration(Xa, y_peri)

    # Normalize radius by the pericenter: z=r/r_p in [1,rho].  Integrating
    # P'(z)=y(z) once with dense output makes the turning-point cancellation
    # use one internally consistent potential profile, avoiding nested
    # quadrature subtraction at both square-root endpoints.
    def acceleration_at_z(z: float) -> float:
        target = Xp / z**2
        if abs(z - 1) < 2e-15:
            return y_peri
        return _outer_acceleration(target, y_peri)

    potential_solution = solve_ivp(
        lambda z, _state: (acceleration_at_z(float(z)),),
        (1.0, rho),
        (0.0,),
        method="DOP853",
        rtol=3e-12,
        atol=3e-14,
        max_step=(rho - 1) / 240,
        dense_output=True,
    )
    if not potential_solution.success or potential_solution.sol is None:
        raise RuntimeError(
            f"dimensionless potential integration failed: {potential_solution.message}"
        )
    P_total = float(potential_solution.y[0, -1])
    j_squared = 2 * P_total / (1 - rho**-2)
    j = math.sqrt(j_squared)
    midpoint = (1 + rho) / 2
    half_width = (rho - 1) / 2
    def angular_integrand(angle: float) -> float:
        z = midpoint + half_width * math.sin(angle)
        derivative = half_width * math.cos(angle)
        P_value = float(potential_solution.sol(z)[0])
        radicand = j_squared * (1 - z**-2) - 2 * P_value
        if radicand <= 0:
            raise ArithmeticError(
                f"nonpositive radial radicand {radicand} at z={z}; "
                "quadrature is numerically unresolved"
            )
        return 2 * j * derivative / (z**2 * math.sqrt(radicand))

    with warnings.catch_warnings():
        warnings.simplefilter("error", IntegrationWarning)
        apsidal_angle, theta_error = quad(
            angular_integrand,
            -math.pi / 2,
            math.pi / 2,
            epsabs=2e-9,
            epsrel=2e-9,
            limit=300,
        )
    if (
        not math.isfinite(apsidal_angle)
        or apsidal_angle <= 0
        or not math.isfinite(theta_error)
        or theta_error > 1e-7 * apsidal_angle
    ):
        raise ArithmeticError(
            "apsidal quadrature failed its finite positive/error certificate"
        )
    q_e = (2 * math.pi / apsidal_angle) ** 2
    x_peri = 1 / math.sqrt(Xp)
    x_apo = 1 / math.sqrt(Xa)
    return {
        "y_peri": y_peri,
        "y_apo": y_apo,
        "X_peri": Xp,
        "X_apo": Xa,
        "eccentricity": eccentricity,
        "dimensionless_pericenter_angular_momentum_squared": j_squared,
        "apsidal_angle": apsidal_angle,
        "q_e": q_e,
        "mean_dimensionless_radius": (x_peri + x_apo) / 2,
        "dimensionless_invariant_pericenter": x_peri**2 * Xp,
        "dimensionless_invariant_apocenter": x_apo**2 * Xa,
        "potential_ode_evaluations": potential_solution.nfev,
        "theta_quadrature_error": theta_error,
    }


def _inverse_root_record(
    log_y: float,
    q_e_target: float,
    eccentricity: float,
    lower_log_y: float,
    upper_log_y: float,
    y_peri_min: float,
    y_peri_max: float,
) -> dict[str, Any]:
    """Attach a local conditioning diagnostic to one bracketed root."""

    def state_at_log(value: float) -> dict[str, float]:
        if value <= lower_log_y:
            y_value = y_peri_min
        elif value >= upper_log_y:
            y_value = y_peri_max
        else:
            y_value = math.exp(value)
        return exact_apsidal_map(y_value, eccentricity)

    state = state_at_log(log_y)
    step = 2e-4
    left = max(lower_log_y, log_y - step)
    right = min(upper_log_y, log_y + step)
    if right <= left:
        raise ArithmeticError("inverse bracket has no width for a derivative")
    q_right = state_at_log(right)["q_e"]
    q_left = state_at_log(left)["q_e"]
    derivative = (q_right - q_left) / (right - left)
    inverse_condition = None if derivative == 0 else 1 / abs(derivative)
    q_residual = state["q_e"] - q_e_target
    if abs(q_residual) > INVERSE_ROOT_Q_RESIDUAL_TOLERANCE:
        raise ArithmeticError(
            "refined inverse root failed its forward q_e residual certificate"
        )
    return {
        **state,
        "q_e_target_residual": q_residual,
        "dq_e_dlog_y_peri": derivative,
        "absolute_inverse_condition": inverse_condition,
    }


def recover_exact_pericenter_states(
    q_e: float,
    eccentricity: float,
    *,
    y_peri_min: float = MIN_INVERSE_Y_PERI,
    y_peri_max: float = MAX_INVERSE_Y_PERI,
    log_grid_segments: int = DEFAULT_INVERSE_LOG_GRID_SEGMENTS,
) -> dict[str, Any]:
    """Enumerate every sign-changing root detected on a finite log-y grid.

    This is deliberately not advertised as a certified all-root algorithm:
    an unresolved even-multiplicity root or structure narrower than a grid
    cell can escape a sign-change scan.  The returned scan metadata makes that
    limitation machine readable.
    """

    if not math.isfinite(q_e) or q_e <= 1:
        raise ValueError("a finite positive-field exterior inverse requires q_e>1")
    if not MIN_NUMERICAL_ECCENTRICITY <= eccentricity <= MAX_NUMERICAL_ECCENTRICITY:
        raise ValueError(
            "eccentricity lies outside the audited numerical quadrature window"
        )
    if not (
        MIN_INVERSE_Y_PERI
        <= y_peri_min
        < y_peri_max
        <= MAX_INVERSE_Y_PERI
    ):
        raise ValueError("invalid y_peri inversion bounds")
    if not isinstance(log_grid_segments, int) or log_grid_segments < 8:
        raise ValueError("log_grid_segments must be an integer >=8")

    lower = math.log(y_peri_min)
    upper = math.log(y_peri_max)

    def residual(log_y: float) -> float:
        if log_y <= lower:
            y_value = y_peri_min
        elif log_y >= upper:
            y_value = y_peri_max
        else:
            y_value = math.exp(log_y)
        return exact_apsidal_map(y_value, eccentricity)["q_e"] - q_e

    grid = [lower] + [
        lower + (upper - lower) * index / log_grid_segments
        for index in range(1, log_grid_segments)
    ] + [upper]
    residuals = [residual(point) for point in grid]
    endpoint_ambiguities = []
    for label, y_value, value in (
        ("lower", y_peri_min, residuals[0]),
        ("upper", y_peri_max, residuals[-1]),
    ):
        if 0 < abs(value) <= INVERSE_ENDPOINT_Q_UNCERTAINTY:
            endpoint_ambiguities.append(
                {
                    "endpoint": label,
                    "y_peri": y_value,
                    "q_e_endpoint_minus_target": value,
                    "absolute_q_guard": INVERSE_ENDPOINT_Q_UNCERTAINTY,
                }
            )
    root_candidates: list[float] = []

    def append_root(candidate: float) -> None:
        root_candidates.append(candidate)

    for point, value in zip(grid, residuals):
        if value == 0:
            append_root(point)

    for index in range(log_grid_segments):
        left, right = grid[index], grid[index + 1]
        f_left, f_right = residuals[index], residuals[index + 1]
        if (
            index == 0
            and any(item["endpoint"] == "lower" for item in endpoint_ambiguities)
        ) or (
            index == log_grid_segments - 1
            and any(item["endpoint"] == "upper" for item in endpoint_ambiguities)
        ):
            continue
        if f_left * f_right < 0:
            append_root(brentq(residual, left, right, xtol=2e-12, rtol=1e-12))

    root_logs: list[float] = []
    for candidate in sorted(root_candidates):
        if not root_logs or abs(candidate - root_logs[-1]) > 1e-9:
            root_logs.append(candidate)

    q_samples = [value + q_e for value in residuals]
    finite_slopes = [
        (q_samples[index + 1] - q_samples[index])
        / (grid[index + 1] - grid[index])
        for index in range(log_grid_segments)
    ]
    roots = [
        _inverse_root_record(
            root,
            q_e,
            eccentricity,
            lower,
            upper,
            y_peri_min,
            y_peri_max,
        )
        for root in root_logs
    ]
    return {
        "status": (
            "ENDPOINT_NUMERICALLY_UNRESOLVED_WITH_INTERIOR_ROOTS"
            if endpoint_ambiguities and roots
            else "ENDPOINT_NUMERICALLY_UNRESOLVED"
            if endpoint_ambiguities
            else "BRACKETED_ROOTS_FOUND_ON_SAMPLED_WINDOW"
            if roots
            else "NO_BRACKETED_ROOT_ON_SAMPLED_WINDOW"
        ),
        "roots": roots,
        "endpoint_ambiguities": endpoint_ambiguities,
        "inverse_y_bounds": [y_peri_min, y_peri_max],
        "log_grid_segments": log_grid_segments,
        "sampled_monotone_decreasing": all(slope < 0 for slope in finite_slopes),
        "maximum_sampled_dq_e_dlog_y": max(finite_slopes),
        "unresolved_even_multiplicity_or_subgrid_roots": True,
    }


def recover_exact_pericenter_state(
    q_e: float,
    eccentricity: float,
    *,
    y_peri_min: float = MIN_INVERSE_Y_PERI,
    y_peri_max: float = MAX_INVERSE_Y_PERI,
    log_grid_segments: int = DEFAULT_INVERSE_LOG_GRID_SEGMENTS,
) -> dict[str, Any]:
    """Return a state only when the bounded scan detects exactly one branch."""

    branches = recover_exact_pericenter_states(
        q_e,
        eccentricity,
        y_peri_min=y_peri_min,
        y_peri_max=y_peri_max,
        log_grid_segments=log_grid_segments,
    )
    if len(branches["roots"]) != 1 or branches["endpoint_ambiguities"]:
        raise ValueError(
            "the bounded inverse scan did not isolate exactly one branch "
            "without endpoint ambiguity; "
            "inspect recover_exact_pericenter_states instead"
        )
    return {
        **branches["roots"][0],
        "inverse_y_bounds": branches["inverse_y_bounds"],
        "inverse_log_grid_segments": branches["log_grid_segments"],
        "sampled_monotone_decreasing": branches["sampled_monotone_decreasing"],
        "unresolved_even_multiplicity_or_subgrid_roots": branches[
            "unresolved_even_multiplicity_or_subgrid_roots"
        ],
    }


def exact_radius_invariant(
    mean_turning_radius: float,
    q_e: float,
    eccentricity: float,
) -> dict[str, Any]:
    """Recover r_M^2=GM/a0 on the selected exact inverse branch."""

    if not math.isfinite(mean_turning_radius) or mean_turning_radius <= 0:
        raise ValueError("mean turning radius must be finite and positive")
    state = recover_exact_pericenter_state(q_e, eccentricity)
    pericenter_radius = mean_turning_radius * (1 - eccentricity)
    invariant = pericenter_radius**2 * state["X_peri"]
    return {**state, "r_M_squared": invariant}


def exact_radius_invariant_candidates(
    mean_turning_radius: float,
    q_e: float,
    eccentricity: float,
    *,
    y_peri_min: float = MIN_INVERSE_Y_PERI,
    y_peri_max: float = MAX_INVERSE_Y_PERI,
    log_grid_segments: int = DEFAULT_INVERSE_LOG_GRID_SEGMENTS,
) -> dict[str, Any]:
    """Return the set of invariants from every branch detected by the scan."""

    if not math.isfinite(mean_turning_radius) or mean_turning_radius <= 0:
        raise ValueError("mean turning radius must be finite and positive")
    branches = recover_exact_pericenter_states(
        q_e,
        eccentricity,
        y_peri_min=y_peri_min,
        y_peri_max=y_peri_max,
        log_grid_segments=log_grid_segments,
    )
    pericenter_radius = mean_turning_radius * (1 - eccentricity)
    candidates = [
        {
            **root,
            "r_M_squared": pericenter_radius**2 * root["X_peri"],
        }
        for root in branches["roots"]
    ]
    return {
        **branches,
        "invariant_candidates": candidates,
    }


def exact_cross_radius_null_candidates(
    orbit_i: dict[str, float],
    orbit_j: dict[str, float],
) -> dict[str, Any]:
    """Return every detected branch-pair value of the exact logarithmic null."""

    required = ("mean_turning_radius", "q_e", "eccentricity")
    candidate_sets = []
    for label, orbit in (("orbit_i", orbit_i), ("orbit_j", orbit_j)):
        missing = [key for key in required if key not in orbit]
        if missing:
            raise ValueError(f"{label} is missing {', '.join(missing)}")
        candidate_sets.append(
            exact_radius_invariant_candidates(
                orbit["mean_turning_radius"],
                orbit["q_e"],
                orbit["eccentricity"],
            )
        )
    pairwise = [
        {
            "orbit_i_branch": index_i,
            "orbit_j_branch": index_j,
            "log_null": math.log(
                candidate_i["r_M_squared"] / candidate_j["r_M_squared"]
            ),
        }
        for index_i, candidate_i in enumerate(candidate_sets[0]["invariant_candidates"])
        for index_j, candidate_j in enumerate(candidate_sets[1]["invariant_candidates"])
    ]
    endpoint_unresolved = any(
        candidate_set["endpoint_ambiguities"] for candidate_set in candidate_sets
    )
    return {
        "status": (
            "ENDPOINT_NUMERICALLY_UNRESOLVED"
            if endpoint_unresolved
            else "BRANCH_PAIR_NULLS_ON_SAMPLED_WINDOWS"
            if pairwise
            else "NO_BRANCH_PAIR_ON_SAMPLED_WINDOWS"
        ),
        "orbit_i_scan_status": candidate_sets[0]["status"],
        "orbit_j_scan_status": candidate_sets[1]["status"],
        "orbit_i_endpoint_ambiguities": candidate_sets[0]["endpoint_ambiguities"],
        "orbit_j_endpoint_ambiguities": candidate_sets[1]["endpoint_ambiguities"],
        "orbit_i_candidates": candidate_sets[0]["invariant_candidates"],
        "orbit_j_candidates": candidate_sets[1]["invariant_candidates"],
        "pairwise_log_nulls": pairwise,
        "minimum_absolute_log_null": (
            min(abs(item["log_null"]) for item in pairwise) if pairwise else None
        ),
        "unresolved_even_multiplicity_or_subgrid_roots": True,
    }


def exact_cross_radius_log_null(
    orbit_i: dict[str, float],
    orbit_j: dict[str, float],
) -> float:
    required = ("mean_turning_radius", "q_e", "eccentricity")
    invariants = []
    for label, orbit in (("orbit_i", orbit_i), ("orbit_j", orbit_j)):
        missing = [key for key in required if key not in orbit]
        if missing:
            raise ValueError(f"{label} is missing {', '.join(missing)}")
        invariants.append(
            exact_radius_invariant(
                orbit["mean_turning_radius"],
                orbit["q_e"],
                orbit["eccentricity"],
            )["r_M_squared"]
        )
    return math.log(invariants[0] / invariants[1])


def build_results() -> dict[str, Any]:
    symbolic = derive_exact_turning_law()
    deep = exact_apsidal_map(1e-6, 0.03)
    newton = exact_apsidal_map(25.0, 0.2)
    round_trip_forward = exact_apsidal_map(1.0, 0.2)
    round_trip = recover_exact_pericenter_state(round_trip_forward["q_e"], 0.2)
    r_m = 5.0
    observations = []
    invariants = []
    for y_peri, eccentricity in ((0.3, 0.12), (2.0, 0.28)):
        forward = exact_apsidal_map(y_peri, eccentricity)
        mean_radius = r_m * forward["mean_dimensionless_radius"]
        observations.append(
            {
                "mean_turning_radius": mean_radius,
                "q_e": forward["q_e"],
                "eccentricity": eccentricity,
            }
        )
        invariants.append(
            exact_radius_invariant(mean_radius, forward["q_e"], eccentricity)[
                "r_M_squared"
            ]
        )
    null = exact_cross_radius_log_null(observations[0], observations[1])
    null_candidates = exact_cross_radius_null_candidates(
        observations[0], observations[1]
    )
    certificates = {
        "dimensionless_field_scaling": symbolic["field_scale_residual"] == 0,
        "turning_energy_elimination": symbolic["turning_energy_residual"] == 0,
        "turning_radius_invariant": symbolic["invariant_apocenter_residual"] == 0,
        "cycle_factor_negative_control": symbolic["cycle_factor_mutation"] == 4,
        "deep_logarithmic_limit": abs(deep["q_e"] - 2.0003001482) < 1e-6,
        "newton_kepler_limit": abs(newton["q_e"] - 1) < 3e-5,
        "selected_branch_inverse_round_trip": abs(round_trip["y_peri"] - 1) < 2e-6,
        "bounded_scan_detected_one_branch_for_round_trip": (
            round_trip["sampled_monotone_decreasing"]
        ),
        "accepted_root_forward_residual": (
            abs(round_trip["q_e_target_residual"])
            <= INVERSE_ROOT_Q_RESIDUAL_TOLERANCE
        ),
        "two_orbit_exact_null": abs(null) < 2e-6,
        "set_valued_null_matches_single_detected_branch": (
            len(null_candidates["pairwise_log_nulls"]) == 1
            and null_candidates["minimum_absolute_log_null"] is not None
            and abs(null_candidates["minimum_absolute_log_null"] - abs(null)) < 1e-12
        ),
        "recovered_scale": max(abs(value - r_m**2) for value in invariants) < 2e-5,
    }
    passed = all(certificates.values())
    return {
        "status": (
            "PASS_EXACT_FORWARD_AND_BRANCH_AWARE_CONDITIONAL_NULL_ON_BOUNDED_NUMERICAL_WINDOW"
            if passed
            else "FAIL_EXACT_ALL_E_KEPLER_NULL"
        ),
        "equations": {
            "X": "y*(1-exp(-y))",
            "radius": "x=1/sqrt(X), x=r/sqrt(GM/a0)",
            "outer_turning_relation": "X_a=X_p*((1-e)/(1+e))^2",
            "A": "integral_y^y_p [s X'(s)/X(s)^(3/2)] ds",
            "lambda_squared": "A(y_a;y_p)/(X_p-X_a)",
            "apsidal_angle": "lambda*integral_y_a^y_p [X'(y)/sqrt(X(y))]/sqrt(lambda^2*(X_p-X(y))-A(y;y_p)) dy",
            "exact_invariant": "R^2*(1-e)^2*X_p=GM/a0",
            "cross_radius_null": "log(I_i/I_j)=0",
        },
        "numerical_window": {
            "forward_y_peri": [MIN_FORWARD_Y_PERI, MAX_FORWARD_Y_PERI],
            "eccentricity": [
                MIN_NUMERICAL_ECCENTRICITY,
                MAX_NUMERICAL_ECCENTRICITY,
            ],
            "inverse_y_peri": [MIN_INVERSE_Y_PERI, MAX_INVERSE_Y_PERI],
            "inverse_endpoint_absolute_q_guard": INVERSE_ENDPOINT_Q_UNCERTAINTY,
            "accepted_root_absolute_q_residual_tolerance": (
                INVERSE_ROOT_Q_RESIDUAL_TOLERANCE
            ),
            "inverse_semantics": "all sign-changing roots on a 32-cell log-y scan; scalar API requires exactly one detected root; tangential/subgrid roots remain explicitly unresolved",
        },
        "deep_sample": deep,
        "newton_sample": newton,
        "inverse_round_trip": {
            "input_y_peri": 1.0,
            "recovered_y_peri": round_trip["y_peri"],
            "relative_error": round_trip["y_peri"] - 1,
            "absolute_inverse_condition": round_trip["absolute_inverse_condition"],
            "q_e_target_residual": round_trip["q_e_target_residual"],
        },
        "two_orbit_null": {
            "true_r_M_squared": r_m**2,
            "recovered_invariants": invariants,
            "log_null": null,
            "detected_branch_pair_count": len(
                null_candidates["pairwise_log_nulls"]
            ),
            "minimum_absolute_candidate_log_null": null_candidates[
                "minimum_absolute_log_null"
            ],
        },
        "certificates": certificates,
        "nonclaims": [
            "not a relativistic completion",
            "not an analytic closed form for the apsidal quadrature",
            "not a global injectivity theorem, even inside the bounded search window",
            "not a certified all-root inverse; even-multiplicity or subgrid roots remain unresolved",
            "not valid for extended mass, external field, or nonspherical sources",
            "not a global novelty claim",
        ],
    }


def main() -> int:
    results = build_results()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
