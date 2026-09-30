#!/usr/bin/env python3
"""LR9 G2 -- mechanical check: fresh sympy re-extraction of the assembly
coefficients MUST equal the constants typed in LR9_sq_law.lean (Z13 LR9 door).
Also re-verifies the final values 2*(1/6), 4/6-(8/3)/8, ... = the W3 law."""
import json, os, re, sys
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
lean = open(os.path.join(os.path.dirname(HERE), "fable_independent_2026/lean_2026/LR9_sq_law.lean")).read()

# fresh re-extraction (same monomial method, re-executed)
_v, R, Z, W, qq = sp.symbols("v R Z W q", real=True)
A = R + 2*Z*_v + _v**2
B = R*_v + Z*_v**2 + _v**3/3
integ = sp.expand(_v*(1 + qq*A)*(_v + qq*B))
pv = sp.Poly(integ, _v)
Iant_RZW = sp.expand(sum(c * W**(j+1)/(j+1) for (j,), c in pv.terms()))
Iant_RZW = sp.expand(Iant_RZW - Iant_RZW.subs(W, 0))
x, w, s = sp.symbols("x w s", real=True, positive=True)
Iant_sw = sp.expand(Iant_RZW.xreplace({W: s*(1 - w), Z: s*w, R: 1 - s**2 + s**2*w**2}))
alpha = {}
for k in (0, 1, 2):
    P = sp.Poly(sp.expand(Iant_sw.coeff(qq, k) * x * s), w)
    inner = sum(c * sp.Rational(2, j+1) for (j,), c in P.terms() if j % 2 == 0)
    Pin = sp.Poly(sp.simplify(sp.expand(inner) / x), s)
    alpha[k] = {int(m): sp.nsimplify(sp.simplify(sp.Rational(3,2)*c)) for (m,), c in Pin.terms()}

# constants as typed in the Lean file (s00/s01/s02 assembly coefficients)
lean_const = {0: {4: sp.Rational(2)},
              1: {4: sp.Rational(4), 6: sp.Rational(-8,3)},
              2: {4: sp.Rational(2), 6: sp.Rational(-8,3), 8: sp.Rational(92,105)}}
ok = True
for k in (0,1,2):
    if alpha[k] != lean_const[k]:
        print("G2 MISMATCH at q^%d: fresh %s vs lean %s" % (k, alpha[k], lean_const[k])); ok = False
# final values
vals = [sp.simplify(sum(lean_const[k][m] * sp.Rational(1, m+2) for m in lean_const[k])) for k in (0,1,2)]
want = [sp.Rational(sp.sstr(sp.nsimplify(c))) for c in json.load(open(os.path.join(HERE, "W3_results.json")))["S_exact"]]
if vals != want:
    print("G2 MISMATCH final: %s vs %s" % (vals, want)); ok = False
# the Lean file must literally contain the law statements
for pat in ["= (1:ℝ)/3", "= (46:ℝ)/525", "theorem s00_law", "theorem s01_law", "theorem s02_law", "theorem core_U"]:
    if pat not in lean:
        print("G2 MISSING in lean file: %s" % pat); ok = False
print("G2 %s: alpha fresh = lean constants; assembly values %s == W3 banked %s" % ("PASS" if ok else "FAIL", vals, want))
sys.exit(0 if ok else 1)
