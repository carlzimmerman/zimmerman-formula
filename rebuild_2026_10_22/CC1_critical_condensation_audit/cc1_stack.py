#!/usr/bin/env python3
"""CC1 part C: GH8 stack on the cached part of the type-corrected bin, GH9's model at type offsets."""
import os, json
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); M = json.load(open(os.path.join(ROOT, "GH9_cigale_chen_mass_offset", "gh9_match.json")))
g7p, g8p = os.path.join(ROOT, "GH7_ksz_desi_centrals", "gh7_cap.py"), os.path.join(ROOT, "GH8_ksz_velocity_hardened", "gh8_mw.py")
N7 = {"__file__": g7p, "__name__": "gh7"}; exec(open(g7p).read().split("# real CAPs")[0], N7)
N8 = {"__file__": g8p, "__name__": "gh8"}; exec(open(g8p).read().split("Cc = {}")[0], N8); N8["Cc"] = {}
C0 = N8["C_"]; L = N8["L_"]; z, good = L["z"], C0["good"]; iz7 = C0["iz"]; H = N7["H"]; lb = np.array([10.6, 10.7, 10.8, 10.9, 11.0]) + 2 * np.log10(.704 / H); ZC = [float(z[good & (iz7 == i)].mean()) for i in range(10)]; KS = N8["KS"]; Rs = N8["Rs"]; TCMB = N8["TCMB"]; est = N8["est"]; RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
def build(D):
    o = {}
    for k in KS:
        a = np.zeros((10, 4, 8))
        for i in range(10):
            for j in range(4): a[i, j] = N7["model_cap"](ZC[i], float((lb[j] + lb[j + 1]) / 2 - D[j]), float(k))
        o[k] = a
    return o
lm8 = L["lm"][N8["g"]]; ss = N8["ss"]; pas = ss < -11; iz0, il0, ra0 = N8["iz0"], N8["il0"], N8["ra"]
def stack(sel, lab, Mfun, nsh=2200):
    O, mod, Ci, w, T = N8["run"](sel, lab, nsh); c, u, wt = N8["Cc"][lab]; iz, il = iz0[sel], il0[sel]; wu = np.sum(wt * (u * u)[:, None], axis=0); r = np.random.default_rng(1828)
    NS = np.array([est(c, N8["shuf"](u, iz, r), wt) for _ in range(2000)]); PJ = []
    for p in np.array_split(np.argsort(ra0[sel]), 50):
        k_ = np.ones(len(u), bool); k_[p] = False; PJ.append(est(c[k_], u[k_], wt[k_]))
    PJ = np.array(PJ); out = dict(N=int(sel.sum()), That=T.tolist(), null_chi2=float(T @ Ci @ T), flip=float(np.max(np.abs(est(c, -u, wt) + T))))
    for n, R in Rs.items():
        out[n] = {}
        for k in KS:
            mm = np.sum(wt * Mfun(k, iz, il, sel) * (u * u)[:, None], axis=0) / wu * TCMB * R; f = np.einsum("i,ij", mm, Ci) / np.einsum("i,ij,j", mm, Ci, mm); js = PJ @ f
            s = float((NS @ f).std()); j = float(np.sqrt(49 / 50 * np.sum((js - js.mean()) ** 2))); out[n][k] = dict(A=float(f @ T), s=s, j=j, e=max(s, j))
    return out
Dj = np.array(M["Dj"]); D1 = build(Dj); allS = np.ones(len(lm8), bool); W = stack(allS, "ALLK1", lambda k, iz, il, s: D1[k][iz, il]); a = W["fm"]["1.8"]["A"]; check("K1_GH9_D1", abs(a - .2372) < 1e-3, f"{a:.4f}"); check("K2_flip", W["flip"] < 1e-9, f"{W['flip']:.1e}")
RES["whole_sample_D1"] = W
Mp, Ms = build(np.full(4, -.14)), build(np.full(4, -.31)); corr = lm8 + np.where(pas, .14, .31); sel = (corr >= 10.5) & (corr < 11.0)
print("selected", int(sel.sum()), "passive", int((sel & pas).sum()), "sf", int((sel & ~pas).sum()), "lm max p", float(lm8[sel & pas].max()), "s", float(lm8[sel & ~pas].max()), flush=True)
def Mf(k, iz, il, s):
    return np.where(pas[s][:, None], Mp[k][iz, il], Ms[k][iz, il])
O = stack(sel, "CORR", Mf); RES["corrected"] = O; ctrl, sc = .58, .14; RES["tiers"] = {}
for n in Rs:
    t = {}
    for k in KS:
        A, e = O[n][k]["A"], O[n][k]["e"]; t3s = abs(A / ctrl) * np.hypot(e / A if A else 0, sc / ctrl); t[k] = dict(T1=(A, e, A + 1.96 * e), T2=(A * 264 / 194, e * 264 / 194, (A + 1.96 * e) * 264 / 194), T3=(A / ctrl, t3s, A / ctrl + 1.96 * t3s))
    RES["tiers"][n] = t; print(n, {k: {q: [round(float(x), 3) for x in v] for q, v in t[k].items()} for k in KS}, flush=True)
RES["class"] = {n: ("EXTENDED GAS BELOW NEED" if RES["tiers"][n]["1.8"]["T1"][2] < 1 and RES["tiers"][n]["1.8"]["T2"][2] < 1 else "NOT BELOW") for n in Rs}; RES["extent_lock"] = {n: RES["tiers"][n]["1.0"]["T1"][2] < 1 for n in Rs}; print("CLASS", RES["class"], "A(1)+1.96e<1", RES["extent_lock"], flush=True)
json.dump(RES, open(os.path.join(HERE, "cc1_stack.json"), "w"), indent=1, sort_keys=True, default=float)
