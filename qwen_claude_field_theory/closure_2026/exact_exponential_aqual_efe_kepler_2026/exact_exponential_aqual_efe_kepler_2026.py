#!/usr/bin/env python3
"""Exact external-field clock laws of exponential AQUAL.

This module starts from the AQUAL action with

    G(y) = y^2 + 2(1+y) exp(-y) - 2,

so that G'(y)/(2y) = mu(y) = 1-exp(-y).  Linearizing the Euler--
Lagrange equation about a constant external field along z gives

    mu_e [d_x^2 + d_y^2 + (1+L_e)d_z^2] phi = 4 pi G rho,

where L_e=d ln(mu)/d ln(g).  The functions below derive two clock
experiments from that same operator: a point-mass nodal/Kepler law and
the boundary-matched harmonic tensor inside a prescribed uniform sphere.

Scope: this is an action-derived nonrelativistic AQUAL result in the
external-field-dominated limit.  It is not a relativistic completion.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class ExternalFieldParameters:
    eta: float
    mu: float
    L: float
    q: float


@dataclass(frozen=True)
class PointMassClockLaws:
    eta: float
    mu: float
    L: float
    q: float
    kepler_coefficient: float
    azimuthal_frequency_squared_coefficient: Optional[float]
    vertical_frequency_squared_coefficient: Optional[float]
    vertical_to_azimuthal_frequency: float
    vertical_to_azimuthal_period: float
    node_shift_per_azimuth_period: float
    node_shift_per_vertical_period: float


@dataclass(frozen=True)
class DepolarizationFactors:
    perpendicular: float
    parallel: float


@dataclass(frozen=True)
class CoreClockLaws:
    eta: float
    mu: float
    L: float
    q: float
    perpendicular_depolarization: float
    parallel_depolarization: float
    perpendicular_frequency_squared_coefficient: float
    parallel_frequency_squared_coefficient: float
    parallel_to_perpendicular_frequency_squared: float
    parallel_to_perpendicular_period: float
    old_local_operator_shortcut: float


@dataclass(frozen=True)
class SecularNodeLaw:
    eta: float
    mu: float
    L: float
    epsilon: float
    eccentricity: float
    inclination: float
    argument_of_periapsis: float
    alpha: float
    geometry_bracket: float
    node_shift_per_orbit: float
    perturbative_control: float


def _nonnegative_finite(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def action_primitive(y: float) -> float:
    """Return the dimensionless AQUAL primitive G(y), stably near y=0."""
    y = _nonnegative_finite(y, "y")
    if y < 1.0e-3:
        # 2 y^3/3 - y^4/4 + y^5/15 - y^6/72 + y^7/420 + O(y^8).
        return y**3 * (2.0 / 3.0 + y * (-1.0 / 4.0 + y * (1.0 / 15.0 + y * (-1.0 / 72.0 + y / 420.0))))
    return y * y + 2.0 * ((1.0 + y) * math.exp(-y) - 1.0)


def external_field_parameters(eta: float) -> ExternalFieldParameters:
    """Return mu_e, L_e, and q=1+L_e for eta=g_ext/a0.

    eta=0 is retained as a controlled one-sided mathematical limit.  The
    external-field-dominated approximation itself still requires a nonzero
    external field that dominates the internal acceleration.
    """
    eta = _nonnegative_finite(eta, "eta")
    if eta == 0.0:
        return ExternalFieldParameters(eta=0.0, mu=0.0, L=1.0, q=2.0)
    mu = -math.expm1(-eta)
    L = eta * math.exp(-eta) / mu
    return ExternalFieldParameters(eta=eta, mu=mu, L=L, q=1.0 + L)


def point_mass_clock_laws(eta: float) -> PointMassClockLaws:
    """Return the EFD point-mass Kepler and nodal clock coefficients.

    With cylindrical radius R and C=GM/mu_e, the exact Green potential is

        phi = -C / sqrt(z^2 + q R^2).

    For an infinitesimally inclined circular orbit about z=0,

        Omega_phi^2 = [GM/R^3] / [mu_e sqrt(q)],
        nu_z^2      = [GM/R^3] / [mu_e q^(3/2)].

    `kepler_coefficient` is the dimensionless factor K in
    T_phi^2 = 4*pi^2*K*R^3/(GM).  The two node shifts state explicitly
    whether the elapsed reference clock is one azimuthal or one vertical
    period, avoiding a common 2*pi convention ambiguity.
    """
    pars = external_field_parameters(eta)
    root_q = math.sqrt(pars.q)
    kepler = pars.mu * root_q
    if pars.mu == 0.0:
        omega_phi_coefficient = None
        omega_z_coefficient = None
    else:
        omega_phi_coefficient = 1.0 / (pars.mu * root_q)
        omega_z_coefficient = 1.0 / (pars.mu * pars.q * root_q)
    frequency_ratio = 1.0 / root_q
    return PointMassClockLaws(
        eta=pars.eta,
        mu=pars.mu,
        L=pars.L,
        q=pars.q,
        kepler_coefficient=kepler,
        azimuthal_frequency_squared_coefficient=omega_phi_coefficient,
        vertical_frequency_squared_coefficient=omega_z_coefficient,
        vertical_to_azimuthal_frequency=frequency_ratio,
        vertical_to_azimuthal_period=root_q,
        node_shift_per_azimuth_period=2.0 * math.pi * (1.0 - frequency_ratio),
        node_shift_per_vertical_period=2.0 * math.pi * (root_q - 1.0),
    )


def depolarization_factors(q: float) -> DepolarizationFactors:
    """Return N_perp,N_parallel for axes (1,1,1/sqrt(q)).

    The factors sum as 2*N_perp+N_parallel=1.  A series prevents the
    cancellation in xi-atan(xi) in the Newtonian q->1 limit.
    """
    q = float(q)
    if not math.isfinite(q) or q < 1.0:
        raise ValueError("q must be finite and at least one")
    t = q - 1.0
    if t < 1.0e-6:
        n_parallel = 1.0 / 3.0 + t * (
            2.0 / 15.0 + t * (-2.0 / 35.0 + t * (2.0 / 63.0 - 2.0 * t / 99.0))
        )
    else:
        xi = math.sqrt(t)
        n_parallel = (1.0 + xi * xi) * (xi - math.atan(xi)) / (xi**3)
    n_perpendicular = (1.0 - n_parallel) / 2.0
    return DepolarizationFactors(perpendicular=n_perpendicular, parallel=n_parallel)


def core_clock_laws(eta: float) -> CoreClockLaws:
    """Return the exact boundary-matched harmonic tensor of a uniform sphere.

    After z'=z/sqrt(q), the physical sphere becomes an oblate Newtonian
    ellipsoid.  Frequencies are reported in units of 4*pi*G*rho/mu_e:

        omega_perp^2     = base*N_perp,
        omega_parallel^2 = base*N_parallel/q.

    This is a prescribed-density response.  It does not assert that an
    isotropic distribution function self-consistently remains spherical.
    """
    pars = external_field_parameters(eta)
    factors = depolarization_factors(pars.q)
    perpendicular = factors.perpendicular
    parallel = factors.parallel / pars.q
    ratio_squared = parallel / perpendicular
    period_ratio = math.sqrt(1.0 / ratio_squared)
    return CoreClockLaws(
        eta=pars.eta,
        mu=pars.mu,
        L=pars.L,
        q=pars.q,
        perpendicular_depolarization=factors.perpendicular,
        parallel_depolarization=factors.parallel,
        perpendicular_frequency_squared_coefficient=perpendicular,
        parallel_frequency_squared_coefficient=parallel,
        parallel_to_perpendicular_frequency_squared=ratio_squared,
        parallel_to_perpendicular_period=period_ratio,
        old_local_operator_shortcut=1.0 / pars.q,
    )


def secular_node_law(
    eta: float,
    eccentricity: float,
    inclination: float,
    argument_of_periapsis: float,
) -> SecularNodeLaw:
    """Return the finite-e first-order secular EFD nodal advance.

    Expanding the exact external-field-dominated point potential as

        Phi = -k/[r sqrt(1-epsilon cos(theta)^2)]
            = -k/r - k*epsilon*cos(theta)^2/(2r) + O(epsilon^2),

    and averaging the perturbation over the Kepler eccentric anomaly gives

        P dot(Omega_node) = pi*epsilon*cos(i)/sqrt(1-e^2)
          * [1-alpha^2 cos(2 omega)] + O(epsilon^2),

    where alpha=e/[1+sqrt(1-e^2)].  Angles follow a right-handed frame
    with +z along the external field and prograde motion in +phi.
    """
    pars = external_field_parameters(eta)
    eccentricity = float(eccentricity)
    inclination = float(inclination)
    argument_of_periapsis = float(argument_of_periapsis)
    if not math.isfinite(eccentricity) or not 0.0 <= eccentricity < 1.0:
        raise ValueError("eccentricity must satisfy 0 <= e < 1")
    if not math.isfinite(inclination) or not math.isfinite(argument_of_periapsis):
        raise ValueError("orbit angles must be finite")
    epsilon = pars.L / pars.q
    s = math.sqrt(1.0 - eccentricity * eccentricity)
    alpha = eccentricity / (1.0 + s)
    bracket = 1.0 - alpha * alpha * math.cos(2.0 * argument_of_periapsis)
    shift = math.pi * epsilon * math.cos(inclination) * bracket / s
    return SecularNodeLaw(
        eta=pars.eta,
        mu=pars.mu,
        L=pars.L,
        epsilon=epsilon,
        eccentricity=eccentricity,
        inclination=inclination,
        argument_of_periapsis=argument_of_periapsis,
        alpha=alpha,
        geometry_bracket=bracket,
        node_shift_per_orbit=shift,
        perturbative_control=epsilon / s,
    )


def _audit_rows(etas: Iterable[float]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for eta in etas:
        point = point_mass_clock_laws(eta)
        core = core_clock_laws(eta)
        rows.append({"eta": float(eta), "point_mass": asdict(point), "uniform_core": asdict(core)})
    return rows


def build_certificate(etas: Iterable[float]) -> dict[str, object]:
    """Build a calculation certificate with live, falsifiable invariants."""
    rows = _audit_rows(etas)
    checks: dict[str, bool] = {}
    for index, row in enumerate(rows):
        core = row["uniform_core"]
        point = row["point_mass"]
        checks[f"trace_{index}"] = abs(
            2.0 * core["perpendicular_frequency_squared_coefficient"]
            + core["q"] * core["parallel_frequency_squared_coefficient"]
            - 1.0
        ) < 2.0e-13
        if point["azimuthal_frequency_squared_coefficient"] is None:
            checks[f"point_ratio_{index}"] = point["eta"] == 0.0
        else:
            checks[f"point_ratio_{index}"] = abs(
                point["vertical_frequency_squared_coefficient"]
                / point["azimuthal_frequency_squared_coefficient"]
                - 1.0 / point["q"]
            ) < 2.0e-13
        if core["eta"] == 0.0:
            checks[f"zero_field_degenerate_{index}"] = core["mu"] == 0.0 and core["q"] == 2.0
        else:
            checks[f"elliptic_{index}"] = core["mu"] > 0.0 and 1.0 <= core["q"] <= 2.0
    deep = core_clock_laws(0.0)
    checks["deep_boundary_matching_changes_old_shortcut"] = (
        abs(deep.parallel_to_perpendicular_frequency_squared - deep.old_local_operator_shortcut) > 0.25
    )
    node_samples = {
        "controlled_eta_6": asdict(secular_node_law(6.0, 0.3, math.radians(20.0), math.radians(40.0))),
        "frozen_eta_2p47812944": asdict(
            secular_node_law(2.47812944, 0.3, math.radians(20.0), math.radians(40.0))
        ),
    }
    checks["secular_geometry_bracket_positive"] = all(
        sample["geometry_bracket"] > 0.0 for sample in node_samples.values()
    )
    return {
        "status": (
            "PASS_NONRELATIVISTIC_EFD_CALCULATION"
            if all(checks.values())
            else "FAIL_NONRELATIVISTIC_EFD_CALCULATION"
        ),
        "scope": {
            "action_derived_nonrelativistic_AQUAL": True,
            "external_field_dominated_linearization": True,
            "relativistic_completion": False,
            "self_consistent_uniform_core_equilibrium": False,
            "global_novelty_claim": False,
        },
        "checks": checks,
        "rows": rows,
        "finite_eccentricity_node_samples": node_samples,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eta", type=float, action="append", dest="etas")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    etas = args.etas if args.etas is not None else [0.0, 0.1, 1.0, 2.47813, 10.0, 50.0]
    certificate = build_certificate(etas)
    rendered = json.dumps(certificate, indent=2, sort_keys=True, allow_nan=False)
    print(rendered)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if certificate["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
