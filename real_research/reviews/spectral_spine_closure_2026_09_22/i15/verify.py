#!/usr/bin/env python3
"""Bounded checks of the actual character Hamiltonians, not a spectral proof.

All finite spectra below are Ritz truncations. The untruncated lower bounds
are proved in PROOF.md. No fitted, random, or synthetic pass flags are used.
"""
import argparse
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

import numpy as np
from scipy.linalg import eigvalsh


def casimir(labels):
    n = len(labels) + 1
    return sum(
        Q(min(i, j) * (n - max(i, j)), 2 * n) * labels[i - 1]
        * (labels[j - 1] + 2)
        for i in range(1, n) for j in range(1, n)
    )


def character_matrix(n, cutoff, x, b):
    """Multiplication by Re chi_f/N with characters orthonormal in Haar norm."""
    if n == 2:
        labels = [(k,) for k in range(cutoff + 1)]
        fusion = lambda a: [(a[0] + 1,), (a[0] - 1,)]
    elif n == 3:
        labels = [(p, q) for p in range(cutoff + 1)
                  for q in range(cutoff + 1 - p)]
        fusion = lambda a: [(a[0] + 1, a[1]),
                            (a[0] - 1, a[1] + 1),
                            (a[0], a[1] - 1)]
    else:
        raise ValueError("Numerical character tests only implement SU(2), SU(3)")
    where = {a: i for i, a in enumerate(labels)}
    f = np.zeros((len(labels), len(labels)))
    for column, a in enumerate(labels):
        for target in fusion(a):
            if target in where:
                f[where[target], column] += 1
    t = (f + f.T) / (2 * n)
    c = np.array([float(casimir(a)) for a in labels])
    h = np.diag(2 * x * c + b / x) - (b / x) * t
    return labels, t, h, c


def run():
    checks = []

    def check(name, predicate, **data):
        checks.append({"name": name, "passed": bool(predicate), **data})

    casimir_rows = []
    for n in range(2, 9):
        family = [a for a in product(range(3), repeat=n - 1) if any(a)]
        values = [casimir(a) for a in family]
        minimum = min(values)
        cf = Q(n * n - 1, 2 * n)
        check(f"exact Casimir minimum N={n}", minimum == cf,
              tested=len(family), minimum=str(minimum), expected=str(cf))
        casimir_rows.append({"N": n, "count": len(family), "minimum": str(minimum)})

    rows = []
    for n in (2, 3):
        for x in (2., 4., 8.):
            for b in sorted({2., float(n), 2. * n}):
                spectra = []
                for cutoff in (8, 12, 16):
                    labels, t, h, c = character_matrix(n, cutoff, x, b)
                    spectrum = eigvalsh(h, subset_by_index=(0, 1))
                    gap = float(spectrum[1] - spectrum[0])
                    cf = Q(n * n - 1, 2 * n)
                    lower = 2 * x * float(cf) - b / x
                    original_lower = x * (n * n - 1) / n - 2 * n / x
                    norm_t = float(np.max(np.abs(eigvalsh(t))))
                    electric_vacuum_residual = float(np.linalg.norm(h[:, 0] - h[0, 0] * np.eye(len(h))[:, 0]))
                    check(f"character normalization N={n},x={x},b={b},K={cutoff}",
                          np.max(np.abs(h-h.T)) == 0 and norm_t <= 1 + 1e-12
                          and t[0, 0] == 0 and c[0] == 0,
                          norm_T=norm_t)
                    check(f"min-max benchmark N={n},x={x},b={b},K={cutoff}",
                          spectrum[0] <= b/x + 1e-10
                          and spectrum[1] >= 2*x*float(cf) - 1e-10
                          and gap >= lower - 1e-10
                          and lower >= original_lower - 1e-10,
                          E0=float(spectrum[0]), E1=float(spectrum[1]),
                          gap=gap, proved_lower=lower)
                    check(f"bare vacuum not an eigenvector N={n},x={x},b={b},K={cutoff}",
                          electric_vacuum_residual > 1e-6,
                          residual=electric_vacuum_residual)
                    spectra.append(spectrum)
                error = float(np.max(np.abs(spectra[-1] - spectra[-2])))
                check(f"cutoff convergence N={n},x={x},b={b}", error < 1e-9,
                      last_two_level_max_difference=error)
                rows.append({"N": n, "x": x, "b": b,
                             "E0": float(spectra[-1][0]), "E1": float(spectra[-1][1]),
                             "gap": float(spectra[-1][1]-spectra[-1][0]),
                             "analytic_lower": lower, "original_lower": original_lower,
                             "cutoff_difference": error})

    # Exact two-state principal minor: subtracting the bare-vacuum expectation
    # produces [[0,-t],[-t,e]], with determinant -t²<0. It cannot be a positive
    # gap Hamiltonian. This is a counterexample to that identification, not to
    # the actual interacting spectral-gap theorem.
    for x in (Q(2), Q(8)):
        electric_loop, t = 3*x/2, Q(1)/x  # SU(2), repository b=2
        determinant = -t*t
        epsilon = t/electric_loop
        unnormalized_work = electric_loop*epsilon**2 - 2*t*epsilon
        check(f"bare-vacuum subtraction fails x={x}",
              determinant < 0 and unnormalized_work < 0,
              determinant=str(determinant), witness_work=str(unnormalized_work))

    return {"claim": "I15 single-plaquette character-basis benchmarks",
            "arithmetic": "Fractions exact for Casimirs and 2-state witnesses; binary64 spectra",
            "checks": checks, "casimir_family": casimir_rows, "spectra": rows,
            "passed": all(c["passed"] for c in checks),
            "non_claims": ["No finite cutoff establishes an infinite-matrix lower gap bound",
                           "No numerical value for the lattice-wide strong-coupling threshold",
                           "No continuum or scalar-framework identification"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    failed = [c for c in result["checks"] if not c["passed"]]
    print(f"{len(result['checks'])-len(failed)}/{len(result['checks'])} checks passed")
    for row in result["spectra"]:
        print(row)
    if failed:
        print(json.dumps(failed, indent=2))
        raise SystemExit(1)
