#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG283 -- ALPAKA 24 (ADF22.5, z = 3.094) with gas-only baryons: B1 = a gas floor (alpha_CO,min = 0.8, r_J1 = 1; a LOWER limit, the headline) and B2 = the Galactic conversion (alpha_CO = 4.36, r_J1 = 1; sensitivity). No stellar mass exists.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG283_alpaka24_gas_only/FROZEN_CRITERIA.md (e46390c14).
  STAGE=A   the engineering pre-flight: no velocity column is loaded; every number it prints was seen in the criteria's section 0.3 (it is NOT blind).
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_ext, sigma_ext x 2); STAGE=B SELFTEST=1 (fabricated V_ext on the law at s = 2; the real velocities are never loaded).
Points file: no_root = 1 only for a FLOOR; a CEILING (D > 1 but s* > 1000) is written s_star = 1000, no_root = 0, status = ceiling (CFG277's convention).
Run: STAGE=A python3 .../cfg283_alpaka24.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
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
P(f"\nSTAGE {STAGE}" + ("  *** MUTATE=1: V_ext and sigma_ext x 2 (g_obs x 4) ***" if MUTATE else "") + ("  *** SELFTEST: FABRICATED V_ext on the law at s_true = 2 (+0.15 dex scatter); the real velocities are never loaded; debugging only ***" if SELFTEST else ""))

A0C, A0A, FLOOR, NU, NUP2 = H.A0C, H.A0A, H.FLOOR, H.NU, H.NUP2
ID = 24
B_MC = 10000
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
dirs = {"samp": "alpaka1_sample.csv", "prop": "alpaka1_properties.csv", "geo": "alpaka1_geometry.csv", "obs": "alpaka1_alma_obs.csv"}
T = {k: pd.read_csv(os.path.join(AT, v)).set_index("id") for k, v in dirs.items()}
OUTER = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"), usecols=["id", "z", "n_rings", "R_ext_arcsec", "R_ext_kpc", "Re_kpc_dashed_line"]).set_index("id")   # no velocity-bearing column
RING = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"), usecols=["id", "ring", "panel", "R_kpc"])
KINP = os.path.join(AT, "alpaka1_kinematics.csv")
P("sha256: " + ", ".join(f"{v} {H.sha(os.path.join(AT, v))}" for v in dirs.values()) + f", alpaka1_outer_summary.csv {H.sha(os.path.join(AT, 'alpaka1_digitised', 'alpaka1_outer_summary.csv'))}; velocity columns loaded: {STAGE == 'B' and not SELFTEST}")
KIN = pd.read_csv(KINP).set_index("id") if (STAGE == "B" and not SELFTEST) else None

s, p, ge, ob, ou = T["samp"].loc[ID], T["prop"].loc[ID], T["geo"].loc[ID], T["obs"].loc[ID], OUTER.loc[ID]
Z = float(s["z"]); NAME = str(s["name"])
LP = float(p["lprime_1e10_kkmspc2"]) * 1e10; ELP = float(p["e_lprime"]) * 1e10; SIGL = ELP / LP / math.log(10)
ILINE, EILINE = float(p["iline_jykms"]), float(p["e_iline"])
I_AD = float(ge["i_alma"]); E_I = 0.5 * (float(ge["e1.3"]) + float(ge["e2.3"]))
R_EXT = float(ou["R_ext_kpc"]); R_EXT_AS = float(ou["R_ext_arcsec"]); KPA = R_EXT / R_EXT_AS
RE_DASH = float(ou["Re_kpc_dashed_line"]); RE = RE_DASH if np.isfinite(RE_DASH) else R_EXT / 1.2
rr = RING[(RING["id"] == ID) & (RING["panel"] == "V")].sort_values("ring"); R_MEAN = float(rr["R_kpc"].iloc[-2:].mean())
BEAM_MAJ, BEAM_MIN = float(ob["beam_major_arcsec"]), float(ob["beam_minor_arcsec"])
MSTAR = float(p["mstar_1e10msun"])
ALPHA = {"B1": 0.8, "B2": 4.36}                                                            # frozen in CFG272 (B1 a lower limit, B2 the Galactic conversion), r_J1 = 1 for both
ROUTES = ["B1", "B2"]
LABEL = {"B1": f"ALPAKA 24 {NAME} [gas floor]", "B2": f"ALPAKA 24 {NAME} [gas Galactic]"}
GCL = {"B1": "L (line L' only; alpha_CO frozen as a lower limit)", "B2": "L (line L' only; alpha_CO 4.36 Galactic, r_J1 = 1; sensitivity)"}
if STAGE == "B" and not SELFTEST:
    k = KIN.loc[ID]
    VEXT, EVHI, EVLO, SIG = float(k["vext_kms"]), float(k["vext_errhi"]), float(k["vext_errlo"]), float(k["sigma_ext_kms"])
P(f"row: ID {ID} {NAME} z {Z:.3f}  L' {LP:.3e} +- {ELP:.2e} ({SIGL:.4f} dex)  R_ext {R_EXT:.3f} kpc ({R_EXT_AS:.4f} arcsec, {KPA:.3f} kpc/arcsec)  R_e {RE:.3f} kpc ({'dashed line' if np.isfinite(RE_DASH) else 'R_ext/1.2, assumed'})  i_ALMA {I_AD:.0f} +- {E_I:.0f}  M* {MSTAR}  beam {BEAM_MAJ:.2f} x {BEAM_MIN:.2f} arcsec = {BEAM_MAJ * KPA:.2f} x {BEAM_MIN * KPA:.2f} kpc")


def gobs_gbar(route="B1", vm="pub", inc="adopt", rad="ext", refac=1.0, sph=False, gas_fac=1.0, tg=0.0, V=None, SG=None, Lp=None, stars=0.0):
    """g_obs and g_bar [m s^-2] of the gas disc under a route (B1 / B2) and a knob setting; `stars` is an ASSUMED stellar mass added to the same disc (only the M* ladder uses it)."""
    R = R_EXT if rad == "ext" else R_MEAN
    Mg = ALPHA[route] * (LP if Lp is None else Lp) * gas_fac
    f = H.gsph if sph else H.gdisc
    gb = f(Mg * 10 ** tg, RE * refac, R) + (f(stars, RE * refac, R) if stars > 0 else 0.0)
    go = None
    if STAGE == "B":
        sg = SIG if SG is None else SG
        V2 = (VEXT if V is None else V) ** 2 + {"pub": 0.0, "a168": 1.68 * sg ** 2, "a336": 3.36 * sg ** 2}[vm]
        i_new = {"adopt": I_AD, "lo": max(5.0, I_AD - E_I), "hi": min(85.0, I_AD + E_I)}[inc]
        go = V2 * (math.sin(math.radians(I_AD)) / math.sin(math.radians(i_new))) ** 2 / R * H.G2SI
    return go, gb


GB = {r: float(gobs_gbar(r)[1]) for r in ROUTES}
Y = {r: GB[r] / A0C for r in ROUTES}
NUY = {r: float(NU(np.array([Y[r]]))[0]) for r in ROUTES}
P(f"baryon side: " + "; ".join(f"{r}: alpha_CO {ALPHA[r]} M_gas {ALPHA[r] * LP:.3e} g_bar {GB[r]:.4e} y {Y[r]:.3f} nu(y) {NUY[r]:.4f}" for r in ROUTES))

KNOB_LIST = [("R_e x1.5", dict(refac=1.5)), ("R_e /1.5", dict(refac=1 / 1.5)), ("spherical", dict(sph=True)), ("pressure +1.68 sigma^2", dict(vm="a168")), ("pressure +3.36 sigma^2", dict(vm="a336")),
             ("inclination -1 sigma", dict(inc="lo")), ("inclination +1 sigma", dict(inc="hi")), ("V_ext at R_mean of the last two rings", dict(rad="mean")), ("kernel P2", dict(nu=NUP2)),
             ("gas: r_31 = 0.6 (gas x 1/0.6)", dict(gas_fac=1 / 0.6)), ("gas: helium x 1.36", dict(gas_fac=1.36))]
KGROUP = {"R_e x1.5": "geometry", "R_e /1.5": "geometry", "spherical": "geometry", "pressure +1.68 sigma^2": "pressure", "pressure +3.36 sigma^2": "pressure", "inclination -1 sigma": "inclination", "inclination +1 sigma": "inclination",
          "V_ext at R_mean of the last two rings": "radius", "kernel P2": "kernel", "gas: r_31 = 0.6 (gas x 1/0.6)": "gas conversion", "gas: helium x 1.36": "gas conversion"}


def dl_mpc(z, H0=67.4, Om=H.OM):
    zz = np.linspace(0.0, z, 20001); f = 1.0 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om)
    return 299792.458 / H0 * float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(zz))) * (1 + z)


def inv_nu(Dv):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
        else: hi = mid
    return math.exp(0.5 * (lo + hi))


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE ENGINEERING PRE-FLIGHT (no velocity column is loaded; not blind: every number below was seen in the criteria's section 0.3)")
    check("C1 CONTROL: the ID 24 row exists with finite z, L', e_L', R_ext, inclination and its error; M* is empty; R_e is the assumed R_ext/1.2; the CSV hashes are printed above",
          f"z {Z}; L' {LP:.2e} +- {ELP:.1e}; R_ext {R_EXT:.3f}; i {I_AD:.0f} +- {E_I:.0f}; M* {MSTAR}; R_e {RE:.3f} (assumed {not np.isfinite(RE_DASH)})",
          all(np.isfinite([Z, LP, ELP, R_EXT, I_AD, E_I])) and not np.isfinite(MSTAR) and not np.isfinite(RE_DASH) and abs(RE - R_EXT / 1.2) < 1e-12)
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
    src223 = open(os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")).read(); seg = src223[src223.index("LO_LS, HI_LS, NIT"):src223.index("_IDX = {}")]
    ns223 = {"np": np}; exec(compile(seg, "cfg223_a0_over_time.py", "exec"), ns223)
    rr_ = np.random.default_rng(1234); same = True
    for _ in range(200):
        Dq = 10 ** rr_.uniform(-0.3, 0.9, size=(5, 7)); gq = 10 ** rr_.uniform(-11, -8, size=(5, 7))
        a1, u1 = ns223["implied"](Dq, gq, NU, A0C); a2, u2 = H.AI.implied(Dq, gq, NU, A0C)
        same = same and np.array_equal(a1, a2) and np.array_equal(u1, u2)
    check("C3 CONTROL: the imported estimator equals CFG223's original bit for bit on 200 random sets", f"identical {same}", bool(same))
    d4 = 0.0
    for st_ in (0.5, 1.0, 2.5):
        ls, unb = H.s_star(NU(np.array([GB["B1"] / (A0C * st_)])), np.array([GB["B1"]])); d4 = max(d4, abs(ls - math.log10(st_)) if not unb else 9.0)
    check("C4 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on the B1 baryons", f"max |d log10 s| {d4:.1e}", d4 < 1e-6)
    r272 = json.load(open(os.path.join(CFG, "CFG272_alpaka_five_discs", "cfg272_stageB_results.json")))["numbers"]["rows"]["24"]
    d5 = max(abs(GB["B1"] / r272["GB_B1"] - 1), abs(GB["B2"] / r272["GB_B2"] - 1))
    check("C5 CONTROL: the B1 and B2 g_bar equal CFG272's committed GB_B1 and GB_B2 to 1e-9 relative (only the baryon values are used at stage A)", f"relative deviation {d5:.1e} (B1 {GB['B1']:.6e} vs {r272['GB_B1']:.6e}; B2 {GB['B2']:.6e} vs {r272['GB_B2']:.6e})", d5 < 1e-9)
    nuo = 345.79599 / (1 + Z); DL = dl_mpc(Z); Lcalc = 3.25e7 * ILINE * nuo ** -2 * DL ** 2 * (1 + Z) ** -3
    check("C6 CONTROL (load-bearing: the gas mass is the only baryon): the tabulated L' equals the line-flux formula L' = 3.25e7 S dv nu_obs^-2 D_L^2 (1+z)^-3 (flat LCDM 67.4 / 0.315) to 5 %",
          f"S dv = {ILINE} +- {EILINE} Jy km/s ({ILINE / EILINE:.1f} sigma); nu_obs {nuo:.3f} GHz; D_L {DL:.1f} Mpc; formula {Lcalc:.3e} vs table {LP:.3e} ({Lcalc / LP - 1:+.3f})", abs(Lcalc / LP - 1) < 0.05)
    P("\nA1  BARYON SIDE AND THE CFG240 READING (noiseless world; lever = d log10 s* / d(baryon dex); ILL-CONDITIONED iff |lever| >= 10 or not computable; CFG240 T3: nu -> 1 at large y removes the a0 dependence)")
    ILL, LEV = {}, {}
    for r in ROUTES:
        lv, fl = H.lever1(np.array([NUY[r]]), np.array([GB[r]])); LEV[r] = lv; ILL[r] = bool(fl or abs(lv) >= 10)
        P(f"    {r} (alpha_CO {ALPHA[r]}): M_gas {ALPHA[r] * LP:.3e}  g_bar {GB[r]:.3e}  y {Y[r]:.3f}  nu(y) {NUY[r]:.4f}  lever {lv:+.2f}{' (flag: a +-0.03 dex baryon move removes the noiseless root)' if fl else ''}  {'ILL-CONDITIONED' if ILL[r] else 'conditioned'}   one radius (R_ext): no deep point")
    P("\nA2  KNOB EFFECTS ON g_bar (dex relative to B1; baryon side only)")
    for nm, kw in KNOB_LIST:
        if "inclination" in nm or "pressure" in nm or nm == "kernel P2": continue
        kk = {k_: v_ for k_, v_ in kw.items() if k_ != "nu"}
        gk = float(gobs_gbar("B1", **kk)[1]); P(f"    {nm}: g_bar {math.log10(gk / GB['B1']):+.3f} dex")
    P(f"\nA3  M_gas(B2) / M_gas(B1) = {ALPHA['B2'] / ALPHA['B1']:.3f} ({math.log10(ALPHA['B2'] / ALPHA['B1']):+.3f} dex); beam {BEAM_MAJ:.2f} x {BEAM_MIN:.2f} arcsec = {BEAM_MAJ * KPA:.2f} x {BEAM_MIN * KPA:.2f} kpc against R_ext {R_EXT:.2f} kpc ({R_EXT / (BEAM_MAJ * KPA):.1f} beams); R_e assumed {RE:.3f} kpc")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR AND BARYON SIDE VALIDATED: {pfd1} (controls C1-C6)")
    he = {"HE10": bool(pfd1 and abs(Y["B1"] - 2.203) < 0.01 and abs(Y["B2"] - 12.005) < 0.01 and abs(LEV["B1"] + 3.747) < 0.02 and ILL["B2"] and not ILL["B1"])}
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE1-HE9 are scored at stage B):")
    P(f"    HE10: C1-C6 pass; y(B1) 2.203, y(B2) 12.005, B1 lever -3.75 conditioned, B2 not computable (ILL) reproduced: {'hit' if he['HE10'] else 'MISS (kept as it falls)'}")
    NUM.update(inputs=dict(z=Z, Lp=LP, eLp=ELP, R_ext=R_EXT, Re=RE, R_mean=R_MEAN, i=I_AD, ei=E_I, GB=GB, y=Y, nuy=NUY, Lcalc=Lcalc, DL=DL), lever=LEV, ill=ILL, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_ext and sigma_ext x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2830)
    if SELFTEST:
        gob = GB["B1"] * float(NU(np.array([GB["B1"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15)
        VEXT = math.sqrt(gob * R_EXT / H.G2SI); EVHI = EVLO = 0.10 * VEXT; SIG = 0.10 * VEXT
        P("SELFTEST: V_ext fabricated from the law at s_true = 2 on the B1 baryons (+0.15 dex scatter on g_obs); the real velocities are not used")
    if MUTATE:
        VEXT *= 2.0; EVHI *= 2.0; EVLO *= 2.0; SIG *= 2.0
    RES = {}

    def solve(route, **kw):
        kw = dict(kw); nu = kw.pop("nu", NU)
        go, gb = gobs_gbar(route, **kw)
        ls, st = H.s_status(np.array([go / gb]), np.array([gb]), nu)
        return ls, st, float(go), float(gb)

    def mc_draws(rng, Vc, eh, el, n):
        Vd = H.split_normal(rng, Vc, eh, el, n)
        ii = rng.normal(I_AD, E_I, n)
        for _ in range(60):
            bad = (ii < 5) | (ii > 85)
            if not bad.any(): break
            ii[bad] = rng.normal(I_AD, E_I, int(bad.sum()))
        facd = (math.sin(math.radians(I_AD)) / np.sin(np.radians(ii))) ** 2
        Lpd = LP * 10 ** rng.normal(0, SIGL, n)
        return Vd ** 2 / R_EXT * H.G2SI * facd, Lpd

    for r in ROUTES:
        lab = LABEL[r]
        ls0, st0, go0, gb0 = solve(r); D0 = go0 / gb0
        rng = np.random.default_rng(zlib.crc32(("283|" + lab).encode()) % 100000)
        god, Lpd = mc_draws(rng, VEXT, EVHI, EVLO, B_MC)
        gbd = H.gdisc(ALPHA[r] * Lpd, RE, R_EXT)
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
        Dd = god / gbd
        frac_floor = float(np.mean(ud & (Dd <= 1.0))); frac_ceiling = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(go0 / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        bands = H.band_solutions(np.array([D0]), np.array([gb0]))
        gas_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(r, tg=s_)[1])]), np.array([float(gobs_gbar(r, tg=s_)[1])])) for s_ in (-0.671, -0.213, 0.213, 0.671)}
        kn, kD, kst = {}, {}, {}
        for nm, kw in KNOB_LIST:
            lk, stk, gok, gbk = solve(r, **dict(kw))
            kn[nm] = None if (st0 != "root" or stk != "root") else lk - ls0; kst[nm] = stk; kD[nm] = math.log10((gok / gbk) / D0)
        grp = {}
        for nm, _ in KNOB_LIST:
            if kn[nm] is not None: grp.setdefault(KGROUP[nm], []).append(abs(kn[nm]))
        gmax = {g_: max(v) for g_, v in grp.items()}
        half = math.sqrt(sum(v ** 2 for v in gmax.values())) if gmax else float("nan")
        n_root = sum(1 for nm, _ in KNOB_LIST if kst[nm] == "root")
        lv_nl, lf_nl = H.lever1(np.array([NUY[r]]), np.array([GB[r]]))
        dflo = H.delta_floor(np.array([D0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        a_D1 = ALPHA[r] * D0; a_s1 = ALPHA[r] * 10 ** d1 if np.isfinite(d1) else float("nan")
        sval = H.s_val_status(ls0, st0)
        lo95 = 10 ** q[0] if np.isfinite(q[0]) else float("nan")
        vac = int(st0 == "ceiling" or (st0 == "root" and np.isfinite(lo95) and lo95 >= H.LAWS["H(z)"](Z)))
        RES[r] = dict(route=r, label=lab, alpha=ALPHA[r], z=Z, GO=go0, GB=gb0, D=D0, y=Y[r], ls=ls0, status=st0, s=sval, q=q, frac_mc_noroot=frn, frac_mc_floor=frac_floor, frac_mc_ceiling=frac_ceiling, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1],
                      bands={f"{k_:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in bands.items()}, gas_bands={f"{k_:+.3f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in gas_b.items()},
                      knobs=kn, knob_D_dex=kD, knob_status=kst, group_max=gmax, recipe_half=half, n_knobs_with_root=n_root, n_knobs=len(KNOB_LIST), lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)),
                      delta_floor=dflo, delta_to_s1=d1, alpha_D1=a_D1, alpha_s1=a_s1, vacuous=vac, M_gas=ALPHA[r] * LP)
        R_ = RES[r]
        P(f"  {lab}: z {Z:.3f}  g_obs {go0:.4e}  g_bar {gb0:.4e}  D {D0:.4f}  delta_FLAT {dF0:+.3f} [{dq[0]:+.3f}, {dq[1]:+.3f}]  y {Y[r]:.3f}  status {st0.upper()}" + (f"  s* <= {10 ** ls0:.4g} (a0 <= {10 ** ls0 * 0.93603:.4g}e-10)" if st0 == "root" else ""))
        P(f"      Monte Carlo (B = {B_MC}): draws without a root {frn:.3f} (floor {frac_floor:.3f}, ceiling {frac_ceiling:.3f}); rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.4g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.4g}]  95 % [{10 ** q[0] if np.isfinite(q[0]) else float('nan'):.4g}, {10 ** q[4] if np.isfinite(q[4]) else float('nan'):.4g}]  median {10 ** q[2] if np.isfinite(q[2]) else float('nan'):.4g}")
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        gbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["gas_bands"].items()}; gi = H.band_edges(gbn, -0.213, 0.213); go_ = H.band_edges(gbn, -0.671, 0.671)
        P(f"      bands: all baryons +-0.15 [{b15[0]:.4g}, {b15[1]:.4g}]{' (no-root corner)' if b15[2] else ''}  +-0.30 [{b30[0]:.4g}, {b30[1]:.4g}]{' (no-root corner)' if b30[2] else ''};  gas +-0.213 [{gi[0]:.4g}, {gi[1]:.4g}]{' (no-root corner)' if gi[2] else ''}  +-0.671 [{go_[0]:.4g}, {go_[1]:.4g}]{' (no-root corner)' if go_[2] else ''}")
        P(f"      Delta_floor {dflo:+.3f} dex; baryon shift for s* = 1: {d1:+.3f} dex; alpha_CO at D = 1: {a_D1:.3f}; alpha_CO at s* = 1: {a_s1:.3f}; lever (noiseless) {lv_nl:+.2f}{' ILL-CONDITIONED' if R_['ill'] else ' (conditioned)'}; knobs with a root {n_root}/{len(KNOB_LIST)}; recipe half-width {half:.3f}" + ("; VACUOUS (D2)" if vac else ""))
        P("      knobs (Delta log10 s*; -- = the base or the variant has no root; [status; Delta log10 D]): " + "; ".join(f"{nm} " + ("--" if kn[nm] is None else f"{kn[nm]:+.3f}") + f" [{kst[nm]}; {kD[nm]:+.3f}]" for nm, _ in KNOB_LIST))
        P("      knob groups (max |Delta log10 s*|): " + (", ".join(f"{g_} {v:.3f}" for g_, v in gmax.items()) if gmax else "none (no root at the base)"))
    # dynamics context and the M* ladder (main run only)
    MDYN = VEXT ** 2 * R_EXT / H.G_KPC
    P(f"\n  context: M_dyn(< R_ext) = V_ext^2 R_ext / G = {MDYN:.3e} Msun (a scale, not a baryon mass); M_gas B1 {RES['B1']['M_gas']:.3e}, B2 {RES['B2']['M_gas']:.3e}")
    NUM["context"] = dict(M_dyn=MDYN)
    if not MUTATE and not SELFTEST:
        R1 = RES["B1"]; go1, gb1 = R1["GO"], R1["GB"]
        gunit = float(H.gdisc(1.0, RE, R_EXT))                                                   # g per Msun of the same disc (linear in M)
        mfloor = (go1 - gb1) / gunit if go1 > gb1 else float("nan")
        mstar_s1 = R1["M_gas"] * (10 ** R1["delta_to_s1"] - 1) if np.isfinite(R1["delta_to_s1"]) and R1["delta_to_s1"] > 0 else float("nan")
        lad = []
        P("\n  M* LADDER (route 2 pre-computed; ASSUMED stellar masses added to the B1 gas in the same disc, g_obs as measured; NOT data)")
        for lm in (9.5, 10.0, 10.5, 10.8, 11.0):
            gbl = gb1 + float(H.gdisc(10 ** lm, RE, R_EXT)); Dl = go1 / gbl; lsl, stl = H.s_status(np.array([Dl]), np.array([gbl]))
            lad.append(dict(log_mstar=lm, g_bar=gbl, y=gbl / A0C, D=Dl, status=stl, s=H.s_val_status(lsl, stl)))
            P(f"    log M* {lm:5.2f}: g_bar {gbl:.4e} (y {gbl / A0C:.2f})  D {Dl:.3f}  {stl.upper()}" + (f"  s* <= {10 ** lsl:.3g}" if stl == "root" else ""))
        P(f"    log M* at D = 1 (the floor boundary): {math.log10(mfloor):.3f}" + f";  log M* at s* = 1 (closed form from the baryon shift): {math.log10(mstar_s1) if np.isfinite(mstar_s1) else float('nan'):.3f}")
        gbs1 = gb1 + float(H.gdisc(mstar_s1, RE, R_EXT)) if np.isfinite(mstar_s1) else float("nan")
        ls_chk = H.s_status(np.array([go1 / gbs1]), np.array([gbs1]))[0] if np.isfinite(gbs1) else float("nan")
        NUM["ladder"] = dict(rows=lad, log_mstar_at_D1=math.log10(mfloor), log_mstar_at_s1=math.log10(mstar_s1) if np.isfinite(mstar_s1) else None, s1_check_log10_s=ls_chk)
        check("M7 CONTROL: the stellar mass the closed form gives for s* = 1 returns s* = 1 to 0.02 dex when added to the B1 gas", f"log10 s* at log M* {math.log10(mstar_s1):.3f}: {ls_chk:+.4f}", np.isfinite(ls_chk) and abs(ls_chk) < 0.02)
    # ---------------------------------------------------------------- SELFTEST: 100 worlds on the law at s_true = 2 (B1 baryons)
    if SELFTEST:
        P("\n  SELFTEST (100 worlds): V_ext fabricated from the law at s_true = 2 on the B1 baryons, 0.15 dex scatter on g_obs, 10 % V errors; Monte Carlo B = 1,000 per world; the L' error is drawn as in the main run")
        rW = np.random.default_rng(28300); cnt = {"root": 0, "floor": 0, "ceiling": 0}; sroot, cover = [], 0
        for w in range(100):
            gobw = GB["B1"] * float(NU(np.array([GB["B1"] / (2.0 * A0C)]))[0]) * 10 ** rW.normal(0, 0.15)
            Vw = math.sqrt(gobw * R_EXT / H.G2SI)
            lsw, stw = H.s_status(np.array([gobw / GB["B1"]]), np.array([GB["B1"]])); cnt[stw] += 1
            if stw != "root": continue
            godw, Lpdw = mc_draws(rW, Vw, 0.10 * Vw, 0.10 * Vw, 1000); gbdw = H.gdisc(ALPHA["B1"] * Lpdw, RE, R_EXT)
            lsdw, udw = H.AI.implied((godw / gbdw)[:, None], gbdw[:, None], NU, A0C); qw, _ = H.rooted_pct(lsdw, udw)
            sroot.append(10 ** lsw)
            if np.isfinite(qw[0]) and qw[0] <= math.log10(2.0) <= qw[4]: cover += 1
        nroot = cnt["root"]
        P(f"    status of the fabricated worlds: root {cnt['root']}, floor {cnt['floor']}, ceiling {cnt['ceiling']}; of the {nroot} rooted worlds the 95 % interval contains s = 2 in {cover}; s* of the rooted worlds: median {np.median(sroot):.3g}, 16-84 % [{np.percentile(sroot, 16):.3g}, {np.percentile(sroot, 84):.3g}]" if nroot else "    no rooted world")
        NUM["selftest"] = dict(counts=cnt, rooted=nroot, covered=cover, s_median=float(np.median(sroot)) if nroot else None, s_16_84=[float(np.percentile(sroot, 16)), float(np.percentile(sroot, 84))] if nroot else None)
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg283_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nm_ = 0; n0 = sum(1 for r in ROUTES if main[r]["status"] == "root")
        for r in ROUTES:
            R_ = RES[r]
            if R_["status"] == "root":
                nm_ += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        check("M2 MUTATE=1 (reactivity): V_ext and sigma_ext x 2; rows with a root satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and their number is at least the main run's", f"rows with a root: mutated {nm_}, main {n0}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and nm_ >= n0)
    else:
        d1m = 0.0
        for r in ROUTES:
            R_ = RES[r]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array([R_["D"]]), np.array([R_["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r in ROUTES if RES[r]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        check("M3 two rows (B1, B2), both ID 24", f"rows {[RES[r]['label'] for r in ROUTES]}", len(RES) == 2 and all(RES[r]["z"] == Z for r in ROUTES))
        check("M6 CONTROL: the two routes give the same conversion equivalents (alpha_CO at D = 1 to 1e-9 relative; at s* = 1 to 0.01 dex, the grid of the shift)", f"D = 1: B1 {RES['B1']['alpha_D1']:.6f} vs B2 {RES['B2']['alpha_D1']:.6f}; s* = 1: B1 {RES['B1']['alpha_s1']:.4f} vs B2 {RES['B2']['alpha_s1']:.4f}",
              abs(RES["B1"]["alpha_D1"] / RES["B2"]["alpha_D1"] - 1) < 1e-9 and np.isfinite(RES["B1"]["alpha_s1"]) and np.isfinite(RES["B2"]["alpha_s1"]) and abs(math.log10(RES["B1"]["alpha_s1"] / RES["B2"]["alpha_s1"])) < 0.01)
    if not MUTATE and not SELFTEST:
        r272 = json.load(open(os.path.join(CFG, "CFG272_alpaka_five_discs", "cfg272_stageB_results.json")))["numbers"]["rows"]["24"]
        d_go = abs(RES["B1"]["GO"] / r272["GO"] - 1); d_b1 = abs(RES["B1"]["D"] / r272["D_B1"] - 1); d_b2 = abs(RES["B2"]["D"] / r272["D_B2"] - 1)
        check("M5 CROSS-CHECK: g_obs and the D of B1 and B2 equal CFG272's committed GO, D_B1, D_B2 to 1e-9 relative (the same inputs)", f"relative deviations g_obs {d_go:.1e}, D_B1 {d_b1:.1e}, D_B2 {d_b2:.1e}", max(d_go, d_b1, d_b2) < 1e-9)
    # ---------------------------------------------------------------- hand estimates scored (frozen in section 9)
    he = {}
    B1_, B2_ = RES["B1"], RES["B2"]
    if not MUTATE and not SELFTEST:
        q1 = B1_["q"]; b15 = H.band_edges({float(k_): (v["ls"], v["unb"]) for k_, v in B1_["bands"].items()}, -0.15, 0.15); b30 = H.band_edges({float(k_): (v["ls"], v["unb"]) for k_, v in B1_["bands"].items()}, -0.30, 0.30)
        gbn = {float(k_): (v["ls"], v["unb"]) for k_, v in B1_["gas_bands"].items()}; gi = H.band_edges(gbn, -0.213, 0.213); go_ = H.band_edges(gbn, -0.671, 0.671)
        he["HE1"] = bool(B1_["frac_mc_noroot"] <= 0.01 and all(np.isfinite(q1)) and 16 <= 10 ** q1[1] <= 24 and 33 <= 10 ** q1[3] <= 46 and 10 <= 10 ** q1[0] <= 18 and 45 <= 10 ** q1[4] <= 75)
        gm = B1_["group_max"]; top2 = sorted(gm, key=gm.get, reverse=True)[:2]
        he["HE2"] = bool(0.30 <= B1_["recipe_half"] <= 0.60 and set(top2) == {"gas conversion", "geometry"} and all(gm.get(g_, 0) < 0.1 for g_ in ("pressure", "inclination", "radius")))
        he["HE3"] = bool(3.2 <= B1_["alpha_D1"] <= 3.3 and 2.9 <= B1_["alpha_s1"] <= 3.2)
        he["HE4"] = bool(14 <= b15[0] <= 21 and 36 <= b15[1] <= 52 and 8 <= b30[0] <= 12 and 52 <= b30[1] <= 80 and 10 <= gi[0] <= 18 and 40 <= gi[1] <= 70 and go_[2] == 1)
        he["HE5"] = bool(B2_["status"] == "floor" and 0.70 <= B2_["D"] <= 0.80 and 0.88 <= B2_["frac_mc_noroot"] <= 0.98)
        he["HE6"] = bool(B1_["vacuous"] == 1)
        lad = {round(d_["log_mstar"], 2): d_ for d_ in NUM["ladder"]["rows"]}
        sv = [d_["s"] for d_ in NUM["ladder"]["rows"]]
        he["HE9"] = bool(all(sv[i + 1] <= sv[i] + 1e-9 for i in range(len(sv) - 1)) and 4 <= lad[10.5]["s"] <= 11 and 1.0 <= lad[10.8]["s"] <= 2.5 and lad[11.0]["status"] == "floor" and 10.80 <= NUM["ladder"]["log_mstar_at_D1"] <= 10.95)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE1 (B1 Monte Carlo 68 % [16-24, 33-46], 95 % [10-18, 45-75], rooted >= 0.99): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}")
        P(f"    HE2 (recipe half-width 0.30-0.60; the two largest groups gas conversion and geometry; the others < 0.1): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}  (half {B1_['recipe_half']:.3f}; groups {B1_['group_max']})")
        P(f"    HE3 (alpha_CO at D = 1 in [3.2, 3.3], at s* = 1 in [2.9, 3.2]): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}  ({B1_['alpha_D1']:.3f}, {B1_['alpha_s1']:.3f})")
        P(f"    HE4 (bands +-0.15 [14-21, 36-52], +-0.30 [8-12, 52-80], gas +-0.213 [10-18, 40-70], gas +-0.671 no-root corner): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}  (+-0.15 [{b15[0]:.3g}, {b15[1]:.3g}]; +-0.30 [{b30[0]:.3g}, {b30[1]:.3g}]; gas +-0.213 [{gi[0]:.3g}, {gi[1]:.3g}]; +-0.671 corner {go_[2]})")
        P(f"    HE5 (B2 FLOOR, D 0.70-0.80, no-root fraction 0.88-0.98): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}  (D {B2_['D']:.4f}; no-root {B2_['frac_mc_noroot']:.3f})")
        P(f"    HE6 (B1 VACUOUS under D2): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}")
        P(f"    HE9 (ladder monotone; s*(10.5) 4-11; s*(10.8) 1.0-2.5; floor at 11.0; log M* at D = 1 in [10.80, 10.95]): {'hit' if he['HE9'] else 'MISS (kept as it falls)'}")
    if MUTATE:
        he["HE7"] = bool(B1_["status"] == "root" and 400 <= B1_["s"] <= 700 and B2_["status"] == "root" and 50 <= B2_["s"] <= 100)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE7 (MUTATE=1: B1 s* in [400, 700]; B2 gains a root with s* in [50, 100]): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}  (B1 {B1_['status']} s {B1_['s']:.4g}; B2 {B2_['status']} s {B2_['s']:.4g})")
    if SELFTEST:
        he["HE8"] = bool(0.03 <= NUM["selftest"]["counts"]["floor"] / 100.0 <= 0.20)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE8 (SELFTEST: the fraction of worlds at the floor in [3 %, 20 %]): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}  ({NUM['selftest']['counts']['floor']} of 100)")
    NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "gas_in_lo", "gas_in_hi", "gas_out_lo", "gas_out_hi", "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "s_B1", "noroot_B1", "s_B2", "noroot_B2", "status",
                              "alpha_CO", "alpha_CO_at_D1", "alpha_CO_at_s1", "vacuous", "limit", "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r in ROUTES:
        R_ = RES[r]; st = R_["status"]; q = R_["q"]
        bands = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        gbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["gas_bands"].items()}; gi = H.band_edges(gbn, -0.213, 0.213); go_ = H.band_edges(gbn, -0.671, 0.671)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]; sstar = R_["s"]
        sB = {rr_: (RES[rr_]["s"], int(RES[rr_]["status"] == "floor")) for rr_ in ROUTES}
        extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], gi[0], gi[1], go_[0], go_[1], float("nan"), float("nan"), float("nan"), float("nan"),
                 R_["delta_floor"], R_["delta_to_s1"], sB["B1"][0], sB["B1"][1], sB["B2"][0], sB["B2"][1], st, R_["alpha"], R_["alpha_D1"], R_["alpha_s1"], R_["vacuous"]]
        q_ = ("gas only (no M*, no HST, no continuum on disk); " + {"root": "has a root with " + ("the lower-limit gas B1: s* is an UPPER bound" if r == "B1" else "the Galactic gas B2 (sensitivity, not a limit)"),
                                                                    "floor": "FLOOR: no root, D <= 1: " + ("robust against any added baryon, not against a lower alpha_CO" if r == "B1" else "the Galactic-conversion gas alone exceeds the dynamics"),
                                                                    "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st]
              + ("; VACUOUS (the rooted 95 % lower edge is above the H(z) law's value: the bound excludes neither law)" if R_["vacuous"] else "") + ("; ILL-CONDITIONED near-Newtonian (|lever| >= 10)" if R_["ill"] else "; conditioned (|lever| < 10) but a lower limit")
              + f"; CO(3-2) {ILINE / EILINE:.1f} sigma; i_ALMA {I_AD:.0f} deg; protocluster SSA22; R_e assumed R_ext/1.2; one outer radius")
        rows.append(["CFG283", R_["label"], GCL[r], f"{Z:.4f}", f"{Z:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are a lower limit (B1) or a conventional conversion (B2): s* is an upper bound only for B1", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg283_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg283_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg283{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg283{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
