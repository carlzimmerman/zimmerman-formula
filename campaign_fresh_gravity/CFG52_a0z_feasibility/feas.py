#!/usr/bin/env python3
"""a0(z) feasibility with the repo's on-disk high-z kinematic tables (read-only; no repo file written).
Assumptions are printed in the output. Run: python3 feas.py"""
import os, csv, json, math, sys
import numpy as np
from scipy.special import i0, i1, k0, k1
from astropy.io import fits
from astropy.cosmology import Planck18, FlatLambdaCDM

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
D = REPO + "/real_research/data"
OUT = os.path.dirname(os.path.abspath(__file__))
G = 6.6743e-11; MSUN = 1.98847e30; KPC = 3.0856775814913673e19
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
OM = 0.3138
E = lambda z: np.sqrt(OM * (1 + np.asarray(z)) ** 3 + 1 - OM)
SIG_MFLOOR = 0.20   # dex on M_bar (stated floor)
LN10 = math.log(10)

# ---- kernel nu_mono: copy of the repo's definition (CFG3_common / L340): nu_RAR-derived monotone kernel
def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def _dh(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)
from scipy.optimize import brentq
_YP = brentq(lambda y: float(_dh(y)), 1.0, 5.0); _HP = float(_h_rar(_YP)); _DELTA = 0.05
_LYG = np.linspace(-12, 12, 240001); _YG = 10 ** _LYG
_DH = np.maximum(_dh(_YG), _DELTA * _HP / (_YG + _YP))
_HM = float(_h_rar(_YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (_DH[1:] + _DH[:-1]) * np.diff(_YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12)
    return 1.0 + np.interp(np.log10(y), _LYG, _HM) / y
def gpred(gb, a0):
    return gb * nu_mono(gb / a0)
def slope(gb, a0, e=0.02):   # d log g_pred / d log g_bar
    return (np.log10(gpred(gb * 10 ** e, a0)) - np.log10(gpred(gb * 10 ** -e, a0))) / (2 * e)

# ---- baryon models
def g_disc(Mbar_msun, R_kpc, Re_kpc):
    """exact Freeman exponential thin disc, R_d = R_e/1.68; returns v^2/R [m/s^2] at R"""
    Rd = Re_kpc / 1.68; y = R_kpc / (2 * Rd)
    v2 = (2 * G * Mbar_msun * MSUN / (Rd * KPC)) * y * y * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / (R_kpc * KPC)
def g_point(Mbar_msun, R_kpc):
    return G * Mbar_msun * MSUN / (R_kpc * KPC) ** 2
def gas_scaling(Ms, fg1=1.0):   # repo's project10c recipe: Mbar = Ms (1 + fg (Ms/1e10)^-0.4)
    return Ms * (1 + fg1 * (Ms / 1e10) ** -0.4)

rows = []   # unified per-galaxy records
def add(**k):
    rows.append(k)

# =============== 1. RC100 (Nestor Shachar+2023 Table 3) : V at R_e; logMbar incl. scaling gas
for r in csv.DictReader(open(D + "/rc100_nestorshachar2023_table3.csv")):
    add(ds="RC100", name=r["name"], z=float(r["z"]), Mbar=10 ** float(r["logMbar_Msun"]), Re=float(r["Re_kpc"]),
        r=float(r["Re_kpc"]), V=float(r["Vc_Re_kms"]), sV=0.10, note=f"fDM={r['fDM_within_Re']}, sig0={r['sigma0_kms']}",
        fdm=float(r["fDM_within_Re"]), flag_tab=int(r["deepMOND_g_lt_a0"]), gas="scaling(Tacconi)")

# =============== 2. MSA-3D (arXiv:2606.27853): stars only; V at R_e,disk; errors quoted
def fnum(s):
    try:
        x = float(s); return x if np.isfinite(x) else np.nan
    except Exception:
        return np.nan
for r in csv.DictReader(open(D + "/msa3d_2026_rotation_curves.csv")):
    V = float(r["Vrot_Re"]); ep, em = fnum(r["eVrot_p"]), fnum(r["eVrot_m"])
    e = np.nanmean([ep, em]) if not (np.isnan(ep) and np.isnan(em)) else 0.1 * V
    sV = max(e / V, 0.05)
    Ms = 10 ** float(r["logMstar"])
    for tag, Mb in (("stars", Ms), ("stars+gas", gas_scaling(Ms))):
        add(ds="MSA-3D " + tag, name="MSA" + r["ID"] + "/" + r["sample"], z=float(r["z"]), Mbar=Mb, Re=float(r["Re_disk_kpc"]),
            r=float(r["Re_disk_kpc"]), V=V, sV=sV, note=f"{r['sample']} vsig={r['vsig']} {r['RC_shape']}", gas=tag,
            fdm=float(r["fDM_Re"]), flag_tab=0)

# =============== 3. KMOS3D (Ubler+17 kinematics x catalogue R_half): cross-match as L332
h = fits.open(D + "/kmos3d/k3d_fnlsp_table_v3.fits")[1].data
nmatch = 0; nrows = 0
for r in csv.DictReader(open(D + "/kmos3d_ubler2017.csv")):
    nrows += 1
    z = float(r["z"]); lm = float(r["logMstar"])
    sel = np.where((abs(h["Z"] - z) < 0.002) & (abs(h["LMSTAR"] - lm) < 0.006))[0]
    if len(sel) != 1:
        continue
    rh = float(h["RHALF"][sel[0]])
    if not (rh > 0):
        continue
    nmatch += 1
    Re = rh * Planck18.kpc_proper_per_arcmin(z).value / 60.0
    add(ds="KMOS3D", name=f"K3D z={z:.3f}", z=z, Mbar=10 ** float(r["logMbar"]), Re=Re, r=1.311 * Re,
        V=float(r["Vcirc_kms"]), sV=0.10, note=f"sig0={r['sigma0_kms']}", gas="scaling(Tacconi)", fdm=np.nan, flag_tab=0)
KMOS_N = (nrows, nmatch)

# =============== 4. KROSS (Harrison+17): stars only; Reff in kpc; V_C assumed at 2.2 R_d = 1.311 R_e
for r in csv.DictReader(open(D + "/kross_harrison2017.csv")):
    z = float(r["z"]); Ms = float(r["Mstar"]); Re = float(r["Reff_kpc"])
    if not (Re > 0 and Ms > 0 and float(r["VC_kms"]) > 0):
        continue
    for tag, Mb in (("stars", Ms), ("stars+gas", gas_scaling(Ms))):
        add(ds="KROSS " + tag, name="KROSS", z=z, Mbar=Mb, Re=Re, r=1.311 * Re, V=float(r["VC_kms"]), sV=0.10,
            note=f"sig0={r['sigma0_kms']}", gas=tag, fdm=np.nan, flag_tab=0)

# =============== 5. Jeanneau+26 MUSE-DARK II (VizieR J/A+A/709/A120): Mbar incl. scaling gas; V(2.0 Re)
cos = FlatLambdaCDM(H0=70, Om0=0.3)
for r in csv.DictReader(open(REPO + "/prep_2026/jeanneau_refit/jeanneau26_catalog_cds.csv")):
    z = float(r["zR21"]); Re = float(r["Reff"]) * cos.kpc_proper_per_arcmin(z).value / 60.0
    lV = float(r["logV2_0"]); slV = float(r["s_logV2_0"])
    add(ds="MUSE-DARK II", name=f"{r['Cluster']}-{r['IdR21']}", z=z, Mbar=10 ** float(r["logMBar"]), Re=Re, r=2.0 * Re,
        V=10 ** lV, sV=max(slV * LN10, 0.05), note=f"mu={float(r['muR21']):.1f} sig0={r['sigma0']}", gas="scaling(Tacconi+NUM)",
        fdm=np.nan, flag_tab=0)

# =============== 6. lensed/CO ledger (prep_2026/a0z_crossscale, verified 2026-09-23): rows with M, R_out and V
L = json.load(open(REPO + "/prep_2026/a0z_crossscale/highz_target_ledger_verified_2026_results.json"))
LEDGER_N = len(L["rows"]); ledger_used = []
for r in L["rows"]:
    if r.get("Mstar") and r.get("Rout") and r.get("V") and (r.get("Mmol") or r["name"] in ("A1689B11", "zC-400569 (cold-tracer control)")):
        Mb = r["Mstar"] + (r.get("Mmol") or 0.0)
        add(ds="lensed/CO ledger", name=r["name"], z=r["z"], Mbar=Mb, Re=r["Rout"] / 1.311, r=r["Rout"], V=r["V"], sV=0.15,
            note=("gas PUB" if r.get("Mmol") else "stars only (no gas)"), gas="published" if r.get("Mmol") else "none", fdm=np.nan, flag_tab=0)

# ============================================================ compute
def quantities(d, foot):
    a0 = A0[foot]
    gb = g_disc(d["Mbar"], d["r"], d["Re"]); gp = g_point(d["Mbar"], d["r"])
    go = (d["V"] * 1e3) ** 2 / (d["r"] * KPC)
    return gb, gp, go
res = []
for d in rows:
    o = dict(d)
    for foot in ("can", "alt"):
        a0 = A0[foot]
        gb, gp, go = quantities(d, foot)
        a0z = a0 * float(E(d["z"]))
        pf = float(gpred(gb, a0)); pr = float(gpred(gb, a0z))
        s_f = float(slope(gb, a0)); s_r = float(slope(gb, a0z))
        s_obs = 2 * d["sV"] / LN10                      # dex on g_obs
        sig = math.hypot(s_obs, s_f * SIG_MFLOOR)       # total per-galaxy sigma of Delta (flat slope; rival differs <10%)
        o[foot] = dict(gb=gb, gp=gp, go=go, y=gb / a0, yp=gp / a0, yo=go / a0,
                       Df=math.log10(go / pf), Dr=math.log10(go / pr), sep=math.log10(pr / pf), sig=sig,
                       s_obs=s_obs, sf=s_f)
    o["gb_over_a0_can"] = o["can"]["y"]
    res.append(o)

def sel(ds, cond=None):
    return [o for o in res if o["ds"] == ds and (cond is None or cond(o))]

dsets = []
for o in res:
    if o["ds"] not in dsets: dsets.append(o["ds"])

def count(ds, foot):
    S = sel(ds)
    n = len(S)
    zs = np.array([o["z"] for o in S])
    y = np.array([o[foot]["y"] for o in S]); yp = np.array([o[foot]["yp"] for o in S]); yo = np.array([o[foot]["yo"] for o in S])
    sf = np.array([o[foot]["sf"] for o in S])
    yrob = y * 10 ** (SIG_MFLOOR)  # 1-sigma-robust on the mass floor (g_bar scales linearly with M)
    return dict(N=n, zmed=float(np.median(zs)), zmin=float(zs.min()), zmax=float(zs.max()),
                gb_lt_a0=int((y < 1).sum()), gb_lt_0p3=int((y < 0.3).sum()), go_lt_a0=int((yo < 1).sum()),
                gbpoint_lt_a0=int((yp < 1).sum()), gbpoint_lt_0p3=int((yp < 0.3).sum()),
                gb_lt_0p3_robust=int((yrob < 0.3).sum()), gb_lt_a0_robust=int((yrob < 1).sum()),
                med_y=float(np.median(y)), med_yo=float(np.median(yo)),
                gb_lt_0p3_z15=int(((y < 0.3) & (zs >= 1.5)).sum()), gb_lt_a0_z15=int(((y < 1) & (zs >= 1.5)).sum()),
                gb_lt_a0_z2=int(((y < 1) & (zs >= 2)).sum()), n_z15=int((zs >= 1.5).sum()), n_z2=int((zs >= 2).sum()))

def discr(ds, foot, ycut, key="y"):
    S = [o for o in sel(ds) if o[foot][key] < ycut]
    n = len(S)
    if n == 0:
        return dict(n=0)
    sep = np.array([o[foot]["sep"] for o in S]); sig = np.array([o[foot]["sig"] for o in S])
    Df = np.array([o[foot]["Df"] for o in S]); Dr = np.array([o[foot]["Dr"] for o in S])
    w = 1 / sig ** 2
    # mean offsets: statistical part averages down, mass-floor part (calibration) treated correlated
    s_obs = np.array([o[foot]["s_obs"] for o in S]); sf = np.array([o[foot]["sf"] for o in S])
    wo = 1 / np.maximum(s_obs, 1e-3) ** 2  # obs-only weights
    mean_f = float(np.sum(w * Df) / np.sum(w)); mean_r = float(np.sum(w * Dr) / np.sum(w))
    sig_ind = float(1 / math.sqrt(w.sum()))
    sig_corr = float(math.sqrt(1 / np.sum(1 / s_obs ** 2) + (np.mean(sf) * SIG_MFLOOR) ** 2))
    return dict(n=n, n_sep_gt1=int((sep / sig > 1).sum()), n_sep_gt2=int((sep / sig > 2).sum()),
                n_flat_within1=int((abs(Df) / sig < 1).sum()), n_rival_within1=int((abs(Dr) / sig < 1).sum()),
                med_sep=float(np.median(sep)), med_sig=float(np.median(sig)),
                mean_Df=mean_f, mean_Dr=mean_r, sig_ind=sig_ind, sig_corr=sig_corr,
                pull_f_ind=mean_f / sig_ind, pull_r_ind=mean_r / sig_ind, pull_f_corr=mean_f / sig_corr, pull_r_corr=mean_r / sig_corr,
                zmed=float(np.median([o["z"] for o in S])))

C = {ds: {f: count(ds, f) for f in ("can", "alt")} for ds in dsets}
DISC = {ds: {f: {"y<1": discr(ds, f, 1.0), "y<0.3": discr(ds, f, 0.3), "yo<1": discr(ds, f, 1.0, "yo")} for f in ("can", "alt")} for ds in dsets}

# ------------------------------------------------------------ print
P = lambda *a: print(*a)
P("ASSUMPTIONS: a0 canonical 9.3603e-11 (alt 1.1312e-10); nu_mono (repo FP1/L340 kernel, re-implemented); rival a0(z)=a0*E(z), Om=0.3138;")
P("  g_bar = exact Freeman exp. disc (R_d=R_e/1.68) at the velocity radius; point-mass GM/r^2 = upper bracket; g_obs = V^2/r;")
P("  sigma_V/V: RC100/KMOS3D/KROSS 10% (tables carry no errors), MSA-3D quoted (>=5%), MUSE-DARK II posterior (>=5%), ledger 15%;")
P("  + 0.20 dex floor on M_bar propagated with the local slope dlog g_pred/dlog g_bar; Re error, inclination, distance NOT propagated.")
P(f"  KMOS3D cross-match: {KMOS_N[1]} of {KMOS_N[0]} Ubler rows matched uniquely to catalogue R_half; ledger rows {LEDGER_N}, with M+R+V: {sum(1 for o in res if o['ds']=='lensed/CO ledger')}")
P()
hdr = f"{'dataset':22}{'N':>5}{'z range':>13}{'medz':>6}{'med gb/a0':>10}{'med go/a0':>10}{'gb<a0':>6}{'gb<.3a0':>8}{'go<a0':>6}{'pt<a0':>6}{'pt<.3':>6}{'rob<.3':>7}{'gb<a0&z>=1.5':>13}{'gb<.3&z>=1.5':>13}{'N(z>=1.5)':>10}{'N(z>=2)':>8}"
for foot in ("can", "alt"):
    P(f"--- COUNTS, footing {foot} (a0={A0[foot]:.4e}) ---"); P(hdr)
    for ds in dsets:
        c = C[ds][foot]
        P(f"{ds:22}{c['N']:5d}{c['zmin']:6.2f}-{c['zmax']:<6.2f}{c['zmed']:6.2f}{c['med_y']:10.2f}{c['med_yo']:10.2f}{c['gb_lt_a0']:6d}{c['gb_lt_0p3']:8d}{c['go_lt_a0']:6d}{c['gbpoint_lt_a0']:6d}{c['gbpoint_lt_0p3']:6d}{c['gb_lt_0p3_robust']:7d}{c['gb_lt_a0_z15']:13d}{c['gb_lt_0p3_z15']:13d}{c['n_z15']:10d}{c['n_z2']:8d}")
    P()
P("--- DISCRIMINATION flat vs a0*E(z): galaxies with g_bar<a0 (disc), canonical ---")
P(f"{'dataset':22}{'n':>5}{'medz':>6}{'med sep dex':>12}{'med sig':>8}{'n sep>1s':>9}{'n sep>2s':>9}{'mean Df':>9}{'mean Dr':>9}{'sig ind':>8}{'sig corr':>9}{'Df pull(ind/corr)':>19}{'Dr pull(ind/corr)':>19}")
for foot in ("can",):
    for cut in ("y<1", "y<0.3", "yo<1"):
        P(f"  [{cut}]")
        for ds in dsets:
            r = DISC[ds][foot][cut]
            if r["n"] == 0:
                P(f"{ds:22}{0:5d}"); continue
            P(f"{ds:22}{r['n']:5d}{r['zmed']:6.2f}{r['med_sep']:12.3f}{r['med_sig']:8.3f}{r['n_sep_gt1']:9d}{r['n_sep_gt2']:9d}{r['mean_Df']:9.3f}{r['mean_Dr']:9.3f}{r['sig_ind']:8.3f}{r['sig_corr']:9.3f}{r['pull_f_ind']:9.2f}/{r['pull_f_corr']:<8.2f}{r['pull_r_ind']:9.2f}/{r['pull_r_corr']:<8.2f}")
P()
# list of the deepest z>=1.5 objects
P("--- deep candidates at z>=1.4 (disc g_bar/a0<1, canonical): all datasets ---")
for o in sorted([o for o in res if o["z"] >= 1.4 and o["can"]["y"] < 1.0], key=lambda o: o["can"]["y"]):
    c = o["can"]
    P(f"  {o['ds']:22}{o['name']:22} z={o['z']:.2f} gb/a0={c['y']:.2f} (pt {c['yp']:.2f}) go/a0={c['yo']:.2f} Df={c['Df']:+.2f} Dr={c['Dr']:+.2f} sep={c['sep']:.2f} sig={c['sig']:.2f}")
P()
P("--- objects with g_bar/a0<0.3 at z>=1.0 (disc, canonical) ---")
for o in sorted([o for o in res if o["z"] >= 1.0 and o["can"]["y"] < 0.3], key=lambda o: -o["z"]):
    c = o["can"]
    P(f"  {o['ds']:22}{o['name']:22} z={o['z']:.2f} gb/a0={c['y']:.2f} (pt {c['yp']:.2f}) go/a0={c['yo']:.2f} Df={c['Df']:+.2f} Dr={c['Dr']:+.2f} sep={c['sep']:.2f} sig={c['sig']:.2f} {o['note'][:40]}")

# z-binned deep-MOND stats pooled over the two best data sets (own-gas variants only, no double counting)
P()
P("--- POOLED Delta_flat / Delta_rival, MUSE-DARK II (best deep sample), by z-bin, g_bar<a0 (disc) ---")
S = [o for o in sel("MUSE-DARK II") if o["can"]["y"] < 1]
for lo, hi in [(0.5, 0.9), (0.9, 1.2), (1.2, 1.5)]:
    T = [o for o in S if lo <= o["z"] < hi]
    if not T: continue
    Df = np.array([o["can"]["Df"] for o in T]); Dr = np.array([o["can"]["Dr"] for o in T]); sg = np.array([o["can"]["sig"] for o in T])
    so = np.array([o["can"]["s_obs"] for o in T]); sf = np.array([o["can"]["sf"] for o in T])
    sc = math.sqrt(1 / np.sum(1 / so ** 2) + (np.mean(sf) * SIG_MFLOOR) ** 2)
    P(f"  z {lo}-{hi}: N={len(T):3d}  mean Df={Df.mean():+.3f}  mean Dr={Dr.mean():+.3f}  sigma(mean, indep)={1/math.sqrt(np.sum(1/sg**2)):.3f} sigma(mean, correlated mass floor)={sc:.3f}  median sep={np.median([o['can']['sep'] for o in T]):.3f}")

# ---------- forecast: N objects at z=2.5 for 3-sigma separation, deep-MOND objects at y=0.1 and 0.3
P()
P("--- FORECAST: N deep-MOND rotators at z=2.5 for 3-sigma flat vs a0*E(z) (independent errors, per-object sigma on g) ---")
z = 2.5
for y0 in (0.05, 0.1, 0.3):
    gb = y0 * A0["can"]
    sep = math.log10(float(gpred(gb, A0["can"] * float(E(z)))) / float(gpred(gb, A0["can"])))
    P(f"  y=g_bar/a0={y0}: separation on g_obs = {sep:.3f} dex (E(2.5)={float(E(z)):.3f}, log={math.log10(float(E(z))):.3f})")
    for sV in (0.05, 0.10):
        for sM in (0.10, 0.20):
            s = math.hypot(2 * sV / LN10, float(slope(gb, A0['can'])) * sM)
            N = (3 * s / sep) ** 2
            P(f"     sigma_V/V={sV:.2f}, sigma_logM={sM:.2f}: per-object sigma={s:.3f} dex -> N(3 sigma)={N:.1f}")

# dump json
def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return float(o)
    return o
json.dump(clean(dict(counts=C, disc=DISC)), open(OUT + "/feas_results.json", "w"), indent=1)
import csv as _c
with open(OUT + "/feas_per_galaxy.csv", "w", newline="") as f:
    w = _c.writer(f); w.writerow(["ds", "name", "z", "Mbar", "Re_kpc", "r_kpc", "V", "gb_disc/a0", "gb_pt/a0", "go/a0", "Df", "Dr", "sep", "sig"])
    for o in res:
        c = o["can"]; w.writerow([o["ds"], o["name"], o["z"], f"{o['Mbar']:.3e}", f"{o['Re']:.3f}", f"{o['r']:.3f}", f"{o['V']:.1f}", f"{c['y']:.3f}", f"{c['yp']:.3f}", f"{c['yo']:.3f}", f"{c['Df']:.3f}", f"{c['Dr']:.3f}", f"{c['sep']:.3f}", f"{c['sig']:.3f}"])

# ---------------- extra: 1-sigma classification per galaxy (primary variants), by z-cut
P()
P("--- PER-GALAXY 1-SIGMA CLASSIFICATION (canonical a0; g_bar<a0 disc); sigma = obs + 0.20 dex mass floor ---")
P("    'flat-ok' = |Delta_flat|<1s ; 'rival-ok' = |Delta_rival|<1s ; separable = (rival-flat prediction gap)/sigma > 1")
PRIM = ["RC100", "KMOS3D", "MSA-3D stars+gas", "MSA-3D stars", "KROSS stars+gas", "MUSE-DARK II", "lensed/CO ledger"]
P(f"{'dataset':20}{'zcut':>6}{'ycut':>6}{'n':>4}{'sep>1s':>7}{'flat-ok':>8}{'rival-ok':>9}{'both-ok':>8}{'flat only':>10}{'rival only':>11}{'neither':>8}")
for zc in (0.0, 1.0, 1.5, 2.0):
    for yc in (1.0, 0.3):
        for ds in PRIM:
            S = [o for o in sel(ds) if o["can"]["y"] < yc and o["z"] >= zc]
            if not S: continue
            fo = np.array([abs(o["can"]["Df"]) < o["can"]["sig"] for o in S]); ro = np.array([abs(o["can"]["Dr"]) < o["can"]["sig"] for o in S])
            sp = np.array([o["can"]["sep"] > o["can"]["sig"] for o in S])
            P(f"{ds:20}{zc:6.1f}{yc:6.1f}{len(S):4d}{sp.sum():7d}{fo.sum():8d}{ro.sum():9d}{(fo&ro).sum():8d}{(fo&~ro).sum():10d}{(ro&~fo).sum():11d}{(~fo&~ro).sum():8d}")
# RC100 consistency: disc g_bar vs table-implied
P()
P("--- CONTROL: RC100 disc g_bar vs the table's own (1-fDM) g_obs: median log ratio (table/disc) = see below ---")
S = sel("RC100"); a = np.array([math.log10((1 - o["fdm"]) * o["can"]["go"] / o["can"]["gb"]) for o in S])
P(f"    median {np.median(a):+.3f} dex, 16-84% [{np.percentile(a,16):+.3f},{np.percentile(a,84):+.3f}], max {a.max():+.3f} ({S[int(np.argmax(a))]['name']})")
P("    RC100 GS4 01529: V=313 km/s, R_e=4.5 kpc, logMbar=9.63 -> g_obs=7.5 a0 vs disc g_bar=0.2 a0; table fDM=0.11 implies g_bar~6.7 a0: the row's M_bar/V/R are mutually inconsistent (treated as a data outlier, not a deep-MOND object)")
