#!/usr/bin/env python3
"""GH11: two-halo shape from DR1 neighbours + miscentring, fitted to GH10's DR2 differential bin; grades the gas budget."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import chi2 as CH
from scipy.optimize import nnls
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); g10 = os.path.join(ROOT, "GH10_dr2_ksz_published_points", "gh10.py"); N = {"__file__": g10, "__name__": "g"}; exec(open(g10).read().split("def load(lbl)")[0], N)
EXT, Z, tau_tab, DA, FT, BF, FG, TCMB, ST, hterm = N["EXT"], N["Z"], N["tau_tab"], N["DA"], N["FT"], N["BF"], N["FG"], N["TCMB"], N["ST"], 2 * np.log10(.704 / N["H"]); DAREA = FG * FG; RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
Af, Bf = [np.load(os.path.join(Z, f"Fig6_BGS_BRIGHT-20.2_logm{l}.npz")) for l in ("10.50", "11.00")]; G = json.load(open(os.path.join(ROOT, "GH10_dr2_ksz_published_points", "gh10.json"))); w = G["w"]; th = Af["th"]; T = (Af["prof"] - (1 - w) * Bf["prof"]) / w; C = (Af["cov"] - (1 - w) ** 2 * Bf["cov"]) / w ** 2; Ci = np.linalg.inv(C)
Dj = json.load(open(os.path.join(ROOT, "GH9_cigale_chen_mass_offset", "gh9_match.json")))["Dj"]; DG = lambda x: Dj[int(np.clip((x - 10.6) // .1, 0, 3))]
h = np.load(os.path.join(Z, "Fig2_BGS_BRIGHT-20.2.npz")); bc, hh = h["binc"], h["hist"]; wd = float(np.median(np.diff(bc)))
def Nn(a, b): return float(np.sum(hh * np.clip((np.minimum(bc + wd / 2, b) - np.maximum(bc - wd / 2, a)) / wd, 0, 1)))
D = np.load(os.path.join(EXT, "gh6_work", "gh6_bgs.npz")); ra, de, z, lm = D["ra"], D["de"], D["z"], D["lm"]; print("BGS", len(z), flush=True)
K1, K2 = np.fft.fftfreq(FT.shape[0], FG), np.fft.rfftfreq(FT.shape[0], FG); KK2 = K1[:, None] ** 2 + K2[None, :] ** 2
o = np.argsort(FT.ravel()); fs_sort = FT.ravel()[o]
def cap_from_field(cv, thv):
    cs = np.cumsum(cv.ravel()[o]) * DAREA; a = np.interp(thv, fs_sort, cs); b = np.interp(thv * math.sqrt(2), fs_sort, cs); return a - (b - a)
def smear(sig_arcmin): return np.exp(-2 * math.pi ** 2 * sig_arcmin ** 2 * KK2)
TAB = {}
def gas_field(zc, l, k):
    key = (round(l, 4), k)
    if key not in TAB: TAB[key] = tau_tab(l, k)
    Rk, t = TAB[key]; return np.interp(FT * DA(zc) * 1e3 * math.pi / 180 / 60, Rk, t, right=0)
ed = np.linspace(10.5, 11, 6); CELLS = []
for j in range(5):
    q = (lm >= ed[j]) & (lm < ed[j + 1]) & (z > .05) & (z < .5); c = (ed[j] + ed[j + 1]) / 2; CELLS.append((Nn(ed[j], ed[j + 1]), c + hterm - DG(c), np.quantile(z[q], [.125, .375, .625, .875])))
WT = sum(c[0] for c in CELLS)
def model(k, fs, sig_kpc):
    o1 = np.zeros(len(th))
    for wj, l, zq in CELLS:
        for zc in zq:
            F = np.fft.rfft2(gas_field(float(zc), float(l), k)) * BF; S = 1.0
            if fs > 0: S = (1 - fs) + fs * smear(sig_kpc / (DA(float(zc)) * 1e3 * math.pi / 180 / 60))
            o1 += wj / 4 * cap_from_field(np.fft.irfft2(F * S, s=FT.shape), th)
    return TCMB * ST * o1 / WT
def mass(k):
    t = 0
    for wj, l, zq in CELLS:
        R0 = float(N["Rv"](l)); rr = np.linspace(.01, k * R0, 200001); sh = (1 + (rr / 6.) ** 2) ** (-.645) * rr ** 2; t += wj * 1.84 * 10 ** l * np.trapz(sh, rr) / np.trapz(sh[rr <= R0], rr[rr <= R0])
    return t / WT
# template
def unit(r, d): r, d = np.radians(r), np.radians(d); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
s0 = (z > .05) & (z < .5); U = unit(ra[s0], de[s0]); zn, ln = z[s0], lm[s0]; Tr = cKDTree(U); rng = np.random.default_rng(1111); pool = np.where((lm >= 10.5) & (lm < 11) & (z >= .1) & (z <= .4))[0]; L = rng.choice(pool, 20000, replace=False); EDG = np.arange(0, 22.01, .1); AR = math.pi * (EDG[1:] ** 2 - EDG[:-1] ** 2)
def stack(idx, dra=0., ddec=None, mode="n", hole=1000., parts=10):
    out = np.zeros((parts, len(EDG) - 1))
    for p, i in enumerate(idx):
        zc, r0, d0 = z[i], ra[i] + dra, de[i]; 
        if ddec is not None: r0, d0 = r0 + ddec[p % len(ddec)][0], d0 + ddec[p % len(ddec)][1]
        u = unit(np.array([r0]), np.array([d0]))[0]; nb = np.array(Tr.query_ball_point(u, 2 * math.sin(math.radians(22 / 60) / 2)), dtype=int)
        if not len(nb): continue
        nb = nb[np.abs(zn[nb] - zc) / (1 + zc) * 299792.458 < 2000]
        if not len(nb): continue
        sep = np.degrees(2 * np.arcsin(np.clip(np.linalg.norm(U[nb] - u, axis=1) / 2, 0, 1))) * 60; dv = np.abs(zn[nb] - zc) / (1 + zc) * 299792.458; mk = ~((sep * DA(zc) * 1e3 * math.pi / 180 / 60 < hole) & (dv < 500)); wt = np.ones(mk.sum()) if mode == "n" else 10 ** (ln[nb][mk] - 10.8); out[p % parts] += np.histogram(sep[mk], EDG, weights=wt)[0]
    return out
rs = np.random.default_rng(1112); off = np.c_[rs.uniform(1, 2, 4096) * rs.choice([-1, 1], 4096), rs.uniform(1, 2, 4096) * rs.choice([-1, 1], 4096)]
zm = float(z[L].mean()); lmean = float(sum(c[0] * c[1] for c in CELLS) / WT); G1 = np.fft.rfft2(np.fft.ifftshift(gas_field(zm, lmean, 1.0))) * BF
def template(mode, hole):
    S = stack(L, mode=mode, hole=hole) - stack(L, ddec=off, mode=mode, hole=hole); prof = S.sum(0) / AR / len(L); cen = .5 * (EDG[1:] + EDG[:-1]); img = np.interp(FT, cen, prof, right=0); return cap_from_field(np.fft.irfft2(np.fft.rfft2(img) * G1, s=FT.shape), th), prof
Tn, pn = template("n", 1000.); Tm, _ = template("m", 1000.); Tn5, _ = template("n", 500.); print("T_n", np.round(Tn / np.abs(Tn).max(), 3), flush=True); print("T_m", np.round(Tm / np.abs(Tm).max(), 3), flush=True); print("T_n hole .5", np.round(Tn5 / np.abs(Tn5).max(), 3), flush=True)
RES["Tn"] = (Tn / np.abs(Tn).max()).tolist(); RES["prof_excess"] = pn[::10].tolist()
# K4: rotated field, jackknife per 10 subsets
Sr = stack(L, dra=5.) - stack(L, dra=5., ddec=off); cen = .5 * (EDG[1:] + EDG[:-1]); sub = []
for p in range(10):
    img = np.interp(FT, cen, Sr[p] / AR * 10 / len(L), right=0); sub.append(cap_from_field(np.fft.irfft2(np.fft.rfft2(img) * G1, s=FT.shape), th))
sub = np.array(sub); zs = sub.mean(0) / (sub.std(0, ddof=1) / math.sqrt(10)); check("K4_rotated_null", np.max(np.abs(zs)) < 3, f"max |z| {np.max(np.abs(zs)):.2f}")
def fit(m, t=None, sel=None):
    if sel is None: sel = np.ones(len(T), bool)
    CI = np.linalg.inv(C[np.ix_(sel, sel)]); y, M = T[sel], m[sel]
    if t is None: s = 1 / math.sqrt(M @ CI @ M); a = float(M @ CI @ y) * s * s; c2 = float((y - a * M) @ CI @ (y - a * M)); return dict(A=a, s=s, b=0., sb=0., chi2=c2, p=float(CH.sf(c2, sel.sum() - 1)))
    Lc = np.linalg.cholesky(CI); X = Lc.T @ np.c_[M, t[sel]]; Y = Lc.T @ y; XI = np.linalg.inv(X.T @ X); be = XI @ X.T @ Y; a, bb = float(be[0]), float(be[1]); cov = XI
    if bb < 0: a, bb = float(M @ CI @ y / (M @ CI @ M)), 0.; cov = np.array([[1 / (M @ CI @ M), 0], [0, 0]])
    c2 = float((y - a * M - bb * t[sel]) @ CI @ (y - a * M - bb * t[sel])); return dict(A=a, s=float(math.sqrt(cov[0, 0])), b=bb, sb=float(math.sqrt(max(XI[1, 1], 0))), chi2=c2, p=float(CH.sf(c2, sel.sum() - 2)))
m0 = model(1.8, 0., 300.); a0 = fit(m0)["A"]; check("K1_reproduce_GH10", abs(a0 - G["primary"]["1.8"]["A"]) < 1e-3, f"{a0:.4f} vs {G['primary']['1.8']['A']:.4f}")
mz = model(1.8, .24, .01); d = float(np.max(np.abs(mz / m0 - 1)[th >= 2])); check("K2_sigma0", d < .01, f"{d:.1e}")
tn = Tn / np.abs(Tn).max(); ii = fit(m0, tn); inj = .5 * m0 + .3 * tn; Lc = np.linalg.cholesky(Ci); X = Lc.T @ np.c_[m0, tn]; be = np.linalg.solve(X.T @ X, X.T @ (Lc.T @ inj)); check("K3_injection", abs(be[0] - .5) < 1e-6 and abs(be[1] - .3) < 1e-6, str(np.round(be, 8))); check("MUTATE_flip", abs(float(m0 @ Ci @ (-T) / (m0 @ Ci @ m0)) + a0) < 1e-9, "T -> -T")
KS = (1.0, 1.8, 3.0, 5.0, 8.0); Mneed = mass(1.8); RES["Mneed"] = Mneed; print(f"Mneed {Mneed:.3e}", flush=True); RES["fits"] = {}
for lab, fs, sg in (("primary", .24, 300.), ("bracket", .5, 500.), ("nomis", 0., 300.)):
    for k in KS:
        m = model(k, fs, sg); M = mass(k); fb, f0 = fit(m, tn), fit(m); fb["M"] = fb["A"] * M; fb["sM"] = fb["s"] * M; f0["M"] = f0["A"] * M; f0["sM"] = f0["s"] * M; fin = fit(m, None, th <= 3.0); RES["fits"][f"{lab}_{k}"] = dict(b_free=fb, b0=f0, inner=fin, M_k=M, Tm=fit(m, Tm / np.abs(Tm).max()), hole5=fit(m, Tn5 / np.abs(Tn5).max()))
        print(f"{lab} k {k}: b free A {fb['A']:+.3f}+-{fb['s']:.3f} b {fb['b']:+.2f}+-{fb['sb']:.2f} chi2 {fb['chi2']:.1f} p {fb['p']:.3f} M {fb['M']:.2e}+-{fb['sM']:.2e}; b=0 A {f0['A']:+.3f}+-{f0['s']:.3f} chi2 {f0['chi2']:.1f} p {f0['p']:.3f} M {f0['M']:.2e}; inner A {fin['A']:+.3f}+-{fin['s']:.3f}; Tm b {RES['fits'][f'{lab}_{k}']['Tm']['b']:+.2f} A {RES['fits'][f'{lab}_{k}']['Tm']['A']:+.3f}; hole.5 A {RES['fits'][f'{lab}_{k}']['hole5']['A']:+.3f}", flush=True)
F = lambda lab, k: RES["fits"][f"{lab}_{k}"]; q1 = {}
for lab in ("primary", "bracket"):
    f = F(lab, 1.8)["b_free"]; e = math.hypot(f["s"], .1 * f["A"]); q1[lab] = dict(A=f["A"], e=e, below=bool(f["A"] + 2 * e < 1))
RES["Q1"] = q1; f = F("primary", 1.8); dc = f["b0"]["chi2"] - f["b_free"]["chi2"]; RES["Q2"] = "TWO-HALO SHAPE SUFFICES" if f["b_free"]["p"] > .01 and f["b_free"]["b"] / max(f["b_free"]["sb"], 1e-9) >= 2 and dc >= 4 else "NOT SHOWN"; RES["Q2_dchi2"] = dc
ok = [k for k in KS if F("primary", k)["b_free"]["p"] > .01]; sup = [k for k in ok if F("primary", k)["b_free"]["M"] - 2 * F("primary", k)["b_free"]["sM"] >= Mneed]; RES["Q3"] = "BUDGET SUPPLIED" if sup else ("BUDGET EXCLUDED" if (not ok or all(F("primary", k)["b_free"]["M"] + 2 * F("primary", k)["b_free"]["sM"] < Mneed for k in ok)) else "BUDGET ALLOWED, NOT SHOWN"); print("Q1", q1, flush=True); print("Q2", RES["Q2"], f"dchi2 {dc:.1f}", flush=True); print("Q3", RES["Q3"], "acceptable k", ok, "supplying k", sup, flush=True)
json.dump(RES, open(os.path.join(HERE, "gh11.json"), "w"), indent=1, sort_keys=True)
