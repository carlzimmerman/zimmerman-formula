#!/usr/bin/env python3
"""SR3 known answers K1-K5. SR3_MUTATE=1: a0 x 1.5 labelled the law; must exit 1. kappa = 1/2 FITTED; not theory closed."""
import csv, glob, json, math, os, sys
sys.dont_write_bytecode = True
os.environ["OMP_NUM_THREADS"] = "1"; os.nice(19)
import numpy as np
import sr3_core as K
TAG = "_MUTATE" if K.MUT else ""; L = []; bad = 0
def chk(n, ok, d):
    global bad; bad += not ok; s = f"[{'PASS' if ok else 'FAIL'}] {n}: {d}"; print(s, flush=True); L.append(s)
P = K.prep("real", "canonical"); a0 = P["a0"]; G = P["gals"]; X = P["X"]; tr = [g for g in G if K.is_train(g)]; ho = [g for g in G if K.is_hold(g)]
x = K.xcop_stat(X, None, a0); chk("K1 X-COP all 7, H = 1", abs(x["mean"] - .4675) < .001 and abs(x["rms"] - .4763) < .001, f"{x['mean']:+.4f}, {x['rms']:.4f}, n {x['n']}; record +0.4675, 0.4763")
fx = K.fixed_path(tr, None, a0); chk("K1 SPARC fixed train", abs(fx["rms"] - .1664) < .001, f"{fx['rms']:.4f} med {fx['med']:+.4f}; record 0.1664")
BF = "(((f+2.0)/(1/(1+f)))**2)*(1/(1+((f+pi)+(f/y))))"; Hb = K.compile_form(BF); a = K.fixed_path(tr, Hb, a0); b = K.fixed_path(ho, Hb, a0); xt = K.xcop_stat(X, Hb, a0, 0); xh = K.xcop_stat(X, Hb, a0, 1)
vals = [(a["rms"], .184), (a["med"], -.012), (xt["mean"], .033), (xt["rms"], .099), (xh["mean"], -.009), (xh["rms"], .077), (b["rms"], .213)]
chk("K2 BF1's best, reading only", all(abs(p - q) <= .001 for p, q in vals), " ".join(f"{p:+.4f}/{q:+.3f}" for p, q in vals))
RL = json.load(open(os.path.join(K.RB, "RQ3_acceptance_v2", "results", "law.json")))["footings"]["canonical"]["rows"]
# RQ3 a0 rounded at 9.3603e-11: same path on all 175
f = K.free_path(G, None, K.A0_ACC["canonical"] * (1.5 if K.MUT else 1)); chk("K3 law, free path, all 175", abs(f["rms"] - RL["A1"]["value"]) < 1e-4 and abs(f["U"] - RL["A2"]["value"]) < 1e-4, f"rms {f['rms']:.5f}/{RL['A1']['value']:.5f}, U {f['U']:.2f}/{RL['A2']['value']:.2f}, tilt {f['tilt']:+.2f}")
K3 = json.load(open(os.path.join(K.RB, "UX3_cluster_gas_term", "ux3_kfit.json")))["canonical"]; Hu = lambda ff, y: 1 + K3 * ff * y
u = K.free_path(G, Hu, K.A0_ACC["canonical"]); xu = K.xcop_stat(X, Hu, K.A0_ACC["canonical"]); chk("K4 UX3 term, free path", abs(u["rms"] - .0907) < .001 and abs(u["U"] - .30) < .001 and abs(u["tilt"] + .05) < .011 and abs(xu["mean"] + .016) < .001 and abs(xu["rms"] - .089) < .001, f"rms {u['rms']:.4f} U {u['U']:.2f} tilt {u['tilt']:+.2f}; X {xu['mean']:+.4f}, {xu['rms']:.4f}")
LT = K.lt_stat(None, K.A0_ACC["canonical"]); chk("K-extra LITTLE THINGS, law", abs(LT["E"] - RL["A9"]["value"]) < 1e-3, f"{LT['E']:+.4f}/{RL['A9']['value']:+.4f}")
if not K.MUT:
    fs = sorted(glob.glob(os.path.join(K.HERE, "fronts", "hof_*.csv")))
    for F in fs:
        t = os.path.basename(F)[4:-4].split("_"); job, foot, tier, path = t[:4]; Pj = K.prep(job, foot); tab = K.search_table(Pj, path == "fixed"); wr = 0.0; n = 0
        for r in csv.DictReader(open(F)):
            Hf = K.compile_form(r["equation"], tier)
            try: pl = K.py_loss(tab, Hf, path == "fixed")
            except Exception as e: pl = float("nan")
            base = float(r["loss"])
            if tier == "T1FY":
                pf, py = np.meshgrid([.1, .3, .5, .7, .9, 1.0], [1e6, 1e8, 1e10, 1e12]); mx = np.max(np.abs(np.log10(Hf(pf.ravel(), py.ravel())))); pl += 100 * mx ** 2 if mx > 1e-3 else 0
            wr = max(wr, abs(pl / base - 1)); n += 1
        chk(f"K5 Julia loss = Python, {os.path.basename(F)[4:-4]}", wr < 1e-6, f"worst rel {wr:.2e} over {n} forms")
open(os.path.join(K.HERE, f"sr3_known{TAG}.out"), "w").write("\n".join(L) + f"\n{'exit 1' if bad else 'exit 0'}\n"); sys.exit(1 if bad else 0)
