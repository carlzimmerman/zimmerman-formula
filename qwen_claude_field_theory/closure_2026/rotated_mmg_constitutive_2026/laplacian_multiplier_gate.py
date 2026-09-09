"""Laplacian-multiplier refinement for the auxiliary relay.

The refinement follows the mechanism of Sangtawee, De Felice & Karwan
(arXiv:2607.26031): multiply auxiliary constraints by spatial Laplacians of
their multipliers.  Local nonzero modes retain the same constraints, while
homogeneous multiplier functions drop out and are treated separately.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from auxiliary_relay_dirac import relay_dirac


def laplacian_scaled(k_value: float, u_value: float, a0_value: float):
    base = relay_dirac(k_value, u_value, a0_value)
    scale = k_value**2
    matrix = np.asarray(base["dirac_matrix"], dtype=float) * scale**2
    rank = int(np.linalg.matrix_rank(matrix, tol=1e-10))
    return {
        "k": k_value,
        "scale_from_laplacian": scale,
        "dirac_matrix": matrix.tolist(),
        "dirac_rank": rank,
        "determinant": float(np.linalg.det(matrix)),
        "nonzero_equivalent_to_direct_relay": bool(rank == base["dirac_rank"]),
        "homogeneous_constraints_vanish": bool(k_value == 0 and rank == 0),
    }


def run():
    local = laplacian_scaled(1.0, 2.0, 1.0)
    homogeneous = laplacian_scaled(0.0, 2.0, 1.0)
    result = {
        "candidate": "rotated_mmg_laplacian_multiplier_relay_2026",
        "local": local,
        "homogeneous": homogeneous,
        "gates": {
            "local_rank_retained": local["nonzero_equivalent_to_direct_relay"],
            "homogeneous_multiplier_sector_removed": homogeneous["homogeneous_constraints_vanish"],
            "rank_jump_exposed": homogeneous["dirac_rank"] < local["dirac_rank"],
        },
        "open": [
            "derive full nonlinear metric constraint algebra",
            "show matter Ward identity after clock/Stueckelberg completion",
            "derive FLRW tensor coefficients and c_T from the same Hamiltonian",
        ],
    }
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "laplacian_multiplier_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("LAPLACIAN_MULTIPLIER_RELAY_GATE")
    for name, passed in result["gates"].items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print(f"rank_k_nonzero: {local['dirac_rank']}")
    print(f"rank_k_zero: {homogeneous['dirac_rank']}")
    print("STATUS: OPEN (local constraints retained; FLRW/covariant closure remains)")


if __name__ == "__main__":
    run()
