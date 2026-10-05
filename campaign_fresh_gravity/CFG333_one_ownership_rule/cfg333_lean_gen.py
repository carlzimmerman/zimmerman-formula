#!/usr/bin/env python3
"""Writes CFG333_certificate.lean from cfg333_one_rule_results.json: one theorem per rule x population x footing,
certifying the decisive |m| vs 2e inequality from rational bounds rounded outward (1e-4). Arithmetic, not statistics."""
import os, json, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg333_one_rule_results.json")))
S = 10000
dn = lambda x: F(math.floor(x * S), S); up = lambda x: F(math.ceil(x * S), S)
q = lambda f: f"({f.numerator}/{f.denominator} : ℚ)" if f.denominator != 1 else f"({f.numerator} : ℚ)"
L = ["import Mathlib", "", "/-! CFG333: decisive pass/fail inequalities, rational bounds rounded outward from cfg333_one_rule_results.json.",
     "  m = offset (dex) | gamma_hat - gamma_pred | joint-Ups distance to [1.3, 2.2]; e = its 1-sigma error. Pass = |m| < 2e. -/", ""]
n = 0; bad = []
for rule, rr in R["rules"].items():
    for key, v in rr["res"].items():
        pop, foot = key.split("|"); m, e = v["m"], v["err"]
        ml, mh, el, eh = dn(m), up(m), dn(e), up(e)
        nm = f"cfg333_{rule}_{pop}_{foot}"
        if abs(m) < 2 * e:
            if not (mh < 2 * el and ml > -2 * el): bad.append(nm)
            L += [f"theorem {nm}_pass (m e : ℚ) (h1 : {q(ml)} ≤ m) (h2 : m ≤ {q(mh)}) (h3 : {q(el)} ≤ e) :",
                  "    -(2 * e) < m ∧ m < 2 * e := by", "  constructor <;> linarith", ""]
        elif m > 0:
            if not ml >= 2 * eh: bad.append(nm)
            L += [f"theorem {nm}_fail (m e : ℚ) (h1 : {q(ml)} ≤ m) (h2 : e ≤ {q(eh)}) :", "    2 * e ≤ m := by", "  linarith", ""]
        else:
            if not mh <= -2 * eh: bad.append(nm)
            L += [f"theorem {nm}_fail (m e : ℚ) (h1 : m ≤ {q(mh)}) (h2 : e ≤ {q(eh)}) :", "    m ≤ -(2 * e) := by", "  linarith", ""]
        n += 1
open(os.path.join(HERE, "CFG333_certificate.lean"), "w").write("\n".join(L))
print(f"{n} theorems written; rounding-ambiguous cells: {bad if bad else 'none'}")
