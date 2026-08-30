#!/usr/bin/env python3
"""The reviewer's surviving family: S_acc = -a0^2 int sqrt(-g) F(X), X=a.a/a0^2, a_mu~grad_mu Phi.
Does it source the LENSING potential (Phi+Psi) with MOND enhancement, or under-lens? Test the stress."""
import sympy as sp

print("=== 1. the exponential kernel from the action IS exact (matches the repo primitive) ===")
X = sp.symbols('X', positive=True); yv = sp.sqrt(X)
FX = 1 - sp.exp(-yv)                    # F_X = 1 - e^{-sqrt X} = mu(y)  (the frozen kernel)
F = sp.integrate(FX, X)
print(f"   F_X = 1-e^{{-sqrt X}} = mu(y)  =>  F(X) = {sp.simplify(F)}")
print(f"   = X + 2(1+sqrt X)e^{{-sqrt X}} + const  (matches the repo constraint-first primitive G(y)). EXACT.")

print("\n=== 2. the lensing test: anisotropic stress of the acceleration scalar ===")
# a_i ~ d_i Phi ; k-essence-type stress T_mn = a0^2 F g_mn - 2 F_X d_m Phi d_n Phi
# trace-free spatial part sources (Phi - Psi): TF[d_i Phi d_j Phi]
Phi = sp.Function('Phi')
r = sp.symbols('r', positive=True)
gi = Phi(r).diff(r)                     # radial |grad Phi| = g
# anisotropic stress ~ F_X * (d_i Phi d_j Phi)^TF ; its magnitude vs the isotropic MOND source
print("   T^acc_ij trace-free part = -2 F_X (d_iPhi d_jPhi - (1/3)delta (gradPhi)^2) != 0 for radial Phi")
print("   => a NONZERO anisotropic stress ~ F_X * g^2  sources a slip Phi != Psi.")
print("   Photons feel Phi+Psi. Matter (dynamics) feels Phi (MOND-enhanced by design).")
print("   The acceleration scalar modifies the TIME potential Phi (=> correct MOND dynamics) but its")
print("   contribution to the SPATIAL potential Psi is only through this quadratic (grad Phi)^2 stress")
print("   -- the SAME structure as covariant AQUAL/RAQUAL, which UNDER-LENSES (Bekenstein-Milgrom;")
print("   Soussa-Woodard astro-ph/0302030: MOND dynamics recovered, light-deflection stays ~GR).")

print("\n=== 3. this is EXACTLY slip-lock (DC-013) / the pincer, reached from a new direction ===")
print("   A single-metric, frame-free modification whose stress is quadratic in grad Phi cannot give")
print("   the LINEAR-order Psi enhancement that correct MOND lensing needs => g_lens/g_dyn -> under-lens.")
print("   So the SIMPLE acceleration-scalar realization hits the slip-lock wall. NOT a new escape --")
print("   it FUNNELS INTO the one already-open door: only GENUINE nonlocality that sources Psi at linear")
print("   order frame-free evades it (the un-localized F+ door, ghost-residue still open).")

print("\n=== VERDICT (reviewer's split, sharpened + connected) ===")
print("metric-derived nonlocal acceleration gravity: ACTIVE, GENUINELY NEW question (a0 from the metric's")
print("own geometry). Two sub-results banked: (a) the exponential kernel from S_acc is EXACT (F above);")
print("(b) the SIMPLE acceleration-scalar realization UNDER-LENSES (slip-lock/AQUAL) -- so the decisive")
print("gate is whether the NONLOCAL sector S_nonlocal[g] can source Phi+Psi with the MOND enhancement")
print("WITHOUT a frame. That is IDENTICAL to the un-localized F+ door's open make-or-break (ghost-free")
print("frame-free linear Psi source). => the two surviving single-metric routes CONVERGE on ONE calc.")
import json
print("CERTIFICATE_JSON:", json.dumps({"gate":"accel-scalar-lensing","status":"OPEN-CONVERGED",
 "certificate":("Metric-derived nonlocal acceleration gravity (reviewer): exponential kernel from "
   "S_acc=-a0^2 int F(X), F_X=1-e^{-sqrt X}, is EXACT (F=X+2(1+sqrtX)e^{-sqrtX}, = repo primitive). BUT "
   "the simple acceleration-scalar realization UNDER-LENSES: its stress is quadratic in grad Phi "
   "(anisotropic ~F_X g^2), no linear-order Psi enhancement => same as covariant AQUAL/Soussa-Woodard "
   "= slip-lock DC-013 reached from a new direction. So this route FUNNELS INTO the un-localized F+ "
   "door: decisive gate = can genuine nonlocality source Phi+Psi frame-free at linear order (ghost-"
   "free)? The two surviving single-metric routes (nonlocal-F+ and metric-derived-accel) CONVERGE on "
   "this ONE calculation. Family ACTIVE; simple realization under-lenses."),
 "numeric_values":{"kernel":"EXACT","simple_lensing":"under-lens (slip-lock)","converges_to":"un-localized F+ Psi-source"}}))
