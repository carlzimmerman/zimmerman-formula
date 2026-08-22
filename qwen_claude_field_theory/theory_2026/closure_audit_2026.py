#!/usr/bin/env python3
r"""Audit of the closed candidate: F_MOND, A(X), Lambda, and the naturalness of epsilon."""
import sympy as sp, numpy as np
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c
X=sp.symbols('X',positive=True); x=sp.sqrt(X)

head("A -- does the proposed F_MOND give the right mu?")
F_prop=-X+2*sp.sqrt(X)-2*sp.log(1+sp.sqrt(X))
mu_prop=sp.simplify(1+sp.diff(F_prop,X))
print(f"  proposed F = -X + 2 sqrt(X) - 2 ln(1+sqrt(X))")
print(f"  => mu = 1 + F_X = {sp.simplify(mu_prop)}")
print(f"     in terms of x = sqrt(X) = g/a0:  mu = {sp.simplify(mu_prop.rewrite(sp.Pow)).subs(X,sp.Symbol('xx')**2)}")
lim0=sp.limit(mu_prop,X,0); limI=sp.limit(mu_prop,X,sp.oo)
print(f"     mu(X->0) = {lim0}      mu(X->oo) = {limI}")
ok(not(lim0==0 and limI==1),"A1  *** the proposed F_MOND has the asymptotics BACKWARDS ***",
   "it gives mu = 1/(1+x): mu -> 1 deep-MOND and mu -> 0 Newtonian. Exactly inverted.")
F_corr=-2*sp.sqrt(X)+2*sp.log(1+sp.sqrt(X))
mu_corr=sp.simplify(1+sp.diff(F_corr,X))
print(f"\n  CORRECTED F_MOND = -2 sqrt(X) + 2 ln(1+sqrt(X))")
print(f"  => mu = {sp.simplify(mu_corr)} = x/(1+x)")
ok(sp.limit(mu_corr,X,0)==0 and sp.limit(mu_corr,X,sp.oo)==1,
   "A2  corrected F gives mu -> x (deep MOND) and mu -> 1 (Newtonian)",
   "difference is exactly the spurious -X term plus a sign flip: F_prop = -X - F_corr")
ok(sp.simplify(F_prop-(-X-F_corr))==0,"A3  F_proposed = -X - F_corrected  (identity)")

head("B -- the X-window A(X) = X^2/(1+X)^4")
A=X**2/(1+X)**4; Ap=sp.simplify(sp.diff(A,X))
print(f"  A'(X) = {Ap}")
ok(sp.simplify(Ap-2*X*(1-X)/(1+X)**5)==0,"B1  A' = 2X(1-X)/(1+X)^5")
ok(sp.simplify(Ap.subs(X,1))==0,"B2  A'(1) = 0  -- no direct mu-correction at the transition")
ok(sp.simplify(A.subs(X,1))==sp.Rational(1,16),"B3  A(1) = 1/16")
ok(sp.limit(A/X**2,X,0)==1 and sp.limit(A*X**2,X,sp.oo)==1,
   "B4  A ~ X^2 (X<<1) and A ~ X^-2 (X>>1): suppressed at both ends")

head("C -- the lever Lambda = c^4/(G M a0)")
C_=2.99792458e8; G=6.6743e-11; MSUN=1.98892e30; A0=9.3619e-11
Lam=lambda M: C_**4/(G*M*MSUN*A0)
print(f"  {'system':<20}{'v_inf [m/s]':>13}{'Lambda':>13}")
for nm,M in (("Sun",1.0),("1e11 Msun galaxy",1e11),("dwarf 1e8",1e8)):
    print(f"  {nm:<20}{(G*M*MSUN*A0)**0.25:13.4g}{Lam(M):13.4e}")
ok(abs(Lam(1.0)/6.50e23-1)<0.02,"C1  Lambda_sun = 6.50e23 confirmed")
ok(abs(Lam(1.0)/Lam(1e11)-1e11)<1e9,"C2  Lambda_sun/Lambda_gal = 1e11 confirmed",
   "the M^-1 lever is real and is much stronger than the M^-1/2 lever of Z_E itself")

head("D -- correction to MY earlier 'biharmonic annihilates the quadrupole' claim")
print("  I claimed the Y-sector cannot change Q2 because lap^2(r^2 P_2) = 0.")
print("  That statement about the OPERATOR is true, but the CONCLUSION was too strong.")
print("  Outside sources the equation factors as  lap(1 - l^2 lap) phi = 0, whose l=2")
print("  solutions are  A2 r^2 + B2 r^-3 + C2 i_2(r/l) + D2 k_2(r/l).")
print("  The r^2 P_2 mode survives; the Yukawa-type modes change the MATCHING that fixes A2.")
ok(True,"D1  my kill was CONDITIONAL on l << R_M, which held for my closure (l/R_M ~ 0.02)",
   "the linear-Y closure evades it by construction, putting l ~ R_M.  Concede.")
for chi in (0.01,1.0,12.0,100.0):
    print(f"     chi = {chi:>6}  ->  l_Y/R_M = sqrt(chi/12) = {np.sqrt(chi/12):.4f}")

head("E -- THE NEW OBJECTION: epsilon is universal, so the theory acquires a preferred MASS")
print("  chi(M) = epsilon * Lambda(M) = epsilon c^4/(G M a0).  chi ~ 1 therefore defines")
print("     M_* = epsilon c^4/(G a0)")
for eps in (1.8e-23,1e-22,1e-24):
    Mstar=eps*C_**4/(G*A0)/MSUN
    print(f"  epsilon = {eps:.1e}  ->  M_* = {Mstar:.4g} Msun")
Mstar=1.8e-23*C_**4/(G*A0)/MSUN
ok(0.05<Mstar<50,"E1  *** the tuning chi_sun ~ 12 puts the theory's preferred mass at ~1 Msun ***",
   f"M_* = {Mstar:.3g} Msun")
print("\n  This is the objection.  epsilon is a UNIVERSAL dimensionless constant, but chi ~ 1")
print("  singles out a MASS.  Setting chi_sun ~ 12 means the tidal sector switches on at")
print(f"  M ~ {Mstar:.2g} Msun -- i.e. at the mass of the star we happen to orbit.  Nothing in the")
print("  action explains why a fundamental coupling should be tuned to that.  And epsilon ~ 2e-23")
print("  is itself a 23-order hierarchy in a dimensionless number.")
print("\n  Sharper still: the SAME chi that suppresses Q2 at the Sun makes the tidal sector")
print("  IRRELEVANT for every other bound system.  So the mechanism is not 'environmental")
print("  dependence' at all -- it is a switch tuned to one object's mass.")
print("\n  Test it: what does chi ~ 12 at the Sun imply elsewhere?")
for nm,M in (("Jupiter",9.5e-4),("Sun",1.0),("star cluster 1e4",1e4),("dwarf 1e8",1e8),("galaxy 1e11",1e11)):
    print(f"     {nm:<20} chi = {1.8e-23*Lam(M):>12.3e}")
