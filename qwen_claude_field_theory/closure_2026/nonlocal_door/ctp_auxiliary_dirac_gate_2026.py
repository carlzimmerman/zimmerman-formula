#!/usr/bin/env python3
"""Canonical audit of the standard doubled CTP auxiliary block.

Claim card
==========
For one transverse--traceless component, the conventional local CTP action is
the difference of the two branch actions.  In Keldysh variables ``c`` and
``d`` (average and difference), its exact quadratic principal part is

    S_CTP = integral dt [c_dot d_dot - omega^2 c d + J d].

Variation with respect to ``d`` gives the driven physical equation for ``c``;
the contour supplies endpoint/initial-history data.  This script asks the
narrow canonical question left by that construction: do physical-branch
matching conditions themselves furnish the needed second-class Dirac pair?

They do not in the conventional doubled action.  The kinetic Hessian is
regular, so it has no primary constraints.  If the endpoint condition d=0 is
artificially promoted to a condition on a Cauchy slice, preservation yields
p_c=0, but their computed Poisson-bracket matrix is singular.  Thus this is
not the requested second-class reduction of the local response pair.

Scope: this rules out only the ordinary two-branch CTP difference action with
standard diagonal matching as a *canonical Dirac* completion.  It does not
rule out a new, explicitly constrained doubled action; such an action would
have to be written and separately varied.
"""

from __future__ import annotations

import sys

import sympy as sp


def _poisson_bracket(left: sp.Expr, right: sp.Expr, pairs: list[tuple[sp.Symbol, sp.Symbol]]) -> sp.Expr:
    return sp.simplify(sum(
        sp.diff(left, q) * sp.diff(right, p) - sp.diff(left, p) * sp.diff(right, q)
        for q, p in pairs
    ))


def derive_ctp_auxiliary_dirac_gate() -> dict[str, object]:
    """Derive variation, Legendre map, and the attempted physical-branch chain."""
    t = sp.symbols("t", real=True)
    k = sp.symbols("k", nonnegative=True, real=True)
    source = sp.symbols("J", real=True)
    c_fn = sp.Function("c")(t)
    d_fn = sp.Function("d")(t)

    # This is S[q_+] - S[q_-] in c=(q_++q_-)/2, d=q_+-q_- variables.
    lagrangian = sp.diff(c_fn, t) * sp.diff(d_fn, t) - k**2 * c_fn * d_fn + source * d_fn
    el_c = sp.simplify(sp.diff(lagrangian, c_fn) - sp.diff(sp.diff(lagrangian, sp.diff(c_fn, t)), t))
    el_d = sp.simplify(sp.diff(lagrangian, d_fn) - sp.diff(sp.diff(lagrangian, sp.diff(d_fn, t)), t))
    expected_c = -sp.diff(d_fn, t, 2) - k**2 * d_fn
    expected_d = -sp.diff(c_fn, t, 2) - k**2 * c_fn + source

    c_dot, d_dot = sp.symbols("c_dot d_dot", real=True)
    velocity_lagrangian = c_dot * d_dot
    hessian = sp.hessian(velocity_lagrangian, (c_dot, d_dot))
    hessian_det = sp.simplify(hessian.det())
    hessian_rank = hessian.rank()
    is_regular = hessian_rank == hessian.rows

    c, d, p_c, p_d = sp.symbols("c d p_c p_d", real=True)
    hamiltonian = sp.expand(p_c * p_d + k**2 * c * d - source * d)
    canonical_pairs = [(c, p_c), (d, p_d)]

    # Diagonal matching is a contour endpoint condition.  Promoting it to a
    # slice condition makes its Dirac content testable without assuming it.
    chi_1 = d
    chi_2 = _poisson_bracket(chi_1, hamiltonian, canonical_pairs)
    chi_2 = sp.simplify(chi_2)
    chi_2_dot = sp.simplify(_poisson_bracket(chi_2, hamiltonian, canonical_pairs))
    constraints = [chi_1, chi_2]
    pb_matrix = sp.Matrix([
        [_poisson_bracket(left, right, canonical_pairs) for right in constraints]
        for left in constraints
    ])
    pb_rank = pb_matrix.rank()
    closure_residual = sp.simplify(chi_2_dot.subs({chi_1: 0, chi_2: 0}))

    # The zero spatial-momentum mode is the FLRW/homogeneous danger sector; a
    # positive placeholder kappa samples every nonzero TT Fourier mode without
    # treating the rank as an input.
    kappa = sp.symbols("kappa", positive=True, real=True)
    mode_sectors = {}
    for name, replacement in (("k=0", 0), ("k!=0", kappa)):
        sector_matrix = sp.simplify(pb_matrix.subs(k, replacement))
        sector_closure = sp.simplify(closure_residual.subs(k, replacement))
        sector_rank = sector_matrix.rank()
        mode_sectors[name] = {
            "pb_matrix": sector_matrix,
            "pb_rank": sector_rank,
            "closure_residual": sector_closure,
            "is_second_class": sector_rank == sector_matrix.rows,
        }

    return {
        "variation": {
            "lagrangian": lagrangian,
            "el_c": el_c,
            "el_d": el_d,
            "c_equation_residual": sp.simplify(el_d - expected_d),
            "d_equation_residual": sp.simplify(el_c - expected_c),
        },
        "kinetic": {
            "hessian": hessian,
            "hessian_det": hessian_det,
            "hessian_rank": hessian_rank,
            "primary_constraint_count": hessian.cols - hessian_rank,
            "is_regular": is_regular,
        },
        "physical_branch": {
            "hamiltonian": hamiltonian,
            "constraints": constraints,
            "preservation_equations": [chi_2, chi_2_dot],
            "preserved_constraints": len(constraints),
            "pb_matrix": pb_matrix,
            "pb_rank": pb_rank,
            "closure_residual": closure_residual,
            "is_closed": closure_residual == 0,
            "is_second_class": pb_rank == pb_matrix.rows,
        },
        "mode_sectors": mode_sectors,
    }


def main() -> int:
    result = derive_ctp_auxiliary_dirac_gate()
    variation = result["variation"]
    kinetic = result["kinetic"]
    branch = result["physical_branch"]

    print("=" * 92)
    print("CTP AUXILIARY DIRAC GATE: STANDARD DOUBLED ACTION VS PHYSICAL-BRANCH MATCHING")
    print("=" * 92)
    print("\n[1] Varied doubled action")
    print("  L_CTP =", variation["lagrangian"])
    print("  delta S / delta d =", variation["el_d"])
    print("  delta S / delta c =", variation["el_c"])
    print("  driven c-equation residual =", variation["c_equation_residual"])
    print("  response d-equation residual =", variation["d_equation_residual"])

    print("\n[2] Legendre map before contour boundary data")
    print("  velocity Hessian =", kinetic["hessian"])
    print("  det(W) =", kinetic["hessian_det"])
    print("  rank(W) =", kinetic["hessian_rank"])
    print("  nullity(W) / primary constraints =", kinetic["primary_constraint_count"])
    print("  regular Legendre map =", kinetic["is_regular"])

    print("\n[3] Attempted slice realization of diagonal matching")
    print("  H_CTP =", branch["hamiltonian"])
    print("  endpoint condition promoted to slice: chi_1 =", branch["constraints"][0])
    print("  preservation gives chi_2 =", branch["constraints"][1])
    print("  preservation of chi_2 =", branch["preservation_equations"][1])
    print("  Poisson-bracket matrix C_ab =", branch["pb_matrix"])
    print("  rank(C) =", branch["pb_rank"])
    print("  closure residual on chi_1=chi_2=0 =", branch["closure_residual"])
    print("  second-class pair =", branch["is_second_class"])

    print("\n[4] Separate Fourier sectors")
    for name, sector in result["mode_sectors"].items():
        print(f"  {name}: C_ab = {sector['pb_matrix']}; rank(C) = {sector['pb_rank']}; "
              f"closure residual = {sector['closure_residual']}; second class = {sector['is_second_class']}")

    checks = [
        variation["c_equation_residual"] == 0,
        variation["d_equation_residual"] == 0,
        kinetic["is_regular"],
        branch["is_closed"],
        not branch["is_second_class"],
        all(not sector["is_second_class"] for sector in result["mode_sectors"].values()),
    ]
    labels = [
        "the difference variation gives the driven average-field equation",
        "the average variation gives the homogeneous response-field equation",
        "the ordinary doubled action has no primary Dirac constraint",
        "the attempted physical-branch chain closes without a new constraint",
        "the actual PB matrix is not invertible, so matching is not a second-class reduction",
        "the obstruction persists separately in the k=0 and k!=0 sectors",
    ]
    for okay, label in zip(checks, labels):
        print(f"  [{'PASS' if okay else 'FAIL'}] {label}")

    print("\n[VERDICT]")
    print("  DEAD as the missing canonical rescue for the standard CTP difference action: it generates")
    print("  causal equations, but its diagonal matching is boundary/history data rather than a computed")
    print("  second-class Dirac pair.  The finite-localized auxiliary ghost is therefore not canonically")
    print("  removed by this CTP step.  OPEN only for a different explicitly constrained doubled action,")
    print("  which must be supplied with its complete constraint algebra and physical stress tensor.")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
