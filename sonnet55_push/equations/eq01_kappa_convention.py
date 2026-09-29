#!/usr/bin/env python3
"""eq01_kappa_convention.py -- put the framework's kappa and Milgrom's 1/2pi in ONE convention, and read the data in it.

The framework writes a0 = kappa * c * sqrt(G rho)          (kappa multiplies c*sqrt(G rho))
Milgrom writes    a0 = c H / (2 pi)                        (a number multiplies c*H)
Friedmann, rho = 3 H^2/(8 pi G), turns sqrt(G rho) into H*sqrt(3/(8 pi)), so the two conventions differ by exactly
the factor sqrt(8 pi/3) that the record's own Z carries.  E1-E4 state what that does to the comparison.
Exit 0 = every exact identity held and every quoted number was recomputed here.
"""
import math
import sys
import sympy as sp

ok = []
def check(cond, msg):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {msg}")

# ---- E1: exact identities -------------------------------------------------------------------------------
kap, c, G, rho, H = sp.symbols('kappa c G rho H', positive=True)
friedmann = sp.Eq(rho, 3 * H**2 / (8 * sp.pi * G))
a0_kappa = kap * c * sp.sqrt(G * rho)
a0_in_H = sp.simplify(a0_kappa.subs(rho, friedmann.rhs))
kap_M = sp.symbols('kappa_M', positive=True)
sol = sp.solve(sp.Eq(a0_in_H.subs(kap, kap_M), c * H / (2 * sp.pi)), kap_M)[0]
print("\n  E1  Milgrom's cH/2pi written as kappa*c*sqrt(G rho):")
print(f"      kappa_M = {sp.simplify(sol)}  = {float(sol):.6f}")
check(sp.simplify(sol - sp.sqrt(2 / (3 * sp.pi))) == 0, "E1a  kappa_M = sqrt(2/(3 pi)) exactly")
Zf, ZM = sp.sqrt(32 * sp.pi / 3), 2 * sp.pi
check(sp.simplify(Zf - sp.sqrt(sp.Rational(8, 3) * sp.pi) / sp.Rational(1, 2)) == 0,
      "E1b  Z = sqrt(8 pi/3) / kappa at kappa = 1/2, i.e. Z = 2*sqrt(8 pi/3): the 2 is 1/kappa, the sqrt(8 pi/3) is Friedmann")
check(sp.simplify((sp.Rational(1, 2) / sol)**2 - 3 * sp.pi / 8) == 0,
      "E1c  (kappa_framework / kappa_M)^2 = 3 pi / 8 exactly   (=> Z_M^2 / Z^2 = 3 pi/8)")
gap = math.log(float(ZM / Zf))
print(f"      ln(Z_M/Z) = {gap:.4f}  -> the '8.2% gap' between the two constants is this one number")
check(abs(gap - 0.0819) < 5e-4, "E1d  the record's 8.2% gap = ln(2 pi / Z) recomputed")

# ---- E2: what the data give for kappa, in each footing ----------------------------------------------------
c_, G_ = 2.99792458e8, 6.674e-11
H0 = 67.4e3 / 3.0856775814913673e22
OmL = 0.685
rho_tot = 3 * H0**2 / (8 * math.pi * G_)
a0_best, sig = 1.0766e-10, 0.0544          # SPARC profile likelihood, Upsilon free, galaxy-clustered (the committed run)
kap_tot = a0_best / (c_ * math.sqrt(G_ * rho_tot))
kap_lam = a0_best / (c_ * math.sqrt(G_ * OmL * rho_tot))
kM, kF = float(sol), 0.5
print("\n  E2  the SPARC a0 (1.0766e-10, 5.44% clustered) converted to kappa in each footing:")
print(f"      {'footing':<28}{'kappa_hat':>10}{'+-':>8}{'framework 1/2':>16}{'Milgrom 0.4607':>17}")
for nm, kh in (("rho_total  (cH0)", kap_tot), ("rho_Lambda (cH_Lambda)", kap_lam)):
    s = kh * sig
    print(f"      {nm:<28}{kh:>10.4f}{s:>8.4f}{(kF-kh)/s:>+14.2f} s{(kM-kh)/s:>+15.2f} s")
check(abs(kap_tot - 0.4757) < 2e-3 and abs(kap_lam - 0.5755) < 2e-3, "E2a  kappa_hat = 0.476 (rho_total) and 0.575 (rho_Lambda) recomputed")
check(abs(kap_tot - kM) < abs(kap_tot - kF), "E2b  on the rho_total footing SPARC's kappa is CLOSER to Milgrom's 0.4607 than to the framework's 1/2")
print("      The published BTFR kappa = 0.465 +- 0.076 sits", f"{(0.465-kM)/0.076:+.2f} sigma from 0.4607 and {(0.465-kF)/0.076:+.2f} sigma from 1/2.")

# ---- E3: one family for both footings -----------------------------------------------------------------------
print("\n  E3  one family: a0 = kappa * c * H0 * sqrt(Omega_X) / sqrt(8 pi/3),  X in {tot (Omega=1), Lambda (Omega=0.685)}")
for nm, Om in (("tot", 1.0), ("Lambda", OmL)):
    for kn, kv in (("1/2", 0.5), ("sqrt(2/3pi)", kM)):
        print(f"      X={nm:<7} kappa={kn:<12} a0 = {kv * c_ * H0 * math.sqrt(Om) / math.sqrt(8 * math.pi / 3):.4e}")
check(abs(0.5 * c_ * H0 * math.sqrt(OmL) / math.sqrt(8 * math.pi / 3) - 9.36e-11) < 2e-13, "E3a  canonical 9.36e-11 recomputed")
check(abs(kM * c_ * H0 / math.sqrt(8 * math.pi / 3) - 1.0421e-10) < 5e-14, "E3b  Milgrom's own cH0/2pi = 1.0421e-10 recomputed")

# ---- E4: cosmic-scale kernel argument, footing-explicit ---------------------------------------------------
print("\n  E4  the kernel argument at Hubble scale, y_H = a0 / (c H0):")
for nm, Om in (("Lambda", OmL), ("tot", 1.0)):
    yH = 0.5 * math.sqrt(Om) / math.sqrt(8 * math.pi / 3)
    print(f"      footing {nm:<7} a0/(cH0) = {yH:.5f}   (cH0/a0)^2 = {1/yH**2:.2f}   sqrt(1 + a0/(cH0)) = {math.sqrt(1+yH):.4f}")
check(abs((1 / (0.5 * math.sqrt(OmL) / math.sqrt(8 * math.pi / 3)))**2 - 48.9) < 0.1, "E4a  (cH0/a0)^2 = Z^2/Omega_Lambda = 48.9  (the record's '49')")
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
