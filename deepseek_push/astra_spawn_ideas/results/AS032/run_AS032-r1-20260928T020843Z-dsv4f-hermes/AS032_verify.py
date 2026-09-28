#!/usr/bin/env python3
"""
AS032 verify -- independent re-derivation in floating double precision with
DIFFERENT representations than the main 50-digit mpmath run:

  1. peak root: fixed-point iteration  t_{n+1} = 2 - 2/exp(t_n)  (derived from
     e^t (2-t) = 2  <=>  t = 2 - 2 e^{-t}), starting inside (1,2); independent of
     the mpmath bisection+Newton used in AS032_compute.py.
  2. h_p: direct y-space evaluation h = y/expm1(sqrt(y)) at y = t^2 (expm1 form
     avoids cancellation; main run used t-space t^2/(e^t-1)).
  3. h'(y_p): central finite difference in y-space at two steps (main run used
     the exact analytic derivative F(t)/(2(e^t-1)^2)).
  4. h''(y_p): second central difference of h(y) in y-space (main run: exact
     closed form + FD of h').
  5. Contract landmarks and peak-equation residual checks vs raw_output.json.
  6. Finite-box sup check: h_RAR(y) <= h_p on the grid y = 10^k, k in [-10,8]
     step 0.1 (181 points) -- exact on the grid, brackets the peak.
Runs in < 1 s, single thread, no external deps.
"""
import json, math, os

RAW = "raw_output.json"
with open(RAW) as f:
    raw = json.load(f)

fail = []
def check(name, cond, tol, got, want):
    ok = bool(cond)
    print(f"{'PASS' if ok else 'FAIL'} {name}: got={got} want={want} tol={tol}")
    if not ok:
        fail.append(name)

def h_y(y):            # h/a0 in y-space, expm1-stable (tail: asymptotic y*e^{-t})
    if y == 0.0:                       # boundary limit h(0+) = 0
        return 0.0
    t = math.sqrt(y)
    if t > 700.0:
        return y * math.exp(-t)
    return y / math.expm1(t)

def hp_y_num(y, d):    # numeric derivative via FIVE-point stencil
    return (-h_y(y + 2*d) + 8*h_y(y + d) - 8*h_y(y - d) + h_y(y - 2*d)) / (12*d)

# 1) root by fixed point t = 2 - 2/e^t (contraction on (1,2): |phi'| = 2 e^-t < 1)
t = 1.6
for _ in range(200):
    t = 2.0 - 2.0 / math.exp(t)
t_p = t
y_p = t_p * t_p
res_peak_eq = (2 - t_p) * math.exp(t_p) - 2.0      # residual of e^t(2-t) = 2
check("fixed-point converges to peak equation residual < 1e-13", abs(res_peak_eq) < 1e-13,
      1e-13, res_peak_eq, 0.0)

# 2) h_p via expm1 in y-space; compare with landmark law t*(2-t) and with raw
h_p_y = h_y(y_p)
h_p_landmark = t_p * (2 - t_p)
check("h_p direct (expm1) == landmark law t(2-t)", abs(h_p_y - h_p_landmark) < 1e-14,
      1e-14, h_p_y, h_p_landmark)
raw_hp = float(raw["peak"]["h_p_exact_t(2-t)"])
check("h_p matches 50-digit raw (0.6476102378919149)", abs(h_p_y - raw_hp) < 1e-13,
      1e-13, h_p_y, raw_hp)
raw_yp = float(raw["peak"]["y_p"])
check("y_p matches 50-digit raw (2.5396382821881653)", abs(y_p - raw_yp) < 1e-12,
      1e-12, y_p, raw_yp)

# 3) h'(y_p) ~ 0 by five-point numeric differentiation (y-space)
d1, d2 = 1e-4, 1e-5
hp1 = hp_y_num(y_p, d1)
hp2 = hp_y_num(y_p, d2)
check("numeric h'(y_p) < 1e-9 (both steps)", abs(hp1) < 1e-9 and abs(hp2) < 1e-9,
      1e-9, (hp1, hp2), 0.0)

# 4) h''(y_p) via second central difference of h(y); compare with closed form.
# NOTE: fp64 cancellation floor for this stencil is ~ h(y_p)*eps/(|h''|*d^2) ~ 2e-5
# relative; exact agreement to 1e-25 is established by the 50-digit mpmath FD rows
# in raw_output.json (three steps). Tolerance here = 2x the fp64 floor.
hpp_num = (h_y(y_p + d2) - 2*h_y(y_p) + h_y(y_p - d2)) / d2**2
hpp_exact = (1 - t_p) * (2 - t_p) / (2 * t_p**3)
check("numeric h''(y_p) == closed form (1-t)(2-t)/(2t^3) within fp64 floor",
      abs(hpp_num - hpp_exact) / abs(hpp_exact) < 5e-5, 5e-5, hpp_num, hpp_exact)
raw_hpp = float(raw["peak"]["h''_y(y_p)_exact_(1-t)(2-t)/(2t^3)"])
check("h'' matches 50-digit raw (-0.029802426216689)", abs(hpp_exact - raw_hpp) < 1e-12,
      1e-12, hpp_exact, raw_hpp)

# 5) grid sup check: h_RAR <= h_p + slack at every grid point
ks = [-10.0 + 0.1*i for i in range(181)]
sup, sup_y = 0.0, None
for k in ks:
    y = 10.0 ** k
    v = h_y(y)
    if v > sup:
        sup, sup_y = v, y
check("grid sup h_RAR <= h_p (181 pts, y=10^k k=-10..8)", sup <= h_p_y + 1e-9,
      1e-9, sup, h_p_y)
print("    grid sup =", sup, "at y =", sup_y, " (h_p =", h_p_y, ")")

# 6) t=0 boundary solution is NOT an extremum: h'(y) -> +inf as y -> 0+
hpsmall = (h_y(1e-12) - h_y(0.0)) / 1e-12
check("h'(y)->+inf at y->0+ (positive, not a critical point)",
      hpsmall > 1e5, 1e5, hpsmall, "+inf")

# 7) Q cap numeric: max over grid of h_Q < 1/2 with margin; MU2 max at x=2
# USE THE CERTIFIED STABLE FORM 1/(1+sqrt(1+1/y)) (Lean: q_identity); the naive
# form y*(sqrt(1+1/y)-1) cancels catastrophically at y = 1e8 in fp64 (0.5000000006
# instead of 0.499975) -- the identity certificate is what makes this check valid.
def hQ(y):
    return 1.0 / (1.0 + math.sqrt(1.0 + 1.0 / y))
qsup = max(hQ(10.0**k) for k in ks)
check("sup h_Q on grid < 1/2 (strict cap, asymptotic)", qsup < 0.5, 0.5, qsup, 0.5)
def hMU2(x):
    return x / (1 + x/2)**2
m2 = max(hMU2(10.0**k) for k in ks)
check("sup h_MU2 on grid == 1/2 attained at x=2", abs(hMU2(2.0) - 0.5) < 1e-15 and m2 <= 0.5 + 1e-9,
      1e-9, m2, 0.5)

# 8) RAR peak exceeds the Q/MU2 cap
check("h_p > 1/2 (RAR max exceeds Q/MU2 cap)", h_p_y > 0.5, 0.5, h_p_y, 0.5)

print()
print("SUMMARY:", "ALL PASS" if not fail else f"FAILED: {fail}")
if fail:
    raise SystemExit(1)
print("y_p =", y_p, " h_p =", h_p_y, " h''(y_p) =", hpp_exact)
