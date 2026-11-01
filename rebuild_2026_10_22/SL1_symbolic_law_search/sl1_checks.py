#!/usr/bin/env python3
"""SL1 K1-K3, K5-K7, MUTATE, speed. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time
os.environ.setdefault("SL1_HERE", os.path.dirname(os.path.abspath(__file__)))
exec(compile(open(os.path.join(os.environ["SL1_HERE"], "discover_law.py")).read(), "discover_law", "exec"), globals())
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
t0 = time.time(); D = Data(); P(f"load {time.time()-t0:.1f} s; SPARC {len(D.gals)}; unique graded {len(D.sel)}; train {len(D.split['train'])} holdout {len(D.split['holdout'])}; I1 {I1:.5f}")
ok = True; ALL = list(range(len(D.gals))); NR = D.C["NR1_sparc"]["canonical"]; REC = json.load(open(os.path.join(RB, "NR1_native_n_ng80", "NR1_PRIMARY_x74_results_fs0.034_nat_s2.7774.json")))["footings"]["canonical"]["sparc"]
dk = 0.0
for t in TAGS:
    o = D.sparc(ALL, t); U, wr, ws, _ = D.sparc_fit(o, "1", "1", D.a0["canonical"]); m = float(np.median(U)); r = math.sqrt(wr.sum() / ws.sum()); dk = max(dk, abs(m - REC[t]["U_median"]), abs(r - REC[t]["rms"])); P(f"  {t}: U {m:.3f} rms {r:.5f} vs record {REC[t]['U_median']:.3f} {REC[t]['rms']:.5f}")
k = dk <= 1e-9; ok &= k; P(f"K1 NR1 PRIMARY on 175: max |d| {dk:.1e}: {'PASS' if k else 'FAIL'}")
BR = {"20-60": 1.20, "60-100": 1.19, "100-150": 0.91, "150-200": 0.57, "200-250": 0.62, "250-400": 0.77}; o = D.sparc(ALL, TA); U, *_ = D.sparc_fit(o, "1", "1", D.a0["canonical"]); dk = 0.0; ns = []
for (l, h) in BINS:
    idx = [i for i in D.sel if l <= D.gals[i]["vf"] <= h]; u = float(np.median(U[idx])); ns.append(len(idx)); dk = max(dk, abs(u - BR[f"{l}-{h}"]))
k = dk <= 0.0051 and sum(ns) == 124; ok &= k; P(f"K2 U by V_flat inclusive bins, n {ns} sum {sum(ns)}, unique {len(D.sel)}: max |d| {dk:.3f}: {'PASS' if k else 'FAIL'}")
CC = D.C["clusters"]; dk = 0.0; dz = 0.0
for f in ("canonical", "alt"):
    for h in HKS:
        V = D.cluster_V(h, "1", "1", D.a0[f]); pl = dict(capture=True, pred_out={}); Z = keys_core(CC, V, f, h, pl); pv = pl["pred_out"][h]; c = CC["NR1_cells"][f][h]; dk = max(dk, max(abs(pv[i] - c[n]["pred"]) for i, n in enumerate(KEYS)))
        if f == "canonical": P(f"  {h} one-template Z: " + ", ".join(f"{n} {Z[i]:+.2f}" for i, n in enumerate(KEYS) if abs(Z[i]) > 1.5))
k = dk <= 1e-6; ok &= k; P(f"K3 cluster preds vs NR1 PRIMARY cells, both footings: max |d| {dk:.1e}: {'PASS' if k else 'FAIL'}")
NDR = json.load(open(os.path.join(RB, "ND1_native_dwarfs", "nd1_ab_results.json")))["native"]; dk = max(abs(D.C["K5_nd1"][t] - NDR[t]["lt"]["all"]["median"]) for t in TAGS); k = dk <= 1e-6; ok &= k; P(f"K5 LITTLE THINGS at ND1's rule: {D.C['K5_nd1'][TA]:+.4f}, max |d| {dk:.1e}: {'PASS' if k else 'FAIL'}"); P(f"  LITTLE THINGS at NR1 PRIMARY: {float(np.median(D.lt_E(TA,'1','1',D.a0['canonical']))):+.4f}, {float(np.median(D.lt_E(TB,'1','1',D.a0['canonical']))):+.4f}")
g = D.groups("1", "1"); rg = D.C["groups"]["K6"]; dk = abs(g["Z"] - rg["Z"]); dk2 = abs(g["mean"] - rg["mean"]); k = max(dk, dk2) <= 1e-6; ok &= k; P(f"K6 groups Z {g['Z']:+.4f} vs {rg['Z']:+.4f}, mean |d| {dk2:.1e}: {'PASS' if k else 'FAIL'}")
x = D.xcop("1", "1"); r = D.C["xcop"]["canonical"]; dk = max(abs(x["mean"] - r["mean"]), abs(x["rms"] - r["rms"])); k = dk <= 1e-9; ok &= k; P(f"K7 X-COP mean {x['mean']:+.4f} rms {x['rms']:.4f} ({'PASS' if x['PASS'] else 'FAIL'} line): max |d| {dk:.1e}: {'PASS' if k else 'FAIL'}")
b = D.grade("1", "1"); P(f"baseline train: gate {b['gate']:.3f} g1 {b['g1']:.3f} g2 {b['g2']:.3f} g3 {b['g3']:.3f} g4 {b['g4']:.3f}; bad {b['detail']['bad']}; U {b['detail'][TA]} S_z {[round(z,2) for z in b['detail']['S_z']]}")
for nm, ctx in (("SPARC", D.sparc(ALL, TA)["s"]), ("LT", D.lt[TA]["s"]), ("clusters", D.cl[HKS[0]]["s"])):
    P(f"  {nm} leaves: " + ", ".join(f"{k} [{np.percentile(v,2):.3g}, {np.median(v):.3g}, {np.percentile(v,98):.3g}]" for k, v in ctx.V.items()))
T = ("inv1p", ("log1p", ("mul", "q", "fb"))); B_ = ("add", "1", ("mul", "xb", ("inv1p", ("mul", "q", "xc")))); P(f"tier1 probe A {to_s(T)}: {tier1(T,'A')}, B {to_s(B_)}: {tier1(B_,'B')}, A='2': {tier1('2','A')}")
t0 = time.time(); n = 0
for _ in range(20): D.grade(T, "1"); n += 1
ta = (time.time() - t0) / n; t0 = time.time()
for _ in range(20): D.grade(T, B_); D.sparc(D.split["train"], TA)["memo"].clear(); D.sparc(D.split["train"], TB)["memo"].clear(); n += 1
P(f"speed: A only {ta*1e3:.0f} ms, A+B {(time.time()-t0)/20*1e3:.0f} ms")
g1 = D.grade(T, "1"); s = D.sparc(D.split["train"], TA)["s"]; q0 = s.V["q"].copy(); s.V["q"] = np.random.default_rng(1).permutation(q0); g2 = D.grade(T, "1"); s.V["q"] = q0; m = abs(g1["gate"] - g2["gate"]) > 1e-3; ok &= m; P(f"MUTATE q_diss scrambled: gate {g1['gate']:.3f} -> {g2['gate']:.3f}: {'BITES' if m else 'NO BITE'}")
P("CHECKS " + ("ALL PASS" if ok else "FAILED")); open(os.path.join(HERE, "sl1_checks.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
