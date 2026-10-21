#!/usr/bin/env python3
"""Scratch 3: the chi-machinery.

Static spherical background:  N(r), h_ij = f(r)[delta_ij + chi*T_ij],
T_ij = n_i n_j - (1/3) delta_ij  (the trace-free / "slip" mode).

In the orthonormal frame this is  h_rr = f(1+2chi/3), h_thth = f r^2 (1-chi/3):
the radial-vs-tangential anisotropy, i.e. EXACTLY the mode whose equation of
motion is the trace-free spatial Einstein equation.

At first order in chi, sqrt(h) N is chi-independent (tr T = 0).
The traceless stress of any operator O follows from
    dS/dchi = -(1/3) int d^3x sqrt(h) N * Pi_O     =>  Pi_O = -3 dL_O/dchi
where L_O is the Lagrangian density per sqrt(h) N.
"""
import sympy as sp

r, K, a0, gm, gs, ch = sp.symbols('r K a0 gamma gamma_s chi', positive=True)
N = sp.Function('N')(r)
f = sp.Function('f')(r)
P = sp.Function('P')(r)
Np = sp.diff(N, r)
fp = sp.diff(f, r)

# ---- chi-dressed building blocks (first order in chi) ----
u0 = K*P/sp.sqrt(f)
u = u0*(1 - ch/3)                                     # |P|
d0 = sp.diff(P, r)/f + 2*P/(r*f) + fp*P/(2*f**2)      # D_i P^i
d = d0*(1 - 2*ch/3)
clock = P*Np/(f*N)*(1 - 2*ch/3)                        # P^i d_i ln N
W = sp.Function('W')
uS = sp.Symbol('u', positive=True)
Wp = sp.Derivative(W(uS), uS)                          # placeholder

ops = {}
# 0-derivative
ops['W(u)'] = -W(uS).subs(uS, u)
# 1-derivative
ops['P^iD_ilnN'] = clock
# 2-derivative, scalar
ops['(D.P)^2'] = -(gm/2)*d**2
ops['F_ijF^ij'] = sp.Integer(0)          # identically 0 for radial gradient P
ops['(P.DlnN)^2'] = -clock**2
ops['(D_iu)(D^iu)'] = -(gm/2)*(sp.diff(u, r))**2/f
ops['D_i(P^i d) tot.div.'] = 0           # total derivative: no bulk
# kinetic (time) - identically zero on a static background
ops['E_iE^i'] = sp.Integer(0)

print("operator                Pi_O = -3 dL/dchi      (symbolic)")
for nm, L in ops.items():
    if L == 0:
        print(f"  {nm:26s}  0")
        continue
    Pi = sp.simplify(-3*sp.diff(L, ch)).subs(ch, 0)
    print(f"  {nm:26s}  {Pi}")

print()
print("check: for -W(u), Pi =", sp.simplify(-3*sp.diff(-W(uS).subs(uS, u), ch).subs(ch, 0)))
print("   i.e. W'(u)*u  ->", sp.simplify((-3*sp.diff(-W(uS).subs(uS, u), ch)).subs(ch, 0)))
