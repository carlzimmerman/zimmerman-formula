#!/usr/bin/env python3
"""Hardened Cassini quadrupole audit for exact-exponential QUMOND.

This file does *not* certify AQUAL or a relativistic completion.  It evaluates the
standard QUMOND external-field quadrupole for the physical interpolation law

    mu(g/a0) = 1 - exp(-g/a0).

The inverse function is computed from its defining equation rather than replacing
its argument by ``sqrt(g_N/a0)``.  Two independent integration algorithms are
used: adaptive nested Gauss--Kronrod quadrature and a shell-split tensor-product
Gauss--Legendre rule.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import platform
import warnings
from typing import Callable, Union

import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy import integrate
from scipy.optimize import brentq


# Physical inputs.  GM_SUN is the IAU nominal solar mass parameter in SI units.
GM_SUN = 1.32712440018e20
A0_CANONICAL = 9.3619e-11
A0_ALTERNATE = 1.1279e-10
G_EXTERNAL = 2.32e-10
PARK_Q2_CENTRAL = 1.6e-27
PARK_Q2_SIGMA = 1.8e-27
PARK_Q2_2SIGMA_CEILING = PARK_Q2_CENTRAL + 2.0 * PARK_Q2_SIGMA


NumericInput = Union[np.ndarray, float]
ArrayFunction = Callable[[NumericInput], NumericInput]


@dataclass(frozen=True)
class QuadratureResult:
    q: float
    reported_error: float
    method: str
    radial_max: float
    order: int | None = None


def mu_exponential(true_y: np.ndarray | float) -> np.ndarray | float:
    """Return mu(y)=1-exp(-y), where ``true_y`` is g/a0 (not g_N/a0)."""

    values = np.asarray(true_y, dtype=float)
    if np.any(values < 0.0):
        raise ValueError("true acceleration y=g/a0 must be non-negative")
    result = -np.expm1(-values)
    return float(result) if result.ndim == 0 else result


def _inverse_scalar(newtonian_x: float) -> float:
    """Solve x=y(1-exp(-y)) for y, with x=g_N/a0 and y=g/a0."""

    x = float(newtonian_x)
    if not math.isfinite(x) or x < 0.0:
        raise ValueError("Newtonian acceleration x=g_N/a0 must be finite and non-negative")
    if x == 0.0:
        return 0.0

    def residual(y: float) -> float:
        return y * (-math.expm1(-y)) - x

    upper = x + math.sqrt(x) + 2.0
    return float(
        brentq(
            residual,
            0.0,
            upper,
            xtol=np.nextafter(0.0, 1.0),
            rtol=4.0 * np.finfo(float).eps,
        )
    )


def _inverse_array(newtonian_x: np.ndarray) -> np.ndarray:
    """Vector Newton solve, with bracketed scalar fallback for difficult entries."""

    x = np.asarray(newtonian_x, dtype=float)
    if np.any(~np.isfinite(x)) or np.any(x < 0.0):
        raise ValueError("Newtonian acceleration x=g_N/a0 must be finite and non-negative")
    y = np.zeros_like(x)
    active = x > 0.0
    if not np.any(active):
        return y

    xa = x[active]
    ya = np.empty_like(xa)
    small = xa < 1.0
    root_x = np.sqrt(xa[small])
    # Series gives an accurate, positive seed in the deep-MOND regime.
    ya[small] = root_x + 0.25 * xa[small] + (7.0 / 96.0) * xa[small] * root_x
    medium = (~small) & (xa < 50.0)
    ya[medium] = xa[medium] + xa[medium] * np.exp(-xa[medium]) / (
        1.0 - np.exp(-xa[medium])
    )
    ya[xa >= 50.0] = xa[xa >= 50.0]

    for _ in range(16):
        exp_minus = np.exp(-ya)
        mu = -np.expm1(-ya)
        residual = ya * mu - xa
        derivative = mu + ya * exp_minus
        step = residual / derivative
        candidate = ya - step
        ya = np.where(candidate > 0.0, candidate, 0.5 * ya)
        if np.max(np.abs(residual) / np.maximum(xa, 1.0e-300)) < 2.0e-14:
            break

    relative_residual = np.abs(ya * (-np.expm1(-ya)) - xa) / np.maximum(xa, 1.0e-300)
    failed = (~np.isfinite(relative_residual)) | (relative_residual > 5.0e-13)
    if np.any(failed):
        failed_indices = np.flatnonzero(failed)
        for index in failed_indices:
            ya[index] = _inverse_scalar(float(xa[index]))
    y[active] = ya
    return y


def exact_inverse_total_acceleration(
    newtonian_x: np.ndarray | float,
) -> np.ndarray | float:
    """Return true ``y=g/a0`` from Newtonian ``x=g_N/a0`` for exact exponential mu."""

    values = np.asarray(newtonian_x, dtype=float)
    if values.ndim == 0:
        return _inverse_scalar(float(values))
    return _inverse_array(values)


def nu_exponential_exact(newtonian_x: np.ndarray | float) -> np.ndarray | float:
    """Exact QUMOND nu(x)=g/g_N, whose argument is x=g_N/a0."""

    values = np.asarray(newtonian_x, dtype=float)
    if np.any(values < 0.0):
        raise ValueError("Newtonian acceleration x=g_N/a0 must be non-negative")
    inverse = np.asarray(exact_inverse_total_acceleration(values), dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        result = inverse / values
    result = np.where(values == 0.0, math.inf, result)
    return float(result) if result.ndim == 0 else result


def nu_minus_one_exponential_exact(
    newtonian_x: np.ndarray | float,
) -> np.ndarray | float:
    """Return exact ``nu(x)-1`` without subtractive cancellation at large x."""

    values = np.asarray(newtonian_x, dtype=float)
    inverse = np.asarray(exact_inverse_total_acceleration(values), dtype=float)
    exp_minus = np.exp(-inverse)
    denominator = -np.expm1(-inverse)
    with np.errstate(divide="ignore", invalid="ignore"):
        result = exp_minus / denominator
    result = np.where(values == 0.0, math.inf, result)
    return float(result) if result.ndim == 0 else result


def newtonian_external_from_true_eta(true_eta: float) -> float:
    """Map eta=g_ext/a0 to e_N=g_N,ext/a0 using the physical mu law."""

    eta = float(true_eta)
    if eta < 0.0 or not math.isfinite(eta):
        raise ValueError("external-field eta must be finite and non-negative")
    return eta * float(mu_exponential(eta))


def _external_newtonian_for_kernel(true_eta: float, nu_minus_one: ArrayFunction) -> float:
    if true_eta == 0.0:
        return 0.0
    if nu_minus_one is nu_minus_one_exponential_exact:
        return newtonian_external_from_true_eta(true_eta)

    def residual(e_newtonian: float) -> float:
        delta_nu = float(np.asarray(nu_minus_one(e_newtonian), dtype=float))
        return e_newtonian * (1.0 + delta_nu) - true_eta

    return float(
        brentq(
            residual,
            np.nextafter(0.0, 1.0),
            true_eta,
            xtol=np.nextafter(0.0, 1.0),
            rtol=4.0 * np.finfo(float).eps,
        )
    )


def _quadrupole_polynomial(e_newtonian: float, v: np.ndarray, xi: np.ndarray) -> np.ndarray:
    return e_newtonian * (3.0 * xi - 5.0 * xi**3) + v**2 * (1.0 - 3.0 * xi**2)


def q_direct_adaptive(
    true_eta: float,
    *,
    radial_max: float,
    absolute_tolerance: float = 1.0e-12,
    relative_tolerance: float = 1.0e-10,
    nu_minus_one: ArrayFunction = nu_minus_one_exponential_exact,
) -> QuadratureResult:
    """Direct nested adaptive quadrature over v and xi, with warnings promoted to errors."""

    eta = float(true_eta)
    if eta < 0.0 or radial_max <= 0.0:
        raise ValueError("eta must be non-negative and radial_max must be positive")
    if eta == 0.0:
        return QuadratureResult(0.0, 0.0, "adaptive-dblquad", radial_max)
    e_newtonian = _external_newtonian_for_kernel(eta, nu_minus_one)

    def integrand(xi: float, v: float) -> float:
        discriminant = e_newtonian**2 + v**4 + 2.0 * e_newtonian * v**2 * xi
        if discriminant <= 0.0:
            return 0.0
        magnitude = math.sqrt(discriminant)
        delta_nu = float(np.asarray(nu_minus_one(magnitude), dtype=float))
        polynomial = e_newtonian * (3.0 * xi - 5.0 * xi**3) + v**2 * (
            1.0 - 3.0 * xi**2
        )
        return delta_nu * polynomial

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        value, error = integrate.dblquad(
            integrand,
            0.0,
            radial_max,
            lambda _v: -1.0,
            lambda _v: 1.0,
            epsabs=absolute_tolerance,
            epsrel=relative_tolerance,
        )
    return QuadratureResult(abs(1.5 * float(value)), 1.5 * float(error), "adaptive-dblquad", radial_max)


def _default_radial_splits(e_newtonian: float, radial_max: float) -> np.ndarray:
    critical_radius = math.sqrt(e_newtonian)
    proposed = [
        0.0,
        0.5 * critical_radius,
        0.9 * critical_radius,
        critical_radius,
        1.1 * critical_radius,
        2.0 * critical_radius,
        4.0,
        radial_max,
    ]
    retained = [point for point in proposed if 0.0 <= point <= radial_max]
    retained.extend([0.0, radial_max])
    return np.unique(np.asarray(retained, dtype=float))


def q_split_gauss(
    true_eta: float,
    *,
    radial_max: float,
    order: int,
    nu_minus_one: ArrayFunction = nu_minus_one_exponential_exact,
) -> QuadratureResult:
    """Independent fixed-order Gauss rule split at the cancellation shell v=sqrt(e_N)."""

    eta = float(true_eta)
    if eta < 0.0 or radial_max <= 0.0 or order < 2:
        raise ValueError("eta/radial_max/order outside the supported domain")
    if eta == 0.0:
        return QuadratureResult(0.0, 0.0, "split-gauss-legendre", radial_max, order)
    e_newtonian = _external_newtonian_for_kernel(eta, nu_minus_one)
    nodes, weights = leggauss(order)
    xi = nodes[None, :]
    xi_weights = weights[None, :]
    integral = 0.0

    splits = _default_radial_splits(e_newtonian, radial_max)
    for lower, upper in zip(splits[:-1], splits[1:]):
        half_width = 0.5 * (upper - lower)
        midpoint = 0.5 * (upper + lower)
        v = (midpoint + half_width * nodes)[:, None]
        radial_weights = weights[:, None]
        discriminant = e_newtonian**2 + v**4 + 2.0 * e_newtonian * v**2 * xi
        magnitude = np.sqrt(np.maximum(discriminant, 0.0))
        delta_nu = np.asarray(nu_minus_one(magnitude), dtype=float)
        polynomial = _quadrupole_polynomial(e_newtonian, v, xi)
        integral += half_width * float(
            np.sum(radial_weights * xi_weights * delta_nu * polynomial)
        )

    return QuadratureResult(abs(1.5 * integral), 0.0, "split-gauss-legendre", radial_max, order)


def radial_tail_bound(true_eta: float, *, radial_min: float) -> float:
    """Rigorous absolute bound on the omitted exact-mu QUMOND tail above radial_min.

    For v^2>e_N and v^2-e_N>=log(2), ``nu-1 <= 2 exp(e_N-v^2)``.
    Also ``|3 xi-5 xi^3|<=2`` and ``|1-3 xi^2|<=2`` on [-1,1].
    Applying these bounds to the full angular interval and the 3/2 prefactor gives

        |q_tail| <= 12 exp(e_N) int_V^inf (e_N+v^2) exp(-v^2) dv.
    """

    eta = float(true_eta)
    v_min = float(radial_min)
    if eta < 0.0 or v_min <= 0.0:
        raise ValueError("eta must be non-negative and radial_min must be positive")
    if eta == 0.0:
        return 0.0
    e_newtonian = newtonian_external_from_true_eta(eta)
    if v_min**2 <= e_newtonian or v_min**2 - e_newtonian < math.log(2.0):
        raise ValueError("radial_min is too small for the certified exponential-tail inequality")
    gaussian_tail = (
        0.5 * v_min * math.exp(-(v_min**2))
        + math.sqrt(math.pi) * (0.5 * e_newtonian + 0.25) * math.erfc(v_min)
    )
    return 12.0 * math.exp(e_newtonian) * gaussian_tail


def q2_from_q(q: float, *, a0: float, central_mass_parameter: float) -> float:
    """Convert dimensionless QUMOND q to Q2 in inverse seconds squared."""

    if q < 0.0 or a0 <= 0.0 or central_mass_parameter <= 0.0:
        raise ValueError("q must be non-negative and dimensional inputs positive")
    return 1.5 * a0**1.5 * q / math.sqrt(central_mass_parameter)


def _check(condition: bool, label: str, failures: list[str]) -> None:
    marker = "PASS" if condition else "FAIL"
    print(f"[{marker}] {label}")
    if not condition:
        failures.append(label)


def run_certificate() -> bool:
    """Run all numerical cross-checks; return True when the computation is certified."""

    warnings.simplefilter("error")
    failures: list[str] = []
    eta = G_EXTERNAL / A0_CANONICAL
    e_newtonian = newtonian_external_from_true_eta(eta)

    print("EXACT-EXPONENTIAL QUMOND CASSINI CONVERGENCE CERTIFICATE")
    print("SCOPE: QUMOND ONLY; NOT AQUAL; NOT A RELATIVISTIC-ACTION CERTIFICATE")
    print(f"python={platform.python_version()} numpy={np.__version__} scipy={scipy.__version__}")
    print(f"script_sha256={hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
    print(f"GM_sun={GM_SUN:.12e} m^3 s^-2")
    print(f"a0={A0_CANONICAL:.12e} m s^-2")
    print(f"g_external={G_EXTERNAL:.12e} m s^-2")
    print(f"eta_true=g_external/a0={eta:.15g}")
    print(f"e_N=eta_true*mu(eta_true)={e_newtonian:.15g}")
    print()

    inverse_grid = np.logspace(-14.0, 6.0, 161)
    true_grid = np.asarray(exact_inverse_total_acceleration(inverse_grid), dtype=float)
    reconstructed = true_grid * np.asarray(mu_exponential(true_grid), dtype=float)
    inverse_relative_error = float(
        np.max(np.abs(reconstructed - inverse_grid) / inverse_grid)
    )
    print(f"inverse_max_relative_residual={inverse_relative_error:.6e}")
    _check(inverse_relative_error < 5.0e-12, "exact inverse closes x=y[1-exp(-y)]", failures)

    direct6 = q_direct_adaptive(
        eta,
        radial_max=6.0,
        absolute_tolerance=1.0e-12,
        relative_tolerance=1.0e-10,
    )
    direct10 = q_direct_adaptive(
        eta,
        radial_max=10.0,
        absolute_tolerance=1.0e-12,
        relative_tolerance=1.0e-10,
    )
    print(
        f"direct_adaptive_v6 q={direct6.q:.15g} "
        f"reported_error={direct6.reported_error:.6e}"
    )
    print(
        f"direct_adaptive_v10 q={direct10.q:.15g} "
        f"reported_error={direct10.reported_error:.6e}"
    )

    split_results = [
        q_split_gauss(eta, radial_max=6.0, order=order)
        for order in (32, 64, 128, 256)
    ]
    for result in split_results:
        print(f"split_gauss_v6_order{result.order} q={result.q:.15g}")
    delta_32_64 = abs(split_results[1].q - split_results[0].q)
    delta_64_128 = abs(split_results[2].q - split_results[1].q)
    delta_128_256 = abs(split_results[3].q - split_results[2].q)
    print(f"order_delta_32_64={delta_32_64:.6e}")
    print(f"order_delta_64_128={delta_64_128:.6e}")
    print(f"order_delta_128_256={delta_128_256:.6e}")
    _check(
        delta_128_256 < delta_64_128 < delta_32_64,
        "split-rule order sequence converges",
        failures,
    )

    tail6 = radial_tail_bound(eta, radial_min=6.0)
    direct_domain_delta = abs(direct10.q - direct6.q)
    direct_domain_allowance = tail6 + direct6.reported_error + direct10.reported_error
    print(f"analytic_tail_bound_v6={tail6:.6e}")
    print(f"direct_domain_delta_v6_v10={direct_domain_delta:.6e}")
    _check(
        direct_domain_delta <= 4.0 * direct_domain_allowance,
        "adaptive domain change is covered by reported error plus analytic tail",
        failures,
    )
    _check(tail6 < 1.0e-12, "analytic tail above v=6 is negligible", failures)

    finest_split = split_results[-1]
    independent_delta = abs(finest_split.q - direct6.q)
    independent_allowance = 5.0 * delta_128_256 + direct6.reported_error + tail6
    print(f"independent_method_delta={independent_delta:.6e}")
    print(f"independent_method_allowance={independent_allowance:.6e}")
    _check(
        independent_delta <= independent_allowance,
        "adaptive and split quadrature agree within observed convergence allowance",
        failures,
    )

    split6_96 = q_split_gauss(eta, radial_max=6.0, order=96)
    split10_96 = q_split_gauss(eta, radial_max=10.0, order=96)
    split_domain_delta = abs(split10_96.q - split6_96.q)
    print(f"split_domain_delta_v6_v10_order96={split_domain_delta:.6e}")
    _check(
        split_domain_delta <= tail6 + 3.0e-10,
        "split-rule domain scan is stable",
        failures,
    )

    def newtonian_nu_minus_one(value: np.ndarray | float) -> np.ndarray:
        return np.zeros_like(np.asarray(value, dtype=float))

    mutation_newton = q_split_gauss(
        eta,
        radial_max=6.0,
        order=32,
        nu_minus_one=newtonian_nu_minus_one,
    ).q
    mutation_eta_zero = q_split_gauss(0.0, radial_max=6.0, order=32).q
    print(f"mutation_nu_equals_one_q={mutation_newton:.15g}")
    print(f"mutation_eta_equals_zero_q={mutation_eta_zero:.15g}")
    _check(mutation_newton == 0.0, "nu=1 mutation annihilates the phantom quadrupole", failures)
    _check(mutation_eta_zero == 0.0, "eta=0 mutation annihilates the EFE quadrupole", failures)

    q_final = direct6.q
    q2 = q2_from_q(q_final, a0=A0_CANONICAL, central_mass_parameter=GM_SUN)
    ceiling_ratio = q2 / PARK_Q2_2SIGMA_CEILING
    sigma_offset = (q2 - PARK_Q2_CENTRAL) / PARK_Q2_SIGMA
    print()
    print(f"q_adopted={q_final:.15g}")
    print(f"Q2={q2:.12e} s^-2")
    print(f"Park_2sigma_ceiling={PARK_Q2_2SIGMA_CEILING:.12e} s^-2")
    print(f"Q2_over_ceiling={ceiling_ratio:.9f}")
    print(f"offset_from_Park_central={sigma_offset:.9f} sigma")
    if q2 > PARK_Q2_2SIGMA_CEILING:
        print("PHYSICAL VERDICT: exact-mu QUMOND is above the adopted Cassini 2-sigma ceiling.")
    else:
        print("PHYSICAL VERDICT: exact-mu QUMOND is not excluded by this adopted ceiling.")

    # The repository carries two a0 footings.  Recompute the dimensionless
    # external field and the integral for the alternate value; rescaling the
    # canonical q would be wrong because q depends on eta=g_ext/a0.
    alternate_eta = G_EXTERNAL / A0_ALTERNATE
    alternate_direct = q_direct_adaptive(
        alternate_eta,
        radial_max=6.0,
        absolute_tolerance=1.0e-12,
        relative_tolerance=1.0e-10,
    )
    alternate_split = q_split_gauss(
        alternate_eta, radial_max=6.0, order=256
    )
    alternate_tail = radial_tail_bound(alternate_eta, radial_min=6.0)
    alternate_delta = abs(alternate_direct.q - alternate_split.q)
    alternate_allowance = (
        alternate_direct.reported_error + alternate_tail + 1.0e-8
    )
    alternate_q2 = q2_from_q(
        alternate_direct.q,
        a0=A0_ALTERNATE,
        central_mass_parameter=GM_SUN,
    )
    alternate_ratio = alternate_q2 / PARK_Q2_2SIGMA_CEILING
    print()
    print("[ALTERNATE a0 FOOTING]")
    print(f"a0_alternate={A0_ALTERNATE:.12e} m s^-2")
    print(f"eta_true_alternate={alternate_eta:.15g}")
    print(f"q_adaptive_alternate={alternate_direct.q:.15g}")
    print(f"q_split256_alternate={alternate_split.q:.15g}")
    print(f"independent_delta_alternate={alternate_delta:.6e}")
    print(f"Q2_alternate={alternate_q2:.12e} s^-2")
    print(f"Q2_over_ceiling_alternate={alternate_ratio:.9f}")
    _check(
        alternate_delta <= alternate_allowance,
        "alternate-footing adaptive and split quadratures agree",
        failures,
    )
    _check(
        alternate_q2 > PARK_Q2_2SIGMA_CEILING,
        "alternate a0 footing also exceeds the adopted ceiling",
        failures,
    )

    print()
    if failures:
        print(f"NUMERICAL CERTIFICATE: FAIL ({len(failures)} failed checks)")
        return False
    print("NUMERICAL CERTIFICATE: PASS (the exclusion result, not the theory, is certified)")
    return True


def main() -> int:
    return 0 if run_certificate() else 1


if __name__ == "__main__":
    raise SystemExit(main())
