#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG274 -- implied-a0 points (or no-root / ill-conditioned markers) for the eight Amvrosiadis+25 sub-mm discs without an a0: ALESS 007.1, 022.1, 041.1, 049.1, 065.1, 066.1, 071.1, 075.1.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG274_amvrosiadis_eight_discs/FROZEN_CRITERIA.md (a7c4f7eef).
  model     CFG227's class-S rule: g_obs = V_circ(2 r_e)^2 / (2 r_e) (pressure included once); g_bar = one thin exponential disc (R_d = r_e / 1.678) of M* + M_gas at r = 2 r_e.
  estimator CFG223's median-residual s* (CFG229's a0implied), nu_mono, canonical a0; a root exists only if the row's median D > 1.
  STAGE=A   the blind pre-flight: the velocity columns are NOT loaded; no g_obs, D, delta or s* of any disc is formed.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_circ x 2); STAGE=B SELFTEST=1 (fabricated V on the law at s = 2).
Run: STAGE=A python3 .../cfg274_amvrosiadis_eight.py ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: every V_circ x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V on the law at s_true = 2 (+0.15 dex scatter); debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
IDS = ["007.1", "022.1", "041.1", "049.1", "065.1", "066.1", "071.1", "075.1"]
POOLS = {"P8": IDS, "P6": [i for i in IDS if i not in ("066.1", "075.1")]}
TEXT_FLAG = {"066.1": "text: poor SED, foreground quasar", "075.1": "text: poor SED"}
FOOT = {"049.1": "M*/L_IR/SFR da Cunha+15, gas Wardlow+18", "075.1": "M*/L_IR/SFR da Cunha+15, gas Wardlow+18"}
B_MC = 10000
VELO = ("vmax", "sigma", "vcirc", "mdyn")
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
PAR = os.path.join(AT, "amvrosiadis_parent.csv")
BST = os.path.join(AT, "amvrosiadis_bestfit.csv")
bcols = list(pd.read_csv(BST, nrows=0).columns)
use_b = bcols if STAGE == "B" else [c for c in bcols if not any(v in c for v in VELO)]
par = pd.read_csv(PAR, dtype={"alessid": str}).set_index("alessid")
bst = pd.read_csv(BST, usecols=use_b, dtype={"alessid": str}).set_index("alessid")
P(f"parent {os.path.basename(PAR)} sha256 {H.sha(PAR)}; best-fit {os.path.basename(BST)} sha256 {H.sha(BST)}; velocity columns loaded: {STAGE == 'B'}")

# ------------------------------------------------------------------ the inputs (baryon and geometry side)
G = {}
for i in IDS:
    p, b = par.loc[i], bst.loc[i]
    z = float(p["z"]); kpa = H.kpc_per_arcsec(z)
    Re = float(b["re_arcsec"]) * kpa
    beam_maj = float(str(p["beam_arcsec"]).split("x")[0])
    G[i] = dict(id=i, z=z, kpa=kpa, Re=Re, R=2 * Re, logMs=float(p["logMstar"]), eMs=0.5 * (float(p["logMstar_errhi"]) + float(p["logMstar_errlo"])), logMg=float(p["logMgas_msun"]), eMg=float(p["logMgas_err"]),
                snr=float(p["snr"]), co=str(p["co_transition"]), beam=beam_maj, incl=float(b["inc_deg"]), R_over_beam=2 * float(b["re_arcsec"]) / beam_maj)
    G[i]["Ms"] = 10 ** G[i]["logMs"]; G[i]["Mg"] = 10 ** G[i]["logMg"]
    if STAGE == "B":
        G[i].update(V=float(b["vcirc_2re_kms"]), eVhi=float(b["vcirc_2re_kms_errhi"]), eVlo=float(b["vcirc_2re_kms_errlo"]), sig=float(b["sigma_kms"]))


def gbar_of(g, Ms=None, Mg=None, star_fac=1.0, refac=1.0, sph=False, gas_fac=1.0, ts=0.0, tg=0.0):
    Ms = g["Ms"] if Ms is None else Ms
    Mg = g["Mg"] if Mg is None else Mg
    f = H.gsph if sph else H.gdisc
    Re = g["Re"] * refac
    return f(Ms * 10 ** ts, Re * star_fac, g["R"]) + f(Mg * gas_fac * 10 ** tg, Re, g["R"])


for i in IDS:
    G[i]["GB"] = float(gbar_of(G[i])); G[i]["y"] = G[i]["GB"] / A0C; G[i]["nuy"] = float(NU(np.array([G[i]["y"]]))[0])
P("rows: " + "; ".join(f"{i} z {G[i]['z']:.3f} R_e {G[i]['Re']:.2f} kpc log M* {G[i]['logMs']:.2f} log Mgas {G[i]['logMg']:.2f} SNR {G[i]['snr']:.1f} i {G[i]['incl']:.0f} 2r_e/beam {G[i]['R_over_beam']:.2f}" for i in IDS))

# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE BLIND PRE-FLIGHT (the velocity columns are not loaded; no g_obs, D, delta or s* of any disc is formed)")
    check("C1 CONTROL: the eight rows exist with the stated ids, finite z, baryon and geometry inputs, and the CSV hashes are printed above",
          f"{len(IDS)} rows; z {[G[i]['z'] for i in IDS]}", all(np.isfinite([G[i][k] for k in ('z', 'Re', 'logMs', 'logMg', 'eMs', 'eMg', 'snr', 'incl')]).all() for i in IDS) and len(IDS) == 8)
    # ---- C2: the disc function
    yy = np.linspace(0.05, 40, 400000)
    hh = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy)
    peak = float(np.max(2 * yy ** 2 * hh))                                     # v^2 Rd/(GM) = 2 y^2 [...]
    M1, Re1, Rr1 = 1e11, 3.0, 150.0
    farr = float(H.gdisc(M1, Re1, Rr1) / (H.G_KPC * M1 / Rr1 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read()
    seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}
    exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr.uniform(9, 12.5), rr.uniform(0.5, 8), rr.uniform(1, 20)
        dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, and gdisc equals CFG229's on 200 random inputs to 1e-12",
          f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation from CFG229's gdisc {dmax:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12)
    # ---- C3: g_bar parity with CFG227's committed S1 g_bar (only the deviation is printed)
    pts = list(csv.DictReader(open(os.path.join(CFG, "CFG227_rar_z2_5", "cfg227_points.csv"))))
    s1 = {r["id"]: float(r["g_bar"]) for r in pts if r["set"] == "S1 Amvrosiadis"}
    s1s = {r["id"]: r["g_bar"] for r in pts if r["set"] == "S1 Amvrosiadis"}
    dev3 = max(abs(G[i]["GB"] / s1[i] - 1) for i in IDS)
    same3 = all(f"{G[i]['GB']:.4e}" == s1s[i] for i in IDS)
    check("C3 CONTROL (restated by Addendum 1): every g_bar formatted %.4e equals CFG227's printed five-significant-digit string, and the relative deviation is at most 5.1e-5 (only g_bar is read from that file)",
          f"exact string match for {sum(f'{G[i][chr(71)+chr(66)]:.4e}' == s1s[i] for i in IDS)} of 8; max relative deviation {dev3:.1e} (the file's rounding)", same3 and dev3 < 5.1e-5)
    # ---- C4: estimator identity against CFG223's original
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read()
    seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}
    exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C4 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    # ---- C5: noiseless identity
    d5 = 0.0
    for i in IDS:
        for st in (0.5, 1.0, 2.5):
            D = NU(np.array([G[i]["GB"] / (A0C * st)]))
            ls, unb = H.s_star(D, np.array([G[i]["GB"]]))
            d5 = max(d5, abs(ls - math.log10(st)) if not unb else 9.0)
    check("C5 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on every galaxy's baryon side", f"max |d log10 s| {d5:.1e}", d5 < 1e-6)
    # ---- A1 baryon-side table
    P("\nA1  BARYON SIDE (noiseless world: D = nu_mono(y), y = g_bar(2 r_e) / a0; lever = d log10 s* / d(baryon dex); ILL-CONDITIONED iff |lever| >= 10)")
    ILL, LEV = {}, {}
    for i in IDS:
        g = G[i]
        lv, fl = H.lever1(np.array([g["nuy"]]), np.array([g["GB"]]))
        LEV[i] = lv; ILL[i] = bool(fl or abs(lv) >= 10)
        P(f"    {i}: g_bar {g['GB']:.3e} m/s^2  y {g['y']:.1f}  nu_mono(y) {g['nuy']:.4f}  lever {lv:+.1f}{' (flag)' if fl else ''}  {'ILL-CONDITIONED' if ILL[i] else 'conditioned'}  2r_e/beam {g['R_over_beam']:.2f}  SNR {g['snr']:.1f}")
    # ---- C6 coverage (declared fractional V error 0.10; the published V errors are not loaded at stage A)
    P("\nC6 / A2  COVERAGE AND PRECISION FORECAST (noiseless world on each galaxy's baryons; declared fractional V error 0.10 on V, i.e. 0.087 dex on g_obs; published M* and gas errors; 300 mock datasets, B = 1,000)")
    rng6 = np.random.default_rng(274)
    COV, PREC = {}, {}
    for i in IDS:
        g = G[i]; c68 = c95 = nd = 0; sds = []
        sM, sG = g["eMs"], g["eMg"]
        for it in range(300):
            Ms_o = g["Ms"] * 10 ** rng6.normal(0, sM); Mg_o = g["Mg"] * 10 ** rng6.normal(0, sG)           # the 'observed' baryons
            gob_true = g["GB"] * float(NU(np.array([g["GB"] / A0C]))[0])
            god = gob_true * (1 + 0.10 * rng6.normal()) ** 2                                             # the 'observed' g_obs (V error 0.10)
            gobm = god * (1 + 0.10 * rng6.normal(size=1000)) ** 2                                         # Monte Carlo around the observed values
            Msd = Ms_o * 10 ** rng6.normal(0, sM, 1000); Mgd = Mg_o * 10 ** rng6.normal(0, sG, 1000)
            gbd = H.gdisc(Msd, g["Re"], g["R"]) + H.gdisc(Mgd, g["Re"], g["R"])
            lsd, ud = H.AI.implied((gobm / gbd)[:, None], gbd[:, None], NU, A0C)
            q, fr = H.rooted_pct(lsd, ud)
            if np.isfinite(q[0]):
                nd += 1; c68 += (q[1] <= 0.0 <= q[3]); c95 += (q[0] <= 0.0 <= q[4]); sds.append(0.5 * (q[3] - q[1]))
        COV[i] = (c68 / max(nd, 1), c95 / max(nd, 1), nd); PREC[i] = float(np.median(sds)) if sds else float("nan")
        P(f"    {i}: coverage 68 % {COV[i][0]:.2f}, 95 % {COV[i][1]:.2f} (mocks with a rooted interval {nd} of 300); median 68 % half-width {PREC[i]:.2f} dex")
    ok6 = all(COV[i][0] >= 0.60 and COV[i][1] >= 0.88 for i in IDS if not ILL[i]) if any(not ILL[i] for i in IDS) else True
    check("C6 (reported; load-bearing only for the conditioned rows): the Monte Carlo interval covers the truth in >= 60 % (68 %) and >= 88 % (95 %) of the mocks for every conditioned row", "; ".join(f"{i} {COV[i][0]:.2f}/{COV[i][1]:.2f}" for i in IDS)
          + ("" if any(not ILL[i] for i in IDS) else "  (no conditioned row: not applicable)"), ok6, load_bearing=any(not ILL[i] for i in IDS))
    # ---- A3 knob effects on g_bar (baryon side only)
    P("\nA3  KNOB EFFECTS ON g_bar (baryon side only; dex relative to the headline g_bar)")
    KB = {}
    for i in IDS:
        g = G[i]; g0 = g["GB"]
        KB[i] = {"stars 2R_e": gbar_of(g, star_fac=2.0), "R_e x1.5": gbar_of(g, refac=1.5), "R_e /1.5": gbar_of(g, refac=1 / 1.5), "spherical": gbar_of(g, sph=True), "helium x1.36": gbar_of(g, gas_fac=1.36)}
        KB[i] = {k: math.log10(float(v) / g0) for k, v in KB[i].items()}
        P(f"    {i}: " + "; ".join(f"{k} {v:+.3f}" for k, v in KB[i].items()))
    P("\nA4  POOLED-ROW FORECAST: median y of P8 = %.1f, of P6 = %.1f" % (np.median([G[i]["y"] for i in POOLS["P8"]]), np.median([G[i]["y"] for i in POOLS["P6"]])))
    # ---- decisions and hand estimates
    pfd1 = all(ok for n, ok, lb in CHK if lb and not n.startswith("C6"))
    n_ill = sum(ILL.values())
    P("\nDECISIONS (the frozen map)")
    P(f"  PF-D1 ESTIMATOR VALIDATED: {pfd1} (controls C1-C5)")
    P(f"  PF-D2 ILL-CONDITIONED rows ({n_ill} of 8): " + ", ".join(i for i in IDS if ILL[i]) + "; conditioned: " + (", ".join(i for i in IDS if not ILL[i]) or "none"))
    P("  PF-D3 DRAWABLE as an a0 point: " + (", ".join(i for i in IDS if pfd1 and not ILL[i]) or "none") + "; every other row is a marker (floor triangle if it has no root, labelled open symbol otherwise), never a measurement")
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9) scored (HE4-HE8 are scored at stage B):")
    he = {}
    ys = {i: G[i]["y"] for i in IDS}
    he["HE1"] = sum(ys[i] >= 5 for i in IDS) >= 6 and all(ys[i] >= 10 for i in ("007.1", "022.1", "066.1", "071.1")) and all(LEV[i] < -10 for i in ("007.1", "022.1", "066.1", "071.1")) \
        and set(sorted(IDS, key=lambda k: abs(LEV[k]))[:2]) == {"049.1", "065.1"}
    he["HE2"] = 4 <= n_ill <= 8 and sum((not ILL[i]) for i in IDS) <= 2
    he["HE3"] = all(PREC[i] < 0.3 for i in IDS if not ILL[i]) and all(PREC[i] > 1.0 for i in IDS if ILL[i])
    for k, v in he.items():
        P(f"    {k}: {'hit' if v else 'MISS (kept as it falls)'}")
    NUM.update(inputs={i: {k: G[i][k] for k in ("z", "Re", "R", "logMs", "logMg", "snr", "incl", "R_over_beam", "GB", "y", "nuy")} for i in IDS}, lever=LEV, ill=ILL, coverage={i: list(COV[i]) for i in IDS},
               precision=PREC, knob_gbar=KB, hand_estimates=he, pf=dict(PF_D1=bool(pfd1), n_ill=n_ill))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2740)
    if SELFTEST:
        for i in IDS:
            g = G[i]
            gob = g["GB"] * float(NU(np.array([g["GB"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15)
            g["V"] = math.sqrt(gob * g["R"] / H.G2SI); g["eVhi"] = g["eVlo"] = 0.10 * g["V"]; g["sig"] = 0.25 * g["V"]
        P("SELFTEST: V fabricated from the law at s_true = 2 on each galaxy's own baryons (+0.15 dex scatter on g_obs); the real velocities are not used")
    if MUTATE:
        for i in IDS:
            G[i]["V"] *= 2.0; G[i]["eVhi"] *= 2.0; G[i]["eVlo"] *= 2.0
    for i in IDS:
        g = G[i]
        g["GO"] = g["V"] ** 2 / g["R"] * H.G2SI
        g["D"] = g["GO"] / g["GB"]
    RES = {}

    def solve(g, **kw):
        """s* of one galaxy under baryon-side variants (kw to gbar_of) and velocity variants (vmode)."""
        vm = kw.pop("vmode", "pub"); nu = kw.pop("nu", NU)
        V2 = {"pub": g["V"] ** 2, "P-": max(g["V"] ** 2 - 3.36 * g["sig"] ** 2, 1.0), "P+": g["V"] ** 2 + 3.36 * g["sig"] ** 2}[vm]
        go = V2 / g["R"] * H.G2SI
        gb = float(gbar_of(g, **kw))
        return H.s_star(np.array([go / gb]), np.array([gb]), nu), go, gb

    KNOBS = [("stars at 2 R_e", dict(star_fac=2.0)), ("R_e x1.5", dict(refac=1.5)), ("R_e /1.5", dict(refac=1 / 1.5)), ("spherical", dict(sph=True)), ("pressure P-", dict(vmode="P-")),
             ("pressure P+ (double count)", dict(vmode="P+")), ("helium x1.36", dict(gas_fac=1.36)), ("kernel P2", dict(nu=NUP2))]
    KGROUP = {"stars at 2 R_e": "geometry", "R_e x1.5": "geometry", "R_e /1.5": "geometry", "spherical": "geometry", "pressure P-": "pressure", "pressure P+ (double count)": "pressure", "helium x1.36": "helium", "kernel P2": "kernel"}
    for i in IDS:
        g = G[i]; lab = i
        (ls0, u0), go0, gb0 = solve(g)
        D0 = np.array([g["D"]]); GB0 = np.array([g["GB"]])
        rng = np.random.default_rng(zlib.crc32(("274|" + lab).encode()) % 100000)
        Vd = H.split_normal(rng, g["V"], g["eVhi"], g["eVlo"], B_MC)
        Msd = g["Ms"] * 10 ** rng.normal(0, g["eMs"], B_MC); Mgd = g["Mg"] * 10 ** rng.normal(0, g["eMg"], B_MC)
        god = Vd ** 2 / g["R"] * H.G2SI
        gbd = H.gdisc(Msd, g["Re"], g["R"]) + H.gdisc(Mgd, g["Re"], g["R"])
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C)
        q, frn = H.rooted_pct(lsd, ud)
        dFd = np.log10(god / (gbd * NU(gbd / A0C)))
        dF0 = float(np.log10(go0 / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        bands = H.band_solutions(g["D"], g["GB"])
        gas_b = {s_: H.s_star(np.array([go0 / float(gbar_of(g, tg=s_))]), np.array([float(gbar_of(g, tg=s_))])) for s_ in (-0.671, -0.213, 0.213, 0.671)}
        star_b = {s_: H.s_star(np.array([go0 / float(gbar_of(g, ts=s_))]), np.array([float(gbar_of(g, ts=s_))])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        kn = {}
        for nm, kw in KNOBS:
            (lk, uk), _, _ = solve(g, **dict(kw))
            kn[nm] = None if (u0 or uk) else lk - ls0
            kn[nm + "|root"] = (not uk)
        grp = {}
        for nm, _ in KNOBS:
            if kn[nm] is not None:
                grp.setdefault(KGROUP[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        n_root_knobs = sum(1 for nm, _ in KNOBS if kn[nm + "|root"])
        lv, lf = H.lever1(D0, GB0)                                                                  # the data lever (nan without a root)
        lv_nl, lf_nl = H.lever1(np.array([g["nuy"]]), np.array([g["GB"]]))                          # the noiseless-world (baryon-side) lever of the frozen rule
        dflo = H.delta_floor(D0); d1 = H.shift_to_s1(D0, GB0)
        RES[lab] = dict(id=i, z=g["z"], n=1, V=g["V"], GO=g["GO"], GB=g["GB"], D=g["D"], y=g["y"], ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=q, frac_mc_noroot=frn, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1],
                        bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, gas_bands={f"{k:+.3f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in gas_b.items()},
                        star_bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in star_b.items()}, knobs=kn, recipe_half=half, n_knobs_with_root=n_root_knobs, lever=lv_nl, lever_data=lv, delta_floor=dflo, delta_to_s1=d1,
                        ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)))
        R_ = RES[lab]
        P(f"  {i}: z {g['z']:.3f}  g_obs {g['GO']:.3e}  g_bar {g['GB']:.3e}  D {g['D']:.3f}  delta_FLAT {dF0:+.3f} [{dq[0]:+.3f}, {dq[1]:+.3f}]  y {g['y']:.1f}  "
          + ("NO ROOT" if u0 else f"s* = {10 ** ls0:.3g} (a0 = {10 ** ls0 * 0.93603:.3g}e-10)") + f"  MC rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.3g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.3g}] (draws without a root {frn:.2f})")
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"      baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}]{' (no-root corner)' if b15[2] else ''}  +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]{' (no-root corner)' if b30[2] else ''};  Delta_floor {dflo:+.3f} dex; baryon shift for s* = 1: {d1:+.3f}; lever {lv:+.1f}; knobs with a root {n_root_knobs}/{len(KNOBS)}; recipe half-width {half:.3f}; noiseless-world lever {lv_nl:+.1f}{' (ILL-CONDITIONED)' if R_['ill'] else ''}")
        P("      knobs (Delta log10 s*; -- = no root): " + "; ".join(f"{nm} " + ("--" if kn[nm] is None else f"{kn[nm]:+.3f}") + ("" if kn[nm + '|root'] else " (variant has no root)") for nm, _ in KNOBS))
    # ---- pooled rows
    for pn, members in POOLS.items():
        D = np.array([G[i]["D"] for i in members]); GB = np.array([G[i]["GB"] for i in members]); zm = float(np.median([G[i]["z"] for i in members]))
        ls0, u0 = H.s_star(D, GB)
        rng = np.random.default_rng(zlib.crc32(("274|" + pn).encode()) % 100000)
        ib = rng.integers(0, len(members), size=(B_MC, len(members)))
        lsb, ub = H.AI.implied(D[ib], GB[ib], NU, A0C)
        q, frn = H.rooted_pct(lsb, ub)
        bands = H.band_solutions(D, GB)
        kn = {}
        for nm, kw in KNOBS:
            kw = dict(kw); vm = kw.pop("vmode", "pub"); nu = kw.pop("nu", NU)
            gos, gbs = [], []
            for i in members:
                g = G[i]
                V2 = {"pub": g["V"] ** 2, "P-": max(g["V"] ** 2 - 3.36 * g["sig"] ** 2, 1.0), "P+": g["V"] ** 2 + 3.36 * g["sig"] ** 2}[vm]
                gos.append(V2 / g["R"] * H.G2SI); gbs.append(float(gbar_of(g, **kw)))
            lk, uk = H.s_star(np.array(gos) / np.array(gbs), np.array(gbs), nu)
            kn[nm] = None if (u0 or uk) else lk - ls0
        grp = {}
        for nm, _ in KNOBS:
            if kn[nm] is not None: grp.setdefault(KGROUP[nm], []).append(abs(kn[nm]))
        half = math.sqrt(sum(max(v) ** 2 for v in grp.values())) if grp else float("nan")
        RES[pn] = dict(id=pn, z=zm, n=len(members), members=members, ls=ls0, no_root=u0, s=H.s_val(ls0, u0), q=q, frac_mc_noroot=frn, median_D=float(np.median(D)), delta_floor=H.delta_floor(D),
                       bands={f"{k:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k, v in bands.items()}, knobs=kn, recipe_half=half, delta_to_s1=H.shift_to_s1(D, GB), lever=H.lever1(D, GB)[0])
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"  {pn} (n {len(members)}, z_med {zm:.3f}): median D {np.median(D):.3f}  " + ("NO ROOT" if u0 else f"s* = {10 ** ls0:.3g}") + f"  bootstrap rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.3g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.3g}] (resamples without a root {frn:.2f});  baryon +-0.15 [{b15[0]:.3g}, {b15[1]:.3g}] +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; Delta_floor {np.log10(np.median(D)):+.3f}")
    # ---- cross-check ALESS 122.1 with CFG229's committed inputs
    if not MUTATE and not SELFTEST:
        st = pd.read_csv(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_inputs_static.csv")).set_index("gid").loc["ALESS_122.1"]
        kn_ = pd.read_csv(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_inputs_kin.csv")).set_index("gid").loc["ALESS_122.1"]
        c229 = json.load(open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score_results.json")))["IMPL"]["ALESS_122.1"]
        Ms_, Mg_ = float(st["Mstar"]), 10 ** float(st["logMgas_He"])
        Re_, R_ = float(st["Re_kpc"]), float(st["R_kpc"])
        go_ = float(kn_["V_pub"]) ** 2 / R_ * H.G2SI; gb_ = float(H.gdisc(Ms_, Re_, R_) + H.gdisc(Mg_, Re_, R_))
        lsx, ux = H.s_star(np.array([go_ / gb_]), np.array([gb_]))
        rng = np.random.default_rng(zlib.crc32(b"274|ALESS_122.1") % 100000)
        Vd = H.split_normal(rng, float(kn_["V_pub"]), float(kn_["eV_hi"]), float(kn_["eV_lo"]), B_MC)
        Msd = Ms_ * 10 ** rng.normal(0, float(st["e_logMstar_inner"]), B_MC); Mgd = Mg_ * 10 ** rng.normal(0, float(st["e_logMH2"]), B_MC)
        gbd = H.gdisc(Msd, Re_, R_) + H.gdisc(Mgd, Re_, R_)
        lsd, ud = H.AI.implied((Vd ** 2 / R_ * H.G2SI / gbd)[:, None], gbd[:, None], NU, A0C)
        qx, frx = H.rooted_pct(lsd, ud)
        dcen = abs(lsx - c229["s0"][0]); dq_ = max(abs(a - b) for a, b in zip(qx, c229["stat"]["q"]))
        RES["XCHECK_ALESS_122.1"] = dict(ls=lsx, no_root=ux, q=qx, frac_mc_noroot=frx, cfg229_ls=c229["s0"][0], cfg229_q=c229["stat"]["q"])
        check("M5 CROSS-CHECK: ALESS 122.1 through this lane's functions with CFG229's committed inputs reproduces CFG229's central s* to 1e-6 dex and its Monte Carlo quantiles to 0.05 dex",
              f"central log10 s* {lsx:.6f} vs {c229['s0'][0]:.6f} (|d| {dcen:.1e}); MC quantiles [2.5/16/50/84/97.5] " + "/".join(f"{v:.3f}" for v in qx) + " vs " + "/".join(f"{v:.3f}" for v in c229["stat"]["q"]) + f" (max |d| {dq_:.3f})", dcen < 1e-6 and dq_ < 0.05)
    NUM["rows"] = RES

    # ---------------------------------------------------------------- controls
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg274_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nroot_m = 0; nroot_0 = sum(1 for i in IDS if not main[i]["no_root"])
        def inv_nu(Dv):
            lo, hi = -25.0, 25.0
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
                else: hi = mid
            return math.exp(0.5 * (lo + hi))
        for i in IDS:
            R_ = RES[i]
            if not R_["no_root"]:
                nroot_m += 1
                ycl = inv_nu(R_["D"]); lscl = math.log10(R_["GB"] / ycl / A0C)
                bad = max(bad, abs(lscl - R_["ls"]))
        check("M2 MUTATE=1 (reactivity without needing a main-run root): every V_circ x 2; the rows with a root in the mutated run satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and their number is at least the main run's",
              f"rows with a root: mutated {nroot_m}, main {nroot_0}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and nroot_m >= nroot_0)
    else:
        d1m = 0.0
        for i in IDS:
            if RES[i]["no_root"]: continue
            la, ua = H.AI.implied(np.array([RES[i]["D"]]), np.array([RES[i]["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - RES[i]["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for i in IDS if not RES[i]['no_root'])} rows with a root)", d1m < 1e-9)
        check("M3 the pooled rows hold 8 and 6 members and P6 is a subset of P8", f"P8 {RES['P8']['n']}, P6 {RES['P6']['n']}", RES["P8"]["n"] == 8 and RES["P6"]["n"] == 6 and set(POOLS["P6"]) <= set(POOLS["P8"]))
        if SELFTEST:
            tested = [i for i in IDS if not RES[i]["ill"] and not RES[i]["no_root"]]
            if tested:
                okst = all(RES[i]["q"][0] <= math.log10(2.0) <= RES[i]["q"][4] for i in tested)
                check("SELFTEST: every conditioned row returns the fabricated truth inside its 95 % interval", "; ".join(f"{i} s* {RES[i]['s']:.3g}" for i in tested) + " (truth 2)", okst)
            else:
                P("  SELFTEST: every row is ILL-CONDITIONED (or has no root): the truth-recovery check is not applicable; intervals: " + "; ".join(f"{i} s* " + ("no root" if RES[i]["no_root"] else f"{RES[i]['s']:.3g}") for i in IDS))
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot",
                              "gas_in_lo", "gas_in_hi", "gas_out_lo", "gas_out_hi", "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for lab in IDS + list(POOLS):
        R_ = RES[lab]; pooled = lab in POOLS
        bands = {float(k): (v["ls"], v["unb"]) for k, v in R_["bands"].items()}
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        q = R_["q"]; lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (FLOOR, FLOOR); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (FLOOR, FLOOR)
        fl = H.flags_for(R_["z"], lo95, hi95, b15[:2], b30[:2], not R_["no_root"])
        if not pooled:
            gb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["gas_bands"].items()}; sb_ = {float(k): (v["ls"], v["unb"]) for k, v in R_["star_bands"].items()}
            gi = H.band_edges(gb_, -0.213, 0.213); go_ = H.band_edges(gb_, -0.671, 0.671); si = H.band_edges(sb_, -0.15, 0.15); so = H.band_edges(sb_, -0.30, 0.30)
            extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], gi[0], gi[1], go_[0], go_[1], si[0], si[1], so[0], so[1], R_["delta_floor"], R_["delta_to_s1"]]
            g = G[lab]
            q_ = ("ILL-CONDITIONED near-Newtonian (|lever| >= 10); " if R_["ill"] else "") + ("NO ROOT (D <= 1: baryons above the dynamics at 2 r_e)" if R_["no_root"] else "has a root: an ill-conditioned residual D - 1, not an a0 measurement" if R_["ill"] else "has a root") \
                + f"; SNR {g['snr']:.1f}; i {g['incl']:.0f}; 2 r_e/beam {g['R_over_beam']:.2f}" + (f"; {TEXT_FLAG[lab]}" if lab in TEXT_FLAG else "") + (f"; {FOOT[lab]}" if lab in FOOT else "")
        else:
            extra = [float("nan"), R_["lever"], 1, float("nan"), float("nan"), float("nan"), R_["median_D"], R_["frac_mc_noroot"]] + [float("nan")] * 8 + [R_["delta_floor"], R_["delta_to_s1"]]
            q_ = "pooled row (mixes z 2.26-4.45), never a headline; " + ("NO ROOT (median D <= 1)" if R_["no_root"] else "has a root")
        half = R_["recipe_half"]
        rows.append(["CFG274", f"Amvrosiadis ALESS {lab}" if not pooled else f"Amvrosiadis pooled {lab}", "S (CO only, alpha_CO 0.92)", f"{R_['z']:.4f}", f"{R_['z']:.4f}", int(R_["no_root"]), f"{R_['s']:.6g}", f"{R_['s'] * 0.93603:.6g}",
                     f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}", f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2],
                     f"{half:.4f}", f"{R_['s'] * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{R_['s'] * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_.get("n_knobs_with_root", ""), *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra],
                     fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg274_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg274_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg274{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg274{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
