#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADVERSARIAL VERIFIER for svt_scalar_quasistatic_2026.py.

Independent re-derivation of the second-order dark-sector action INCLUDING the sqrt(-g)
measure and the FULL second-order pieces L_Q dQ^(2) + L_Y dY^(2) that the derivation
script's D1 Hessian omitted.  The dark-sector Lagrangian DENSITY is

    sqrt(-g) * [ (A(Q)/8piG) F(Y/A(Q)) + K(Q) + A_b B(Y/A(Q)) (Q-Q0)^2 ]

expanded to O(eps^2) around  phi = Qbar t + psibar(z),  A^mu = (A^0, eps a_x, 0, eps a_z),
Newtonian gauge  ds^2 = -(1+2ePhi)dt^2 + (1-2ePsi)dx^2,  A^0 solved exactly from A.A = -1.

Outputs, per block, BOTH the density-only Hessian (what the derivation script computed)
and the full sqrt(-g)-included Hessian, and diffs them.
"""
import sympy as sp

t, zc = sp.symbols("t z", real=True)
eps = sp.Symbol("e", positive=True)
Qb = sp.Symbol("Qbar", positive=True)
G, piG = sp.symbols("G piG", positive=True)

# perturbation SYMBOLS (pointwise Hessian; derivatives as independent symbols)
chid, chiz = sp.symbols("chidot chiz", real=True)   # chi_t, chi_z
ax, az, Ph, Ps = sp.symbols("a_x a_z Phi Psi", real=True)
pp = sp.Symbol("psip", positive=True)               # psibar'(z)

g_dd = sp.diag(-(1 + 2*eps*Ph), (1 - 2*eps*Ps), (1 - 2*eps*Ps), (1 - 2*eps*Ps))
g_uu = g_dd.inv()
sqrtg = sp.sqrt(-g_dd.det())

A0 = sp.sqrt((1 + (1 - 2*eps*Ps)*(eps**2*ax**2 + eps**2*az**2)) / (1 + 2*eps*Ph))
A_up = sp.Matrix([A0, eps*ax, 0, eps*az])

# independent cross-check of the unit norm
norm = sp.simplify((A_up.T * g_dd * A_up)[0, 0] + 1)
assert norm == 0, "A0 unit-norm FAILS"
print("[ok] unit norm A.A=-1 exact")

dphi = sp.Matrix([Qb + eps*chid, 0, 0, pp + eps*chiz])
Q = sum(A_up[m]*dphi[m] for m in range(4))
h_uu = g_uu + A_up*A_up.T
Y = sp.expand(sum(h_uu[m, n]*dphi[m]*dphi[n] for m in range(4) for n in range(4)))

# ---- independent order-by-order (cross-check of A3-A9) ----
Qs = sp.series(Q, eps, 0, 3).removeO()
Ys = sp.series(Y, eps, 0, 3).removeO()
Q0c, Q1, Q2 = [sp.expand(Qs.coeff(eps, i)) for i in range(3)]
Y0c, Y1, Y2 = [sp.expand(Ys.coeff(eps, i)) for i in range(3)]
print("Q0 =", Q0c, " | Y0 =", Y0c)
print("Q1 =", sp.simplify(Q1))
print("Y1 =", sp.simplify(Y1))
print("Q2 =", sp.simplify(Q2))
print("Y2 =", sp.simplify(Y2))
assert sp.simplify(Q1 - (chid - Qb*Ph + pp*az)) == 0, "A6 REFUTED"
assert sp.simplify(Y1 - (2*pp*chiz + 2*Ps*pp**2 + 2*Qb*pp*az)) == 0, "A4 REFUTED"
assert sp.diff(Y1, chid) == 0 and sp.diff(sp.diff(Y2, chid).subs({ax: 0, az: 0}), chid) == 0
assert sp.simplify(sp.diff(Y2, chid).subs({ax: 0, az: 0})) == 0, "A7 REFUTED"
print("[ok] A4/A6/A7 independently confirmed")

# ---- generic-derivative Lagrangian expansion, WITH and WITHOUT sqrt(-g) ----
LQ, LY, LQQ, LQY, LYY = sp.symbols("L_Q L_Y L_QQ L_QY L_YY", real=True)
dQ = sp.expand(eps*Q1 + eps**2*Q2)
dY = sp.expand(eps*Y1 + eps**2*Y2)
Ldens2 = sp.expand(LQ*dQ + LY*dY + sp.Rational(1, 2)*LQQ*dQ**2 + LQY*dQ*dY
                   + sp.Rational(1, 2)*LYY*dY**2)
Ldens2 = sp.expand(Ldens2).coeff(eps, 2)   # second-order part of the DENSITY

Lbar = sp.Symbol("Lbar", real=True)        # background L value (multiplies sqrt(-g) expansion)
sg = sp.series(sqrtg, eps, 0, 3).removeO()
sg0, sg1, sg2 = [sp.expand(sg.coeff(eps, i)) for i in range(3)]
print("sqrt(-g): 1 +", sg1, "e +", sp.simplify(sg2), "e^2")

Lfirst = LQ*Q1 + LY*Y1                     # first-order density
Lfull2 = sp.expand(Ldens2 + sg1*Lfirst + sg2*Lbar)   # full second-order LAGRANGIAN DENSITY

vars5 = [chid, chiz, Ph, az, Ps]
names = ["chid", "chiz", "Phi", "az", "Psi"]

H_script = sp.hessian(sp.expand(sp.Rational(1, 2)*LQQ*Q1**2 + LQY*Q1*Y1
                                + sp.Rational(1, 2)*LYY*Y1**2 + LY*chiz**2), vars5)
H_full = sp.hessian(Lfull2.subs({ax: 0}), vars5)     # a_x decouples from these 5

print("\n==== FULL Hessian (sqrt(-g) included, L_Q dQ2 + L_Y dY2 included) ====")
for i in range(5):
    print(" [" + ", ".join(str(sp.simplify(H_full[i, j])) for j in range(5)) + "]")
print("\n==== DIFF (full - script's D1) ====")
any_diff = False
for i in range(5):
    for j in range(i, 5):
        d = sp.simplify(H_full[i, j] - H_script[i, j])
        if d != 0:
            any_diff = True
            print(f"  H[{names[i]},{names[j]}]: script={sp.simplify(H_script[i,j])}  "
                  f"full={sp.simplify(H_full[i,j])}  DIFF={d}")
if not any_diff:
    print("  (none)")

# chi-chi 2x2 sub-block: is it affected?
print("\nchi-chi block diff:",
      [sp.simplify(H_full[i, j] - H_script[i, j]) for i in range(2) for j in range(2)])
