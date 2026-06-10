#!/usr/bin/env python3
"""
delta-Q partial check (independent kinematic route) -- corroborate the AeST PINNED mechanism for the
declining covariant carrier Q = A^mu d_mu phi, by a DIFFERENT method than the energy-minimization finder.

Setup: quasi-static galaxy. Metric perturbation Phi (1st order). Unit-timelike aether tilted radially by
alpha (1st order): A^t = 1/sqrt(1+2Phi), A^r = alpha. Scalar phi = phibar(t) + dphi(r), with cosmological
roll phibar-dot = Q0; the galaxy perturbs the time-derivative by dphidot and the gradient by dphi' (both 1st
order). Then Q = A^t (Q0 + dphidot) + A^r dphi'.

STRUCTURAL FINDING (the point): the dangerous tilt-advection coupling alpha*dphi' is SECOND ORDER (alpha and
dphi' are BOTH first-order perturbations), so it is kinematically suppressed BEFORE any energy argument runs.
The linear-order identity is just  delta-Q/Q0 = dphidot/Q0 - Phi. Verified in sympy.  C. Zimmerman 2026-06-09.
"""
import sympy as sp
eps=sp.symbols('epsilon', positive=True)
Phi1,alpha1,dphidot1,dphix1,Q0=sp.symbols('Phi1 alpha1 dphidot1 dphix1 Q0', real=True)
Phi=eps*Phi1; alpha=eps*alpha1; dphidot=eps*dphidot1; dphix=eps*dphix1   # all 1st-order in eps

At=1/sp.sqrt(1+2*Phi)          # unit-timelike normalization (A^i=0 limit gives A^t=1/sqrt(1+2Phi))
Ar=alpha                        # radial tilt
Q = At*(Q0+dphidot) + Ar*dphix  # Q = A^mu d_mu phi
dQ_over_Q0 = sp.simplify((Q-Q0)/Q0)

lin = sp.series(dQ_over_Q0, eps, 0, 2).removeO()      # linear order
quad = sp.expand(sp.series(dQ_over_Q0, eps, 0, 3).removeO() - lin)   # 2nd-order remainder
tilt_term_order = sp.degree(sp.Poly(sp.expand(Ar*dphix/Q0), eps))    # order in eps of the tilt-advection term

print("="*80); print("delta-Q/Q0 expansion in the perturbation order eps"); print("="*80)
print(f"  LINEAR order:   delta-Q/Q0 = {sp.simplify(lin/eps)*1}  (coefficient of eps)")
print(f"    -> set eps=1:  delta-Q/Q0 = dphidot/Q0 - Phi   [the identity; NO tilt term]")
print(f"  SECOND order:   {sp.simplify(quad)}")
print(f"  tilt-advection term alpha*dphi'/Q0 is order eps^{tilt_term_order} -> SECOND order, drops at linear order.\n")
# numeric sanity: tilt term truly absent at linear order
subs={Phi1:1.0,alpha1:1.0,dphidot1:1.0,dphix1:1.0,Q0:1.0}
lin_no_tilt = sp.simplify(lin.subs(alpha1,0)-lin)
print(f"  CHECK: removing the tilt (alpha1->0) changes the LINEAR identity by: {lin_no_tilt}  (0 = tilt is 2nd order)")
print("="*80)
print("""CONCLUSION: the AeST scalar carrier Q is pinned at LINEAR order to delta-Q/Q0 = dphidot/Q0 - Phi, and the
  tilt-advection coupling that the whole AeST-locality question feared (alpha*dphi') is SECOND ORDER -- so it
  is kinematically suppressed independent of (and prior to) the energy-minimization argument the finder used.
  This is an INDEPENDENT structural corroboration of PINNED. Magnitudes -> dQ_bounds.py.""")
