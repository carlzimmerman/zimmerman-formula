#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG285 POST-HOC addendum (written AFTER CFG284 and CFG285 were committed and verified; NOT a frozen item; no frozen result is changed): the exponential-disc-matched geometry.

Why: reading the two ADF22 PDFs directly (arXiv:2502.01868 Table 4, arXiv:2502.01868 Table 3; data_assembly/adf22_5_literature_2026-10-02/adf22_pdf_direct_reads_A7.csv) shows that the frozen headline radius, R_e = 2.24 kpc, is the semi-major-axis
R_e of the FREE-n F444W fit (Sersic n = 3.21), not the scale of an exponential disc.  The same table lists the n = 1 fit: R_e = 1.55 kpc (b/a 0.57), and the 870 um masked fit (n = 1.01) gives 1.53 kpc: stars and dust agree on ~1.5 kpc when
both are described as exponentials, the profile the Freeman disc assumes.  This script recomputes the six CFG285 rows with R_e,* = 1.55 kpc (stars) and R_e,gas = 1.53 kpc (the 870 um dust size as the gas proxy), everything else as CFG285 (real velocities,
the same Monte Carlo design with new seeds, the same estimator).  It also tabulates the stars-only and gas-only bounds for the thin-disc inclinations of the two PDFs (including the unmasked 870 um fit, b/a 0.40 = 66.4 deg).
Hand estimates written BEFORE the first run (arithmetic only): the Freeman factor at R/R_d = 3.84 is about 1.17, so g_bar rises by about +0.07 dex: S0 s* about 4.7 (+-0.7); G1 about 7.3 (+-1.2); S1 D about 0.80 (FLOOR, borderline resolution);
G2 D about 1.04 (near the floor, s* below 1); S2 and G3 FLOORS.
Control: with the frozen radii (2.24, 2.24) this script reproduces CFG285's committed nominal D of all six rows to 1e-9.
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math, zlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))

A0C, NU = H.A0C, H.NU
AT = os.path.join(REPO, "data_assembly", "arxiv_tables"); LD = os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02")
T = {k: pd.read_csv(os.path.join(AT, v)).set_index("id") for k, v in {"samp": "alpaka1_sample.csv", "geo": "alpaka1_geometry.csv"}.items()}
OUTER = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"), usecols=["id", "z", "R_ext_kpc"]).set_index("id")
KIN = pd.read_csv(os.path.join(AT, "alpaka1_kinematics.csv")).set_index("id").loc[24]
L2 = pd.read_csv(os.path.join(LD, "adf22_5_literature_values.csv"), dtype=str).set_index("quantity"); L3 = pd.read_csv(os.path.join(LD, "adf22web3_2609.06679_A7_values.csv"), dtype=str).set_index("quantity")
LD_ = pd.read_csv(os.path.join(LD, "adf22_pdf_direct_reads_A7.csv"), dtype=str).set_index("quantity")
f2 = lambda q, c="value": float(L2.loc[q, c]); f3 = lambda q, c="value": float(L3.loc[q, c]); fd = lambda q, c="value": float(LD_.loc[q, c])
Z = float(T["samp"].loc[24, "z"]); R_EXT = float(OUTER.loc[24, "R_ext_kpc"]); I_AD = float(T["geo"].loc[24, "i_alma"]); E_I = 0.5 * (float(T["geo"].loc[24, "e1.3"]) + float(T["geo"].loc[24, "e2.3"]))
V, EVHI, EVLO = float(KIN["vext_kms"]), float(KIN["vext_errhi"]), float(KIN["vext_errlo"])
MSTAR = f2("Mstar"); LOGM0 = math.log10(MSTAR); SIG_HI = math.log10((MSTAR + f2("Mstar", "err_hi")) / MSTAR); SIG_LO = -math.log10((MSTAR - f2("Mstar", "err_lo")) / MSTAR)
LOGLP10, SLP10 = f3("logLp_CO10"), f3("logLp_CO10", "err_hi"); LP10 = 10 ** LOGLP10
RE_FROZEN = f2("F444W_Re")                                                       # 2.24 (the free-n fit)
RE_S_EXP, RE_G_EXP = fd("umehata25_F444W_n1_Re"), fd("umehata25_870um_masked_Re")   # 1.55 (F444W n = 1 fit), 1.53 (870 um masked, n = 1.01)
LAWV = {k: H.LAWS[k](Z) for k in ("FLAT", "H(z)", "PROXY")}
ROWS = {"S0": (True, 0.0), "S1": (True, 0.8), "S2": (True, 3.6), "G1": (False, 0.8), "G2": (False, 1.36), "G3": (False, 3.6)}
B = 10000
r285 = json.load(open(os.path.join(HERE, "cfg285_stageB_results.json")))["numbers"]["rows"]


def forces(stars, alpha, re_s, re_g):
    gs = float(H.gdisc(MSTAR, re_s, R_EXT)) if stars else 0.0
    gg = float(H.gdisc(alpha * LP10, re_g, R_EXT)) if alpha > 0 else 0.0
    return gs, gg


def gobs(i_deg=None):
    inc = I_AD if i_deg is None else i_deg
    return V ** 2 * (math.sin(math.radians(I_AD)) / math.sin(math.radians(inc))) ** 2 / R_EXT * H.G2SI


def nominal(stars, alpha, re_s, re_g, i_deg=None):
    gs, gg = forces(stars, alpha, re_s, re_g); gb = gs + gg; go = gobs(i_deg)
    ls, st = H.s_status(np.array([go / gb]), np.array([gb]))
    return dict(go=go, gb=gb, D=go / gb, status=st, s=H.s_val_status(ls, st), ls=ls)


def mc(stars, alpha, re_s, re_g, label):
    rng = np.random.default_rng(zlib.crc32(("285|posthoc|" + label).encode()) % 100000)
    Vd = H.split_normal(rng, V, EVHI, EVLO, B); ii = rng.normal(I_AD, E_I, B)
    for _ in range(60):
        bad = (ii < 5) | (ii > 85)
        if not bad.any(): break
        ii[bad] = rng.normal(I_AD, E_I, int(bad.sum()))
    god = Vd ** 2 / R_EXT * H.G2SI * (math.sin(math.radians(I_AD)) / np.sin(np.radians(ii))) ** 2
    Lpd = 10 ** H.split_normal(rng, LOGLP10, SLP10, SLP10, B); Msd = 10 ** H.split_normal(rng, LOGM0, SIG_HI, SIG_LO, B)
    gbd = (H.gdisc(Msd, re_s, R_EXT) if stars else 0.0) + (H.gdisc(alpha * Lpd, re_g, R_EXT) if alpha > 0 else 0.0)
    lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
    return q, float(np.mean(ud))


def eq_alpha(s_law, go, gstar, gun):
    hi = (go - gstar) / gun
    if hi <= 0: return float("nan")
    def too_high(a):
        gb = gstar + a * gun; ls, st = H.s_status(np.array([go / gb]), np.array([gb]))
        return True if st == "ceiling" else (False if st == "floor" else ls > math.log10(s_law))
    if gstar > 0 and not too_high(0.0): return float("nan")
    lo = 0.0 if gstar > 0 else 1e-6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if too_high(mid): lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


P(__doc__.strip().split("Control:")[0].strip()); P("")
P(f"radii: frozen {RE_FROZEN} kpc (free-n F444W, n = 3.21); exponential-matched: stars {RE_S_EXP} kpc (F444W n = 1 fit), gas proxy {RE_G_EXP} kpc (870 um masked, n = 1.01); R_ext {R_EXT:.3f} kpc; g_obs {gobs():.4e}")
# control: the frozen radii reproduce CFG285's committed nominal D
dmax = max(abs(nominal(st, a, RE_FROZEN, RE_FROZEN)["D"] / r285[k]["D"] - 1) for k, (st, a) in ROWS.items())
P(f"CONTROL: with the frozen radii this script reproduces CFG285's committed nominal D of all six rows to {dmax:.1e} relative: {'PASS' if dmax < 1e-9 else 'FAIL'}")
RES = {}
P("\nSIX ROWS: frozen geometry (CFG285, committed) against the exponential-matched geometry (post hoc)")
hdr = f"{'row':4s} {'frozen: D / status / s* / no-root / resolution':62s} | {'exp-fit: D / status / s* / no-root / resolution':62s} | rooted 68 % / 95 % (exp-fit)"
P(hdr)
for k, (st, a) in ROWS.items():
    nm = nominal(st, a, RE_S_EXP, RE_G_EXP); q, frn = mc(st, a, RE_S_EXP, RE_G_EXP, k)
    res = "RESOLVED-ROOT" if frn <= 0.16 else ("RESOLVED-FLOOR" if frn >= 0.84 else "UNRESOLVED")
    fz = r285[k]; sf = f"{fz['s']:.3g}" if fz["status"] == "root" else "-"; sn = f"{nm['s']:.3g}" if nm["status"] == "root" else "-"
    rp = f"[{10 ** q[1]:.3g}, {10 ** q[3]:.3g}] / [{10 ** q[0]:.3g}, {10 ** q[4]:.3g}]" if np.isfinite(q[0]) else "-"
    RES[k] = dict(nominal=nm, frac_noroot=frn, resolution=res, q=q)
    P(f"{k:4s} D {fz['D']:.3f} {fz['status']:5s} s* {sf:>6s} nr {fz['frac_mc_noroot']:.3f} {fz['resolution']:14s} | D {nm['D']:.3f} {nm['status']:5s} s* {sn:>6s} nr {frn:.3f} {res:14s} | {rp}")
P("\nCONVERSION EQUIVALENTS (alpha_CO x the measured L'(1-0); exponential-matched geometry): floor boundary / FLAT / PROXY / H(z)")
for fam, st in (("stars + gas", True), ("gas only", False)):
    go = gobs(); gs, _ = forces(True, 0.0, RE_S_EXP, RE_G_EXP); gstar = gs if st else 0.0; gun = float(H.gdisc(LP10, RE_G_EXP, R_EXT))
    a_d1 = (go - gstar) / gun
    eq = {k_: eq_alpha(LAWV[k_], go, gstar, gun) for k_ in ("FLAT", "PROXY", "H(z)")}
    RES["eq_" + fam] = dict(D1=a_d1, **eq)
    P(f"  {fam:12s}: {a_d1:.3f} / {eq['FLAT']:.3f} / {eq['PROXY']:.3f} / {eq['H(z)']:.3f}   (frozen geometry: {r285['S1' if st else 'G1']['alpha_D1']:.3f} / {r285['S1' if st else 'G1']['alpha_eq']['FLAT']:.3f} / {r285['S1' if st else 'G1']['alpha_eq']['PROXY']:.3f} / {r285['S1' if st else 'G1']['alpha_eq']['H(z)']:.3f})")
P("\nTHIN-DISC INCLINATIONS (nominal s* under the exponential-matched radii; the kinematic inclination is 75 deg): S0 stars only / G1 gas only at 0.8")
incs = [("kinematic 75 (frozen)", None), ("F444W free n, b/a 0.54", math.degrees(math.acos(fd("umehata25_F444W_free_ba")))), ("F444W n = 1, b/a 0.57", math.degrees(math.acos(fd("umehata25_F444W_n1_ba")))),
        ("870 um masked, b/a 0.58", math.degrees(math.acos(fd("umehata25_870um_masked_ba")))), ("870 um unmasked, b/a 0.40", math.degrees(math.acos(fd("umehata25_870um_unmasked_ba"))))]
RES["inclination"] = {}
for nm_, ideg in incs:
    a = nominal(True, 0.0, RE_S_EXP, RE_G_EXP, ideg); b_ = nominal(False, 0.8, RE_S_EXP, RE_G_EXP, ideg)
    RES["inclination"][nm_] = dict(i_deg=ideg or I_AD, S0=a, G1=b_)
    P(f"  {nm_:28s} i = {ideg or I_AD:5.1f} deg: S0 {a['status']:5s} " + (f"s* <= {a['s']:.3g}" if a["status"] == "root" else "").ljust(14) + f" | G1 {b_['status']:5s} " + (f"s* <= {b_['s']:.3g}" if b_["status"] == "root" else ""))
open(os.path.join(HERE, "cfg285_posthoc_expfit_geometry.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(H.jc(dict(radii=dict(frozen=RE_FROZEN, stars_exp=RE_S_EXP, gas_exp=RE_G_EXP), control_dmax=dmax, rows=RES)), open(os.path.join(HERE, "cfg285_posthoc_expfit_geometry_results.json"), "w"), indent=1)
sys.exit(0 if dmax < 1e-9 else 1)
