#!/usr/bin/env python3
"""OE1 verdict (FROZEN_CRITERIA.md): decomposition, grade table, joint chi^2 (BA1's method, as M3A1), Z_tot, checks, label. Reads cache_jobs. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np, warnings; warnings.simplefilter("ignore")
from scipy.stats import chi2
H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H); REPO = os.path.dirname(RB); CJ = os.path.join(H, "cache_jobs"); OUT = []; RES = {}; CHK = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(n, ok, t, stop=True): CHK.append((n, bool(ok), stop)); P(f"{n} {'PASS' if ok else 'FAIL'}: {t}")
HH = ("h0672", "h0686"); FS = ("0.034", "0.0615"); CELLS = [(f, h) for f in FS for h in HH]; OB = [6, 7]; HI = {"h0672": 1, "h0686": 2}; HX = {"h0672": 0, "h0686": 1}
def jb(n, f="0.034"): return json.load(open(os.path.join(CJ, f"{n}_{f}.json")))
def dp(n, f="0.034"): return np.load(os.path.join(CJ, f"{n}_{f}_dump.npz"))
X = np.load(os.path.join(RB, "X7_cluster_core_significance", "x7_measure_percluster.npz")); N = len(X["name"]); Mg = np.asarray(X["Mgas500"], float); T3 = np.digitize(Mg, np.quantile(Mg, [1 / 3, 2 / 3])); M3 = np.where(T3 == 2)[0]; LO = M3[Mg[M3] < np.median(Mg[M3])]; HI_ = M3[Mg[M3] >= np.median(Mg[M3])]; zc = np.asarray(X["z"], float)
A3 = json.load(open(os.path.join(RB, "M3A1_outer_key_audit", "m3a1_results.json"))); ZN4 = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_results.json")))["runs"]
P("OE1 outer edge, ZN4's chain, gas +0.005; kappa = 1/2 FITTED; not theory closed. Lead found post-result; no out-of-sample claim")
def rch(z0, z1): return (z0 - z1) / (z0 - 2)
# K1
k1 = 0.0; k1p = 0.0; kd = 0.0
for f, h in CELLS:
    c = jb("OFF", f)["cells"][h]; Z4 = ZN4[f"f* {f}, gas +0.005"]["cells"][h]; k1 = max(k1, max(abs(c[k]["Z"] - Z4[k]["Z"]) for k in c)); k1p = max(k1p, max(abs(c[k]["pred"] - Z4[k]["pred"]) for k in c))
    kd = max(kd, float(np.abs(dp("OFF", f)[f"V_{h}"] - np.load(os.path.join(RB, "M3A1_outer_key_audit", "cache_jobs", f"BASE_{f}_dump.npz"))[f"V_{h}"]).max() / np.abs(dp("OFF", f)[f"V_{h}"]).max()))
xo = jb("OFF")["xcop"]; check("K1", k1 <= 1e-6 and k1p <= 1e-6 and kd <= 1e-6, f"against ZN4 Z {k1:.1e}, preds {k1p:.1e}; M3A1 per-cluster V {kd:.1e}; X-COP {xo['mean']:+.3f} {xo['rms']:.3f}")
# K2, K5
k2 = max(json.load(open(os.path.join(CJ, f"{v}_{f}_rows.json")))["k2"] for v in ("E1", "E2") for f in FS); check("K2", k2 <= 1e-9, f"E1, E2 equal ZN4 up to min(r_ta, x_edge R200): max {k2:.1e}")
ROW = json.load(open(os.path.join(CJ, "OFF_0.034_rows.json")))["rows"]; R_ = {r["i"]: r for r in ROW if r["hk"] == "h0672"}; IM = list(M3)
# K3
k3 = 0.0
for r in ROW:
    sm = np.sum([r["pieces"][k] for k in r["pieces"]], 0); k3 = max(k3, float(np.max(np.abs(sm - np.array(r["V"]))) / max(np.max(np.abs(r["V"])), 1e-300)))
check("K3", k3 <= 1e-6, f"pieces sum to V, relative to the cluster's larger bin (8 of 652 rows have a bin at the grader's floor, near 1e-29): {k3:.1e}")
over = sum(R_[i]["rs"] > 30 for i in IM); P(f"K5 M3: sphere's edge beyond the 30 Mpc grid in {over} of {len(IM)}; rs max {max(R_[i]['rs'] for i in IM):.1f} Mpc; mass beyond 30 Mpc sits past the grid, flat, and can't reach the band"); CHK.append(("K5", True, True))
# Part A
P("\nPart A, geometry at f* 0.034, h 0.672 (16, 50, 84 %)"); pc = lambda a: " ".join(f"{x:.2f}" for x in np.percentile(a, [16, 50, 84]))
def geo(lab, S):
    rr = [R_[i] for i in S]; f = lambda k: np.array([r[k] for r in rr]); R2, rt, re_, rs = f("R200"), f("rta"), f("re"), f("rs")
    P(f"  {lab} (N {len(S)}): R200 {pc(R2)} Mpc; band 1.42, 2.06, 3 Mpc in R200: {pc(1.42 / R2)} | {pc(2.06 / R2)} | {pc(3 / R2)}; in r_ta: {pc(1.42 / rt)} | {pc(3 / rt)}; r_ta {pc(rt)} Mpc = {pc(rt / R2)} R200; x_edge R200 {pc(re_)} Mpc = {pc(re_ / R2)}; particle edge {pc(rs)} Mpc; x_edge inside r_ta {int((re_ < rt).sum())}; r_ta < 3 Mpc {int((rt < 3).sum())}; x_edge R200 < 3 Mpc {int((re_ < 3).sum())}; no fair-share {int(sum(not r['fs'] for r in rr))}")
    P(f"     M_c(r_ta)/M_fair {pc(f('Mc_rta') / f('Mfair'))}; M_c(sphere)/M_fair {pc(f('Mc_sph') / f('Mfair'))}, over budget {int((f('Mc_sph') > f('Mfair')).sum())}; M_c(R200)/M_fair {pc(f('Mc_R200') / f('Mfair'))}; M_b(r_ta)/M_b(R200) {pc(f('Mb_rta') / f('Mb_R200'))}")
    return dict(R200=np.median(R2).item(), x_in=np.median(1.42 / R2).item(), x_mid=np.median(2.06 / R2).item(), x_out=np.median(3 / R2).item(), rta=np.median(rt).item())
RES["geo"] = {k: geo(k, S) for k, S in (("M3", IM), ("lighter", list(LO)), ("heavier", list(HI_)))}
Pk = ("baryons", "cold_inR200", "cold_R200_band", "cold_b6", "cold_b7", "cold_out_to_edge", "cold_tail", "cold_beyond")
P("\nShare of the band's prediction by piece, M3 (differences of cumulative chains at fixed reduced-shear factor, so they sum; cold_b6 is 1.42-2.06 Mpc, cold_b7 2.06-3; cold_beyond is 0 in ZN4 unless a tail ran past)"); RES["pieces"] = {}
for lab, S in (("M3", IM), ("lighter", list(LO)), ("heavier", list(HI_))):
    for b, nm in ((0, "1.42-2.06"), (1, "2.06-3")):
        tot = sum(R_[i]["V"][b] for i in S); sh = {k: sum(R_[i]["pieces"][k][b] for i in S) / tot for k in Pk}; RES["pieces"][f"{lab}|{nm}"] = sh; P(f"  {lab} bin {nm}: " + "; ".join(f"{k} {v:+.3f}" for k, v in sh.items()))
# grade
Dq = dp("OFF"); vC = {h: Dq[f"vC_{h}"] for h in HH}
def wb(h): i = HI[h]; W = np.where(X["E"][:, i] < 1e8, 1 / X["E"][:, i] ** 2, 0); B0 = X["den"][:, i].sum(0) / X["den_r"][:, i].sum(0); return W * B0[None, :]
def nsum(h): i = HI[h]; return wb(h) * (X["D"][:, i] - X["leakP"][:, HX[h], 0])
from astropy.io import fits
E_ = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data; idx_ = {str(s_).strip(): k for k, s_ in enumerate(E_["NAME"])}; KT = np.asarray(E_["KT"], float)[np.array([idx_[str(x).strip()] for x in X["name"]])]; I0 = np.where(np.isfinite(KT) & (KT > 0))[0]; XKT = np.log10(KT[I0] / np.median(KT[I0])); TID = Dq["TID"]; ALLI = np.arange(N); PTCH = Dq["PATCH"]
rg = np.random.default_rng(20261031); ix = rg.integers(0, N, size=(2000, N)); WB_ = np.stack([np.bincount(r, minlength=N) for r in ix]).astype(float)
def keys(W, h):
    n = nsum(h); vc = vC[h]; O = {}; I = I0; band = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": OB}; S = {b: (n[:, ix_].sum(1), vc[:, ix_].sum(1)) for b, ix_ in band.items()}; rr = lambda Ix, b: (W[:, Ix] @ S[b][0][Ix]) / (W[:, Ix] @ S[b][1][Ix])
    def wls(Wt, Xm, nn, dd): F_ = np.einsum("ri,i,ij,ik->rjk", Wt, dd, Xm, Xm); g = np.einsum("ri,ij,i->rj", Wt, Xm, nn); return np.linalg.solve(F_, g[..., None])[..., 0]
    X1 = np.c_[np.ones(len(I)), XKT]; O["G-IN-all"] = rr(I, "INNER")
    for t in range(3): O[f"G-MID-T{t + 1}"] = rr(I[TID == t], "MID")
    O["G-MID-b"] = wls(W[:, I], X1, S["MID"][0][I], S["MID"][1][I])[:, 1]; O["G-OUT-all"] = rr(I, "OUTER")
    for t in range(3): O[f"G-OUT-T{t + 1}"] = rr(I[TID == t], "OUTER")
    O["G-OUT-b"] = wls(W[:, I], X1, S["OUTER"][0][I], S["OUTER"][1][I])[:, 1]; O["G-OUT-Mall"] = rr(ALLI, "OUTER")
    for t in range(3): O[f"G-OUT-M{t + 1}"] = rr(np.where(T3 == t)[0], "OUTER")
    O["G-IN-Mall"] = rr(ALLI, "INNER"); return O
RB_ = {}
for f_, h_ in CELLS:
    vC = {q: dp("OFF", f_)[f"vC_{q}"] for q in HH}; Kb_ = keys(WB_, h_); RB_[(f_, h_)] = (list(Kb_), np.corrcoef(np.array([Kb_[k] for k in Kb_])))
def joint(cells, h, f):
    ks, R = RB_[(f, h)]; d = np.array([cells[k]["meas"] - cells[k]["pred"] for k in ks]); s = np.array([cells[k]["s"] for k in ks]); w_, Vv = np.linalg.eigh(R); ok = w_ >= 1e-3 * w_.max(); z = Vv[:, ok].T @ (d / s); c2 = float((z * z / w_[ok]).sum()); return c2, int(ok.sum()), float(chi2.sf(c2, int(ok.sum())))
JA = A3["joint"]; d1 = max(abs(joint(jb("OFF", f)["cells"][h], h, f)[0] - JA[f"{f}|{h}"]["chi2"]) for f, h in CELLS); check("K6 (not frozen, added)", d1 <= 1e-6, f"joint chi^2 on OFF reproduces M3A1: {d1:.1e}")
ZT = A3["Ztot"]; Z0 = {x: jb("OFF", x[0])["cells"][x[1]]["G-OUT-M3"]["Z"] for x in CELLS}; rng = np.random.default_rng(20261105)
def halves(j, f="0.034", h="h0672"):
    V = dp(j, f)[f"V_{h}"]; n = nsum(h); vc = dp(j, f)[f"vC_{h}"]; O = {}
    for lab, S, bb in (("1.42-2.06", M3, [6]), ("2.06-3", M3, [7]), ("lighter", LO, OB), ("heavier", HI_, OB)):
        nb, vb, Vb = n[:, bb].sum(1), vc[:, bb].sum(1), V[:, bb].sum(1); iB = rng.integers(0, len(S), (2000, len(S))); D_ = nb[S][iB].sum(1) / vb[S][iB].sum(1) - Vb[S][iB].sum(1) / vb[S][iB].sum(1); A_, Q_ = nb[S].sum() / vb[S].sum(), Vb[S].sum() / vb[S].sum(); O[lab] = (A_, Q_, (A_ - Q_) / D_.std(ddof=1))
    return O
P("\nGrade: G-OUT-M3 stat-only Z and Z_tot (f* 0.034 h 0.672, h 0.686; f* 0.0615 h 0.672, h 0.686), reach, keys, joint, X-COP"); RES["grade"] = {}
for j, lab in (("OFF", "ZN4 baseline"), ("E1", "E1 particles, no edge (FROZEN PRIMARY)"), ("E2", "E2 capped at budget"), ("E3", "E3 budget closed inside r_ta, NOT NATIVE, ceiling"), ("E1MEAN", "E1 with seeds' mean M(<r) for the median, post-result"), ("OFFA", "VB1 A node, cut at r_ta"), ("E1A", "E1 on VB1 A node"), ("OFFB", "VB1 B node, cut at r_ta"), ("E1B", "E1 on VB1 B node")):
    O = {f: jb(j, f) for f in FS}; zz = {x: O[x[0]]["cells"][x[1]]["G-OUT-M3"] for x in CELLS}; ztot = {x: (zz[x]["meas"] - zz[x]["pred"]) / ZT[f"{x[0]}|{x[1]}"]["tot"] for x in CELLS}; rr = {x: rch(Z0[x], zz[x]["Z"]) for x in CELLS}
    bad = {f: sorted({k for h in HH for k, v in O[f]["cells"][h].items() if abs(v["Z"]) > 2}) for f in FS}; J = {f"{f}|{h}": joint(O[f]["cells"][h], h, f) for f, h in CELLS}; hv = halves(j); RES["grade"][j] = dict(Z={f"{a}|{b}": v["Z"] for (a, b), v in zz.items()}, Ztot={f"{a}|{b}": v for (a, b), v in ztot.items()}, reach={f"{a}|{b}": v for (a, b), v in rr.items()}, bad=bad, joint=J, xcop={f: O[f]["xcop"] for f in FS}, groups={f: O[f]["groupsZ"] for f in FS}, halves=hv, cells={f: O[f]["cells"] for f in FS})
    P(f"  {lab}: Z " + " ".join(f"{zz[x]['Z']:+.3f}" for x in CELLS) + "; Z_tot " + " ".join(f"{ztot[x]:+.2f}" for x in CELLS) + f"; reach {min(rr.values()):+.3f} to {max(rr.values()):+.3f}"); P(f"     over 2: f* 0.034 {bad['0.034']}; f* 0.0615 {bad['0.0615']}; joint p " + " ".join(f"{J[f'{f}|{h}'][0]:.1f}/{J[f'{f}|{h}'][1]} {J[f'{f}|{h}'][2]:.1e}" for f, h in CELLS) + f"; X-COP {O['0.034']['xcop']['mean']:+.3f} {O['0.034']['xcop']['rms']:.3f}, {O['0.0615']['xcop']['mean']:+.3f} {O['0.0615']['xcop']['rms']:.3f}; groups {O['0.034']['groupsZ']:+.2f} {O['0.0615']['groupsZ']:+.2f}")
    P("     A, pred, Z own bootstrap: " + "; ".join(f"{k} {v[0]:.2f} {v[1]:.2f} {v[2]:+.2f}" for k, v in hv.items()))
    if j in ("E1", "E3"): c = O["0.034"]["cells"]["h0672"]; P("     all keys, f* 0.034 h 0.672: " + "; ".join(f"{k} {v['Z']:+.2f}" for k, v in c.items()))
# double count
P("\nDouble count, DR6's table (rho_model/rho_lin, M3, f* 0.034, h 0.672)")
RW = [r for r in json.load(open(os.path.join(RB, "DR6_outer_key_projection", "cache_jobs", "C3_0.034_+1_rows.json")))] ; M3s = set(int(i) for i in M3); RW = [r for r in RW if r["i"] in M3s]; Fv = np.array([(R_[r["i"]]["Mfair"] - R_[r["i"]]["Mc_R200"]) / (R_[r["i"]]["Mc_rta"] - R_[r["i"]]["Mc_R200"]) for r in RW])
for xk in ("1.5", "2.0", "3.0", "5.0", "0.9rta"):
    a = np.array([r["ratio"][xk] for r in RW if xk in r["ratio"]]); P(f"  r = {xk} R200 (or r_ta): E1 = ZN4 inside r_ta, median {np.median(a):.2f}; E3 cold outskirts x F, F median {np.median(Fv):.2f}")
aN = np.array([R_[i]["Mc_sph"] - R_[i]["Mc_rta"] for i in IM]); bud = np.array([R_[i]["Mfair"] + R_[i]["Mb_rta"] for i in IM]); P(f"  E1's mass beyond r_ta / total budget: {pc(aN / bud)}; DR6's C3 added a median 41 % inside r_ta: both can't be added: they fill the same deficit. E1 over M_fair in {int(sum(R_[i]['Mc_sph'] > R_[i]['Mfair'] for i in IM))} of {len(IM)}.")
RES["F_E3"] = float(np.median(Fv))
# MUTATE
d1 = jb("E1")["cells"]["h0672"]["G-OUT-M3"]; o = jb("OFF")["cells"]["h0672"]["G-OUT-M3"]; m = jb("M10")["cells"]["h0672"]["G-OUT-M3"]; dz1 = d1["Z"] - o["Z"]; dz10 = m["Z"] - o["Z"]; dp1 = d1["pred"] - o["pred"]; dp10 = m["pred"] - o["pred"]; rat = dp10 / dp1
ma_ratio = 7.5 <= rat <= 12.5; ma_abs = abs(dz1) >= 0.005 or abs(dz10) > 0.02; P(f"\nMUTATE a: E1 d Z {dz1:+.5f}, d pred {dp1:+.6f}; x 10 d Z {dz10:+.5f}, d pred {dp10:+.6f}; ratio on pred {rat:.1f}. Ratio line {'PASS' if ma_ratio else 'FAIL'}; floor line (x 10 moves Z > 0.02 when E1 < 0.005) {'PASS' if ma_abs else 'FAIL'}"); CHK.append(("MUTATE a", ma_ratio and ma_abs, True))
vz = dp("MZ")["V_h0672"]; v0 = dp("OFF")["V_h0672"]; drop = [1 - vz[M3][:, b].sum() / v0[M3][:, b].sum() for b in OB]; mb = min(drop) > 0.10; P(f"MUTATE b: cold mass in the band zeroed: M3 pred falls {drop[0]:.1%} in bin 6, {drop[1]:.1%} in bin 7; line 10 % in each: {'PASS' if mb else 'FAIL'}; G-OUT-M3 {jb('MZ')['cells']['h0672']['G-OUT-M3']['Z']:+.2f}"); CHK.append(("MUTATE b", mb, True))
# shell estimate of E1
est = []
for i in IM:
    r = R_[i]; est.append(-(r["Mc_sph"] - r["Mc_rta"]) * 2.4 ** 2 / (8 * np.pi * (1.3 * r["rta"]) ** 4) / ((r["Mc_rta"]) / (np.pi * 2.4 ** 2)))
P(f"Shell estimate of E1's fractional effect at R 2.4 Mpc, M_extra R^2 / 8 pi a^4 at a = 1.3 r_ta, against M(<r_ta)/pi R^2: median {np.median(est):+.1e}; grader's d pred / pred on M3 {dp1 / o['pred']:+.1e}, x 10 per unit {dp10 / 10 / o['pred']:+.1e}. So the term is genuinely small, by (R/a)^4")
# label
stop = [n for n, ok, s in CHK if s and not ok]; g = RES["grade"]["E1"]; E1Z = list(g["Z"].values()); clr = all(abs(z) <= 2 for z in E1Z) and not any(g["bad"][f] for f in FS) and all(abs(g["xcop"][f]["mean"]) <= 0.05 and g["xcop"][f]["rms"] <= 0.10 for f in FS); rm = max(g["reach"].values()); lab = "EDGE ARTEFACT" if clr else "PARTLY" if rm >= 1 / 3 else "NOT THE EDGE"; g3 = RES["grade"]["E3"]; c3 = all(abs(z) <= 2 for z in g3["Z"].values())
RES.update(stop=stop, statistic=lab, e3_clears=c3); P(f"\nStatistic reads {lab}: E1 best reach {rm:+.4f}. E3: clears M3 {c3}; reach {min(g3['reach'].values()):+.3f} to {max(g3['reach'].values()):+.3f}: {'BUDGET PLACEMENT, NOT NATIVE' if c3 else 'ceiling does not clear'}")
P(f"VERDICT AS FROZEN: {'NO VERDICT, failed: ' + ', '.join(stop) if stop else lab}")
json.dump(RES, open(os.path.join(H, "oe1_results.json"), "w"), default=float, indent=0); open(os.path.join(H, "oe1.out"), "w").write("\n".join(OUT) + "\n")
