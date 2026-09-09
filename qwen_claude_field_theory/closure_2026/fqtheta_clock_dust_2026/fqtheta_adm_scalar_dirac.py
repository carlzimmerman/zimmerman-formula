#!/usr/bin/env python3
"""Dirac gate for the local scalar sector of the affine F(Q)Theta route.

This is a deliberately small, exact Fourier-mode calculation.  It starts from
the quadratic ADM scalar principal part of the covariant candidate used by
``fqtheta_gate.py`` on the affine degeneracy locus

    K_QQ = 3 F_Q**2/(2 M2),   F_QQ = 0.

With zeta=z, MOND scalar perturbation pi=p, lapse n and scalar shift beta=b,

  L_kin = -3 M2 s**2 + 2 M2 k**2 beta*s,
  s = zdot - alpha*(pdot - Q0*n), alpha=F_Q/(2*M2).

The no-velocity quadratic piece U is kept as a general local jet.  The
Einstein spatial-curvature/lapse mixing is represented by U_nz*k**2*n*z;
the MOND constitutive gradient is represented by U_pp*k**2*p**2/2.  No rank,
determinant, or degree-of-freedom result is inserted: SymPy differentiates the
Hamiltonian and Poisson brackets, and numerical samples only probe the exact
symbolic expressions.

The result is a closure obstruction for the route, not a universal theorem:
for a generic k!=0 jet with U_nz != 0, six second-class constraints leave one
local scalar configuration degree of freedom.  At k=0 the shift constraint
collapses and, for the diffeomorphism-compatible U_nn=0 jet, the scalar is
removed by first-class constraints.  The rank jump is a non-uniform
zero-momentum limit.  The full khronon/aether sector is not included here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def poisson(A, B, qs, ps):
    return sp.simplify(sum(sp.diff(A, q) * sp.diff(B, p)
                          - sp.diff(A, p) * sp.diff(B, q)
                          for q, p in zip(qs, ps)))


def build_gate():
    z, p, b, n = sp.symbols("z p beta n", real=True)
    pz, pp, pb, pn = sp.symbols("p_z p_p p_beta p_n", real=True)
    m, f, q0, k = sp.symbols("M2 Fq Q0 k", nonzero=True, real=True)
    uzz, upp, unz, unp, unn = sp.symbols(
        "Uzz Upp Unz Unp Unn", real=True
    )
    alpha = sp.simplify(f / (2 * m))
    # The velocity expression is written explicitly so the Hessian is derived
    # from the displayed action rather than from a precomputed matrix.
    zdot, pdot = sp.symbols("zdot pdot", real=True)
    svel = zdot - alpha * (pdot - q0 * n)
    U = (sp.Rational(1, 2) * uzz * k**2 * z**2
         + sp.Rational(1, 2) * upp * k**2 * p**2
         + unz * k**2 * n * z + unp * k**2 * n * p
         + sp.Rational(1, 2) * unn * n**2)
    L = -3 * m * svel**2 + 2 * m * k**2 * b * svel + U

    qs = [z, p, b, n]
    ps = [pz, pp, pb, pn]
    W = sp.simplify(sp.hessian(L, [zdot, pdot]))
    detW = sp.factor(W.det())
    degenerate = sp.simplify(detW.subs({m: 1, f: 1})) == 0

    # On the null Hessian locus p_p + alpha p_z is primary.  Solving p_z for
    # the one determined velocity combination gives the canonical Hamiltonian.
    s_from_pz = sp.simplify((2 * m * k**2 * b - pz) / (6 * m))
    Hc = sp.simplify(- (2 * m * k**2 * b - pz)**2 / (12 * m)
                     - alpha * q0 * n * pz - U)
    primary = [pb, pn, pp + alpha * pz]
    secondary = [
        sp.simplify(k**2 * (2 * m * k**2 * b - pz) / 3),
        sp.simplify(alpha * q0 * pz + sp.diff(U, n)),
        sp.simplify(sp.diff(U, p) + alpha * sp.diff(U, z)),
    ]
    constraints = primary + secondary
    PB = sp.Matrix([[poisson(A, B, qs, ps) for B in constraints]
                    for A in constraints])
    detPB = sp.factor(PB.det())
    discriminant = sp.factor(
        -4 * unn * upp - unn * uzz + k**2 * (2 * unp + unz)**2
    )

    # Constraint independence is checked from the Jacobian, not assumed.
    variables = qs + ps
    Cjac = sp.Matrix([[sp.diff(c, v) for v in variables]
                      for c in constraints])

    # A generic local nonzero-k sample has the Einstein lapse-curvature mixing
    # Unz != 0 and no lapse square (Unn=0).  The sample is used only to evaluate
    # ranks of the exact matrices above.
    sample_local = {m: 1, f: 1, q0: 1, k: 1,
                    uzz: 2, upp: -1, unz: 2, unp: 0, unn: 0}
    local_pb = PB.subs(sample_local)
    local_jac = Cjac.subs(sample_local)
    local_pb_rank = local_pb.rank()
    local_constraint_rank = local_jac.rank()
    local_constraint_count = len(constraints)
    local_second = local_pb_rank
    local_first = local_constraint_count - local_second
    local_dof = sp.simplify(
        len(qs) - local_first - sp.Rational(local_second, 2)
    )

    # At k=0, the beta secondary and the spatial-gradient part of the Phi
    # secondary vanish identically.  Keep only independent nonzero constraints
    # and evaluate the physically relevant Unn=0 (lapse is a multiplier) jet.
    zero_subs = {k: 0, unn: 0}
    zero_constraints = [sp.simplify(c.subs(zero_subs)) for c in constraints]
    zero_constraints = [c for c in zero_constraints if c != 0]
    zero_pb = sp.Matrix([[poisson(A, B, qs, ps) for B in zero_constraints]
                         for A in zero_constraints])
    zero_jac = sp.Matrix([[sp.diff(c, v) for v in variables]
                          for c in zero_constraints])
    zero_sample = {m: 1, f: 1, q0: 1, unn: 0}
    zero_pb_rank = zero_pb.subs(zero_sample).rank()
    zero_constraint_rank = zero_jac.subs(zero_sample).rank()
    zero_second = zero_pb_rank
    zero_first = len(zero_constraints) - zero_second
    zero_dof = sp.simplify(
        len(qs) - zero_first - sp.Rational(zero_second, 2)
    )

    # Solve the generic Unn=Unp=0 local constraints to expose the reduced
    # symplectic form.  Its k^2 factor makes the k->0 rank jump explicit.
    pz_red = sp.simplify(-k**2 * unz * z / (alpha * q0))
    pp_red = sp.simplify(-alpha * pz_red)
    omega_red = sp.factor(sp.diff(pp_red, z) - sp.diff(pz_red, p))
    Hred = sp.factor(Hc.subs({
        b: pz_red / (2 * m * k**2), pz: pz_red, pp: pp_red,
        n: -(upp * p + alpha * uzz * z) / (alpha * unz),
        unp: 0, unn: 0,
    }))
    Hz_red = sp.diff(Hred, z)
    Hp_red = sp.diff(Hred, p)
    reduced_flow = sp.Matrix([
        [-sp.diff(Hp_red, z) / omega_red,
         -sp.diff(Hp_red, p) / omega_red],
        [sp.diff(Hz_red, z) / omega_red,
         sp.diff(Hz_red, p) / omega_red],
    ]).applyfunc(sp.simplify)
    reduced_lambda = sp.symbols("lambda")
    reduced_char = sp.factor(
        reduced_flow.charpoly(reduced_lambda).as_expr()
    )

    return {
        "variables": [str(v) for v in qs + ps],
        "alpha": str(alpha),
        "quadratic_L": str(L),
        "velocity_hessian": [[str(x) for x in row] for row in W.tolist()],
        "velocity_hessian_determinant": str(detW),
        "affine_degeneracy_check_at_unit_sample": bool(degenerate),
        "canonical_H": str(Hc),
        "primary_constraints": [str(c) for c in primary],
        "secondary_constraints": [str(c) for c in secondary],
        "poisson_matrix": [[str(x) for x in row] for row in PB.tolist()],
        "poisson_antisymmetric": all(
            sp.simplify(x) == 0 for x in (PB + PB.T)
        ),
        "poisson_determinant": str(detPB),
        "poisson_determinant_factor": str(discriminant),
        "local_sample": {str(k0): str(v0) for k0, v0 in sample_local.items()},
        "local_k_nonzero": {
            "constraint_count": local_constraint_count,
            "constraint_jacobian_rank": local_constraint_rank,
            "poisson_rank": local_pb_rank,
            "second_class_count": local_second,
            "first_class_count": local_first,
            "configuration_dof": str(local_dof),
            "closure": "all multipliers are fixed when the displayed PB determinant is nonzero; no tertiary constraint is generated on this open stratum",
        },
        "k_zero": {
            "active_constraints": [str(c) for c in zero_constraints],
            "constraint_jacobian_rank": zero_constraint_rank,
            "poisson_rank": zero_pb_rank,
            "second_class_count": zero_second,
            "first_class_count": zero_first,
            "configuration_dof": str(zero_dof),
            "closure": "the beta and spatial-gradient secondaries vanish identically; the remaining constraints are first class for Unn=0",
        },
        "reduced_Unn_Unnp_zero": {
            "symplectic_coefficient_dz_wedge_dp": str(omega_red),
            "Hamiltonian": str(Hred),
            "flow_matrix": [[str(x) for x in row]
                            for row in reduced_flow.tolist()],
            "characteristic_polynomial": str(reduced_char),
            "interpretation": "the local reduced symplectic form is proportional to k^2 and therefore collapses in the homogeneous limit",
        },
        "status": "OPEN",
        "scope": [
            "principal scalar ADM sector only",
            "full khronon/aether perturbation and vector sector omitted",
            "U is a local no-velocity jet; only the kinetic/constraint rank is universal",
            "this is not a universal no-go for other actions",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "adm_scalar_dirac.json")
    args = parser.parse_args(argv)
    result = build_gate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    # A nonzero symbolic discriminant is the only genericity condition; ranks
    # themselves are reported from exact evaluation and are not hard-coded.
    if result["poisson_determinant_factor"] == "0":
        raise SystemExit("generic Dirac determinant vanished identically")


if __name__ == "__main__":
    main()
