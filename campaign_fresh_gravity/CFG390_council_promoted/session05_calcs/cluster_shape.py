#!/usr/bin/env python3
"""Session 5, test K: is the X-COP clusters' missing mass shaped like the law's phantom (settling model) or like the baryons?
Run: python3 cluster_shape.py [--mutate]"""
import os, sys, json, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
sys.path.insert(0, os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026"))
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C
    import cluster_audit as CA
OUT = []
def P(s=""): print(s); OUT.append(str(s))
clusters = [CA.load_cluster(p.name) for p in sorted(CA.DATA.iterdir()) if p.is_dir()]
names = [c["name"] for c in clusters]
R = CA.RADII
gas, stars, mh = CA.profiles(clusters, R)
mb = gas + stars
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
sel = (R >= 100) & (R <= 1000)
def slopes(ratio):
    out = []
    for i in range(len(clusters)):
        y = ratio[i, sel]; x = np.log10(R[sel]); ok = np.isfinite(y) & (y > 0)
        out.append(np.polyfit(x[ok], np.log10(y[ok]), 1)[0] if ok.sum() >= 3 else np.nan)
    return np.array(out)
def boot(s, seed=31):
    s = s[np.isfinite(s)]; rng = np.random.default_rng(seed)
    return float(np.median(s)), float(np.std([np.median(s[rng.integers(0, len(s), len(s))]) for _ in range(2000)])), len(s)
def verdict(t, b):
    # guard (fixed after the 10-06 run, disclosed): an exactly zero bootstrap spread (the MUTATE case, ratio slope identically 0)
    # crashed with ZeroDivisionError; a zero slope with zero spread is 0 sigma, a non-zero slope with zero spread is infinite
    z = lambda x: (0.0 if abs(x[0]) < 1e-12 else float("inf")) if x[1] == 0 else abs(x[0]) / x[1]
    tz, bz = z(t), z(b)
    if tz < 2 and bz > 3: return "TARGET-SHAPED"
    if bz < 2 and tz > 3: return "BARYON-SHAPED"
    if tz > 3 and bz > 3: return "NEITHER"
    return "NON-DISCRIMINATING"
res = {}
for foot, a0 in A0.items():
    gb = C.G if hasattr(C, "G") else None
    g_b = 6.674e-11 * mb * 1.989e30 / (R * 3.0857e19) ** 2
    mlaw = C.nu_mono(g_b / a0) * mb
    mph = mlaw - mb
    for bias in (0.0, 0.2):
        mtrue = mh / (1 - bias)
        mc = 2 * mb if MUT else mtrue - mlaw
        for subset, idx in (("all", np.arange(len(clusters))), ("relaxed", np.array([i for i, n in enumerate(names) if n in CA.RELAXED])),
                            ("stellar-file", np.array([i for i, c in enumerate(clusters) if c["has_star"]]))):
            sT = slopes(mc / mph)[idx]; sB = slopes(mc / mb)[idx]
            t, b = boot(sT), boot(sB)
            v = verdict(t, b)
            key = f"{foot}|b{bias}|{subset}"
            res[key] = dict(slope_vs_phantom=t, slope_vs_baryons=b, verdict=v)
            if subset == "all" or bias == 0.0:
                P(f"{foot:9s} b={bias} {subset:12s} N {t[2]:2d}: slope log(Mc/Mph) {t[0]:+.3f} +- {t[1]:.3f} | slope log(Mc/Mb) {b[0]:+.3f} +- {b[1]:.3f} -> {v}")
    if foot == "canonical":
        P("  per cluster (canonical, b=0): name | Mc/Mph at 300 kpc | slope vs Mph | slope vs Mb | Mc>0 at all fit radii")
        sT = slopes((mh - mlaw) / mph); sB = slopes((mh - mlaw) / mb); j300 = list(R).index(300.0)
        for i, n in enumerate(names):
            P(f"    {n:8s} {((mh-mlaw)/mph)[i, j300]:6.2f}  {sT[i]:+.3f}  {sB[i]:+.3f}  {bool(np.all((mh-mlaw)[i, sel][np.isfinite((mh-mlaw)[i, sel])] > 0))}")
json.dump(res, open(os.path.join(HERE, f"cluster_shape{TAG}_results.json"), "w"), indent=1)
open(os.path.join(HERE, f"cluster_shape{TAG}.out"), "w").write("\n".join(OUT) + "\n")
rc = 0
if MUT:
    rc = 1 if res["canonical|b0.0|all"]["verdict"] == "BARYON-SHAPED" else 0
    P(f"MUTATE: verdict {res['canonical|b0.0|all']['verdict']} -> {'detected' if rc else 'NOT detected'}")
sys.exit(rc)
