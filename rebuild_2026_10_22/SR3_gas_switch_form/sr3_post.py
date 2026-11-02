#!/usr/bin/env python3
"""SR3 post-result reads, no label: nearest real rows to G2, label control's held-out clusters, BF1's best on the free path, plant error by rms, constants near simple numbers. kappa = 1/2 FITTED; not theory closed."""
import json, os, re, sys
sys.dont_write_bytecode = True; os.nice(19)
import numpy as np
import sr3_core as K
J = json.load(open(os.path.join(K.HERE, "sr3_grade.json")))["fronts"]; L = []
def say(s): print(s); L.append(s)
short = lambda q: f"c{q['c']} k{q['nfit']} {q['label']} X {q['xt']['mean']:+.3f},{q['xt']['rms']:.3f} Xh {q['xh']['mean']:+.3f},{q['xh']['rms']:.3f} S {q['tr']['rms']:.4f}/{q['law_tr']:.4f} U {q['tr']['U']:.2f} t {q['tr']['tilt']:+.2f} Sh {q['ho']['rms']:.4f}/{q['law_ho']:.4f} U {q['ho']['U']:.2f} t {q['ho']['tilt']:+.2f} LT {q['lt']['E']:+.3f} YL {q['limits']['Y_LIMIT']} FX {q['limits']['F_EXACT']} {q['eq'][:80]}"
for t, R in J.items():
    G = [q for q in R if q["G1"] and 0.5 <= q["tr"]["U"] <= 0.8 and abs(q["tr"]["tilt"]) <= .15]; say(f"\n{t}: G1 rows {sum(q['G1'] for q in R)} of {len(R)}; with U and tilt inside {len(G)}; Y_LIMIT rows {sum(q['limits']['Y_LIMIT'] for q in R)}; G1 + Y_LIMIT {sum(q['G1'] and q['limits']['Y_LIMIT'] for q in R)}; G1 + F_EXACT {sum(q['G1'] and q['limits']['F_EXACT'] for q in R)}")
    for q in sorted(G, key=lambda q: q["tr"]["rms"])[:2]: say("  " + short(q))
    b = min((q for q in R if q["limits"]["Y_LIMIT"] and q["limits"]["F_EXACT"]), key=lambda q: q["loss"], default=None)
    if b and b["c"] > 1: say("  lowest-loss with both limits: " + short(b))
P = K.prep("real", "canonical"); a = P["a0"]; tr = [g for g in P["gals"] if K.is_train(g)]; ho = [g for g in P["gals"] if K.is_hold(g)]; Hb = K.compile_form("(((f+2.0)/(1/(1+f)))**2)*(1/(1+((f+pi)+(f/y))))")
for n, s in (("train", tr), ("held", ho)): r = K.free_path(s, Hb, a); say(f"BF1 best, free path, {n}: rms {r['rms']:.4f} U {r['U']:.2f} tilt {r['tilt']:+.2f} (law {K.free_path(s, None, a)['rms']:.4f})")
say(f"BF1 best LT {K.lt_stat(Hb, a)['E']:+.3f}")
T = K.search_table(K.prep("planted", "canonical")); f = np.r_[T["S"][:, 0], T["Xf"]]; y = np.r_[T["S"][:, 1], T["Xy"]]
for t in ("planted_canonical_T0_free", "planted_canonical_T1FY_free"):
    say(t)
    for q in J[t]:
        if q["c"] <= 15:
            d = np.log10(K.compile_form(q["eq"], q["tier"])(f, y)) - np.log10(K.H_plant(f, y)); say(f"  c{q['c']} {q['label']} rms dex {np.sqrt(np.mean(d*d)):.4f} worst {np.max(np.abs(d)):.3f} X-COP-row worst {np.max(np.abs(d[-len(T['Xf']):])):.3f} {q['eq'][:70]}")
near = []
for t, R in J.items():
    if t.startswith("real"):
        for q in R:
            for c in re.findall(r"(?<![A-Za-z_])\d+\.\d+(?:[eE][-+]?\d+)?", q["eq"]):
                for v in (1, 2, .5, 3.14159265):
                    if abs(float(c) / v - 1) <= .01: near.append((t, q["c"], c, v))
say(f"\nconstants within 1 % of 1, 2, 1/2, pi on real rows: {len(near)}: {near[:12]}")
open(os.path.join(K.HERE, "sr3_post.out"), "w").write("\n".join(L) + "\n")
