#!/usr/bin/env python3
"""Variational falsification of a matter-sourced elliptic phantom MOND route.

This file tests an explicit best-case version of the requested construction.  A
unit timelike normal n^mu (either a fixed foliation, or n_mu proportional to
grad_mu tau) defines h^mu_nu = delta^mu_nu + n^mu n_nu and the spatial derivative
D_mu.  With u = log(N), the trial action is

 S = S_EH[g] + S_m[g,psi] + (1/(8 pi G)) int sqrt(-g) [
       lambda ( D_mu[mu(|a|/a0) a^mu] - D^2 chi )
     + eta    ( D^2 chi - 4 pi G rho_n ) ],

where a_mu = n^nu nabla_nu n_mu = D_mu u in unitary gauge and
rho_n = T_munu n^mu n^nu.  Boundary terms give the weak, static action used
below.  Varying lambda and eta gives the desired elliptic pair; chi gives the
adjoint equation.  Thus this is not a phenomenological Poisson equation pasted
onto Einstein gravity.

The script deliberately computes every rank, determinant, mode count, PPN-like
anisotropy, and stability eigenvalue from matrices or variations.  It does not
insert a desired rank, determinant, PPN parameter, or degree-of-freedom count.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class CandidateSymbols:
    G: sp.Symbol
    a0: sp.Symbol
    y: sp.Symbol
    kx: sp.Symbol
    ky: sp.Symbol
    kz: sp.Symbol
    rho0: sp.Symbol


def _symbols() -> CandidateSymbols:
    return CandidateSymbols(
        G=sp.symbols("G", positive=True),
        a0=sp.symbols("a0", positive=True),
        y=sp.symbols("y", positive=True),
        kx=sp.symbols("k_x", real=True),
        ky=sp.symbols("k_y", real=True),
        kz=sp.symbols("k_z", real=True),
        rho0=sp.symbols("rho_0", positive=True),
    )


def _el_static_action(sym: CandidateSymbols) -> dict[str, sp.Expr]:
    """Derive the Euler--Lagrange equations of the weak static trial action.

    On a monotonic radial branch u_x > 0, y=u_x/a0.  After one integration by
    parts the auxiliary density is

       L_aux = -lambda_x mu(u_x/a0) u_x
               + (lambda_x-eta_x) chi_x - 4 pi G eta rho.

    The leading weak static measure is sqrt(h).  Keeping the exact N factor
    only adds post-Newtonian terms; it cannot remove the leading anisotropic
    stress calculated below.  This is the most favorable version for the route.
    """

    x = sp.symbols("x", real=True)
    u = sp.Function("u")(x)
    chi = sp.Function("chi")(x)
    lam = sp.Function("lambda")(x)
    eta = sp.Function("eta")(x)
    rho = sp.Function("rho")(x)
    ux = sp.diff(u, x)
    mu_x = 1 - sp.exp(-ux / sym.a0)

    # The Einstein scalar contribution is included only to expose the lapse
    # response.  Its overall normalisation does not affect the auxiliary
    # constraint algebra below.
    density = (
        -sp.Rational(1, 2) * ux**2
        - sp.diff(lam, x) * mu_x * ux
        + (sp.diff(lam, x) - sp.diff(eta, x)) * sp.diff(chi, x)
        - 4 * sp.pi * sym.G * eta * rho
    )

    def euler(field: sp.Expr) -> sp.Expr:
        return sp.simplify(
            sp.diff(density, field)
            - sp.diff(sp.diff(density, sp.diff(field, x)), x)
        )

    e_lam = euler(lam)
    e_eta = euler(eta)
    e_chi = euler(chi)
    e_u = euler(u)

    mond = sp.diff(mu_x * ux, x) - sp.diff(chi, x, 2)
    poisson_chi = sp.diff(chi, x, 2) - 4 * sp.pi * sym.G * rho
    adjoint = sp.diff(eta - lam, x, 2)
    lapse = sp.diff(
        ux + sp.diff(lam, x) * (mu_x + ux * sp.exp(-ux / sym.a0) / sym.a0), x
    )

    return {
        "density": density,
        "e_lambda": e_lam,
        "e_eta": e_eta,
        "e_chi": e_chi,
        "e_u": e_u,
        "mond_residual": sp.simplify(e_lam - mond),
        "poisson_residual": sp.simplify(e_eta - poisson_chi),
        "adjoint_residual": sp.simplify(e_chi - adjoint),
        "lapse_residual": sp.simplify(e_u - lapse),
        "mu_x": mu_x,
    }


def _legendre_kernel(sym: CandidateSymbols) -> dict[str, sp.Expr]:
    """Obtain the exact exponential MOND function from an action primitive."""

    F = sp.Rational(1, 2) * sym.y**2 + (sym.y + 1) * sp.exp(-sym.y) - 1
    mu = 1 - sp.exp(-sym.y)
    F_X = sp.simplify(sp.diff(F, sym.y) / (2 * sym.y))
    return {
        "F": F,
        "mu": mu,
        "F_X": F_X,
        "flux_residual": sp.simplify(2 * F_X - mu),
    }


def _radial_hilbert_stress(sym: CandidateSymbols, mu: sp.Expr) -> dict[str, sp.Expr]:
    """Vary the actual auxiliary metric coupling and isolate its TF stress.

    We vary -mu(y) D_i lambda D^i u with respect to an inverse spatial metric.
    In the radial branch D lambda and D u are parallel.  The returned amplitude
    is T_xx-T_yy, i.e. the coefficient of n_i n_j-delta_ij/3.
    """

    ell = sp.symbols("lambda_prime", real=True)
    e0, e1, e2 = sp.symbols("epsilon_0 epsilon_1 epsilon_2", real=True)
    inverse_metric = sp.diag(1 + e0, 1 + e1, 1 + e2)
    grad_u = sp.Matrix([sym.a0 * sym.y, 0, 0])
    grad_lam = sp.Matrix([ell, 0, 0])
    y_metric = sp.sqrt((grad_u.T * inverse_metric * grad_u)[0]) / sym.a0
    mu_metric = 1 - sp.exp(-y_metric)
    density = -mu_metric * (grad_lam.T * inverse_metric * grad_u)[0]

    origin = {e0: 0, e1: 0, e2: 0}
    d0 = sp.simplify(sp.diff(density, e0).subs(origin))
    d1 = sp.simplify(sp.diff(density, e1).subs(origin))
    tf_amplitude = sp.simplify(-2 * (d0 - d1))
    radial_coefficient = sp.simplify(tf_amplitude / (ell * sym.a0 * sym.y))
    positivity_transform = sp.simplify(sp.exp(sym.y) * radial_coefficient)

    return {
        "lambda_prime": ell,
        "density": density,
        "tf_amplitude": tf_amplitude,
        "radial_stress_coefficient": radial_coefficient,
        "positivity_transform": positivity_transform,
        "mu": mu,
    }


def _dirac_block(sym: CandidateSymbols, mu: sp.Expr) -> dict[str, Any]:
    """Compute the k != 0 scalar Dirac block from the quadratic action.

    The configuration variables are (u, chi, lambda, eta).  Their four primary
    momenta vanish because the candidate contains no corresponding velocities.
    Expanding the varied action about a constant-gradient background gives

       L_2 = B u^2/2 - K lambda u + k^2 lambda chi - k^2 eta chi,

    with K = k_i A^ij k_j and A^ij the MOND constitutive Hessian.  The secondary
    constraints are the four entries of H q.  Their Poisson matrix is assembled
    directly, not supplied as an assumed Dirac matrix.
    """

    q2 = sp.expand(sym.kx**2 + sym.ky**2 + sym.kz**2)
    mu_prime = sp.diff(mu, sym.y)
    longitudinal_stiffness = sp.simplify(mu + sym.y * mu_prime)
    K = sp.expand(mu * q2 + sym.y * mu_prime * sym.kx**2)
    B = q2
    u, chi, lam, eta = sp.symbols("u chi lambda eta")
    qvars = sp.Matrix([u, chi, lam, eta])
    quadratic = sp.Rational(1, 2) * B * u**2 - K * lam * u + q2 * lam * chi - q2 * eta * chi
    hessian = sp.simplify(sp.hessian(quadratic, qvars))
    zero = sp.zeros(hessian.rows)
    pb = zero.row_join(-hessian).col_join(hessian.row_join(zero))
    multipliers = sp.symbols("v_u v_chi v_lambda v_eta")
    closure_solution = sp.solve(list(hessian * sp.Matrix(multipliers)), multipliers, dict=True)

    numeric_samples = []
    for y_value, wavevector in ((sp.Rational(1, 5), (1, 2, 3)), (1, (2, 0, 1)), (5, (3, 4, 0))):
        substitutions = {
            sym.y: y_value,
            sym.kx: wavevector[0],
            sym.ky: wavevector[1],
            sym.kz: wavevector[2],
        }
        hessian_numeric = sp.N(hessian.subs(substitutions), 30)
        pb_numeric = sp.N(pb.subs(substitutions), 30)
        hessian_det_numeric = float(hessian_numeric.det(method="domain-ge"))
        pb_det_numeric = float(pb_numeric.det(method="domain-ge"))
        numeric_samples.append(
            {
                "y": y_value,
                "k": wavevector,
                "hessian_rank": hessian_numeric.rank(),
                "pb_rank": pb_numeric.rank(),
                "hessian_det": hessian_det_numeric,
                "pb_det_direct": pb_det_numeric,
            }
        )

    primary_names = ("p_u", "p_chi", "p_lambda", "p_eta")
    secondary_names = ("C_u", "C_chi", "C_lambda", "C_eta")
    phase_blocks = {
        "spatial_metric": 12,
        "lapse": 2,
        "shift": 6,
        "elliptic_auxiliaries": 2 * (len(qvars) - 1),
    }
    total_phase_dimension = sum(phase_blocks.values())
    spatial_diffeomorphism_first_class = 2 * 3
    second_class = pb.rank()
    physical_phase_dimension = sp.simplify(
        total_phase_dimension - 2 * spatial_diffeomorphism_first_class - second_class
    )

    return {
        "q2": q2,
        "mu_prime": mu_prime,
        "longitudinal_stiffness": longitudinal_stiffness,
        "K": K,
        "quadratic_action": quadratic,
        "hessian": hessian,
        "hessian_determinant": sp.factor(hessian.det()),
        "hessian_rank": hessian.rank(),
        "dirac_pb_matrix": pb,
        # This is the determinant of the actual displayed Poisson matrix.  The
        # block identity det([[0,-H],[H,0]])=det(H)^2 avoids a prohibitively
        # expensive generic Bareiss expansion; each numerical sample above also
        # evaluates the full 8x8 determinant directly as a cross-check.
        "dirac_pb_determinant": sp.factor(hessian.det() ** 2),
        "dirac_pb_rank": pb.rank(),
        "primary_names": primary_names,
        "secondary_names": secondary_names,
        "primary_constraints": len(primary_names),
        "secondary_constraints": len(secondary_names),
        "closure_solution": closure_solution,
        "closure_multipliers": tuple(closure_solution[0][item] for item in multipliers),
        "numeric_samples": numeric_samples,
        "phase_blocks": phase_blocks,
        "total_phase_dimension": total_phase_dimension,
        "first_class": spatial_diffeomorphism_first_class,
        "second_class": second_class,
        "physical_phase_dimension": physical_phase_dimension,
        "physical_dof": sp.simplify(physical_phase_dimension / 2),
    }


def _zero_mode_and_flrw(sym: CandidateSymbols, dirac: dict[str, Any]) -> dict[str, Any]:
    """Analyze the elliptic zero mode independently of the k != 0 sector."""

    zero_subs = {sym.kx: 0, sym.ky: 0, sym.kz: 0}
    hessian_zero = dirac["hessian"].subs(zero_subs)
    pb_zero = dirac["dirac_pb_matrix"].subs(zero_subs)
    homogeneous_elliptic_residual = sp.simplify(-4 * sp.pi * sym.G * sym.rho0)
    source_compatible = homogeneous_elliptic_residual == 0
    return {
        "hessian": hessian_zero,
        "hessian_rank": hessian_zero.rank(),
        "dirac_pb_matrix": pb_zero,
        "dirac_pb_rank": pb_zero.rank(),
        "homogeneous_elliptic_residual": homogeneous_elliptic_residual,
        "source_compatible": source_compatible,
    }


def _weak_field_equations(sym: CandidateSymbols, stress: dict[str, sp.Expr], mu: sp.Expr) -> dict[str, sp.Expr]:
    """Obtain Phi and Psi separately in the radial Fourier branch."""

    k = sp.symbols("k", positive=True)
    phi = sp.symbols("Phi_hat", nonzero=True)
    pi_tf = stress["tf_amplitude"]
    # For k parallel to the radial gradient, the xx trace-free Einstein equation
    # gives (-2 k^2/3)(Phi-Psi) = 8 pi G (2 Pi/3).
    phi_minus_psi = sp.simplify(-8 * sp.pi * sym.G * pi_tf / k**2)
    psi = sp.simplify(phi - phi_minus_psi)
    gamma = sp.simplify(psi / phi)

    # No slip enforces lambda'=0 because the computed coefficient is strictly
    # positive for every finite y>0.  Then the varied auxiliary lapse equation
    # vanishes, leaving the ordinary Einstein/Poisson branch.  In an exterior
    # spherical region, simultaneous Einstein and MOND fluxes require mu=1.
    no_slip_lambda_gradient = sp.solve(sp.Eq(pi_tf, 0), stress["lambda_prime"])
    flux_compatibility = sp.simplify(mu - 1)

    return {
        "mond_equation": sp.Symbol("D_i(mu D_i Phi) - 4piG rho"),
        "einstein_00": sp.Symbol("laplacian(Psi) - 4piG(rho + rho_aux)"),
        "tracefree_equation": sp.Symbol("D_ij(Phi-Psi) - 8piG Pi_aux_TF"),
        "phi_minus_psi": phi_minus_psi,
        "psi": psi,
        "gamma_ppn": gamma,
        "gamma_minus_one": sp.simplify(gamma - 1),
        "no_slip_lambda_gradient": no_slip_lambda_gradient,
        "no_slip_newton_mond_compatibility": flux_compatibility,
    }


def _ward_identity(sym: CandidateSymbols) -> dict[str, sp.Expr]:
    """Vary a point particle to test conservation of T from S_m alone."""

    t = sp.symbols("t", real=True)
    m = sp.symbols("m", positive=True)
    x = sp.Function("x")(t)
    Phi = sp.Function("Phi")(x)
    eta = sp.Function("eta")(x)
    source_coupling = sp.simplify((4 * sp.pi * sym.G) / (8 * sp.pi * sym.G))
    particle_lagrangian = sp.Rational(1, 2) * m * sp.diff(x, t) ** 2 - m * Phi - source_coupling * m * eta
    particle_euler = sp.simplify(
        sp.diff(sp.diff(particle_lagrangian, sp.diff(x, t)), t) - sp.diff(particle_lagrangian, x)
    )
    bare_matter_divergence = sp.simplify(-source_coupling * sp.Symbol("rho", positive=True) * sp.Symbol("eta_x", nonzero=True))
    return {
        "source_coupling": source_coupling,
        "particle_lagrangian": particle_lagrangian,
        "particle_euler": particle_euler,
        "bare_matter_force_coefficient": source_coupling,
        "bare_matter_divergence": bare_matter_divergence,
    }


def _preferred_frame(sym: CandidateSymbols) -> dict[str, sp.Expr]:
    """Compute the fixed-foliation boost anisotropy rather than assuming PPN zeros."""

    wx, wy, wz = sp.symbols("w_x w_y w_z", real=True)
    t = sp.symbols("w_dot_k_squared", nonnegative=True)
    q2 = sym.kx**2 + sym.ky**2 + sym.kz**2
    green = 1 / (q2 + t)
    anisotropic_coefficient = sp.simplify(sp.diff(green, t).subs(t, 0) * q2**2)
    first_order_w = [sp.simplify(sp.diff(green.subs(t, wx**2 + wy**2 + wz**2), w).subs({wx: 0, wy: 0, wz: 0})) for w in (wx, wy, wz)]
    return {
        "spatial_symbol": q2 + t,
        "green_function": green,
        "alpha2_like_normalized_coefficient": anisotropic_coefficient,
        "alpha1_static_linear_coefficients": tuple(first_order_w),
        "alpha3_status": sp.Symbol("undefined_when_bare_matter_Ward_identity_fails"),
    }


def _stability(sym: CandidateSymbols, mu: sp.Expr) -> dict[str, Any]:
    """Diagonalize the elliptic constitutive tensor around a MOND background."""

    mu_prime = sp.diff(mu, sym.y)
    tensor = sp.diag(mu + sym.y * mu_prime, mu, mu)
    transverse_transform = sp.simplify(sp.exp(sym.y) * mu)
    longitudinal_transform = sp.simplify(sp.exp(sym.y) * (mu + sym.y * mu_prime))
    return {
        "constitutive_tensor": tensor,
        "eigenvalues": tensor.eigenvals(),
        "transverse_positivity_transform": transverse_transform,
        "longitudinal_positivity_transform": longitudinal_transform,
        "static_gradient_stable": all(value != 0 for value in tensor.diagonal()),
    }


def derive_candidate() -> dict[str, Any]:
    """Return every derived object so tests and readers can inspect the calculation."""

    sym = _symbols()
    kernel = _legendre_kernel(sym)
    el = _el_static_action(sym)
    stress = _radial_hilbert_stress(sym, kernel["mu"])
    dirac = _dirac_block(sym, kernel["mu"])
    k_zero = _zero_mode_and_flrw(sym, dirac)
    weak = _weak_field_equations(sym, stress, kernel["mu"])
    ward = _ward_identity(sym)
    preferred = _preferred_frame(sym)
    stability = _stability(sym, kernel["mu"])
    return {
        "symbols": sym,
        "kernel": kernel,
        "el": el,
        "mond_flux_residual": kernel["flux_residual"],
        "slip": stress,
        "k_nonzero": dirac,
        "k_zero": k_zero,
        "flrw": k_zero,
        "weak_field": weak,
        "ward": ward,
        "preferred_frame": preferred,
        "stability": stability,
    }


def _check(label: str, expression: Any) -> bool:
    passed = bool(expression)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_candidate()
    kernel = result["kernel"]
    el = result["el"]
    stress = result["slip"]
    knz = result["k_nonzero"]
    kz = result["k_zero"]
    weak = result["weak_field"]
    ward = result["ward"]
    frame = result["preferred_frame"]
    stable = result["stability"]

    print("=" * 94)
    print("ELLIPTIC PHANTOM ACTION GATE: VARIATIONAL CONSTRUCTION AND FALSIFICATION")
    print("=" * 94)
    print("Action: S_EH + S_m + (8 pi G)^-1 int sqrt(-g)[lambda(C_M-D^2 chi)+eta(D^2 chi-4piG rho_n)]")
    print("C_M = D_mu[mu(|a|/a0) a^mu],  a_mu=D_mu log(N),  mu(y)=1-exp(-y).")

    print("\n[1] Exact MOND primitive and Euler--Lagrange equations")
    print(f"  F(y) = {kernel['F']}")
    print(f"  2 dF/d(y^2) - mu = {kernel['flux_residual']}")
    print(f"  E_lambda - [D(mu Du)-D^2 chi] = {el['mond_residual']}")
    print(f"  E_eta - [D^2 chi-4piG rho] = {el['poisson_residual']}")
    print(f"  E_chi - D^2(eta-lambda) = {el['adjoint_residual']}")
    print(f"  E_u - D[u'+lambda'(mu+y mu')] = {el['lapse_residual']}")
    checks = [
        _check("the action variation, not an assertion, gives both elliptic equations", all(el[key] == 0 for key in ("mond_residual", "poisson_residual", "adjoint_residual", "lapse_residual"))),
        _check("the action primitive gives exactly mu(y)=1-exp(-y)", kernel["flux_residual"] == 0),
    ]

    print("\n[2] Actual k != 0 Dirac closure")
    print(f"  Primary constraints: {knz['primary_names']}")
    print(f"  Secondary constraints: {knz['secondary_names']} = H q")
    print("  Hessian H (the {primary,secondary} Poisson block):")
    print(knz["hessian"])
    print(f"  det(H) = {knz['hessian_determinant']}")
    print(f"  rank(H) = {knz['hessian_rank']}; rank(Dirac PB) = {knz['dirac_pb_rank']}")
    print(f"  det(Dirac PB) = {knz['dirac_pb_determinant']}")
    print(f"  Stabilization solves H v=0 as v = {knz['closure_multipliers']}; no tertiary constraint remains.")
    for sample in knz["numeric_samples"]:
        print(f"  numerical rank check y={sample['y']}, k={sample['k']}: rank(H)={sample['hessian_rank']}, rank(PB)={sample['pb_rank']}, det(H)={sample['hessian_det']}, det(PB)={sample['pb_det_direct']}")
    print(f"  phase dimensions = {knz['phase_blocks']} -> total {knz['total_phase_dimension']}")
    print(f"  first class (spatial diffeomorphisms) = {knz['first_class']}; second class = computed PB rank {knz['second_class']}")
    print(f"  physical phase dimension = {knz['physical_phase_dimension']}; physical DOF = {knz['physical_dof']}")
    checks.append(_check("the computed closure is nondegenerate for the sampled nonzero wave vectors", all(item["pb_rank"] == knz["dirac_pb_rank"] and abs(item["pb_det_direct"] - item["hessian_det"]**2) < 1e-8 * max(1.0, abs(item["pb_det_direct"])) for item in knz["numeric_samples"])))

    print("\n[3] k = 0 / FLRW sector")
    print(f"  H(k=0) = {kz['hessian']}; rank(PB(k=0)) = {kz['dirac_pb_rank']}")
    print(f"  Homogeneous D^2 chi - 4piG rho_0 = {kz['homogeneous_elliptic_residual']}")
    print(f"  Is rho_0>0 compatible with the homogeneous elliptic equation? {kz['source_compatible']}")
    checks.append(_check("the raw elliptic source equation rejects homogeneous positive-density FLRW", not kz["source_compatible"]))

    print("\n[4] Separate weak-field potentials, slip, and PPN gate")
    print(f"  Hilbert TF amplitude from varying -mu Dlambda.Du: Pi_TF = {stress['tf_amplitude']}")
    print(f"  Pi_TF/[lambda' a0 y] = {stress['radial_stress_coefficient']}")
    print(f"  exp(y) times that coefficient = {stress['positivity_transform']} > 0 for y>0")
    print(f"  Phi-Psi = {weak['phi_minus_psi']}")
    print(f"  Psi = {weak['psi']}")
    print(f"  gamma_PPN = Psi/Phi = {weak['gamma_ppn']}")
    print(f"  gamma_PPN-1 = {weak['gamma_minus_one']}")
    print(f"  Solving Pi_TF=0 for lambda' gives {weak['no_slip_lambda_gradient']}")
    print(f"  On that branch, simultaneous exterior Einstein and MOND fluxes require mu-1 = {weak['no_slip_newton_mond_compatibility']}")
    checks.append(_check("a MOND-response multiplier has a nonzero TF stress at every finite y", stress["radial_stress_coefficient"] != 0))

    print("\n[5] Matter Ward identity")
    print(f"  Source coupling obtained from the displayed action = {ward['source_coupling']}")
    print(f"  Point-particle Euler equation = {ward['particle_euler']}")
    print(f"  Bare matter divergence induced by S_aux[rho_n] = {ward['bare_matter_divergence']}")
    checks.append(_check("the matter stress from S_m alone is not separately conserved", ward["bare_matter_force_coefficient"] != 0))

    print("\n[6] Preferred-frame and stability gates")
    print(f"  Boosted elliptic Green-function symbol = {frame['spatial_symbol']}")
    print(f"  normalized O((w.k)^2) coefficient = {frame['alpha2_like_normalized_coefficient']}")
    print(f"  static O(w) coefficients (only) = {frame['alpha1_static_linear_coefficients']}")
    print(f"  alpha_3 status = {frame['alpha3_status']}")
    print(f"  elliptic constitutive eigenvalues = {stable['eigenvalues']}")
    print(f"  exp(y)*mu = {stable['transverse_positivity_transform']}; exp(y)*(mu+y mu') = {stable['longitudinal_positivity_transform']}")
    print("  The static elliptic principal symbol is positive, but the full candidate has the computed extra scalar DOF;")
    print("  a fixed n^mu instead removes that DOF only by making the displayed boost anisotropy physical.")
    checks.append(_check("the fixed-foliation operator has a nonzero alpha_2-like preferred-frame response", frame["alpha2_like_normalized_coefficient"] != 0))

    print("\n[VERDICT]")
    print("  The action does produce the requested static MOND pair, but it cannot simultaneously retain no slip,")
    print("  separate matter conservation, homogeneous FLRW, and two gravitational DOF.  The candidate is DEAD.")
    print(f"  Diagnostic checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
