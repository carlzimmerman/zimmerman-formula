#!/usr/bin/env python3
"""CFG228 -- SCORING: g_obs, g_bar, D, the Newtonian-floor status, delta_L for FLAT / PROXY / H(z) / M-DEC, the pooled statistic, and the IMPLIED a0 with its error budget, for the six ALPINE [CII] rotators (rotation from our own
forward model, Stage 3) and SPT0418-47 (the authors' published source-plane curve).  The blind pre-flight (0c4c5778d) was committed before Stage 3 existed and GATES every wording.
Compilation; two un-optimised tracers; calibration-limited; not blind to the published kinematics; not a detection; not a verdict.  LambdaCDM has no a0: the proxy is an effective-a0 PROXY.  kappa = 1/2 FITTED.
Frozen criteria: FROZEN_CRITERIA.md (71ec12282).  Run: python3 campaign_fresh_gravity/CFG228_alma_cubes/cfg228_score.py        MUTATE=1: g_obs x 1.5;  =2: +0.30 dex on both baryon components;  =3: gas / 1.36 (a helium factor removed)"""
import os, sys, math, json, time, itertools
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import i0e, i1e, k0e, k1e, j1
from scipy.integrate import quad

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MODE = os.environ.pop("MUTATE", "").strip()
TAG = {"": "", "1": "_MUTATE1", "2": "_MUTATE2", "3": "_MUTATE3"}[MODE]
sys.path.insert(0, CFG)
import CFG4_common as K
sys.path.insert(0, os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z"))
import zcommon as Z1
sys.path.insert(0, os.path.join(CFG, "CFG229_class_m_gold"))
from a0implied import implied, lever, kernel_slope

OUT, CHK = [], []
T0 = time.time()
G2SI = 1e6 / 3.0856775814913673e19
G_KPC = 4.30091e-6
XN = 1.678
OM = 0.315
SEED = 228
NB = 10000
B_STAR_OUT = 0.30
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
NU, A0 = KER["nu_mono"], A0F["canonical"]
ALT_OVER_CAN = A0F["alt"] / A0F["canonical"]
LAWN = ("FLAT", "PROXY", "H(z)", "M-DEC")
EV_SPT = 10.0


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


def gdisc(M, Re, Rr):
    return disc_v2(M, Re, Rr) / Rr * G2SI


def gsph(M, Re, Rr):
    x = Rr / (Re / XN)
    return G_KPC * M * (1 - (1 + x) * math.exp(-x)) / Rr ** 2 * G2SI


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {MODE or 'none'}" + {"": "", "1": " (g_obs x 1.5)", "2": " (+0.30 dex on both baryon components)", "3": " (gas / 1.36)"}[MODE])
ST = pd.read_csv(os.path.join(LANE, "cfg228_stage1_static.csv"))
MS = pd.read_csv(os.path.join(LANE, "cfg228_stage1_alpine_measurements.csv")).set_index("gid")
S3 = json.load(open(os.path.join(LANE, "cfg228_stage3_results.json")))
S3R = {r["gid"]: r for r in S3["REAL"]}
PF = json.load(open(os.path.join(LANE, "cfg228_preflight_results.json")))
PRO = json.load(open(os.path.join(LANE, "cfg228_stage3_profile_results.json"))) if os.path.exists(os.path.join(LANE, "cfg228_stage3_profile_results.json")) else None
n = len(ST)
gid = ST["gid"].tolist()
isS = np.array([g == "SPT0418-47" for g in gid])
z = ST["z"].values
FL = {L: np.array([LAWS[L](float(x)) for x in z]) for L in LAWS}
GM = 1.5 if MODE == "1" else 1.0
Ms0 = 10 ** ST["logMstar"].values * (10 ** 0.30 if MODE == "2" else 1.0)
Mg0 = 10 ** ST["logMgas"].values * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0)
Re0 = ST["Re_kpc"].values
R_OUT = {"1.0": ST["R_out_kpc"].values, "0.75": ST["R_out_kpc_15"].values, "1.5": ST["R_out_kpc_30"].values}          # primary R_out = 2 R_e (ALPINE) / 4 R_gas (SPT); the two variants = 1.5 and 3 R_e / 2 and 5 R_gas
R0 = R_OUT["1.0"]
e_st, e_gas_band = ST["e_logMstar_inner"].values, ST["gas_band_inner"].values
GIN, GOUT = ST["gas_band_inner"].values, ST["gas_band_outer"].values
i_used, e_i = ST["inc_kin"].values, ST["e_inc_kin"].values
a_cii = np.where(np.isfinite(ST["S_CII"].values), 0.4343 * ST["sS_CII"].values / ST["S_CII"].values, 0.05)
b_cont = 0.4343 * ST["sS_cont_mJy"].values / np.abs(ST["S_cont_mJy"].values)
b_cont = np.where(isS, 0.4343 * math.sqrt((9.67 / 75.99) ** 2 + (2.5 / 32.3) ** 2), b_cont)
both = ST["cont_det"].values.astype(bool)
e_gas = np.where(both, 0.5 * np.sqrt(a_cii ** 2 + b_cont ** 2), a_cii)


# ---------------------------------------------------------------- kinematics
def rizzo_V(R, Vt=245.1, Rt=0.14, beta=0.80, xi=2.0):
    return Vt * (1 + Rt / R) ** beta / (1 + (Rt / R) ** xi) ** (1 / xi)


VR, SIG, EV = {}, np.zeros(n), np.zeros(n)
for lab in R_OUT:
    VR[lab] = np.zeros(n)
for i, g in enumerate(gid):
    if isS[i]:
        for lab in R_OUT:
            VR[lab][i] = rizzo_V(R_OUT[lab][i])
        SIG[i] = 18.0                                                    # sigma_ext of Rizzo+20 Extended Data Table 2 (used only in the pressure VARIANT; the authors find the asymmetric drift < 1%)
        EV[i] = EV_SPT
    else:
        r = S3R[g]
        VR["1.0"][i], VR["0.75"][i], VR["1.5"][i] = r["V_Rout"], r["V_R15"], r["V_R30"]
        SIG[i] = r["sigma0"]; EV[i] = r["eV_Rout"] if np.isfinite(r["eV_Rout"]) else 0.3 * r["V_Rout"]
Rd_dyn = np.where(isS, 0.9, Re0 / XN)                                     # exponential scale of the dynamical tracer (ALPINE: [CII]; SPT0418-47: R_gas)
alpha_of = lambda R: np.where(isS, 0.0, 2.0 * R / Rd_dyn)                 # primary pressure term: the asymmetric drift of an exponential isothermal disc (ALPINE); the authors' value (negligible) for SPT0418-47


def gbar_of(Ms, Mg, Re_, R_, tg=0.0, ts=0.0, star_fac=1.0, sph=False):
    Ms_, Mg_ = np.asarray(Ms * 10 ** ts, float) * np.ones(len(gid)), np.asarray(Mg * 10 ** tg, float) * np.ones(len(gid))
    Re_ = np.asarray(Re_, float) * np.ones(len(gid)); R_ = np.asarray(R_, float) * np.ones(len(gid))
    f = gsph if sph else gdisc
    g_disc = np.array([f(Ms_[i], Re_[i] * star_fac, R_[i]) for i in range(len(gid))])
    g_pt = G_KPC * Ms_ / R_ ** 2 * G2SI
    g_star = np.where(isS, g_pt, g_disc)
    g_gas = np.array([f(Mg_[i], Re_[i], R_[i]) for i in range(len(gid))])
    return g_star + g_gas


def delta_L(go, gb, zz_F, nu=NU, a0=A0):
    return np.log10(go / (gb * nu(gb / (a0 * zz_F))))


def gobs_of(V, sig, alpha, R):
    return (V ** 2 + alpha * sig ** 2) / R * G2SI * GM


ALPHA = alpha_of(R0)
GO = gobs_of(VR["1.0"], SIG, ALPHA, R0)
GB = gbar_of(Ms0, Mg0, Re0, R0)
D = GO / GB
y = GB / A0
P("\nBASELINE (ALPINE: thin exponential disc with stars + gas at R_e,[CII]; SPT0418-47: stars a point mass, gas a thin disc with R_d = R_gas = 0.9 kpc; V_c^2 = V_rot^2 + alpha sigma^2 with alpha = 2 R_out/R_d (ALPINE) and 0 (SPT0418-47))")
P("  galaxy          z     R_out   V_rot (+-)      sigma  alpha   g_obs (m/s2)  g_bar (m/s2)   y=g_bar/a0    D=g_obs/g_bar   gas class   gas share")
for i in range(n):
    P(f"  {gid[i]:12s} {z[i]:.3f}  {R0[i]:5.2f}  {VR['1.0'][i]:6.1f} +- {EV[i]:5.1f}  {SIG[i]:5.0f}  {ALPHA[i]:5.2f}   {GO[i]:.3e}   {GB[i]:.3e}    {y[i]:8.2f}     {D[i]:8.3f}      {ST['gas_class'][i]:4s}      {Mg0[i] / (Mg0[i] + Ms0[i]):.2f}")
P("\nDELTA_L = log10[g_obs / (g_bar nu_mono(g_bar / (a0 F_L(z))))]  (canonical footing; the alt footing and P2 beside)")
DL = {L: delta_L(GO, GB, FL[L]) for L in LAWN}
DL_alt = {L: delta_L(GO, GB, FL[L], NU, A0F["alt"]) for L in LAWN}
DL_p2 = {L: delta_L(GO, GB, FL[L], KER["P2"], A0) for L in LAWN}
P("  galaxy          FLAT     PROXY    H(z)     M-DEC     | alt footing: FLAT  H(z)   | P2 kernel: FLAT  H(z)")
for i in range(n):
    P(f"  {gid[i]:12s} {DL['FLAT'][i]:+.3f}   {DL['PROXY'][i]:+.3f}   {DL['H(z)'][i]:+.3f}   {DL['M-DEC'][i]:+.3f}     | {DL_alt['FLAT'][i]:+.3f} {DL_alt['H(z)'][i]:+.3f}   | {DL_p2['FLAT'][i]:+.3f} {DL_p2['H(z)'][i]:+.3f}")


# ---------------------------------------------------------------- floor
def variant_D(i):
    out = []
    for lab in R_OUT:
        Rr = R_OUT[lab][i]
        V0 = VR[lab][i]
        incs = [1.0] + ([math.sin(math.radians(i_used[i])) / math.sin(math.radians(max(5.0, i_used[i] - e_i[i])))] if not isS[i] else [])
        alphas = (0.0, float(alpha_of(np.full(n, Rr))[i]), 3.36) if not isS[i] else (0.0, 3.36)
        geos = [dict(), dict(refac=1.5), dict(refac=1 / 1.5), dict(star_fac=0.5), dict(sph=True)]
        for fv, al, gk in itertools.product(incs, alphas, geos):
            go = float(gobs_of(V0 * fv, SIG[i] * fv, al, Rr))
            kw = dict(gk); rf = kw.pop("refac", 1.0)
            Rev = np.array(Re0); Rev[i] *= rf
            gb = gbar_of(Ms0, Mg0, Rev, np.where(np.arange(n) == i, Rr, R0), tg=-GOUT, ts=-B_STAR_OUT, **kw)[i]
            out.append(go / gb)
    return max(out)


status, Dbest = [], []
for i in range(n):
    db = variant_D(i); Dbest.append(db)
    status.append("PASS" if D[i] >= 1 else ("BAND-DEPENDENT" if db >= 1 else "ROBUST FAIL"))
P("\nNEWTONIAN FLOOR (D < 1 is a baryon-model inconsistency for ANY law): PASS if D >= 1; BAND-DEPENDENT if D < 1 but D >= 1 at the most favourable corner of the declared bands and variants (gas -outer, stars -0.30, R_out 1.5 / 2 / 3 R_e, pressure, geometry, inclination - 1 sigma); ROBUST FAIL otherwise")
for i in range(n):
    P(f"  {gid[i]:12s} D = {D[i]:6.3f}; most favourable corner D_best = {Dbest[i]:6.3f} -> {status[i]}")
P(f"  => PASS {status.count('PASS')}, BAND-DEPENDENT {status.count('BAND-DEPENDENT')}, ROBUST FAIL {status.count('ROBUST FAIL')}")
PASSI = [i for i in range(n) if status[i] == "PASS"]
IDX = {"ALPINE6": [i for i in range(n) if not isS[i]], "ALL7": list(range(n))}


def med_ci(d, idx):
    d = np.asarray(d)[idx]
    m = len(idx)
    ib = np.random.default_rng(SEED * 1000 + m).integers(0, m, size=(NB, m))
    bs = np.median(d[ib], axis=1)
    return float(np.median(d)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


P("\nPOOLED (median delta with the 10,000-resample galaxy bootstrap 95% interval; DESCRIPTIVE; the pre-flight gate decides what may be said)")
POOL = {}
for sname, idx in (("ALPINE6", IDX["ALPINE6"]), ("ALL7", IDX["ALL7"]), ("PASS subset", PASSI)):
    if len(idx) < 2:
        P(f"  {sname}: N = {len(idx)} (< 2): no pooled statistic"); continue
    POOL[sname] = {L: med_ci(DL[L], idx) for L in LAWN}
    P(f"  {sname:12s} (N = {len(idx)}): " + "   ".join(f"{L} {POOL[sname][L][0]:+.3f} [{POOL[sname][L][1]:+.3f}, {POOL[sname][L][2]:+.3f}]" for L in LAWN) + f"   | median(FLAT - H(z)) = {np.median(DL['FLAT'][idx] - DL['H(z)'][idx]):+.3f}; median D = {np.median(D[idx]):.3f}")

# ---------------------------------------------------------------- bands and sensitivities
P("\nBANDS (per-galaxy delta_FLAT at the corners: gas inner +-0.213 / outer +-0.671; stars inner +-0.20 / outer +-0.30; joint = same sign)")
BANDS, BANDS_GB = {}, {}
for kind, (tg, ts) in (("gas -outer", (-GOUT, np.zeros(n))), ("gas -inner", (-GIN, np.zeros(n))), ("gas +inner", (GIN, np.zeros(n))), ("gas +outer", (GOUT, np.zeros(n))),
                       ("stars -outer", (np.zeros(n), np.full(n, -B_STAR_OUT))), ("stars -inner", (np.zeros(n), -e_st)), ("stars +inner", (np.zeros(n), e_st)), ("stars +outer", (np.zeros(n), np.full(n, B_STAR_OUT))),
                       ("joint -outer", (-GOUT, np.full(n, -B_STAR_OUT))), ("joint -inner", (-GIN, -e_st)), ("joint +inner", (GIN, e_st)), ("joint +outer", (GOUT, np.full(n, B_STAR_OUT)))):
    Msi, Mgi = Ms0 * 10 ** ts, Mg0 * 10 ** tg
    gbt = gbar_of(Msi, Mgi, Re0, R0)
    BANDS[kind] = delta_L(GO, gbt, FL["FLAT"]); BANDS_GB[kind] = gbt.tolist()
P("  band          " + "  ".join(f"{g[:10]:>10s}" for g in gid) + "   median ALPINE6")
for kind, v in BANDS.items():
    P(f"  {kind:13s} " + "  ".join(f"{x:+10.3f}" for x in v) + f"   {np.median(v[IDX['ALPINE6']]):+.3f}")

P("\nSENSITIVITIES (delta_FLAT / delta_H(z) per galaxy; beside the baseline, never substituted)")
SENS = {}


def sens_line(label, go_arr, gb_arr):
    dF, dH = delta_L(go_arr, gb_arr, FL["FLAT"]), delta_L(go_arr, gb_arr, FL["H(z)"])
    SENS[label] = dict(dFLAT=dF.tolist(), dHz=dH.tolist())
    P(f"  {label:40s} " + " ".join(f"{a:+.2f}/{b:+.2f}" for a, b in zip(dF, dH)) + f"   median ALPINE6 {np.median(dF[IDX['ALPINE6']]):+.3f}/{np.median(dH[IDX['ALPINE6']]):+.3f}")


P("  variant                                  " + " ".join(f"{g[:8]:>10s}" for g in gid))
for al_lab, al in (("pressure alpha = 0", np.zeros(n)), ("pressure alpha = 3.36", np.full(n, 3.36))):
    sens_line(al_lab, gobs_of(VR["1.0"], SIG, al, R0), GB)
for lab, kw in (("R_e x 1.5", dict(refac=1.5)), ("R_e / 1.5", dict(refac=1 / 1.5)), ("stars at 0.5 R_e,gas", dict(star_fac=0.5)), ("spherical enclosed mass", dict(sph=True))):
    Rev = Re0 * kw.get("refac", 1.0)
    sens_line(lab, GO, gbar_of(Ms0, Mg0, Rev, R0, star_fac=kw.get("star_fac", 1.0), sph=kw.get("sph", False)))
for lab, key in (("R_out = 1.5 R_e (SPT: 2 R_gas)", "0.75"), ("R_out = 3 R_e (SPT: 5 R_gas)", "1.5")):
    Rv = R_OUT[key]
    sens_line(lab, gobs_of(VR[key], SIG, alpha_of(Rv), Rv), gbar_of(Ms0, Mg0, Re0, Rv))
for lab, col in (("dust at T_d = 25 K (gas log-mean where detected)", "logMd25"), ("dust at T_d = 45 K (gas log-mean where detected)", "logMd45")):
    lg = np.where(both, 0.5 * (ST["logM_CII"].values + ST[col].values), ST["logMgas"].values)
    sens_line(lab, GO, gbar_of(Ms0, 10 ** lg * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0), Re0, R0))
ratio_cube = np.array([MS.loc[g, "S_CII_cube"] / MS.loc[g, "S_CII"] if g in MS.index else 1.0 for g in gid])
lg_cube = np.where(both, 0.5 * (ST["logM_CII"].values + np.log10(ratio_cube) + ST["logMd35"].values), ST["logM_CII"].values + np.log10(ratio_cube))
sens_line("own-cube [CII] flux (mass x cube/moment-0)", GO, gbar_of(Ms0, 10 ** lg_cube * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0), Re0, R0))
lg_cii = ST["logM_CII"].values; lg_dust = np.where(both, ST["logMd35"].values, np.nan)
sens_line("gas = [CII] only", GO, gbar_of(Ms0, 10 ** lg_cii * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0), Re0, R0))
for lab, i_alt_sign in (("inclination - 1 sigma (ALPINE)", -1), ("inclination + 1 sigma (ALPINE)", +1)):
    go_ = GO.copy()
    for i in range(n):
        if not isS[i]:
            inew = min(85.0, max(5.0, i_used[i] + i_alt_sign * e_i[i]))
            go_[i] = GO[i] * (math.sin(math.radians(i_used[i])) / math.sin(math.radians(inew))) ** 2
    sens_line(lab, go_, GB)
if PRO is not None:
    for kk in ("0.2", "1.0", "3.0"):
        go_ = GO.copy()
        for i in range(n):
            if not isS[i]:
                Vp = PRO["PROFILE"][gid[i]][kk]["V_Rout"]
                go_[i] = float(gobs_of(Vp, SIG[i], ALPHA[i], R0[i]))
        sens_line(f"POST HOC: rotation-curve shape R_t fixed at {kk} kpc (refit)", go_, GB)

# ---------------------------------------------------------------- gate
P("\nPRE-FLIGHT GATE (cfg228_preflight.py, committed before Stage 3; read from its results JSON)")
for sname in ("ALPINE6", "ALL7"):
    r = PF["RES"][sname]["rule"]
    P(f"  {sname}: flat vs H(z) outer / gas-only / inner = {r['H(z)']['outer']} / {r['H(z)']['gas_only']} / {r['H(z)']['inner']}; flat vs PROXY = {r['PROXY']['outer']} / {r['PROXY']['gas_only']} / {r['PROXY']['inner']}  (True = POSSIBLE)")
ANY_POSSIBLE = any(PF["RES"][s]["rule"][T]["outer"] for s in ("ALPINE6", "ALL7") + tuple(gid) for T in ("H(z)", "PROXY"))
P(f"  => {'POSSIBLE in at least one set at the JOINT OUTER band: law statements allowed ONLY for that set' if ANY_POSSIBLE else 'NOT POSSIBLE in any set at the joint outer band (S/L gas +-0.671, stars +-0.30): NO sentence of this lane may say any law is separated, preferred or disfavoured; the delta table is descriptive'}")

# ---------------------------------------------------------------- implied a0
P("\nIMPLIED a0 (descriptive, not a verdict).  s* = the root of median_i log10[D_i / nu_mono(g_bar,i/(a0 s))] = 0 (CFG223's estimator); a0_implied = s* x 9.3603e-11 m/s^2 (footing-independent); alt footing ratio s*/%.4f" % ALT_OVER_CAN)
P("  z ~ 0 reference (QUOTED from the record, no SPARC analysis here): canonical 9.3603e-11 and alt 1.1312e-10 m/s^2 (CFG4_common.A0); SPARC fits both at equal quality at fixed Upsilon (CFG0 F9); a0 and Upsilon degenerate (CFG4 H2b: best free a0 1.37e-10 for nu_mono, 1.78e-10 for P2 at Upsilon 0.50)")
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
sets_imp.update({"ALPINE6": IDX["ALPINE6"], "ALL7": IDX["ALL7"]})
if len(PASSI) >= 3:
    sets_imp["PASS subset"] = PASSI
rngi = np.random.default_rng(SEED + 1)
BMC = 10000
MC = {}
for i in range(n):
    Vd = VR["1.0"][i] + rngi.normal(0, EV[i], BMC)
    fac = np.ones(BMC)
    ii = rngi.normal(i_used[i], e_i[i], BMC)
    for _ in range(60):
        bad = (ii < 5) | (ii > 85)
        if not bad.any(): break
        ii[bad] = rngi.normal(i_used[i], e_i[i], int(bad.sum()))
    fac = (math.sin(math.radians(i_used[i])) / np.sin(np.radians(ii))) ** 2
    god = gobs_of(np.abs(Vd), SIG[i], ALPHA[i], R0[i]) * fac
    Msd, Mgd = Ms0[i] * 10 ** rngi.normal(0, e_st[i], BMC), Mg0[i] * 10 ** rngi.normal(0, e_gas[i], BMC)
    if isS[i]:
        gbd = G_KPC * Msd / R0[i] ** 2 * G2SI + gdisc(Mgd, Re0[i], R0[i])
    else:
        gbd = gdisc(Msd, Re0[i], R0[i]) + gdisc(Mgd, Re0[i], R0[i])
    ls, unb = implied((god / gbd)[:, None], gbd[:, None], NU, A0)
    ok = ~unb
    MC[gid[i]] = dict(frac_noroot=float(unb.mean()), q=[float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5)
VARSETS = {}
for sname, idx in sets_imp.items():
    s0 = s_star(D, GB, idx)
    lam, lflag = lever(D[idx], GB[idx], NU, A0)
    lam = float(lam[0]); lflag = bool(lflag[0])
    if lflag or s0[1]:
        lam = float("nan")
    sl = float(np.median(kernel_slope(NU, GB[idx] / A0)))

    def s_at(tg, ts):
        gbt = gbar_of(Ms0 * 10 ** ts, Mg0 * 10 ** tg, Re0, R0)
        return s_star(GO / gbt, gbt, idx)
    corners = {}
    for kind, (tg, ts) in (("gas -inner", (-GIN, np.zeros(n))), ("gas +inner", (GIN, np.zeros(n))), ("gas -outer", (-GOUT, np.zeros(n))), ("gas +outer", (GOUT, np.zeros(n))),
                           ("stars -inner", (np.zeros(n), -e_st)), ("stars +inner", (np.zeros(n), e_st)), ("stars -outer", (np.zeros(n), np.full(n, -B_STAR_OUT))), ("stars +outer", (np.zeros(n), np.full(n, B_STAR_OUT))),
                           ("joint -inner", (-GIN, -e_st)), ("joint +inner", (GIN, e_st)), ("joint -outer", (-GOUT, np.full(n, -B_STAR_OUT))), ("joint +outer", (GOUT, np.full(n, B_STAR_OUT)))):
        corners[kind] = s_at(tg, ts)
    var = {}
    for al_lab, al in (("alpha 0", np.zeros(n)), ("alpha 3.36", np.full(n, 3.36))):
        var[al_lab] = s_star(gobs_of(VR["1.0"], SIG, al, R0) / GB, GB, idx)
    for lab, kw in (("R_e x1.5", dict(refac=1.5)), ("R_e /1.5", dict(refac=1 / 1.5)), ("stars 0.5R_e", dict(star_fac=0.5)), ("spherical", dict(sph=True))):
        gbv = gbar_of(Ms0, Mg0, Re0 * kw.get("refac", 1.0), R0, star_fac=kw.get("star_fac", 1.0), sph=kw.get("sph", False))
        var[lab] = s_star(GO / gbv, gbv, idx)
    for lab, key in (("R_out 1.5R_e", "0.75"), ("R_out 3R_e", "1.5")):
        Rv = R_OUT[key]; gov = gobs_of(VR[key], SIG, alpha_of(Rv), Rv); gbv = gbar_of(Ms0, Mg0, Re0, Rv)
        var[lab] = s_star(gov / gbv, gbv, idx)
    for lab, col in (("T_d 25 K", "logMd25"), ("T_d 45 K", "logMd45")):
        lg = np.where(both, 0.5 * (ST["logM_CII"].values + ST[col].values), ST["logMgas"].values)
        gbv = gbar_of(Ms0, 10 ** lg * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0), Re0, R0)
        var[lab] = s_star(GO / gbv, gbv, idx)
    gbv = gbar_of(Ms0, 10 ** lg_cube * (10 ** 0.30 if MODE == "2" else 1.0) / (1.36 if MODE == "3" else 1.0), Re0, R0); var["own-cube flux"] = s_star(GO / gbv, gbv, idx)
    for lab, sgn in (("incl -1sig", -1), ("incl +1sig", +1)):
        go_ = GO.copy()
        for i in range(n):
            if not isS[i]:
                inew = min(85.0, max(5.0, i_used[i] + sgn * e_i[i])); go_[i] = GO[i] * (math.sin(math.radians(i_used[i])) / math.sin(math.radians(inew))) ** 2
        var[lab] = s_star(go_ / GB, GB, idx)
    if PRO is not None:
        for kk in ("0.2", "1.0", "3.0"):
            go_ = GO.copy()
            for i in range(n):
                if not isS[i]:
                    go_[i] = float(gobs_of(PRO["PROFILE"][gid[i]][kk]["V_Rout"], SIG[i], ALPHA[i], R0[i]))
            var[f"R_t={kk} (post hoc)"] = s_star(go_ / GB, GB, idx)
    var["P2 kernel"] = s_star(D, GB, idx, nu=KER["P2"])
    if len(idx) == 1:
        stat = dict(kind="MC (V fit error, inclination, random baryon errors)", **MC[gid[idx[0]]])
    else:
        ib = np.random.default_rng(SEED * 1000 + len(idx)).integers(0, len(idx), size=(NB, len(idx)))
        sub = np.array(idx)
        ls, unb = implied(D[sub][ib], GB[sub][ib], NU, A0)
        ok = ~unb
        stat = dict(kind="galaxy bootstrap (CFG223)", frac_noroot=float(unb.mean()), q=[float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5)
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
P("\n  s* per galaxy and pooled set; 'no root' = no a0 in [1e-3, 1e3] x the footing zeroes the median delta (D <= 1)")
P("  set            s*       a0 (1e-10 m/s2)   s*/alt      lever     slope    statistical (log10 s*: 16 / 50 / 84%, no-root fraction)            INFORMATIVE?")
for sname, r in IMPL.items():
    q = r["stat"]["q"]
    a0s = "no root" if r["s0"][1] else f"{r['a0_imp'] * 1e10:.3f}"
    salt = "-" if r["s0"][1] else f"{10 ** r['s0'][0] / ALT_OVER_CAN:.3g}"
    lam_s = ("%+8.1f" % r["lever"]) if math.isfinite(r["lever"]) else "     n/a"
    verdict = "INFORMATIVE" if r["informative"] else "UNINFORMATIVE: " + "; ".join(r["why"])
    P(f"  {sname:12s} {fmt(r['s0']):>8s}  {a0s:>14s}      {salt:>8s}   {lam_s:>8s}   {r['slope']:.3f}   [{q[1]:+.2f}, {q[2]:+.2f}, {q[3]:+.2f}]  no-root {r['stat']['frac_noroot']:.2f} ({r['stat']['kind'][:14]})   {verdict}")
P("\n  systematic bars: s* at the band corners (gas inner +-0.213 / outer +-0.671; stars inner +-0.20 / outer +-0.30; joint = same sign)")
for sname, r in IMPL.items():
    P(f"  {sname:12s} " + "  ".join(f"{k}: {fmt(v)}" for k, v in r["corners"].items()))
P("\n  variants (s*): pressure, geometry, R_out, dust temperature, own-cube flux, inclination, rotation-curve shape (post hoc), P2 kernel")
for sname, r in IMPL.items():
    P(f"  {sname:12s} " + "  ".join(f"{k}: {fmt(v)}" for k, v in r["variants"].items()))
P("\n  expected s* if each law were true (pre-flight, noise-free, nominal baryons; FLAT/PROXY/H(z)/M-DEC): " + "; ".join(f"{g}: " + "/".join(f"{IMPL[g]['expected'][T]:.2f}" for T in LAWN) for g in ("ALPINE6", "ALL7")))

# ---------------------------------------------------------------- literature check (Jones+21), reported
P("\nLITERATURE CHECK (reported, not a control): our V_rot at Jones+21's outer-ring radius against their published outer-ring V_rot")
RJ = {}
for i, g in enumerate(gid):
    if isS[i]:
        continue
    r = S3R[g]
    dV = r["V_RJ"] - r["jones_V"]; sig_c = math.sqrt((r["eV_RJ"] if np.isfinite(r["eV_RJ"]) else 0) ** 2 + r["jones_eV"] ** 2)
    RJ[g] = dV / sig_c
    P(f"  {g:13s} R_J {r['jones_R']:.2f} kpc: ours {r['V_RJ']:6.1f} +- {r['eV_RJ']:5.1f} vs Jones {r['jones_V']:6.1f} +- {r['jones_eV']:5.1f}  ({RJ[g]:+.2f} sigma)")

# ---------------------------------------------------------------- controls
P("\nCONTROLS")
base_path = os.path.join(LANE, "cfg228_score_results.json")
if MODE == "":
    dgas = delta_L(GO, gbar_of(Ms0, Mg0 * 10 ** 0.1, Re0, R0), FL["FLAT"]) - DL["FLAT"]
    dst = delta_L(GO, gbar_of(Ms0 * 10 ** 0.1, Mg0, Re0, R0), FL["FLAT"]) - DL["FLAT"]
    check("C5 raising the gas or the stellar mass by 0.1 dex lowers delta_FLAT at every galaxy", f"max shift gas {dgas.max():+.3f}, stars {dst.max():+.3f}", bool((dgas < 0).all() and (dst < 0).all()))
    sp0, sp1 = SENS["pressure alpha = 0"]["dFLAT"], SENS["pressure alpha = 3.36"]["dFLAT"]
    check("C5c a larger pressure term raises g_obs and delta at every galaxy with sigma > 0 (alpha 0 <= 3.36)", f"{sum(1 for i in range(n) if sp0[i] <= sp1[i] + 1e-12)} of {n}", all(sp0[i] <= sp1[i] + 1e-12 for i in range(n)))
    # C11: recompute the galaxy with the largest g_bar/a0 gradient by hand: VC5110377875 with g_bar from the Hankel integral
    i6 = gid.index("VC5110377875")
    Mtot = Ms0[i6] + Mg0[i6]
    Rd = Re0[i6] / XN; S0 = Mtot / (2 * math.pi * Rd ** 2)
    f_k = lambda k: k * j1(k * R0[i6]) * (1 + (k * Rd) ** 2) ** (-1.5)
    edges = np.linspace(0, 400.0 / Rd, 4001)
    gh = 2 * math.pi * G_KPC * S0 * Rd ** 2 * sum(quad(f_k, a_, b_, limit=200)[0] for a_, b_ in zip(edges[:-1], edges[1:])) * G2SI
    nu_h = float(K.KERNELS["nu_mono"](np.array([gh / A0]))[0])
    d_chk = math.log10(((VR["1.0"][i6] ** 2 + ALPHA[i6] * SIG[i6] ** 2) * 1e6 / (R0[i6] * 3.0856775814913673e19)) / (gh * nu_h))
    check("C11 VC5110377875's delta_FLAT recomputed by hand (g_bar from the Hankel-transform integral, g_obs from V^2/R in SI, the committed kernel) equals the script's", f"{d_chk:+.6f} vs {DL['FLAT'][i6]:+.6f}", abs(d_chk - DL["FLAT"][i6]) < 1e-6)
elif MODE in ("1", "2", "3") and os.path.exists(base_path):
    B0 = json.load(open(base_path))
    dB, dH, gB = np.array(B0["DL"]["FLAT"]), np.array(B0["DL"]["H(z)"]), np.array(B0["GB"])
    if MODE == "1":
        check("MUTATE 1: g_obs x 1.5 shifts every delta_L by +0.17609 to 1e-9 and leaves g_bar unchanged", f"shifts {np.round(DL['FLAT'] - dB, 6).tolist()}", bool(np.allclose(DL["FLAT"] - dB, math.log10(1.5), atol=1e-9) and np.allclose(DL["H(z)"] - dH, math.log10(1.5), atol=1e-9) and np.allclose(GB, gB, rtol=1e-12)))
    if MODE == "2":
        ref = delta_L(GO, gbar_of(10 ** ST["logMstar"].values, 10 ** ST["logMgas"].values, Re0, R0, tg=0.30, ts=0.30), FL["FLAT"])
        check("MUTATE 2: +0.30 dex on both baryon components equals the baseline re-evaluated at the +0.30 dex corner (to 1e-9) and lowers every delta", f"max difference {np.abs(DL['FLAT'] - ref).max():.1e}; shifts {np.round(DL['FLAT'] - dB, 3).tolist()}", bool(np.allclose(DL["FLAT"], ref, atol=1e-9) and (DL["FLAT"] < dB).all()))
    if MODE == "3":
        gexp = gbar_of(10 ** ST["logMstar"].values, 10 ** ST["logMgas"].values / 1.36, Re0, R0)
        check("MUTATE 3: the gas divided by 1.36 gives the expected g_bar (to 1e-9) and raises every delta", f"max |g_bar - expected| {np.abs(GB / gexp - 1).max():.1e}; shifts {np.round(DL['FLAT'] - dB, 3).tolist()}", bool(np.allclose(GB, gexp, rtol=1e-9) and (DL["FLAT"] > dB).all()))
else:
    P("  (MUTATE run needs the main run's cfg228_score_results.json first)")

# ---------------------------------------------------------------- hand estimates (scored by code)
if MODE == "":
    P("\nHAND ESTIMATES (frozen before any computation; scored by code; misses kept)")
    H = []

    def hscore(tag, text, ok):
        H.append((tag, bool(ok))); P(f"  {tag:4s} {'REPRODUCES' if ok else 'WRONG     '} {text}")
    alp = IDX["ALPINE6"]
    hscore("H1", f"[CII] detected at aperture S/N >= 5 for all six ALPINE rotators (S/N {[round(float(MS.loc[g, 'S_CII'] / MS.loc[g, 'sS_CII']), 1) for g in gid if g in MS.index]})", all(MS.loc[g, "S_CII"] / MS.loc[g, "sS_CII"] >= 5 for g in gid if g in MS.index))
    hscore("H2", f"the dust continuum is detected (S/N >= 3) for at least 3 of the 6 ({int(MS['cont_det'].sum())} of 6)", MS["cont_det"].sum() >= 3)
    hscore("H3", f"every ALPINE L_[CII] lies between 10^8.3 and 10^9.3 Lsun (log range {np.log10(MS['L_CII']).min():.2f} to {np.log10(MS['L_CII']).max():.2f})", bool(((np.log10(MS["L_CII"]) > 8.3) & (np.log10(MS["L_CII"]) < 9.3)).all()))
    hscore("H4", f"every [CII]-based gas mass lies between 10^10.0 and 10^11.0 Msun (range {MS['logM_CII'].min():.2f} to {MS['logM_CII'].max():.2f})", bool(((MS["logM_CII"] > 10.0) & (MS["logM_CII"] < 11.0)).all()))
    dd = MS["d_AB"].dropna().values
    st1 = json.load(open(os.path.join(LANE, "cfg228_stage1_results.json")))
    hscore("H5", f"|mu_d| > 0.15 dex for the galaxies with both tracers (ALPINE + SPT0418-47: mean {st1['class_all']['mu']:+.2f}, N {st1['class_all']['N']})", abs(st1["class_all"]["mu"]) > 0.15)
    hscore("H6", f"class M2 is NOT achieved (N_both {st1['class_all']['N']} < 5 or K_AB {st1['class_all']['K']:.2f} > 0.10)", not st1["class_all"]["M2"])
    hscore("H7", f"R_half exceeds the beam HWHM for at least 4 of the 6 ({int(MS['resolved'].sum())} of 6)", MS["resolved"].sum() >= 4)
    hscore("H8", f"the image-plane [CII] magnification of SPT0418-47 lies between 20 and 45 ({st1['spt']['mu_CII_implied']:.1f})", 20 < st1["spt"]["mu_CII_implied"] < 45)
    yy_ = [PF["PG"][g]["y"] for g in gid if g != "SPT0418-47"]
    hscore("H9", f"y at R_out lies between 1 and 10 for at least 4 of the 6 ALPINE ({sum(1 for v in yy_ if 1 < v < 10)} of 6) and above 10 for SPT0418-47 at 2 R_gas ({PF['PG']['SPT0418-47']['y15']:.1f})", sum(1 for v in yy_ if 1 < v < 10) >= 4 and PF["PG"]["SPT0418-47"]["y15"] > 10)
    hscore("H10", "flat vs H(z) is NOT POSSIBLE for the ALPINE six pooled at the outer band and at the inner band", (not PF["RES"]["ALPINE6"]["rule"]["H(z)"]["outer"]) and (not PF["RES"]["ALPINE6"]["rule"]["H(z)"]["inner"]))
    nunin = sum(1 for g in gid if g != "SPT0418-47" and not PF["IMP"][g]["informative"])
    hscore("H11", f"at least 5 of the 6 ALPINE rotators are UNINFORMATIVE for the implied a0 at the outer band ({nunin} of 6) and SPT0418-47 is INFORMATIVE ({PF['IMP']['SPT0418-47']['informative']})", nunin >= 5 and PF["IMP"]["SPT0418-47"]["informative"])
    s3 = json.load(open(os.path.join(LANE, "cfg228_stage3_results.json")))["REC"]
    nrec = sum(1 for g in s3 if s3[g]["frac15"] >= 0.90)
    hscore("H12", f"the planted-rotation recovery returns V(R_out) within 15% in >= 90% of the mocks for every galaxy ({nrec} of 6 galaxies reach 90%)", nrec == 6)
    nj = sum(1 for g in RJ if abs(RJ[g]) <= 1.0)
    hscore("H13", f"our V_rot at Jones+21's outer-ring radius agrees with theirs within the combined 1 sigma for at least 4 of the 6 ({nj} of 6)", nj >= 4)
    nd = int((D[IDX['ALPINE6']] < 1).sum())
    hscore("H14", f"at least 3 of the 6 ALPINE rotators have D < 1 ({nd} of 6)", nd >= 3)
    hscore("H15", f"SPT0418-47 has D > 1 at R_out = 4 R_gas (D = {D[gid.index('SPT0418-47')]:.3f})", D[gid.index("SPT0418-47")] > 1)
    hscore("H16", "the pooled ALPINE implied a0 has no root or is UNINFORMATIVE", IMPL["ALPINE6"]["s0"][1] or (not IMPL["ALPINE6"]["informative"]))
    P(f"  => {sum(1 for t, o in H if o)} of {len(H)} hand estimates reproduce")

P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
res = dict(gid=gid, z=z.tolist(), GO=GO.tolist(), GB=GB.tolist(), D=D.tolist(), y=y.tolist(), status=status, DL={L: DL[L].tolist() for L in LAWN}, DL_alt={L: DL_alt[L].tolist() for L in LAWN}, DL_p2={L: DL_p2[L].tolist() for L in LAWN},
           POOL=POOL, SENS=SENS, BANDS_GB=BANDS_GB, V=VR["1.0"].tolist(), EV=EV.tolist(), SIG=SIG.tolist(), ALPHA=ALPHA.tolist(), R_out=R0.tolist(), gas_class=ST["gas_class"].tolist(),
           IMPL={k: {kk: (vv if not isinstance(vv, dict) else {a: (list(b) if isinstance(b, tuple) else b) for a, b in vv.items()}) for kk, vv in v.items()} for k, v in IMPL.items()},
           pf_gate_any_possible=bool(ANY_POSSIBLE), alt_over_can=ALT_OVER_CAN, mode=MODE, controls=CHK)
json.dump(res, open(os.path.join(LANE, f"cfg228_score_results{TAG}.json"), "w"), indent=1, default=float)
rows = []
for i in range(n):
    rows.append(dict(gid=gid[i], z=z[i], R_out_kpc=R0[i], V_kms=VR["1.0"][i], eV_kms=EV[i], sigma=SIG[i], g_obs=GO[i], g_bar=GB[i], y=y[i], D=D[i], status=status[i], dFLAT=DL["FLAT"][i], dPROXY=DL["PROXY"][i], dHz=DL["H(z)"][i], dMDEC=DL["M-DEC"][i],
                     log10_s=IMPL[gid[i]]["s0"][0], s_noroot=IMPL[gid[i]]["s0"][1], a0_implied=IMPL[gid[i]]["a0_imp"], lever=IMPL[gid[i]]["lever"], informative=IMPL[gid[i]]["informative"], gas_class=ST["gas_class"][i]))
pd.DataFrame(rows).to_csv(os.path.join(LANE, f"cfg228_points{TAG}.csv"), index=False, float_format="%.8g")
open(os.path.join(LANE, f"cfg228_score{TAG}.out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(CHK) else 1)
