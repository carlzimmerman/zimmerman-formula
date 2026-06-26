#!/usr/bin/env python3
r"""
RECONCILE: the original route1 script prints G_00 = 2 lap Psi (involves PSI).
My ADVERSARIAL_phi_eq prints G_00 = lap Phi (involves PHI). These cannot both be the linearized
Einstein (00) for the SAME metric. Find which is right -- it decides the whole delta-Phi argument.

Both use ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2. The DIFFERENCE: the original builds G from the FULL
g.inv() and series; mine builds R_ab from the linearized inverse eta - eps eta h eta and the
*Ricci* with a hand sum for the scalar. A sign/index slip in one of them is possible. Compute the
linearized G_00 the CLEAN textbook way and compare to BOTH.
"""
import sympy as sp
x,y,z,t=sp.symbols('x y z t', real=True); coords=[t,x,y,z]
eps=sp.symbols('epsilon', positive=True)
Phi=sp.Function('Phi')(x,y,z); Psi=sp.Function('Psi')(x,y,z)
lap=lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)

# FULL nonlinear metric, exact inverse, exact Einstein -- then linearize. The gold standard.
g=sp.diag(-(1+2*eps*Phi), 1-2*eps*Psi, 1-2*eps*Psi, 1-2*eps*Psi)
ginv=g.inv()
def christ(g,gi,c):
    n=len(c); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s=0
                for d in range(n): s+=gi[a,d]*(sp.diff(g[d,b],c[cc])+sp.diff(g[d,cc],c[b])-sp.diff(g[b,cc],c[d]))
                G[a][b][cc]=sp.expand(s/2)
    return G
Gamma=christ(g,ginv,coords)
def Ric(b,d):
    n=4; s=0
    for a in range(n):
        s+=sp.diff(Gamma[a][b][d],coords[a])-sp.diff(Gamma[a][b][a],coords[d])
        for e in range(n): s+=Gamma[a][a][e]*Gamma[e][b][d]-Gamma[a][d][e]*Gamma[e][b][a]
    return s
def lin(ex):
    s=sp.series(sp.expand(ex),eps,0,2).removeO(); return sp.expand(s.coeff(eps,1))
Rab={(a,b):lin(Ric(a,b)) for a in range(4) for b in range(4)}
# scalar R = g^ab R_ab ; to linear order use eta for the inverse on the linear Ricci
Rsc=lin(sum(ginv[i,i]*Ric(i,i) for i in range(4)))
def G(a,b):
    return sp.simplify(lin(Ric(a,b) - sp.Rational(1,2)*g[a,b]*Rsc))
G00=G(0,0); Gxx=G(1,1)
print("GOLD-STANDARD linearized Einstein (full inverse, full Ricci, then linearize):")
print("  G_00 =", G00)
print("  G_00 == 2 lap Psi ?", sp.simplify(G00-2*lap(Psi))==0)
print("  G_00 ==   lap Phi ?", sp.simplify(G00-lap(Phi))==0)
print("  G_xx =", Gxx)
print()
# Textbook value: for this metric, G_00 = 2 grad^2 Psi. (e.g. Weinberg, Dodelson.) Confirm.
print("Textbook: G_00 = 2 grad^2 Psi (matter density sources PSI). Matches gold standard above:",
      sp.simplify(G00-2*lap(Psi))==0)
print()
print("""
RECONCILIATION:
 * The ORIGINAL route1 script (full g.inv + series) is CORRECT: G_00 = 2 lap Psi.
   => the (00)/energy-density equation sources PSI (the spatial-curvature potential), NOT Phi.
 * My ADVERSARIAL_phi_eq used the linearized-inverse shortcut (eta - eps eta h eta) with a
   hand-built Ricci scalar; that introduced a Phi<->Psi mislabel in the printed G_00. The GOLD
   standard here (exact inverse) settles it: G_00 = 2 lap Psi.

CONSEQUENCE FOR THE delta-Phi ARGUMENT (corrected, and it CUTS BOTH WAYS):
 In GR with a perfect-fluid (isotropic, P=0) source:
    (00):    2 lap Psi      = 8piG rho           -> Psi = Newtonian potential
    (ij)off: d_idj(Psi-Phi) = 8piG * anisotropic stress = 0 (no anisotropic stress) -> Phi=Psi.
 So in standard GR a density gives Phi=Psi=Newtonian (gamma=1).
 A pure SLIP (Phi != Psi) needs a TRACELESS ANISOTROPIC stress sigma_ij in the (ij) eq:
    d_idj(Psi-Phi) = 8piG sigma_ij  ->  Psi-Phi = 8piG f  (f the stress potential).
 Now: lap Psi = 4piG rho_b fixes PSI to the baryon Newtonian value. Then Phi = Psi - 8piG f.
 MATTER feels grad(Phi) = grad(Psi_baryon) - 8piG grad f. So delta-Phi = -8piG grad f != 0
 UNLESS f=0. The anisotropic stress that makes light see the slip ALSO moves Phi -> fifth force.

 ==> SAME CONCLUSION as before, now on the CORRECT G_00: a traceless anisotropic stress that
     produces a light-bending slip moves BOTH Psi and Phi (it sets Psi-Phi). To keep Phi at the
     baryon value you must INDEPENDENTLY fix Phi -- which the (ij) eq does NOT allow for a metric-
     coupled source. The 'delta-Phi=0' escape requires the preferred frame to BREAK the (ij)
     Einstein equation's tie between the anisotropic stress and Phi: i.e. the frame force lambda_j
     must enter the (ij) sector to hold Phi fixed while Psi carries the slip. But lambda_j is a
     (0j) object (Section-3 sympy: reaches only G_0x) -> it does NOT enter (ij). So the (ij) tie
     is NOT broken by the multiplier as specified.
""")
print("="*88)
print(" CORRECTED ADVERSARIAL FINDING (on the right G_00):")
print("="*88)
print("""
 The construction needs Phi pinned to baryon while Psi carries the slip. The slip (Phi != Psi) is
 carried by a TRACELESS (ij) anisotropic stress, which the (ij) Einstein eq ties to (Psi - Phi).
 Pinning Psi to baryon (from 00) then FORCES Phi = Psi - slip != baryon -> delta-Phi != 0. The
 ONLY way out is a force that enters the (ij) equation to decouple Phi from the anisotropic stress.
 The specified multiplier lambda^j is a (0j) object and (by the original's own Section-3 sympy)
 does NOT reach (ij). THEREFORE, AS LITERALLY SPECIFIED, the multiplier does NOT protect delta-Phi=0
 -- the (ij) anisotropic-stress equation still moves Phi.

 To actually hold delta-Phi=0 one would need a SECOND multiplier acting in the (ij) sector (a
 traceless spatial-stress multiplier mu^{ij}), engineered to cancel the Phi-piece of the (ij) eq.
 That is a FURTHER hand-tuned constraint -- another free-function input. It can be ADDED (nothing
 forbids a second non-dynamical constraint), and THEN delta-Phi=0 holds by construction. But that
 makes delta-Phi=0 ALSO a by-hand imposition, not a structural consequence -- exactly parallel to
 the hand-tuned slip. Two postulates, not 'three of four free + one tuned'.
""")
print("NET: even granting the Lorentz-violating frame, delta-Phi=0 is achieved BY ADDING constraints")
print("(one in 0j to absorb the divergence, AND effectively one in ij to hold Phi), i.e. it is")
print("PASS-BY-CONSTRUCTION, the SAME phenomenological status as the slip -- NOT an independent")
print("structural PASS. The honest count is: delta-Phi=0 and the slip are bought TOGETHER by hand;")
print("c_T=c and ghost-freedom (propagating sector) are the only genuinely-free PASSes.")
