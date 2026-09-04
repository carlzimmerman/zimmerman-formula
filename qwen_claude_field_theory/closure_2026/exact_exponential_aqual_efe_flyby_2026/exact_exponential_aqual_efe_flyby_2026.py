#!/usr/bin/env python3
"""Flyby and scattering laws of exponential AQUAL in its linear EFD regime.

Starting from the already-varied exponential AQUAL equation, linearization
about a constant external field gives

    mu_e (d_x^2 + d_y^2 + q d_z^2) phi = 4 pi G rho,

where mu_e=1-exp(-eta), q=1+eta/(exp(eta)-1), and eta=g_e/a0.
The point-source potential is

    phi(r) = -(GM/mu_e) / sqrt(r.T A r),   A=diag(q,q,1).

This module derives the straight-line (first-Born) three-dimensional flyby
impulse and exact results on the invariant equatorial plane z=0.  It does not
promote the EFD approximation to a relativistic completion or claim accuracy
outside the declared EFD and weak-deflection regimes.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import NamedTuple, Sequence

import numpy as np


class ExternalFieldParameters(NamedTuple):
    eta: float
    mu: float
    L: float
    q: float


class ImpulseGeometry(NamedTuple):
    trajectory_quadratic: float
    cross_term: float
    schur_distance_squared: float
    schur_matrix: np.ndarray


class EquatorialBoundOrbit(NamedTuple):
    kepler_constant: float
    semimajor_axis: float
    eccentricity: float
    sem_latus_rectum: float
    specific_energy: float
    specific_angular_momentum: float
    period: float


class EquatorialHyperbolicScattering(NamedTuple):
    kepler_constant: float
    impact_parameter: float
    v_inf: float
    eccentricity: float
    deflection_angle: float
    differential_cross_section: float


def _positive_finite(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return number


def _nonnegative_finite(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def _unit_vector(vector: Sequence[float], name: str) -> np.ndarray:
    array = np.asarray(vector, dtype=float)
    if array.shape != (3,) or not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must be a finite three-vector")
    norm = float(np.linalg.norm(array))
    if norm <= 0.0:
        raise ValueError(f"{name} must be nonzero")
    return array / norm


def _efd_q(q: float) -> float:
    q = float(q)
    if not math.isfinite(q) or q < 1.0 or q > 2.0:
        raise ValueError("q must lie in the exponential-AQUAL EFD range [1,2]")
    return q


def external_field_parameters(eta: float) -> ExternalFieldParameters:
    """Return the exact exponential-kernel EFD parameters.

    eta=0 is retained only as a one-sided ratio limit.  Since mu_e=0 there,
    absolute potentials, forces, and impulses reject that endpoint.
    """
    eta = _nonnegative_finite(eta, "eta")
    if eta == 0.0:
        return ExternalFieldParameters(eta=0.0, mu=0.0, L=1.0, q=2.0)
    mu = -math.expm1(-eta)
    L = eta * math.exp(-eta) / mu
    return ExternalFieldParameters(eta=eta, mu=mu, L=L, q=1.0 + L)


def anisotropy_matrix(q: float, external_axis: Sequence[float] = (0.0, 0.0, 1.0)) -> np.ndarray:
    """Return A=q I-(q-1)e e^T for a unit external-field direction e."""
    q = _efd_q(q)
    axis = _unit_vector(external_axis, "external_axis")
    return q * np.eye(3) - (q - 1.0) * np.outer(axis, axis)


def impulse_geometry(
    direction: Sequence[float],
    impact_parameter: Sequence[float],
    q: float,
    external_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> ImpulseGeometry:
    """Return the Gram/Schur data controlling a straight flyby."""
    n = _unit_vector(direction, "direction")
    b = np.asarray(impact_parameter, dtype=float)
    if b.shape != (3,) or not np.all(np.isfinite(b)):
        raise ValueError("impact_parameter must be a finite three-vector")
    bnorm = float(np.linalg.norm(b))
    if bnorm <= 0.0:
        raise ValueError("impact_parameter must be nonzero")
    if abs(float(np.dot(n, b))) > 2.0e-12 * bnorm:
        raise ValueError("impact_parameter must be perpendicular to direction")
    A = anisotropy_matrix(q, external_axis)
    An = A @ n
    a = float(n @ An)
    d = float(n @ A @ b)
    B = A - np.outer(An, An) / a
    D = float(b @ B @ b)
    if not D > 0.0:
        raise ValueError("the Schur-complement impact distance must be positive")
    return ImpulseGeometry(a, d, D, B)


def efd_potential(
    position: Sequence[float],
    gm: float,
    mu_e: float,
    q: float,
    external_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> float:
    """Return the internal point-source EFD potential."""
    gm = _positive_finite(gm, "gm")
    mu_e = _positive_finite(mu_e, "mu_e")
    r = np.asarray(position, dtype=float)
    if r.shape != (3,) or not np.all(np.isfinite(r)):
        raise ValueError("position must be a finite three-vector")
    A = anisotropy_matrix(q, external_axis)
    radius_squared = float(r @ A @ r)
    if radius_squared <= 0.0:
        raise ValueError("the point-source potential is singular at the origin")
    return -(gm / mu_e) / math.sqrt(radius_squared)


def efd_acceleration(
    position: Sequence[float],
    gm: float,
    mu_e: float,
    q: float,
    external_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> np.ndarray:
    """Return -grad(phi) for the point-source EFD Green potential."""
    gm = _positive_finite(gm, "gm")
    mu_e = _positive_finite(mu_e, "mu_e")
    r = np.asarray(position, dtype=float)
    if r.shape != (3,) or not np.all(np.isfinite(r)):
        raise ValueError("position must be a finite three-vector")
    A = anisotropy_matrix(q, external_axis)
    radius_squared = float(r @ A @ r)
    if radius_squared <= 0.0:
        raise ValueError("the point-source acceleration is singular at the origin")
    return -(gm / mu_e) * (A @ r) / radius_squared ** 1.5


def born_impulse(
    gm: float,
    mu_e: float,
    v_inf: float,
    direction: Sequence[float],
    impact_parameter: Sequence[float],
    q: float,
    external_axis: Sequence[float] = (0.0, 0.0, 1.0),
) -> np.ndarray:
    """Return the exact line integral along the unperturbed straight path.

    The result is exact for the first-Born surrogate r=b+v_inf*t*n.  It is not
    the exact generic three-dimensional scattering map of the curved orbit.
    """
    gm = _positive_finite(gm, "gm")
    mu_e = _positive_finite(mu_e, "mu_e")
    v_inf = _positive_finite(v_inf, "v_inf")
    n = _unit_vector(direction, "direction")
    b = np.asarray(impact_parameter, dtype=float)
    geometry = impulse_geometry(n, b, q, external_axis)
    A = anisotropy_matrix(q, external_axis)
    shifted_impact = b - n * geometry.cross_term / geometry.trajectory_quadratic
    prefactor = -2.0 * (gm / mu_e) / (
        v_inf
        * math.sqrt(geometry.trajectory_quadratic)
        * geometry.schur_distance_squared
    )
    return prefactor * (A @ shifted_impact)


def trajectory_anisotropy(q: float, theta: float) -> float:
    """Return a=n^T A n for trajectory/external-field angle theta."""
    q = _efd_q(q)
    theta = float(theta)
    if not math.isfinite(theta):
        raise ValueError("theta must be finite")
    return math.cos(theta) ** 2 + q * math.sin(theta) ** 2


def azimuth_magnitude_factor(trajectory_anisotropy: float, phi: float) -> float:
    """Return the generic impact-azimuth multiplier F(a,phi)."""
    a = float(trajectory_anisotropy)
    phi = float(phi)
    if not math.isfinite(a) or a < 1.0 or a > 2.0:
        raise ValueError("trajectory_anisotropy must lie in [1,2]")
    if not math.isfinite(phi):
        raise ValueError("phi must be finite")
    cosine_squared = math.cos(phi) ** 2
    sine_squared = math.sin(phi) ** 2
    return math.sqrt(cosine_squared + sine_squared / a**2) / (
        cosine_squared + sine_squared / a
    )


def maximum_azimuth_magnitude_factor(trajectory_anisotropy: float) -> float:
    a = float(trajectory_anisotropy)
    if not math.isfinite(a) or a < 1.0 or a > 2.0:
        raise ValueError("trajectory_anisotropy must lie in [1,2]")
    return (a + 1.0) / (2.0 * math.sqrt(a))


def parallel_to_perpendicular_impulse_ratio(q: float, impact_azimuth: float) -> float:
    """Compare parallel and perpendicular trajectories at equal M,b,v.

    For the perpendicular trajectory, impact_azimuth is measured in its impact
    plane from the eigenvector perpendicular to both the trajectory and the
    external field.  Only the two principal azimuths give exactly sqrt(q).
    """
    q = _efd_q(q)
    return math.sqrt(q) / azimuth_magnitude_factor(q, impact_azimuth)


def kick_misalignment(trajectory_anisotropy: float, impact_azimuth: float) -> float:
    """Return the unsigned angle between -Delta-v and the impact vector."""
    a = float(trajectory_anisotropy)
    phi = float(impact_azimuth)
    if not math.isfinite(a) or a < 1.0 or a > 2.0:
        raise ValueError("trajectory_anisotropy must lie in [1,2]")
    if not math.isfinite(phi):
        raise ValueError("impact_azimuth must be finite")
    numerator = (a - 1.0) * math.sin(phi) * math.cos(phi)
    denominator = a * math.cos(phi) ** 2 + math.sin(phi) ** 2
    return abs(math.atan2(numerator, denominator))


def maximum_kick_misalignment(trajectory_anisotropy: float) -> float:
    a = float(trajectory_anisotropy)
    if not math.isfinite(a) or a < 1.0 or a > 2.0:
        raise ValueError("trajectory_anisotropy must lie in [1,2]")
    return math.asin((a - 1.0) / (a + 1.0))


def anisotropic_rutherford_cross_section(
    gm: float,
    mu_e: float,
    v_inf: float,
    deflection_phi: float,
    deflection_theta: float,
    trajectory_anisotropy: float,
) -> float:
    """Return the generic 3-D small-angle Born differential cross-section.

    The two deflection components use the principal impact-plane basis.  Since
    dOmega=d(deflection_phi)d(deflection_theta) only at small angle, this is a
    Born/small-angle law, unlike `equatorial_hyperbolic_scattering` below.
    """
    gm = _positive_finite(gm, "gm")
    mu_e = _positive_finite(mu_e, "mu_e")
    v_inf = _positive_finite(v_inf, "v_inf")
    a = float(trajectory_anisotropy)
    if not math.isfinite(a) or a < 1.0 or a > 2.0:
        raise ValueError("trajectory_anisotropy must lie in [1,2]")
    angle_1 = float(deflection_phi)
    angle_2 = float(deflection_theta)
    if not math.isfinite(angle_1) or not math.isfinite(angle_2):
        raise ValueError("deflection components must be finite")
    angular_quadratic = angle_1**2 + a * angle_2**2
    if angular_quadratic <= 0.0:
        raise ValueError("the zero-deflection Coulomb cross-section diverges")
    return 4.0 * (gm / mu_e) ** 2 / (v_inf**4 * angular_quadratic**2)


def equatorial_kepler_constant(gm: float, mu_e: float, q: float) -> float:
    """Return k_e=GM/(mu_e sqrt(q)) on the invariant plane z=0."""
    gm = _positive_finite(gm, "gm")
    mu_e = _positive_finite(mu_e, "mu_e")
    q = _efd_q(q)
    return gm / (mu_e * math.sqrt(q))


def equatorial_conic_radius(sem_latus_rectum: float, eccentricity: float, true_anomaly: float) -> float:
    """Return r=p/(1+e cos f) on any allowed equatorial Kepler conic."""
    p = _positive_finite(sem_latus_rectum, "sem_latus_rectum")
    e = _nonnegative_finite(eccentricity, "eccentricity")
    f = float(true_anomaly)
    if not math.isfinite(f):
        raise ValueError("true_anomaly must be finite")
    denominator = 1.0 + e * math.cos(f)
    if denominator <= 0.0:
        raise ValueError("true_anomaly lies outside the physical branch of this conic")
    return p / denominator


def equatorial_bound_orbit(
    k_e: float,
    semimajor_axis: float,
    eccentricity: float,
) -> EquatorialBoundOrbit:
    """Return exact ellipse invariants and the finite-e Kepler period."""
    k_e = _positive_finite(k_e, "k_e")
    semimajor_axis = _positive_finite(semimajor_axis, "semimajor_axis")
    eccentricity = _nonnegative_finite(eccentricity, "eccentricity")
    if eccentricity >= 1.0:
        raise ValueError("a bound ellipse requires 0 <= eccentricity < 1")
    p = semimajor_axis * (1.0 - eccentricity**2)
    return EquatorialBoundOrbit(
        kepler_constant=k_e,
        semimajor_axis=semimajor_axis,
        eccentricity=eccentricity,
        sem_latus_rectum=p,
        specific_energy=-k_e / (2.0 * semimajor_axis),
        specific_angular_momentum=math.sqrt(k_e * p),
        period=2.0 * math.pi * math.sqrt(semimajor_axis**3 / k_e),
    )


def equatorial_hyperbolic_scattering(
    k_e: float,
    impact_parameter: float,
    v_inf: float,
) -> EquatorialHyperbolicScattering:
    """Return the exact attractive-Kepler hyperbolic scattering observables."""
    k_e = _positive_finite(k_e, "k_e")
    impact_parameter = _positive_finite(impact_parameter, "impact_parameter")
    v_inf = _positive_finite(v_inf, "v_inf")
    half_angle_tangent = k_e / (impact_parameter * v_inf**2)
    angle = 2.0 * math.atan(half_angle_tangent)
    eccentricity = math.sqrt(1.0 + 1.0 / half_angle_tangent**2)
    cross_section = k_e**2 / (
        4.0 * v_inf**4 * math.sin(angle / 2.0) ** 4
    )
    return EquatorialHyperbolicScattering(
        kepler_constant=k_e,
        impact_parameter=impact_parameter,
        v_inf=v_inf,
        eccentricity=eccentricity,
        deflection_angle=angle,
        differential_cross_section=cross_section,
    )


def calculation_certificate() -> dict:
    """Build a strict-JSON certificate from live evaluations."""
    eta_rows = []
    for eta in (0.0, 0.1, 0.5, 1.0, 2.0, 2.47812944, 5.0, 10.0):
        params = external_field_parameters(eta)
        eta_rows.append(
            {
                "eta": eta,
                "mu_e": params.mu,
                "L_e": params.L,
                "q": params.q,
                "principal_parallel_to_perpendicular_ratio": math.sqrt(params.q),
                "maximum_azimuth_factor": maximum_azimuth_magnitude_factor(params.q),
                "maximum_kick_misalignment_radians": maximum_kick_misalignment(params.q),
            }
        )

    generic_q = 2.0
    generic_phi = math.pi / 4.0
    k_e = equatorial_kepler_constant(12.0, 0.75, 16.0 / 9.0)
    bound = equatorial_bound_orbit(k_e, 3.0, 0.5)
    hyperbolic = equatorial_hyperbolic_scattering(2.0, 3.0, 2.0)
    axis_impulse = born_impulse(3.0, 0.5, 4.0, [0, 0, 1], [2, 0, 0], 1.6)

    checks = {
        "axis_impulse_finite": bool(np.all(np.isfinite(axis_impulse))),
        "axis_impulse_transverse": abs(float(axis_impulse[2])) < 1.0e-14,
        "generic_azimuth_is_not_principal": azimuth_magnitude_factor(generic_q, generic_phi) > 1.0,
        "generic_ratio_below_sqrt_q": parallel_to_perpendicular_impulse_ratio(generic_q, generic_phi)
        < math.sqrt(generic_q),
        "deep_misalignment_below_twenty_degrees": maximum_kick_misalignment(2.0)
        < math.radians(20.0),
        "equatorial_period_positive": bound.period > 0.0,
        "hyperbolic_eccentricity_above_one": hyperbolic.eccentricity > 1.0,
        "hyperbolic_angle_between_zero_and_pi": 0.0 < hyperbolic.deflection_angle < math.pi,
    }
    passed = all(checks.values())
    return {
        "schema_version": 1,
        "status": (
            "PASS_FORMAL_EFD_FLYBY_CALCULATION_WITH_DECLARED_BOUNDS"
            if passed
            else "FAIL_INTERNAL_CHECK"
        ),
        "checks": checks,
        "eta_rows": eta_rows,
        "generic_deep_limit_example": {
            "impact_azimuth_radians": generic_phi,
            "azimuth_magnitude_factor": azimuth_magnitude_factor(generic_q, generic_phi),
            "parallel_to_perpendicular_ratio": parallel_to_perpendicular_impulse_ratio(
                generic_q, generic_phi
            ),
            "principal_ratio": math.sqrt(generic_q),
            "maximum_factor": maximum_azimuth_magnitude_factor(generic_q),
        },
        "axis_impulse_example": axis_impulse.tolist(),
        "equatorial_bound_example": bound._asdict(),
        "equatorial_hyperbolic_example": hyperbolic._asdict(),
        "scope": {
            "generic_3d_result": "first Born order in the linearized EFD Green potential",
            "equatorial_result": "exact orbit dynamics within the linearized EFD Green potential",
            "zero_field": "eta=0 retained only in finite ratios; absolute impulse is undefined",
            "relativistic_completion": False,
            "global_novelty_claim": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = calculation_certificate()
    payload = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
