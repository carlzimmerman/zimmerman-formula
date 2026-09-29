#!/usr/bin/env python3
"""CFG90 -- independent re-derivation of the CFG52 a0(z) feasibility counts and the CFG54 PHIBSS count.

The frozen question, selection rules, pass lines and controls are in FROZEN.md (written before this file existed).
Nothing of CFG52/CFG54's scripts/outputs was read.  Run:  python3 cfg90.py          (main)
                                                        MUTATE=1 python3 cfg90.py  (a0 -> 2 a0; must exit 1)
"""
import os, sys, json, re, math
import numpy as np, pandas as pd
from scipy import special, integrate

MUT = os.environ.get("MUTATE", "0") == "1"
REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUT else ""
out_lines = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out_lines.append(s)

# ---------------- constants ----------------
G = 6.6743e-11; MSUN = 1.98841e30; KPC = 3.085678e19; CLIGHT = 2.99792458e8
OM = 0.3138; OL = 1 - OM; H0KMS = 67.36
H0 = H0KMS * 1e3 / (1e6 * 3.085678e16)     # s^-1
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
MF = 2.0 if MUT else 1.0                    # MUTATE multiplier on a0
for k in A0: A0[k] *= MF
MASSFLOOR = 0.20
LN10 = math.log(10)

def E(z): return np.sqrt(OM * (1 + np.asarray(z, float)) ** 3 + OL)

def nu_mono(y):            # 1/(1-exp(-sqrt y))
    y = np.asarray(y, float); return 1.0 / (-np.expm1(-np.sqrt(y)))
def nu_simple(y):
    y = np.asarray(y, float); return 0.5 * (1 + np.sqrt(1 + 4.0 / y))
NU = nu_mono

def f_freeman(x):
    """g_disc R_d^2/(G M) for an exact Freeman disc at x = R/R_d."""
    x = np.asarray(x, float); y = x / 2
    return 2 * y ** 2 * (special.i0e(y) * special.k0e(y) - special.i1e(y) * special.k1e(y)) / x

def dA_kpc_per_arcsec(z):
    dc = integrate.quad(lambda zz: 1 / E(zz), 0, z)[0] * CLIGHT / H0 / 3.085678e22  # Mpc
    da = dc / (1 + z) * 1e3  # kpc
    return da * math.pi / 180 / 3600

# ---------------- controls ----------------
ctrl = {}
def check(name, ok, detail):
    ctrl[name] = bool(ok); P(("PASS " if ok else "FAIL ") + name + " -- " + detail)

def run_controls():
    # C1 closed-form a0
    a_can = 0.5 * CLIGHT * H0 * math.sqrt(3 * OL / (8 * math.pi))
    a_alt = 0.5 * CLIGHT * H0 * math.sqrt(3 / (8 * math.pi))
    a_can0, a_alt0 = 9.3603e-11, 1.1312e-10
    check("C1a a0_can closed form", abs(a_can / a_can0 - 1) < 5e-3, f"(1/2)cH0 sqrt(3 OL/8pi) = {a_can:.4e} vs 9.3603e-11 ({a_can/a_can0-1:+.4%})")
    check("C1b a0_alt closed form", abs(a_alt / a_alt0 - 1) < 5e-3, f"(1/2)cH0 sqrt(3/8pi) = {a_alt:.4e} vs 1.1312e-10 ({a_alt/a_alt0-1:+.4%})")
    check("C1c alt/can = 1/sqrt(OL)", abs(a_alt0 / a_can0 * math.sqrt(OL) - 1) < 3e-3, f"{a_alt0/a_can0:.5f} vs {1/math.sqrt(OL):.5f}")
    # C2 E(z) independent from densities
    rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
    for z in (0.0, 0.85, 1.0, 2.0, 2.5):
        rho = OM * rho_c * (1 + z) ** 3 + OL * rho_c
        Ez = math.sqrt(8 * math.pi * G * rho / (3 * H0 ** 2))
        ok = abs(Ez / float(E(z)) - 1) < 1e-12
        if not ok: break
    check("C2a E(z) closed form vs Friedmann densities", ok, f"E(1)={float(E(1)):.6f}, E(2)={float(E(2)):.6f}, E(2.5)={float(E(2.5)):.6f}")
    s1 = dA_kpc_per_arcsec(1.0)
    check("C2b angular scale at z=1 (7.8-8.4 kpc/arcsec)", 7.8 < s1 < 8.4, f"{s1:.3f} kpc/arcsec")
    # C3 Freeman disc vs direct ring sum
    def phi(R):
        f = lambda a: (1 / (2 * math.pi)) * math.exp(-a) * 2 * math.pi * a * (-(2 / math.pi) * special.ellipk(min(4 * R * a / (R + a) ** 2, 1 - 1e-15)) / (R + a))
        v = integrate.quad(f, 0, R, limit=400, epsabs=1e-13, epsrel=1e-13)[0] + integrate.quad(f, R, 60, limit=400, epsabs=1e-13, epsrel=1e-13)[0]
        return v
    maxrel = 0
    for R in (0.5, 1, 2, 3.36, 4, 6):
        h = 1e-4 * R
        g_num = (phi(R + h) - phi(R - h)) / (2 * h)
        maxrel = max(maxrel, abs(g_num / float(f_freeman(R)) - 1))
    check("C3a Freeman closed form vs direct ring-sum potential", maxrel < 1e-3, f"max rel dev {maxrel:.2e} over R/Rd = 0.5..6")
    xx = np.linspace(0.5, 6, 200001); vv2 = xx * f_freeman(xx)
    check("C3b Freeman v^2 peaks at 2.15 R_d", abs(xx[np.argmax(vv2)] - 2.15) < 0.01, f"peak at {xx[np.argmax(vv2)]:.3f} R_d, v2max = {vv2.max():.4f} GM/Rd")
    check("C3c Freeman -> GM/R^2 at large R", abs(float(f_freeman(60.0)) * 60 ** 2 - 1) < 2e-3, f"f(60)*60^2 = {float(f_freeman(60.0))*3600:.5f}")
    # C4 kernel
    gb = np.logspace(-14, -8, 61)
    a0 = A0["can"]
    gob = gb * NU(gb / a0)
    from scipy.optimize import brentq
    back = np.array([brentq(lambda g: g * NU(g / a0) - go, go * 1e-6, go * 1.0000001, xtol=1e-30, rtol=1e-13) for go in gob])
    check("C4a kernel round trip g_bar->g_obs->g_bar", np.max(np.abs(back / gb - 1)) < 1e-8, f"max rel {np.max(np.abs(back/gb-1)):.1e}")
    y = 1e-4; y2 = 1e4
    check("C4b deep-MOND and Newton limits", abs(NU(y) * math.sqrt(y) - 1) < 1e-2 and abs(NU(y2) - 1) < 1e-2, f"nu(1e-4) sqrt(y) = {float(NU(y))*math.sqrt(y):.5f}, nu(1e4) = {float(NU(y2)):.5f}")
    return

# ---------------- data loading ----------------
def tacconi18_mu(z, logM):
    return 10 ** (0.06 - 3.3 * (np.log10(1 + z) - 0.65) ** 2 - 0.41 * (logM - 10.7))

def load():
    rows = []
    # RC100
    d = pd.read_csv(f"{REPO}/real_research/data/rc100_nestorshachar2023_table3.csv")
    for _, r in d.iterrows():
        rows.append(dict(survey="RC100", name=r["name"], z=r.z, logM=r.logMbar_Msun, Re=r.Re_kpc, V=r.Vc_Re_kms, sigV=0.10,
                         xn=1.68, fDM=r.fDM_within_Re, gas="table"))
    # MSA-3D (stars + Tacconi18 molecular gas)
    d = pd.read_csv(f"{REPO}/real_research/data/msa3d_2026_rotation_curves.csv")
    for _, r in d.iterrows():
        mu = tacconi18_mu(r.z, r.logMstar)
        lm = r.logMstar + math.log10(1 + mu)
        ev = np.nanmean([r.eVrot_p, r.eVrot_m]); ev = ev if np.isfinite(ev) else 0.1 * r.Vrot_Re
        sv = max(ev / r.Vrot_Re, 0.02)
        rows.append(dict(survey="MSA3D", name=str(r.ID), z=r.z, logM=lm, logMstar=r.logMstar, Re=r.Re_disk_kpc, V=r.Vrot_Re, sigV=sv,
                         xn=1.68, fDM=r.fDM_Re, gas="tacconi18"))
    # KMOS3D (Ubler) with R_e from the KMOS3D catalogue
    u = pd.read_csv(f"{REPO}/real_research/data/kmos3d_ubler2017.csv")
    c = pd.read_csv(f"{REPO}/data_assembly/kmos3d_phibss/kmos3d_catalog.csv")
    c = c[(c.Z > 0) & (c.LMSTAR > 0)].reset_index(drop=True)
    nmatch = 0; ndrop = 0; kmatch = []
    for i, r in u.iterrows():
        dd = np.hypot((c.Z - r.z) / 0.002, (c.LMSTAR - r.logMstar) / 0.02)
        j = dd.idxmin()
        if dd[j] > 1.0:
            ndrop += 1; continue
        nmatch += 1
        Re = c.loc[j, "RHALF"] * dA_kpc_per_arcsec(r.z)
        kmatch.append(c.loc[j, "ID"])
        rows.append(dict(survey="KMOS3D", name=f"K{i}:{c.loc[j,'ID']}", z=r.z, logM=r.logMbar, Re=Re, V=r.Vcirc_kms, sigV=0.10,
                         xn=2.2, fDM=np.nan, gas="table", kid=c.loc[j, "ID"]))
    # KROSS: stars only (+ variant with Tacconi gas evaluated at loading time via flag)
    k = pd.read_csv(f"{REPO}/real_research/data/kross_harrison2017.csv")
    for i, r in k.iterrows():
        lm = math.log10(r.Mstar)
        rows.append(dict(survey="KROSS", name=f"KR{i}", z=r.z, logM=lm, logM_gas=lm + math.log10(1 + float(tacconi18_mu(r.z, lm))),
                         Re=r.Reff_kpc, V=r.VC_kms, sigV=0.10, xn=2.2, fDM=np.nan, gas="stars_only"))
    # MUSE-DARK II (Jeanneau+26 table E1): logMBar, Reff arcsec -> kpc, V2.0 at 2 Re
    m = pd.read_csv(f"{REPO}/prep_2026/jeanneau_refit/jeanneau26_catalog_cds.csv")
    for _, r in m.iterrows():
        Re = r.Reff * dA_kpc_per_arcsec(r.zR21)
        rows.append(dict(survey="MUSE2", name=str(r.IdR21), z=r.zR21, logM=r.logMBar, Re=Re, V=10 ** r.logV2_0,
                         sigV=r.s_logV2_0 * LN10, xn=3.36, fDM=np.nan, gas="table"))
    R = pd.DataFrame(rows)
    return R, dict(kmos_matched=nmatch, kmos_dropped=ndrop, kmos_ids=set(kmatch), rc_names=set(R[R.survey == "RC100"].name))

def load_phibss():
    d = pd.read_csv(f"{REPO}/data_assembly/kmos3d_phibss/phibss13_joined.csv")
    n_v = d.vrot_kms.notna().sum()
    d = d[d.vrot_kms.notna()]
    rh_opt = d.rh_opt_kpc; rh = d.rh_opt_kpc.fillna(d.rh_co_kpc)
    d = d.assign(rh=rh, rh_optonly=rh_opt)
    return d, n_v

# ---------------- physics per object ----------------
def per_object(R, a0key, xmode="native", nu=None, mass="tab", pointmass=False, xfix=None):
    """returns arrays: x used, g_bar (m/s2), y=g_bar/a0"""
    nu = nu or NU
    a0 = A0[a0key]
    Rd = R.Re.values * KPC / 1.68
    lm = R.logM.values.copy()
    if mass == "kross_gas":
        m = (R.survey == "KROSS").values
        lm[m] = R.loc[m, "logM_gas"].values
    Mkg = 10 ** lm * MSUN
    gunit = G * Mkg / Rd ** 2
    if xmode == "native": x = R.xn.values.copy()
    elif xmode == "1.31rh": x = np.full(len(R), 2.2)
    elif xmode == "rpeak": x = np.full(len(R), 2.15)
    elif xmode == "xfix": x = np.full(len(R), float(xfix))
    elif xmode in ("rflat", "rpeak_tot"):
        x = np.zeros(len(R)); grid = np.linspace(0.5, 20, 3901)
        fg = f_freeman(grid)
        for i in range(len(R)):
            gb = gunit[i] * fg
            V2 = gb * nu(gb / a0) * grid       # V^2 / Rd (units)
            lv = 0.5 * np.log(V2)
            sl = np.gradient(lv, np.log(grid))
            if xmode == "rflat":
                idx = np.where(np.abs(sl) < 0.05)[0]
                x[i] = grid[idx[0]] if len(idx) else grid[-1]
            else:
                k = int(np.argmax(V2))
                if 0 < k < len(grid) - 1: x[i] = grid[k]
                else:
                    idx = np.where(np.abs(sl) < 0.05)[0]
                    x[i] = grid[idx[0]] if len(idx) else grid[-1]
    else: raise ValueError(xmode)
    gb = gunit * (1.0 / x ** 2 if pointmass else f_freeman(x))
    return x, gb, gb / a0

def law_pred(gb, z, a0key, rival=False, nu=None):
    nu = nu or NU
    a0 = A0[a0key] * (E(z) if rival else 1.0)
    return gb * nu(gb / a0)

def slope_flat(gb, a0key, nu=None):
    nu = nu or NU
    e = 1e-4
    g1 = np.log10(gb * nu(gb * 10 ** e / A0[a0key])) ; g0 = np.log10(gb * nu(gb * 10 ** -e / A0[a0key]))
    return (np.log10(gb * 10 ** e * nu(gb * 10 ** e / A0[a0key])) - np.log10(gb * 10 ** -e * nu(gb * 10 ** -e / A0[a0key]))) / (2 * e)

# ---------------- main ----------------
def main():
    P(f"CFG90 run {'MUTATE (a0 x2)' if MUT else 'MAIN'}   a0can={A0['can']:.4e} a0alt={A0['alt']:.4e}")
    P("=" * 100)
    run_controls()
    R, aux = load()
    R["z"] = R.z.astype(float)
    P(f"\nloaded: " + ", ".join(f"{s}:{(R.survey==s).sum()}" for s in ["RC100", "MSA3D", "KMOS3D", "KROSS", "MUSE2"]) +
      f"   KMOS3D matched {aux['kmos_matched']} of 135, dropped {aux['kmos_dropped']}")
    check("C8a KMOS3D R_half match >= 95%", aux["kmos_matched"] >= 0.95 * 135, f"{aux['kmos_matched']}/135")
    # C5: RC100 disc g_bar vs (1-fDM) g_obs
    rc = R[R.survey == "RC100"]
    x, gb, y = per_object(rc, "can")
    gobs = (rc.V.values * 1e3) ** 2 / (rc.Re.values * KPC)
    gimp = (1 - rc.fDM.values) * gobs
    dif = np.log10(gb / gimp)
    med = np.median(dif)
    check("C5 disc g_bar vs (1-fDM) g_obs on RC100 (README -0.01 dex; pass |median| < 0.03)", abs(med) < 0.03, f"median {med:+.3f} dex, MAD {np.median(np.abs(dif-med)):.3f}, N={len(rc)}")
    # per-object canonical native
    res = {}
    for key in ("can", "alt"):
        x, gb, y = per_object(R, key)
        R["gb_" + key] = gb; R["y_" + key] = y; R["x_" + key] = x
    R["Rv_m"] = R.x_can * R.Re * KPC / 1.68
    R["gobs"] = (R.V * 1e3) ** 2 / R.Rv_m
    R["logg_obs"] = np.log10(R.gobs)
    R["slope"] = slope_flat(R.gb_can.values, "can")
    R["sigma"] = np.sqrt((2 * R.sigV / LN10) ** 2 + (R.slope * MASSFLOOR) ** 2)
    R["dflat"] = R.logg_obs - np.log10(law_pred(R.gb_can.values, R.z.values, "can"))
    R["drival"] = R.logg_obs - np.log10(law_pred(R.gb_can.values, R.z.values, "can", rival=True))
    R["gap"] = np.abs(np.log10(law_pred(R.gb_can.values, R.z.values, "can")) - np.log10(law_pred(R.gb_can.values, R.z.values, "can", rival=True)))
    R["gapsig"] = R.gap / R.sigma
    R["clean_dfm"] = True
    m = R.fDM.notna()
    gimp = (1 - R.fDM[m]) * R.gobs[m]
    R.loc[m, "clean_dfm"] = np.abs(np.log10(R.gb_can[m] / gimp)) < 0.5

    SUR = ["RC100", "MSA3D", "KMOS3D", "KROSS", "MUSE2"]
    P("\n" + "=" * 100 + "\nQ1: counts (canonical, native radii, disc baryons)")
    P(f"{'set':8s} {'N':>4s} {'<a0':>5s} {'<0.5a0':>7s} {'<0.3a0':>7s} | z>=1.5: {'<a0':>4s} {'<0.3a0':>7s} | CFG52 README (<a0,<0.3a0,z>=1.5 <a0,<0.3a0)")
    ref = {"RC100": (26, 4, 9, 1), "MSA3D": (19, 4, 3, 0), "KMOS3D": (16, 5, 2, 0), "KROSS": (106, 15, 0, 0), "MUSE2": (74, 43, 0, 0)}
    cnt = {}
    for s in SUR:
        q = R[R.survey == s]
        hz = q.z >= 1.5
        cnt[s] = (int((q.y_can < 1).sum()), int((q.y_can < 0.3).sum()), int(((q.y_can < 1) & hz).sum()), int(((q.y_can < 0.3) & hz).sum()))
        P(f"{s:8s} {len(q):4d} {cnt[s][0]:5d} {int((q.y_can<0.5).sum()):7d} {cnt[s][1]:7d} |          {cnt[s][2]:4d} {cnt[s][3]:7d} | {ref[s]}")
    tot5 = sum(cnt[s][0] for s in SUR)
    # ledger supplement
    led_txt = open(f"{REPO}/prep_2026/a0z_crossscale/highz_target_ledger_verified_2026.out").read()
    ledger_pub = []
    for line in led_txt.splitlines():
        mm = re.match(r"^(.{30,34}?)\s+([0-9]\.[0-9]{3})\s+\S+\s+\S+\s+PUB\s+([0-9.]+) \(PUB\)", line)
        if mm: ledger_pub.append((mm.group(1).strip(), float(mm.group(2)), float(mm.group(3))))
    led_below = [t for t in ledger_pub if t[2] * (1.0 if not MUT else 1 / MF) < 1]
    P(f"total g_bar<a0, five surveys: {tot5}   (README: 242 incl. ledger; the five README rows sum to 241)")
    P(f"ledger PUB point-valued rows parsed: {ledger_pub}; below a0: {[t[0] for t in led_below]}")
    tot6 = tot5 + len(led_below)
    P(f"total including ledger PUB rows: {tot6}")

    # Q2 gaps
    sel = R[R.y_can < 1]
    P("\n" + "=" * 100 + f"\nQ2: prediction gap flat vs a0 E(z) over the {len(sel)} discs with g_bar<a0 (five surveys)")
    n1 = int((sel.gapsig > 1).sum()); n2 = int((sel.gapsig > 2).sum())
    P(f"gap/sigma > 1 : {n1}     > 2 : {n2}     (CFG52 README: 16 and 0)")
    P(f"gap dex: median {sel.gap.median():.3f} (p16 {sel.gap.quantile(.16):.3f}, p84 {sel.gap.quantile(.84):.3f});  sigma_i median {sel.sigma.median():.3f} (p16 {sel.sigma.quantile(.16):.3f}, p84 {sel.sigma.quantile(.84):.3f})")
    for s in SUR:
        q = sel[sel.survey == s]
        if len(q): P(f"   {s:7s} N={len(q):3d} gap med {q.gap.median():.3f}  sigma med {q.sigma.median():.3f}  n(>1sig)={int((q.gapsig>1).sum())}  max gap/sig={q.gapsig.max():.2f}")
    P("top gap/sigma objects:"); P(sel.sort_values("gapsig", ascending=False).head(20)[["survey", "name", "z", "y_can", "gap", "sigma", "gapsig"]].to_string(index=False))
    check("C6 median sigma_i in 0.10-0.20 dex (README 0.13-0.16)", 0.10 <= sel.sigma.median() <= 0.20, f"{sel.sigma.median():.3f}")

    # Q3
    P("\n" + "=" * 100 + "\nQ3: z>=1.5 objects with g_bar<0.3 a0")
    q3 = {}
    for key in ("can", "alt"):
        q = R[(R.z >= 1.5) & (R["y_" + key] < 0.3)]
        q3[key] = q
        P(f"[{key}] raw N={len(q)}; clean (f_DM consistency) N={int(q.clean_dfm.sum())}")
        if len(q): P(q[["survey", "name", "z", "y_" + key, "clean_dfm"]].to_string(index=False))
    P("z>=1.5 objects with g_bar/a0 in [0.3,1.0), canonical (the whole z>=1.5 g_bar<a0 set):")
    z15 = R[(R.z >= 1.5) & (R.y_can < 1)].sort_values("y_can")
    P(z15[["survey", "name", "z", "y_can", "y_alt", "clean_dfm", "dflat", "drival", "gap", "sigma"]].round(3).to_string(index=False))
    z15a = R[(R.z >= 1.5) & (R.y_alt < 1)]
    P(f"z>=1.5 with g_bar<a0: canonical N={len(z15)}, alt N={len(z15a)}; by survey can {dict(z15.survey.value_counts())} alt {dict(z15a.survey.value_counts())}")
    P(f"ledger PUB rows at z>=1.5 below a0: {[t for t in led_below if t[1]>=1.5]}")
    # zC 410041
    zc = R[R.name.str.contains("410041")]
    P("zC 410041 row(s):"); P(zc[["survey", "name", "z", "y_can", "y_alt"]].to_string(index=False) if len(zc) else "none")

    # Q4 pooled
    P("\n" + "=" * 100 + "\nQ4: pooled z>=1.5, g_bar<a0")
    pz = z15
    Np = len(pz)
    df = pz.dflat.mean(); dr = pz.drival.mean()
    sig_pool = math.sqrt(np.sum((2 * pz.sigV / LN10) ** 2) / Np ** 2 + (pz.slope.mean() * MASSFLOOR) ** 2)
    P(f"N={Np}: <D_flat> = {df:+.4f}  <D_rival> = {dr:+.4f}   (CFG52 README: N=14, +0.135, -0.037)")
    P(f"sigma_pool = {sig_pool:.3f}; significance flat {df/sig_pool:+.2f} sigma, rival {dr/sig_pool:+.2f} sigma   (README: +1.0, -0.3)")
    P("by set: " + "; ".join(f"{s}: N={int((pz.survey==s).sum())} flat {pz[pz.survey==s].dflat.mean():+.3f} rival {pz[pz.survey==s].drival.mean():+.3f}" for s in SUR if (pz.survey == s).sum()))
    # overlap RC100-KMOS3D
    ov = [n for n in pz[pz.survey == "RC100"].name if n.replace(" ", "_") in aux["kmos_ids"]]
    ov_all = [n for n in R[R.survey == "RC100"].name if n.replace(" ", "_") in aux["kmos_ids"]]
    P(f"overlap diagnostics: RC100 rows whose ID is also a matched KMOS3D row: {len(ov_all)} of 100 (in the z>=1.5,g_bar<a0 pool: {len(ov)}: {ov})")

    # C7 selection mock
    P("\n" + "=" * 100 + "\nQ4-control C7: selection mock (flat law true, selection on noisy g_bar)")
    hz = R[R.z >= 1.5]
    pop = np.log10(hz.gb_can.values)
    rng = np.random.default_rng(90)
    def mock(noise, nmock=3000, npop=len(hz)):
        bias = []; ns = []
        for _ in range(nmock):
            lt = rng.choice(pop, npop) + rng.normal(0, 0.15, npop)
            zz = rng.choice(hz.z.values, npop)
            gt = 10 ** lt
            lo = lt + rng.normal(0, noise, npop)
            s = lo < math.log10(A0["can"])
            if s.sum() < 3: continue
            gobs_m = law_pred(gt, zz, "can") * 10 ** rng.normal(0, 0.10 / LN10 * 2, npop)
            pred_obs = law_pred(10 ** lo, zz, "can")
            bias.append(np.mean(np.log10(gobs_m[s]) - np.log10(pred_obs[s]))); ns.append(s.sum())
        b = np.array(bias); return b.mean(), b.std(), b.std() / math.sqrt(len(b)), np.mean(ns)
    b0 = mock(0.0); b2 = mock(0.20)
    P(f"noise 0.00 dex: bias {b0[0]:+.4f} (sd {b0[1]:.3f}, MC se {b0[2]:.4f}, mean N {b0[3]:.1f})")
    P(f"noise 0.20 dex: bias {b2[0]:+.4f} (sd {b2[1]:.3f}, MC se {b2[2]:.4f}, mean N {b2[3]:.1f})   README: +0.03 to +0.11")
    check("C7 mock null (noise 0 -> bias 0 within 3 se)", abs(b0[0]) < 3 * b0[2] + 1e-3, f"{b0[0]:+.4f} vs se {b0[2]:.4f}")
    check("C7 mock sign (noise 0.2 -> positive bias)", b2[0] > 3 * b2[2], f"{b2[0]:+.4f}")
    P(f"observed pooled flat offset {df:+.3f} minus mock 0.2-dex selection bias {b2[0]:+.3f} = {df-b2[0]:+.3f} dex")

    # Q5 PHIBSS
    P("\n" + "=" * 100 + "\nQ5: PHIBSS (Tacconi+2013) at the frozen radius")
    ph, n_v = load_phibss()
    def phib(sel_rule, xr=1.31, a0key="can", rhcol="rh"):
        d = ph.copy()
        d = d[(d[rhcol].notna()) & (d.z_co.notna())]
        n_pre = len(d)
        d = d[(d.co_upper_limit == 0) & (d.fgas_inconsistent_in_source == 0)]
        Rd = d[rhcol].values * KPC / 1.68
        x = np.full(len(d), xr * 1.68)
        gb = G * d.mbar_msun.values * MSUN / Rd ** 2 * f_freeman(x)
        return d, n_pre, gb / A0[a0key], x
    d, n_pre, yph, x = phib(None)
    P(f"rows with vrot {n_v}; with radius+z {n_pre}; after removing 6 upper limits and 3 inconsistent rows: {len(d)}   (CFG54: 51)")
    P(f"g_bar/a0 at 1.31 r_h: N<1: {(yph<1).sum()}   min {yph.min():.3f}, next {np.sort(yph)[:4].round(3)}, median {np.median(yph):.2f}, max {yph.max():.1f}  (CFG54: 0; lowest 1.10 then 1.11, 1.28; median 4.7; max 114)")
    P("radius sweep (in r_h): N(g_bar<a0)  [min y]   canonical | alt | (rh_opt only)  -- CFG54 post-hoc line: 1.31:0, 2:7 (0.63), 3:20 (0.29), 4:31 (0.16)")
    ph_res = {}
    for xr in (1.0, 1.31, 2, 3, 4, 6):
        dc, _, yc, _ = phib(None, xr, "can"); _, _, ya, _ = phib(None, xr, "alt"); do, _, yo, _ = phib(None, xr, "can", "rh_optonly")
        P(f"   {xr:4.2f} r_h: can {int((yc<1).sum()):3d} [{yc.min():.2f}] (<0.5: {int((yc<0.5).sum())}, <0.3: {int((yc<0.3).sum())}) | alt {int((ya<1).sum()):3d} [{ya.min():.2f}] (<0.3: {int((ya<0.3).sum())}) | opt-only n={len(do)} N<1 {int((yo<1).sum())}")
        ph_res[xr] = dict(can=int((yc < 1).sum()), alt=int((ya < 1).sum()), n=len(dc))
    dc, _, yc, _ = phib(None, 1.31, "can"); da, _, ya, _ = phib(None, 1.31, "alt")
    P(f"at 1.31 r_h: alt N<1 = {(ya<1).sum()}, N<0.3 alt = {(ya<0.3).sum()}, N<0.3 can = {(yc<0.3).sum()}  (CFG54 referee note: alt ~2 rows below 0.3 a0 by scaling; not run)")
    # r_peak/r_flat for PHIBSS
    Pn = pd.DataFrame(dict(survey="PH", name=dc.name.values, z=dc.z_co.values, logM=np.log10(dc.mbar_msun.values), Re=dc.rh.values, xn=2.2))
    for xm in ("rpeak", "rflat", "rpeak_tot"):
        xx, gg, yy = per_object(Pn, "can", xm); xa, ga, ya2 = per_object(Pn, "alt", xm)
        P(f"   PHIBSS {xm:9s}: can N<1 {int((yy<1).sum())} min {yy.min():.2f} <0.3 {int((yy<0.3).sum())}; alt N<1 {int((ya2<1).sum())} <0.3 {int((ya2<0.3).sum())}  (median x {np.median(xx):.1f} R_d)")

    # Sensitivity grid
    P("\n" + "=" * 100 + "\nSENSITIVITY: count of discs (g_bar < thr*a0) [all z / z>=1.5], five surveys, by radius definition and footing")
    hdr = f"{'radius':10s} {'foot':4s} {'thr':>4s} | " + " ".join(f"{s:>9s}" for s in SUR) + " |   total    | z>=1.5 by set (RC,MSA,KMOS,KR,MUSE) total"
    P(hdr)
    grid = {}
    for xm in ("native", "1.31rh", "rpeak", "rpeak_tot", "rflat"):
        for key in ("can", "alt"):
            x_, gb_, y_ = per_object(R, key, xm)
            for thr in (0.3, 0.5, 1.0):
                sel_ = y_ < thr
                allc = [int((sel_ & (R.survey == s).values).sum()) for s in SUR]
                hzc = [int((sel_ & (R.survey == s).values & (R.z >= 1.5).values).sum()) for s in SUR]
                grid[f"{xm}|{key}|{thr}"] = dict(all=allc, z15=hzc)
                P(f"{xm:10s} {key:4s} {thr:4.1f} | " + " ".join(f"{c:9d}" for c in allc) + f" | {sum(allc):4d}      | {hzc} {sum(hzc)}")
    P("\nother variants (canonical, native, thr 1.0 / 0.3): point-mass g_bar; alt kernel; KROSS with Tacconi gas")
    for lab, kw in (("point mass", dict(pointmass=True)), ("kross+gas", dict(mass="kross_gas"))):
        x_, gb_, y_ = per_object(R, "can", "native", **kw)
        P(f"   {lab:11s}: total<a0 {int((y_<1).sum())}, <0.3a0 {int((y_<0.3).sum())}; z>=1.5 <a0 {int(((y_<1)&(R.z>=1.5).values).sum())}, <0.3 {int(((y_<0.3)&(R.z>=1.5).values).sum())}; KROSS <a0 {int(((y_<1)&(R.survey=='KROSS').values).sum())}")
    # alt kernel: counts unchanged (g_bar only); gap counts change
    NUs = nu_simple
    gsim = law_pred(R.gb_can.values, R.z.values, "can", nu=NUs); gsimr = law_pred(R.gb_can.values, R.z.values, "can", rival=True, nu=NUs)
    gapS = np.abs(np.log10(gsim) - np.log10(gsimr)); slS = slope_flat(R.gb_can.values, "can", nu=NUs)
    sigS = np.sqrt((2 * R.sigV / LN10) ** 2 + (slS * MASSFLOOR) ** 2)
    ms = (R.y_can < 1).values
    P(f"   simple kernel: gap>1 sigma: {int((gapS[ms]/sigS[ms]>1).sum())}, >2 sigma: {int((gapS[ms]/sigS[ms]>2).sum())}")
    # footing sensitivity of gap counts
    for key in ("alt",):
        gf = law_pred(R.gb_alt.values, R.z.values, key); gr = law_pred(R.gb_alt.values, R.z.values, key, rival=True)
        gapA = np.abs(np.log10(gf) - np.log10(gr)); slA = slope_flat(R.gb_alt.values, key)
        sigA = np.sqrt((2 * R.sigV / LN10) ** 2 + (slA * MASSFLOOR) ** 2); msa = (R.y_alt < 1).values
        P(f"   alt footing: N<a0 {int(msa.sum())}; gap>1 sigma {int((gapA[msa]/sigA[msa]>1).sum())}, >2 sigma {int((gapA[msa]/sigA[msa]>2).sum())}; z>=1.5 pooled: "
          f"flat {np.mean((R.logg_obs-np.log10(gf))[msa&(R.z>=1.5).values]):+.3f} rival {np.mean((R.logg_obs-np.log10(gr))[msa&(R.z>=1.5).values]):+.3f} N={int((msa&(R.z>=1.5).values).sum())}")
    # sigma-threshold sensitivity of the count of >1 sigma
    for thr in (0.3, 0.5, 1.0):
        s2 = R[R.y_can < thr]
        P(f"   gap>1 sigma among g_bar<{thr}a0: {int((s2.gapsig>1).sum())} of {len(s2)}; >2 sigma {int((s2.gapsig>2).sum())}; >1.5 sigma {int((s2.gapsig>1.5).sum())}")

    # ---------------- verdict block ----------------
    P("\n" + "=" * 100 + "\nREPRODUCTION SCORECARD (main-run values against CFG52/CFG54 README statements; compared BEFORE reading their scripts/outputs)")
    sc = {
        "Q1 total g_bar<a0 = 242": (tot6, 242),
        "Q1 five-survey total = 241": (tot5, 241),
        "Q2 n(gap>1 sigma) = 16": (n1, 16),
        "Q2 n(gap>2 sigma) = 0": (n2, 0),
        "Q3 clean z>=1.5 <0.3a0 canonical = 0": (int(q3["can"].clean_dfm.sum()), 0),
        "Q3 raw z>=1.5 <0.3a0 alt = 2 (RC100)": (len(q3["alt"]), 2),
        "Q4 N pooled = 14": (Np, 14),
        "Q4 D_flat = +0.135": (round(df, 3), 0.135),
        "Q4 D_rival = -0.037": (round(dr, 3), -0.037),
        "Q5 PHIBSS usable N = 0": (int((yph < 1).sum()), 0),
        "Q5 PHIBSS sample N = 51": (len(d), 51),
    }
    for s in SUR:
        for i, nm in enumerate(("<a0", "<0.3a0", "z15<a0", "z15<0.3a0")):
            sc[f"{s} {nm} = {ref[s][i]}"] = (cnt[s][i], ref[s][i])
    n_match = 0
    for k, (mine, theirs) in sc.items():
        ok = abs(mine - theirs) < (5e-4 if isinstance(theirs, float) else 0.5)
        n_match += ok
        P(f"   {'MATCH ' if ok else 'DIFFER'}  {k:45s} mine {mine}")
    P(f"reproduced {n_match} of {len(sc)} items")
    all_ctrl = all(ctrl.values())
    P(f"\ncontrols: {sum(ctrl.values())}/{len(ctrl)} pass")
    res = dict(mutate=MUT, controls=ctrl, counts=cnt, tot5=tot5, tot_with_ledger=tot6, n1=n1, n2=n2, pooled=dict(N=Np, flat=df, rival=dr, sigma=sig_pool),
               phibss=dict(n=len(d), nlt1=int((yph < 1).sum()), min=float(yph.min()), sweep={str(k): v for k, v in ph_res.items()}),
               q3=dict(can_raw=len(q3["can"]), can_clean=int(q3["can"].clean_dfm.sum()), alt_raw=len(q3["alt"])), grid=grid, score=dict(match=int(n_match), n=len(sc)),
               mock=dict(b0=b0, b2=b2))
    json.dump(res, open(f"{HERE}/cfg90{TAG}_results.json", "w"), indent=1, default=float)
    R.to_csv(f"{HERE}/cfg90{TAG}_per_object.csv", index=False)
    # exit logic
    if not MUT:
        rc = 0 if all_ctrl else 1
    else:
        base = json.load(open(f"{HERE}/cfg90_results.json"))
        dir_ok = all(cnt[s][i] >= base["counts"][s][i] for s in SUR for i in range(4)) and tot5 > base["tot5"]
        equal = (cnt == {k: tuple(v) for k, v in base["counts"].items()})
        P(f"MUTATE direction test (all counts >= main, total strictly larger): {'PASS' if dir_ok else 'FAIL'}; counts equal main: {equal}")
        P(f"MUTATE main total {base['tot5']} -> {tot5}; z>=1.5 pool N {base['pooled']['N']} -> {Np}; PHIBSS N<a0 {base['phibss']['nlt1']} -> {int((yph<1).sum())}")
        rc = 1 if (dir_ok and not equal and all_ctrl_mut(ctrl)) else 0
    open(f"{HERE}/cfg90{TAG}.out", "w").write("\n".join(out_lines) + f"\nexit {rc}\n")
    sys.exit(rc)

def all_ctrl_mut(c):
    # under MUTATE the a0 closed-form controls (C1a/b/c) are expected to fail (a0 doubled) -> ignore them; others must pass
    return all(v for k, v in c.items() if not k.startswith("C1a") and not k.startswith("C1b"))

if __name__ == "__main__":
    main()
