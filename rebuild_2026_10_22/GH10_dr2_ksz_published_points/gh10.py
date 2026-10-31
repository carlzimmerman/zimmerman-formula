#!/usr/bin/env python3
"""GH10: Zhang's gas against DESI DR2 x ACT DR6 published kSZ points, differential bin from nested thresholds."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); EXT = os.path.join(os.path.dirname(os.path.dirname(ROOT)), "_external_data"); Z = os.path.join(EXT, "desi_dr2_ksz_zenodo", "x", "zenodo"); RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
H, OM = .679, .3085; DH = 299792.458 / (100 * H); zz = np.linspace(0, 1, 4001); EE = np.sqrt(OM * (1 + zz) ** 3 + 1 - OM); CH = np.r_[0, np.cumsum(.5 * (1 / EE[1:] + 1 / EE[:-1]) * np.diff(zz))]
DA = lambda x: DH * np.interp(x, zz, CH) / (1 + x); ZTF = np.array([[9, 82.], [9.5, 102.], [10, 131.], [10.5, 178.], [10.75, 210.], [11, 295.], [11.25, 480.], [11.5, 950.]]); Rv = lambda l: np.interp(l, ZTF[:, 0], ZTF[:, 1])
BETA, RCK, NORM, MUE = .43, 6., 1.84, 1.14; MSUN, KPC, MP, SIGT, TCMB = 1.98847e30, 3.0856776e19, 1.67262192e-27, 6.6524587e-29, 2.72548e6; ST = 300 / 299792.458; SB = 1.6 / (2 * math.sqrt(2 * math.log(2)))
def tau_tab(l, k):
    R0 = float(Rv(l)); rr = np.linspace(0, R0, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA); ne0 = NORM * 10 ** l * MSUN / (np.trapz(4 * np.pi * rr ** 2 * sh, rr) * KPC ** 3) / (MUE * MP); Rk = np.r_[0, np.geomspace(.1, k * R0, 500)]; o = np.zeros_like(Rk)
    for i, R in enumerate(Rk[:-1]):
        ll = np.linspace(0, math.sqrt((k * R0) ** 2 - R * R), 2001); o[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return Rk, SIGT * ne0 * o
FG = .05; nf = int(22 / FG); fx = (np.arange(2 * nf + 1) - nf) * FG; X, Y = np.meshgrid(fx, fx); FT = np.hypot(X, Y); BK = np.exp(-.5 * FT ** 2 / SB ** 2); BK /= BK.sum(); BF = np.fft.rfft2(np.fft.ifftshift(BK)); DAREA = FG * FG
TAB = {}
def cap_int(zc, l, k, th):
    key = (round(l, 4), k)
    if key not in TAB: TAB[key] = tau_tab(l, k)
    Rk, t = TAB[key]; img = np.interp(FT * DA(zc) * 1e3 * math.pi / 180 / 60, Rk, t, right=0); cv = np.fft.irfft2(np.fft.rfft2(img) * BF, s=img.shape); o = np.argsort(FT.ravel()); fs, cs = FT.ravel()[o], np.cumsum(cv.ravel()[o]) * DAREA
    a = np.interp(th, fs, cs); b = np.interp(th * math.sqrt(2), fs, cs); return a - (b - a)
def load(lbl): return np.load(os.path.join(Z, f"Fig6_BGS_BRIGHT-20.2_logm{lbl}.npz"))
print("Fig6 labels", sorted(f for f in os.listdir(Z) if f.startswith("Fig6_BGS")), flush=True)
A, B, C_ = load("10.50"), load("11.00"), load("10.00"); th = A["th"]; assert np.allclose(th, B["th"]); print("th", np.round(th, 2), "R", np.round(A["R"], 3), flush=True)
sn = float(np.sqrt(A["prof"] @ np.linalg.inv(A["cov"]) @ A["prof"])); check("K2_SN_vs_paper", abs(sn / 8.23 - 1) < .25, f"S/N(>10.5) {sn:.2f} vs 8.23")
h = np.load(os.path.join(Z, "Fig2_BGS_BRIGHT-20.2.npz")); bc, hh = h["binc"], h["hist"]; wd = float(np.median(np.diff(bc))); print("Fig2 bin width", wd, "N total", hh.sum(), flush=True)
def N(a, b=99):
    e0 = bc - wd / 2; e1 = bc + wd / 2; return float(np.sum(hh * np.clip((np.minimum(e1, b) - np.maximum(e0, a)) / wd, 0, 1)))
N105, N11, N10 = N(10.5), N(11), N(10); w = (N105 - N11) / N105; w0 = (N10 - N105) / N10; RES.update(N105=N105, N11=N11, N10=N10, w=w, w0=w0); print(f"N>10 {N10:.0f} N>10.5 {N105:.0f} N>11 {N11:.0f} w {w:.3f} w0 {w0:.3f}", flush=True); check("K3_labels_counts", 1e5 < N105 < 2.3e6, f"N(>10.5) {N105:.0f}")
Tb = (A["prof"] - (1 - w) * B["prof"]) / w; Cb = (A["cov"] - (1 - w) ** 2 * B["cov"]) / w ** 2; pd = bool(np.all(np.linalg.eigvalsh(Cb) > 0)); check("K4_Cbin_posdef", pd, f"min eig {np.linalg.eigvalsh(Cb).min():.3g}"); Cb_use = Cb if pd else np.diag(np.diag(Cb))
Tl = (C_["prof"] - (1 - w0) * A["prof"]) / w0; Cl = (C_["cov"] - (1 - w0) ** 2 * A["cov"]) / w0 ** 2; 
D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); print("gh6 keys", D.files, flush=True); lmk = "lm" if "lm" in D.files else [k for k in D.files if k.lower().startswith(("lm", "logm", "mass"))][0]; zb0, lb0 = D["z"], D[lmk]; zh = np.load(os.path.join(Z, "Fig3_BGS_BRIGHT-20.2.npz")); print("mean z Fig3", round(float(np.sum(zh["binc"] * zh["hist"]) / zh["hist"].sum()), 3), "DR1 all z<.5", round(float(zb0[zb0 < .5].mean()), 3), flush=True)
Dj = json.load(open(os.path.join(ROOT, "GH9_cigale_chen_mass_offset", "gh9_match.json")))["Dj"]; hterm = 2 * np.log10(.704 / H)
def model(lo, hi, Dv, thv, ks=("1.0", "1.8", "3.0"), n=5):
    ed = np.linspace(lo, hi, n + 1); o = {k: np.zeros(len(thv)) for k in ks}; wt = 0
    for j in range(n):
        q = (lb0 >= ed[j]) & (lb0 < ed[j + 1]) & (zb0 > .05) & (zb0 < .5); wj = N(ed[j], ed[j + 1]); zq = np.quantile(zb0[q], [.125, .375, .625, .875]); lc = (ed[j] + ed[j + 1]) / 2 + hterm - Dv(lc0 := (ed[j] + ed[j + 1]) / 2)
        for zc in zq:
            for k in ks: o[k] += wj / 4 * np.array([cap_int(float(zc), float(lc), float(k), float(t)) for t in thv])
        wt += wj
    return {k: TCMB * ST * o[k] / wt for k in ks}
def DG(x):
    return Dj[int(np.clip((x - 10.6) // .1, 0, 3))]
def fit(T, C, M, lab, sel=None):
    if sel is None: sel = np.ones(len(T), bool)
    Ci = np.linalg.inv(C[np.ix_(sel, sel)]); T2 = T[sel]; o = {}
    for k, m0 in M.items():
        m = m0[sel]; s = 1 / math.sqrt(m @ Ci @ m); a = float(m @ Ci @ T2) * s ** 2; o[k] = dict(A=a, s=s, chi2_A1=float((T2 - m) @ Ci @ (T2 - m)), chi2_best=float((T2 - a * m) @ Ci @ (T2 - a * m)))
    o["null"] = float(T2 @ Ci @ T2); o["n"] = int(sel.sum()); print(f"{lab}: " + "; ".join(f"A({k}) {o[k]['A']:+.3f}+-{o[k]['s']:.3f} chi2(A=1) {o[k]['chi2_A1']:.1f}" for k in M) + f"; null chi2 {o['null']:.1f}/{o['n']}", flush=True); return o
M1 = model(10.5, 11, DG, th); M0 = model(10.5, 11, lambda x: 0., th); print("model k=1.8 D1", np.round(M1["1.8"], 2), flush=True); print("T_bin", np.round(Tb, 2), "err", np.round(np.sqrt(np.diag(Cb_use)), 2), flush=True)
RES["th"] = th.tolist(); RES["R"] = A["R"].tolist(); RES["Tb"] = Tb.tolist(); RES["errb"] = np.sqrt(np.diag(Cb_use)).tolist(); RES["m18"] = M1["1.8"].tolist()
F = fit(Tb, Cb_use, M1, "PRIMARY bin 10.5-11 D1"); RES["primary"] = F; RES["D0"] = fit(Tb, Cb_use, M0, "bin D=0"); RES["inner3"] = fit(Tb, Cb_use, M1, "bin D1 theta<=3'", th <= 3.0)
RES["thr105"] = fit(A["prof"], A["cov"], M1, "threshold >10.5 as published vs bin model")
lp = bool(np.all(np.linalg.eigvalsh(Cl) > 0)); ML = model(10, 10.5, lambda x: Dj[0], th); RES["bin10"] = fit(Tl, Cl if lp else np.diag(np.diag(Cl)), ML, f"bin 10-10.5 (posdef {lp}), lowest D extrapolated")
a, s = F["1.8"]["A"], F["1.8"]["s"]; cl = "BELOW NEED" if a + 2 * s < 1 else ("ABOVE NEED" if a - 2 * s > 1 else ("CONSISTENT WITH NEED" if a / s >= 3 else "NOT DETECTED")); RES["class"] = cl; print("CLASS", cl, flush=True)
inj = .5 * M1["1.8"]; Ci = np.linalg.inv(Cb_use); m = M1["1.8"]; v = float(m @ Ci @ inj / (m @ Ci @ m)); check("K5_injection", abs(v - .5) < 1e-6, f"{v:.8f}"); check("MUTATE_flip", abs(float(m @ Ci @ (-Tb) / (m @ Ci @ m)) + a) < 1e-9, "T -> -T")
r = np.load(os.path.join(Z, "Fig8_BGS_BRIGHT-20.2_logm10.50.npz")); RES["fig8"] = dict(th=r["th"].tolist(), ratio=r["ratio"].tolist(), err=r["yerr"].tolist()); print("Fig8 >10.5 ratio", np.round(r["ratio"], 2), "+-", np.round(r["yerr"], 2), flush=True)
# K1: shape against GH7's model at GH7's grid (mean CAP there, area here)
Gc = np.load(os.path.join(EXT, "gh7_work", "gh7_cap.npz")); TH = Gc["TH"]; zq = float(np.load(os.path.join(EXT, "gh7_work", "gh7_lenses.npz"))["z"][Gc["good"] & (Gc["iz"] == 4)].mean()); lb = np.array([10.6, 10.7, 10.8, 10.9, 11.0]) + hterm; mm = np.array([cap_int(zq, float((lb[1] + lb[2]) / 2), 1.8, float(t)) / (math.pi * t * t) for t in TH]); g = Gc["m1.8"][4, 1]; rat = (mm / g)[TH >= 2]; check("K1_model_vs_GH7", np.max(np.abs(rat - 1)) < .02, f"ratio {np.round(rat, 4)}")
json.dump(RES, open(os.path.join(HERE, "gh10.json"), "w"), indent=1, sort_keys=True)
