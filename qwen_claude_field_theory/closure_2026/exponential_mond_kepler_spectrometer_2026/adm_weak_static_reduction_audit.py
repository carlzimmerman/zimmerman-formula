#!/usr/bin/env python3
"""Audit the ADM action -> weak-static two-potential density reduction.

This is a deliberately symmetry-reduced calculation.  Starting from the
displayed HPI-Delta ADM action, it expands the static, zero-shift branch

    N = exp(Phi/c^2),       h_ij = exp(-2 Psi/c^2) delta_ij,
    K_ij = 0,               D^2 lambda = 0,

through order c^-4 while keeping u/a0 = |grad Phi|/a0 finite.  It derives the
Einstein-gradient density, the exact (unexpanded in u/a0) exponential MOND
term, and the minimally-coupled dust normalization.  It does not claim that a
symmetry-reduced expansion substitutes for the parent theory's full Dirac or
PPN analysis.

The executable negative controls reverse the spatial-metric sign, double the
overall gravitational prefactor, or corrupt the c/Planck/Lambda scalings.
Each mutation must miss the target weak action, so the audited coefficients
are not hard-coded as unconditional passes.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

import sympy as sp


@lru_cache(maxsize=1)
def derive_spatial_ricci_direct() -> dict[str, Any]:
    """Generate R^(3) directly from h_ij=exp(2 s epsilon Psi) delta_ij.

    This independent tensor contraction prevents the conformal-curvature
    identity used by ``derive_reduction`` from serving as an unchecked input.
    No field equation or target weak density is supplied to the contraction.
    """

    x, y, z, epsilon = sp.symbols("x y z epsilon", real=True)
    sign = sp.symbols("s", real=True, nonzero=True)
    coords = (x, y, z)
    psi_field = sp.Function("Psi")(*coords)
    conformal = sp.exp(2 * sign * epsilon * psi_field)
    metric = sp.diag(conformal, conformal, conformal)
    inverse = sp.diag(1 / conformal, 1 / conformal, 1 / conformal)
    dimension = 3

    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[i, ell]
                        * (
                            sp.diff(metric[ell, k], coords[j])
                            + sp.diff(metric[ell, j], coords[k])
                            - sp.diff(metric[j, k], coords[ell])
                        )
                        for ell in range(dimension)
                    )
                    / 2
                )
                for k in range(dimension)
            ]
            for j in range(dimension)
        ]
        for i in range(dimension)
    ]
    ricci = [
        [
            sp.simplify(
                sum(
                    sp.diff(christoffel[k][i][j], coords[k])
                    - sp.diff(christoffel[k][i][k], coords[j])
                    + sum(
                        christoffel[k][k][ell] * christoffel[ell][i][j]
                        - christoffel[k][j][ell] * christoffel[ell][i][k]
                        for ell in range(dimension)
                    )
                    for k in range(dimension)
                )
            )
            for j in range(dimension)
        ]
        for i in range(dimension)
    ]
    scalar = sp.simplify(
        sum(
            inverse[i, j] * ricci[i][j]
            for i in range(dimension)
            for j in range(dimension)
        )
    )
    expected = sp.exp(-2 * sign * epsilon * psi_field) * (
        -4
        * sign
        * epsilon
        * sum(sp.diff(psi_field, coordinate, 2) for coordinate in coords)
        - 2
        * sign**2
        * epsilon**2
        * sum(sp.diff(psi_field, coordinate) ** 2 for coordinate in coords)
    )
    nonzero_christoffel_components = sum(
        component != 0
        for plane in christoffel
        for row in plane
        for component in row
    )
    return {
        "scalar": scalar,
        "expected": expected,
        "residual": sp.simplify(scalar - expected),
        "nonzero_christoffel_components": nonzero_christoffel_components,
    }


def _epsilon2_coefficient(expression: sp.Expr, epsilon: sp.Symbol) -> sp.Expr:
    """Return the exact epsilon^2 Taylor coefficient at epsilon=0."""

    return sp.simplify(sp.diff(expression, epsilon, 2).subs(epsilon, 0) / 2)


def derive_reduction(
    spatial_exponent_sign: int = -1,
    action_prefactor: sp.Expr = sp.Rational(1, 2),
    ell0_epsilon_power: int = -1,
    planck_epsilon_power: int = -2,
    cosmological_epsilon_power: int = 2,
) -> dict[str, Any]:
    """Derive the weak-static density from the displayed ADM action.

    ``spatial_exponent_sign=-1`` is the physical isotropic metric
    h_ij=exp(-2 epsilon Psi) delta_ij.  The opposite sign is retained as a
    live mutation.  ``epsilon=c^-2`` is both the weak-field bookkeeper and the
    restored-c conversion.  The nonrelativistic scaling holds
    ell_0=(epsilon*a0)^-1, so y remains finite instead of being Taylor
    expanded about y=0.
    """

    if spatial_exponent_sign not in (-1, 1):
        raise ValueError("spatial_exponent_sign must be -1 or +1")
    for name, power in (
        ("ell0_epsilon_power", ell0_epsilon_power),
        ("planck_epsilon_power", planck_epsilon_power),
        ("cosmological_epsilon_power", cosmological_epsilon_power),
    ):
        if not isinstance(power, int):
            raise TypeError(f"{name} must be an integer")

    s = sp.Integer(spatial_exponent_sign)
    prefactor = sp.sympify(action_prefactor)
    epsilon = sp.symbols("epsilon", positive=True)
    phi, psi = sp.symbols("Phi Psi", real=True)
    lap_psi = sp.symbols("laplacian_Psi", real=True)
    grad_phi_dot_grad_psi = sp.symbols("grad_Phi_dot_grad_Psi", real=True)
    grad_psi_squared = sp.symbols("grad_Psi_squared", nonnegative=True)
    u, a0 = sp.symbols("u a_0", positive=True)
    mass, rho, G = sp.symbols("m rho_rest G", positive=True)
    Lambda_2 = sp.symbols("Lambda_2", real=True)

    # For h_ij=exp(2 sigma) delta_ij in three dimensions,
    # R^(3)=exp(-2 sigma)[-4 Delta sigma-2(grad sigma)^2].  Here
    # sigma=s*epsilon*Psi.  N sqrt(h)=exp[epsilon(Phi+3s Psi)].
    lapse = sp.exp(epsilon * phi)
    sqrt_h = sp.exp(3 * s * epsilon * psi)
    ricci_3 = sp.exp(-2 * s * epsilon * psi) * (
        -4 * s * epsilon * lap_psi
        - 2 * s**2 * epsilon**2 * grad_psi_squared
    )
    eh_density_exact = sp.simplify(prefactor * lapse * sqrt_h * ricci_3)
    eh_pre_ibp = sp.expand(_epsilon2_coefficient(eh_density_exact, epsilon))

    # Perform the only two integrations by parts explicitly:
    # int Phi Delta Psi = -int grad Phi.grad Psi and
    # int Psi Delta Psi = -int |grad Psi|^2, modulo a boundary term.
    phi_lap_coefficient = sp.expand(eh_pre_ibp).coeff(phi * lap_psi)
    psi_lap_coefficient = sp.expand(eh_pre_ibp).coeff(psi * lap_psi)
    remainder = sp.expand(
        eh_pre_ibp
        - phi_lap_coefficient * phi * lap_psi
        - psi_lap_coefficient * psi * lap_psi
    )
    eh_post_ibp = sp.simplify(
        remainder
        - phi_lap_coefficient * grad_phi_dot_grad_psi
        - psi_lap_coefficient * grad_psi_squared
    )
    eh_target = -2 * grad_phi_dot_grad_psi + grad_psi_squared
    eh_residual = sp.simplify(eh_post_ibp - eh_target)

    # In the fixed-a0 nonrelativistic scaling suggested by
    # a0 proportional to c^2 sqrt(Lambda), Lambda=epsilon^2 Lambda_2.
    # After division by the common epsilon^2 weak scale this contributes only
    # a field-independent constant at leading order.  We calculate, rather
    # than verbally discard, the field-dependent remainder.  Power one is a
    # live mutation which leaves a nonzero Phi/Psi term.
    cosmological_constant = epsilon**cosmological_epsilon_power * Lambda_2
    cosmological_scaled_exact = sp.simplify(
        prefactor
        * lapse
        * sqrt_h
        * (-2 * cosmological_constant)
        / epsilon**2
    )
    cosmological_background_exact = sp.simplify(
        cosmological_scaled_exact.subs({phi: 0, psi: 0})
    )
    cosmological_field_exact = sp.simplify(
        cosmological_scaled_exact - cosmological_background_exact
    )
    cosmological_field_residual = sp.simplify(
        sp.limit(cosmological_field_exact, epsilon, 0, dir="+")
    )

    # ell_0=c^2/a0=1/(epsilon*a0), while
    # h^ij=exp(-2s epsilon Psi) delta^ij and d_i ln N=epsilon d_i Phi.
    # Thus the exact ADM argument is y=exp(-s epsilon Psi)u/a0 and its
    # leading weak-field value is u/a0 without expanding the exponential
    # constitutive function in u/a0.
    ell0 = epsilon**ell0_epsilon_power / a0
    grad_ln_lapse_norm = epsilon * sp.exp(-s * epsilon * psi) * u
    y_exact = sp.simplify(ell0 * grad_ln_lapse_norm)
    y_leading = sp.simplify(sp.limit(y_exact, epsilon, 0, dir="+"))
    y_residual = sp.simplify(y_leading - u / a0)
    F = lambda z: 2 * ((1 + z) * sp.exp(-z) - 1)

    # The ADM bracket contains -2 F/ell_0^2.  After removing the common
    # M_Pl^2 epsilon^2 scale, its exact leading contribution is below.
    mond_scaled_exact = sp.simplify(
        prefactor
        * lapse
        * sqrt_h
        * (-2 / (ell0**2 * epsilon**2))
        * F(y_exact)
    )
    mond_leading = sp.simplify(sp.limit(mond_scaled_exact, epsilon, 0, dir="+"))
    mond_target = sp.simplify(-a0**2 * F(u / a0))
    mond_residual = sp.simplify(mond_leading - mond_target)

    # A static minimally coupled point particle has L_m=-m c^2 N.
    # Subtracting its field-independent rest energy before epsilon -> 0
    # leaves -m Phi.  Replacing m delta^3(x) by rho gives -rho Phi.
    particle_potential_exact = -mass * (lapse - 1) / epsilon
    particle_leading = sp.simplify(sp.limit(particle_potential_exact, epsilon, 0))
    particle_residual = sp.simplify(particle_leading + mass * phi)

    # With c restored, M_Pl^2=c^4/(8 pi G)=1/(8 pi G epsilon^2).
    # Therefore M_Pl^2 epsilon^2=1/(8 pi G); multiplying the complete weak
    # density by 8 pi G normalizes the gravitational terms to one and maps
    # -rho Phi to the source -8 pi G rho Phi used in the radial action.
    planck_sq_restored = epsilon**planck_epsilon_power / (8 * sp.pi * G)
    weak_gravity_scale = sp.simplify(planck_sq_restored * epsilon**2)
    planck_scaling_residual = sp.simplify(
        weak_gravity_scale - 1 / (8 * sp.pi * G)
    )
    dust_source = sp.simplify((-rho * phi) / weak_gravity_scale)
    dust_source_target = -8 * sp.pi * G * rho * phi
    dust_source_residual = sp.simplify(dust_source - dust_source_target)

    # Generate the no-slip high-y radial EL equation from the already derived
    # EH, MOND, and dust densities.  The exponential term tends to a
    # field-independent constant, leaving the Newtonian gradient density.
    # This checks the Poisson normalization implied by the stated Planck-G
    # relation; it does not independently measure or derive G.
    radial_coordinate = sp.symbols("r_Poisson", positive=True)
    Phi_radial = sp.Function("Phi_Poisson")(radial_coordinate)
    rho_radial = sp.Function("rho_rest_Poisson")(radial_coordinate)
    high_y_grad_squared = sp.symbols("high_y_grad_squared", nonnegative=True)
    high_y_eh_density = sp.simplify(
        eh_post_ibp.subs(
            {
                grad_phi_dot_grad_psi: high_y_grad_squared,
                grad_psi_squared: high_y_grad_squared,
            }
        )
    )
    high_y_mond_constant = sp.simplify(sp.limit(mond_leading, u, sp.oo))
    high_y_radial_density = sp.simplify(
        radial_coordinate**2
        * (high_y_eh_density + high_y_mond_constant + dust_source).subs(
            {
                high_y_grad_squared: sp.diff(Phi_radial, radial_coordinate) ** 2,
                phi: Phi_radial,
                rho: rho_radial,
            }
        )
    )
    high_y_euler = sp.simplify(
        (
            sp.diff(high_y_radial_density, Phi_radial)
            - sp.diff(
                sp.diff(
                    high_y_radial_density,
                    sp.diff(Phi_radial, radial_coordinate),
                ),
                radial_coordinate,
            )
        )
        / radial_coordinate**2
    )
    high_y_poisson_target = (
        2 * sp.diff(Phi_radial, radial_coordinate, 2)
        + 4 * sp.diff(Phi_radial, radial_coordinate) / radial_coordinate
        - 8 * sp.pi * G * rho_radial
    )
    high_y_poisson_residual = sp.simplify(high_y_euler - high_y_poisson_target)

    # On the static zero-shift branch K_ij=0.  Generate the trace contraction
    # for bar K_ij=-(b/2)h_ij, b=D^2 lambda/N, rather than assigning it:
    # barK_ij barK^ij-barK^2=-3b^2/2.  At leading weak order a Fourier mode
    # has b=-k^2 lambda_k.  Its EL equation sets lambda_k=0 for k!=0; at k=0
    # D^2 lambda vanishes identically.  There is no frequency or lambda-dot in
    # this reduced auxiliary equation.
    b = sp.symbols("b", real=True)
    bar_eigenvalue = -b / 2
    bar_kij_squared = sp.simplify(3 * bar_eigenvalue**2)
    barK_squared = sp.simplify((3 * bar_eigenvalue) ** 2)
    auxiliary_trace_invariant = sp.simplify(bar_kij_squared - barK_squared)
    auxiliary_trace_residual = sp.simplify(
        auxiliary_trace_invariant + sp.Rational(3, 2) * b**2
    )
    k = sp.symbols("k", positive=True)
    lambda_k = sp.symbols("lambda_k", real=True)
    b_fourier = -k**2 * lambda_k
    auxiliary_fourier_density = sp.simplify(
        prefactor * auxiliary_trace_invariant.subs(b, b_fourier)
    )
    lambda_euler = sp.simplify(sp.diff(auxiliary_fourier_density, lambda_k))
    lambda_nonzero_k_solution = sp.solve(lambda_euler, lambda_k)[0]
    lambda_euler_nonzero_k_residual = sp.simplify(lambda_nonzero_k_solution)
    lambda_euler_k0 = sp.simplify(lambda_euler.subs(k, 0))
    lambda_dot_k = sp.symbols("lambda_dot_k", real=True)
    # Differentiate the displayed reduced density instead of entering its
    # velocity Hessian as an expected value.  Since lambda_dot_k never occurs,
    # SymPy must return zero.
    auxiliary_velocity_hessian = sp.simplify(
        sp.diff(auxiliary_fourier_density, lambda_dot_k, 2)
    )
    K_ij_branch = sp.Integer(0)
    D2lambda_branch = sp.simplify(
        b_fourier.subs(lambda_k, lambda_nonzero_k_solution)
    )
    barK_ij_branch = sp.simplify(K_ij_branch - D2lambda_branch / 2)

    # Spherical radial fields satisfy grad Phi.grad Psi=Phi'Psi' and
    # |grad Phi|=|Phi'|.  On the attractive convention used in the orbit
    # calculation Phi'>0, so the Cartesian measure 4 pi r^2 dr yields exactly
    # the recorded radial density after removing the common 4 pi.
    radius = sp.symbols("r", positive=True)
    phi_prime = sp.symbols("Phi_prime", positive=True)
    psi_prime = sp.symbols("Psi_prime", real=True)
    radial_u = sp.simplify(sp.Abs(phi_prime))
    radial_u_residual = sp.simplify(radial_u - phi_prime)
    cartesian_weak_density = sp.simplify(
        eh_post_ibp + mond_leading + dust_source
    )
    spherical_radial_density = sp.simplify(
        radius**2
        * cartesian_weak_density.subs(
            {
                grad_phi_dot_grad_psi: phi_prime * psi_prime,
                grad_psi_squared: psi_prime**2,
                u: radial_u,
            }
        )
    )
    radial_target = sp.simplify(
        radius**2
        * (
            -2 * phi_prime * psi_prime
            + psi_prime**2
            - a0**2 * F(phi_prime / a0)
            - 8 * sp.pi * G * rho * phi
        )
    )
    spherical_reduction_residual = sp.simplify(
        spherical_radial_density - radial_target
    )

    return {
        "epsilon": epsilon,
        "Phi": phi,
        "Psi": psi,
        "u": u,
        "a0": a0,
        "G": G,
        "rho": rho,
        "grad_phi_dot_grad_psi": grad_phi_dot_grad_psi,
        "grad_psi_squared": grad_psi_squared,
        "lapse": lapse,
        "sqrt_h": sqrt_h,
        "ricci_3": ricci_3,
        "eh_density_exact": eh_density_exact,
        "eh_pre_ibp": eh_pre_ibp,
        "eh_post_ibp": eh_post_ibp,
        "eh_target": eh_target,
        "eh_residual": eh_residual,
        "Lambda_2": Lambda_2,
        "cosmological_constant": cosmological_constant,
        "cosmological_scaled_exact": cosmological_scaled_exact,
        "cosmological_background_exact": cosmological_background_exact,
        "cosmological_field_exact": cosmological_field_exact,
        "cosmological_field_residual": cosmological_field_residual,
        "y_exact": y_exact,
        "ell0": ell0,
        "grad_ln_lapse_norm": grad_ln_lapse_norm,
        "y_leading": y_leading,
        "y_residual": y_residual,
        "mond_scaled_exact": mond_scaled_exact,
        "mond_leading": mond_leading,
        "mond_target": mond_target,
        "mond_residual": mond_residual,
        "particle_potential_exact": particle_potential_exact,
        "particle_leading": particle_leading,
        "particle_residual": particle_residual,
        "planck_sq_restored": planck_sq_restored,
        "weak_gravity_scale": weak_gravity_scale,
        "planck_scaling_residual": planck_scaling_residual,
        "dust_source": dust_source,
        "dust_source_residual": dust_source_residual,
        "high_y_euler": high_y_euler,
        "high_y_poisson_target": high_y_poisson_target,
        "high_y_poisson_residual": high_y_poisson_residual,
        "auxiliary_trace_invariant": auxiliary_trace_invariant,
        "auxiliary_trace_residual": auxiliary_trace_residual,
        "auxiliary_fourier_density": auxiliary_fourier_density,
        "lambda_euler": lambda_euler,
        "lambda_nonzero_k_solution": lambda_nonzero_k_solution,
        "lambda_euler_nonzero_k_residual": lambda_euler_nonzero_k_residual,
        "lambda_euler_k0": lambda_euler_k0,
        "lambda_dot_k": lambda_dot_k,
        "auxiliary_velocity_hessian": auxiliary_velocity_hessian,
        "K_ij_branch": K_ij_branch,
        "D2lambda_branch": D2lambda_branch,
        "barK_ij_branch": barK_ij_branch,
        "spherical_radial_density": spherical_radial_density,
        "spherical_reduction_residual": spherical_reduction_residual,
        "radial_u": radial_u,
        "radial_u_residual": radial_u_residual,
        "boundary_term_discarded": True,
        "cosmological_fixed_a0_scaling": True,
        "symmetry_reduced_branch_only": True,
    }


def build_results() -> dict[str, Any]:
    """Return a serializable ledger, including live mutation failures."""

    direct_ricci = derive_spatial_ricci_direct()
    physical = derive_reduction()
    wrong_sign = derive_reduction(spatial_exponent_sign=1)
    missing_half = derive_reduction(action_prefactor=sp.Integer(1))
    wrong_ell0_scaling = derive_reduction(ell0_epsilon_power=0)
    wrong_planck_scaling = derive_reduction(planck_epsilon_power=-1)
    wrong_cosmological_scaling = derive_reduction(cosmological_epsilon_power=1)
    certificates = {
        "spatial_ricci_from_metric": direct_ricci["residual"] == 0,
        "einstein_density_after_ibp": physical["eh_residual"] == 0,
        "finite_exact_mond_argument": physical["y_residual"] == 0,
        "exact_exponential_density": physical["mond_residual"] == 0,
        "point_particle_source": physical["particle_residual"] == 0,
        "poisson_normalization_from_planck_G_relation": physical[
            "high_y_poisson_residual"
        ]
        == 0,
        "dust_normalization": physical["dust_source_residual"] == 0,
        "fixed_a0_cosmological_scaling": physical[
            "cosmological_field_residual"
        ]
        == 0,
        "static_auxiliary_branch": physical["barK_ij_branch"] == 0,
        "auxiliary_trace_contraction": physical["auxiliary_trace_residual"] == 0,
        "auxiliary_nonzero_k_equation": physical[
            "lambda_euler_nonzero_k_residual"
        ]
        == 0,
        "auxiliary_k0_kernel_separated": physical["lambda_euler_k0"] == 0,
        "spherical_radial_measure": physical["spherical_reduction_residual"] == 0,
        "wrong_spatial_sign_rejected": wrong_sign["eh_residual"] != 0,
        "doubled_gravitational_prefactor_rejected": missing_half["eh_residual"] != 0,
        "wrong_ell0_scaling_rejected": wrong_ell0_scaling["y_residual"] != 0,
        "wrong_planck_scaling_rejected": wrong_planck_scaling[
            "dust_source_residual"
        ]
        != 0,
        "wrong_cosmological_scaling_rejected": wrong_cosmological_scaling[
            "cosmological_field_residual"
        ]
        != 0,
    }
    passed = all(certificates.values())
    return {
        "status": (
            "PASS_EXPLICIT_SYMMETRY_REDUCED_ADM_TO_WEAK_STATIC_BRANCH"
            if passed
            else "FAIL_EXPLICIT_SYMMETRY_REDUCED_ADM_TO_WEAK_STATIC_BRANCH"
        ),
        "branch": {
            "N": "exp(epsilon*Phi)",
            "h_ij": "exp(-2*epsilon*Psi) delta_ij",
            "epsilon": "c^-2",
            "K_ij": "0",
            "D2_lambda": "0",
            "Lambda": "epsilon^2 Lambda_2 (fixed-a0 nonrelativistic scaling)",
        },
        "derived": {
            "direct_spatial_ricci": str(direct_ricci["scalar"]),
            "nonzero_christoffel_components": direct_ricci[
                "nonzero_christoffel_components"
            ],
            "N_sqrt_h_R3_epsilon2_pre_ibp": str(physical["eh_pre_ibp"]),
            "einstein_density_post_ibp": str(physical["eh_post_ibp"]),
            "y_leading": str(physical["y_leading"]),
            "mond_density_leading": str(physical["mond_leading"]),
            "point_particle_leading": str(physical["particle_leading"]),
            "weak_gravity_scale": str(physical["weak_gravity_scale"]),
            "normalized_dust_source": str(physical["dust_source"]),
            "cosmological_leading_background": str(
                sp.limit(
                    physical["cosmological_background_exact"],
                    physical["epsilon"],
                    0,
                    dir="+",
                )
            ),
            "cosmological_leading_field_term": str(
                physical["cosmological_field_residual"]
            ),
            "high_y_radial_euler": str(physical["high_y_euler"]),
            "auxiliary_trace_invariant": str(
                physical["auxiliary_trace_invariant"]
            ),
            "auxiliary_fourier_density": str(
                physical["auxiliary_fourier_density"]
            ),
            "lambda_euler_nonzero_k": str(physical["lambda_euler"]),
            "lambda_nonzero_k_solution": str(
                physical["lambda_nonzero_k_solution"]
            ),
            "lambda_euler_k0": str(physical["lambda_euler_k0"]),
            "auxiliary_velocity_hessian": str(
                physical["auxiliary_velocity_hessian"]
            ),
            "spherical_radial_density": str(
                physical["spherical_radial_density"]
            ),
        },
        "residuals": {
            "direct_spatial_ricci": str(direct_ricci["residual"]),
            "einstein_density": str(physical["eh_residual"]),
            "mond_argument": str(physical["y_residual"]),
            "mond_density": str(physical["mond_residual"]),
            "point_particle": str(physical["particle_residual"]),
            "planck_scaling": str(physical["planck_scaling_residual"]),
            "high_y_poisson": str(physical["high_y_poisson_residual"]),
            "cosmological_field": str(physical["cosmological_field_residual"]),
            "dust_source": str(physical["dust_source_residual"]),
            "auxiliary_trace": str(physical["auxiliary_trace_residual"]),
            "spherical_reduction": str(
                physical["spherical_reduction_residual"]
            ),
        },
        "mutations": {
            "spatial_sign_plus_one_residual": str(wrong_sign["eh_residual"]),
            "action_prefactor_one_residual": str(missing_half["eh_residual"]),
            "ell0_epsilon_power_zero_y_residual": str(
                wrong_ell0_scaling["y_residual"]
            ),
            "planck_epsilon_power_minus_one_source_residual": str(
                wrong_planck_scaling["dust_source_residual"]
            ),
            "Lambda_epsilon_power_one_field_residual": str(
                wrong_cosmological_scaling["cosmological_field_residual"]
            ),
        },
        "certificates": certificates,
        "nonclaims": [
            "not a full unrestricted ADM variation",
            "not a nonlinear Dirac closure proof",
            "not a PPN calculation",
            "not a resurrection of the dead regular-center branch",
        ],
    }


def main() -> int:
    results = build_results()
    print(json.dumps(results, indent=2, sort_keys=True, allow_nan=False))
    return 0 if results["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
