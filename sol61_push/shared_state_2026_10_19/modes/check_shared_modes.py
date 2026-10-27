#!/usr/bin/env python3
"""Bounded Rayleigh--Ritz controls for the explicitly closed two-fluid TF state.

No evolution, parameter fit, sampling, or finite-GP claim.  The mathematical
domain and tolerances are in contract.json.  Result path must be runner-owned.
"""

import argparse
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import eigh
from scipy.special import eval_jacobi, roots_legendre, spherical_jn


def gauss(n):
    z, w = roots_legendre(n)
    return (z + 1) / 2, w / 2


def profile(x):
    """f=sinc(pi*x), f'/x; Gauss nodes are strictly interior."""
    z = math.pi * x
    f = np.sinc(x)
    g = (z * np.cos(z) - np.sin(z)) / (math.pi * x**3)
    small = x < 1e-3
    g[small] = (
        -math.pi**2 / 3
        + math.pi**4 * x[small] ** 2 / 30
        - math.pi**6 * x[small] ** 4 / 840
    )
    return f, g


def basis(n, ell, x):
    """u_n=x^ell P_n^(0,ell+1/2)(2*x^2-1), L2(x^2 dx)-normalized.

    Returns u, u', h=-div(f grad(uY))/Y.  Evaluating the regular radial
    Laplacian in polynomial t=x^2 avoids cancellation of the angular barrier.
    """
    x = np.asarray(x)
    t = x**2
    z = 2 * t - 1
    f, fpx = profile(x)
    us, ds, hs = [], [], []
    for j in range(n):
        norm = math.sqrt(4 * j + 2 * ell + 3)
        p = norm * eval_jacobi(j, 0, ell + 0.5, z)
        pt = np.zeros_like(x)
        ptt = np.zeros_like(x)
        if j >= 1:
            pt = norm * (j + ell + 1.5) * eval_jacobi(
                j - 1, 1, ell + 1.5, z
            )
        if j >= 2:
            ptt = norm * (j + ell + 1.5) * (j + ell + 2.5) * eval_jacobi(
                j - 2, 2, ell + 2.5, z
            )
        u = x**ell * p
        d = x ** (ell - 1) * (ell * p + 2 * t * pt)
        h = -x**ell * (
            f * ((4 * ell + 6) * pt + 4 * t * ptt)
            + fpx * (ell * p + 2 * t * pt)
        )
        us.append(u)
        ds.append(d)
        hs.append(h)
    return np.stack(us, axis=-1), np.stack(ds, axis=-1), np.stack(hs, axis=-1)


def matrices(n, ell, nq):
    x, w = gauss(nq)
    u, d, h = basis(n, ell, x)
    f, _ = profile(x)
    kinetic = d.T @ ((w * f * x**2)[:, None] * d)
    kinetic += ell * (ell + 1) * u.T @ ((w * f)[:, None] * u)
    density = u.T @ ((w * x**2)[:, None] * u)
    # Evaluate the exact multipole Green integral with separate smooth
    # quadratures on [0,x] and [x,1].  A one-grid kernel would converge slowly
    # across its diagonal kink and would contaminate the translation check.
    z, wz = gauss(nq)
    inside = x[:, None] * z[None, :]
    outside = x[:, None] + (1 - x[:, None]) * z[None, :]
    hi = basis(n, ell, inside)[2]
    ho = basis(n, ell, outside)[2]
    left = x[:, None] * np.einsum(
        "j,ij,ijk->ik", wz, inside ** (ell + 2), hi
    )
    right = (1 - x[:, None]) * np.einsum(
        "j,ij,ijk->ik", wz, outside ** (1 - ell), ho
    )
    v = -math.pi**2 / (2 * ell + 1) * (
        x[:, None] ** (-ell - 1) * left + x[:, None] ** ell * right
    )
    stiffness = h.T @ ((w * x**2)[:, None] * (h + v))
    asym = float(np.max(np.abs(stiffness - stiffness.T)))
    stiffness = (stiffness + stiffness.T) / 2
    return x, w, u, d, h, kinetic, density, stiffness, asym


def exact_controls():
    rows = []
    for kd, kb, rho, eta, vd, vb in [
        (Q(1), Q(1), Q(3), Q(1, 4), Q(2), Q(-3)),
        (Q(1, 3), Q(7, 2), Q(5, 2), Q(-1, 5), Q(-2, 3), Q(4)),
        (Q(11), Q(2, 7), Q(2), Q(1, 9), Q(1, 3), Q(2, 5)),
    ]:
        a = kb / (kd + kb)
        b = kd / (kd + kb)
        k = kd * kb / (kd + kb)
        rd, rb = a * rho + eta, b * rho - eta
        assert kd * rd**2 + kb * rb**2 == k * rho**2 + k * eta**2 / (a * b)
        v, zeta = a * vd + b * vb, vd - vb
        assert a * vd**2 + b * vb**2 == v**2 + a * b * zeta**2
        assert a * kd == b * kb == k
        assert rd + rb == rho
        rows.append({"Kd": str(kd), "Kb": str(kb), "a": str(a), "b": str(b)})
    return rows


def relative_spectrum(n, nq):
    x, w, u, _, _, kinetic, density, _, _ = matrices(n, 1, nq)
    assert np.max(np.abs(density - np.eye(n))) < 2e-11
    val, vec = eigh(kinetic, density)
    assert val[0] > 0
    phi = u @ vec
    j = phi.T @ (w * x**3)
    strength = math.pi**2 / 3 * val * j**2
    static = float(np.sum(strength / val))
    # The source xY10 is exactly present in every retained space: both the
    # first moment and static moment follow from independent completeness.
    assert abs(float(np.sum(strength)) - 1) < 2e-10
    assert abs(static - math.pi**2 / 15) < 2e-11
    assert val[0] < math.pi**2 / 6  # rigid displacement variational bound
    return {
        "basis_size": n,
        "quadrature_order": nq,
        "eigenvalues_GM_over_R3": val[:6].tolist(),
        "dipole_first_moment_fractions": strength[:6].tolist(),
        "first_moment_fraction_all_retained": float(np.sum(strength)),
        "static_inverse_moment_all_retained": static,
        "mass_matrix_max_error": float(np.max(np.abs(density - np.eye(n)))),
    }


def total_spectrum(n, nq):
    x, w, _, _, h, kinetic, _, stiffness, asym = matrices(n, 1, nq)
    # Exact total translation is n=0.  Remove it by kinetic orthogonality,
    # without altering or suppressing its raw stiffness residual.
    project = np.zeros((n, n - 1))
    project[1:, :] = np.eye(n - 1)
    project[0, :] = -kinetic[0, 1:] / kinetic[0, 0]
    vals, vecs = eigh(project.T @ stiffness @ project, project.T @ kinetic @ project)
    assert np.max(np.abs(stiffness[0, :])) < 5e-9
    assert asym < 5e-8
    assert vals[0] > 0
    vecs = project @ vecs
    hmodes = h @ vecs
    # COM orthogonality equals the zero physical integrated mass dipole.
    dipoles = hmodes.T @ (w * x**3)
    assert np.max(np.abs(dipoles)) < 5e-10
    # Finite-k Fourier source along z: -i sqrt(12*pi) rho_c R^2 int x^2 h j1.
    # vecs have unit dimensionless kinetic norm.  Report source |sigma_k|^2
    # divided by rho_c R and polarization susceptibility times 4*pi*G/V.
    # For one object, V=4*pi*R^3/3; omega²=GM/R³ * lambda.
    source_rows = []
    for q in [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]:
        integral = hmodes.T @ (w * x**2 * spherical_jn(1, q * x))
        sq = 12 * math.pi * integral**2
        # 4*pi*G * [sum |sigma|²/(k² omega²)]/V = 9*pi²*sum I²/(q² lambda).
        normalized = float(9 * math.pi**2 * np.sum(integral**2 / vals) / q**2)
        source_rows.append({
            "kR": q,
            "sigma_squared_over_rho_c_R_first_three": sq[:3].tolist(),
            "4piG_chiP_over_object_volume": normalized,
        })
    return {
        "basis_size": n,
        "quadrature_order": nq,
        "positive_eigenvalues_GM_over_R3": vals[:6].tolist(),
        "translation_raw_stiffness_max": float(np.max(np.abs(stiffness[0, :]))),
        "stiffness_raw_asymmetry_max": asym,
        "positive_mode_mass_dipole_max": float(np.max(np.abs(dipoles))),
        "source_rows": source_rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    results = {
        "assertion_tested": "Exact two-fluid channel algebra and finite l=1 radial Rayleigh--Ritz spectra and mass-source overlaps for the declared common-profile n=1 TF control.",
        "software": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__},
        "exact_controls": exact_controls(),
        "relative": [relative_spectrum(n, 128) for n in [6, 10, 14, 18]],
        "total": [total_spectrum(n, 128) for n in [6, 10, 14]],
        "quadrature_control_relative": relative_spectrum(14, 192),
        "quadrature_control_total": total_spectrum(14, 192),
        "known_coefficients": {
            "rigid_relative_rayleigh_upper_bound": math.pi**2 / 6,
            "relative_static_sum": math.pi**2 / 15,
            "equal_fraction_fixed_profile_max_Dd_over_MR": (math.pi**2 - 4) / (4 * math.pi**2),
        },
        "outcome": "conditional numerical finite controls, with exact channel identities proved in SHARED_MODES.md",
    }
    # Cross-resolution agreement for retained low modes; this is convergence
    # evidence, not certified eigenvalue error bars or a completeness theorem.
    for branch, key in [("relative", "eigenvalues_GM_over_R3"), ("total", "positive_eigenvalues_GM_over_R3")]:
        final = np.array(results[branch][-1][key][:3])
        prev = np.array(results[branch][-2][key][:3])
        results[branch][-1]["first_three_change_from_previous_basis"] = (final - prev).tolist()
        quad = np.array(results["quadrature_control_" + branch][key][:3])
        # Relative quad comparison is n=14, while final spectrum is n=18.
        same_n = results[branch][-2] if branch == "relative" else results[branch][-1]
        assert np.max(np.abs(quad - np.array(same_n[key][:3]))) < 1e-8
    out = Path(args.result)
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "relative_first_six": results["relative"][-1]["eigenvalues_GM_over_R3"],
        "total_positive_first_six": results["total"][-1]["positive_eigenvalues_GM_over_R3"],
        "relative_strength_first_six": results["relative"][-1]["dipole_first_moment_fractions"],
        "result_path": str(out),
        "status": "all finite assertions passed",
    }, indent=2))


if __name__ == "__main__":
    main()
