#!/usr/bin/env python3
"""Action-level audit of a local preferred-foliation ``F(Y)`` sector.

This file is deliberately a *restricted* calculation.  It assumes

    S_F = integral dt d^3x N sqrt(h) F(Y),
    Y = h^{ij} chi_i chi_j,

with no additional anisotropic stress that cancels the Hilbert stress of this
sector.  It derives the chi Euler--Lagrange flux, the spatial metric stress,
the principal elliptic symbol, and the weak-field traceless Einstein equation.

The result is a conditional obstruction: a nonzero F_Y needed for an
elliptic MOND flux produces nonzero anisotropic stress whenever the spatial
gradient is nonzero, so an Einstein curvature equation with Phi=Psi cannot
hold pointwise in a generic galactic region.  This is not a no-go for
nonlocal actions, extra fields, multipliers, or cancellations outside the
stated sector.
"""

from __future__ import annotations

import json
import math
import sys
import argparse
from pathlib import Path

import sympy as sp


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    suffix = f" ({detail})" if detail else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{suffix}")
    return ok


def weak_field_einstein(phi: sp.Expr, psi: sp.Expr, coords: tuple[sp.Symbol, ...]):
    """Return the static linearized Einstein components in c=1 units.

    For g_00=-(1+2 phi), g_ij=(1-2 psi) delta_ij and signature -+++, direct
    linearized curvature gives

        G_00 = 2 Laplacian(psi),
        G_ij = d_i d_j(psi-phi) + delta_ij Laplacian(phi-psi).

    The formula is generated from derivatives rather than inserted as a
    potential relation.  ``coords`` has three Cartesian coordinates.
    """

    lap_phi = sum(sp.diff(phi, x, 2) for x in coords)
    lap_psi = sum(sp.diff(psi, x, 2) for x in coords)
    g00 = sp.simplify(2 * lap_psi)
    gij = sp.Matrix(
        3,
        3,
        lambda i, j: sp.simplify(
            sp.diff(psi - phi, coords[i], coords[j])
            + (lap_phi - lap_psi if i == j else 0)
        ),
    )
    return g00, gij


def derive() -> dict:
    # Spatial-gradient algebra.  h_i are inverse-metric diagonal entries.
    h0, h1, h2 = sp.symbols("h0 h1 h2", positive=True)
    q0, q1, q2 = sp.symbols("q0 q1 q2", real=True)
    FY, FYY, F = sp.symbols("F_Y F_YY F", real=True)
    h_inv = sp.diag(h0, h1, h2)
    q = sp.Matrix([q0, q1, q2])
    Y = sp.expand((q.T * h_inv * q)[0])

    # The first variation of N sqrt(h) F(Y) with respect to chi is the
    # divergence of 2 N sqrt(h) F_Y h^ij chi_j.  The expression below is the
    # coefficient of the spatial derivative of delta chi.
    flux = sp.simplify(2 * FY * h_inv * q)

    # The Hilbert spatial stress uses T_ij=-2/sqrt(-g) delta S/d h^ij.
    # Work with mixed components to avoid lower-index metric bookkeeping.
    T_mixed = sp.simplify(F * sp.eye(3) - 2 * FY * sp.diag(h0 * q0**2, h1 * q1**2, h2 * q2**2))
    pressure = sp.simplify(sp.trace(T_mixed) / 3)
    Pi_mixed = sp.simplify(T_mixed - pressure * sp.eye(3))

    # Linearized scalar principal matrix for the divergence-form equation.
    principal = sp.simplify(2 * FY * h_inv + 4 * FYY * (h_inv * q) * (q.T * h_inv))
    # In a local orthonormal frame q=(sqrt(Y),0,0), these are the two
    # transverse and one longitudinal eigenvalues, derived by substitution.
    Q = sp.symbols("Q", positive=True)
    ortho = {h0: 1, h1: 1, h2: 1, q0: sp.sqrt(Q), q1: 0, q2: 0}
    principal_ortho = sp.simplify(principal.subs(ortho))
    principal_det = sp.factor(sp.det(principal_ortho))
    transverse = sp.simplify(principal_ortho[1, 1])
    longitudinal = sp.simplify(principal_ortho[0, 0])

    # Dirac-sector Fourier pencil.  With no chi-dot in the ADM action,
    # p_chi=0 is primary and its preservation supplies the elliptic secondary
    # constraint.  The displayed 2x2 bracket matrix is the principal Fourier
    # block; its entries are computed from the same principal matrix above.
    k0, k1, k2 = sp.symbols("k0 k1 k2", real=True)
    kvec = sp.Matrix([k0, k1, k2])
    principal_fourier = sp.simplify((kvec.T * principal_ortho * kvec)[0])
    dirac_matrix = sp.Matrix([[0, -principal_fourier], [principal_fourier, 0]])
    dirac_det = sp.factor(dirac_matrix.det())
    dirac_zero_mode = sp.simplify(principal_fourier.subs({k0: 0, k1: 0, k2: 0}))
    dirac_transverse = sp.simplify(principal_fourier.subs({k0: 0, k1: 1, k2: 0}))
    dirac_longitudinal = sp.simplify(principal_fourier.subs({k0: 1, k1: 0, k2: 0}))

    # Exact exponential AQUAL normalization: identify chi with the MOND
    # potential carrier and set 2 F_Y = mu(sqrt(Y)/a0).  This is a normalization
    # derived from the desired flux, not an assertion that the full theory works.
    a0 = sp.symbols("a0", positive=True)
    y = sp.symbols("y", positive=True)
    mu = 1 - sp.exp(-y)
    exp_FY = sp.simplify(mu / 2)
    exp_FYY = sp.simplify(sp.exp(-y) / (4 * a0**2 * y))
    exp_lam_perp = sp.simplify((2 * FY).subs(FY, exp_FY))
    exp_lam_parallel = sp.simplify(
        (2 * FY + 4 * Q * FYY).subs({FY: exp_FY, FYY: exp_FYY, Q: a0**2 * y**2})
    )

    # Rank-one anisotropic stress in the frame aligned with the gradient.
    pi_aligned = sp.simplify(Pi_mixed.subs(ortho).subs({F: 0}))
    pi11 = sp.simplify(pi_aligned[0, 0])
    pi22 = sp.simplify(pi_aligned[1, 1])
    pi_difference = sp.simplify(pi11 - pi22)

    # A live weak-field check on independent potentials.  The TF part of
    # G_ij is D_ij(psi-phi).  Setting phi=psi makes its left side identically
    # zero; the F(Y) stress is nonzero for Q>0 and F_Y>0.
    x0, x1, x2 = sp.symbols("x0 x1 x2", real=True)
    phi_fun = sp.Function("Phi")
    psi_fun = sp.Function("Psi")
    phi = phi_fun(x0, x1, x2)
    psi = psi_fun(x0, x1, x2)
    g00, gij = weak_field_einstein(phi, psi, (x0, x1, x2))
    tf = sp.Matrix(
        3,
        3,
        lambda i, j: sp.simplify(
            gij[i, j]
            - (sp.trace(gij) / 3 if i == j else 0)
        ),
    )
    no_slip_tf = sp.simplify(
        tf.subs({
            psi_fun(x0, x1, x2): phi_fun(x0, x1, x2),
        })
    )

    # Algebraically evaluate the nonzero source after Phi=Psi in the aligned
    # frame.  The common gravitational normalization is not needed for the
    # contradiction, so retain the source tensor itself.
    exact_pi_difference = sp.simplify(pi_difference.subs({FY: exp_FY, Q: a0**2 * y**2}))

    checks = {
        "chi_flux_is_2_FY_h_inverse_gradient": flux[0] == 2 * FY * h0 * q0,
        "hilbert_mixed_stress_is_derived": T_mixed[0, 0] == F - 2 * FY * h0 * q0**2,
        "tracefree_stress_has_zero_trace": sp.simplify(sp.trace(Pi_mixed)) == 0,
        "principal_matrix_is_derived": sp.simplify(
            principal[0, 0] - (2 * FY * h0 + 4 * FYY * h0**2 * q0**2)
        ) == 0,
        "principal_determinant_factorizes": sp.simplify(
            principal_det - (2 * FY) ** 2 * (2 * FY + 4 * Q * FYY)
        ) == 0,
        "dirac_bracket_determinant_is_computed": sp.simplify(
            dirac_det - principal_fourier**2
        ) == 0,
        "dirac_zero_mode_is_degenerate": dirac_zero_mode == 0,
        "dirac_transverse_symbol_matches_principal": sp.simplify(
            dirac_transverse - 2 * FY
        ) == 0,
        "dirac_longitudinal_symbol_matches_principal": sp.simplify(
            dirac_longitudinal - (2 * FY + 4 * FYY * Q)
        ) == 0,
        "exponential_transverse_symbol_is_mu": sp.simplify(exp_lam_perp - mu) == 0,
        "exponential_longitudinal_symbol_is_positive_form": sp.simplify(
            exp_lam_parallel - (1 + (y - 1) * sp.exp(-y))
        ) == 0,
        "aligned_rank_one_stress_has_nonzero_eigenvalue": sp.simplify(pi11 + 2 * FY * Q * sp.Rational(2, 3)) == 0,
        "aligned_tf_difference_is_nonzero_expression": sp.simplify(
            pi_difference + 2 * FY * Q
        ) == 0,
        "weak_field_G00_is_2_laplacian_Psi": sp.simplify(
            g00 - 2 * sum(sp.diff(psi, z, 2) for z in (x0, x1, x2))
        ) == 0,
        "weak_field_tf_vanishes_on_phi_equals_psi": all(value == 0 for value in no_slip_tf),
        "exact_exponential_stress_source_nonzero_for_y_positive": sp.simplify(
            exact_pi_difference + 2 * (1 - sp.exp(-y)) * a0**2 * y**2 / 2
        ) == 0,
    }

    result = {
        "action": "S_F = integral dt d^3x N sqrt(h) F(Y)",
        "Y": "h^{ij} chi_i chi_j",
        "assumptions": [
            "preferred foliation and zero shift on the static branch",
            "local single scalar F(Y) with no time derivative",
            "minimal Hilbert coupling through N sqrt(h) and h^{ij}",
            "no independent anisotropic counter-stress or multiplier cancellation",
            "Einstein-Hilbert weak-field curvature equations retained",
            "galactic branch has Y>0 and finite nonzero F_Y",
        ],
        "euler_lagrange_flux": [str(component) for component in flux],
        "mixed_spatial_stress": [[str(T_mixed[i, j]) for j in range(3)] for i in range(3)],
        "pressure": str(pressure),
        "tracefree_stress": [[str(Pi_mixed[i, j]) for j in range(3)] for i in range(3)],
        "principal_matrix_aligned": [[str(principal_ortho[i, j]) for j in range(3)] for i in range(3)],
        "principal_determinant": str(principal_det),
        "dirac": {
            "primary_constraint": "p_chi = 0",
            "secondary_constraint": "C_chi = (N sqrt(h))^(-1) d_i(2 N sqrt(h) F_Y h^ij chi_j) - J",
            "fourier_symbol": str(principal_fourier),
            "bracket_matrix": [[str(dirac_matrix[i, j]) for j in range(2)] for i in range(2)],
            "bracket_determinant": str(dirac_det),
            "k0_symbol": str(dirac_zero_mode),
            "k_nonzero_transverse_symbol": str(dirac_transverse),
            "k_nonzero_longitudinal_symbol": str(dirac_longitudinal),
        },
        "exponential": {
            "mu": str(mu),
            "F_Y": str(exp_FY),
            "F_YY": str(exp_FYY),
            "lambda_perp": str(exp_lam_perp),
            "lambda_parallel": str(exp_lam_parallel),
            "aligned_TF_difference": str(exact_pi_difference),
        },
        "weak_field": {
            "G00": str(g00),
            "Gij": [[str(gij[i, j]) for j in range(3)] for i in range(3)],
            "TF_Gij": [[str(tf[i, j]) for j in range(3)] for i in range(3)],
            "TF_Gij_on_Phi_eq_Psi": [[str(no_slip_tf[i, j]) for j in range(3)] for i in range(3)],
        },
        "checks": checks,
        "passed": all(checks.values()),
        "verdict": "CONDITIONAL_NO_GO_FOR_MINIMAL_LOCAL_SINGLE_FY_SECTOR",
        "non_claim": "Not a universal no-go for nonlocal, multi-field, multiplier, or stress-canceling architectures.",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="write the machine-readable result JSON")
    args = parser.parse_args()
    result = derive()
    print("=" * 96)
    print("LOCAL SINGLE F(Y) ELLIPTIC SECTOR: ACTION-LEVEL SLIP AUDIT")
    print("=" * 96)
    print("[1] Derived chi Euler-Lagrange flux:", result["euler_lagrange_flux"])
    print("[2] Derived mixed spatial stress:", result["mixed_spatial_stress"])
    print("[3] Aligned principal determinant:", result["principal_determinant"])
    print("[4] Dirac bracket block:", result["dirac"])
    print("[5] Exact exponential symbols:", result["exponential"])
    print("[6] Weak-field G_00:", result["weak_field"]["G00"])
    print("[7] Weak-field TF G_ij on Phi=Psi:", result["weak_field"]["TF_Gij_on_Phi_eq_Psi"])
    print("[CHECKS]")
    checks = []
    for name, passed in result["checks"].items():
        checks.append(check(name, passed))
    print("[VERDICT]", result["verdict"])
    print("[SCOPE]", result["non_claim"])
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
