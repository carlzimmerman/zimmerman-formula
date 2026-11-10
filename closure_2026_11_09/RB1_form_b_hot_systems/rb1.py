#!/usr/bin/env python3
"""RB1 (FROZEN_CRITERIA.md, ef53f5512f): form B on the hot systems. TEST lane; relabels nothing, adopts nothing.
Form B: M_dyn = M_b,obs + M_cold, M_cold = R x (baryons that fell in) >= R x M_b,obs; f_ret = R M_b / (M_dyn - M_b) <= 1 at the edge.
Gate 1 conservation (one-sided), gate 2 trend with depth, gate 3 X-COP radial shape (ZN4 native profile), gate 4 the Bullet
(UX6's model as DB1's child ran it, copied here). Known answers KA-1..KA-5; MUTATE M1..M4 written to rb1_MUTATE.out / .json.
Other lanes' code is COPIED (not imported); their folders are read only.
    python3 rb1.py   -> rb1.json / rb1.out, rb1_MUTATE.json / rb1_MUTATE.out
kappa = 1/2 FITTED; not theory closed. Relabels nothing."""
import os, sys, json, math, csv, time, warnings, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from astropy.io import fits
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data"); RB = os.path.join(REPO, "rebuild_2026_10_22")
CRIT = "ef53f5512f"; T0 = time.time(); SEED = 1109; NBOOT = 10000
L, LM_ = [], []
def P(s=""): print(s, flush=True); L.append(str(s))
def PM(s=""): print("[MUTATE] " + str(s), flush=True); LM_.append(str(s))

# ------------------------------------------------------------------ constants (PD1's values)
G, MS, PC = 6.6743e-11, 1.98892e30, 3.0857e16; KPC = 1e3 * PC; MPC = 1e6 * PC; G_KPC = 4.3009172706e-6
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}; FOOTS = ("canonical", "alt")
R_COS, R_BR = 5.41, 5.562
def glaw(g, a0): g = np.asarray(g, float); return 0.5 * g + np.sqrt(0.25 * g * g + a0 * np.maximum(g, 0.0))
def Mph(r, Mb, a0):
    if r <= 0: return 0.0
    y = G * Mb / r ** 2 / a0; return Mb * (math.sqrt(0.25 + 1.0 / y) - 0.5)
def fret(Mb, Md, R=R_COS):
    Mb = np.asarray(Mb, float); Md = np.asarray(Md, float); d = Md - Mb
    return np.where(d > 0, R * Mb / np.where(d > 0, d, 1.0), np.inf)
def li(r, m, t):
    """log-log interpolation inside the tabulated range, nan outside (QX5's / HL3's li)."""
    r = np.asarray(r, float); m = np.asarray(m, float); t = float(t)
    if t < r[0] or t > r[-1]: return float("nan")
    return float(10 ** np.interp(math.log10(t), np.log10(r), np.log10(m)))
def kvm18(M500): return 1.7e12 * (np.asarray(M500, float) / 1e14) ** 0.60     # Kravtsov, Vikhlinin & Meshcheryakov 2018 (stated import)

# ------------------------------------------------------------------ loaders: Lovisari+15 groups (as QX5's groups(), errors kept)
def load_lovisari():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv")) if not l.startswith("#")]
    hdr, rows = rows[0], rows[1:]; out = []
    for r in rows:
        d = dict(zip(hdr, r))
        out.append(dict(name=d["name"], z=float(d["z"]), kT=float(d["kT_keV"]), R5=float(d["R500_kpc"]), R25=float(d["R2500_kpc"]),
                        M5=float(d["M500_1e13"]) * 1e13, eM5=float(d["eM500"]) * 1e13, M25=float(d["M2500_1e13"]) * 1e13, eM25=float(d["eM2500"]) * 1e13,
                        g5=float(d["Mgas500_1e12"]) * 1e12, eg5=float(d["eMgas500"]) * 1e12, g25=float(d["Mgas2500_1e12"]) * 1e12, eg25=float(d["eMgas2500"]) * 1e12))
    return out
LOV = load_lovisari()

# ------------------------------------------------------------------ loaders: X-COP (HL3's builder, restated; errors kept)
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
             z=R5J[name]["z"], M500_json=R5J[name]["M500"] * 1e14, stars=st is not None, ra=ra_, dec=de_, hm_raw=hm, gas_raw=gas)
    if st is not None:
        sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float); sL = np.array(st["MSTAR_LO"], float); sH = np.array(st["MSTAR_HI"], float)
        oks = np.isfinite(sM) & (sM > 0) & (sr > 0); d["sr"], d["sM"], d["sL"], d["sH"] = sr[oks], sM[oks], sL[oks], sH[oks]
    PROF[name] = d
WITH = [n for n in XN if PROF[n]["stars"]]; WITHOUT = [n for n in XN if not PROF[n]["stars"]]
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
X_PRIM = [p for p in HYD if p["measured"]]

# QX5's X-COP points (PD1's KA): x in (0.1, 0.2, 0.3, 0.5, 0.7) x the hydro header R500, clusters with a stellar file; Mb_last
XS5 = (0.1, 0.2, 0.3, 0.5, 0.7); XC5 = []
for name in WITH:
    d = PROF[name]; hm = d["hm_raw"]; hr = np.array(hm["RADIUS"], float); hMr = np.array(hm["M_FORW"], float); r500 = float(d["r500_fits"])
    gas = d["gas_raw"]; grr = np.array(gas["RADIUS"], float) * r500; gMr = np.array(gas["MGAS"], float)
    with fits.open(os.path.join(XD, name, f"{name}_mstar.fits")) as h: st = h[2].data.copy()
    srr = np.array(st["RADIUS"], float); sMr = np.array(st["MSTAR"], float); Mb_last = None
    for t in hr[::-1]:
        mg, ms = li(grr, gMr, t), li(srr, sMr, t)
        if np.isfinite(mg) and np.isfinite(ms): Mb_last = (mg + ms, t); break
    for x in XS5:
        r = x * r500; mh = li(hr, hMr, r); mg = li(grr, gMr, r); ms = li(srr, sMr, r); em = li(hr, np.array(hm["EM_FORW"], float), r)
        if np.all(np.isfinite([mh, mg, ms])): XC5.append(dict(name=name, r_kpc=r, M_obs=mh, M_b=mg + ms, M_gas=mg, eM=em, Mb_last=Mb_last))

# ------------------------------------------------------------------ loaders: KT2017 groups (HG1's builder, copied; eRASS1 match vectorised, same rule)
C_KMS = 299792.458; ERASS = os.path.join(os.path.dirname(REPO), "_external_data", "cfg687_inputs", "erass1_main.tsv")
RA_P, DE_P, L_NCP = np.radians(192.85948), np.radians(27.12825), np.radians(122.93192)
def galactic(ra, de):
    ra, de = np.radians(ra), np.radians(de)
    sb = np.sin(de) * np.sin(DE_P) + np.cos(de) * np.cos(DE_P) * np.cos(ra - RA_P); b = np.arcsin(np.clip(sb, -1, 1))
    y = np.cos(de) * np.sin(ra - RA_P); x = np.sin(de) * np.cos(DE_P) - np.cos(de) * np.sin(DE_P) * np.cos(ra - RA_P)
    l = (L_NCP - np.arctan2(y, x)) % (2 * np.pi); return np.degrees(l), np.degrees(b)
def vizier_rows(path):
    rows = [l.rstrip('\n').split('\t') for l in open(path) if l.strip() and not l.startswith('#')]; return rows[0], rows[3:]
def load_groups():
    h, rows = vizier_rows(os.path.join(DATA, 'kt2017_groups.tsv')); g = {}
    for r in rows:
        try: g[int(r[0])] = dict(Nm=int(r[1]), sigma=float(r[2]))
        except ValueError: continue
    h, rows = vizier_rows(os.path.join(DATA, 'kt2017_galaxies.tsv')); mem = {}
    for r in rows:
        try: pgc, ra, de, hrv, ks, pgc1 = int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[5])
        except ValueError: continue
        mem.setdefault(pgc1, []).append((pgc, ra, de, hrv, ks))
    return g, mem
def load_erass():
    out = []
    for l in open(ERASS):
        r = l.rstrip('\n').split('\t')
        try: ra, de, z, mg, r5 = float(r[1]), float(r[2]), float(r[3]), float(r[5]), float(r[8])
        except (ValueError, IndexError): continue
        if mg > 0 and r5 > 0: out.append((r[0].strip(), ra, de, z, mg * 1e11, r5 / 1e3))
    return out
def sep_rad(ra1, de1, ra2, de2):
    ra1, de1, ra2, de2 = map(np.radians, (ra1, de1, ra2, de2))
    c = np.sin(de1) * np.sin(de2) + np.cos(de1) * np.cos(de2) * np.cos(ra1 - ra2); return np.arccos(np.clip(c, -1, 1))
def beta_mass_fraction(r, r500, rc_f=0.15, beta=2 / 3):
    def m(R_):
        x = np.linspace(0, R_, 4001); rc = rc_f * r500; return TRAPZ(4 * np.pi * x ** 2 * (1 + (x / rc) ** 2) ** (-1.5 * beta), x)
    return m(r) / m(r500)
def build_kt(groups, mem, erass, nm_min=5, h0=67.70, ups=0.6):
    rows, drops = [], {}; EN = [e[0] for e in erass]; ERA = np.array([e[1] for e in erass]); EDE = np.array([e[2] for e in erass]); EZ = np.array([e[3] for e in erass])
    EMG = np.array([e[4] for e in erass]); ER5 = np.array([e[5] for e in erass])
    def drop(k): drops[k] = drops.get(k, 0) + 1
    for pgc1, gi in groups.items():
        if gi['Nm'] < nm_min or gi['sigma'] <= 0: drop('Nm/sigma'); continue
        ms = [m for m in mem.get(pgc1, []) if np.isfinite(m[4])]
        if len(ms) < 5: drop('<5 members with Ks'); continue
        prin = next((m for m in ms if m[0] == pgc1), None)
        if prin is None: drop('no principal galaxy'); continue
        hrv = prin[3]
        if hrv < 600: drop('HRV<600'); continue
        l, b = galactic(prin[1], prin[2])
        if not (179.94 <= l <= 359.94 and abs(b) >= 10): drop('outside eRASS1 footprint'); continue
        d = hrv / h0
        lk = np.array([10 ** (-0.4 * (m[4] - 5 * np.log10(d * 1e6) + 5 - 3.28)) for m in ms])
        ra = np.array([m[1] for m in ms]); de = np.array([m[2] for m in ms]); cra, cde = np.average(ra, weights=lk), np.average(de, weights=lk)
        rp = sep_rad(ra, de, cra, cde) * d; Rh = np.median(rp); r = 4 / 3 * Rh
        if r <= 0: drop('zero radius'); continue
        mstar = ups * lk.sum(); cand = np.nonzero(np.abs(C_KMS * EZ - hrv) <= 1500)[0]; best = None
        if cand.size:
            s = sep_rad(prin[1], prin[2], ERA[cand], EDE[cand]) * d; okc = s <= 0.5
            if okc.any():
                k = cand[okc][int(np.argmin(s[okc]))]; best = (float(s[okc].min()), EN[k], float(EMG[k]), float(ER5[k]))
        if best: mg500, r500 = best[2], best[3]; mgas = mg500 * beta_mass_fraction(r, r500); flag = 'BRIGHT'
        else: mgas = 0.0; flag = 'FAINT'; r500 = None
        rows.append(dict(name=str(pgc1), flag=flag, sigma=gi['sigma'], Nm=gi['Nm'], r_mpc=r, mstar=mstar, mgas=mgas, erass=best[1] if best else None, r500=r500,
                         M_dyn=3 * (gi['sigma'] * 1e3) ** 2 * r * MPC / G / MS))
    return rows, drops
KTG, KTM = load_groups(); KT, KTD = build_kt(KTG, KTM, load_erass())
GA1T = {t["group"]: t for t in json.load(open(os.path.join(RB, "GA1_group_gas_audit", "ga1_group_gas_audit_results.json")))["runs"]["PRIMARY"]["table"]}

# ------------------------------------------------------------------ loaders: GS4 compilation (FR1's line-H catalogues), reported ladder
def load_gs4():
    out = []
    for r in csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_inputs.csv"))):
        if r["cat"] not in ("L20", "L15", "S09", "L13"): continue
        try: M, Mg, z, ra, de = float(r["M500"]), float(r["Mgas"]), float(r["z"]), float(r["ra"]), float(r["dec"])
        except ValueError: continue
        if M > 0 and Mg > 0 and np.isfinite(M + Mg + ra + de + z): out.append(dict(cat=r["cat"], name=r["name"], M500=M, Mg=Mg, z=z, ra=ra, dec=de))
    xp = [(PROF[n]["ra"], PROF[n]["dec"], PROF[n]["z"]) for n in XN]
    def near(a, b): return math.degrees(float(sep_rad(a[0], a[1], b[0], b[1]))) * 60 <= 6.0 and abs(a[2] - b[2]) <= 0.02
    keep = [o for o in out if not any(near((o["ra"], o["dec"], o["z"]), x) for x in xp)]; nX = len(out) - len(keep)
    par = list(range(len(keep)))
    def fnd(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i in range(len(keep)):
        for j in range(i + 1, len(keep)):
            if near((keep[i]["ra"], keep[i]["dec"], keep[i]["z"]), (keep[j]["ra"], keep[j]["dec"], keep[j]["z"])): par[fnd(i)] = fnd(j)
    grp = {}
    for i in range(len(keep)): grp.setdefault(fnd(i), []).append(keep[i])
    merged = [dict(M500=10 ** float(np.median([np.log10(o["M500"]) for o in g])), Mg=10 ** float(np.median([np.log10(o["Mg"]) for o in g])), n=len(g), cats=sorted({o["cat"] for o in g})) for g in grp.values()]
    return merged, len(out), nX
GS4, GS4_N, GS4_NX = load_gs4()

# ------------------------------------------------------------------ PD1's machinery (copied from pd1.py, pd1_a1.py, ss1_core.halo) for KA-1
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
class BG:
    def __init__(s, OB, OD, h, OR_h2=4.15e-5):
        s.OB, s.OD, s.h = OB, OD, h; s.R = OD / OB; s.Om = (OB + OD) / h ** 2; s.Orr = OR_h2 / h ** 2; s.OL = 1 - s.Om - s.Orr
        s.H0s = 100 * h * 1e3 / MPC; s.RHOC = 3 * s.H0s ** 2 / (8 * math.pi * G); s.RHO_M0 = s.Om * s.RHOC; s.RHO_D0 = OD / h ** 2 * s.RHOC
    def Hs(s, a): return s.H0s * math.sqrt(s.Orr / a ** 4 + s.Om / a ** 3 + s.OL)
    def shell(s, xL, dM, a0, a_end=1.0):
        AI = 1 / 1001.0
        def rhs(t, y):
            a, r, v = y; acc = -(4 * math.pi * G / 3) * (s.RHO_M0 / a ** 3 + 2 * s.Orr * s.RHOC / a ** 4 - 2 * s.OL * s.RHOC) * r; gN = G * dM / r ** 2
            acc -= (float(glaw(gN, a0)) if a0 > 0 else gN); return [a * s.Hs(a), v, acc]
        def turn(t, y): return y[2]
        turn.terminal, turn.direction = True, -1
        def end(t, y): return y[0] - a_end
        end.terminal = True
        r0 = xL * AI; so = solve_ivp(rhs, (0, 3e18), [AI, r0, s.Hs(AI) * r0], events=(turn, end), rtol=1e-9, atol=[1e-12, r0 * 1e-12, 1e-6], method="DOP853")
        if so.t_events[0].size: return "early", so.y_events[0][0]
        return "late", so.y_events[1][0] if so.t_events[1].size else so.y[:, -1]
    def r_ta(s, dM, a0, a_end=1.0):
        lo, hi = math.log(1e-6 * MPC), math.log(1e3 * MPC)
        for _ in range(60):
            mid = 0.5 * (lo + hi); kind, st = s.shell(math.exp(mid), dM, a0, a_end)
            if kind == "early": lo = mid
            else: hi = mid
            if hi - lo < 1e-7: break
        kind, st = s.shell(math.exp(hi), dM, a0, a_end); return float(st[1]), math.exp(hi)
def footing_bg(f): th = Q15["footings"][f]["main"]["theta"]; return BG(th["omega_b"], th["omega_d"], float(Q15["footings"][f]["main"]["h"]))
RHOC0_PER_H2 = 277.536627
def rho_crit(z, h, Om, Or=0.0): E2 = Om * (1 + z) ** 3 + Or * (1 + z) ** 4 + (1.0 - Om - Or); return RHOC0_PER_H2 * h * h * E2
def duffy_c200(M200, z, h): return 5.71 * (M200 / (2e12 / h)) ** -0.084 * (1 + z) ** -0.47
def halo_nfw(M200, z, h, Om):
    rc = rho_crit(z, h, Om); R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); return dict(M200=M200, R200=R200, c200=duffy_c200(M200, z, h))
LMT = np.arange(7.0, 15.001, 0.25)
def rms_table(B, z=0.0): return np.array([B.r_ta(10 ** m * MS * (1 + B.R), 0.0, 1 / (1 + z))[0] / MPC for m in LMT])
VST = {"canonical": 265.8, "alt": 288.1}; CS_IGM = 15.0
def pd1_system(B, f, rmsT, Msys, share_mult=5.41, fcpre=1.0, z=0.0):
    a0 = A0[f]; m = math.log10(Msys); share = share_mult * Msys; rms = float(10 ** np.interp(m, LMT, np.log10(rmsT))) * MPC
    H = halo_nfw(Msys + share, z, B.h, B.Om); v = math.sqrt(G_KPC * H["M200"] / H["R200"])
    fc = fcpre * (1 - (VST[f] / v) ** 2) if v > VST[f] else 0.0; W = 1.5 * v * v / (1.5 * v * v + CS_IGM ** 2)
    c = H["c200"]; rs = H["R200"] / c; mu = lambda x: np.log1p(x) - x / (1 + x)
    core = lambda r_kpc: fc * share * float(mu(min(r_kpc, H["R200"]) / rs) / mu(c))
    E = (1 - fc) * share; mph_ms = W * Mph(rms, Msys * MS, a0) / MS
    rt = brentq(lambda r: W * Mph(r, Msys * MS, a0) / MS - E, 1e-6 * KPC, rms) if mph_ms > E else rms
    return dict(share=share, R_ms=rms, v_vir=v, f_core=fc, W=W, core=core, E=E, R_trunc=rt, remainder=max(0.0, E - mph_ms), R200_kpc=H["R200"], c200=c)
def pd1_rem_in(S, r): return S["remainder"] * min(r, S["R_ms"]) / S["R_ms"] if S["remainder"] > 0 else 0.0
def pd1_g_sys(S, a0, r, Mb_r, Msys):
    gN = G * Mb_r * MS / r ** 2
    if r < S["R_trunc"]: gph = S["W"] * (float(glaw(gN, a0)) - gN)
    else: gt = G * Msys * MS / S["R_trunc"] ** 2; gph = S["W"] * (float(glaw(gt, a0)) - gt) * (S["R_trunc"] / r) ** 2
    return gN + gph + G * (S["core"](r / KPC) * MS + pd1_rem_in(S, r)) / r ** 2

# ------------------------------------------------------------------ UX6's Bullet model (copied) + DB1's galaxy-traced extra (copied)
BG_G = 6.674e-11; BKPC = 3.0857e19; BMSUN = 1.989e30
GAS = [(2.0e14, 565.0, 190.0, 90.0), (1.5e13, 505.0, 525.0, 120.0), (1.5e13, 90.0, 670.0, 170.0), (-6.8e12, 70.0, 670.0, 170.0)]
GAL = [(1.196e13, 470.0, 0.0, 0.0), (4.0e12, 245.0, 820.0, 220.0)]
BCG1 = np.array([0.0, 0.0]); BCG3 = np.array([820.0, 220.0]); GASM = np.array([190.0, 90.0]); GASB = np.array([670.0, 170.0])
OBS300 = {"BCG1": 3.5e14, "BCG3": 2.3e14}; PAIRS = {"main": (BCG1, GASM), "sub": (BCG3, GASB)}; SIG_CRIT = 1.827e9; Z_BOX = 18000.0
SIG_DELTA = math.sqrt((1 / 8) ** 2 + 0.15 ** 2); SIG_O3 = 0.15; DB1_OBS = [3.5e14, 2.3e14]; DB1_SIG = 0.15; ZL = 2.0
GROUPS = [(BCG1, [0], [0]), (BCG3, [1, 2, 3], [1])]; OWN = {0: 0, 1: 1}
MST = [sum(GAL[i][0] for i in ii) for (_, _, ii) in GROUPS]; MGJ = [sum(GAS[i][0] for i in ig) for (_, ig, _) in GROUPS]; MGAS = sum(c[0] for c in GAS)
def blaw(g, a): g = np.asarray(g, float); return np.where(g > 0, 0.5 * g + np.sqrt(0.25 * g * g + a * g), g)
def fld(X, Y, Z, c):
    M, a, xc, yc = c; dx = X - xc; dy = Y - yc; dz = Z
    f = -BG_G * M * BMSUN / ((dx * dx + dy * dy + dz * dz + a * a) ** 1.5 * BKPC ** 3) * BKPC; return f * dx, f * dy, f * dz
def ctx(X, Y, Z):
    C = dict(X=X, Y=Y, Z=Z, gas=[fld(X, Y, Z, c) for c in GAS]); st = [fld(X, Y, Z, c) for c in GAL]; C["st"] = tuple(sum(v[i] for v in st) for i in range(3)); return C
def zgrid(Z, n_in=500, n_out=500, z_in=1500.0): return np.concatenate([np.linspace(0.0, z_in, n_in + 1), np.geomspace(z_in, Z, n_out + 1)[1:]])
ZS = zgrid(Z_BOX); ZM = zgrid(6000.0, n_in=140, n_out=110, z_in=1200.0)
def sig_pl(D, M, a): return M * a * a / (math.pi * (D * D + a * a) ** 2)
def M2D(x0, y0, Rr, plum, nrho=400, nphi=720):
    rho = np.linspace(0.0, Rr, nrho + 1); phi = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi
    X = x0 + rho[:, None] * np.cos(phi)[None, :]; Y = y0 + rho[:, None] * np.sin(phi)[None, :]; S = np.zeros_like(X)
    for M, a, xc, yc in plum: S += sig_pl(np.sqrt((X - xc) ** 2 + (Y - yc) ** 2), M, a)
    return float(TRAPZ(np.sum(S, axis=1) * (2 * math.pi / nphi) * rho, rho))
def plum_of(sp): sc = sp.get("scale", 1.0); return [(sc * M, a, x, y) for M, a, x, y in GAS] + GAL
def mk_extra(Rs, on):
    def extra(sp, Cc, reg=True):
        a0 = sp["a0"]; gv = tuple(sum(q[i] for q in Cc["gas"]) for i in range(3)); gb = [gv[i] + Cc["st"][i] for i in range(3)]
        if reg: gb[1] = gb[1] + a0 / 1000.0
        if on == "gas":
            s = sum(Rs[j] * MST[j] for j in range(len(MST))) / MGAS; cb = [s * gv[i] for i in range(3)]
        else:
            cb = [0.0, 0.0, 0.0]
            for i, c in enumerate(GAL):
                w = Rs[OWN.get(i, 0)]
                if w: fq = fld(Cc["X"], Cc["Y"], Cc["Z"], c); cb = [cb[q] + w * fq[q] for q in range(3)]
        tot = [gb[i] + cb[i] for i in range(3)]; g = np.sqrt(tot[0] ** 2 + tot[1] ** 2 + tot[2] ** 2); m = blaw(g, a0) / np.maximum(g, 1e-300)
        return tuple(tot[i] * m - gb[i] for i in range(3))
    return extra
EXTRA = {"f": None}
def surface(specs, x0, y0, Rr, nphi=360, nrho=200):
    phi = (np.arange(nphi) + 0.5) * 2 * math.pi / nphi; CP, SP = np.cos(phi), np.sin(phi)
    X = (x0 + Rr * CP)[:, None] * np.ones((1, len(ZS))); Y = (y0 + Rr * SP)[:, None] * np.ones((1, len(ZS))); Zg = np.broadcast_to(ZS[None, :], X.shape)
    C = ctx(X, Y, Zg); side = {}
    for n, sp in specs.items():
        e = EXTRA["f"](sp, C); side[n] = 2.0 * TRAPZ(np.sum(e[0] * CP[:, None] + e[1] * SP[:, None], axis=0) * (2 * math.pi / nphi) * Rr, ZS)
    rho = np.linspace(0.0, Rr, nrho + 1); Xc = x0 + rho[:, None] * CP[None, :]; Yc = y0 + rho[:, None] * SP[None, :]
    C = ctx(Xc, Yc, np.full_like(Xc, Z_BOX)); out = {}
    for n, sp in specs.items():
        e = EXTRA["f"](sp, C); caps = 2.0 * TRAPZ(np.sum(e[2], axis=1) * (2 * math.pi / nphi) * rho, rho); out[n] = -(side[n] + caps) * BKPC ** 2 / (4 * math.pi * BG_G) / BMSUN
    return out
BXS = np.arange(-500.0, 1400.0 + 1e-9, 10.0); BYS = np.arange(-400.0, 700.0 + 1e-9, 10.0); XX, YY = np.meshgrid(BXS, BYS, indexing="ij")
def maps(specs, h=2.0):
    S = {n: np.zeros_like(XX) for n in specs}
    for j0 in range(0, len(BYS), 6):
        ys = BYS[j0:j0 + 6]; X, Y, Z = np.meshgrid(BXS, ys, ZM, indexing="ij"); div = {n: 0.0 for n in specs}
        for ax, (dx, dy, dz) in enumerate(((h, 0, 0), (0, h, 0), (0, 0, h))):
            for sgn in (1.0, -1.0):
                C = ctx(X + sgn * dx, Y + sgn * dy, Z + sgn * dz)
                for n, sp in specs.items(): div[n] = div[n] + sgn * EXTRA["f"](sp, C)[ax]
        for n in specs: S[n][:, j0:j0 + 6] = 2.0 * TRAPZ(-div[n] / (2 * h) / (4 * math.pi * BG_G) * BKPC ** 2 / BMSUN, ZM, axis=2)
    for n, sp in specs.items():
        for M, a, xc, yc in plum_of(sp): S[n] += sig_pl(np.hypot(XX - xc, YY - yc), M, a)
    return S
def peak(S, A, B):
    mid = 0.5 * (A + B); w = np.hypot(XX - mid[0], YY - mid[1]) <= 350.0
    i = int(np.argmax(np.where(w, S, -np.inf))); a, b = np.unravel_index(i, S.shape)
    edge = not (0 < a < S.shape[0] - 1 and 0 < b < S.shape[1] - 1) or not w[a - 1:a + 2, b - 1:b + 2].all()
    lm = (not edge) and S[a, b] >= S[a - 1:a + 2, b - 1:b + 2].max() and (S[a - 1:a + 2, b - 1:b + 2] == S[a, b]).sum() == 1
    return np.array([XX[a, b], YY[a, b]]), bool(lm)
def observe(S, m):
    o = {}
    for k, (bc, gc) in PAIRS.items():
        pk, lm = peak(S, bc, gc); dg = float(np.hypot(*(pk - gc))); db = float(np.hypot(*(pk - bc))); sep = float(np.hypot(*(bc - gc)))
        o[k] = dict(peak=pk.tolist(), local_max=lm, d_gas=dg, d_bcg=db, delta=dg / sep, Z=(dg / sep - 1) / SIG_DELTA, guard=bool(lm and db < dg),
                    dkappa=(m[f"bcg_{k}"] - m[f"gas_{k}"]) / (math.pi * 1e4) / SIG_CRIT)
    o["M300"] = [m["BCG1"], m["BCG3"]]; o["ZO3"] = [(m["BCG1"] / OBS300["BCG1"] - 1) / SIG_O3, (m["BCG3"] / OBS300["BCG3"] - 1) / SIG_O3]
    pos = [not (o[k]["guard"] and abs(o[k]["Z"]) <= 3 and o[k]["dkappa"] > 0) for k in PAIRS]; o["pos_or_sign_fail"] = bool(any(pos))
    mass = any(abs(z) > 3 for z in o["ZO3"]); o["mass_fail"] = bool(mass)
    o["cls"] = "FAIL" if (o["pos_or_sign_fail"] or mass) else ("PASS" if all(abs(o[k]["Z"]) <= 2 for k in PAIRS) and all(abs(z) <= 2 for z in o["ZO3"]) else "TENSION")
    return o
APS = dict(BCG1=(BCG1, 300.0), BCG3=(BCG3, 300.0), P1=(BCG1, 250.0), P3=(BCG3, 250.0), bcg_main=(BCG1, 100.0), gas_main=(GASM, 100.0), bcg_sub=(BCG3, 100.0), gas_sub=(GASB, 100.0))
def brun(specs):
    sf = {a: surface(specs, *c, Rr) for a, (c, Rr) in APS.items()}; S = maps(specs); res = {}
    for n, sp in specs.items():
        pl = plum_of(sp); m = {a: M2D(*c, Rr, pl) + sf[a][n] for a, (c, Rr) in APS.items()}; res[n] = (S[n], m)
    return res
def bullet_row(a0, Rs, on="gal"):
    EXTRA["f"] = mk_extra(Rs, on); R_ = brun({"x": dict(form="CAND", k=0.0, a0=a0)}); o = observe(*R_["x"])
    zs = [(o["M300"][i] / DB1_OBS[i] - 1) / DB1_SIG for i in (0, 1)]; ok = o["cls"] != "FAIL" and all(abs(z) <= ZL for z in zs)
    return dict(label="PASS" if ok else "FAIL", cls=o["cls"], R=[float(x) for x in Rs], Mcold=[float(Rs[j] * MST[j]) for j in range(2)], M300=[float(x) for x in o["M300"]], ZM=zs,
                Zoff=[o["main"]["Z"], o["sub"]["Z"]], d_gal=[o["main"]["d_bcg"], o["sub"]["d_bcg"]], d_gas=[o["main"]["d_gas"], o["sub"]["d_gas"]],
                dkappa=[o["main"]["dkappa"], o["sub"]["dkappa"]], local_max=[o["main"]["local_max"], o["sub"]["local_max"]])

# ------------------------------------------------------------------ statistics
RNG = np.random.default_rng(SEED)
def fin(v): v = np.asarray(v, float); return np.where(np.isfinite(v), v, 1e9)
def class_stat(vals, seed=SEED):
    v = fin(vals); n = len(v)
    if n < 5: return dict(n=n, median=float(np.median(v)) if n else float("nan"), lo=float("nan"), hi=float("nan"), label="NOT EVALUABLE")
    rng = np.random.default_rng(seed); idx = rng.integers(0, n, size=(NBOOT, n)); meds = np.median(v[idx], axis=1)
    lo, hi = float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))
    return dict(n=n, median=float(np.median(v)), lo=lo, hi=hi, n_above1=int(np.sum(v > 1)), label="FAILS" if lo > 1 else "CONSISTENT")
def mc_above(Mb_parts, sig_parts, Md, sMd, R=R_COS, nd=4000, seed=SEED):
    """per-system P(f_ret > 1) with lognormal errors (ln sigma) on each baryon part and on M_dyn."""
    rng = np.random.default_rng(seed); Mb = sum(m * np.exp(s * rng.standard_normal(nd)) for m, s in zip(Mb_parts, sig_parts)); Md_ = Md * np.exp(sMd * rng.standard_normal(nd))
    return float(np.mean(fin(fret(Mb, Md_, R)) > 1))
def ols_boot(x, y, seed=SEED):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x); b = np.polyfit(x, y, 1)[0]
    rng = np.random.default_rng(seed); bs = []
    for _ in range(NBOOT):
        i = rng.integers(0, n, n)
        if np.ptp(x[i]) > 0: bs.append(np.polyfit(x[i], y[i], 1)[0])
    return dict(slope=float(b), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), n=n)
def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y)); return float(np.corrcoef(rx, ry)[0, 1])
EDGES = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]
def cl_bin_median(points, val, edges=EDGES, min_cl=0):
    names = sorted({p["name"] for p in points}); M = np.full((len(names), len(edges) - 1), np.nan)
    for i, nm in enumerate(names):
        for b in range(len(edges) - 1):
            v = [val(p) for p in points if p["name"] == nm and edges[b] <= p["x"] < edges[b + 1]]
            if v: M[i, b] = float(np.median(v))
    cnt = np.sum(np.isfinite(M), axis=0); med = np.nanmedian(M, axis=0)
    return med, cnt

RES = dict(criteria=CRIT, note="TEST lane; relabels nothing; adopts nothing; kappa = 1/2 FITTED; not theory closed", R=R_COS, R_bracket=R_BR, footings=A0)
MRES = dict(criteria=CRIT, note="MUTATE twins (deliberately wrong); kappa = 1/2 FITTED; not theory closed")
P(f"RB1 (criteria {CRIT}): form B on the hot systems. R = {R_COS} (bracket {R_BR}); footings canonical a0 {A0['canonical']:.4e}, alt {A0['alt']:.4e}, never pooled.")
P("kappa = 1/2 FITTED; not theory closed. Relabels nothing. Cold dark energy, never a particle.")

# ================================================================== KNOWN ANSWERS
P(); P("KNOWN ANSWERS")
KA = {}
# KA-5 parsers
n_b = sum(r["flag"] == "BRIGHT" for r in KT); KA["KA5"] = dict(lovisari=len(LOV), xcop=len(XN), xcop_stars=len(WITH), kt=len(KT), kt_bright=n_b, kt_faint=len(KT) - n_b,
    gs4_rows=GS4_N, gs4_xcop_removed=GS4_NX, gs4_merged=len(GS4))
KA["KA5"]["pass"] = bool(len(LOV) == 20 and len(XN) == 12 and len(WITH) == 7 and len(KT) == 190 and n_b == 14)
P(f"KA-5 parsers: Lovisari {len(LOV)} (20); X-COP {len(XN)} (12), with stars {len(WITH)} (7); KT2017 {len(KT)} / BRIGHT {n_b} / FAINT {len(KT) - n_b} (190 / 14 / 176) -> {'PASS' if KA['KA5']['pass'] else 'FAIL'}"
  f"; GS4 line-H rows {GS4_N}, X-COP removed {GS4_NX}, merged systems {len(GS4)} (reported)")
# KA-4 identities
fid = float(fret(1.0e14, (1 + R_COS) * 1.0e14)); KA["KA4"] = dict(fret_identity=fid)
# KA-2 TR1's fractions
TR1REF = {"canonical": [0.71, 0.66, 0.58, 0.46, 0.32], "alt": [0.68, 0.63, 0.54, 0.41, 0.26]}; KA["KA2"] = {}
def mlaw(p, a0): r = p["r_kpc"] * KPC; return float(glaw(G * p["M_bar"] * MS / r ** 2, a0)) * r ** 2 / G / MS
def tr1_frac(points, mx, mt, drop=True):
    """TR1's RESULT table (A1 KA-2b): per point l = log10(M_X / M_T), M_X <= 0 points dropped (drop=False: the -1.0 marker of TR1's rows),
    per-cluster per-bin median, median over clusters, 10^."""
    med, cnt = cl_bin_median(points, lambda p: math.log10(mx(p) / mt(p)) if mx(p) > 0 else (float("nan") if drop else -1.0)); return 10 ** med, cnt
def per_cluster_Q(points, val, edges=EDGES):
    out = {}
    for nm in sorted({p["name"] for p in points}):
        row = []
        for b in range(len(edges) - 1):
            v = [val(p) for p in points if p["name"] == nm and edges[b] <= p["x"] < edges[b + 1]]; row.append(float(np.median(v)) if v else float("nan"))
        out[nm] = row
    return out
def tr1_rows(f):
    """TR1's printed per-cluster tot rows, reading D (tr1.out, read only): log10 A + residual per bin."""
    Lr = open(os.path.join(REPO, "closure_2026_11_09", "TR1_cluster_tracer", "tr1.out")).read().splitlines(); i = next(k for k, l in enumerate(Lr) if l.startswith(f"== XCOP reading D [{f}]"))
    j = next(k for k in range(i, len(Lr)) if "tot per-cluster residuals" in Lr[k]); out = {}
    for l in Lr[j + 1:j + 8]:
        t = l.split(); A = float(t[2]); out[t[0]] = [math.log10(A) + float(v) if v != "--" else float("nan") for v in t[3:8]]
    return out
for f in FOOTS:
    mine = per_cluster_Q(X_PRIM, lambda p: math.log10((p["M_dyn"] - mlaw(p, A0[f])) / p["M_dyn"]) if p["M_dyn"] > mlaw(p, A0[f]) else -1.0); ref = tr1_rows(f)
    dmax = max(abs(mine[n][b] - ref[n][b]) for n in ref for b in range(5) if np.isfinite(ref[n][b])); nanok = all(np.isfinite(mine[n][b]) == np.isfinite(ref[n][b]) for n in ref for b in range(5))
    oka = bool(dmax <= 0.002 and nanok and set(mine) == set(ref))
    med, cnt = tr1_frac(X_PRIM, lambda p: p["M_dyn"] - mlaw(p, A0[f]), lambda p: p["M_dyn"]); mk, _ = tr1_frac(X_PRIM, lambda p: p["M_dyn"] - mlaw(p, A0[f]), lambda p: p["M_dyn"], drop=False)
    okb = bool(np.all(np.abs(med - np.array(TR1REF[f])) <= 0.0051))
    KA["KA2"][f] = dict(a_rows_max_dev_dex=dmax, a_pass=oka, b_fractions=med.tolist(), b_ref=TR1REF[f], b_pass=okb, marker_version=mk.tolist(), pass_=bool(oka and okb),
                        frozen_ka2_pass=bool(np.all(np.abs(mk - np.array(TR1REF[f])) <= 0.0051)), definition="A1: KA-2a TR1's per-cluster rows; KA-2b TR1's table with M_X <= 0 points dropped")
    P(f"KA-2a [{f}] TR1's per-cluster tot rows (log A + residual), 7 clusters x 5 bins: max dev {dmax:.4f} dex (line 0.002) -> {'PASS' if oka else 'FAIL'}")
    P(f"KA-2b [{f}] TR1's table, M_X <= 0 dropped: {' / '.join(f'{v:.3f}' for v in med)} (TR1 {' / '.join(f'{v:.2f}' for v in TR1REF[f])}) -> {'PASS' if okb else 'FAIL'}; "
      f"with the -1.0 marker (the frozen KA-2's reading) {' / '.join(f'{v:.3f}' for v in mk)} -> {'PASS' if KA['KA2'][f]['frozen_ka2_pass'] else 'FAIL'}")
# KA-1 PD1's bracket (share 5.41, full share in the core)
KA["KA1"] = {}; PD1REF = {"canonical": dict(xcop=0.019, g0=0, g1=9, m0=0.30, m1=0.04), "alt": dict(xcop=0.010, g0=0, g1=8, m0=0.31, m1=0.04)}
for f in FOOTS:
    B = footing_bg(f); a0 = A0[f]; T = rms_table(B, 0.0); d = []
    for name in sorted({z["name"] for z in XC5}):
        pts = [z for z in XC5 if z["name"] == name]; Msys = pts[0]["Mb_last"][0]; S = pd1_system(B, f, T, Msys)
        for z in pts:
            rm = z["r_kpc"] * KPC; g = pd1_g_sys(S, a0, rm, z["M_b"], Msys); d.append(math.log10(z["M_obs"] / (g * rm ** 2 / G / MS)))
    xm = float(np.mean(d)); o = {}
    for fst in (0, 1):
        npass = 0; med = []
        for gp in LOV:
            Msys = gp["g5"] * (1 + fst); S = pd1_system(B, f, T, Msys); ok_ = True
            for (rk, Mo, Mg, eM) in ((gp["R25"], gp["M25"], gp["g25"], gp["eM25"]), (gp["R5"], gp["M5"], gp["g5"], gp["eM5"])):
                rm = rk * KPC; g = pd1_g_sys(S, a0, rm, Mg * (1 + fst), Msys); dl = math.log10(Mo / (g * rm ** 2 / G / MS)); med.append(dl); ok_ &= abs(dl) <= 2 * eM / (Mo * math.log(10))
            npass += ok_
        o[fst] = (npass, float(np.median(med)))
    rf = PD1REF[f]; ok = bool(abs(xm - rf["xcop"]) <= 0.002 and o[0][0] == rf["g0"] and o[1][0] == rf["g1"] and abs(round(o[0][1], 2) - rf["m0"]) <= 0.0051 and abs(round(o[1][1], 2) - rf["m1"]) <= 0.0051)
    KA["KA1"][f] = dict(xcop_mean=xm, groups_npass=[o[0][0], o[1][0]], groups_median=[o[0][1], o[1][1]], ref=rf, pass_=ok)
    P(f"KA-1 [{f}] PD1 bracket (share 5.41, prefactor 1): X-COP mean {xm:+.4f} (PD1 {rf['xcop']:+.3f}); groups {o[0][0]}/{o[1][0]} of 20 (PD1 {rf['g0']}/{rf['g1']}), medians {o[0][1]:+.3f}/{o[1][1]:+.3f} (PD1 {rf['m0']:+.2f}/{rf['m1']:+.2f}) -> {'PASS' if ok else 'FAIL'}")
# KA-3 Bullet
t1 = time.time()
lawrow = {f: bullet_row(A0[f], [0.0, 0.0]) for f in FOOTS}
ROW_S0 = bullet_row(1e-30, [R_COS * (MST[j] + MGJ[j]) / MST[j] for j in range(2)])
ka3a = bool(abs(lawrow["canonical"]["ZM"][0] + 4.548) <= 0.01 and abs(lawrow["canonical"]["ZM"][1] + 4.540) <= 0.01)
ka3b = bool(abs(ROW_S0["ZM"][0] - 0.49) <= 0.02 and abs(ROW_S0["ZM"][1] + 2.58) <= 0.02 and abs(ROW_S0["d_gal"][0] - 14) <= 2 and abs(ROW_S0["d_gal"][1] - 22) <= 2
            and abs(ROW_S0["d_gas"][0] - 197) <= 2 and abs(ROW_S0["d_gas"][1] - 136) <= 2)
KA["KA3"] = dict(law_row={f: lawrow[f] for f in FOOTS}, S0_row=ROW_S0, a_pass=ka3a, b_pass=ka3b, seconds=time.time() - t1)
P(f"KA-3a law-only Bullet row Z {lawrow['canonical']['ZM'][0]:+.3f}, {lawrow['canonical']['ZM'][1]:+.3f} (DB1 -4.548, -4.540) -> {'PASS' if ka3a else 'FAIL'}; alt {lawrow['alt']['ZM'][0]:+.3f}, {lawrow['alt']['ZM'][1]:+.3f}")
P(f"KA-3b S0 = PD1 A2 galaxy-traced Newtonian row: M300 Z {ROW_S0['ZM'][0]:+.3f}, {ROW_S0['ZM'][1]:+.3f} (PD1 +0.49, -2.58); d_gal {ROW_S0['d_gal'][0]:.0f}/{ROW_S0['d_gal'][1]:.0f} (14/22), d_gas {ROW_S0['d_gas'][0]:.0f}/{ROW_S0['d_gas'][1]:.0f} (197/136) kpc; cls {ROW_S0['cls']} -> {'PASS' if ka3b else 'FAIL'} ({time.time() - t1:.0f} s for three rows)")

# ================================================================== GATE 1: conservation
P(); P("GATE 1, conservation (HARD, ONE-SIDED): class median f_ret at the outermost aperture, 95 % bootstrap over systems; FAILS iff lower bound > 1")
def g1_lov(R=R_COS, stars="kvm", Mpert=None):
    Mb = []; Md = []
    for g in LOV:
        s = {"kvm": kvm18(g["M5"]), "gas": 0.0, "kvm_x1.5": 1.5 * kvm18(g["M5"]), "kvm_/1.5": kvm18(g["M5"]) / 1.5, "eq_gas": g["g5"]}[stars]
        Mb.append(g["g5"] + float(s)); Md.append(g["M5"])
    Mb = np.array(Mb) if Mpert is None else Mpert(np.array(Mb)); return fret(Mb, np.array(Md), R), np.array(Mb), np.array(Md)
def xcop_last(names, at="last"):
    out = []
    for n in names:
        pts = [p for p in HYD if p["name"] == n]
        if at == "last": p = max(pts, key=lambda q: q["r_kpc"])
        else:
            d = PROF[n]; r = d["R500"]; mh, mg = li(d["hr"], d["hM"], r), li(d["gr"], d["gM"], r); ms = li(d["sr"], d["sM"], r) if d["stars"] else fstar(1.0) * mg
            p = dict(name=n, r_kpc=r, x=1.0, M_dyn=mh, M_gas=mg, M_star=ms, M_bar=mg + ms, measured=d["stars"], fallback=False)
            if not np.all(np.isfinite([mh, mg, ms])):          # profile ends just inside R500 (A2319: 0.999): the outermost point at x <= 1
                p = dict(max([q for q in pts if q["x"] <= 1.0], key=lambda q: q["r_kpc"])); p["fallback"] = True
        out.append(p)
    return out
def g1_xcop(names=WITH, R=R_COS, at="last", hscale=1.0):
    pts = xcop_last(names, at); Mb = np.array([p["M_gas"] * hscale + p["M_star"] for p in pts]); Md = np.array([p["M_dyn"] for p in pts]); return fret(Mb, Md, R), pts
def g1_kt(flag, R=R_COS, faint_gas=0.0, gas_src="erass"):
    rows = [r for r in KT if r["flag"] == flag]; Mb = []; Md = []; used = []
    for r in rows:
        mg = r["mgas"]
        if flag == "FAINT": mg = faint_gas * r["mstar"]
        elif gas_src == "ga1":
            t = GA1T.get(r["name"])
            if t is None: continue
            mg = t["mgas500_aud"] * beta_mass_fraction(r["r_mpc"], t["r500_aud"])
        Mb.append(0.5 * r["mstar"] + mg); Md.append(r["M_dyn"]); used.append(r)
    return fret(np.array(Mb), np.array(Md), R), used
G1 = {}
for f in FOOTS:
    rows = {}
    fl, Mb, Md = g1_lov(); rows["G-H"] = class_stat(fl)
    rows["G-H"]["n_above_2sigma"] = int(sum(mc_above([g["g5"], float(kvm18(g["M5"]))], [g["eg5"] / g["g5"], math.log(1.5)], g["M5"], g["eM5"] / g["M5"], seed=SEED + i) > 0.977 for i, g in enumerate(LOV)))
    fx, pts = g1_xcop(); rows["C-X"] = class_stat(fx); rows["C-X"]["per_cluster"] = {p["name"]: dict(x_last=p["x"], f_ret=float(v), fb=p["M_bar"] / p["M_dyn"]) for p, v in zip(pts, fx)}
    nab = 0
    for i, p in enumerate(pts):
        d = PROF[p["name"]]; r = p["r_kpc"]; eM = li(d["hr"], d["heM"], r) / p["M_dyn"]
        eg = 0.5 * (li(d["gr"], d["gH"], r) - li(d["gr"], d["gL"], r)) / p["M_gas"]; es = 0.5 * (li(d["sr"], d["sH"], r) - li(d["sr"], d["sL"], r)) / p["M_star"]
        pr = mc_above([p["M_gas"], p["M_star"]], [eg, es], p["M_dyn"], eM, seed=SEED + 100 + i); rows["C-X"]["per_cluster"][p["name"]].update(P_above1=pr, eM_frac=eM, eg_frac=eg, es_frac=es); nab += pr > 0.977
    rows["C-X"]["n_above_2sigma"] = int(nab)
    fb_, used = g1_kt("BRIGHT"); rows["G-DB"] = class_stat(fb_); rows["G-DB"]["tag"] = "[INNER APERTURE]"
    rows["G-DB"]["n_above_2sigma"] = int(sum(mc_above([0.5 * r["mstar"], r["mgas"]], [0.23, 0.23], r["M_dyn"], math.sqrt(2.0 / (r["Nm"] - 1)), seed=SEED + 200 + i) > 0.977 for i, r in enumerate(used)))
    ff_, used = g1_kt("FAINT"); rows["G-DF"] = class_stat(ff_); rows["G-DF"]["tag"] = "[INNER APERTURE] lower bound (gas 0)"
    rows["G-DF"]["n_above_2sigma"] = int(sum(mc_above([0.5 * r["mstar"]], [0.23], r["M_dyn"], math.sqrt(2.0 / (r["Nm"] - 1)), seed=SEED + 400 + i) > 0.977 for i, r in enumerate(used)))
    br = {}
    for st in ("gas", "kvm_/1.5", "kvm_x1.5", "eq_gas"): br[f"G-H stars {st}"] = class_stat(g1_lov(stars=st)[0])
    br["G-H R 5.562"] = class_stat(g1_lov(R=R_BR)[0])
    for b_ in (0.1, 0.2): br[f"G-H hydrostatic bias b {b_}"] = class_stat(fret(Mb, Md / (1 - b_)))
    br["C-X all 12 (imputed stars)"] = class_stat(g1_xcop(XN)[0]); fr5, p5 = g1_xcop(WITH, at="R500"); br["C-X at R500"] = class_stat(fr5); br["C-X R 5.562"] = class_stat(g1_xcop(R=R_BR)[0])
    per5 = {}
    for i, (p, v) in enumerate(zip(p5, fr5)):
        d = PROF[p["name"]]; r = p["r_kpc"]; eM = li(d["hr"], d["heM"], r) / p["M_dyn"]
        eg = 0.5 * (li(d["gr"], d["gH"], r) - li(d["gr"], d["gL"], r)) / p["M_gas"]; es = 0.5 * (li(d["sr"], d["sH"], r) - li(d["sr"], d["sL"], r)) / p["M_star"]
        per5[p["name"]] = dict(x=p["x"], f_ret=float(v), fb=p["M_bar"] / p["M_dyn"], P_above1=mc_above([p["M_gas"], p["M_star"]], [eg, es], p["M_dyn"], eM, seed=SEED + 300 + i), eM_frac=eM, fallback=p.get("fallback", False))
    br["C-X at R500"]["per_cluster"] = per5
    # A1 item 3 (post hoc, reported, never graded): X-COP's NFW-fit hydrostatic mass (M_NFW, fgas file) in place of M_FORW
    for at in ("R500", "last"):
        vv = {}
        for p in (xcop_last(WITH, at) if at == "last" else p5):
            d = PROF[p["name"]]; gr_all = np.array(d["gas_raw"]["RADIUS"], float) * d["r500_fits"]; mn = np.array(d["gas_raw"]["M_NFW"], float); okn = np.isfinite(mn) & (mn > 0) & (gr_all > 0)
            Mn = li(gr_all[okn], mn[okn], p["r_kpc"]); vv[p["name"]] = float(fret(p["M_bar"], Mn)) if np.isfinite(Mn) else float("nan")
        cs = class_stat([v for v in vv.values() if np.isfinite(v)]); cs["per_cluster"] = vv; br[f"C-X M_NFW at {at} (A1, post hoc)"] = cs
    hB = float(Q15["footings"][f]["main"]["h"]); br[f"C-X h 0.7 -> {hB:.4f}"] = class_stat(g1_xcop(hscale=(0.7 / hB) ** 0.5)[0])
    for b_ in (0.1, 0.2):
        fx_, pts_ = g1_xcop(); br[f"C-X hydrostatic bias b {b_}"] = class_stat(fret([p["M_bar"] for p in pts_], np.array([p["M_dyn"] for p in pts_]) / (1 - b_)))
    br["G-DB GA1 audited gas"] = class_stat(g1_kt("BRIGHT", gas_src="ga1")[0])
    for fg in (0.1, 1.0): br[f"G-DF faint gas {fg} x stars"] = class_stat(g1_kt("FAINT", faint_gas=fg)[0])
    star_dep = br["G-H stars kvm_/1.5"]["label"] != br["G-H stars kvm_x1.5"]["label"]
    graded = {k: rows[k]["label"] for k in ("G-H", "C-X", "G-DB", "G-DF")}
    G1[f] = dict(classes=rows, brackets=br, star_dependent=bool(star_dep), graded=graded)
    P(f"[{f}]")
    for k in ("G-H", "C-X", "G-DB", "G-DF"):
        c = rows[k]; P(f"  {k:5s} n {c['n']:3d}: median f_ret {c['median']:.3f} [{c['lo']:.3f}, {c['hi']:.3f}], {c['n_above1']} above 1, {c['n_above_2sigma']} above 1 at > 2 sigma -> {c['label']} {c.get('tag', '')}")
    P("  C-X per cluster (x_last, f_ret, P(f_ret > 1)): " + "; ".join(f"{n} {v['x_last']:.2f} {v['f_ret']:.3f} {v['P_above1']:.2f}" for n, v in rows["C-X"]["per_cluster"].items()))
    P("  C-X at R500 per cluster (x, f_ret, f_b, P(f_ret > 1), eM/M): " + "; ".join(f"{n} {v['x']:.3f} {v['f_ret']:.3f} {v['fb']:.3f} {v['P_above1']:.2f} {v['eM_frac']:.2f}" for n, v in per5.items()))
    P("  brackets (reported; never graded): " + "; ".join(f"{k} {v['median']:.3f} [{v['lo']:.3f}, {v['hi']:.3f}] {v['label']}" for k, v in br.items()))
    P(f"  [STAR-DEPENDENT] on G-H: {'yes' if star_dep else 'no'}")

# ================================================================== GATE 2: trend with depth
P(); P("GATE 2, trend with depth: OLS of log10 f_ret on log10 M500 over G-H (20) + C-X (7) at R500; T1 FAILS iff the 97.5th pct of the slope < 0; T2 FAILS iff C-X's upper bound < 0.85")
def ladder(stars="kvm", R=R_COS, scramble=None):
    Mb = []; M5 = []
    for g in LOV:
        s = {"kvm": float(kvm18(g["M5"])), "gas": 0.0, "kvm_x1.5": 1.5 * float(kvm18(g["M5"]))}[stars]; Mb.append(g["g5"] + s); M5.append(g["M5"])
    for p in xcop_last(WITH, at="R500"): Mb.append(p["M_bar"]); M5.append(p["M_dyn"])
    Mb = np.array(Mb); M5 = np.array(M5)
    if scramble is not None: Mb = Mb[scramble]
    fr = fin(fret(Mb, M5, R)); return np.log10(M5), np.log10(np.maximum(fr, 1e-6)), fr
G2 = {}
for f in FOOTS:
    x, y, fr = ladder(); s = ols_boot(x, y); t1 = "FAILS" if s["hi"] < 0 else "OK"; cx = G1[f]["classes"]["C-X"]; t2 = "FAILS" if cx["hi"] < 0.85 else "OK"
    sg = ols_boot(*ladder("gas")[:2]); sk = ols_boot(*ladder("kvm_x1.5")[:2]); dep = ("FAILS" if sg["hi"] < 0 else "OK") != ("FAILS" if sk["hi"] < 0 else "OK")
    lab = "CONSISTENT" if (t1 == "OK" and t2 == "OK") else "FAILS"
    gx = np.log10([o["M500"] for o in GS4]); gy0 = np.log10(fin(fret([o["Mg"] for o in GS4], [o["M500"] for o in GS4])))
    gy1 = np.log10(fin(fret([o["Mg"] + float(kvm18(o["M500"])) for o in GS4], [o["M500"] for o in GS4])))
    ext = dict(gas_only=ols_boot(gx, gy0), kvm=ols_boot(gx, gy1), n=len(GS4), median_fret_gas_by_mass={})
    for lo_, hi_ in ((13.0, 13.5), (13.5, 14.0), (14.0, 14.5), (14.5, 15.0), (15.0, 15.5)):
        m_ = (gx >= lo_) & (gx < hi_)
        if m_.sum(): ext["median_fret_gas_by_mass"][f"{lo_}-{hi_}"] = dict(n=int(m_.sum()), gas=float(np.median(10 ** gy0[m_])), kvm=float(np.median(10 ** gy1[m_])))
    kb, ub = g1_kt("BRIGHT"); kf, uf = g1_kt("FAINT")
    sp = dict(bright=spearman([r["sigma"] for r in ub], fin(kb)), faint=spearman([r["sigma"] for r in uf], fin(kf)))
    G2[f] = dict(slope=s, T1=t1, T2=t2, T2_value=dict(median=cx["median"], hi=cx["hi"]), label=lab, star_dependent=bool(dep), gas_only=sg, kvm_x1p5=sk, extended_GS4=ext, spearman_sigma=sp,
                 ladder_median_fret=dict(groups=float(np.median(fr[:20])), xcop_R500=float(np.median(fr[20:]))))
    P(f"[{f}] slope {s['slope']:+.3f} [{s['lo']:+.3f}, {s['hi']:+.3f}] -> T1 {t1}; C-X median {cx['median']:.3f}, upper {cx['hi']:.3f} -> T2 {t2}; LABEL {lab}{' [STAR-DEPENDENT]' if dep else ''}")
    P(f"  ladder medians at R500: groups {np.median(fr[:20]):.3f}, X-COP {np.median(fr[20:]):.3f}; brackets slope gas only {sg['slope']:+.3f} [{sg['lo']:+.3f}, {sg['hi']:+.3f}], KVM18 x 1.5 {sk['slope']:+.3f} [{sk['lo']:+.3f}, {sk['hi']:+.3f}]")
    P(f"  reported GS4 ladder ({len(GS4)} systems, line-H catalogues, X-COP removed): slope gas only {ext['gas_only']['slope']:+.3f} [{ext['gas_only']['lo']:+.3f}, {ext['gas_only']['hi']:+.3f}], with KVM18 {ext['kvm']['slope']:+.3f} [{ext['kvm']['lo']:+.3f}, {ext['kvm']['hi']:+.3f}]; "
      + "; ".join(f"lg M500 {k}: n {v['n']} f_ret {v['gas']:.2f} (gas) {v['kvm']:.2f} (KVM18)" for k, v in ext["median_fret_gas_by_mass"].items()))
    P(f"  reported Spearman f_ret vs sigma: G-DB {sp['bright']:+.2f}, G-DF {sp['faint']:+.2f}")

# ================================================================== GATE 3: X-COP radial shape
P(); P("GATE 3, X-COP radial shape: ZN4 native z = 0 shape, cold = f_c M200 m(r/R200), anchored at R x M_b at the last radius; |bin median log(M_obs/M_model)| <= 0.10 dex")
ZN = json.load(open(os.path.join(RB, "ZN4_cluster_resolution", "zn4_shapes.json")))
SH = {k: ZN[k]["0.00"] for k in ("1e14", "1e15")}
for k in SH: SH[k]["x_"] = np.array(SH[k]["x"], float); SH[k]["l_"] = np.array(SH[k]["lnm"], float)
KA["KA4"]["m1"] = {k: float(np.exp(np.interp(0.0, np.log(SH[k]["x_"]), SH[k]["l_"]))) for k in SH}
def m_native(x, lgM, stretch=1.0):
    x = np.asarray(x, float) / stretch; a, b = SH["1e14"], SH["1e15"]; w = float(np.clip((lgM - a["lgM"]) / (b["lgM"] - a["lgM"]), 0.0, 1.0)); out = []
    for s in (a, b):
        xe = s["x_edge"]; xx = np.minimum(x, xe); lx = np.log(np.maximum(xx, 1e-12)); l0 = np.log(s["x_"][0])
        v = np.where(xx >= s["x_"][0], np.interp(lx, np.log(s["x_"]), s["l_"]), s["l_"][0] + 2.0 * (lx - l0)); out.append(v)
    return np.exp((1 - w) * out[0] + w * out[1])
def m_nfw(x, c): mu = lambda t: np.log1p(t) - t / (1 + t); return mu(c * np.asarray(x, float)) / mu(c)
def solve_R200(Mb_anchor, r_anchor, z, R=R_COS, shape="native", stretch=1.0):
    fc = R / (1 + R); rc = rho_crit(z, 0.7, 0.3)
    def cold_in(R2):
        M200 = 200 * rc * 4 * math.pi / 3 * R2 ** 3
        m = m_native(r_anchor / R2, math.log10(M200), stretch) if shape == "native" else m_nfw(r_anchor / R2, duffy_c200(M200, z, 0.7))
        return fc * M200 * float(m)
    R2 = math.exp(brentq(lambda lr: math.log(cold_in(math.exp(lr))) - math.log(R * Mb_anchor), math.log(50.0), math.log(2e4), xtol=1e-12))
    M200 = 200 * rc * 4 * math.pi / 3 * R2 ** 3; return R2, M200, cold_in(R2) / (R * Mb_anchor) - 1
def g3(names=WITH, R=R_COS, anchor="last", shape="native", stretch=1.0, f="canonical"):
    pts = []; per = {}; anc_err = 0.0
    for n in names:
        P_ = [dict(p) for p in HYD if p["name"] == n]; d = PROF[n]
        if anchor == "last": pa = max(P_, key=lambda q: q["r_kpc"]); ra, Ma = pa["r_kpc"], pa["M_bar"]
        else: pa = xcop_last([n], "R500")[0]; ra, Ma = pa["r_kpc"], pa["M_bar"]
        R2, M200, e = solve_R200(Ma, ra, d["z"], R, shape, stretch); anc_err = max(anc_err, abs(e)); fc = R / (1 + R)
        c = duffy_c200(M200, d["z"], 0.7)
        for p in P_:
            m = m_native(p["r_kpc"] / R2, math.log10(M200), stretch) if shape == "native" else m_nfw(p["r_kpc"] / R2, c)
            p["M_cold_model"] = fc * M200 * float(m); p["M_model"] = p["M_bar"] + p["M_cold_model"]; p["D"] = math.log10(p["M_dyn"] / p["M_model"]); pts.append(p)
        per[n] = dict(R200_kpc=R2, M200=M200, R200_over_R500=R2 / d["R500"], x_last_over_R200=ra / R2)
    med, cnt = cl_bin_median(pts, lambda p: p["D"]); graded = cnt >= 5
    lab = "CONSISTENT" if np.all(np.abs(med[graded]) <= 0.10) else "FAILS"
    a0 = A0[f]; fXm, _ = tr1_frac(pts, lambda p: p["M_model"] - mlaw(p, a0), lambda p: p["M_model"]); fXd, _ = tr1_frac(pts, lambda p: p["M_dyn"] - mlaw(p, a0), lambda p: p["M_dyn"])
    fCm, _ = tr1_frac(pts, lambda p: p["M_cold_model"], lambda p: p["M_model"]); fCd, _ = tr1_frac(pts, lambda p: p["M_dyn"] - p["M_bar"], lambda p: p["M_dyn"])
    return dict(bins=med.tolist(), n_clusters=cnt.tolist(), graded=graded.tolist(), label=lab, fX_model=fXm.tolist(), fX_data=fXd.tolist(), fcold_model=fCm.tolist(), fcold_data=fCd.tolist(),
                per_cluster=per, anchor_max_err=anc_err, all_mean=float(np.mean([p["D"] for p in pts])), all_rms=float(np.sqrt(np.mean([p["D"] ** 2 for p in pts])))), pts
G3 = {}
for f in FOOTS:
    g, pts = g3(f=f); br = {}
    br["anchor R500"] = g3(anchor="R500", f=f)[0]; br["R 5.562"] = g3(R=R_BR, f=f)[0]; br["all 12 (imputed stars)"] = g3(XN, f=f)[0]
    br["NFW Duffy (EXTERNALLY CALIBRATED)"] = g3(shape="nfw", f=f)[0]
    # inner row (iii): the stars' own law phantom against the measured cold, bin 0 - 0.25 R500
    a0 = A0[f]; inner = {}
    for n in WITH:
        rr = [p for p in HYD if p["name"] == n and p["x"] < 0.25]; q = []
        for p in rr:
            r = p["r_kpc"] * KPC; gN = G * p["M_star"] * MS / r ** 2; mph = p["M_star"] * (float(glaw(gN, a0)) / gN - 1); cold = p["M_dyn"] - p["M_bar"]; q.append(mph / cold if cold > 0 else np.inf)
        inner[n] = dict(median_ratio=float(np.median(fin(q))), frac_points_above1=float(np.mean(fin(q) > 1)), n=len(q))
    G3[f] = dict(main=g, brackets=br, inner_phantom_over_cold=inner); KA["KA4"][f"anchor_err_{f}"] = g["anchor_max_err"]
    P(f"[{f}] bins {EDGES}: " + " / ".join(f"{v:+.3f}{'' if gr else '*'}" for v, gr in zip(g["bins"], g["graded"])) + f" (clusters {g['n_clusters']}) -> {g['label']}; all-point mean {g['all_mean']:+.3f}, rms {g['all_rms']:.3f}")
    P("  R200/R500 per cluster: " + ", ".join(f"{n} {v['R200_over_R500']:.2f}" for n, v in g["per_cluster"].items()))
    P(f"  TR1 statistic f_X = (M - M_law)/M per bin: model {' / '.join(f'{v:.2f}' for v in g['fX_model'])}; data {' / '.join(f'{v:.2f}' for v in g['fX_data'])} (TR1 {' / '.join(f'{v:.2f}' for v in TR1REF[f])})")
    P(f"  B's own cold fraction (M - M_b)/M per bin: model {' / '.join(f'{v:.2f}' for v in g['fcold_model'])}; data {' / '.join(f'{v:.2f}' for v in g['fcold_data'])}")
    for k, v in br.items(): P(f"  bracket {k}: " + " / ".join(f"{u:+.3f}" for u in v["bins"]) + f" -> {v['label']} (reported)")
    P("  inner row (reported): stars' law phantom / measured cold inside 0.25 R500, median per cluster: " + ", ".join(f"{n} {v['median_ratio']:.2f}" for n, v in inner.items()))

# ================================================================== GATE 4: the Bullet
P(); P("GATE 4, the Bullet: cold = R x (stars + gas that fell in) per cluster, placed with its galaxies (DB1 on='gal'), Newtonian")
def stripped_split(t):
    """gas per cluster: t = 0 the record's split (S0); t = 1 shared in proportion to stars (S1); the transfer scales linearly."""
    s1 = [MGAS * MST[j] / sum(MST) for j in range(2)]; return [MGJ[j] + t * (s1[j] - MGJ[j]) for j in range(2)]
def bullet_B(t, R=R_COS, on="gal"):
    gj = stripped_split(t); Rs = [R * (MST[j] + gj[j]) / MST[j] for j in range(2)]; row = bullet_row(1e-30, Rs, on); row["gas_assigned"] = gj; return row
t1 = time.time(); ROWS = {"S1": bullet_B(1.0), "S1/2": bullet_B(0.5), "S0": ROW_S0}; ROWS["S0"]["gas_assigned"] = stripped_split(0.0)
ROWS["S1, R 5.562"] = bullet_B(1.0, R=R_BR)
labs = {k: ROWS[k]["label"] for k in ("S0", "S1/2", "S1")}; strip_dep = len(set(labs.values())) > 1
lab4 = "CONSISTENT" if ROWS["S1"]["label"] == "PASS" else "FAILS"
for k, r in ROWS.items():
    P(f"  {k:12s} gas main/sub {r['gas_assigned'][0]:.3e}/{r['gas_assigned'][1]:.3e}; cold {r['Mcold'][0]:.3e}/{r['Mcold'][1]:.3e}; M300 {r['M300'][0]:.3e}/{r['M300'][1]:.3e} Z {r['ZM'][0]:+.2f}/{r['ZM'][1]:+.2f}; "
      f"d_gal {r['d_gal'][0]:.0f}/{r['d_gal'][1]:.0f}, d_gas {r['d_gas'][0]:.0f}/{r['d_gas'][1]:.0f} kpc, Z_off {r['Zoff'][0]:+.2f}/{r['Zoff'][1]:+.2f}; cls {r['cls']}; DB1 row {r['label']}")
# the stripped transfer the subcluster needs for |Z| <= 2 (linear in the cold amounts; unit Plummer apertures)
k_ = [[M2D(*c, 300.0, [(1.0, GAL[j][1], GAL[j][2], GAL[j][3])]) for j in range(2)] for c in (BCG1, BCG3)]
def m300_lin(t):
    gj = stripped_split(t); cold = [R_COS * (MST[j] + gj[j]) for j in range(2)]; base = [ROW_S0["M300"][i] - sum(R_COS * (MST[j] + MGJ[j]) * k_[i][j] for j in range(2)) for i in range(2)]
    return [base[i] + sum(cold[j] * k_[i][j] for j in range(2)) for i in range(2)]
lin_chk = [abs(m300_lin(1.0)[i] / ROWS["S1"]["M300"][i] - 1) for i in range(2)]
ts = np.linspace(0.0, 3.0, 3001); zsub = np.array([(m300_lin(t)[1] / DB1_OBS[1] - 1) / DB1_SIG for t in ts]); zmain = np.array([(m300_lin(t)[0] / DB1_OBS[0] - 1) / DB1_SIG for t in ts])
okt = ts[(np.abs(zsub) <= 2) & (np.abs(zmain) <= 2)]
need = dict(t_range=[float(okt.min()), float(okt.max())] if okt.size else None, transfer_S1=float(stripped_split(1.0)[1] - MGJ[1]), linear_check=lin_chk)
P(f"  transfer S1 moves {need['transfer_S1']:.3e} Msun of gas to the subcluster's account; both |Z_M300| <= 2 for t in {need['t_range']} (t = 1 is S1; linear model checked to {max(lin_chk):.1e})")
# native-shape placement (reported): cold with ZN4's shape centred on each cluster's galaxies, M300 only (Abel projection)
def sigma_table(Mtot, R2, lgM, mode="R200_to_edge"):
    """projected cold column of one cluster. Modes: 'R200_to_edge' = ZN's rule, cold f_c M200 m(r/R200) with R x M_b inside R200, the shape
    continued to x_edge (cold beyond R200 counted); 'R200_trunc' = R x M_b x min(m, 1), nothing beyond R200; 'total_at_edge' = the first
    implementation (the total R x M_b spread to 7.4 R200), kept visible, superseded."""
    rr = np.geomspace(0.5, 7.8 * R2, 3000); m = m_native(rr / R2, lgM)
    if mode == "R200_to_edge": Mc = Mtot * m
    elif mode == "R200_trunc": Mc = Mtot * np.minimum(m, 1.0)
    else: Mc = np.minimum(Mtot * m / m_native(np.array([7.4]), lgM)[0], Mtot)
    rho = np.gradient(Mc, rr) / (4 * math.pi * rr ** 2); D = np.geomspace(0.5, 4000.0, 400); zq = np.geomspace(0.05, 7.8 * R2, 2000)
    S = np.array([2 * TRAPZ(np.interp(np.sqrt(Dd * Dd + zq * zq), rr, rho, right=0.0), zq) for Dd in D]); return D, S
def m300_native(t, R=R_COS, mode="R200_to_edge"):
    gj = stripped_split(t); tot = [M2D(*c, 300.0, plum_of({})) for c in (BCG1, BCG3)]; info = []
    rc = rho_crit(0.296, 0.7, 0.3)
    for j in range(2):
        Mb = MST[j] + gj[j]; Mtot = R * Mb; M200 = (1 + R) * Mb; R2 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3); D, S = sigma_table(Mtot, R2, math.log10(M200), mode)
        ctr = GAL[j][2:4]; info.append(dict(R200=R2, Mcold=Mtot))
        for i, c in enumerate((BCG1, BCG3)):
            rho_ = np.linspace(0.0, 300.0, 301); phi = (np.arange(360) + 0.5) * 2 * math.pi / 360
            X = c[0] + rho_[:, None] * np.cos(phi)[None, :]; Y = c[1] + rho_[:, None] * np.sin(phi)[None, :]; Dd = np.hypot(X - ctr[0], Y - ctr[1])
            tot[i] += float(TRAPZ(np.sum(np.interp(Dd, D, S), axis=1) * (2 * math.pi / 360) * rho_, rho_))
    return tot, [(tot[i] / DB1_OBS[i] - 1) / DB1_SIG for i in range(2)], info
NAT = {}
for mode in ("R200_to_edge", "R200_trunc", "total_at_edge"):
    for k, t in (("S0", 0.0), ("S1/2", 0.5), ("S1", 1.0)):
        m, z, inf = m300_native(t, mode=mode); NAT[f"{mode} {k}"] = dict(M300=m, Z=z, info=inf)
        P(f"  native-shape placement (reported, {mode}{', SUPERSEDED first implementation' if mode == 'total_at_edge' else ''}) {k}: M300 {m[0]:.3e}/{m[1]:.3e}, Z {z[0]:+.2f}/{z[1]:+.2f}; R200 {inf[0]['R200']:.0f}/{inf[1]['R200']:.0f} kpc")
G4 = dict(rows=ROWS, label=lab4, stripping_dependent=bool(strip_dep), labels_by_assignment=labs, need=need, native=NAT, seconds=time.time() - t1)
P(f"  GATE 4 LABEL (S1 graded): {lab4}{' [STRIPPING-DEPENDENT]' if strip_dep else ''}; by assignment " + ", ".join(f"{k} {v}" for k, v in labs.items()) + f" ({time.time() - t1:.0f} s)")

# ================================================================== MUTATE twins (separate files)
PM(f"RB1 MUTATE twins (criteria {CRIT}); deliberately wrong versions that must fail. kappa = 1/2 FITTED; not theory closed.")
M1 = {}
for f in FOOTS:
    c = dict(GH=class_stat(g1_lov(R=2 * R_COS)[0]), CX=class_stat(g1_xcop(R=2 * R_COS)[0]), GDB=class_stat(g1_kt("BRIGHT", R=2 * R_COS)[0]), GDF=class_stat(g1_kt("FAINT", R=2 * R_COS)[0]))
    flips = [k for k, v in c.items() if v["label"] == "FAILS"]; M1[f] = dict(classes=c, flipped=flips, bites=bool(flips))
    PM(f"M1 [{f}] R x 2: " + "; ".join(f"{k} {v['median']:.3f} [{v['lo']:.3f}, {v['hi']:.3f}] {v['label']}" for k, v in c.items()) + f" -> {'BITES' if flips else 'DOES NOT BITE'} ({flips})")
M2 = {}
for f in FOOTS:
    x, y, _ = ladder(); real = ols_boot(x, y); perm = np.random.default_rng(SEED).permutation(len(x)); xs_, ys_, _ = ladder(scramble=perm); sc = ols_boot(xs_, ys_)
    rng = np.random.default_rng(SEED + 1); many = [float(np.polyfit(*ladder(scramble=rng.permutation(len(x)))[:2], 1)[0]) for _ in range(1000)]
    bites = bool(real["slope"] < sc["lo"] or real["slope"] > sc["hi"]); M2[f] = dict(real=real, scrambled=sc, median_1000=float(np.median(many)), bites=bites)
    PM(f"M2 [{f}] baryons scrambled: slope {sc['slope']:+.3f} [{sc['lo']:+.3f}, {sc['hi']:+.3f}] (median of 1000 permutations {np.median(many):+.3f}) vs real {real['slope']:+.3f} -> {'BITES' if bites else 'DOES NOT BITE'}")
M3 = {}
for f in FOOTS:
    gm = g3(stretch=1.5, f=f)[0]; d = np.array(gm["bins"]) - np.array(G3[f]["main"]["bins"]); ok = np.isfinite(d); rms = float(np.sqrt(np.mean(d[ok] ** 2)))
    M3[f] = dict(bins=gm["bins"], label=gm["label"], rms_shift=rms, bites=bool(rms >= 0.05))
    PM(f"M3 [{f}] native shape r x 1.5: bins " + " / ".join(f"{v:+.3f}" for v in gm["bins"]) + f" ({gm['label']}); rms shift {rms:.3f} -> {'BITES' if rms >= 0.05 else 'DOES NOT BITE'}")
M4row = bullet_B(1.0, on="gas"); M4 = dict(row=M4row, bites=bool(M4row["cls"] == "FAIL"))
PM(f"M4 Bullet cold on the gas (S1 amounts): cls {M4row['cls']}, d_gal {M4row['d_gal'][0]:.0f}/{M4row['d_gal'][1]:.0f}, d_gas {M4row['d_gas'][0]:.0f}/{M4row['d_gas'][1]:.0f}, M300 Z {M4row['ZM'][0]:+.2f}/{M4row['ZM'][1]:+.2f} -> {'BITES' if M4['bites'] else 'DOES NOT BITE'}")
MRES.update(M1=M1, M2=M2, M3=M3, M4=M4)

# ================================================================== labels
P(); P("LABELS (per footing; never PASS while gate 1 is one-sided)")
KA["KA4"]["footing_identity"] = bool(all(G1["canonical"]["classes"][k]["median"] == G1["alt"]["classes"][k]["median"] for k in ("G-H", "C-X", "G-DB", "G-DF")) and G2["canonical"]["slope"]["slope"] == G2["alt"]["slope"]["slope"])
KA["KA4"]["pass"] = bool(abs(fid - 1) <= 1e-12 and all(abs(v - 1) <= 1e-3 for v in KA["KA4"]["m1"].values()) and max(KA["KA4"][f"anchor_err_{f}"] for f in FOOTS) <= 1e-8 and KA["KA4"]["footing_identity"])
P(f"KA-4 identities: f_ret(M_dyn = (1+R) M_b) = {fid:.15f}; native m(1) " + ", ".join(f"{k} {v:.5f}" for k, v in KA["KA4"]["m1"].items())
  + f"; anchor max rel err {max(KA['KA4'][f'anchor_err_{f}'] for f in FOOTS):.1e}; footings identical on gates 1-2: {KA['KA4']['footing_identity']} -> {'PASS' if KA['KA4']['pass'] else 'FAIL'}")
ka_ok = dict(g1=KA["KA5"]["pass"] and KA["KA4"]["pass"], g2=KA["KA5"]["pass"] and KA["KA4"]["pass"], g3=all(KA["KA2"][f]["pass_"] for f in FOOTS) and KA["KA4"]["pass"],
             g4=KA["KA3"]["a_pass"] and KA["KA3"]["b_pass"], pd1=all(KA["KA1"][f]["pass_"] for f in FOOTS))
LAB = {}
for f in FOOTS:
    l1 = "FAILS" if any(v == "FAILS" for v in G1[f]["graded"].values()) else "CONSISTENT"
    if not M1[f]["bites"]: l1 = "NOT EVALUABLE"
    l2 = G2[f]["label"] if M2[f]["bites"] else "NOT EVALUABLE"; l3 = G3[f]["main"]["label"] if M3[f]["bites"] else "NOT EVALUABLE"; l4 = lab4 if M4["bites"] else "NOT EVALUABLE"
    gl = {"gate 1 conservation": l1 if ka_ok["g1"] else "NO VERDICT", "gate 2 trend": l2 if ka_ok["g2"] else "NO VERDICT", "gate 3 X-COP shape": l3 if ka_ok["g3"] else "NO VERDICT", "gate 4 Bullet": l4 if ka_ok["g4"] else "NO VERDICT"}
    vals = list(gl.values()); ov = "FAILS" if "FAILS" in vals else ("NOT FALSIFIED (ONE-SIDED)" if "CONSISTENT" in vals else "NOT EVALUABLE")
    tags = []
    if G1[f]["star_dependent"]: tags.append("gate 1 [STAR-DEPENDENT]")
    if G2[f]["star_dependent"]: tags.append("gate 2 [STAR-DEPENDENT]")
    if strip_dep: tags.append("gate 4 [STRIPPING-DEPENDENT]")
    LAB[f] = dict(gates=gl, overall=ov, tags=tags)
    P(f"[{f}] " + "; ".join(f"{k}: {v}" for k, v in gl.items()) + f" -> OVERALL {ov}" + (f"  tags: {', '.join(tags)}" if tags else ""))
fz = all(KA["KA2"][f]["frozen_ka2_pass"] for f in FOOTS)
for f in FOOTS: LAB[f]["gate3_under_frozen_KA2"] = LAB[f]["gates"]["gate 3 X-COP shape"] if fz else "NO VERDICT"
P(f"under the FROZEN KA-2 (TR1's table read with the -1.0 marker), gate 3 reads: {LAB['canonical']['gate3_under_frozen_KA2']} / {LAB['alt']['gate3_under_frozen_KA2']} (A1 is post hoc; both readings stated)")
P(f"known answers: KA-1 (PD1 bracket) {'PASS' if ka_ok['pd1'] else 'FAIL'}; KA-2a+b (TR1, A1) {'PASS' if ka_ok['g3'] else 'FAIL'}; KA-3 (Bullet) {'PASS' if ka_ok['g4'] else 'FAIL'}; KA-4 {'PASS' if KA['KA4']['pass'] else 'FAIL'}; KA-5 {'PASS' if KA['KA5']['pass'] else 'FAIL'}")
P("Stated: gate 1 is one-sided; the two-sided amount gate stays FAIL as PD1 graded it. The measurement that closes it: the baryons between R500 and turnaround around the same groups (stacked tSZ + X-ray + stars) with a non-hydrostatic total mass to that radius.")
RES.update(KA=KA, KA_ok=ka_ok, gate1=G1, gate2=G2, gate3=G3, gate4=G4, labels=LAB, mutate_summary={k: {f: MRES[k][f]["bites"] for f in FOOTS} if k != "M4" else MRES[k]["bites"] for k in ("M1", "M2", "M3", "M4")},
           seconds=time.time() - T0, peak_rss_MB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)
P(f"run {time.time() - T0:.0f} s, peak RSS {RES['peak_rss_MB']:.0f} MB")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not callable(v)}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): v = float(o); return v if math.isfinite(v) else (None if math.isnan(v) else ("inf" if v > 0 else "-inf"))
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(RES), open(os.path.join(HERE, "rb1.json"), "w"), indent=1); open(os.path.join(HERE, "rb1.out"), "w").write("\n".join(L) + "\n")
json.dump(clean(MRES), open(os.path.join(HERE, "rb1_MUTATE.json"), "w"), indent=1); open(os.path.join(HERE, "rb1_MUTATE.out"), "w").write("\n".join(LM_) + "\n")
