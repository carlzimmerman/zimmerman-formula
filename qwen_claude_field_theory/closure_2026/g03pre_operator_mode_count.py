#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03pre -- mode count, health and dispersion of the scalar sector with the f32 operator, in the aether rest frame.
Quadratic scalar Lagrangian of the host with Y -> Y + xi^2 |grad_perp V|^2 (aether at rest: V = grad chi, grad_perp V = the Hessian):
L2 = (K2/2) chidot^2 - (J/2) [ |grad chi|^2 + xi^2 |grad grad chi|^2 ].  Checks can fail."""
import sympy as sp, sys
t, x, k, w = sp.symbols('t x k omega', real=True); K2, J, xi = sp.symbols('K_2 J xi', positive=True)
chi = sp.Function('chi')(t, x)
L2 = sp.Rational(1, 2)*K2*sp.diff(chi, t)**2 - sp.Rational(1, 2)*J*(sp.diff(chi, x)**2 + xi**2*sp.diff(chi, x, 2)**2)
from sympy.calculus.euler import euler_equations
eom = euler_equations(L2, chi, [t, x])[0].lhs
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
print("g03pre -- the f32 operator's scalar sector, aether rest frame")
print(f"  Euler-Lagrange: {sp.simplify(eom)} = 0")
orders_t = [n for n in range(1, 5) if eom.has(sp.Derivative(chi, (t, n)))]
check("M1 the field equation is second order in time and fourth order in space: one degree of freedom (two phase-space dimensions), no Ostrogradsky mode",
      max(orders_t) == 2 and eom.has(sp.Derivative(chi, (x, 4))), f"time-derivative orders present {orders_t}")
p = sp.symbols('p'); chidot = p/K2
H = sp.simplify(p*chidot - L2.subs(sp.diff(chi, t), chidot))
check("H1 the Hamiltonian density p^2/(2K_2) + (J/2)[(grad chi)^2 + xi^2 (grad grad chi)^2] is positive definite for K_2, J, xi^2 > 0: no ghost, no gradient instability",
      sp.simplify(H - (p**2/(2*K2) + J/2*(sp.diff(chi, x)**2 + xi**2*sp.diff(chi, x, 2)**2))) == 0)
disp = sp.simplify(eom.subs(chi, sp.exp(sp.I*(k*x - w*t))).doit()/sp.exp(sp.I*(k*x - w*t)))
w2 = sp.solve(disp, w**2)[0]
check("D1 dispersion omega^2 = (J/K_2) k^2 (1 + xi^2 k^2), the Bogoliubov form (xi = healing length)", sp.simplify(w2 - J/K2*k**2*(1 + xi**2*k**2)) == 0, f"omega^2 = {w2}")
cs = sp.sqrt(J/K2); vg = sp.simplify(sp.diff(sp.sqrt(w2), k))
vg1 = sp.simplify(vg.subs(k, 1/xi)/cs); vg_big = sp.limit(vg/(cs*2*xi*k), k, sp.oo)
check("C1 group velocity exceeds the sound speed above k = 1/xi: v_g/c_s = 3/sqrt(2) at k = 1/xi and -> 2 xi k for xi k >> 1 -- the number the causal screen must judge "
      "(preferred-frame theory: not a paradox by itself; at Solar-System k, xi k ~ 1e4, the scalar's short-wavelength front is ~2e4 c_s)",
      sp.simplify(vg1 - 3/sp.sqrt(2)) == 0 and vg_big == 1, f"v_g/c_s(k = 1/xi) = {vg1}, asymptotic v_g/(2 c_s xi k) = {vg_big}")
print("  handed to G03: the operator adds no mode to the host; its price is the superluminal short-wavelength front in the aether frame, to be judged by the spec's causality gate (G11), not here.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
