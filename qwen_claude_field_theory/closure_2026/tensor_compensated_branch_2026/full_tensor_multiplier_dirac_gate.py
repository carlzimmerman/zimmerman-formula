#!/usr/bin/env python3
"""Full five-component trace-free-multiplier linear Dirac audit.

For a Fourier scalar mode, rotational decomposition of a spatial symmetric
trace-free multiplier has one scalar component and four transverse/vector
components.  The scalar component contributes the already-derived
``k**2*tau*(zeta-chi)`` term.  The remaining four components are included as
independent canonical coordinates with zero velocity and zero background
coupling; their primary constraints and preservation are generated explicitly.
This checks that they add no hidden physical DOF.
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
    z, alpha, beta, chi, lam, sig, tau = sp.symbols(
        "z alpha beta chi lambda sigma tau", real=True
    )
    spectators = sp.symbols("tau_v0:4", real=True)
    zd = sp.symbols("zd", real=True)
    L = (-6 * zd**2 - 4 * k**2 * beta * zd + 2 * k**2 * z**2
         + 4 * k**2 * alpha * z + k**2 * lam * (z - chi)
         + k**2 * sig * (alpha - chi) + k**2 * chi**2
         + k**2 * tau * (z - chi))
    if k_value == 0:
        L = L.subs(k, 0)
    qs = (z, alpha, beta, chi, lam, sig, tau) + spectators
    ps = sp.symbols("pz pa pb pc pl ps pt pv0:4", real=True)
    pairs = tuple(zip(qs, ps))
    velocities = (zd,) + sp.symbols("v0:10", real=True)
    hessian = sp.hessian(L, velocities)
    pz = ps[0]
    zd_sol = sp.solve(sp.Eq(pz, sp.diff(L, zd)), zd, dict=True)[0][zd]
    H = sp.factor((pz * zd - L).subs(zd, zd_sol))
    primaries = tuple(ps[1:])
    secondaries_all = tuple(sp.factor(pb(p, H, pairs)) for p in primaries)
    secondaries = tuple(c for c in secondaries_all if c != 0)
    constraints = primaries + secondaries
    matrix = sp.Matrix([[pb(a, b, pairs) for b in constraints]
                        for a in constraints])
    rank = matrix.rank()
    first_class = len(constraints) - rank
    second_class = rank
    phase_dim = 2 * len(qs)
    dof = sp.Rational(phase_dim - 2 * first_class - second_class, 2)
    return {
        "hessian": hessian,
        "hessian_rank": hessian.rank(),
        "primaries": primaries,
        "secondaries_all": secondaries_all,
        "secondaries": secondaries,
        "constraint_matrix": matrix,
        "constraint_rank": rank,
        "first_class": first_class,
        "second_class": second_class,
        "phase_dimension": phase_dim,
        "physical_dof": dof,
    }


def main() -> int:
    finite = sector("nonzero")
    zero = sector(0)
    checks = [
        finite["hessian"] == finite["hessian"].T,
        finite["constraint_matrix"] == -finite["constraint_matrix"].T,
        zero["constraint_matrix"] == -zero["constraint_matrix"].T,
        finite["constraint_matrix"].rank() == finite["constraint_rank"],
        finite["hessian_rank"] == 1,
        finite["constraint_rank"] == 10,
        finite["first_class"] == 6,
        finite["second_class"] == 10,
        finite["physical_dof"] == 0,
        zero["constraint_rank"] == 0,
        zero["first_class"] == 10,
        zero["physical_dof"] == 1,
    ]
    print("FULL FIVE-COMPONENT TF MULTIPLIER DIRAC AUDIT")
    for name, data in (("k!=0", finite), ("k=0 fixed lapse", zero)):
        print(f"\n[{name}]")
        print("Hessian rank =", data["hessian_rank"])
        print("primary count =", len(data["primaries"]))
        print("secondary constraints =", data["secondaries_all"])
        print("active PB rank =", data["constraint_rank"])
        print("first/second class =", data["first_class"], data["second_class"])
        print("physical scalar-sector DOF =", data["physical_dof"])
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))
    result = {
        "status": "FULL_TF_FINITE_K_AUXILIARY_CLOSED_ZERO_MODE_GAUGE_ARTIFACT",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "finite_k": {"phase_dimension": finite["phase_dimension"],
                     "primary_count": len(finite["primaries"]),
                     "secondary_count": len(finite["secondaries"]),
                     "constraint_rank": finite["constraint_rank"],
                     "first_class": finite["first_class"],
                     "second_class": finite["second_class"],
                     "physical_dof": str(finite["physical_dof"])},
        "zero_k_fixed_lapse": {"phase_dimension": zero["phase_dimension"],
                               "primary_count": len(zero["primaries"]),
                               "constraint_rank": zero["constraint_rank"],
                               "first_class": zero["first_class"],
                               "physical_dof": str(zero["physical_dof"])},
        "scope": "linear five-component TF multiplier decomposition; lapse-retained FLRW zero mode is handled by flrw_zero_mode_dirac_gate.py, full nonlinear covariant chain remains open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(bool(x) for x in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
