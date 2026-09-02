#!/usr/bin/env python3
"""Zero-field gate for a universal field-dependent no-slip spin-2 action.

The remaining pole-free route can make the universal Einstein form factor
field dependent.  In the weak static scalar sector a nonlinear function of
the universal Einstein quadratic form can indeed give both the MOND flux and
Phi=Psi.  This script grants that strongest case and tests the tensor sector.

If the same universal coefficient multiplies the Einstein Hessian, exact
MOND fixes it to mu(y).  For mu=1-exp(-y), mu(0)=0: both TT kinetic terms lose
rank on the zero-acceleration branch.  A positive floor restores the tensors
but changes the requested MOND law.  The result is scoped to a *universal*
spin-2 coefficient.  A non-universal covariant projector that modifies only
the static scalar constraint remains a different, unconstructed route.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def _poisson(f: sp.Expr, g: sp.Expr, qs: list[sp.Symbol], ps: list[sp.Symbol]) -> sp.Expr:
    return sp.simplify(sum(sp.diff(f, q) * sp.diff(g, p) - sp.diff(f, p) * sp.diff(g, q) for q, p in zip(qs, ps)))


def derive_zero_field_gate() -> dict[str, Any]:
    """Derive the static branch, TT Hessian rank, and floor obstruction."""

    y, a0 = sp.symbols("y a_0", positive=True)
    mu = 1 - sp.exp(-y)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu_from_primitive = sp.simplify(sp.diff(primitive, y) / (2 * y))
    mu_residual = sp.simplify(mu_from_primitive - mu)
    deep_mond_residual = sp.simplify(sp.limit(mu / y, y, 0) - 1)
    newtonian_limit = sp.limit(mu, y, sp.oo)

    # Strongest static scalar construction.  q is the reduced universal
    # Einstein quadratic form; q=y^2 when Phi=Psi.  Varying the same primitive
    # produces the MOND flux in the Phi equation and the no-slip equation in
    # the Psi variation.
    p_phi, p_psi = sp.symbols("p_Phi p_Psi", positive=True)
    q = (2 * p_phi * p_psi - p_psi**2) / a0**2
    root_q = sp.sqrt(q)
    Gq = root_q**2 + 2 * (1 + root_q) * sp.exp(-root_q) - 2
    static_lagrangian = sp.simplify(a0**2 * Gq)
    flux_phi = sp.diff(static_lagrangian, p_phi)
    flux_psi = sp.diff(static_lagrangian, p_psi)
    no_slip_substitution = {p_phi: a0 * y, p_psi: a0 * y}
    flux_phi_on_branch = sp.simplify(flux_phi.subs(no_slip_substitution))
    flux_psi_on_branch = sp.simplify(flux_psi.subs(no_slip_substitution))
    expected_flux = 2 * a0 * y * mu

    # General covariant metric propagator, not yet assuming universality.
    # For a conserved source its gauge-independent part is
    #   P^(2)/a - P^(0-s)/(2c).
    # Build the Barnes--Rivers projectors and contract them with static dust.
    spin2_factor, scalar_factor = sp.symbols("a c", nonzero=True)
    rho = sp.symbols("rho", positive=True)
    eta = sp.diag(-1, 1, 1, 1)
    theta = sp.diag(-1, 1, 1, 0)  # static momentum along z

    def p2(mu_i: int, nu_i: int, rho_i: int, sigma_i: int) -> sp.Expr:
        return sp.Rational(1, 2) * (
            theta[mu_i, rho_i] * theta[nu_i, sigma_i]
            + theta[mu_i, sigma_i] * theta[nu_i, rho_i]
        ) - sp.Rational(1, 3) * theta[mu_i, nu_i] * theta[rho_i, sigma_i]

    def p0(mu_i: int, nu_i: int, rho_i: int, sigma_i: int) -> sp.Expr:
        return sp.Rational(1, 3) * theta[mu_i, nu_i] * theta[rho_i, sigma_i]

    # Mixed-index 16x16 forms verify idempotence and orthogonality rather
    # than taking the projector algebra as an input.
    p2_mixed = sp.zeros(16, 16)
    p0_mixed = sp.zeros(16, 16)
    for mu_i in range(4):
        for nu_i in range(4):
            row = 4 * mu_i + nu_i
            for rho_i in range(4):
                for sigma_i in range(4):
                    col = 4 * rho_i + sigma_i
                    p2_mixed[row, col] = sum(
                        p2(mu_i, nu_i, alpha, beta)
                        * eta[alpha, rho_i]
                        * eta[beta, sigma_i]
                        for alpha in range(4)
                        for beta in range(4)
                    )
                    p0_mixed[row, col] = sum(
                        p0(mu_i, nu_i, alpha, beta)
                        * eta[alpha, rho_i]
                        * eta[beta, sigma_i]
                        for alpha in range(4)
                        for beta in range(4)
                    )
    projector_idempotence_residual = sp.simplify(
        sum((p2_mixed * p2_mixed - p2_mixed)[i, j] ** 2 for i in range(16) for j in range(16))
        + sum((p0_mixed * p0_mixed - p0_mixed)[i, j] ** 2 for i in range(16) for j in range(16))
    )
    projector_orthogonality_residual = sp.simplify(
        sum((p2_mixed * p0_mixed)[i, j] ** 2 for i in range(16) for j in range(16))
        + sum((p0_mixed * p2_mixed)[i, j] ** 2 for i in range(16) for j in range(16))
    )
    dust = sp.zeros(4, 4)
    dust[0, 0] = rho  # T^{00}=rho
    h_response = sp.zeros(4, 4)
    for mu_i in range(4):
        for nu_i in range(4):
            h_response[mu_i, nu_i] = sp.simplify(
                sum(
                    (p2(mu_i, nu_i, rr, ss) / spin2_factor
                     - p0(mu_i, nu_i, rr, ss) / (2 * scalar_factor))
                    * dust[rr, ss]
                    for rr in range(4)
                    for ss in range(4)
                )
            )
    gamma_general = sp.factor(h_response[1, 1] / h_response[0, 0])
    gamma_minus_one = sp.factor(gamma_general - 1)
    gamma_minus_one_numerator = sp.factor(sp.together(gamma_minus_one).as_numer_denom()[0])
    no_slip_solution = sp.solve(sp.Eq(gamma_general, 1), scalar_factor)
    h00_no_slip = sp.simplify(h_response[0, 0].subs(scalar_factor, spin2_factor))
    h00_gr = sp.simplify(h_response[0, 0].subs({spin2_factor: 1, scalar_factor: 1}))
    common_response_ratio = sp.simplify(h00_no_slip / h00_gr)

    # Two TT polarizations.  Universality means the same A(y)=mu(y)
    # multiplies their Einstein kinetic and gradient terms.
    hp, hx, hp_dot, hx_dot, k = sp.symbols(
        "h_plus h_cross h_plus_dot h_cross_dot k", real=True
    )
    A = mu_from_primitive
    tensor_lagrangian = sp.Rational(1, 2) * A * (
        hp_dot**2 + hx_dot**2 - k**2 * (hp**2 + hx**2)
    )
    tensor_hessian = sp.hessian(tensor_lagrangian, (hp_dot, hx_dot))
    generic_determinant = sp.factor(tensor_hessian.det())
    positive_mu_form = 2 * sp.exp(-y / 2) * sp.sinh(y / 2)
    generic_determinant_positive = bool(
        sp.simplify(A - positive_mu_form.rewrite(sp.exp)) == 0
        and positive_mu_form.is_positive is True
    )
    generic_rank = tensor_hessian.rank()
    tensor_speed_squared = sp.simplify(A / A)

    # Exact y=0 branch.  Take the one-sided limit because y is a norm.
    zero_hessian = tensor_hessian.applyfunc(lambda item: sp.limit(item, y, 0, dir="+"))
    zero_rank = zero_hessian.rank()
    p_plus, p_cross = sp.symbols("p_plus p_cross", real=True)
    primary_constraints = [p_plus, p_cross] if zero_rank == 0 else []
    q_plus, q_cross = sp.symbols("q_plus q_cross", real=True)
    qs = [q_plus, q_cross]
    ps = [p_plus, p_cross]
    poisson_matrix = sp.Matrix(
        [[_poisson(ci, cj, qs, ps) for cj in primary_constraints] for ci in primary_constraints]
    )
    u_plus, u_cross = sp.symbols("u_plus u_cross", real=True)
    total_hamiltonian_zero_branch = u_plus * p_plus + u_cross * p_cross
    preservation = [
        _poisson(constraint, total_hamiltonian_zero_branch, qs, ps)
        for constraint in primary_constraints
    ]
    secondary_constraints: list[sp.Expr] = [] if all(item == 0 for item in preservation) else preservation
    first_class_count = len(primary_constraints) - poisson_matrix.rank()
    second_class_count = poisson_matrix.rank()
    quadratic_tensor_dof = (
        2 * len(qs) - 2 * first_class_count - second_class_count
    ) // 2

    mode_sectors = {
        "k=0": {
            "hessian": zero_hessian.subs(k, 0),
            "rank": zero_hessian.subs(k, 0).rank(),
        },
        "k!=0": {
            "hessian": zero_hessian,
            "rank": zero_hessian.rank(),
        },
    }

    inverse_kinetic_limit = sp.limit(1 / A, y, 0, dir="+")
    amplitude = sp.symbols("epsilon", positive=True)
    h_amp = sp.symbols("h_amp", real=True)
    mu_small = sp.series(mu.subs(y, amplitude), amplitude, 0, 3).removeO()
    interaction_order_probe = sp.expand(mu_small * h_amp**2)
    monomials = sp.Poly(interaction_order_probe, amplitude, h_amp).monoms()
    minimum_total_degree = min(sum(monomial) for monomial in monomials)
    quadratic_action_starts_above_second_order = minimum_total_degree > 2

    # The obvious regularization A -> epsilon+mu restores a nonzero Hessian,
    # but the same coefficient occurs in the static flux, so it is no longer
    # the requested exact law.  At sufficiently small y the floor dominates.
    floor = sp.symbols("epsilon_floor", positive=True)
    A_floor = floor + mu
    floor_hessian = sp.diag(A_floor, A_floor)
    floor_hessian_zero = floor_hessian.applyfunc(
        lambda item: sp.limit(item, y, 0, dir="+")
    )
    floor_mu_residual = sp.simplify(A_floor - mu)
    deep_mond_flux_ratio_limit = sp.limit(floor / mu, y, 0, dir="+")
    exact_target_preserved = bool(floor_mu_residual == 0)

    return {
        "kernel": {
            "primitive": primitive,
            "mu": mu,
            "mu_from_primitive": mu_from_primitive,
            "mu_residual": mu_residual,
            "deep_mond_residual": deep_mond_residual,
            "newtonian_limit": newtonian_limit,
        },
        "static_branch": {
            "q": q,
            "lagrangian": static_lagrangian,
            "phi_flux": flux_phi,
            "psi_flux": flux_psi,
            "phi_flux_on_no_slip_branch": flux_phi_on_branch,
            "psi_flux_on_no_slip_branch": flux_psi_on_branch,
            "expected_mond_flux": expected_flux,
            "mond_flux_residual": sp.simplify(flux_phi_on_branch - expected_flux),
            "no_slip_residual": flux_psi_on_branch,
        },
        "projector": {
            "spin2_form_factor": spin2_factor,
            "scalar_form_factor": scalar_factor,
            "theta": theta,
            "p2_mixed": p2_mixed,
            "p0_mixed": p0_mixed,
            "projector_idempotence_residual": projector_idempotence_residual,
            "projector_orthogonality_residual": projector_orthogonality_residual,
            "dust_response": h_response,
            "gamma": gamma_general,
            "gamma_minus_one": gamma_minus_one,
            "gamma_minus_one_numerator": gamma_minus_one_numerator,
            "no_slip_solution": no_slip_solution,
            "common_response_ratio": common_response_ratio,
        },
        "tensor": {
            "universal_coefficient": A,
            "lagrangian": tensor_lagrangian,
            "hessian": tensor_hessian,
            "generic_determinant": generic_determinant,
            "generic_determinant_positive": generic_determinant_positive,
            "generic_rank": generic_rank,
            "tensor_speed_squared": tensor_speed_squared,
        },
        "zero_field": {
            "hessian": zero_hessian,
            "hessian_rank": zero_rank,
            "primary_constraints": primary_constraints,
            "preservation": preservation,
            "secondary_constraints": secondary_constraints,
            "poisson_bracket_matrix": poisson_matrix,
            "first_class_count": first_class_count,
            "second_class_count": second_class_count,
            "quadratic_tensor_dof": quadratic_tensor_dof,
            "mode_sectors": mode_sectors,
        },
        "strong_coupling": {
            "inverse_kinetic_limit": inverse_kinetic_limit,
            "mu_small": mu_small,
            "interaction_order_probe": interaction_order_probe,
            "minimum_total_degree": minimum_total_degree,
            "quadratic_action_starts_above_second_order": quadratic_action_starts_above_second_order,
        },
        "floor_repair": {
            "coefficient": A_floor,
            "tensor_hessian_at_zero": floor_hessian_zero,
            "tensor_hessian_rank_at_zero": floor_hessian_zero.rank(),
            "mond_residual": floor_mu_residual,
            "deep_mond_flux_ratio_limit": deep_mond_flux_ratio_limit,
            "exact_target_preserved": exact_target_preserved,
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_zero_field_gate()
    kernel = result["kernel"]
    static = result["static_branch"]
    projector = result["projector"]
    tensor = result["tensor"]
    zero = result["zero_field"]
    strong = result["strong_coupling"]
    floor = result["floor_repair"]

    print("=" * 96)
    print("FIELD-DEPENDENT UNIVERSAL SPIN-2 ZERO-FIELD GATE")
    print("=" * 96)
    print("\n[1] Exact static construction granted")
    print("  G(y) =", kernel["primitive"])
    print("  G'(y)/(2y) =", kernel["mu_from_primitive"])
    print("  q =", static["q"])
    print("  delta_Phi flux on Phi=Psi =", static["phi_flux_on_no_slip_branch"])
    print("  expected MOND flux =", static["expected_mond_flux"])
    print("  delta_Psi flux on Phi=Psi =", static["psi_flux_on_no_slip_branch"])
    checks = [
        _check("the primitive gives exactly mu=1-exp(-y)", kernel["mu_residual"] == 0),
        _check("the strongest universal static branch derives both the exact MOND flux and no slip", static["mond_flux_residual"] == 0 and static["no_slip_residual"] == 0),
    ]

    print("\n[2] General covariant spin projectors: no slip forces universality")
    print("  theta_mn =", projector["theta"])
    print("  projector idempotence residual =", projector["projector_idempotence_residual"])
    print("  projector orthogonality residual =", projector["projector_orthogonality_residual"])
    print("  dust response h_mn =", projector["dust_response"])
    print("  gamma = h_11/h_00 =", projector["gamma"])
    print("  gamma-1 =", projector["gamma_minus_one"])
    print("  gamma=1 solution for c =", projector["no_slip_solution"])
    print("  common response / GR response at c=a =", projector["common_response_ratio"])
    checks.append(_check("for a general Lorentz-covariant metric propagator, gamma=1 forces c=a and the common enhancement is 1/a", projector["projector_idempotence_residual"] == 0 and projector["projector_orthogonality_residual"] == 0 and projector["no_slip_solution"] == [projector["spin2_form_factor"]] and projector["common_response_ratio"] == 1 / projector["spin2_form_factor"]))

    print("\n[3] No-slip tensor principal block")
    print("  A(y) =", tensor["universal_coefficient"])
    print("  L_T =", tensor["lagrangian"])
    print("  W_T =", tensor["hessian"])
    print("  det/rank for y>0 =", tensor["generic_determinant"], "/", tensor["generic_rank"])
    print("  c_T^2 =", tensor["tensor_speed_squared"])
    checks.append(_check("at every y>0 the two tensors are luminal and have a positive rank-2 Hessian", tensor["generic_determinant_positive"] and tensor["generic_rank"] == 2 and tensor["tensor_speed_squared"] == 1))

    print("\n[4] Exact zero-field Dirac chain")
    print("  W_T(0+) =", zero["hessian"], "; rank =", zero["hessian_rank"])
    print("  primaries =", zero["primary_constraints"])
    print("  preservation =", zero["preservation"], "; secondaries =", zero["secondary_constraints"])
    print("  PB matrix =", zero["poisson_bracket_matrix"])
    print("  first/second class =", zero["first_class_count"], "/", zero["second_class_count"])
    print("  quadratic tensor DOF =", zero["quadratic_tensor_dof"])
    print("  k sectors =", zero["mode_sectors"])
    checks.append(_check("mu(0)=0 removes both tensor kinetic terms in k=0 and k!=0, so the linear two-tensor theory is lost", zero["hessian_rank"] == 0 and zero["quadratic_tensor_dof"] == 0 and all(sector["rank"] == 0 for sector in zero["mode_sectors"].values())))

    print("\n[5] Strong-coupling diagnostic")
    print("  lim_y->0 1/A(y) =", strong["inverse_kinetic_limit"])
    print("  A(epsilon) =", strong["mu_small"])
    print("  amplitude probe A(epsilon) h^2 =", strong["interaction_order_probe"])
    print("  lowest total field order =", strong["minimum_total_degree"])
    checks.append(_check("the inverse kinetic normalization diverges and the leading tensor term is above quadratic order", strong["inverse_kinetic_limit"].is_infinite and strong["quadratic_action_starts_above_second_order"]))

    print("\n[6] Positive-floor repair")
    print("  A_floor =", floor["coefficient"])
    print("  W_floor(0) =", floor["tensor_hessian_at_zero"], "; rank =", floor["tensor_hessian_rank_at_zero"])
    print("  MOND-law residual =", floor["mond_residual"])
    print("  floor/MOND flux ratio as y->0 =", floor["deep_mond_flux_ratio_limit"])
    checks.append(_check("a positive tensor floor restores rank but destroys the exact MOND/deep-MOND law", floor["tensor_hessian_rank_at_zero"] == 2 and floor["mond_residual"] != 0 and floor["deep_mond_flux_ratio_limit"].is_infinite and not floor["exact_target_preserved"]))

    print("\n[VERDICT]")
    print("  SCOPED NO-GO: a universal field-dependent Einstein form factor can derive exact MOND")
    print("  and no slip in the static branch, but exact mu(0)=0 simultaneously zeros the TT")
    print("  Hessian.  A positive floor saves the gravitons only by changing the requested law.")
    print("  Residual: a non-universal covariant tensor projector that leaves TT untouched while")
    print("  modifying only the static scalar constraint.  No such metric-only action is supplied.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
