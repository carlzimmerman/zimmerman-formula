#!/usr/bin/env python3
"""Exact inverse and distinct prediction rails for mu(y)=1-exp(-y).

The repository's historical ``Route A`` function

    nu_RA(x) = 1 / (1-exp(-sqrt(x)))

is an empirical shortcut.  It is not the inverse of the required field law.
For x=g_N/a0 and y=g/a0 the exact spherical/circular relation is

    x = y * (1-exp(-y)),        nu_exact(x) = y(x)/x.

This module keeps both functions under explicit names, computes the monotone
implicit inverse, and exposes twelve distinct observational channels with an
explicit dependency graph.  Some follow from the kernel alone, others require
an AQUAL modified-gravity branch, and lensing channels additionally require a
metric completion.  They are not advertised as independent laws or as results
of a closed relativistic action.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import sys
from typing import Any

import numpy as np
import sympy as sp


def _nonnegative_finite_values(value: Any, name: str) -> np.ndarray:
    values = np.asarray(value, dtype=float)
    if np.any(~np.isfinite(values)) or np.any(values < 0.0):
        raise ValueError(f"{name} must be finite and nonnegative")
    return values


def mu(y: Any) -> Any:
    """Preferred interpolation function, evaluated stably near zero."""

    values = _nonnegative_finite_values(y, "y")
    result = -np.expm1(-values)
    if result.ndim == 0:
        return float(result)
    return result


def flux_x(y: Any) -> Any:
    """Dimensionless AQUAL flux x(y)=y*mu(y)."""

    values = _nonnegative_finite_values(y, "y")
    result = values * (-np.expm1(-values))
    if result.ndim == 0:
        return float(result)
    return result


def lambda_perpendicular(y: Any) -> Any:
    """Tangential constitutive eigenvalue."""

    return mu(y)


def lambda_parallel(y: Any) -> Any:
    """Longitudinal constitutive eigenvalue dx/dy=mu+y*mu'."""

    values = _nonnegative_finite_values(y, "y")
    result = -np.expm1(-values) + values * np.exp(-values)
    if result.ndim == 0:
        return float(result)
    return result


def logarithmic_mu_slope(y: Any) -> Any:
    """L=d ln(mu)/d ln(y), with its continuous y=0 value."""

    values = _nonnegative_finite_values(y, "y")
    # y/(exp(y)-1) is algebraically identical to
    # y*exp(-y)/(1-exp(-y)); the latter cannot overflow in the Newtonian tail.
    decay = np.exp(-values)
    numerator = values * decay
    denominator = -np.expm1(-values)
    result = np.divide(
        numerator,
        denominator,
        out=np.ones_like(values),
        where=values != 0.0,
    )
    if result.ndim == 0:
        return float(result)
    return result


def _exact_inverse_scalar(x: float) -> float:
    if not math.isfinite(x) or x < 0.0:
        raise ValueError("x must be finite and nonnegative")
    if x == 0.0:
        return 0.0

    # x(y) is strictly increasing for y>0 because lambda_parallel>0.
    low = 0.0
    high = max(1.0, x + 1.0)
    guess = math.sqrt(x) + x / 4.0 if x < 1.0 else x
    y = min(max(guess, low), high)

    for _ in range(120):
        residual = y * (-math.expm1(-y)) - x
        if residual > 0.0:
            high = y
        elif residual < 0.0:
            low = y
        else:
            return y

        derivative = -math.expm1(-y) + y * math.exp(-y)
        newton = y - residual / derivative if derivative > 0.0 else math.nan
        if not math.isfinite(newton) or not (low < newton < high):
            newton = 0.5 * (low + high)
        y = newton

        # The inverse is y~sqrt(x) in the deep regime.  Scaling this stopping
        # test to one (rather than to y) loses relative accuracy precisely as
        # x->0 because dx/dy~2y.  Stop at the local floating-point scale.
        local_scale = max(abs(y), math.sqrt(np.finfo(float).tiny))
        if high - low <= 4.0 * np.finfo(float).eps * local_scale:
            break
    return y


def exact_inverse_y(x: Any) -> Any:
    """Solve x=y(1-exp(-y)) without replacing y by sqrt(x)."""

    values = _nonnegative_finite_values(x, "x")
    if values.ndim == 0:
        return _exact_inverse_scalar(float(values))
    result = np.empty_like(values)
    iterator = np.nditer(values, flags=["multi_index"])
    for value in iterator:
        result[iterator.multi_index] = _exact_inverse_scalar(float(value))
    return result


def exact_nu(x: Any) -> Any:
    """Exact boost nu(x)=y(x)/x; infinite at the mathematical x=0 point."""

    values = _nonnegative_finite_values(x, "x")
    y_values = exact_inverse_y(values)
    result = np.divide(
        y_values,
        values,
        out=np.full_like(values, np.inf),
        where=values != 0.0,
    )
    if result.ndim == 0:
        return float(result)
    return result


def route_a_nu(x: Any) -> Any:
    """Historical shortcut retained under a name that cannot be confused."""

    values = _nonnegative_finite_values(x, "x")
    denominator = -np.expm1(-np.sqrt(values))
    result = np.divide(
        1.0,
        denominator,
        out=np.full_like(values, np.inf),
        where=values != 0.0,
    )
    if result.ndim == 0:
        return float(result)
    return result


def deep_inverse_coefficients() -> tuple[float, float, float]:
    """Derive y=sqrt(x)+a*x+b*x^(3/2)+... by coefficient matching."""

    t = sp.symbols("t", positive=True)
    a, b = sp.symbols("a b")
    trial = t + a * t**2 + b * t**3
    residual = sp.series(
        trial * (1 - sp.exp(-trial)) - t**2,
        t,
        0,
        5,
    ).removeO()
    solution = sp.solve(
        [sp.expand(residual).coeff(t, 3), sp.expand(residual).coeff(t, 4)],
        [a, b],
        dict=True,
    )[0]
    return (1.0, float(solution[a]), float(solution[b]))


@dataclass(frozen=True)
class Prediction:
    number: int
    title: str
    equation: str
    observable: str
    scope: str
    status: str
    dependencies: tuple[int, ...]
    observable_key: str


PREDICTIONS = (
    Prediction(
        1,
        "Exact circular acceleration relation",
        "x=y(1-exp(-y)); g=a0*y(x)",
        "Resolved rotation curves / radial-acceleration relation",
        "Spherical AQUAL; circular MI only if the same map is separately postulated",
        "exact-kernel",
        (),
        "circular-force-map",
    ),
    Prediction(
        2,
        "Point-mass radial slope",
        "d ln g/d ln r=-2/(1+L); d ln v_c/d ln r=(L-1)/(2(1+L))",
        "Multi-radius exterior rotation/dynamical slopes",
        "Exterior point-mass spherical AQUAL with L=y/(exp(y)-1)",
        "conditional-AQUAL",
        (1,),
        "radial-shape",
    ),
    Prediction(
        3,
        "Epicycle and apsidal precession",
        "kappa^2/Omega^2=3-2/(1+L); Delta_varpi=2pi(Omega/kappa-1)",
        "Near-circular test-particle apsidal precession",
        "Exterior point mass, isolated central AQUAL potential; not comparable-mass or EFE dominated",
        "conditional-AQUAL",
        (2,),
        "noncircular-frequency",
    ),
    Prediction(
        4,
        "Deep isolated pressure virial",
        "<v^2>_M=(2/3)sqrt(GMa0)[1-Sum_i(m_i/M)^(3/2)]; sigma_los^4=(4/81)GMa0[1-Sum_i(m_i/M)^(3/2)]^2",
        "Globular clusters and isolated pressure-supported systems",
        "Deep, isolated, equilibrated, globally sampled, spherical and nonrotating; continuum coefficient drops the finite-mass term",
        "conditional-AQUAL",
        (),
        "pressure-virial",
    ),
    Prediction(
        5,
        "Resolved Jeans profile",
        "sigma_r^2=[n f_beta]^-1 int_r^inf n(s)f_beta(s)g(s)ds; f_beta=exp[int 2 beta dr/r]",
        "Proper-motion plus line-of-sight dispersion profiles",
        "Generic spherical Jeans pipeline supplied with AQUAL g, boundary condition, measured tracer density and anisotropy",
        "conditional-AQUAL",
        (1,),
        "resolved-pressure-profile",
    ),
    Prediction(
        6,
        "Local constitutive response anisotropy",
        "partial_i[(lambda_perp Pperp_ij+lambda_parallel n_i n_j)partial_j deltaPhi]=4piG delta rho",
        "Radial/transverse baryonic bumps, vertical/planar force, lensing shape",
        "Linear response of exact AQUAL about y>0; lensing requires a separate metric completion",
        "conditional-AQUAL",
        (),
        "local-response-tensor",
    ),
    Prediction(
        7,
        "External-field anisotropic Green function",
        "phi=-GM/[mu_e sqrt(1+L_e)]*(R_perp^2+z^2/(1+L_e))^(-1/2)",
        "Orientation-binned binaries, satellites, or lensing quadrupoles",
        "Uniform y_e>0 AQUAL field with internal field much smaller than external; derived from rail 6",
        "conditional-AQUAL",
        (6,),
        "efe-anisotropy",
    ),
    Prediction(
        8,
        "External-field ending radius and escape law",
        "r_EFE~sqrt(GMa0)/g_e; v_esc^2=2sqrt(GMa0)[ln(r_EFE/r)+C(theta;y_e)]",
        "Outer escape speeds and the radius where lensing steepens",
        "Asymptotic matching estimate inside the EFE radius; C and escape surface need the outer BVP; lensing is additional",
        "conditional-AQUAL",
        (1, 7),
        "efe-ending-radius",
    ),
    Prediction(
        9,
        "Solar external-field quadrupole",
        "Q_ij=Q2(e_i e_j-delta_ij/3); |Q2|=(3/2)(a0/r_M)|q| for q=Q_zz r_M/a0",
        "Cassini ranging and planetary ephemerides",
        "Full nonlinear nonspherical BVP; AQUAL and QUMOND q are distinct and must be solved separately; not derived from the linear-response channel",
        "conditional-AQUAL",
        (),
        "solar-quadrupole",
    ),
    Prediction(
        10,
        "Pair-minus-sum non-superposition",
        "Delta gamma_t[rho1,rho2]=gamma_t[rho1+rho2]-gamma_t[rho1]-gamma_t[rho2] is generically not identically zero",
        "Pair-versus-isolated weak lensing",
        "Proposed nonlinear functional; amplitude/sign require the full nonlinear operator, profiles, separation, environment, projection and a metric completion; not derived from the linear-response channel",
        "conditional-no-slip",
        (),
        "nonlinear-pair-lensing",
    ),
    Prediction(
        11,
        "No-slip lensing/dynamics equality",
        "g_lens=-grad(Phi+Psi)/2=-grad Phi=g_dyn; alpha_deep(b;R)=4sqrt(GMa0)c^-2 atan(sqrt(R^2-b^2)/b) -> 2pi sqrt(GMa0)/c^2",
        "Joint lensing and orbital dynamics",
        "Physical metric with Phi=Psi; 2pi is the b/R->0 limit before the EFE/outer transition",
        "conditional-no-slip",
        (1,),
        "lensing-dynamics-rail",
    ),
    Prediction(
        12,
        "Metric gravitational-redshift profile",
        "z_1to2=[Phi(r2)-Phi(r1)]/c^2=sqrt(GMa0)c^-2 ln(r2/r1); c z=DeltaPhi/c",
        "Stacked satellite/galaxy gravitational redshifts",
        "Both radii exterior to baryons and inside the deep pre-EFE region; AQUAL Phi must be the minimally coupled physical lapse; no slip not required",
        "conditional-physical-lapse",
        (1,),
        "metric-redshift",
    ),
)


def derive_symbolic_identities() -> dict[str, Any]:
    y = sp.symbols("y", positive=True)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu_symbolic = 1 - sp.exp(-y)
    parallel = sp.simplify(mu_symbolic + y * sp.diff(mu_symbolic, y))
    return {
        "primitive": primitive,
        "primitive_residual": sp.simplify(sp.diff(primitive, y) / (2 * y) - mu_symbolic),
        "parallel": parallel,
        "parallel_derivative": sp.simplify(sp.diff(parallel, y)),
        "parallel_zero_limit": sp.limit(parallel, y, 0, dir="+"),
        "parallel_at_one": sp.simplify(parallel.subs(y, 1)),
        "deep_primitive": sp.series(primitive, y, 0, 6),
    }


def derive_prediction_identities() -> dict[str, Any]:
    """Executable algebra behind the bankable subset of the channel ledger."""

    logarithmic_slope, enclosed_mass_slope = sp.symbols(
        "L m", nonnegative=True
    )
    dlog_x_dlog_r = enclosed_mass_slope - 2
    dlog_y_dlog_r = sp.simplify(
        dlog_x_dlog_r / (1 + logarithmic_slope)
    )
    spherical_slope_residual = sp.simplify(
        dlog_y_dlog_r
        - (enclosed_mass_slope - 2) / (1 + logarithmic_slope)
    )
    point_mass_slope = dlog_y_dlog_r.subs(enclosed_mass_slope, 0)
    epicycle_ratio = sp.simplify(3 + point_mass_slope)
    epicycle_residual = sp.simplify(
        epicycle_ratio
        - (1 + 3 * logarithmic_slope) / (1 + logarithmic_slope)
    )

    x_coordinate, y_coordinate, z_coordinate = sp.symbols(
        "x_coordinate y_coordinate z_coordinate", real=True
    )
    external_slope = sp.symbols("L_e", positive=True)
    anisotropic_radius = sp.sqrt(
        x_coordinate**2
        + y_coordinate**2
        + z_coordinate**2 / (1 + external_slope)
    )
    green_shape = 1 / anisotropic_radius
    efe_green_vacuum_residual = sp.factor(
        sp.diff(green_shape, x_coordinate, 2)
        + sp.diff(green_shape, y_coordinate, 2)
        + (1 + external_slope) * sp.diff(green_shape, z_coordinate, 2)
    )

    quadrupole_amplitude, q_zz, a0_symbol, r_m = sp.symbols(
        "Q2 q_zz a0 r_M", nonzero=True
    )
    Q_zz = sp.Rational(2, 3) * quadrupole_amplitude
    q_definition = sp.Eq(q_zz, Q_zz * r_m / a0_symbol)
    solved_Q2 = sp.solve(q_definition, quadrupole_amplitude)[0]
    quadrupole_conversion_residual = sp.simplify(
        solved_Q2 - sp.Rational(3, 2) * a0_symbol * q_zz / r_m
    )

    impact_parameter, line_coordinate, cutoff, speed_squared, c_symbol = sp.symbols(
        "b z Z v_sq c", positive=True
    )
    ray_integral = sp.integrate(
        impact_parameter / (impact_parameter**2 + line_coordinate**2),
        (line_coordinate, -cutoff, cutoff),
    )
    finite_deflection = sp.simplify(
        2 * speed_squared * ray_integral / c_symbol**2
    )
    finite_deflection_limit_residual = sp.simplify(
        sp.limit(finite_deflection, cutoff, sp.oo)
        - 2 * sp.pi * speed_squared / c_symbol**2
    )

    delta_phi = sp.symbols("Delta_Phi", real=True)
    redshift = delta_phi / c_symbol**2
    redshift_velocity_residual = sp.simplify(
        c_symbol * redshift - delta_phi / c_symbol
    )

    return {
        "dlog_x_dlog_r": dlog_x_dlog_r,
        "dlog_y_dlog_r": dlog_y_dlog_r,
        "spherical_slope_residual": spherical_slope_residual,
        "epicycle_ratio": epicycle_ratio,
        "epicycle_residual": epicycle_residual,
        "efe_green_shape": green_shape,
        "efe_green_vacuum_residual": efe_green_vacuum_residual,
        "quadrupole_definition": q_definition,
        "quadrupole_amplitude": solved_Q2,
        "quadrupole_conversion_residual": quadrupole_conversion_residual,
        "finite_deflection": finite_deflection,
        "finite_deflection_limit_residual": finite_deflection_limit_residual,
        "redshift_velocity_residual": redshift_velocity_residual,
    }


def _check(label: str, condition: Any, detail: str = "") -> bool:
    passed = bool(condition)
    suffix = f" ({detail})" if detail else ""
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}{suffix}")
    return passed


def main() -> int:
    identities = derive_symbolic_identities()
    prediction_identities = derive_prediction_identities()
    checks: list[bool] = []

    print("=" * 96)
    print("EXACT EXPONENTIAL-MU INVERSE AND TWELVE SCOPED OBSERVATIONAL CHANNELS")
    print("=" * 96)

    print("\n[1] Action-kernel identities")
    print("  G(y) =", identities["primitive"])
    print("  G'(y)/(2y)-mu(y) =", identities["primitive_residual"])
    print("  lambda_parallel =", identities["parallel"])
    print("  d lambda_parallel/dy =", identities["parallel_derivative"])
    print("  deep G =", identities["deep_primitive"])
    checks.append(_check("the exact primitive differentiates to mu", identities["primitive_residual"] == 0))
    y_symbol = next(iter(identities["parallel"].free_symbols))
    # On 0<y<=1 the derivative (2-y)e^-y is positive and lambda rises
    # from zero to one.  For y>=1, lambda=1+(y-1)e^-y is manifestly >=1.
    checks.append(_check(
        "lambda_parallel is positive by its two analytic branches",
        identities["parallel_zero_limit"] == 0
        and identities["parallel_at_one"] == 1
        and sp.simplify(
            identities["parallel_derivative"] / sp.exp(-y_symbol)
        ) == 2 - y_symbol,
    ))

    print("\n[2] Implicit inverse versus historical Route A")
    anchors = np.array([0.01, 0.1, 1.0, 10.0])
    exact_y = exact_inverse_y(anchors)
    exact_boost = exact_nu(anchors)
    route_boost = route_a_nu(anchors)
    bias = route_boost / exact_boost - 1.0
    for x, y_value, n_exact, n_route, delta in zip(
        anchors, exact_y, exact_boost, route_boost, bias
    ):
        print(
            f"  x={x:5.2g} y_exact={y_value:.12g} "
            f"nu_exact={n_exact:.9g} nu_RA={n_route:.9g} "
            f"RA/exact-1={100*delta:+.3f}%"
        )
    residual = np.max(np.abs(flux_x(exact_y) / anchors - 1.0))
    checks.append(_check("the numerical inverse closes x=y*mu(y)", residual < 2e-13, f"max relative residual={residual:.3e}"))
    checks.append(_check("Route A is detectably different near the transition", np.max(bias) > 0.1, f"max bias={100*np.max(bias):.2f}%"))

    print("\n[3] Controlled asymptotic calculations")
    coefficients = deep_inverse_coefficients()
    print("  y(x) = sqrt(x) +", coefficients[1], "x +", coefficients[2], "x^(3/2) + ...")
    deep_x = 1e-10
    deep_y = exact_inverse_y(deep_x)
    deep_series = math.sqrt(deep_x) + coefficients[1] * deep_x + coefficients[2] * deep_x**1.5
    checks.append(_check("derived deep inverse matches the exact solve", abs(deep_y / deep_series - 1.0) < 1e-9))
    newtonian_x = 20.0
    newtonian_y = exact_inverse_y(newtonian_x)
    scaled_tail = (newtonian_y - newtonian_x) / (
        newtonian_x * math.exp(-newtonian_x)
    )
    checks.append(_check(
        "Newtonian recovery has the derived exponential leading correction",
        abs(scaled_tail - 1.0) < 1e-5,
        f"(y-x)/(x exp(-x))={scaled_tail:.9g}",
    ))

    print("\n[4] Executable identities behind the bankable channels")
    print("  d ln y/d ln r =", prediction_identities["dlog_y_dlog_r"])
    print("  kappa^2/Omega^2 =", prediction_identities["epicycle_ratio"])
    print("  anisotropic Green shape =", prediction_identities["efe_green_shape"])
    print("  Q2 from q_zz =", prediction_identities["quadrupole_amplitude"])
    print("  finite deep deflection =", prediction_identities["finite_deflection"])
    checks.append(_check(
        "slope, epicycle, EFE Green, quadrupole, deflection and redshift identities close",
        all(
            prediction_identities[name] == 0
            for name in (
                "spherical_slope_residual",
                "epicycle_residual",
                "efe_green_vacuum_residual",
                "quadrupole_conversion_residual",
                "finite_deflection_limit_residual",
                "redshift_velocity_residual",
            )
        ),
    ))

    print("\n[5] Twelve observable channels and their dependencies")
    for entry in PREDICTIONS:
        print(f"  {entry.number:2d}. {entry.title} [{entry.status}]")
        print(f"      {entry.equation}")
        print(f"      observable: {entry.observable}")
        print(f"      scope: {entry.scope}")
        print(f"      depends on channels: {entry.dependencies or 'base'}")
    keys = [entry.observable_key for entry in PREDICTIONS]
    dependency_graph_is_ordered = all(
        all(dependency < entry.number for dependency in entry.dependencies)
        for entry in PREDICTIONS
    )
    checks.append(_check("the ledger contains exactly twelve scoped channels", len(PREDICTIONS) == 12, f"count={len(PREDICTIONS)}"))
    checks.append(_check("the channels have distinct observable keys", len(keys) == len(set(keys))))
    checks.append(_check(
        "the dependency graph is explicit and acyclic",
        dependency_graph_is_ordered and any(entry.dependencies for entry in PREDICTIONS),
    ))
    checks.append(_check(
        "no kernel rail is mislabeled as a closed relativistic action result",
        all(entry.status != "closed-relativistic-action" for entry in PREDICTIONS),
    ))

    print("\n[SCOPE]")
    print("  Exact-kernel rows follow from x=y(1-exp(-y)).")
    print("  Conditional-AQUAL rows additionally assume the nonlinear modified-gravity field equation.")
    print("  Conditional-no-slip rows also require a relativistic physical metric with Phi=Psi.")
    print("  These are twelve observational channels, not twelve mathematically independent laws.")
    print("  None of these labels substitutes for a full action/Dirac/PPN/stability certificate.")

    passed = sum(checks)
    print(f"\nChecks completed: {passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
