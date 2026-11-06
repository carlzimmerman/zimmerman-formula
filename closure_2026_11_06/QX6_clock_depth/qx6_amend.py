#!/usr/bin/env python3
"""QX6 amendments A1/A2 (AMENDMENTS.md 03f80829fc, POST-RESULT). Writes qx6_amend.json / .out.
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
Q5 = os.path.join(REPO, "closure_2026_11_06", "QX5_cluster_terms", "qx5.py"); src = open(Q5).read()
argv0, sys.argv = sys.argv, [Q5]; os.environ.pop("QX5_GCUT", None)
NS = {"__file__": Q5, "__name__": "qx5_reused"}; exec(compile(src[:src.index("DIR = dict(")], Q5, "exec"), NS); sys.argv = argv0
G, MS, KPC, A0, glaw, XC, tables = (NS[k] for k in ("G", "MS", "KPC", "A0", "glaw", "XC", "tables"))
def mlaw(Mb, r, a0): rm = r * KPC; return glaw(G * Mb * MS / rm ** 2, a0) * rm ** 2 / G / MS
RES = dict(tag="qx6_amend", amendments="03f80829fc", note="POST-RESULT; kappa = 1/2 FITTED; not theory closed")
for f, a0 in A0.items():
    T = tables("a", a0, False)
    d0 = np.array([math.log10(z["M_obs"] / mlaw(z["M_b"], z["r_kpc"], a0)) for z in XC])
    d = np.array([math.log10(z["M_obs"] / mlaw(z["M_b"], z["r_kpc"], a0 * (1 + 2.1e5 * x["k"]))) for z, x in zip(XC, T["X"])])
    a1 = dict(shift=float(d.mean() - d0.mean()), bites=bool(d.mean() - d0.mean() <= -0.2))
    kg = max([c["k"] for c in T["C"]] + [e["k"] for e in T["E"]] + [l["k"] for l in T["L"]]); kxs = np.array([x["k"] for x in T["X"]])
    kts = np.concatenate([np.geomspace(kg * 1.0001, kxs.min(), 60), np.sort(kxs)])
    Ml = np.array([x["M_law"] for x in T["X"]]); Mb = np.array([x["M_b"] for x in T["X"]]); Mo = np.array([x["M_obs"] for x in T["X"]])
    best = None; npass = 0
    for kt in kts:
        on = kxs >= kt
        for A in np.arange(1.0, 10.0001, 0.01):
            dd = np.log10(Mo / (Mb + np.where(on, A, 1.0) * (Ml - Mb))); m, r = dd.mean(), math.sqrt((dd ** 2).mean())
            if abs(m) <= 0.05 and r <= 0.10: npass += 1
            if best is None or r < best[2]: best = (kt, A, r, m)
    RES[f] = dict(A1=a1, A2=dict(n_pass=npass, best=dict(k_t=best[0], A=best[1], rms=best[2], mean=best[3]), n_kt=len(kts)))
    P(f"[{f}] A1: x1e5 control shift {a1['shift']:+.3f} -> bites {a1['bites']}")
    P(f"[{f}] A2: single-step (A, k_t) passing G-X: {npass}; minimum rms {best[2]:.4f} at k_t {best[0]:.3e}, A {best[1]:.2f} (mean {best[3]:+.3f})")
json.dump(RES, open(os.path.join(HERE, "qx6_amend.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "qx6_amend.out"), "w").write("\n".join(OUT) + "\n")
