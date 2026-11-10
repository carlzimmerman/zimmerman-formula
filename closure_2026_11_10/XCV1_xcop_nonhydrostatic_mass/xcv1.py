#!/usr/bin/env python3
"""XCV1 (FROZEN_CRITERIA.md, 88ad74dd17): X-COP clusters with a mass that does not assume hydrostatic equilibrium.
HeCS-omnibus caustic M200 (Sohn+2020) at each HeCS R200; RB1's conservation reading f_ret = R M_b / (M_dyn - M_b) <= 1;
hydrostatic-bias reading Q = M_caus / M_FORW at the same radius. TEST lane: adopts nothing, relabels nothing.
RB1's X-COP builder and L24's NFW-DM14 machinery are COPIED (not imported); their folders are read only.
    python3 -I xcv1.py   -> xcv1.json / xcv1.out, xcv1_MUTATE.json / xcv1_MUTATE.out
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.optimize import brentq
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); HECS = os.path.join(os.path.dirname(REPO), "_external_data", "hecs_omnibus_2026_11_10", "table2.tsv")
RB1D = os.path.join(REPO, "closure_2026_11_09", "RB1_form_b_hot_systems")
CRIT = "88ad74dd17"; T0 = time.time(); SEED = 1110; NBOOT = 10000; ND = 4000
L, LM_ = [], []
def P(s=""): print(s, flush=True); L.append(str(s))
def PM(s=""): print("[MUTATE] " + str(s), flush=True); LM_.append(str(s))

# ------------------------------------------------------------------ constants (RB1's values)
G, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; KPC = 1e3 * PC; MPC = 1e6 * PC
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
R_COS, R_BR = 5.41, 5.562; FB_ASSUMED = 0.7; SIG_METHOD = math.log(1.4)
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def fret(Mb, Md, R=R_COS):
    Mb = np.asarray(Mb, float); Md = np.asarray(Md, float); d = Md - Mb
    return np.where(d > 0, R * Mb / np.where(d > 0, d, 1.0), np.inf)
def li(r, m, t):
    """log-log interpolation inside the tabulated range, nan outside (RB1's / HL3's li)."""
    r = np.asarray(r, float); m = np.asarray(m, float); t = float(t)
    if t < r[0] or t > r[-1]: return float("nan")
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))
def fin(v): v = np.asarray(v, float); return np.where(np.isfinite(v), v, 1e9)
def class_stat(vals, seed=SEED):
    """RB1's class_stat, with XCV1's three-way label."""
    v = fin(vals); n = len(v)
    if n < 5: return dict(n=n, median=float(np.median(v)) if n else float("nan"), lo=float("nan"), hi=float("nan"), label="NOT EVALUABLE")
    rng = np.random.default_rng(seed); idx = rng.integers(0, n, size=(NBOOT, n)); meds = np.median(v[idx], axis=1)
    lo, hi = float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))
    lab = "ABOVE THE CEILING" if lo > 1 else ("BELOW THE CEILING" if hi < 1 else "AT THE CEILING")
    return dict(n=n, median=float(np.median(v)), lo=lo, hi=hi, n_above1=int(np.sum(v > 1)), label=lab)
def q_stat(vals, seed=SEED):
    v = np.asarray(vals, float); n = len(v); rng = np.random.default_rng(seed); idx = rng.integers(0, n, size=(NBOOT, n)); meds = np.median(v[idx], axis=1)
    lo, hi = float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))
    return dict(n=n, median=float(np.median(v)), lo=lo, hi=hi, label="HYDROSTATIC LOW" if lo > 1 else ("HYDROSTATIC HIGH" if hi < 1 else "NO DETECTED BIAS"))

# ------------------------------------------------------------------ X-COP (RB1's builder, copied)
R5J = json.load(open(os.path.join(DATA, "xcop", "xcop_r500_ettori2019.json")))
XD = os.path.join(DATA, "xcop"); XN = sorted(d for d in os.listdir(XD) if os.path.isdir(os.path.join(XD, d)))
PROF = {}
for name in XN:
    p_ = os.path.join(XD, name)
    with fits.open(os.path.join(p_, f"{name}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r500h = float(h[1].header["R500"])
    with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h: gas = h[1].data.copy(); hdrg = h[1].header; ra_, de_ = float(hdrg.get("RA", np.nan)), float(hdrg.get("DEC", np.nan))
    st = None
    if os.path.exists(os.path.join(p_, f"{name}_mstar.fits")):
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    hr = np.array(hm["RADIUS"], float); hM = np.array(hm["M_FORW"], float); heM = np.array(hm["EM_FORW"], float); okh = np.isfinite(hM) & (hM > 0)
    gr = np.array(gas["RADIUS"], float) * r500h; gM = np.array(gas["MGAS"], float); gL = np.array(gas["MGAS_LO"], float); gH = np.array(gas["MGAS_HI"], float)
    okg = np.isfinite(gM) & (gM > 0) & (gr > 0)
    d = dict(hr=hr[okh], hM=hM[okh], heM=heM[okh], gr=gr[okg], gM=gM[okg], gL=gL[okg], gH=gH[okg], r500_fits=r500h, R500=R5J[name]["R500"] * 1e3,
             z=R5J[name]["z"], stars=st is not None, ra=ra_, dec=de_, hm_raw=hm, gas_raw=gas)
    if st is not None:
        sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); sL = np.array(st["MSTAR_LO"], float); sH = np.array(st["MSTAR_HI"], float)
        oks = np.isfinite(sM) & (sM > 0) & (sr > 0); d["sr"], d["sM"], d["sL"], d["sH"] = sr[oks], sM[oks], sL[oks], sH[oks]
    gr_all = np.array(gas["RADIUS"], float) * r500h; mn = np.array(gas["M_NFW"], float); okn = np.isfinite(mn) & (mn > 0) & (gr_all > 0)
    d["nr"], d["nM"] = gr_all[okn], mn[okn]
    PROF[name] = d
WITH = [n for n in XN if PROF[n]["stars"]]
xg = np.geomspace(0.02, 2.0, 60); FR = []
for n in WITH:
    d = PROF[n]; FR.append([(li(d["sr"], d["sM"], x * d["R500"]) / li(d["gr"], d["gM"], x * d["R500"])) if np.isfinite(li(d["gr"], d["gM"], x * d["R500"])) else np.nan for x in xg])
fstar_med = np.nanmedian(np.array(FR), axis=0); okf = np.isfinite(fstar_med)
def fstar(x): return float(np.interp(math.log(x), np.log(xg[okf]), fstar_med[okf]))
HYD = []
for name in XN:
    d = PROF[name]
    for r in d["gr"]:
        mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r)
        if d["stars"]: ms = li(d["sr"], d["sM"], r); imput = False
        else: ms = fstar(r / d["R500"]) * mg if np.isfinite(mg) else np.nan; imput = True
        if not (np.isfinite(mh) and np.isfinite(mg) and np.isfinite(ms)): continue
        HYD.append(dict(name=name, r_kpc=float(r), x=float(r / d["R500"]), M_dyn=mh, M_gas=mg, M_star=ms, M_bar=mg + ms, measured=not imput))
def xcop_point(n, at):
    """RB1's xcop_last for one cluster (at = 'last' or 'R500')."""
    pts = [p for p in HYD if p["name"] == n]
    if at == "last": return max(pts, key=lambda q: q["r_kpc"])
    d = PROF[n]; r = d["R500"]; mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r); ms = li(d["sr"], d["sM"], r) if d["stars"] else fstar(1.0) * mg
    p = dict(name=n, r_kpc=r, x=1.0, M_dyn=mh, M_gas=mg, M_star=ms, M_bar=mg + ms, measured=d["stars"], fallback=False)
    if not np.all(np.isfinite([mh, mg, ms])): p = dict(max([q for q in pts if q["x"] <= 1.0], key=lambda q: q["r_kpc"])); p["fallback"] = True
    return p

# ------------------------------------------------------------------ baryons at an arbitrary radius (criteria section 2)
def baryons_at(n, r, star_rule="ratio", hscale=1.0):
    d = PROF[n]; mg = li(d["gr"], d["gM"], r)
    eg = abs(0.5 * (li(d["gr"], d["gH"], r) - li(d["gr"], d["gL"], r)) / mg) if np.isfinite(mg) else float("nan")
    note = ""
    if d["stars"]:
        if r <= d["sr"][-1]:
            ms = li(d["sr"], d["sM"], r); es = abs(0.5 * (li(d["sr"], d["sH"], r) - li(d["sr"], d["sL"], r)) / ms)
        else:
            rl = d["sr"][-1]; msl = d["sM"][-1]; es = abs(0.5 * (d["sH"][-1] - d["sL"][-1]) / msl)
            if star_rule == "ratio": ms = msl / li(d["gr"], d["gM"], rl) * mg; note = f"stars beyond {rl:.0f} kpc: star/gas ratio held"
            else: ms = msl; note = f"stars beyond {rl:.0f} kpc: M_star held constant"
        imput = False
    else:
        ms = fstar(r / d["R500"]) * mg; es = math.log(1.5); imput = True; note = "stars imputed (RB1's median ratio)"
    return dict(M_gas=mg * hscale, M_star=ms, M_bar=mg * hscale + ms, eg=eg, es=es, imputed=imput, note=note)

# ------------------------------------------------------------------ HeCS-omnibus table (untrusted; parsed defensively)
def load_hecs(path):
    rows = []; hdr = None
    for l in open(path, encoding="utf-8", errors="replace"):
        if l.startswith("#") or not l.strip(): continue
        t = [c.strip() for c in l.rstrip("\n").split("\t")]
        if hdr is None: hdr = t; continue
        if len(t) != len(hdr) or not t[0].isdigit(): continue
        rows.append(dict(zip(hdr, t)))
    return rows
HR = load_hecs(HECS)
NAMEMAP = {"A85": "A85", "A1795": "A1795", "Zw1215": "ZW1215", "A2029": "A2029", "A2255": "A2255", "A2142": "A2142"}
def sep_arcmin(ra1, de1, ra2, de2):
    a1, d1, a2, d2 = map(math.radians, (ra1, de1, ra2, de2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2); return math.degrees(math.acos(min(1.0, max(-1.0, c)))) * 60
HC = {}; ka3 = dict(n_rows=len(HR), matches={})
for hn, xn in NAMEMAP.items():
    m = [r for r in HR if r["ID"] == hn]; d = PROF[xn]
    near = [r for r in HR if sep_arcmin(float(r["RAJ2000"]), float(r["DEJ2000"]), d["ra"], d["dec"]) <= 6.0 and abs(float(r["zspec"]) - d["z"]) <= 0.01]
    ka3["matches"][xn] = dict(by_name=len(m), by_position=len(near), same=bool(len(m) == 1 and len(near) == 1 and near[0]["ID"] == hn),
                              sep_arcmin=sep_arcmin(float(m[0]["RAJ2000"]), float(m[0]["DEJ2000"]), d["ra"], d["dec"]) if m else None)
    r = m[0]; HC[xn] = dict(z=float(r["zspec"]), R200=float(r["R200"]) * 1e3, eR200=float(r["e_R200"]) * 1e3, M200=float(r["M200"]) * 1e14,
                            eM200=float(r["e_M200"]) * 1e14, sigma=float(r["sigmaCl"]), esig=float(r["e_sigmaCl"]), Nmem=int(r["Nmem"]), N200=int(r["N200"]))
ka3["xcop"] = len(XN); ka3["xcop_stars"] = len(WITH)
ka3["pass"] = bool(ka3["n_rows"] == 227 and all(v["same"] for v in ka3["matches"].values()) and len(XN) == 12 and len(WITH) == 7)
SIX = ["A85", "A1795", "A2029", "A2142", "ZW1215", "A2255"]; FIVE = [n for n in SIX if PROF[n]["stars"]]

# ------------------------------------------------------------------ KA-2: HeCS frame (H0 70, Om 0.3)
H0S = 70e3 / MPC
def rho_c(z): return 3 * (H0S * math.sqrt(0.3 * (1 + z) ** 3 + 0.7)) ** 2 / (8 * math.pi * G)
def M_of_R(R_kpc, z, D=200.0): return D * rho_c(z) * 4 * math.pi / 3 * (R_kpc * KPC) ** 3 / MS
ka2 = {}
for n in SIX:
    h = HC[n]; lo = M_of_R(h["R200"] - 5.0, h["z"]) - 0.005e14; hi = M_of_R(h["R200"] + 5.0, h["z"]) + 0.005e14; mid = M_of_R(h["R200"], h["z"])
    ka2[n] = dict(M200_table=h["M200"], M_implied=mid, ratio=h["M200"] / mid, band=[lo, hi], pass_=bool(lo <= h["M200"] <= hi))
KA2_PASS = all(v["pass_"] for v in ka2.values())

# ------------------------------------------------------------------ KA-1: RB1's per-cluster rows reproduced
RBJ = json.load(open(os.path.join(RB1D, "rb1.json")))
ka1 = {}
for f in FOOTS:
    g = RBJ["gate1"][f]; worst = 0.0; rows = {}
    for n in FIVE:
        pl = xcop_point(n, "last"); p5 = xcop_point(n, "R500")
        mine = dict(last=float(fret(pl["M_bar"], pl["M_dyn"])), R500=float(fret(p5["M_bar"], p5["M_dyn"])),
                    nfw_last=float(fret(pl["M_bar"], li(PROF[n]["nr"], PROF[n]["nM"], pl["r_kpc"]))), nfw_R500=float(fret(p5["M_bar"], li(PROF[n]["nr"], PROF[n]["nM"], p5["r_kpc"]))))
        ref = dict(last=g["classes"]["C-X"]["per_cluster"][n]["f_ret"], R500=g["brackets"]["C-X at R500"]["per_cluster"][n]["f_ret"],
                   nfw_last=g["brackets"]["C-X M_NFW at last (A1, post hoc)"]["per_cluster"][n], nfw_R500=g["brackets"]["C-X M_NFW at R500 (A1, post hoc)"]["per_cluster"][n])
        for k in mine: worst = max(worst, abs(mine[k] / ref[k] - 1))
        rows[n] = dict(mine=mine, rb1=ref)
    ka1[f] = dict(rows=rows, worst_rel=worst, pass_=bool(worst <= 1e-6))
KA1_PASS = all(v["pass_"] for v in ka1.values())

# ------------------------------------------------------------------ L24's NFW-DM14 machinery (copied; its own constants, frame h 0.7)
G24 = 6.674e-11; MSUN24 = 1.989e30; Mpc24 = 3.0857e22; H024 = 0.7 * 100e3 / Mpc24
def rho_crit24(z): return 3 * (H024 * math.sqrt(0.3 * (1 + z) ** 3 + 0.7)) ** 2 / (8 * math.pi * G24)
def nfw_delta_c(c): return (200.0 / 3.0) * c ** 3 / (math.log(1 + c) - c / (1 + c))
def nfw_M3d(r, rs, dc, rhoc): x = r / rs; return 4 * math.pi * dc * rhoc * rs ** 3 * (math.log(1 + x) - x / (1 + x))
def c200_DM14(M200_Msun, z):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z; return 10 ** (a + b * math.log10(M200_Msun * 0.7 / 1e12))
def r_Delta(M_Msun, z, D=200.0): return (3 * M_Msun * MSUN24 / (4 * math.pi * D * rho_crit24(z))) ** (1.0 / 3.0)
def nfw_from_M200(M200_Msun, z): c = c200_DM14(M200_Msun, z); r200 = r_Delta(M200_Msun, z, 200.0); return r200 / c, nfw_delta_c(c), rho_crit24(z), c, r200
def nfw_MDelta(M200_Msun, z, D):
    rs, dc, rhoc, c, r200 = nfw_from_M200(M200_Msun, z)
    f = lambda r: nfw_M3d(r, rs, dc, rhoc) / MSUN24 - D * (4 * math.pi / 3) * rhoc * r ** 3 / MSUN24
    rD = brentq(f, 0.05 * r200, 3 * r200, xtol=1e-3 * r200); return nfw_M3d(rD, rs, dc, rhoc) / MSUN24, rD
def nfw_M_at(M200_Msun, z, r_kpc): rs, dc, rhoc, c, r200 = nfw_from_M200(M200_Msun, z); return nfw_M3d(r_kpc * Mpc24 / 1e3, rs, dc, rhoc) / MSUN24
def nfw_M_at_hecs(M200_Msun, R200_kpc, z, r_kpc):
    """NFW-DM14 normalised to M(<R200_HeCS) = M200_HeCS exactly (the caustic profile transferred)."""
    rs, dc, rhoc, c, r200 = nfw_from_M200(M200_Msun, z); return M200_Msun * nfw_M3d(r_kpc * Mpc24 / 1e3, rs, dc, rhoc) / nfw_M3d(R200_kpc * Mpc24 / 1e3, rs, dc, rhoc)
WL_H20 = {"A85": dict(z=0.055, M200=8.4, eM200=3.3, M500=5.7), "A1795": dict(z=0.062, M200=13.9, eM200=3.3, M500=9.3), "A2029": dict(z=0.077, M200=18.1, eM200=3.8, M500=12.1),
          "A2142": dict(z=0.091, M200=14.5, eM200=3.4, M500=9.7), "ZW1215": dict(z=0.075, M200=5.1, eM200=3.1, M500=3.5)}     # L24's transcription of Herbonnet+2020 tables 2-3
WL_LC2 = [("A85", "Cypriano+04", 3.943, 0.725, 5.915, 1.087), ("A2029", "Cypriano+04", 5.038, 0.618, 7.557, 0.928), ("A2142", "Umetsu+09", 6.560, 0.627, 9.679, 1.033),
          ("A2142", "Okabe&Umetsu08", 6.149, 1.446, 9.483, 2.472), ("ZW1215", "Kubo+09", 2.140, 1.401, 2.994, 2.114)]     # L24's LC2 rows (1e14 Msun at 1.0 / 1.5 Mpc)
ka5 = max(abs(nfw_MDelta(v["M200"] * 1e14, v["z"], 500.0)[0] / 1e14 / v["M500"] - 1) for v in WL_H20.values()); KA5_PASS = bool(ka5 <= 0.05)

# ------------------------------------------------------------------ the gate at R200_HeCS
def cluster_rows(names, scale=1.0, R=R_COS, star_rule="ratio", hscale=1.0, mass_override=None, seed0=SEED):
    out = {}
    for i, n in enumerate(names):
        h = HC[n]; r = h["R200"]; b = baryons_at(n, r, star_rule, hscale)
        Md = h["M200"] * scale if mass_override is None else mass_override[n]
        f = float(fret(b["M_bar"], Md, R)); estat = h["eM200"] / h["M200"]; etot = math.sqrt(estat ** 2 + SIG_METHOD ** 2)
        rng = np.random.default_rng(seed0 + i); zg, zs, zm = rng.standard_normal((3, ND))
        Mb_d = b["M_gas"] * np.exp(b["eg"] * zg) + b["M_star"] * np.exp(b["es"] * zs)
        f_tot = fin(fret(Mb_d, Md * np.exp(etot * zm), R)); f_st = fin(fret(Mb_d, Md * np.exp(estat * zm), R))
        Pt, Ps = float(np.mean(f_tot > 1)), float(np.mean(f_st > 1))
        lab = lambda p_: "ABOVE THE CEILING" if p_ > 0.977 else ("BELOW THE CEILING" if p_ < 0.023 else "AT THE CEILING")
        lf = np.log(np.clip(f_tot, 1e-6, 1e6)); sl = float(np.std(lf[f_tot < 1e8]))
        out[n] = dict(r_kpc=r, x_R500=r / PROF[n]["R500"], M_dyn=Md, M_gas=b["M_gas"], M_star=b["M_star"], M_bar=b["M_bar"], fb=b["M_bar"] / Md, f_ret=f,
                      P_above1=Pt, label=lab(Pt), P_above1_stat=Ps, label_stat=lab(Ps), sig_lnf=sl, eM_stat=estat, eg=b["eg"], es=b["es"], imputed=b["imputed"], note=b["note"])
    return out
def parametric(rows):
    v = [(math.log(r["f_ret"]), r["sig_lnf"]) for r in rows.values() if np.isfinite(r["f_ret"]) and r["sig_lnf"] > 0]
    w = np.array([1 / s ** 2 for _, s in v]); m = float(np.sum(w * np.array([x for x, _ in v])) / np.sum(w)); e = float(1 / math.sqrt(np.sum(w)))
    return dict(f_ret=math.exp(m), lo=math.exp(m - 1.96 * e), hi=math.exp(m + 1.96 * e), sig_ln=e)
def gate(names=FIVE, **kw):
    rows = cluster_rows(names, **kw); cs = class_stat([rows[n]["f_ret"] for n in names]); return cs, rows

Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
OUT = dict(lane="XCV1", criteria=CRIT, footings={}, known_answers={}, coverage=dict(hecs=SIX, measured_stars=FIVE, not_covered=[n for n in XN if n not in SIX]))
P(f"XCV1: X-COP clusters with HeCS-omnibus caustic masses (criteria {CRIT}). TEST lane; adopts nothing; relabels nothing. kappa = 1/2 FITTED; not theory closed.")
P(f"Covered: {', '.join(SIX)} (6 of 12); measured stars: {', '.join(FIVE)}; not covered: {', '.join(OUT['coverage']['not_covered'])}.")
P(); P("KNOWN ANSWERS")
P(f"KA-1 RB1 per-cluster hydrostatic f_ret reproduced (last, R500, M_NFW last, M_NFW R500), worst rel. diff canonical {ka1['canonical']['worst_rel']:.1e}, alt {ka1['alt']['worst_rel']:.1e} (tol 1e-6) -> {'PASS' if KA1_PASS else 'FAIL'}")
for n in FIVE:
    m = ka1["canonical"]["rows"][n]["mine"]; P(f"    {n:6s} last {m['last']:.4f}  R500 {m['R500']:.4f}  M_NFW last {m['nfw_last']:.4f}  M_NFW R500 {m['nfw_R500']:.4f}")
p2l, p25 = xcop_point("A2255", "last"), xcop_point("A2255", "R500")
a2255_hse = dict(last=float(fret(p2l["M_bar"], p2l["M_dyn"])), R500=float(fret(p25["M_bar"], p25["M_dyn"])))
P(f"    A2255 (imputed stars, no RB1 per-cluster reference): last {a2255_hse['last']:.4f}  R500 {a2255_hse['R500']:.4f}")
P(f"KA-2 HeCS frame, M200 = 200 rho_c (4 pi/3) R200^3 within the R200 rounding: " + "; ".join(f"{n} {v['ratio']:.3f} {'ok' if v['pass_'] else 'MISS'}" for n, v in ka2.items()) + f" -> {'PASS' if KA2_PASS else 'FAIL'}")
P(f"KA-3 parser: {ka3['n_rows']} HeCS rows; name = position match for the six: " + "; ".join(f"{n} {v['sep_arcmin']:.2f}'" for n, v in ka3["matches"].items()) + f"; X-COP {ka3['xcop']} / {ka3['xcop_stars']} with stars -> {'PASS' if ka3['pass'] else 'FAIL'}")
ka4_id = float(fret(1.0, 1.0 + R_COS)); g_a = gate()[0]; g_b = gate(scale=FB_ASSUMED / 0.7)[0]
KA4_PASS = bool(abs(ka4_id - 1) <= 1e-12 and g_a["median"] == g_b["median"])
from scipy.integrate import quad
def D_A_kpc(z): return quad(lambda t: 299792.458 / 70.0 / math.sqrt(0.3 * (1 + t) ** 3 + 0.7), 0.0, z)[0] / (1 + z) * 1e3
for n, v in ka3["matches"].items(): v["sep_kpc"] = v["sep_arcmin"] * math.radians(1 / 60) * D_A_kpc(HC[n]["z"]); v["sep_over_R200"] = v["sep_kpc"] / HC[n]["R200"]
P("    centre offsets HeCS - X-COP (kpc, / HeCS R200): " + "; ".join(f"{n} {v['sep_kpc']:.0f} ({v['sep_over_R200']:.2f})" for n, v in ka3["matches"].items()) + "  [frozen KA-3 tolerance 6 arcmin]")
P(f"KA-5 L24's NFW-DM14 reproduces Herbonnet's M500 from M200: worst {100 * ka5:.1f} % (tol 5 %) -> {'PASS' if KA5_PASS else 'FAIL'}")
OUT["known_answers"] = dict(KA1=ka1, KA1_pass=KA1_PASS, A2255_hse=a2255_hse, KA2=ka2, KA2_pass=KA2_PASS, KA3=ka3, KA5_worst=ka5, KA5_pass=KA5_PASS)

def fmt_rows(rows):
    for n, r in rows.items():
        P(f"    {n:6s} R200 {r['r_kpc']:.0f} kpc ({r['x_R500']:.2f} R500)  M_caus {r['M_dyn'] / 1e14:5.2f}e14 (+-{100 * r['eM_stat']:.0f} % stat)  M_gas {r['M_gas'] / 1e13:5.2f}e13  M_star {r['M_star'] / 1e13:5.2f}e13"
          f"  f_b {r['fb']:.3f}  f_ret {r['f_ret']:.3f}  P(>1) {r['P_above1']:.3f} -> {r['label']}  [stat only {r['P_above1_stat']:.3f} {r['label_stat']}]" + (f"  ({r['note']})" if r["note"] else ""))
GATE = {}
for f in FOOTS:
    P(); P(f"==================== footing {f} (a0 {A0[f]:.4e}) ====================")
    cs, rows = gate(); per = cluster_rows(SIX)
    P("GATE (graded): f_ret = R M_b / (M_caus - M_b) at each HeCS R200, R 5.41, F_beta 0.7")
    fmt_rows(per)
    P(f"  CLASS (5 measured-star clusters): median f_ret {cs['median']:.3f} [{cs['lo']:.3f}, {cs['hi']:.3f}], {cs['n_above1']} of 5 above 1 -> {cs['label']}")
    br = {}
    for s_, k in ((0.9, "M_caus x 0.9"), (1.1, "M_caus x 1.1")): br[k] = gate(scale=s_)[0]
    tag = br["M_caus x 0.9"]["label"] != cs["label"] or br["M_caus x 1.1"]["label"] != cs["label"]
    br["F_beta 0.5 (x 0.714, superseded DG97/D99)"] = gate(scale=0.5 / 0.7)[0]
    br["R 5.562"] = gate(R=R_BR)[0]; br["stars held constant beyond their profile"] = gate(star_rule="const")[0]
    br["all 6 (A2255 imputed stars)"] = class_stat([per[n]["f_ret"] for n in SIX])
    hB = float(Q15["footings"][f]["main"]["h"]); br[f"h 0.7 -> {hB:.4f} (gas x (0.7/h)^0.5)"] = gate(hscale=(0.7 / hB) ** 0.5)[0]
    def med_at(s_): return gate(scale=s_)[0]["median"] - 1.0
    try: s1 = brentq(med_at, 0.3, 3.0, xtol=1e-6); fb1 = 0.7 * s1
    except ValueError: s1 = fb1 = float("nan")
    par = parametric(rows); par6 = parametric(per)
    P(f"  calibration bracket: x0.9 -> {br['M_caus x 0.9']['median']:.3f} [{br['M_caus x 0.9']['lo']:.3f}, {br['M_caus x 0.9']['hi']:.3f}] {br['M_caus x 0.9']['label']};"
      f" x1.1 -> {br['M_caus x 1.1']['median']:.3f} [{br['M_caus x 1.1']['lo']:.3f}, {br['M_caus x 1.1']['hi']:.3f}] {br['M_caus x 1.1']['label']} => {'[CALIBRATION-DEPENDENT]' if tag else 'label holds across the bracket'}")
    for k, v in br.items():
        if k.startswith("M_caus x"): continue
        P(f"  reported: {k}: median {v['median']:.3f} [{v['lo']:.3f}, {v['hi']:.3f}] -> {v['label']}")
    P(f"  reported: F_beta that puts the class median at exactly 1: {fb1:.3f} (mass scale x{s1:.3f})")
    P(f"  reported: parametric class (inverse-variance mean of ln f_ret, method scatter in): 5 clusters {par['f_ret']:.3f} [{par['lo']:.3f}, {par['hi']:.3f}]; all 6 {par6['f_ret']:.3f} [{par6['lo']:.3f}, {par6['hi']:.3f}]")
    # hydrostatic-bias reading at the same radius
    Qrows = {}
    for i, n in enumerate(SIX):
        d = PROF[n]; r = HC[n]["R200"]; mf = li(d["hr"], d["hM"], r); emf = li(d["hr"], d["heM"], r) / mf; mn = li(d["nr"], d["nM"], r)
        Q = HC[n]["M200"] / mf; eQ = math.sqrt((HC[n]["eM200"] / HC[n]["M200"]) ** 2 + emf ** 2)
        Qrows[n] = dict(M_FORW=mf, eM_FORW=emf, M_NFW=mn, Q=Q, eQ_stat=eQ, Q_NFW=HC[n]["M200"] / mn, f_hse_FORW=float(fret(per[n]["M_bar"], mf)), f_hse_NFW=float(fret(per[n]["M_bar"], mn)))
    qs = q_stat([Qrows[n]["Q"] for n in FIVE]); qn = q_stat([Qrows[n]["Q_NFW"] for n in FIVE]); fh = class_stat([Qrows[n]["f_hse_FORW"] for n in FIVE]); fhn = class_stat([Qrows[n]["f_hse_NFW"] for n in FIVE])
    P("HYDROSTATIC-BIAS READING at the same radius (HeCS R200): Q = M_caus / M_HSE")
    for n in SIX:
        q = Qrows[n]; P(f"    {n:6s} M_FORW {q['M_FORW'] / 1e14:5.2f}e14 (+-{100 * q['eM_FORW']:.0f} %)  Q {q['Q']:.3f} (+-{100 * q['eQ_stat']:.0f} % stat)  Q_NFW {q['Q_NFW']:.3f}"
                        f"  hydrostatic f_ret here: M_FORW {q['f_hse_FORW']:.3f}, M_NFW {q['f_hse_NFW']:.3f}")
    P(f"  class Q (M_FORW) median {qs['median']:.3f} [{qs['lo']:.3f}, {qs['hi']:.3f}] -> {qs['label']};  Q (M_NFW) {qn['median']:.3f} [{qn['lo']:.3f}, {qn['hi']:.3f}] -> {qn['label']}")
    P(f"  hydrostatic f_ret at HeCS R200, class: M_FORW {fh['median']:.3f} [{fh['lo']:.3f}, {fh['hi']:.3f}] {fh['label']}; M_NFW {fhn['median']:.3f} [{fhn['lo']:.3f}, {fhn['hi']:.3f}] {fhn['label']}")
    # transfers to RB1's radii (reported)
    tr = {}
    for at in ("R500", "last"):
        vq, vn = {}, {}
        for n in FIVE:
            p = xcop_point(n, at); vq[n] = float(fret(p["M_bar"], Qrows[n]["Q"] * p["M_dyn"]))
            vn[n] = float(fret(p["M_bar"], nfw_M_at_hecs(HC[n]["M200"], HC[n]["R200"], HC[n]["z"], p["r_kpc"])))
        tr[at] = dict(Q_rescaled=dict(per=vq, **class_stat(list(vq.values()))), NFW_DM14=dict(per=vn, **class_stat(list(vn.values()))))
        P(f"  reported transfer to RB1's {at}: Q x M_FORW -> {tr[at]['Q_rescaled']['median']:.3f} [{tr[at]['Q_rescaled']['lo']:.3f}, {tr[at]['Q_rescaled']['hi']:.3f}] {tr[at]['Q_rescaled']['label']}"
          f"; NFW-DM14 (EXTERNALLY CALIBRATED) -> {tr[at]['NFW_DM14']['median']:.3f} [{tr[at]['NFW_DM14']['lo']:.3f}, {tr[at]['NFW_DM14']['hi']:.3f}] {tr[at]['NFW_DM14']['label']}"
          + "  per cluster " + ", ".join(f"{n} {vq[n]:.2f}/{vn[n]:.2f}" for n in FIVE))
    # a0 row: the law's missing-mass fraction at R200_HeCS
    law = {}
    for n in SIX:
        r = per[n]["r_kpc"] * KPC; Ml = float(glaw(G * per[n]["M_bar"] * MS / r ** 2, A0[f])) * r ** 2 / G / MS; law[n] = dict(M_law=Ml, frac_missing=(per[n]["M_dyn"] - Ml) / per[n]["M_dyn"])
    P("  a0 row (reported): the law's missing fraction (M_caus - M_law)/M_caus at HeCS R200: " + ", ".join(f"{n} {law[n]['frac_missing']:.2f}" for n in SIX)
      + f"; median (5) {np.median([law[n]['frac_missing'] for n in FIVE]):.3f}")
    # section 6: weak lensing beside (never graded, never raw)
    wl = {}
    for n in FIVE:
        w = WL_H20[n]; Mw = nfw_M_at(w["M200"] * 1e14, w["z"], HC[n]["R200"]); wl[n] = dict(M_WL_R200=Mw, eM_WL=w["eM200"] / w["M200"], ratio_caus_over_WL=HC[n]["M200"] / Mw, f_ret_WL=float(fret(per[n]["M_bar"], Mw)))
    lc2 = []
    for n, ref, m1, e1, m15, e15 in WL_LC2:
        b = baryons_at(n, 1500.0); Mc = nfw_M_at_hecs(HC[n]["M200"], HC[n]["R200"], HC[n]["z"], 1500.0)
        lc2.append(dict(name=n, ref=ref, M_WL_1p5=m15 * 1e14, eM=e15 / m15, M_caus_1p5_NFW=Mc, ratio_caus_over_WL=Mc / (m15 * 1e14), f_ret_WL=float(fret(b["M_bar"], m15 * 1e14)), f_ret_caus=float(fret(b["M_bar"], Mc))))
    wlc = class_stat([wl[n]["f_ret_WL"] for n in FIVE])
    P("SECTION 6 (reported, never graded, never raw): weak lensing beside the caustic mass")
    P("  Herbonnet+2020 NFW-DM14 inside HeCS R200: " + "; ".join(f"{n} M_WL {wl[n]['M_WL_R200'] / 1e14:.2f}e14 (+-{100 * wl[n]['eM_WL']:.0f} %), M_caus/M_WL {wl[n]['ratio_caus_over_WL']:.2f}, f_ret {wl[n]['f_ret_WL']:.2f}" for n in FIVE))
    P(f"  class f_ret on Herbonnet's NFW mass: {wlc['median']:.3f} [{wlc['lo']:.3f}, {wlc['hi']:.3f}] {wlc['label']}; median M_caus/M_WL {np.median([wl[n]['ratio_caus_over_WL'] for n in FIVE]):.3f}")
    P("  LC2 at 1.5 Mpc (independent teams): " + "; ".join(f"{r['name']} {r['ref']} M_WL {r['M_WL_1p5'] / 1e14:.2f}e14 (+-{100 * r['eM']:.0f} %), M_caus(NFW-transferred) {r['M_caus_1p5_NFW'] / 1e14:.2f}e14, ratio {r['ratio_caus_over_WL']:.2f}, f_ret WL {r['f_ret_WL']:.2f} / caus {r['f_ret_caus']:.2f}" for r in lc2))
    GATE[f] = dict(class_=cs, per_cluster=per, brackets=br, calibration_dependent=bool(tag), Fbeta_at_median_1=fb1, parametric5=par, parametric6=par6,
                   Q=Qrows, Q_class=qs, Q_NFW_class=qn, f_hse_FORW_class=fh, f_hse_NFW_class=fhn, transfers=tr, law=law, wl_H20=wl, wl_H20_class=wlc, wl_LC2=lc2)

# ------------------------------------------------------------------ KA-4 footing identity
fid = all(GATE["canonical"]["class_"][k] == GATE["alt"]["class_"][k] for k in ("median", "lo", "hi")) and all(GATE["canonical"]["per_cluster"][n]["f_ret"] == GATE["alt"]["per_cluster"][n]["f_ret"] and GATE["canonical"]["Q"][n]["Q"] == GATE["alt"]["Q"][n]["Q"] for n in SIX)
KA4_PASS = KA4_PASS and fid
P(); P(f"KA-4 identities: M_dyn = (1+R) M_b -> f_ret {ka4_id:.15f}; F_beta 0.7/0.7 scaling returns the input; footings identical on gate and Q: {fid} -> {'PASS' if KA4_PASS else 'FAIL'}")
OUT["known_answers"].update(KA4_identity=ka4_id, KA4_footing_identity=bool(fid), KA4_pass=KA4_PASS)

# ------------------------------------------------------------------ MUTATE
MUT = {}
for f in FOOTS:
    base = GATE[f]
    m1 = gate(R=2 * R_COS)[0]; m2 = gate(scale=0.5)[0]
    rng = np.random.default_rng(SEED)
    while True:
        perm = rng.permutation(len(FIVE))
        if all(perm[i] != i for i in range(len(FIVE))): break
    ov = {n: HC[FIVE[perm[i]]]["M200"] for i, n in enumerate(FIVE)}
    m3rows = cluster_rows(FIVE, mass_override=ov); d3 = [m3rows[n]["f_ret"] - base["per_cluster"][n]["f_ret"] for n in FIVE]
    rms3 = float(np.sqrt(np.mean(np.square(np.clip(d3, -1e3, 1e3)))))
    m4rows = cluster_rows(SIX, mass_override={n: base["Q"][n]["M_FORW"] for n in SIX}); d4 = max(abs(m4rows[n]["f_ret"] / base["Q"][n]["f_hse_FORW"] - 1) for n in SIX)
    MUT[f] = dict(M1=dict(**m1, bites=m1["label"] == "ABOVE THE CEILING"), M2=dict(**m2, bites=m2["label"] == "ABOVE THE CEILING"),
                  M3=dict(permutation=[FIVE[j] for j in perm], per={n: m3rows[n]["f_ret"] for n in FIVE}, rms_shift=rms3, bites=bool(rms3 >= 0.10)),
                  M4=dict(max_rel_diff=d4, bites=bool(d4 <= 1e-12)))
    PM(f"[{f}] M1 R x 2: class {m1['median']:.3f} [{m1['lo']:.3f}, {m1['hi']:.3f}] {m1['label']} -> {'bites' if MUT[f]['M1']['bites'] else 'DOES NOT BITE'}")
    PM(f"[{f}] M2 F_beta 0.35: class {m2['median']:.3f} [{m2['lo']:.3f}, {m2['hi']:.3f}] {m2['label']} -> {'bites' if MUT[f]['M2']['bites'] else 'DOES NOT BITE'}")
    PM(f"[{f}] M3 caustic masses permuted ({', '.join(f'{a}<-{b}' for a, b in zip(FIVE, MUT[f]['M3']['permutation']))}): per-cluster f_ret rms shift {rms3:.3f} (line 0.10) -> {'bites' if MUT[f]['M3']['bites'] else 'DOES NOT BITE'}")
    PM(f"[{f}] M4 M_dyn = M_FORW at HeCS R200: max rel. diff from section 4's hydrostatic f_ret {d4:.1e} -> {'reproduces' if MUT[f]['M4']['bites'] else 'DOES NOT REPRODUCE'}")

# ------------------------------------------------------------------ labels
P(); P("LABELS (frozen vocabulary)")
LAB = {}
for f in FOOTS:
    g = GATE[f]; m = MUT[f]
    if not (KA1_PASS and KA2_PASS and ka3["pass"]): lab = "NO VERDICT"
    elif not (m["M1"]["bites"] and m["M2"]["bites"]): lab = "NOT EVALUABLE"
    else: lab = g["class_"]["label"] + (" [CALIBRATION-DEPENDENT]" if g["calibration_dependent"] else "")
    per_lab = {n: g["per_cluster"][n]["label"] for n in FIVE}
    against = (lab.startswith("ABOVE")) or any(v == "ABOVE THE CEILING" for v in per_lab.values())
    LAB[f] = dict(label=lab, per_cluster=per_lab, A2255_bracket=g["per_cluster"]["A2255"]["label"], Q_reading=g["Q_class"]["label"], counts_against_form_B=bool(against),
                  per_cluster_labels_evaluable=bool(m["M3"]["bites"]))
    P(f"  [{f}] FROZEN class: {lab}; per cluster: " + ", ".join(f"{n} {v}" for n, v in per_lab.items()) + f"; A2255 (bracket) {LAB[f]['A2255_bracket']}; Q: {LAB[f]['Q_reading']};"
      f" counts against form B: {'YES' if against else 'no'}")
    # AMENDMENT A1 (post hoc, 4010867a6f): KA-3 by name + z with the centre offset printed; A85 tagged; brackets without A85
    ka3a1 = bool(ka3["n_rows"] == 227 and all(v["by_name"] == 1 for v in ka3["matches"].values()) and all(abs(HC[n]["z"] - PROF[n]["z"]) <= 0.01 for n in SIX))
    if not (KA1_PASS and KA2_PASS and ka3a1): la = "NO VERDICT"
    elif not (m["M1"]["bites"] and m["M2"]["bites"]): la = "NOT EVALUABLE"
    else: la = g["class_"]["label"] + (" [CALIBRATION-DEPENDENT]" if g["calibration_dependent"] else "") + " (A85 tagged [CENTRE OFFSET 9.5'])"
    noA = ["A1795", "A2029", "A2142", "ZW1215"]; b5 = class_stat([g["per_cluster"][n]["f_ret"] for n in noA + ["A2255"]]); b4 = class_stat([g["per_cluster"][n]["f_ret"] for n in noA])
    b5c = {k: class_stat([cluster_rows(noA + ["A2255"], scale=s_)[n]["f_ret"] for n in noA + ["A2255"]]) for k, s_ in (("x0.9", 0.9), ("x1.1", 1.1))}
    against_a1 = la.startswith("ABOVE") or any(per_lab[n] == "ABOVE THE CEILING" for n in noA)
    LAB[f]["A1"] = dict(KA3_A1_pass=ka3a1, label=la, without_A85_with_A2255=b5, without_A85_with_A2255_calib=b5c, without_A85_measured_only=b4, counts_against_form_B=bool(against_a1))
    P(f"  [{f}] A1 (post hoc) class: {la}; counts against form B: {'YES' if against_a1 else 'no'}")
    P(f"      bracket without A85, with A2255 (5): {b5['median']:.3f} [{b5['lo']:.3f}, {b5['hi']:.3f}] {b5['label']} (x0.9 {b5c['x0.9']['label']}, x1.1 {b5c['x1.1']['label']});"
      f" without A85, measured stars only (4): median {b4['median']:.3f} -> {b4['label']}")
OUT["footings"] = {f: dict(gate=GATE[f], labels=LAB[f]) for f in FOOTS}; OUT["mutate"] = MUT; OUT["runtime_s"] = time.time() - T0
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): v = float(o); return v if math.isfinite(v) else str(v)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(OUT), open(os.path.join(HERE, "xcv1.json"), "w"), indent=1)
json.dump(clean(MUT), open(os.path.join(HERE, "xcv1_MUTATE.json"), "w"), indent=1)
P(f"runtime {time.time() - T0:.1f} s. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
open(os.path.join(HERE, "xcv1.out"), "w").write("\n".join(L) + "\n"); open(os.path.join(HERE, "xcv1_MUTATE.out"), "w").write("\n".join(LM_) + "\n")
