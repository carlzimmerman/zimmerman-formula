#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERC3_symbolic.py -- adversarial re-derivation of Lane C3's Part A claims with an
INDEPENDENT and STRICTLY MORE GENERAL ansatz than the lane script used.

Attacks:
  V1  A.J = 0 identically -- proved on a GENERAL 1+1 metric with an OFF-DIAGONAL
      component g_tr (the lane only checked longitudinal gauge, diagonal), with the
      general exact unit-norm solution for A^0 at arbitrary tilt.
  V2  J = 0 on FLRW exactly.
  V3  delta J^0 = 0 at first order (longitudinal gauge), and the O(eps^2) piece of
      2(2-K_B) J.grad(phi) is NONZERO.
  V4  static limit: L_term = 2(2-K_B) J^mu d_mu phi equals + 2(2-K_B) grad(Phi).grad(phi)
      at leading order == -(2-K_B) * ( -2 grad(Phi).grad(phi) ), i.e. EXACTLY the
      committed Eq 6 transcription's cross term (AEST_SPHERICAL_COLLAPSE_SETUP.md:136,
      S = -int (2-K_B)/(16 pi Gt) [ |grad Phi|^2 - 2 grad Phi . grad phi + ... ]),
      sign AND coefficient.
  V5  EXCLUSIVITY: the OTHER phi-terms of Eq 5 (-(2-K_B) Y with Y = q^{mn} d_m phi d_n phi)
      produce NO Phi-phi cross term at quadratic order in the static untilted limit --
      so the Eq 6 cross term comes from the J-term ALONE ("EXACTLY" justified).
  V6  the shift current: for L16 = 2(2-K_B) J^mu w_mu - (2-K_B) Y - F(Y,Q)  (w_mu = d_mu phi),
      Js^mu = dL/dw_mu = 2(2-K_B) J^mu - 2(2-K_B) q^{mu nu} w_nu - 2 F_Y q^{mu nu} w_nu - F_Q A^mu.
      Check: A.(J-piece) = 0 and A.(q-pieces) = 0 exactly => the charge density n = -A.Js
      comes from F_Q ALONE; the J-term is PURE FLUX.  (This is the algebraic backbone of the
      lane's transport reading.)
"""
import sympy as sp

FAIL = []
def check(cond, label):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}")
    if not ok:
        FAIL.append(label)

t, r, eps, KB = sp.symbols("t r epsilon K_B", real=True)

# ---------- V1: GENERAL metric incl. off-diagonal, general tilt ----------
N  = sp.Function("N",  positive=True)(t, r)   # lapse-like
B  = sp.Function("B",  real=True)(t, r)       # OFF-DIAGONAL g_tr (lane had none)
h  = sp.Function("h",  positive=True)(t, r)   # spatial metric
wt = sp.Function("w",  real=True)(t, r)       # arbitrary (NOT small) tilt A^r = wt

gdd = sp.Matrix([[-N, B], [B, h]])
guu = gdd.inv()
X = (t, r)
Gam = [[[sp.simplify(sum(guu[m, s] * (sp.diff(gdd[s, al], X[be]) + sp.diff(gdd[s, be], X[al])
                                      - sp.diff(gdd[al, be], X[s])) for s in range(2)) / 2)
         for be in range(2)] for al in range(2)] for m in range(2)]

# exact unit-timelike A^0 at arbitrary tilt: g00 A0^2 + 2 g01 A0 w + g11 w^2 = -1
A0 = sp.symbols("A0v")
sols = sp.solve(sp.Eq(gdd[0, 0] * A0**2 + 2 * gdd[0, 1] * A0 * wt + gdd[1, 1] * wt**2, -1), A0)
A0 = sols[1]                                   # future-directed branch
Au = sp.Matrix([A0, wt])
Ju = sp.Matrix([sp.together(sum(Au[al] * (sp.diff(Au[m], X[al])
                                          + sum(Gam[m][al][be] * Au[be] for be in range(2)))
                                for al in range(2))) for m in range(2)])
AdotJ = sp.simplify(sum(gdd[m, n] * Au[m] * Ju[n] for m in range(2) for n in range(2)))
check(AdotJ == 0, "V1  A.J = 0 IDENTICALLY on a GENERAL metric (incl. g_tr != 0) at arbitrary "
                  "finite tilt -- stronger than the lane's diagonal-gauge check")

# ---------- V2/V3: longitudinal-gauge perturbative structure (independent rebuild) ----------
a  = sp.Function("a", positive=True)(t)
Ph = sp.Function("Phi", real=True)(t, r)
Ps = sp.Function("Psi", real=True)(t, r)
w1 = sp.Function("w1", real=True)(t, r)
dp = sp.Function("dphi", real=True)(t, r)
pb = sp.Function("phibar", real=True)(t)

gdd2 = sp.diag(-(1 + 2 * eps * Ph), a**2 * (1 - 2 * eps * Ps))
guu2 = gdd2.inv()
Gam2 = [[[sp.simplify(sum(guu2[m, s] * (sp.diff(gdd2[s, al], X[be]) + sp.diff(gdd2[s, be], X[al])
                                        - sp.diff(gdd2[al, be], X[s])) for s in range(2)) / 2)
          for be in range(2)] for al in range(2)] for m in range(2)]
A0e = sp.sqrt((1 + gdd2[1, 1] * (eps * w1)**2) / (1 + 2 * eps * Ph))
Au2 = sp.Matrix([A0e, eps * w1])
Ju2 = sp.Matrix([sum(Au2[al] * (sp.diff(Au2[m], X[al])
                                + sum(Gam2[m][al][be] * Au2[be] for be in range(2)))
                     for al in range(2)) for m in range(2)])

check(sp.simplify(Ju2.subs(eps, 0)) == sp.Matrix([0, 0]),
      "V2  J^mu = 0 EXACTLY on FLRW (eps=0)")

J0_1 = sp.simplify(sp.series(Ju2[0], eps, 0, 2).removeO().coeff(eps, 1))
check(J0_1 == 0, "V3a delta J^0 = 0 at first order (longitudinal gauge)")

term = 2 * (2 - KB) * (Ju2[0] * sp.diff(pb + eps * dp, t) + Ju2[1] * sp.diff(pb + eps * dp, r))
ser = sp.series(term, eps, 0, 3).removeO().expand()
check(sp.simplify(ser.coeff(eps, 0)) == 0 and sp.simplify(ser.coeff(eps, 1)) == 0,
      "V3b the term's O(1) and O(eps) pieces vanish on FLRW")
c2 = sp.simplify(ser.coeff(eps, 2))
check(c2 != 0, "V3c the O(eps^2) piece is NONZERO (term lives in the quadratic action => "
               "linear EOMs)  [matches lane A4b]")
print(f"        c2 = {c2}")

# ---------- V4: static limit vs the committed Eq 6 transcription ----------
Ju_st = Ju2.subs([(w1, sp.Integer(0)), (a, sp.Integer(1))])
L_term_st = 2 * (2 - KB) * (Ju_st[0] * sp.diff(eps * dp, t) + Ju_st[1] * sp.diff(eps * dp, r))
L_term_lead = sp.simplify(sp.series(L_term_st, eps, 0, 3).removeO().coeff(eps, 2))
eq6_cross = -(2 - KB) * (-2 * sp.diff(Ph, r) * sp.diff(dp, r))   # -(2-K_B)[ -2 grad Phi . grad phi ]
check(sp.simplify(L_term_lead - eq6_cross) == 0,
      "V4  leading static Lagrangian of the J-term == -(2-K_B)*(-2 dPhi dphi): the committed "
      "Eq 6 cross term, SIGN AND COEFFICIENT EXACT  [lane A3 'EXACTLY' verified]")

# ---------- V5: exclusivity -- the Y-term gives no cross term at this order ----------
w_mu = sp.Matrix([sp.diff(pb + eps * dp, t), sp.diff(pb + eps * dp, r)])
Au_st = Au2.subs([(w1, sp.Integer(0)), (a, sp.Integer(1))])
Ad_st = gdd2.subs([(a, sp.Integer(1))]) * Au_st
quu = sp.simplify(guu2.subs([(a, sp.Integer(1))]) + Au_st * Au_st.T)     # q^{mn} = g^{mn} + A^m A^n
Y = sp.expand(sum(quu[m, n] * w_mu[m] * w_mu[n] for m in range(2) for n in range(2)))
LY = sp.series(-(2 - KB) * Y, eps, 0, 3).removeO().coeff(eps, 2)
check(sp.diff(sp.expand(LY), sp.diff(Ph, r)) == 0 and sp.diff(sp.expand(LY), Ph) == 0,
      "V5  the -(2-K_B) Y term's quadratic static piece contains NO Phi coupling at all "
      "(pure |grad dphi|^2 + temporal pieces): the Eq 6 Phi-phi cross term is the J-term's ALONE")

# ---------- V6: the shift current decomposition (general tilted frame, V1 ansatz) ----------
wm = sp.Matrix([sp.symbols("w_t w_r", real=True)])                        # d_mu phi as free covector
wmv = sp.Matrix(sp.symbols("w_t w_r", real=True))
FY, FQ = sp.symbols("F_Y F_Q", real=True)
Auv, gddv = Au, gdd                                                       # from V1: general metric+tilt
guuv = gddv.inv()
Adv = gddv * Auv
quuv = sp.simplify(guuv + Auv * Auv.T)
Js_J = 2 * (2 - KB) * Ju                                                  # J-term piece (upper index)
Js_Y = -2 * (2 - KB) * quuv * wmv                                         # Y kinetic piece
Js_FY = -2 * FY * quuv * wmv                                              # F_Y piece
Js_FQ = -FQ * Auv                                                         # F_Q piece
dot = lambda V: sp.simplify((Adv.T * V)[0, 0])
check(dot(Js_J) == 0 and dot(Js_Y) == 0 and dot(Js_FY) == 0,
      "V6a A.(J-piece) = A.(q-pieces) = 0 EXACTLY (general metric, arbitrary tilt): the "
      "shift-charge density n = -A.Js is sourced by F_Q ALONE")
check(sp.simplify(dot(Js_FQ) - FQ) == 0,
      "V6b -A.(F_Q piece) = -F_Q*(A.A)*(-1)... => n = F_Q x (normalization): the dust charge "
      "is the F_Q sector's, untouched by the J-term  [lane A1 consequence verified]")

print()
if FAIL:
    print("FAILED:", *FAIL, sep="\n  - ")
    raise SystemExit(1)
print("VERC3_symbolic: ALL CHECKS PASSED")
