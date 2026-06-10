#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #1 -- the BOUNDARY-CONDITION crux.

The two repo scripts disagree because they use two DIFFERENT metrics:

  (A) project03d_aether_stiffness.py : STRICTLY STATIC, no a(t):
        ds^2 = -e^{2Phi} dt^2 + e^{2Psi}(dr^2 + r^2 dOmega^2)
        aether A^mu = (e^{-Phi}, 0, 0, 0).  Claim: theta = nabla.A = 0 EXACTLY.

  (B) aest_locality_theta_profile.py : McVITTIE (FRW-embedded), a(t) present:
        ds^2 = -(1+2Phi) dt^2 + a(t)^2 (1-2Phi)(dr^2 + r^2 dOmega^2)
        aether A^mu = (1/sqrt(1+2Phi), 0, 0, 0).  Claim: theta = 3H/sqrt(1+2Phi).

I recompute theta = (1/sqrt(-g)) d_mu( sqrt(-g) A^mu ) from scratch for BOTH, with my own
metric determinant, to confirm which claim is correct and isolate exactly what flips the label.
The label-flipping ingredient is whether a(t) is in the spatial metric. That is the crux.
"""
import sympy as sp

print("="*90)
print("METRIC (A): STRICTLY STATIC (project03d) -- no scale factor a(t)")
print("="*90)
t, r, th = sp.symbols('t r theta', real=True)
Phi = sp.Function('Phi')(r)
Psi = sp.Function('Psi')(r)
# strictly static, NO a(t)
gA = sp.diag(-sp.exp(2*Phi), sp.exp(2*Psi), sp.exp(2*Psi)*r**2, sp.exp(2*Psi)*r**2*sp.sin(th)**2)
sqrtgA = sp.sqrt(-gA.det())
# unit-timelike aligned aether: A^t = e^{-Phi}, A^i=0  (A.A = g_tt (A^t)^2 = -e^{2Phi} e^{-2Phi} = -1) OK
AtA = sp.exp(-Phi)
# theta = (1/sqrt-g) d_mu(sqrt-g A^mu);  only mu=t contributes (A^i=0); sqrt-g is t-independent here
thetaA = sp.simplify(sp.diff(sqrtgA*AtA, t)/sqrtgA)
print(f"  unit check A.A = {sp.simplify(gA[0,0]*AtA**2)} (should be -1)")
print(f"  theta_static = {thetaA}")
assert thetaA == 0, "static theta should be exactly 0"
print("  => CONFIRMED: with NO a(t), theta = 0 EXACTLY. project03d is correct on its own metric.\n")

print("="*90)
print("METRIC (B): McVITTIE / FRW-embedded (aest_locality) -- a(t) present")
print("="*90)
a = sp.Function('a', positive=True)(t)
H = sp.diff(a, t)/a
# McVittie weak-field: static well in expanding cosmos
gtt = -(1 + 2*Phi)
grr = a**2*(1 - 2*Phi)
gB = sp.diag(gtt, grr, grr*r**2, grr*r**2*sp.sin(th)**2)
sqrtgB = sp.sqrt(sp.simplify(-gB.det()))
# unit-timelike: A^t = 1/sqrt(-g_tt) = 1/sqrt(1+2Phi), A^i=0
AtB = 1/sp.sqrt(1+2*Phi)
print(f"  unit check A.A = {sp.simplify(gB[0,0]*AtB**2)} (should be -1)")
thetaB = sp.simplify(sp.diff(sqrtgB*AtB, t)/sqrtgB)
thetaB = sp.simplify(thetaB)
print(f"  theta_McVittie = {thetaB}")
# compare to the claimed 3H/sqrt(1+2Phi)
claim = 3*H/sp.sqrt(1+2*Phi)
resid = sp.simplify(thetaB - claim)
print(f"  claimed 3H/sqrt(1+2Phi):  residual (theta - claim) = {resid}")
# weak field expansion in Phi
eps = sp.symbols('eps')
wf = sp.series((3*H)/sp.sqrt(1+2*eps), eps, 0, 2).removeO()
print(f"  weak field: theta = {wf}  (Phi<0 => theta = 3H(1+|Phi|), pinned to 3H at O(|Phi|)).")
print()

print("="*90)
print("THE CRUX, ISOLATED")
print("="*90)
print(f"""  The label flips ENTIRELY on whether the spatial metric carries a(t):
    - NO a(t) (strictly static): theta = 0  -> a0=(c/3Z)theta -> 0  -> FATAL (project03d).
    - WITH a(t) (McVittie/FRW):  theta = 3H/sqrt(1+2Phi) ~ 3H -> a0 ~ cH/Z -> PINNED (locality).
  Both algebra results are CORRECT. The physics question is which metric a real virialized galaxy
  sits in. That is NOT settled by the divergence algebra -- it is a boundary-condition/embedding
  question. The finder's headline 'PINNED' is contingent on the McVittie (FRW-comoving) BC.""")
