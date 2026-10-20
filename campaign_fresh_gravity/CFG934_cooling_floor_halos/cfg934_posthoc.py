#!/usr/bin/env python3
"""CFG934 POST-HOC diagnostic (added 2026-10-20 AFTER the frozen main run was seen; no class weight, no verdict change).
Why does the LVD-83 class stay above the floor's prediction under reading (S)?  Split the 83 dwarfs by whether the cooling-floor
debris acts (f_ex > 0) and by M_V, and list the largest residuals, at every corner, both footings, readings S and M.
Uses cfg934.py's own definitions (exec'd read-only up to its K section; nothing in cfg934.py changed).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg934_posthoc.py  -> cfg934_posthoc.out / cfg934_posthoc.json
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "cfg934.py")
os.environ["CFG934_MODE"] = "main"
src = open(SRC).read()
g = {"__file__": SRC, "__name__": "cfg934_defs"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# =====================================================================================================================  K\n")], "cfg934", "exec"), g)
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


P(__doc__.split("Run:")[0].strip())
SAMP, PRE, L_parts, hcf, CK, ckey, A0X, FBN = (g[k] for k in ("SAMP880", "PRE880", "L_parts", "hcf", "CK", "ckey", "A0X", "FBN"))
MV = np.array([PRE[d["name"]]["MV"] for d in SAMP]); names = [d["name"] for d in SAMP]
bins = (("M_V <= -10", MV <= -10), ("-10 < M_V <= -7.7", (MV > -10) & (MV <= -7.7)), ("M_V > -7.7", MV > -7.7))
RES = {}
for f in ("canonical", "alt"):
    a0 = A0X[f]
    Eb, _, _, _, _ = g["L_parts"](f, a0, "L", None, FBN)
    P(f"\n[{f}] bare law: mean E {Eb.mean():+.3f} ln; by M_V: " + "; ".join(f"{lab} {Eb[m].mean():+.3f} (N {m.sum()})" for lab, m in bins))
    for reading in ("S", "M"):
        for c in CK:
            E, eps, fx, boost, _ = L_parts(f, a0, reading, hcf(*c)["lvd"], FBN)
            act = boost > 1e-6
            r = dict(mean=float(E.mean()), n_act=int(act.sum()),
                     act_mean=(float(E[act].mean()) if act.any() else None), act_bare=(float(Eb[act].mean()) if act.any() else None),
                     off_mean=(float(E[~act].mean()) if (~act).any() else None), off_bare=(float(Eb[~act].mean()) if (~act).any() else None),
                     by_MV={lab: dict(N=int(m.sum()), E=float(E[m].mean()), bare=float(Eb[m].mean()), n_act=int((act & m).sum())) for lab, m in bins},
                     top=[(names[i], float(MV[i]), float(E[i]), float(fx[i]), bool(act[i])) for i in np.argsort(-E)[:8]])
            RES[f"{f}|{reading}|{ckey(c)}"] = r
            P(f"  ({reading}) {ckey(c):18s} mean {r['mean']:+.3f} | floor acts in {r['n_act']:2d}: residual {r['act_mean'] if r['act_mean'] is None else round(r['act_mean'], 3):+} "
              f"(bare {r['act_bare'] if r['act_bare'] is None else round(r['act_bare'], 3):+}) | floor silent in {83 - r['n_act']:2d}: residual "
              f"{r['off_mean'] if r['off_mean'] is None else round(r['off_mean'], 3):+} | by M_V: " +
              "; ".join(f"{v['E']:+.2f} ({v['n_act']}/{v['N']} act)" for v in r["by_MV"].values()))
    best = RES[f"{f}|S|mu0.59|t50|C6000"]
    P(f"  largest residuals, (S) mu0.59|t50|C6000: " + ", ".join(f"{n} (M_V {m:.1f}, E {e:+.2f}, f_ex {x:.2f})" for n, m, e, x, _ in best["top"]))
    # where f_ex switches off: baryon mass of the f_ex = 0 / f_ex > 0 boundary (part 2 of this post-hoc diagnostic, same date)
    Mb = np.array([2.0 * 10 ** (0.4 * (4.83 - PRE[n]["MV"])) + (1.33 * 10 ** PRE[n]["lHI"] if PRE[n]["lHI"] is not None else 0.0) for n in names])
    EP = np.array([g["ephan"](m, f) for m in Mb])
    for c in CK:
        Hf = hcf(*c)["lvd"]; cold = np.array([(1 - FBN) * Hf(d)[0] for d in SAMP]); on = EP < cold
        RES[f"{f}|S|{ckey(c)}"]["switch"] = dict(max_Mb_on=float(Mb[on].max()) if on.any() else None, min_Mb_off=float(Mb[~on].min()) if (~on).any() else None)
        P(f"  f_ex switch (S) {ckey(c):18s}: f_ex > 0 up to M_b {Mb[on].max():.2e}; f_ex = 0 from M_b {Mb[~on].min():.2e} (edge phantom vs cold floor (1-f_b) M_cool)")
    Hf = hcf(0.59, "t50", 6000)["lvd"]
    for n in ("Eridanus II", "Draco", "Andromeda IX", "Andromeda V", "Bootes I", "Segue 1"):
        i = names.index(n); cold = (1 - FBN) * Hf(SAMP[i])[0]
        P(f"     {n:14s} M_V {MV[i]:6.2f}  M_b {Mb[i]:.2e}  edge phantom {EP[i]:.2e}  cold floor {cold:.2e}  f_ex {max(0.0, 1 - EP[i] / cold):.3f}  (mu0.59|t50|C6000)")
json.dump(RES, open(os.path.join(HERE, "cfg934_posthoc.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg934_posthoc.out"), "w").write("\n".join(OUT) + "\n")
