#!/usr/bin/env python3
"""X77 AMENDMENT A1 (post-result, reported only): hot-CGM profile cut at k R_vir; m_CGM(k) and the k giving the X76 needs.
kappa = 1/2 FITTED; not theory closed.      python3 x77_cut_profile.py
"""
import os, sys, json, math
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = ["x"]; src = open(os.path.join(HERE, "x77_cgm.py")).read(); src = src[:src.index('P("X77_cgm_budget  criteria')]
    G = {"__file__": os.path.join(HERE, "x77_cgm.py"), "__name__": "x77_ro"}; exec(compile(src, "x77_cgm.py", "exec"), G)
XP, BINS, NEED, shape_mass, cold, Z = G["XP"], G["BINS"], G["NEED"], G["shape_mass"], G["cold"], G["Z_TA"]
OUT = []; RES = {"amendment": "A1 post-result reported only", "bins": {}}
def m_cut(b, fb, beta, k):
    Ms, Mc = b["Ms"], cold(b["Ms"]); M0 = Ms + Mc + 0.5 * Ms; Mhv = fb * b["Mvir"] - Ms
    norm = Mhv / shape_mass(b["Rvir"], beta, b["rc"]); rcut = k * b["Rvir"]
    Mh = lambda r: norm * shape_mass(min(r, rcut), beta, b["rc"])
    rta = math.exp(brentq(lambda lr: math.log(XP.rta_pc(Ms + Mc + Mh(math.exp(lr)), Z)) - lr, math.log(1e4), math.log(1e8), xtol=1e-12))
    return math.log10((Ms + Mc + Mh(rta)) / M0), rta / 1e3
for name, b in BINS.items():
    rows = {}
    for lab, (fb, be) in {"central": (b["fb"], b["beta"]), "generous": (b["fb"] + b["sfb"], b["beta"] - b["bm"]), "tight": (max(b["fb"] - b["sfb"], 1e-3), b["beta"] + b["bp"])}.items():
        if fb * b["Mvir"] <= b["Ms"]: continue
        grid = {k: m_cut(b, fb, be, k) for k in (1, 2, 3, 5, 8)}
        need_k = {}
        for t, mv in NEED.items():
            try: need_k[t] = brentq(lambda k: m_cut(b, fb, be, k)[0] - mv, 0.2, 60)
            except ValueError: need_k[t] = None
        rows[lab] = dict(m_of_k={k: v[0] for k, v in grid.items()}, rta_kpc_of_k={k: v[1] for k, v in grid.items()}, k_needed=need_k)
        s = f"[{name} {lab:8s}] m(k=1,2,3,5,8) " + " ".join(f"{grid[k][0]:+.2f}" for k in grid) + "; k for sat +1.25 / lens +0.85: " + " / ".join("—" if need_k[t] is None else f"{need_k[t]:.2f}" for t in ("sat", "lens"))
        print(s); OUT.append(s)
    RES["bins"][name] = rows
json.dump(RES, open(os.path.join(HERE, "x77_cut_profile_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "x77_cut_profile.out"), "w").write("\n".join(OUT) + "\n")
