#!/usr/bin/env python3
"""FSP-A exact scope checks, independent of the archived implementations.

Run from the repository root:
  python3 fine_structure_puzzle/archive_audit/scope_checks.py

No measured alpha is used. These are exact algebraic checks under the
explicit hypotheses below, not a computation of a physical effective action.
"""
import json
import sympy as s

checks = []


def check(label, condition):
    ok = bool(condition)
    checks.append({"label": label, "passed": ok})
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        raise AssertionError(label)


# Dimensions M,L,T; Gaussian e^2. Zero exponents give the trivial constant 1.
D = s.Matrix([[0, -1, 0, 1, 1], [1, 3, -2, 2, 3], [-1, -2, 0, -1, -2]])
xvec = s.Matrix([-3, 1, 1, 1, 0])
avec = s.Matrix([-1, 0, 0, -1, 1])
check("c,G,Lambda have no NONTRIVIAL dimensionless monomial", D[:, :3].det() != 0)
check("with hbar the rational nullspace is one-dimensional", len(D[:, :4].nullspace()) == 1)
check("x = Lambda G hbar/c^3 is dimensionless", D * xvec == s.zeros(3, 1))
check("alpha = e^2/(hbar c) is dimensionless", D * avec == s.zeros(3, 1))
check("x,alpha span the TWO-dimensional rational nullspace", s.Matrix.hstack(xvec, avec).rank() == 2 and len(D.nullspace()) == 2)

# AH3 premise applies only to Phi(e E/H^2,m/H). Maxwell energy and the
# induced current do not obey that same rescaling symmetry.
e, E, H, k, M = s.symbols("e E H k M", positive=True)
rescale = {e: k * e, E: E / k}
lam = e * E / H**2
rho = E**2 / 2
J = e * H**3 * s.Function("f")(lam, M)
check("external-field lambda invariant", s.simplify(lam.subs(rescale, simultaneous=True) - lam) == 0)
check("Maxwell energy scales as k^-2", s.simplify(rho.subs(rescale, simultaneous=True) - rho / k**2) == 0)
check("current e H^3 f(lambda,M) scales as k", s.simplify(J.subs(rescale, simultaneous=True) - k * J) == 0)
check("Maxwell source J/E scales as k^2", s.simplify((J / E).subs(rescale, simultaneous=True) - k**2 * J / E) == 0)

# Restricted candidate lifting form, NOT derived from Salam-Sezgin:
# dimensionless modulus t=chat>0, M0>0, power p>0, A real, B!=0.
# In the archived tree-level dictionary alpha_SU2=t^2/pi^2. This is not
# yet the physical electromagnetic coupling; its U(1) is massive.
t, M0, p = s.symbols("t M0 p", positive=True)
A = s.symbols("A", real=True)
B = s.symbols("B", nonzero=True, real=True)
V = M0**4 * t**p * (A + B * s.log(t))
Aprime = -B * s.log(t) - B / p
dV = s.diff(V, t)
check("stationary locus A=-B log(t)-B/p", s.simplify(dV.subs(A, Aprime)) == 0)
check("stationary curvature = M0^4 p B t^(p-2)", s.simplify(s.diff(V, t, 2).subs(A, Aprime) - M0**4 * p * B * t**(p - 2)) == 0)
check("stationary energy = -M0^4 B t^p/p", s.simplify(V.subs(A, Aprime) + M0**4 * B * t**p / p) == 0)
tstar = s.exp(-A / B - 1 / p)
check("tstar solves the stationarity equation", s.simplify(dV.subs(t, tstar)) == 0)
alpha_star = tstar**2 / s.pi**2
check("finite A shifts log(alpha_SU2) by -2 dA/B", s.simplify(s.diff(s.log(alpha_star), A) + 2 / B) == 0)
target_t = s.symbols("target_t", positive=True)
check("every target t is selectable by finite A", s.simplify(tstar.subs(A, -B * s.log(target_t) - B / p) - target_t) == 0)
shift = s.symbols("shift", real=True)
check("additive vacuum energy changes no stationary point", s.diff(V + shift * M0**4, t) == dV)

print("RESULT " + json.dumps({"checks": checks, "count": len(checks), "status": "passed", "non_claim": "No physical alpha or full quantum effective action computed."}, sort_keys=True))
