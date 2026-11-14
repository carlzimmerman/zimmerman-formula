#!/usr/bin/env python3
"""OTA1 read-out (FROZEN_CRITERIA.md): known answers, twins, checks, lane words per footing, other keys. Reads cache_jobs only; writes ota1.out, ota1_results.json.
kappa = 1/2 and X = 5.41 FITTED; cold dark energy, never a particle; not theory closed."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CJ = os.path.join(HERE, "cache_jobs"); OUT = []; HH = ("h0672", "h0686"); FEET = ("canonical", "alt")
def P(s): print(s, flush=True); OUT.append(s)
J = {f[:-5]: json.load(open(os.path.join(CJ, f))) for f in sorted(os.listdir(CJ)) if f.endswith(".json")}
P("OTA1 read-out: cold share X x M_b(< r_ta) counted once, share beyond the fair-share R200c in the record's layout, rescaled; gas +0.005; kappa = 1/2 and X = 5.41 FITTED; not theory closed")
ok = True; R = {}
# KA1
KA = {("0.034", "h0672"): 4.41, ("0.034", "h0686"): 4.07, ("0.0615", "h0672"): 4.13, ("0.0615", "h0686"): 3.81}; XK = {"0.034": (0.013, 0.075), "0.0615": (0.005, 0.074)}
for fs in ("0.034", "0.0615"):
    b = J.get(f"BASE_{fs}")
    if b is None: P(f"KA1 f* {fs}: BASE missing"); ok = False; continue
    d = max(abs(b["cells"]["canonical"][h]["G-OUT-M3"]["Z"] - KA[(fs, h)]) for h in HH); x = b["xcop"]["canonical"]; dx = max(abs(x["mean"] - XK[fs][0]), abs(x["rms"] - XK[fs][1]))
    k = d <= 0.01 and dx <= 0.001; ok &= k; P(f"KA1 f* {fs}: base G-OUT-M3 canonical " + " / ".join(f"{b['cells']['canonical'][h]['G-OUT-M3']['Z']:+.3f}" for h in HH) + f" (record {KA[(fs, 'h0672')]:+.2f} / {KA[(fs, 'h0686')]:+.2f}; max |d| {d:.4f}), X-COP {x['mean']:+.4f} {x['rms']:.4f} (|d| {dx:.4f}): {'PASS' if k else 'FAIL'}")
# TW0
b, t = J.get("BASE_0.034"), J.get("TW0_0.034")
if b and t:
    dp = max(abs(b["cells"][ft][h][k]["pred"] - t["cells"][ft][h][k]["pred"]) for ft in FEET for h in HH for k in b["cells"][ft][h]); dz = max(abs(b["cells"][ft][h][k]["Z"] - t["cells"][ft][h][k]["Z"]) for ft in FEET for h in HH for k in b["cells"][ft][h])
    dxx = max(abs(b["xcop"][ft][q] - t["xcop"][ft][q]) for ft in FEET for q in ("mean", "rms")); k = dp <= 1e-9 and dxx <= 1e-9; ok &= k
    P(f"TW0 zero extra share (lambda = 1) against base, both footings, 15 keys: max |d pred| {dp:.1e}, |d Z| {dz:.1e}, X-COP {dxx:.1e}: {'PASS' if k else 'FAIL'}")
else: P("TW0: missing"); ok = False
# TW2
r, t2 = J.get("RULE_0.034"), J.get("TW2_0.034")
if b and t2:
    dd = [abs(t2["cells"]["canonical"][h]["G-OUT-M3"]["Z"] - b["cells"]["canonical"][h]["G-OUT-M3"]["Z"]) for h in HH]; k = min(dd) >= 0.10; ok &= k
    P(f"TW2 doubled share moves G-OUT-M3 canonical by " + " / ".join(f"{x:.3f}" for x in dd) + f" (line 0.10 every cell): {'BITES' if k else 'DOES NOT BITE'}")
else: P("TW2: missing"); ok = False
# K1, K2 and per-cluster stats on the rule
if r:
    st = [q for q in r["ota1"] if q.get("case") in ("scaled", "uniform")]
    k1 = max(abs(q["k1_tot_mf"]) for q in st); k1i = max(q["k1_in"] for q in st); kk = k1 <= 1e-9 and k1i <= 1e-12; ok &= kk
    P(f"K1 rule, every call ({len(st)} scaled or uniform): max |M_new(r_ta)/Mfair - 1| {k1:.1e}, max inside R2 {k1i:.1e}: {'PASS' if kk else 'FAIL'}")
    from collections import Counter; P("  cases: " + ", ".join(f"{a} {n}" for a, n in Counter(q["case"] for q in r["ota1"]).items()))
    dg = max(abs(np.array(r["groups"][ft]["Z"], float) - np.array(b["groups"][ft]["Z"], float)).max() if isinstance(b["groups"][ft]["Z"], list) else abs(r["groups"][ft]["Z"] - b["groups"][ft]["Z"]) for ft in FEET)
    ds = max(abs(r["sparc"][ft][t_]["rms"] - b["sparc"][ft][t_]["rms"]) for ft in FEET for t_ in b["sparc"][ft]) if isinstance(b["sparc"]["canonical"], dict) and "A_c2b_refit" in b["sparc"]["canonical"] else max(abs(r["sparc"][ft]["rms"] - b["sparc"][ft]["rms"]) for ft in FEET)
    k2 = dg <= 1e-12 and ds <= 1e-12; ok &= k2; P(f"K2 groups Z |d| {dg:.1e}, SPARC rms |d| {ds:.1e}: {'PASS' if k2 else 'FAIL'}")
    T3M = None
    try:
        import sys; sys.path.insert(0, HERE)
    except Exception: pass
    for ft in FEET:
        for hk in ("h0672",):
            ss = [q for q in st if q["foot"] == ft and q["hk"] == hk]; xc = [q for q in st if q["foot"] == ft and q["hk"] == "xcop"]
            if ss: P(f"  {ft} {hk} KiDS clusters ({len(ss)}): lambda median {np.nanmedian([q['lam'] for q in ss]):.3f} [16-84 {np.nanpercentile([q['lam'] for q in ss], 16):.3f}, {np.nanpercentile([q['lam'] for q in ss], 84):.3f}]; record's cold to r_ta / Mfair median {np.median([q['rec_over_Mfair'] for q in ss]):.3f}; at R2 / Mfair {np.median([q['R2_over_Mfair'] for q in ss]):.3f}; R2 {np.median([q['R2_mpc'] for q in ss]):.2f} Mpc, r_ta {np.median([q['rta_mpc'] for q in ss]):.2f} Mpc")
            if xc: P(f"  {ft} X-COP calls ({len(xc)}): lambda median {np.nanmedian([q['lam'] for q in xc]):.3f}; record / Mfair {np.median([q['rec_over_Mfair'] for q in xc]):.3f}")
    R["rule_stats"] = [q for q in r["ota1"] if q.get("hk") in ("h0672", "xcop")]
# labels
def passes(c, k): return all(abs(c[h][k]["Z"]) <= 2 for h in HH)
xok = lambda x: abs(x["mean"]) <= 0.05 and x["rms"] <= 0.10
LAB = {}
for ft in FEET:
    zz = {(fs, h): J[f"RULE_{fs}"]["cells"][ft][h]["G-OUT-M3"]["Z"] for fs in ("0.034", "0.0615") if f"RULE_{fs}" in J for h in HH}
    if len(zz) < 4 or not ok: w = "NO VERDICT"
    else:
        np_ = sum(abs(v) <= 2 for v in zz.values()); w = "OUTER SHEAR ROW PASSES WITH THE SHARE TO TURNAROUND" if np_ == 4 else "STILL FAILS" + (" (OVER)" if min(zz.values()) < -2 else "") if np_ == 0 else "STILL FAILS [CELL-DEPENDENT]"
    br, mi = [], []
    for fs in ("0.034", "0.0615"):
        if f"RULE_{fs}" not in J: continue
        cb, cr = J[f"BASE_{fs}"]["cells"][ft], J[f"RULE_{fs}"]["cells"][ft]
        for k in cb["h0672"]:
            if k == "G-OUT-M3": continue
            if passes(cb, k) and not passes(cr, k): br.append(f"{k} at f* {fs}")
            if not passes(cb, k) and passes(cr, k): mi.append(f"{k} at f* {fs}")
        if xok(J[f"BASE_{fs}"]["xcop"][ft]) and not xok(J[f"RULE_{fs}"]["xcop"][ft]): br.append(f"X-COP at f* {fs}")
    w2 = "OTHER KEYS: NONE BROKEN" if not br else "OTHER KEYS BROKEN: " + ", ".join(br)
    LAB[ft] = dict(word=w, other=w2, moved_in=mi, Z={f"{a}|{b}": v for (a, b), v in zz.items()}); P(f"WORD {ft}: {w}. {w2}." + (f" Moved in: {', '.join(mi)}." if mi else ""))
# tables
for ft in FEET:
    P(f"--- {ft}")
    for j in ("BASE_0.034", "RULE_0.034", "TW0_0.034", "TW2_0.034", "BRK2.676_0.034", "BRK3.071_0.034", "BASE_0.0615", "RULE_0.0615"):
        if j not in J: continue
        c = J[j]["cells"][ft]; bad = sorted({k for h in HH for k, v in c[h].items() if abs(v["Z"]) > 2}); x = J[j]["xcop"][ft]
        P(f"  {j}: {15 - len(bad)} of 15 keys, over 2 {bad}; X-COP {x['mean']:+.4f} {x['rms']:.4f}")
        for h in HH: P(f"     {h}: " + "; ".join(f"{k} {v['Z']:+.2f} (pred {v['pred']:.3f}, A {v['meas']:.3f})" if k.startswith("G-OUT-M") else f"{k} {v['Z']:+.2f}" for k, v in c[h].items()))
R.update(labels=LAB, checks_ok=bool(ok)); json.dump(R, open(os.path.join(HERE, "ota1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "ota1.out"), "w").write("\n".join(OUT) + "\n")
