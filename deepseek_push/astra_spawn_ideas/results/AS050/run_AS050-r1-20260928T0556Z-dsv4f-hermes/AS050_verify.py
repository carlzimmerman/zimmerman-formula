#!/usr/bin/env python3
# AS050 — independent verification (separate implementation from AS050_compute.py)
# Routes that differ from the main run:
#   (a) Bernoulli numbers via the B^- convention recurrence with sign map q_k = (-1)^k B^-_k/k!
#   (b) reference self-convergence: 70-digit vs 50-digit Decimal on the deep grid
#   (c) split-form identity x = y + h (h = -y*exp(-s)/expm1(-s)) vs direct expm1 form, fp64
#   (d) Newton re-derivation of the MONO splice landmarks (contract: delta=0.05)
#   (e) dense rescan k step 0.01 (1201 pts) of the mandated range with an independent 50-digit
#       reference: pass/fail counts per evaluation form at the 1e-14 bar
#   (f) 120-term series at arbitrary (non-decade) y<=10 points vs independent reference
import math, sys
from fractions import Fraction
from decimal import Decimal, getcontext

OK = True
def check(name, cond, observed, tolerance):
    global OK
    print(f"VERIFY {name}: {'PASS' if cond else 'FAIL'} observed={observed} tol={tolerance}")
    if not cond: OK = False

# ---- (a) Bernoulli, independent route: B^- via recurrence, q_k = (-1)^k B^-_k/k!
N = 130
Bm = [Fraction(0)] * (N + 1)
Bm[0] = Fraction(1)
for m in range(1, N + 1):
    Bm[m] = Fraction(-sum(math.comb(m + 1, k) * Bm[k] for k in range(m)), m + 1)
q2 = [Fraction((-1) ** k) * Bm[k] / math.factorial(k) for k in range(N)]

p = [Fraction((-1) ** k, math.factorial(k + 1)) for k in range(N)]
q1 = [Fraction(0)] * N
q1[0] = Fraction(1)
for n in range(1, N):
    q1[n] = -sum(p[k] * q1[n - k] for k in range(1, n + 1))

check("C1_bernstein_independent_route", q1 == q2, "all 130 coeffs equal", "exact")
print("   q[:12]:", [str(x) for x in q1[:12]])

# ---- (b) reference self-convergence: 70-digit vs 50-digit Decimal on the deep grid
def x_ref_at(y, prec):
    getcontext().prec = prec
    s = Decimal(y).sqrt()
    return Decimal(y) / (Decimal(1) - (-s).exp())
worst = 0.0
for k in range(-160, -39):
    y = 10.0 ** (k / 10)
    r70 = x_ref_at(y, 70); r50 = x_ref_at(y, 50)
    worst = max(worst, float(abs((r70 - r50) / r70)))
check("C2_reference_self_convergence", worst < 1e-40, f"{worst:.2e}", "< 1e-40 (50-digit ref floor is ~1e-50/s; fp64 claims need only << 1e-16)")

# ---- (c) split form x = y + h, h = -y*exp(-s)/expm1(-s); vs direct expm1 form, fp64
def x_direct(y):
    return -y / math.expm1(-math.sqrt(y))
def x_split(y):
    s = math.sqrt(y)
    h = -y * math.exp(-s) / math.expm1(-s)
    return y + h
worst = 0.0; w_at = None
for k in range(-160, 81):
    y = 10.0 ** (k / 10)
    e = abs(x_direct(y) - x_split(y)) / abs(x_direct(y))
    if e > worst: worst, w_at = e, y
check("C3_split_form_identity_fp64", worst < 5e-16, f"{worst:.2e} at y={w_at}", "< 5e-16")

# ---- (d) Newton re-derivation of MONO splice landmarks
def h_rar(y):
    return y / (math.exp(math.sqrt(y)) - 1.0)
def hp_rar(y):
    s = math.sqrt(y); e = math.exp(s)
    return (e * (2.0 - s) - 2.0) / (2.0 * (e - 1.0) ** 2)
def hpp_rar(y):
    # exact second derivative: f' where f = hp_rar, N = e(2-s)-2, D = 2(e-1)^2
    s = math.sqrt(y); e = math.exp(s); d = e - 1.0
    N = e * (2.0 - s) - 2.0
    Np = e * (1.0 - s) / (2.0 * s)        # dN/dy
    D = 2.0 * d * d                       # D = 2 d^2
    Dp = 2.0 * d * e / s                  # dD/dy = 4 d (e/(2s)) = 2 d e / s
    return (Np * D - N * Dp) / D ** 2
def newton(f, fp, x0, iters=60):
    x = x0
    for _ in range(iters):
        x = x - f(x) / fp(x)
    return x
DELTA = 0.05
y_p_n = newton(hp_rar, hpp_rar, 2.5)
f_star = lambda y: hp_rar(y) - DELTA * h_rar(y_p_n) / (y + y_p_n)
fp_star = lambda y: hpp_rar(y) + DELTA * h_rar(y_p_n) / (y + y_p_n) ** 2
y_s_n = newton(f_star, fp_star, 2.0)
h_p_n = h_rar(y_p_n)
check("C4_mono_landmarks_newton",
      abs(y_s_n - 2.337412) < 1e-5 and abs(y_p_n - 2.53964) < 1e-4 and abs(h_p_n - 0.647610) < 1e-5,
      f"y*={y_s_n:.9f} yp={y_p_n:.9f} hp={h_p_n:.9f}", "|dev| < 1e-5 / 1e-4 / 1e-5")
print(f"   newton: y*={y_s_n:.12f} y_p={y_p_n:.12f} h_p={h_p_n:.12f}")

# ---- (e) dense rescan of the mandated range (k step 0.01 -> 1201 pts), 50-digit reference
BAR = 1e-14
fails = {"naive": 0, "expform": 0, "expm1": 0, "ser": 0}
deep_y = [10.0 ** (k / 100) for k in range(-1600, -399)]
for y in deep_y:
    s = math.sqrt(y)
    ref = float(x_ref_at(y, 50))
    f_naive = y / (1.0 - math.exp(-s))
    e_ = math.exp(s)
    f_exp = y * e_ / (e_ - 1.0)
    f_m1 = -y / math.expm1(-s)
    acc = 0.0
    for k in range(29, -1, -1):
        acc = acc * s + float(q1[k])
    f_ser = acc * s
    for name, v in (("naive", f_naive), ("expform", f_exp), ("expm1", f_m1), ("ser", f_ser)):
        if abs(v - ref) / abs(ref) > BAR: fails[name] += 1
check("C5_dense_rescan_counts",
      fails["naive"] > 900 and fails["expform"] > 900 and fails["expm1"] == 0 and fails["ser"] == 0,
      f"naive={fails['naive']} expform={fails['expform']} expm1={fails['expm1']} ser={fails['ser']} (of 1201)",
      "naive/expform > 900 failures, expm1/ser 0")

# ---- (f) 120-term series at arbitrary (non-decade) y<=10 points vs independent reference
worst = 0.0
for y in [0.00123, 0.0123456, 0.137, 0.777, 1.2345, 2.71828, 4.7, 9.99]:
    s = math.sqrt(y)
    ref = float(x_ref_at(y, 50))
    acc = 0.0
    for k in range(119, -1, -1):
        acc = acc * s + float(q1[k])
    worst = max(worst, abs(acc * s - ref) / ref)
check("C6_series_arbitrary_points", worst < 3e-16, f"{worst:.2e}", "< 3e-16")

print("VERIFY_OK" if OK else "VERIFY_FAIL")
sys.exit(0 if OK else 1)
