#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
wf_cs2_KB_causality_check.py
============================
TASK: independently CHECK the K_B-dependence of the AeST scalar characteristic
(sound) speed, and decide whether K_B >= 1 is (i) a causality (c_s<=c) condition,
(ii) a stability (c_s^2>0) condition, or (iii) not forced.  Specialize the general
SZ21 result to the exponential J10 kernel J_Y = 1 - e^{-u}, u = sqrt(Y)/a0(Q).

LITERATURE ANCHORS (fetched this session):
  * Skordis-Zlosnik 2021, PRL 127 161302 = arXiv:2007.00082 (ar5iv), scalar dispersion
    omega^2 = c_s^2 k^2 + M^2 with
        c_s^2 = (2 - K_B)/(K_2 K_B) * (1 + (1/2) K_B lambda_s)          [SZ21]
    vector dispersion omega^2 = k^2 + M_vec^2 (gradient coeff = 1, LUMINAL) with
        M_vec^2 = (2 - K_B)(1 + lambda_s) Q0^2 / K_B                    [SZ21]
    stability window 0 < K_B < 2, K_2 > 0, lambda_s > 0 (from lambda_s > -1).
    Background derivative defs: dF/dY = (2 - K_B) lambda_s,  d^2F/dQ^2 -> -4 K_2.
  * Mistele:  m_x = Q0 sqrt((2 - K_B)/(2 K_B))                          [Mistele Eq 21]
  * All 5 above are LITERATURE-INHERITED; this script verifies the ALGEBRA that turns
    them into the causality verdict, and does the J10 specialization myself.

Every printed conclusion is labelled SOLID / SUGGESTIVE / NOT-COMPUTED.
Run only.  Do NOT git commit.
"""
import sympy as sp

K_B, K_2, lam_s, Q0, mu, k, u = sp.symbols('K_B K_2 lambda_s Q0 mu k u', positive=True)

print("="*88)
print("1. THE SZ21 SCALAR SOUND SPEED AND ITS K_B DEPENDENCE  [formula: LITERATURE-INHERITED]")
print("="*88)
cs2 = (2 - K_B)/(K_2*K_B) * (1 + sp.Rational(1,2)*K_B*lam_s)
print("   c_s^2 =", cs2)

# (a) small-K_B scaling: does c_s^2 ~ 1/K_B?
lead = sp.limit(K_B*cs2, K_B, 0)          # coefficient of 1/K_B
print("\n   lim_{K_B->0} (K_B * c_s^2) =", sp.simplify(lead),
      "  => c_s^2 ~ (2/K_2)*(1/K_B) as K_B->0  [SOLID: c_s^2 ~ 1/K_B confirmed]")
print("   BUT the magnitude carries 1/K_2 too: the OVERALL normalization is set jointly")
print("   by K_B (aether Maxwell) AND K_2 (curvature of F in Q). Not K_B alone.")

# (b) sign / gradient stability
print("\n   gradient stability c_s^2 > 0 on 0<K_B<2, K_2>0, lambda_s>0 ?")
test = cs2.subs({K_B: sp.Rational(1,3), K_2: 2, lam_s: sp.Rational(1,2)})
print("     sample (K_B=1/3,K_2=2,lam_s=1/2): c_s^2 =", test, " > 0 =>",
      test > 0, "  [SOLID: stability needs 0<K_B<2, NOT K_B>=1]")

print("\n"+"="*88)
print("2. THE SUBLUMINALITY (c_s<=c) FLOOR ON K_B  [algebra derived here from the SZ21 formula]")
print("="*88)
# solve c_s^2 = 1 for K_B, general lambda_s
sol = sp.solve(sp.Eq(cs2, 1), K_B)
print("   c_s^2 = 1  =>  K_B =", [sp.simplify(s) for s in sol])
# at lambda_s = 0 (the J10 cosmological value, see part 4):
sol0 = sp.solve(sp.Eq(cs2.subs(lam_s, 0), 1), K_B)
print("   at lambda_s=0:  c_s^2 = (2-K_B)/(K_2 K_B) = 1  =>  K_B =", sol0,
      "= 2/(K_2+1)")
print("   => SUBLUMINALITY FLOOR  K_B >= 2/(K_2+1).   [SOLID algebra]")
print("      * K_2 = 1  gives  K_B >= 1   <-- the repo's schematic 'K_B>=1 for c_s<=c'")
print("      * K_2 > 1  gives floor < 1 ; K_2 >> 1 (CMB fits) gives floor ~ 2/K_2 << 1")
print("      * so 'K_B>=1' is the K_2=1 SLICE of a K_2-dependent floor, NOT universal.")
# monotonicity in lambda_s
dcs_dlam = sp.diff(cs2, lam_s)
print("   d c_s^2/d lambda_s =", sp.simplify(dcs_dlam), "> 0 on window => lambda_s>0 only")
print("   RAISES c_s^2 (helps superluminality), so lambda_s cannot rescue subluminality.")

print("\n"+"="*88)
print("3. EXACT IDENTITY c_s^2 <-> m_x, mu  [derived here from 3 literature formulas]")
print("="*88)
mx2 = (2 - K_B)*Q0**2/(2*K_B)                 # Mistele Eq 21 (squared)
mu2 = 2*K_2*Q0**2/(2 - K_B)                    # SZ21 mu^2 = 2 K_2 Q0^2/(2-K_B)
identity = 4*(mx2/mu2)/(2 - K_B)*(1 + sp.Rational(1,2)*K_B*lam_s)
print("   c_s^2 - [4 m_x^2/((2-K_B) mu^2)](1+K_B lam_s/2) =",
      sp.simplify(cs2 - identity), " (== 0) [SOLID]")
print("   => at small K_B, c_s^2 = 2 (m_x/mu)^2 : scalar SUBLUMINAL iff 1/m_x >= sqrt2/mu")
print("      i.e. the curl scale 1/m_x is no shorter than the Compton scale 1/mu.")

print("\n"+"="*88)
print("4. SPECIALIZE TO THE EXPONENTIAL J10 KERNEL  [derived here]")
print("="*88)
# J10:  J = a0^2 [ u^2 + 2(1+u) e^{-u} - 2 ],  u = sqrt(Y)/a0 ; K(Q) dark sector.
uu = sp.symbols('uu', nonnegative=True)
a0 = sp.symbols('a0', positive=True)
Jbracket = uu**2 + 2*(1+uu)*sp.exp(-uu) - 2
J = a0**2 * Jbracket
# J_Y = dJ/dY ; Y = (a0 u)^2 => dY = 2 a0^2 u du ; dJ/du = a0^2 * d(bracket)/du
dbr = sp.diff(Jbracket, uu)
J_Y = sp.simplify((a0**2*dbr)/(2*a0**2*uu))     # = (1/(2u)) d(bracket)/du
print("   J(Y=0):  bracket at u=0 =", Jbracket.subs(uu,0), " => J(0,Q)=0 identically in Q")
print("   J_Y(u) =", sp.simplify(J_Y))
print("   J_Y(u->0) =", sp.limit(J_Y, uu, 0), " ; J_Y(u->oo) =", sp.limit(J_Y, uu, sp.oo))
print("   SZ21:  dF/dY=(2-K_B)lambda_s and F=(2-K_B)J-2K  =>  lambda_s = J_Y.")
print("   => J10 gives  lambda_s = 1 - e^{-u}  in [0,1):")
print("        * cosmological / CMB background  (Y=0, u=0):   lambda_s = 0   [SOLID]")
print("        * deep-MOND / finite gradient    (0<u<1)   :   0<lambda_s<1")
print("        * Newtonian / solar system       (u->oo)   :   lambda_s -> 1")
# K_2 for J10: d^2F/dQ^2 = (2-K_B) J_QQ - 2 K_QQ ; at Y=0, J(0,Q)=0 for all Q => J_QQ=0
print("\n   K_2:  d^2F/dQ^2|_bg = -4 K_2.  Since J(0,Q)=0 for ALL Q (u=0 => bracket=0),")
print("         J_Q = J_QQ = 0 at Y=0, so d^2F/dQ^2|_bg = -2 K''(Q0) => K_2 = (1/2)K''(Q0).")
print("   => for J10 the cosmological c_s^2 is set ENTIRELY by the dark-energy sector:")
cs2_J10 = cs2.subs({lam_s: 0, K_2: sp.Symbol('Kpp')/2})   # Kpp = K''(Q0)
print("        c_s^2(J10, cosmological) = (2-K_B)/(K_2 K_B) =",
      sp.simplify(cs2_J10), "   with Kpp=K''(Q0)  [SOLID structural]")
print("        subluminality floor: K_B >= 2/(K_2+1) = 4/(K''(Q0)+2).")
print("        CMB pin mu^-1 >~ 1 Mpc forces K_2=K''/2 large => c_s^2 tiny (deeply subluminal),")
print("        so K_B>=1 is NOT needed for subluminality in any CMB-fitting J10 model.")

print("\n"+"="*88)
print("5. IN-FORCE UPPER BOUND ON K_B (repo, literature-anchored)")
print("="*88)
print("   * stability window itself:            K_B < 2         [SZ21]")
print("   * BBN (Oost et al.; Carroll-Lim He):  K_B <~ 0.25      [repo stage50, IN FORCE]")
print("   * PPN alpha_1 = -4 K_B => K_B<2.5e-5: WITHDRAWN (AeST sits on c_123=0 where the")
print("       Einstein-aether PPN series is inapplicable; VSZ give alpha_1=alpha_2=0). [repo stage70/74]")
print("   => the naive causality window K_B in [1,2) is EMPTIED by BBN (0.25 < 1) alone. [SOLID]")

print("\n   NOTE (NOT-COMPUTED): SZ21 c_s^2 is the COSMOLOGICAL-background value (K_2 = curvature")
print("   of F about the cosmological Q0). The LOCAL solar-system characteristic needs F's")
print("   second derivatives deep in the Newtonian regime (large u) -- NOT COMPUTED in the")
print("   corpus or here. The causality verdict for the LOCAL cone is therefore open.")
print("\nDONE.")
