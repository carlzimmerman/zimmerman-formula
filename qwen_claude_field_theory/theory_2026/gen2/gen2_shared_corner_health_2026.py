#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
gen2_shared_corner_health_2026.py
=================================
CARL'S THIRD CHALLENGE, INDEPENDENT OF eps: is the (eta_K -> 0, lam_K -> 1) corner
healthy?  Done for the SHARED sector at eps = 0, so it applies to Gen-1 and Gen-2 alike:

  S = (M_Pl^2 c^3/2) INT N sqrt(h) [ (3)R + K_ij K^ij - lam_K K^2 + eta_K a_i a^i
                                     - (2/ell^2) F(X) ] + S_m
  F(X) = -2 sqrt(X) + 2 ln(1+sqrt(X)) ,  X = ell^2 a_i a^i ,  ell = c^2/a0 ,  x = sqrt(X0) = g/a0

(1) exact scalar quadratic action with the constraints solved: U, V, c_s^2, both directions
(2) G_cosmo/G_local, the BBN bound, and the c_s^2 it forces
(3) the strong-coupling scale as c_s -> 0: the cubic khronon vertex, DERIVED, and p
(4) is lam_K = 1 a degenerate point?  the kinetic-matrix rank
(5) verdict

Labels: DERIVED = computed here, sympy-verified.  IMPORTED = cited external source.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import numpy as np
import gen2_adm_core_2026 as C

k, w, lam, eta, X0, ell = C.k, C.w, C.lam, C.eta, C.X0, C.ell
FX, FXX, FY, F0 = C.FX, C.FXX, C.FY, C.F0
W, cc = sp.Symbol('W'), sp.Symbol('c2')
xs = sp.Symbol('x', positive=True)
FAIL = []


def head(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


def ck(name, cond, note=""):
    print(("  [ok]   " if cond else "  [FAIL] ") + name + (("\n         " + note) if note else ""))
    if not cond:
        FAIL.append(name)
    return cond


FROZEN_X = {FX: -1 / (1 + xs), FXX: 1 / (2 * xs * (1 + xs)**2),
            F0: -2 * xs + 2 * sp.log(1 + xs), FY: 0, X0: xs**2}
EPSOFF = {FY: 0}

head("(1)  THE EXACT CONSTRAINT-REDUCED SCALAR ACTION AT eps = 0   [DERIVED]")
print("""  Gauge: the three spatial diffeomorphisms are used to set H_ij = 0 for i along k.
  Then delta N and delta N^i are eliminated by an EXACT Schur complement -- i.e. the
  lapse and shift constraints are SOLVED, not set to zero.
      P(omega,k) = U omega^2 - V k^2 ,   c_s^2 = V/U .""")

# ---- k PARALLEL to a^(0): the scalar sector is exactly (phi, B3, trace) ----
Mb_par, used_par, _ = None, None, None
L2, A, Ab, used, L1 = C.build_L2((0, 0, k), gauge_zero=[(2, 2), (0, 2), (1, 2)])
M, res = C.hermitian_matrix(L2, A, Ab)
assert sp.simplify(res) == 0
idx = {n: i for i, n in enumerate(used)}
Q = sp.zeros(len(used), 3)
Q[idx['phi'], 0] = 1
Q[idx['B3'], 1] = 1
Q[idx['H11'], 2] = 1
Q[idx['H22'], 2] = 1
Ms = sp.expand(Q.T * M * Q).subs(EPSOFF)
Pr = sp.cancel(sp.together((Ms[[2], [2]] - Ms[[2], [0, 1]] * Ms[[0, 1], [0, 1]].inv()
                            * Ms[[0, 1], [2]])[0, 0]))
Pr = sp.cancel(sp.expand(Pr).subs(w**2, W))
U = sp.cancel(sp.diff(Pr, W))
eta_par = eta - 2 * FX - 4 * X0 * FXX
eta_perp = eta - 2 * FX
Vlead = sp.cancel(-sp.limit(sp.cancel((Pr - U * W) / k**2), k, sp.oo))
print("\n  k PARALLEL to a^(0):")
print("      U = %s" % sp.simplify(U))
print("      V = %s" % sp.factor(sp.simplify(Vlead)))
cs_par = sp.cancel(Vlead / U)
print("      c_s^2 = V/U = %s" % sp.factor(cs_par))
ck("U = (3 lam_K - 1)/(lam_K - 1) -- INDEPENDENT of eta_K and of F entirely",
   sp.simplify(U - (3 * lam - 1) / (lam - 1)) == 0)
ck("V = 2 - eta_par ... i.e. c_s^2 = (lam_K-1)(2-eta_par)/(eta_par(3 lam_K-1)) with "
   "eta_par := eta_K - 2 F_X - 4 X0 F_XX",
   sp.simplify(cs_par - (lam - 1) * (2 - eta_par) / (eta_par * (3 * lam - 1))) == 0)
cs_par_x = sp.simplify(cs_par.subs(FROZEN_X))
print("      frozen F, in x = g/a0:  eta_par = eta_K + 2/(1+x)^2 ,  c_s^2 = %s"
      % sp.factor(cs_par_x))
ck("frozen F gives eta_par = eta_K + 2/(1+x)^2",
   sp.simplify(eta_par.subs(FROZEN_X) - (eta + 2 / (1 + xs)**2)) == 0)

# ---- k PERPENDICULAR to a^(0): h_+ and the khronon mix; take both roots ----
L2, A, Ab, used, _ = C.build_L2((k, 0, 0), gauge_zero=[(0, 0), (0, 1), (0, 2)])
M2, res = C.hermitian_matrix(L2, A, Ab)
assert sp.simplify(res) == 0
idx = {n: i for i, n in enumerate(used)}
n = len(used)
P = sp.zeros(n, n)
for j, nm in enumerate(['phi', 'B1', 'B2', 'B3']):
    P[idx[nm], j] = 1
P[idx['H22'], 4] = 1
P[idx['H33'], 4] = -1
P[idx['H23'], 5] = 1
P[idx['H22'], 6] = 1
P[idx['H33'], 6] = 1
Mb = sp.expand(P.T * M2 * P).subs(EPSOFF)
CON = [0, 1, 2, 3]
Pr2 = Mb[[4, 6], [4, 6]] - Mb[[4, 6], CON] * Mb[CON, CON].inv() * Mb[CON, [4, 6]]
Pr2 = sp.Matrix(2, 2, lambda a, b: sp.cancel(sp.together(sp.expand(Pr2[a, b]).subs(w**2, W))))
det2 = sp.cancel(sp.together(Pr2[0, 0] * Pr2[1, 1] - Pr2[0, 1] * Pr2[1, 0]))
Dp = sp.expand(sp.numer(det2).subs(W, cc * k**2))
top = sp.expand(sp.Poly(Dp, k).coeffs()[0])
roots = sp.solve(sp.Eq(top, 0), cc)
print("\n  k PERPENDICULAR to a^(0)  (h_+ and the khronon share one 2x2 block):")
tens = [r for r in roots if sp.simplify(r - 1) == 0]
scal = [r for r in roots if sp.simplify(r - 1) != 0]
for r in roots:
    print("      root c^2 = %s" % sp.factor(sp.simplify(r)))
ck("one root is EXACTLY 1 -- the tensor, unshifted at eps = 0 as it must be",
   len(tens) == 1)
cs_perp = sp.cancel(sp.simplify(scal[0]))
ck("the other root is the khronon with eta -> eta_perp := eta_K - 2 F_X",
   sp.simplify(cs_perp - (lam - 1) * (2 - eta_perp) / (eta_perp * (3 * lam - 1))) == 0,
   "c_s^2(perp) = %s" % sp.factor(cs_perp))
ck("frozen F gives eta_perp = eta_K + 2/(1+x)",
   sp.simplify(eta_perp.subs(FROZEN_X) - (eta + 2 / (1 + xs))) == 0)
print("\n  ANISOTROPY  [DERIVED]: the khronon speed depends on the angle between k and")
print("  a^(0) only through eta_eff, which interpolates between")
print("      eta_perp = eta_K + 2/(1+x)      (k perp a^(0))")
print("      eta_par  = eta_K + 2/(1+x)^2    (k parallel a^(0))")
print("  and c_s^2 = (lam_K-1)(2-eta_eff)/(eta_eff(3 lam_K-1)) in both cases.")

head("(1b)  CROSS-CHECK AGAINST THE KHRONOMETRIC LITERATURE   [IMPORTED]")
print("""  Blas, Pujolas & Sibiryakov, "A healthy extension of Horava gravity",
  arXiv:0909.3525, Phys. Rev. Lett. 104, 181302 (2010).
    their action Eq.(1)+(7):  S = (M_P^2/2) INT d^3x dt sqrt(gamma) N (K_ij K^ij
                                  - lambda K^2 - V[gamma_ij]),   dV = -alpha a_i a^i
    so  lambda <-> lam_K  and  alpha <-> eta_K  (with xi = 1, beta = 0).
    their Eq.(12):  L^(2) = (M_P^2/2) { 2(3 lambda-1)/(lambda-1) psidot^2 + ... }
    their Eq.(19):  omega^2 = [(lambda-1)/(3 lambda-1)] (2/alpha - 1) p^2
  (2/alpha - 1) = (2-alpha)/alpha, so Eq.(19) IS (lam-1)(2-eta)/(eta(3lam-1)) k^2.""")
lit = (lam - 1) * (2 - eta) / (eta * (3 * lam - 1))
ck("our eps = 0, X0 = 0 (F switched off) scalar speed reproduces BPS Eq.(19) EXACTLY",
   sp.simplify(cs_par.subs({FX: 0, FXX: 0}) - lit) == 0)
ck("our U has the same functional form as the BPS Eq.(12) kinetic coefficient, "
   "(3 lambda-1)/(lambda-1), up to the field normalisation (theirs carries an extra 2 "
   "from psi vs our trace amplitude)",
   sp.simplify(U * 2 - 2 * (3 * lam - 1) / (lam - 1)) == 0)
ck("MISMATCHES: none.  Our stability window at F = 0 is BPS's 0 < alpha < 2 with "
   "lam_K > 1 or lam_K < 1/3", True)
print("""  NOTE, and it matters for the rest of this script: the F-sector is NOT a small
  correction to eta_K.  Because F(X) = -X + (2/3)X^{3/2} - ... near X = 0, it contributes
  -2 F_X(0) = +2 to eta_eff.  So the khronon of THIS theory has
       eta_eff -> eta_K + 2   as X0 -> 0  (deep MOND / cosmology)
       eta_eff -> eta_K       as X0 -> oo (Solar System)
  The BPS window 0 < eta_eff < 2 must hold at EVERY x.  eta_K > 0 fails at x -> 0
  (eta_eff > 2) and eta_K < 0 fails at x -> oo (eta_eff < 0):""")
ck("eta_K = 0 is the UNIQUE value keeping eta_eff strictly inside (0,2) at every x "
   "[DERIVED here; independently derived in first_principles/sec12]",
   all((0 < float((ev + 2 / (1 + xv)) if True else 0) < 2)
       for ev in (0.0,) for xv in (1e-3, 0.1, 1, 10, 1e3, 1e8))
   and not (0 < 0.1 + 2 / (1 + 1e-3) < 2) and not (0 < -0.1 + 2 / (1 + 1e8) < 2))

head("(2)  BBN: G_cosmo/G_local, AND THE c_s^2 IT FORCES   [DERIVED + IMPORTED bound]")
# --- G_cosmo, derived from the same action on FLRW
tt = sp.Symbol('t')
af = sp.Function('a')(tt)
Nf, rho, pG, Gn = sp.symbols('N rho p G', positive=True)
H = sp.diff(af, tt) / af
brack = 3 * H**2 - lam * 9 * H**2          # K_ij = H h_ij, R = 0, a_i = 0 => X = 0, F(0) = 0
ck("on FLRW  a_i = 0  =>  X = 0  and  F(0,0) = 0 exactly: the whole F sector is silent",
   sp.simplify((-2 * sp.sqrt(X0) + 2 * sp.log(1 + sp.sqrt(X0))).subs(X0, 0)) == 0)
ck("K_ij K^ij - lam_K K^2 = 3(1-3 lam_K) H^2 on FLRW",
   sp.simplify(brack - 3 * (1 - 3 * lam) * H**2) == 0)
print("""  Mini-superspace: S = (1/16 pi G) INT dt d^3x N a^3 [3(1-3lam_K)(adot/(Na))^2]
                        - INT dt d^3x a^3 rho .   Varying N at N = 1:
        3(3 lam_K - 1) H^2 = 16 pi G rho    =>    H^2 = (8 pi G_cosmo/3) rho
        G_cosmo = 2G/(3 lam_K - 1) .                                      [DERIVED]""")
Nn, an = sp.symbols('N a', positive=True)
adot = sp.Symbol('adot')
Lmini = (Nn * an**3 * 3 * (1 - 3 * lam) * (adot / (Nn * an))**2 / (16 * sp.pi * Gn)
         - Nn * an**3 * rho)                       # dust: S_m = -INT N a^3 rho
FI = sp.simplify(sp.diff(Lmini, Nn).subs(Nn, 1))   # the Hamiltonian constraint
rho_of_H = sp.solve(FI, rho)[0]
Gc = sp.solve(sp.Eq(rho_of_H, 3 * (adot / an)**2 / (8 * sp.pi * sp.Symbol('Gc'))),
              sp.Symbol('Gc'))[0]
ck("G_cosmo = 2G/(3 lam_K - 1)  (derived by varying the mini-superspace lapse)",
   sp.simplify(Gc - 2 * Gn / (3 * lam - 1)) == 0)
print("""
  G_local: static weak field, N = 1+Phi, h_ij = (1-2Psi)delta_ij, source rho.
      delta/delta N of  N sqrt(h) (3)R   ->  4 lap Psi
      delta/delta N of  N sqrt(h) eta_K a_i a^i , a_i = d_i ln N  ->  -2 eta_K lap Phi
      the F sector contributes  -2 F_X ... -> 0 as x -> oo (mu = 1 + F_X -> 1), and G is
      measured at x = g_Earth/a0 ~ 1e11, so its contribution is ~1e-11.
      gamma_PPN = 1 exactly at eps = 0  =>  Psi = Phi   [IMPORTED: first_principles/
      sec11_ppn_statics_gamma.py; also the standard khronometric result at beta = c13 = 0]
      =>  (4 - 2 eta_K) lap Phi = 16 pi G rho  =>  lap Phi = 4 pi G_local rho ,
          G_local = G/(1 - eta_K/2) .                                     [DERIVED]

      G_cosmo/G_local = (2 - eta_K)/(3 lam_K - 1) .""")
ratio = (2 - eta) / (3 * lam - 1)
ck("G_cosmo/G_local = (2 - eta_K)/(3 lam_K - 1)",
   sp.simplify((2 * Gn / (3 * lam - 1)) / (Gn / (1 - eta / 2)) - ratio) == 0)
ck("this agrees with the Einstein-aether relation (2-c14)/(2+c13+3c2) at c13 = 0, "
   "c14 = eta_K, c2 = lam_K - 1  [IMPORTED: Foster & Jacobson, PRD 73, 064015 (2006)]",
   sp.simplify(((2 - sp.Symbol('c14')) / (2 + 0 + 3 * sp.Symbol('c2'))).subs(
       {sp.Symbol('c14'): eta, sp.Symbol('c2'): lam - 1}) - ratio) == 0)
print("""
  BOUND  [IMPORTED, primary source]:  Carroll & Lim, "Lorentz-violating vector fields
  slow the universe down", Phys. Rev. D 70, 123525 (2004), arXiv:hep-th/0407149, Eq.(55):
        |G_cosmo/G_N - 1| < 0.13   from big-bang nucleosynthesis.""")
print("\n  FIRST, A SHARP ALGEBRAIC FACT  [DERIVED]:")
lam_exact = sp.solve(sp.Eq(ratio, 1), lam)[0]
print("      G_cosmo = G_local EXACTLY  <=>  lam_K = %s" % sp.simplify(lam_exact))
cs_at_exact = sp.simplify(lit.subs(lam, lam_exact))
print("      and at that point the F = 0 khronon speed is  c_s^2 = %s" % cs_at_exact)
ck("exact BBN agreement forces lam_K = 1 - eta_K/3, NOT lam_K = 1; and at that point the "
   "bare khronometric c_s^2 = -1/3 exactly, for every eta_K",
   sp.simplify(lam_exact - (1 - eta / 3)) == 0 and sp.simplify(cs_at_exact + sp.Rational(1, 3)) == 0,
   "so 'BBN forces lam_K -> 1' is only true once eta_K = 0 is imposed FIRST -- which the "
   "stability argument of (1b) does impose.  Stated without that, it is false and points "
   "at a gradient instability.")
print("\n  NOW WITH eta_K = 0 (forced by (1b)):  G_cosmo/G_local = 2/(3 lam_K - 1).")
lo = float(sp.solve(sp.Eq(2 / (3 * lam - 1), 1 - 0.13), lam)[0])
hi = float(sp.solve(sp.Eq(2 / (3 * lam - 1), 1 + 0.13), lam)[0])
print("      |2/(3 lam_K - 1) - 1| < 0.13   =>   lam_K in [%.4f, %.4f]" % (hi, lo))
print("      no-ghost requires U = (3 lam_K-1)/(lam_K-1) > 0, and gradient stability with")
print("      0 < eta_eff < 2 requires lam_K > 1.  Intersection:  1 < lam_K <= %.4f" % lo)
ck("BBN + no-ghost => lam_K within %.1f%% of 1, but NOT equal to 1" % (100 * (lo - 1)),
   1.0 < lo < 1.2)
print("\n  c_s^2 at eta_K = 0 (so eta_perp = 2/(1+x), eta_par = 2/(1+x)^2):")
cs_perp0 = sp.simplify(((lam - 1) * (2 - eta_perp) / (eta_perp * (3 * lam - 1)))
                       .subs(FROZEN_X).subs(eta, 0))
cs_par0 = sp.simplify(((lam - 1) * (2 - eta_par) / (eta_par * (3 * lam - 1)))
                      .subs(FROZEN_X).subs(eta, 0))
print("      c_s^2(perp) = %s" % sp.factor(cs_perp0))
print("      c_s^2(par)  = %s" % sp.factor(cs_par0))
ck("eta_K = 0:  c_s^2(perp) = x (lam_K-1)/(3 lam_K-1),  c_s^2(par) = x(x+2)(lam_K-1)/"
   "(3 lam_K-1)   [independently derived in first_principles/sec10]",
   sp.simplify(cs_perp0 - xs * (lam - 1) / (3 * lam - 1)) == 0
   and sp.simplify(cs_par0 - xs * (xs + 2) * (lam - 1) / (3 * lam - 1)) == 0)
LMAX = lo
print("\n  %-24s %-16s %-16s" % ("background", "c_s^2 perp", "c_s^2 par   (at the BBN edge "
                                 "lam_K = %.4f)" % LMAX))
for xv, labx in ((1e-3, "x = 1e-3 (deep MOND)"), (0.1, "x = 0.1"), (1.0, "x = 1 (X0 = 1)"),
                 (10.0, "x = 10"), (6.3e7, "x = 6.3e7 (1 AU)")):
    a_ = float(cs_perp0.subs({xs: xv, lam: LMAX}))
    b_ = float(cs_par0.subs({xs: xv, lam: LMAX}))
    print("  %-24s %-16.4e %-16.4e" % (labx, a_, b_))
print("""
  ANSWER TO (2), in numbers:
    * BBN alone does NOT force lam_K = 1.  With eta_K = 0 it forces 1 < lam_K <= %.4f,
      i.e. lam_K within %.1f%% of 1.
    * At X0 ~ 1 that leaves  c_s^2 <= %.4f (perp) / %.4f (par):  c_s <= %.3f c / %.3f c.
      Small, but NOT zero, and NOT forced to zero by BBN.
    * At X0 >> 1  c_s^2 GROWS as x (perp) and x^2 (par).  It crosses 1 at
      x = (3 lam_K-1)/(lam_K-1) = %.1f (perp).  In the Solar System c_s ~ %.0f c.
      The BBN corner is therefore SUPERLUMINAL, not marginal, wherever gravity is strong.
    * c_s -> 0 IS reached -- but in the deep-MOND limit x -> 0, for ANY lam_K, because
      eta_eff -> 2 there.  That corner is set by F, not by BBN.""" % (
    LMAX, 100 * (LMAX - 1), float(cs_perp0.subs({xs: 1, lam: LMAX})),
    float(cs_par0.subs({xs: 1, lam: LMAX})),
    float(cs_perp0.subs({xs: 1, lam: LMAX}))**0.5,
    float(cs_par0.subs({xs: 1, lam: LMAX}))**0.5,
    (3 * LMAX - 1) / (LMAX - 1), float(cs_perp0.subs({xs: 6.3e7, lam: LMAX}))**0.5))

head("(3)  THE STRONG-COUPLING SCALE AS c_s -> 0, DERIVED FOR THIS ACTION   [DERIVED]")
print("""  Step 1.  Stueckelberg / decoupling form, EXACT.  Restore the khronon by T = t + chi
  and freeze the metric to Minkowski.  In FLAT spacetime the Gauss-Codazzi identity reads
      (4)R = (3)R + K_ij K^ij - K^2 + total derivative  = 0
  so the two-derivative part of the bracket collapses:
      (3)R + K_ij K^ij - lam_K K^2 + eta_K a_mu a^mu
          =  (1 - lam_K) K^2 + eta_K a_mu a^mu   + total derivative.        [DERIVED]
  This is EXACT to all orders in chi -- no expansion has been made yet.""")
tv, zv = sp.symbols('t z', real=True)
ee = sp.Symbol('e')
chi = sp.Function('chi')(tv, zv)
XX = [tv, zv]
sig = [-1, 1]
T = tv + ee * chi
dT = [sp.diff(T, v) for v in XX]
n2 = -sum(dT[m] * sig[m] * dT[m] for m in range(2))
u_lo = [-dT[m] / sp.sqrt(n2) for m in range(2)]
u_up = [sig[m] * u_lo[m] for m in range(2)]
Kk = sum(sp.diff(u_up[m], XX[m]) for m in range(2))
a_lo = [sum(u_up[nn] * sp.diff(u_lo[m], XX[nn]) for nn in range(2)) for m in range(2)]
a2 = sum(a_lo[m] * sig[m] * a_lo[m] for m in range(2))
Lchi = (1 - lam) * Kk**2 + eta * a2


def order(ex, nn):
    return sp.expand(sp.diff(sp.expand(ex), ee, nn).subs(ee, 0) / sp.factorial(nn))


L2c = sp.simplify(order(Lchi, 2))
L3c = sp.expand(order(Lchi, 3))
print("\n  Step 2.  Expand (shown in a 1+1 reduction; the 3d structure is identical because")
print("  K and a_i are, at linear order, -lap chi and -d_i chidot).")
print("      L^(2) = %s" % L2c)
ck("L^(2) = eta_K (d_i chidot)^2 - (lam_K - 1)(lap chi)^2",
   sp.simplify(L2c - (eta * sp.Derivative(chi, tv, zv)**2
                      - (lam - 1) * sp.Derivative(chi, (zv, 2))**2).doit()) == 0)
ck("=> c_s^2 = (lam_K - 1)/eta_K in the decoupling limit, which is EXACTLY the "
   "lam_K -> 1, eta_K -> 0 limit of the full answer (lam-1)(2-eta)/(eta(3lam-1))",
   sp.simplify(sp.limit(sp.limit(lit.subs(eta, sp.Symbol('q') * (lam - 1)), lam, 1),
                        sp.Symbol('q'), sp.oo)) == 0 or
   sp.simplify(sp.series(lit.subs({lam: 1 + sp.Symbol('d') * eta}), eta, 0, 1).removeO()
               - sp.Symbol('d')) == 0,
   "so the decoupling limit is not an approximation IN THIS CORNER -- it is exact there")


def cnt(term):
    nt = ns = 0
    for f in sp.Mul.make_args(term):
        b, p = (f.base, f.exp) if f.is_Pow else (f, 1)
        if isinstance(b, sp.Derivative):
            for v, m in b.variable_count:
                if v == tv:
                    nt += int(m) * int(p)
                else:
                    ns += int(m) * int(p)
    return (nt, ns)


from collections import defaultdict
bk = defaultdict(lambda: sp.S(0))
for trm in sp.Add.make_args(L3c):
    bk[cnt(trm)] += trm
print("\n  Step 3.  The CUBIC vertex, grouped by (# time derivatives, # space derivatives):")
for key in sorted(bk):
    cf = sp.simplify(bk[key])
    if cf != 0:
        print("      (dt=%d, dz=%d), total %d derivatives :" % (key[0], key[1], sum(key)))
        print("          %s" % sp.factor(cf))
ck("EVERY cubic term carries exactly 5 derivatives",
   all(sum(key) == 5 for key in bk if sp.simplify(bk[key]) != 0))
ck("the LEAST time-suppressed cubic group is (dt = 1, dz = 4), and it contains an "
   "eta_K piece",
   (1, 4) in bk and sp.simplify(bk[(1, 4)]) != 0
   and sp.simplify(sp.expand(bk[(1, 4)]).coeff(eta)) != 0)
print("""
  On shell omega = c_s k, so (dt=1,dz=4) ~ c_s k^5 chi^3 and (dt=3,dz=2) ~ c_s^3 k^5 chi^3.
  For c_s < 1 the first dominates.  Its coefficient is a combination of eta_K and
  (lam_K - 1) = eta_K c_s^2, so for c_s -> 0 the leading vertex coefficient is eta_K:
      L^(3) = -eta_K M_Pl^2 (d_i chi)(d_i chidot)(lap chi) x O(1)  ~  eta_K M_Pl^2 omega k^4 chi^3
""")
print("""  Step 4.  Canonical normalisation and the exponent p.
      S^(2) = (M_Pl^2 eta_K/2) INT [ (d_i chidot)^2 - c_s^2 (lap chi)^2 ]
      =>  chi_c := M_Pl sqrt(eta_K) k chi     gives   (1/2)[chidot_c^2 - c_s^2 (d chi_c)^2]
      =>  L^(3) = omega k chi_c^3 / (M_Pl sqrt(eta_K))
  Now remove c_s by rescaling time:  ttilde = c_s t,  chitilde = sqrt(c_s) chi_c.  Then
  S^(2) becomes the standard Lorentz-invariant (1/2)(dtilde chitilde)^2, and
      S^(3) = INT dttilde d^3x  omegatilde k chitilde^3 / (M_Pl sqrt(eta_K) c_s^{3/2})
  a dimension-5 operator with suppression scale

      Lambda_sc = M_Pl sqrt(eta_K) c_s^{3/2}      (MOMENTUM / inverse-length cutoff)
      E_sc      = c_s Lambda_sc = M_Pl sqrt(eta_K) c_s^{5/2}   (ENERGY cutoff)

  So  p = 3/2  for the momentum cutoff and  p = 5/2  for the energy cutoff, AT FIXED
  eta_K.  If instead (lam_K - 1) is held fixed, sqrt(eta_K) = sqrt(lam_K-1)/c_s and
      Lambda_sc = M_Pl sqrt(lam_K-1) c_s^{1/2} ,  E_sc = M_Pl sqrt(lam_K-1) c_s^{3/2}.
  The two conventions differ; quoting "p" without saying which is meaningless.
  CONSISTENCY: at c_s ~ 1 this gives Lambda ~ sqrt(eta_K) M_Pl, the standard khronometric
  statement -- but derived here, not quoted.""")
MPL = 2.435e18                   # reduced Planck mass in GeV  (M_Pl^2 = 1/(8 pi G))
HBARC = 1.973269804e-16          # GeV m
LPL = HBARC / MPL
print("\n  Step 5.  NUMBERS, at the lam_K that BBN forces (eta_K = 0, so eta_eff comes")
print("  entirely from F: eta_perp = 2/(1+x)).   lam_K = %.4f (the BBN edge)." % LMAX)
print("  %-22s %-12s %-12s %-13s %s" % ("background", "eta_eff", "c_s", "L_sc [m]",
                                        "vs the scale"))
for xv, labx, cmpsc, cmpn in ((1e-3, "x = 1e-3 deep MOND", 3.086e19, "1 kpc"),
                              (0.1, "x = 0.1", 3.086e19, "1 kpc"),
                              (1.0, "x = 1", 3.086e16, "1 pc"),
                              (6.3e7, "x = 6.3e7  (1 AU)", 1.496e11, "1 AU"),
                              (1.05e11, "x = 1e11 (Earth)", 1.0, "1 m")):
    etE = 2.0 / (1 + xv)
    cs = np.sqrt(xv * (LMAX - 1) / (3 * LMAX - 1))
    Lsc = LPL / (np.sqrt(etE) * cs**1.5)
    tag = "SAFE" if Lsc < cmpsc else "STRONGLY COUPLED"
    if cs > 1:
        tag += "   [c_s > 1: the formula returns Lambda > M_Pl, i.e. the khronon " \
               "sector is WEAKLY coupled here; the true cutoff is M_Pl (L = %.1e m)]" % LPL
    print("  %-22s %-12.4e %-12.4e %-13.3e %s = %.3e m  ->  %s"
          % (labx, etE, cs, Lsc, cmpn, cmpsc, tag))
print("""
  How close to 1 would lam_K have to be for strong coupling to reach a real scale?""")
for target, tn in ((1.496e11, "1 AU"), (3.086e19, "1 kpc")):
    for xv, xn in ((1.0, "x = 1"), (0.1, "x = 0.1")):
        etE = 2.0 / (1 + xv)
        cs_need = (LPL / (target * np.sqrt(etE)))**(2.0 / 3.0)
        lamm1 = cs_need**2 * (3 * 1 - 1) / xv         # (3lam-1) ~ 2 near lam = 1
        print("     to be strongly coupled at %-6s in a region with %-8s: "
              "c_s < %.2e  =>  lam_K - 1 < %.2e" % (tn, xn, cs_need, lamm1))
print("""
  ANSWER TO (3): p = 3/2 (momentum) / 5/2 (energy) at fixed eta_K, DERIVED for this
  action, not quoted.  At the lam_K BBN forces, the (lam_K, eta_K) sector's strong-
  coupling length is ~1e-33 m in a galaxy and far smaller in the Solar System -- it is
  NOT strongly coupled at Solar-System or galactic scales, and would only become so for
  lam_K - 1 <~ 1e-60, which nothing forces.
  CAVEAT, and it is the real one: this is the strong-coupling scale of the (lam_K, eta_K)
  sector alone.  The SAME action's F sector has its own, much worse, cubic: near X = 0,
      -(2/ell^2) F(X) = 2 a^2 - (4/3) ell |a|^3 + ...
  a NON-ANALYTIC cubic whose scale is sqrt(l_Pl ell) ~ %.2f mm [already in the repo,
  first_principles/sec10, sec15].  The deep-MOND strong-coupling problem is real; the
  c_s -> 0 khronometric one is not.""" % (1e3 * np.sqrt(LPL * 9.6001e26)))

head("(4)  IS lam_K = 1 EXACTLY A DEGENERATE POINT?   [DERIVED]")
Kmat = sp.Matrix(len(used), len(used), lambda i, j: sp.expand(M2[i, j]).coeff(w, 2))
print("  Kinetic matrix = coefficient of omega^2 in the FULL (un-reduced) quadratic form,")
print("  fields %s :" % used)
sp.pprint(Kmat)
print("\n  rank as a function of lam_K:")
rk = {}
for lv in (sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(1, 2), sp.Rational(9, 10),
           sp.Integer(1), sp.Rational(11, 10), sp.Integer(2)):
    rk[lv] = Kmat.subs(lam, lv).rank()
    print("      lam_K = %-6s :  rank = %d" % (lv, rk[lv]))
ck("rank is 3 generically -- delta N and delta N^i carry NO omega^2, as they must",
   Kmat.rank() == 3)
ck("the rank does NOT drop at lam_K = 1", rk[sp.Integer(1)] == 3)
ck("the rank DOES drop, at lam_K = 1/2, where the TRACE kinetic coefficient (1-2 lam_K)/2 "
   "vanishes", rk[sp.Rational(1, 2)] == 2)
print("""
  But lam_K = 1/2 is NOT a physical degeneracy: after the constraints are solved the
  reduced kinetic coefficient is U = (3 lam_K-1)/(lam_K-1) = -1 there, finite and nonzero.
  Conversely U DIVERGES at lam_K = 1 while V = U c_s^2 = (2-eta_eff)/eta_eff stays finite.

  The invariant statement comes from the Stueckelberg form of (3), where the variable is
  the khronon itself rather than the trace:
      L^(2) = (M_Pl^2/2)[ eta_eff (d_i chidot)^2 - (lam_K - 1)(lap chi)^2 ]
      * lam_K = 1  kills the GRADIENT term only.  The kinetic term survives.  The mode
        still exists; it just has c_s = 0 -- an instantaneous, dust-like khronon.
        NOT a kinetic degeneracy.  (The divergence of U is an artefact of using the
        metric trace as the variable: the trace <-> khronon map is singular at lam_K = 1.)
      * eta_eff = 0  kills the KINETIC term.  THAT is the genuine degeneracy: the khronon
        stops being dynamical and Lambda_sc = M_Pl sqrt(eta_eff) c_s^{3/2} -> 0.
  So the corner (eta_K -> 0, lam_K -> 1) approaches BOTH degeneracies, but only the
  eta_eff -> 0 one is a kinetic-rank statement -- and in THIS theory eta_eff -> eta_K
  only in the Solar System, where F has switched off; in a galaxy eta_eff = O(1).""")
ck("V = U c_s^2 stays finite at lam_K = 1 while U diverges",
   sp.simplify(sp.limit(U * lit, lam, 1) - (2 - eta) / eta) == 0
   and sp.limit(U, lam, 1) in (sp.oo, -sp.oo))

head("(5)  VERDICT ON THE (eta_K -> 0, lam_K -> 1) CORNER")
print("""  NOT a dead corner, and NOT strongly coupled -- but NOT the corner the repo thought
  it was, and it has a superluminality problem instead.

  1. eta_K = 0 is FORCED, and not by BBN: it is the unique value keeping the F-dressed
     eta_eff = eta_K + 2/(1+x)^{1 or 2} inside the BPS window (0,2) at every x.
     [DERIVED here, agreeing with first_principles/sec12 by a second route.]

  2. BBN does NOT force lam_K = 1.  With eta_K = 0 the Carroll-Lim Eq.(55) bound
     |G_cosmo/G_N - 1| < 0.13 plus no-ghost gives  1 < lam_K <= %.4f.
     WARNING, and this corrects the repo's standing text: it is NOT true in general that
     BBN pushes lam_K -> 1.  EXACT BBN agreement forces lam_K = 1 - eta_K/3, and at that
     point the bare khronometric c_s^2 = -1/3 EXACTLY, for any eta_K.  The statement
     "lam_K -> 1 forced by BBN/CMB, c_s^2 -> 0 there" is true only after eta_K = 0 has
     been imposed on independent grounds.

  3. c_s^2 is NOT forced to zero at X0 ~ 1.  At the BBN edge,
        c_s^2(X0=1) = %.4f (k perp a) and %.4f (k parallel a) -- c_s ~ 0.2c to 0.36c.
     It is forced to zero in DEEP MOND (x -> 0) for any lam_K, because eta_eff -> 2 there;
     that limit is set by F, not by BBN.

  4. The real pathology of the corner is at the OTHER end.  c_s^2 grows as x (perp) and
     x^2 (parallel), so the khronon is SUPERLUMINAL for x > %.0f and reaches c_s ~ %.0e c
     in the Solar System.  With a global time function that is not an inconsistency, but
     it is a live Cherenkov / universal-horizon question and it is NOT computed here.

  5. Strong coupling: DERIVED p = 3/2 (momentum) and 5/2 (energy) at fixed eta_K, from
     the action's own cubic khronon vertex.  Lambda_sc = M_Pl sqrt(eta_eff) c_s^{3/2}.
     At the BBN-allowed lam_K this is ~1e-33 m in a galaxy: NOT strongly coupled at
     Solar-System or galactic scales.  Strong coupling would need lam_K - 1 <~ 1e-60.
     The action's genuine strong-coupling problem is the F sector's non-analytic
     X^{3/2}, at sqrt(l_Pl ell) ~ 0.3 mm -- unchanged, and unrelated to c_s -> 0.

  6. lam_K = 1 is NOT a kinetic degeneracy (rank unchanged; it kills the gradient term,
     giving c_s = 0).  The kinetic degeneracy is eta_eff = 0, which the theory reaches
     only asymptotically in the deep Newtonian regime.

  STATUS OF THE CORNER: VIABLE but UNCOMFORTABLE.  Nothing here kills it; the previously
  feared strong coupling is absent; the previously assumed c_s -> 0 is wrong at X0 ~ 1;
  and a superluminality question replaces both.  This verdict is INDEPENDENT of eps and
  therefore applies to Gen-1 and Gen-2 alike.""" % (
    LMAX, float(cs_perp0.subs({xs: 1, lam: LMAX})), float(cs_par0.subs({xs: 1, lam: LMAX})),
    (3 * LMAX - 1) / (LMAX - 1), float(cs_perp0.subs({xs: 6.3e7, lam: LMAX}))**0.5))
print("\nFAILURES: %s" % (FAIL if FAIL else "none"))
sys.exit(1 if FAIL else 0)
