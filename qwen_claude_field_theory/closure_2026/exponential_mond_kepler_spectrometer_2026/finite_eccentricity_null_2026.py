#!/usr/bin/env python3
"""Finite-eccentricity completion of the exponential-MOND clock null.

The circular spectrometer uses q=kappa^2/Omega^2.  Real orbit families have
finite radial amplitude, so this module derives—rather than fits—the first
nonzero correction to the ratio of the two *fundamental* frequencies.  It
also corrects the guiding radius and builds a cross-radius null in which the
central mass, a0, distance, and absolute time calibration cancel.

All statements are Newtonian/weak-static central-force results.  They do not
repair the parent relativistic theory's independent closure obstruction.
"""

from __future__ import annotations

import json
import math
from typing import Any

import mpmath as mp
import sympy as sp


MAX_NUMERICALLY_AUDITED_ECCENTRICITY = 0.03


class AsymptoticEndpointError(ValueError):
    """The physical orbit may exist, but the O(e^2) inverse cannot resolve it."""


def _circle_average(expression: sp.Expr, angle: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.integrate(sp.expand_trig(expression), (angle, 0, 2 * sp.pi))
        / (2 * sp.pi)
    )


def derive_generic_finite_amplitude() -> dict[str, Any]:
    """Generate the Poincare-Lindstedt and mean-azimuth corrections.

    In tau=Omega_0 t and x=(r-r0)/r0, the fixed-angular-momentum radial
    equation is

        x'' + q x + u3 x^2/2 + u4 x^3/6 = O(x^4).

    The coefficient returned below is fractional in q_e:
    q_e=q[1+C_e epsilon^2+O(epsilon^4)].
    """

    angle, epsilon = sp.symbols("theta epsilon", real=True)
    q = sp.symbols("q", positive=True)
    u3, u4 = sp.symbols("u_3 u_4", real=True)
    A0, A2, radial_squared_correction = sp.symbols("A_0 A_2 f_r", real=True)

    x = epsilon * sp.cos(angle) + epsilon**2 * (
        A0 + A2 * sp.cos(2 * angle)
    )
    omega_r_squared = q * (1 + radial_squared_correction * epsilon**2)
    ode = sp.series(
        omega_r_squared * sp.diff(x, angle, 2)
        + q * x
        + u3 * x**2 / 2
        + u4 * x**3 / 6,
        epsilon,
        0,
        4,
    ).removeO().expand()

    order2 = ode.coeff(epsilon, 2)
    order2_constant = _circle_average(order2, angle)
    order2_second_harmonic = sp.simplify(
        2 * _circle_average(order2 * sp.cos(2 * angle), angle)
    )
    second_order_solution = sp.solve(
        (order2_constant, order2_second_harmonic), (A0, A2), dict=True
    )[0]

    order3 = sp.simplify(ode.coeff(epsilon, 3).subs(second_order_solution))
    order3_secular = sp.simplify(
        2 * _circle_average(order3 * sp.cos(angle), angle)
    )
    radial_solution = sp.solve(order3_secular, radial_squared_correction)[0]

    inverse_radius_squared = sp.series(
        (1 + x.subs(second_order_solution)) ** -2, epsilon, 0, 3
    ).removeO()
    mean_inverse_radius_squared = _circle_average(inverse_radius_squared, angle)
    azimuthal_linear_correction = sp.simplify(
        sp.expand(mean_inverse_radius_squared).coeff(epsilon, 2)
    )
    azimuthal_squared_correction = sp.simplify(2 * azimuthal_linear_correction)
    finite_e_correction = sp.simplify(
        radial_solution - azimuthal_squared_correction
    )
    expected = sp.simplify(
        u4 / (8 * q) - 5 * u3**2 / (24 * q**2) - 3 - u3 / q
    )

    return {
        "theta": angle,
        "epsilon": epsilon,
        "q": q,
        "u3": u3,
        "u4": u4,
        "A0": second_order_solution[A0],
        "A2": second_order_solution[A2],
        "order2_constant_residual": sp.simplify(
            order2_constant.subs(second_order_solution)
        ),
        "order2_second_harmonic_residual": sp.simplify(
            order2_second_harmonic.subs(second_order_solution)
        ),
        "order3_secular_residual": sp.simplify(
            order3_secular.subs(radial_squared_correction, radial_solution)
        ),
        "radial_frequency_squared_correction": radial_solution,
        "azimuthal_frequency_linear_correction": azimuthal_linear_correction,
        "azimuthal_frequency_squared_correction": azimuthal_squared_correction,
        "finite_e_correction": finite_e_correction,
        "finite_e_correction_residual": sp.simplify(
            finite_e_correction - expected
        ),
    }


def derive_turning_point_parity() -> dict[str, Any]:
    """Generate the turning-point exchange lemma behind the O(e^4) remainder.

    Write the two turning points as r_\pm=R(e)(1\pm e) at fixed angular
    momentum.  The energy-matching equation is unchanged by e -> -e because
    that map only exchanges the two roots.  For a stable circle q>0, the
    implicit-function theorem gives a unique analytic R(e), hence R is even.
    The radial period and apsidal angle are integrals over the same unordered
    pair of roots, so they too are even.  The symbolic calculation below
    generates the first odd coefficients of R and the required quadratic
    guiding-radius correction from a generic effective potential.
    """

    e = sp.symbols("e", real=True)
    q = sp.symbols("q", positive=True)
    u3, u4, u5 = sp.symbols("u_3 u_4 u_5", real=True)
    b1, b2, b3, b4 = sp.symbols("b_1 b_2 b_3 b_4", real=True)
    x = sp.symbols("x", real=True)
    potential = q * x**2 / 2 + u3 * x**3 / 6 + u4 * x**4 / 24 + u5 * x**5 / 120
    mean_radius = 1 + b1 * e + b2 * e**2 + b3 * e**3 + b4 * e**4
    x_plus = sp.expand(mean_radius * (1 + e) - 1)
    x_minus = sp.expand(mean_radius * (1 - e) - 1)
    energy_difference = sp.series(
        potential.subs(x, x_plus) - potential.subs(x, x_minus), e, 0, 6
    ).removeO().expand()

    b1_solution = sp.solve(energy_difference.coeff(e, 2), b1)[0]
    order3 = sp.simplify(energy_difference.coeff(e, 3).subs(b1, b1_solution))
    b2_solution = sp.solve(order3, b2)[0]
    order4 = sp.simplify(
        energy_difference.coeff(e, 4).subs({b1: b1_solution, b2: b2_solution})
    )
    b3_solution = sp.solve(order4, b3)[0]

    # With an explicitly even mean radius, exchanging e swaps x_+ and x_-.
    # Dividing the antisymmetric energy difference by 2e therefore gives an
    # exactly even turning equation (for the polynomial used in this audit).
    mean_radius_even = 1 + b2 * e**2 + b4 * e**4
    even_plus = sp.expand(mean_radius_even * (1 + e) - 1)
    even_minus = sp.expand(mean_radius_even * (1 - e) - 1)
    turning_equation = sp.simplify(
        (potential.subs(x, even_plus) - potential.subs(x, even_minus)) / (2 * e)
    )
    turning_equation_evenness_residual = sp.simplify(
        turning_equation.subs(e, -e) - turning_equation
    )
    # Independently extend Poincare--Lindstedt with possible odd frequency
    # coefficients.  The first- and third-order coefficients must be solved
    # to zero; they are not excluded by the ansatz.  The first-harmonic cubic
    # coefficient is the amplitude gauge and is set to zero.
    angle, amplitude = sp.symbols("theta a", real=True)
    A0, A2, B3 = sp.symbols("A_0 A_2 B_3", real=True)
    w1, w2, w3 = sp.symbols("w_1 w_2 w_3", real=True)
    orbit = (
        amplitude * sp.cos(angle)
        + amplitude**2 * (A0 + A2 * sp.cos(2 * angle))
        + amplitude**3 * B3 * sp.cos(3 * angle)
    )
    omega_squared = q * (
        1 + w1 * amplitude + w2 * amplitude**2 + w3 * amplitude**3
    )
    pl_ode = sp.series(
        omega_squared * sp.diff(orbit, angle, 2)
        + q * orbit
        + u3 * orbit**2 / 2
        + u4 * orbit**3 / 6
        + u5 * orbit**4 / 24,
        amplitude,
        0,
        5,
    ).removeO().expand()

    order2_pl = pl_ode.coeff(amplitude, 2)
    pl_second = sp.solve(
        (
            _circle_average(order2_pl, angle),
            2 * _circle_average(order2_pl * sp.cos(2 * angle), angle),
            2 * _circle_average(order2_pl * sp.cos(angle), angle),
        ),
        (A0, A2, w1),
        dict=True,
    )[0]
    order3_pl = sp.simplify(pl_ode.coeff(amplitude, 3).subs(pl_second))
    pl_third = sp.solve(
        (
            2 * _circle_average(order3_pl * sp.cos(angle), angle),
            2 * _circle_average(order3_pl * sp.cos(3 * angle), angle),
        ),
        (w2, B3),
        dict=True,
    )[0]
    parity_solution = {**pl_second, **pl_third}
    order4_first_harmonic = sp.simplify(
        2
        * _circle_average(
            pl_ode.coeff(amplitude, 4).subs(parity_solution) * sp.cos(angle),
            angle,
        )
    )
    w3_solution = sp.solve(order4_first_harmonic, w3)[0]
    parity_solution[w3] = w3_solution

    inverse_radius_mean = _circle_average(
        sp.series((1 + orbit) ** -2, amplitude, 0, 4).removeO(), angle
    )
    inverse_radius_mean = sp.simplify(inverse_radius_mean.subs(parity_solution))
    signed_eccentricity = sp.series(
        (orbit.subs(angle, 0) - orbit.subs(angle, sp.pi))
        / (2 + orbit.subs(angle, 0) + orbit.subs(angle, sp.pi)),
        amplitude,
        0,
        5,
    ).removeO().subs(parity_solution).expand()

    return {
        "e": e,
        "q": q,
        "u3": u3,
        "energy_difference": energy_difference,
        "odd_mean_radius_linear": sp.simplify(b1_solution),
        "mean_radius_quadratic": sp.simplify(b2_solution),
        "mean_radius_quadratic_residual": sp.simplify(
            b2_solution + u3 / (6 * q)
        ),
        "odd_mean_radius_cubic": sp.simplify(b3_solution),
        "turning_equation_evenness_residual": turning_equation_evenness_residual,
        "radial_frequency_linear": sp.simplify(parity_solution[w1]),
        "radial_frequency_quadratic": sp.simplify(parity_solution[w2]),
        "radial_frequency_cubic": sp.simplify(parity_solution[w3]),
        "radial_frequency_cubic_negative_control": sp.simplify(
            order4_first_harmonic.subs(w3, 1)
        ),
        "azimuthal_mean_linear": sp.simplify(
            inverse_radius_mean.coeff(amplitude, 1)
        ),
        "azimuthal_mean_cubic": sp.simplify(
            inverse_radius_mean.coeff(amplitude, 3)
        ),
        "signed_eccentricity_quadratic": sp.simplify(
            signed_eccentricity.coeff(amplitude, 2)
        ),
        "signed_eccentricity_quartic": sp.simplify(
            signed_eccentricity.coeff(amplitude, 4)
        ),
        "observable_remainder": "O(e^4) by turning-point exchange plus analyticity",
    }


def derive_force_derivative_coefficients() -> dict[str, Any]:
    """Generate potential derivatives by a logarithmic-derivative recurrence."""

    s, D, E = sp.symbols("s D E", real=True)

    # A_n=r^n g^(n)/g obeys A_(n+1)=dA_n/dlnr+(s-n)A_n.
    # At the orders needed here, d/dlnr = D d/ds + E d/dD.
    def log_derivative(expression: sp.Expr) -> sp.Expr:
        return sp.simplify(sp.diff(expression, s) * D + sp.diff(expression, D) * E)

    A1 = s
    A2 = sp.expand(log_derivative(A1) + (s - 1) * A1)
    A3 = sp.expand(log_derivative(A2) + (s - 2) * A2)
    A2_expected = D + s**2 - s
    A3_expected = E + 3 * (s - 1) * D + (s - 2) * (s**2 - s)
    u3 = sp.expand(A2 - 12)
    u4 = sp.expand(A3 + 60)
    return {
        "s": s,
        "D": D,
        "E": E,
        "A1": A1,
        "A2": A2,
        "A3": A3,
        "A2_residual": sp.simplify(A2 - A2_expected),
        "A3_residual": sp.simplify(A3 - A3_expected),
        "u3": u3,
        "u4": u4,
        "u3_residual": sp.simplify(u3 - (D + s**2 - s - 12)),
        "u4_residual": sp.simplify(u4 - (A3_expected + 60)),
    }


def derive_exact_exponential_correction() -> dict[str, Any]:
    """Insert the exact exponential exterior law and simplify C_e(y)."""

    y = sp.symbols("y", positive=True)
    L = y / (sp.exp(y) - 1)
    q = sp.simplify((1 + 3 * L) / (1 + L))
    s = sp.simplify(q - 3)
    dlny_dlnr = sp.simplify(-2 / (1 + L))
    y_dot = sp.simplify(y * dlny_dlnr)
    D = sp.factor(sp.diff(q, y) * y_dot)
    E = sp.factor(sp.diff(D, y) * y_dot)
    D_expected = 4 * L * (y + L - 1) / (1 + L) ** 3
    E_expected = -8 * L / (1 + L) ** 5 * (
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
    derivative_data = derive_force_derivative_coefficients()
    u3 = sp.simplify(
        derivative_data["u3"].subs(
            {derivative_data["s"]: s, derivative_data["D"]: D}
        )
    )
    u4 = sp.simplify(
        derivative_data["u4"].subs(
            {
                derivative_data["s"]: s,
                derivative_data["D"]: D,
                derivative_data["E"]: E,
            }
        )
    )
    generic = derive_generic_finite_amplitude()
    Ce = sp.factor(
        generic["finite_e_correction"].subs(
            {generic["q"]: q, generic["u3"]: u3, generic["u4"]: u4}
        )
    )
    polynomial = (
        9 * L**5
        + 54 * L**4
        + (192 - 33 * y) * L**3
        + (42 + 105 * y - 36 * y**2) * L**2
        + (-41 + 65 * y - 14 * y**2) * L
        + 6 * y**2
        - 9 * y
    )
    Ce_explicit = sp.factor(
        L * polynomial / (6 * (1 + L) ** 4 * (1 + 3 * L) ** 2)
    )
    return {
        "y": y,
        "L": L,
        "q": q,
        "s": s,
        "D": D,
        "E": E,
        "D_residual": sp.simplify(D - D_expected),
        "E_residual": sp.simplify(E - E_expected),
        "u3": u3,
        "u4": u4,
        "Ce": Ce,
        "Ce_explicit": Ce_explicit,
        "explicit_Ce_residual": sp.simplify(Ce - Ce_explicit),
        "deep_limit": sp.limit(Ce, y, 0, dir="+"),
        "newton_limit": sp.limit(Ce, y, sp.oo),
    }


def _numeric_transition(y: mp.mpf) -> dict[str, mp.mpf]:
    """High-precision forward transition and finite-e coefficient."""

    L = y / mp.expm1(y)
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
    # The generic form suffers catastrophic cancellation in the Newtonian
    # tail.  Evaluate the algebraically identical explicit polynomial instead.
    polynomial = (
        9 * L**5
        + 54 * L**4
        + (192 - 33 * y) * L**3
        + (42 + 105 * y - 36 * y**2) * L**2
        + (-41 + 65 * y - 14 * y**2) * L
        + 6 * y**2
        - 9 * y
    )
    Ce = L * polynomial / (6 * (1 + L) ** 4 * (1 + 3 * L) ** 2)
    return {"L": L, "q": q, "s": s, "D": D, "E": E, "u3": u3, "u4": u4, "Ce": Ce}


def _working_dps(y: float) -> int:
    """Precision sufficient for both y->0 and exponentially small y->infinity tails."""

    yy = mp.mpf(y)
    endpoint_digits = max(abs(mp.log10(yy)), yy / mp.log(10))
    return min(2000, max(80, int(mp.ceil(endpoint_digits)) + 80))


def circular_clock_ratio(y: float) -> float:
    if not math.isfinite(y) or y <= 0:
        raise ValueError("the positive exterior branch requires y>0")
    with mp.workdps(_working_dps(y)):
        return float(_numeric_transition(mp.mpf(y))["q"])


def finite_e_coefficient(y: float) -> float:
    if not math.isfinite(y) or y <= 0:
        raise ValueError("the positive exterior branch requires y>0")
    with mp.workdps(_working_dps(y)):
        return float(_numeric_transition(mp.mpf(y))["Ce"])


def _validate_eccentricity(eccentricity: float) -> None:
    if (
        not math.isfinite(eccentricity)
        or eccentricity < 0
        or eccentricity > MAX_NUMERICALLY_AUDITED_ECCENTRICITY
    ):
        raise ValueError(
            "the O(e^2) implementation is numerically audited only for "
            f"0<=e<={MAX_NUMERICALLY_AUDITED_ECCENTRICITY}; this is not a "
            "uniform remainder theorem"
        )


def _truncated_model_endpoint(eccentricity: mp.mpf) -> mp.mpf:
    return 2 * (1 + eccentricity**2 / 6)


def _invert_truncated_target(target: mp.mpf, eccentricity: mp.mpf) -> mp.mpf:
    """Invert a target strictly inside the O(e^2) model image."""

    def residual(log_y: mp.mpf) -> mp.mpf:
        state = _numeric_transition(mp.exp(log_y))
        return state["q"] * (1 + state["Ce"] * eccentricity**2) - target

    lower, upper = mp.mpf(-700), mp.mpf(700)
    f_lower, f_upper = residual(lower), residual(upper)
    if not (f_lower > 0 and f_upper < 0):
        raise AsymptoticEndpointError(
            "target is too close to an asymptotic endpoint for the O(e^2) inverse"
        )
    for _ in range(800):
        middle = (lower + upper) / 2
        if residual(middle) > 0:
            lower = middle
        else:
            upper = middle
    return mp.exp((lower + upper) / 2)


def recover_circular_state(q_e: float, eccentricity: float) -> dict[str, float]:
    """Recover y and q0 from a finite-e fundamental frequency ratio.

    The solve is performed in log(y), so q_e may lie slightly above two.  The
    returned state is accurate through the O(e^2) model, not an all-orders
    finite-e inverse.
    """

    _validate_eccentricity(eccentricity)
    if not math.isfinite(q_e):
        raise ValueError("q_e must be finite")
    q_max = 2 * (1 + eccentricity**2 / 6)
    if not 1 < q_e < q_max:
        raise AsymptoticEndpointError(
            "q_e lies outside the image of the truncated O(e^2) model.  "
            "This does not reject the physical orbit: valid all-orders orbits "
            "can differ by O(e^4).  Supply an absolute model-error bound to "
            "recover_circular_state_interval()."
        )

    with mp.workdps(80):
        target = mp.mpf(q_e)
        ecc = mp.mpf(eccentricity)
        y = _invert_truncated_target(target, ecc)
        state = _numeric_transition(y)
        endpoint_margin = min(target - 1, _truncated_model_endpoint(ecc) - target)
        e4_scale = ecc**4
        return {
            "y": float(y),
            "q0": float(state["q"]),
            "Ce": float(state["Ce"]),
            "u3": float(state["u3"]),
            "q_model_endpoint_margin": float(endpoint_margin),
            "endpoint_margin_over_e4": (
                math.inf if e4_scale == 0 else float(endpoint_margin / e4_scale)
            ),
            "interpretation": "formal O(e^2) point inverse; no uniform remainder bound",
        }


def recover_circular_state_interval(
    q_e: float,
    eccentricity: float,
    *,
    absolute_q_model_error: float,
) -> dict[str, float | bool | str]:
    """Invert with a caller-supplied absolute bound on the omitted q remainder.

    Unlike the point inverse, this routine can honestly represent a physical
    q_e above the truncated deep-MOND endpoint.  In that case the compatible
    interval touches y=0 and the acceleration is reported as unresolved, not
    invalid.  No universal O(e^4) coefficient bound is assumed here.
    """

    _validate_eccentricity(eccentricity)
    if not math.isfinite(q_e):
        raise ValueError("q_e must be finite")
    if not math.isfinite(absolute_q_model_error) or absolute_q_model_error <= 0:
        raise ValueError("absolute_q_model_error must be finite and positive")

    with mp.workdps(100):
        target = mp.mpf(q_e)
        ecc = mp.mpf(eccentricity)
        error = mp.mpf(absolute_q_model_error)
        q_min = mp.mpf(1)
        q_max = _truncated_model_endpoint(ecc)
        compatible_low = max(q_min, target - error)
        compatible_high = min(q_max, target + error)
        if not compatible_low < compatible_high:
            raise ValueError(
                "measurement interval does not intersect the O(e^2) model image"
            )

        deep_unresolved = compatible_high == q_max
        newton_unresolved = compatible_low == q_min
        y_min = mp.mpf(0) if deep_unresolved else _invert_truncated_target(compatible_high, ecc)
        y_max = mp.inf if newton_unresolved else _invert_truncated_target(compatible_low, ecc)
        return {
            "model_interval_intersects": True,
            "deep_endpoint_unresolved": bool(deep_unresolved),
            "newton_endpoint_unresolved": bool(newton_unresolved),
            "y_min": float(y_min),
            "y_max": float(y_max),
            "q_model_low": float(compatible_low),
            "q_model_high": float(compatible_high),
            "absolute_q_model_error": float(error),
            "interpretation": "interval conditional on caller-supplied q remainder bound",
        }


def corrected_radius_invariant(
    mean_turning_radius: float, q_e: float, eccentricity: float
) -> dict[str, float]:
    """Return r0^2 y(1-exp(-y)), equal to GM/a0 for every exterior orbit."""

    if not math.isfinite(mean_turning_radius) or mean_turning_radius <= 0:
        raise ValueError("mean turning radius must be positive")
    state = recover_circular_state(q_e, eccentricity)
    r0 = mean_turning_radius * (
        1 + state["u3"] * eccentricity**2 / (6 * state["q0"])
    )
    X = state["y"] * (-math.expm1(-state["y"]))
    return {
        **state,
        "guiding_radius": r0,
        "X": X,
        "r0_squared_X": r0**2 * X,
    }


def cross_radius_log_null(
    orbit_i: dict[str, float], orbit_j: dict[str, float]
) -> float:
    """Compute ln[I_i/I_j]; a common distance scale cancels identically."""

    required = ("mean_turning_radius", "q_e", "eccentricity")
    for label, orbit in (("orbit_i", orbit_i), ("orbit_j", orbit_j)):
        missing = [key for key in required if key not in orbit]
        if missing:
            raise ValueError(f"{label} is missing {', '.join(missing)}")
    invariant_i = corrected_radius_invariant(
        orbit_i["mean_turning_radius"], orbit_i["q_e"], orbit_i["eccentricity"]
    )["r0_squared_X"]
    invariant_j = corrected_radius_invariant(
        orbit_j["mean_turning_radius"], orbit_j["q_e"], orbit_j["eccentricity"]
    )["r0_squared_X"]
    return math.log(invariant_i / invariant_j)


def synthetic_finite_e_observables(y: float, eccentricity: float) -> dict[str, float]:
    """Generate O(e^2) observables in units GM/a0=1 for a consistency test."""

    _validate_eccentricity(eccentricity)
    with mp.workdps(_working_dps(y)):
        yy = mp.mpf(y)
        state = _numeric_transition(yy)
        mu = -mp.expm1(-yy)
        r0 = mp.sqrt(1 / (yy * mu))
        ecc = mp.mpf(eccentricity)
        q_e = state["q"] * (1 + state["Ce"] * ecc**2)
        mean_radius = r0 * (1 - state["u3"] * ecc**2 / (6 * state["q"]))
        return {
            "y": float(yy),
            "q0": float(state["q"]),
            "q_e": float(q_e),
            "Ce": float(state["Ce"]),
            "u3": float(state["u3"]),
            "guiding_radius": float(r0),
            "mean_turning_radius": float(mean_radius),
            "eccentricity": float(ecc),
        }


def build_results() -> dict[str, Any]:
    generic = derive_generic_finite_amplitude()
    parity = derive_turning_point_parity()
    exact = derive_exact_exponential_correction()
    samples = {
        str(y): {
            "q0": circular_clock_ratio(y),
            "Ce": finite_e_coefficient(y),
        }
        for y in (0.1, 1.0, 3.0, 7.0)
    }
    synthetic = []
    null_observations = []
    for y in (0.2, 1.0, 3.0):
        observed = synthetic_finite_e_observables(y, 0.03)
        null_observations.append(
            {
                "mean_turning_radius": observed["mean_turning_radius"],
                "q_e": observed["q_e"],
                "eccentricity": 0.03,
            }
        )
        recovered = corrected_radius_invariant(
            observed["mean_turning_radius"], observed["q_e"], 0.03
        )
        synthetic.append(
            {
                "y": y,
                "r0_squared_X": recovered["r0_squared_X"],
                "absolute_null_residual": abs(recovered["r0_squared_X"] - 1),
            }
        )
    base_null = cross_radius_log_null(null_observations[0], null_observations[-1])
    scaled_observations = [dict(observation) for observation in null_observations]
    for observation in scaled_observations:
        observation["mean_turning_radius"] *= 37
    scaled_null = cross_radius_log_null(
        scaled_observations[0], scaled_observations[-1]
    )
    distance_cancellation_residual = abs(base_null - scaled_null)
    controls = {
        "kepler_Ce": sp.simplify(
            generic["finite_e_correction"].subs(
                {generic["q"]: 1, generic["u3"]: -6, generic["u4"]: 36}
            )
        ),
        "harmonic_Ce": sp.simplify(
            generic["finite_e_correction"].subs(
                {generic["q"]: 4, generic["u3"]: -12, generic["u4"]: 60}
            )
        ),
        "deep_Ce": sp.simplify(
            generic["finite_e_correction"].subs(
                {generic["q"]: 2, generic["u3"]: -10, generic["u4"]: 54}
            )
        ),
        "deep_radial_only_mutation": sp.simplify(
            generic["radial_frequency_squared_correction"].subs(
                {generic["q"]: 2, generic["u3"]: -10, generic["u4"]: 54}
            )
        ),
    }
    certificates = {
        "poincare_lindstedt_order2": generic["order2_constant_residual"] == 0
        and generic["order2_second_harmonic_residual"] == 0,
        "poincare_lindstedt_secular_cancellation": generic[
            "order3_secular_residual"
        ]
        == 0,
        "fundamental_clock_correction": generic["finite_e_correction_residual"]
        == 0,
        "turning_point_exchange_evenness": parity[
            "turning_equation_evenness_residual"
        ]
        == 0
        and parity["odd_mean_radius_linear"] == 0
        and parity["odd_mean_radius_cubic"] == 0,
        "signed_amplitude_frequency_evenness": parity[
            "radial_frequency_linear"
        ]
        == 0
        and parity["radial_frequency_cubic"] == 0
        and parity["azimuthal_mean_linear"] == 0
        and parity["azimuthal_mean_cubic"] == 0
        and parity["signed_eccentricity_quadratic"] == 0
        and parity["signed_eccentricity_quartic"] == 0
        and parity["radial_frequency_cubic_negative_control"] != 0,
        "force_derivative_transition": exact["D_residual"] == 0
        and exact["E_residual"] == 0,
        "explicit_exponential_polynomial": exact["explicit_Ce_residual"] == 0,
        "deep_limit_one_sixth": exact["deep_limit"] == sp.Rational(1, 6),
        "newton_limit_zero": exact["newton_limit"] == 0,
        "closed_orbit_controls": controls["kepler_Ce"] == 0
        and controls["harmonic_Ce"] == 0,
        "radial_only_mutation_rejected": controls["deep_radial_only_mutation"]
        != controls["deep_Ce"],
        "synthetic_corrected_null": max(
            row["absolute_null_residual"] for row in synthetic
        )
        < 5e-5,
        "common_distance_cancels": distance_cancellation_residual < 1e-14,
    }
    passed = all(certificates.values())
    return {
        "status": (
            "PASS_FINITE_E_WEAK_STATIC_EXTERIOR_NULL_TO_ORDER_E4"
            if passed
            else "FAIL_FINITE_E_WEAK_STATIC_EXTERIOR_NULL"
        ),
        "generic": {
            "A0": str(generic["A0"]),
            "A2": str(generic["A2"]),
            "radial_frequency_squared_correction": str(
                generic["radial_frequency_squared_correction"]
            ),
            "azimuthal_frequency_squared_correction": str(
                generic["azimuthal_frequency_squared_correction"]
            ),
            "finite_e_fractional_correction": str(
                generic["finite_e_correction"]
            ),
        },
        "turning_point_parity": {
            "odd_mean_radius_linear": str(parity["odd_mean_radius_linear"]),
            "mean_radius_quadratic": str(parity["mean_radius_quadratic"]),
            "odd_mean_radius_cubic": str(parity["odd_mean_radius_cubic"]),
            "turning_equation_evenness_residual": str(
                parity["turning_equation_evenness_residual"]
            ),
            "radial_frequency_linear": str(parity["radial_frequency_linear"]),
            "radial_frequency_quadratic": str(
                parity["radial_frequency_quadratic"]
            ),
            "radial_frequency_cubic": str(parity["radial_frequency_cubic"]),
            "radial_frequency_cubic_negative_control": str(
                parity["radial_frequency_cubic_negative_control"]
            ),
            "azimuthal_mean_linear": str(parity["azimuthal_mean_linear"]),
            "azimuthal_mean_cubic": str(parity["azimuthal_mean_cubic"]),
            "signed_eccentricity_quadratic": str(
                parity["signed_eccentricity_quadratic"]
            ),
            "signed_eccentricity_quartic": str(
                parity["signed_eccentricity_quartic"]
            ),
            "observable_remainder": parity["observable_remainder"],
        },
        "exact_exponential": {
            "D": str(exact["D"]),
            "E": str(exact["E"]),
            "Ce": str(exact["Ce_explicit"]),
            "deep_limit": str(exact["deep_limit"]),
            "newton_limit": str(exact["newton_limit"]),
            "samples": samples,
        },
        "controls": {key: str(value) for key, value in controls.items()},
        "synthetic_nulls_e_0.03": synthetic,
        "distance_cancellation_residual": distance_cancellation_residual,
        "certificates": certificates,
        "nonclaims": [
            "not an all-orders eccentric-orbit solution",
            "not valid for extended mass, external field, or nonspherical sources",
            "not a relativistic closure result",
            "not a global novelty claim",
            "no uniform finite-e remainder bound; point inverses are asymptotic",
        ],
    }


def main() -> int:
    results = build_results()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
