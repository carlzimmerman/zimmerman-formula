#!/usr/bin/env python3
"""GH10: GH8/GH9's kSZ grade with smooth gas tapers in place of the sharp 3D cut. GH7, GH8 code and GH9's offsets read-only."""
import os, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
from scipy.special import erfc
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); M = json.load(open(os.path.join(ROOT, "GH9_cigale_chen_mass_offset", "gh9_match.json")))
g7p, g8p = os.path.join(ROOT, "GH7_ksz_desi_centrals", "gh7_cap.py"), os.path.join(ROOT, "GH8_ksz_velocity_hardened", "gh8_mw.py")
N7 = {"__file__": g7p, "__name__": "gh7"}; exec(open(g7p).read().split("# real CAPs")[0], N7)
N8 = {"__file__": g8p, "__name__": "gh8"}; exec(open(g8p).read().split("Cc = {}")[0], N8); N8["Cc"] = {}
RES = {"checks": {}}; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def check(n, ok, msg): RES["checks"][n] = bool(ok); P(("PASS " if ok else "FAIL ") + n + ": " + msg)
P("GH10 smooth gas taper (see FROZEN_CRITERIA.md); no detection in these data; kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; not a statement that the law wins")
Rv, RCK, BETA, NORM, MUE, MSUN, KPC, MP, SIGT = (N7[k] for k in ("Rv", "RCK", "BETA", "NORM", "MUE", "MSUN", "KPC", "MP", "SIGT"))
def taper(r, kR, form, w=0.3):
    if form == "F1": return np.exp(-.5 * (r / kR) ** 2)
    return .5 * erfc(np.log(np.maximum(r, 1e-6) / kR) / (math.sqrt(2) * w))
def massint(f, rmax, n=60001):
    rr = np.r_[0, np.geomspace(1e-2, rmax, n)]; return np.trapz(4 * np.pi * rr ** 2 * f(rr), rr)
def tab(l, k, form, norm="mass", w=0.3):
    R0 = float(Rv(l)); kR = k * R0; base = lambda r: (1 + (r / RCK) ** 2) ** (-1.5 * BETA); sharp_in_R0 = massint(base, R0); ne0 = NORM * 10 ** l * MSUN / (sharp_in_R0 * KPC ** 3) / (MUE * MP)
    f = (lambda r: base(r) * taper(r, kR, form, w)); Rm = 6 * kR
    fac = massint(base, kR) / massint(f, Rm) if norm == "mass" else sharp_in_R0 / massint(f, R0)
    Rk = np.r_[0, np.geomspace(.1, Rm, 500)]; o = np.zeros_like(Rk)
    for i, R in enumerate(Rk[:-1]):
        ll = np.linspace(0, math.sqrt(Rm ** 2 - R * R), 4001); o[i] = 2 * np.trapz(f(np.sqrt(R * R + ll * ll)), ll) * KPC
    return Rk, SIGT * ne0 * fac * o, fac
EDGES, caps, DA, SB = N7["EDGES"], N7["caps"], N7["DA"], N7["SB"]
def grid(half):
    nf = int(half / .05); fx = (np.arange(2 * nf + 1) - nf) * .05; X, Y = np.meshgrid(fx, fx); F = np.hypot(X, Y); B = np.exp(-.5 * F ** 2 / SB ** 2); B /= B.sum(); ib = np.searchsorted(EDGES, F.ravel())
    return F, np.fft.rfft2(np.fft.ifftshift(B)), ib, np.cumsum(np.bincount(ib, minlength=len(EDGES) + 1))[:len(EDGES)]
G16 = grid(16)
def cap_tab(zc, Rk, t, G=G16):
    F, BF, ib, nall = G; img = np.interp(F * DA(zc) * 1e3 * math.pi / 180 / 60, Rk, t, right=0); cv = np.fft.irfft2(np.fft.rfft2(img) * BF, s=img.shape); return caps(np.cumsum(np.bincount(ib, cv.ravel(), len(EDGES) + 1))[:len(EDGES)], nall)
C0, L = N8["C_"], N8["L_"]; z, good = L["z"], C0["good"]; iz7 = C0["iz"]; H = N7["H"]; lb = np.array([10.6, 10.7, 10.8, 10.9, 11.0]) + 2 * np.log10(.704 / H); ZC = [float(z[good & (iz7 == i)].mean()) for i in range(10)]; KS = N8["KS"]
def build(D, form, norm="mass"):
    o = {}
    for k in KS:
        a = np.zeros((10, 4, 8))
        for i in range(10):
            for j in range(4):
                l = float((lb[j] + lb[j + 1]) / 2 - D[j])
                if form == "sharp": a[i, j] = N7["model_cap"](ZC[i], l, float(k))
                else: Rk, t, _ = tab(l, float(k), form, norm); a[i, j] = cap_tab(ZC[i], Rk, t)
        o[k] = a
    return o
sel = np.ones(N8["g"].sum(), bool); O, _, Ci, w, T = N8["run"](sel, "ALL"); c, u, wt = N8["Cc"]["ALL"]; iz, il, Rs, TCMB, est = N8["iz0"], N8["il0"], N8["Rs"], N8["TCMB"], N8["est"]; wu = np.sum(wt * (u * u)[:, None], axis=0)
rng = np.random.default_rng(1828); NS = np.array([est(c, N8["shuf"](u, iz, rng), wt) for _ in range(2000)]); parts = np.array_split(np.argsort(N8["ra"]), 50); PJ = []
for p in parts:
    k_ = np.ones(len(u), bool); k_[p] = False; PJ.append(est(c[k_], u[k_], wt[k_]))
PJ = np.array(PJ)
TH = N7["TH"]
def stack(MM, k, R): return np.sum(wt * MM[k][iz, il] * (u * u)[:, None], axis=0) / wu * TCMB * R
def grade(MM, label):
    out = {}
    for n, R in Rs.items():
        r = {}
        for k in KS:
            m = stack(MM, k, R); f = np.einsum("i,ij", m, Ci) / np.einsum("i,ij,j", m, Ci, m); js = PJ @ f; A = float(f @ T); d = T - A * m; r[k] = dict(A=A, s=float((NS @ f).std()), j=float(np.sqrt(49 / 50 * np.sum((js - js.mean()) ** 2))), chi2=float(d @ Ci @ d), nullmean=float((NS @ f).mean()), model=m.tolist())
        e = max(r["1.8"]["s"], r["1.8"]["j"]); out[n] = dict(r, upper=r["1.8"]["A"] + 2 * e, below=bool(r["1.8"]["A"] + 2 * e < 1))
        P(f"  {label} R {n}: " + "; ".join(f"A({k}) {r[k]['A']:+.3f}+-{r[k]['s']:.3f} chi2 {r[k]['chi2']:.1f}" for k in KS) + f"; A(1.8)+2e {out[n]['upper']:.3f} BELOW {out[n]['below']}")
    return out
def dip(m):
    q = (TH >= 1.5) & (TH <= 3); idx = np.where(q)[0]; i = idx[np.argmin(m[idx])]; interior = 0 < i < len(m) - 1 and m[i] < m[i - 1] and m[i] < m[i + 1]; pk = m[TH <= 8][-1]; return bool(interior and m[i] > 0 and pk >= 1.5 * m[i])
P(f"data That {np.round(T, 1).tolist()}, null chi2 {T @ Ci @ T:.1f}/8, p {O['p_null']:.3f}")
Z = np.zeros(4); Dj = np.array(M["Dj"])
M0 = build(Z, "sharp"); d = max(float(np.max(np.abs(M0[k] - C0["m" + k]) / np.abs(C0["m" + k]).max())) for k in KS); check("K1_sharp_rebuild", d < 1e-6, f"{d:.1e}")
GS = grade(build(Dj, "sharp"), "D1 sharp"); a9 = json.load(open(os.path.join(ROOT, "GH9_cigale_chen_mass_offset", "gh9_prop.json")))["D1"]["grade"]["fm"]["1.8"]["A"]; d = abs(GS["fm"]["1.8"]["A"] - a9); check("K2_reproduce_GH9", d < 1e-3, f"{GS['fm']['1.8']['A']:.4f} vs {a9:.4f}")
lk = float((lb[1] + lb[2]) / 2); Rk, t, _ = tab(lk, 1.8, "F2", "mass", 0.005); a = cap_tab(ZC[5], Rk, t); b = N7["model_cap"](ZC[5], lk, 1.8); d = float(np.max(np.abs(a - b)) / np.abs(b).max()); check("K3_narrow_F2_is_sharp", d < .02, f"{d:.2e}")
R0 = float(Rv(lk)); base = lambda r: (1 + (r / RCK) ** 2) ** (-1.5 * BETA); ds = []
for fm in ("F1", "F2"):
    _, _, fac = tab(lk, 1.8, fm); ds.append(abs(fac * massint(lambda r: base(r) * taper(r, 1.8 * R0, fm), 6 * 1.8 * R0) / massint(base, 1.8 * R0) - 1))
check("K4_mass", max(ds) < 1e-3, f"{max(ds):.1e}")
Rk, t, _ = tab(lk, 3.0, "F1"); a, b = cap_tab(ZC[0], Rk, t), cap_tab(ZC[0], Rk, t, grid(24)); d = float(np.max(np.abs(a - b)) / np.abs(b).max()); check("K5_grid", d < .02, f"{d:.2e}")
RES["sharp_D1"] = GS; F = {}
for fm in ("F1", "F2"):
    MM = build(Dj, fm); F[fm] = MM; RES[f"{fm}_D1"] = grade(MM, f"D1 {fm}"); RES[f"{fm}_D1_RvirNorm"] = grade(build(Dj, fm, "rvir"), f"D1 {fm} Rvir-norm [reported]"); RES[f"{fm}_D0"] = grade(build(Z, fm), f"D0 {fm} [reported]")
m1 = F["F1"]; dbl = {k: 2 * m1[k] for k in KS}; A1 = RES["F1_D1"]["fm"]["1.8"]["A"]; m = stack(dbl, "1.8", Rs["fm"]); f = np.einsum("i,ij", m, Ci) / np.einsum("i,ij,j", m, Ci, m); d = abs(float(f @ T) * 2 / A1 - 1); check("MUTATE_double", d < 1e-9, f"{d:.1e}")
d = float(np.max(np.abs(est(c, -u, wt) + T))); check("MUTATE_flip", d < 1e-9, f"{d:.1e}"); q = RES["F1_D1"]["fm"]["1.8"]; check("MUTATE_shuffle_mean", abs(q["nullmean"]) < .1 * q["s"], f"{q['nullmean']:+.4f} vs s {q['s']:.3f}")
RES["bias"] = {}; RES["dip"] = {}
for fm in ("F1", "F2"):
    RES["bias"][fm] = {n: RES[f"{fm}_D1"][n]["1.8"]["A"] / GS[n]["1.8"]["A"] for n in Rs}; RES["dip"][fm] = {k: dip(np.array(RES[f"{fm}_D1"]["fm"][k]["model"])) for k in KS}
    P(f"bias factor {fm} A_taper/A_sharp k 1.8: " + ", ".join(f"{n} {v:.3f}" for n, v in RES["bias"][fm].items()) + f" (proposal holds if >= 2: {all(v >= 2 for v in RES['bias'][fm].values())}); template dip k 1/1.8/3: {RES['dip'][fm]}")
    P(f"  stacked template k 1.8 at D1: {np.round(RES[f'{fm}_D1']['fm']['1.8']['model'], 1).tolist()}")
P(f"  sharp template k 1.8 at D1: {np.round(GS['fm']['1.8']['model'], 1).tolist()}; sharp dip: { {k: dip(np.array(GS['fm'][k]['model'])) for k in KS} }")
bel = [RES[f"{fm}_D1"][n]["below"] for fm in ("F1", "F2") for n in Rs]; ok = all(RES["checks"].values())
RES["verdict"] = "NOT DECIDED" if not ok else "BELOW SURVIVES TAPER" if all(bel) else "TAPER REMOVES BELOW" if not any(bel) else "FORM-DEPENDENT"; P(f"VERDICT: {RES['verdict']}")
json.dump(RES, open(os.path.join(HERE, "gh10.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, "gh10.out"), "w").write("\n".join(OUT) + "\n")
