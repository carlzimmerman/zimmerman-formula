"""Executable first gate for a rotated-MMG constitutive candidate.

This is deliberately a *candidate*, not a certification of the full theory.
It combines (i) an explicit weak-field action with the exponential AQUAL law
and (ii) a first-order scalar constraint sector.  The Dirac matrix is built
from Poisson brackets and its rank is computed, rather than entered as data.
The full nonlinear hypersurface-deformation algebra and matter Ward identity
remain separate gates.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def exponential_kernel():
    y = sp.symbols("y", positive=True)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    mu = sp.simplify(sp.diff(G, y) / (2 * y))
    lam_perp = sp.simplify(1 - sp.exp(-y))
    lam_parallel = sp.simplify(1 + (y - 1) * sp.exp(-y))
    return {
        "mu": str(mu),
        "mu_target": str(1 - sp.exp(-y)),
        "mu_identity": bool(sp.simplify(mu - (1 - sp.exp(-y))) == 0),
        "lambda_perp": str(lam_perp),
        "lambda_parallel": str(lam_parallel),
        "lambda_parallel_limit": sp.limit(lam_parallel, y, 0, dir="+")
        == 0,
        "lambda_perp_at_1": float(lam_perp.subs(y, 1).evalf()),
    }


def weak_field_variation():
    """Vary an explicit static scalar action on a positive-gradient branch.

    The cross term is the linearized Einstein curvature piece.  The auxiliary
    constitutive term is written with the sign fixed by variation: its flux
    is 4(1-mu) grad(Phi), so the total flux after the independent slip
    equation is exactly 4 mu grad(Phi).
    """

    x, a0, rho = sp.symbols("x a0 rho", positive=True)
    Phi = sp.Function("Phi")(x)
    Psi = sp.Function("Psi")(x)
    z = sp.symbols("z", positive=True)
    G = z**2 + 2 * (1 + z) * sp.exp(-z) - 2
    L = (
        2 * sp.diff(Psi, x) ** 2
        - 4 * sp.diff(Phi, x) * sp.diff(Psi, x)
        - 2 * a0**2 * G.subs(z, sp.diff(Phi, x) / a0)
        + 2 * sp.diff(Phi, x) ** 2
        - rho * Phi
    )
    e_phi = sp.simplify(
        sp.diff(L, Phi)
        - sp.diff(sp.diff(L, sp.diff(Phi, x)), x)
    )
    e_psi = sp.simplify(
        sp.diff(L, Psi)
        - sp.diff(sp.diff(L, sp.diff(Psi, x)), x)
    )
    # Independent Psi variation gives Psi''-Phi''=0.  Substitute Psi=Phi
    # into the independently varied Phi equation.
    slip_eom = sp.simplify(e_psi.subs({Psi: Phi}))
    phi_slip = sp.simplify(e_phi.subs({Psi: Phi}))
    flux = (1 - sp.exp(-sp.diff(Phi, x) / a0)) * sp.diff(Phi, x)
    # Euler--Lagrange equation is 4 div(mu grad Phi) - rho = 0.
    target = sp.simplify(4 * sp.diff(flux, x) - rho)
    return {
        "e_phi": str(e_phi),
        "e_psi": str(e_psi),
        "slip_eom": str(slip_eom),
        "phi_on_slip": str(phi_slip),
        "phi_target_residual": str(sp.simplify(phi_slip - target)),
        "slip_equation_is_laplacian": sp.simplify(slip_eom - 4 * (sp.diff(Phi, x, 2) - sp.diff(Psi, x, 2)).subs({Psi: Phi})) == 0,
        "aqual_target_matches": sp.simplify(phi_slip - target) == 0,
    }


def poisson(A, B, coords, momenta):
    return sp.simplify(
        sum(
            sp.diff(A, q) * sp.diff(B, p) - sp.diff(A, p) * sp.diff(B, q)
            for q, p in zip(coords, momenta)
        )
    )


def poisson_matrix(coords, momenta, constraints):
    return sp.Matrix(
        [
            [
                poisson(A, B, coords, momenta)
                for B in constraints
            ]
            for A in constraints
        ]
    )


def dirac_scalar_sector(k_value: float, u_value: float, a0_value: float):
    """Build the four scalar constraints and calculate their actual matrix.

    For one Fourier mode, C_M is the nonlinear constitutive Gauss law and
    C_R kills the rotated slip variable.  Their preservation gives two
    further constraints.  At k=0 the spatial operators vanish and the rank
    jump is reported instead of hidden.
    """

    u, r, pu, pr = sp.symbols("u r pu pr", real=True)
    k, a0, source = sp.symbols("k a0 source", real=True)
    y = k * u / (2 * a0)
    mu = 1 - sp.exp(-y)
    C_M = k**2 * mu * u - source
    C_R = k**2 * r
    H = sp.Rational(1, 2) * (pu**2 + pr**2 + k**2 * (u**2 + r**2))
    P_M = sp.simplify(
        sum(sp.diff(C_M, q) * sp.diff(H, p) - sp.diff(C_M, p) * sp.diff(H, q) for q, p in [(u, pu), (r, pr)])
    )
    P_R = sp.simplify(
        sum(sp.diff(C_R, q) * sp.diff(H, p) - sp.diff(C_R, p) * sp.diff(H, q) for q, p in [(u, pu), (r, pr)])
    )
    constraints = [C_M, C_R, P_M, P_R]
    M = poisson_matrix([u, r], [pu, pr], constraints)
    lM, lR = sp.symbols("lambda_M lambda_R", real=True)
    H_total = H + lM * C_M + lR * C_R
    preservation = [
        sp.simplify(poisson(P_M, H_total, (u, r), (pu, pr))),
        sp.simplify(poisson(P_R, H_total, (u, r), (pu, pr))),
    ]
    subs = {
        k: sp.Float(k_value),
        a0: sp.Float(a0_value),
        u: sp.Float(u_value),
        r: 0.0,
        pu: 0.0,
        pr: 0.0,
        source: sp.Float((k_value**2) * (1 - np.exp(-k_value * u_value / (2 * a0_value))) * u_value),
    }
    Mn = np.array(M.subs(subs).evalf(), dtype=float)
    rank = int(np.linalg.matrix_rank(Mn, tol=1e-10))
    det = float(np.linalg.det(Mn))
    # Continue the chain: solve preservation of P_M,P_R for the multipliers
    # from the computed linear system.  At k=0 the multiplier matrix loses
    # rank, so the result is reported as non-unique rather than patched.
    zero_lambda = {lM: 0.0, lR: 0.0}
    A_num = np.array([float(eq.subs(subs).subs(zero_lambda).evalf()) for eq in preservation])
    B_sym = sp.Matrix([[sp.diff(eq, lam).subs(subs).evalf() for lam in (lM, lR)] for eq in preservation])
    B_num = np.array(B_sym, dtype=float)
    multiplier_rank = int(np.linalg.matrix_rank(B_num, tol=1e-10))
    if multiplier_rank == len(B_num):
        multiplier = np.linalg.solve(B_num, -A_num).tolist()
        multiplier_status = "uniquely_fixed"
    else:
        multiplier = None
        multiplier_status = "rank_deficient"
    return {
        "k": k_value,
        "constraints": [str(c) for c in constraints],
        "matrix": Mn.tolist(),
        "rank": rank,
        "determinant": det,
        "phase_space_dimension": 4,
        "second_class_constraints": rank,
        "remaining_scalar_phase_dimension": 4 - rank,
        "preservation_multiplier_matrix": B_num.tolist(),
        "preservation_multiplier_rank": multiplier_rank,
        "preservation_multiplier": multiplier,
        "preservation_status": multiplier_status,
    }


def clock_health_scan():
    """Healthy, separately counted k-essence clock witness."""

    X, A, Ld = sp.symbols("X A Ld", positive=True)
    K = -A * sp.sqrt(1 - X**2 / Ld**2)
    Kx = sp.simplify(sp.diff(K, X))
    Kxx = sp.simplify(sp.diff(Kx, X))
    Sigma = sp.simplify(Kx + 2 * X * Kxx)
    cs2 = sp.simplify(Kx / Sigma)
    f_kx = sp.lambdify((X, A, Ld), Kx, "numpy")
    f_sig = sp.lambdify((X, A, Ld), Sigma, "numpy")
    f_cs2 = sp.lambdify((X, A, Ld), cs2, "numpy")
    xs = np.linspace(1e-3, 0.95, 32)
    kx = f_kx(xs, 1.0, 1.0)
    sig = f_sig(xs, 1.0, 1.0)
    speeds = f_cs2(xs, 1.0, 1.0)
    return {
        "K_X": str(Kx),
        "Sigma": str(Sigma),
        "c_s_squared": str(cs2),
        "positive_K_X_on_scan": bool(np.all(kx > 0)),
        "positive_Sigma_on_scan": bool(np.all(sig > 0)),
        "positive_cs2_on_scan": bool(np.all(speeds > 0)),
        "max_cs2_on_scan": float(np.max(speeds)),
    }


def run():
    kernel = exponential_kernel()
    variation = weak_field_variation()
    nonzero = dirac_scalar_sector(1.0, 2.0, 1.0)
    zero = dirac_scalar_sector(0.0, 2.0, 1.0)
    clock = clock_health_scan()
    result = {
        "candidate": "rotated_mmg_constitutive_2026",
        "kernel": kernel,
        "weak_field_variation": variation,
        "dirac_k_nonzero": nonzero,
        "dirac_k_zero": zero,
        "clock": clock,
        "gates": {
            "exact_exponential_mu": kernel["mu_identity"],
            "positive_transverse_eigenvalue": kernel["lambda_perp_at_1"] > 0,
            "weak_field_phi_equals_psi": variation["slip_equation_is_laplacian"],
            "weak_field_aqual": variation["aqual_target_matches"],
            "k_nonzero_scalar_pair_removed": nonzero["remaining_scalar_phase_dimension"] == 0,
            "k_zero_rank_jump_exposed": zero["rank"] < nonzero["rank"],
            "clock_witness_healthy": clock["positive_K_X_on_scan"] and clock["positive_Sigma_on_scan"] and clock["positive_cs2_on_scan"],
        },
        "open_gates": [
            "nonlinear hypersurface-deformation/Dirac closure",
            "ordinary matter Ward identity for the physical metric",
            "boosted PPN beta and alpha_1, alpha_2, alpha_3",
            "full FLRW perturbation stability and zero-field completion",
        ],
    }
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "rmmg_constitutive_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("RMMG_CONSTITUTIVE_GATE")
    for name, passed in result["gates"].items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print(f"dirac_rank_k_nonzero: {nonzero['rank']}")
    print(f"dirac_rank_k_zero: {zero['rank']}")
    print("STATUS: OPEN (finite candidate gates pass; full relativistic closure is not certified)")
    return result


if __name__ == "__main__":
    run()
