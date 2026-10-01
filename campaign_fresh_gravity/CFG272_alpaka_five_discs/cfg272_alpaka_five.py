#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG272 -- implied-a0 bounds (or no-root floors) for the five ALPAKA I discs without a gas mass or an a0: IDs 13, 23, 24, 25, 28 (z 2.10-3.63).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG272_alpaka_five_discs/FROZEN_CRITERIA.md (e06a91b8a).
  baryons   LOWER LIMITS: B0 = stars only (headline), B1 = stars + a gas floor (alpha_CO,min = 0.8, r_J1 = 1; alpha_[CI],min = 1.0 for ID 13), B2 = conventional gas (sensitivity).
  g_obs     V_ext^2 / R_ext (a rotation speed, pressure term is a knob); inclination as adopted by the paper, in the Monte Carlo.
  STAGE=A   the blind pre-flight: no velocity column is loaded; no g_obs, D, delta or s* is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V x 2); STAGE=B SELFTEST=1 (fabricated V on the law at s = 2).
Run: STAGE=A python3 .../cfg272_alpaka_five.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv, contextlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

STAGE = os.environ.get("STAGE", "").strip().upper()
MUTATE = os.environ.get("MUTATE", "0") == "1"
SELFTEST = os.environ.get("SELFTEST", "0") == "1"
assert STAGE in ("A", "B"), "set STAGE=A or STAGE=B"
assert not ((MUTATE or SELFTEST) and STAGE == "A") and not (MUTATE and SELFTEST), "MUTATE / SELFTEST apply to stage B, one at a time"
SFX = f"_stage{STAGE}" + ("_MUTATE1" if MUTATE else "") + ("_SELFTEST" if SELFTEST else "")
LOG, CHK, NUM = [], [], {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def check(name, detail, ok, load_bearing=True):
    CHK.append((name, bool(ok), load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         {detail}")


P(__doc__.split("Run:")[0].strip())
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: every V_ext x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
IDS = [13, 23, 24, 25, 28]
WITH_M = [13, 23, 25, 28]
B_MC = 10000
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
dirs = {"samp": "alpaka1_sample.csv", "prop": "alpaka1_properties.csv", "geo": "alpaka1_geometry.csv", "obs": "alpaka1_alma_obs.csv"}
T = {k: pd.read_csv(os.path.join(AT, v)).set_index("id") for k, v in dirs.items()}
OUTER = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv")).set_index("id")
RING = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"), usecols=["id", "ring", "panel", "R_kpc"])
KINP = os.path.join(AT, "alpaka1_kinematics.csv")
P("sha256: " + ", ".join(f"{v} {H.sha(os.path.join(AT, v))}" for v in dirs.values()) + f", alpaka1_outer_summary.csv {H.sha(os.path.join(AT, 'alpaka1_digitised', 'alpaka1_outer_summary.csv'))}; velocity columns loaded: {STAGE == 'B'}")
KIN = pd.read_csv(KINP).set_index("id") if STAGE == "B" else None

# the frozen gas routes (alpha_CO frozen before any velocity is read): (B1 floor, B2 conventional)
GAS_ALPHA = {13: (1.0, 9.7), 23: (0.8, 4.36), 24: (0.8, 4.36), 25: (0.8, 0.8), 28: (0.8, 0.8)}
LINE = {13: "[CI](2-1)", 23: "CO(3-2)", 24: "CO(3-2)", 25: "CO(3-2)", 28: "CO(6-5)"}
G = {}
for i in IDS:
    s, p, ge, ob, ou = T["samp"].loc[i], T["prop"].loc[i], T["geo"].loc[i], T["obs"].loc[i], OUTER.loc[i]
    Ms = float(p["mstar_1e10msun"]) * 1e10 if np.isfinite(p["mstar_1e10msun"]) else float("nan")
    eM = float(p["e_mstar"]) / (float(p["mstar_1e10msun"]) * math.log(10)) if np.isfinite(p["mstar_1e10msun"]) else float("nan")
    if np.isfinite(ge["i_hst"]):
        i_ad, e_i = float(ge["i_hst"]), 0.5 * (float(ge["e1.1"]) + float(ge["e2.1"])); i_alt = float(ge["i_alma"]) if np.isfinite(ge["i_alma"]) else float("nan")
        i_src = "i_HST"
    else:
        i_ad, e_i = float(ge["i_alma"]), 0.5 * (float(ge["e1.3"]) + float(ge["e2.3"])); i_alt = float("nan"); i_src = "i_ALMA"
    R_ext = float(ou["R_ext_kpc"]); Re = float(ou["Re_kpc_dashed_line"]) if np.isfinite(ou["Re_kpc_dashed_line"]) else R_ext / 1.2
    rr = RING[(RING["id"] == i) & (RING["panel"] == "V")].sort_values("ring")
    R_mean = float(rr["R_kpc"].iloc[-2:].mean())
    Lp = float(p["lprime_1e10_kkmspc2"]) * 1e10
    G[i] = dict(id=i, name=str(s["name"]), z=float(s["z"]), Ms=Ms, eM=eM, Lp=Lp, line=LINE[i], i=i_ad, ei=e_i, i_alt=i_alt, i_src=i_src, R=R_ext, R_ext=R_ext, Re=Re, R_mean=R_mean, Re_dashed=bool(np.isfinite(ou["Re_kpc_dashed_line"])),
                beam_maj=float(ob["beam_major_arcsec"]), beam_min=float(ob["beam_minor_arcsec"]), R_ext_arcsec=float(ou["R_ext_arcsec"]), kpa=float(ou["R_ext_kpc"]) / float(ou["R_ext_arcsec"]),
                Mg1=GAS_ALPHA[i][0] * Lp, Mg2=GAS_ALPHA[i][1] * Lp, snr_line=float(p["iline_jykms"]) / float(p["e_iline"]), type=str(p["type_ms_or_other"]))
    if STAGE == "B":
        k = KIN.loc[i]
        G[i].update(V=float(k["vext_kms"]), eVhi=float(k["vext_errhi"]), eVlo=float(k["vext_errlo"]), sig=float(k["sigma_ext_kms"]))


def gobs_gbar(g, route="B0", vm="pub", inc="adopt", rad="ext", star_fac=1.0, refac=1.0, sph=False, jwst=False, gas_fac=1.0, ts=0.0, tg=0.0, Ms=None, V=None):
    """g_obs and g_bar [m s^-2] of one galaxy under a baryon route (B0 / B1 / B2) and a knob setting."""
    R = g["R_ext"] if rad == "ext" else g["R_mean"]
    gb = None
    Ms_ = g["Ms"] if Ms is None else Ms
    Re_s, Re_g = g["Re"] * refac * star_fac, g["Re"] * refac
    if jwst:
        Re_s, Re_g = 3.34, 5.1
    Mg = {"B0": 0.0, "B1": g["Mg1"], "B2": g["Mg2"]}[route] * gas_fac
    f = H.gsph if sph else H.gdisc
    gb = (f(Ms_ * 10 ** ts, Re_s, R) if np.isfinite(g["Ms"]) else 0.0) + f(Mg * 10 ** tg, Re_g, R)
    go = None
    if STAGE == "B":
        V2 = (g["V"] if V is None else V) ** 2 + {"pub": 0.0, "a168": 1.68 * g["sig"] ** 2, "a336": 3.36 * g["sig"] ** 2}[vm]
        i_new = {"adopt": g["i"], "alt": g["i_alt"], "lo": max(5.0, g["i"] - g["ei"]), "hi": min(85.0, g["i"] + g["ei"])}[inc]
        go = V2 * (math.sin(math.radians(g["i"])) / math.sin(math.radians(i_new))) ** 2 / R * H.G2SI
    return go, gb


for i in IDS:
    g = G[i]
    g["GB0"] = float(gobs_gbar(g, "B0")[1]) if np.isfinite(g["Ms"]) else float("nan")
    g["GB1"] = float(gobs_gbar(g, "B1")[1]); g["GB2"] = float(gobs_gbar(g, "B2")[1])
    g["y0"] = g["GB0"] / A0C; g["y1"] = g["GB1"] / A0C; g["y2"] = g["GB2"] / A0C
    g["nuy0"] = float(NU(np.array([g["y0"]]))[0]) if np.isfinite(g["y0"]) else float("nan")
P("rows: " + "; ".join(f"{i} {G[i]['name']} z {G[i]['z']:.3f} line {G[i]['line']} R_ext {G[i]['R_ext']:.2f} kpc R_e {G[i]['Re']:.2f}{' (dashed)' if G[i]['Re_dashed'] else ' (R_ext/1.2)'} M* {G[i]['Ms']:.2e} i {G[i]['i']:.0f} ({G[i]['i_src']})" for i in IDS))

KNOB_LIST = [("stars at 2 R_e", dict(star_fac=2.0)), ("R_e x1.5", dict(refac=1.5)), ("R_e /1.5", dict(refac=1 / 1.5)), ("spherical", dict(sph=True)), ("pressure +1.68 sigma^2", dict(vm="a168")),
             ("pressure +3.36 sigma^2", dict(vm="a336")), ("inclination: the other of (i_HST, i_ALMA)", dict(inc="alt")), ("inclination -1 sigma", dict(inc="lo")), ("inclination +1 sigma", dict(inc="hi")),
             ("V_ext at R_mean of the last two rings", dict(rad="mean")), ("kernel P2", dict(nu=NUP2)), ("ID 13: JWST R_e 3.34 kpc, gas disc 5.1 kpc", dict(jwst=True))]
KGROUP = {"stars at 2 R_e": "geometry", "R_e x1.5": "geometry", "R_e /1.5": "geometry", "spherical": "geometry", "pressure +1.68 sigma^2": "pressure", "pressure +3.36 sigma^2": "pressure",
          "inclination: the other of (i_HST, i_ALMA)": "inclination", "inclination -1 sigma": "inclination", "inclination +1 sigma": "inclination", "V_ext at R_mean of the last two rings": "radius", "kernel P2": "kernel",
          "ID 13: JWST R_e 3.34 kpc, gas disc 5.1 kpc": "geometry"}

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (no velocity column is loaded; no g_obs, D, delta or s* is formed)")
    check("C1 CONTROL: the five rows exist with finite z, R_ext, R_e, inclination, L' and (except ID 24) M*, and the CSV hashes are printed above",
          f"z {[G[i]['z'] for i in IDS]}; M* finite for {[i for i in IDS if np.isfinite(G[i]['Ms'])]}", all(np.isfinite([G[i][k] for k in ("z", "R_ext", "Re", "i", "Lp")]).all() for i in IDS) and [i for i in IDS if np.isfinite(G[i]["Ms"])] == WITH_M)
    yy = np.linspace(0.05, 40, 400000); hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh))
    farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20)
        dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12",
          f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation from CFG229's gdisc {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    pts = list(csv.DictReader(open(os.path.join(CFG, "CFG227_rar_z2_5", "cfg227_points.csv"))))
    s3 = {r["id"]: r["g_bar"] for r in pts if r["set"].startswith("S3 ALPAKA")}
    miss = [i for i in WITH_M if str(i) not in s3]
    same3 = all(f"{G[i]['GB0']:.4e}" == s3[str(i)] for i in WITH_M if str(i) in s3)
    dev3 = max(abs(G[i]["GB0"] / float(s3[str(i)]) - 1) for i in WITH_M if str(i) in s3) if len(miss) < len(WITH_M) else float("nan")
    check("C3 CONTROL: the stars-only g_bar of 13, 23, 25, 28 formatted %.4e equals CFG227's printed S3 g_bar string and the relative deviation is at most 5.1e-5 (only g_bar is read from that file)",
          f"rows found in CFG227 S3: {[i for i in WITH_M if str(i) in s3]} (missing {miss}); exact match {same3}; max relative deviation {dev3:.1e}", same3 and not miss and dev3 < 5.1e-5)
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C4 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    d5 = 0.0
    for i in WITH_M:
        for st in (0.5, 1.0, 2.5):
            ls, unb = H.s_star(NU(np.array([G[i]["GB0"] / (A0C * st)])), np.array([G[i]["GB0"]])); d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every stars-only baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)
    P("\nA1 / A2  BARYON SIDE AND THE CFG240 READING (noiseless world; lever = d log10 s* / d(baryon dex); ILL-CONDITIONED iff |lever| >= 10 or not computable; CFG240 T3: nu -> 1 at large y removes the a0 dependence; break-even needs y >~ 8 with deep points)")
    ILL, LEV = {}, {}
    for i in WITH_M:
        g = G[i]; lv, fl = H.lever1(np.array([g["nuy0"]]), np.array([g["GB0"]]))
        LEV[i] = lv; ILL[i] = bool(fl or abs(lv) >= 10)
        P(f"    {i} {g['name']}: B0 g_bar {g['GB0']:.3e}  y {g['y0']:.1f}  nu(y) {g['nuy0']:.4f}  lever {lv:+.1f}{' (flag)' if fl else ''}  {'ILL-CONDITIONED' if ILL[i] else 'conditioned'}   B1 y {g['y1']:.1f}  B2 y {g['y2']:.1f}   one radius per disc: no point below y_min = 0.1 (CFG240: never reaches 0.1 dex)")
    g24 = G[24]; P(f"    24 {g24['name']}: no M*; gas floor only: B1 y {g24['y1']:.2f}, B2 y {g24['y2']:.2f} (a baryon lower limit made of the gas alone: uninformative; no point)")
    P("\nC6  COVERAGE (noiseless world on the B0 baryons; declared 10 % V error, the published inclination error truncated to [5, 85] deg, the published M* error; 300 mock datasets, B = 1,000)")
    rng6 = np.random.default_rng(272); COV, PREC = {}, {}
    for i in WITH_M:
        g = G[i]; c68 = c95 = nd = 0; sds = []
        for it in range(300):
            Ms_o = g["Ms"] * 10 ** rng6.normal(0, g["eM"])                                              # the 'observed' stellar mass
            gob_true = g["GB0"] * float(NU(np.array([g["GB0"] / A0C]))[0])
            i_o = min(max(rng6.normal(g["i"], g["ei"]), 5.0), 85.0)                                       # the 'observed' (adopted) inclination
            fac_obs = (math.sin(math.radians(g["i"])) / math.sin(math.radians(i_o))) ** 2
            god = gob_true * (1 + 0.10 * rng6.normal()) ** 2 * fac_obs                                    # the 'observed' g_obs (V error 0.10, inclination error)
            ii = rng6.normal(i_o, g["ei"], 1000)
            for _ in range(60):
                bad = (ii < 5) | (ii > 85)
                if not bad.any(): break
                ii[bad] = rng6.normal(i_o, g["ei"], int(bad.sum()))
            facm = (math.sin(math.radians(i_o)) / np.sin(np.radians(ii))) ** 2                            # Monte Carlo around the observed values
            gobm = god * (1 + 0.10 * rng6.normal(size=1000)) ** 2 * facm
            Msd = Ms_o * 10 ** rng6.normal(0, g["eM"], 1000); gbd = H.gdisc(Msd, g["Re"], g["R"])
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C); q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]):
                nd += 1; c68 += (q[1] <= 0.0 <= q[3]); c95 += (q[0] <= 0.0 <= q[4]); sds.append(0.5 * (q[3] - q[1]))
        COV[i] = (c68 / max(nd, 1), c95 / max(nd, 1), nd); PREC[i] = float(np.median(sds)) if sds else float("nan")
        P(f"    {i}: coverage 68 % {COV[i][0]:.2f}, 95 % {COV[i][1]:.2f} (rooted mocks {nd} of 300); median 68 % half-width {PREC[i]:.2f} dex")
    check("C6 (reported; load-bearing only for conditioned rows): the Monte Carlo interval covers the truth in >= 60 % (68 %) and >= 88 % (95 %) of the mocks for every conditioned row", "; ".join(f"{i} {COV[i][0]:.2f}/{COV[i][1]:.2f}" for i in WITH_M) + ("" if any(not ILL[i] for i in WITH_M) else "  (no conditioned row: not applicable)"),
          all(COV[i][0] >= 0.60 and COV[i][1] >= 0.88 for i in WITH_M if not ILL[i]) if any(not ILL[i] for i in WITH_M) else True, load_bearing=any(not ILL[i] for i in WITH_M))
    P("\nA3  KNOB EFFECTS ON g_bar (dex relative to B0; baryon side only)")
    for i in WITH_M:
        g = G[i]; g0 = g["GB0"]
        kb = {"stars 2R_e": gobs_gbar(g, star_fac=2.0)[1], "R_e x1.5": gobs_gbar(g, refac=1.5)[1], "R_e /1.5": gobs_gbar(g, refac=1 / 1.5)[1], "spherical": gobs_gbar(g, sph=True)[1]}
        if i == 13: kb["JWST R_e 3.34"] = gobs_gbar(g, jwst=True)[1]
        P(f"    {i}: " + "; ".join(f"{k} {math.log10(float(v) / g0):+.3f}" for k, v in kb.items()))
    P("\nA4  GAS FLOOR AS A FRACTION OF THE STARS (g_bar ratios B1/B0 and B2/B0 at R_ext, and the mass ratio)")
    for i in WITH_M:
        g = G[i]; P(f"    {i}: M_gas,B1/M* {g['Mg1'] / g['Ms']:.3f}, M_gas,B2/M* {g['Mg2'] / g['Ms']:.3f}; g_bar B1/B0 {g['GB1'] / g['GB0']:.3f}, B2/B0 {g['GB2'] / g['GB0']:.3f}")
    P("\nA5  INCLINATION (no velocity): the g_obs factor between the adopted and the other inclination, sin^2(i_adopted)/sin^2(i_other) (dex)")
    for i in IDS:
        g = G[i]
        if np.isfinite(g["i_alt"]): P(f"    {i}: i {g['i']:.0f} ({g['i_src']}) vs {g['i_alt']:.0f}: factor {(math.sin(math.radians(g['i'])) / math.sin(math.radians(g['i_alt']))) ** 2:.2f} = {2 * math.log10(math.sin(math.radians(g['i'])) / math.sin(math.radians(g['i_alt']))):+.3f} dex")
        else: P(f"    {i}: i {g['i']:.0f} ({g['i_src']}), no second value (error {g['ei']:.1f} deg)")
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P(f"  PF-D2 ILL-CONDITIONED rows ({sum(ILL.values())} of 4 with an M*): " + (", ".join(str(i) for i in WITH_M if ILL[i]) or "none") + "; ID 24: no M*, no point")
    P("  PF-D3 DRAWABLE as an a0 point: " + (", ".join(str(i) for i in WITH_M if pfd1 and not ILL[i]) or "none") + "; every row is in any case a LIMIT (baryons are a lower limit), never a measurement")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE3-HE7 are scored at stage B):")
    he = {}
    he["HE1"] = all(G[i]["y0"] >= 5 for i in WITH_M) and all(ILL[i] for i in WITH_M) and not any(pfd1 and not ILL[i] for i in WITH_M)
    he["HE2"] = G[13]["Mg1"] / G[13]["Ms"] < 0.3 and G[23]["Mg1"] / G[23]["Ms"] < 0.3 and G[25]["Mg1"] / G[25]["Ms"] < 0.3 and 0.35 <= G[28]["Mg1"] / G[28]["Ms"] <= 0.65
    for k, v in he.items(): P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(inputs={i: {k: G[i][k] for k in ("z", "Ms", "eM", "Lp", "i", "ei", "i_alt", "R_ext", "Re", "R_mean", "Mg1", "Mg2", "GB0", "GB1", "GB2", "y0", "y1", "y2")} for i in IDS}, lever=LEV, ill=ILL, coverage={i: list(COV[i]) for i in WITH_M}, precision=PREC, hand_estimates=he,
               pf=dict(PF_D1=bool(pfd1), n_ill=sum(ILL.values())))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2720)
    if SELFTEST:
        for i in WITH_M:
            g = G[i]; gob = g["GB0"] * float(NU(np.array([g["GB0"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15)
            g["V"] = math.sqrt(gob * g["R_ext"] / H.G2SI); g["eVhi"] = g["eVlo"] = 0.10 * g["V"]; g["sig"] = 0.10 * g["V"]
        G[24]["V"] = 200.0; G[24]["eVhi"] = G[24]["eVlo"] = 20.0; G[24]["sig"] = 20.0
        P("SELFTEST: V fabricated from the law at s_true = 2 on the B0 baryons (+0.15 dex scatter on g_obs); the real velocities are not used")
    if MUTATE:
        for i in IDS: G[i]["V"] *= 2.0; G[i]["eVhi"] *= 2.0; G[i]["eVlo"] *= 2.0
    RES = {}

    def solve(g, route="B0", **kw):
        kw = dict(kw); nu = kw.pop("nu", NU)
        go, gb = gobs_gbar(g, route, **kw)
        return H.s_star(np.array([go / gb]), np.array([gb]), nu), float(go), float(gb)

    for i in WITH_M:
        g = G[i]; lab = str(i)
        (ls0, u0), go0, gb0 = solve(g)
        D0 = go0 / gb0
        (ls1, u1), go1, gb1 = solve(g, "B1"); (ls2, u2), go2, gb2 = solve(g, "B2")
        rng = np.random.default_rng(zlib.crc32(("272|" + lab).encode()) % 100000)
        Vd = H.split_normal(rng, g["V"], g["eVhi"], g["eVlo"], B_MC)
        ii = rng.normal(g["i"], g["ei"], B_MC)
        for _ in range(60):
            bad = (ii < 5) | (ii > 85)
            if not bad.any(): break
            ii[bad] = rng.normal(g["i"], g["ei"], int(bad.sum()))
        facd = (math.sin(math.radians(g["i"])) / np.sin(np.radians(ii))) ** 2
        god = Vd ** 2 / g["R_ext"] * H.G2SI * facd
        Msd = g["Ms"] * 10 ** rng.normal(0, g["eM"], B_MC); gbd = H.gdisc(Msd, g["Re"], g["R_ext"])
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(go0 / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        bands = H.band_solutions(np.array([D0]), np.array([gb0]))
        gas_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(g, "B1", tg=s_)[1])]), np.array([float(gobs_gbar(g, "B1", tg=s_)[1])])) for s_ in (-0.671, -0.213, 0.213, 0.671)}
        star_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(g, ts=s_)[1])]), np.array([float(gobs_gbar(g, ts=s_)[1])])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        kn = {}
        for nm, kw in KNOB_LIST:
            if nm.startswith("ID 13") and i != 13: continue
            if nm.startswith("inclination: the other") and not np.isfinite(g["i_alt"]): continue
            (lk, uk), _, _ = solve(g, **dict(kw))
            kn[nm] = None if (u0 or uk) else lk - ls0; kn[nm + "|root"] = (not uk)
        grp = {}
        for nm, _ in KNOB_LIST:
            if nm in kn and kn[nm] is not None: grp.setdefault(KGROUP[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root = sum(1 for nm, _ in KNOB_LIST if nm in kn and kn[nm + "|root"]); n_k = sum(1 for nm, _ in KNOB_LIST if nm in kn)
        lv_nl, lf_nl = H.lever1(np.array([g["nuy0"]]), np.array([g["GB0"]]))
        dflo = H.delta_floor(np.array([D0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        inc_eff = float("nan")
        if np.isfinite(g["i_alt"]): inc_eff = 2 * math.log10(math.sin(math.radians(g["i"])) / math.sin(math.radians(g["i_alt"])))
        RES[lab] = dict(id=i, name=g["name"], z=g["z"], n=1, V=g["V"], GO=go0, GB=gb0, D=D0, y=g["y0"], ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=q, frac_mc_noroot=frn, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1],
                        s_B1=H.s_val(ls1, u1), noroot_B1=u1, D_B1=go1 / gb1, s_B2=H.s_val(ls2, u2), noroot_B2=u2, D_B2=go2 / gb2,
                        bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, gas_bands={f"{k:+.3f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in gas_b.items()},
                        star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root, n_knobs=n_k, lever=lv_nl,
                        ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=dflo, delta_to_s1=d1, inc_factor_dex=inc_eff)
        R_ = RES[lab]
        P(f"  {i} {g['name']}: z {g['z']:.3f}  g_obs {go0:.3e}  g_bar(B0) {gb0:.3e}  D {D0:.3f}  delta_FLAT {dF0:+.3f} [{dq[0]:+.3f}, {dq[1]:+.3f}]  y {g['y0']:.1f}  " + ("NO ROOT" if u0 else f"s* <= {10 ** ls0:.3g} (a0 <= {10 ** ls0 * 0.93603:.3g}e-10)")
          + f"  MC rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.3g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.3g}] (draws without a root {frn:.2f})")
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"      B1 (gas floor): D {go1 / gb1:.3f} " + ("NO ROOT" if u1 else f"s* <= {10 ** ls1:.3g}") + f";  B2 (conventional gas): D {go2 / gb2:.3f} " + ("NO ROOT" if u2 else f"s* = {10 ** ls2:.3g}") + f";  baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}]{' (no-root corner)' if b15[2] else ''}  +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]{' (no-root corner)' if b30[2] else ''}")
        P(f"      Delta_floor {dflo:+.3f} dex; baryon shift for s* = 1: {d1:+.3f}; lever (noiseless) {lv_nl:+.1f}{' ILL-CONDITIONED' if R_['ill'] else ''}; knobs with a root {n_root}/{n_k}; recipe half-width {half:.3f}")
        P("      knobs (Delta log10 s*; -- = no root): " + "; ".join(f"{nm} " + ("--" if kn[nm] is None else f"{kn[nm]:+.3f}") + ("" if kn[nm + '|root'] else " (variant has no root)") for nm, _ in KNOB_LIST if nm in kn))
    # ID 24: the gas-floor diagnostic only
    g = G[24]
    go24 = float(g["V"] ** 2 / g["R_ext"] * H.G2SI); gb24 = float(g["GB1"]); gb24b = float(g["GB2"])
    RES["24"] = dict(id=24, name=g["name"], z=g["z"], n=1, V=g["V"], GO=go24, GB_B1=gb24, GB_B2=gb24b, D_B1=go24 / gb24, D_B2=go24 / gb24b, no_root=True, no_point=True)
    P(f"  24 {g['name']}: NO M*: no point; gas-floor-only diagnostic: g_obs {go24:.3e}, g_bar(B1 gas only) {gb24:.3e} (D {go24 / gb24:.2f}), g_bar(B2) {gb24b:.3e} (D {go24 / gb24b:.2f}): the baryon lower limit is made of the gas alone, uninformative")
    # pooled P4
    mem = WITH_M
    Dp = np.array([RES[str(i)]["D"] for i in mem]); GBp = np.array([RES[str(i)]["GB"] for i in mem]); zm = float(np.median([G[i]["z"] for i in mem]))
    ls0, u0 = H.s_star(Dp, GBp); rng = np.random.default_rng(zlib.crc32(b"272|P4") % 100000)
    ib = rng.integers(0, len(mem), size=(B_MC, len(mem))); lsb, ub = H.AI.implied(Dp[ib], GBp[ib], NU, A0C); q, frn = H.rooted_pct(lsb, ub)
    bands = H.band_solutions(Dp, GBp)
    RES["P4"] = dict(id="P4", z=zm, n=4, members=mem, ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=q, frac_mc_noroot=frn, median_D=float(np.median(Dp)), delta_floor=H.delta_floor(Dp),
                     bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs={}, recipe_half=float("nan"), delta_to_s1=H.shift_to_s1(Dp, GBp), lever=H.lever1(Dp, GBp)[0])
    b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
    P(f"  P4 (13, 23, 25, 28; z_med {zm:.3f}): median D {np.median(Dp):.3f}  " + ("NO ROOT" if u0 else f"s* <= {10 ** ls0:.3g}") + f"; bootstrap rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.3g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.3g}] (resamples without a root {frn:.2f}); baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}] +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; Delta_floor {np.log10(np.median(Dp)):+.3f}")
    # cross-check ALPAKA 15 (not in MUTATE / SELFTEST)
    if not MUTATE and not SELFTEST:
        stx = pd.read_csv(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_inputs_static.csv")).set_index("gid").loc["ALPAKA15"]
        knx = pd.read_csv(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_inputs_kin.csv")).set_index("gid").loc["ALPAKA15"]
        c229 = json.load(open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score_results.json")))
        k15 = c229["gid"].index("ALPAKA15")
        go_ = (float(knx["V_noP"]) ** 2 + float(knx["alpha_pub"]) * float(knx["sigma"]) ** 2) / float(stx["R_kpc"]) * H.G2SI
        gb_ = float(H.gdisc(float(stx["Mstar"]), float(stx["Re_kpc"]), float(stx["R_kpc"])) + H.gdisc(10 ** float(stx["logMgas_He"]), float(stx["Re_kpc"]), float(stx["R_kpc"])))
        d_go, d_gb, d_D = abs(go_ / c229["GO"][k15] - 1), abs(gb_ / c229["GB"][k15] - 1), abs((go_ / gb_) / c229["D"][k15] - 1)
        RES["XCHECK_ALPAKA15"] = dict(GO=go_, GB=gb_, D=go_ / gb_, cfg229_GO=c229["GO"][k15], cfg229_GB=c229["GB"][k15], cfg229_D=c229["D"][k15])
        check("M5 CROSS-CHECK: ALPAKA 15 through this lane's functions with CFG229's committed inputs reproduces CFG229's committed g_obs, g_bar and D to 5e-5 relative", f"relative deviations g_obs {d_go:.1e}, g_bar {d_gb:.1e}, D {d_D:.1e}", max(d_go, d_gb, d_D) < 5e-5)
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg272_stageB_results.json")))["numbers"]["rows"]
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        bad = 0.0; nm_ = 0; n0 = sum(1 for i in WITH_M if not main[str(i)]["no_root"])
        for i in WITH_M:
            R_ = RES[str(i)]
            if not R_["no_root"]:
                nm_ += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        check("M2 MUTATE=1 (reactivity without needing a main-run root): every V_ext x 2; rows with a root satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and their number is at least the main run's", f"rows with a root: mutated {nm_}, main {n0}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and nm_ >= n0)
    else:
        d1m = 0.0
        for i in WITH_M:
            R_ = RES[str(i)]
            if R_["no_root"]: continue
            la, ua = H.AI.implied(np.array([R_["D"]]), np.array([R_["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for i in WITH_M if not RES[str(i)]['no_root'])} rows with a root)", d1m < 1e-9)
        check("M3 P4 holds four members, the rows with an M*", f"P4 {RES['P4']['n']} = {RES['P4']['members']}", RES["P4"]["n"] == 4 and RES["P4"]["members"] == WITH_M)
        if SELFTEST:
            tested = [i for i in WITH_M if not RES[str(i)]["ill"] and not RES[str(i)]["no_root"]]
            if tested:
                check("SELFTEST: every conditioned row returns the fabricated truth inside its 95 % interval", "; ".join(f"{i} s* {RES[str(i)]['s']:.3g}" for i in tested) + " (truth 2)", all(RES[str(i)]["q"][0] <= math.log10(2.0) <= RES[str(i)]["q"][4] for i in tested))
            else:
                P("  SELFTEST: every row is ILL-CONDITIONED (or has no root): the truth-recovery check is not applicable; s*: " + "; ".join(f"{i} " + ("no root" if RES[str(i)]["no_root"] else f"{RES[str(i)]['s']:.3g}") for i in WITH_M))
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot",
                              "gas_in_lo", "gas_in_hi", "gas_out_lo", "gas_out_hi", "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "s_B1", "noroot_B1", "s_B2", "noroot_B2", "limit",
                              "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    nan = float("nan"); rows = []
    for lab in [str(i) for i in IDS] + ["P4"]:
        R_ = RES[lab]; pooled = lab == "P4"
        if lab == "24":
            g = G[24]
            rows.append(["CFG272", f"ALPAKA {lab} {g['name']}", "L (line L' only; alpha_CO frozen as a lower limit)", f"{g['z']:.4f}", f"{g['z']:.4f}", 1] + ["nan"] * 12 + ["nan"] * 4 + ["nan"] * 23 + ["na", "na", "na", "NO M*: stars-only baryons do not exist; no point (listed as CFG227); gas-floor-only diagnostic g_bar(B1) %.3e, D %.2f (uninformative)" % (R_["GB_B1"], R_["D_B1"])])
            continue
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30); q = R_["q"]
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (FLOOR, FLOOR); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (FLOOR, FLOOR)
        fl = H.flags_for(R_["z"], lo95, hi95, b15[:2], b30[:2], not R_["no_root"])
        half = R_["recipe_half"]
        if not pooled:
            gb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["gas_bands"].items()}; sb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()}
            gi = H.band_edges(gb_, -0.213, 0.213); go_ = H.band_edges(gb_, -0.671, 0.671); si = H.band_edges(sb_, -0.15, 0.15); so = H.band_edges(sb_, -0.30, 0.30)
            extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], gi[0], gi[1], go_[0], go_[1], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"], R_["s_B1"], int(R_["noroot_B1"]), R_["s_B2"], int(R_["noroot_B2"])]
            g = G[int(lab)]
            q_ = ("ILL-CONDITIONED near-Newtonian (|lever| >= 10); " if R_["ill"] else "") + ("NO ROOT with stars-only baryons (a lower limit): robust against any added gas" if R_["no_root"] else "has a root with stars-only baryons: s* is an UPPER bound") + f"; line {g['line']} ({g['snr_line']:.1f} sigma); {g['i_src']} {g['i']:.0f} deg" + ("; AGN" if lab in ("23", "25", "28") else "") + ("; protocluster SSA22" if lab in ("23", "25") else "")
            n_k = R_["n_knobs_with_root"]; gcl = "L (line L' only; alpha_CO frozen as a lower limit)"
        else:
            extra = [nan, R_["lever"], 1, nan, nan, nan, R_["median_D"], R_["frac_mc_noroot"]] + [nan] * 8 + [R_["delta_floor"], R_["delta_to_s1"]] + [nan, "", nan, ""]
            q_ = "pooled row of the four discs with an M*, stars-only lower limit, never a headline; " + ("NO ROOT (median D <= 1)" if R_["no_root"] else "has a root"); n_k = ""; gcl = "L (pooled)"
        rows.append(["CFG272", f"ALPAKA {lab}" + (f" {G[int(lab)]['name']}" if not pooled else " pooled P4"), gcl, f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(R_["no_root"]), f"{R_['s']:.6g}", f"{R_['s'] * 0.93603:.6g}",
                     f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}", f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2],
                     f"{half:.4f}" if np.isfinite(half) else "nan", f"{R_['s'] * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{R_['s'] * 10 ** half:.6g}" if np.isfinite(half) else "nan", n_k,
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit: s* is an upper bound", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg272_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg272_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg272{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg272{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
