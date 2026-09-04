#!/usr/bin/env python3
r"""Action-derived weak-static predictions for the HPI-Delta prototype.

This is a bounded symbolic audit of the weak-static and test-particle sectors.
It is not a nonlinear functional Dirac theorem, a full PPN calculation, a
covariant clock completion, or a novelty claim.
"""

from __future__ import annotations

import json
import sys
from typing import Any

import sympy as sp


ACTION_REFERENCE = r"""
S_HPI_Delta = integral dt d^3x [
  pi^{ij} dot(h_ij) + p_psi dot(psi)
  - N(H_GR[h,pi] + H_exp[h,N] + H_m)
  - N^i(H_i^GR + H_i^m)
  - sqrt(h) lambda_pi D^2(pi/sqrt(h)) ],
H_exp=(M_Pl^2/ell_0^2)sqrt(h) F_exp(y),
y=ell_0 sqrt(h^{ij}D_i ln(N)D_j ln(N)), ell_0=c^2/a_0,
F_exp(y)=2[(1+y)exp(-y)-1].
""".strip()

REDUCED_WEAK_STATIC_ACTION = r"""
S_ws proportional to integral d^3x [
  -2 grad(Phi).grad(Psi) + |grad(Psi)|^2
  - a_0^2 F_exp(|grad(Phi)|/a_0) - 8 pi G rho_b Phi ].
""".strip()


def _euler_first_order(
    lagrangian: sp.Expr, field: sp.Expr, coordinate: sp.Symbol
) -> sp.Expr:
    """Euler--Lagrange derivative for a first-spatial-derivative density."""

    return sp.factor(
        sp.diff(lagrangian, field)
        - sp.diff(sp.diff(lagrangian, sp.diff(field, coordinate)), coordinate)
    )


def _poisson_bracket(
    first: sp.Expr,
    second: sp.Expr,
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
) -> sp.Expr:
    return sp.factor(
        sum(
            sp.diff(first, q) * sp.diff(second, p)
            - sp.diff(first, p) * sp.diff(second, q)
            for q, p in zip(coordinates, momenta)
        )
    )


def _derive_kernel() -> dict[str, Any]:
    """Differentiate the action primitive instead of inserting ``mu``."""

    y = sp.symbols("y", positive=True)
    F_exp = 2 * ((1 + y) * sp.exp(-y) - 1)
    primitive = y**2 + F_exp
    expected_primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu_from_action = sp.factor(sp.diff(primitive, y) / (2 * y))
    expected_mu = 1 - sp.exp(-y)
    return {
        "y": y,
        "F_exp": F_exp,
        "primitive": primitive,
        "expected_primitive": expected_primitive,
        "primitive_residual": sp.simplify(primitive - expected_primitive),
        "mu": mu_from_action,
        "expected_mu": expected_mu,
        "mu_residual": sp.simplify(mu_from_action - expected_mu),
        "newtonian_limit": sp.limit(mu_from_action, y, sp.oo),
        "deep_ratio": sp.limit(mu_from_action / y, y, 0, dir="+"),
        "zero_field_mu": sp.limit(mu_from_action, y, 0, dir="+"),
    }


def _derive_weak_static_action(
    kernel: dict[str, Any],
    *,
    mixed_coefficient: sp.Expr = sp.Integer(1),
    psi_coefficient: sp.Expr = sp.Integer(1),
) -> dict[str, Any]:
    """Vary the EH-plus-F_exp density separately in Phi and Psi.

    The Cartesian jet calculation establishes the vector fluxes.  The radial
    calculation includes the spherical measure and will feed the orbit audit.
    """

    a0, G = sp.symbols("a_0 G", positive=True)
    rho_jet, phi_jet = sp.symbols("rho_jet phi_jet", real=True)
    p = sp.symbols("p_1:4", real=True)
    q = sp.symbols("q_1:4", real=True)
    p_norm = sp.sqrt(sum(component**2 for component in p))
    y_jet = p_norm / a0
    F_jet = kernel["F_exp"].subs(kernel["y"], y_jet)
    density = sp.factor(
        -2 * mixed_coefficient * sum(pi * qi for pi, qi in zip(p, q))
        + psi_coefficient * sum(qi**2 for qi in q)
        - a0**2 * F_jet
        - 8 * sp.pi * G * rho_jet * phi_jet
    )
    phi_flux = tuple(sp.factor(sp.diff(density, component)) for component in p)
    psi_flux = tuple(sp.factor(sp.diff(density, component)) for component in q)
    expected_phi_flux = tuple(
        -2 * mixed_coefficient * qi + 2 * sp.exp(-y_jet) * pi
        for pi, qi in zip(p, q)
    )
    expected_psi_flux = tuple(
        -2 * mixed_coefficient * pi + 2 * psi_coefficient * qi
        for pi, qi in zip(p, q)
    )

    r = sp.symbols("r", positive=True)
    Phi = sp.Function("Phi")(r)
    Psi = sp.Function("Psi")(r)
    rho = sp.Function("rho_b")(r)
    g_phi = sp.diff(Phi, r)
    g_psi = sp.diff(Psi, r)
    y_radial = g_phi / a0
    F_radial = kernel["F_exp"].subs(kernel["y"], y_radial)
    radial_lagrangian = sp.factor(
        r**2
        * (
            -2 * mixed_coefficient * g_phi * g_psi
            + psi_coefficient * g_psi**2
            - a0**2 * F_radial
            - 8 * sp.pi * G * rho * Phi
        )
    )
    E_phi = _euler_first_order(radial_lagrangian, Phi, r)
    E_psi = _euler_first_order(radial_lagrangian, Psi, r)
    expected_E_phi = sp.factor(
        2
        * sp.diff(
            r**2
            * (
                mixed_coefficient * g_psi
                - sp.exp(-y_radial) * g_phi
            ),
            r,
        )
        - 8 * sp.pi * G * r**2 * rho
    )
    expected_E_psi = sp.factor(
        2
        * sp.diff(
            r**2
            * (
                mixed_coefficient * g_phi
                - psi_coefficient * g_psi
            ),
            r,
        )
    )
    gamma = sp.factor(mixed_coefficient / psi_coefficient)
    return {
        "density": density,
        "mixed_coefficient": mixed_coefficient,
        "psi_coefficient": psi_coefficient,
        "p": p,
        "q": q,
        "p_norm": p_norm,
        "phi_flux": phi_flux,
        "psi_flux": psi_flux,
        "phi_flux_residuals": tuple(
            sp.simplify(actual - expected)
            for actual, expected in zip(phi_flux, expected_phi_flux)
        ),
        "psi_flux_residuals": tuple(
            sp.simplify(actual - expected)
            for actual, expected in zip(psi_flux, expected_psi_flux)
        ),
        "gamma_from_integrated_psi_equation": gamma,
        "radial": {
            "symbols": {
                "r": r,
                "a0": a0,
                "G": G,
                "Phi": Phi,
                "Psi": Psi,
                "rho": rho,
            },
            "lagrangian": radial_lagrangian,
            "E_phi": E_phi,
            "E_psi": E_psi,
            "E_phi_residual": sp.simplify(E_phi - expected_E_phi),
            "E_psi_residual": sp.simplify(E_psi - expected_E_psi),
            "positive_radial_gradient_branch": True,
        },
    }


def _derive_trace_preservation() -> dict[str, Any]:
    """Derive one-mode C_pi preservation from the Legendre transform."""

    A, k, longitudinal = sp.symbols(
        "A k lambda_parallel", positive=True, nonzero=True
    )
    Phi, Psi, B, eta = sp.symbols("Phi Psi B eta_pi", real=True)
    Psi_dot = sp.symbols("Psi_dot", real=True)
    p_Phi, p_Psi, p_B, p_eta = sp.symbols(
        "p_Phi p_Psi p_B p_eta", real=True
    )
    source = sp.symbols("J_rho", real=True)
    lagrangian = A * (
        -3 * Psi_dot**2
        + 2 * k**2 * B * Psi_dot
        + k**2
        * ((1 - longitudinal) * Phi**2 - 2 * Phi * Psi + Psi**2)
    ) - source * Phi
    derived_p_Psi = sp.factor(sp.diff(lagrangian, Psi_dot))
    velocity = sp.solve(sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True)[0]
    H0 = sp.factor((p_Psi * Psi_dot - lagrangian).subs(velocity))
    Hamiltonian = sp.factor(H0 + eta * k**2 * p_Psi)
    coordinates = (Phi, Psi, B, eta)
    momenta = (p_Phi, p_Psi, p_B, p_eta)
    secondary_C_pi = _poisson_bracket(
        p_eta, Hamiltonian, coordinates, momenta
    )
    dot_C_pi = _poisson_bracket(
        secondary_C_pi, Hamiltonian, coordinates, momenta
    )
    expected = 2 * A * k**4 * (Phi - Psi)
    weak_E_psi_mode = -2 * k**2 * (Phi - Psi)
    solutions = sp.solve(sp.Eq(dot_C_pi, 0), Psi, dict=True)
    return {
        "symbols": {
            "A": A,
            "k": k,
            "lambda_parallel": longitudinal,
            "Phi": Phi,
            "Psi": Psi,
            "B": B,
            "eta": eta,
            "p_Psi": p_Psi,
        },
        "lagrangian": lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "velocity_solution": velocity,
        "canonical_hamiltonian": Hamiltonian,
        "secondary_C_pi": secondary_C_pi,
        "dot_C_pi": dot_C_pi,
        "preservation_residual": sp.simplify(dot_C_pi - expected),
        "weak_E_psi_mode": weak_E_psi_mode,
        "weak_E_psi_relation_residual": sp.simplify(
            dot_C_pi + A * k**2 * weak_E_psi_mode
        ),
        "derived_Psi_solution": solutions[0][Psi],
        "requires_k_nonzero": bool(k.is_nonzero),
        "k_zero_preservation": sp.simplify(dot_C_pi.subs(k, 0)),
    }


def _derive_source_normalization() -> dict[str, Any]:
    """Bridge the physical dust term to the reduced c=1 normalization."""

    Mpl2, G = sp.symbols("M_Pl_sq G", positive=True)
    rho, Phi = sp.symbols("rho_b Phi", real=True)
    laplacian_Phi = sp.symbols("Laplacian_Phi", real=True)
    physical_matter_density = -rho * Phi
    normalized_matter_density = physical_matter_density / Mpl2
    planck_relation = {Mpl2: 1 / (8 * sp.pi * G)}
    reduced_matter_density = -8 * sp.pi * G * rho * Phi
    high_acceleration_equation = 2 * laplacian_Phi - 8 * sp.pi * G * rho
    poisson_solution = sp.solve(
        sp.Eq(high_acceleration_equation, 0), laplacian_Phi, dict=True
    )[0][laplacian_Phi]
    measured_G = sp.simplify(poisson_solution / (4 * sp.pi * rho))
    return {
        "symbols": {"Mpl2": Mpl2, "G": G, "rho": rho, "Phi": Phi},
        "units": "c=1 for the action normalization; c is restored only in lensing",
        "assumption": (
            "standard minimally coupled nonrelativistic dust gives -rho_b Phi; "
            "an explicit dust action is not varied in this script"
        ),
        "physical_matter_density": physical_matter_density,
        "normalized_matter_density": normalized_matter_density,
        "planck_relation": sp.Eq(Mpl2, 1 / (8 * sp.pi * G)),
        "reduced_matter_density": reduced_matter_density,
        "matter_rescaling_residual": sp.simplify(
            normalized_matter_density.subs(planck_relation)
            - reduced_matter_density
        ),
        "high_acceleration_equation": high_acceleration_equation,
        "poisson_solution": poisson_solution,
        "high_acceleration_poisson_residual": sp.simplify(
            poisson_solution - 4 * sp.pi * G * rho
        ),
        "measured_G": measured_G,
        "measured_G_residual": sp.simplify(measured_G - G),
    }


def _derive_aqual(
    action: dict[str, Any], kernel: dict[str, Any]
) -> dict[str, Any]:
    """Apply only the regular isolated solution of the derived Psi equation."""

    radial = action["radial"]
    symbols = radial["symbols"]
    r = symbols["r"]
    a0 = symbols["a0"]
    G = symbols["G"]
    Phi = symbols["Phi"]
    Psi = symbols["Psi"]
    rho = symbols["rho"]
    g = sp.diff(Phi, r)
    psi_gradient = sp.diff(Psi, r)
    integrated_psi_flux = sp.factor(
        action["mixed_coefficient"] * g
        - action["psi_coefficient"] * psi_gradient
    )
    psi_gradient_solution = sp.solve(
        sp.Eq(integrated_psi_flux, 0), psi_gradient, dict=True
    )[0][psi_gradient]
    slip_substitution = {
        psi_gradient: psi_gradient_solution,
        sp.diff(Psi, r, 2): sp.diff(psi_gradient_solution, r),
    }
    E_phi_on_slip = sp.factor(
        radial["E_phi"].subs(slip_substitution, simultaneous=True)
    )
    mu_radial = kernel["mu"].subs(kernel["y"], g / a0)
    expected_aqual = sp.factor(
        2 * sp.diff(r**2 * mu_radial * g, r)
        - 8 * sp.pi * G * r**2 * rho
    )
    return {
        "symbols": symbols,
        "integrated_psi_flux": integrated_psi_flux,
        "derived_psi_gradient": psi_gradient_solution,
        "derived_slip_residual": sp.simplify(psi_gradient_solution - g),
        "boundary_condition": "r^2(Phi'-Psi')->0 on the regular isolated branch",
        "E_phi_on_slip": E_phi_on_slip,
        "expected_aqual": expected_aqual,
        "aqual_residual": sp.simplify(E_phi_on_slip - expected_aqual),
        "aqual_equation": sp.Eq(
            sp.diff(r**2 * mu_radial * g, r),
            4 * sp.pi * G * r**2 * rho,
        ),
    }


def _derive_spherical(
    aqual: dict[str, Any], kernel: dict[str, Any]
) -> dict[str, Any]:
    """Integrate AQUAL over a sphere with its source normalization intact."""

    radial_symbols = aqual["symbols"]
    r_source = radial_symbols["r"]
    a0_source = radial_symbols["a0"]
    G_source = radial_symbols["G"]
    Phi_source = radial_symbols["Phi"]
    rho_source = radial_symbols["rho"]
    g_source = sp.diff(Phi_source, r_source)
    M_source = sp.Function("M_b")(r_source)
    rho_from_mass = sp.diff(M_source, r_source) / (4 * sp.pi * r_source**2)
    aqual_half_with_mass = sp.factor(
        (aqual["expected_aqual"] / 2).subs(rho_source, rho_from_mass)
    )
    mu_source = kernel["mu"].subs(kernel["y"], g_source / a0_source)
    mass_flux = sp.factor(
        r_source**2 * mu_source * g_source - G_source * M_source
    )
    mass_flux_derivative = sp.factor(sp.diff(mass_flux, r_source))

    r = r_source
    a0 = a0_source
    G = G_source
    g, M = sp.symbols("g M_b", positive=True)
    mu_g = sp.factor(kernel["mu"].subs(kernel["y"], g / a0))
    spherical_law = sp.factor(mu_g * g - G * M / r**2)
    integrated_flux = sp.factor(r**2 * spherical_law)
    exterior_projection = sp.factor(
        mass_flux.subs({g_source: g, M_source: M}, simultaneous=True)
    )
    deep_equation = sp.Eq(g**2 / a0, G * M / r**2)
    deep_solution = sp.solve(deep_equation, g, dict=True)[0][g]
    return {
        "symbols": {"r": r, "g": g, "a0": a0, "G": G, "M": M},
        "mu_g": mu_g,
        "integrated_flux": integrated_flux,
        "spherical_law": spherical_law,
        "spherical_law_residual": sp.simplify(
            integrated_flux / r**2 - spherical_law
        ),
        "mass_source": {
            "M": M_source,
            "rho_from_mass": rho_from_mass,
            "mass_definition_residual": sp.simplify(
                4 * sp.pi * r_source**2 * rho_from_mass
                - sp.diff(M_source, r_source)
            ),
            "aqual_half_with_mass": aqual_half_with_mass,
            "mass_flux": mass_flux,
            "mass_flux_derivative": mass_flux_derivative,
            "flux_derivative_residual": sp.simplify(
                aqual_half_with_mass - mass_flux_derivative
            ),
            "exterior_projection": exterior_projection,
            "exterior_projection_residual": sp.simplify(
                exterior_projection - integrated_flux
            ),
            "integration_condition": (
                "mass_flux is constant; regular origin/isolated-source boundary "
                "sets that constant to zero"
            ),
        },
        "equation": sp.Eq(mu_g * g, G * M / r**2),
        "newtonian_mu_limit": sp.limit(mu_g, g, sp.oo),
        "deep_flux_ratio": sp.limit(
            mu_g * g / (g**2 / a0), g, 0, dir="+"
        ),
        "deep_equation": deep_equation,
        "deep_acceleration": deep_solution,
    }


def _derive_orbit(spherical: dict[str, Any]) -> dict[str, Any]:
    """Substitute circular kinematics into the already-derived flux law."""

    r = spherical["symbols"]["r"]
    g = spherical["symbols"]["g"]
    a0 = spherical["symbols"]["a0"]
    G = spherical["symbols"]["G"]
    M = spherical["symbols"]["M"]
    T = sp.symbols("T", positive=True)
    g_circular = 4 * sp.pi**2 * r / T**2
    generalized_kepler = sp.factor(
        spherical["integrated_flux"].subs(g, g_circular)
    )
    displayed = sp.factor(
        4
        * sp.pi**2
        * r**3
        / T**2
        * (1 - sp.exp(-4 * sp.pi**2 * r / (a0 * T**2)))
        - G * M
    )
    T2_newton = 4 * sp.pi**2 * r**3 / (G * M)
    newton_equation = 4 * sp.pi**2 * r**3 / T**2 - G * M
    T2_deep = 4 * sp.pi**2 * r**2 / sp.sqrt(G * M * a0)
    deep_equation = r**2 * g_circular**2 / a0 - G * M
    speed = 2 * sp.pi * r / T
    return {
        "symbols": {"r": r, "T": T, "a0": a0, "G": G, "M": M},
        "circular_acceleration": g_circular,
        "generalized_kepler_law": generalized_kepler,
        "displayed_generalized_kepler_law": displayed,
        "generalized_kepler_residual": sp.simplify(
            generalized_kepler - displayed
        ),
        "newtonian_T_squared": T2_newton,
        "newtonian_kepler_residual": sp.simplify(
            newton_equation.subs(T, sp.sqrt(T2_newton))
        ),
        "deep_T_squared": T2_deep,
        "deep_period_residual": sp.simplify(
            deep_equation.subs(T, sp.sqrt(T2_deep))
        ),
        "asymptotic_speed_squared": sp.sqrt(G * M * a0),
        "btfr_residual": sp.simplify(
            (speed**4).subs(T, sp.sqrt(T2_deep)) - G * M * a0
        ),
    }


def _derive_epicycle(
    kernel: dict[str, Any], spherical: dict[str, Any]
) -> dict[str, Any]:
    """Differentiate the same spherical constitutive law for near-circular motion."""

    y = kernel["y"]
    mu = kernel["mu"]
    L_from_mu = sp.factor(y * sp.diff(mu, y) / mu)
    expected_L = y / (sp.exp(y) - 1)
    r = spherical["symbols"]["r"]
    g_symbol = spherical["symbols"]["g"]
    a0 = spherical["symbols"]["a0"]
    G = spherical["symbols"]["G"]
    M_symbol = spherical["symbols"]["M"]
    g_profile = sp.Function("g_profile")(r)
    M_profile = sp.Function("M_profile")(r)
    slope, mass_log_slope = sp.symbols("s m", real=True)
    profile_flux = spherical["integrated_flux"].subs(
        {g_symbol: g_profile, M_symbol: M_profile}, simultaneous=True
    )
    differentiated_flux = sp.diff(profile_flux, r)
    reduced_flux_derivative = differentiated_flux.subs(
        sp.diff(g_profile, r), slope * g_profile / r
    ).subs(
        sp.diff(M_profile, r), mass_log_slope * M_profile / r
    ).subs(
        M_profile,
        r**2 * g_profile * (1 - sp.exp(-g_profile / a0)) / G,
    )
    normalized_flux_derivative = sp.factor(
        sp.simplify(
            reduced_flux_derivative
            / (r * g_profile * (1 - sp.exp(-g_profile / a0)))
        )
    )
    normalized_flux_y = sp.factor(
        normalized_flux_derivative.subs(g_profile, a0 * y)
    )
    derived_general_slope = sp.factor(
        sp.solve(sp.Eq(normalized_flux_y, 0), slope, dict=True)[0][slope]
    )
    expected_general_slope = sp.factor(
        (mass_log_slope - 2) / (1 + L_from_mu)
    )
    log_g_slope = sp.factor(derived_general_slope.subs(mass_log_slope, 0))
    general_kappa2_over_omega2 = sp.factor(3 + derived_general_slope)
    kappa2_over_omega2 = sp.factor(
        general_kappa2_over_omega2.subs(mass_log_slope, 0)
    )
    expected_ratio = sp.factor((1 + 3 * L_from_mu) / (1 + L_from_mu))
    rotation_log_slope = sp.factor((1 + log_g_slope) / 2)
    omega_over_kappa = sp.sqrt(sp.factor(1 / kappa2_over_omega2))
    precession = sp.factor(2 * sp.pi * (omega_over_kappa - 1))
    return {
        "y": y,
        "mu": mu,
        "L": L_from_mu,
        "L_from_mu_residual": sp.simplify(L_from_mu - expected_L),
        "mass_log_slope": mass_log_slope,
        "profile_flux": profile_flux,
        "differentiated_profile_flux": differentiated_flux,
        "normalized_flux_derivative": normalized_flux_y,
        "general_log_g_slope": derived_general_slope,
        "differentiated_flux_residual": sp.simplify(
            derived_general_slope - expected_general_slope
        ),
        "log_g_slope": log_g_slope,
        "exterior_log_g_slope": log_g_slope,
        "log_slope_residual": sp.simplify(
            (1 + L_from_mu) * log_g_slope + 2
        ),
        "general_kappa2_over_omega2": general_kappa2_over_omega2,
        "kappa2_over_omega2": kappa2_over_omega2,
        "central_force_identity_residual": sp.simplify(
            kappa2_over_omega2 - (3 + log_g_slope)
        ),
        "closed_form_ratio_residual": sp.simplify(
            kappa2_over_omega2 - expected_ratio
        ),
        "omega_over_kappa": omega_over_kappa,
        "positive_branch_frequency_residual": sp.simplify(
            omega_over_kappa**2 * kappa2_over_omega2 - 1
        ),
        "exterior_rotation_log_slope": rotation_log_slope,
        "rotation_closed_form_residual": sp.simplify(
            rotation_log_slope
            - (1 + y - sp.exp(y)) / (2 * (sp.exp(y) - 1 + y))
        ),
        "precession": precession,
        "newtonian_L": sp.limit(L_from_mu, y, sp.oo),
        "deep_L": sp.limit(L_from_mu, y, 0, dir="+"),
        "newtonian_kappa2_over_omega2": sp.limit(
            kappa2_over_omega2, y, sp.oo
        ),
        "deep_kappa2_over_omega2": sp.limit(
            kappa2_over_omega2, y, 0, dir="+"
        ),
        "newtonian_precession": sp.limit(precession, y, sp.oo),
        "deep_precession": sp.limit(precession, y, 0, dir="+"),
        "newtonian_rotation_log_slope": sp.limit(
            rotation_log_slope, y, sp.oo
        ),
        "deep_rotation_log_slope": sp.limit(
            rotation_log_slope, y, 0, dir="+"
        ),
        "mass_profile_scope": (
            "m=d ln M_b/d ln r; apsidal limits below use exterior m=0"
        ),
        "convention": "Delta_varpi=2*pi*(Omega/kappa_ep-1) per radial period",
    }


def _derive_lensing(action: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the null-geodesic line integral for the two derived potentials."""

    z = sp.symbols("z", real=True)
    b, a0, G, M, c = sp.symbols("b a_0 G M_b c", positive=True)
    radius = sp.sqrt(b**2 + z**2)
    gamma = action["gamma_from_integrated_psi_equation"]
    metric_sum_factor = sp.factor(1 + gamma)
    g_profile = sp.Function("g")
    exact_single_integral = sp.Integral(
        b * g_profile(radius) / radius, (z, -sp.oo, sp.oo)
    )
    exact_deflection = metric_sum_factor * exact_single_integral / c**2

    newton_integrand = G * M * b / radius**3
    newton_single_integral = sp.simplify(
        sp.integrate(newton_integrand, (z, -sp.oo, sp.oo))
    )
    newton_deflection = sp.factor(
        metric_sum_factor * newton_single_integral / c**2
    )

    asymptotic_speed_squared = sp.sqrt(G * M * a0)
    deep_integrand = asymptotic_speed_squared * b / radius**2
    deep_single_integral = sp.simplify(
        sp.integrate(deep_integrand, (z, -sp.oo, sp.oo))
    )
    deep_deflection = sp.factor(
        metric_sum_factor * deep_single_integral / c**2
    )
    one_potential_deep = sp.factor(deep_single_integral / c**2)
    transition_radius = sp.sqrt(G * M / a0)
    return {
        "symbols": {"z": z, "b": b, "a0": a0, "G": G, "M": M, "c": c},
        "gamma": gamma,
        "metric_sum_factor": metric_sum_factor,
        "exact_single_potential_integral": exact_single_integral,
        "exact_deflection_integral": exact_deflection,
        "newtonian_integrand": newton_integrand,
        "newtonian_single_potential_integral": newton_single_integral,
        "newtonian_deflection": newton_deflection,
        "deep_integrand": deep_integrand,
        "deep_single_potential_integral": deep_single_integral,
        "deep_deflection": deep_deflection,
        "one_potential_deep_deflection": one_potential_deep,
        "no_slip_to_one_potential_factor": sp.simplify(
            deep_deflection / one_potential_deep
        ),
        "transition_radius": transition_radius,
        "deep_to_baryon_newtonian_ratio": sp.simplify(
            deep_deflection / newton_deflection
        ),
        "metric_convention": (
            "ds^2=-(1+2Phi/c^2)c^2dt^2+(1-2Psi/c^2)dx^2; "
            "alpha=c^-2 integral grad_perp(Phi+Psi) dz"
        ),
        "deep_limit_scope": (
            "formal isolated scale-free exterior; a physical finite system or "
            "external field supplies the large-distance cutoff"
        ),
    }


def _derive_mutations(
    kernel: dict[str, Any],
    action: dict[str, Any],
    epicycle: dict[str, Any],
) -> dict[str, Any]:
    """Recompute named negative controls rather than toggling PASS flags."""

    y = kernel["y"]
    primitive_without_F = y**2
    mu_without_F = sp.factor(sp.diff(primitive_without_F, y) / (2 * y))

    wrong_action = _derive_weak_static_action(
        kernel, mixed_coefficient=sp.Integer(1), psi_coefficient=sp.Integer(2)
    )
    wrong_gamma = wrong_action["gamma_from_integrated_psi_equation"]
    wrong_modulus = sp.factor(
        wrong_action["mixed_coefficient"] * wrong_gamma - sp.exp(-y)
    )

    dropped_gamma = sp.Integer(0)
    dropped_metric_factor = 1 + dropped_gamma
    correct_metric_factor = 1 + action["gamma_from_integrated_psi_equation"]

    ignored_L = sp.Integer(0)
    ignored_ratio = sp.factor(3 - 2 / (1 + ignored_L))
    ignored_precession = sp.factor(2 * sp.pi * (1 / sp.sqrt(ignored_ratio) - 1))
    return {
        "remove_F_exp": {
            "primitive": primitive_without_F,
            "effective_mu": mu_without_F,
            "mu_residual": sp.simplify(mu_without_F - kernel["mu"]),
            "deep_mu_over_y": sp.limit(mu_without_F / y, y, 0, dir="+"),
        },
        "wrong_EH_psi_coefficient": {
            "psi_coefficient": wrong_action["psi_coefficient"],
            "gamma": wrong_gamma,
            "effective_modulus": wrong_modulus,
            "mond_modulus_residual": sp.simplify(wrong_modulus - kernel["mu"]),
            "phi_flux_residuals": wrong_action["phi_flux_residuals"],
            "psi_flux_residuals": wrong_action["psi_flux_residuals"],
        },
        "drop_Psi_from_lensing": {
            "gamma": dropped_gamma,
            "deep_factor": dropped_metric_factor,
            "relative_to_no_slip": sp.factor(
                dropped_metric_factor / correct_metric_factor
            ),
        },
        "ignore_constitutive_slope": {
            "L": ignored_L,
            "deep_kappa2_over_omega2": ignored_ratio,
            "deep_precession": ignored_precession,
            "ratio_defect": sp.simplify(
                ignored_ratio - epicycle["deep_kappa2_over_omega2"]
            ),
        },
    }


def derive_predictions() -> dict[str, Any]:
    kernel = _derive_kernel()
    action = _derive_weak_static_action(kernel)
    aqual = _derive_aqual(action, kernel)
    spherical = _derive_spherical(aqual, kernel)
    epicycle = _derive_epicycle(kernel, spherical)
    return {
        "action_reference": ACTION_REFERENCE,
        "reduced_weak_static_action": REDUCED_WEAK_STATIC_ACTION,
        "source_normalization": _derive_source_normalization(),
        "kernel": kernel,
        "weak_static_action": action,
        "trace_preservation": _derive_trace_preservation(),
        "aqual": aqual,
        "spherical": spherical,
        "orbit": _derive_orbit(spherical),
        "epicycle": epicycle,
        "lensing": _derive_lensing(action),
        "mutations": _derive_mutations(kernel, action, epicycle),
        "scope": {
            "leading_weak_static_gamma_only": True,
            "deep_scale_free_lensing_requires_cutoff": True,
            "source_normalization_bridge_is_explicit": True,
            "source_normalization_conditional_on_reduced_action": True,
            "explicit_dust_action_varied": False,
            "full_ADM_to_weak_reduction_certified": False,
            "full_ppn_certified": False,
            "full_nonlinear_dirac_certified": False,
            "covariant_clock_completion_certified": False,
            "global_stability_certified": False,
            "novelty_claimed": False,
            "candidate_status": "OPEN",
        },
    }


def evaluate_checks(result: dict[str, Any]) -> dict[str, bool]:
    """Evaluate exact residuals and live negative controls used by the CLI."""

    kernel = result["kernel"]
    normalization = result["source_normalization"]
    action = result["weak_static_action"]
    trace = result["trace_preservation"]
    aqual = result["aqual"]
    spherical = result["spherical"]
    orbit = result["orbit"]
    epicycle = result["epicycle"]
    lensing = result["lensing"]
    mutations = result["mutations"]
    return {
        "primitive differentiates to exact exponential mu": (
            kernel["primitive_residual"] == 0 and kernel["mu_residual"] == 0
        ),
        "Planck normalization yields measured Newton G": (
            normalization["matter_rescaling_residual"] == 0
            and normalization["high_acceleration_poisson_residual"] == 0
            and normalization["measured_G_residual"] == 0
        ),
        "Cartesian Phi/Psi fluxes independently varied": (
            all(value == 0 for value in action["phi_flux_residuals"])
            and all(value == 0 for value in action["psi_flux_residuals"])
        ),
        "radial Phi/Psi Euler-Lagrange equations independently varied": (
            action["radial"]["E_phi_residual"] == 0
            and action["radial"]["E_psi_residual"] == 0
        ),
        "C_pi preservation generates finite-k no slip": (
            trace["preservation_residual"] == 0
            and trace["weak_E_psi_relation_residual"] == 0
            and trace["derived_Psi_solution"] == trace["symbols"]["Phi"]
        ),
        "k=0 is not inferred from finite-k preservation": (
            trace["requires_k_nonzero"] and trace["k_zero_preservation"] == 0
        ),
        "derived no slip reduces lapse equation to AQUAL": (
            aqual["derived_slip_residual"] == 0 and aqual["aqual_residual"] == 0
        ),
        "AQUAL source integrates to enclosed baryonic mass": (
            spherical["mass_source"]["mass_definition_residual"] == 0
            and spherical["mass_source"]["flux_derivative_residual"] == 0
            and spherical["mass_source"]["exterior_projection_residual"] == 0
        ),
        "exact spherical law and asymptotic limits": (
            spherical["spherical_law_residual"] == 0
            and spherical["newtonian_mu_limit"] == 1
            and spherical["deep_flux_ratio"] == 1
        ),
        "generalized Kepler law and BTFR": (
            orbit["generalized_kepler_residual"] == 0
            and orbit["newtonian_kepler_residual"] == 0
            and orbit["deep_period_residual"] == 0
            and orbit["btfr_residual"] == 0
        ),
        "epicycle law comes from differentiated mass flux": (
            epicycle["differentiated_flux_residual"] == 0
            and epicycle["central_force_identity_residual"] == 0
            and epicycle["closed_form_ratio_residual"] == 0
        ),
        "epicycle Newton/deep limits": (
            epicycle["newtonian_kappa2_over_omega2"] == 1
            and epicycle["deep_kappa2_over_omega2"] == 2
            and epicycle["newtonian_precession"] == 0
        ),
        "two-potential lensing integrals": (
            lensing["metric_sum_factor"] == 2
            and lensing["no_slip_to_one_potential_factor"] == 2
        ),
        "mutations alter constitutive/slip/lensing/orbit outputs": (
            mutations["remove_F_exp"]["mu_residual"] != 0
            and mutations["wrong_EH_psi_coefficient"]["mond_modulus_residual"] != 0
            and mutations["drop_Psi_from_lensing"]["relative_to_no_slip"] != 1
            and mutations["ignore_constitutive_slope"]["ratio_defect"] != 0
        ),
    }


def _main() -> int:
    result = derive_predictions()
    checks = evaluate_checks(result)
    print("=" * 78)
    print("HPI-DELTA WEAK-STATIC / ORBIT / LENSING PREDICTION AUDIT")
    print("=" * 78)
    for label, passed in checks.items():
        print(("[PASS] " if passed else "[FAIL] ") + label)
    print("\nDerived exterior laws:")
    print("  spherical:", result["spherical"]["equation"])
    print("  circular:", sp.Eq(result["orbit"]["generalized_kepler_law"], 0))
    print("  kappa_ep^2/Omega^2:", result["epicycle"]["kappa2_over_omega2"])
    print("  Delta_varpi:", result["epicycle"]["precession"])
    print("  deep deflection:", result["lensing"]["deep_deflection"])
    print("\nBounded verdict:")
    print("  These weak-static consequences pass for the reduced action branch.")
    print("  Full PPN, nonlinear functional Dirac closure, clock covariance,")
    print("  global stability, and novelty remain unproved. Status: OPEN.")
    summary = {
        "status": result["scope"]["candidate_status"],
        "checks_passed": sum(bool(value) for value in checks.values()),
        "checks_total": len(checks),
        "gamma_weak_static": str(result["lensing"]["gamma"]),
        "deep_kappa2_over_omega2": str(
            result["epicycle"]["deep_kappa2_over_omega2"]
        ),
        "deep_precession": str(result["epicycle"]["deep_precession"]),
        "deep_deflection": str(result["lensing"]["deep_deflection"]),
    }
    print("CERTIFICATE_JSON:", json.dumps(summary, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(_main())
