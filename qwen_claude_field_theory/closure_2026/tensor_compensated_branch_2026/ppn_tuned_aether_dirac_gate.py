#!/usr/bin/env python3
"""Dirac test of the PPN-tuned aether block inside the tensor branch.

On c13=0 the hypersurface-orthogonal Einstein-aether principal terms reduce
to c2*K^2+c4*a_i a^i (up to the common normalization).  The alpha1=alpha2=0
and cT=1 locus has c4=-c1, hence c14=0.  This gate inserts that principal
block into the already-derived tensor-compensator scalar density and computes
the finite-k Hessian, every primary/secondary constraint, and the Poisson rank.
It tests whether the extra tensor constraint removes the scalar pole rather
than treating the singular standard-aether speed formula as a verdict.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def pb(left, right, pairs):
    return sp.simplify(sum(sp.diff(left, q) * sp.diff(right, p)
                           - sp.diff(left, p) * sp.diff(right, q)
                           for q, p in pairs))


def derive(k_value):
    k = sp.symbols("k", real=True)
    c2, c4 = sp.symbols("c2 c4", real=True)
    z, alpha, beta, chi, lam, sig, tau = sp.symbols(
        "z alpha beta chi lambda sigma tau", real=True
    )
    zd = sp.symbols("zd", real=True)
    # K = 3 zd + k^2 beta and a_i a^i = k^2 alpha^2 in the frozen
    # unitary-clock scalar principal block.  c13=0 has removed K_ij K^ij.
    K = 3 * zd + k**2 * beta
    L = (-6 * zd**2 - 4 * k**2 * beta * zd + 2 * k**2 * z**2
         + 4 * k**2 * alpha * z + k**2 * lam * (z - chi)
         + k**2 * sig * (alpha - chi) + k**2 * chi**2
         + k**2 * tau * (z - chi) + c2 * K**2 + c4 * k**2 * alpha**2)
    if k_value == 0:
        L = L.subs(k, 0)
    qs = (z, alpha, beta, chi, lam, sig, tau)
    ps = sp.symbols("pz pa pb pc pl ps pt", real=True)
    pairs = tuple(zip(qs, ps))
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
    witness = {c2: sp.Rational(1, 3), c4: -sp.Rational(1, 2), k: 1}
    return {
        "L": L,
        "hessian": sp.hessian(L, (zd,) + sp.symbols("v0:6")),
        "hessian_rank": sp.hessian(L, (zd,) + sp.symbols("v0:6")).rank(),
        "primaries": primaries,
        "secondaries_all": secondaries_all,
        "secondaries": secondaries,
        "constraint_matrix": matrix,
        "constraint_rank": rank,
        "witness_rank": matrix.subs(witness).rank(),
        "first_class": first_class,
        "second_class": second_class,
        "phase_dimension": phase_dim,
        "physical_dof": dof,
        "witness": witness,
    }


def main() -> int:
    finite = derive("nonzero")
    zero = derive(0)
    checks = [
        finite["hessian"] == finite["hessian"].T,
        finite["constraint_matrix"] == -finite["constraint_matrix"].T,
        finite["witness_rank"] == finite["constraint_rank"],
        finite["hessian_rank"] == 1,
        finite["constraint_rank"] == 10,
        finite["first_class"] == 2,
        finite["second_class"] == 10,
        finite["physical_dof"] == 0,
        zero["constraint_rank"] == 0,
        zero["physical_dof"] == 1,
    ]
    print("PPN-TUNED AETHER + TENSOR-COMPENSATOR DIRAC AUDIT")
    print("finite-k L =", finite["L"])
    print("finite-k Hessian rank =", finite["hessian_rank"])
    print("finite-k secondary constraints =", finite["secondaries_all"])
    print("finite-k PB rank =", finite["constraint_rank"])
    print("finite-k first/second class =", finite["first_class"], finite["second_class"])
    print("finite-k physical scalar DOF =", finite["physical_dof"])
    print("witness PB rank =", finite["witness_rank"])
    print("fixed-lapse k=0 PB rank/DOF =", zero["constraint_rank"], zero["physical_dof"])
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))
    result = {
        "status": "PPN_TUNED_C14_ZERO_SCALAR_REMOVED_BY_TENSOR_CONSTRAINT",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "finite_k": {"phase_dimension": finite["phase_dimension"],
                     "constraint_rank": finite["constraint_rank"],
                     "first_class": finite["first_class"],
                     "second_class": finite["second_class"],
                     "physical_dof": str(finite["physical_dof"]),
                     "witness_rank": finite["witness_rank"]},
        "fixed_lapse_k0": {"constraint_rank": zero["constraint_rank"],
                           "physical_dof": str(zero["physical_dof"])},
        "scope": "frozen-coefficient c13=0,c14=0 aether principal block plus tensor scalar constraint; full covariant Dirac and causality remain open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(bool(x) for x in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
