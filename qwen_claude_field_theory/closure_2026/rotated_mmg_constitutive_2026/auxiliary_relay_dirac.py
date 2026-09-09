"""Primary/secondary Dirac chain for a genuinely auxiliary relay version.

Unlike the pedagogical p^2 surrogate, this first-order action has no scalar
kinetic term.  The primary momenta vanish, and their preservation generates
the constitutive and slip elliptic equations.  The computed Hessian decides
whether the pair is second class mode by mode.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import sympy as sp


def poisson(A, B, coords, momenta):
    return sp.simplify(
        sum(
            sp.diff(A, q) * sp.diff(B, p) - sp.diff(A, p) * sp.diff(B, q)
            for q, p in zip(coords, momenta)
        )
    )


def relay_dirac(k_value: float, u_value: float, a0_value: float):
    u, r, pu, pr = sp.symbols("u r pu pr", real=True)
    k, a0, source = sp.symbols("k a0 source", positive=True)
    y = k * u / (2 * a0)
    G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    # V is the Hamiltonian potential for one constitutive Fourier mode.
    # Its u derivative is k^2*mu(y)*u; source enters through the same lapse
    # constraint in the full matter-coupled action.
    V = 2 * a0**2 * G + sp.Rational(1, 2) * k**2 * r**2 - source * u
    H = V
    primary = [pu, pr]
    secondary = [
        sp.simplify(poisson(c, H, (u, r), (pu, pr))) for c in primary
    ]
    constraints = primary + secondary
    M = sp.Matrix(
        [
            [poisson(A, B, (u, r), (pu, pr)) for B in constraints]
            for A in constraints
        ]
    )
    matched_source = float(
        (k_value**2)
        * (1.0 - np.exp(-k_value * u_value / (2.0 * a0_value)))
        * u_value
    )
    subs = {
        k: k_value,
        a0: a0_value,
        u: u_value,
        r: 0.0,
        pu: 0.0,
        pr: 0.0,
        source: matched_source,
    }
    Mn = np.array(M.subs(subs).evalf(), dtype=float)
    rank = int(np.linalg.matrix_rank(Mn, tol=1e-10))
    det = float(np.linalg.det(Mn))

    lm, lr = sp.symbols("lambda_u lambda_r", real=True)
    H_total = H + lm * pu + lr * pr
    preservation = [
        sp.simplify(poisson(c, H_total, (u, r), (pu, pr)))
        for c in secondary
    ]
    Bn = np.array(
        [
            [float(sp.diff(eq, lam).subs(subs).evalf()) for lam in (lm, lr)]
            for eq in preservation
        ],
        dtype=float,
    )
    An = np.array(
        [float(eq.subs(subs).subs({lm: 0.0, lr: 0.0}).evalf()) for eq in preservation]
    )
    multiplier_rank = int(np.linalg.matrix_rank(Bn, tol=1e-10))
    multiplier = np.linalg.solve(Bn, -An).tolist() if multiplier_rank == len(Bn) else None
    return {
        "k": k_value,
        "primary_constraints": [str(c) for c in primary],
        "secondary_constraints": [str(c) for c in secondary],
        "dirac_matrix": Mn.tolist(),
        "dirac_rank": rank,
        "dirac_determinant": det,
        "phase_space_dimension": 4,
        "remaining_scalar_phase_dimension": 4 - rank,
        "preservation_multiplier_matrix": Bn.tolist(),
        "preservation_multiplier_rank": multiplier_rank,
        "preservation_multiplier": multiplier,
        "preservation_status": "uniquely_fixed" if multiplier is not None else "rank_deficient",
    }


def run():
    nonzero = relay_dirac(1.0, 2.0, 1.0)
    zero = relay_dirac(0.0, 2.0, 1.0)
    result = {
        "candidate": "rotated_mmg_auxiliary_relay_2026",
        "nonzero_mode": nonzero,
        "zero_mode": zero,
        "gates": {
            "nonzero_mode_is_second_class": nonzero["dirac_rank"] == len(nonzero["dirac_matrix"]),
            "nonzero_mode_has_no_scalar_phase_dimension": nonzero["remaining_scalar_phase_dimension"] == 0,
            "zero_mode_rank_jump_exposed": zero["dirac_rank"] < nonzero["dirac_rank"],
            "nonzero_multipliers_fixed": nonzero["preservation_status"] == "uniquely_fixed",
            "zero_mode_multipliers_not_falsely_fixed": zero["preservation_status"] == "rank_deficient",
        },
        "scope": "auxiliary relay Dirac chain; full metric constraint algebra remains open",
    }
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "auxiliary_relay_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("AUXILIARY_RELAY_DIRAC_GATE")
    for name, passed in result["gates"].items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    print(f"dirac_rank_k_nonzero: {nonzero['dirac_rank']}")
    print(f"dirac_rank_k_zero: {zero['dirac_rank']}")
    print("STATUS: OPEN (auxiliary local chain passes; full metric algebra remains)")
    return result


if __name__ == "__main__":
    run()
