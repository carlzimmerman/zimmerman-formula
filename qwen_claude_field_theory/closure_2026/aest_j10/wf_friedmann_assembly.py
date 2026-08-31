#!/usr/bin/env python3
"""
Friedmann sector of AeST+J10 background, assembled from the literature-anchored
k-essence stress (dynamical-system paper arXiv:2309.06232):
   rho_phi = -(F - Q F_Q)/(8 pi Gt),   P_phi = F/(8 pi Gt)
specialised to J10 using our EXACT background values  F(0,Q)=-2K(Q), F_Q=-2K_Q.
Shows the split into (i) a w=-1 dark-energy piece and (ii) a dust piece ~a^-3.
"""
import sympy as sp

Gt, Q = sp.symbols('Gtilde Q', positive=True)
Kf = sp.Function('K'); K = Kf(Q); KQ = sp.diff(K,Q)

# background F-values (from wf_background_j10.py, EXACT):
F_bg  = -2*K            # F(0,Q) = (2-K_B)*J(0,Q) - 2K = -2K   since J(0,Q)=0
FQ_bg = -2*KQ           # F_Q(0,Q) = -2 K_Q                    since J_Q(0,Q)=0

rho_phi = sp.simplify(-(F_bg - Q*FQ_bg)/(8*sp.pi*Gt))
P_phi   = sp.simplify( F_bg/(8*sp.pi*Gt))
print("rho_phi =", rho_phi, "   = (K - Q K_Q)/(4 pi Gt)")
print("P_phi   =", P_phi,   "   = -K/(4 pi Gt)")
print()
print("Split:")
print("  DARK-ENERGY piece :  rho_de = K/(4 pi Gt),   P_de = -K/(4 pi Gt)  => w=-1")
print("  DUST piece        :  rho_du = -Q K_Q/(4 pi Gt),  P_du = 0")
print("  and K_Q ~ a^-3 (shift charge) => rho_du ~ a^-3  (CDM-like)")
print()
# de Sitter minimum: K_Q(Q0)=0
print("At the K-minimum Q->Q0 (K_Q=0):")
print("  rho_phi -> K(Q0)/(4 pi Gt),  P_phi -> -K(Q0)/(4 pi Gt)  (pure w=-1 de Sitter)")
print("  => shift charge dilutes to zero, a0 = a0(Q0) becomes CONSTANT.")
print()
# effective eq of state of the whole phi-sector
w = sp.simplify(P_phi/rho_phi)
print("w_phi = P_phi/rho_phi =", w, " = K/(K - Q K_Q)  (|w|<<1 when dust dominates,")
print("        -> -1 as K_Q->0).  [matches lit: w = F/(-F+Q F_Q)]")
print()
print("Full background Friedmann (flat, matter rho_m):")
print("  3 H^2 = 8 pi Gt rho_m + 8 pi Gt rho_phi + Lambda")
print("        = 8 pi Gt rho_m + (2K - 2Q K_Q)/... + Lambda   [Lambda absorbable into K]")
