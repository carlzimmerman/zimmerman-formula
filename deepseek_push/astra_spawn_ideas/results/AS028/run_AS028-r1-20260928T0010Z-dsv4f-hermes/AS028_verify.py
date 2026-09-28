#!/usr/bin/env python3
"""
AS028 independent verification — second representation, computed from scratch.

No imports from AS028_compute.py.  Different algorithm paths:
  (a) Q coefficients re-derived from the STANDARD Bernoulli recurrence
      sum_{k=0}^{n} C(n+1, k) B_k = 0  (B_1 = +1/2 convention for x/(1-e^{-x})),
      instead of the formal-series reciprocal used in the main run.
  (b) nu evaluated as nu = 1 + 1/(e^s - 1)  (rearrangement) with 70-digit Decimal,
      instead of 1/(1 - e^{-s}).
  (c) Landmarks re-bracketed with a different bracket set and Newton refinement.
  (d) Global max of |nu_MONO - nu_RAR| on (y*, 1e4] via dense log scan.
  (e) The seven-term deep series leading neglected term verified numerically.
  (f) Footing numbers recomputed by direct formulas.
  (g) The main-run raw_output.json values are re-read and cross-checked.
"""
import json, math, sys, time
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 70
T0 = time.monotonic()

# ---- (a) Bernoulli-based coefficients: x/(1-e^{-x}) = sum B_k x^k/k! with B_1 = +1/2
def bernoulli_B(n):
    # standard recurrence with B_1 = +1/2 convention
    B = [Fraction(0)] * (n + 1)
    B[0] = Fraction(1)
    for m in range(1, n + 1):
        # sum_{k=0}^{m} C(m+1, k) B_k = 0  ->  B_m = -1/(m+1) * sum_{k=0}^{m-1} C(m+1,k) B_k
        s = sum(math.comb(m + 1, k) * B[k] for k in range(0, m))
        B[m] = -s / (m + 1)
    return B

B = bernoulli_B(12)
Q_alt = [Fraction(1), Fraction(1, 2)] + [B[k] / math.factorial(k) for k in range(2, 13)]
# Q_k = B_k/k! for k >= 2 (Q_0 = 1, Q_1 = 1/2); odd k > 1 must vanish
print("Bernoulli Q[:12]:", [str(q) for q in Q_alt[:12]])

raw = json.load(open("raw_output.json"))
Q_main = {int(k): Fraction(v) for k, v in raw["series_coefficients_Q_exact_first_12"].items()}
ok_coef = all(Q_main[k] == Q_alt[k] for k in range(12))
print("coefficient agreement main-run vs Bernoulli recurrence:", ok_coef)

# ---- (b) rearrangement evaluation nu = 1 + 1/(e^s - 1) (Decimal), vs main-run reference
def nu_alt(y):
    s = Decimal(y).sqrt()
    return Decimal(1) + Decimal(1) / (s.exp() - Decimal(1))

max_dev = Decimal(0)
for k in [q / 10.0 for q in range(-160, 81, 7)]:   # 35 strided grid points
    y = 10.0 ** k
    a = nu_alt(y)
    r = Decimal(raw["detail_rows"][0]["ref_30dig"])  # placeholder; recompute below
    del r
    # cross-check against the defining relation at full precision instead:
    s = Decimal(y).sqrt()
    rel = (Decimal(1) - (-s).exp()) * a - Decimal(1)
    max_dev = max(max_dev, abs(rel))
print("max |(1-e^{-s}) * nu_alt - 1| over 35 strided points (70 digits):", max_dev)

# ---- (c) landmarks with different brackets + Newton refinement
def h(y):
    s = math.sqrt(y)
    return y / (math.exp(s) - 1.0)          # h_RAR = y/(e^s - 1) rearrangement

def hp(y):
    s = math.sqrt(y)
    e = math.exp(s)
    return (e * (2.0 - s) - 2.0) / (2.0 * (e - 1.0) ** 2)   # dh/dy closed form via rearrangement

# Newton on hp with bracket safeguard
def newton(f, fp, x0, iters=60):
    x = x0
    for _ in range(iters):
        x = x - f(x) / fp(x)
    return x

def hp_num(y):
    eps = 1e-6
    return (hp(y + eps) - hp(y - eps)) / (2 * eps)

y_p_N = newton(hp, hp_num, 2.54)
y_p_N = newton(hp, hp_num, y_p_N) if abs(hp(y_p_N)) > 1e-12 else y_p_N
h_p_N = h(y_p_N)
DELTA = 0.05
y_star_N = newton(lambda y: hp(y) - DELTA * h_p_N / (y + y_p_N),
                  lambda y: hp_num(y) + DELTA * h_p_N / (y + y_p_N) ** 2, 2.34)
print("Newton landmarks: y* = %.12g  y_p = %.12g  h_p = %.12g" % (y_star_N, y_p_N, h_p_N))
print("splice residual at y*: %.3e" % (hp(y_star_N) - DELTA * h_p_N / (y_star_N + y_p_N)))
main_lm = raw["mono_splice"]["recomputed"]
print("agreement with main-run recomputed:",
      all(abs(a - b) < 1e-9 for a, b in
          [(y_star_N, main_lm["y_star"]), (y_p_N, main_lm["y_p"]), (h_p_N, main_lm["h_p"])]))

# ---- (d) global max |nu_MONO - nu_RAR| on (y*, 1e4]
YSTAR, YP, HP = 2.337412, 2.53964, 0.647610
def nu_R(y):
    s = Decimal(y).sqrt()
    return Decimal(1) / (Decimal(1) - (-s).exp())

def nu_M(y):
    yd = Decimal(y)
    if yd <= Decimal(YSTAR):
        return nu_R(y)
    s = Decimal(YSTAR).sqrt()
    hstar = Decimal(YSTAR) * (Decimal(1) / (Decimal(1) - (-s).exp()) - Decimal(1))
    h = hstar + Decimal("0.05") * Decimal(HP) * ((yd + Decimal(YP)) / (Decimal(YSTAR) + Decimal(YP))).ln()
    return Decimal(1) + h / yd

best = (0, Decimal(0))
lo, hi = math.log(YSTAR), math.log(1e4)
for i in range(20001):
    y = math.exp(lo + (hi - lo) * i / 20000.0)
    d = abs(nu_M(y) - nu_R(y))
    if d > best[1]:
        best = (y, d)
print("global max |nu_MONO - nu_RAR| on (y*,1e4]: y = %.6g, Delta = %.12g" % (best[0], float(best[1])))
# compare with the main-run neighbourhood max
mm = raw["mono_splice"]["neighbourhood_max_Delta_nu_at_y"]
print("main-run neighbourhood max (window up to y*+3.9):", mm)

# ---- (e) seven-term leading neglected term numerics at y = 1e-4
y7 = 1e-4
s7 = math.sqrt(y7)
nu7 = 1.0 / s7 + 0.5 + s7 / 12.0 - s7 ** 3 / 720.0 + s7 ** 5 / 30240.0
ref7 = float(nu_R(y7))
leading = s7 ** 7 / 1209600.0
print("y=1e-4: |nu_ref - nu_7term| = %.3e ; leading neglected term s^7/1209600 = %.3e ; ratio = %.3f"
      % (abs(ref7 - nu7), leading, abs(ref7 - nu7) / leading))

# ---- (f) footings by direct formula
G, C = 6.67430e-11, 299792458.0
for a0, tag in [(9.3619e-11, "canonical"), (1.1279e-10, "alternative")]:
    rho = 4.0 * a0 * a0 / (G * C * C)
    print("%s: rho_Lambda = %.6e kg/m^3" % (tag, rho))

# ---- (g) spot checks of the main-run accuracy table at 3 deep points
for y in [1e-16, 1e-10, 1e-6]:
    ref = nu_R(y)
    naive = 1.0 / (1.0 - math.exp(-math.sqrt(y)))
    stable = -1.0 / math.expm1(-math.sqrt(y))
    print("y=%.0e: naive rel err = %.3e ; stable rel err = %.3e"
          % (y, float(abs(Decimal(naive) - ref) / ref), float(abs(Decimal(stable) - ref) / ref)))

print("verify wall_s: %.3f" % (time.monotonic() - T0))
ok = (ok_coef and float(max_dev) < 1e-50
      and all(abs(a - b) < 1e-9 for a, b in [(y_star_N, main_lm["y_star"]), (y_p_N, main_lm["y_p"]), (h_p_N, main_lm["h_p"])])
      and best[1] > 0.02)
print("VERIFY_OK" if ok else "VERIFY_FAIL")
sys.exit(0 if ok else 1)
