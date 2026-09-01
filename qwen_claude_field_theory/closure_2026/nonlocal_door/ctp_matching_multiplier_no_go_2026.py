#!/usr/bin/env python3
"""Why an explicit multiplier cannot turn CTP matching into the missing Dirac rescue.

Claim card
==========
The most direct modification of the ordinary Keldysh auxiliary action is to
enforce the difference field ``d`` by a Lagrange multiplier:

    L = c_dot d_dot - k^2 c d + J d + lambda d.

This is a genuine local action, so it is the sharpest simple proposal for
making diagonal CTP matching a canonical constraint.  The script varies it and
performs the entire finite Dirac chain.  The result is an obstruction, not a
construction: d=0 makes the multiplier absorb the desired response equation,
leaving the average field c arbitrary.  Setting lambda=0 would restore the
driven equation, but that is an external condition rather than an
Euler--Lagrange/Dirac consequence.

Scope: a single TT Fourier component and the literal multiplier completion
above.  More elaborate constrained doubled actions are not ruled out, but
they must evade this multiplier-absorption mechanism explicitly.
"""

from __future__ import annotations

import sys

import sympy as sp


def _pb(left: sp.Expr, right: sp.Expr, pairs: list[tuple[sp.Symbol, sp.Symbol]]) -> sp.Expr:
    return sp.simplify(sum(
        sp.diff(left, q) * sp.diff(right, p) - sp.diff(left, p) * sp.diff(right, q)
        for q, p in pairs
    ))


def derive_matching_multiplier_gate() -> dict[str, object]:
    """Vary the constrained action and close its actual Dirac chain."""
    t = sp.symbols("t", real=True)
    k = sp.symbols("k", nonnegative=True, real=True)
    source = sp.symbols("J", real=True)
    c_fn = sp.Function("c")(t)
    d_fn = sp.Function("d")(t)
    lam_fn = sp.Function("lambda")(t)
    lagrangian = (
        sp.diff(c_fn, t) * sp.diff(d_fn, t)
        - k**2 * c_fn * d_fn
        + source * d_fn
        + lam_fn * d_fn
    )

    def euler(field: sp.Expr) -> sp.Expr:
        return sp.simplify(sp.diff(lagrangian, field) - sp.diff(sp.diff(lagrangian, sp.diff(field, t)), t))

    el_c = euler(c_fn)
    el_d = euler(d_fn)
    el_lam = euler(lam_fn)
    desired_driven_residual = -sp.diff(c_fn, t, 2) - k**2 * c_fn + source
    lambda_solution = sp.solve(sp.Eq(el_d, 0), lam_fn)[0]

    c, d, lam, p_c, p_d, p_lam = sp.symbols("c d lambda p_c p_d p_lambda", real=True)
    hamiltonian = sp.expand(p_c * p_d + k**2 * c * d - (source + lam) * d)
    pairs = [(c, p_c), (d, p_d), (lam, p_lam)]
    primary = p_lam
    secondary = sp.simplify(_pb(primary, hamiltonian, pairs))
    tertiary = sp.simplify(_pb(secondary, hamiltonian, pairs))
    closure_step = sp.simplify(_pb(tertiary, hamiltonian, pairs))
    constraints = [primary, secondary, tertiary]
    pb_matrix = sp.Matrix([
        [_pb(left, right, pairs) for right in constraints]
        for left in constraints
    ])
    closure_residual = sp.simplify(closure_step.subs({secondary: 0, tertiary: 0}))
    rank = pb_matrix.rank()

    kappa = sp.symbols("kappa", positive=True, real=True)
    mode_sectors = {}
    for name, replacement in (("k=0", 0), ("k!=0", kappa)):
        matrix = sp.simplify(pb_matrix.subs(k, replacement))
        mode_sectors[name] = {
            "pb_matrix": matrix,
            "pb_rank": matrix.rank(),
            "closure_residual": sp.simplify(closure_residual.subs(k, replacement)),
            "is_second_class": matrix.rank() == matrix.rows,
        }

    return {
        "variation": {
            "lagrangian": lagrangian,
            "el_c": el_c,
            "el_d": el_d,
            "el_lambda": el_lam,
            "difference_equation_residual": sp.simplify(el_d - (desired_driven_residual + lam_fn)),
            "matching_equation": el_lam,
            "matching_constraint_residual": sp.simplify(el_lam - d_fn),
            "lambda_solution": lambda_solution,
            "multiplier_solution_contains_c_acceleration": lambda_solution.has(sp.diff(c_fn, t, 2)),
            "physical_response_is_determined": sp.simplify(lambda_solution) == 0,
        },
        "dirac": {
            "hamiltonian": hamiltonian,
            "constraints": constraints,
            "preservation_chain": [secondary, tertiary, closure_step],
            "pb_matrix": pb_matrix,
            "pb_rank": rank,
            "closure_residual": closure_residual,
            "is_closed": closure_residual == 0,
            "is_second_class": rank == pb_matrix.rows,
        },
        "mode_sectors": mode_sectors,
    }


def main() -> int:
    result = derive_matching_multiplier_gate()
    variation = result["variation"]
    dirac = result["dirac"]
    print("=" * 92)
    print("CTP MATCHING-MULTIPLIER GATE: CONSTRAINING d ERases THE PHYSICAL RESPONSE EQUATION")
    print("=" * 92)
    print("\n[1] Euler--Lagrange variation")
    print("  L =", variation["lagrangian"])
    print("  delta S / delta d =", variation["el_d"])
    print("  delta S / delta c =", variation["el_c"])
    print("  delta S / delta lambda =", variation["el_lambda"])
    print("  lambda solved from delta S / delta d = 0:", variation["lambda_solution"])
    print("  multiplier absorbs c acceleration =", variation["multiplier_solution_contains_c_acceleration"])
    print("  c response fixed without externally imposing lambda=0 =", variation["physical_response_is_determined"])

    print("\n[2] Canonical Dirac chain")
    print("  H =", dirac["hamiltonian"])
    print("  primary -> secondary -> tertiary =", dirac["constraints"])
    print("  next preservation step =", dirac["preservation_chain"][-1])
    print("  C_ab =", dirac["pb_matrix"])
    print("  rank(C) =", dirac["pb_rank"])
    print("  closure residual =", dirac["closure_residual"])
    print("  second-class completion =", dirac["is_second_class"])

    print("\n[3] Separate Fourier sectors")
    for name, sector in result["mode_sectors"].items():
        print(f"  {name}: C_ab = {sector['pb_matrix']}; rank(C) = {sector['pb_rank']}; "
              f"closure residual = {sector['closure_residual']}; second class = {sector['is_second_class']}")

    checks = [
        variation["difference_equation_residual"] == 0,
        variation["matching_constraint_residual"] == 0,
        variation["multiplier_solution_contains_c_acceleration"],
        not variation["physical_response_is_determined"],
        dirac["is_closed"],
        not dirac["is_second_class"],
        all(not sector["is_second_class"] for sector in result["mode_sectors"].values()),
    ]
    labels = [
        "the desired driven equation appears only together with the new multiplier",
        "the multiplier variation enforces d=0 exactly",
        "on d=0 the multiplier absorbs the average-field acceleration",
        "there is no Euler--Lagrange equation left that fixes the physical average response",
        "the actual Dirac chain closes",
        "the computed constraint matrix is not a second-class completion",
        "the failure remains in both k=0 and k!=0 sectors",
    ]
    for okay, label in zip(checks, labels):
        print(f"  [{'PASS' if okay else 'FAIL'}] {label}")

    print("\n[VERDICT]")
    print("  DEAD for the direct multiplier repair.  A local constraint lambda*d=0 does remove the")
    print("  difference field, but it replaces the sought equation c_ddot+k^2 c=J by a definition of")
    print("  lambda.  Restoring lambda=0 is an imposed boundary rule, not an action-derived Dirac result.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
