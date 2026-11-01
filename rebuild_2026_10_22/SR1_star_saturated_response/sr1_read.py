#!/usr/bin/env python3
"""SR1 read, FROZEN_CRITERIA.md. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "sr1_results.json"))); A, B = "A_c2b_refit", "B_cfg886_bg"; OUT = []; U2 = json.load(open(os.path.join(H, "..", "UR2_response_mass_pinch", "ur2_results.json")))["rows"]["blum|+0.00"]
def P(s): print(s); OUT.append(s)
def row(l, r):
    s = r["sparc"]; g = r["groups"]; bb = s[A]["bins"]; c = bb["150-200"] >= .5 and bb["200-250"] >= .5 and s[A]["lowU"] >= .5; G = [n for n, ok in (("line", s[A]["line"] and s[B]["line"]), ("tilt", abs(s[A]["tilt"]) <= .15), ("groups", g["verdict"] == "CONSISTENT"), ("LT", abs(r["lt"][A]) <= .1)) if not ok]
    P(f"{l:10s} U {s[A]['U']:.2f}/{s[B]['U']:.2f} rms {s[A]['rms']:.4f} tilt {s[A]['tilt']:+.2f}/{s[B]['tilt']:+.2f} lowU {s[A]['lowU']:.2f} bins {[round(v, 2) for v in bb.values()]} groups {g['Z']:+.2f} {g['verdict']} LT {r['lt'][A]:+.3f} | " + ("CLAIM FAILS" if not c else "CLEARS" if not G else "CLAIM HOLDS, GATES FAIL") + f" {G}")
    if r.get("eff") and r["m"]: P("   f, chi at 2.2 R_d: " + " ".join(f"{k} {v[0]:.2f},{v[1]:.1f}" for k, v in r["eff"].items()))
row("K1", R["rows"]["K1"])
for k in ("sat|+0.00", "sat|+0.10", "lit|+0.00", "lit|+0.10"): row(k, R["rows"][k])
row("MUT M*x.1", R["MUT"]); k = R["rows"]["K1"]; P(f"K1 vs UR2 |d| {max(abs(U2['sparc'][t][q] - k['sparc'][t][q]) for t in (A, B) for q in ('U', 'rms', 'tilt')):.1e}")
open(os.path.join(H, "sr1.out"), "w").write("\n".join(OUT) + "\n")
