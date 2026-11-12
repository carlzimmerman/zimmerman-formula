#!/usr/bin/env python3
"""LWB1 mutation grading (FROZEN_CRITERIA.md f4b3128cc1, section 4): reads lwb1.json and lwb1_MUTATE_MU{1,2,3}.json,
writes lwb1_mutate_grade.json / .out. kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, json
H = os.path.dirname(os.path.abspath(__file__)); L = lambda f: json.load(open(os.path.join(H, f)))
P0 = L("lwb1.json")["primary"]; M = {m: L(f"lwb1_MUTATE_{m}.json")["primary"] for m in ("MU1", "MU2", "MU3")}
out, res = [], {}
for ft in ("canonical", "alt"):
    b = lambda m, v: M[m][ft][v]["best_sigma8"] / P0[ft][v]["best_sigma8"]
    r1, r2, r3k = b("MU1", "J"), b("MU2", "J"), b("MU3", "KiDS"); d3 = abs(M["MU3"][ft]["DES"]["best_sigma8"] - P0[ft]["DES"]["best_sigma8"])
    res[ft] = dict(MU1_ratio=r1, MU1_bites=abs(r1 - 0.85) <= 0.02, MU2_ratio=r2, MU2_bites=abs(r2 - 1.3 ** -0.5) <= 0.02,
                   MU3_kids_ratio=r3k, MU3_des_shift=d3, MU3_bites=abs(r3k - 1.2) <= 0.03 and d3 <= 0.005)
    out.append(f"[{ft}] MU1 J ratio {r1:.4f} (0.85 +- 0.02) {'bites' if res[ft]['MU1_bites'] else 'DOES NOT BITE'}; MU2 J ratio {r2:.4f} (0.877 +- 0.02) "
               f"{'bites' if res[ft]['MU2_bites'] else 'DOES NOT BITE'}; MU3 KiDS ratio {r3k:.4f} (1.20 +- 0.03), DES shift {d3:.5f} {'bites' if res[ft]['MU3_bites'] else 'DOES NOT BITE'}")
print("\n".join(out)); json.dump(res, open(os.path.join(H, "lwb1_mutate_grade.json"), "w"), indent=1, default=bool)
open(os.path.join(H, "lwb1_mutate_grade.out"), "w").write("\n".join(out) + "\n")
