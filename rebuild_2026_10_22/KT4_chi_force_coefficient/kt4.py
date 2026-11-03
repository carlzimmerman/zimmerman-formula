#!/usr/bin/env python3
"""KT4: chi's force coefficient alpha with the vacuum constant set to rho c^2. See FROZEN_CRITERIA.md."""
import json, os, sys
import sympy as sp
MUT = os.environ.get("KT4_MUTATE") == "1"
FAC = 4 if MUT else 8
chi, g, G, rho, c, al, r, R, m, T, H, hb = sp.symbols("chi g G rho c alpha r R m T H hbar", positive=True)
# R1: d/dchi [ -(1-chi^2) g^2/(FAC pi G) - rho c^2 alpha u ] = 0
eom = 2 * chi * g**2 / (FAC * sp.pi * G) - rho * c**2 * al * (1 - chi) ** 2 / chi
gs = sp.solve(eom, g)[0]
Y = gs / (c * sp.sqrt(G * rho))
# Y = (1-chi)/(b chi) -> b = (1-chi)/(chi Y)
b = sp.simplify((1 - chi) / (chi * Y))
k2 = sp.simplify(1 / (4 * b**2))
print("R1 b =", b, "; kappa^2 =", k2, "; chi independent:", not k2.has(chi))
print("R1 alpha for kappa=1/2:", sp.solve(sp.Eq(k2, sp.Rational(1, 4)), al))
rows = {}
for name, a in [("1", 1), ("2", 2), ("1/2", sp.Rational(1, 2)), ("1/(4 pi) TARGET", 1 / (4 * sp.pi)), ("1/(8 pi) needs T", 1 / (8 * sp.pi))]:
    kv = sp.sqrt(k2.subs(al, a))
    fv = float(kv)
    rows[name] = fv
    print(f"R2 alpha {name}: kappa {sp.simplify(kv)} = {fv:.4f}; window {0.227 <= fv <= 0.607}; half {sp.simplify(kv - sp.Rational(1,2)) == 0}")
# R3
Eball = sp.integrate(4 * sp.pi * r**2 / (4 * sp.pi * r), (r, 0, R))
print("R3 massless: int d3y /(4 pi r) over ball =", Eball, "; pi left:", Eball.has(sp.pi))
Eyuk = sp.integrate(4 * sp.pi * r**2 * sp.exp(-m * r) / (4 * sp.pi * r), (r, 0, sp.oo))
print("R3 massive: int d3y exp(-m r)/(4 pi r) =", Eyuk, "; pi left:", Eyuk.has(sp.pi))
# R4
print("R4 G(0) regulated = -m/(4 pi): keeps 1/(4 pi) only for a fluctuating field; amplitude T")
f = -T * m**3 / (12 * sp.pi)
print("R4 d f/d(m^2) =", sp.simplify(sp.diff(f, m) / (2 * m)))
Tds = hb * H / (2 * sp.pi)
print("R4 with T_dS: amplitude T m/(4 pi) =", sp.simplify(Tds * m / (4 * sp.pi)), "; hbar present:", True, "; extra 1/(2 pi) from T_dS shifts the pi weight")
lab = "NEEDS FLUCTUATIONS" if not Eball.has(sp.pi) and not Eyuk.has(sp.pi) else "NO ROUTE"
print("LABEL", lab)
json.dump(dict(rows=rows, label=lab), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt4_MUTATE.json" if MUT else "kt4.json"), "w"), indent=1)
if MUT:
    print("MUTATE kappa^2 =", k2, "expected pi alpha / 2:", sp.simplify(k2 - sp.pi * al / 2) == 0)
    sys.exit(1)
