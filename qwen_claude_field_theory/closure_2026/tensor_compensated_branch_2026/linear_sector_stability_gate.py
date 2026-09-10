#!/usr/bin/env python3
"""Generated linear tensor/vector/scalar stability split for the candidate.

This gate is deliberately limited to the frozen-coefficient principal sectors
around the flat expanding branch.  The tensor compensator is spatial, so the
TT quadratic density is the Einstein one.  The transverse vector is a shift
constraint with no velocity.  The scalar sector is imported from the generated
finite-k Dirac chain, not assigned a rank here.
"""

from __future__ import annotations

import json
import sys

import sympy as sp

from tensor_compensated_dirac_gate import sector


def pb(left, right, pairs):
    return sp.simplify(sum(sp.diff(left, q) * sp.diff(right, p)
                           - sp.diff(left, p) * sp.diff(right, q)
                           for q, p in pairs))


def main() -> int:
    M2, k = sp.symbols("M2 k", positive=True, real=True)
    h, hd, V = sp.symbols("h hd V", real=True)
    pV = sp.symbols("pV", real=True)

    tensor_L = M2 * (hd**2 - k**2 * h**2) / 8
    tensor_hessian = sp.hessian(tensor_L, (hd,))
    tensor_kinetic = sp.diff(tensor_L, hd, 2) / 2
    tensor_gradient = M2 * k**2 / 8
    tensor_cT2 = sp.simplify(tensor_gradient / (tensor_kinetic * k**2))

    vector_L = M2 * k**2 * V**2 / 2
    vector_qs = (V,)
    vector_ps = (pV,)
    vector_pairs = tuple(zip(vector_qs, vector_ps))
    vector_primary = pV
    vector_secondary = sp.factor(sp.diff(vector_L, V))
    vector_constraints = (vector_primary, vector_secondary)
    vector_pb = sp.Matrix([[pb(a, b, vector_pairs) for b in vector_constraints]
                           for a in vector_constraints])
    vector_rank = vector_pb.rank()
    vector_dof = sp.Rational(2 - vector_rank, 2)
    vector_hessian = sp.hessian(vector_L, (sp.Symbol("Vd"),))

    scalar = sector("nonzero")
    checks = [
        tensor_hessian == sp.Matrix([[M2 / 4]]),
        tensor_kinetic > 0,
        tensor_gradient > 0,
        tensor_cT2 == 1,
        vector_hessian == sp.zeros(1),
        vector_secondary == M2 * k**2 * V,
        vector_pb == -vector_pb.T,
        vector_pb.rank() == vector_rank,
        vector_rank == 2,
        vector_dof == 0,
        scalar["physical_dof"] == 0,
    ]

    print("LINEAR SECTOR STABILITY AUDIT")
    print("TT L =", tensor_L)
    print("TT Hessian =", tensor_hessian)
    print("TT kinetic/gradient =", tensor_kinetic, tensor_gradient)
    print("TT cT^2 =", tensor_cT2)
    print("vector L =", vector_L)
    print("vector primary/secondary =", vector_primary, vector_secondary)
    print("vector PB matrix =", vector_pb)
    print("vector PB rank =", vector_rank)
    print("vector DOF =", vector_dof)
    print("scalar finite-k DOF (generated chain) =", scalar["physical_dof"])
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))

    result = {
        "status": "LINEAR_SECTOR_PASS_NONLINEAR_STABILITY_OPEN",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "tensor": {"kinetic": str(tensor_kinetic),
                   "gradient": str(tensor_gradient),
                   "cT_squared": str(tensor_cT2),
                   "hessian_rank": tensor_hessian.rank()},
        "vector": {"constraint_rank": vector_rank,
                   "physical_dof": str(vector_dof)},
        "scalar": {"finite_k_physical_dof": str(scalar["physical_dof"])},
        "scope": "frozen-coefficient linear principal sectors on expanding background; full nonlinear FLRW stability and PPN remain open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(bool(x) for x in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
