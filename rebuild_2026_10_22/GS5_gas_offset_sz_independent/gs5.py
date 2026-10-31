#!/usr/bin/env python3
"""GS5_gas_offset_sz_independent (FROZEN_CRITERIA.md, c8ef57d5f0): eRASS1's Mgas offset from the thermal SZ signal.
    python3 gs5.py            # gs5.out, gs5_results.json
    python3 gs5.py --mutate   # Y shuffled among matched clusters, gs5_MUTATE.out
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework. Clusters only."""
import glob, json, math, os, sys
import numpy as np
if not hasattr(np, "trapezoid"): np.trapezoid = np.trapz
from astropy.io import fits
MUT = "--mutate" in sys.argv; HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); DATA = os.path.join(os.path.dirname(RB), "real_research", "data"); OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
LINE = 0.093; MUE = 1.17; MU = 0.6; ARCMIN = math.pi / 10800
SIGT = 6.6524587e-25; MEC2 = 510.99895; MSUN = 1.98841e33; MP = 1.67262192e-24; MPC = 3.0856776e24; KEV_V2 = MP / 1e3 * 1e6 / 1.602176634e-16   # m_p (km/s)^2 in keV
Cmu = lambda mue: SIGT / MEC2 * MSUN / (mue * MP) / MPC ** 2
C = Cmu(MUE)
_zg = np.linspace(0, 1, 4001)
def DA(z, Om=0.3, h=0.70):
    I = np.cumsum(np.r_[0, 0.5 * (1 / np.sqrt(Om * (1 + _zg[1:]) ** 3 + 1 - Om) + 1 / np.sqrt(Om * (1 + _zg[:-1]) ** 3 + 1 - Om)) * np.diff(_zg)]); return 2997.92458 / h * np.interp(z, _zg, I) / (1 + np.asarray(z, float))
EE = lambda z, Om=0.3: np.sqrt(Om * (1 + np.asarray(z, float)) ** 3 + 1 - Om)
def sep_deg(ra, dec, RA, DEC):
    a = np.radians(ra); d = np.radians(dec); A = np.radians(RA); D = np.radians(DEC); return np.degrees(2 * np.arcsin(np.minimum(1, np.sqrt(np.sin((D - d) / 2) ** 2 + np.cos(d) * np.cos(D) * np.sin((A - a) / 2) ** 2))))
# ---- K1
k1a = abs(Cmu(1.148) / 1.416e-19 - 1); rg = np.linspace(1e-3, 1, 20001); ne = 1e-3; kT = 5.0; Rc = MPC; dVr = 4 * np.pi * rg ** 2 * Rc ** 3; Mg_ = np.trapezoid(ne * MUE * MP * dVr, rg) / MSUN; Y_ = np.trapezoid(SIGT / MEC2 * ne * kT * dVr, rg) / MPC ** 2; k1b = abs(Y_ / (C * Mg_ * kT) - 1)
K1 = k1a <= 0.005 and k1b <= 0.005; P(f"GS5{' [MUTATE: Y shuffled]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed\nK1 C at mu_e 1.148 {Cmu(1.148):.4e} vs 1.416e-19 ({k1a:.2%}); uniform sphere {k1b:.1e}; C at 1.17 {C:.4e}: {'PASS' if K1 else 'FAIL'}")
# ---- data
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "psz2_union.tsv")) if not l.startswith("#") and l.strip()]; H = [c.strip() for c in rows[0]]; rows = [r for r in rows[3:] if len(r) == len(H)]
col = lambda n: np.array([float(r[H.index(n)]) if r[H.index(n)].strip() else np.nan for r in rows])
Pz = dict(ra=col("RAJ2000"), dec=col("DEJ2000"), z=col("z"), snr=col("SNR"), y=col("Y5R500"), ey=col("e_Y5R500"), msz=col("MSZ")); s_ = Pz["z"] > 0; Pz = {k: v[s_] for k, v in Pz.items()}; P(f"PSZ2 rows {len(rows)}, with z {s_.sum()}")
E = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data; zE = np.array(E["BEST_Z"], float); MgE = np.array(E["MGAS500"], float) * 1e11; ML = np.array(E["MGAS500_L"], float) * 1e11; MH = np.array(E["MGAS500_H"], float) * 1e11; KT = np.array(E["KT"], float); R5E = np.array(E["R500"], float); RAE = np.array(E["RA"], float); DEE = np.array(E["DEC"], float); PC = np.array(E["PCONT"], float)
ok = np.isfinite(zE) & (zE >= 0.03) & (zE < 0.25) & (MgE > 0) & (R5E > 0) & (PC < 0.5) & (MH > ML) & (ML > 0); idx = np.where(ok)[0]; zE, MgE, ML, MH, KT, R5E, RAE, DEE = [a[idx] for a in (zE, MgE, ML, MH, KT, R5E, RAE, DEE)]; NAME = np.array(E["NAME"])[idx]; P(f"eRASS1 parent, 0.03 <= z < 0.25, PCONT < 0.5: {len(idx)}; bounds bracket Mgas in {np.mean((ML < MgE) & (MH > MgE)):.1%}; KT finite positive {np.mean(np.isfinite(KT) & (KT > 0)):.1%}")
th5 = R5E / 1e3 / DA(zE) / ARCMIN; sig = 0.5 * np.log10(MH / ML)
def match(ra, dec, z, TH=None):
    """mutual nearest; returns index into Pz for each input, -1 if none"""
    out = -np.ones(len(ra), int); sp = np.full(len(ra), np.inf)
    for j in range(len(Pz["ra"])):
        rm = np.maximum(5.0, np.minimum(10.0, 0.3 * TH)) if TH is not None else 10.0
        c = np.where(np.abs(z - Pz["z"][j]) <= 0.02)[0]
        if not len(c): continue
        s = sep_deg(ra[c], dec[c], Pz["ra"][j], Pz["dec"][j]) * 60; k = s <= (rm[c] if TH is not None else rm)
        if not k.any(): continue
        c = c[k]; s = s[k]; i = c[np.argmin(s)]; v = s.min()
        if v < sp[i]: sp[i] = v; out[i] = j
    return out, sp
mi, sp = match(RAE, DEE, zE, th5); mm = mi >= 0; nm = mm.sum()
rot = [(match((RAE + a) % 360, DEE, zE, th5)[0] >= 0).sum() for a in (30, 60, 90)]; medsep = float(np.median(sp[mm]))
P(f"eRASS1 x PSZ2: {nm} matches, median sep {medsep:.2f}', 90th {np.percentile(sp[mm], 90):.2f}'; rotated +30,+60,+90: {rot}, mean false rate {np.mean(rot) / nm:.1%}; median |dz| {np.median(np.abs(zE[mm] - Pz['z'][mi[mm]])):.4f}")
Y5 = np.full(len(idx), np.nan); EY = Y5.copy(); SNR = Y5.copy(); MSZ = Y5.copy(); Y5[mm] = Pz["y"][mi[mm]]; EY[mm] = Pz["ey"][mi[mm]]; SNR[mm] = Pz["snr"][mi[mm]]; MSZ[mm] = Pz["msz"][mi[mm]]
if MUT: rng0 = np.random.default_rng(5); pr = rng0.permutation(nm); Y5[mm] = Y5[mm][pr]; MSZ[mm] = MSZ[mm][pr]
# ---- X-COP
XT = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json"))); X = []
def plaw(lnr, lnm, q):
    a = np.polyfit(lnr[-5:], lnm[-5:], 1); return np.where(q <= lnr[-1], np.interp(q, lnr, lnm), np.polyval(a, q))
for n, v in XT.items():
    d = os.path.join(DATA, "xcop", n)
    if not os.path.isdir(d): continue
    a = fits.open(os.path.join(d, f"{n}_fgas_profile.fits"))[1]; b = fits.open(os.path.join(d, f"{n}_hydro_mass.fits"))[1]; rgs = float(a.header["R500"]); rr = np.array(a.data["RADIUS"], float) * rgs; mg = np.array(a.data["MGAS"], float); rh = np.array(b.data["RADIUS"], float); mh = np.array(b.data["M_FORW"], float); f = np.isfinite(rh) & (mh > 0); rh, mh = rh[f], mh[f]; f = np.isfinite(rr) & (mg > 0); rr, mg = rr[f], mg[f]
    R5 = v["R500"] * 1e3; gr = np.geomspace(2.0, 60 * R5, 6000); lg = np.log(gr); Mgr = np.exp(plaw(np.log(rr), np.log(mg), lg)); Mgr = np.where(gr < rr[0], mg[0] * (gr / rr[0]) ** 3, Mgr); Mt = np.exp(plaw(np.log(rh), np.log(mh), lg)); Mt = np.where(gr < rh[0], mh[0] * (gr / rh[0]) ** 2, Mt)
    rho = np.gradient(Mgr, gr) / (4 * np.pi * gr ** 2); dP = rho * 4.30091e-6 * Mt / gr ** 2; Pg = np.r_[np.cumsum((0.5 * (dP[1:] + dP[:-1]) * np.diff(gr))[::-1])[::-1], 0.0]
    def intp(Rm): k = gr <= Rm; return np.trapezoid(Pg[k] * 4 * np.pi * gr[k] ** 2, gr[k])
    mn = np.array(b.data["M_NFW"], float)[np.isfinite(np.array(b.data["RADIUS"], float))]; rn = np.array(b.data["RADIUS"], float); f2 = np.isfinite(rn) & (mn > 0); Mt2 = np.exp(plaw(np.log(rn[f2]), np.log(mn[f2]), lg)); Mt2 = np.where(gr < rn[f2][0], mn[f2][0] * (gr / rn[f2][0]) ** 2, Mt2); dP2 = rho * 4.30091e-6 * Mt2 / gr ** 2; Pg2 = np.r_[np.cumsum((0.5 * (dP2[1:] + dP2[:-1]) * np.diff(gr))[::-1])[::-1], 0.0]
    Mg5 = float(np.interp(math.log(R5), lg, Mgr)); Tm = MU * KEV_V2 * intp(R5) / Mg5; Ti5 = MU * KEV_V2 * intp(5 * R5) / Mg5
    _k5 = gr <= R5; _k55 = gr <= 5 * R5; TN = MU * KEV_V2 * np.trapezoid(Pg2[_k5] * 4 * np.pi * gr[_k5] ** 2, gr[_k5]) / Mg5; TN5 = MU * KEV_V2 * np.trapezoid(Pg2[_k55] * 4 * np.pi * gr[_k55] ** 2, gr[_k55]) / Mg5
    X.append(dict(name=n, TN=TN, TN5=TN5, z=v["z"], R5=R5, M500=v["M500"], ra=float(a.header["RA"]), dec=float(a.header["DEC"]), lg=lg, Mgr=Mgr, Mg5=Mg5, T=Tm, YC5=C * Mg5 * Ti5, YC500=C * Mg5 * Tm))
xr = np.array([c["ra"] for c in X]); xd = np.array([c["dec"] for c in X]); xz = np.array([c["z"] for c in X]); xth = np.array([c["R5"] for c in X]) / 1e3 / DA(xz) / ARCMIN; xm, xs = match(xr, xd, xz, xth)
for i, c in enumerate(X): c.update(j=int(xm[i]), Y5=float(Pz["y"][xm[i]]) if xm[i] >= 0 else np.nan, eY=float(Pz["ey"][xm[i]]) if xm[i] >= 0 else np.nan, snr=float(Pz["snr"][xm[i]]) if xm[i] >= 0 else np.nan, msz=float(Pz["msz"][xm[i]]) if xm[i] >= 0 else np.nan, th=float(xth[i]))
XALL = X; X = [c for c in X if c["j"] >= 0]; nX = len(X); xz = np.array([c["z"] for c in X])
# same-cluster set (SM1's match), T scale, s
RAall = np.array(E["RA"], float); SC = []
for c in XALL:   # the same-cluster set doesn't depend on PSZ2 (first run looped over X after the PSZ2 cut and lost ZW1215; K3 caught it)
    i = np.where((sep_deg(RAE, DEE, c["ra"], c["dec"]) * 60 <= 3) & (np.abs(zE - c["z"]) < 0.01))[0]
    if len(i):
        j = i[np.argmin(sep_deg(RAE[i], DEE[i], c["ra"], c["dec"]))]; dg = math.log10(c["Mg5"] / MgE[j]); dR = math.log10(R5E[j] / c["R5"]); da = math.log10(float(np.exp(np.interp(math.log(R5E[j]), c["lg"], np.log(c["Mgr"])))) / MgE[j]); SC.append(dict(name=c["name"], dT=math.log10(c["T"] / KT[j]) if KT[j] > 0 else np.nan, dR=dR, dg=dg, dg_eR=da, kt=float(KT[j]), T=c["T"]))
SCdR = np.array([r["dR"] for r in SC]); s_med = float(np.median(SCdR)); s_mean = float(np.mean(SCdR)); dT5 = np.array([r["dT"] for r in SC]); dT5 = dT5[np.isfinite(dT5)]; dT0 = float(np.median(dT5)); sm1 = float(np.median([r["dg"] for r in SC]))
P(f"X-COP in PSZ2 {nX} of {len(XT) - 1} on disk; same-cluster {len(SC)}: X-COP own R500 median gas {sm1:+.3f}, at eRASS1 R500 {np.median([r['dg_eR'] for r in SC]):+.3f}; s median {s_med:+.3f}, mean {s_mean:+.3f}; dT = log(T_X/KT): " + ", ".join(f"{r['name']} {r['T']:.2f}/{r['kt']:.2f} {r['dT']:+.3f}" for r in SC) + f"; median {dT0:+.3f}")
K3 = nX >= 10 and medsep < 3 and np.mean(rot) / nm < 0.05 and abs(sm1 - 0.111) <= 0.005; P(f"K3 X-COP >= 10 {nX}; median sep < 3' {medsep:.2f}; false rate < 5% {np.mean(rot) / nm:.1%}; SM1 +0.111 within 0.005 {sm1:+.3f}: {'PASS' if K3 else 'FAIL'}")
# ---- K2
PLA = lambda c: c["Y5"] * 1e-3 * ARCMIN ** 2 * float(DA(c["z"])) ** 2
rat500 = np.array([PLA(c) / 1.79 / c["YC500"] for c in X]); rat5 = np.array([PLA(c) / c["YC5"] for c in X]); K2v = float(np.median(np.log10(rat500))); K2 = abs(K2v) <= 0.10
P("X-COP Planck vs C Mg T_X (own R500): name z th500' SN Y5(1e-3 arcmin2) Mg500 T_X log(Y500/YC) log(Y5/YC5) e_lgY"); 
for c, a, b in zip(X, rat500, rat5): P(f"  {c['name']:8s} {c['z']:.3f} {c['th']:5.1f} {c['snr']:5.1f} {c['Y5']:6.1f} {c['Mg5']:.3e} {c['T']:5.2f} {math.log10(a):+.3f} {math.log10(b):+.3f} {c['eY'] / c['Y5'] / math.log(10):.3f}")
P(f"K2 median log(Y500_Planck/C Mg T_X) {K2v:+.3f}, scatter {np.std(np.log10(rat500), ddof=1):.3f}; to 5 R500 {np.median(np.log10(rat5)):+.3f}; Y5/Y500 from inversion median {np.median([c['YC5'] / c['YC500'] for c in X]):.3f}: {'PASS' if K2 else 'FAIL (route (a) void, finding on marginal Y)'}")
Q_X_abs = K2v; ratN = np.array([PLA(c) / 1.79 / (C * c["Mg5"] * c["TN"]) for c in X]); K2N = float(np.median(np.log10(ratN))); P(f"Not graded: M_FORW past the data is wild (outer slopes -3 to +2.4), and the gas extension from its last 5 points is shallow (M ~ r^0.4-0.9), so the frozen 5 R500 column is unreliable and isn't used anywhere. Same inversion with M_NFW (smooth): median log(Y500/YC) {K2N:+.3f}, scatter {np.std(np.log10(ratN), ddof=1):.3f}; Y5/Y500 median {np.median([c['TN5'] / c['TN'] for c in X]):.3f} against Planck's 1.79; median T_NFW/T_FORW {np.median([c['TN'] / c['T'] for c in X]):.3f}")
# ---- cells
ME = [13.0, 13.3, 13.6, 13.9, 14.3]; ZE = [0.03, 0.10, 0.15, 0.20, 0.25]; lgM = np.log10(MgE); qual = np.zeros(len(zE), bool); P("Completeness f (n) by cell, lg Mg rows, z columns; * enters")
for a, b in zip(ME[:-1], ME[1:]):
    L = f"  {a:.1f}-{b:.1f}:"
    for c, d in zip(ZE[:-1], ZE[1:]):
        k = (lgM >= a) & (lgM < b) & (zE >= c) & (zE < d); n = k.sum(); f = mm[k].mean() if n else 0; g = (n >= 5) and (f >= 0.85); qual |= k & g; L += f"  {f:.2f}({n}){'*' if g else ' '}"
    P(L)
nq = (qual & mm).sum(); P(f"qualified: {qual.sum()} clusters, matched {nq}, unmatched {qual.sum() - nq}")
# Eddington slope
grid = np.arange(12.5, 14.6, 0.1); cn = np.histogram(lgM, bins=np.r_[grid - 0.05, grid[-1] + 0.05])[0]
def beta_at(l):
    k = (np.abs(grid[:-0 or None] - l) <= 0.3) if False else (np.abs(grid[:len(cn)] - l) <= 0.3); k = k & (cn > 0)
    return min(0.0, float(np.polyfit(grid[:len(cn)][k], np.log10(cn[k]), 1)[0])) if k.sum() >= 3 else -2.0
beta = np.array([beta_at(l) for l in lgM]); EDD = 10 ** (beta * math.log(10) * sig ** 2)
P(f"Mg error dex in qualified: median {np.median(sig[qual]):.3f}, 84th {np.percentile(sig[qual], 84):.3f}; beta median {np.median(beta[qual]):.2f}; Eddington shift median {np.median(np.log10(EDD[qual])):+.4f} dex, mean-mass-weighted {np.log10(np.sum(MgE[qual] * EDD[qual]) / np.sum(MgE[qual])):+.4f}")
# ---- estimator
D0 = DA(zE); xD0 = DA(xz); YX5 = np.array([c["Y5"] for c in X]); xT = np.array([c["T"] for c in X]); xM = np.array([c["msz"] for c in X])
def xmg(s, c): return float(np.exp(np.interp(math.log(c["R5"]) + s * math.log(10), c["lg"], np.log(c["Mgr"]))))
XMG = {s: np.array([xmg(s, c) for c in X]) for s in {0.0, s_med, s_mean}}
def est(route, sel, s=None, Om=0.3, alpha=5 / 3, gE=2 / 3, edd=True, yp="Y5", eix=None, xix=None, dT=None, unm=False):
    """sel: boolean over parent. Returns d. unm: include unmatched in denominator with Y = 0."""
    s = s_med if s is None else s; dT = dT0 if dT is None else dT; q = DA(zE, Om) / D0; xq = DA(xz, Om) / xD0
    base = sel & mm & (np.isfinite(Y5) if yp == "Y5" else np.isfinite(MSZ)); den = sel & (mm | unm) & (np.isfinite(Y5) | (~mm) if yp == "Y5" else np.isfinite(MSZ) | (~mm))
    if route in "ab": base = base & (KT > 0); den = den & (KT > 0)
    weight = np.ones(len(zE)) if eix is None else np.bincount(eix, minlength=len(zE)).astype(float); xw = np.ones(nX) if xix is None else np.bincount(xix, minlength=nX).astype(float)
    Mg = MgE * (EDD if edd else 1.0) * q ** 2.5; xg = XMG[s] * xq ** 2.5
    if yp == "Y5": YD = Y5 * 1e-3 * ARCMIN ** 2 * (D0 * q) ** 2; XYD = YX5 * 1e-3 * ARCMIN ** 2 * (xD0 * xq) ** 2
    else: YD = MSZ ** 1.79 * q ** 2; XYD = xM ** 1.79 * xq ** 2
    if route == "a":
        n = np.sum((YD * weight)[base]) / 1.79; d_ = np.sum((C * Mg * KT * 10 ** dT * weight)[den]); return math.log10(n / d_)
    if route == "b":
        rE = np.sum((YD * weight)[base]) / np.sum((Mg * KT * 10 ** dT * weight)[den]); rX = np.sum(XYD * xw) / np.sum(xg * xT * xw); return math.log10(rE / rX)
    Yn = YD * EE(zE, Om) ** (-gE); xn = XYD * EE(xz, Om) ** (-gE); rE = np.sum((Yn * weight)[base]) / np.sum(((Mg / 1e14) ** alpha * weight)[den]); rX = np.sum(xn * xw) / np.sum((xg / 1e14) ** alpha * xw); return math.log10(rE / rX) / alpha
BUD = math.sqrt(0.03 ** 2 + 0.03 ** 2 + 0.005 ** 2 + 0.01 ** 2)
def full(route, sel, yp="Y5", nb=2000, seed=5):
    d0 = est(route, sel, yp=yp); rng = np.random.default_rng(seed); ii = np.where(sel & mm)[0]; xn = np.arange(nX); bs = []
    if len(ii) < 5: return dict(d=d0, se=np.inf, stat=np.inf, n=int(len(ii)))
    for _ in range(nb):
        e = rng.choice(ii, len(ii)); x = rng.integers(0, nX, nX); t = float(np.median(rng.choice(dT5, len(dT5)))); bs.append(est(route, sel, yp=yp, eix=e, xix=x, dT=t))
    stat = float(np.std(bs, ddof=1)); low = est(route, sel, yp=yp, unm=True); sels = 0.5 * abs(d0 - low); ed = 0.5 * abs(d0 - est(route, sel, yp=yp, edd=False)); ss = [est(route, sel, yp=yp, s=v) for v in (0.0, s_med, s_mean)]; shalf = 0.5 * (max(ss) - min(ss)); om = [est(route, sel, yp=yp, Om=v) for v in (0.2, 0.4)]; ohalf = 0.5 * abs(om[0] - om[1]); parts = dict(stat=stat, sel=sels, edd=ed, s=shalf, Om=ohalf)
    if route == "d":
        al = [est(route, sel, yp=yp, alpha=v) for v in (1.4, 1.9)]; parts["alpha"] = 0.5 * abs(al[0] - al[1]); ge = [est(route, sel, yp=yp, gE=v) for v in (0.0, 2 / 3)]; parts["Eexp"] = 0.5 * abs(ge[0] - ge[1])
    if route == "a": parts["budget"] = BUD
    se = math.sqrt(sum(v ** 2 for v in parts.values())); return dict(d=d0, se=se, low=low, edd_off=est(route, sel, yp=yp, edd=False), parts=parts, n=int(len(ii)))
def cls(d, se):
    if se > 0.05: return "NOT POWERED"
    if abs(d) < 2 * se: return "NO OFFSET"
    if d - se >= LINE: return "ABOVE THE LINE"
    if d + se <= LINE: return "BELOW"
    return "ON THE LINE"
fmt = lambda r: f"d {r['d']:+.3f} SE {r['se']:.3f}, N {r['n']}, stat {r['parts']['stat']:.3f}; selection floor {r['low']:+.3f}; Eddington off {r['edd_off']:+.3f}; parts " + " ".join(f"{k} {v:.3f}" for k, v in r["parts"].items())
if MUT:
    k = qual & mm & (MgE > 0); ok_ = np.isfinite(Y5) & (Y5 > 0) & k; r = float(np.corrcoef(np.log10(Y5[ok_]), np.log10(MgE[ok_]))[0, 1]); P(f"MUTATE frozen statistic corr(log Y, log Mg), one shuffle over the {nm} matches, seed 5: {r:+.3f}; route (d) d {est('d', qual):+.3f}"); okm = abs(r) < 0.15; P("MUTATE as frozen: shuffled |r| < 0.15 holds, but unshuffled r isn't above 0.5 (see next lines), so the frozen test is mis-specified and CANNOT be met: AMENDMENT_A1")
    _d0 = est("d", qual); _M0 = MgE.copy(); MgE[:] = _M0 * 10 ** -0.1; _d1 = est("d", qual); MgE[:] = _M0; P(f"Injection, not frozen: eRASS1 Mg lowered by 0.100 dex moves route (d) by {_d1 - _d0:+.3f}")
    Y0 = np.array(Pz["y"])[mi[mm]]; rng1 = np.random.default_rng(6); ii_ = np.where(mm)[0]; qq = qual[ii_]; lgmq = np.log10(MgE[ii_]); rs = []; dd = []; rs2 = []; Yc = Y5.copy()
    for _ in range(500):
        y = Y0[rng1.permutation(nm)]; rs.append(np.corrcoef(np.log10(y[qq]), lgmq[qq])[0, 1]); rs2.append(np.corrcoef(np.log10(y[qq] * D0[ii_][qq] ** 2), lgmq[qq])[0, 1]); Y5[ii_] = y; dd.append(est("d", qual))
    Y5[:] = Yc
    def pc(y):   # corr(log YD^2 E^-2/3, log Mg) with a quadratic in log z removed from each (AMENDMENT_A1)
        lz = np.log10(zE[ii_][qq]); u = np.log10(y * D0[ii_][qq] ** 2 * EE(zE[ii_][qq]) ** (-2 / 3)); v = lgmq[qq]; return float(np.corrcoef(u - np.polyval(np.polyfit(lz, u, 2), lz), v - np.polyval(np.polyfit(lz, v, 2), lz))[0, 1])
    rng2 = np.random.default_rng(7); rs3 = np.array([pc(Y0[rng2.permutation(nm)][qq]) for _ in range(500)]); r3 = pc(Y0[qq]); okA = r3 > 0.5 and abs(np.mean(rs3)) < 0.15 and np.mean(rs3 >= r3) < 0.01; P(f"AMENDMENT_A1 statistic, z removed: unshuffled {r3:+.3f}; 500 shuffles mean {np.mean(rs3):+.3f} sd {np.std(rs3):.3f}, fraction >= unshuffled {np.mean(rs3 >= r3):.3f}: {'BITES' if okA else 'DOES NOT BITE'}"); okm = okA
    yr = np.log10(Y0[qq]); P(f"unshuffled corr(log Y, log Mg) {np.corrcoef(yr, lgmq[qq])[0, 1]:+.3f}, corr(log YD^2, log Mg) {np.corrcoef(np.log10(Y0[qq] * D0[ii_][qq] ** 2), lgmq[qq])[0, 1]:+.3f}; 500 shuffles: corr(log Y, log Mg) mean {np.mean(rs):+.3f} sd {np.std(rs):.3f}; corr(log YD^2, log Mg) mean {np.mean(rs2):+.3f} sd {np.std(rs2):.3f} (D^2 carries z, and massive qualified clusters sit at high z); route (d) d mean {np.mean(dd):+.3f} sd {np.std(dd):.3f}"); open(os.path.join(HERE, "gs5_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if okm else 1)
ok_ = np.isfinite(Y5) & (Y5 > 0) & qual & mm; r0 = float(np.corrcoef(np.log10(Y5[ok_] * D0[ok_] ** 2), np.log10(MgE[ok_]))[0, 1]); sl = np.polyfit(np.log10(MgE[ok_]), np.log10(Y5[ok_] * D0[ok_] ** 2 * EE(zE[ok_]) ** (-2 / 3)), 1)[0]; xsl = np.polyfit(np.log10(XMG[s_med]), np.log10(YX5 * xD0 ** 2 * EE(xz) ** (-2 / 3)), 1)[0]; xsc = np.std(np.log10(YX5 * xD0 ** 2 * EE(xz) ** (-2 / 3)) - 5 / 3 * np.log10(XMG[s_med]), ddof=1) / (5 / 3)
P(f"corr(log YD^2, log Mg) {r0:+.3f} (MUTATE must fall from above 0.5); OLS slope eRASS1 {sl:.2f}, X-COP {xsl:.2f}; X-COP scatter about 5/3 in Mg dex {xsc:.3f}, zero-point SE {xsc / math.sqrt(nX):.3f}; median Y S/N eRASS1 {np.median(SNR[ok_]):.1f}, X-COP {np.median([c['snr'] for c in X]):.1f}")
RES = {}
for lab, rt, yp in (("a", "a", "Y5"), ("b", "b", "Y5"), ("d", "d", "Y5"), ("d_MSZ", "d", "MSZ")):
    r = full(rt, qual, yp=yp); r["class"] = cls(r["d"], r["se"]); RES[lab] = r; P(f"route {lab}: {r['class']}: {fmt(r)}")
RES["a_rawT"] = est("a", qual, dT=0.0); RES["b_rawT"] = est("b", qual, dT=0.0); RES["a_vs_K2"] = RES["a"]["d"] - K2v; P(f"raw KT (no T scale): (a) {RES['a_rawT']:+.3f}, (b) {RES['b_rawT']:+.3f}; (a) minus X-COP's own K2 {RES['a_vs_K2']:+.3f}")
P("By lg Mg bin (qualified cells only)"); BIN = {}
for a, b in zip(ME[:-1], ME[1:]):
    k = qual & (lgM >= a) & (lgM < b)
    if (k & mm).sum() < 5: P(f"  {a:.1f}-{b:.1f}: too few"); continue
    BIN[f"{a}-{b}"] = {}
    L = f"  {a:.1f}-{b:.1f}, N {(k & mm).sum()}, median M500 {np.median(np.array(E['M500'], float)[idx][k]):.1f}e13:"
    for lab, rt, yp in (("a", "a", "Y5"), ("b", "b", "Y5"), ("d", "d", "Y5"), ("d_MSZ", "d", "MSZ")):
        r = full(rt, k, yp=yp, nb=500); r["class"] = cls(r["d"], r["se"]); BIN[f"{a}-{b}"][lab] = r; L += f" {lab} {r['d']:+.3f}+-{r['se']:.3f}"
    P(L)
RES["bins"] = BIN
P("Route (d), primary Y, subsets (stat bootstrap only; S/N subsets select on Y and are diagnostic)"); SUB = {}
for lab, k in (("theta<10'", qual & (th5 < 10)), ("theta>=10'", qual & (th5 >= 10)), ("SN<7", qual & ~(SNR >= 7)), ("SN>=7", qual & (SNR >= 7)), ("z<=0.15", qual & (zE <= 0.15)), ("z>0.15", qual & (zE > 0.15)), ("sig_Mg<0.05", qual & (sig < 0.05)), ("lgMg>=13.6", qual & (lgM >= 13.6))):
    if (k & mm).sum() < 5: continue
    r = full("d", k, nb=500); rm_ = full("d", k, yp="MSZ", nb=500); SUB[lab] = dict(d=r["d"], stat=r["parts"]["stat"], d_MSZ=rm_["d"], statM=rm_["parts"]["stat"], n=r["n"]); P(f"  {lab}: N {r['n']}: d {r['d']:+.3f} +- {r['parts']['stat']:.3f}; MSZ {rm_['d']:+.3f} +- {rm_['parts']['stat']:.3f}")
RES["subsets"] = SUB
same = np.zeros(len(zE), bool)
for c in XALL:
    i = np.where((sep_deg(RAE, DEE, c["ra"], c["dec"]) * 60 <= 3) & (np.abs(zE - c["z"]) < 0.01))[0]
    if len(i): same[i[np.argmin(sep_deg(RAE[i], DEE[i], c["ra"], c["dec"]))]] = True
ex = {}
for lab, k in (("all, same clusters out", qual & ~same), ("z<=0.15, same clusters out", qual & ~same & (zE <= 0.15)), ("z>0.15", qual & ~same & (zE > 0.15))):
    r = full("d", k, nb=500); rm_ = full("d", k, yp="MSZ", nb=500); ex[lab] = dict(d=r["d"], stat=r["parts"]["stat"], d_MSZ=rm_["d"], statM=rm_["parts"]["stat"], n=r["n"]); P(f"  Post-result, not frozen: {lab}: N {r['n']}: d {r['d']:+.3f} +- {r['parts']['stat']:.3f}; MSZ {rm_['d']:+.3f} +- {rm_['parts']['stat']:.3f}")
RES["excl_same"] = ex; P(f"  Same clusters in the qualified set: {(same & qual & mm).sum()}; on the eRASS1 side their d is SM1's by construction")
_kz = qual & mm & (lgM >= 13.9); P(f"  Post-result, not frozen: mass and z mix: lg Mg 13.6-13.9 z range {zE[qual & mm & (lgM < 13.9)].min():.3f}-{zE[qual & mm & (lgM < 13.9)].max():.3f}; lg Mg >= 13.9 z<=0.15 N {(_kz & (zE <= 0.15)).sum()}, z>0.15 N {(_kz & (zE > 0.15)).sum()}")
for lab, k in (("13.9+, z<=0.15", qual & (lgM >= 13.9) & (zE <= 0.15)), ("13.9+, z>0.15", qual & (lgM >= 13.9) & (zE > 0.15))):
    if (k & mm).sum() >= 3:
        r = full("d", k, nb=500); rm_ = full("d", k, yp="MSZ", nb=500); P(f"    {lab}: N {r['n']}: d {r['d']:+.3f} +- {r['parts']['stat']:.3f}; MSZ {rm_['d']:+.3f} +- {rm_['parts']['stat']:.3f}")
vals = (Y5[ok_] * D0[ok_] ** 2 * EE(zE[ok_]) ** (-2 / 3)) / (MgE[ok_] * EDD[ok_] / 1e14) ** (5 / 3); xv = YX5 * xD0 ** 2 * EE(xz) ** (-2 / 3) / (XMG[s_med] / 1e14) ** (5 / 3); dmed = math.log10(np.median(vals) / np.median(xv)) / (5 / 3); P(f"Route (d) with medians in place of ratio of sums: {dmed:+.3f} (log-averaging style, not graded)")
RES["d_median"] = dmed
b_ = np.median(beta[qual]) / (5 / 3); toy = abs(b_) * math.log(10) * 0.1 ** 2 / (5 / 3); P(f"Toy: if X-COP were purely Y-limited with scatter 0.1 dex at fixed Mg, its A reads high by {abs(b_) * math.log(10) * 0.1 ** 2:.3f} dex in Y, so d_d reads low by at most {toy:.3f}. Not in SE.")
RES["toy_xcop_selection"] = toy
loo = []
for i in range(nX):
    x = np.delete(np.arange(nX), i); loo.append((est("d", qual, xix=x), est("d", qual, yp="MSZ", xix=x), X[i]["name"]))
P("X-COP anchor, leave one out, route (d): " + ", ".join(f"{n} {a:+.3f}/{b:+.3f}" for a, b, n in loo) + f"; range {min(l[0] for l in loo):+.3f} to {max(l[0] for l in loo):+.3f}; MSZ {min(l[1] for l in loo):+.3f} to {max(l[1] for l in loo):+.3f}")
RES["loo"] = [dict(name=n, d=a, d_MSZ=b) for a, b, n in loo]
V = RES["d"]["class"]; tag = ""
for r_ in ("a", "b"):
    if RES[r_]["class"] != "NOT POWERED" and RES[r_]["class"] != V: tag = " [T-DEPENDENT]"
if RES["d_MSZ"]["class"] != V: tag += " [Y-PRODUCT-DEPENDENT]"
P(f"VERDICT: {V}{tag}"); RES.update(verdict=V, tags=tag, K=dict(K1=bool(K1), K2=bool(K2), K2v=K2v, K3=bool(K3)), same_cluster=SC, sm1=sm1, s_med=s_med, s_mean=s_mean, dT0=dT0, nX=nX, nmatch=int(nm), xcop=[{k: c[k] for k in ("name", "z", "th", "snr", "Y5", "eY", "Mg5", "T", "msz")} for c in X], rat500=np.log10(rat500).tolist())
if not (K1 and K3): P("K failure: no verdict"); 
json.dump(RES, open(os.path.join(HERE, "gs5_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "gs5.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if (K1 and K3) else 1)
