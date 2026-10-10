"""CFG585 POST HOC (disclosed, no verdict weight): empirical null of D from 200 random OLD/YOUNG relabels within mass
quintiles, construction A, canonical; compares the real D (K-in, K9) with the null distribution."""
import os, sys, io, json, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg585_age.py")).read().split('P("=" * 100)')[0]
ns = {"__file__": os.path.join(HERE, "cfg585_age.py")}
os.environ.pop("CFG585_MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src, "cfg585_head", "exec"), ns)
g = ns; E, OLD, YOUNG, qid, BANDS, NPATCH = g["E"], g["OLD"], g["YOUNG"], g["qid"], g["BANDS"], g["NPATCH"]
esd_loo, comps, all_bands = g["esd_loo"], g["comps"], g["all_bands"]
def Dval(o, y, c="A", foot="canonical"):
    out = {}
    fbs = {}
    for nm, mk in (("o", o), ("y", y)):
        d, C, L = esd_loo(mk); cp = comps(c, foot, mk); fbs[nm] = all_bands(d, C, cp)
    return {bd: fbs["o"][bd]["eps"] - fbs["y"][bd]["eps"] for bd in ("K-in", "K9")}
real = Dval(OLD, YOUNG)
rng = np.random.default_rng(5851); lab0 = np.zeros(len(E), int); lab0[OLD] = 1; lab0[YOUNG] = -1
null = {"K-in": [], "K9": []}
for i in range(200):
    lab = lab0.copy()
    for q in range(5):
        m = E & (qid == q); lab[m] = rng.permutation(lab[m])
    d = Dval(lab == 1, lab == -1)
    for bd in null: null[bd].append(d[bd])
out = {}
for bd in null:
    a = np.array(null[bd]); p = (np.sum(a >= real[bd]) + 1) / (len(a) + 1)
    out[bd] = dict(real=real[bd], null_mean=float(a.mean()), null_sd=float(a.std(ddof=1)), p_one_sided=float(p), z_emp=float((real[bd] - a.mean()) / a.std(ddof=1)))
    print(f"{bd}: real D {real[bd]:+.3f}; null mean {a.mean():+.3f} sd {a.std(ddof=1):.3f}; empirical one-sided p {p:.4f} (Z_emp {out[bd]['z_emp']:+.2f})")
json.dump(out, open(os.path.join(HERE, "cfg585_null_results.json"), "w"), indent=1)
