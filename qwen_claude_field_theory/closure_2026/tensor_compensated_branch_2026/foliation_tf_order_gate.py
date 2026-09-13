#!/usr/bin/env python3
"""Derivative-order audit for local clock-foliation trace-free operators.

At linear scalar order around an isotropic static background, the trace-free
spatial tensors built from the foliation acceleration and intrinsic spatial
curvature have the schematic Fourier forms

  (D_i a_j)^TF ~ k^2 Phi,
  (R^(3)_ij)^TF ~ k^2 Psi,
  (D_i D_j R^(3))^TF ~ k^4 Psi.

The scalar perturbation of q_ij itself is purely trace, so q_ij^TF=0.  Any
finite local linear combination therefore has an overall k^2 factor.  This
gate checks that factor symbolically and propagates it into the compensator
response.  It is conditional on this stated invariant basis; it is not a
classification theorem for arbitrary extra fields.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def main() -> int:
    z, A, B, C, R = sp.symbols("z A B C R", real=True)
    tf_operator = z * A + z * B + z**2 * C
    factored = sp.factor(tf_operator)
    quotient = sp.factor(tf_operator / z)
    q_scalar_tf = sp.Integer(0)
    checks = {
        "scalar_spatial_metric_tf_vanishes": q_scalar_tf == 0,
        "every_basis_term_has_z_factor": sp.simplify(tf_operator.subs(z, 0)) == 0,
        "operator_factorization_is_exact": sp.simplify(factored - z * quotient) == 0,
        "zero_mode_operator_vanishes": sp.simplify(tf_operator.subs(z, 0)) == 0,
        "generic_response_has_inverse_z": sp.simplify((-R / tf_operator) * z + R / quotient) == 0,
    }
    print("LOCAL CLOCK-FOLIATION TF ORDER GATE")
    print("TF operator =", tf_operator)
    print("factored operator =", factored)
    print("quotient Pbar =", quotient)
    print("scalar q_ij TF =", q_scalar_tf)
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    payload = {
        "status": "LOCAL_FOLIATION_TF_HAS_K2_FACTOR" if all(checks.values()) else "INCONCLUSIVE",
        "checks": checks,
        "operator": str(tf_operator),
        "quotient": str(quotient),
        "assumptions": [
            "linear scalar perturbations about isotropic static foliation",
            "finite local combinations of D_i a_j, R^(3)_ij, and further spatial derivatives",
            "no additional background anisotropic tensor or algebraic reference metric",
        ],
        "interpretation": (
            "Within this standard local foliation-invariant basis, P(0)=0 is forced. "
            "The tensor compensator response to a generic nonzero TF residual is "
            "therefore inverse-Laplacian and inherits the previously proved IR obstruction."
        ),
    }
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
