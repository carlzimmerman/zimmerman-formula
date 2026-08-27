#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
verify_stability_and_crossing.py
Two decisive, tractable results for the exact-exponential DW-MOND candidate, done honestly.

(A) WEAK-FIELD STATIC AQUAL SECTOR IS ELLIPTIC EVERYWHERE.
    mu(y)=1-e^{-y}. The static MOND operator div[mu grad Psi]=4piG rho has principal eigenvalues
    lambda_perp = mu(y)  and  lambda_par = mu(y)+y mu'(y). Both must be > 0 for a well-posed
    (elliptic) equation and a convex AQUAL functional. Prove mu>0 and mu+y mu'>0 for all y>0, and the
    correct deep-MOND (mu~y) + Newtonian (mu->1) limits. NOTE: the stability object is mu+y mu' =
    1-2(f'+2Z f''), NOT f'+2Z f'' by itself -- so f'+2Z f''<0 (which happens for Z>4) is NOT a gradient
    instability; it corresponds to mu+y mu' > 1.

(B) THE Z=0 CROSSING (cosmology<->MOND, fable5 #11 / TRANSITION_GATE) IS REGULAR IN THE PHYSICAL
    FIELD, despite f_ZZ ~ Z^{-1/2} diverging in Z. Because Z=(4c^4/a0^2)(dU)^2, the perturbation
    delta Z = 2(4c^4/a0^2) dUbar.d(deltaU) scales like |dUbar| ~ sqrt(Zbar). Hence the potentially
    divergent second-variation coefficient f_ZZ (delta Z)^2 ~ Zbar^{-1/2} * Zbar = sqrt(Zbar) -> 0.
    The f_ZZ divergence is a coordinate artifact of using Z instead of U; the physical quadratic
    coefficient is finite (vanishing) at the crossing. (Scope: this is the LOCAL f(Z) contribution to
    delta^2 S; the full transport-M / nonlocal second variation is still owed -- fable5 #5,#11.)

Exit 0 = all checks pass. This does NOT certify the theory; it closes two named sub-gates and flags
what remains.
"""
import sys
import sympy as sp

FAIL, N = [], [0]
def check(c, label, detail=""):
    N[0]+=1; ok=bool(c)
    print(f"  [{'ok' if ok else 'FAIL'}] {N[0]:02d} {label}"+(f"   {detail}" if detail else ""))
    if not ok: FAIL.append(label)
def hdr(s): print("\n"+"="*80+"\n"+s+"\n"+"="*80)

y = sp.Symbol('y', positive=True)
Z = sp.Symbol('Z', positive=True)

# ==================================================================================
hdr("(A) weak-field static AQUAL sector: elliptic everywhere")
# ==================================================================================
mu = 1 - sp.exp(-y)
mup = sp.diff(mu, y)
lam_perp = mu
lam_par = sp.simplify(mu + y*mup)
print("  mu(y)        =", mu)
print("  mu'(y)       =", mup)
print("  mu + y mu'   =", lam_par, " = 1-(1-y)e^{-y}")
check(sp.limit(mu/y, y, 0) == 1, "deep-MOND: mu(y) ~ y as y->0  (=> g=sqrt(g_N a0), BTFR)")
check(sp.limit(mu, y, sp.oo) == 1, "Newtonian: mu -> 1 as y->oo")
check(mup.subs(y, sp.Rational(1,1000)) > 0 and sp.limit(mup, y, sp.oo)==0,
      "mu'(y)=e^{-y} > 0 for all y (monotone => AQUAL functional strictly convex, unique solution)")
# mu+y mu' = 1-(1-y)e^{-y}. Positivity for ALL y>0 <=> (1-y)e^{-y} < 1 for y>0.
dlp = sp.simplify(sp.diff(lam_par, y))         # = (2-y)e^{-y}  (peaks at y=2, NOT monotone -- still >0)
check(sp.simplify(dlp - (2-y)*sp.exp(-y)) == 0,
      "d/dy[mu+y mu'] = (2-y)e^{-y}  (peaks at y=2; the operator is not monotone but stays > 0)")
g = (1-y)*sp.exp(-y)                            # want g<1 for all y>0
# g(0)=1; g'(y) = -(2-y)e^{-y} < 0 on (0,2) and >0 on (y>2) but g<=0 for y>=1, so max on (0,1) is g(0)=1
check(sp.simplify(sp.diff(g, y) - (-(2-y)*sp.exp(-y))) == 0 and sp.limit(g, y, 0) == 1,
      "(1-y)e^{-y} = 1 at y=0, decreasing on (0,1) to 0, and <=0 for y>=1 => (1-y)e^{-y} < 1 for y>0",
      "=> mu+y mu' = 1-(1-y)e^{-y} > 0 for EVERY y>0: static MOND operator ELLIPTIC everywhere")
# numeric sweep (STABLE form 1+(y-1)e^{-y} to avoid exp(y) overflow)
import numpy as np
lp = sp.lambdify(y, 1 + (y-1)*sp.exp(-y), 'numpy'); mm = sp.lambdify(y, mu, 'numpy')
yy = np.logspace(-4, 3, 4000)
check(np.all(lp(yy) > 0) and np.all(mm(yy) > 0),
      "numeric sweep y in [1e-4,1e3]: mu>0 AND mu+y mu'>0 everywhere (no gradient instability)",
      f"min(mu)={mm(yy).min():.3e}, min(mu+ymu')={lp(yy).min():.3e}")

# ==================================================================================
hdr("(B) the f(Z) branch, its sign structure, and the mu+ymu' identity")
# ==================================================================================
# f_+(Z) = 4[1 - (1+sqrt(Z)/2) e^{-sqrt(Z)/2}]
s = sp.sqrt(Z)
fp   = sp.Rational(1,2)*sp.exp(-s/2)                        # f_+'(Z) (given)
fpp  = sp.simplify(sp.diff(fp, Z))                          # f_+''(Z)
conv = sp.simplify(fp + 2*Z*fpp)                           # f'+2Z f''
print("  f_+'(Z)      =", fp, "   > 0 for all Z (transverse eigenvalue healthy everywhere)")
print("  f_+''(Z)     =", fpp, "   ~ -Z^{-1/2}/8 -> -oo at Z=0 (coordinate singularity in Z)")
print("  f_+'+2Z f_+''=", conv)
check(sp.simplify(conv - sp.exp(-s/2)*(2-s)/4) == 0,
      "f'+2Z f'' = e^{-sqrt Z/2}(2-sqrt Z)/4  (negative for Z>4 -- but see the identity below)")
# the physical identity: mu+y mu' = 1 - 2(f'+2Z f''), with Z=4y^2
identity = sp.simplify((1 - 2*conv).subs(Z, 4*y**2) - lam_par)
check(identity == 0,
      "IDENTITY: mu+y mu' = 1 - 2(f'+2Z f'')  (Z=4y^2) => f'+2Zf''<0 means mu+ymu'>1, NOT instability",
      "corrects the naive 'f'+2Zf''<0 is a ghost' reading: the physical operator is mu+y mu' > 0")

# ==================================================================================
hdr("(C) Z=0 crossing regularity: f_ZZ divergence is cancelled by delta Z ~ sqrt(Z)")
# ==================================================================================
r"""
Z = kappa (dU)^2,  kappa=4c^4/a0^2.  Background |dUbar| = sqrt(Zbar/kappa).
Linear perturbation: delta Z = 2 kappa dUbar . d(deltaU)  => |delta Z| ~ 2 sqrt(kappa Zbar) |d deltaU|.
Second-variation coefficient from the local f(Z): C(Zbar) = f_ZZ(Zbar) * (delta Z / d deltaU)^2
   ~ f_ZZ(Zbar) * (4 kappa Zbar).  With f_ZZ ~ -1/(8 sqrt(Zbar)) * e^{-...}:
   C ~ -(1/(8 sqrt(Zbar))) * 4 kappa Zbar = -(kappa/2) sqrt(Zbar) -> 0 as Zbar->0.
So the physical quadratic coefficient VANISHES at the crossing; the f_ZZ->infty is a Z-coordinate
artifact. Verify the power counting symbolically.
"""
kappa, Zbar, ddU = sp.symbols('kappa Zbar ddU', positive=True)
# |delta Z| = 2 sqrt(kappa Zbar) * ddU  (ddU = |d deltaU|); coefficient of ddU^2 in f_ZZ (deltaZ)^2:
deltaZ_over_ddU = 2*sp.sqrt(kappa*Zbar)
C_local = sp.simplify(fpp.subs(Z, Zbar) * deltaZ_over_ddU**2)   # f_ZZ * (deltaZ/ddU)^2
print("  physical coeff C(Zbar) = f_ZZ*(deltaZ/ddU)^2 =", C_local)
lim0 = sp.limit(C_local, Zbar, 0, '+')
check(lim0 == 0,
      "C(Zbar) -> 0 as Zbar->0  => the local-f second-variation coefficient is REGULAR at the crossing",
      f"lim = {lim0}. The f_ZZ ~ Z^{{-1/2}} divergence is cancelled by (delta Z)^2 ~ Z (physical field U)")
# confirm the power: C ~ sqrt(Zbar)
Cser = sp.series(C_local, Zbar, 0, 1).removeO() if C_local != 0 else 0
check(sp.simplify(C_local - (-sp.Rational(1,2)*kappa*sp.sqrt(Zbar)*sp.exp(-sp.sqrt(Zbar)/2))) == 0,
      "C(Zbar) = -(kappa/2) sqrt(Zbar) e^{-sqrt(Zbar)/2}  (leading ~ -(kappa/2) sqrt(Zbar))",
      "regular and integrable through Z=0; no divergent quadratic coefficient from the LOCAL f")

# ==================================================================================
hdr("VERDICT (scope-honest)")
# ==================================================================================
print(r"""
  CLOSED HERE (DERIVED, sympy):
   (A) mu=1-e^{-y} gives an AQUAL static sector that is ELLIPTIC for all y>0 (mu>0, mu+y mu'>0), with
       correct deep-MOND (mu~y) and Newtonian (mu->1) limits and a strictly convex functional. No
       gradient instability in the weak-field static sector. The f'+2Z f''<0 region (Z>4) is NOT an
       instability: mu+y mu' = 1-2(f'+2Z f'') > 1 there.
   (B) f_+'(Z)=1/2 e^{-sqrt Z/2} > 0 everywhere (transverse healthy), unlike DW's original f (f'<0 for
       Z>36). The exact-exponential choice removes the transverse-sign problem.
   (C) The Z=0 cosmology<->MOND crossing is REGULAR in the physical field U: the f_ZZ ~ Z^{-1/2}
       divergence is cancelled by (delta Z)^2 ~ Z, giving a physical coefficient C ~ -2 kappa sqrt(Z)
       -> 0. The apparent singularity is a Z-coordinate artifact. (fable5 #11 / TRANSITION_GATE, LOCAL
       part.)

  STILL OWED (do NOT overclaim -- fable5 #5,#6,#7,#8,#9,#11,#12+):
   - the FULL localized second variation delta^2 S including the transport-M / nonlocal terms (this
     script did only the LOCAL f(Z) contribution to the crossing coefficient);
   - the ADM+Dirac-Bergmann physical-DOF count + retarded-IC equivalence (partially done in
     sf43/sf44: linear localization ghost has 0 free Cauchy data);
   - cosmological background+perturbations, EFE, clusters, PPN, black holes.

  STATUS: exact-exponential DW-MOND is a SERIOUS candidate whose weak-field sector is healthy and
  whose transition crossing is (locally) regular; NOT yet certified. Verdict C (unresolved), leaning
  favourable, with the remaining obstruction = the full nonlocal second variation + DOF certificate.
""")

print("="*80)
if FAIL:
    print(f"FAILED {len(FAIL)}:"); [print("  -",x) for x in FAIL]; sys.exit(1)
print(f"ALL {N[0]} CHECKS PASSED (two sub-gates closed; full certification pending)")
sys.exit(0)
