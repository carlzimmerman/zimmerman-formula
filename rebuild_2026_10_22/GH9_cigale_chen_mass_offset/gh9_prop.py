#!/usr/bin/env python3
"""GH9 propagation: rebuild GH7's gas model at log M* - Delta_j and re-grade GH8's ALL stack with the same lenses, velocities, R and weights."""
import os, json
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); M = json.load(open(os.path.join(HERE, "gh9_match.json")))
g7p, g8p = os.path.join(ROOT, "GH7_ksz_desi_centrals", "gh7_cap.py"), os.path.join(ROOT, "GH8_ksz_velocity_hardened", "gh8_mw.py")
N7 = {"__file__": g7p, "__name__": "gh7"}; exec(open(g7p).read().split("# real CAPs")[0], N7)
N8 = {"__file__": g8p, "__name__": "gh8"}; exec(open(g8p).read().split("Cc = {}")[0], N8); N8["Cc"] = {}
RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
C0 = N8["C_"]; L = N8["L_"]; z, good = L["z"], C0["good"]; iz7 = C0["iz"]; H = N7["H"]; lb = np.array([10.6, 10.7, 10.8, 10.9, 11.0]) + 2 * np.log10(.704 / H); ZC = [float(z[good & (iz7 == i)].mean()) for i in range(10)]; KS = N8["KS"]
def build(D, ks=KS):
    o = {}
    for k in ks:
        a = np.zeros((10, 4, 8))
        for i in range(10):
            for j in range(4): a[i, j] = N7["model_cap"](ZC[i], float((lb[j] + lb[j + 1]) / 2 - D[j]), float(k))
        o[k] = a
    return o
M0 = build(np.zeros(4)); d = max(float(np.max(np.abs(M0[k] - C0["m" + k]) / np.abs(C0["m" + k]).max())) for k in KS); check("K2a_model_rebuild", d < 1e-6, f"{d:.1e}")
Cd = dict(C0); N8["C_"] = Cd; sel = np.ones(N8["g"].sum(), bool); O, mod, Ci, w, T = N8["run"](sel, "ALL"); c, u, wt = N8["Cc"]["ALL"]; iz, il = N8["iz0"], N8["il0"]; Rs = N8["Rs"]; TCMB = N8["TCMB"]; est = N8["est"]; wu = np.sum(wt * (u * u)[:, None], axis=0)
rs = np.random.default_rng(828); NS = None
rng = np.random.default_rng(1828); NS = np.array([est(c, N8["shuf"](u, iz, rng), wt) for _ in range(2000)])
parts = np.array_split(np.argsort(N8["ra"]), 50); PJ = []
for p in parts:
    k_ = np.ones(len(u), bool); k_[p] = False; PJ.append(est(c[k_], u[k_], wt[k_]))
PJ = np.array(PJ); print("jackknife estimates done", flush=True)
def grade(MM, label):
    out = {}
    for n, R in Rs.items():
        mm = {k: np.sum(wt * MM[k][iz, il] * (u * u)[:, None], axis=0) / wu * TCMB * R for k in KS}; r = {}
        for k in KS:
            f = np.einsum("i,ij", mm[k], Ci) / np.einsum("i,ij,j", mm[k], Ci, mm[k]); js = PJ @ f; r[k] = dict(A=float(f @ T), s=float((NS @ f).std()), j=float(np.sqrt(49 / 50 * np.sum((js - js.mean()) ** 2))))
        e = max(r["1.8"]["s"], r["1.8"]["j"]); a1 = r["1.0"]; bel = r["1.8"]["A"] + 2 * e < 1; every = bel and a1["A"] + 2 * a1["s"] < 1
        out[n] = dict(r, below=bool(bel), every=bool(every), upper=r["1.8"]["A"] + 2 * e)
        print(f"  {label} R {n}: " + "; ".join(f"A({k}) {r[k]['A']:+.3f}+-{r[k]['s']:.3f}/j{r[k]['j']:.3f}" for k in KS) + f"; A(1.8)+2e {out[n]['upper']:.3f} BELOW {bel} every-extent {every}", flush=True)
    return out
Dj = np.array(M["Dj"]); RES["D0"] = grade(M0, "D=0"); a8 = json.load(open(os.path.join(ROOT, "GH8_ksz_velocity_hardened", "gh8_mw.json")))["ALL"]["A_1.8_fm"]["A"]; d = abs(RES["D0"]["fm"]["1.8"]["A"] - a8); check("K2b_reproduce_GH8", d < 1e-3, f"{RES['D0']['fm']['1.8']['A']:.4f} vs {a8:.4f}")
for lab, D in (("D1", Dj), ("D2", Dj + .04), ("D3", Dj + M["dD3"])):
    RES[lab] = dict(D=D.tolist(), grade=grade(build(D), lab))
sc = []
for dd in (.05, .1, .15, .2, .25, .3):
    g = grade(build(np.full(4, dd), ("1.0", "1.8", "3.0")), f"const {dd}"); sc.append((dd, g["fm"]["upper"]))
RES["scan"] = sc; xs, ys = np.array(sc).T; RES["break_even"] = float(np.interp(1.0, ys, xs)) if ys.max() >= 1 and ys.min() <= 1 else None; print("break-even constant Delta (CIGALE high)", RES["break_even"], "scan", np.round(ys, 3), flush=True)
fl = -u; d = float(np.max(np.abs(est(c, fl, wt) + T))); check("MUTATE_flip", d < 1e-9, f"{d:.1e}")
b = [all(RES[l]["grade"][n]["below"] for n in Rs) for l in ("D1", "D2", "D3")]; RES["class"] = "SURVIVES MASS SCALE" if all(b) else ("REMOVED BY MASS SCALE" if not b[0] else "PARTLY LIMITED"); RES["every_extent_D1"] = {n: RES["D1"]["grade"][n]["every"] for n in Rs}; print("CLASS", RES["class"], b, "every-extent D1", RES["every_extent_D1"], flush=True)
json.dump(RES, open(os.path.join(HERE, "gh9_prop.json"), "w"), indent=1, sort_keys=True)
