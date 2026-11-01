#!/usr/bin/env python3
"""DR7 reader (FROZEN_CRITERIA.md). Exit 1 if a check fails, and then no verdict. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = ("A_c2b_refit", "B_cfg886_bg"); OUT = []
def P(s): print(s); OUT.append(s)
L = lambda p: json.load(open(os.path.join(H, f"dr7_{p}_results.json")))["rows"]
M, LO, HI, MU = L("MEDIAN"), L("LOW"), L("HIGH"), L("MUTATE"); N = json.load(open(os.path.join(H, "..", "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]["EM1|blum"]; C = json.load(open(os.path.join(H, "dr7_checks.json")))
def row(k, r):
    s = r["sparc"]; x = f"{k}: U {s[T[0]]['U']:.3f}/{s[T[1]]['U']:.3f} rms {s[T[0]]['rms']:.4f}/{s[T[1]]['rms']:.4f} tilt {s[T[0]]['tilt']:+.2f}/{s[T[1]]['tilt']:+.2f} bins {[round(v, 2) for v in s[T[0]]['bins'].values()]} groups {r['groups']['Z']:+.2f} {r['groups']['verdict']} LT {r['lt'][T[0]]:+.3f}/{r['lt'][T[1]]:+.3f}"
    if "keys" in r: x += f"; keys {r['keys']['n']} {r['keys']['bad']} G-IN-Mall {r['keys']['Z']['h0672']['G-IN-Mall']:+.2f}; alt bad {r['keys_alt']}; X-COP {r['xcop']['mean']:+.3f}, {r['xcop']['rms']:.3f}"
    if "cap" in r: c = r["cap"]; x += f"\n   cap: calls {c['n']}, bound {c['bound']}; M/M_c at r_h median {c['Mrh_med']:.4f}, min {c['Mrh_min']:.4f}; response f at r_h median {c['frh_med']:.3f}; last capped radius / r_h median {c['rx_med']:.3f}, p90 {c['rx_p90']:.3f}; conv {c['conv']:.1e}; M/M_c max {c['over']:.6f}; min dM {c['mono']:.2e}; edge {c['edge']:.1e}"
    return x
for k, r in M.items():
    if not k.startswith("resp"): P(row("MEDIAN " + k, r))
for n, R in (("LOW", LO), ("HIGH", HI), ("MUTATE", MU)):
    for k, r in R.items(): P(row(f"{n} {k}", r))
for k in ("resp|off", "resp|cap"):
    q = M[k]; P(f"{k} M_f/M_0 at r0: " + ", ".join(f"{b} {v['Q']:.2f}" for b, v in q["gal"].items()) + "; clusters gas + stars: " + ", ".join(f"{b} {v['gas_stars_only']:.2f}" for b, v in q["clusters"].items()) + "; with BCG: " + ", ".join(f"{b} {v['with_BCG']:.2f}" for b, v in q["clusters"].items()))
o, c = M["EM1|blum|off"], M["EM1|blum|cap"]; HK = list(o["keys"]["preds"]); KY = list(o["keys"]["preds"][HK[0]])
k1 = max([abs(o["sparc"][t][q] - N["sparc"][t][q]) for t in T for q in ("U", "rms")] + [abs(o["keys"]["preds"][h][k] - N["keys"]["preds"][h][k]) for h in HK for k in KY]); k = c["cap"]
K = dict(K1=k1 <= 1e-6, K2=C["K2"]["PASS"], K3=C["K3"]["PASS"], K4=C["K4"]["PASS"], K5=k["over"] <= 1 + 1e-9 and k["mono"] >= -2e34 and k["edge"] <= 1e-6 and k["conv"] <= 1e-3, MUTATE=max(abs(MU["EM1|blum|cap_mut"]["sparc"][t]["U"] - c["sparc"][t]["U"]) for t in T) >= 0.02)
P(f"checks K1 |d| {k1:.1e}; K2 {C['K2']['capped_over_Q0']:.3f} (uncapped {C['K2']['uncapped_over_Q0']:.0f}); K3 {C['K3']['dev']:.1e}; K4 {C['K4']['move']:.1e}; {K}")
def lab(r, full):
    s = r["sparc"]; mv = max(abs(s[t]["U"] - o["sparc"][t]["U"]) for t in T); g = dict(line=all(s[t]["rms"] <= 0.11 and 0.5 <= s[t]["U"] <= 0.8 for t in T), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in T), groups=r["groups"]["verdict"] == "CONSISTENT", lt=all(abs(r["lt"][t]) <= 0.10 for t in T)); bad = [a for a, b in g.items() if not b]
    return ("CLEARS SPARC SIDE" if not bad else "BITES, FAILS" if mv >= 0.02 else "CAP INERT"), bad, mv, g["line"]
a = lab(c, 1); bm = lab(LO["EM1|blum|cap"], 0); bh = lab(HI["EM1|blum|cap"], 0); nl = any(x[0] != a[0] or x[3] != a[3] for x in (bm, bh))
P(f"LOW {bm}; HIGH {bh}"); ok = all(K.values()); V = "NOT DECIDED" if not ok else a[0] + (" [NOISE-LIMITED]" if nl else ""); P(f"VERDICT: {V}; failing {a[1]}; Upsilon move from baseline {a[2]:.3f}")
open(os.path.join(H, "dr7.out"), "w").write("\n".join(OUT) + "\n"); json.dump(dict(verdict=V, failing=a[1], move=a[2], checks=K, k1=k1), open(os.path.join(H, "dr7_results.json"), "w"), indent=1); sys.exit(0 if ok else 1)
