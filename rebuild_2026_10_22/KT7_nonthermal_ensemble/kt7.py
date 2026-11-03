#!/usr/bin/env python3
"""KT7: non-thermal Gaussian ensembles against odd term, w = -1, counting. See FROZEN_CRITERIA.md."""
import json, math, os, sys
import numpy as np, sympy as sp
from scipy import integrate
from scipy.special import ive
MUT = os.environ.get("KT7_MUTATE") == "1"
def i0e(x):
    return ive(0, x) if x < 1e4 else (1 + 1 / (8 * x)) / math.sqrt(2 * math.pi * x)
def G(m):
    f = lambda lt: math.exp(-m * m * math.exp(lt)) * i0e(2 * math.exp(lt)) ** 3 * math.exp(lt)
    return integrate.quad(f, -30, 25, limit=800, epsabs=1e-9, epsrel=1e-8)[0]
print("E1 frozen, a = 1, A = 1 per cell: <psi^2> = G, <grad^2> = 1 - m^2 G (sum rule: S (K + m^2) = 1 per mode)")
sgn = 1 if MUT else -1
out = {}
for m in (0.5, 0.2, 0.1, 0.01):
    g_ = G(m)
    gr = 1 - m * m * g_
    rho = .5 * gr + .5 * m * m * g_
    p = sgn * gr / 6 - .5 * m * m * g_
    print(f"  m {m}: rho per cell {rho:.5f} (A/2), w = {p/rho:+.4f}")
    out[str(m)] = dict(rho=rho, w=p / rho)
if MUT:
    print("MUTATE bites" if out["0.01"]["w"] > .3 else "MUTATE FAILED")
    sys.exit(1)
print("E1 c_E = 2, kappa =", math.sqrt(2 * 2 / 8), "; rho_DE window [0.227, 0.607]; rho_crit [0.189, 0.501]: outside both")
k, mm, D, A = sp.symbols("k m D A", positive=True)
e2 = sp.simplify(sp.integrate(4 * sp.pi * k**2 / (2 * sp.pi) ** 3 * D / (k**2 + mm**2) ** 2, (k, 0, sp.oo)))
print("E2 G(0) =", e2, ": diverges as m -> 0, no linear term")
def I4(a):
    return sp.gamma(a - 2) / (16 * sp.pi**2 * sp.gamma(a)) * mm ** (4 - 2 * a)
print("E3 a = 1 in 4D, dim-reg pole; nonanalytic part of G(0) ~ m^2 ln m^2 / (16 pi^2): V' ~ delta^3 ln delta, g ~ delta^(3/2), mu ~ delta ~ Y^(2/3): R1 fails")
e4 = sp.simplify(I4(sp.Rational(3, 2)))
print("E4 a = 3/2: G(0) =", e4)
ratio = sp.simplify((e4 / mm) / (-1 / (4 * sp.pi)))
print("E4 coefficient ratio to thermal -1/(4 pi):", ratio)
k2_c1 = sp.Rational(2, 8) * ratio
Vm = sp.integrate(A / 2 * e4 * 2 * mm, mm)
ce = sp.simplify(1 / (sp.Abs(Vm.subs(mm, 1)) / A))
k2_sc = sp.simplify(k2_c1 * ce)
print("E4 c_E = 1: kappa^2 =", k2_c1, "=", float(sp.sqrt(k2_c1)), "(kappa); V =", Vm, "; self-consistent c_E =", ce, ": kappa^2 =", k2_sc, "kappa =", float(sp.sqrt(k2_sc)))
print("E4 c_E = 1 has no meaning here: with w = -1 energy is V + C, so no separate count (R3 fails), and C is KT3's zero mode")
tbl = {"E1": "R1 yes, R2 no (w -> -1/3), R3 yes (c_E = 2)", "E2": "R1 no", "E3": "R1 no, R2 yes, R3 no", "E4": "R1 yes by construction, R2 yes, R3 no", "thermal KT6": "R1 yes, R2 no (w > 0), R3 yes"}
for a_, b_ in tbl.items():
    print(" ", a_, ":", b_)
print("LABEL NO-GO IN THIS CLASS")
json.dump(dict(E1=out, table=tbl, label="NO-GO IN THIS CLASS", k2_c1=str(k2_c1), k2_sc=str(k2_sc)), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt7.json"), "w"), indent=1)
