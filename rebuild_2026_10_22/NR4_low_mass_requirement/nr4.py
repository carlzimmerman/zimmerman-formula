#!/usr/bin/env python3
"""NR4 (FROZEN_CRITERIA.md): requirement map, low-mass eta multiplier m by net response f, on UR1's path, read only. m, f FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SL1 = os.path.join(RB, "SL1_symbolic_law_search"); UR1 = os.path.join(RB, "UR1_one_response_rule"); NR2 = os.path.join(RB, "NR2_low_mass_ng80"); NR3 = os.path.join(RB, "NR3_ur1_on_nr2"); OUT = []; TG = ("A_c2b_refit", "B_cfg886_bg"); ETA = 21.53
def P(s): print(s, flush=True); OUT.append(s)
J = json.load(open(os.path.join(NR2, "nr2_results.json"))); R10, R11 = J["r10"], J["r11"]; E10 = J["eta"]["1e+10_ng80"]; E11 = J["eta"]["1e+11_ng80"]; PRE = re.search(r'pre = (""".*?""")', open(os.path.join(UR1, "ur1.py")).read(), re.S).group(1); FS = [0, 0.25, 0.5, 0.75, 0.87, 1]; MS = [1, 1.15, 1.3, 1.5, 1.7, 2]
def go(tag, r10, r11, fs, flip=False):
    O = os.path.join(HERE, f"nr4_{tag}_results.json")
    if os.path.exists(O) and set(json.load(open(O))) >= {f"{x:g}" for x in fs}: return json.load(open(O))
    W = os.path.join(HERE, f"cache_{tag}"); os.makedirs(W, exist_ok=True); t = open(os.path.join(UR1, "ur1_tail.py")).read(); i = t.index("import time as _tm"); tl = os.path.join(W, "nr4_tail.py"); open(tl, "w").write(t[:i] + open(os.path.join(HERE, "nr4_tail_add.py")).read())
    d = open(os.path.join(SL1, "sl1_harvest.py")).read()
    for a, b in (('SL1ADD = f"sub(', 'SL1ADD = ' + repr(eval(PRE)) + ' + f"sub('), ('os.path.join(HERE, "sl1_tail_harvest.py")', repr(tl)), ('WD = os.path.join(HERE, "cache")', f'WD = {W!r}'), ('HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)', f'HERE = {HERE!r}; RB = {RB!r}'), ('json.dumps([math.log10(29.26 / E), math.log10(24.34 / E), 0.0])', f'json.dumps([math.log10({r10!r}), math.log10({r11!r}), 0.0])'), ('os.path.join(NRD, "NR1_PRIMARY_cf_table.json")', repr(os.path.join(NR2, "NR2_MEDIAN_cf_table.json")))): assert d.count(a) == 1, a; d = d.replace(a, b)
    df = os.path.join(W, "nr4_driver.py"); open(df, "w").write(d); env = dict(os.environ, UR1_SL1=SL1, SL1_OUT=O, CN1_FORCE="1", OMP_NUM_THREADS="1", UR1_DRIVER="1", NR4_FS=json.dumps(fs), NR4_FLIP="1" if flip else "0")
    subprocess.run(["nice", "-n", "15", sys.executable, df], env=env, stdout=open(os.path.join(HERE, f"nr4_{tag}_run.log"), "w"), stderr=subprocess.STDOUT)
    if not os.path.exists(O): raise SystemExit(f"NOT DECIDED: {tag} wrote no result")
    return json.load(open(O))
def dif(c, ref): return max(max(abs(c["sparc"][t]["U"] - ref["sparc"][t]["U"]), abs(c["sparc"][t]["rms"] - ref["sparc"][t]["rms"]), abs(c["sparc"][t]["tilt"] - ref["sparc"][t]["tilt"]), abs(c["lt"][t] - ref["lt"][t])) for t in TG)
def gate(c): s = c["sparc"]; return dict(line=all(s[t]["rms"] <= 0.110 and 0.5 <= s[t]["U"] <= 0.8 for t in TG), tilt=all(abs(s[t]["tilt"]) <= 0.15 for t in TG), groups=c["groups"]["verdict"] == "CONSISTENT", lt=all(abs(c["lt"][t]) <= 0.10 for t in TG))
P("NR4 requirement map, m and f FITTED; kappa = 1/2 FITTED, unused; not theory closed"); M3 = json.load(open(os.path.join(NR3, "nr3_MEDIAN_results.json")))["runs"]; H3 = json.load(open(os.path.join(NR3, "nr3_HIGH_results.json")))["runs"]; G = {}
for m in MS: G[m] = go(f"m{m:g}", R10 * m, R11 * m, FS); P(f"m {m:g} done")
k1 = dif(G[1]["1"], M3["EM1|blum"]); k2 = dif(G[1]["0"], M3["EM1|off"]); K3 = go("K3", J["r10_68"][1], J["r11_68"][1], [0]); k3 = dif(K3["0"], H3["EM1|off"]); MU = go("MUTATE", R10, R11, [1], flip=True); mt = dif(MU["1"], M3["EM1|blum"]) > 1e-6; ok = k1 <= 1e-6 and k2 <= 1e-6 and k3 <= 1e-6 and mt; P(f"K1 {k1:.1e} K2 {k2:.1e} K3 {k3:.1e}; MUTATE breaks K1: {mt}: {'PASS' if ok else 'FAIL'}")
P("cells: m, f, U A/B, rms A, tilt A/B, groups, LT A/B, bins A, gates failed"); C = []
for m in MS:
    for f in FS:
        c = G[m][f"{f:g}"]; s = c["sparc"]; g = gate(c); fail = [k for k, v in g.items() if not v]; C.append((m, f, not fail)); P(f"  {m:g} {f:g}: {s[TG[0]]['U']:.2f}/{s[TG[1]]['U']:.2f} {s[TG[0]]['rms']:.4f} {s[TG[0]]['tilt']:+.2f}/{s[TG[1]]['tilt']:+.2f} {c['groups']['Z']:+.2f} {c['lt'][TG[0]]:+.3f}/{c['lt'][TG[1]]:+.3f} {[round(v, 2) for v in s[TG[0]]['bins'].values()]} {'CLEARS' if not fail else fail}")
Y = [x for x in C if x[2]]; e10 = lambda m: ETA * R10 * m; e11 = lambda m: ETA * R11 * m
if not Y: L = "NO CELL"
else:
    fm = max(x[1] for x in Y); ms = sorted({x[0] for x in Y}); L = "REGION AT f >= 0.87" if fm >= 0.87 else "REGION ONLY BELOW f 0.87"; lo = min(ms); L += " [ABOVE EVERY SEED]" if (e10(lo) > max(E10) or e11(lo) > max(E11)) else " [ABOVE BAND]" if (e10(lo) > 29.71 or e11(lo) > 26.33) else ""; P(f"clearing: f_max {fm:g}; m {ms}; lowest m needs eta {e10(lo):.1f}, {e11(lo):.1f} vs seed max {max(E10):.1f}, {max(E11):.1f}")
V = L if ok else "NOT DECIDED"; P("VERDICT: " + V); json.dump(dict(verdict=V, clear=[x[:2] for x in Y], K=[k1, k2, k3]), open(os.path.join(HERE, "nr4_results.json"), "w"), indent=1); open(os.path.join(HERE, "nr4.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
