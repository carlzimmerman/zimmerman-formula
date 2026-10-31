#!/usr/bin/env python3
"""RF3 POST-RESULT, reported only, not graded: caustic rows by source, WL by redshift, G-OUT-M3 against gas scale, the h convention in XF. Reads runs/ and rf3_inputs.json. kappa = 1/2 FITTED; not theory closed."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); I = json.load(open(os.path.join(HERE, "rf3_inputs.json"))); L = lambda t: json.load(open(os.path.join(HERE, "runs", f"{t}.json"))); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def stat(rows, V):
    C = {}
    for r in rows: v = V[str(r["i"])]; C.setdefault(r["erass"], []).append(math.log10(r["M"] / (v[0] + v[1])))
    D = np.array([np.median(q) for q in C.values()]); return len(D), float(np.median(D)), float(np.std(D, ddof=1) / math.sqrt(len(D))) if len(D) > 2 else float("nan")
M = I["match_rows"]; P("RF3 post-result, not graded; kappa = 1/2 FITTED; not theory closed")
for rule, g in (("ZN3", "X"), ("ZN3", "XF"), ("ZN3", "E"), ("C4", "E"), ("NAT", "E")):
    V = L(f"{rule}_{g}_0.034")["rf"]["match"]["canonical"]
    for lab, q in (("CM HeCS", [r for r in M if r["method"] == "CM" and r["src"] == "HeCS"]), ("CM Rines & Diaferio 06, h 0.7", [r for r in M if r["method"] == "CM" and r["src"] == "G16" and "Rines" in r["ref"] and r["h_used"] == 0.7]), ("CM Rines & Diaferio 06, h 1", [r for r in M if r["method"] == "CM" and r["src"] == "G16" and "Rines" in r["ref"] and r["h_used"] == 1.0]), ("WL z < 0.3", [r for r in M if r["method"] == "WL" and r["z"] < 0.3]), ("WL z >= 0.3", [r for r in M if r["method"] == "WL" and r["z"] >= 0.3])):
        n, m, s = stat(q, V); P(f"  {rule} gas {g} f* 0.034 {lab}: clusters {n}, median {m:+.3f}, SE {s:.3f}")
fx = lambda t: (lambda R: (lambda c, m: (m["terc"][2] - c["G-OUT-M3"]["pred"]) / (c["G-OUT-M3"]["s"] * m["terc"][2] / c["G-OUT-M3"]["meas"]))(R["grader"]["canonical"]["clusters"]["cells"]["h0672"], R["M_outer"]["canonical|h0672"]))(L(t))
xf = I["XF"]["median_dex"]; a, b, e = fx("ZN3_X_0.034"), fx("ZN3_XF_0.034"), fx("ZN3_E_0.034"); sl = (a - b) / (0.111 - xf); d2 = xf + (2.0 - b) / sl; rms = float(np.std([r["dex_at_eRASS_R500"] for r in I["XF"]["rows"]], ddof=1))
P(f"  G-OUT-M3 h 0.672, ZN3 f* 0.034: E {e:+.2f}, XF ({xf:+.3f}) {b:+.2f}, X (+0.111) {a:+.2f}; slope {sl:.1f} per dex; Z = 2 at {d2:+.3f} dex. XF rows rms {rms:.3f}, SE {rms / math.sqrt(5):.3f}")
h = 0.6774; dm = 2.5 * math.log10(h / 0.7); P(f"  h convention, neither SM1 nor XF converts eRASS1 (assumed h {h}, from memory, PROVISIONAL) to X-COP's 0.7: Mgas500 x h^-2.5 alone shifts the scale by {-dm:+.3f} dex; R500 x 1/h shifts the radius by {math.log10(h / 0.7):+.3f} dex")
open(os.path.join(HERE, "rf3_post.out"), "w").write("\n".join(OUT) + "\n")
