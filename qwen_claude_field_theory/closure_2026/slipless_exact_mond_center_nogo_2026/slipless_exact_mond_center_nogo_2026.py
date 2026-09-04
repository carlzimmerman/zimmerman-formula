#!/usr/bin/env python3
"""Symbolic audit of the force-free-center obstruction in exact MOND.

The calculation separates three statements:

1. spherical exact exponential AQUAL fixes a Puiseux, rather than Taylor,
   acceleration at a positive-density force-free center;
2. the Puiseux lapse term is embedded in a one-metric weak field, with the
   spatial potential retained independently;
3. direct construction and contraction of the linearized Riemann tensor tests
   whether either zero slip or arbitrary slip can keep curvature regular.

Nothing in this module assigns the final curvature coefficients or the MOND
root.  They are generated from the constitutive equation and tensor algebra.
"""

from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path
from typing import Dict, Tuple

import sympy as sp


def derive_exponential_puiseux(*, a0: sp.Expr, b: sp.Expr) -> Dict[int, sp.Expr]:
    """Derive g(r)=c1*r^(1/2)+c2*r+c3*r^(3/2)+... from mu(g/a0)g=b*r.

    ``b`` is the coefficient of the enclosed-source acceleration.  For a
    smooth baryonic core in the requested MOND equation,
    b=4*pi*G*rho_0/3.  The positive root is selected because ``g`` denotes
    the inward acceleration magnitude.
    """

    z = sp.symbols("z", positive=True)
    c1, c2, c3 = sp.symbols("c1 c2 c3")
    g = c1 * z + c2 * z**2 + c3 * z**3
    residual = sp.series(
        g * (1 - sp.exp(-g / a0)) - b * z**2, z, 0, 5
    ).removeO().expand()

    equation_2 = sp.expand(residual).coeff(z, 2)
    positive_c1 = sp.sqrt(a0 * b)
    if sp.simplify(equation_2.subs(c1, positive_c1)) != 0:
        raise AssertionError("positive leading MOND root does not solve z^2 balance")

    equation_3 = sp.expand(residual.subs(c1, positive_c1)).coeff(z, 3)
    solutions_c2 = sp.solve(sp.Eq(equation_3, 0), c2)
    if len(solutions_c2) != 1:
        raise AssertionError(f"expected one c2 solution, found {solutions_c2}")
    solved_c2 = sp.simplify(solutions_c2[0])

    equation_4 = sp.expand(
        residual.subs({c1: positive_c1, c2: solved_c2})
    ).coeff(z, 4)
    solutions_c3 = sp.solve(sp.Eq(equation_4, 0), c3)
    if len(solutions_c3) != 1:
        raise AssertionError(f"expected one c3 solution, found {solutions_c3}")
    solved_c3 = sp.simplify(solutions_c3[0])

    return {1: positive_c1, 2: solved_c2, 3: solved_c3}


def derive_operator_eigenvalues(y: sp.Expr) -> Tuple[sp.Expr, sp.Expr]:
    """Derive the transverse/longitudinal flux-Jacobian eigenvalues."""

    mu = 1 - sp.exp(-y)
    return sp.simplify(mu), sp.simplify(mu + y * sp.diff(mu, y))


def derive_inner_kepler_series(
    *, a0: sp.Expr, b: sp.Expr, sqrt_radius: sp.Expr
) -> sp.Expr:
    """Derive v_c^4/r^3=g^2/r through O(r) for the exponential kernel."""

    coefficients = derive_exponential_puiseux(a0=a0, b=b)
    z = sqrt_radius
    acceleration = sum(coefficients[order] * z**order for order in coefficients)
    return sp.expand(sp.series(acceleration**2 / z**2, z, 0, 3).removeO())


def _radial_hessian_on_axis(
    amplitude: sp.Expr, power: sp.Expr, radius: sp.Expr
) -> sp.Matrix:
    """Cartesian Hessian of amplitude*r**power on the positive x axis."""

    radial = sp.simplify(amplitude * power * (power - 1) * radius ** (power - 2))
    tangential = sp.simplify(amplitude * power * radius ** (power - 2))
    return sp.diag(radial, tangential, tangential)


def linearized_radial_hessian_curvature_on_axis(
    *,
    phi_radial: sp.Expr,
    phi_tangential: sp.Expr,
    psi_radial: sp.Expr,
    psi_tangential: sp.Expr,
) -> Tuple[sp.Expr, sp.Expr]:
    """Construct curvature from independent radial Hessian eigenvalues.

    All four inputs are Hessian eigenvalues of the dimensionless potentials
    Phi/c^2 and Psi/c^2.  No radial power law or derivative asymptotic is
    assumed here.
    """

    phi_hessian = sp.diag(phi_radial, phi_tangential, phi_tangential)
    psi_hessian = sp.diag(psi_radial, psi_tangential, psi_tangential)
    eta = (-1, 1, 1, 1)

    def second_h(mu: int, nu: int, alpha: int, beta: int) -> sp.Expr:
        if alpha == 0 or beta == 0:
            return sp.S.Zero
        i, j = alpha - 1, beta - 1
        if mu == 0 and nu == 0:
            return -2 * phi_hessian[i, j]
        if mu == nu and mu > 0:
            return -2 * psi_hessian[i, j]
        return sp.S.Zero

    riemann: Dict[Tuple[int, int, int, int], sp.Expr] = {}
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    riemann[(rho, sigma, mu, nu)] = sp.simplify(
                        (
                            second_h(rho, nu, sigma, mu)
                            + second_h(sigma, mu, rho, nu)
                            - second_h(rho, mu, sigma, nu)
                            - second_h(sigma, nu, rho, mu)
                        )
                        / 2
                    )

    ricci = [[sp.S.Zero for _ in range(4)] for _ in range(4)]
    for sigma in range(4):
        for nu in range(4):
            ricci[sigma][nu] = sp.simplify(
                sum(
                    eta[rho] * riemann[(rho, sigma, rho, nu)]
                    for rho in range(4)
                )
            )
    ricci_scalar = sp.simplify(
        sum(eta[index] * ricci[index][index] for index in range(4))
    )

    kretschmann = sp.simplify(
        sum(
            eta[rho]
            * eta[sigma]
            * eta[mu]
            * eta[nu]
            * riemann[(rho, sigma, mu, nu)] ** 2
            for rho in range(4)
            for sigma in range(4)
            for mu in range(4)
            for nu in range(4)
        )
    )
    return ricci_scalar, kretschmann


def linearized_radial_curvature_on_axis(
    *,
    power: sp.Expr,
    phi_amplitude: sp.Expr,
    psi_amplitude: sp.Expr,
    radius: sp.Expr,
) -> Tuple[sp.Expr, sp.Expr]:
    """Construct R and R_abcd R^abcd for radial weak potentials.

    Conventions are signature (-,+,+,+), x^0=ct, and

        g_00=-(1+2 Phi/c^2),  g_ij=(1-2 Psi/c^2) delta_ij.

    The amplitudes passed here are those of the dimensionless potentials
    ``Phi/c^2`` and ``Psi/c^2``.  Thus callers that start with physical
    acceleration coefficients must divide the integrated-potential amplitudes
    by ``c^2``.  The calculation is linear in the Riemann tensor and quadratic
    in that tensor for the leading Kretschmann invariant.
    """

    power = sp.sympify(power)
    phi_hessian = _radial_hessian_on_axis(phi_amplitude, power, radius)
    psi_hessian = _radial_hessian_on_axis(psi_amplitude, power, radius)
    return linearized_radial_hessian_curvature_on_axis(
        phi_radial=phi_hessian[0, 0],
        phi_tangential=phi_hessian[1, 1],
        psi_radial=psi_hessian[0, 0],
        psi_tangential=psi_hessian[1, 1],
    )


def derive_generic_center_scaling(
    *,
    mu_power: sp.Expr,
    mu_coefficient: sp.Expr,
    a0: sp.Expr,
    b: sp.Expr,
    radius: sp.Expr,
    speed_of_light: sp.Expr = sp.S.One,
) -> dict:
    """Derive the center class for mu(y)=kappa*y**n+o(y**n), n>0.

    Balancing powers and positive coefficients in

        kappa*(g/a0)**n*g = b*r

    fixes both the radial exponent and its coefficient.  Curvature is then
    obtained by feeding the integrated potential into the same tensor builder
    used for the exponential and Schwarzschild cases.
    """

    n = sp.sympify(mu_power)
    kappa = sp.sympify(mu_coefficient)
    acceleration_power = sp.simplify(1 / (n + 1))
    acceleration_coefficient = sp.simplify(
        (b * a0**n / kappa) ** acceleration_power
    )
    potential_power = sp.simplify(1 + acceleration_power)
    c_light = sp.sympify(speed_of_light)
    potential_amplitude = sp.simplify(
        acceleration_coefficient / (potential_power * c_light**2)
    )
    ricci, kretschmann = linearized_radial_curvature_on_axis(
        power=potential_power,
        phi_amplitude=potential_amplitude,
        psi_amplitude=potential_amplitude,
        radius=radius,
    )
    return {
        "acceleration_power": acceleration_power,
        "acceleration_coefficient": acceleration_coefficient,
        "potential_power": potential_power,
        "Ricci_scalar": sp.simplify(ricci),
        "Kretschmann": sp.simplify(kretschmann),
        "derivative_hypothesis": "r*g'(r)/g(r) -> 1/(n+1)",
    }


def derive_value_asymptotic_curvature_lower_bound(
    *,
    mu_power: sp.Expr,
    mu_coefficient: sp.Expr,
    a0: sp.Expr,
    source_coefficient: sp.Expr,
    radius: sp.Expr,
    speed_of_light: sp.Expr = sp.S.One,
) -> dict:
    """Derive the no-go without differentiating a little-o remainder.

    Value asymptotics alone fix g/r.  The tensor contraction is first built
    with all other radial Hessian eigenvalues independent, then minimized over
    them.  The surviving tangential electric term is therefore a genuine lower
    bound even when g' has no asymptotic limit.
    """

    n = sp.sympify(mu_power)
    kappa = sp.sympify(mu_coefficient)
    b = sp.sympify(source_coefficient)
    c_light = sp.sympify(speed_of_light)
    s = sp.simplify(1 / (n + 1))
    coefficient = sp.simplify((b * a0**n / kappa) ** s)

    phi_rr, phi_tt, psi_rr, psi_tt = sp.symbols(
        "phi_rr phi_tt psi_rr psi_tt", real=True
    )
    _, general_k = linearized_radial_hessian_curvature_on_axis(
        phi_radial=phi_rr,
        phi_tangential=phi_tt,
        psi_radial=psi_rr,
        psi_tangential=psi_tt,
    )
    free = (phi_rr, psi_rr, psi_tt)
    stationary = sp.solve(
        [sp.diff(general_k, variable) for variable in free],
        free,
        dict=True,
    )
    if len(stationary) != 1:
        raise AssertionError(f"expected one curvature minimizer, got {stationary}")
    quadratic_hessian = sp.hessian(general_k, free)
    principal_minors = tuple(
        sp.factor(quadratic_hessian[:size, :size].det())
        for size in range(1, len(free) + 1)
    )
    minimum_at_fixed_phi_tt = sp.factor(general_k.subs(stationary[0]))
    physical_phi_tt = sp.simplify(
        coefficient * radius ** (s - 1) / c_light**2
    )
    lower_bound = sp.simplify(
        minimum_at_fixed_phi_tt.subs(phi_tt, physical_phi_tt)
    )
    return {
        "acceleration_power": s,
        "acceleration_coefficient": coefficient,
        "general_Kretschmann": sp.factor(general_k),
        "minimizer_at_fixed_phi_tangential": stationary[0],
        "quadratic_hessian_principal_minors": principal_minors,
        "tangential_K_lower_bound": lower_bound,
        "tangential_K_lower_bound_power": sp.simplify(2 * s - 2),
        "uses_derivative_asymptotics": False,
    }


def derive_arbitrary_slip_center_curvature(
    *,
    acceleration_power: sp.Expr,
    phi_acceleration_coefficient: sp.Expr,
    psi_acceleration_coefficient: sp.Expr,
    radius: sp.Expr,
    speed_of_light: sp.Expr = sp.S.One,
) -> dict:
    """Derive curvature when Phi' and Psi' have independent leading terms.

    The input coefficients multiply ``r**acceleration_power``.  This makes it
    possible to test directly whether gravitational slip can remove the tidal
    singularity generated by the dynamical time potential.
    """

    s = sp.sympify(acceleration_power)
    c_light = sp.sympify(speed_of_light)
    potential_power = sp.simplify(s + 1)
    phi_amplitude = sp.simplify(
        phi_acceleration_coefficient / (potential_power * c_light**2)
    )
    psi_amplitude = sp.simplify(
        psi_acceleration_coefficient / (potential_power * c_light**2)
    )
    ricci, kretschmann = linearized_radial_curvature_on_axis(
        power=potential_power,
        phi_amplitude=phi_amplitude,
        psi_amplitude=psi_amplitude,
        radius=radius,
    )
    return {
        "Ricci_scalar": sp.factor(ricci),
        "Kretschmann": sp.factor(kretschmann),
    }


def derive_density_power_threshold(
    *, mu_power: sp.Expr, density_power: sp.Expr
) -> dict:
    """Derive the source-vanishing order needed for finite center curvature.

    If rho_eff is asymptotic to r**m, the enclosed-source acceleration is
    asymptotic to r**(m+1).  Matching this to mu(g/a0)g with mu~y**n fixes
    the remaining exponents without assuming their values.
    """

    n = sp.sympify(mu_power)
    m = sp.sympify(density_power)
    source_acceleration_power = sp.simplify(m + 1)
    acceleration_power = sp.simplify(source_acceleration_power / (n + 1))
    ricci_power = sp.simplify(acceleration_power - 1)
    kretschmann_lower_bound_power = sp.simplify(2 * ricci_power)
    return {
        "source_acceleration_power": source_acceleration_power,
        "acceleration_power": acceleration_power,
        "formal_Ricci_scalar_power_with_derivative_control": ricci_power,
        "Kretschmann_tangential_lower_bound_power": kretschmann_lower_bound_power,
        "regularity_claim": "necessary_not_sufficient",
    }


def derive_symbolic_certificate() -> dict:
    """Build live pass/fail predicates from the derivations themselves."""

    a0, b, r, c_light = sp.symbols("a0 b r c_light", positive=True)
    n, kappa = sp.symbols("n kappa", positive=True)
    z = sp.symbols("z", positive=True)

    coefficients = derive_exponential_puiseux(a0=a0, b=b)
    g = sum(coefficients[order] * z**order for order in coefficients)
    residual = sp.series(
        g * (1 - sp.exp(-g / a0)) - b * z**2, z, 0, 5
    ).removeO()
    series_solves_equation = sp.simplify(residual) == 0

    lower = derive_value_asymptotic_curvature_lower_bound(
        mu_power=n,
        mu_coefficient=kappa,
        a0=a0,
        source_coefficient=b,
        radius=r,
        speed_of_light=c_light,
    )
    lower_bound_exponent_is_negative = (
        sp.ask(sp.Q.negative(lower["tangential_K_lower_bound_power"])) is True
    )
    curvature_quadratic_is_positive = all(
        sp.ask(sp.Q.positive(minor)) is True
        for minor in lower["quadratic_hessian_principal_minors"]
    )
    lower_bound_is_strictly_positive = (
        sp.ask(sp.Q.positive(lower["tangential_K_lower_bound"])) is True
    )

    y = sp.symbols("y", positive=True)
    transverse, longitudinal = derive_operator_eigenvalues(y)
    zero_field_rank_loss = (
        sp.limit(transverse, y, 0, dir="+") == 0
        and sp.limit(longitudinal, y, 0, dir="+") == 0
    )
    off_zero_sample_ellipticity = all(
        transverse.subs(y, sample).is_positive
        and longitudinal.subs(y, sample).is_positive
        for sample in (sp.Rational(1, 100), sp.Rational(1, 2), 1, 10)
    )

    checks = {
        "exponential_puiseux_solves_constitutive_series": series_solves_equation,
        "curvature_quadratic_positive_definite": curvature_quadratic_is_positive,
        "tangential_lower_bound_positive": lower_bound_is_strictly_positive,
        "value_asymptotic_lower_bound_diverges_for_n_positive":
            lower_bound_exponent_is_negative,
        "zero_field_flux_jacobian_loses_rank": zero_field_rank_loss,
        "sampled_off_zero_flux_jacobian_positive": off_zero_sample_ellipticity,
    }
    return {"checks": checks, "passed": all(checks.values())}


def derive_audit_results() -> dict:
    """Run all symbolic derivations and return serializable evidence."""

    a0, b, radius, acceleration_coefficient, c_light = sp.symbols(
        "a0 b r C c_light", positive=True
    )
    y = sp.symbols("y", positive=True)
    puiseux = derive_exponential_puiseux(a0=a0, b=b)
    sqrt_radius = sp.symbols("sqrt_r", positive=True)
    inner_kepler = derive_inner_kepler_series(
        a0=a0, b=b, sqrt_radius=sqrt_radius
    )
    transverse, longitudinal = derive_operator_eigenvalues(y)

    potential_amplitude = (
        sp.Rational(2, 3) * acceleration_coefficient / c_light**2
    )
    ricci, kretschmann = linearized_radial_curvature_on_axis(
        power=sp.Rational(3, 2),
        phi_amplitude=potential_amplitude,
        psi_amplitude=potential_amplitude,
        radius=radius,
    )

    mass = sp.symbols("m_geo", positive=True)
    schwarzschild_ricci, schwarzschild_kretschmann = (
        linearized_radial_curvature_on_axis(
            power=-1,
            phi_amplitude=-mass,
            psi_amplitude=-mass,
            radius=radius,
        )
    )
    hubble = sp.symbols("H_phys", positive=True)
    de_sitter_ricci, de_sitter_kretschmann = linearized_radial_curvature_on_axis(
        power=2,
        phi_amplitude=-hubble**2 / (2 * c_light**2),
        psi_amplitude=hubble**2 / (4 * c_light**2),
        radius=radius,
    )
    generic_power, generic_kappa = sp.symbols("n kappa", positive=True)
    generic = derive_generic_center_scaling(
        mu_power=generic_power,
        mu_coefficient=generic_kappa,
        a0=a0,
        b=b,
        radius=radius,
        speed_of_light=c_light,
    )
    value_asymptotic_lower_bound = derive_value_asymptotic_curvature_lower_bound(
        mu_power=generic_power,
        mu_coefficient=generic_kappa,
        a0=a0,
        source_coefficient=b,
        radius=radius,
        speed_of_light=c_light,
    )
    generic_acceleration_power = sp.symbols("s", positive=True)
    c_phi, c_psi = sp.symbols("C_phi C_psi", real=True)
    arbitrary_slip = derive_arbitrary_slip_center_curvature(
        acceleration_power=generic_acceleration_power,
        phi_acceleration_coefficient=c_phi,
        psi_acceleration_coefficient=c_psi,
        radius=radius,
        speed_of_light=c_light,
    )
    density_power = sp.symbols("m", nonnegative=True)
    density_threshold = derive_density_power_threshold(
        mu_power=generic_power, density_power=density_power
    )

    certificate = derive_symbolic_certificate()
    classification = (
        "NO_GO_UNDER_STATED_CENTER_ASSUMPTIONS"
        if certificate["passed"]
        else "CERTIFICATE_FAILED"
    )
    return {
        "conventions": {
            "signature": "-+++",
            "time_coordinate": "x0=ct",
            "metric": "g00=-(1+2 Phi/c^2), gij=(1-2 Psi/c^2) delta_ij",
            "source_coefficient": "mu(g/a0) g = b r + O(r^3)",
            "units": "a0,b,C_phi,C_psi and H_phys are physical; c_light is explicit; m_geo=G*M/c_light^2",
        },
        "software": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
        "puiseux_g_coefficients": {
            ("r^1" if order == 2 else f"r^({order}/2)"): sp.sstr(value)
            for order, value in puiseux.items()
        },
        "exact_exponential_inner_kepler_series": {
            "quantity": "v_c^4/r^3 = g^2/r",
            "sqrt_radius_variable": "sqrt_r=sqrt(r)",
            "through_O_r": sp.sstr(inner_kepler),
        },
        "flux_jacobian_eigenvalues": {
            "transverse": sp.sstr(transverse),
            "longitudinal": sp.sstr(longitudinal),
            "zero_field_limits": [
                sp.sstr(sp.limit(transverse, y, 0, dir="+")),
                sp.sstr(sp.limit(longitudinal, y, 0, dir="+")),
            ],
        },
        "slipless_center_curvature": {
            "Ricci_scalar": sp.sstr(ricci),
            "Kretschmann": sp.sstr(kretschmann),
            "normalized_R_coefficient": sp.sstr(
                sp.simplify(
                    ricci * sp.sqrt(radius) * c_light**2
                    / acceleration_coefficient
                )
            ),
            "normalized_K_coefficient": sp.sstr(
                sp.simplify(
                    kretschmann * radius * c_light**4
                    / acceleration_coefficient**2
                )
            ),
        },
        "schwarzschild_linearized_benchmark": {
            "Ricci_scalar": sp.sstr(schwarzschild_ricci),
            "normalized_K_coefficient": sp.sstr(
                sp.simplify(schwarzschild_kretschmann * radius**6 / mass**2)
            ),
        },
        "de_sitter_linearized_benchmark": {
            "normalized_R_coefficient": sp.sstr(
                sp.simplify(de_sitter_ricci * c_light**2 / hubble**2)
            ),
            "normalized_K_coefficient": sp.sstr(
                sp.simplify(de_sitter_kretschmann * c_light**4 / hubble**4)
            ),
        },
        "generic_mu_power_universality_class": {
            key: sp.sstr(value) for key, value in generic.items()
        },
        "value_asymptotic_curvature_lower_bound": {
            key: (
                {sp.sstr(k): sp.sstr(v) for k, v in value.items()}
                if isinstance(value, dict)
                else [sp.sstr(item) for item in value]
                if isinstance(value, tuple)
                else sp.sstr(value)
            )
            for key, value in value_asymptotic_lower_bound.items()
        },
        "arbitrary_slip_curvature": {
            key: sp.sstr(value) for key, value in arbitrary_slip.items()
        },
        "density_kernel_regular_center_matching": {
            **{key: sp.sstr(value) for key, value in density_threshold.items()},
            "finite_curvature_condition": "m >= n",
        },
        "certificate": certificate,
        "classification": {
            "result": classification,
            "scope": [
                "exact spherical MOND law remains valid into a force-free center",
                "smooth positive central source coefficient b",
                "the measured acceleration is the lapse potential Phi of one physical metric",
                "one physical metric interpreted as a classical C2 geometry",
                "Phi=Psi is evaluated as the requested specialization but is not needed for K to diverge",
            ],
            "non_claims": [
                "not a no-go for theories that modify the center equation",
                "not a global uniqueness theorem for relativistic MOND actions",
                "not a PPN or propagating-degree-of-freedom calculation",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = derive_audit_results()
    rendered = json.dumps(results, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if results["certificate"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
