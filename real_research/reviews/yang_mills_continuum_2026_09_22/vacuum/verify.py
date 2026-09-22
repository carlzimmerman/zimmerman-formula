#!/usr/bin/env python3
"""Bounded normalization checks; not certified lower bounds for YM."""
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal


def character_spectrum(x, b, cutoff):
    n = np.arange(cutoff, dtype=float)
    diagonal = 0.5 * x * n * (n + 2) + b / x
    off_diagonal = np.full(cutoff - 1, -b / (2 * x))
    return eigh_tridiagonal(diagonal, off_diagonal,
                            select="i", select_range=(0, 2),
                            eigvals_only=True)


def radial_spectrum(x, b, grid):
    # Independent second-order finite difference of equation (8), Dirichlet.
    h = math.pi / (grid + 1)
    theta = h * np.arange(1, grid + 1)
    diagonal = x / h**2 + (b / x) * (1 - np.cos(theta)) - x / 2
    off_diagonal = np.full(grid - 1, -x / (2 * h**2))
    return eigh_tridiagonal(diagonal, off_diagonal,
                            select="i", select_range=(0, 2),
                            eigvals_only=True)


def main():
    checks = []
    plaquette = []
    for x in (1.0, 0.25, 0.1, 0.04, 0.01, 0.002):
        b = 2.0
        e200 = character_spectrum(x, b, 200)
        e400 = character_spectrum(x, b, 400)
        cutoff_difference = float(np.max(np.abs(e200 - e400)))
        assert cutoff_difference < 1e-9
        radial = radial_spectrum(x, b, 8192)
        radial_difference = float(np.max(np.abs(radial - e400)))
        assert radial_difference < 6e-4
        gap = float(e400[1] - e400[0])
        curvature_trace = 6 - (4 / x) * (2 * b / x - e400[0])
        assert curvature_trace <= 6 - 4 * b / x**2 + 1e-8
        if x * x < 2 * b / 3:
            assert curvature_trace < 0
        plaquette.append({
            "x": x, "b": b, "eigenvalues_ritz": e400.tolist(),
            "gap_ritz": gap, "limiting_gap": 2 * math.sqrt(b),
            "gap_over_limit": gap / (2 * math.sqrt(b)),
            "cutoff_200_vs_400_max_difference": cutoff_difference,
            "radial_8192_vs_character_max_difference": radial_difference,
            "curvature_trace_from_ritz_ground_energy": float(curvature_trace),
            "analytic_curvature_trace_upper_bound": 6 - 4 * b / x**2,
        })
    electric = character_spectrum(1.0, 0.0, 10)
    assert np.allclose(electric, (0, 1.5, 4.0), atol=1e-14)
    assert abs(plaquette[-1]["gap_over_limit"] - 1) < 0.001
    checks.extend(["electric Casimir normalization", "character cutoff stability",
                   "independent radial finite-difference normalization",
                   "negative curvature trace at small x",
                   "single-plaquette semiclassical limiting-gap benchmark"])

    chains = []
    x = 0.1
    r = 3  # SU(2) adjoint dimension; ratios do not depend on r.
    for length in (1, 2, 4, 8, 16, 32, 64, 128):
        kk = np.arange(1, length + 1, dtype=float)
        jj = np.arange(1, length + 1, dtype=float)
        vectors = np.sqrt(2 / (length + 1)) * np.sin(
            math.pi * np.outer(jj, kk) / (length + 1))
        omega = 2 * np.sin(kk * math.pi / (2 * (length + 1)))
        qmat = (vectors * omega) @ vectors.T
        kmat = np.diag(np.full(length, 2.0))
        if length > 1:
            kmat += np.diag(np.full(length - 1, -1.0), 1)
            kmat += np.diag(np.full(length - 1, -1.0), -1)
        assert np.max(np.abs(qmat @ qmat - kmat)) < 1e-12
        assert np.max(np.abs(vectors.T @ vectors - np.eye(length))) < 1e-12
        qdiag = np.diag(qmat)
        assert qdiag.min() >= 1 - 1e-12
        mode = vectors[:, 0]
        w = omega[0]
        variance = r * x**2 / (2 * w**2)
        conditional_variance_sum = r * x**2 * np.sum(
            mode**2 / (qdiag * w) - mode**4 / (2 * qdiag**2))
        tensorization_ratio = variance / conditional_variance_sum
        assert tensorization_ratio >= 1 / (2 * w) - 1e-12
        chains.append({
            "length": length, "x": x, "adjoint_dimension": r,
            "min_conditional_poincare_eigenvalue": float(2*qdiag.min()/x),
            "full_gap_exact_formula": float(w),
            "singlet_gap_exact_formula": float(2*w),
            "singlet_poincare_eigenvalue_exact_formula": float(4*w/x),
            "quadratic_witness_tensorization_ratio": float(tensorization_ratio),
            "proved_ratio_lower_bound": float(1/(2*w)),
        })
    checks.extend(["Dirichlet square-root matrix identity and sine normalization",
                   "uniform conditional gap floor",
                   "quadratic singlet witness conditional-variance formula bound"])
    result = {
        "claim": "Finite numerical benchmarks of four analytic vacuum-route lemmas",
        "arithmetic": "IEEE float64; no interval enclosure",
        "checks": checks,
        "single_plaquette": plaquette,
        "oscillator_chains": chains,
        "non_claims": [
            "Ritz gaps are not certified lower bounds for infinite operators.",
            "Cutoff stability is not a theorem of convergence.",
            "Gaussian oscillator chains are not the interacting SU(N) lattice model.",
            "No many-volume Yang-Mills or continuum mass-gap estimate is proved by this run.",
        ],
    }
    output = Path(__file__).parent / "run" / "results.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks_passed": len(checks),
                      "smallest_x_gap_ratio": plaquette[-1]["gap_over_limit"],
                      "largest_chain": chains[-1]}, indent=2))


if __name__ == "__main__":
    main()
