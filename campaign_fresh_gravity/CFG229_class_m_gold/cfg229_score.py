#!/usr/bin/env python3
"""CFG229 -- SCORING: g_obs, g_bar, D, the Newtonian-floor status, delta_L for FLAT / PROXY / H(z) / M-DEC, the pooled class-M statistic, and the IMPLIED a0 (Addendum 1) with its error budget,
for the seven class-M galaxies.  Read the pre-flight first: cfg229_preflight.py was committed (e3f30dee5) before this script existed and is the GATE for every wording.
Compilation; class-M gas; calibration-limited; not blind for the ALPAKA order of magnitude; not a detection.  LambdaCDM has no a0: the proxy is an effective-a0 PROXY.  kappa = 1/2 FITTED.
No sentence of this lane says the data favour a law; the implied a0 is descriptive, not a verdict.
Frozen criteria: FROZEN_CRITERIA.md (5c131c037) + Addendum 1 (7e3b14d20).
Run: python3 campaign_fresh_gravity/CFG229_class_m_gold/cfg229_score.py        MUTATE=1: g_obs x 1.5;  MUTATE=2: +0.30 dex on both baryon components;  MUTATE=3: the helium factor removed"""
import os, sys, io, math, json, contextlib, time, hashlib, itertools
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import i0e, i1e, k0e, k1e

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MODE = os.environ.pop("MUTATE", "").strip()                               # '', '1', '2', '3'
TAG = {"": "", "1": "_MUTATE1", "2": "_MUTATE2", "3": "_MUTATE3"}[MODE]
sys.path.insert(0, CFG)
import CFG4_common as K
sys.path.insert(0, os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z"))
import zcommon as Z1                                                     # READ-ONLY: lcdm_native
sys.path.insert(0, LANE)
from a0implied import implied, lever, kernel_slope, nuv

OUT, CHK = [], []
T0 = time.time()
G2SI = 1e6 / 3.0856775814913673e19
G_KPC = 4.30091e-6
XN = 1.678
OM = 0.315
HE, LOGHE = 1.36, math.log10(1.36)
SEED = 229
NB = 10000
B_GAS, B_STAR, IN_GAS = 0.093, 0.30, 0.03
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
NU, A0 = KER["nu_mono"], A0F["canonical"]
ALT_OVER_CAN = A0F["alt"] / A0F["canonical"]
LAWN = ("FLAT", "PROXY", "H(z)", "M-DEC")


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def E(zz):
    return math.sqrt(OM * (1 + zz) ** 3 + 1 - OM)


def R_dec(zz, w0=-0.838, wa=-0.62):
    return math.sqrt((1.0 + zz) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * zz / (1.0 + zz)))


LAWS = {"FLAT": lambda zz: 1.0, "PROXY": lambda zz: Z1.lcdm_native(zz), "H(z)": E, "M-DEC": R_dec}


def disc_v2(M, Re, Rr):
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def gdisc(M, Re, Rr):                                                    # m/s^2, thin exponential disc
    return disc_v2(M, Re, Rr) / Rr * G2SI


def gsph(M, Re, Rr):                                                     # m/s^2, enclosed exponential-disc mass as a point mass
    x = Rr / (Re / XN)
    return G_KPC * M * (1 - (1 + x) * math.exp(-x)) / Rr ** 2 * G2SI


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {MODE or 'none'}" + {"": "", "1": " (g_obs x 1.5)", "2": " (+0.30 dex on both baryon components)", "3": " (helium factor removed)"}[MODE])
ST = pd.read_csv(os.path.join(LANE, "cfg229_inputs_static.csv"))
KN = pd.read_csv(os.path.join(LANE, "cfg229_inputs_kin.csv"))
PF = json.load(open(os.path.join(LANE, "cfg229_preflight_results.json")))
n = len(ST)
gid = ST["gid"].tolist()
z = ST["z"].values
FL = {L: np.array([LAWS[L](float(x)) for x in z]) for L in LAWS}
Ms0 = ST["Mstar"].values * (10 ** 0.30 if MODE == "2" else 1.0)
lg_gas = ST["logMgas_He"].values - (LOGHE if MODE == "3" else 0.0) + (0.30 if MODE == "2" else 0.0)
Mg0 = 10 ** lg_gas
Mg_noHe = 10 ** (ST["logMH2"].values + (0.30 if MODE == "2" else 0.0))
Re0, R0 = ST["Re_kpc"].values, ST["R_kpc"].values
e_st, e_gas = ST["e_logMstar_inner"].values, ST["e_logMH2"].values
i_used, e_i, i_alt = ST["i_used"].values, ST["e_i_used"].values, ST["i_alt"].values
V_pub, V_noP, alpha_pub = KN["V_pub"].values.astype(float), KN["V_noP"].values.astype(float), KN["alpha_pub"].values.astype(float)
sig, eVhi, eVlo = KN["sigma"].values.astype(float), KN["eV_hi"].values.astype(float), KN["eV_lo"].values.astype(float)
GM = 1.5 if MODE == "1" else 1.0
is_alp = np.array([g.startswith("ALPAKA") for g in gid])


def gobs_of(V2, R):
    return V2 / R * G2SI * GM


def gbar_of(Ms, Mg, Re, R, tg=0.0, ts=0.0, star_fac=1.0, sph=False):
    f = gsph if sph else gdisc
    return f(Ms * 10 ** ts, Re * star_fac, R) + f(Mg * 10 ** tg, Re, R)


def delta_L(go, gb, zz_F, nu=NU, a0=A0):
    return np.log10(go / (gb * nu(gb / (a0 * zz_F))))


# ------------------------------------------------------------------ baseline
V2_base = V_noP ** 2 + alpha_pub * sig ** 2
GO = np.array([float(gobs_of(V2_base[i], R0[i])) for i in range(n)])
GB = np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i], R0[i])) for i in range(n)])
D = GO / GB
y = GB / A0
P(f"\nBASELINE (thin exponential disc for stars + gas with one R_e; gas = 1.36 x 10^logMH2{' [MUTATE: no He]' if MODE == '3' else ''}; the source's own velocity convention)")
P("  galaxy        z      R (kpc)  V (km/s)  sigma  g_obs (m/s2)  g_bar (m/s2)  y=g_bar/a0   D=g_obs/g_bar   gas share (mass)   R/beam")
for i in range(n):
    gsh = Mg0[i] / (Mg0[i] + Ms0[i])
    P(f"  {gid[i]:12s} {z[i]:.3f}  {R0[i]:7.2f}  {np.sqrt(V2_base[i]):7.1f}  {sig[i]:5.0f}  {GO[i]:.3e}   {GB[i]:.3e}   {y[i]:9.2f}   {D[i]:10.3f}        {gsh:.2f}          {ST['R_over_beam'][i]:.2f}")

P("\nDELTA_L = log10[g_obs / (g_bar nu_mono(g_bar / (a0 F_L(z))))]  (canonical footing; the alt footing and P2 below)")
DL = {L: delta_L(GO, GB, FL[L], NU, A0) for L in LAWN}
P("  galaxy        FLAT     PROXY    H(z)     M-DEC     | alt footing: FLAT  H(z)   | P2 kernel: FLAT  H(z)")
DL_alt = {L: delta_L(GO, GB, FL[L], NU, A0F["alt"]) for L in LAWN}
DL_p2 = {L: delta_L(GO, GB, FL[L], KER["P2"], A0) for L in LAWN}
for i in range(n):
    P(f"  {gid[i]:12s} {DL['FLAT'][i]:+.3f}   {DL['PROXY'][i]:+.3f}   {DL['H(z)'][i]:+.3f}   {DL['M-DEC'][i]:+.3f}     | {DL_alt['FLAT'][i]:+.3f} {DL_alt['H(z)'][i]:+.3f}   | {DL_p2['FLAT'][i]:+.3f} {DL_p2['H(z)'][i]:+.3f}")

# ------------------------------------------------------------------ diagnostic (POST HOC, added after the first scoring run)
P("\nDIAGNOSTIC (POST HOC, added after the first scoring run and labelled as such): which baryon component exceeds the dynamics?  M_dyn(<R) = V^2 R / G (spherical shortcut); D restricted to the stars or to the gas alone")
P("  galaxy        log M*   log M_gas(He)  log M_dyn(<R)   M*/M_dyn   M_bar/M_dyn   D (stars only)   D (gas only)")
DIAG = {}
for i in range(n):
    Md = V2_base[i] * R0[i] / G_KPC
    Dst, Dga = GO[i] / float(gdisc(Ms0[i], Re0[i], R0[i])), GO[i] / float(gdisc(Mg0[i], Re0[i], R0[i]))
    DIAG[gid[i]] = dict(logMdyn=math.log10(Md), Mstar_over_Mdyn=Ms0[i] / Md, Mbar_over_Mdyn=(Ms0[i] + Mg0[i]) / Md, D_stars=Dst, D_gas=Dga)
    P(f"  {gid[i]:12s} {math.log10(Ms0[i]):6.2f}   {math.log10(Mg0[i]):8.2f}        {math.log10(Md):6.2f}        {Ms0[i] / Md:6.2f}       {(Ms0[i] + Mg0[i]) / Md:6.2f}         {Dst:7.2f}        {Dga:7.2f}")

# ------------------------------------------------------------------ pooled medians
IDXB = np.random.default_rng(SEED).integers(0, n, size=(NB, n))


def med_ci(d, idx):
    d = np.asarray(d)[idx]
    m = len(idx)
    ib = np.random.default_rng(SEED * 1000 + m).integers(0, m, size=(NB, m))
    bs = np.median(d[ib], axis=1)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


# ------------------------------------------------------------------ the Newtonian floor (law-independent) and variants
def variant_space(i):
    """all (R, V^2, g_bar) corners of the declared outer bands for galaxy i; returns D at each"""
    rings = [("V_ext@R_ext", R0[i], V_noP[i])]
    if is_alp[i]:
        rings += [("V_ring@R_ext", R0[i], KN["V_ring"][i]), ("V_ext@R_mean", KN["R_mean_last2_kpc"][i], V_noP[i])]
    incs = [("i_used", 1.0)]
    if is_alp[i]:
        for lab, inew in (("i_alt", i_alt[i]), ("i_used-1sig", max(5.0, i_used[i] - e_i[i])), ("i_used+1sig", min(85.0, i_used[i] + e_i[i]))):
            incs.append((lab, math.sin(math.radians(i_used[i])) / math.sin(math.radians(inew))))
    alphas = (0.0, 1.68, 3.36)
    geos = [("thin", dict()), ("thin Re x1.5", dict(refac=1.5)), ("thin Re /1.5", dict(refac=1 / 1.5)), ("stars 2Re", dict(star_fac=2.0)), ("spherical", dict(sph=True))]
    out = []
    for (rl, Rr, Vr), (il, fv), al, (gl, gk) in itertools.product(rings, incs, alphas, geos):
        if not math.isfinite(Vr):
            continue
        go = gobs_of((Vr * fv) ** 2 + al * (sig[i] * fv) ** 2, Rr)
        kw = dict(gk); re_ = Re0[i] * kw.pop("refac", 1.0)
        gbt = float(gbar_of(Ms0[i], Mg0[i], re_, Rr, tg=-B_GAS, ts=-B_STAR, **kw))
        out.append((go / gbt, (rl, il, al, gl)))
    return out


status = []
Dbest = []
for i in range(n):
    sp = variant_space(i)
    db = max(sp, key=lambda t: t[0])
    Dbest.append(db)
    status.append("PASS" if D[i] >= 1 else ("BAND-DEPENDENT" if db[0] >= 1 else "ROBUST FAIL"))
P("\nNEWTONIAN FLOOR (every law has nu >= 1, so D < 1 is a baryon-model inconsistency for ANY of them): status PASS if D >= 1; BAND-DEPENDENT if D < 1 but D >= 1 at the most favourable corner of the declared outer bands (gas -0.093, stars -0.30, geometry, pressure, ALPAKA ring and inclination variants); ROBUST FAIL otherwise")
for i in range(n):
    P(f"  {gid[i]:12s} D = {D[i]:6.3f}; most favourable corner D_best = {Dbest[i][0]:6.3f} ({Dbest[i][1][0]}, {Dbest[i][1][1]}, alpha {Dbest[i][1][2]}, {Dbest[i][1][3]}) -> {status[i]}")
npass, nband, nfail = status.count("PASS"), status.count("BAND-DEPENDENT"), status.count("ROBUST FAIL")
P(f"  => PASS {npass}, BAND-DEPENDENT {nband}, ROBUST FAIL {nfail}")
PASSI = [i for i in range(n) if status[i] == "PASS"]

P("\nPOOLED CLASS-M RESULT (this lane's own rule N_M >= 5; median delta with the 10,000-resample galaxy bootstrap 95% interval; DESCRIPTIVE; the pre-flight gate below decides what may be said)")
POOL = {}
for sname, idx in (("ALL7", list(range(n))), ("ALPAKA5", [i for i in range(n) if is_alp[i]]), ("BX610+ALESS", [i for i in range(n) if not is_alp[i]]), ("PASS subset", PASSI)):
    if len(idx) < 2:
        P(f"  {sname}: N = {len(idx)} (< 2): no pooled statistic"); continue
    POOL[sname] = {}
    for L in LAWN:
        m, lo, hi = med_ci(DL[L], idx)
        POOL[sname][L] = (m, lo, hi)
    P(f"  {sname:12s} (N = {len(idx)}): " + "   ".join(f"{L} {POOL[sname][L][0]:+.3f} [{POOL[sname][L][1]:+.3f}, {POOL[sname][L][2]:+.3f}]" for L in LAWN) + f"   | median(FLAT - H(z)) = {np.median(DL['FLAT'][idx] - DL['H(z)'][idx]):+.3f}; median D = {np.median(D[idx]):.3f}")

# ------------------------------------------------------------------ bands
P("\nBANDS: the median-free per-galaxy delta_FLAT at the band corners (gas inner +-0.03 / outer +-0.093; stars inner +-1 sigma / outer +-0.30; joint = same sign), and the set medians")
BAND = {}
for kind, (tg, ts) in (("gas -outer", (-B_GAS, np.zeros(n))), ("gas -inner", (-IN_GAS, np.zeros(n))), ("gas +inner", (IN_GAS, np.zeros(n))), ("gas +outer", (B_GAS, np.zeros(n))),
                       ("stars -outer", (0.0, np.full(n, -B_STAR))), ("stars -inner", (0.0, -e_st)), ("stars +inner", (0.0, e_st)), ("stars +outer", (0.0, np.full(n, B_STAR))),
                       ("joint -outer", (-B_GAS, np.full(n, -B_STAR))), ("joint -inner", (-IN_GAS, -e_st)), ("joint +inner", (IN_GAS, e_st)), ("joint +outer", (B_GAS, np.full(n, B_STAR)))):
    gbt = np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i], R0[i], tg=tg, ts=(ts[i] if hasattr(ts, "__len__") else ts))) for i in range(n)])
    BAND[kind] = dict(gb=gbt, dFLAT=delta_L(GO, gbt, FL["FLAT"], NU, A0), dHz=delta_L(GO, gbt, FL["H(z)"], NU, A0))
P("  band          " + "  ".join(f"{g[:10]:>10s}" for g in gid) + "   median ALL7")
for kind in BAND:
    P(f"  {kind:13s} " + "  ".join(f"{v:+10.3f}" for v in BAND[kind]["dFLAT"]) + f"   {np.median(BAND[kind]['dFLAT']):+.3f}")

# ------------------------------------------------------------------ sensitivities (beside, never substituted)
P("\nSENSITIVITIES (delta_FLAT / delta_H(z) per galaxy; beside the baseline, never substituted)")
SENS = {}


def sens_line(label, go_arr, gb_arr):
    dF, dH = delta_L(go_arr, gb_arr, FL["FLAT"], NU, A0), delta_L(go_arr, gb_arr, FL["H(z)"], NU, A0)
    SENS[label] = dict(dFLAT=dF.tolist(), dHz=dH.tolist())
    P(f"  {label:44s} " + " ".join(f"{a:+.2f}/{b:+.2f}" for a, b in zip(dF, dH)) + f"   median {np.median(dF):+.3f}/{np.median(dH):+.3f}")


P("  variant                                      " + " ".join(f"{g[:8]:>10s}" for g in gid))
for al in (0.0, 1.68, 3.36):
    sens_line(f"pressure alpha = {al} (V^2 = V_noP^2 + alpha sigma^2)", np.array([float(gobs_of(V_noP[i] ** 2 + al * sig[i] ** 2, R0[i])) for i in range(n)]), GB)
for lab, ff in (("R_e x 1.5", dict(refac=1.5)), ("R_e / 1.5", dict(refac=1 / 1.5)), ("stars at 2 R_e", dict(star_fac=2.0)), ("spherical enclosed mass", dict(sph=True))):
    gbv = np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i] * ff.get("refac", 1.0), R0[i], star_fac=ff.get("star_fac", 1.0), sph=ff.get("sph", False))) for i in range(n)])
    sens_line(lab, GO, gbv)
sens_line("no helium factor (gas = 10^logMH2)", GO, np.array([float(gdisc(Ms0[i], Re0[i], R0[i]) + gdisc(Mg_noHe[i], Re0[i], R0[i])) for i in range(n)]))
for lab, col in (("Dunne table ad", "logMH2_ad"), ("Dunne table dax", "logMH2_dax"), ("Dunne table xa", "logMH2_xa"), ("Dunne table xd", "logMH2_xd")):
    v = ST[col].values
    if np.isfinite(v).any():
        gbv = np.array([float(gdisc(Ms0[i], Re0[i], R0[i]) + gdisc(10 ** (v[i] + LOGHE), Re0[i], R0[i])) if np.isfinite(v[i]) else float("nan") for i in range(n)])
        sens_line(lab + " (gas, with He)", GO, gbv)
alpi = [i for i in range(n) if is_alp[i]]
for lab, Rsel, Vsel in (("ALPAKA: outermost digitised ring V at R_ext", "R0", "V_ring"), ("ALPAKA: V_ext at the mean radius of the last two rings", "Rmean", "V_noP")):
    go_ = GO.copy(); gb_ = GB.copy()
    for i in alpi:
        Rr = R0[i] if Rsel == "R0" else KN["R_mean_last2_kpc"][i]
        Vr = KN["V_ring"][i] if Vsel == "V_ring" else V_noP[i]
        go_[i] = float(gobs_of(Vr ** 2, Rr)); gb_[i] = float(gbar_of(Ms0[i], Mg0[i], Re0[i], Rr))
    sens_line(lab, go_, gb_)
for lab, key in (("ALPAKA inclination: the other of (i_HST, i_ALMA)", "alt"), ("ALPAKA inclination: i_used - 1 sigma", "lo"), ("ALPAKA inclination: i_used + 1 sigma", "hi")):
    go_ = GO.copy()
    for i in alpi:
        inew = {"alt": i_alt[i], "lo": max(5.0, i_used[i] - e_i[i]), "hi": min(85.0, i_used[i] + e_i[i])}[key]
        go_[i] = GO[i] * (math.sin(math.radians(i_used[i])) / math.sin(math.radians(inew))) ** 2
    sens_line(lab, go_, GB)

# ------------------------------------------------------------------ the pre-flight GATE
P("\nPRE-FLIGHT GATE (cfg229_preflight.py, committed before this script; read from cfg229_preflight_results.json)")
GATE = {}
for sname in ("ALL7", "ALPAKA5", "BX610+ALESS") + tuple(gid):
    r = PF["RES"][sname]
    GATE[sname] = r["rule"]["H(z)"]["outer"] or r["rule"]["PROXY"]["outer"]
P("  flat vs H(z) / vs PROXY at the JOINT OUTER band: " + "; ".join(f"{s}: {'POSSIBLE' if (PF['RES'][s]['rule']['H(z)']['outer'] or PF['RES'][s]['rule']['PROXY']['outer']) else 'NOT POSSIBLE'}" for s in ("ALL7", "ALPAKA5", "BX610+ALESS")))
ANY_POSSIBLE = any(GATE.values())
P(f"  => {'a separation is POSSIBLE in at least one set: law statements are allowed ONLY for that set' if ANY_POSSIBLE else 'NOT POSSIBLE in any set, so NO sentence of this lane may say any law is separated, preferred or disfavoured; the delta table is descriptive'}")
if len(PASSI) >= 3:
    P("  floor-PASS subset has N >= 3: its rule would be recomputed by the pre-flight function (not needed if N < 3)")
else:
    P(f"  the floor-PASS subset has N = {len(PASSI)} (< 3): no pooled law statement is possible from it")

# ------------------------------------------------------------------ IMPLIED a0 (Addendum 1)
P("\nIMPLIED a0 (Addendum 1; descriptive, not a verdict).  s* = the root of median_i log10[D_i / nu_mono(g_bar,i/(a0 s))] = 0 (CFG223's estimator); a0_implied = s* x 9.3603e-11 m/s^2 (footing-independent); the alt footing 1.1312e-10 gives the ratio s*/%.4f" % ALT_OVER_CAN)
P("  z ~ 0 reference (QUOTED from the record, no SPARC analysis here): canonical 9.3603e-11 and alt 1.1312e-10 m/s^2 (CFG4_common.A0), which SPARC fits at equal quality at fixed Upsilon (CFG0 F9: 0.108 dex at the canonical footing, Upsilon 0.70); a0 and Upsilon are degenerate (CFG4 H2b: best free a0 1.37e-10 for nu_mono and 1.78e-10 for P2 at Upsilon 0.50); a free SPARC fit gives kappa ~ 0.46 at the canonical footing (CFG0 F7)")
IMPL = {}


def s_star(Dv, gbv, idx, nu=NU, a0=A0):
    ls, unb = implied(np.asarray(Dv)[idx], np.asarray(gbv)[idx], nu, a0)
    return float(ls[0]), bool(unb[0])


def fmt(v):
    ls, unb = v
    if unb:
        return "no root" if ls <= -2.99 or ls >= 2.99 else f"{10 ** ls:.3g}*"
    return f"{10 ** ls:.3g}"


sets_imp = {g: [i] for i, g in enumerate(gid)}
sets_imp.update({"ALL7": list(range(n)), "ALPAKA5": alpi, "BX610+ALESS": [i for i in range(n) if not is_alp[i]]})
if len(PASSI) >= 3:
    sets_imp["PASS subset"] = PASSI
rngi = np.random.default_rng(SEED + 1)
BMC = 10000
# per-galaxy Monte Carlo: velocity (split normal), ALPAKA inclination (truncated normal), random baryon errors
def split_normal(v, ehi, elo, size):
    g = rngi.normal(size=size)
    return v + np.where(g > 0, g * ehi, g * elo)


MC = {}
for i in range(n):
    Vd = split_normal(np.sqrt(V2_base[i]), eVhi[i], eVlo[i], BMC)
    fac = np.ones(BMC)
    if is_alp[i]:
        ii = rngi.normal(i_used[i], e_i[i], BMC)
        for _ in range(60):
            bad = (ii < 5) | (ii > 85)
            if not bad.any(): break
            ii[bad] = rngi.normal(i_used[i], e_i[i], int(bad.sum()))
        fac = (math.sin(math.radians(i_used[i])) / np.sin(np.radians(ii))) ** 2
    god = (Vd ** 2 / R0[i] * G2SI * GM) * fac
    Msd, Mgd = Ms0[i] * 10 ** rngi.normal(0, e_st[i], BMC), Mg0[i] * 10 ** rngi.normal(0, e_gas[i], BMC)
    gbd = gdisc(Msd, Re0[i], R0[i]) + gdisc(Mgd, Re0[i], R0[i])
    ls, unb = implied((god / gbd)[:, None], gbd[:, None], NU, A0)
    ok = ~unb
    MC[gid[i]] = dict(frac_noroot=float(unb.mean()), q=[float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5)
for sname, idx in sets_imp.items():
    s0 = s_star(D, GB, idx)
    lam, lflag = lever(D[idx], GB[idx], NU, A0)
    lam = float(lam[0]); lflag = bool(lflag[0])
    if lflag or s0[1]:
        lam = float("nan")                                                # undefined where there is no root (the set cannot be shifted onto a root)
    sl = float(np.median(kernel_slope(NU, GB[idx] / A0)))
    # systematic corners
    def s_at(tg, ts):
        gbt = np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i], R0[i], tg=tg, ts=(ts[i] if hasattr(ts, "__len__") else ts))) for i in range(n)])
        return s_star(GO / gbt, gbt, idx)
    corners = {}
    for kind, (tg, ts) in (("gas -inner", (-IN_GAS, np.zeros(n))), ("gas +inner", (IN_GAS, np.zeros(n))), ("gas -outer", (-B_GAS, np.zeros(n))), ("gas +outer", (B_GAS, np.zeros(n))),
                           ("stars -inner", (0.0, -e_st)), ("stars +inner", (0.0, e_st)), ("stars -outer", (0.0, np.full(n, -B_STAR))), ("stars +outer", (0.0, np.full(n, B_STAR))),
                           ("joint -inner", (-IN_GAS, -e_st)), ("joint +inner", (IN_GAS, e_st)), ("joint -outer", (-B_GAS, np.full(n, -B_STAR))), ("joint +outer", (B_GAS, np.full(n, B_STAR)))):
        corners[kind] = s_at(tg, ts)
    # variants
    var = {}
    for al in (0.0, 1.68, 3.36):
        goa = np.array([float(gobs_of(V_noP[i] ** 2 + al * sig[i] ** 2, R0[i])) for i in range(n)])
        var[f"alpha {al}"] = s_star(goa / GB, GB, idx)
    for lab, ff in (("R_e x1.5", dict(refac=1.5)), ("R_e /1.5", dict(refac=1 / 1.5)), ("stars 2R_e", dict(star_fac=2.0)), ("spherical", dict(sph=True))):
        gbv = np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i] * ff.get("refac", 1.0), R0[i], star_fac=ff.get("star_fac", 1.0), sph=ff.get("sph", False))) for i in range(n)])
        var[lab] = s_star(GO / gbv, gbv, idx)
    gbn = np.array([float(gdisc(Ms0[i], Re0[i], R0[i]) + gdisc(Mg_noHe[i], Re0[i], R0[i])) for i in range(n)])
    var["no He"] = s_star(GO / gbn, gbn, idx)
    for lab, key in (("incl alt", "alt"), ("incl -1sig", "lo"), ("incl +1sig", "hi")):
        goi = GO.copy()
        for i in alpi:
            inew = {"alt": i_alt[i], "lo": max(5.0, i_used[i] - e_i[i]), "hi": min(85.0, i_used[i] + e_i[i])}[key]
            goi[i] = GO[i] * (math.sin(math.radians(i_used[i])) / math.sin(math.radians(inew))) ** 2
        var[lab] = s_star(goi / GB, GB, idx)
    for lab, Rsel, Vsel in (("ring V_ring@R_ext", "R0", "V_ring"), ("ring V_ext@R_mean", "Rmean", "V_noP")):
        go_ = GO.copy(); gb_ = GB.copy()
        for i in alpi:
            Rr = R0[i] if Rsel == "R0" else KN["R_mean_last2_kpc"][i]
            Vr = KN["V_ring"][i] if Vsel == "V_ring" else V_noP[i]
            go_[i] = float(gobs_of(Vr ** 2, Rr)); gb_[i] = float(gbar_of(Ms0[i], Mg0[i], Re0[i], Rr))
        var[lab] = s_star(go_ / gb_, gb_, idx)
    var["P2 kernel"] = s_star(D, GB, idx, nu=KER["P2"])
    # statistical: per-galaxy MC for a single galaxy; the galaxy bootstrap for a pooled set
    if len(idx) == 1:
        stat = dict(kind="MC (V, inclination, random baryon errors)", **MC[gid[idx[0]]])
    else:
        ib = np.random.default_rng(SEED * 1000 + len(idx)).integers(0, len(idx), size=(NB, len(idx)))
        sub = np.array(idx)
        ls, unb = implied(D[sub][ib], GB[sub][ib], NU, A0)
        ok = ~unb
        stat = dict(kind="galaxy bootstrap (CFG223)", frac_noroot=float(unb.mean()), q=[float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5)
    # A3
    jo = [corners["joint -outer"], corners["joint +outer"]]
    lost = any(c[1] for c in jo)
    moved = max((abs(c[0] - s0[0]) for c in jo if not c[1]), default=0.0)
    why = []
    if s0[1]: why.append("no root")
    if math.isfinite(lam) and abs(lam) > 10: why.append("|lambda| > 10")
    if lost: why.append("the joint outer band removes the root")
    if moved > 1.0: why.append("the joint outer band moves log s* by > 1 dex")
    IMPL[sname] = dict(s0=s0, a0_imp=(float("nan") if s0[1] else 10 ** s0[0] * A0), lever=lam, lever_flag=lflag, slope=sl, corners=corners, variants=var, stat=stat, informative=(len(why) == 0), why=why,
                       expected={T: PF["IMP"].get(sname, {}).get("s_exp", {}).get(T, float("nan")) for T in LAWN})
P("\n  s* (a0 scale vs the canonical footing) per galaxy and pooled set; 'no root' = no a0 in [1e-3, 1e3] x the footing zeroes the median delta (D <= 1 or D at the edge)")
P("  set            s*       a0 (1e-10 m/s2)   s*/alt      lever     slope    statistical (log10 s*: 16 / 50 / 84%, no-root fraction)            INFORMATIVE?")
for sname, r in IMPL.items():
    q = r["stat"]["q"]
    a0s = "no root" if r["s0"][1] else f"{r['a0_imp'] * 1e10:.3f}"
    salt = "-" if r["s0"][1] else f"{10 ** r['s0'][0] / ALT_OVER_CAN:.3g}"
    verdict = "INFORMATIVE" if r["informative"] else "UNINFORMATIVE: " + "; ".join(r["why"])
    P(f"  {sname:12s} {fmt(r['s0']):>8s}  {a0s:>14s}      {salt:>8s}   {('%+8.1f' % r['lever']) if math.isfinite(r['lever']) else '     n/a':>8s}   {r['slope']:.3f}   [{q[1]:+.2f}, {q[2]:+.2f}, {q[3]:+.2f}]  no-root {r['stat']['frac_noroot']:.2f} ({r['stat']['kind'][:20]})   {verdict}")
P("\n  systematic bars: s* at the band corners (gas inner +-0.03 / outer +-0.093; stars inner +-1 sigma / outer +-0.30; joint = same sign)")
for sname, r in IMPL.items():
    P(f"  {sname:12s} " + "  ".join(f"{k}: {fmt(v)}" for k, v in r["corners"].items()))
P("\n  variants (s*): pressure, geometry, inclination (ALPAKA), ring (ALPAKA), no He, P2 kernel")
for sname, r in IMPL.items():
    P(f"  {sname:12s} " + "  ".join(f"{k}: {fmt(v)}" for k, v in r["variants"].items()))
P("\n  expected s* if each law were true (from the pre-flight, noise-free, nominal baryons): " + "; ".join(f"{g}: " + "/".join(f"{IMPL[g]['expected'][T]:.2f}" for T in LAWN) for g in ("ALL7", "ALESS_122.1")) + "  (FLAT/PROXY/H(z)/M-DEC)")

# ------------------------------------------------------------------ controls
P("\nCONTROLS")
base_path = os.path.join(LANE, "cfg229_score_results.json")
if MODE == "":
    # C5 directions
    gbg, gbs_ = GB.copy(), GB.copy()
    dgas = delta_L(GO, np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i], R0[i], tg=0.1)) for i in range(n)]), FL["FLAT"]) - DL["FLAT"]
    dst = delta_L(GO, np.array([float(gbar_of(Ms0[i], Mg0[i], Re0[i], R0[i], ts=0.1)) for i in range(n)]), FL["FLAT"]) - DL["FLAT"]
    check("C5 raising the gas or the stellar mass by 0.1 dex lowers delta_FLAT at every galaxy", f"max shift gas {dgas.max():+.3f}, stars {dst.max():+.3f}", bool((dgas < 0).all() and (dst < 0).all()))
    sp_ = [SENS[f"pressure alpha = {a} (V^2 = V_noP^2 + alpha sigma^2)"]["dFLAT"] for a in (0.0, 1.68, 3.36)]
    check("C5c a larger pressure term raises g_obs and delta at every galaxy (alpha 0 < 1.68 < 3.36)", "monotone at " + str(sum(1 for i in range(n) if sp_[0][i] <= sp_[1][i] <= sp_[2][i])) + " of 7", all(sp_[0][i] <= sp_[1][i] + 1e-12 and sp_[1][i] <= sp_[2][i] + 1e-12 for i in range(n)))
    nohe = SENS["no helium factor (gas = 10^logMH2)"]["dFLAT"]
    dd = np.array(nohe) - DL["FLAT"]
    check("C5b the helium factor lowers every delta_FLAT relative to the no-He run by an amount between 0 and 0.134 dex", f"shifts {np.round(dd, 3).tolist()}", bool(((dd > 0) & (dd < LOGHE + 1e-9)).all()))
    gsh = Mg0 / (Mg0 + Ms0); gsh_no = Mg_noHe / (Mg_noHe + Ms0)
    check("H2 the helium factor adds exactly +0.1335 dex to every gas mass and raises the gas share by 3 to 8 percentage points", f"share rises {np.round(100 * (gsh - gsh_no), 1).tolist()} points", bool(np.allclose(np.log10(Mg0 / Mg_noHe), LOGHE, atol=1e-9) and ((gsh - gsh_no) >= 0.03 - 1e-9).all() and ((gsh - gsh_no) <= 0.08 + 1e-9).all()))
    # independent recomputation of the galaxy with the most informative implied a0: g_bar from the Hankel-transform integral (a different code path from the Bessel closed form), everything else by hand
    from scipy.integrate import quad
    from scipy.special import j1
    i6 = gid.index("ALESS_122.1")
    Mtot = Ms0[i6] + Mg0[i6]
    Rd = Re0[i6] / XN; S0 = Mtot / (2 * math.pi * Rd ** 2)
    f_k = lambda k: k * j1(k * R0[i6]) * (1 + (k * Rd) ** 2) ** (-1.5)
    edges = np.linspace(0, 400.0 / Rd, 4001)
    gh = 2 * math.pi * G_KPC * S0 * Rd ** 2 * sum(quad(f_k, a_, b_, limit=200)[0] for a_, b_ in zip(edges[:-1], edges[1:])) * G2SI
    nu_h = float(K.KERNELS["nu_mono"](np.array([gh / A0]))[0])
    d_chk = math.log10((V_noP[i6] ** 2 + alpha_pub[i6] * sig[i6] ** 2) * 1e6 / (R0[i6] * 3.0856775814913673e19) / (gh * nu_h))
    check("C11 ALESS 122.1's delta_FLAT recomputed by hand (g_bar from the Hankel-transform integral, g_obs from V^2/R in SI, the committed kernel through CFG4_common.KERNELS) equals the script's", f"{d_chk:+.6f} vs {DL['FLAT'][i6]:+.6f}", abs(d_chk - DL["FLAT"][i6]) < 1e-6)
elif MODE in ("1", "2", "3") and os.path.exists(base_path):
    B0 = json.load(open(base_path))
    dB = np.array(B0["DL"]["FLAT"]); dH = np.array(B0["DL"]["H(z)"]); gB = np.array(B0["GB"]); gO = np.array(B0["GO"])
    if MODE == "1":
        check("MUTATE 1: g_obs x 1.5 shifts every delta_L by +0.17609 to 1e-9 and leaves g_bar unchanged", f"shifts {np.round(DL['FLAT'] - dB, 6).tolist()}; max |g_bar change| {np.abs(GB / gB - 1).max():.1e}", bool(np.allclose(DL["FLAT"] - dB, math.log10(1.5), atol=1e-9) and np.allclose(DL["H(z)"] - dH, math.log10(1.5), atol=1e-9) and np.allclose(GB, gB, rtol=1e-12)))
    if MODE == "2":
        ref = delta_L(GO, np.array([float(gbar_of(ST["Mstar"].values[i], 10 ** ST["logMgas_He"].values[i], Re0[i], R0[i], tg=0.30, ts=0.30)) for i in range(n)]), FL["FLAT"])
        check("MUTATE 2: +0.30 dex on both baryon components equals the baseline run re-evaluated at the +0.30 dex corner (to 1e-9) and moves every delta by the lever", f"max difference {np.abs(DL['FLAT'] - ref).max():.1e}; shifts {np.round(DL['FLAT'] - dB, 3).tolist()}", bool(np.allclose(DL["FLAT"], ref, atol=1e-9) and (DL["FLAT"] < dB).all()))
    if MODE == "3":
        gexp = np.array([float(gdisc(ST['Mstar'].values[i], Re0[i], R0[i]) + gdisc(10 ** ST['logMH2'].values[i], Re0[i], R0[i])) for i in range(n)])
        check("MUTATE 3: the helium factor removed gives the no-He g_bar (to 1e-9) and raises every delta", f"max |g_bar - expected| {np.abs(GB / gexp - 1).max():.1e}; shifts {np.round(DL['FLAT'] - dB, 3).tolist()}", bool(np.allclose(GB, gexp, rtol=1e-9) and (DL['FLAT'] > dB).all()))
else:
    P("  (MUTATE run needs the main run's cfg229_score_results.json first)")

# ------------------------------------------------------------------ hand estimates H1-H19 (scored by code)
if MODE == "":
    P("\nHAND ESTIMATES (frozen before any computation; scored here by code; misses kept)")
    H = []

    def hscore(tag, text, ok):
        H.append((tag, bool(ok))); P(f"  {tag:4s} {'REPRODUCES' if ok else 'WRONG     '} {text}")
    inp_out = open(os.path.join(LANE, "cfg229_inputs.out")).read()
    hscore("H1", "the rule returns exactly the seven ids (read from the inputs script's control C0)", "[PASS] C0 the rule returns exactly the expected seven" in inp_out)
    hscore("H3", f"at least 4 of 7 have baseline D < 1 ({int((D < 1).sum())} of 7); all five ALPAKA D < 1 ({int((D[alpi] < 1).sum())} of 5)", (D < 1).sum() >= 4 and (D[alpi] < 1).all())
    hscore("H4", f"BX610 has D < 1 (D = {D[gid.index('SINS_BX610')]:.3f})", D[gid.index("SINS_BX610")] < 1)
    hscore("H5", f"ALESS 122.1 has D > 1 (D = {D[gid.index('ALESS_122.1')]:.3f})", D[gid.index("ALESS_122.1")] > 1)
    r7 = PF["RES"]["ALL7"]["rule"]
    hscore("H6", "the pre-flight says NOT POSSIBLE for flat vs H(z) for all seven at the outer and inner bands, and for no single galaxy", (not r7["H(z)"]["outer"]) and (not r7["H(z)"]["inner"]) and not any(PF["RES"][g]["rule"]["H(z)"]["outer"] for g in gid))
    big = max(PF["PG"], key=lambda g: abs(PF["PG"][g]["d_Hz"]))
    hscore("H7", f"the per-galaxy noise-free |d(flat, H(z))| is below 0.05 for each ALPAKA disc and is largest for ALESS 122.1 (largest: {big})", all(abs(PF["PG"][g]["d_Hz"]) < 0.05 for g in gid if g.startswith("ALPAKA")) and big == "ALESS_122.1")
    m_, lo_, hi_ = POOL["ALL7"]["FLAT"]
    hscore("H8", f"the all-seven median delta_FLAT is negative ({m_:+.3f}) and its 95% interval [{lo_:+.3f}, {hi_:+.3f}] excludes 0", m_ < 0 and hi_ < 0)
    md = float(np.median(DL["FLAT"] - DL["H(z)"]))
    hscore("H9", f"the median of (delta_FLAT - delta_H(z)) is between 0 and 0.06 ({md:+.3f})", 0 < md < 0.06)
    kp = "pressure alpha = %s (V^2 = V_noP^2 + alpha sigma^2)"
    p10 = [SENS[kp % "3.36"]["dFLAT"][i] - SENS[kp % "0.0"]["dFLAT"][i] for i in alpi]
    hscore("H10", f"alpha = 3.36 raises ALPAKA 15's delta by 0.05 to 0.12 ({p10[0]:+.3f}) and every other ALPAKA disc's by less than 0.08 ({np.round(p10[1:], 3).tolist()})", 0.05 <= p10[0] <= 0.12 and all(v < 0.08 for v in p10[1:]))
    i22 = gid.index("ALPAKA22")
    d11 = SENS["ALPAKA inclination: the other of (i_HST, i_ALMA)"]["dFLAT"][i22] - DL["FLAT"][i22]
    hscore("H11", f"replacing ID22's inclination by i_HST = 66 deg lowers its delta by more than 0.5 dex ({d11:+.3f})", d11 < -0.5)
    import re as _re
    pf_out = open(os.path.join(LANE, "cfg229_preflight.out")).read()
    mm = _re.search(r"C4 independent Hankel.*?max relative difference ([0-9.e+-]+)", pf_out)
    hscore("H12", f"the independent Hankel disc force agrees with the closed form to better than 1e-3 (pre-flight control C4: {mm.group(1) if mm else 'not found'})", bool(mm) and float(mm.group(1)) < 1e-3)
    hscore("H13", f"at least 3 of 7 are ROBUST FAIL on the floor ({nfail} of 7)", nfail >= 3)
    nr = sum(1 for g in gid if IMPL[g]["s0"][1])
    hscore("H14", f"at least 4 of 7 galaxies have NO ROOT ({nr} of 7)", nr >= 4)
    def lam_used(g):
        r_ = IMPL[g]["lever"]
        return (r_, "real data") if math.isfinite(r_) else (PF["IMP"][g]["lever"], "pre-flight nominal: no root in the data")
    hi10 = [g for i, g in enumerate(gid) if y[i] > 10]
    lamtxt = ", ".join("%s: %.0f (%s)" % (g, abs(lam_used(g)[0]), lam_used(g)[1]) for g in hi10)
    hscore("H15", f"|lambda| > 10 at every galaxy with y > 10 ({lamtxt})", all(abs(lam_used(g)[0]) > 10 for g in hi10))
    hscore("H16", "the pooled ALL7 s* has no root or is UNINFORMATIVE by A3", IMPL["ALL7"]["s0"][1] or (not IMPL["ALL7"]["informative"]))
    lam_small = [g for g in gid if abs(lam_used(g)[0]) < 10]
    hscore("H17", f"ALESS 122.1 is the only galaxy with |lambda| < 10 (those with |lambda| < 10: {lam_small}; real-data lambda of ALESS 122.1 = {IMPL['ALESS_122.1']['lever']:+.1f})", lam_small == ["ALESS_122.1"])
    a = IMPL["ALESS_122.1"]
    hscore("H18", "where ALESS 122.1 has a root its log10 s* lies within +-1 dex of 0" + (" (it has NO root: not testable, scored WRONG by default)" if a["s0"][1] else ""), (not a["s0"][1]) and abs(a["s0"][0]) <= 1.0)
    mcs = PF["IMP"]["ALESS_122.1"]["mc_stat"]; mci = PF["IMP"]["ALESS_122.1"]["mc_int"]
    hscore("H19", f"under truth FLAT the pre-flight mock median of log10 s* for ALESS 122.1 is within 0.3 dex of 0 ({mcs[0]:+.2f}) and its 16-84% range is wider than 1 dex (stat-only width {mcs[2] - mcs[1]:.2f}; with sigma_int {mci[2] - mci[1]:.2f}; scored on the stat-only line)", abs(mcs[0]) < 0.3 and (mcs[2] - mcs[1]) > 1.0)
    P(f"  => {sum(1 for t, o in H if o)} of {len(H)} hand estimates reproduce")

# ------------------------------------------------------------------ outputs
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
res = dict(gid=gid, z=z.tolist(), GO=GO.tolist(), GB=GB.tolist(), D=D.tolist(), y=y.tolist(), status=status, DL={L: DL[L].tolist() for L in LAWN}, DL_alt={L: DL_alt[L].tolist() for L in LAWN}, DL_p2={L: DL_p2[L].tolist() for L in LAWN},
           POOL=POOL, SENS=SENS, DIAG=DIAG, IMPL={k: {kk: (vv if not isinstance(vv, dict) else {a: (list(b) if isinstance(b, tuple) else b) for a, b in vv.items()}) for kk, vv in v.items()} for k, v in IMPL.items()},
           pf_gate_any_possible=bool(ANY_POSSIBLE), alt_over_can=ALT_OVER_CAN, mode=MODE, controls=CHK)
json.dump(res, open(os.path.join(LANE, f"cfg229_score_results{TAG}.json"), "w"), indent=1, default=float)
rows = []
for i in range(n):
    rows.append(dict(gid=gid[i], set=ST["set"][i], z=z[i], R_kpc=R0[i], V_kms=float(np.sqrt(V2_base[i])), g_obs=GO[i], g_bar=GB[i], y=y[i], D=D[i], status=status[i], dFLAT=DL["FLAT"][i], dPROXY=DL["PROXY"][i], dHz=DL["H(z)"][i], dMDEC=DL["M-DEC"][i],
                     dFLAT_alt=DL_alt["FLAT"][i], dHz_alt=DL_alt["H(z)"][i], dFLAT_p2=DL_p2["FLAT"][i], dHz_p2=DL_p2["H(z)"][i], log10_s=IMPL[gid[i]]["s0"][0], s_noroot=IMPL[gid[i]]["s0"][1], a0_implied=IMPL[gid[i]]["a0_imp"], lever=IMPL[gid[i]]["lever"],
                     informative=IMPL[gid[i]]["informative"], gas_class="M", source_table=ST["dunne_table"][i], mstar_route=ST["mstar_route"][i]))
pd.DataFrame(rows).to_csv(os.path.join(LANE, f"cfg229_points{TAG}.csv"), index=False, float_format="%.8g")
open(os.path.join(LANE, f"cfg229_score{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(CHK) else 1)
