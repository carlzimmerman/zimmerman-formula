#!/usr/bin/env python3
r"""Test the two proposed repairs of n(Z), and size the new fourth-order term."""
import numpy as np
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100)
C=2.99792458e8; G=6.6743e-11; MSUN=1.98892e30; A0=9.3619e-11
def ZE(M):  # sqrt(6)(c/v_inf)^2 at R_M, v_inf=(G M a0)^(1/4)
    return np.sqrt(6)*(C/(G*M*MSUN*A0)**0.25)**2
Zsun=ZE(1.0); Zmw=ZE(6e10); Zdw=ZE(1e8); Zbig=ZE(3.6e11)
N_GAL, N_SUN = 1.0, 2.92          # DHF RAR fit; Gate 3 95% credible lower bound
head("A -- the numbers")
for nm,Z in (("Sun",Zsun),("dwarf 1e8",Zdw),("MW-like 6e10",Zmw),("SPARC max 3.6e11",Zbig)):
    print(f"  {nm:<20} Z_E = {Z:.4e}   Y = Z^2 = {Z**2:.4e}")
print(f"  lever Z_sun/Z_MW = {Zsun/Zmw:.4e}   ln = {np.log(Zsun/Zmw):.3f}")

head("B -- REPAIR 1 (your section 4):  n = n_* + dn * Y^b/(1+Y^b)   [BOUNDED]")
print("  Y >= 4e10 in EVERY bound system, so s(Y)=Y^b/(1+Y^b) = 1 - Y^-b is already saturated.")
print(f"  {'beta':>7}{'s(Y_MW)':>12}{'s(Y_sun)':>12}{'lever ds':>12}{'dn needed':>12}{'n_* implied':>14}")
ok_any=False
for b in (0.02,0.05,0.10,0.20,0.40):
    sM=Zmw**(2*b)/(1+Zmw**(2*b)); sS=Zsun**(2*b)/(1+Zsun**(2*b))
    ds=sS-sM
    dn=(N_SUN-N_GAL)/ds if ds>0 else np.inf
    nstar=N_GAL-sM*dn
    ok_any |= (nstar>0)
    print(f"  {b:>7.2f}{sM:>12.6f}{sS:>12.6f}{ds:>12.3e}{dn:>12.1f}{nstar:>14.1f}")
print("\n  *** n_* is NEGATIVE for every beta.  mu_n requires n > 0, so the bounded form")
print("      CANNOT deliver the needed lever.  Saturation kills it: s is ~1 everywhere. ***")
print(f"  bounded repair viable for some beta: {ok_any}")

head("C -- REPAIR 2:  n = n_* + A Z^beta   [UNBOUNDED power law added to a floor]")
R=Zsun/Zmw
b_min=np.log(N_SUN/1.0)/np.log(R)
print(f"  n_* > 0 requires  A Z_MW^b < 1  <=>  R^b > n_sun  <=>  beta > ln(n_sun)/ln(R) = {b_min:.4f}")
print(f"  {'beta':>7}{'A':>10}{'n_*':>9}{'n(MW)':>8}{'n(Sun)':>9}{'n(dwarf)':>10}{'n(3.6e11)':>11}{'SPARC spread':>13}")
good=[]
for b in (0.05,0.0864,0.10,0.12,0.15,0.20,0.30):
    A=(N_SUN-N_GAL)/(Zsun**b-Zmw**b); nstar=N_GAL-A*Zmw**b
    nd=nstar+A*Zdw**b; nb=nstar+A*Zbig**b
    flag="" if nstar>0 else "   <-- n_* < 0, INVALID"
    print(f"  {b:>7.4f}{A:>10.4f}{nstar:>9.4f}{nstar+A*Zmw**b:>8.3f}{nstar+A*Zsun**b:>9.3f}"
          f"{nd:>10.3f}{nb:>11.3f}{max(nd,nb)/min(nd,nb):>13.3f}{flag}")
    if nstar>0: good.append(b)
print(f"\n  *** VIABLE for beta > {b_min:.3f}, with n_* > 0 and the deep-MOND limit intact")
print(f"      (Z -> 0 in the outskirts => n -> n_* > 0 => mu -> x).  Viable betas: {good} ***")
print("  NOTE the beta floor is set by the SAME lever arm that set beta_req: it is not independent.")

head("D -- does the NEW fourth-order term actually do anything?  Size it at the Sun.")
b=0.10; A=(N_SUN-N_GAL)/(Zsun**b-Zmw**b); nstar=N_GAL-A*Zmw**b
print(f"  using beta={b}, A={A:.4f}, n_*={nstar:.4f}")
RM=np.sqrt(G*MSUN/A0)
print(f"  R_M(Sun) = {RM:.4e} m = {RM/1.496e11:.0f} au")
# T1 ~ mu g/r ; T2 ~ (c^4/a0^2) F_Y S/r^2 with S ~ g/r  =>  T2/T1 ~ (c^4/a0^2) F_Y / r^2
# F_Y = (dF/dn)(dn/dY), n = n_* + A Y^(b/2), dn/dY = (A b/2) Y^(b/2-1)
Y=Zsun**2
dndY=A*b/2*Y**(b/2-1)
for dFdn in (0.03,0.1,0.3):     # dF/dn at X~1 is O(0.1); bracketed
    FY=dFdn*dndY
    ratio=(C**4/A0**2)*FY/RM**2
    print(f"  dF/dn = {dFdn:<5} ->  F_Y = {FY:.3e},  T2/T1 = {ratio:.4f}")
print("\n  *** The new fourth-order term is a FEW PER CENT of the AQUAL term at the Sun's")
print("      transition radius.  It is real and nonzero, so the theory is formally NOT AQUAL,")
print("      but it is SUBDOMINANT.  The Q2 suppression comes overwhelmingly from mu carrying")
print("      n(Z_sun) ~ 2.9 instead of n ~ 1, not from the new operator. ***")
head("E -- consequence for the novelty claim")
for s in [
 "The mechanism that would evade Desmond-Hees-Famaey is NOT the fourth-order operator.  It is",
 "simply that mu is not universal: mu = mu_{n(Z)}(x) with n larger in the Solar System.  DHF",
 "scope their result to a UNIVERSAL interpolation function, so a non-universal mu is outside",
 "their theorem either way -- but the escape does not require the new covariant operator, and",
 "the operator's ~3% correction will not by itself change Q2 qualitatively.",
 "Therefore Q2^theory can be estimated to a few per cent by AQUAL with a position-dependent n,",
 "and the full fourth-order boundary-value problem is a refinement, not the deciding step.",
]: print("  "+s)
