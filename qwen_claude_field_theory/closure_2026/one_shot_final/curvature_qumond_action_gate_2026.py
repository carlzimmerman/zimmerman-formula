#!/usr/bin/env python3
"""A fully specified curvature-sourced QUMOND action, derived and stress-tested.

Candidate B
===========
Let ``n_mu`` be a unit timelike normal, ``h_mn=g_mn+n_m n_n``,
``Delta_h=D_mu D^mu``, and ``Y=h^mn nabla_m chi nabla_n chi/a0^2``.  The
action is

 S_B = (16 pi G)^-1 integral sqrt(-g) [R - 2 Lambda
       - 2 lambda (Delta_h chi - R_mn n^m n^n) + 2 a0^2 Q(Y)] + S_m[g,psi],

 Q(Y) = 1 - (1 + sqrt(Y)) exp(-sqrt(Y)).

``lambda`` sources no matter field, so this action deliberately fixes the
bare-matter Ward failure of the direct-density elliptic candidate.  In the
static Newtonian reduction, lambda variation gives chi=Phi; chi variation
gives lambda'=(mu-1)Phi'; and the Phi equation gives

   div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho,

with mu=1-exp(-y), while the scalar trace-free Einstein equation gives
Phi=Psi.  Thus it is a serious, action-derived candidate, not a pasted
phantom density.

The full gates then falsify it.  The Q(Y) term has a nonzero physical spatial
trace-free stress on every finite MOND gradient.  On a constant-gradient local
patch the lambda R_nn term contributes only D_i D_j lambda and cannot cancel
that stress.  Hence the scalar weak-field no-slip inference is not preserved
by the full metric variation.  The required normal has a second independent
failure: fixed n gives a boost-anisotropic elliptic symbol, while a clock
normal has a nondegenerate, indefinite FLRW (a,lambda) kinetic block.

Scope: the no-slip calculation is a local constant-gradient witness for this
explicit action.  It kills Candidate B, but does not prove a no-go for every
conceivable tensorial nonlocal action.
"""

from __future__ import annotations

import sys

import sympy as sp


def _euler(density: sp.Expr, field: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.diff(density, field)
        - sp.diff(sp.diff(density, sp.diff(field, coordinate)), coordinate)
    )


def _constitutive() -> dict[str, sp.Expr]:
    y = sp.symbols("y", positive=True, real=True)
    Y = sp.symbols("Y", positive=True, real=True)
    mu = 1 - sp.exp(-y)
    Q_y = 1 - (1 + y) * sp.exp(-y)
    Q_Y = sp.simplify(sp.diff(Q_y, y) / (2 * y))
    return {
        "y": y,
        "Y": Y,
        "mu": mu,
        "Q_y": Q_y,
        "Q_Y": Q_Y,
        "q_derivative_residual": sp.simplify(Q_Y - (1 - mu) / 2),
    }


def _static_variation(constitutive: dict[str, sp.Expr]) -> dict[str, object]:
    """Vary the actual weak-static reduction of S_B before imposing equations."""
    x = sp.symbols("x", real=True)
    G, a0 = sp.symbols("G a0", positive=True, real=True)
    rho = sp.Function("rho")(x)
    phi = sp.Function("Phi")(x)
    psi = sp.Function("Psi")(x)
    chi = sp.Function("chi")(x)
    lam = sp.Function("lambda")(x)
    phi_x = sp.diff(phi, x)
    psi_x = sp.diff(psi, x)
    chi_x = sp.diff(chi, x)
    y_chi = chi_x / a0
    Q_chi = 1 - (1 + y_chi) * sp.exp(-y_chi)

    # Fierz--Pauli scalar action plus the actual lambda(R_nn-Delta_h chi)
    # reduction.  R_nn=Phi_xx at this order.  Both integrations by parts are
    # displayed by the resulting lambda_x(chi_x-Phi_x) coupling.
    density = (
        -2 * phi_x * psi_x
        + psi_x**2
        - 8 * sp.pi * G * rho * phi
        + 2 * sp.diff(lam, x) * (chi_x - phi_x)
        + 2 * a0**2 * Q_chi
    )
    e_phi = _euler(density, phi, x)
    e_psi = _euler(density, psi, x)
    e_chi = _euler(density, chi, x)
    e_lam = _euler(density, lam, x)

    mu_chi = 1 - sp.exp(-y_chi)
    expected_phi = 2 * sp.diff(psi, x, 2) + 2 * sp.diff(lam, x, 2) - 8 * sp.pi * G * rho
    expected_psi = 2 * sp.diff(phi, x, 2) - 2 * sp.diff(psi, x, 2)
    expected_chi = -2 * sp.diff(
        sp.diff(lam, x) + (1 - mu_chi) * chi_x,
        x,
    )
    expected_lam = -2 * sp.diff(chi_x - phi_x, x)
    action_residuals = tuple(sp.simplify(actual - expected) for actual, expected in (
        (e_phi, expected_phi),
        (e_psi, expected_psi),
        (e_chi, expected_chi),
        (e_lam, expected_lam),
    ))

    # On the isolated branch chi=Phi and Psi=Phi, chi variation gives
    # lambda_x=(mu-1) Phi_x.  Substitution in the Phi equation derives MOND.
    lambda_xx_solution = -sp.diff((1 - mu_chi) * chi_x, x)
    phi_equation = sp.simplify(expected_phi.subs({psi: phi, chi: phi}) / 2)
    phi_equation_on_auxiliary_shell = sp.simplify(
        phi_equation.subs(sp.diff(lam, x, 2), lambda_xx_solution.subs(chi, phi))
    )
    mond_equation = sp.simplify(
        sp.diff((1 - sp.exp(-phi_x / a0)) * phi_x, x) - 4 * sp.pi * G * rho
    )
    mond_flux_residual = sp.simplify(phi_equation_on_auxiliary_shell - mond_equation)

    return {
        "density": density,
        "e_phi": e_phi,
        "e_psi": e_psi,
        "e_chi": e_chi,
        "e_lambda": e_lam,
        "action_residuals": action_residuals,
        "mu_chi": mu_chi,
        "lambda_xx_solution": lambda_xx_solution,
        "mond_equation": mond_equation,
        "mond_flux_residual": mond_flux_residual,
        "phi_equation_on_auxiliary_shell": phi_equation_on_auxiliary_shell,
    }


def _full_metric_no_slip(constitutive: dict[str, sp.Expr]) -> dict[str, sp.Expr]:
    """Vary Q(Y) with respect to all spatial metric components, not just Psi."""
    a0, ell = sp.symbols("a0 lambda_prime", positive=True, real=True)
    y = constitutive["y"]
    e0, e1, e2 = sp.symbols("epsilon_0 epsilon_1 epsilon_2", real=True)
    inverse_metric = sp.diag(1 + e0, 1 + e1, 1 + e2)
    grad_chi = sp.Matrix([a0 * y, 0, 0])
    Y_metric = sp.simplify((grad_chi.T * inverse_metric * grad_chi)[0] / a0**2)
    root = sp.sqrt(Y_metric)
    Q_metric = 1 - (1 + root) * sp.exp(-root)
    density_Q = 2 * a0**2 * Q_metric
    origin = {e0: 0, e1: 0, e2: 0}
    d_radial = sp.simplify(sp.diff(density_Q, e0).subs(origin))
    d_transverse = sp.simplify(sp.diff(density_Q, e1).subs(origin))
    q_tf_stress = sp.simplify(-2 * (d_radial - d_transverse))

    # The lambda R_nn contribution to the local TF metric equation is built
    # from the trace-free Hessian of lambda.  On the constant-gradient witness
    # lambda=(mu(y)-1)a0*y*x, that Hessian is computed rather than assumed.
    x = sp.symbols("x", real=True)
    lambda_profile = (constitutive["mu"] - 1) * a0 * y * x
    rnn_tf_stress = sp.simplify(sp.diff(lambda_profile, x, 2))
    return {
        "q_density": density_Q,
        "q_radial_metric_derivative": d_radial,
        "q_transverse_metric_derivative": d_transverse,
        "q_tf_stress": q_tf_stress,
        "rnn_tf_stress_on_constant_gradient_patch": rnn_tf_stress,
    }


def _fixed_foliation() -> dict[str, sp.Expr]:
    """Compute the boost anisotropy of the spatial elliptic inverse."""
    kx, ky, kz, w_dot_k_squared = sp.symbols(
        "k_x k_y k_z w_dot_k_squared", real=True, nonnegative=True
    )
    k2 = kx**2 + ky**2 + kz**2
    green = 1 / (k2 + w_dot_k_squared)
    return {
        "green": green,
        "alpha2_like_coefficient": sp.simplify(
            sp.diff(green, w_dot_k_squared).subs(w_dot_k_squared, 0) * k2**2
        ),
    }


def _clock_flrw() -> dict[str, object]:
    """Derive the FLRW velocity block when n_mu is the clock normal."""
    a, lam, a_dot, lam_dot = sp.symbols("a lambda a_dot lambda_dot", positive=True, real=True)
    # In unitary clock gauge and N=1, R_nn=-3 a_ddot/a.  The term
    # 2 a^3 lambda R_nn=-6 a^2 lambda a_ddot becomes this density after one
    # exact integration by parts.
    integrated_auxiliary_density = 12 * a * lam * a_dot**2 + 6 * a**2 * a_dot * lam_dot
    hessian = sp.hessian(integrated_auxiliary_density, (a_dot, lam_dot))
    eigenvalues = list(hessian.eigenvals().keys())
    return {
        "integrated_auxiliary_density": integrated_auxiliary_density,
        "velocity_hessian": hessian,
        "velocity_hessian_det": sp.simplify(hessian.det()),
        "eigenvalues": eigenvalues,
        "eigenvalue_product": sp.simplify(sp.prod(eigenvalues)),
        "nullity": len(hessian.nullspace()),
    }


def derive_curvature_qumond_gate() -> dict[str, object]:
    """Return every derived gate for Candidate B."""
    constitutive = _constitutive()
    return {
        "action": {
            "covariant": (
                "(16 pi G)^-1 integral sqrt(-g)[R-2 Lambda"
                "-2 lambda(Delta_h chi-R_mn n^m n^n)+2 a0^2 Q(Y)] + S_m[g,psi]"
            ),
            "fields": ("g_mn", "chi", "lambda", "n_mn or clock T", "psi"),
            "Y": "h^mn nabla_m chi nabla_n chi/a0^2",
        },
        "constitutive": constitutive,
        "static_variation": _static_variation(constitutive),
        "no_slip": _full_metric_no_slip(constitutive),
        "matter_ward": {
            "auxiliary_matter_variation": sp.Integer(0),
            "statement": "S_aux contains no psi; minimally coupled matter retains its own diffeomorphism Ward identity.",
        },
        "fixed_foliation": _fixed_foliation(),
        "clock_flrw": _clock_flrw(),
        "a0_relation": "external phenomenological input: a0=c^2 sqrt(Lambda/(32 pi)); not derived by S_B",
    }


def main() -> int:
    result = derive_curvature_qumond_gate()
    static = result["static_variation"]
    no_slip = result["no_slip"]
    fixed = result["fixed_foliation"]
    flrw = result["clock_flrw"]
    constitutive = result["constitutive"]

    print("=" * 94)
    print("ONE-SHOT CANDIDATE B: CURVATURE-SOURCED QUMOND ACTION")
    print("=" * 94)
    print("\n[1] Explicit action and exact constitutive identity")
    print("  S_B =", result["action"]["covariant"])
    print("  Q(y^2) =", constitutive["Q_y"])
    print("  Q_Y =", constitutive["Q_Y"])
    print("  mu(y) =", constitutive["mu"])
    print("  Q_Y-(1-mu)/2 =", constitutive["q_derivative_residual"])

    print("\n[2] Varied weak-static equations")
    print("  delta S/dPhi =", static["e_phi"])
    print("  delta S/dPsi =", static["e_psi"])
    print("  delta S/dchi =", static["e_chi"])
    print("  delta S/dlambda =", static["e_lambda"])
    print("  action-derivation residuals =", static["action_residuals"])
    print("  derived MOND equation =", static["mond_equation"])
    print("  MOND residual =", static["mond_flux_residual"])
    print("  direct auxiliary variation with respect to matter =", result["matter_ward"]["auxiliary_matter_variation"])

    print("\n[3] Full spatial metric variation: no-slip test")
    print("  Q trace-free stress amplitude =", no_slip["q_tf_stress"])
    print("  lambda R_nn TF contribution on constant-gradient witness =", no_slip["rnn_tf_stress_on_constant_gradient_patch"])
    print("  [PASS] the full Q(Y) metric variation contains an uncancelled MOND TF stress" if no_slip["q_tf_stress"] != 0 and no_slip["rnn_tf_stress_on_constant_gradient_patch"] == 0 else "  [FAIL] TF witness")

    print("\n[4] Foliation and FLRW alternatives")
    print("  fixed-foliation alpha_2-like coefficient =", fixed["alpha2_like_coefficient"])
    print("  clock-normal FLRW auxiliary density =", flrw["integrated_auxiliary_density"])
    print("  clock-normal velocity Hessian =", flrw["velocity_hessian"])
    print("  det(H) =", flrw["velocity_hessian_det"])
    print("  eigenvalue product =", flrw["eigenvalue_product"])
    print("  Hessian nullity =", flrw["nullity"])

    checks = [
        constitutive["q_derivative_residual"] == 0,
        static["action_residuals"] == (0, 0, 0, 0),
        static["mond_flux_residual"] == 0,
        result["matter_ward"]["auxiliary_matter_variation"] == 0,
        no_slip["q_tf_stress"] != 0 and no_slip["rnn_tf_stress_on_constant_gradient_patch"] == 0,
        fixed["alpha2_like_coefficient"] != 0,
        flrw["velocity_hessian_det"] != 0,
        flrw["eigenvalue_product"] < 0,
    ]
    labels = [
        "the Q primitive gives the exact exponential coefficient",
        "all four static Euler--Lagrange equations were obtained from the displayed action",
        "the action-derived scalar branch gives the exact MOND flux law",
        "the auxiliary action does not directly vary the matter fields",
        "full metric variation defeats scalar no slip on a constant-gradient MOND patch",
        "an external foliation gives nonzero preferred-frame anisotropy",
        "a clock foliation has no auxiliary velocity degeneracy on FLRW",
        "the clock-normal FLRW velocity block is indefinite",
    ]
    for okay, label in zip(checks, labels):
        print(f"  [{'PASS' if okay else 'FAIL'}] {label}")

    print("\n[VERDICT]")
    print("  Candidate B is DEAD.  It is better than the direct-density elliptic action: exact MOND and")
    print("  bare-matter conservation arise from one action.  But the same Q(Y) term produces an uncancelled")
    print("  trace-free metric stress, so Phi=Psi is not a full metric equation.  A fixed normal also violates")
    print("  preferred-frame requirements; promoting it to a clock gives an indefinite FLRW kinetic block.")
    print("  The a0-Lambda relation remains an external input in this candidate.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
