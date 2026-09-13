#!/usr/bin/env python3
"""Independent consistency check of the AeST finite-k decoupling claims.

Rebuild the K, Omega, and B matrices used by B_decoupling_dispersion.py and
derive the low-frequency Schur complement.  The result is compared with the
ghost-band ansatz used by the FLRW gate.  No numerical sign target is inserted:
the sign is evaluated from the derived expression under K2,Q0,K_B>0.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    K2, KB, Q0, k, w = sp.symbols("K2 K_B Q0 k omega", positive=True, real=True)
    # Matrices reconstructed from B_decoupling_dispersion.py, not imported.
    K = sp.Matrix([[4 * K2, 0], [0, 2 * KB * k**2]])
    Om = 2 * (2 - KB) * k**2 * sp.Matrix([[1, Q0], [Q0, Q0**2]])
    B = sp.Matrix([[0, 0], [2 * k**2 * (2 - KB), 2 * Q0 * k**2 * (2 - KB)]])
    M = -w**2 * K + sp.I * w * (B - B.T) + Om
    Mff, Mfa, Maf, Maa = [M[i, j] for i, j in ((0, 0), (0, 1), (1, 0), (1, 1))]
    schur = sp.factor(Mff - Mfa * Maf / Maa)
    W = sp.symbols("W", real=True)
    # Replace omega^2 by W after simplifying the even dispersion expression.
    schur_W = sp.factor(schur.subs(w**2, W))
    K_eff = sp.factor(-sp.diff(schur_W, W).subs(W, 0))
    Omega_eff = sp.factor(schur_W.subs(W, 0))
    claimed = sp.symbols("A_Y", positive=True) * (
        sp.symbols("lam_s", positive=True) * k**2
        - (1 + sp.symbols("lam_s", positive=True)) * sp.symbols("mu", positive=True) ** 2
    ) / (sp.symbols("lam_s", positive=True) * k**2 + sp.symbols("mu", positive=True) ** 2)
    positivity_witness = sp.simplify(K_eff.subs({K2: 1, Q0: 1, k: 1}))
    zero_gradient = sp.simplify(Omega_eff)
    checks = {
        "schur_computation_is_finite": bool(schur.is_rational_function(w)),
        "derived_goldstone_potential_vanishes": bool(zero_gradient == 0),
        "derived_kinetic_has_no_negative_band": bool(sp.simplify(
            K_eff - (4 * K2 + 4 * k**2 / Q0**2)
        ) == 0),
        "derived_kinetic_positive_at_positive_witness": bool(positivity_witness > 0),
        "claimed_ansatz_is_not_the_derived_schur_complement": bool(sp.simplify(
            K_eff - claimed
        ) != 0),
    }
    print("INDEPENDENT AeST DECOUPLING CONSISTENCY CHECK")
    print("Schur complement M_eff =", schur)
    print("Omega_eff =", Omega_eff)
    print("derived K_eff =", K_eff)
    print("positive witness K_eff(K2=Q0=k=1) =", positivity_witness)
    print("ghost-band ansatz used elsewhere =", claimed)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    payload = {
        "status": "DECoupling_GHOST_BAND_MISMATCH" if all(checks.values()) else "INCONCLUSIVE",
        "checks": checks,
        "derived_K_eff": str(K_eff),
        "derived_Omega_eff": str(Omega_eff),
        "claimed_K_eff_ansatz": str(claimed),
        "interpretation": (
            "The exact decoupling matrices used by the repository derive a positive "
            "low-frequency kinetic coefficient for K2,Q0>0; the separate ghost-band "
            "ansatz is not their Schur complement. A full metric reduction is still "
            "required, but the current finite-k ghost/rescue claim is not certified."
        ),
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
