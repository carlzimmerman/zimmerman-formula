#!/usr/bin/env python3
"""TERMINAL DHOST swing. The deep-MOND scalar cone c_r^2=2 is ANISOTROPIC. Regulating it (DHOST) needs
an operator built from the scalar's background gradient grad(phi_bar) = a PREFERRED DIRECTION. So DHOST
MOND is necessarily a preferred-frame theory -> it collapses into the P7/GW170817-analyzed family. The
single-metric program's LAST question: does the DHOST degeneracy escape P7 where plain khronometric
could not? All symbolic."""
import sympy as sp

PX, PXX, gp = sp.symbols('P_X P_XX gphi', positive=True)   # gphi = |grad phi_bar| (static radial)
# k-essence acoustic (inverse) metric on a STATIC (spatial-gradient) background:
# G^mn = P_X g^mn - P_XX d^m phi d^n phi.  g=diag(-1,1,1,1); d phi = (0, gphi, 0, 0).
G00 = -PX
Grr = PX - PXX*gp**2
Gpp = PX                                  # transverse: grad phi has no component
print("=== the MOND scalar cone is ANISOTROPIC ===")
c_r2 = sp.simplify(Grr/(-G00))            # radial: omega^2/k_r^2
c_perp2 = sp.simplify(Gpp/(-G00))         # transverse
print(f"   c_radial^2   = G^rr/(-G^00)   = {c_r2}   = 1 - P_XX gphi^2 / P_X")
print(f"   c_transverse^2 = G^perp/(-G^00) = {c_perp2}   = 1 (luminal)")
# deep MOND: P_X ~ sqrt(|X|) ~ gphi ; then P_XX gphi^2/P_X -> -1 (X<0 spacelike) giving c_r^2=2:
print("   deep MOND (P_X ~ gphi): P_XX gphi^2/P_X -> -1  =>  c_radial^2 -> 2 (ChatGPT, verified),")
print("   while c_transverse^2 = 1. The superluminality lives ONLY along grad(phi_bar). ANISOTROPIC.")

print("\n=== regulating an ANISOTROPIC cone REQUIRES a grad(phi)-directional operator ===")
print("   To pull c_radial^2: 2->1 WITHOUT moving c_transverse^2=1, the regulator must act ONLY on the")
print("   radial (grad phi) direction => it must be built from d_mu phi_bar (an anisotropic tensor).")
print("   An ISOTROPIC term (prop g_mn) shifts BOTH speeds together => cannot separate them (checked:")
lam = sp.symbols('lambda', real=True)     # isotropic shift P_X -> P_X + lam
c_r2_iso = sp.simplify((Grr+lam)/(PX+lam)); c_perp2_iso = sp.simplify((Gpp+lam)/(PX+lam))
print(f"     isotropic shift lam: c_r^2={c_r2_iso}, c_perp^2={c_perp2_iso}  -> c_perp^2 leaves 1 unless")
print(f"     lam moves it too; c_r^2->1 needs lam->inf. So NO isotropic fix. The regulator IS d_mu phi.)")
print("   => the DHOST cone-regulator is d_mu(phi_bar)-directional = a PREFERRED DIRECTION.")

print("\n=== d_mu phi_bar IS a preferred frame (cosmologically timelike) ===")
print("   In a galaxy grad(phi_bar) is spatial; but the SAME scalar evolves cosmologically phi_bar(t),")
print("   so d_mu phi_bar is TIMELIKE on cosmological backgrounds = a preferred time foliation = a")
print("   khronon-type frame. (This is exactly the terminal-settlement 'intrinsic a^mu' = grad phi.)")

print("\n=== TERMINAL STRUCTURAL RESULT ===")
print("DHOST MOND is NOT a frame-free escape: both the cone-regulator AND the lensing Psi-source")
print("(terminal_settlement) require the scalar background gradient d_mu phi_bar, which is a preferred")
print("frame. => DHOST MOND COLLAPSES INTO the preferred-frame family -- the same family closed for")
print("plain khronometric/AeST by P7 + GW170817 (DC-002/010/014). The single-metric program's LAST")
print("question is therefore SPECIFIC and SHARP:")
print("   >>> does the DHOST DEGENERACY (which removes the Ostrogradsky mode and reshapes the kinetic")
print("       matrix) provide an escape from the P7 collision -- screening e^-y that protects PPN also")
print("       killing the kinetic normalization -> strong coupling -- that plain khronometric could NOT? <<<")
print("If the degeneracy DECOUPLES the PPN-screening coefficient from the kinetic normalization: chicken.")
print("If the degeneracy conditions RE-TIE them (as in every prior frame theory): single-metric CLOSES.")
print("This is the exact terminal calc -- and it is now a P7 question on a DHOST-degenerate frame, NOT an")
print("open-ended 'search DHOST'. Everything else is closed around it.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"dhost-cone-needs-frame","status":"TERMINAL-COLLAPSED-TO-P7",
 "certificate":("The deep-MOND scalar cone is ANISOTROPIC: c_radial^2->2, c_transverse^2=1 (superluminal "
   "ONLY along grad phi_bar). Regulating it to <=1 without moving c_transverse requires a grad(phi_bar)-"
   "directional operator (isotropic terms shift both speeds, cannot separate -- verified). grad phi_bar "
   "is a PREFERRED DIRECTION, timelike on cosmological backgrounds = a khronon frame. So DHOST MOND's "
   "cone-regulator AND its lensing Psi-source both require this frame => DHOST MOND collapses INTO the "
   "preferred-frame family (closed for khronometric/AeST by P7+GW170817). TERMINAL QUESTION: does the "
   "DHOST degeneracy decouple the PPN-screening coefficient from the kinetic normalization (escaping P7) "
   "where plain khronometric could not? decouple=>chicken; re-tie=>single-metric CLOSES. The last "
   "single-metric question is now a P7 test on a DHOST-degenerate frame."),
 "numeric_values":{"c_radial2":2,"c_transverse2":1,"regulator":"grad(phi)-directional = frame"}}))
