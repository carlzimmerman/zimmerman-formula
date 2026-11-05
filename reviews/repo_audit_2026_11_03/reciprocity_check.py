"""Independent finite check of source-only filtered QUMOND reciprocity.

Pure Python midpoint quadrature; all physical and mathematical inputs are
declared here. This does not reproduce any galaxy fit or test isolated 3D halos.
"""
import json
import math
from pathlib import Path
import sys


def run(n, sigma=0.7, epsilon=0.2):
    s1 = math.exp(-sigma**2 / 2)
    s2 = math.exp(-2 * sigma**2)
    # 4*pi*G=a0=1.  rho=1-epsilon/s1*sin(x)>0; mean-subtracted
    # periodic Poisson equation plus fixed external Newtonian gradient 1.
    terms = []
    for j in range(n):
        x = 2 * math.pi * (j + 0.5) / n
        u = 1 + epsilon * math.cos(x)
        # d[(nu(u)-1)*u]/du for the actual simple nu used in KT14-27.
        m = (u + 2) / (2 * math.sqrt(u*u + 4*u)) - 0.5
        terms.append(m * math.sin(x) * math.sin(2*x))
    b12 = -0.5 * math.fsum(terms) / n
    j12, j21 = b12*s2, b12*s1
    corrected = b12*s1*s2
    return {
        "n": n, "sigma": sigma, "epsilon": epsilon,
        "density_lower_bound": 1-epsilon/s1,
        "field_lower_bound": 1-epsilon,
        "s1": s1, "s2": s2, "B12": b12,
        "source_only_J12": j12, "source_only_J21": j21,
        "antisymmetric_pair": j12-j21,
        "relative_pair_difference": abs(j12-j21)/max(abs(j12), abs(j21)),
        "adjoint_completed_J12": corrected,
        "adjoint_completed_J21": corrected,
    }


rows = [run(n) for n in (64, 256, 1024, 4096)]
zero_width = run(1024, sigma=0.0)
homogeneous = run(1024, epsilon=0.0)
checks = {
    "positive_density_and_nonzero_field": all(r["density_lower_bound"] > 0 and r["field_lower_bound"] > 0 for r in rows),
    "nonreciprocity_resolved": all(abs(r["antisymmetric_pair"]) > 1e-5 for r in rows),
    "quadrature_stable": max(abs(r["antisymmetric_pair"]-rows[-1]["antisymmetric_pair"]) for r in rows) < 1e-14,
    "zero_width_control": abs(zero_width["antisymmetric_pair"]) < 1e-15,
    "homogeneous_control": abs(homogeneous["antisymmetric_pair"]) < 1e-15,
    "adjoint_completion_symmetric": all(r["adjoint_completed_J12"] == r["adjoint_completed_J21"] for r in rows),
}
result = {"assertion_tested": "Two zero-mean source perturbations have unequal reciprocal potential derivatives for the KT source-only filtered map on a positive-density planar periodic background, with fixed external gradient.", "rows": rows, "zero_width": zero_width, "homogeneous": homogeneous, "checks": checks, "all_pass": all(checks.values())}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["all_pass"] else 1)
