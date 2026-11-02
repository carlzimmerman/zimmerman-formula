#!/usr/bin/env python3
"""TG1 split stacks on data (FROZEN_CRITERIA.md). TG1_MUTATE=1 shuffles KT. kappa = 1/2 FITTED; not theory closed."""
from tg1_common import *
OUT = []; RES = {"mutate": MUT}; F0 = json.load(open(os.path.join(HERE, f"tg1_forecast{TAG}.json"))); CL = np.load(os.path.join(HERE, f"tg1_clouds{TAG}.npz")); NB = 2000
def P(s=""): print(s, flush=True); OUT.append(str(s))
def bal(C, y, w): return [float((w[h] * y[h]).sum() / w[h].sum() - (w[l] * y[l]).sum() / w[l].sum()) for h, l in C]
def boots(C, e, w, var, patch, key):
    rg = np.random.default_rng([SEED, key]); N = len(e); c = np.stack([np.bincount(r, minlength=N) for r in rg.integers(0, N, (NB, N))]).astype(float); sb = float(np.nanstd(split_w(C, e, w, var, c), ddof=1))
    J = np.array([split_w(C, e, w, var, (patch != q).astype(float)) for q in np.unique(patch)]); n = len(J); return sb, float(np.sqrt((n - 1) / n * np.nansum((J - np.nanmean(J)) ** 2)))
def stat(e, w, t, g, patch, key, s=None, z=None, lab=""):
    CT, CG = cells(g, t), cells(t, g); bT = float(split_w(CT, e, w, t)); bG = float(split_w(CG, e, w, g)); sbT, sjT = boots(CT, e, w, t, patch, key); sbG, sjG = boots(CG, e, w, g, patch, key + 1); o = dict(bT=bT, bG=bG, sbT=sbT, sjT=sjT, sbG=sbG, sjG=sjG)
    o["dt_T"] = bal(CT, t, w); o["dg_T"] = bal(CT, g, w); o["dg_G"] = bal(CG, g, w); o["dt_G"] = bal(CG, t, w); o["dz_T"] = bal(CT, z, w); o["dz_G"] = bal(CG, z, w)
    o["cellsT"] = [[float(e[h].sum() / w[h].sum()), float(e[l].sum() / w[l].sum())] for h, l in CT]; o["cellsG"] = [[float(e[h].sum() / w[h].sum()), float(e[l].sum() / w[l].sum())] for h, l in CG]
    if s is not None: o["sT"] = max(sbT, sjT, s[0]); o["sG"] = max(sbG, sjG, s[1]); o["ZT"] = bT / o["sT"]; o["ZG"] = bG / o["sG"]; o["zT"] = bT / s[0]; o["zG"] = bG / s[1]
    return o
def jointZ(e, w, cols, patch, key):
    th = joint(e, w, cols); rg = np.random.default_rng([SEED, key]); N = len(e); B = np.array([joint(e, w, cols, np.bincount(rg.integers(0, N, N), minlength=N).astype(float)) for _ in range(NB)]); J = np.array([joint(e, w, cols, (patch != q).astype(float)) for q in np.unique(patch)]); n = len(J); sb = B.std(0, ddof=1); sj = np.sqrt((n - 1) / n * ((J - J.mean(0)) ** 2).sum(0)); s_ = np.maximum(sb, sj); return th, s_
RES["cells"] = {}; key = 100
P("Band MID, f* 0.034. b per dex, M_sun/pc^2. Z = b / max(boot, jack, mock H0 sd). z = b / mock sd, the cloud's unit. p from the forecast's clouds.")
for f in FEET:
    for h in HS:
        S = sample(f, h); e = (S["n"] - S["V"]).sum(1); w = S["W"].sum(1); pr = F0["prim"][f"{f}|{h}"]; s = pr["s"]; key += 10; o = stat(e, w, S["t"], S["g"], S["PATCH"], key, s, S["z"])
        cl = {c: CL[f"{f}|{h}|{c}"] for c in ("H0", "HTz", "HGz")}; o["p_T_HG"] = float((np.abs(cl["HGz"][:, 0]) >= abs(o["zT"])).mean()); o["p_G_HT"] = float((np.abs(cl["HTz"][:, 1]) >= abs(o["zG"])).mean()); o["p_T_HT"] = float((np.abs(cl["HTz"][:, 0]) >= abs(o["zT"])).mean()); o["p_G_HG"] = float((np.abs(cl["HGz"][:, 1]) >= abs(o["zG"])).mean()); o["p_T_H0"] = float((np.abs(cl["H0"][:, 0]) >= abs(o["zT"])).mean()); o["p_G_H0"] = float((np.abs(cl["H0"][:, 1]) >= abs(o["zG"])).mean())
        mu = {c: cl[c].mean(0) for c in cl}; Ci = {c: np.linalg.inv(np.cov(cl[c].T)) for c in cl}; x = np.array([o["zT"], o["zG"]]); o["maha"] = {c: float((x - mu[c]) @ Ci[c] @ (x - mu[c])) for c in cl}; o["LR_T_over_G"] = float(np.exp(-.5 * (o["maha"]["HTz"] - o["maha"]["HGz"])) * np.sqrt(np.linalg.det(Ci["HTz"]) / np.linalg.det(Ci["HGz"])))
        one = np.ones(len(e)); th, se = jointZ(e, w, (one, S["t"], S["g"]), S["PATCH"], key + 2); thz, sez = jointZ(e, w, (one, S["t"], S["g"], S["z"] - S["z"].mean()), S["PATCH"], key + 3); o["joint"] = dict(bT=th[1], sT=se[1], bG=th[2], sG=se[2]); o["jointz"] = dict(bT=thz[1], sT=sez[1], bG=thz[2], sG=sez[2], bz=thz[3], sz=sez[3])
        # ratio row
        n = S["n"].sum(1); V = S["V"].sum(1); CT, CG = cells(S["g"], S["t"]), cells(S["t"], S["g"]); o["ratioT"] = [[float(n[a].sum() / V[a].sum()), float(n[b].sum() / V[b].sum())] for a, b in CT]; o["ratioG"] = [[float(n[a].sum() / V[a].sum()), float(n[b].sum() / V[b].sum())] for a, b in CG]
        # L300 row, gas proxy
        okL = np.isfinite(S["L300"]); o["L300"] = stat(e[okL], w[okL], S["t"][okL], S["L300"][okL], S["PATCH"][okL], key + 4, z=S["z"][okL]); q = o["L300"]; q["ZT"] = q["bT"] / max(q["sbT"], q["sjT"], s[0]); q["ZG"] = q["bG"] / max(q["sbG"], q["sjG"], s[1])
        RES["cells"][f"{f}|{h}"] = o
        P(f"\n{f} {h} N {len(e)}: b_T|g {o['bT']:+.1f} (boot {o['sbT']:.1f}, jack {o['sjT']:.1f}, mock {s[0]:.1f}) Z {o['ZT']:+.2f}; b_G|t {o['bG']:+.1f} (boot {o['sbG']:.1f}, jack {o['sjG']:.1f}, mock {s[1]:.1f}) Z {o['ZG']:+.2f}; margins to 3: {abs(o['ZT'])-3:+.2f}, {abs(o['ZG'])-3:+.2f}")
        P(f"  cells, T split, dDS hi/lo by gas bin: " + " | ".join(f"{a:.1f}/{b:.1f}" for a, b in o["cellsT"]) + f"; dt {np.round(o['dt_T'],3).tolist()}, dg {np.round(o['dg_T'],3).tolist()}, dz {np.round(o['dz_T'],3).tolist()}")
        P(f"  cells, G split, dDS hi/lo by T bin:   " + " | ".join(f"{a:.1f}/{b:.1f}" for a, b in o["cellsG"]) + f"; dg {np.round(o['dg_G'],3).tolist()}, dt {np.round(o['dt_G'],3).tolist()}, dz {np.round(o['dz_G'],3).tolist()}")
        P(f"  ratio n/V hi/lo: T split " + " | ".join(f"{a:.2f}/{b:.2f}" for a, b in o["ratioT"]) + "; G split " + " | ".join(f"{a:.2f}/{b:.2f}" for a, b in o["ratioG"]))
        P(f"  cloud z ({o['zT']:+.2f}, {o['zG']:+.2f}); HT mean {np.round(cl['HTz'].mean(0),2).tolist()}, HG mean {np.round(cl['HGz'].mean(0),2).tolist()}; p(T|HG) {o['p_T_HG']:.3f} p(G|HT) {o['p_G_HT']:.3f} p(T|HT) {o['p_T_HT']:.3f} p(G|HG) {o['p_G_HG']:.3f} p(T|H0) {o['p_T_H0']:.3f} p(G|H0) {o['p_G_H0']:.3f}; Mahalanobis H0 {o['maha']['H0']:.2f} HT {o['maha']['HTz']:.2f} HG {o['maha']['HGz']:.2f}; LR T/G {o['LR_T_over_G']:.2f}")
        P(f"  joint b_T {th[1]:+.1f}+-{se[1]:.1f} (Z {th[1]/se[1]:+.2f}) b_G {th[2]:+.1f}+-{se[2]:.1f} (Z {th[2]/se[2]:+.2f}); with lg(1+z): b_T {thz[1]:+.1f}+-{sez[1]:.1f} ({thz[1]/sez[1]:+.2f}) b_G {thz[2]:+.1f}+-{sez[2]:.1f} ({thz[2]/sez[2]:+.2f}) b_z {thz[3]:+.0f}+-{sez[3]:.0f}")
        P(f"  L300 gas proxy: b_T|L {q['bT']:+.1f} Z {q['ZT']:+.2f}; b_L|t {q['bG']:+.1f} Z {q['ZG']:+.2f}")
# K3
c = RES["cells"]["canonical|h0672"]; rT = abs(np.array(c["dg_T"])).sum() / abs(np.array(c["dt_T"])).sum(); rG = abs(np.array(c["dt_G"])).sum() / abs(np.array(c["dg_G"])).sum(); k3 = rT <= .5 and rG <= .5; P(f"\nK3 {'PASS' if k3 else 'FAIL'}: |dg|/|dt| in T split {rT:.3f}, |dt|/|dg| in G split {rG:.3f}; line 0.5"); RES["K3"] = bool(k3)
# bracket and band IM
RES["bracket"] = {}
for f in FEET:
    for fs, band, lab in (("0615", "MID", "f* 0.0615"), ("034", "IM", "band IM")):
        S = sample(f, "h0672", band, fs); e = (S["n"] - S["V"]).sum(1); w = S["W"].sum(1); key += 10; o = stat(e, w, S["t"], S["g"], S["PATCH"], key, z=S["z"]); o["ZTb"] = o["bT"] / max(o["sbT"], o["sjT"]); o["ZGb"] = o["bG"] / max(o["sbG"], o["sjG"]); RES["bracket"][f"{f}|{lab}"] = o; P(f"{lab} {f} h0672: b_T {o['bT']:+.1f} Z(no mock) {o['ZTb']:+.2f}; b_G {o['bG']:+.1f} Z(no mock) {o['ZGb']:+.2f}")
# verdict
RES["label"] = {}
for f in FEET:
    A = [RES["cells"][f"{f}|{h}"] for h in HS]; fl = F0["forecast_label"][f]; RES["label"][f] = fl if fl == "NOT SEPARABLE" else "UNDECIDED"; P(f"VERDICT {f}: {RES['label'][f]} (Z_T {A[0]['ZT']:+.2f}, {A[1]['ZT']:+.2f}; Z_G {A[0]['ZG']:+.2f}, {A[1]['ZG']:+.2f})")
    if fl != "NOT SEPARABLE": P("  separable branch not implemented: forecast did not reach it in the main run; MUTATE only")
open(os.path.join(HERE, f"tg1_split{TAG}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"tg1_split{TAG}.json"), "w"), indent=0, default=float)
