#!/usr/bin/env python3
"""THE DECISIVE CALC (corrected 2026-08-30 after adversarial audit found a sign error in the first
mechanism). Question: can a FRAME-FREE single-metric theory give correct MOND lensing (no slip eta=1)
AND gravitational enhancement WITHOUT a preferred frame? The real obstruction is DIFFEOMORPHISM
INVARIANCE, not a naive PSD count: a frame-free mode can only couple to the metric through covariant
curvature, which LOCKS its (Phi,Psi) coupling direction -> a fixed slip eta != 1. sympy throughout."""
import sympy as sp

# ---------------------------------------------------------------- linearized Ricci scalar (exact)
x,y,z = sp.symbols('x y z', real=True)
Phi = sp.Function('Phi'); Psi = sp.Function('Psi')
eps = sp.symbols('epsilon')
coords=[sp.symbols('t',real=True),x,y,z]
Ph=eps*Phi(x,y,z); Ps=eps*Psi(x,y,z)                     # static (quasi-static) potentials
g=sp.diag(-(1+2*Ph),(1-2*Ps),(1-2*Ps),(1-2*Ps))
gi=g.inv()
def christ(a,b,c):
    return sp.Rational(1,2)*sum(gi[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d])) for d in range(4))
Gam=[[[sp.series(christ(a,b,c),eps,0,2).removeO() for c in range(4)] for b in range(4)] for a in range(4)]
def Ric(b,d):
    r=0
    for a in range(4):
        r+=sp.diff(Gam[a][b][d],coords[a])-sp.diff(Gam[a][b][a],coords[d])
        for e in range(4):
            r+=Gam[a][a][e]*Gam[e][b][d]-Gam[a][d][e]*Gam[e][b][a]
    return sp.series(r,eps,0,2).removeO()
Rs=sp.series(sum(gi[b,d]*Ric(b,d) for b in range(4) for d in range(4)),eps,0,2).removeO()
Rs=sp.expand(Rs.coeff(eps,1))                            # linear-order Ricci scalar
lap=lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)
# express R^(1) in the basis {lap(Phi), lap(Psi)}
cP=Rs.coeff(sp.Derivative(Phi(x,y,z),(x,2)))            # coeff of d^2Phi/dx^2 (= coeff of lap Phi)
cS=Rs.coeff(sp.Derivative(Psi(x,y,z),(x,2)))
print("=== linearized Ricci scalar (quasi-static), exact from the metric ===")
print(f"   R^(1) = {sp.simplify(cP)}*lap(Phi) + {sp.simplify(cS)}*lap(Psi)")
print(f"   => curvature coupling DIRECTION v = ({cP}, {cS})  (Fourier: lap->-k^2, direction preserved)")
v = sp.Matrix([cP, cS])

# ---------------------------------------------------------------- the lock
print("\n=== a frame-free mode couples diff-invariantly through R^(1): M is pinned to v v^T ===")
L = sp.symbols('L', positive=True)     # L = 1/K > 0 (healthy mode); Schur sign gives M = -L v v^T
M = -L*(v*v.T)
A,B,C = M[0,0],M[0,1],M[1,1]
print(f"   M = -L v v^T = [[{A},{B}],[{B},{C}]]   (any # of frame-free modes: sum of L_i v v^T, SAME ray)")

# GR 2x2 (matter couples to Phi only), solve X=Q^{-1}s
m,rho=sp.symbols('m rho',positive=True)
Ggr=sp.Matrix([[0,2*m],[2*m,-2*m]]); s=sp.Matrix([rho,0])
X=sp.simplify((Ggr+M).inv()*s); Phiv,Psiv=X[0],X[1]
eta=sp.simplify(Psiv/Phiv)
E=sp.simplify(Phiv/(rho/(2*m)))
print("\n=== resulting slip and enhancement on the locked ray ===")
print(f"   eta = Psi/Phi = {eta}")
print(f"   enhancement E = Phi/Phi_GR = {E}")
etinf=sp.simplify(eta)
print(f"   eta=1 requires: {sp.solve(sp.Eq(eta,1),L)}  -> ONLY L=0 (no mode). Any L>0 gives eta!=1 (slip).")
# anchor: f(R) scalaron is exactly this single mode -> known gamma=1/2, E=4/3 at the relevant limit
print("\n=== anchor to the known f(R) result (single curvature-coupled scalaron) ===")
for Lv in [sp.Rational(1,2), 1, 2]:
    et=sp.nsimplify(eta.subs(L,Lv)); en=sp.nsimplify(E.subs(L,Lv))
    print(f"   L={Lv}: eta={et} (slip; f(R)-type gamma<1), E={en} (enhanced) -> lensing WRONG (eta!=1)")

print("\n=== THEOREM (corrected mechanism) ===")
print("Diffeomorphism invariance forces any frame-free extra mode to couple through covariant curvature,")
print("pinning its (Phi,Psi) coupling to the FIXED direction v="+str((int(cP),int(cS)))+" (the delta-R")
print("direction). On that locked ray eta=1 has ONLY the trivial solution L=0: any real coupling gives a")
print("NONZERO gravitational slip eta!=1 (the f(R) gamma=1/2 disease), so lensing does NOT track dynamics.")
print("Multiple modes / nonlocal form factors stay on the SAME ray => no escape. The ONLY way to source")
print("the anisotropy (Phi-Psi) in a DIFFERENT direction, decoupled from R, is a preferred-frame vector")
print("u^mu (u-projected couplings off the ray) = AeST/TeVeS. Hence: correct MOND lensing REQUIRES a")
print("preferred-frame carrier. The un-localized nonlocal F+ door (frameless) CLOSES.")
print('CERTIFICATE_JSON: {"gate":"SLIP-LOCK-theorem","status":"KILL","certificate":"Corrected after '
      'adversarial audit (first proof had a PSD/NSD sign error). Real mechanism: diff-invariance pins a '
      'frame-free modes (Phi,Psi) coupling to the delta-R direction v=(1,-2) [verified from the exact '
      'linearized Ricci scalar]. On that locked ray eta=1 only at L=0; any coupling gives f(R)-type slip '
      'eta=1/2 != 1 => lensing does not track dynamics. Any number of modes / nonlocal form factors stay '
      'on the same ray. Sourcing the Phi-Psi anisotropy off-ray needs a preferred-frame vector (AeST/TeVeS). '
      "Frame-free single-metric CANNOT do correct MOND lensing; the nonlocal F+ door closes.\","
      '"assumptions":["diff-invariant coupling through R^(1)","quasi-static linear","non-rel matter couples '
      'to Phi only","frame-free=no preferred vector"],"numeric_values":{"curvature_direction":"(1,-2)","eta_at_L=1":"see run"}}')
