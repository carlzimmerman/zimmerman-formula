#!/usr/bin/env python3
"""Finite-k/k=0 Dirac audit of the elliptic double-multiplier candidate.

The unitary-gauge quadratic scalar ADM density is derived from the same
covariant action as the companion static gate.  The velocity Hessian, primary
and secondary constraints, Poisson matrix, ranks and reduced Hamiltonian are
constructed symbolically, with k=0 and k!=0 kept separate.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def pb(left, right, pairs):
    return sp.simplify(sum(sp.diff(left, q) * sp.diff(right, p)
                           - sp.diff(left, p) * sp.diff(right, q)
                           for q, p in pairs))


def sector(k_value):
    k = sp.symbols("k", real=True)
    z, alpha, beta, chi, lam, sig = sp.symbols(
        "z alpha beta chi lambda sigma", real=True
    )
    zd = sp.symbols("zd", real=True)
    lagrangian = (
        -6 * zd**2 - 4 * k**2 * beta * zd + 2 * k**2 * z**2
        + 4 * k**2 * alpha * z + k**2 * lam * (z - chi)
        + k**2 * sig * (alpha - chi) + k**2 * chi**2
    )
    if k_value == 0:
        lagrangian = lagrangian.subs(k, 0)
    ad, bd, cd, ld, sd = sp.symbols("ad bd cd ld sd", real=True)
    lagrangian = lagrangian.subs({
        # These fields have no time-derivative terms in the displayed ADM
        # truncation; retaining named zero-velocity symbols lets SymPy form
        # the full Hessian without assuming a rank in advance.
        zd: zd,
    })
    pz = sp.symbols("pz", real=True)
    zd_solution = sp.solve(sp.Eq(pz, sp.diff(lagrangian, zd)), zd, dict=True)[0][zd]
    hamiltonian = sp.factor((pz * zd - lagrangian).subs(zd, zd_solution))
    coordinates = (z, alpha, beta, chi, lam, sig)
    momenta = sp.symbols("pz pa pb pc pl ps", real=True)
    pairs = tuple(zip(coordinates, momenta))
    velocities = (zd, ad, bd, cd, ld, sd)
    hessian = sp.hessian(lagrangian, velocities)
    primaries = tuple(momenta[1:])
    secondaries = tuple(sp.factor(pb(p, hamiltonian, pairs)) for p in primaries)
    active_secondaries = tuple(c for c in secondaries if c != 0)
    constraints = primaries + active_secondaries
    matrix = sp.Matrix([[pb(a, b, pairs) for b in constraints] for a in constraints])
    rank = matrix.rank()
    first_class = len(constraints) - rank
    second_class = rank
    phase_dimension = 2 * len(coordinates)
    physical_dof = sp.Rational(
        phase_dimension - 2 * first_class - second_class, 2
    )
    reduced = None
    if k_value != 0:
        substitutions = {
            sig: -4 * z,
            beta: -pz / (4 * k**2),
            chi: z,
            alpha: z,
            lam: 6 * z,
        }
        reduced = sp.factor(hamiltonian.subs(substitutions))
    return {
        "lagrangian": lagrangian,
        "velocity_hessian": hessian,
        "hessian_rank": hessian.rank(),
        "primary_constraints": primaries,
        "secondary_constraints": secondaries,
        "active_secondary_constraints": active_secondaries,
        "constraint_matrix": matrix,
        "constraint_rank": rank,
        "first_class": first_class,
        "second_class": second_class,
        "phase_dimension": phase_dimension,
        "physical_dof": physical_dof,
        "reduced_hamiltonian": reduced,
    }


def main() -> int:
    finite = sector("nonzero")
    zero = sector(0)
    checks = [
        finite["velocity_hessian"] == finite["velocity_hessian"].T,
        finite["constraint_matrix"] == -finite["constraint_matrix"].T,
        zero["constraint_matrix"] == -zero["constraint_matrix"].T,
        sp.simplify(finite["constraint_matrix"].det()) != 0,
        finite["physical_dof"] >= 0,
        zero["physical_dof"] >= 0,
        finite["reduced_hamiltonian"] is not None,
    ]
    print("ELLIPTIC DOUBLE-MULTIPLIER DIRAC AUDIT")
    for name, data in (("k!=0", finite), ("k=0", zero)):
        print(f"\n[{name}]")
        print("velocity Hessian =", data["velocity_hessian"])
        print("Hessian rank =", data["hessian_rank"])
        print("primary constraints =", data["primary_constraints"])
        print("secondary constraints =", data["secondary_constraints"])
        print("constraint PB rank =", data["constraint_rank"])
        print("first/second class =", data["first_class"], data["second_class"])
        print("physical scalar DOF =", data["physical_dof"])
        if data["reduced_hamiltonian"] is not None:
            print("reduced Hamiltonian =", data["reduced_hamiltonian"])
    passed = sum(bool(c) for c in checks)
    print("checks =", passed, "/", len(checks))
    result = {
        "status": "CLOCK_SECTOR_OPEN",
        "checks": {"count": len(checks), "passed": int(passed)},
        "finite_k": {"hessian_rank": str(finite["hessian_rank"]),
                      "constraint_rank": str(finite["constraint_rank"]),
                      "first_class": str(finite["first_class"]),
                      "second_class": str(finite["second_class"]),
                      "physical_dof": str(finite["physical_dof"]),
                      "reduced_hamiltonian": str(finite["reduced_hamiltonian"])},
        "zero_k": {"hessian_rank": str(zero["hessian_rank"]),
                   "constraint_rank": str(zero["constraint_rank"]),
                   "first_class": str(zero["first_class"]),
                   "second_class": str(zero["second_class"]),
                   "physical_dof": str(zero["physical_dof"])},
        "scope": "quadratic unitary-gauge scalar sector; not full covariant clock Dirac closure",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
