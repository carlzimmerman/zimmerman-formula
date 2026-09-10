"""Action-level gate for a lapse-neutral normalized-acceleration parent.

This is a new architecture test, not a certification of a complete theory.
For a timelike clock T define s=sqrt(-dT.dT), n=-dT/s and
a_mu=n^nu nabla_nu n_mu.  The parent uses

    S_A = -C int sqrt(-g) s H(Y),
    Y = c^2 sqrt(a.a)/(a0*s),
    H(Y) = G(Y)-Y^2 = 2(1+Y) exp(-Y)-2.

In clock-unitary gauge (T=t, zero shift), sqrt(-g)s=sqrt(h) and
sqrt(a.a)/s=|D N|.  Therefore the displayed density is independent of
the lapse except through D_i N.  Adding the ordinary Einstein Y^2 piece
gives the exact G primitive and hence mu=1-exp(-Y).

The script derives that result, computes the actual h-stress anisotropy,
and builds a small Fourier Dirac matrix for the lapse primary constraint.
The latter is a local witness only; the full covariant clock/HDA analysis
remains open.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def kernel_identities():
    y = sp.symbols("y", positive=True)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    H = sp.simplify(G - y**2)
    mu_gr = sp.simplify(sp.diff(y**2, y) / (2 * y))
    mu_aux = sp.simplify(sp.diff(H, y) / (2 * y))
    mu_total = sp.simplify(sp.diff(G, y) / (2 * y))
    return {
        "G": str(G),
        "H": str(H),
        "mu_gr": str(mu_gr),
        "mu_aux": str(mu_aux),
        "mu_total": str(mu_total),
        "exact_exponential": bool(sp.simplify(mu_total - (1 - sp.exp(-y))) == 0),
        "auxiliary_cancels_GR_at_origin": bool(sp.limit(mu_gr + mu_aux, y, 0, dir="+") == 0),
        "high_acceleration_GR_recovery": bool(sp.limit(mu_total, y, sp.oo) == 1),
        "auxiliary_high_acceleration_flux_vanishes": bool(sp.limit(mu_aux, y, sp.oo) == 0),
    }


def unitary_gauge_reduction():
    """Verify the two algebraic unitary-gauge cancellations symbolically."""

    N, h, dN = sp.symbols("N h dN", positive=True)
    s = 1 / N
    lapse_prefactor = sp.simplify(N * sp.sqrt(h) * s)
    acceleration = dN / N
    normalized_acceleration = sp.simplify(acceleration / s)
    return {
        "sqrt_minus_g_times_s": str(lapse_prefactor),
        "a_over_s": str(normalized_acceleration),
        "prefactor_is_sqrt_h": bool(sp.simplify(lapse_prefactor - sp.sqrt(h)) == 0),
        "normalized_acceleration_is_DN": bool(sp.simplify(normalized_acceleration - dN) == 0),
    }


def lapse_euler_identity():
    """Compare the normalized parent with the old N-weighted form.

    Work on a one-dimensional positive-gradient branch and set c^2/a0=1.
    The new density is -G(N'), while the old covariant normalization is
    -N*G(N'/N).  The Euler operator is evaluated from the expression itself.
    """

    x = sp.symbols("x", real=True)
    k = sp.symbols("k", positive=True)
    N = sp.Function("N")(x)
    y_new = sp.diff(N, x)
    G = lambda y: y**2 + 2 * (1 + y) * sp.exp(-y) - 2

    L_new = -G(y_new)
    E_new = sp.simplify(sp.diff(L_new, N) - sp.diff(sp.diff(L_new, sp.diff(N, x)), x))

    y_old = sp.diff(N, x) / N
    L_old = -N * G(y_old)
    E_old = sp.simplify(sp.diff(L_old, N) - sp.diff(sp.diff(L_old, sp.diff(N, x)), x))

    affine = sp.exp(k * x)
    subs = {
        N: affine,
        sp.diff(N, x): sp.diff(affine, x),
        sp.diff(N, x, 2): sp.diff(affine, x, 2),
        sp.diff(N, x, 3): sp.diff(affine, x, 3),
    }
    new_affine = sp.factor(E_new.subs(subs))
    old_affine = sp.factor(E_old.subs(subs))
    target_flux = (1 - sp.exp(-sp.diff(N, x))) * sp.diff(N, x)
    target_euler = sp.simplify(2 * sp.diff(target_flux, x))
    return {
        "new_euler": str(E_new),
        "new_target_residual": str(sp.simplify(E_new - target_euler)),
        "new_affine_euler": str(new_affine),
        "old_affine_euler": str(old_affine),
        "new_exact_divergence": bool(sp.simplify(E_new - target_euler) == 0),
        "old_unit_slope_nonzero": bool(sp.simplify(old_affine.subs(k, 1)) != 0),
    }


def spatial_stress_anisotropy():
    """Compute the actual anisotropic h-stress of the covariant parent."""

    y, sp_, st = sp.symbols("y sp st", positive=True)
    Hf = lambda yy: 2 * (1 + yy) * sp.exp(-yy) - 2
    # h_ij=diag(exp(2*sp),exp(2*st),exp(2*st)); |D N|=y at flat point.
    L = -sp.exp(sp_ + 2 * st) * Hf(y * sp.exp(-sp_))
    e_parallel = sp.simplify(sp.diff(L, sp_).subs({sp_: 0, st: 0}))
    e_transverse = sp.simplify(sp.diff(L, st).subs({sp_: 0, st: 0}))
    raw_difference = sp.factor(e_parallel - e_transverse)
    # sigma_perp varies two equal directions, so compare per-direction
    # stresses: e_parallel - e_transverse/2 = y H'(y).
    difference = sp.factor(e_parallel - e_transverse / 2)
    return {
        "parallel_metric_euler": str(e_parallel),
        "transverse_metric_euler": str(e_transverse),
        "raw_parallel_minus_transverse": str(raw_difference),
        "anisotropy_per_direction": str(difference),
        "anisotropy_at_y1": float(difference.subs(y, 1).evalf()),
        "anisotropy_identically_zero": bool(difference == 0),
        "small_y_leading": str(sp.series(difference, y, 0, 5).removeO()),
    }


def lapse_dirac_matrix(k_value: float, y_value: float):
    """Build the primary/secondary lapse matrix from the Fourier constraint."""

    N, pN, k, rho = sp.symbols("N pN k rho", real=True)
    y = k * N
    mu = 1 - sp.exp(-y)
    C = sp.simplify(k**2 * mu * N - rho)
    primary = pN
    constraints = [primary, C]

    def pb(A, B):
        return sp.simplify(sp.diff(A, N) * sp.diff(B, pN) - sp.diff(A, pN) * sp.diff(B, N))

    M = sp.Matrix([[pb(A, B) for B in constraints] for A in constraints])
    N_value = y_value / k_value if k_value else 0.0
    source_value = (k_value**2) * (1 - np.exp(-y_value)) * N_value if k_value else 0.0
    subs = {k: float(k_value), N: float(N_value), rho: float(source_value), pN: 0.0}
    Mn = np.array(M.subs(subs).evalf(), dtype=float)
    rank = int(np.linalg.matrix_rank(Mn, tol=1e-10))
    return {
        "k": k_value,
        "y": y_value,
        "constraints": [str(c) for c in constraints],
        "matrix": Mn.tolist(),
        "rank": rank,
        "phase_dimension": 2,
        "remaining_phase_dimension": 2 - rank,
        "determinant": float(np.linalg.det(Mn)),
    }


def run():
    kernel = kernel_identities()
    reduction = unitary_gauge_reduction()
    lapse = lapse_euler_identity()
    stress = spatial_stress_anisotropy()
    local = lapse_dirac_matrix(1.0, 1.0)
    homogeneous = lapse_dirac_matrix(0.0, 0.0)
    checks = {
        "exact_exponential_kernel": kernel["exact_exponential"],
        "unitary_gauge_prefactor_reduces": reduction["prefactor_is_sqrt_h"],
        "unitary_gauge_acceleration_reduces": reduction["normalized_acceleration_is_DN"],
        "new_lapse_equation_is_exact_divergence": lapse["new_exact_divergence"],
        "old_normalized_form_is_not_same_equation": lapse["old_unit_slope_nonzero"],
        "local_lapse_matrix_rank_computed": local["rank"] == int(np.linalg.matrix_rank(np.asarray(local["matrix"]))),
        "homogeneous_rank_jump_exposed": homogeneous["rank"] < local["rank"],
    }
    result = {
        "candidate": "normalized_acceleration_parent_2026",
        "definitions": {
            "s": "sqrt(-g^{mu nu} d_mu T d_nu T)",
            "n": "-dT/s",
            "a": "n^nu nabla_nu n_mu",
            "Y": "c^2 sqrt(a_mu a^mu)/(a0*s)",
            "H": "G-Y^2=2*(1+Y)*exp(-Y)-2",
        },
        "kernel": kernel,
        "unitary_gauge_reduction": reduction,
        "lapse_variation": lapse,
        "spatial_stress": stress,
        "dirac_local": local,
        "dirac_homogeneous": homogeneous,
        "checks": checks,
        "status": "OPEN",
        "surviving_gate": "The normalized covariant density gives the exact exponential lapse flux without the prior N-weighted affine residual.",
        "obstruction_or_open_gate": "Its metric variation has nonzero finite-y anisotropic stress, so exact Phi=Psi and the full covariant Dirac/Ward/stability closure are not established.",
    }
    out = Path(__file__).parent / "run_001"
    out.mkdir(exist_ok=True)
    (out / "normalized_acceleration_action_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    assert all(checks.values())
    return result


if __name__ == "__main__":
    run()
