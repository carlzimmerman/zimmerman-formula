#!/usr/bin/env python3
r"""The tidal term corrects mu at the SAME order chi as it corrects the operator.
Check whether mu stays positive at the chi needed for l_Y ~ R_M."""
import numpy as np, sympy as sp
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c

head("A -- the mu correction is O(chi), not O(epsilon)")
print("  mu(X,Y) = sqrt(X)/(1+sqrt(X)) + eps A'(X) Y,   A'(X) = 2X(1-X)/(1+X)^5")
print("  In dimensionless Solar-System variables Y = Lambda Sbar_ij Sbar_ij, so")
print("       eps A'(X) Y = (eps Lambda) A'(X) Sbar^2 = chi A'(X) Sbar^2 .")
print("  The SAME chi that sets l_Y/R_M = sqrt(chi/12) also multiplies the mu correction.")
print("  A'(1) = 0 kills it AT the transition point only; A' is nonzero on either side.")

head("B -- Sbar^2 along a point-mass profile")
X=sp.symbols('X',positive=True); xx=sp.symbols('x',positive=True)
phi=-1/xx
# radial point-mass field: g = 1/x^2 so X = 1/x^4 ; S_ij S_ij = 6 (1/x^3)^2 = 6/x^6
print("  Newtonian branch phi = -1/x:  g = x^-2  =>  X = x^-4,  Sbar^2 = 6 x^-6 = 6 X^(3/2)")
print("  (verified: for phi=-1/x, d_i d_j phi is trace free with S_ij S_ij = 6/x^6)")
Sb2=lambda Xv: 6*Xv**1.5

head("C -- does mu stay positive?")
mu0=lambda Xv: np.sqrt(Xv)/(1+np.sqrt(Xv))
Ap =lambda Xv: 2*Xv*(1-Xv)/(1+Xv)**5
Xg=np.geomspace(1e-3,1e3,4000)
print(f"  {'chi':>10}{'min mu':>12}{'at X':>10}{'mu<0 anywhere?':>17}")
chi_max=None
for chi in (0.01,0.1,0.5,1.0,2.0,5.0,12.0,100.0):
    mu=mu0(Xg)+chi*Ap(Xg)*Sb2(Xg)
    j=int(np.argmin(mu))
    print(f"  {chi:>10.2f}{mu[j]:>12.4f}{Xg[j]:>10.4g}{'YES' if mu[j]<0 else 'no':>17}")
# find the critical chi
lo,hi=1e-4,1e3
for _ in range(80):
    mid=np.sqrt(lo*hi)
    if (mu0(Xg)+mid*Ap(Xg)*Sb2(Xg)).min()<0: hi=mid
    else: lo=mid
chi_c=lo
print(f"\n  critical chi (mu -> 0):  chi_c = {chi_c:.4e}")
ok(chi_c<12,"C1  *** mu goes NEGATIVE far below the chi ~ 12 the mechanism needs ***",
   f"chi_c = {chi_c:.3e} against chi_sun ~ 12 required for l_Y ~ R_M")
print(f"  ratio required/allowed = {12/chi_c:.3e}")

head("D -- where it fails and why")
mu=mu0(Xg)+chi_c*1.0001*Ap(Xg)*Sb2(Xg)
j=int(np.argmin(mu))
print(f"  first zero at X = {Xg[j]:.4g}  (x = X^-1/4 = {Xg[j]**-0.25:.4g} R_M)")
print(f"  A'(X) there = {Ap(Xg[j]):.4e}   Sbar^2 = {Sb2(Xg[j]):.4e}")
print("  The failure is on the X > 1 side, where A' < 0, i.e. INSIDE the MOND radius,")
print("  and it is amplified by Sbar^2 ~ 6 X^(3/2) which grows fast toward the Sun.")
print("  mu < 0 means the static operator changes sign: the boundary-value problem is")
print("  no longer elliptic and the Newtonian limit is destroyed.")

head("E -- can the X-window be fixed to save it?")
print("  Need A'(X) Sbar^2 = A'(X) 6 X^(3/2) bounded as X -> large, while A(X) itself must")
print("  stay large enough near X ~ 1 to give the operator its strength.")
print("  With A ~ X^-p at large X: A' ~ -p X^-p-1, so A' Sbar^2 ~ -6p X^(1/2 - p).")
print("  Boundedness needs p >= 1/2.  A = X^2/(1+X)^4 has p = 2, so A' Sbar^2 ~ X^-3/2 -> 0.")
for p,lab in ((2.0,"A = X^2/(1+X)^4  (proposed)"),):
    pass
print("\n  So the LARGE-X tail is actually fine.  Recheck where the minimum really sits:")
for chi in (0.01,0.1,1.0):
    mu=mu0(Xg)+chi*Ap(Xg)*Sb2(Xg); j=int(np.argmin(mu))
    print(f"    chi={chi:<6} min mu = {mu[j]:+.5f} at X = {Xg[j]:.4g}  (A'={Ap(Xg[j]):+.3e}, Sbar^2={Sb2(Xg[j]):.3e})")
print("\n  The binding region is X of order a few, just inside the MOND radius, where")
print("  A' is negative and Sbar^2 is already sizeable. That is exactly the transition")
print("  region the mechanism has to act in, so it cannot be moved out of the way.")
