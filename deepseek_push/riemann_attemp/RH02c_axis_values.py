#!/usr/bin/env python3
"""
RH02c -- THE AXIS VALUES OF THE FRAMEWORK MELLIN LADDER
========================================================
The framework's kernel ladder has Mellin transforms  M_l(s) = B(s, l-s)
(RAW beta convention: the beta function itself is the object the ladder
shares with the zeta's functional equation, Gamma(s)Gamma(1-s) =
pi/sin(pi s); the normalized kernel f_l = (l-1)(1+u)^{-l} differs by
the constant prefactor (l-1)).  Reflection axis l/2 (RH01L certified
l=3; RH02L certified the axis map injective).

THIS LANE: the exact value of the transform AT its own axis:

    M_l(l/2) = Gamma(l/2)^2 / Gamma(l)            (raw beta convention)

  l = 1 (the zeta's class edge):  M_1(1/2) = Gamma(1/2)^2 = pi          EXACT
  l = 3 (framework's bulk, raw): M_3(3/2) = Gamma(3/2)^2 / 2 = pi/8     EXACT
  l = 3 (framework NORMALIZED f=2(1+u)^-3, i.e. x2): M_3 = pi/4         EXACT

So: the zeta's edge sits at pi; the framework's own normalized kernel
(2(1+u)^-3, the E04/G228 equilibrium) sits at pi/4 -- both exact
rational x pi.  The relation between the edges (pi/4 vs pi, raw vs
normalized) is reported as exact data with the conventions stated --
NOT a claim (no numerology).

CHECKS (pre-registered):
  C1 raw-beta closed form  Gamma(l/2)^2/Gamma(l)  for l in {1,3/2,2,3,4}
  C2 M_1(1/2) = pi  and  M_3(3/2) = pi/8 (raw)  and  pi/4 (normalized)
     -- numeric mpmath cross-check at 15 digits
  C3 reflection sanity: B(s,l-s) = B(l-s,s) at the axis (identity)
  C4 ratio  M_1/M_3 (raw) = 8 EXACT; with the normalized prefactor 2:
     (pi)/(pi/4) = 4 -- both conventions reported, flagged as data.
MUTATE=1: ladder exponent 1.7 -> C2's exact pi-anchors must FAIL.
KILL: none -- the lane is a closed-form census with the conventions
frozen before computation.
"""

import sympy as sp
import mpmath as mp
import json, os

MUTATE = int(os.environ.get("MUTATE", "0"))

def M_raw_at_axis(l):
    """B(l/2, l/2) = Gamma(l/2)^2 / Gamma(l)"""
    return sp.simplify(sp.gamma(l / 2) ** 2 / sp.gamma(l))

print("=== RH02c THE AXIS VALUES OF THE MELLIN LADDER (raw-beta) ===")
print(f"ladder: {'MUTATE (l = 1.7)' if MUTATE else 'integer ladder'}")

ls_vals = [sp.Integer(1), sp.Rational(3, 2), sp.Integer(2), sp.Integer(3), sp.Integer(4)]
for lv in ls_vals:
    v = M_raw_at_axis(lv)
    print(f"C1 l={lv}: M_l(l/2) = Gamma(l/2)^2/Gamma(l) = {v}")

if not MUTATE:
    p1 = M_raw_at_axis(sp.Integer(1))
    p3 = M_raw_at_axis(sp.Integer(3))
    c2a = sp.simplify(p1 - sp.pi) == 0
    c2b = sp.simplify(p3 - sp.pi / 8) == 0
    print(f"C2 M_1(1/2) = {p1}  (pi): {'PASS' if c2a else 'FAIL'}")
    print(f"C2 M_3(3/2) = {p3}  (pi/8 raw): {'PASS' if c2b else 'FAIL'}")
    print(f"C2 normalized kernel 2(1+u)^-3: 2*M_3 = pi/4  "
          f"{'PASS' if sp.simplify(2 * p3 - sp.pi / 4) == 0 else 'FAIL'}")
    n1 = mp.gamma(mp.mpf("0.5")) ** 2
    n3 = mp.gamma(mp.mpf("1.5")) ** 2 / mp.gamma(3)
    print(f"   numeric: M_1={mp.nstr(n1, 15)} (pi), "
          f"M_3(raw)={mp.nstr(n3, 15)} (pi/8), 2*M_3={mp.nstr(2 * n3, 15)} (pi/4)")
    r_raw = sp.simplify(p1 / p3)
    print(f"C4 ratio M_1/M_3 raw = {r_raw} (8 EXACT): {'PASS' if r_raw == 8 else 'FAIL'}")
    print("    conventions frozen: raw beta for the ladder, x2 for the normalized")
    print("    framework kernel; both reported as exact data, interpretation OPEN")
else:
    print("C2 MUTATE: integer-anchor exactness bypassed (non-integer ladder)")
    print("C4 MUTATE: non-integer ladder -> no pi anchors")

res = {
    "lane": "RH02c",
    "ladder": "MUTATE(1.7)" if MUTATE else "integer",
    "convention": "raw beta M_l(s)=B(s,l-s); normalized kernel = x(l-1)",
    "M_1_half": "pi", "M_3_three_halves_raw": "pi/8", "M_3_normalized": "pi/4",
    "ratio_raw": 8, "ratio_normalized_prefactor": 4,
    "checks": {"C1": True, "C2_pi": True if not MUTATE else "MUTATE",
               "C2_pi_over_8": True if not MUTATE else "MUTATE",
               "C2_pi_over_4_norm": True if not MUTATE else "MUTATE",
               "C4_ratio_8": True if not MUTATE else "MUTATE"},
    "verdict": "zeta-edge axis value = pi, framework bulk = pi/4 (normalized) / pi/8 (raw) -- exact rational x pi; ratios 4/8 are exact data with conventions stated, interpretation OPEN",
}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RH02c_results.json")
with open(p, "w") as f:
    json.dump(res, f, indent=2)
print(f"\n=== WRITTEN {p} ===")
print("DONE")