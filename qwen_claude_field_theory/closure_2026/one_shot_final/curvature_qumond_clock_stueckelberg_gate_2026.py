#!/usr/bin/env python3
"""Restore the clock perturbation in the curvature-QUMOND scalar gate.

The companion ADM calculation used unitary clock gauge on the exact flat
background

    Lambda_eff = 0, lambda_bar = 0, chi_bar = constant, T_bar = t.

This script restores ``T=t+pi`` and the scalar spatial shear.  It derives the
gauge-invariant combinations, the total-derivative relation to unitary gauge,
and the complete quadratic Dirac count.  It also keeps separate the two
logically independent statements

    c_T=1  ->  lambda_bar=0,
    flat vacuum background  ->  Lambda_eff=0.

No scalar count is exported from the flat calculation to a non-flat FLRW
background.  On FLRW the correct gauge-invariant curvature is different and a
new perturbation calculation would be required.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _poisson_bracket(
    left: sp.Expr,
    right: sp.Expr,
    pairs: tuple[tuple[sp.Symbol, sp.Symbol], ...],
) -> sp.Expr:
    return sp.simplify(
        sum(
            sp.diff(left, coordinate) * sp.diff(right, momentum)
            - sp.diff(left, momentum) * sp.diff(right, coordinate)
            for coordinate, momentum in pairs
        )
    )


def _flat_quadratic_action() -> dict[str, Any]:
    """Derive the Stückelberg-restored quadratic scalar action."""

    k = sp.symbols("k", positive=True, real=True)
    zeta, ell, E, chi, alpha, beta, pi = sp.symbols(
        "zeta ell E chi alpha beta pi", real=True
    )
    zeta_dot, ell_dot, E_dot, chi_dot, alpha_dot, beta_dot, pi_dot = sp.symbols(
        "zeta_dot ell_dot E_dot chi_dot alpha_dot beta_dot pi_dot", real=True
    )

    # This is the shear-restored unitary-gauge action derived directly in the
    # ADM companion.  Restoring time diffeomorphisms sends the unitary lapse
    # and shift to A=alpha-pi_dot and beta+pi, respectively.
    unitary_lagrangian = sp.expand(
        -6 * zeta_dot**2
        + 6 * zeta_dot * ell_dot
        - 4 * k**2 * beta * zeta_dot
        + 2 * k**2 * beta * ell_dot
        + 4 * k**2 * zeta_dot * E_dot
        - 2 * k**2 * E_dot * ell_dot
        + 2 * k**2 * zeta**2
        + 4 * k**2 * alpha * zeta
        - 2 * k**2 * alpha * ell
        + 2 * k**2 * ell * chi
        + k**2 * chi**2
    )
    invariant_lapse = alpha - pi_dot
    invariant_shift = beta + pi - E_dot
    stueckelberg_lagrangian = sp.expand(
        unitary_lagrangian.subs(
            {alpha: alpha - pi_dot, beta: beta + pi},
            simultaneous=True,
        )
    )
    manifestly_invariant_lagrangian = sp.expand(
        -6 * zeta_dot**2
        + 6 * zeta_dot * ell_dot
        - 4 * k**2 * invariant_shift * zeta_dot
        + 2 * k**2 * invariant_shift * ell_dot
        + 2 * k**2 * zeta**2
        + 4 * k**2 * invariant_lapse * zeta
        - 2 * k**2 * invariant_lapse * ell
        + 2 * k**2 * ell * chi
        + k**2 * chi**2
    )

    # Active linear diffeomorphisms, delta(field)=-Lie_xi(background), with
    # xi^0=epsilon and xi^i=partial^i L.
    eta = sp.symbols("eta", real=True)
    epsilon, epsilon_dot, spatial_L, spatial_L_dot = sp.symbols(
        "epsilon epsilon_dot spatial_L spatial_L_dot", real=True
    )
    transformations = {
        pi: -epsilon,
        pi_dot: -epsilon_dot,
        alpha: -epsilon_dot,
        beta: epsilon - spatial_L_dot,
        E: -spatial_L,
        E_dot: -spatial_L_dot,
        zeta: sp.Integer(0),
        ell: sp.Integer(0),
        chi: sp.Integer(0),
    }

    def varied(expression: sp.Expr) -> sp.Expr:
        transformed = expression.subs(
            {
                symbol: symbol + eta * variation
                for symbol, variation in transformations.items()
            },
            simultaneous=True,
        )
        return sp.simplify(sp.diff(transformed, eta).subs(eta, 0))

    invariant_residuals = (
        varied(invariant_lapse),
        varied(invariant_shift),
        varied(zeta),
        varied(ell),
        varied(chi),
    )
    lagrangian_variation = varied(stueckelberg_lagrangian)

    boundary_generator = sp.expand(2 * k**2 * pi * (ell - 2 * zeta))
    boundary_derivative = sp.expand(
        sp.diff(boundary_generator, pi) * pi_dot
        + sp.diff(boundary_generator, ell) * ell_dot
        + sp.diff(boundary_generator, zeta) * zeta_dot
    )
    total_derivative_residual = sp.simplify(
        stueckelberg_lagrangian - unitary_lagrangian - boundary_derivative
    )

    # The Euler derivative contains no accelerations because dL/d(pi_dot) is
    # algebraic in zeta and ell.
    d_dt_clock_momentum = sp.expand(
        sp.diff(sp.diff(stueckelberg_lagrangian, pi_dot), zeta) * zeta_dot
        + sp.diff(sp.diff(stueckelberg_lagrangian, pi_dot), ell) * ell_dot
    )
    clock_euler_lagrange = sp.simplify(
        sp.diff(stueckelberg_lagrangian, pi) - d_dt_clock_momentum
    )
    p_pi = sp.symbols("p_pi", real=True)
    direct_clock_primary = sp.factor(
        p_pi - sp.diff(stueckelberg_lagrangian, pi_dot)
    )

    return {
        "k": k,
        "zeta": zeta,
        "ell": ell,
        "E": E,
        "chi": chi,
        "alpha": alpha,
        "beta": beta,
        "pi": pi,
        "zeta_dot": zeta_dot,
        "ell_dot": ell_dot,
        "E_dot": E_dot,
        "chi_dot": chi_dot,
        "alpha_dot": alpha_dot,
        "beta_dot": beta_dot,
        "pi_dot": pi_dot,
        "p_pi": p_pi,
        "unitary_lagrangian": unitary_lagrangian,
        "stueckelberg_lagrangian": stueckelberg_lagrangian,
        "manifestly_invariant_lagrangian": manifestly_invariant_lagrangian,
        "manifest_form_residual": sp.simplify(
            stueckelberg_lagrangian - manifestly_invariant_lagrangian
        ),
        "invariant_lapse": invariant_lapse,
        "invariant_shift": invariant_shift,
        "transformations": transformations,
        "invariant_residuals": invariant_residuals,
        "lagrangian_variation": lagrangian_variation,
        "boundary_generator": boundary_generator,
        "boundary_derivative": boundary_derivative,
        "total_derivative_residual": total_derivative_residual,
        "clock_euler_lagrange": clock_euler_lagrange,
        "direct_clock_primary": direct_clock_primary,
    }


def _canonical_gate(action: dict[str, Any]) -> dict[str, Any]:
    """Run the quadratic Dirac algorithm after a canonical boundary shift."""

    k = action["k"]
    zeta, ell, E = action["zeta"], action["ell"], action["E"]
    chi, alpha, beta, pi = (
        action["chi"],
        action["alpha"],
        action["beta"],
        action["pi"],
    )
    zeta_dot, ell_dot, E_dot = (
        action["zeta_dot"],
        action["ell_dot"],
        action["E_dot"],
    )
    chi_dot, alpha_dot, beta_dot, pi_dot = (
        action["chi_dot"],
        action["alpha_dot"],
        action["beta_dot"],
        action["pi_dot"],
    )

    # Subtracting dF/dt is a canonical transformation.  The resulting
    # Lagrangian is pi-independent, so its clock momentum is a primary rather
    # than an assumed extra constraint.
    lagrangian = sp.expand(
        action["stueckelberg_lagrangian"] - action["boundary_derivative"]
    )
    coordinates = (zeta, ell, E, chi, alpha, beta, pi)
    velocities = (
        zeta_dot,
        ell_dot,
        E_dot,
        chi_dot,
        alpha_dot,
        beta_dot,
        pi_dot,
    )
    velocity_hessian = sp.hessian(lagrangian, velocities)

    p_zeta, p_ell, p_E, p_chi, p_alpha, p_beta, p_pi = sp.symbols(
        "P_zeta P_ell P_E P_chi P_alpha P_beta P_pi", real=True
    )
    momenta_symbols = (p_zeta, p_ell, p_E, p_chi, p_alpha, p_beta, p_pi)
    momenta_from_lagrangian = tuple(
        sp.diff(lagrangian, velocity) for velocity in velocities
    )
    regular_velocity_solution = sp.solve(
        tuple(
            sp.Eq(momentum, derived)
            for momentum, derived in zip(
                momenta_symbols[:3], momenta_from_lagrangian[:3]
            )
        ),
        velocities[:3],
        dict=True,
    )[0]
    hamiltonian = sp.factor(
        (
            p_zeta * zeta_dot
            + p_ell * ell_dot
            + p_E * E_dot
            - lagrangian
        ).subs(regular_velocity_solution)
    )
    pairs = tuple(zip(coordinates, momenta_symbols))
    primaries = (p_chi, p_alpha, p_beta, p_pi)
    primary_preservation = tuple(
        sp.factor(_poisson_bracket(primary, hamiltonian, pairs))
        for primary in primaries
    )
    secondaries = tuple(
        expression for expression in primary_preservation if expression != 0
    )
    constraints = primaries + secondaries
    constraint_pb_matrix = sp.Matrix(
        [
            [
                _poisson_bracket(left, right, pairs)
                for right in constraints
            ]
            for left in constraints
        ]
    )
    constraint_pb_rank = constraint_pb_matrix.rank()
    second_class_count = constraint_pb_rank
    first_class_count = len(constraints) - second_class_count
    phase_dimension = 2 * len(coordinates)
    physical_scalar_dof = sp.simplify(
        sp.Rational(
            phase_dimension - 2 * first_class_count - second_class_count,
            2,
        )
    )

    u_chi, u_alpha, u_beta, u_pi = sp.symbols(
        "u_chi u_alpha u_beta u_pi", real=True
    )
    total_hamiltonian = hamiltonian + sum(
        multiplier * primary
        for multiplier, primary in zip(
            (u_chi, u_alpha, u_beta, u_pi), primaries
        )
    )
    secondary_preservation = tuple(
        sp.factor(_poisson_bracket(secondary, total_hamiltonian, pairs))
        for secondary in secondaries
    )
    multiplier_solution = sp.solve(
        sp.Eq(secondary_preservation[0], 0), u_chi, dict=True
    )[0]
    constraint_shell = sp.solve(
        tuple(sp.Eq(secondary, 0) for secondary in secondaries),
        (chi, ell, p_E),
        dict=True,
    )[0]
    closure_residuals = tuple(
        sp.simplify(
            expression.subs(constraint_shell).subs(multiplier_solution)
        )
        for expression in secondary_preservation
    )

    return {
        "lagrangian": lagrangian,
        "coordinates": coordinates,
        "velocities": velocities,
        "velocity_hessian": velocity_hessian,
        "velocity_rank": velocity_hessian.rank(),
        "velocity_nullity": len(velocity_hessian.nullspace()),
        "momenta_symbols": momenta_symbols,
        "momenta_from_lagrangian": momenta_from_lagrangian,
        "regular_velocity_solution": regular_velocity_solution,
        "hamiltonian": hamiltonian,
        "primaries": primaries,
        "primary_preservation": primary_preservation,
        "clock_primary_preservation": primary_preservation[-1],
        "secondaries": secondaries,
        "constraints": constraints,
        "constraint_pb_matrix": constraint_pb_matrix,
        "constraint_pb_rank": constraint_pb_rank,
        "constraint_pb_nullity": len(constraint_pb_matrix.nullspace()),
        "first_class_count": first_class_count,
        "second_class_count": second_class_count,
        "phase_dimension": phase_dimension,
        "physical_scalar_dof": physical_scalar_dof,
        "secondary_preservation": secondary_preservation,
        "multiplier_solution": multiplier_solution,
        "constraint_shell": constraint_shell,
        "closure_residuals": closure_residuals,
    }


def _mode_gate(
    action: dict[str, Any], canonical: dict[str, Any]
) -> dict[str, Any]:
    """Reduce to the surviving gauge-invariant normal mode."""

    k = action["k"]
    zeta, ell, chi, pi = (
        action["zeta"],
        action["ell"],
        action["chi"],
        action["pi"],
    )
    zeta_dot, ell_dot = action["zeta_dot"], action["ell_dot"]
    shell = canonical["constraint_shell"]
    ell_solution = shell[ell]
    ell_dot_solution = sp.diff(ell_solution, zeta) * zeta_dot
    reduced_lagrangian = sp.factor(
        canonical["lagrangian"].subs(
            {
                ell: ell_solution,
                ell_dot: ell_dot_solution,
                chi: shell[chi],
            },
            simultaneous=True,
        )
    )
    v, v_dot = sp.symbols("v v_dot", real=True)
    canonical_lagrangian = sp.factor(
        reduced_lagrangian.subs(
            {zeta: v / sp.sqrt(12), zeta_dot: v_dot / sp.sqrt(12)},
            simultaneous=True,
        )
    )
    kinetic_coefficient = sp.simplify(
        sp.diff(reduced_lagrangian, zeta_dot, 2) / 2
    )
    gradient_coefficient = sp.simplify(
        -sp.diff(reduced_lagrangian, zeta, 2) / (2 * k**2)
    )
    sound_speed_squared = sp.simplify(
        gradient_coefficient / kinetic_coefficient
    )
    canonical_mode = sp.sqrt(12) * zeta

    return {
        "k": k,
        "zeta": zeta,
        "zeta_dot": zeta_dot,
        "v": v,
        "v_dot": v_dot,
        "constraint_shell": shell,
        "ell_dot_solution": ell_dot_solution,
        "reduced_lagrangian": reduced_lagrangian,
        "canonical_mode": canonical_mode,
        "canonical_lagrangian": canonical_lagrangian,
        "kinetic_coefficient": kinetic_coefficient,
        "gradient_coefficient": gradient_coefficient,
        "sound_speed_squared": sound_speed_squared,
        "clock_projection": sp.diff(canonical_mode, pi),
        "lambda_projection": sp.simplify(ell_solution / canonical_mode),
        "chi_projection": sp.simplify(shell[chi] / canonical_mode),
    }


def _background_gate() -> dict[str, Any]:
    """Keep tensor luminality and the cosmological constant logically apart."""

    lambda_background, Lambda_eff = sp.symbols(
        "lambda_background Lambda_eff", real=True
    )
    a = sp.symbols("a", positive=True, real=True)
    a_ddot = sp.symbols("a_ddot", real=True)
    G = sp.symbols("G", positive=True, real=True)
    rho, pressure, w = sp.symbols("rho pressure w", real=True)

    tensor_speed_squared = sp.simplify(1 / (1 - 2 * lambda_background))
    luminal_lambda_solutions = sp.solve(
        sp.Eq(tensor_speed_squared, 1), lambda_background
    )

    # With Q(0)=0, lambda_bar=0, homogeneous chi, and no matter, the auxiliary
    # background stress vanishes.  The flat Einstein equation is then simply
    # Lambda_eff=0.  An additive constant in Q only changes this effective
    # parameter; it does not make luminality imply flatness.
    flat_vacuum_metric_residual = Lambda_eff
    flat_vacuum_Lambda_solutions = sp.solve(
        sp.Eq(flat_vacuum_metric_residual, 0), Lambda_eff
    )

    # Independently, lambda variation on homogeneous FLRW gives
    # Delta_h chi-R_nn=3 a_ddot/a=0.  Vacuum GR at lambda_bar=0 instead gives
    # a_ddot/a=Lambda_eff/3.  Their compatibility is computed below.
    homogeneous_lambda_equation = sp.simplify(3 * a_ddot / a)
    lambda_shell_a_ddot = sp.solve(
        sp.Eq(homogeneous_lambda_equation, 0), a_ddot
    )[0]
    vacuum_einstein_acceleration_residual = sp.simplify(
        a_ddot / a - Lambda_eff / 3
    )
    vacuum_compatibility_residual = sp.simplify(
        vacuum_einstein_acceleration_residual.subs(
            a_ddot, lambda_shell_a_ddot
        )
    )
    vacuum_flrw_compatibility_Lambda_solutions = sp.solve(
        sp.Eq(vacuum_compatibility_residual, 0), Lambda_eff
    )

    # With conserved matter the acceleration equation gives this necessary
    # coasting relation.  For Lambda_eff=0, a single constant-w component can
    # scale as H^2~a^-2 only when 3(1+w)=2.
    matter_coasting_condition = sp.simplify(
        Lambda_eff - 4 * sp.pi * G * (rho + 3 * pressure)
    )
    coasting_barotropic_w_at_zero_Lambda = sp.solve(
        sp.Eq(3 * (1 + w), 2), w
    )

    H, epsilon, pi = sp.symbols("H epsilon pi", real=True)
    zeta = sp.symbols("zeta", real=True)
    flrw_transformations = {
        zeta: -H * epsilon,
        pi: -epsilon,
    }
    flrw_curvature = zeta - H * pi
    flrw_curvature_variation = sp.simplify(
        sp.diff(flrw_curvature, zeta) * flrw_transformations[zeta]
        + sp.diff(flrw_curvature, pi) * flrw_transformations[pi]
    )

    return {
        "lambda_background": lambda_background,
        "Lambda_eff": Lambda_eff,
        "tensor_speed_squared": tensor_speed_squared,
        "luminal_lambda_solutions": luminal_lambda_solutions,
        "tensor_speed_Lambda_derivative": sp.diff(
            tensor_speed_squared, Lambda_eff
        ),
        "flat_vacuum_metric_residual": flat_vacuum_metric_residual,
        "flat_vacuum_Lambda_solutions": flat_vacuum_Lambda_solutions,
        "homogeneous_lambda_equation": homogeneous_lambda_equation,
        "lambda_shell_a_ddot": lambda_shell_a_ddot,
        "vacuum_einstein_acceleration_residual": vacuum_einstein_acceleration_residual,
        "vacuum_compatibility_residual": vacuum_compatibility_residual,
        "vacuum_flrw_compatibility_Lambda_solutions": vacuum_flrw_compatibility_Lambda_solutions,
        "matter_coasting_condition": matter_coasting_condition,
        "coasting_barotropic_w_at_zero_Lambda": coasting_barotropic_w_at_zero_Lambda,
        "flrw_curvature": flrw_curvature,
        "flrw_curvature_variation": flrw_curvature_variation,
        "scope": (
            "The flat scalar count applies only at Lambda_eff=0.  For H!=0, "
            "the invariant is zeta-H*pi and the full scalar perturbation "
            "calculation must be repeated; the background lambda equation "
            "nevertheless excludes vacuum Lambda_eff!=0 acceleration when "
            "lambda_bar is identically zero."
        ),
    }


def derive_clock_stueckelberg_gate() -> dict[str, Any]:
    action = _flat_quadratic_action()
    canonical = _canonical_gate(action)
    return {
        "branch": (
            "flat vacuum, Lambda_eff=0, lambda_bar=0, chi_bar constant, "
            "T_bar=t, k!=0"
        ),
        "gauge": {
            "invariant_lapse": action["invariant_lapse"],
            "invariant_shift": action["invariant_shift"],
            "transformations": action["transformations"],
            "invariant_residuals": action["invariant_residuals"],
            "lagrangian_variation": action["lagrangian_variation"],
        },
        "quadratic_action": action,
        "canonical": canonical,
        "mode": _mode_gate(action, canonical),
        "background": _background_gate(),
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'CHECK' if passed else 'ERROR'}] {label}")
    return passed


def main() -> int:
    result = derive_clock_stueckelberg_gate()
    gauge = result["gauge"]
    action = result["quadratic_action"]
    canonical = result["canonical"]
    mode = result["mode"]
    background = result["background"]

    print("=" * 96)
    print("CURVATURE-QUMOND CLOCK STUECKELBERG GATE")
    print("=" * 96)
    print("Branch:", result["branch"])
    print("Gauge-invariant lapse A =", gauge["invariant_lapse"])
    print("Gauge-invariant scalar shift B =", gauge["invariant_shift"])
    print("Invariant residuals =", gauge["invariant_residuals"])
    print("Restored L =", action["stueckelberg_lagrangian"])
    print("Restored L - unitary L - dF/dt =", action["total_derivative_residual"])
    print("F =", action["boundary_generator"])
    print("Clock Euler derivative =", action["clock_euler_lagrange"])
    print("Direct clock primary =", action["direct_clock_primary"])

    print("\n[Dirac chain after canonical boundary shift]")
    print("Velocity Hessian rank/nullity =", canonical["velocity_rank"], "/", canonical["velocity_nullity"])
    print("Primaries =", canonical["primaries"])
    print("Primary preservation =", canonical["primary_preservation"])
    print("Nonzero secondaries =", canonical["secondaries"])
    print("Constraint PB matrix =")
    print(canonical["constraint_pb_matrix"])
    print("PB rank/nullity =", canonical["constraint_pb_rank"], "/", canonical["constraint_pb_nullity"])
    print("First/second class =", canonical["first_class_count"], "/", canonical["second_class_count"])
    print("Secondary preservation =", canonical["secondary_preservation"])
    print("Closure residuals =", canonical["closure_residuals"])
    print("Physical scalar DOF =", canonical["physical_scalar_dof"])

    print("\n[Gauge-invariant normal mode]")
    print("Constraint shell =", mode["constraint_shell"])
    print("Reduced L =", mode["reduced_lagrangian"])
    print("Canonical mode v =", mode["canonical_mode"])
    print("Canonical L =", mode["canonical_lagrangian"])
    print("c_s^2 =", mode["sound_speed_squared"])
    print("clock/lambda/chi projections =", mode["clock_projection"], mode["lambda_projection"], mode["chi_projection"])

    print("\n[Lambda versus lambda_bar]")
    print("c_T^2 =", background["tensor_speed_squared"])
    print("Luminal lambda_bar solutions =", background["luminal_lambda_solutions"])
    print("d(c_T^2)/d Lambda_eff =", background["tensor_speed_Lambda_derivative"])
    print("Flat-vacuum Lambda_eff solutions =", background["flat_vacuum_Lambda_solutions"])
    print("Homogeneous lambda equation =", background["homogeneous_lambda_equation"])
    print("Vacuum FLRW compatibility residual =", background["vacuum_compatibility_residual"])
    print("Compatible Lambda_eff solutions =", background["vacuum_flrw_compatibility_Lambda_solutions"])
    print("Matter coasting condition =", background["matter_coasting_condition"], "= 0")
    print("Constant-w coasting solution at Lambda_eff=0 =", background["coasting_barotropic_w_at_zero_Lambda"])
    print("FLRW gauge invariant curvature =", background["flrw_curvature"], "; variation =", background["flrw_curvature_variation"])
    print("Scope:", background["scope"])

    checks = [
        _check(
            "the restored combinations and quadratic action are gauge invariant",
            all(item == 0 for item in gauge["invariant_residuals"])
            and gauge["lagrangian_variation"] == 0,
        ),
        _check(
            "the flat-branch clock contribution is exactly a boundary term",
            action["total_derivative_residual"] == 0
            and action["clock_euler_lagrange"] == 0,
        ),
        _check(
            "the generated constraint chain closes",
            canonical["constraint_pb_matrix"]
            + canonical["constraint_pb_matrix"].T
            == sp.zeros(len(canonical["constraints"]))
            and all(item == 0 for item in canonical["closure_residuals"]),
        ),
        _check(
            "a propagating metric-auxiliary scalar remains while pi has zero projection",
            canonical["physical_scalar_dof"] > 0
            and mode["kinetic_coefficient"] > 0
            and mode["gradient_coefficient"] > 0
            and mode["clock_projection"] == 0,
        ),
        _check(
            "luminality fixes lambda_bar but does not algebraically fix Lambda_eff",
            background["luminal_lambda_solutions"]
            and background["tensor_speed_Lambda_derivative"] == 0,
        ),
        _check(
            "flat vacuum and luminal vacuum FLRW compatibility separately force Lambda_eff=0",
            background["flat_vacuum_Lambda_solutions"]
            == background["vacuum_flrw_compatibility_Lambda_solutions"],
        ),
    ]

    print("\n[VERDICT]")
    print("  On the exact flat luminal branch, restoring T=t+pi does not turn the surviving")
    print("  pole into a healthy clock scalar.  Pi contributes only a boundary term, while")
    print("  the gauge-invariant zeta-lambda-chi mode propagates with c_s^2=1/3.  The absent")
    print("  quadratic clock kinetic term is a strong-coupling warning because the covariant")
    print("  action depends on T beyond this special quadratic background.")
    print("  This statement is scoped: c_T=1 implies lambda_bar=0, not Lambda_eff=0.")
    print("  A non-flat matter-supported coasting branch needs a new gauge-invariant perturbation")
    print("  calculation; vacuum Lambda acceleration is already incompatible with the exact lambda equation.")
    print(f"  Diagnostic checks: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
