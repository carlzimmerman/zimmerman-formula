#!/usr/bin/env python3
"""KT6: cubic-lattice reading of c_E. See FROZEN_CRITERIA.md."""
import json, math, os, sys
import numpy as np, sympy as sp
from scipy import integrate
from scipy.special import ive
MUT = os.environ.get("KT6_MUTATE") == "1"
D = 2 if MUT else 3
def i0e(x):
    """scaled I0; this scipy returns nan at large x, so use the asymptotic form there"""
    return ive(0, x) if x < 1e4 else (1 + 1 / (8 * x)) / math.sqrt(2 * math.pi * x)
def Gdiff(m):
    """G(0) - G(m^2) = int (1 - exp(-m^2 t)) ive(0, 2t)^D dt, in log t"""
    f = lambda lt: (-np.expm1(-m * m * np.exp(lt))) * i0e(2 * np.exp(lt)) ** D * np.exp(lt)
    return integrate.quad(f, -30, 25, limit=800, epsabs=1e-9, epsrel=1e-8)[0]
target = 1 / (4 * math.pi)
rows = []
for m in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01):
    v = Gdiff(m) / m
    rows.append((m, v, v / target))
    print(f"m a {m}: [G(0)-G(m^2)]/m = {v:.6f}, ratio to 1/(4 pi) {v/target:.4f}")
q1 = abs(rows[-1][2] - 1) < 0.01
print("Q1 universal to 1 percent at smallest m:", q1)
if MUT:
    print("MUTATE bites" if not q1 else "MUTATE FAILED")
    sys.exit(1)
print("Q2 c_E = 2 (T/2 per mode) gives kappa", math.sqrt(2 * 2 / 8), "; c_E = 1 gives", math.sqrt(2 * 1 / 8), ". Gravity sources total energy, kinetic included, so T per mode.")
T, hb, om = sp.symbols("T hbar omega", positive=True)
F = T * sp.log(hb * om / T)
U = T
w = sp.simplify(-F / U)
print("Q3 F =", F, "; U =", U, "; rho + p = (U - F)/V ∝", sp.simplify(U - F), "; w =", w)
for r in (10, 100, 1e6):
    print(f"   T/(hbar omega) = {r}: w = {math.log(r):.2f}")
print("Q3 w = -1 needs T/(hbar omega) =", sp.exp(-1).evalf(4), "which isn't the classical limit; check: w at that T =", sp.simplify(w.subs(T, hb * om * sp.exp(-1))))
lab = "COUNTING WORKS, EOS FAILS" if q1 else "NO"
print("LABEL", lab)
json.dump(dict(rows=rows, q1=bool(q1), label=lab), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "kt6.json"), "w"), indent=1)
