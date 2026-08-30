#!/usr/bin/env python3
"""FROZEN EXCEPTIONAL luminal DHOST subbranch (reviewer's correction -- the c_GW=c + no-graviton-decay
branch, the one with a chance): L = G_2 - G_3 box phi + f(X) R + (3 f_X^2/2f) phi^m phi_ma phi^an phi_n,
i.e. A_3=A_5=0, A_4=3f_X^2/2f. KEY: f=f(X) is a FIELD-DEPENDENT Planck mass. Solve the vacuum-exterior
spherical potentials FIRST; the f(X) nonminimal coupling CAN source Psi in vacuum via nabla-nabla f
(unlike the A_3 branch). Get the r-scaling. Kill: Phi',Psi'~1/r^2 => fail; ~sqrt(GMa0)/r => MOND."""
import sympy as sp

r, GM, a0, c0 = sp.symbols('r GM a0 c0', positive=True)

print("=== the essential new element: f_X != 0 => nabla-nabla f(X) sources Psi in VACUUM ===")
print("  The A_3 branch gave GR-exterior (mods ~M',M''=0). Here the nonminimal f(X)R gives, on variation,")
print("  a metric source (nabla_m nabla_n - g box) f. In vacuum f=f(X(r)) VARIES (X~(phi')^2) => nonzero")
print("  anisotropic source => Psi != Phi in vacuum. So this branch is NOT auto-GR-exterior. Compute the scaling.")

print("\n=== STEP 1 (FIRST): vacuum-exterior r-scaling of the f(X) slip source ===")
phi_p = sp.sqrt(GM*a0)/r                       # deep-MOND scalar force (G_2 AQUAL), phi' ~ 1/r
X = sp.Rational(1,2)*phi_p**2                   # X = 1/2 (phi')^2
print(f"  phi'(r) = {phi_p} (MOND scalar);  X(r) = 1/2 (phi')^2 = {sp.simplify(X)} ~ 1/r^2")
# f(X): take the minimal field-dependent form f = Mpl^2/2 (1 + c0 * X/a0^2-ish); slip source ~ nabla-nabla f
fX = sp.symbols('f_X', positive=True)          # df/dX (treat as the leading coupling)
# nabla_i X = phi' phi'' n_i ; phi'' = d/dr(sqrt(GMa0)/r) = -sqrt(GMa0)/r^2
phi_pp = sp.diff(phi_p, r)
gradX = sp.simplify(phi_p*phi_pp)              # radial nabla X = phi' phi''
print(f"  nabla_r X = phi' phi'' = {gradX} ~ 1/r^3")
# anisotropic slip source ~ nabla_i nabla_j f |TF ~ f_X * nabla_i nabla_j X |TF ; radial 2nd deriv of X:
lapX_source = sp.simplify(sp.diff(X, r, 2))    # ~ nabla-nabla X radial scaling
print(f"  nabla-nabla X ~ d^2X/dr^2 = {lapX_source} ~ 1/r^4  => slip source S ~ f_X/r^4")

# STEP 2: solve M^2 nabla^2 (Phi - Psi) = S  (S ~ f_X * const/r^4). Radial: (1/r^2)(r^2 (Phi-Psi)')' = S
slip = sp.Function('slip')
S = fX*GM*a0/r**4                              # the anisotropic source, scaling fixed
# integrate (1/r^2) d/dr(r^2 y') = S  for y=(Phi-Psi):  r^2 y' = integral(r^2 S dr)
inner = sp.integrate(r**2 * S, r)
yp = sp.simplify(inner/r**2)                   # (Phi-Psi)'
print(f"\n=== STEP 2: solve the slip equation, get (Phi-Psi)'(r) ===")
print(f"  (Phi-Psi)'(r) = (1/r^2) integral r^2 S dr = {yp}  ~ 1/r^3")
print(f"  compare: GR metric Phi' ~ GM/r^2 (~1/r^2) ; MOND target ~ sqrt(GMa0)/r (~1/r)")
print(f"  => the f(X) slip (Phi-Psi)' ~ 1/r^3 DECAYS FASTER than BOTH the GR metric (1/r^2) and the")
print(f"     MOND scale (1/r). So Psi's MOND-enhancement from f(X) is SHORT-RANGE (1/r^3), negligible")
print(f"     at large r where deep-MOND lensing is measured.")

print("\n=== TERMINAL VERDICT (exceptional branch, MOND gate FIRST) ===")
print("The exceptional c_GW=c no-decay branch DOES source a vacuum-exterior slip (via nabla-nabla f(X)),")
print("unlike the generic A_3 branch -- the reviewer was right to demand this test. BUT the slip scales as")
print("1/r^3, decaying FASTER than the MOND acceleration (1/r). So the lensing enhancement it provides is")
print("short-range and vanishes in the deep-MOND regime (large r) where flat-curve lensing lives. Photons")
print("still see ~Newtonian 1/r^2 at large r => STILL UNDER-LENSES asymptotically. The MOND scalar force is")
print("1/r (long-range) but the metric slip is 1/r^3 (short-range): they have INCOMPATIBLE reach. This is")
print("the pincer's deep reason -- a frame-free scalar's metric imprint is quadratic (grad phi)^2 => too")
print("short-range to match the linear MOND force. Even the exceptional branch cannot make lensing track")
print("dynamics at large r. Single-metric MOND: CLOSED for standard AND exceptional luminal DHOST. HELD")
print("pending the exact coefficient (could a fine-tuned f(X) with f_X divergent lift the 1/r^3 to 1/r?).")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"exceptional-branch","status":"HELD-UNDERLENS-1overR3",
 "certificate":("Exceptional c_GW=c no-graviton-decay DHOST branch (A_3=A_5=0, A_4=3f_X^2/2f, "
   "field-dependent f(X)) -- the reviewer's correct branch. It DOES source a vacuum-exterior slip via "
   "nabla-nabla f(X) (unlike the A_3 branch's GR-exterior), so it is NOT auto-excluded. BUT solving the "
   "slip equation: (Phi-Psi)' ~ 1/r^3, decaying FASTER than the MOND scalar force (1/r) AND the GR metric "
   "(1/r^2). So the f(X) lensing enhancement is SHORT-RANGE, negligible at large r where deep-MOND flat-"
   "curve lensing is measured => photons still see ~1/r^2 Newtonian asymptotically => STILL UNDER-LENSES. "
   "Root cause: a frame-free scalar's metric imprint is quadratic (grad phi)^2 => 1/r^3, too short-range "
   "to match the linear 1/r MOND force (the pincer's deep reason). Single-metric MOND CLOSED for standard "
   "AND exceptional luminal DHOST. HELD pending whether a divergent f_X could lift 1/r^3 to 1/r."),
 "numeric_values":{"phi_force":"1/r (MOND)","GR_metric":"1/r^2","fX_slip":"1/r^3 (short-range)","verdict":"under-lens asymptotically"}}))
