#!/usr/bin/env python3
"""BF2 step 6: L4 control on a frozen job sample, one thread. Usage: bf2_control.py N_JOBS ARM. ARM real, control, perm1, perm2. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, time
from bf2_common import *
N = int(sys.argv[1]); ARM = sys.argv[2]; snap = snapshot(); rg = np.random.default_rng(20261102); jobs_all = sorted(snap["done"]); idx = rg.permutation(len(jobs_all))[:N]; jobs = [jobs_all[i] for i in idx]
src = open(os.path.join(BF1, "bf1.py")).read().split('if __name__ == "__main__"')[0]
SEED = {"real": 20261102, "control": 20261102, "perm1": 1, "perm2": 2}[ARM]; a = "rng = np.random.default_rng(20261102)"; assert src.count(a) == 1; src = src.replace(a, f"rng = np.random.default_rng({SEED})")
sys.argv = ["bf1.py", "real" if ARM == "real" else "control"]; ns = {"__file__": os.path.join(BF1, "bf1.py"), "__name__": "bf1x"}; exec(compile(src, "bf1.py", "exec"), ns); nm = names(); t0 = time.time()
EV = ns["EV"]; lv = np.empty((len(nm), EV.shape[0]))
for k, s in enumerate(nm): lv[k] = ns["tree_eval"](s, EV)
lv *= HMUT; print(f"{ARM}: closure {lv.shape} evaluated {time.time() - t0:.0f} s", flush=True)
ns["LV"] = lv; ns["NAMES"] = nm; hits = []; cnt = 0; per = []
for q, jb in enumerate(jobs):
    i = int(jb[:-1]); op = jb[-1]; _, _, c, out = ns["work"]((i, op)); cnt += c; hits += out; per.append(len(out))
    if q % 200 == 0: print(q, cnt, len(hits), f"{time.time() - t0:.0f} s", flush=True)
full, ST, XT, XH = ns["full"], ns["ST"], ns["XT"], ns["XH"]; rows = []
for i, o, j, w in hits:
    s = f"({nm[i]}{o}{nm[j]})"; d, dx, dh = full(s, w, ST), full(s, w, XT), full(s, w, XH); rows.append(dict(i=i, op=o, j=j, w=w, rms=float(np.sqrt((d * d).mean())), med=float(np.median(d)), x=float(dx.mean()), xr=float(np.sqrt((dx * dx).mean())), xh=float(dh.mean()), xhr=float(np.sqrt((dh * dh).mean()))))
json.dump(dict(arm=ARM, n_jobs=N, expressions=cnt, per_job=per, hits=rows), open(os.path.join(LANE, f"control_{ARM}_N{N}{TAG}.json"), "w"), indent=0, sort_keys=True); print(f"{ARM}: jobs {N}, expressions {cnt}, hits {len(rows)}, wall {time.time() - t0:.0f} s", flush=True)
