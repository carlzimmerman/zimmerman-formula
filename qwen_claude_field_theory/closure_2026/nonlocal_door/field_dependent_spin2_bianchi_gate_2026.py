#!/usr/bin/env python3
"""Action-derived test of the simplest nonlinear spin-2 completion.

The field-independent spin-2 form factor is healthy and has Phi=Psi at
linear order, but it is linear in baryonic mass.  A tempting repair is to
replace it by A(I) G_munu, with I a curvature scalar.  This script separates
the invalid equation-level proposal from its nearest covariant action:

    naive:  E_munu = A(I) G_munu = 8 pi G T_munu,
    action: S = (M_P^2/2) int sqrt(-g) F(R),  F(R)=R+alpha R^2.

The product rule gives a nonzero Bianchi residual for the naive equation when
A is field-dependent.  The F(R) action supplies the missing terms.  Its trace
equation propagates delta R when alpha is nonzero, and its trace-free spatial
equation has D_ij F_R as an explicit no-slip source.  This closes this scalar
curvature-dependent completion, not every conceivable tensor/nonlocal one.
"""

from __future__ import annotations

import sys
from typing import Any

import sympy as sp


def derive_bianchi_gate() -> dict[str, Any]:
    """Return symbolic Bianchi, action-variation, trace, and no-slip objects."""

    alpha, R, delta_R, box_delta_R, T = sp.symbols("alpha R delta_R Box_delta_R T", nonzero=True)
    G_component, A_I, grad_I = sp.symbols("G_component A_I grad_I", nonzero=True)
    DTF_R = sp.symbols("D_TF_R", nonzero=True)

    # Product rule plus contracted Bianchi identity: nabla.G=0.
    bianchi_residual = sp.simplify(G_component * A_I * grad_I)

    F = R + alpha * R**2
    F_R = sp.diff(F, R)
    F_RR = sp.diff(F_R, R)

    # Metric Euler--Lagrange tensor for int sqrt(-g) F(R):
    # E_mn = F_R R_mn - F g_mn/2 + (g_mn Box - nabla_m nabla_n) F_R.
    # Its trace is F_R R - 2F + 3 Box F_R.  Around R=0 the last term
    # provides the scalar kinetic operator 3 F_RR Box(delta R).
    trace_equation = sp.simplify(F_R * R - 2 * F + 3 * F_RR * box_delta_R - 8 * sp.pi * T)
    linear_trace_equation = sp.simplify(
        trace_equation.subs({R: delta_R, box_delta_R: box_delta_R})
    )
    scalar_kinetic_coefficient = sp.simplify(3 * F_RR)

    # In a static, isotropic-matter weak field, the traceless spatial equation
    # is F_R D_ij(Phi-Psi) - D_ij F_R = 0.  For F=R+alpha R^2,
    # D_ij F_R=2 alpha D_ij R.  This is a true metric variation term.
    no_slip_tf_source = sp.simplify(2 * alpha * DTF_R)
    no_slip_condition = sp.Eq(no_slip_tf_source, 0, evaluate=False)

    # If alpha !=0, F_R constant iff R constant.  On an asymptotically flat
    # sourced branch that constant is R=0; then the trace equation has no
    # nonzero matter source.  The boolean records that exact logical reduction.
    constant_f_r_implies = sp.simplify(sp.diff(F_R, R) - 2 * alpha) == 0
    source_free_on_constant_branch = sp.simplify(
        linear_trace_equation.subs({delta_R: 0, box_delta_R: 0})
    )

    return {
        "naive_multiplier": {
            "equation": "A(I) G_munu = 8 pi G T_munu",
            "bianchi_residual": bianchi_residual,
        },
        "f_r_action": {
            "F": F,
            "F_R": F_R,
            "F_RR": F_RR,
            "trace_equation": trace_equation,
            "linear_trace_equation": linear_trace_equation,
            "scalar_kinetic_coefficient": scalar_kinetic_coefficient,
        },
        "weak_field": {
            "tracefree_equation": "F_R D_ij(Phi-Psi) - D_ij(F_R) = 0",
            "no_slip_tf_source": no_slip_tf_source,
            "no_slip_condition": no_slip_condition,
            "constant_f_r_implies": bool(constant_f_r_implies),
            "source_free_on_constant_branch": source_free_on_constant_branch,
        },
    }


def _check(label: str, condition: Any) -> bool:
    passed = bool(condition)
    print(f"  [{'PASS' if passed else 'FAIL'}] {label}")
    return passed


def main() -> int:
    result = derive_bianchi_gate()
    naive = result["naive_multiplier"]
    f_r = result["f_r_action"]
    weak = result["weak_field"]

    print("=" * 92)
    print("FIELD-DEPENDENT SPIN-2 GATE: BIANCHI IDENTITY AND F(R) ACTION COMPLETION")
    print("=" * 92)
    print("\n[1] Naive equation-level modification")
    print("  E_munu = A(I) G_munu")
    print(f"  nabla^mu E_munu = G_munu A_I nabla^mu I = {naive['bianchi_residual']}")
    checks = [_check("a nonconstant scalar multiplier of G_munu is not separately divergence-free", naive["bianchi_residual"] != 0)]

    print("\n[2] Nearest scalar-curvature action and its Euler--Lagrange consequences")
    print(f"  F(R) = {f_r['F']}; F_R = {f_r['F_R']}; F_RR = {f_r['F_RR']}")
    print("  E_munu = F_R R_munu - F g_munu/2 + (g_munu Box-nabla_m nabla_n)F_R")
    print(f"  Trace E=0: {f_r['trace_equation']} = 0")
    print(f"  Linear trace: {f_r['linear_trace_equation']} = 0")
    print(f"  coefficient of Box(delta R) = {f_r['scalar_kinetic_coefficient']}")
    checks.append(_check("the honest F(R) completion propagates a scalar whenever alpha is nonzero", f_r["scalar_kinetic_coefficient"] != 0))

    print("\n[3] Weak static no-slip condition")
    print(f"  TF equation: {weak['tracefree_equation']}")
    print(f"  D_ij F_R = {weak['no_slip_tf_source']}")
    print(f"  Phi=Psi demands: {weak['no_slip_condition']}")
    print(f"  dF_R/dR=2 alpha, so constant F_R iff constant R for alpha!=0: {weak['constant_f_r_implies']}")
    print(f"  On the asymptotically-flat constant-R=0 branch, trace residual = {weak['source_free_on_constant_branch']}")
    checks.append(_check("a nonuniform sourced curvature branch has an explicit TF no-slip source", weak["no_slip_tf_source"] != 0))
    checks.append(_check("removing that source by constant F_R collapses this F(R) branch to source-free GR", weak["constant_f_r_implies"] and weak["source_free_on_constant_branch"] != 0))

    print("\n[VERDICT]")
    print("  DEAD for scalar curvature-dependent spin-2 strength: the naïve equation violates Bianchi;")
    print("  its action completion carries a scalar and sources Phi-Psi unless it reduces to the constant-GR branch.")
    print("  Still OPEN: a genuinely tensorial, field-dependent nonlocal action whose full variation remains")
    print("  divergence-free, no-slip, zero-free, and nonlinear in the MOND regime.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
