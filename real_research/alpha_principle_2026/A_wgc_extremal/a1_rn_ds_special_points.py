#!/usr/bin/env python3
"""A1 -- RN-de Sitter special points (cold, ultracold, Nariai) in closed form.
Pre-registered in A_PREREGISTRATION.md (S1-S3). Run: python3 a1_rn_ds_special_points.py [MUTATE]
Exit 0 iff all checks pass; MUTATE (wrong Q^2 on the degenerate curve) must exit 1."""
import sys
import sympy as sp
import numpy as np

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
r, M, Q2, L, y, r0 = sp.symbols("r M Q2 Lambda y r0", positive=True)
checks = []
def chk(name, ok, info=""):
    checks.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")

# P(r) = r^2 f(r): f = 1 - 2M/r + Q2/r^2 - Lambda r^2/3
P = -L*r**4/3 + r**2 - 2*M*r + Q2
f = P/r**2
# closed-form curve of degenerate roots, parametrised by y = Lambda r0^2
Q2_curve = r0**2*(1 - (2*y if MUT else y))
M_curve = r0*(1 - sp.Rational(2, 3)*y)
sub = {Q2: Q2_curve, M: M_curve, L: y/r0**2}

# S1 symbolic
P0 = sp.simplify(P.subs(sub).subs(r, r0))
P1 = sp.simplify(sp.diff(P, r).subs(sub).subs(r, r0))
chk("S1a P(r0)=0 on the curve", sp.simplify(P0) == 0, f"-> {P0}")
chk("S1b P'(r0)=0 on the curve", sp.simplify(P1) == 0, f"-> {P1}")
# uniqueness: solve f=f'=0 for (M,Q2) at given r0, L
sol = sp.solve([P.subs(r, r0), sp.diff(P, r).subs(r, r0)], [M, Q2], dict=True)[0]
sol_M = sp.simplify(sol[M].subs(L, y/r0**2)); sol_Q2 = sp.simplify(sol[Q2].subs(L, y/r0**2))
print("solve():  M =", sol_M, "   Q^2 =", sol_Q2)
chk("S1c solve() gives M = r0(1-2y/3)", sp.simplify(sol_M - M_curve) == 0)
chk("S1d solve() gives Q^2 = r0^2(1-y)", sp.simplify(sol_Q2 - Q2_curve) == 0)
P2 = sp.simplify(sp.diff(P, r, 2).subs(sub).subs(r, r0))
print("P''(r0) =", P2)
# triple root: P''=0 => y=1/2
ysol = sp.solve(sp.Eq(P2, 0), y)
chk("S1e triple root only at y=1/2", ysol == [sp.Rational(1, 2)], f"-> {ysol}")

# numerical root-multiplicity classification (r0 = 1, Lambda = y)
ok_all = True
for yy in [0.05, 0.2, 0.4, 0.5, 0.6, 0.75, 0.9, 0.99, 1.0]:
    Mn = 1 - 2*yy/3; Q2n = 1 - yy
    if MUT: Q2n = 1 - 2*yy
    coeffs = [-yy/3, 0, 1, -2*Mn, Q2n]
    roots = np.roots(coeffs)
    at1 = np.sum(np.abs(roots - 1) < 1e-3)         # multiplicity at r0 (numerical, root splitting ~ eps^(1/k))
    pos = sorted([z.real for z in roots if abs(z.imag) < 1e-9 and z.real > 1e-9])
    if abs(yy - 0.5) < 1e-12: lab = "ultracold"; exp_mult = 3
    elif yy < 0.5: lab = "cold"; exp_mult = 2
    elif yy < 1: lab = "Nariai(charged)"; exp_mult = 2
    else: lab = "Nariai(Schw-dS)"; exp_mult = 2
    ok = (at1 == exp_mult)
    # the remaining positive root: outside r0 for cold, inside r0 for charged Nariai
    others = [p for p in pos if abs(p - 1) > 5e-2]
    if lab == "cold": ok = ok and len(others) == 1 and others[0] > 1
    if lab == "Nariai(charged)": ok = ok and len(others) == 1 and others[0] < 1
    if lab == "Nariai(Schw-dS)": ok = ok and len(others) == 0
    ok_all &= ok
    print(f"   y={yy:5.2f} {lab:16s} mult@r0={at1} (expect {exp_mult}) other positive roots={np.round(others,4)} {'ok' if ok else 'BAD'}")
chk("S1f numerical multiplicity/branch labels on 9 points", ok_all)

# S2
y_ = sp.symbols("y_", positive=True)
Q2L = sp.simplify((Q2_curve*(y_/r0**2)).subs(y, y_))
chk("S2a Q^2 Lambda = y(1-y)", sp.simplify(Q2L - y_*(1 - y_)) == 0, f"-> {Q2L}")
ymax = sp.solve(sp.diff(y_*(1 - y_), y_), y_)
chk("S2b max of Q^2 Lambda at y=1/2 with value 1/4", ymax == [sp.Rational(1, 2)] and (y_*(1 - y_)).subs(y_, sp.Rational(1, 2)) == sp.Rational(1, 4))
z2 = sp.simplify((Q2_curve/M_curve**2).subs(y, y_))
print("z_ext^2 = Q^2/M^2 =", sp.factor(z2))
z_half = sp.simplify(z2.subs(y_, sp.Rational(1, 2)))
chk("S2c ultracold z^2 = 9/8", z_half == sp.Rational(9, 8), f"-> {z_half}")
chk("S2d Schwarzschild-dS Nariai (y=1): Q=0, M^2 Lambda = 1/9",
    sp.simplify(Q2_curve.subs(y, 1)) == 0 and sp.simplify((M_curve**2*y/r0**2).subs(y, 1)) == sp.Rational(1, 9))
grid = np.linspace(0.0, 0.5, 5001)
zn = np.sqrt((1 - grid)/(1 - 2*grid/3)**2)
chk("S2e z_ext in [1, 3/(2 sqrt2)] on the cold branch (numeric grid)",
    zn.min() >= 1 - 1e-15 and zn.max() <= 3/(2*np.sqrt(2)) + 1e-12, f"min={zn.min():.6f} max={zn.max():.6f} 3/(2sqrt2)={3/(2*np.sqrt(2)):.6f}")
# small-y expansion: z = 1 + y/6 + ...
ser = sp.series(sp.sqrt(1 - y_)/(1 - 2*y_/3), y_, 0, 3)
print("z_ext series in y = Lambda r0^2:", ser)
chk("S2f z_ext = 1 + y/6 + O(y^2)", sp.simplify(ser.removeO().coeff(y_, 1) - sp.Rational(1, 6)) == 0)

# S3 : temperature vanishes at every point of the degenerate curve (f'(r0)=0)
fp = sp.simplify(sp.diff(f, r).subs(sub).subs(r, r0))
chk("S3 T = f'(r0)/4pi = 0 on the whole curve (cold and Nariai limits)", fp == 0, f"-> {fp}")

# consequence: a pure-number scan of special charge values (Planck-unit statement)
x = sp.Rational(285, 100)*sp.Integer(10)**(-122)   # Lambda l_P^2 (AH5 value)
Qmax_over_lP = sp.sqrt(1/(4*x))
print(f"\nQ_ultracold / l_P = 1/(2 sqrt x) = {float(Qmax_over_lP):.4e}  (x = {float(x):.3e})")
chk("consequence: Q^2 Lambda on the special curve depends only on the pure number y (no alpha, no other symbol)", Q2L.free_symbols == {y_}, f"free symbols: {Q2L.free_symbols}")

print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(c[1] for c in checks), len(checks), MUT))
sys.exit(0 if all(c[1] for c in checks) else 1)
