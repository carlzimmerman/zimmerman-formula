#!/usr/bin/env python3
"""Writes CFG336_certificate.lean from cfg336_formation_epoch_results.json (main run).  Arithmetic certificates, not statistics:
 (1) per ultra-faint x footing: phantom inside (4/3) r_half > whole native cold share (1-f_b) M_c (integer Msun bounds rounded outward);
 (2) the bookkeeping lemma: max(ph, c) = ph when c <= ph, so reading M adds nothing for ANY profile;
 (3) per population x footing, readings S|P1 and M|P1: the decisive |m| vs 2e inequality (rational bounds rounded outward, 1e-4);
 (4) PARTIAL fails: UFD m > base/2 on both footings."""
import os, json, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "cfg336_formation_epoch_results.json")))
S = 10000
dn = lambda x: F(math.floor(x * S), S); up = lambda x: F(math.ceil(x * S), S)
q = lambda f: f"({f.numerator}/{f.denominator} : ℚ)" if f.denominator != 1 else f"({f.numerator} : ℚ)"
L = ["import Mathlib", "", "/-! CFG336: formation-epoch density of the native cold mass. Bounds rounded outward from cfg336_formation_epoch_results.json. -/", "",
     "theorem cfg336_max_inert (ph c : ℚ) (h : c ≤ ph) : max ph c = ph := max_eq_left h", ""]
n, bad = 1, []
for foot, rows in R["per_object"].items():
    for i, r in enumerate(rows):
        pl, cu = math.floor(r["ph_r"]), math.ceil(r["cold_tot"])
        if not pl > cu: bad.append((foot, i))
        L += [f"-- {r['name']} ({foot})", f"theorem cfg336_ufd{i:02d}_{foot}_bound (ph c : ℚ) (h1 : ({pl} : ℚ) ≤ ph) (h2 : c ≤ ({cu} : ℚ)) :",
              "    c < ph ∧ max ph c = ph := by", "  have h : c < ph := by linarith", "  exact ⟨h, max_eq_left h.le⟩", ""]
        n += 1
for rd in ("S|P1", "M|P1"):
    res = R["main"][rd]
    for key, v in res.items():
        pop, foot = key.split("|"); m, e = v["med"], v["tot"]
        ml, mh, el, eh = dn(m), up(m), dn(e), up(e)
        nm = f"cfg336_{rd.replace('|', '_')}_{pop}_{foot}"
        if abs(m) < 2 * e:
            if not (mh < 2 * el and ml > -2 * el): bad.append(nm)
            L += [f"theorem {nm}_pass (m e : ℚ) (h1 : {q(ml)} ≤ m) (h2 : m ≤ {q(mh)}) (h3 : {q(el)} ≤ e) :", "    -(2 * e) < m ∧ m < 2 * e := by", "  constructor <;> linarith", ""]
        elif m > 0:
            if not ml >= 2 * eh: bad.append(nm)
            L += [f"theorem {nm}_fail (m e : ℚ) (h1 : {q(ml)} ≤ m) (h2 : e ≤ {q(eh)}) :", "    2 * e ≤ m := by", "  linarith", ""]
        else:
            if not mh <= -2 * eh: bad.append(nm)
            L += [f"theorem {nm}_fail (m e : ℚ) (h1 : m ≤ {q(mh)}) (h2 : e ≤ {q(eh)}) :", "    m ≤ -(2 * e) := by", "  linarith", ""]
        n += 1
    for foot in ("canonical", "alt"):
        m = R["main"][rd][f"UFD|{foot}"]["med"]; b = R["law"][f"UFD|{foot}"]["med"]
        ml, bh = dn(m), up(b)
        if not ml * 2 > bh: bad.append(("partial", rd, foot))
        L += [f"theorem cfg336_{rd.replace('|', '_')}_not_partial_{foot} (m b : ℚ) (h1 : {q(ml)} ≤ m) (h2 : b ≤ {q(bh)}) :", "    b / 2 < m := by", "  linarith", ""]
        n += 1
open(os.path.join(HERE, "CFG336_certificate.lean"), "w").write("\n".join(L))
print(f"{n} theorems written; rounding-ambiguous cells: {bad if bad else 'none'}")
