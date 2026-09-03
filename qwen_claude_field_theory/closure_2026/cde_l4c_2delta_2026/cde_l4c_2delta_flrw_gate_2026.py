#!/usr/bin/env python3
"""On-shell FLRW and finite-k principal gate for CDE-L4C-2Delta.

This is a deliberately scoped follow-on to ``cde_l4c_2delta_action_gate_2026``.
It derives the exactly homogeneous minisuperspace equations and the status of
the homogeneous multiplier zero modes.  It then studies the highest-spatial-
derivative scalar quadratic family on flat FLRW, retaining H and arbitrary
homogeneous multiplier backgrounds.

The principal family is not advertised as the complete finite-k FLRW action:
cuscuton/potential/matter terms with fewer spatial derivatives and the full
covariant clock equation are not used to manufacture a constraint.  A zero
exit status means that the displayed scoped algebra reproduced, not that the
candidate passed its full Dirac, stability, or cosmology gates.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp

from cde_l4c_2delta_action_gate_2026 import _derive_minkowski_adm_principal


def _poisson_bracket(
    first: sp.Expr,
    second: sp.Expr,
    coordinates: tuple[sp.Symbol, ...],
    momenta: tuple[sp.Symbol, ...],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(first, coordinate) * sp.diff(second, momentum)
            - sp.diff(first, momentum) * sp.diff(second, coordinate)
            for coordinate, momentum in zip(coordinates, momenta)
        )
    )


def _derive_background() -> dict[str, Any]:
    """Derive the exact homogeneous reduction before choosing multipliers."""

    H, lambda_s_bar, lambda_K_bar = sp.symbols(
        "H lambda_s_bar lambda_K_bar", real=True
    )
    a_squared = sp.Integer(0)
    R3 = sp.Integer(0)
    D2_C_slip = sp.Integer(0)
    D2_K = sp.Integer(0)
    multiplier_density = lambda_s_bar * D2_C_slip + lambda_K_bar * D2_K
    E_lambda_s = sp.diff(multiplier_density, lambda_s_bar)
    E_lambda_K = sp.diff(multiplier_density, lambda_K_bar)
    multiplier_equations = sp.Matrix([E_lambda_s, E_lambda_K])
    multiplier_coefficient_matrix = multiplier_equations.jacobian(
        (lambda_s_bar, lambda_K_bar)
    )

    return {
        "H": H,
        "lambda_s_bar": lambda_s_bar,
        "lambda_K_bar": lambda_K_bar,
        "a_squared": a_squared,
        "R3": R3,
        "D2_C_slip": D2_C_slip,
        "D2_K": D2_K,
        "multiplier_density": multiplier_density,
        "E_lambda_s": E_lambda_s,
        "E_lambda_K": E_lambda_K,
        "multiplier_equations": multiplier_equations,
        "multiplier_coefficient_matrix": multiplier_coefficient_matrix,
        "homogeneous_multipliers_fixed": multiplier_coefficient_matrix.rank() > 0,
        "interpretation": (
            "The homogeneous Euler equations leave lambda_s_bar(t) and "
            "lambda_K_bar(t) arbitrary.  They are multiplier zero modes, not "
            "derived zero backgrounds."
        ),
    }


def _derive_minisuperspace() -> dict[str, Any]:
    """Vary flat-FLRW EH + positive-branch cuscuton + arbitrary matter."""

    t = sp.symbols("t", real=True)
    scale = sp.Function("a")(t)
    N = sp.Function("N")(t)
    T = sp.Function("T")(t)
    T_dot = sp.diff(T, t)
    scale_dot = sp.diff(scale, t)
    Mpl2, Mc2, Lambda = sp.symbols("M_Pl_sq M_c_sq Lambda", positive=True)
    V = sp.Function("V")
    potential = V(T)
    matter_lagrangian = sp.Function("L_m")(N, scale, t)
    rho = sp.Function("rho")(t)
    pressure = sp.Function("p")(t)
    H = sp.simplify(scale_dot / (scale * N))

    # F_exp(0)=0 in the frozen convention.  Both spatial-Laplacian multiplier
    # terms vanish exactly on homogeneous fields.  On the T_dot>0 branch,
    # N sqrt(gamma) M_c^2 sqrt(X)=a^3 M_c^2 T_dot.
    lagrangian = (
        -3 * Mpl2 * scale * scale_dot**2 / N
        - Mpl2 * Lambda * N * scale**3
        + scale**3 * Mc2 * T_dot
        - N * scale**3 * potential
        + matter_lagrangian
    )

    E_N = sp.simplify(sp.diff(lagrangian, N))
    E_T = sp.simplify(
        sp.diff(lagrangian, T)
        - sp.diff(sp.diff(lagrangian, T_dot), t)
    )
    E_scale = sp.simplify(
        sp.diff(lagrangian, scale)
        - sp.diff(sp.diff(lagrangian, scale_dot), t)
    )

    matter_N_derivative = sp.diff(matter_lagrangian, N)
    matter_scale_derivative = sp.diff(matter_lagrangian, scale)
    matter_replacements = {
        matter_N_derivative: -scale**3 * rho,
        matter_scale_derivative: 3 * N * scale**2 * pressure,
    }
    E_N_matter = sp.simplify(E_N.xreplace(matter_replacements))
    E_scale_matter = sp.simplify(E_scale.xreplace(matter_replacements))

    friedmann_equation = sp.simplify(E_N_matter / scale**3)
    expected_friedmann = sp.simplify(
        3 * Mpl2 * H**2 - Mpl2 * Lambda - potential - rho
    )
    friedmann_residual = sp.simplify(
        friedmann_equation - expected_friedmann
    )

    cuscuton_equation = sp.simplify(-E_T / (N * scale**3))
    expected_cuscuton = sp.simplify(3 * Mc2 * H + sp.diff(potential, T))
    cuscuton_residual = sp.simplify(cuscuton_equation - expected_cuscuton)

    scale_equation = sp.simplify(E_scale_matter / (3 * N * scale**2))
    # SymPy expands H into a_dot/(a N), so a literal H**2 substitution does
    # not eliminate the Friedmann contribution.  The lapse/scale Euler
    # combination below performs the on-shell elimination invariantly.
    scale_after_friedmann = sp.simplify(
        scale_equation - friedmann_equation
    )
    expected_raychaudhuri = sp.simplify(
        2 * Mpl2 * sp.diff(H, t) / N
        + rho
        + pressure
        + Mc2 * T_dot / N
    )
    raychaudhuri_residual = sp.simplify(
        scale_after_friedmann - expected_raychaudhuri
    )

    V0 = sp.symbols("V_0", real=True)
    mass_sq = sp.symbols("m_T_sq", positive=True)
    quadratic_potential = V0 + sp.Rational(1, 2) * mass_sq * T**2
    H_from_quadratic_potential = sp.solve(
        sp.Eq(
            expected_cuscuton.subs(potential, quadratic_potential).doit(),
            0,
        ),
        H,
        dict=True,
    )[0][H]

    # Do not confuse solving the cuscuton equation alone with a cosmological
    # existence proof.  Impose the vacuum Friedmann and Raychaudhuri equations
    # simultaneously, derive the required potential parameters, then build an
    # explicit positive-clock branch T=t-T_* and integrate H=a_dot/a.
    clock_value, clock_velocity = sp.symbols("T_value T_dot_value", real=True)
    H_algebraic = -mass_sq * clock_value / (3 * Mc2)
    friedmann_vacuum_polynomial = sp.expand(
        3 * Mpl2 * H_algebraic**2
        - Mpl2 * Lambda
        - V0
        - sp.Rational(1, 2) * mass_sq * clock_value**2
    )
    raychaudhuri_vacuum_coefficient = sp.simplify(
        -2 * Mpl2 * mass_sq * clock_velocity / (3 * Mc2)
        + Mc2 * clock_velocity
    )
    consistency_equations = (
        friedmann_vacuum_polynomial.coeff(clock_value, 2),
        friedmann_vacuum_polynomial.coeff(clock_value, 0),
        sp.diff(raychaudhuri_vacuum_coefficient, clock_velocity),
    )
    parameter_solutions = sp.solve(
        consistency_equations, (mass_sq, V0), dict=True
    )
    parameter_solution = parameter_solutions[0] if parameter_solutions else {}

    T_star, scale_normalization = sp.symbols("T_star a_star", positive=True)
    T_witness = t - T_star
    H_witness = sp.simplify(
        H_algebraic.subs(clock_value, T_witness).subs(parameter_solution)
    )
    scale_factor = sp.simplify(
        scale_normalization * sp.exp(sp.integrate(H_witness, t))
    )
    witness_potential = sp.simplify(
        quadratic_potential.subs(T, T_witness).subs(parameter_solution)
    )
    witness_potential_derivative = sp.simplify(
        mass_sq * T_witness
    ).subs(parameter_solution)
    witness_equation_residuals = (
        sp.simplify(
            3 * Mpl2 * H_witness**2
            - Mpl2 * Lambda
            - witness_potential
        ),
        sp.simplify(3 * Mc2 * H_witness + witness_potential_derivative),
        sp.simplify(
            2 * Mpl2 * sp.diff(H_witness, t)
            + Mc2 * sp.diff(T_witness, t)
        ),
    )
    vacuum_expanding_witness = {
        "t": t,
        "T_star": T_star,
        "T": T_witness,
        "T_dot": sp.diff(T_witness, t),
        "parameter_solution": parameter_solution,
        "H_witness": H_witness,
        "scale_factor": scale_factor,
        "potential": witness_potential,
        "equation_residuals": witness_equation_residuals,
        "expanding_interval": "t<T_star",
    }

    return {
        "t": t,
        "a": scale,
        "N": N,
        "T": T,
        "T_dot": T_dot,
        "Mpl2": Mpl2,
        "Mc2": Mc2,
        "Lambda": Lambda,
        "V": potential,
        "rho": rho,
        "pressure": pressure,
        "H": H,
        "L_m": matter_lagrangian,
        "L": lagrangian,
        "E_N": E_N,
        "E_T": E_T,
        "E_a": E_scale,
        "friedmann_equation": friedmann_equation,
        "friedmann_residual": friedmann_residual,
        "cuscuton_equation": cuscuton_equation,
        "cuscuton_residual": cuscuton_residual,
        "raychaudhuri_equation": scale_after_friedmann,
        "raychaudhuri_residual": raychaudhuri_residual,
        "quadratic_potential": quadratic_potential,
        "H_from_quadratic_potential": H_from_quadratic_potential,
        "nonzero_H_allowed": sp.simplify(H_from_quadratic_potential) != 0,
        "vacuum_expanding_witness": vacuum_expanding_witness,
        "matter_conservation_required_for_equation_dependence": True,
    }


def _derive_principal_family() -> dict[str, Any]:
    """Close the finite-k scalar principal Dirac chain on flat FLRW.

    The derivation retains the combinations fixed by the ADM geometry:
    Theta=dot(Psi)+H Phi and, after spatial integration by parts,
    delta(lambda_A)+lambda_A_bar Phi.  Terms with fewer spatial derivatives
    are deliberately outside this principal-symbol calculation.
    """

    A, q = sp.symbols("A q", positive=True, nonzero=True)
    H, lambda_s_bar, lambda_K_bar = sp.symbols(
        "H lambda_s_bar lambda_K_bar", real=True
    )
    Phi, Psi, B, lambda_s, lambda_K = sp.symbols(
        "Phi Psi B delta_lambda_s delta_lambda_K", real=True
    )
    p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K = sp.symbols(
        "p_Phi p_Psi p_B p_lambda_s p_lambda_K", real=True
    )
    Psi_dot = sp.symbols("Psi_dot", real=True)

    coordinates = (Phi, Psi, B, lambda_s, lambda_K)
    momenta = (p_Phi, p_Psi, p_B, p_lambda_s, p_lambda_K)
    phase_variables = coordinates + momenta
    theta = Psi_dot + H * Phi
    effective_lambda_s = lambda_s + lambda_s_bar * Phi
    effective_lambda_K = lambda_K + lambda_K_bar * Phi

    # Import the zero-background block generated directly from the ADM action.
    # The FLRW expression below is a geometry-motivated promotion via
    # Theta=dot(Psi)+H Phi and N lambda perturbations; it is deliberately not
    # mislabeled as a complete second-order expansion on FLRW.
    y = sp.symbols("y", positive=True)
    correction = 2 * ((1 + y) * sp.exp(-y) - 1)
    minkowski_adm = _derive_minkowski_adm_principal(correction, y)
    zero_background_lagrangian = sp.factor(
        minkowski_adm["generated_zero_field_lagrangian"].subs(
            {
                minkowski_adm["A"]: A,
                minkowski_adm["k"]: q,
                minkowski_adm["Phi"]: Phi,
                minkowski_adm["Psi"]: Psi,
                minkowski_adm["B"]: B,
                minkowski_adm["lambda_s"]: lambda_s,
                minkowski_adm["lambda_K"]: lambda_K,
                minkowski_adm["Psi_dot"]: Psi_dot,
            },
            simultaneous=True,
        )
    )
    lagrangian = sp.factor(
        zero_background_lagrangian.subs(
            {
                Psi_dot: theta,
                lambda_s: effective_lambda_s,
                lambda_K: effective_lambda_K,
            },
            simultaneous=True,
        )
    )
    minkowski_adm_source_residual = sp.simplify(
        lagrangian.subs(
            {H: 0, lambda_s_bar: 0, lambda_K_bar: 0}
        )
        - zero_background_lagrangian
    )

    # Check the source of the background shifts rather than inserting them as
    # unexplained replacements: N lambda=(1+eps Phi)(bar+eps delta).
    eps = sp.symbols("epsilon", real=True)
    product_s = (1 + eps * Phi) * (lambda_s_bar + eps * lambda_s)
    product_K = (1 + eps * Phi) * (lambda_K_bar + eps * lambda_K)
    background_shift_identity_s = sp.simplify(
        sp.expand(product_s).coeff(eps, 1) - effective_lambda_s
    )
    background_shift_identity_K = sp.simplify(
        sp.expand(product_K).coeff(eps, 1) - effective_lambda_K
    )

    derived_p_Psi = sp.factor(sp.diff(lagrangian, Psi_dot))
    velocity_solution = sp.solve(
        sp.Eq(p_Psi, derived_p_Psi), Psi_dot, dict=True
    )[0][Psi_dot]
    canonical_hamiltonian = sp.factor(
        (p_Psi * Psi_dot - lagrangian).subs(Psi_dot, velocity_solution)
    )

    primaries = (p_Phi, p_B, p_lambda_s, p_lambda_K)
    secondaries = tuple(
        sp.factor(
            _poisson_bracket(
                primary, canonical_hamiltonian, coordinates, momenta
            )
        )
        for primary in primaries
    )
    constraints = primaries + secondaries
    poisson_matrix = sp.Matrix(
        [
            [
                _poisson_bracket(first, second, coordinates, momenta)
                for second in constraints
            ]
            for first in constraints
        ]
    ).applyfunc(sp.factor)
    poisson_determinant = sp.factor(poisson_matrix.det())
    poisson_rank = poisson_matrix.rank()
    constraint_jacobian = sp.Matrix(constraints).jacobian(phase_variables)
    constraint_jacobian_rank = constraint_jacobian.rank()

    primary_multipliers = sp.symbols(f"u0:{len(primaries)}", real=True)
    total_hamiltonian = canonical_hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(primary_multipliers, primaries)
    )
    preservation_equations = tuple(
        sp.factor(
            _poisson_bracket(
                secondary, total_hamiltonian, coordinates, momenta
            )
        )
        for secondary in secondaries
    )
    preservation_solutions = sp.solve(
        preservation_equations, primary_multipliers, dict=True
    )
    preservation_solution = preservation_solutions[0] if preservation_solutions else {}
    preservation_residuals = tuple(
        sp.simplify(equation.subs(preservation_solution))
        for equation in preservation_equations
    )

    solved_variables = (
        p_Phi,
        p_B,
        p_lambda_s,
        p_lambda_K,
        Phi,
        lambda_s,
        B,
        lambda_K,
    )
    constraint_solutions = sp.solve(
        constraints, solved_variables, dict=True, simplify=False
    )
    constraint_solution = constraint_solutions[0] if constraint_solutions else {}
    reduced_hamiltonian = sp.simplify(
        canonical_hamiltonian.subs(constraint_solution)
    )

    dPsi, dp_Psi = sp.symbols("dPsi dp_Psi")

    def pulled_differential(expression: sp.Expr) -> sp.Expr:
        reduced = sp.simplify(expression.subs(constraint_solution))
        return sp.simplify(
            sp.diff(reduced, Psi) * dPsi
            + sp.diff(reduced, p_Psi) * dp_Psi
        )

    canonical_one_form_pullback = sp.simplify(
        sum(
            momentum.subs(constraint_solution) * pulled_differential(coordinate)
            for coordinate, momentum in zip(coordinates, momenta)
        )
    )

    second_class_count = poisson_rank
    first_class_count = len(constraints) - second_class_count
    phase_dimension = len(phase_variables)
    configuration_dof = sp.Rational(
        phase_dimension - 2 * first_class_count - second_class_count,
        2,
    )
    k_zero_poisson_matrix = poisson_matrix.subs(q, 0)

    # Restart the homogeneous chain from q=0 rather than interpreting the
    # substituted finite-k matrix as a complete homogeneous calculation.
    homogeneous_lagrangian = sp.simplify(lagrangian.subs(q, 0))
    homogeneous_p_Psi = sp.diff(homogeneous_lagrangian, Psi_dot)
    homogeneous_velocity_solution = sp.solve(
        sp.Eq(p_Psi, homogeneous_p_Psi), Psi_dot, dict=True
    )[0][Psi_dot]
    homogeneous_hamiltonian = sp.factor(
        (p_Psi * Psi_dot - homogeneous_lagrangian).subs(
            Psi_dot, homogeneous_velocity_solution
        )
    )
    homogeneous_lapse_secondary = sp.factor(
        _poisson_bracket(
            p_Phi, homogeneous_hamiltonian, coordinates, momenta
        )
    )

    return {
        "A": A,
        "q": q,
        "H": H,
        "lambda_s_bar": lambda_s_bar,
        "lambda_K_bar": lambda_K_bar,
        "coordinates": coordinates,
        "momenta": momenta,
        "theta": theta,
        "effective_lambda_s": effective_lambda_s,
        "effective_lambda_K": effective_lambda_K,
        "background_shift_identity_s": background_shift_identity_s,
        "background_shift_identity_K": background_shift_identity_K,
        "minkowski_adm_source_residual": minkowski_adm_source_residual,
        "lagrangian": lagrangian,
        "zero_background_lagrangian": zero_background_lagrangian,
        "derived_p_Psi": derived_p_Psi,
        "velocity_solution": velocity_solution,
        "canonical_hamiltonian": canonical_hamiltonian,
        "primaries": primaries,
        "secondaries": secondaries,
        "constraints": constraints,
        "poisson_matrix": poisson_matrix,
        "poisson_determinant": poisson_determinant,
        "poisson_rank": poisson_rank,
        "constraint_jacobian": constraint_jacobian,
        "constraint_jacobian_rank": constraint_jacobian_rank,
        "preservation_equations": preservation_equations,
        "preservation_solution": preservation_solution,
        "preservation_residuals": preservation_residuals,
        "tertiary_constraints_found": any(
            residual != 0 for residual in preservation_residuals
        ),
        "constraint_solution": constraint_solution,
        "canonical_one_form_pullback": canonical_one_form_pullback,
        "reduced_hamiltonian": reduced_hamiltonian,
        "phase_dimension": phase_dimension,
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "configuration_dof": configuration_dof,
        "k_zero_poisson_matrix": k_zero_poisson_matrix,
        "k_zero_poisson_rank": k_zero_poisson_matrix.rank(),
        "finite_k_matrix_substitution_is_homogeneous_chain": False,
        "homogeneous_restart": {
            "lagrangian": homogeneous_lagrangian,
            "p_Psi": homogeneous_p_Psi,
            "velocity_solution": homogeneous_velocity_solution,
            "canonical_hamiltonian": homogeneous_hamiltonian,
            "lapse_secondary": homogeneous_lapse_secondary,
        },
        "background_parameters_drop_from_determinant": all(
            sp.diff(poisson_determinant, parameter) == 0
            for parameter in (H, lambda_s_bar, lambda_K_bar)
        ),
    }


def derive_flrw_gate() -> dict[str, Any]:
    background = _derive_background()
    minisuperspace = _derive_minisuperspace()
    principal = _derive_principal_family()
    return {
        "background": background,
        "minisuperspace": minisuperspace,
        "principal": principal,
        "scope": {
            "homogeneous_action_varied": True,
            "homogeneous_multiplier_zero_modes_derived": True,
            "highest_spatial_derivative_flrw_family_derived": False,
            "geometry_motivated_principal_family": True,
            "full_finite_k_flrw_action_derived": False,
            "cuscuton_lower_derivative_terms_in_principal_rank": False,
            "full_covariant_clock_dirac_chain": False,
            "global_nonlinear_dof_theorem": False,
        },
        "verdict": "CONDITIONAL_OBSTRUCTION_ON_FLRW_PRINCIPAL_FAMILY",
        "next_unavoidable_calculation": (
            "Derive the complete second-order scalar action on an on-shell "
            "FLRW solution, including all k^0 and H-dependent cuscuton, "
            "potential, matter, and multiplier terms; then run the nonlinear "
            "Dirac algorithm as the MOND gradient approaches zero from above."
        ),
    }


def _check(label: str, condition: Any, detail: str = "") -> bool:
    passed = bool(condition)
    suffix = f" ({detail})" if detail else ""
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}{suffix}")
    return passed


def main() -> int:
    result = derive_flrw_gate()
    background = result["background"]
    mini = result["minisuperspace"]
    principal = result["principal"]
    checks: list[bool] = []

    print("=" * 96)
    print("CDE-L4C-2DELTA: ON-SHELL FLRW BACKGROUND AND FINITE-k PRINCIPAL GATE")
    print("=" * 96)

    print("\n[1] Exact homogeneous multiplier sector")
    print("  D2 C_slip =", background["D2_C_slip"])
    print("  D2 K      =", background["D2_K"])
    print("  E_lambda_s, E_lambda_K =", background["E_lambda_s"], background["E_lambda_K"])
    print("  multiplier coefficient rank =", background["multiplier_coefficient_matrix"].rank())
    print(" ", background["interpretation"])
    checks.append(_check(
        "homogeneous multiplier equations vanish and do not fix their zero modes",
        background["E_lambda_s"] == 0
        and background["E_lambda_K"] == 0
        and not background["homogeneous_multipliers_fixed"],
    ))

    print("\n[2] Minisuperspace Euler-Lagrange equations")
    print("  Friedmann =", mini["friedmann_equation"])
    print("  cuscuton  =", mini["cuscuton_equation"])
    print("  Raychaudhuri after Friedmann =", mini["raychaudhuri_equation"])
    print("  H for V=V0+m_T^2 T^2/2 =", mini["H_from_quadratic_potential"])
    checks.append(_check(
        "Friedmann, cuscuton, and Raychaudhuri residuals vanish",
        mini["friedmann_residual"] == 0
        and mini["cuscuton_residual"] == 0
        and mini["raychaudhuri_residual"] == 0,
    ))
    checks.append(_check(
        "the homogeneous equations permit H nonzero",
        mini["nonzero_H_allowed"],
    ))
    witness = mini["vacuum_expanding_witness"]
    print("  simultaneous vacuum tuning =", witness["parameter_solution"])
    print("  T witness =", witness["T"])
    print("  H witness =", witness["H_witness"])
    print("  a witness =", witness["scale_factor"])
    print("  three witness residuals =", witness["equation_residuals"])
    checks.append(_check(
        "one explicit expanding interval solves all three background equations",
        bool(witness["parameter_solution"])
        and witness["H_witness"] != 0
        and all(residual == 0 for residual in witness["equation_residuals"]),
        witness["expanding_interval"],
    ))

    print("\n[3] Geometry-motivated FLRW finite-k principal family")
    print("  Theta =", principal["theta"])
    print("  effective delta lambda_s =", principal["effective_lambda_s"])
    print("  effective delta lambda_K =", principal["effective_lambda_K"])
    print("  L_principal =", principal["lagrangian"])
    print("  p_Psi =", principal["derived_p_Psi"])
    checks.append(_check(
        "the zero-H, zero-multiplier limit reproduces the ADM-generated Minkowski block",
        sp.simplify(
            principal["lagrangian"].subs(
                {
                    principal["H"]: 0,
                    principal["lambda_s_bar"]: 0,
                    principal["lambda_K_bar"]: 0,
                }
            )
            - principal["zero_background_lagrangian"]
        ) == 0
        and principal["minkowski_adm_source_residual"] == 0,
    ))

    print("\n[4] Generated Dirac chain")
    print("  primaries   =", principal["primaries"])
    print("  secondaries =", principal["secondaries"])
    print("  determinant =", principal["poisson_determinant"])
    print("  Poisson rank / Jacobian rank =", principal["poisson_rank"], principal["constraint_jacobian_rank"])
    print("  preservation multipliers =", principal["preservation_solution"])
    checks.append(_check(
        "the generated constraints are regular and preservation closes in this family",
        principal["poisson_determinant"] != 0
        and principal["poisson_rank"] == principal["constraint_jacobian_rank"]
        and not principal["tertiary_constraints_found"],
    ))
    checks.append(_check(
        "H and both arbitrary multiplier backgrounds drop from the PB determinant",
        principal["background_parameters_drop_from_determinant"],
    ))

    print("\n[5] Constraint surface and reduced pair")
    print("  solution =", principal["constraint_solution"])
    print("  pulled-back one-form =", principal["canonical_one_form_pullback"])
    print("  H_reduced =", principal["reduced_hamiltonian"])
    print("  scalar configuration DOF =", principal["configuration_dof"])
    checks.append(_check(
        "one scalar canonical pair survives in the FLRW principal family",
        principal["configuration_dof"] > 0
        and principal["canonical_one_form_pullback"] != 0,
    ))

    print("\n[6] Homogeneous symbol and scope")
    print("  finite-k rank / k=0 rank =", principal["poisson_rank"], principal["k_zero_poisson_rank"])
    homogeneous = principal["homogeneous_restart"]
    print("  direct q=0 L =", homogeneous["lagrangian"])
    print("  direct q=0 H_c =", homogeneous["canonical_hamiltonian"])
    print("  direct q=0 lapse secondary =", homogeneous["lapse_secondary"])
    print("  full finite-k FLRW action derived =", result["scope"]["full_finite_k_flrw_action_derived"])
    print("  global nonlinear theorem =", result["scope"]["global_nonlinear_dof_theorem"])
    checks.append(_check(
        "k=0 is rank-distinct and no global nonlinear claim is made",
        principal["k_zero_poisson_rank"] != principal["poisson_rank"]
        and not result["scope"]["global_nonlinear_dof_theorem"],
    ))
    checks.append(_check(
        "the homogeneous chain is restarted rather than inferred from the finite-k matrix",
        not principal["finite_k_matrix_substitution_is_homogeneous_chain"]
        and homogeneous["lapse_secondary"] != 0,
    ))

    print("\n[VERDICT]")
    print(" ", result["verdict"])
    print("  The exact homogeneous equations leave both multiplier zero modes arbitrary.")
    print("  Keeping those backgrounds and H in the geometry-motivated principal family does not")
    print("  remove the finite-k scalar pair. This is a conditional obstruction: the direct")
    print("  q=0 restart differs, and the complete quadratic FLRW action plus nonlinear")
    print("  irregular constraint remain owed.")
    print("  Next:", result["next_unavoidable_calculation"])

    passed = sum(checks)
    print(f"\nChecks completed: {passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
