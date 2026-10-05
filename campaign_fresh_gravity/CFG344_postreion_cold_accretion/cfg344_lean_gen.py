#!/usr/bin/env python3
"""CFG344: emit CFG344_certificate.lean from the results JSONs (rationals rounded OUTWARD at 1e-6).
Run from the repository root after both runs: python3 campaign_fresh_gravity/CFG344_postreion_cold_accretion/cfg344_lean_gen.py"""
import os, json, math
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "cfg344_accretion_results.json")))
U = json.load(open(os.path.join(HERE, "cfg344_accretion_MUTATE_results.json")))
dn = lambda x: F(math.floor(x * 1e6), 10 ** 6)
up = lambda x: F(math.ceil(x * 1e6), 10 ** 6)
q = lambda f: f"({f.numerator} / {f.denominator} : ℚ)"
L = ["import Mathlib", "", "/-! CFG344 certificate: decisive offset inequalities (rule S, per-object R_acc, primary z_f = 8, z_inf = 2).",
     "Values from cfg344_accretion_results.json / _MUTATE_results.json, rounded outward to 1e-6. Interval reasoning only. -/", "",
     "theorem abs_le_of_bounds {s lo hi T : ℚ} (h1 : lo ≤ s) (h2 : s ≤ hi) (h3 : -T ≤ lo) (h4 : hi ≤ T) : |s| ≤ T :=",
     "  abs_le.mpr ⟨le_trans h3 h1, le_trans h2 h4⟩", ""]
n = 0
for tag, R in (("main", M), ("mutate", U)):
    key = next(iter(R["RUNS"])); rows = R["RUNS"][key]["rows"]
    for p in ("nfw", "sis"):
        for f in ("canonical", "alt"):
            s = rows[p]["P1"][f][0]; T = 2 * R["ELAW"][p][f]; n += 1
            nm = f"{tag}_{p}_{f}"
            if abs(s) <= T:
                L += [f"/-- {key} {p} {f}: |s_UFD| = |{s:+.6f}| ≤ 2 e_law = {T:.6f} -/",
                      f"theorem ufd_within_{nm} (s : ℚ) (h1 : {q(dn(s))} ≤ s) (h2 : s ≤ {q(up(s))}) : |s| ≤ {q(dn(T))} :=",
                      f"  abs_le_of_bounds h1 h2 (by norm_num) (by norm_num)", ""]
            else:
                L += [f"/-- {key} {p} {f}: s_UFD = {s:+.6f} > 2 e_law = {T:.6f} -/",
                      f"theorem ufd_outside_{nm} (s : ℚ) (h1 : {q(dn(s))} ≤ s) : {q(up(T))} < s :=",
                      f"  lt_of_lt_of_le (by norm_num) h1", ""]
            if tag == "main":
                for r in ("P2a", "P2b", "P2c", "P2d"):
                    z = rows[p][r][f][1]; n += 1
                    L += [f"theorem other_{r}_{nm} (z : ℚ) (h1 : {q(dn(z))} ≤ z) (h2 : z ≤ {q(up(z))}) : |z| < 2 :=",
                          f"  abs_lt.mpr ⟨by linarith [show (-2 : ℚ) < {q(dn(z))} by norm_num], by linarith [show {q(up(z))} < (2 : ℚ) by norm_num]⟩", ""]
open(os.path.join(HERE, "CFG344_certificate.lean"), "w").write("\n".join(L) + "\n")
print(f"wrote CFG344_certificate.lean with {n} decisive theorems")
