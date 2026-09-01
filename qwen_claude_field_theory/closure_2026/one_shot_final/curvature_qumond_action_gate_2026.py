#!/usr/bin/env python3
"""A curvature-sourced QUMOND action: reduced derivation and diagnostics.

Candidate B
===========
Let ``n_mu`` be a unit timelike normal, ``h_mn=g_mn+n_m n_n``,
``Delta_h=D_mu D^mu``, and ``Y=h^mn nabla_m chi nabla_n chi/a0^2``.  The
action is

 S_B = (16 pi G)^-1 integral sqrt(-g) [R - 2 Lambda
       - 2 lambda (Delta_h chi - R_mn n^m n^n) + 2 a0^2 Q(Y)] + S_m[g,psi],

 Q(Y) = 1 - (1 + sqrt(Y)) exp(-sqrt(Y)).

``lambda`` sources no matter field, so the action avoids the direct-density
candidate's explicit matter coupling.  In the scalar-isotropic static
reduction, lambda variation gives chi=Phi; chi variation
gives lambda'=(mu-1)Phi'; and the Phi equation gives

   div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho,

with mu=1-exp(-y), while the reduced Psi equation gives Phi=Psi.  This is a
serious action-derived candidate, but the reduced branch is not automatically
a solution of every component of the full metric equation.

The diagnostic below finds a nonzero spatial trace-free variation of Q(Y) on
every finite nonzero MOND gradient.  It keeps both -2 lambda Delta_h chi and
+2 lambda R_nn.  In a static
zero-shift slicing R_nn=N^{-1}D^2N; after integration by parts their algebraic
trace-free stresses cancel on the auxiliary shell D_i chi=D_i N.  The Q(Y)
term remains in this auxiliary subset (and the trace-free Hessian of an affine
lambda vanishes).  Because it is second order in weak fields, a valid no-slip
verdict also needs the same-order nonlinear Einstein tensor, second-order
potentials, and all remaining auxiliary terms.  They are not computed here.
The foliation and FLRW Hessians are diagnostics, not standalone ghost or PPN
theorems.

Scope: this script certifies the scalar-isotropic reduction and records partial
diagnostics.  Candidate B is falsified separately by the exact MOND/tensor-
luminality obstruction, not by the incomplete no-slip subset.
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


def _auxiliary_tf_diagnostic(constitutive: dict[str, sp.Expr]) -> dict[str, object]:
    """Vary an auxiliary TF subset on a constant-gradient patch.

    For a static zero-shift metric ``ds^2=-N^2dt^2+h_ij dx^i dx^j``,

        R_nn = N^{-1} D^2 N.

    Including the ``N sqrt(h)`` measure and integrating spatially by parts,
    the two multiplier terms have the exact local representatives

        -2 N lambda D^2 chi -> 2 N Dlambda.Dchi + 2 lambda DN.Dchi,
        +2 N lambda R_nn    -> -2 Dlambda.DN.

    The second term in the first line is cubic in weak fields.  It is retained
    symbolically and only then removed by the leading weak-field shell
    ``N=1, lambda=0, Dchi=DN``.  Thus the auxiliary cancellation below is
    computed rather than assumed.  This is not the full second-order metric
    equation: nonlinear Einstein terms and second-order metric potentials are
    outside this algebraic constant-gradient diagnostic.
    """
    a0, ell = sp.symbols("a0 lambda_prime", positive=True, real=True)
    lapse_value, lambda_value, lapse_prime = sp.symbols(
        "N lambda_value N_prime", real=True
    )
    y = constitutive["y"]
    e0, e1, e2 = sp.symbols("epsilon_0 epsilon_1 epsilon_2", real=True)
    inverse_metric = sp.diag(1 + e0, 1 + e1, 1 + e2)
    grad_chi = sp.Matrix([a0 * y, 0, 0])
    Y_metric = sp.simplify((grad_chi.T * inverse_metric * grad_chi)[0] / a0**2)
    root = sp.sqrt(Y_metric)
    Q_metric = 1 - (1 + root) * sp.exp(-root)
    density_Q = 2 * a0**2 * Q_metric
    origin = {e0: 0, e1: 0, e2: 0}

    grad_lambda = sp.Matrix([ell, 0, 0])
    grad_lapse = sp.Matrix([lapse_prime, 0, 0])
    dot = lambda left, right: (left.T * inverse_metric * right)[0]
    density_minus_lambda_delta = sp.simplify(
        2 * lapse_value * dot(grad_lambda, grad_chi)
        + 2 * lambda_value * dot(grad_lapse, grad_chi)
    )
    density_lambda_rnn = sp.simplify(-2 * dot(grad_lambda, grad_lapse))

    def tf_amplitude(density: sp.Expr) -> sp.Expr:
        radial = sp.diff(density, e0).subs(origin)
        transverse = sp.diff(density, e1).subs(origin)
        return sp.simplify(-2 * (radial - transverse))

    d_radial = sp.simplify(sp.diff(density_Q, e0).subs(origin))
    d_transverse = sp.simplify(sp.diff(density_Q, e1).subs(origin))
    q_tf_stress = sp.simplify(-2 * (d_radial - d_transverse))

    elliptic_tf_general = tf_amplitude(density_minus_lambda_delta)
    rnn_algebraic_tf_general = tf_amplitude(density_lambda_rnn)
    weak_shell = {
        lapse_value: 1,
        lambda_value: 0,
        lapse_prime: a0 * y,
    }
    elliptic_tf_on_shell = sp.simplify(elliptic_tf_general.subs(weak_shell))
    rnn_algebraic_tf_on_shell = sp.simplify(
        rnn_algebraic_tf_general.subs(weak_shell)
    )

    # The lambda R_nn contribution to the local TF metric equation is built
    # from the trace-free Hessian of lambda.  On the constant-gradient witness
    # lambda=(mu(y)-1)a0*y*x, that Hessian is computed rather than assumed.
    x = sp.symbols("x", real=True)
    lambda_profile = (constitutive["mu"] - 1) * a0 * y * x
    rnn_tf_stress = sp.simplify(sp.diff(lambda_profile, x, 2))
    elliptic_curvature_tf_on_shell = sp.simplify(
        elliptic_tf_on_shell + rnn_algebraic_tf_on_shell + rnn_tf_stress
    )
    auxiliary_tf_stress_on_shell = sp.simplify(
        q_tf_stress + elliptic_curvature_tf_on_shell
    )
    return {
        "q_density": density_Q,
        "q_radial_metric_derivative": d_radial,
        "q_transverse_metric_derivative": d_transverse,
        "q_tf_stress": q_tf_stress,
        "minus_lambda_delta_density": density_minus_lambda_delta,
        "lambda_rnn_density": density_lambda_rnn,
        "minus_lambda_delta_tf_general": elliptic_tf_general,
        "lambda_rnn_algebraic_tf_general": rnn_algebraic_tf_general,
        "minus_lambda_delta_tf_on_shell": elliptic_tf_on_shell,
        "lambda_rnn_algebraic_tf_on_shell": rnn_algebraic_tf_on_shell,
        "rnn_tf_stress_on_constant_gradient_patch": rnn_tf_stress,
        "elliptic_curvature_tf_on_shell": elliptic_curvature_tf_on_shell,
        "auxiliary_tf_stress_on_shell": auxiliary_tf_stress_on_shell,
        "full_second_order_metric_equation_included": False,
        "no_slip_verdict": "UNRESOLVED",
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
        "auxiliary_tf_diagnostic": _auxiliary_tf_diagnostic(constitutive),
        "matter_ward_scope": {
            "status": "ANALYTIC CONDITIONAL",
            "assumptions": (
                "S_m is separately diffeomorphism invariant and minimally coupled "
                "to g; S_aux contains no ordinary matter field psi"
            ),
            "identity": "nabla_mu T^{mu nu}=0 on the ordinary matter equations",
            "computed_by_this_gate": False,
        },
        "fixed_foliation": _fixed_foliation(),
        "clock_flrw": _clock_flrw(),
        "a0_relation": "external phenomenological input: a0=c^2 sqrt(Lambda/(32 pi)); not derived by S_B",
    }


def main() -> int:
    result = derive_curvature_qumond_gate()
    static = result["static_variation"]
    tf_diagnostic = result["auxiliary_tf_diagnostic"]
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
    print("  matter Ward status =", result["matter_ward_scope"]["status"])
    print("  matter Ward assumptions =", result["matter_ward_scope"]["assumptions"])

    print("\n[3] Partial auxiliary trace-free metric diagnostic")
    print("  Q trace-free stress amplitude =", tf_diagnostic["q_tf_stress"])
    print("  -2 lambda Delta_h chi algebraic TF stress on shell =", tf_diagnostic["minus_lambda_delta_tf_on_shell"])
    print("  +2 lambda R_nn algebraic TF stress on shell =", tf_diagnostic["lambda_rnn_algebraic_tf_on_shell"])
    print("  lambda R_nn Hessian TF contribution on affine witness =", tf_diagnostic["rnn_tf_stress_on_constant_gradient_patch"])
    print("  elliptic+curvature auxiliary TF contribution on shell =", tf_diagnostic["elliptic_curvature_tf_on_shell"])
    print("  auxiliary TF subset on shell =", tf_diagnostic["auxiliary_tf_stress_on_shell"])
    print("  full second-order metric equation included =", tf_diagnostic["full_second_order_metric_equation_included"])
    print("  no-slip verdict from this diagnostic =", tf_diagnostic["no_slip_verdict"])

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
        tf_diagnostic["elliptic_curvature_tf_on_shell"] == 0
        and tf_diagnostic["auxiliary_tf_stress_on_shell"] == tf_diagnostic["q_tf_stress"]
        and tf_diagnostic["auxiliary_tf_stress_on_shell"] != 0,
        tf_diagnostic["full_second_order_metric_equation_included"] is False
        and tf_diagnostic["no_slip_verdict"] == "UNRESOLVED",
        fixed["alpha2_like_coefficient"] != 0,
        flrw["velocity_hessian_det"] != 0,
        flrw["eigenvalue_product"] < 0,
    ]
    labels = [
        "the Q primitive gives the exact exponential coefficient",
        "all four static Euler--Lagrange equations were obtained from the displayed action",
        "the action-derived scalar branch gives the exact MOND flux law",
        "the displayed auxiliary TF subset is generated consistently",
        "the incomplete TF subset is not promoted to a no-slip verdict",
        "an external foliation gives nonzero preferred-frame anisotropy",
        "a clock foliation has no auxiliary velocity degeneracy on FLRW",
        "the clock-normal FLRW velocity block is indefinite",
    ]
    passed_checks = [bool(okay) for okay in checks]
    for okay, label in zip(passed_checks, labels):
        print(f"  [{'PASS' if okay else 'FAIL'}] {label}")

    print("\n[VERDICT]")
    print("  This script certifies only the scalar-isotropic MOND reduction and partial diagnostics.")
    print("  It does not derive Phi and Psi independently at full second order, classify the clock pole,")
    print("  or turn an unreduced Hessian sign into a ghost theorem.  Candidate B is killed instead by")
    print("  the separate exact MOND/tensor-luminality obstruction.  The a0-Lambda relation remains input.")
    print(f"  Diagnostic checks: {sum(passed_checks)}/{len(passed_checks)}")
    return 0 if all(passed_checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
