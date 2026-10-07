#!/usr/bin/env python3
"""Session 4, test S: skewness of SPARC RAR residuals by g_bar bin (supply limit predicts negative at low g_bar). Run: python3 sparc_skew.py [--mutate]"""
import os, sys, json, io, contextlib
import numpy as np
from scipy.stats import skew
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
OUT = []
def P(s=""): print(s); OUT.append(str(s))
GAL = [g for g in C.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2]
KPC = 3.0857e19; EDGES = [-12.5, -11.5, -11.0, -10.5, -10.0, -9.0]
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
res = {}
for foot, a0 in A0.items():
    per = [[] for _ in range(len(EDGES) - 1)]
    for g in GAL:
        R = g["R"] * KPC
        b = (np.sign(g["Vgas"]) * g["Vgas"] ** 2 + 0.5 * g["Vdisk"] ** 2 + 0.7 * g["Vbul"] ** 2) * 1e6 / R
        o = (g["Vobs"] * 1e3) ** 2 / R
        ok = (b > 0) & (o > 0)
        r = np.log10(o[ok]) - np.log10(C.nu_mono(b[ok] / a0) * b[ok]); lb = np.log10(b[ok])
        w = 1 / (np.clip(g["eV"][ok], 1, None) / np.clip(g["Vobs"][ok], 1, None)) ** 2
        if MUT: r = -r
        for k in range(len(EDGES) - 1):
            m = (lb >= EDGES[k]) & (lb < EDGES[k + 1])
            if m.sum(): per[k].append(float(np.sum(w[m] * r[m]) / np.sum(w[m])))
    rng = np.random.default_rng(23); out = []
    for k, x in enumerate(per):
        x = np.array(x); s = float(skew(x))
        bs = [skew(x[rng.integers(0, len(x), len(x))]) for _ in range(2000)]
        out.append(dict(bin=[EDGES[k], EDGES[k + 1]], n=len(x), median=float(np.median(x)), skew=s, err=float(np.std(bs))))
        P(f"{foot:9s} log g_bar [{EDGES[k]:+.1f},{EDGES[k+1]:+.1f}): N gal {len(x):3d}  median {np.median(x):+.3f}  skew {s:+.2f} +- {np.std(bs):.2f}")
    lo, hi = out[0], out[-1]
    if lo["skew"] >= 0 or abs(lo["skew"]) < 2 * lo["err"]: v = "NO SUPPLY SIGNAL"
    elif lo["skew"] < -3 * lo["err"] and lo["skew"] < hi["skew"]: v = "CONSISTENT WITH A BINDING LIMIT"
    else: v = "INCONCLUSIVE"
    res[foot] = dict(bins=out, verdict=v); P(f"  -> {v}")
json.dump(res, open(os.path.join(HERE, f"sparc_skew{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"sparc_skew{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    m = json.load(open(os.path.join(HERE, "sparc_skew_results.json")))
    rc = 1 if np.sign(m["canonical"]["bins"][0]["skew"]) != np.sign(res["canonical"]["bins"][0]["skew"]) else 0
    P(f"MUTATE: lowest-bin skew sign flipped -> {'detected' if rc else 'NOT detected'}")
sys.exit(rc)
