#!/usr/bin/env python3
"""KT3: can chi's vacuum fix b in KT2's action? See FROZEN_CRITERIA.md."""
import json, math, os, sys
import sympy as sp

MUT = os.environ.get("KT3_MUTATE") == "1"
FAC = 4 if MUT else 8   # field-term coupling is FAC pi G
chi, G, rho, c, b, C, Z = sp.symbols("chi G rho c b C Z", positive=True)
s = c * sp.sqrt(G * rho)
def U(n):
    return sp.integrate(sp.expand(n * (1 - chi) ** 2 * chi ** (n - 3)), chi)
def kappa2(n, DU):
    return sp.Rational(FAC) * sp.pi / (n**2 * DU)
# V1
DU = sp.Symbol("DU", positive=True)
bsol = sp.solve(sp.Eq((s / b) ** 2 * DU / (FAC * sp.pi * G), rho * c**2), b)[0]
k = sp.simplify(1 / (2 * bsol))
print("V1 b =", bsol, "; kappa at n=2 =", k, "; kappa^2 =", sp.simplify(k**2))
print("V1 DU needed for kappa = 1/2:", sp.solve(sp.Eq(k, sp.Rational(1, 2)), DU))
print("V1 d kappa / d DU =", sp.simplify(sp.diff(k, DU)), " (DU = U(1)+C, so the zero mode decides)")
lg, lr, lc = sp.symbols("l_G l_r l_c", positive=True)
a0 = k * s
print("I3 scale invariant:", sp.simplify(a0.subs({G: lg*G, rho: lr*rho, c: lc*c}, simultaneous=True)/(lc*c*sp.sqrt(lg*G*lr*rho)) - k) == 0)
# V2
Ga, ca, hb = 6.674e-11, 2.99792458e8, 1.0546e-34
H0 = 67.4e3 / 3.0857e22
rhoL = 0.685 * 3 * H0**2 / (8 * math.pi * Ga)
sv = ca * math.sqrt(Ga * rhoL)
aP = math.sqrt(ca**7 / (hb * Ga))
U2 = U(2)
def row(name, n, val):
    k2 = float(kappa2(n, val))
    kv = math.sqrt(k2) if k2 > 0 else float("nan")
    print(f"V2 {name}: DU {float(val):.4f} kappa {kv:.4f} window {0.227 <= kv <= 0.607} half {abs(kv-0.5) < 1e-9}")
    return dict(name=name, DU=float(val), kappa=kv)
rows = [row("a C=0 n=2", 2, abs(U2.subs(chi, 1))),
        row("b U(1/2)=0", 2, abs(U2.subs(chi, 1) - U2.subs(chi, sp.Rational(1, 2))))]
Yc = aP / sv
chic = 1 / (1 + Yc)
rows.append(row(f"c Planck Y_c {Yc:.2e} hbar enters", 2, abs(-3 - (2 * math.log(chic) - 4 * chic + chic**2))))
rows.append(row("d Y=1 same as b at b=1", 2, abs(U2.subs(chi, 1) - U2.subs(chi, sp.Rational(1, 2)))))
for n in (3, 4):
    rows.append(row(f"e C=0 n={n}", n, abs(U(n).subs(chi, 1))))
# V3: K delta'' + 3 H K delta' = -(s/b)^2 V'/(2) with V'(chi)=2(1-chi)^2/chi -> at chi~1: 2 delta^2
t, H, K, A = sp.symbols("t H K A", positive=True)
d = sp.Function("d")
sol = 3 * H / (A * t)
res = sp.simplify(3 * H * sp.diff(sol, t) + A * sol**2)
print("V3 late-time slow roll: 3H d' = -A d^2, A = 2 s^2/(b^2 K); d = 3H/(A t), residual", res)
print("V3 V'(1), V''(1):", [sp.simplify(sp.diff(2 * (1 - chi) ** 2 / chi, chi, m).subs(chi, 1)) for m in (0, 1)], "V'''(1) ==", sp.diff(2 * (1 - chi) ** 2 / chi, chi, 2).subs(chi, 1))
print("V3 d depends on K/b^2 only as an amplitude; attractor exists for every b and C. Delta w ~ K (d')^2 / rho falls as t^-4: no fix, and w-1 shift below any data at late time with K free.")
lab = "EXACT CANDIDATE" if any(abs(r["kappa"] - 0.5) < 1e-9 for r in rows) else ("CONSISTENT" if any(0.227 <= r["kappa"] <= 0.607 for r in rows) else "NO FIX")
print("LABEL", lab)
json.dump(dict(rows=rows, label=lab), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt3_MUTATE.json" if MUT else "kt3.json"), "w"), indent=1)
if MUT:
    print("MUTATE: kappa^2 should be half of normal at same DU:", kappa2(2, 3), "(normal 2 pi/3)")
    sys.exit(1)
