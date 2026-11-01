#!/usr/bin/env python3
"""GT1 read, FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "gt1_results.json"))); U2 = json.load(open(os.path.join(H, "..", "UR2_response_mass_pinch", "ur2_results.json")))["rows"]; A, B = "A_c2b_refit", "B_cfg886_bg"; OUT = []
def P(s): print(s); OUT.append(s)
def row(l, r):
    s = r["sparc"]; g = r["groups"]; P(f"{l:12s} U {s[A]['U']:.2f}/{s[B]['U']:.2f} rms {s[A]['rms']:.4f} line {s[A]['line']}/{s[B]['line']} tilt {s[A]['tilt']:+.2f}/{s[B]['tilt']:+.2f} lowU {s[A]['lowU']:.2f} bins {[round(v, 2) for v in s[A]['bins'].values()]} groups {g['Z']:+.2f} {g['verdict']} LT {r['lt'][A]:+.3f}/{r['lt'][B]:+.3f}")
    if "keys" in r: z = r["keys"]["Z"]["h0672"]; P(f"   keys {r['keys']['n']}/15 bad {r['keys']['bad']} G-IN-Mall {z['G-IN-Mall']:+.2f} G-OUT-M3 {z['G-OUT-M3']:+.2f}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f} {r['xcop']['PASS']}")
row("K1 blum", R["rows"]["K1"])
for m in ("h10", "j7", "j7b"):
    for d in ("+0.00", "+0.10"): row(f"{m} {d}", R["rows"][f"{m}|{d}"])
row("MUT h10 a0x10", R["MUT_h10"]); row("MUT j7b jx.1", R["MUT_j7b"]); o = U2["off|+0.10"]; P(f"#5 = off at +0.10: U {o['sparc'][A]['U']:.2f}, tilt {o['sparc'][A]['tilt']:+.2f}, LT {o['lt'][A]:+.3f}, bins {[round(v, 2) for v in o['sparc'][A]['bins'].values()]}")
b = U2["blum|+0.00"]; k = R["rows"]["K1"]; P(f"K1 vs UR2 |d| {max(abs(b['sparc'][t][q] - k['sparc'][t][q]) for t in (A, B) for q in ('U', 'rms', 'tilt')):.1e}; K2 chi_pol range {R['K2']}; K3 {R['K3']:.2e}")
for m in ("h10", "j7", "j7b"):
    r = R["rows"][f"{m}|+0.10"]; s = r["sparc"]; bb = s[A]["bins"]; c = bb["150-200"] >= .5 and bb["200-250"] >= .5 and s[A]["lowU"] >= .5; gates = [n for n, ok in (("line", s[A]["line"] and s[B]["line"]), ("tilt", abs(s[A]["tilt"]) <= .15), ("groups", r["groups"]["verdict"] == "CONSISTENT"), ("LT", abs(r["lt"][A]) <= .1)) if not ok]; P(f"{m}: " + ("CLAIM FAILS" if not c else "CLAIM HOLDS, SPARC SIDE CLEARS" if not gates else f"CLAIM HOLDS, GATES FAIL") + f" failing {gates}")
open(os.path.join(H, "gt1.out"), "w").write("\n".join(OUT) + "\n")
