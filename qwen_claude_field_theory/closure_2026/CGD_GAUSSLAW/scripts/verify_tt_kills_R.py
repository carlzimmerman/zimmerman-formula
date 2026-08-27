#!/usr/bin/env python3
r"""OpenAI's sharper obstruction: verify (3)R^(1)|_TT = 0 for h_ij = delta_ij + gamma^TT_ij,
so any E_i = grad(inverse-Laplacian) of ^(3)R vanishes for TT modes => the CGD action gives
no (grad gamma)^2 gradient term => c_T = 0 (or ill-defined), tensor propagation FAIL."""
import sympy as sp
# Symbols and TT metric perturbation
x, y, z = sp.symbols('x y z')
gamma = sp.Function('gamma')  # gamma_ij(x,y,z), transverse-traceless
# Represent TT as: gamma_ij symbolic 3x3, impose trace=0 and d_i gamma^ij = 0
g11,g22,g33,g12,g13,g23 = [sp.Function(n)(x,y,z) for n in ('g11 g22 g33 g12 g13 g23'.split())]
h = sp.Matrix([[g11,g12,g13],[g12,g22,g33 if False else g22*0 - g11 - 0],[g13,g22*0,g33]])  # will rebuild cleanly
# Rebuild h properly with trace=0 constraint (g33 = -g11 - g22)
g33_TT = -g11 - g22
h = sp.Matrix([[g11,g12,g13],[g12,g22,g23],[g13,g23,g33_TT]])
# Full metric h_ij = delta_ij + eps * gamma_ij
eps = sp.Symbol('eps', positive=True)
delta = sp.eye(3)
gg = delta + eps * h
# Linearized (3)R at O(eps): (3)R = -partial_i partial_j gamma^{ij} + Laplacian(trace gamma)
# For TT: both terms vanish
partials = [sp.diff, ]
coords = [x,y,z]
trace = sum(h[i,i] for i in range(3))
lap_trace = sum(sp.diff(trace, ci, 2) for ci in coords)
div_div = sum(sp.diff(sp.diff(h[i,j], coords[i]), coords[j]) for i in range(3) for j in range(3))
R_linear = -div_div + lap_trace
print("trace(gamma_TT):", sp.simplify(trace), "  (should be 0 identically)")
print("(3)R^(1) at TT:", sp.simplify(R_linear), "  (should be 0 identically for TT)")
# TT means: trace = 0 AND d_j gamma^{ij} = 0. The trace piece is 0 by construction (g33 = -g11-g22).
# The div-div piece: requires d_j gamma^{ij} = 0. Impose it symbolically as a constraint check —
# for a generic h with trace fixed, we don't have transversality yet. Let's take PLANE-WAVE TT:
# gamma^{TT}_ij = e^{ikz} h_ij(polarization), k along z, polarizations in (x,y). Then
# gamma_ij only nonzero for (i,j) in {(1,1),(2,2),(1,2),(2,1)} with h_11=-h_22 (traceless)
# and d_z gamma^{zj} = 0 auto (no z-components).
k = sp.Symbol('k', positive=True)
h_plus, h_cross = sp.symbols('h_plus h_cross', real=True)
gamma_pw = sp.zeros(3,3)
phase = sp.exp(sp.I*k*z)
gamma_pw[0,0] = h_plus*phase; gamma_pw[1,1] = -h_plus*phase
gamma_pw[0,1] = h_cross*phase; gamma_pw[1,0] = h_cross*phase
trace_pw = sum(gamma_pw[i,i] for i in range(3))
divdiv_pw = sum(sp.diff(sp.diff(gamma_pw[i,j],coords[i]),coords[j]) for i in range(3) for j in range(3))
lap_trace_pw = sum(sp.diff(trace_pw,ci,2) for ci in coords)
R_pw = sp.simplify(-divdiv_pw + lap_trace_pw)
print("\nPlane-wave TT (k along z, +/x polarizations):")
print("  trace:", trace_pw, "  divdiv:", sp.simplify(divdiv_pw), "  lap trace:", lap_trace_pw)
print("  (3)R^(1)|_TT:", R_pw, "  <== ZERO confirms OpenAI's claim")
assert R_pw == 0, "TT should kill (3)R^(1)"
print("\n[PASS] (3)R^(1)|_TT = 0 => E_i = D_i grad^{-2} (3)R vanishes for TT")
print("[PASS] => the CGD constitutive potential J(Y=E^2) contributes NOTHING to (grad gamma)^2")
print("[PASS] => tensor dispersion has no k^2 term => c_T = 0 (or ill-defined) => FAIL")
