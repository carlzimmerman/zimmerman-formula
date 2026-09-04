#!/usr/bin/env python3
"""Finite-eccentricity orbit laws from the exponential-MOND exterior flux.

This is a bounded weak-static/test-particle computation.  It derives exact
turning-point quadratures, the deep logarithmic similarity law, and a
single-test-particle virial invariant.  It is not a relativistic closure,
galaxy theorem, or novelty certificate.
"""

from __future__ import annotations

import json
import math
import sys
from typing import Callable
import warnings

import mpmath as mp
import numpy as np
from scipy.integrate import IntegrationWarning, quad, solve_ivp
from scipy.optimize import brentq
import sympy as sp


def derive_symbolic_law() -> dict[str, object]:
    """Derive the scales, potential, turning data, and limiting constants."""

    G, M, a0 = sp.symbols("G M_b a_0", positive=True)
    r, g = sp.symbols("r g", positive=True)
    x, y = sp.symbols("x y", positive=True)
    mu = 1 - sp.exp(-y)
    r_m = sp.sqrt(G * M / a0)
    v_inf = (G * M * a0) ** sp.Rational(1, 4)
    t_m = sp.factor(r_m / v_inf)
    expected_t_m = (G * M / a0**3) ** sp.Rational(1, 4)

    physical_flux = (1 - sp.exp(-g / a0)) * g - G * M / r**2
    reduced_flux = sp.factor(
        physical_flux.subs({g: a0 * y, r: r_m * x}, simultaneous=True)
        / a0
    )
    dimensionless_flux = y * mu - x ** -2

    f = y * mu
    constitutive_slope = sp.diff(f, y)
    expected_constitutive_slope = mu + y * sp.exp(-y)
    # Along x^2 f(y)=1, H=x^3 y has
    # H'/(x^2 y)=3-2*mu/f'.  Its displayed numerator is strictly positive
    # for y>0, proving H is monotone and the generated effective radial
    # potential has a single minimum between its two turning points.
    h_slope_reduced = sp.factor(3 - 2 * mu / constitutive_slope)
    expected_h_slope_reduced = (mu + 3 * y * sp.exp(-y)) / constitutive_slope
    x_of_y = f ** sp.Rational(-1, 2)
    dx_dy = sp.diff(x_of_y, y)
    dW_dy = sp.factor(y * dx_dy)
    # W(y)=y*x(y)-integral^y x(u)du, so this differentiated expression
    # independently checks the parametric primitive without evaluating it.
    parametric_derivative = sp.diff(y * x_of_y, y) - x_of_y

    x_p, x_a = sp.symbols("x_p x_a", positive=True)
    W_p, W_a = sp.symbols("W_p W_a", real=True)
    energy = sp.symbols("E", real=True)
    lambda_squared = sp.factor(
        2 * (W_a - W_p) / (x_p ** -2 - x_a ** -2)
    )
    turning_energy = sp.factor(W_p + lambda_squared / (2 * x_p**2))
    peri_residual = sp.simplify(
        turning_energy - W_p - lambda_squared / (2 * x_p**2)
    )
    apo_residual = sp.simplify(
        turning_energy - W_a - lambda_squared / (2 * x_a**2)
    )

    j2 = sp.symbols("j_c_squared", positive=True)
    W_newton = -1 / x
    newton_effective_potential = W_newton + j2 / (2 * x**2)
    newton_circular_j2 = sp.solve(
        sp.diff(newton_effective_potential, x), j2
    )[0]
    newton_circular_condition_residual = sp.simplify(
        sp.diff(newton_effective_potential, x).subs(j2, newton_circular_j2)
    )
    newton_angular_frequency = sp.simplify(sp.sqrt(newton_circular_j2) / x**2)
    newton_circular_period = sp.simplify(2 * sp.pi / newton_angular_frequency)
    newton_kepler_constant = sp.simplify(newton_circular_period**2 / x**3)

    W_deep = sp.log(x)
    deep_effective_potential = W_deep + j2 / (2 * x**2)
    circular_j2 = sp.solve(sp.diff(deep_effective_potential, x), j2)[0]
    deep_circular_condition_residual = sp.simplify(
        sp.diff(deep_effective_potential, x).subs(j2, circular_j2)
    )
    deep_epicycle_frequency_squared = sp.simplify(
        sp.diff(deep_effective_potential, x, 2).subs(j2, circular_j2)
    )
    deep_radial_period_scaled = sp.simplify(
        2 * sp.pi / (x * sp.sqrt(deep_epicycle_frequency_squared))
    )
    deep_angular_frequency = sp.simplify(sp.sqrt(circular_j2) / x**2)
    deep_near_circular_apsidal_angle = sp.simplify(
        deep_angular_frequency * 2 * sp.pi
        / sp.sqrt(deep_epicycle_frequency_squared)
    )
    r_dot_grad = sp.factor(x * sp.diff(W_deep, x))
    deep_mean_speed_squared = r_dot_grad  # 2<K>=<r.grad W>, <v^2>=2<K>
    v_inf_squared = sp.sqrt(G * M * a0)
    test_particle_virial_residual = sp.simplify(
        (deep_mean_speed_squared * v_inf_squared) ** 2 - G * M * a0
    )

    # A tempting but incorrect finite-eccentricity shortcut is to substitute
    # the arithmetic mean turning radius R and radial period T_r directly into
    # the circular deep-MOND law, T^4=16*pi^4*R^4/(G*M*a0).  The exact law below
    # has T_r^4=F(e)^4*R^4/(G*M*a0), so the shortcut/exact residual ratio is
    # 16*pi^4/F(e)^4.  Derive its two analytic endpoint values rather than
    # baking the expected numbers into the audit.
    F_e = sp.symbols("F_e", positive=True)
    naive_deep_ratio = 16 * sp.pi**4 / F_e**4
    F_near_circular = deep_radial_period_scaled
    radial_limit = derive_radial_deep_limit()
    F_radial_limit = radial_limit["period_scaled"]
    naive_deep_ratio_near_circular = sp.simplify(
        naive_deep_ratio.subs(F_e, F_near_circular)
    )
    naive_deep_ratio_radial_limit = sp.simplify(
        naive_deep_ratio.subs(F_e, F_radial_limit)
    )

    return {
        "symbols": {
            "G": G,
            "M": M,
            "a0": a0,
            "x": x,
            "y": y,
            "energy": energy,
        },
        "r_M": r_m,
        "v_infinity": v_inf,
        "t_M": t_m,
        "time_scale_residual": sp.powsimp(t_m - expected_t_m, force=True),
        "physical_flux": physical_flux,
        "dimensionless_flux": dimensionless_flux,
        "flux_residual": sp.simplify(reduced_flux - dimensionless_flux),
        "constitutive_slope": constitutive_slope,
        "constitutive_slope_residual": sp.simplify(
            constitutive_slope - expected_constitutive_slope
        ),
        "full_force_h_slope_reduced": h_slope_reduced,
        "full_force_h_slope_positive_numerator": mu + 3 * y * sp.exp(-y),
        "full_force_h_slope_residual": sp.simplify(
            h_slope_reduced - expected_h_slope_reduced
        ),
        "x_of_y": x_of_y,
        "dW_dy": dW_dy,
        "potential_chain_rule_residual": sp.simplify(dW_dy / dx_dy - y),
        "potential_parametric_derivative_residual": sp.simplify(
            parametric_derivative - dW_dy
        ),
        "deep_force_residual": sp.simplify(
            sp.limit(x_of_y * y, y, 0, dir="+") - 1
        ),
        "newton_force_residual": sp.simplify(
            sp.limit(x_of_y**2 * y, y, sp.oo) - 1
        ),
        "turning_lambda_squared": lambda_squared,
        "turning_energy": turning_energy,
        "turning_point_pericenter_residual": peri_residual,
        "turning_point_apocenter_residual": apo_residual,
        "newton_circular_condition_residual": newton_circular_condition_residual,
        "newton_kepler_constant": newton_kepler_constant,
        "deep_circular_condition_residual": deep_circular_condition_residual,
        "deep_epicycle_frequency_squared": deep_epicycle_frequency_squared,
        "deep_epicycle_frequency_squared_residual": sp.simplify(
            deep_epicycle_frequency_squared - 2 / x**2
        ),
        "deep_circular_radial_period_scaled": deep_radial_period_scaled,
        "deep_radial_period_scaled": radial_limit["period_scaled"],
        "deep_near_circular_apsidal_angle": deep_near_circular_apsidal_angle,
        "deep_radial_apsidal_angle": radial_limit["apsidal_angle_limit"],
        "deep_r_dot_grad_potential_residual": sp.simplify(r_dot_grad - 1),
        "deep_mean_speed_squared": deep_mean_speed_squared,
        "test_particle_virial_residual": test_particle_virial_residual,
        "naive_deep_ratio": naive_deep_ratio,
        "naive_deep_ratio_near_circular": naive_deep_ratio_near_circular,
        "naive_deep_ratio_radial_limit": naive_deep_ratio_radial_limit,
    }


def mu_exponential(y: float) -> float:
    return -math.expm1(-y)


def solve_dimensionless_acceleration(x: float) -> float:
    """Solve y(1-exp(-y))=x^-2 on its unique y>0 branch."""

    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("x must be positive and finite")
    source = 1.0 / x**2

    def residual(y: float) -> float:
        return y * mu_exponential(y) - source

    upper = source + math.sqrt(source) + 1.0
    return brentq(
        residual,
        0.0,
        upper,
        xtol=5.0e-15,
        rtol=4.0 * np.finfo(float).eps,
        maxiter=100,
    )


def _validate_eccentricity(eccentricity: float) -> None:
    if (
        not math.isfinite(eccentricity)
        or eccentricity <= 0.0
        or eccentricity >= 1.0
    ):
        raise ValueError("eccentricity must lie strictly between zero and one")


def _checked_mp_real(value: mp.mpf | mp.mpc, label: str, digits: int) -> mp.mpf:
    real_part = mp.re(value)
    imaginary_part = abs(mp.im(value))
    tolerance = mp.power(10, -digits // 3) * max(1, abs(real_part))
    if not mp.isfinite(real_part) or not mp.isfinite(imaginary_part):
        raise RuntimeError(f"nonfinite multiprecision {label}")
    if imaginary_part > tolerance:
        raise RuntimeError(
            f"multiprecision {label} has unresolved imaginary part "
            f"{imaginary_part} > {tolerance}"
        )
    return real_part


def _evaluate_deep_near_radial_mp(
    eccentricity: float, digits: int
) -> dict[str, str]:
    """Tanh-sinh quadrature for the sharp e->1 logarithmic boundary layer."""

    with mp.workdps(digits):
        e = mp.mpf(str(eccentricity))
        u_p, u_a = 1 - e, 1 + e
        j_squared = (1 - e**2) ** 2 * mp.atanh(e) / e
        j = mp.sqrt(j_squared)
        energy = mp.log(u_a) + j_squared / (2 * u_a**2)

        def radial_function(u: mp.mpf) -> mp.mpf:
            return 2 * (energy - mp.log(u)) - j_squared / u**2

        midpoint = (u_p + u_a) / 2

        def integrate(numerator: Callable[[mp.mpf, mp.mpf], mp.mpf], label: str) -> mp.mpf:
            raw = mp.quad(
                lambda u: numerator(u, radial_function(u))
                / mp.sqrt(radial_function(u)),
                [u_p, midpoint, u_a],
            )
            return _checked_mp_real(raw, label, digits)

        one_way_time = integrate(lambda _u, _q: mp.mpf(1), "radial time")
        one_way_angle = integrate(lambda u, _q: j / u**2, "apsidal angle")
        one_way_v2 = integrate(
            lambda u, q_value: q_value + j_squared / u**2,
            "virial numerator",
        )
        turning_residual = max(
            abs(radial_function(u_p)), abs(radial_function(u_a))
        )
        return {
            "j_squared": mp.nstr(j_squared, digits),
            "energy": mp.nstr(energy, digits),
            "one_way_time": mp.nstr(one_way_time, digits),
            "one_way_angle": mp.nstr(one_way_angle, digits),
            "one_way_v2": mp.nstr(one_way_v2, digits),
            "turning_residual": mp.nstr(turning_residual, digits),
        }


def _endpoint_regularized_integral(
    low: float,
    high: float,
    radicand: Callable[[float], float],
    radicand_prime: Callable[[float], float],
    numerator: Callable[[float, float], float],
    *,
    epsabs: float = 2.0e-11,
    epsrel: float = 2.0e-11,
) -> float:
    """Integrate numerator/sqrt(F) between two simple turning points."""

    width = high - low
    if width <= 0.0:
        raise ValueError("turning points must be ordered")
    low_slope = radicand_prime(low)
    high_slope = radicand_prime(high)
    if not math.isfinite(low_slope) or low_slope <= 0.0:
        raise RuntimeError("lower turning point is not a simple positive root")
    if not math.isfinite(high_slope) or high_slope >= 0.0:
        raise RuntimeError("upper turning point is not a simple negative root")
    low_limit = math.sqrt(width / low_slope)
    high_limit = math.sqrt(width / (-high_slope))

    def transformed(theta: float) -> float:
        if theta < 1.0e-5:
            return numerator(low, 0.0) * low_limit
        if math.pi - theta < 1.0e-5:
            return numerator(high, 0.0) * high_limit
        coordinate = (low + high) / 2.0 - width * math.cos(theta) / 2.0
        jacobian = width * math.sin(theta) / 2.0
        value = radicand(coordinate)
        if not math.isfinite(value) or value <= 0.0:
            raise RuntimeError(f"nonpositive radial kinetic function: {value}")
        return numerator(coordinate, value) * jacobian / math.sqrt(value)

    with warnings.catch_warnings():
        warnings.simplefilter("error", IntegrationWarning)
        try:
            integral, error = quad(
                transformed,
                0.0,
                math.pi,
                epsabs=epsabs,
                epsrel=epsrel,
                limit=300,
            )
        except IntegrationWarning as warning:
            raise RuntimeError(f"quadrature did not converge: {warning}") from warning
    if not math.isfinite(integral) or not math.isfinite(error):
        raise RuntimeError("quadrature returned a nonfinite value or error estimate")
    allowed_error = 10.0 * max(epsabs, epsrel * abs(integral))
    if error > allowed_error:
        raise RuntimeError(
            f"quadrature error estimate {error} exceeds {allowed_error}"
        )
    return float(integral)


def deep_log_orbit(eccentricity: float) -> dict[str, float | bool]:
    """Evaluate the exact deep-MOND logarithmic-potential quadratures.

    Radii are u_p=1-e and u_a=1+e in units of their arithmetic mean R.
    Therefore ``radial_period_scaled`` means T_r*v_inf/R.
    """

    _validate_eccentricity(eccentricity)
    e = eccentricity
    u_p, u_a = 1.0 - e, 1.0 + e
    precision_crosscheck_error = 0.0
    if e > 9.99e-1:
        base_digits = max(60, int(-math.log10(1.0 - e)) * 4 + 40)
        lower_precision = _evaluate_deep_near_radial_mp(e, base_digits)
        higher_precision = _evaluate_deep_near_radial_mp(e, base_digits + 20)
        with mp.workdps(base_digits + 20):
            precision_crosscheck_error = float(
                max(
                    abs(
                        mp.mpf(higher_precision[key])
                        / mp.mpf(lower_precision[key])
                        - 1
                    )
                    for key in ("one_way_time", "one_way_angle", "one_way_v2")
                )
            )
        j_squared = float(higher_precision["j_squared"])
        j = math.sqrt(j_squared)
        energy = float(higher_precision["energy"])
        one_way_time = float(higher_precision["one_way_time"])
        one_way_angle = float(higher_precision["one_way_angle"])
        one_way_v2_time_integral = float(higher_precision["one_way_v2"])
        turning_residual_max = float(higher_precision["turning_residual"])
    elif e < 2.0e-2:
        # Q_e is O(e^2), while its two defining terms are O(e).  Direct
        # double-precision subtraction therefore becomes singular as e->0.
        # Evaluate q=Q/e^2 with adaptive decimal precision and integrate in
        # s=(u-1)/e on the fixed interval [-1,1].
        decimal_places = max(50, int(-math.log10(e)) * 4 + 20)
        with mp.workdps(decimal_places):
            e_mp = mp.mpf(str(e))
            j_squared_mp = (1 - e_mp**2) ** 2 * mp.atanh(e_mp) / e_mp
            j_mp = mp.sqrt(j_squared_mp)
            u_a_mp = 1 + e_mp
            energy_mp = mp.log(u_a_mp) + j_squared_mp / (2 * u_a_mp**2)

            def scaled_radial_function(s: float) -> float:
                s_mp = mp.mpf(str(s))
                u_mp = 1 + e_mp * s_mp
                value = (
                    2 * mp.log(u_a_mp / u_mp)
                    + j_squared_mp * (u_a_mp**-2 - u_mp**-2)
                ) / e_mp**2
                return float(value)

            def scaled_radial_prime(s: float) -> float:
                s_mp = mp.mpf(str(s))
                u_mp = 1 + e_mp * s_mp
                value = (-2 / u_mp + 2 * j_squared_mp / u_mp**3) / e_mp
                return float(value)

            j_squared = float(j_squared_mp)
            j = float(j_mp)
            energy = float(energy_mp)
            one_way_time = _endpoint_regularized_integral(
                -1.0,
                1.0,
                scaled_radial_function,
                scaled_radial_prime,
                lambda _s, _q: 1.0,
            )
            one_way_angle = _endpoint_regularized_integral(
                -1.0,
                1.0,
                scaled_radial_function,
                scaled_radial_prime,
                lambda s, _q: j / (1.0 + e * s) ** 2,
            )
            one_way_v2_time_integral = _endpoint_regularized_integral(
                -1.0,
                1.0,
                scaled_radial_function,
                scaled_radial_prime,
                lambda s, q_value: (
                    e**2 * q_value + j_squared / (1.0 + e * s) ** 2
                ),
            )
            turning_residual_max = float(
                e_mp**2
                * max(
                    abs(scaled_radial_function(-1.0)),
                    abs(scaled_radial_function(1.0)),
                )
            )
    else:
        log_ratio = 2.0 * math.atanh(e)
        j_squared = (1.0 - e**2) ** 2 * log_ratio / (2.0 * e)
        j = math.sqrt(j_squared)
        energy = math.log(u_a) + j_squared / (2.0 * u_a**2)

        def radial_function(u: float) -> float:
            return 2.0 * math.log(u_a / u) + j_squared * (
                u_a**-2 - u**-2
            )

        def radial_prime(u: float) -> float:
            return -2.0 / u + 2.0 * j_squared / u**3

        one_way_time = _endpoint_regularized_integral(
            u_p, u_a, radial_function, radial_prime, lambda _u, _f: 1.0
        )
        one_way_angle = _endpoint_regularized_integral(
            u_p,
            u_a,
            radial_function,
            radial_prime,
            lambda u, _f: j / u**2,
        )
        one_way_v2_time_integral = _endpoint_regularized_integral(
            u_p,
            u_a,
            radial_function,
            radial_prime,
            lambda u, f_value: f_value + j_squared / u**2,
        )
        turning_residual_max = max(
            abs(radial_function(u_p)), abs(radial_function(u_a))
        )
    radial_period_scaled = 2.0 * one_way_time
    apsidal_angle = 2.0 * one_way_angle
    mean_speed_squared = one_way_v2_time_integral / one_way_time
    epicycle_angle = math.sqrt(2.0) * math.pi
    mutation_error = abs(apsidal_angle / epicycle_angle - 1.0)
    mutation_tolerance = 1.0e-4
    return {
        "eccentricity": e,
        "u_pericenter": u_p,
        "u_apocenter": u_a,
        "j_squared": j_squared,
        "energy": energy,
        "radial_period_scaled": radial_period_scaled,
        "apsidal_angle": apsidal_angle,
        "precession_degrees": math.degrees(apsidal_angle - 2.0 * math.pi),
        "mean_speed_squared": mean_speed_squared,
        "turning_residual_max": turning_residual_max,
        "epicycle_mutation_error": mutation_error,
        "epicycle_mutation_survives": mutation_error <= mutation_tolerance,
        "precision_crosscheck_error": precision_crosscheck_error,
    }


def validate_deep_log_orbit_ode(
    eccentricity: float,
) -> dict[str, float | int]:
    """Measure the log-force period/angle from nonlinear orbit events."""

    quadrature = deep_log_orbit(eccentricity)
    u_p = float(quadrature["u_pericenter"])
    u_a = float(quadrature["u_apocenter"])
    j_squared = float(quadrature["j_squared"])
    angular_momentum = math.sqrt(j_squared)
    predicted_period = float(quadrature["radial_period_scaled"])
    predicted_angle = float(quadrature["apsidal_angle"])

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        radius, radial_velocity, _angle = state
        return (
            radial_velocity,
            j_squared / radius**3 - 1.0 / radius,
            angular_momentum / radius**2,
        )

    def pericenter(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    def apocenter(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    pericenter.direction = 1.0
    pericenter.terminal = False
    apocenter.direction = -1.0
    apocenter.terminal = False
    solution = solve_ivp(
        equations,
        (0.0, 1.25 * predicted_period),
        (u_p, 0.0, 0.0),
        method="RK45",
        events=(pericenter, apocenter),
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=predicted_period / 500.0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    peri_times = solution.t_events[0]
    peri_states = solution.y_events[0]
    keep = peri_times > predicted_period * 1.0e-7
    peri_times = peri_times[keep]
    peri_states = peri_states[keep]
    apo_states = solution.y_events[1]
    if len(peri_times) < 1 or len(apo_states) < 1:
        raise RuntimeError("required deep-log orbit events were not found")
    measured_period = float(peri_times[0])
    measured_angle = float(peri_states[0, 2])
    measured_apocenter = float(apo_states[0, 0])
    return {
        "eccentricity": eccentricity,
        "predicted_period": predicted_period,
        "measured_period": measured_period,
        "period_relative_error": abs(measured_period / predicted_period - 1.0),
        "predicted_angle": predicted_angle,
        "measured_angle": measured_angle,
        "angle_relative_error": abs(measured_angle / predicted_angle - 1.0),
        "target_apocenter": u_a,
        "measured_apocenter": measured_apocenter,
        "apocenter_relative_error": abs(measured_apocenter / u_a - 1.0),
        "force_evaluations": int(solution.nfev),
    }


def derive_radial_deep_limit() -> dict[str, sp.Expr]:
    """Evaluate the e->1 radial-period limit as a Gamma integral.

    This is the formal scale-free log-potential limit of noncollision orbits
    at fixed R; it is not a prescription through the singular center.  For the
    full exponential branch it requires a joint limit xi=R/r_M -> infinity,
    e->1 with xi*(1-e)->infinity and the pericenter outside the source.
    """

    z, s, delta = sp.symbols("z s delta", positive=True)
    eccentricity = 1 - delta
    logarithmic_scale = sp.log((2 - delta) / delta)
    j_squared = (
        (1 - eccentricity**2) ** 2
        * logarithmic_scale
        / (2 * eccentricity)
    )
    energy = sp.log(1 + eccentricity) + j_squared / (
        2 * (1 + eccentricity) ** 2
    )
    boundary_radius = delta * s
    radial_function = (
        2 * (energy - sp.log(boundary_radius))
        - j_squared / boundary_radius**2
    )
    j_scaling = sp.limit(
        j_squared / (2 * delta**2 * logarithmic_scale),
        delta,
        0,
        dir="+",
    )
    energy_limit = sp.limit(energy, delta, 0, dir="+")
    radial_function_scaling = sp.simplify(
        sp.limit(
            radial_function / (2 * logarithmic_scale),
            delta,
            0,
            dir="+",
        )
    )
    angular_prefactor = sp.limit(
        sp.sqrt(j_squared)
        / (delta * sp.sqrt(2 * logarithmic_scale)),
        delta,
        0,
        dir="+",
    )
    gamma_integral = sp.integrate(sp.exp(-z) / sp.sqrt(2 * z), (z, 0, sp.oo))
    expected_one_way_over_apocenter = sp.sqrt(sp.pi / 2)
    # r_a -> 2R, and a radial period is twice the one-way center-to-apocenter time.
    period_over_mean_radius = sp.simplify(4 * gamma_integral)
    # With delta=1-e, L=log(2/delta), and u=delta*s, the half-angle
    # integrand tends to 1/[s^2 sqrt(1-s^-2)].  Its integral gives the
    # noncollision e->1^- limit rather than inserting pi by inspection.
    half_angle_integral = sp.integrate(
        1 / (s**2 * sp.sqrt(1 - s**-2)), (s, 1, sp.oo)
    )
    apsidal_angle_limit = sp.simplify(2 * half_angle_integral)
    return {
        "j_scaling_residual": sp.simplify(j_scaling - 1),
        "energy_limit_residual": sp.simplify(energy_limit - sp.log(2)),
        "radial_function_scaling_residual": sp.simplify(
            radial_function_scaling - (1 - s**-2)
        ),
        "angular_prefactor_residual": sp.simplify(angular_prefactor - 1),
        "one_way_over_apocenter": gamma_integral,
        "gamma_integral_residual": sp.simplify(
            gamma_integral - expected_one_way_over_apocenter
        ),
        "period_scaled": period_over_mean_radius,
        "half_angle_integral": half_angle_integral,
        "half_angle_integral_residual": sp.simplify(
            half_angle_integral - sp.pi / 2
        ),
        "apsidal_angle_limit": apsidal_angle_limit,
        "apsidal_angle_limit_residual": sp.simplify(
            apsidal_angle_limit - sp.pi
        ),
        "scope": (
            "formal e->1 limit of noncollision log-potential orbits; full "
            "branch needs xi->infinity with xi*(1-e)->infinity"
        ),
    }


def _build_potential_interpolant(
    x_p: float, x_a: float
) -> tuple[Callable[[float], float], float]:
    """Integrate W'=Y(x) once and return a dense potential interpolant."""

    width = x_a - x_p
    solution = solve_ivp(
        lambda coordinate, _state: (solve_dimensionless_acceleration(coordinate),),
        (x_p, x_a),
        (0.0,),
        method="DOP853",
        rtol=3.0e-12,
        atol=3.0e-13,
        max_step=width / 300.0,
        dense_output=True,
    )
    if not solution.success or solution.sol is None:
        raise RuntimeError(solution.message)
    delta = float(solution.y[0, -1])

    def potential(coordinate: float) -> float:
        if coordinate <= x_p:
            return 0.0
        if coordinate >= x_a:
            return delta
        return float(solution.sol(coordinate)[0])

    return potential, delta


def _full_exponential_orbit_near_circular_mp(
    x_p_float: float, x_a_float: float
) -> dict[str, float | str]:
    """Resolve the O(e^2) radial well without double-precision cancellation."""

    eccentricity_float = (x_a_float - x_p_float) / (x_a_float + x_p_float)
    decimal_places = max(
        60, int(-math.log10(eccentricity_float)) * 5 + 30
    )
    with mp.workdps(decimal_places):
        x_p = mp.mpf(str(x_p_float))
        x_a = mp.mpf(str(x_a_float))
        mean_radius_mp = (x_p + x_a) / 2
        half_width = (x_a - x_p) / 2

        def acceleration_mp(coordinate: mp.mpf) -> mp.mpf:
            source = coordinate**-2
            value = mp.mpf(
                str(solve_dimensionless_acceleration(float(coordinate)))
            )
            for _iteration in range(20):
                exponential = mp.exp(-value)
                residual = value * (1 - exponential) - source
                derivative = 1 + (value - 1) * exponential
                step = residual / derivative
                value -= step
                if abs(step) <= 10 * mp.eps * max(1, abs(value)):
                    break
            return value

        potential_difference_mp = mp.quad(
            lambda coordinate: acceleration_mp(coordinate), [x_p, x_a]
        )
        lambda_squared_mp = 2 * potential_difference_mp / (
            x_p**-2 - x_a**-2
        )
        angular_momentum_mp = mp.sqrt(lambda_squared_mp)
        energy_mp = lambda_squared_mp / (2 * x_p**2)

        def radial_scaled_mp(s_float: float) -> mp.mpf:
            s = mp.mpf(str(s_float))
            coordinate = mean_radius_mp + half_width * s
            if s_float >= 1.0:
                upper_potential_difference = mp.mpf("0")
            elif s_float <= -1.0:
                upper_potential_difference = potential_difference_mp
            else:
                upper_potential_difference = mp.quad(
                    lambda position: acceleration_mp(position),
                    [coordinate, x_a],
                )
            radial_squared = (
                2 * upper_potential_difference
                + lambda_squared_mp * (x_a**-2 - coordinate**-2)
            )
            return radial_squared / half_width**2

        def radial_scaled(s_float: float) -> float:
            return float(radial_scaled_mp(s_float))

        def radial_scaled_prime(s_float: float) -> float:
            s = mp.mpf(str(s_float))
            coordinate = mean_radius_mp + half_width * s
            derivative = (
                -2 * acceleration_mp(coordinate)
                + 2 * lambda_squared_mp / coordinate**3
            ) / half_width
            return float(derivative)

        angular_momentum = float(angular_momentum_mp)
        one_way_time = _endpoint_regularized_integral(
            -1.0,
            1.0,
            radial_scaled,
            radial_scaled_prime,
            lambda _s, _q: 1.0,
        )
        one_way_angle = _endpoint_regularized_integral(
            -1.0,
            1.0,
            radial_scaled,
            radial_scaled_prime,
            lambda s, _q: angular_momentum
            / float(mean_radius_mp + half_width * mp.mpf(str(s))) ** 2,
        )
        turning_residual_max = float(
            half_width**2
            * max(abs(radial_scaled_mp(-1.0)), abs(radial_scaled_mp(1.0)))
        )
        potential_difference = float(potential_difference_mp)
        lambda_squared = float(lambda_squared_mp)
        energy = float(energy_mp)

    radial_period = 2.0 * one_way_time
    apsidal_angle = 2.0 * one_way_angle
    mean_radius = (x_p_float + x_a_float) / 2.0
    newton_period = 2.0 * math.pi * mean_radius ** 1.5
    return {
        "x_pericenter": x_p_float,
        "x_apocenter": x_a_float,
        "mean_radius": mean_radius,
        "eccentricity": eccentricity_float,
        "potential_difference": potential_difference,
        "lambda_squared": lambda_squared,
        "energy": energy,
        "radial_period_dimensionless": radial_period,
        "radial_period_over_mean_radius": radial_period / mean_radius,
        "apsidal_angle": apsidal_angle,
        "precession_degrees": math.degrees(apsidal_angle - 2.0 * math.pi),
        "newton_period_ratio": radial_period / newton_period,
        "turning_residual_max": turning_residual_max,
        "numerical_branch": "scaled_mpmath",
    }


def full_exponential_orbit(x_p: float, x_a: float) -> dict[str, float | str]:
    """Evaluate the exact exponential-force turning-point quadratures.

    ``x=r/r_M`` and time is measured in ``t_M=(GM/a0^3)^(1/4)``.
    """

    if not all(math.isfinite(value) and value > 0.0 for value in (x_p, x_a)):
        raise ValueError("turning radii must be positive and finite")
    if x_a <= x_p:
        raise ValueError("x_a must exceed x_p")
    eccentricity = (x_a - x_p) / (x_a + x_p)
    if eccentricity <= 2.0e-2:
        return _full_exponential_orbit_near_circular_mp(x_p, x_a)
    potential, delta_W = _build_potential_interpolant(x_p, x_a)
    lambda_squared = 2.0 * delta_W / (x_p ** -2 - x_a ** -2)
    angular_momentum = math.sqrt(lambda_squared)
    energy = lambda_squared / (2.0 * x_p**2)

    def radial_function(x: float) -> float:
        return 2.0 * (energy - potential(x)) - lambda_squared / x**2

    def radial_prime(x: float) -> float:
        return -2.0 * solve_dimensionless_acceleration(x) + 2.0 * lambda_squared / x**3

    one_way_time = _endpoint_regularized_integral(
        x_p, x_a, radial_function, radial_prime, lambda _x, _f: 1.0
    )
    one_way_angle = _endpoint_regularized_integral(
        x_p,
        x_a,
        radial_function,
        radial_prime,
        lambda x, _f: angular_momentum / x**2,
    )
    radial_period = 2.0 * one_way_time
    apsidal_angle = 2.0 * one_way_angle
    mean_radius = (x_p + x_a) / 2.0
    newton_period = 2.0 * math.pi * mean_radius ** 1.5
    return {
        "x_pericenter": x_p,
        "x_apocenter": x_a,
        "mean_radius": mean_radius,
        "eccentricity": eccentricity,
        "potential_difference": delta_W,
        "lambda_squared": lambda_squared,
        "energy": energy,
        "radial_period_dimensionless": radial_period,
        "radial_period_over_mean_radius": radial_period / mean_radius,
        "apsidal_angle": apsidal_angle,
        "precession_degrees": math.degrees(apsidal_angle - 2.0 * math.pi),
        "newton_period_ratio": radial_period / newton_period,
        "turning_residual_max": max(
            abs(radial_function(x_p)), abs(radial_function(x_a))
        ),
        "numerical_branch": "dense_potential",
    }


def validate_full_orbit_ode(x_p: float, x_a: float) -> dict[str, float | int]:
    """Compare the turning quadrature with independent nonlinear orbit events."""

    quadrature = full_exponential_orbit(x_p, x_a)
    lambda_squared = float(quadrature["lambda_squared"])
    angular_momentum = math.sqrt(lambda_squared)
    predicted_period = float(quadrature["radial_period_dimensionless"])
    predicted_angle = float(quadrature["apsidal_angle"])

    def equations(_time: float, state: np.ndarray) -> tuple[float, float, float]:
        radius, radial_velocity, _angle = state
        return (
            radial_velocity,
            lambda_squared / radius**3 - solve_dimensionless_acceleration(radius),
            angular_momentum / radius**2,
        )

    def pericenter(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    def apocenter(_time: float, state: np.ndarray) -> float:
        return float(state[1])

    pericenter.direction = 1.0
    pericenter.terminal = False
    apocenter.direction = -1.0
    apocenter.terminal = False
    solution = solve_ivp(
        equations,
        (0.0, 1.25 * predicted_period),
        (x_p, 0.0, 0.0),
        method="RK45",
        events=(pericenter, apocenter),
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=predicted_period / 300.0,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    peri_times = solution.t_events[0]
    peri_states = solution.y_events[0]
    keep = peri_times > predicted_period * 1.0e-7
    peri_times = peri_times[keep]
    peri_states = peri_states[keep]
    apo_states = solution.y_events[1]
    if len(peri_times) < 1 or len(apo_states) < 1:
        raise RuntimeError("required pericenter/apocenter events were not found")
    measured_period = float(peri_times[0])
    measured_angle = float(peri_states[0, 2])
    measured_apocenter = float(apo_states[0, 0])
    return {
        "predicted_period": predicted_period,
        "measured_period": measured_period,
        "period_relative_error": abs(measured_period / predicted_period - 1.0),
        "predicted_angle": predicted_angle,
        "measured_angle": measured_angle,
        "angle_relative_error": abs(measured_angle / predicted_angle - 1.0),
        "target_apocenter": x_a,
        "measured_apocenter": measured_apocenter,
        "apocenter_relative_error": abs(measured_apocenter / x_a - 1.0),
        "force_evaluations": int(solution.nfev),
    }


def run_full_audit() -> dict[str, object]:
    symbolic = derive_symbolic_law()
    deep_rows = [deep_log_orbit(e) for e in (0.1, 0.3, 0.6, 0.9)]
    deep_ode_grid = [validate_deep_log_orbit_ode(e) for e in (0.1, 0.6, 0.9)]
    transition = full_exponential_orbit(0.7, 2.3)
    transition_ode_grid = [
        validate_full_orbit_ode(x_p, x_a)
        for x_p, x_a in ((1.35, 1.65), (0.7, 2.3), (0.15, 2.85))
    ]
    transition_ode = transition_ode_grid[1]
    newton = full_exponential_orbit(0.01, 0.03)
    deep_full = full_exponential_orbit(1000.0, 3000.0)
    deep_anchor = deep_log_orbit(0.5)
    radial_limit = derive_radial_deep_limit()
    force_solver_grid = []
    previous_y = math.inf
    for x_value in (1.0e-3, 1.0e-2, 0.1, 1.0, 10.0, 1.0e3, 1.0e6):
        y_value = solve_dimensionless_acceleration(x_value)
        source = x_value**-2
        relative_residual = abs(
            y_value * mu_exponential(y_value) - source
        ) / source
        force_solver_grid.append(
            {
                "x": x_value,
                "y": y_value,
                "relative_residual": relative_residual,
                "decreases_from_previous": y_value < previous_y,
            }
        )
        previous_y = y_value
    max_force_solver_residual = max(
        row["relative_residual"] for row in force_solver_grid
    )
    max_virial_error = max(
        abs(float(row["mean_speed_squared"]) - 1.0) for row in deep_rows
    )
    deep_period_error = abs(
        deep_full["radial_period_over_mean_radius"]
        / float(deep_anchor["radial_period_scaled"])
        - 1.0
    )
    deep_angle_error = abs(
        deep_full["apsidal_angle"] / float(deep_anchor["apsidal_angle"]) - 1.0
    )
    fixed_e_scale_separation = abs(
        newton["radial_period_over_mean_radius"]
        / deep_full["radial_period_over_mean_radius"]
        - 1.0
    )
    max_transition_ode_error = max(
        max(
            float(row["period_relative_error"]),
            float(row["angle_relative_error"]),
            float(row["apocenter_relative_error"]),
        )
        for row in transition_ode_grid
    )
    max_deep_ode_error = max(
        max(
            float(row["period_relative_error"]),
            float(row["angle_relative_error"]),
            float(row["apocenter_relative_error"]),
        )
        for row in deep_ode_grid
    )
    checks = {
        "symbolic_flux_to_orbit_chain": all(
            symbolic[key] == 0
            for key in (
                "flux_residual",
                "constitutive_slope_residual",
                "full_force_h_slope_residual",
                "time_scale_residual",
                "potential_chain_rule_residual",
                "potential_parametric_derivative_residual",
                "turning_point_pericenter_residual",
                "turning_point_apocenter_residual",
                "test_particle_virial_residual",
                "newton_circular_condition_residual",
                "deep_circular_condition_residual",
                "deep_epicycle_frequency_squared_residual",
            )
        ),
        "numerical_exponential_force_solver": (
            max_force_solver_residual < 5.0e-10
            and all(row["decreases_from_previous"] for row in force_solver_grid)
        ),
        "deep_test_particle_virial_invariant": max_virial_error < 2.0e-9,
        "deep_quadrature_matches_nonlinear_events": max_deep_ode_error < 2.0e-9,
        "finite_eccentricity_changes_apsidal_angle": not bool(
            deep_log_orbit(0.6)["epicycle_mutation_survives"]
        ),
        "turning_point_algebra_consistency": (
            transition["turning_residual_max"] < 2.0e-10
        ),
        "transition_quadrature_matches_nonlinear_events": (
            max_transition_ode_error < 2.0e-8
        ),
        "newtonian_kepler_limit": (
            abs(newton["newton_period_ratio"] - 1.0) < 2.0e-8
            and abs(newton["apsidal_angle"] / (2.0 * math.pi) - 1.0) < 2.0e-8
        ),
        "deep_similarity_limit": deep_period_error < 8.0e-4
        and deep_angle_error < 8.0e-4,
        "full_transition_retains_scale_dependence": fixed_e_scale_separation
        > 0.5,
        "radial_limit_closed_integrals": (
            radial_limit["j_scaling_residual"] == 0
            and radial_limit["energy_limit_residual"] == 0
            and radial_limit["radial_function_scaling_residual"] == 0
            and radial_limit["angular_prefactor_residual"] == 0
            and radial_limit["gamma_integral_residual"] == 0
            and radial_limit["half_angle_integral_residual"] == 0
            and radial_limit["apsidal_angle_limit_residual"] == 0
        ),
        "naive_one_point_kepler_substitution_falsified": (
            symbolic["naive_deep_ratio_near_circular"] != 1
            and symbolic["naive_deep_ratio_radial_limit"] != 1
        ),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "symbolic": symbolic,
        "deep_rows": deep_rows,
        "deep_ode_grid": deep_ode_grid,
        "transition": transition,
        "transition_ode": transition_ode,
        "transition_ode_grid": transition_ode_grid,
        "newton": newton,
        "deep_full": deep_full,
        "deep_anchor": deep_anchor,
        "radial_limit": radial_limit,
        "force_solver_grid": force_solver_grid,
        "max_force_solver_residual": max_force_solver_residual,
        "max_virial_error": max_virial_error,
        "deep_period_error": deep_period_error,
        "deep_angle_error": deep_angle_error,
        "fixed_e_scale_separation": fixed_e_scale_separation,
        "max_transition_ode_error": max_transition_ode_error,
        "max_deep_ode_error": max_deep_ode_error,
        "scope": {
            "proves_relativistic_closure": False,
            "proves_novelty": False,
            "requires_spherical_exterior": True,
            "requires_leading_weak_field_slow_motion_geodesic": True,
            "includes_external_field_effect": False,
            "includes_exact_y_zero": False,
        },
    }


def _main() -> int:
    audit = run_full_audit()
    print("=" * 88)
    print("HPI-DELTA FINITE-ECCENTRICITY KEPLER LAW")
    print("=" * 88)
    print("Deep-MOND eccentric test-particle laws:")
    print("  <v^2>^2 = G*M*a0  (one exterior test particle; time average)")
    print("  T_r = R/(G*M*a0)^(1/4) * F(e)")
    print("  Theta_peri->peri = Theta(e),  Delta_varpi=Theta(e)-2*pi")
    print("\nComputed universal deep functions:")
    print("       e          F(e)      Theta(e)    precession[deg]   <v^2>/v_inf^2")
    for row in audit["deep_rows"]:
        print(
            f"  {row['eccentricity']:6.3f}  {row['radial_period_scaled']:12.9f}"
            f"  {row['apsidal_angle']:12.9f}  {row['precession_degrees']:17.9f}"
            f"  {row['mean_speed_squared']:15.12f}"
        )
    print("\nLimiting values:")
    print("  e->0: F=Theta=sqrt(2)*pi; Delta_varpi=-105.4415588 deg")
    print("  formal log e->1: F=2*sqrt(2*pi), Theta->pi")
    print("    full branch requires xi*(1-e)>>1 and an exterior pericenter")
    print("\nFalsified shortcut:")
    print(
        "  Reusing the circular law with (R,T_r) misses the exact deep law by "
        f"a factor {audit['symbolic']['naive_deep_ratio_near_circular']} as e->0 "
        f"and {audit['symbolic']['naive_deep_ratio_radial_limit']} in the "
        "formal log e->1 limit."
    )
    print("\nChecks:")
    for label, passed in audit["checks"].items():
        print(("  [PASS] " if passed else "  [FAIL] ") + label)
    print("\nVERDICT: " + ("PASS_BOUNDED" if audit["passed"] else "FAIL"))
    print(
        "NON-CLAIMS: known central/log-potential machinery; no novelty, PPN, "
        "full-action closure, galaxy BTFR, EFE, or exact-y=0 proof."
    )
    certificate = {
        "status": "PASS_BOUNDED" if audit["passed"] else "FAIL",
        "checks_passed": sum(bool(value) for value in audit["checks"].values()),
        "checks_total": len(audit["checks"]),
        "max_test_particle_virial_error": audit["max_virial_error"],
        "max_deep_ode_error": audit["max_deep_ode_error"],
        "deep_period_similarity_error": audit["deep_period_error"],
        "deep_angle_similarity_error": audit["deep_angle_error"],
        "fixed_e_scale_separation": audit["fixed_e_scale_separation"],
        "max_force_solver_residual": audit["max_force_solver_residual"],
        "max_transition_ode_error": audit["max_transition_ode_error"],
        "proves_relativistic_closure": False,
        "proves_novelty": False,
    }
    print("CERTIFICATE_JSON:", json.dumps(certificate, sort_keys=True))
    return 0 if audit["passed"] else 1


if __name__ == "__main__":
    sys.exit(_main())
