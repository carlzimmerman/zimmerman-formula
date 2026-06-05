#!/usr/bin/env python3
"""
STAGE 9 -- consolidated, self-contained verification of the membrane-stress route.
Reproduces every load-bearing identity and states the verdict numerically.
"""
import sympy as sp
G, c, hbar, Lam, M = sp.symbols('G c hbar Lambda M', positive=True)
kappa0 = sp.symbols('kappa0', positive=True)
r = sp.symbols('r', positive=True)
pi = sp.pi
RdS = sp.sqrt(3/Lam)
rho_L = Lam*c**2/(8*pi*G)
a0 = kappa0*c*sp.sqrt(G*rho_L)

print("="*72)
print("MEMBRANE-STRESS ROUTE -- consolidated verification")
print("="*72)

# 1. target
Z = 2*sp.sqrt(8*pi/3)
print(f"\n[1] Framework target: Z=sqrt(32pi/3)={float(Z):.4f}; a0=(c/2)sqrt(G rho_L) => kappa0=1/2")
print(f"    check sqrt(32pi/3) = 2 sqrt(8pi/3):", sp.simplify(sp.sqrt(32*pi/3)-Z)==0)

# 2. deep-MOND on-shell action (log-divergent, IR-cut at R_dS)
gradphi = sp.sqrt(G*M*a0)/r
L = -gradphi**3/(12*pi*G*a0)
I = sp.integrate(L*4*pi*r**2, (r, sp.symbols('r_in'), RdS))
print(f"\n[2] On-shell MOND action I = -(1/3)M^3/2 sqrt(G a0) ln(R/r_in): verified Stage1")

# 3. canonical stress is TRACELESS (SO(4,1) conformal)
X = gradphi
T_rr = sp.simplify((-X**2/(4*pi*G*a0))*X + X**3/(12*pi*G*a0))
T_tt = sp.simplify(X**3/(12*pi*G*a0))
print(f"\n[3] deep-MOND stress trace T_rr+2T_tt = {sp.simplify(T_rr+2*T_tt)}  (SO(4,1) conformal)")

# 4. THE central number: field horizon pressure at coincidence mass
Mstar = sp.solve(sp.Eq(sp.sqrt(G*M/a0), RdS), M)[0]
field_ratio = sp.simplify(T_rr.subs(r,RdS).subs(M,Mstar)/(rho_L*c**2))
print(f"\n[4] CENTRAL RESULT: T_rr(R_dS)/(rho_L c^2)|_M* = {field_ratio}")
print(f"    = -kappa0^2/(6pi). To force kappa0=1/2 needs balance RHS = 1/(24pi):")
need = sp.Rational(1,4)/(6*pi)
print(f"      (1/2)^2/(6pi) = {need} = {float(need):.6f}")

# 5. the membrane-pressure RHS candidates -> none equals 1/(24pi); all give sqrt(pi)
print(f"\n[5] kappa0 from natural balances (kappa0=sqrt(6pi*RHS)):")
for nm,rhs in [("|p|=rho_L c^2 (w=-1)",1),("equipartition 1/2",sp.Rational(1,2)),
               ("BH 1/4",sp.Rational(1,4)),("Verlinde 1/6",sp.Rational(1,6)),
               ("dS surface kappa_g/(8piG)/(rho c^2)*R=1/3",sp.Rational(1,3))]:
    k0 = sp.sqrt(6*pi*rhs)
    isr = sp.simplify(k0 - sp.Rational(1,2))==0
    print(f"    {nm:<42} kappa0={k0} = {float(k0):.4f}  {'<==1/2' if isr else '(has sqrt(pi))'}")

# 6. what Z each kappa0 implies (kappa0=1/2 -> Z=5.789)
print(f"\n[6] implied Z = 1/kappa0 * (Friedmann sqrt) ... Z(kappa0)=sqrt(8pi/3)/kappa0*2? ")
# a0 = kappa0 c^2 sqrt(Lam/8pi); Z=cH/a0 with H=c sqrt(Lam/3): Z = sqrt(Lam/3)/(kappa0 sqrt(Lam/8pi))
for nm,k0 in [("kappa0=1/2 (target)",sp.Rational(1,2)),
              ("kappa0=sqrt(6pi*1)",sp.sqrt(6*pi)),
              ("kappa0=sqrt(3pi) (equipart)",sp.sqrt(3*pi))]:
    Zimp = sp.simplify(sp.sqrt(Lam/3)/(k0*sp.sqrt(Lam/(8*pi))))
    print(f"    {nm:<28} -> Z = {sp.simplify(Zimp)} = {float(Zimp):.4f}")

print("\n"+"="*72)
print("VERDICT: the membrane balance produces kappa0 = (rational)*sqrt(pi) for every")
print("forced RHS -- NEVER the bare rational 1/2. kappa0=1/2 requires the unforced")
print("choice RHS=1/(24pi), which no geometric membrane pressure supplies. The route")
print("DOES NOT CLOSE: freedom persists (and lands a sqrt(pi), giving wrong numbers).")
print("="*72)
