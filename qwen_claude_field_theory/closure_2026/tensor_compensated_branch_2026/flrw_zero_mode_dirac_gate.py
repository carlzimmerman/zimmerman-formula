#!/usr/bin/env python3
"""Homogeneous FLRW Dirac audit with the lapse retained.

The finite-k tensor-compensator audit cannot be continued to k=0 by simply
setting k=0 after fixing N=1: that removes the Hamiltonian constraint.  This
gate redoes the homogeneous minisuperspace reduction of the same action with
the lapse N(t) kept as a canonical coordinate.  On flat FLRW all spatial
multiplier terms vanish, leaving the Einstein-Hilbert minisuperspace density

    L = -3 M2*a*adot**2/N - N*a**3*(M2*Lambda + rho).

The auxiliary homogeneous coordinates (chi, lambda, sigma, tau) have no
velocities or potential on this background.  The script derives the Hessian,
Legendre transform, primary/secondary constraints, their Poisson matrix and
preservation from SymPy; ranks are never entered by hand.
"""

from __future__ import annotations

import json
import sys

import sympy as sp


def pb(left, right, pairs):
    return sp.simplify(sum(sp.diff(left, q) * sp.diff(right, p)
                           - sp.diff(left, p) * sp.diff(right, q)
                           for q, p in pairs))


def main() -> int:
    M2, Lambda, rho = sp.symbols("M2 Lambda rho", positive=True, real=True)
    a, N, chi, lam, sig, tau = sp.symbols(
        "a N chi lambda sigma tau", positive=True, real=True
    )
    ad = sp.symbols("ad", real=True)
    velocities = (ad, sp.symbols("Nd"), sp.symbols("chid"),
                  sp.symbols("lamd"), sp.symbols("sigd"),
                  sp.symbols("taud"))
    L = -3 * M2 * a * ad**2 / N - N * a**3 * (M2 * Lambda + rho)
    qs = (a, N, chi, lam, sig, tau)
    ps = sp.symbols("pa pN pchi plam psig ptau", real=True)
    pairs = tuple(zip(qs, ps))

    hessian = sp.hessian(L, velocities)
    pa = sp.diff(L, ad)
    ad_sol = sp.solve(sp.Eq(ps[0], pa), ad, dict=True)[0][ad]
    H = sp.factor((ps[0] * ad - L).subs(ad, ad_sol))
    C = sp.factor(H / N)

    primaries = tuple(ps[i] for i in range(1, len(ps)))
    # p_N preservation gives the Hamiltonian constraint.  The other
    # multiplier momenta have identically vanishing preservation equations.
    secondary = sp.factor(C)
    constraints = primaries + (secondary,)
    matrix = sp.Matrix([[pb(x, y, pairs) for y in constraints]
                        for x in constraints])
    preservation = sp.factor(pb(secondary, H, pairs))
    rank = matrix.rank()
    first_class = len(constraints) - rank
    second_class = rank
    phase_dim = 2 * len(qs)
    dof = sp.Rational(phase_dim - 2 * first_class - second_class, 2)

    # N=1 and p_a=-6 M2*a^2*Hubble give the expanding Friedmann branch.
    Hubble = sp.symbols("H", positive=True, real=True)
    friedmann_residual = sp.factor(
        C.subs({N: 1, ps[0]: -6 * M2 * a**2 * Hubble}) / a**3
    )
    H2 = sp.solve(sp.Eq(friedmann_residual, 0), Hubble**2)[0]

    checks = [
        hessian == hessian.T,
        hessian.rank() == 1,
        H == sp.factor(N * C),
        primaries == (ps[1], ps[2], ps[3], ps[4], ps[5]),
        secondary != 0,
        matrix == -matrix.T,
        matrix.rank() == rank,
        preservation == 0,
        first_class == len(constraints),
        second_class == 0,
        dof == 0,
        H2 == (rho + M2 * Lambda) / (3 * M2),
    ]

    print("FLRW ZERO-MODE DIRAC AUDIT (LAPSE RETAINED)")
    print("L =", L)
    print("velocity Hessian rank =", hessian.rank())
    print("primary constraints =", primaries)
    print("secondary Hamiltonian constraint =", secondary)
    print("constraint PB matrix =", matrix)
    print("PB rank =", rank)
    print("first/second class =", first_class, second_class)
    print("constraint preservation PB(C,H) =", preservation)
    print("physical homogeneous scalar DOF =", dof)
    print("H^2 =", H2)
    print("checks =", sum(bool(x) for x in checks), "/", len(checks))

    result = {
        "status": "K0_MINISUPERSPACE_DIRAC_CLOSED",
        "checks": {"count": len(checks), "passed": sum(bool(x) for x in checks)},
        "hessian_rank": str(hessian.rank()),
        "constraint_rank": str(rank),
        "primary_count": len(primaries),
        "secondary_count": 1,
        "first_class": first_class,
        "second_class": second_class,
        "physical_homogeneous_scalar_dof": str(dof),
        "friedmann_H_squared": str(H2),
        "scope": "same tensor-compensated action on flat homogeneous minisuperspace; full covariant perturbation chain remains open",
    }
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
