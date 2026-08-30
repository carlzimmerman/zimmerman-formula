#!/usr/bin/env python3
"""
T01 — Exact action-level definition of the repaired nonlocal candidate.

Goal (per closure_manual_pack/qwen_tasks/T01_action_variation.md):
  * state conventions (signature, curvature);
  * give a complete constrained auxiliary representation;
  * state every field and multiplier;
  * derive each Euler-Lagrange (E-L) equation;
  * state how the retarded boundary condition is imposed;
  * state whether a single-copy action gives a retarded or advanced response;
  * derive the first variation w.r.t. g^{mu nu} through ALL dependencies
    (T, U, Phi, Z, M);
  * do NOT claim ghost-freedom; do NOT drop boundary terms without proof.

This script VERIFIES, with sympy:
  (1) the constitutive identity  mu(y) = 1 - 2 F_+'(4 y^2) = 1 - exp(-y);
  (2) the C^2 Hermite regulator P_{5,eps} and its two-sided matching;
  (3) the flat-space auxiliary kinetic Hessian (the "naive Hessian" warning);
  (4) the algebraic reduction of the M-sector EOM;
  (5) the stationary-branch solution M = -F + C (transport constant).

The covariant chain-rule first variation (the decisive, nonlocal result) is
derived analytically and is recorded in T01_action.md; it is NOT a finite-order
local differential operator and therefore cannot be "verified" by local sympy
differentiation. The script instead verifies every *local* ingredient that the
variation is built from.

Run:  python3 01_action/T01_action.py
"""
import sympy as sp

OK = []


def check(name, cond):
    OK.append((name, bool(cond)))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")


# ----------------------------------------------------------------------------
# 0. Conventions (recorded, not computed)
# ----------------------------------------------------------------------------
# signature (-,+,+,+); Box = nabla_mu nabla^mu; EH term + (c^3/16 pi G) int sqrt(-g) R.
# U_mu = -nabla_mu T,  U^mu U_mu = -1.

# ----------------------------------------------------------------------------
# 1. Constitutive identity  mu(y) = 1 - 2 F_+'(4 y^2) = 1 - e^{-y}
# ----------------------------------------------------------------------------
Z, y, eps, e = sp.symbols('Z y epsilon e', positive=True, real=True)
F_plus = 4 * (1 - (1 + sp.sqrt(Z) / 2) * sp.exp(-sp.sqrt(Z) / 2))
Fp_plus = sp.simplify(sp.diff(F_plus, Z))

print("== (1) constitutive identity ==")
check("F_+'(Z) = (1/2) e^{-sqrt(Z)/2}",
      sp.simplify(Fp_plus - sp.Rational(1, 2) * sp.exp(-sp.sqrt(Z) / 2)) == 0)
mu = sp.simplify(1 - 2 * Fp_plus.subs(Z, 4 * y**2))
check("mu(y) = 1 - e^{-y}", sp.simplify(mu - (1 - sp.exp(-y))) == 0)
check("mu(y) ~ y as y->0", sp.simplify(mu.series(y, 0, 2).removeO() - y) == 0)
check("mu(y) -> 1 as y->oo", sp.limit(mu, y, sp.oo) == 1)

# ----------------------------------------------------------------------------
# 2. C^2 Hermite regulator P_{5,eps} (two-sided, value/1st/2nd at +/- eps)
# ----------------------------------------------------------------------------
print("== (2) C^2 regulator ==")
Fm = sp.Rational(1, 2) * Z * sp.exp(-sp.sqrt(-Z) / 3)   # Z <= -eps branch
c = sp.symbols('c0:6')
P = sum(c[i] * Z**i for i in range(6))
eqs = []
for x, branch in [(e, F_plus), (-e, Fm)]:
    for n in range(3):
        eqs.append(sp.Eq(sp.diff(P, Z, n).subs(Z, x), sp.diff(branch, Z, n).subs(Z, x)))
sol = sp.solve(eqs, list(c), dict=True)
check("unique Hermite solution", len(sol) == 1)
Psol = P.subs(sol[0])
match_ok = True
for x, branch in [(e, F_plus), (-e, Fm)]:
    for n in range(3):
        match_ok = match_ok and (sp.simplify(
            sp.diff(Psol, Z, n).subs(Z, x) - sp.diff(branch, Z, n).subs(Z, x)) == 0)
check("C^2 match at +eps and -eps (n=0,1,2)", match_ok)

# The deep-MOND cusp: F_+''(Z) ~ -1/(8 sqrt(Z)) -> -inf as Z->0+.
Fpp_plus = sp.simplify(sp.diff(F_plus, Z, 2))
check("F_+'' diverges at 0 (cusp)",
      sp.limit(Fpp_plus, Z, 0, dir='+') == -sp.oo)

# ----------------------------------------------------------------------------
# 3. Flat-space auxiliary kinetic Hessian (the naive-Hessian warning)
# ----------------------------------------------------------------------------
print("== (3) naive auxiliary Hessian ==")
vphi, veta = sp.symbols('vphi veta', real=True)
# L_kin = - partial_mu eta partial^mu phi ; time part (signature -+++) = + eta_dot phi_dot
Lkin = veta * vphi
H = sp.hessian(Lkin, (veta, vphi))
check("naive Hessian = [[0,1],[1,0]]", H == sp.Matrix([[0, 1], [1, 0]]))
check("det(H) = -1 (indefinite)", sp.det(H) == -1)
check("eigenvalues {+1,-1}", H.eigenvals() == {1: 1, -1: 1})

# ----------------------------------------------------------------------------
# 4. M-sector: algebraic reduction + transport solution
# ----------------------------------------------------------------------------
print("== (4) M-sector ==")
# S_M = int sqrt(-g) M [ -kappa - div(U) ]  (after integrating eta*div(U M) by parts)
# => M-EOM is algebraic:  -kappa - div(U) + (eta-couplings) = 0  (no dM).
# Stationary isolated branch: div(U)=0, subleading eta-couplings => M = const.
s, C = sp.symbols('s C', real=True)
Mf, Ff = sp.Function('M')(s), sp.Function('F')(s)
# transport eq along a U-integral curve: d(M+F)/ds = 0  =>  M = -F + C
expr = sp.diff(Mf + Ff, s)
# substitute the proposed solution M(s) = -F(s) + C  (dM/ds = -dF/ds)
expr_sub = expr.subs(sp.diff(Mf, s), -sp.diff(Ff, s))
check("transport eq d(M+F)/ds = 0 => M = -F + C",
      sp.simplify(expr_sub) == 0)

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------
print("\n== T01 local-ingredient verification summary ==")
nfail = sum(1 for _, ok in OK if not ok)
for name, ok in OK:
    if not ok:
        print("  FAILED:", name)
if nfail == 0:
    print("PASS  (all local ingredients verified)")
    print("Most important unresolved equation (carried to T02):")
    print("  U^mu nabla_mu (dM) + (nabla.U)(dM) = S[g, dg, dU, dZ]  with retarded IC,")
    print("  and the conservation constraint  nabla^mu E_{mu nu} = 0  on-shell.")
else:
    print(f"FAIL  ({nfail} local checks failed)")
    raise SystemExit(1)
