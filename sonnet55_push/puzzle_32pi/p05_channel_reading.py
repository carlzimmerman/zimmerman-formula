#!/usr/bin/env python3
"""p05_channel_reading.py -- the factor 1/2 as a slope, and how many 'natural' dimension-dependences agree at d = 3.

READING (from real_research/reviews/kappa_unit_response_2026_09_20/ACTION_ROUTE.md): with s = c sqrt(G rho_L) and p = g/s, the interpolation
function mu = 1 - (1 - p)^N has mu'(0) = N, so the deep-MOND scale is a0 = s/N, i.e. kappa = 1/N.  The natural (no-free-factor) crossover is the
Rindler distance c^2/g = R* (kappa = 1, Z = sqrt(8 pi/3) = 2.894); the framework's 1/2 is N = 2.
PART A  the literature coefficients as N x the forced kernel:  Z = N sqrt(8 pi/3)  =>  N = Z/sqrt(8 pi/3).
PART B  five 'natural' d-dependences of kappa, all equal to 1/2 at d = 3 and different elsewhere:
   (1) two static response channels (PD02): kappa = 1/2 for every d
   (2) Tolman active-density count d-1 (PD11):  kappa = 1/(d-1)
   (3) D-dimensional Schwarzschild surface gravity (D-3)/(2 r_s):  kappa = (d-2)/2
   (4) enthalpy premise (M5-B, Lean):  kappa = (2/3)(D-1)/D = (2/3) d/(d+1)
   (5) fixed Z, forced kernel Z_f,d = 4 sqrt(pi/(d(d-1))):  kappa = Z_f,d / Z = sqrt(3/(2 d (d-1)))   (= the rigidity form (1/2) sqrt(6/((D-1)(D-2))))
Exit 0 = the algebra holds and the controls behave.
"""
import math
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

# ------------------------------------------------------------- A
p, N = sp.symbols('p N', positive=True)
mu = 1 - (1 - p)**N
check("A1  mu = 1 - (1 - p)^N has mu'(0) = N, hence a0 = s/N", sp.simplify(sp.diff(mu, p).subs(p, 0) - N) == 0)
Zf = math.sqrt(8 * math.pi / 3)
print(f"\n  forced kernel Z_f = sqrt(8 pi/3) = {Zf:.4f}   (kappa = 1);  N = Z/Z_f for the literature coefficients:")
lit = [("Milgrom 2 pi", 2 * math.pi), ("Verlinde 6", 6.0), ("framework sqrt(32 pi/3)", math.sqrt(32 * math.pi / 3)), ("Nariai-shell 3 sqrt 3", 3 * math.sqrt(3))]
Ns = {}
for nm, Z in lit:
    Ns[nm] = Z / Zf
    print(f"      {nm:<26} Z = {Z:.4f}   N = {Z / Zf:.4f}")
check("A2  the three coefficients within 1 sigma of SPARC (Milgrom, Verlinde, framework) are all N = 2 within 9%", all(abs(Ns[k] - 2) < 0.18 for k in ("Milgrom 2 pi", "Verlinde 6", "framework sqrt(32 pi/3)")))
check("A3  the framework's N is exactly 2", abs(Ns["framework sqrt(32 pi/3)"] - 2) < 1e-12)

# ------------------------------------------------------------- B
d = sp.symbols('d', positive=True)
cands = {
    "(1) two static channels": sp.Rational(1, 2) + 0 * d,
    "(2) Tolman count d-1": 1 / (d - 1),
    "(3) D-dim Schwarzschild (d-2)/2": (d - 2) / 2,
    "(4) enthalpy (2/3) d/(d+1)": sp.Rational(2, 3) * d / (d + 1),
    "(5) fixed-Z rigidity": sp.sqrt(sp.Rational(3, 2) / (d * (d - 1))),
}
print(f"\n  {'origin of kappa':<34}" + "".join(f"{'d=' + str(x):>9}" for x in range(2, 7)))
at3 = []
for nm, expr in cands.items():
    vals = [float(expr.subs(d, x)) for x in range(2, 7)]
    at3.append(float(expr.subs(d, 3)))
    print(f"  {nm:<34}" + "".join(f"{v:>9.4f}" for v in vals))
check("B1  all five equal exactly 1/2 at d = 3", all(abs(v - 0.5) < 1e-12 for v in at3))
spread4 = [float(e.subs(d, 4)) for e in cands.values()]
check("B2  at d = 4 they disagree (range %.3f to %.3f): d = 3 cannot say which structural origin is real" % (min(spread4), max(spread4)), max(spread4) - min(spread4) > 0.5)
# control: (5) really is Z_f,d/Z
Zfd = 4 * sp.sqrt(sp.pi / (d * (d - 1)))
check("B3  form (5) equals Z_f,d/Z with Z = 2 sqrt(8 pi/3) and equals (1/2) sqrt(6/(d(d-1)))",
      sp.simplify((Zfd / (2 * sp.sqrt(8 * sp.pi / 3)))**2 - sp.Rational(3, 2) / (d * (d - 1))) == 0 and sp.simplify((sp.Rational(1, 2) * sp.sqrt(6 / (d * (d - 1))))**2 - sp.Rational(3, 2) / (d * (d - 1))) == 0)
check("C1  control: a wrong candidate kappa = 1/d is NOT 1/2 at d = 3", abs((1 / 3) - 0.5) > 0.1)
print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
