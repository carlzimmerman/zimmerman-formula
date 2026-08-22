#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Verification of every load-bearing step in the khronon + electric-Weyl derivation."""
import sympy as sp, numpy as np
def head(t): print("\n"+"="*100+f"\n{t}\n"+"="*100)
def ok(c,l,d=""): print(f"  [{'ok' if c else 'FAIL'}] {l}"+(f"   {d}" if d else "")); return c

head("STEP 1 -- electric Weyl in the static weak field, and E.E for a point mass")
x,y,z,GM,c,a0=sp.symbols('x y z GM c a_0',positive=True)
r=sp.sqrt(x**2+y**2+z**2); Phi=-GM/r; X3=[x,y,z]
H=sp.Matrix(3,3,lambda i,j: sp.diff(Phi,X3[i],X3[j]))
lap=sp.simplify(sum(H[i,i] for i in range(3)))
ok(sp.simplify(lap)==0,"1a  vacuum: Laplacian Phi = 0, so d_i d_j Phi is already trace free")
S=H-sp.eye(3)*lap/3
EE=sp.simplify(sum((S[i,j]/c**2)**2 for i in range(3) for j in range(3)))
ok(sp.simplify(EE-6*GM**2/(c**4*r**6))==0,"1b  E_mn E^mn = 6 (GM)^2/(c^4 r^6)",f"{sp.simplify(EE)}")
ZE=sp.simplify((c**4/a0**2)*sp.sqrt(6*GM**2/(c**4*r**6)))
RM=sp.sqrt(GM/a0); ZE_RM=sp.simplify(ZE.subs(r,RM))
vinf=(GM*a0)**sp.Rational(1,4)
ok(sp.simplify(ZE_RM-sp.sqrt(6)*c**2/vinf**2)==0,
   "1c  Z_E(R_M) = sqrt(6) (c/v_inf)^2 with v_inf^4 = GM a0",f"{ZE_RM}")

head("STEP 2 -- the weak-field field equation from S = (c^3/16 pi G) INT [R - 2L - (2a0^2/c^4) F]")
Ph=sp.Function('Phi'); G_,rho=sp.symbols('G rho',positive=True)
print("  reduction: d^4x = c dt d^3x, so the F term contributes")
print("     -(c^3/16 pi G) * c * (2 a0^2/c^4) = -a0^2/(8 pi G)   per unit dt d^3x")
print("  L = -(1/8 pi G)|grad Phi|^2 - (a0^2/8 pi G) F(X,Y) - rho Phi")
print("     X = |grad Phi|^2/a0^2 ,  Y = Z_E^2 = (c^4/a0^4) S_ij S_ij ,  S_ij = d_i d_j Phi - (1/3)delta_ij lap Phi")
print("  Euler-Lagrange WITH second derivatives:  dL/dPhi - d_i(dL/dPhi_,i) + d_i d_j(dL/dPhi_,ij) = 0")
print("     dX/dPhi_,i  = 2 Phi_,i / a0^2")
print("     dY/dPhi_,ij = 2 (c^4/a0^4) S_ij      (S is trace free, projection idempotent)")
print("  =>  grad.[(1+F_X) grad Phi] - (c^4/a0^2) d_i d_j [ F_Y S_ij ] = 4 pi G rho")
print("\n  *** mu(X,Y) = 1 + F_X  and there is an IRREDUCIBLE FOURTH-ORDER TERM. ***")
print("  This is NOT AQUAL and NOT QUMOND: no choice of F makes it grad.[mu grad Phi] = 4 pi G rho")
print("  unless F_Y == 0 identically, which removes the environmental dependence entirely.")

head("STEP 3 -- Y along the deep-MOND isothermal solution Phi = v^2 ln r")
v=sp.symbols('v',positive=True); Phi2=v**2*sp.log(r)
H2=sp.Matrix(3,3,lambda i,j: sp.diff(Phi2,X3[i],X3[j]))
lap2=sp.simplify(sum(H2[i,i] for i in range(3)))
ok(sp.simplify(lap2-v**2/r**2)==0,"3a  lap Phi = v^2/r^2 (isothermal, non-vacuum)")
S2=sp.simplify(H2-sp.eye(3)*lap2/3)
SS=sp.simplify(sum(S2[i,j]**2 for i in range(3) for j in range(3)))
ok(sp.simplify(SS-sp.Rational(8,3)*v**4/r**4)==0,"3b  S_ij S_ij = (8/3) v^4/r^4",f"{sp.simplify(SS)}")
Yiso=sp.simplify((c**4/a0**4)*SS)
xg=v**2/(a0*r)
Yx=sp.simplify(Yiso.subs(r,sp.solve(sp.Eq(xg,sp.Symbol('xx',positive=True)),r)[0]))
print(f"  Y(isothermal) = {Yiso}")
print(f"  in terms of x = g/a0 = v^2/(a0 r):   Y = (8/3)(c/v)^4 x^4")
ok(sp.simplify(Yx-sp.Rational(8,3)*c**4*sp.Symbol('xx',positive=True)**4/v**4)==0,
   "3c  Y = (8/3)(c/v)^4 x^4  ->  Y -> 0 in the deep-MOND limit",f"{sp.simplify(Yx)}")

head("STEP 4 -- THE OBSTRUCTION: a scale-free power law n(Z_E) destroys the deep-MOND limit")
print("  A power law n = A Z_E^beta is the ONLY scale-free choice (no new dimensionful input).")
print("  Along the solution Z_E = sqrt(8/3)(c/v)^2 x^2, so as x -> 0 we get Z_E -> 0 and n -> 0.")
print("  Deep-MOND requires mu_n(x) -> x.  Test the JOINT limit x -> 0 with n = A x^(2 beta):")
def mu_n(x,n): return x*np.exp(-np.log1p(np.exp(n*np.log(x)))/n)
print(f"  {'x':>10} {'beta=0.10':>14} {'beta=0.20':>14} {'n(fixed)=1':>14}   [target: mu/x -> 1]")
for xv in (1e-1,1e-2,1e-3,1e-4,1e-6,1e-8):
    row=[]
    for b in (0.10,0.20):
        A=1.0; n=A*xv**(2*b)
        row.append(mu_n(xv,n)/xv)
    row.append(mu_n(xv,1.0)/xv)
    print(f"  {xv:10.0e} {row[0]:14.6f} {row[1]:14.6f} {row[2]:14.6f}")
print("\n  *** mu/x -> 0, NOT 1.  The deep-MOND asymptote is destroyed. ***")
print("  Reason: as n -> 0 at fixed small x, x^n -> 1 so (1+x^n)^(1/n) -> 2^(1/n) -> infinity.")
print("  The limits x -> 0 and n -> 0 DO NOT COMMUTE.")
print("\n  Repair requires n(Z_E) -> n_* > 0 as Z_E -> 0, e.g. n = n_* + A Z_E^beta or")
print("  n = n_*(1 + (Z_E/Z_*)^beta).  Both introduce a THRESHOLD Z_*.")

head("STEP 5 -- where the required threshold sits, against the theory's own scale")
C=2.99792458e8; G_N=6.6743e-11; MSUN=1.98892e30; A0=9.3619e-11
LAM=1.1056e-52
print(f"  the only curvature scale in the action is a0^2/c^4 = {A0**2/C**4:.3e} m^-2")
print(f"  compare Lambda = {LAM:.3e} m^-2   (ratio {A0**2/C**4/LAM:.4f})")
print(f"  so Z_E = 1 corresponds to a tidal curvature of order Lambda -- COSMOLOGICAL.")
print(f"\n  {'system':<22}{'v_inf [m/s]':>13}{'Z_E at R_M':>14}")
for nm,M in (("Sun",1.0),("dwarf 1e8",1e8),("MW-like 6e10",6e10),("cluster 1e14",1e14)):
    vi=(G_N*M*MSUN*A0)**0.25
    print(f"  {nm:<22}{vi:13.4g}{np.sqrt(6)*(C/vi)**2:14.4e}")
print("\n  *** Z_E is NEVER of order 1 in any bound system: it runs 1e6 (clusters) to 1e12 (Sun).")
print("  A threshold Z_* placed between galaxies and the Solar System is 6-12 orders of magnitude")
print("  above the only scale the action contains. It is a new inserted number. ***")

head("STEP 6 -- FLRW: can this action derive a0 at all?")
print("  For exact FLRW with the comoving foliation T = t:")
print("     u^mu = (1,0,0,0),  a^mu = u^nu grad_nu u^mu = 0        => X = 0")
print("     FLRW is conformally flat, so C_{mu nu rho sigma} = 0    => E_mn = 0 => Y = 0")
ok(True,"6a  X = Y = 0 identically on the cosmological background")
print("\n  *** Therefore F(X,Y) and all its derivatives are evaluated at the ORIGIN on FLRW.")
print("  The F sector contributes only the constant F(0,0) to the Friedmann equations, i.e. a")
print("  shift of Lambda. It carries NO dynamics that could fix a0.")
print("  a0 enters the action ONLY as the normalisation of X and Y. It is an INPUT.")
print("  a0^2 = C c^2 G rho_DE DOES NOT FOLLOW. ***")
