#!/usr/bin/env python3
# wf_j10_scalar_dispersion.py
# ---------------------------------------------------------------------------
# FINITE-k SCALAR-SECTOR DISPERSION of AeST, specialized to the EXPONENTIAL
# ("J10") kernel  J_Y = 1 - e^{-u},  u = sqrt(Y)/a0.
#
# LITERATURE ANCHOR (SOLID, transcribed with citation):
#   Skordis & Zlosnik, "Aether scalar tensor theory: Linear stability on
#   Minkowski space", arXiv:2109.13287v2, Phys. Rev. D 106, 104041 (2022).
#   Scalar sector: Eqs. (10),(22),(27),(28),(29),(30),(31),(58),(60),(61-63).
#
# This script (a) reconstructs det U [Eq.27], solves det U = 0, and CROSS-CHECKS
# the extracted c_s^2 and M^2 against the paper's Eq.(30) and Eq.(22);
# (b) Taylor-expands the given J10 at the Minkowski (Y=0) background to fix the
# background F-derivatives (lambda_s, K2 sector) that feed the dispersion;
# (c) specializes c_s^2, M^2, mu^2, k_*^2 to J10 and reports the
# no-ghost / gradient-stability band.  NO fabricated numbers: every symbol is
# either transcribed from the paper or derived here in sympy.
# ---------------------------------------------------------------------------
import sympy as sp

print("="*78)
print("AeST J10 scalar dispersion  --  sympy verification")
print("Literature: Skordis & Zlosnik 2021, arXiv:2109.13287 = PRD 106,104041")
print("="*78)

# ---- symbols -------------------------------------------------------------
KB, K2, Q0, lam, k, w = sp.symbols('K_B K2 Q0 lambda_s k omega', positive=True)
# (positive=True is a convenience for simplification; sign conditions handled explicitly)
KBs = sp.symbols('K_B', real=True)   # for range 0<KB<2 reasoning

# ---- Eq.(27): determinant of the 4x4 scalar coefficient matrix U ---------
# det U = 4 k^6 omega^2 [ (2-KB)((2+KB*lam)k^2 + 2 K2 Q0^2 (1+lam)) - 2 K2 KB omega^2 ]
detU = 4*k**6 * w**2 * ( (2-KB)*((2+KB*lam)*k**2 + 2*K2*Q0**2*(1+lam)) - 2*K2*KB*w**2 )
print("\n[Eq.27] det U =")
sp.pprint(sp.expand(detU))

# ---- solve det U = 0 for omega^2 -----------------------------------------
w2 = sp.symbols('omega2', real=True)
detU_w2 = detU.subs(w**2, w2)               # treat omega^2 as the unknown
# the non-trivial (propagating) branch: bracket = 0
bracket = (2-KB)*((2+KB*lam)*k**2 + 2*K2*Q0**2*(1+lam)) - 2*K2*KB*w2
sol = sp.solve(sp.Eq(bracket, 0), w2)
w2_prop = sp.simplify(sol[0])
print("\n[det U = 0 -> propagating branch] omega^2 =")
sp.pprint(w2_prop)

# extract coefficient of k^2 (=c_s^2) and the k-independent part (=M^2)
w2_poly = sp.Poly(sp.expand(w2_prop), k)
cs2_derived = sp.simplify(w2_poly.coeff_monomial(k**2))
M2_derived  = sp.simplify(w2_poly.coeff_monomial(1))
print("\n  c_s^2 (coeff of k^2, DERIVED from det U):")
sp.pprint(cs2_derived)
print("  M^2 (k-independent part, DERIVED from det U):")
sp.pprint(M2_derived)

# ---- paper's quoted values -----------------------------------------------
cs2_paper = (2-KB)/(K2*KB) * (1 + sp.Rational(1,2)*KB*lam)     # Eq.(30)
M2_paper  = (2-KB)*(1+lam)*Q0**2/KB                            # Eq.(22)
print("\n[Eq.30] paper c_s^2 = (2-K_B)/(K2 K_B) * (1 + (1/2) K_B lambda_s):")
sp.pprint(cs2_paper)
print("[Eq.22] paper M^2   = (2-K_B)(1+lambda_s) Q0^2 / K_B:")
sp.pprint(M2_paper)

chk_cs = sp.simplify(cs2_derived - cs2_paper)
chk_M  = sp.simplify(M2_derived  - M2_paper)
print("\n  CROSS-CHECK c_s^2 (derived - paper) =", chk_cs, "  -> ", "MATCH" if chk_cs==0 else "MISMATCH")
print("  CROSS-CHECK M^2  (derived - paper) =", chk_M,  "  -> ", "MATCH" if chk_M==0 else "MISMATCH")

# ---- mu^2 [Eq.58] and k_*^2 [Eq.60] --------------------------------------
mu2   = 2*K2*Q0**2/(2-KB)                 # Eq.(58)
kstar2= (1+lam)/lam * mu2                 # Eq.(60)
print("\n[Eq.58] mu^2   = 2 K2 Q0^2/(2-K_B):"); sp.pprint(mu2)
print("[Eq.60] k_*^2  = (1+lambda_s)/lambda_s * mu^2:"); sp.pprint(kstar2)

print("\n" + "="*78)
print("SPECIALIZE TO J10:  J = a0^2[ u^2 + 2(1+u)e^{-u} - 2 ],  u = sqrt(Y)/a0")
print("="*78)

# ---- background F-derivatives from the given J10 -------------------------
a0, u, Y = sp.symbols('a0 u Y', positive=True)
Jexpr = a0**2*( u**2 + 2*(1+u)*sp.exp(-u) - 2 )

# J_Y via chain rule: Y = a0^2 u^2  => dY = 2 a0^2 u du
dJdu = sp.diff(Jexpr, u)
dYdu = 2*a0**2*u
JY = sp.simplify(dJdu/dYdu)
print("\nJ_Y = dJ/dY =")
sp.pprint(JY)                              # expect 1 - e^{-u}
print("  -> J_Y(u->0) =", sp.limit(JY, u, 0), " (deep-MOND: mu->0)")
print("  -> J_Y(u->oo)=", sp.limit(JY, u, sp.oo), " (Newtonian: mu->1)")

# small-Y (small-u) expansion of J: identify the leading powers
Jser = sp.series(Jexpr, u, 0, 6).removeO()
print("\nsmall-u expansion of J (u=sqrt(Y)/a0):")
sp.pprint(sp.expand(Jser))
# rewrite in Y
Jser_Y = Jser.subs(u, sp.sqrt(Y)/a0)
print("  in terms of Y:")
sp.pprint(sp.simplify(Jser_Y))

# background F-derivative that feeds the QUADRATIC action:
# F = (2-KB) J(Y,Q0) - 2 K(Q);  the ONLY J-piece entering delta^2 S is the
# coefficient of the term LINEAR in Y  (because Y ~ |grad phi|^2 is already 2nd order)
# => F_Y(0,Q0) = (2-KB) * J_Y(0)  => lambda_s = J_Y(0).
lam_s_J10 = sp.limit(JY, u, 0)
print("\n  F_Y(0,Q0) = (2-K_B) J_Y(0)  =>  lambda_s(J10) = J_Y(0) =", lam_s_J10)

# J_YY behaviour at Y->0 (shows non-analyticity of the exponential kernel)
JYY = sp.simplify(sp.diff(JY, u)/dYdu)
print("  J_YY =", JYY)
print("  J_YY(u->0) =", sp.limit(JYY, u, 0), " (DIVERGES: |Y|^{3/2} non-analytic kernel)")

# ---- specialization lambda_s -> 0 ----------------------------------------
print("\n" + "-"*78)
print("J10 SPECIALIZATION  (lambda_s = 0):")
print("-"*78)
cs2_J10 = sp.simplify(cs2_paper.subs(lam, 0))
M2_J10  = sp.simplify(M2_paper.subs(lam, 0))
print("  c_s^2(J10) = (2-K_B)/(K2 K_B) =")
sp.pprint(cs2_J10)
print("  M^2(J10)   = (2-K_B) Q0^2/K_B =")
sp.pprint(M2_J10)
print("  mu^2(J10)  = 2 K2 Q0^2/(2-K_B)  (unchanged) =")
sp.pprint(mu2)
kstar2_lim = sp.limit(kstar2, lam, 0, '+')
print("  k_*^2(J10) = lim_{lambda_s->0+} (1+lambda_s)/lambda_s * mu^2 =", kstar2_lim)

# ---- ratio c_s^2 / (mu^2/Q0^2) etc, useful identities --------------------
print("\n  identity check:  c_s^2 * mu^2  =")
sp.pprint(sp.simplify(cs2_J10*mu2))
print("  ->  c_s^2 = M^2 / (2 K2 Q0^2/(2-KB)) * ... ; relation c_s^2 = M^2/(mu^2) * (2-KB)^2/(...)")
rel = sp.simplify(cs2_J10 / (M2_J10))
print("  c_s^2 / M^2 (J10) = 1/(K2 Q0^2) =")
sp.pprint(rel)

# ---- stability band summary ----------------------------------------------
print("\n" + "="*78)
print("STABILITY BAND  (J10, lambda_s=0),  aH << k :")
print("="*78)
print("""
 PROPAGATING massive scalar mode  omega^2 = c_s^2 k^2 + M^2 :
   no-ghost      : kinetic coeff |P_chi|^2/(8 K2) > 0     <=>  K2 > 0        [Eq.62]
   gradient-stab : c_s^2 = (2-K_B)/(K2 K_B) > 0           <=>  K2>0, 0<K_B<2 [Eq.61,31]
   non-tachyonic : M^2   = (2-K_B) Q0^2/K_B > 0           <=>  0<K_B<2       [Eq.22]
   => HEALTHY at ALL k for 0<K_B<2, K2>0.  c_s^2 finite & positive; no finite-k
      gradient/ghost instability that is absent at k->0.

 NON-PROPAGATING (omega=0) Y-mode  (Y = A0(k) t + B0(k)):
   linear-theory |P_Y|^2 sign in H flips at k_*^2=(1+lam_s)/lam_s * mu^2.
   For J10 (lam_s=0) -> k_*^2 -> +infinity : the LINEARIZED Hamiltonian is
   NOT positive-definite for any finite k (the known AeST low-k feature).
   The NONLINEAR MOND term J ~ (2/3a0)|Y|^{3/2}  (delta^3, invisible at
   quadratic order) restores boundedness for  k > mu  [Eqs.64-67,B31,B32].
   => residual Jeans-type non-positive Hamiltonian only for  k < mu ~< Mpc^-1
      (super-horizon/super-Mpc), i.e. the instability is at LOW k, NOT finite k.
""")
print("mu^-1 must exceed ~Mpc so MOND holds at galaxy (kpc) scales [SZ discussion].")
print("done.")
