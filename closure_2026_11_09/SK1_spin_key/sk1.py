#!/usr/bin/env python3
"""SK1 (FROZEN_CRITERIA.md, origin 8fd9c516e3): does the a0 law's residual at fixed M* and g_N rise as lambda_Re falls?
python3 -I sk1.py            -> sk1.json / sk1.out
python3 -I sk1.py --mutate   -> sk1_MUTATE.json / sk1_MUTATE.out (M1 lambda shuffle, M2 +0.2 dex plant, M3 mass column swap)
MaNGA DynPop (untracked, on disk), ATLAS3D replication row, T15 environment. One thread, seconds.
kappa = 1/2 FITTED; not theory closed. Adopts nothing. Footings never pooled."""
import os, sys, json, math, signal, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u
signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))   # short, rerunnable; outputs written only at the end

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
MUT = "--mutate" in sys.argv; TAG = "sk1_MUTATE" if MUT else "sk1"; OUT = []; RES = dict(tag=TAG, criteria="8fd9c516e3", note="kappa = 1/2 FITTED; not theory closed; adopts nothing")
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MS, MPC, KPC, C = 6.6743e-11, 1.98892e30, 3.0857e22, 3.0857e19, 2.99792458e5
A0 = {"canonical": 1.2e-10, "alt": 1.1e-10}; A0H = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
NB = 2000; SEED = 20261109; HCONV = 2 * math.log10(100 / 67.8); LN10 = math.log(10)
LBINS = [0.0, 0.1, 0.2, 0.3, 0.45, 0.6, 1.0001]; LCEN = [0.05, 0.15, 0.25, 0.375, 0.525, 0.8]

# ------------------------------------------------ record's IMF handling (QX26 / ST1)
A_SL, A_IC, K_TO_S = 0.38, -0.06, 1 / 0.63
def alpha(se): return 10 ** (A_SL * np.log10(np.asarray(se, float) / 200.0) + A_IC)
def fK(se): return np.maximum(alpha(se) * K_TO_S, 1.0)
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)
def rho(gd, gN, a0): return np.log10(gd) - np.log10(glaw(gN, a0))

# ------------------------------------------------ matched cell statistic, vectorised (QX22 / KU / NC3 rule)
def Dstat(r, grp, cell, idx=None):
    """sum_c w_c [median r(grp) - median r(~grp)] / sum w_c over cells with >= 2 of each; w_c = min(n1, n0)."""
    if idx is not None: r, grp, cell = r[idx], grp[idx], cell[idx]
    key = cell * 2 + grp.astype(np.int64); o = np.lexsort((r, key)); k = key[o]; rr = r[o]
    st = np.flatnonzero(np.r_[True, k[1:] != k[:-1]]); cnt = np.diff(np.r_[st, len(k)])
    med = 0.5 * (rr[st + (cnt - 1) // 2] + rr[st + cnt // 2]); uk = k[st]; uc, ug = uk // 2, uk % 2
    p1 = np.flatnonzero(ug == 1); p1 = p1[p1 > 0]; p1 = p1[(uc[p1 - 1] == uc[p1]) & (ug[p1 - 1] == 0)]; p0 = p1 - 1
    ok = (cnt[p1] >= 2) & (cnt[p0] >= 2); p1, p0 = p1[ok], p0[ok]
    if len(p1) == 0: return float("nan"), 0, 0
    w = np.minimum(cnt[p1], cnt[p0]); return float(np.sum(w * (med[p1] - med[p0])) / np.sum(w)), int(len(p1)), int(np.sum(cnt[p1]))
def boot(r, grp, cell, nb=NB, seed=SEED):
    rng = np.random.default_rng(seed); n = len(r)
    b = np.array([Dstat(r, grp, cell, rng.integers(0, n, n))[0] for _ in range(nb)]); b = b[np.isfinite(b)]
    if len(b) < nb // 2: return float("nan"), float("nan")
    return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
def mkcell(x, dx, y, dy): return (np.floor(x / dx).astype(np.int64) + 10000) * 100000 + (np.floor(y / dy).astype(np.int64) + 50000)
def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])

# ------------------------------------------------ DynPop
F = os.path.join(REPO, "_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits")
with fits.open(F) as h:
    d = h[1].data
    COL = {k: np.array(d[k], float) for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "Re_arcsec_MGE", "DA", "z", "nsa_sersic_mass", "nsa_elpetro_mass", "Qual", "obj_ra", "obj_dec")}
    AB = np.array(d["nsa_elpetro_absmag"], float)
    MT = np.array([np.array(h[i].data["log_Mt_rhalf"], float) for i in range(2, 12)])
    RH = np.array([np.array(h[i].data["rhalf_arcsec"], float) for i in range(2, 12)])
    X2 = np.array([np.array(h[i].data["chi2_dof"], float) for i in range(2, 12)])
NTOT = len(COL["z"])
nfin = np.sum(np.isfinite(MT) & np.isfinite(RH) & (RH > 0), axis=0)

# ---- KA2 first: KU2 replayed with KU2's own conventions (hosted footings, elpetro as stored, H0 70 D_A from z, ln)
def ka2():
    lam, eps, sig, me, msr, z, q = (COL[k] for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "nsa_elpetro_mass", "nsa_sersic_mass", "z", "Qual"))
    sel = (q >= 1) & np.isfinite(me) & (me > 0) & np.isfinite(msr) & (z > 0.005) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & (nfin >= 8)
    lam, eps, sig, me, z = lam[sel], eps[sel], sig[sel], me[sel], z[sel]; mt, rh, x2 = MT[:, sel], RH[:, sel], X2[:, sel]
    slow = (lam < 0.08 + eps / 4) & (eps < 0.4); n = len(z); DA = C * z / 70.0 / (1 + z) * MPC
    xv = np.where(np.isfinite(x2) & np.isfinite(mt) & np.isfinite(rh) & (rh > 0), x2, np.inf); b1 = np.argsort(xv, axis=0, kind="stable")[0]; jj = np.arange(n)
    r = rh[b1, jj] * math.pi / 648000 * DA; go = G * 10 ** mt[b1, jj] * MS / r ** 2; gb = G * 0.5 * 10 ** me * MS / r ** 2
    cell = np.floor(me / 0.2).astype(np.int64) * 1000 + np.floor(np.log10(sig) / 0.1).astype(np.int64); out = {}
    for f, a0 in A0H.items():
        ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0); res = np.log(go[ok]) - np.log(glaw(gb[ok], a0))
        Dv, nc, _ = Dstat(res, slow[ok], cell[ok]); out[f] = dict(D=Dv, n=int(ok.sum()), n_slow=int(slow[ok].sum()), cells=nc)
    return out
KU2 = {"canonical": 0.023331704062784637, "alt": 0.025382603421918913}
k2 = ka2(); RES["KA2"] = {}
for f in A0H:
    dd = abs(k2[f]["D"] - KU2[f]); okk = dd <= 1e-5 and k2[f]["n"] == 6056 and k2[f]["n_slow"] == 536 and k2[f]["cells"] == 27
    RES["KA2"][f] = dict(k2[f], record=KU2[f], diff=dd, ok=bool(okk))
    P(f"KA2 KU2 replay [{f}]: D {k2[f]['D']:+.6f} ln vs {KU2[f]:+.6f} (|d| {dd:.1e}); n {k2[f]['n']}, slow {k2[f]['n_slow']}, cells {k2[f]['cells']} -> {'PASS' if okk else 'FAIL'}")

# ---- SK1 sample
lam, eps, sig, ReA, DAc, z, msr, mel, q, RA, DE = (COL[k] for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "Re_arcsec_MGE", "DA", "z", "nsa_sersic_mass", "nsa_elpetro_mass", "Qual", "obj_ra", "obj_dec"))
sel = ((q >= 1) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & np.isfinite(DAc) & (DAc > 0) & (z > 0.005) & np.isfinite(msr) & (msr > 0)
       & np.isfinite(mel) & (mel > 0) & (nfin >= 8))
lam, eps, sig, ReA, DAc, z, msr, mel, RA, DE = (x[sel] for x in (lam, eps, sig, ReA, DAc, z, msr, mel, RA, DE)); AB = AB[sel]
MT, RH, X2 = MT[:, sel], RH[:, sel], X2[:, sel]; n = len(z); jj = np.arange(n)
ur = AB[:, 2] - AB[:, 4]; red = np.isfinite(ur) & (ur >= 2.5)
X2v = np.where(np.isfinite(X2) & np.isfinite(MT) & np.isfinite(RH) & (RH > 0), X2, np.inf); ordr = np.argsort(X2v, axis=0, kind="stable")
b1, b2 = ordr[0], ordr[1]
slow0 = (lam < 0.08 + eps / 4) & (eps < 0.4)
P(f"\nSK1 {TAG}: DynPop rows {NTOT}; sample {n} (Qual >= 1 and cuts); slow {int(slow0.sum())} ({slow0.mean():.3f}), fast {int((~slow0).sum())}; red {int(red.sum())}")
P(f"chosen JAM model fractions (HDU 2-11): " + " ".join(f"{np.mean(b1 == k):.3f}" for k in range(10)))
RES["sample"] = dict(n=n, n_slow=int(slow0.sum()), n_red=int(red.sum()), model_frac=[float(np.mean(b1 == k)) for k in range(10)])

# ---- T15 environment (NC3's matching)
def t15():
    L = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "campaign_fresh_gravity/_external_data/cfg393/t15_table5.tsv")) if l.strip() and not l.startswith("#")]
    hdr = [x.strip() for x in L[0]]; c = {k: i for i, k in enumerate(hdr)}
    def col(k):
        o = np.full(len(L) - 3, np.nan)
        for i, r in enumerate(L[3:]):
            try: o[i] = float(r[c[k]])
            except (ValueError, IndexError): pass
        return o
    T = {k: col(k) for k in ("_RA.icrs", "_DE.icrs", "HV", "Nmb", "PGC", "PGC1")}; g = np.isfinite(T["_RA.icrs"]) & np.isfinite(T["_DE.icrs"])
    return {k: v[g] for k, v in T.items()}
T = t15(); i15, s15, _ = SkyCoord(RA * u.deg, DE * u.deg).match_to_catalog_sky(SkyCoord(T["_RA.icrs"] * u.deg, T["_DE.icrs"] * u.deg))
okT = (s15.arcsec < 10) & (np.abs(C * z - T["HV"][i15]) < 300); nmb = T["Nmb"][i15]; cenT = T["PGC"][i15] == T["PGC1"][i15]
ENV = dict(field=okT & (nmb == 1), satellite=okT & ~cenT & (nmb >= 2), central=okT & cenT & (nmb >= 2))
P("T15 matched " + str(int(okT.sum())) + "; " + ", ".join(f"{k} {int(v.sum())} (slow {int((v & slow0).sum())})" for k, v in ENV.items()))

# ---- accelerations
def build(model_idx, mass_log_stored, imf="posacki"):
    r = RH[model_idx, jj] * math.pi / 648000 * DAc * MPC; gd = G * 10 ** MT[model_idx, jj] * MS / r ** 2
    lm = mass_log_stored + HCONV
    f = fK(sig) if imf == "posacki" else (np.ones(n) if imf == "chabrier" else np.full(n, K_TO_S))
    lmi = lm + np.log10(f); gN = G * 0.5 * 10 ** lmi * MS / r ** 2
    return gd, gN, lmi
def grade_core(gd, gN, lmi, slow, a0, idx=None, cellkind="gN", bootit=True):
    m = np.isfinite(gd) & np.isfinite(gN) & (gd > 0) & (gN > 0)
    if idx is not None: m &= idx
    r = rho(gd[m], gN[m], a0)
    cell = mkcell(lmi[m], 0.2, np.log10(gN[m]), 0.1) if cellkind == "gN" else mkcell(lmi[m], 0.2, np.log10(sig[m]), 0.1)
    Dv, nc, nin = Dstat(r, slow[m], cell); nsl = int(np.sum(slow[m] & np.isin(cell, cell[slow[m]])))
    # slow galaxies that sit in matched cells
    key = cell * 2 + slow[m].astype(np.int64); uc = np.unique(cell[slow[m]]); matched_cells = []
    for c in uc:
        s_ = (cell == c); ns_ = int(np.sum(s_ & slow[m])); nf_ = int(np.sum(s_ & ~slow[m]))
        if ns_ >= 2 and nf_ >= 2: matched_cells.append(ns_)
    lo, hi = boot(r, slow[m], cell) if bootit else (float("nan"), float("nan"))
    return dict(D=Dv, lo=lo, hi=hi, cells=nc, n=int(m.sum()), n_slow=int(slow[m].sum()), n_slow_matched=int(sum(matched_cells)))

def full_grade(a0, slow, mass_stored, plant=0.0, bootit=True, rows=True):
    gd, gN, lmi = build(b1, mass_stored); gd = gd * np.where(slow, 10 ** plant, 1.0)
    o = dict(primary=grade_core(gd, gN, lmi, slow, a0, bootit=bootit))
    m = np.isfinite(gd) & np.isfinite(gN) & (gd > 0) & (gN > 0); o["median_y"] = float(np.median(gN[m] / a0))
    o["abs_median"] = dict(slow=float(np.median(rho(gd[m & slow], gN[m & slow], a0))), fast=float(np.median(rho(gd[m & ~slow], gN[m & ~slow], a0))))
    # SHAPE
    Db = []
    for (lo_, hi_), cen in zip(zip(LBINS[:-1], LBINS[1:]), LCEN):
        inb = (lam >= lo_) & (lam < hi_); pop = inb | (~slow & ~inb)
        g = grade_core(gd, gN, lmi, inb, a0, idx=pop, bootit=bootit); g["bin"] = [lo_, min(hi_, 1.0)]; g["centre"] = cen; g["n_bin"] = int(inb.sum()); Db.append(g)
    Dbv = np.array([g["D"] for g in Db]); okb = np.isfinite(Dbv)
    S = spearman(np.array(LCEN)[okb], Dbv[okb]) if okb.sum() >= 3 else float("nan")
    o["shape"] = dict(bins=Db, S=S, low2=[Db[0]["D"], Db[1]["D"]])
    # robustness: second-best model
    gd2, gN2, lmi2 = build(b2, mass_stored); gd2 = gd2 * np.where(slow, 10 ** plant, 1.0)
    o["second_model"] = grade_core(gd2, gN2, lmi2, slow, a0, bootit=False)
    if not rows: return o
    # controls
    ctl = {}
    for k in ("field", "satellite", "central"):
        g = grade_core(gd, gN, lmi, slow, a0, idx=ENV[k], bootit=bootit); g["evaluable"] = bool(g["n_slow_matched"] >= 10 and g["cells"] >= 3); ctl["a_" + k] = g
    ctl["b_sigma_matched"] = grade_core(gd, gN, lmi, slow, a0, cellkind="sigma", bootit=bootit)
    ctl["c1_Re_ge_4arcsec"] = grade_core(gd, gN, lmi, slow, a0, idx=ReA >= 4.0, bootit=bootit)
    ctl["c2_eps_lt_0p4"] = grade_core(gd, gN, lmi, slow, a0, idx=eps < 0.4, bootit=bootit)
    ctl["d_red"] = grade_core(gd, gN, lmi, slow, a0, idx=red, bootit=bootit)
    o["controls"] = ctl
    # disclosed rows
    o["imf_brackets"] = {}
    for imf in ("chabrier", "salpeter"):
        g_, n_, l_ = build(b1, mass_stored, imf); g_ = g_ * np.where(slow, 10 ** plant, 1.0); o["imf_brackets"][imf] = grade_core(g_, n_, l_, slow, a0, bootit=False)["D"]
    o["per_model"] = []
    for k in range(10):
        mk = np.full(n, k); g_, n_, l_ = build(mk, mass_stored); g_ = g_ * np.where(slow, 10 ** plant, 1.0); o["per_model"].append(grade_core(g_, n_, l_, slow, a0, bootit=False)["D"])
    # OLS beside
    r_ = rho(gd[m], gN[m], a0); X = np.c_[np.ones(m.sum()), lam[m], lmi[m], np.log10(gN[m])]; beta, *_ = np.linalg.lstsq(X, r_, rcond=None)
    o["ols_slope_lambda"] = float(beta[1])
    return o

def label(o):
    p = o["primary"]; D, lo, hi = p["D"], p["lo"], p["hi"]; why = []
    if not np.isfinite(D) or not np.isfinite(lo) or (hi - lo) / 2 > 0.10: return "NO POWER", ["95 % half-width > 0.10 dex or undefined"]
    if D < 0.10: return "FAIL", ["D < +0.10 dex" + (" (wrong sign)" if D < 0 else "")]
    if D < 0.20: return "UNDECIDED", ["+0.10 <= D < +0.20"]
    if not lo > 0: why.append("interval includes 0")
    sh = o["shape"]
    if not (np.isfinite(sh["S"]) and sh["S"] <= -0.6 and all(np.isfinite(x) and x >= 0.10 for x in sh["low2"])): why.append("SHAPE fails")
    if not o["second_model"]["D"] >= 0.20: why.append("second-best model D < +0.20")
    c = o.get("controls", {})
    ev = [k for k in ("a_field", "a_satellite") if c[k]["evaluable"]]
    if not ev: why.append("control (a) NOT EVALUABLE")
    elif any(not c[k]["D"] >= 0.10 for k in ev): why.append("control (a) environment fails")
    if not c["b_sigma_matched"]["D"] >= 0.10: why.append("control (b): Sigma_Re alone carries it")
    if not (c["c1_Re_ge_4arcsec"]["D"] >= 0.10 and c["c2_eps_lt_0p4"]["D"] >= 0.10): why.append("control (c) seeing/inclination fails")
    if not c["d_red"]["D"] >= 0.10: why.append("control (d) red sequence fails")
    return ("PASS (SELECTOR HIT)" if not why else "UNDECIDED"), why

def fmt(g): return f"{g['D']:+.4f} [{g['lo']:+.4f}, {g['hi']:+.4f}] (cells {g['cells']}, n {g['n']}, slow {g['n_slow']})"

# ---- KA4: residual function
gdK, gNK, lmK = build(b1, msr); mK = np.isfinite(gNK) & (gNK > 0)
ka4 = float(np.max(np.abs(rho(glaw(gNK[mK], A0["canonical"]), gNK[mK], A0["canonical"])))); RES["KA4"] = dict(max=ka4, ok=bool(ka4 <= 1e-12))
P(f"KA4 residual of the law's own prediction: max {ka4:.1e} -> {'PASS' if ka4 <= 1e-12 else 'FAIL'}")

# ---- KA1: ST1 / QX26 X-ray elliptical IMF offset replayed (QX26's formula ups = alpha(0.87 sigma_0) Ups_Salp, SK1's alpha)
def ka1():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research/data/humphrey2006_ellipticals.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]; SIG0 = dict(NGC720=239, NGC1407=271, NGC4125=226, NGC4261=309, NGC4472=282, NGC4649=331, NGC6482=302); out = {}
    for f, a0 in A0H.items():
        per = []
        for rr in rows:
            dd = dict(zip(hdr, rr)); LK = float(dd["LK_1e11"]) * 1e11; Re = float(dd["Re_kpc"]); Mv = float(dd["Mvir_1e12"]) * 1e12
            Rv = float(dd["Rvir_kpc"]); c = float(dd["c"]); a = Re / 1.8153; rs = Rv / c; Mfit = float(dd["ups_fit"]) * LK; Mh = Mv - Mfit; mc = math.log(1 + c) - c / (1 + c)
            ups = float(alpha(0.87 * SIG0[dd["name"]])) * float(dd["ups_salp"]); vals = []
            for mm in (2, 4, 8):
                r = mm * Re; Mobs = Mh * (math.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / mc + Mfit * r ** 2 / (r + a) ** 2; Mst = ups * LK * r ** 2 / (r + a) ** 2
                gN = G * Mst * MS / (r * KPC) ** 2; Ml = float(glaw(gN, a0)) * (r * KPC) ** 2 / G / MS; vals.append(math.log10(Mobs / Ml))
            per.append(np.mean(vals))
        out[f] = float(np.mean(per))
    return out
k1 = ka1(); ST1v = {"canonical": 0.09304277543049821, "alt": 0.07425213300075065}; RES["KA1"] = {}
for f in A0H:
    dd = abs(k1[f] - ST1v[f]); RES["KA1"][f] = dict(D_imf=k1[f], record=ST1v[f], diff=dd, ok=bool(dd <= 1e-4))
    P(f"KA1 ST1/QX26 X-ray elliptical IMF offset [{f}]: {k1[f]:+.6f} vs {ST1v[f]:+.6f} (|d| {dd:.1e}) -> {'PASS' if dd <= 1e-4 else 'FAIL'}")

# ---- ATLAS3D: KA3 + replication row (not graded)
def atlas():
    A = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research/data/atlas3d_fj_table.tsv")) if not l.startswith("#")]
    ha, A = A[0], A[1:]; A = {r[0].strip(): dict(zip(ha, r)) for r in A}
    E = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "_external_data/atlas3d_emsellem11/tableb1.tsv")) if l.strip() and not l.startswith("#")]
    he = [x.strip() for x in E[0]]; E = [dict(zip(he, [x.strip() for x in r])) for r in E[3:]]
    nS = sum(1 for e in E if e["F/S"] == "S"); rows = []
    for e in E:
        a = A.get(e["Gal"])
        if a is None: continue
        try:
            rows.append(dict(name=e["Gal"], lam=float(e["lamRe"]), eps=float(e["epse"]), FS=e["F/S"], sig=10 ** float(a["logsig_e"]), mlj=float(a["logML_JAM"]),
                             r12=10 ** float(a["logr12"]), L=float(a["logL"]), mls=float(a["logML_Salp"]), D=float(a["Dist_Mpc"]), qual=int(a["qual"])))
        except ValueError: continue   # a missing ('--') cell in either table: row dropped, count printed
    return nS, len(E), rows
nS, nE, AR = atlas(); okka3 = (nS == 36 and nE == 260); RES["KA3"] = dict(atlas3d_slow=nS, atlas3d_n=nE, joined=len(AR), ok=bool(okka3), dynpop_record_note="KA2 reproduces KU2's 536 slow / 6056")
P(f"KA3 ATLAS3D III F/S: {nS} slow of {nE} (published 36 of 260, 14 %) -> {'PASS' if okka3 else 'FAIL'}; joined to the FJ table: {len(AR)}")
P(f"    DynPop record count (KU1/KU2 cuts): 536 slow, 5520 fast -> {'PASS' if RES['KA2']['canonical']['n_slow'] == 536 and RES['KA2']['canonical']['n'] - 536 == 5520 else 'FAIL'} (via KA2)")
def atlas_row(a0, plant=0.0):
    R = [r for r in AR if r["qual"] >= 1]; lamA = np.array([r["lam"] for r in R]); epsA = np.array([r["eps"] for r in R]); sl = (lamA < 0.08 + epsA / 4) & (epsA < 0.4)
    sigA = np.array([r["sig"] for r in R]); rk = np.array([r["r12"] * math.pi / 648000 * r["D"] * MPC for r in R]); L = np.array([r["L"] for r in R])
    Md = 0.5 * 10 ** (np.array([r["mlj"] for r in R]) + L); Ms = 10 ** (np.array([r["mls"] for r in R]) + math.log10(0.63) + L) * fK(sigA)
    gd = G * Md * MS / rk ** 2 * np.where(sl, 10 ** plant, 1.0); gN = G * 0.5 * Ms * MS / rk ** 2; r_ = rho(gd, gN, a0); cell = mkcell(np.log10(Ms), 0.2, np.log10(gN), 0.1)
    Dv, nc, _ = Dstat(r_, sl, cell); lo, hi = boot(r_, sl, cell)
    return dict(D=Dv, lo=lo, hi=hi, cells=nc, n=len(R), n_slow=int(sl.sum()), abs_slow=float(np.median(r_[sl])), abs_fast=float(np.median(r_[~sl])),
                raw_slow_minus_fast=float(np.median(r_[sl]) - np.median(r_[~sl])))

# ------------------------------------------------ main grade
RES["foot"] = {}
if not MUT:
    for f, a0 in A0.items():
        o = full_grade(a0, slow0, msr); pl = full_grade(a0, slow0, msr, plant=0.2, bootit=True, rows=False)["primary"]
        o["plant_check"] = dict(D=pl["D"], lo=pl["lo"], hi=pl["hi"], rise=pl["D"] - o["primary"]["D"], ok=bool(abs(pl["D"] - o["primary"]["D"] - 0.2) <= 0.03 and pl["lo"] > 0))
        lab, why = label(o)
        if not o["plant_check"]["ok"]: lab, why = "NO POWER", ["MUTATE (2) plant not recovered"]
        o["label"] = lab; o["why"] = why
        if lab == "FAIL" and 0.07 <= o["primary"]["D"] < 0.10: o["gas_flag"] = "FAIL within 0.03 dex of the +0.10 line (gas omission biases D low)"
        o["atlas3d_row"] = atlas_row(a0); RES["foot"][f] = o
        p = o["primary"]; P(f"\n[{f}] a0 {a0:.2e}; median y = g_N/a0 {o['median_y']:.2f}; absolute median rho slow {o['abs_median']['slow']:+.3f}, fast {o['abs_median']['fast']:+.3f} dex")
        P(f"[{f}] PRIMARY slow - fast at matched (M*_IMF, g_N): D = {fmt(p)}; slow in matched cells {p['n_slow_matched']}")
        P(f"[{f}] SHAPE: " + "; ".join(f"[{g['bin'][0]:.2f},{g['bin'][1]:.2f}) n {g['n_bin']}: {g['D']:+.3f} [{g['lo']:+.3f}, {g['hi']:+.3f}] c{g['cells']}" for g in o["shape"]["bins"]))
        P(f"[{f}] SHAPE Spearman(D_b, lambda centre) S = {o['shape']['S']:+.3f} (spin key needs <= -0.6); two lowest bins {o['shape']['low2'][0]:+.3f}, {o['shape']['low2'][1]:+.3f} (need >= +0.10)")
        P(f"[{f}] second-best JAM model D {o['second_model']['D']:+.4f}; per HDU 2-11: " + " ".join(f"{x:+.3f}" for x in o["per_model"]))
        P(f"[{f}] IMF brackets (disclosed): Chabrier as stored {o['imf_brackets']['chabrier']:+.4f}, Salpeter everywhere {o['imf_brackets']['salpeter']:+.4f}; Posacki (primary) {p['D']:+.4f}")
        for k, g in o["controls"].items():
            ex = f", evaluable {g['evaluable']}" if "evaluable" in g else ""
            P(f"[{f}] control {k}: {fmt(g)}; slow in matched cells {g['n_slow_matched']}{ex}")
        P(f"[{f}] beside: OLS slope of rho on lambda_Re (with log M*, log g_N) {o['ols_slope_lambda']:+.4f} dex per unit lambda")
        P(f"[{f}] plant +0.2 dex on slow: D {pl['D']:+.4f} [{pl['lo']:+.4f}, {pl['hi']:+.4f}], rise {o['plant_check']['rise']:+.4f} -> {'RECOVERED' if o['plant_check']['ok'] else 'NOT RECOVERED'}")
        A3 = o["atlas3d_row"]; P(f"[{f}] ATLAS3D replication row (not graded, qual >= 1): D {A3['D']:+.4f} [{A3['lo']:+.4f}, {A3['hi']:+.4f}] cells {A3['cells']}, n {A3['n']}, slow {A3['n_slow']}; unmatched median slow - fast {A3['raw_slow_minus_fast']:+.3f}")
        P(f"[{f}] LABEL: {lab}" + (f" ({'; '.join(why)})" if why else "") + (f"; {o['gas_flag']}" if "gas_flag" in o else ""))
else:
    rng = np.random.default_rng(SEED + 1); cM = np.floor((msr + HCONV + np.log10(fK(sig))) / 0.2).astype(int); lam_s = lam.copy()
    for c in np.unique(cM): ii = np.where(cM == c)[0]; lam_s[ii] = rng.permutation(lam[ii])
    slow_s = (lam_s < 0.08 + eps / 4) & (eps < 0.4); M = {}
    for f, a0 in A0.items():
        base = full_grade(a0, slow0, msr, rows=True); bl, _ = label(base)
        m1 = grade_core(*build(b1, msr), slow_s, a0); ok1 = bool(abs(m1["D"]) < 0.05 and m1["lo"] <= 0 <= m1["hi"])
        m2 = full_grade(a0, slow0, msr, plant=0.2, rows=False)["primary"]; ok2 = bool(abs(m2["D"] - base["primary"]["D"] - 0.2) <= 0.03 and m2["lo"] > 0)
        o3 = full_grade(a0, slow0, mel, rows=True); o3pl = full_grade(a0, slow0, mel, plant=0.2, rows=False)["primary"]
        o3["plant_check"] = dict(ok=bool(abs(o3pl["D"] - o3["primary"]["D"] - 0.2) <= 0.03 and o3pl["lo"] > 0)); l3, w3 = label(o3)
        if not o3["plant_check"]["ok"]: l3 = "NO POWER"
        ok3 = l3 == bl
        M[f] = dict(base_label=bl, base_D=base["primary"]["D"], M1=dict(m1, ok=ok1), M2=dict(m2, rise=m2["D"] - base["primary"]["D"], ok=ok2),
                    M3=dict(D=o3["primary"]["D"], lo=o3["primary"]["lo"], hi=o3["primary"]["hi"], label=l3, why=w3, ok=bool(ok3)))
        P(f"\n[{f}] base label {bl}, D {base['primary']['D']:+.4f}")
        P(f"[{f}] M1 lambda_Re shuffled within M* bins: D {fmt(m1)} -> {'PASS (trend vanishes)' if ok1 else 'FAIL'}")
        P(f"[{f}] M2 plant +0.2 dex on slow g_dyn: D {fmt(m2)}, rise {m2['D'] - base['primary']['D']:+.4f} -> {'PASS (detected)' if ok2 else 'FAIL'}")
        P(f"[{f}] M3 elpetro mass column: D {o3['primary']['D']:+.4f} [{o3['primary']['lo']:+.4f}, {o3['primary']['hi']:+.4f}], label {l3} -> {'PASS (label holds)' if ok3 else 'FAIL (label flips)'}")
    RES["MUTATE"] = M; allok = all(M[f][k]["ok"] for f in M for k in ("M1", "M2", "M3")); RES["MUTATE_bites"] = bool(allok)
    P(f"\nMUTATE: M1 shuffle vanishes, M2 plant detected, M3 label holds on both footings -> {'ALL PASS' if allok else 'NOT ALL PASS'}")

ka_ok = all(RES["KA1"][f]["ok"] and RES["KA2"][f]["ok"] for f in A0H) and RES["KA3"]["ok"] and RES["KA4"]["ok"]; RES["known_answers_ok"] = bool(ka_ok)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1 if sys.platform == "darwin" else 1 / 1024) / 1e9; RES["peak_rss_GB"] = rss
P(f"\nknown answers KA1-KA4: {'ALL PASS' if ka_ok else 'NOT ALL PASS'}; peak RSS {rss:.2f} GB")
def clean(x):
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.floating, float)): return None if not math.isfinite(float(x)) else float(x)
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, np.bool_): return bool(x)
    return x
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
sys.exit(1 if MUT else (0 if ka_ok else 2))
