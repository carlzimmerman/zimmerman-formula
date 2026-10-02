#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG284 -- ADF22.5 (ALPAKA 24, z = 3.094) with its literature stellar mass (Huang+2025, ADF22+ Table 3, source A7): CFG272's three baryon routes.
  B0 = stars only (the headline; a LOWER limit), B1 = stars + the CO gas floor (alpha_CO,min = 0.8, r_J1 = 1; a lower limit), B2 = stars + Galactic gas (alpha_CO = 4.36; sensitivity).
  Stars and gas are Freeman discs of the measured JWST F444W R_e = 2.24 kpc (CFG272's convention: the optical R_e where a measurement exists).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG284_adf22_5_with_stars/FROZEN_CRITERIA.md (b1ca92033) with the look-up record data_assembly/adf22_5_literature_2026-10-02/.
  STAGE=A   the engineering pre-flight with real hand predictions: no velocity column is loaded.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_ext, sigma_ext x 2); STAGE=B SELFTEST=1 (fabricated V_ext on the law at s = 2; the real velocities are never loaded).
Points file: no_root = 1 only for a FLOOR; a CEILING (D > 1 but s* > 1000) is written s_star = 1000, no_root = 0, status = ceiling (CFG277's convention); `resolution` = RESOLVED-ROOT / RESOLVED-FLOOR / UNRESOLVED (the Monte Carlo no-root fraction <= 0.16 / >= 0.84 / between).
Run: STAGE=A python3 .../cfg284_adf22_5_stars.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, io, json, math, time, zlib, csv
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import j0, j1, ive, gammaincinv, gammaln

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
LITP = os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02", "adf22_5_literature_values.csv")
dirs = {"samp": "alpaka1_sample.csv", "prop": "alpaka1_properties.csv", "geo": "alpaka1_geometry.csv", "obs": "alpaka1_alma_obs.csv"}
T = {k: pd.read_csv(os.path.join(AT, v)).set_index("id") for k, v in dirs.items()}
OUTER = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"), usecols=["id", "z", "n_rings", "R_ext_arcsec", "R_ext_kpc", "Re_kpc_dashed_line"]).set_index("id")   # no velocity-bearing column
RING = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"), usecols=["id", "ring", "panel", "R_kpc"])
KINP = os.path.join(AT, "alpaka1_kinematics.csv")
LIT = pd.read_csv(LITP, dtype=str).set_index("quantity")
P("sha256: " + ", ".join(f"{v} {H.sha(os.path.join(AT, v))}" for v in dirs.values()) + f", alpaka1_outer_summary.csv {H.sha(os.path.join(AT, 'alpaka1_digitised', 'alpaka1_outer_summary.csv'))}, adf22_5_literature_values.csv {H.sha(LITP)}; velocity columns loaded: {STAGE == 'B' and not SELFTEST}")
KIN = pd.read_csv(KINP).set_index("id") if (STAGE == "B" and not SELFTEST) else None


def lit(q, col="value"):
    return float(LIT.loc[q, col])


s, p, ge, ob, ou = T["samp"].loc[ID], T["prop"].loc[ID], T["geo"].loc[ID], T["obs"].loc[ID], OUTER.loc[ID]
Z = float(s["z"]); NAME = str(s["name"])
LP = float(p["lprime_1e10_kkmspc2"]) * 1e10; ELP = float(p["e_lprime"]) * 1e10; SIGL = ELP / LP / math.log(10)
ILINE, EILINE = float(p["iline_jykms"]), float(p["e_iline"])
I_AD = float(ge["i_alma"]); E_I = 0.5 * (float(ge["e1.3"]) + float(ge["e2.3"]))
R_EXT = float(ou["R_ext_kpc"]); R_EXT_AS = float(ou["R_ext_arcsec"]); KPA = R_EXT / R_EXT_AS
rr = RING[(RING["id"] == ID) & (RING["panel"] == "V")].sort_values("ring"); R_MEAN = float(rr["R_kpc"].iloc[-2:].mean())
BEAM_MAJ, BEAM_MIN = float(ob["beam_major_arcsec"]), float(ob["beam_minor_arcsec"])
# --- the literature record (Huang+2025 Table 3 row A7; Umehata+2025 Tables 3-4 row ADF22.A7)
MSTAR = lit("Mstar"); EM_HI, EM_LO = lit("Mstar", "err_hi"), lit("Mstar", "err_lo")
LOGM0 = math.log10(MSTAR); SIG_HI = math.log10((MSTAR + EM_HI) / MSTAR); SIG_LO = -math.log10((MSTAR - EM_LO) / MSTAR)
RE_STAR, ERE_STAR, N_STAR, BA_STAR = lit("F444W_Re"), lit("F444W_Re", "err_hi"), lit("F444W_sersic_n"), lit("F444W_axis_ratio")
RE_DUST, BA_DUST = lit("alma870_Re"), lit("alma870_axis_ratio")
I_F444W, I_870 = math.degrees(math.acos(BA_STAR)), math.degrees(math.acos(BA_DUST))
RE_G = RE_STAR                                                                              # CFG272's convention: the gas in the stars' disc
ALPHA = {"B0": 0.0, "B1": 0.8, "B2": 4.36}                                                  # B1 / B2 frozen in CFG272 and CFG283 (r_J1 = 1)
ROUTES = ["B0", "B1", "B2"]
LABEL = {"B0": f"ALPAKA 24 {NAME} [M* H25 stars only]", "B1": f"ALPAKA 24 {NAME} [M* H25 + gas floor]", "B2": f"ALPAKA 24 {NAME} [M* H25 + gas Galactic]"}
GCL = {"B0": "D (stars only: Huang+25 SED M*; CO gas not added; lower limit)", "B1": "L (line L' only; alpha_CO frozen as a lower limit) + SED M*", "B2": "L (line L' only; alpha_CO 4.36 Galactic, r_J1 = 1; sensitivity) + SED M*"}
LAWV = {k: H.LAWS[k](Z) for k in ("FLAT", "H(z)", "PROXY")}
VEXT = EVHI = EVLO = SIG = float("nan")                                                     # placeholders: g_bar never uses them; stage B (real) overwrites, SELFTEST fabricates
if STAGE == "B" and not SELFTEST:
    k = KIN.loc[ID]
    VEXT, EVHI, EVLO, SIG = float(k["vext_kms"]), float(k["vext_errhi"]), float(k["vext_errlo"]), float(k["sigma_ext_kms"])
P(f"row: ID {ID} {NAME} z {Z:.3f}  L' {LP:.3e} +- {ELP:.2e}  R_ext {R_EXT:.3f} kpc ({KPA:.3f} kpc/arcsec)  i_ALMA {I_AD:.0f} +- {E_I:.0f}  | M* {MSTAR:.3e} (+{EM_HI:.2e} -{EM_LO:.2e}; log {LOGM0:.5f} +{SIG_HI:.5f} -{SIG_LO:.5f})  F444W R_e {RE_STAR} +- {ERE_STAR} kpc n {N_STAR} b/a {BA_STAR} (thin-disc i {I_F444W:.1f} deg)  870um R_e {RE_DUST} kpc b/a {BA_DUST} (i {I_870:.1f} deg)  laws at z: FLAT {LAWV['FLAT']:.3f}, PROXY {LAWV['PROXY']:.3f}, H(z) {LAWV['H(z)']:.3f}")


# ---------------------------------------------------------------- geometry
def b_proj(n):
    return float(gammaincinv(2 * n, 0.5))


def sigma_unit(R, n, Re):
    b = b_proj(n); Se = 1.0 / (2 * math.pi * n * math.exp(b) * b ** (-2 * n) * math.exp(gammaln(2 * n)) * Re ** 2)
    return Se * np.exp(-b * ((R / Re) ** (1.0 / n) - 1.0))


_HC = {}


def hankel_g_unit(n, Re, Rk, NRp=4000, Rmax_f=14.0, NK=24000, Kmax_f=60.0, chunk=2000):
    """razor-thin Sersic disc of unit mass: g [m s^-2 per Msun] at radii Rk [kpc] by the Hankel transform (CFG275/276/278's validated function)"""
    key = (n, Re, tuple(np.round(np.atleast_1d(Rk), 9)))
    if key in _HC: return _HC[key]
    Rp = np.linspace(0, Rmax_f * Re, NRp + 1); dR = Rp[1] - Rp[0]; S = sigma_unit(Rp, n, Re) * Rp
    w = np.ones(NRp + 1); w[0] = w[-1] = 0.5
    ks = np.linspace(0, Kmax_f / Re, NK + 1); dk = ks[1] - ks[0]; St = np.empty(NK + 1)
    for a in range(0, NK + 1, chunk):
        kk = ks[a:a + chunk]; St[a:a + chunk] = (j0(np.outer(kk, Rp)) * (S * w * dR)).sum(axis=1)
    wk = np.ones(NK + 1); wk[0] = wk[-1] = 0.5
    Rk = np.atleast_1d(Rk).astype(float)
    g = np.array([(ks * j1(ks * R) * St * wk * dk).sum() for R in Rk]) * 2 * math.pi * H.G_KPC * H.G2SI
    _HC[key] = g
    return g


def gauss_closed(s_, R):
    x = R ** 2 / (4 * s_ ** 2)
    return H.G_KPC * math.sqrt(math.pi / 2) * R / (2 * s_ ** 3) * (ive(0, x) - ive(1, x)) * H.G2SI


def gobs_gbar(route="B0", vm="pub", inc="adopt", rad="ext", refac=1.0, sph=False, gas_fac=1.0, ts=0.0, tg=0.0, re_s=None, re_g=None, sersic=False, V=None, SG=None, Lp=None, Ms=None, i_deg=None):
    """g_obs and g_bar [m s^-2] of the stars (+ gas) under a route (B0 / B1 / B2) and a knob setting; Ms / Lp may be arrays (the Monte Carlo)."""
    R = R_EXT if rad == "ext" else R_MEAN
    Ms_ = (MSTAR if Ms is None else Ms) * 10 ** ts
    Mg = ALPHA[route] * (LP if Lp is None else Lp) * gas_fac * 10 ** tg
    Rs = (RE_STAR if re_s is None else re_s) * refac
    Rg = (RE_G if re_g is None else re_g) * refac
    f = H.gsph if sph else H.gdisc
    if sersic:
        gstar = Ms_ * float(hankel_g_unit(N_STAR, Rs, np.array([R]))[0])
    else:
        gstar = f(Ms_, Rs, R)
    gb = gstar + (f(Mg, Rg, R) if route != "B0" else 0.0)
    go = None
    if STAGE == "B":
        sg = SIG if SG is None else SG
        V2 = (VEXT if V is None else V) ** 2 + {"pub": 0.0, "a168": 1.68 * sg ** 2, "a336": 3.36 * sg ** 2}[vm]
        i_new = i_deg if i_deg is not None else {"adopt": I_AD, "lo": max(5.0, I_AD - E_I), "hi": min(85.0, I_AD + E_I)}[inc]
        go = V2 * (math.sin(math.radians(I_AD)) / math.sin(math.radians(i_new))) ** 2 / R * H.G2SI
    return go, gb


GB = {r: float(gobs_gbar(r)[1]) for r in ROUTES}
GSTAR = float(H.gdisc(MSTAR, RE_STAR, R_EXT)); GUN_GAS = float(H.gdisc(LP, RE_G, R_EXT))   # stellar force; gas force per unit alpha_CO
Y = {r: GB[r] / A0C for r in ROUTES}
NUY = {r: float(NU(np.array([Y[r]]))[0]) for r in ROUTES}
P("baryon side: " + "; ".join(f"{r}: g_bar {GB[r]:.4e} y {Y[r]:.3f} nu(y) {NUY[r]:.4f}" for r in ROUTES) + f"; g_* {GSTAR:.4e} (M* {MSTAR:.2e}); gas force per unit alpha_CO {GUN_GAS:.4e}")

KNOB_LIST = [("R_e x1.5 (stars and gas)", dict(refac=1.5)), ("R_e /1.5 (stars and gas)", dict(refac=1 / 1.5)), ("stars R_e +1 sigma", dict(re_s=RE_STAR + ERE_STAR)), ("stars R_e -1 sigma", dict(re_s=RE_STAR - ERE_STAR)),
             ("spherical (enclosed mass as a point mass)", dict(sph=True)), ("gas at R_ext/1.2 (CFG283's R_e)", dict(re_g=R_EXT / 1.2)), ("gas at the 870 um dust R_e", dict(re_g=RE_DUST)), ("stars as the Sersic n = 3.21 thin disc (Hankel)", dict(sersic=True)),
             ("pressure +1.68 sigma^2", dict(vm="a168")), ("pressure +3.36 sigma^2", dict(vm="a336")),
             ("inclination -1 sigma", dict(inc="lo")), ("inclination +1 sigma", dict(inc="hi")), (f"inclination from the F444W axis ratio ({I_F444W:.1f} deg)", dict(i_deg=I_F444W)), (f"inclination from the 870 um axis ratio ({I_870:.1f} deg)", dict(i_deg=I_870)),
             ("V_ext at R_mean of the last two rings", dict(rad="mean")), ("kernel P2", dict(nu=NUP2)), ("M* x 10^-0.30", dict(ts=-0.30)), ("M* x 10^+0.30", dict(ts=+0.30)),
             ("gas: r_31 = 0.6 (gas x 1/0.6)", dict(gas_fac=1 / 0.6)), ("gas: helium x 1.36", dict(gas_fac=1.36))]
KGROUP = {}
for nm, _ in KNOB_LIST:
    KGROUP[nm] = ("geometry" if nm.startswith(("R_e", "stars R_e", "spherical", "gas at", "stars as")) else "pressure" if nm.startswith("pressure") else "inclination" if nm.startswith("inclination") else "radius" if nm.startswith("V_ext")
                  else "kernel" if nm.startswith("kernel") else "stellar mass" if nm.startswith("M*") else "gas conversion")
assert len(KNOB_LIST) == 20 and set(KGROUP.values()) == {"geometry", "pressure", "inclination", "radius", "kernel", "stellar mass", "gas conversion"}


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


def eq_alpha(s_law, go, gstar):
    """the CO conversion alpha_CO at which the median residual is zero for a law with a0 = s_law x canonical (stars fixed, gas = alpha L' in the gas disc); nan if even alpha = 0 gives s* below the law or the stars alone exceed g_obs"""
    hi = (go - gstar) / GUN_GAS
    if hi <= 0: return float("nan")
    def f(a):
        gb = gstar + a * GUN_GAS; ls, st = H.s_status(np.array([go / gb]), np.array([gb])); return ls - math.log10(s_law), st
    f0, st0 = f(0.0)
    if st0 != "root" or f0 < 0: return float("nan")
    lo = 0.0
    for _ in range(200):
        mid = 0.5 * (lo + hi); fm, stm = f(mid)
        if stm == "root" and fm > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE ENGINEERING PRE-FLIGHT (no velocity column is loaded; no g_obs, D, delta or s* is formed)")
    pos = LIT.loc["position_huang25", "value"].split(); hh, mm, ss = (float(x_) for x_ in pos[0].split(":")); sg_ = -1.0 if pos[1].startswith("-") else 1.0; dd, dm, ds = (float(x_) for x_ in pos[1].lstrip("+-").split(":"))
    ra_l = (hh + mm / 60 + ss / 3600) * 15.0; dec_l = sg_ * (dd + dm / 60 + ds / 3600)
    sep = math.hypot((ra_l - float(s["ra_deg"])) * math.cos(math.radians(dec_l)), dec_l - float(s["dec_deg"])) * 3600.0
    ok_log = abs(float(LIT.loc["log10_Mstar", "value"]) - LOGM0) < 1e-4 and abs(float(LIT.loc["log10_Mstar", "err_hi"]) - SIG_HI) < 1e-4 and abs(float(LIT.loc["log10_Mstar", "err_lo"]) - SIG_LO) < 1e-4
    check("C1 CONTROL: the ID 24 row and the literature record load (M*, its asymmetric errors and the log widths agree with the record's own log row to 1e-4, F444W and 870 um sizes and axis ratios finite) and the ALPAKA coordinates equal the record's A7 position within 1 arcsec",
          f"M* {MSTAR:.3e} +{EM_HI:.2e} -{EM_LO:.2e} (log {LOGM0:.5f} +{SIG_HI:.5f} -{SIG_LO:.5f}; record log row consistent {ok_log}); R_e {RE_STAR} / {RE_DUST}; b/a {BA_STAR} / {BA_DUST}; separation {sep:.2f} arcsec; z {Z}",
          all(np.isfinite([MSTAR, EM_HI, EM_LO, RE_STAR, RE_DUST, N_STAR, BA_STAR, BA_DUST, Z, LP, ELP, R_EXT, I_AD, E_I])) and ok_log and sep < 1.0)
    yy = np.linspace(0.05, 40, 400000); hh_ = H.i0e(yy) * H.k0e(yy) - H.i1e(yy) * H.k1e(yy); peak = float(np.max(2 * yy ** 2 * hh_))
    farr = float(H.gdisc(1e11, 3.0, 150.0) / (H.G_KPC * 1e11 / 150.0 ** 2 * H.G2SI))
    src29 = open(os.path.join(CFG, "CFG229_class_m_gold", "cfg229_score.py")).read(); seg = src29[src29.index("def disc_v2"):src29.index("P(__doc__")]
    ns29 = {"G_KPC": H.G_KPC, "XN": H.XN, "G2SI": H.G2SI, "i0e": H.i0e, "i1e": H.i1e, "k0e": H.k0e, "k1e": H.k1e, "math": math, "np": np}; exec(compile(seg, "cfg229_score.py", "exec"), ns29)
    rr_ = np.random.default_rng(1234); dmax = 0.0
    for _ in range(200):
        M_, Re_, Rr_ = 10 ** rr_.uniform(9, 12.5), rr_.uniform(0.5, 8), rr_.uniform(1, 20)
        dmax = max(dmax, abs(H.gdisc(M_, Re_, Rr_) / ns29["gdisc"](M_, Re_, Rr_) - 1))
    g_h1 = hankel_g_unit(1.0, 2.57, np.array([1.0, 3.6, 7.2])); g_f = np.array([float(H.gdisc(1.0, 2.57, r)) for r in (1.0, 3.6, 7.2)]); d1h = float(np.max(np.abs(g_h1 / g_f - 1)))
    s_g = 2.57 / math.sqrt(2 * b_proj(0.5)); g_h5 = hankel_g_unit(0.5, 2.57, np.array([1.0, 3.6, 7.2])); g_c = np.array([gauss_closed(s_g, r) for r in (1.0, 3.6, 7.2)]); d5h = float(np.max(np.abs(g_h5 / g_c - 1)))
    check("C2 CONTROL: Freeman's peak V^2 = 0.3872 G M / R_d to 0.003, g -> G M / r^2 far from a compact mass to 1e-3, gdisc equals CFG229's on 200 random inputs to 1e-12, and the Hankel thin Sersic disc equals Freeman's exact exponential disc (n = 1) and the exact Gaussian (n = 0.5) closed form to 2e-3",
          f"peak {peak:.4f}; far-field ratio {farr:.5f}; max deviation from CFG229's gdisc {dmax:.1e}; Hankel vs Freeman {d1h:.1e}; vs Gaussian {d5h:.1e}", abs(peak / 0.3872 - 1) < 0.003 and abs(farr - 1) < 1e-3 and dmax < 1e-12 and d1h < 2e-3 and d5h < 2e-3)
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
    r283 = json.load(open(os.path.join(CFG, "CFG283_alpaka24_gas_only", "cfg283_stageB_results.json")))["numbers"]["rows"]
    c1_ = float(gobs_gbar("B1", Ms=0.0, re_g=R_EXT / 1.2)[1]); c2_ = float(gobs_gbar("B2", Ms=0.0, re_g=R_EXT / 1.2)[1])
    d5 = max(abs(c1_ / r283["B1"]["GB"] - 1), abs(c2_ / r283["B2"]["GB"] - 1))
    check("C5 CONTINUITY: with M* = 0 and the gas at R_ext/1.2 the B1 and B2 g_bar equal CFG283's committed values to 1e-9 relative (only the baryon values are read)", f"relative deviation {d5:.1e} (B1 {c1_:.6e} vs {r283['B1']['GB']:.6e}; B2 {c2_:.6e} vs {r283['B2']['GB']:.6e})", d5 < 1e-9)
    nuo = 345.79599 / (1 + Z); DL = dl_mpc(Z); Lcalc = 3.25e7 * ILINE * nuo ** -2 * DL ** 2 * (1 + Z) ** -3
    check("C6 CONTROL: the tabulated L' equals the line-flux formula L' = 3.25e7 S dv nu_obs^-2 D_L^2 (1+z)^-3 (flat LCDM 67.4 / 0.315) to 5 %", f"S dv = {ILINE} +- {EILINE} Jy km/s; D_L {DL:.1f} Mpc; formula {Lcalc:.3e} vs table {LP:.3e} ({Lcalc / LP - 1:+.3f})", abs(Lcalc / LP - 1) < 0.05)
    P("\nA1  BARYON SIDE AND THE CFG240 READING (noiseless world; lever = d log10 s* / d(baryon dex); ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    ILL, LEV = {}, {}
    for r in ROUTES:
        lv, fl = H.lever1(np.array([NUY[r]]), np.array([GB[r]])); LEV[r] = lv; ILL[r] = bool(fl or abs(lv) >= 10)
        P(f"    {r} (alpha_CO {ALPHA[r]}): g_bar {GB[r]:.3e}  y {Y[r]:.3f}  nu(y) {NUY[r]:.4f}  lever {lv:+.2f}{' (flag: a +-0.03 dex baryon move removes the noiseless root)' if fl else ''}  {'ILL-CONDITIONED' if ILL[r] else 'conditioned'}   one radius (R_ext): no deep point")
    P("\nA2  KNOB EFFECTS ON g_bar (dex relative to the nominal; baryon side only; B0 / B1 / B2)")
    A2 = {}
    for nm, kw in KNOB_LIST:
        if KGROUP[nm] in ("pressure", "inclination", "kernel") or nm.startswith("V_ext"): continue
        kk = {k_: v_ for k_, v_ in kw.items() if k_ != "nu"}
        A2[nm] = [math.log10(float(gobs_gbar(r, **kk)[1]) / GB[r]) for r in ROUTES]
        P(f"    {nm}: " + " / ".join(f"{x_:+.3f}" for x_ in A2[nm]))
    P(f"\nA3  g_*/g_bar by route: B0 1.000, B1 {GSTAR / GB['B1']:.3f}, B2 {GSTAR / GB['B2']:.3f}; M*/M_gas: B1 {MSTAR / (ALPHA['B1'] * LP):.2f}, B2 {MSTAR / (ALPHA['B2'] * LP):.2f}; beam {BEAM_MAJ:.2f} x {BEAM_MIN:.2f} arcsec = {BEAM_MAJ * KPA:.2f} x {BEAM_MIN * KPA:.2f} kpc against R_ext {R_EXT:.2f} kpc; the thin-disc inclinations {I_F444W:.1f} / {I_870:.1f} deg against the kinematic {I_AD:.0f} +- {E_I:.0f}: g_obs factors {(math.sin(math.radians(I_AD)) / math.sin(math.radians(I_F444W))) ** 2:.3f} / {(math.sin(math.radians(I_AD)) / math.sin(math.radians(I_870))) ** 2:.3f} (no velocity)")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR, GEOMETRY AND BARYON SIDE VALIDATED: {pfd1} (controls C1-C6)")
    he = {"HE1": bool(5.0 <= Y["B0"] <= 5.4 and 7.8 <= Y["B1"] <= 8.3 and 20 <= Y["B2"] <= 21.5 and -8.5 <= LEV["B0"] <= -5.5 and not ILL["B0"] and 8.5 <= abs(LEV["B1"]) <= 13 and not np.isfinite(LEV["B2"]) and ILL["B2"])}
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE2-HE9 are scored at stage B):")
    P(f"    HE1: y(B0) in [5.0, 5.4], y(B1) in [7.8, 8.3], y(B2) in [20, 21.5]; lever B0 in [-8.5, -5.5] (conditioned), |lever| B1 in [8.5, 13], B2 not computable (ILL): {'hit' if he['HE1'] else 'MISS (kept as it falls)'}  (y {Y['B0']:.3f} / {Y['B1']:.3f} / {Y['B2']:.3f}; lever {LEV['B0']:+.2f} / {LEV['B1']:+.2f} / {LEV['B2']})")
    NUM.update(inputs=dict(z=Z, Lp=LP, eLp=ELP, R_ext=R_EXT, R_mean=R_MEAN, i=I_AD, ei=E_I, Mstar=MSTAR, logM0=LOGM0, sig_hi=SIG_HI, sig_lo=SIG_LO, Re_star=RE_STAR, N_star=N_STAR, GB=GB, GSTAR=GSTAR, y=Y, nuy=NUY, Lcalc=Lcalc, sep_arcsec=sep, i_F444W=I_F444W, i_870=I_870), lever=LEV, ill=ILL, knob_gbar_dex=A2, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_ext and sigma_ext x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2840)
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
        Msd = 10 ** H.split_normal(rng, LOGM0, SIG_HI, SIG_LO, n)
        return Vd ** 2 / R_EXT * H.G2SI * facd, Lpd, Msd

    def gbar_draws(route, Lpd, Msd):
        return H.gdisc(Msd, RE_STAR, R_EXT) + (H.gdisc(ALPHA[route] * Lpd, RE_G, R_EXT) if route != "B0" else 0.0)

    MDYN = VEXT ** 2 * R_EXT / H.G_KPC
    for r in ROUTES:
        lab = LABEL[r]
        ls0, st0, go0, gb0 = solve(r); D0 = go0 / gb0
        rng = np.random.default_rng(zlib.crc32(("284|" + lab).encode()) % 100000)
        god, Lpd, Msd = mc_draws(rng, VEXT, EVHI, EVLO, B_MC)
        gbd = gbar_draws(r, Lpd, Msd)
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
        Dd = god / gbd
        frac_floor = float(np.mean(ud & (Dd <= 1.0))); frac_ceiling = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(go0 / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        bands = H.band_solutions(np.array([D0]), np.array([gb0]))
        gas_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(r, tg=s_)[1])]), np.array([float(gobs_gbar(r, tg=s_)[1])])) for s_ in (-0.671, -0.213, 0.213, 0.671)} if r != "B0" else {s_: (float("nan"), True) for s_ in (-0.671, -0.213, 0.213, 0.671)}
        star_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(r, ts=s_)[1])]), np.array([float(gobs_gbar(r, ts=s_)[1])])) for s_ in (-0.30, -0.15, 0.15, 0.30)}
        kn, kD, kst = {}, {}, {}
        for nm, kw in KNOB_LIST:
            lk, stk, gok, gbk = solve(r, **dict(kw))
            kn[nm] = None if (st0 != "root" or stk != "root") else lk - ls0; kst[nm] = stk; kD[nm] = math.log10((gok / gbk) / D0)
        grp = {}
        for nm, _ in KNOB_LIST:
            if kn[nm] is not None: grp.setdefault(KGROUP[nm], []).append(abs(kn[nm]))
        gmax = {g_: max(v) for g_, v in grp.items()}
        half = math.sqrt(sum(v ** 2 for v in gmax.values())) if gmax else float("nan")
        n_root = sum(1 for nm, _ in KNOB_LIST if kst[nm] == "root"); n_floor = sum(1 for nm, _ in KNOB_LIST if st0 == "root" and kst[nm] == "floor")
        lv_nl, lf_nl = H.lever1(np.array([NUY[r]]), np.array([GB[r]]))
        dflo = H.delta_floor(np.array([D0])); d1 = H.shift_to_s1(np.array([D0]), np.array([gb0]))
        gstar0 = float(gobs_gbar("B0")[1])
        a_D1 = (go0 - gstar0) / GUN_GAS if go0 > gstar0 else float("nan")
        eqs = {k_: eq_alpha(LAWV[k_], go0, gstar0) for k_ in ("FLAT", "PROXY", "H(z)")}
        sval = H.s_val_status(ls0, st0)
        resol = "RESOLVED-ROOT" if frn <= 0.16 else ("RESOLVED-FLOOR" if frn >= 0.84 else "UNRESOLVED")
        lo95 = 10 ** q[0] if np.isfinite(q[0]) else float("nan"); hi95 = 10 ** q[4] if np.isfinite(q[4]) else float("nan")
        vac = int(resol == "RESOLVED-ROOT" and np.isfinite(lo95) and lo95 >= LAWV["H(z)"])
        below = int(resol == "RESOLVED-ROOT" and np.isfinite(hi95) and hi95 < LAWV["H(z)"])
        RES[r] = dict(route=r, label=lab, alpha=ALPHA[r], z=Z, GO=go0, GB=gb0, D=D0, y=Y[r], ls=ls0, status=st0, s=sval, q=q, frac_mc_noroot=frn, frac_mc_floor=frac_floor, frac_mc_ceiling=frac_ceiling, resolution=resol, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1],
                      bands={f"{k_:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in bands.items()}, gas_bands={f"{k_:+.3f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in gas_b.items()},
                      star_bands={f"{k_:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in star_b.items()}, knobs=kn, knob_D_dex=kD, knob_status=kst, group_max=gmax, recipe_half=half, n_knobs_with_root=n_root, n_knobs_to_floor=n_floor, n_knobs=len(KNOB_LIST),
                      lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=dflo, delta_to_s1=d1, alpha_D1=a_D1, alpha_eq=eqs, vacuous=vac, below_rival=below, M_gas=ALPHA[r] * LP, M_star=MSTAR)
        R_ = RES[r]
        P(f"  {lab}: z {Z:.3f}  g_obs {go0:.4e}  g_bar {gb0:.4e}  D {D0:.4f}  delta_FLAT {dF0:+.3f} [{dq[0]:+.3f}, {dq[1]:+.3f}]  y {Y[r]:.3f}  status {st0.upper()}" + (f"  s* <= {10 ** ls0:.4g} (a0 <= {10 ** ls0 * 0.93603:.4g}e-10)" if st0 == "root" else "") + f"  [{resol}]")
        P(f"      Monte Carlo (B = {B_MC}): draws without a root {frn:.3f} (floor {frac_floor:.3f}, ceiling {frac_ceiling:.3f}); rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.4g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.4g}]  95 % [{lo95:.4g}, {hi95:.4g}]  median {10 ** q[2] if np.isfinite(q[2]) else float('nan'):.4g}")
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"      bands: all baryons +-0.15 [{b15[0]:.4g}, {b15[1]:.4g}]{' (no-root corner)' if b15[2] else ''}  +-0.30 [{b30[0]:.4g}, {b30[1]:.4g}]{' (no-root corner)' if b30[2] else ''}")
        P(f"      Delta_floor {dflo:+.3f} dex; baryon shift for s* = 1: {d1:+.3f} dex; alpha_CO at D = 1: {a_D1:.4f}; alpha_CO for FLAT {eqs['FLAT']:.4f}, PROXY {eqs['PROXY']:.4f}, H(z) {eqs['H(z)']:.4f}; lever (noiseless) {lv_nl:+.2f}{' ILL-CONDITIONED' if R_['ill'] else ' (conditioned)'}; variants with a root {n_root}/{len(KNOB_LIST)} (to a floor {n_floor}); recipe half-width {half:.3f}" + ("; VACUOUS (D2)" if vac else "") + ("; BELOW THE RIVAL (D3)" if below else ""))
        P("      knobs (Delta log10 s*; -- = the base or the variant has no root; [status; Delta log10 D]): " + "; ".join(f"{nm} " + ("--" if kn[nm] is None else f"{kn[nm]:+.3f}") + f" [{kst[nm]}; {kD[nm]:+.3f}]" for nm, _ in KNOB_LIST))
        P("      knob groups (max |Delta log10 s*|): " + (", ".join(f"{g_} {v:.3f}" for g_, v in gmax.items()) if gmax else "none (no root at the base)"))
    P(f"\n  context: M_dyn(< R_ext) = V_ext^2 R_ext / G = {MDYN:.3e} Msun (a scale); M*/M_dyn {MSTAR / MDYN:.3f}; (M* + M_gas(B1))/M_dyn {(MSTAR + RES['B1']['M_gas']) / MDYN:.3f}; (M* + M_gas(B2))/M_dyn {(MSTAR + RES['B2']['M_gas']) / MDYN:.3f}")
    NUM["context"] = dict(M_dyn=MDYN, Mstar_over_Mdyn=MSTAR / MDYN)
    # ---------------------------------------------------------------- SELFTEST: 100 worlds per set on the law at s_true = 2
    if SELFTEST:
        NUM["selftest"] = {}
        for rs_ in ("B0", "B1"):
            P(f"\n  SELFTEST (100 worlds on the {rs_} baryons): V_ext fabricated from the law at s_true = 2, 0.15 dex scatter on g_obs, 10 % V errors; Monte Carlo B = 1,000 per world; the L' and M* errors drawn as in the main run")
            rW = np.random.default_rng(28400 + (0 if rs_ == "B0" else 1)); cnt = {"root": 0, "floor": 0, "ceiling": 0}; sroot, cover = [], 0
            for w in range(100):
                gobw = GB[rs_] * float(NU(np.array([GB[rs_] / (2.0 * A0C)]))[0]) * 10 ** rW.normal(0, 0.15)
                Vw = math.sqrt(gobw * R_EXT / H.G2SI)
                lsw, stw = H.s_status(np.array([gobw / GB[rs_]]), np.array([GB[rs_]])); cnt[stw] += 1
                if stw != "root": continue
                godw, Lpdw, Msdw = mc_draws(rW, Vw, 0.10 * Vw, 0.10 * Vw, 1000); gbdw = gbar_draws(rs_, Lpdw, Msdw)
                lsdw, udw = H.AI.implied((godw / gbdw)[:, None], gbdw[:, None], NU, A0C); qw, _ = H.rooted_pct(lsdw, udw)
                sroot.append(10 ** lsw)
                if np.isfinite(qw[0]) and qw[0] <= math.log10(2.0) <= qw[4]: cover += 1
            nroot = cnt["root"]
            P(f"    status of the fabricated worlds: root {cnt['root']}, floor {cnt['floor']}, ceiling {cnt['ceiling']}; of the {nroot} rooted worlds the 95 % interval contains s = 2 in {cover}; s* of the rooted worlds: median {np.median(sroot):.3g}, 16-84 % [{np.percentile(sroot, 16):.3g}, {np.percentile(sroot, 84):.3g}]" if nroot else "    no rooted world")
            NUM["selftest"][rs_] = dict(counts=cnt, rooted=nroot, covered=cover, s_median=float(np.median(sroot)) if nroot else None, s_16_84=[float(np.percentile(sroot, 16)), float(np.percentile(sroot, 84))] if nroot else None)
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg284_stageB_results.json")))["numbers"]["rows"]
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
        check("M3 three rows (B0, B1, B2), all ID 24", f"rows {[RES[r]['label'] for r in ROUTES]}", len(RES) == 3 and all(RES[r]["z"] == Z for r in ROUTES))
        ad = [RES[r]["alpha_D1"] for r in ROUTES]; ok6 = all(np.isfinite(ad)) and max(abs(a / ad[0] - 1) for a in ad) < 1e-9
        for k_ in ("FLAT", "PROXY", "H(z)"):
            v = [RES[r]["alpha_eq"][k_] for r in ROUTES]
            ok6 = ok6 and (all(np.isnan(v)) or (all(np.isfinite(v)) and max(abs(a / v[0] - 1) for a in v) < 1e-9))
        check("M6 CONTROL: the alpha_CO equivalents agree across the three rows (same stars, same disc) to 1e-9 relative", f"D = 1: {ad}; FLAT {[RES[r]['alpha_eq']['FLAT'] for r in ROUTES]}", ok6)
        gstar0 = float(gobs_gbar("B0")[1]); worst = 0.0
        for k_ in ("FLAT", "PROXY", "H(z)"):
            a_ = RES["B1"]["alpha_eq"][k_]
            if np.isfinite(a_):
                gbq = gstar0 + a_ * GUN_GAS; lq, _ = H.s_status(np.array([RES["B1"]["GO"] / gbq]), np.array([gbq])); worst = max(worst, abs(lq - math.log10(LAWV[k_])))
        check("M7 CONTROL: each law-equivalent alpha_CO returns its law's s to 1e-6 dex when re-solved", f"max |d log10 s| {worst:.1e}", worst < 1e-6)
    if not MUTATE and not SELFTEST:
        r283 = json.load(open(os.path.join(CFG, "CFG283_alpaka24_gas_only", "cfg283_stageB_results.json")))["numbers"]["rows"]
        d_go = abs(RES["B1"]["GO"] / r283["B1"]["GO"] - 1)
        go1, gb1 = gobs_gbar("B1", Ms=0.0, re_g=R_EXT / 1.2); go2, gb2 = gobs_gbar("B2", Ms=0.0, re_g=R_EXT / 1.2)
        d_b1 = abs((go1 / gb1) / r283["B1"]["D"] - 1); d_b2 = abs((go2 / gb2) / r283["B2"]["D"] - 1)
        check("M5 CONTINUITY: g_obs equals CFG283's committed GO, and with the stars removed and the gas at R_ext/1.2 the D of B1 and B2 equal CFG283's committed D_B1 and D_B2, to 1e-9 relative", f"relative deviations g_obs {d_go:.1e}, D_B1 {d_b1:.1e}, D_B2 {d_b2:.1e}", max(d_go, d_b1, d_b2) < 1e-9)
    # ---------------------------------------------------------------- hand estimates scored (frozen in section 9)
    he = {}
    B0_, B1_, B2_ = RES["B0"], RES["B1"], RES["B2"]
    if not MUTATE and not SELFTEST:
        he["HE2"] = bool(1.65 <= B0_["D"] <= 1.80 and B0_["status"] == "root" and 6.0 <= B0_["s"] <= 8.0 and 1.08 <= B1_["D"] <= 1.15 and B1_["status"] == "root" and 1.0 <= B1_["s"] <= 2.2 and 0.41 <= B2_["D"] <= 0.46 and B2_["status"] == "floor")
        q0 = B0_["q"]
        he["HE3"] = bool(0.07 <= B0_["frac_mc_noroot"] <= 0.20 and 0.28 <= B1_["frac_mc_noroot"] <= 0.48 and B2_["frac_mc_noroot"] >= 0.99 and B0_["resolution"] == "RESOLVED-ROOT" and B1_["resolution"] == "UNRESOLVED" and B2_["resolution"] == "RESOLVED-FLOOR"
                         and all(np.isfinite(q0)) and 2.0 <= 10 ** q0[1] <= 4.5 and 20 <= 10 ** q0[3] <= 45 and 0.5 <= 10 ** q0[0] <= 1.5 and 50 <= 10 ** q0[4] <= 110 and 6 <= 10 ** q0[2] <= 12)
        he["HE4"] = bool(B0_["vacuous"] == 0 and B0_["below_rival"] == 0)
        eq = B1_["alpha_eq"]
        he["HE5"] = bool(1.00 <= B1_["alpha_D1"] <= 1.12 and 0.85 <= eq["FLAT"] <= 1.00 and 0.40 <= eq["PROXY"] <= 0.75 and 0.10 <= eq["H(z)"] <= 0.50 and 0.5 <= MSTAR / MDYN <= 0.65)
        kn1, ks1 = B1_["knobs"], B1_["knob_status"]; nm_f444 = f"inclination from the F444W axis ratio ({I_F444W:.1f} deg)"; nm_870 = f"inclination from the 870 um axis ratio ({I_870:.1f} deg)"
        he["HE6"] = bool(all(ks1[n_] == "root" and kn1[n_] is not None and 0.5 <= kn1[n_] <= 0.8 for n_ in (nm_f444, nm_870)) and ks1["M* x 10^-0.30"] == "root" and 0.4 <= kn1["M* x 10^-0.30"] <= 0.8
                         and all(ks1[n_] == "floor" for n_ in ("M* x 10^+0.30", "gas: r_31 = 0.6 (gas x 1/0.6)", "gas: helium x 1.36", "R_e /1.5 (stars and gas)"))
                         and all(kn1[n_] is not None and 0.4 <= kn1[n_] <= 0.7 for n_ in ("R_e x1.5 (stars and gas)", "spherical (enclosed mass as a point mass)")) and 0.8 <= B1_["recipe_half"] <= 1.4 and 12 <= B1_["n_knobs_with_root"] <= 18)
        he["HE7"] = bool(0.5 <= B0_["recipe_half"] <= 1.0 and B0_["knob_status"]["M* x 10^+0.30"] == "floor")
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE2 (nominal D, status, s*: B0 1.65-1.80 / root / 6-8; B1 1.08-1.15 / root / 1.0-2.2; B2 0.41-0.46 / floor): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}  (D {B0_['D']:.4f} / {B1_['D']:.4f} / {B2_['D']:.4f}; s* {B0_['s']:.4g} / {B1_['s']:.4g} / {B2_['s']:.4g})")
        P(f"    HE3 (no-root fractions B0 0.07-0.20, B1 0.28-0.48, B2 >= 0.99; resolutions; B0 rooted 68 % [2-4.5, 20-45], 95 % [0.5-1.5, 50-110], median 6-12): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}  (fractions {B0_['frac_mc_noroot']:.3f} / {B1_['frac_mc_noroot']:.3f} / {B2_['frac_mc_noroot']:.3f}; {B0_['resolution']} / {B1_['resolution']} / {B2_['resolution']}; B0 q {[round(10 ** v, 3) for v in q0]})")
        P(f"    HE4 (B0 not vacuous and not below the rival): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}")
        P(f"    HE5 (alpha_CO at D = 1 in 1.00-1.12; FLAT 0.85-1.00; PROXY 0.40-0.75; H(z) 0.10-0.50; M*/M_dyn 0.5-0.65): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}  ({B1_['alpha_D1']:.4f}; {eq['FLAT']:.4f}, {eq['PROXY']:.4f}, {eq['H(z)']:.4f}; {MSTAR / MDYN:.3f})")
        P(f"    HE6 (B1 knobs: thin-disc inclinations +0.5..+0.8; M* -0.30 +0.4..+0.8; floors for M* +0.30, r_31, helium, R_e/1.5; R_e x1.5 and spherical +0.4..+0.7; half-width 0.8-1.4; 12-18 roots): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}  (half {B1_['recipe_half']:.3f}; roots {B1_['n_knobs_with_root']}; groups {B1_['group_max']})")
        P(f"    HE7 (B0 recipe half-width 0.5-1.0 and M* +0.30 -> floor): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}  (half {B0_['recipe_half']:.3f})")
    if MUTATE:
        he["HE8"] = bool(B0_["status"] == "root" and 150 <= B0_["s"] <= 300 and B1_["status"] == "root" and 80 <= B1_["s"] <= 200 and B2_["status"] == "root" and 15 <= B2_["s"] <= 50)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE8 (MUTATE=1: B0 s* in [150, 300]; B1 in [80, 200]; B2 gains a root with s* in [15, 50]): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}  (B0 {B0_['status']} {B0_['s']:.4g}; B1 {B1_['status']} {B1_['s']:.4g}; B2 {B2_['status']} {B2_['s']:.4g})")
    if SELFTEST:
        f0 = NUM["selftest"]["B0"]["counts"]["floor"] / 100.0; f1 = NUM["selftest"]["B1"]["counts"]["floor"] / 100.0
        he["HE9"] = bool(0.12 <= f0 <= 0.40 and 0.20 <= f1 <= 0.50)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE9 (SELFTEST: the fraction of worlds at the floor in [12 %, 40 %] on the B0 baryons and [20 %, 50 %] on the B1 baryons): {'hit' if he['HE9'] else 'MISS (kept as it falls)'}  ({f0:.2f}, {f1:.2f})")
    NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "gas_in_lo", "gas_in_hi", "gas_out_lo", "gas_out_hi", "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "status", "resolution", "alpha_CO", "alpha_CO_at_D1", "alpha_CO_FLAT",
                              "alpha_CO_PROXY", "alpha_CO_Hz", "vacuous", "below_rival", "M_star", "M_gas", "limit", "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r in ROUTES:
        R_ = RES[r]; st = R_["status"]; q = R_["q"]
        bands = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        gbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["gas_bands"].items()}; sbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["star_bands"].items()}
        gi = H.band_edges(gbn, -0.213, 0.213) if r != "B0" else (float("nan"),) * 3; go_ = H.band_edges(gbn, -0.671, 0.671) if r != "B0" else (float("nan"),) * 3
        si = H.band_edges(sbn, -0.15, 0.15); so = H.band_edges(sbn, -0.30, 0.30)
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]; sstar = R_["s"]; eq = R_["alpha_eq"]
        extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], gi[0], gi[1], go_[0], go_[1], si[0], si[1], so[0], so[1],
                 R_["delta_floor"], R_["delta_to_s1"], st, R_["resolution"], R_["alpha"], R_["alpha_D1"], eq["FLAT"], eq["PROXY"], eq["H(z)"], R_["vacuous"], R_["below_rival"], R_["M_star"], R_["M_gas"]]
        q_ = ({"B0": "stars only (Huang+25 SED M*, a lower limit)", "B1": "stars + the CO gas floor (alpha_CO,min 0.8; lower limits)", "B2": "stars + Galactic-conversion gas (sensitivity, not a limit)"}[r] + "; "
              + {"root": "has a root: s* is an UPPER bound (only if the stellar mass belongs to the disc whose rotation was measured)", "floor": "FLOOR: no root, D <= 1" + (" (robust against added gas)" if r == "B0" else ""), "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st]
              + f"; {R_['resolution']} (Monte Carlo no-root fraction {R_['frac_mc_noroot']:.2f})" + ("; VACUOUS" if R_["vacuous"] else "") + ("; ILL-CONDITIONED (|lever| >= 10)" if R_["ill"] else "; conditioned (|lever| < 10)")
              + f"; M* one SED fit (CIGALE, Chabrier, near-IR flag Y; {SIG_HI:.2f}/-{SIG_LO:.2f} dex) with two NIRCam peaks neither at the dust position; kinematic i {I_AD:.0f} vs thin-disc {I_F444W:.0f}/{I_870:.0f} deg; protocluster SSA22; F444W R_e {RE_STAR} kpc")
        rows.append(["CFG284", R_["label"], GCL[r], f"{Z:.4f}", f"{Z:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], "baryons are lower limits (B0, B1) or a conventional conversion (B2): s* is an upper bound only for B0 and B1", fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg284_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg284_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg284{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg284{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
