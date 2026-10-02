#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG285 -- ADF22.5 (ALPAKA 24, z = 3.094) with the MEASURED CO(1-0) gas of the 2026 ADF22-WEB paper (Umehata+2026, arXiv:2609.06679; A7: log L'CO(1-0) = 10.66 +- 0.03, log M_mol = 11.21 = 3.6 x L'):
  six rows at the measured L'(1-0): S0 stars only (= CFG284 B0), S1 stars + gas at alpha_CO 0.8 (a lower limit), S2 stars + gas at 3.6 (the published M_mol), G1 gas only at 0.8 (a lower limit that does not use the SED stellar mass),
  G2 gas only at 1.36 (the DSFG standard), G3 gas only at 3.6 (the published gas alone).  Stars (Huang+2025: log M* 10.64 +0.20/-0.36) and gas are Freeman discs of the measured F444W semi-major-axis R_e = 2.24 kpc (CFG284's geometry).

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG285_adf22_5_measured_gas/FROZEN_CRITERIA.md (e6a70d499) with the paper's record data_assembly/adf22_5_literature_2026-10-02/adf22web3_2609.06679_A7_values.csv.
  STAGE=A   the engineering pre-flight with real hand predictions: no velocity column is loaded.
  STAGE=B   the measurement (once, after stage A and this script are committed); STAGE=B MUTATE=1 (V_ext, sigma_ext x 2); STAGE=B SELFTEST=1 (fabricated V_ext on the law at s = 2; the real velocities are never loaded).
Points file: no_root = 1 only for a FLOOR; a CEILING (D > 1 but s* > 1000) is written s_star = 1000, no_root = 0, status = ceiling; `resolution` = RESOLVED-ROOT / RESOLVED-FLOOR / UNRESOLVED (Monte Carlo no-root fraction <= 0.16 / >= 0.84 / between).
Run: STAGE=A python3 .../cfg285_adf22_5_gas.py ; STAGE=B SELFTEST=1 python3 ... ; STAGE=B python3 ... ; STAGE=B MUTATE=1 python3 ...
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
LD = os.path.join(REPO, "data_assembly", "adf22_5_literature_2026-10-02")
LIT2P, LIT3P = os.path.join(LD, "adf22_5_literature_values.csv"), os.path.join(LD, "adf22web3_2609.06679_A7_values.csv")
dirs = {"samp": "alpaka1_sample.csv", "prop": "alpaka1_properties.csv", "geo": "alpaka1_geometry.csv", "obs": "alpaka1_alma_obs.csv"}
T = {k: pd.read_csv(os.path.join(AT, v)).set_index("id") for k, v in dirs.items()}
OUTER = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv"), usecols=["id", "z", "n_rings", "R_ext_arcsec", "R_ext_kpc", "Re_kpc_dashed_line"]).set_index("id")   # no velocity-bearing column
RING = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"), usecols=["id", "ring", "panel", "R_kpc"])
KINP = os.path.join(AT, "alpaka1_kinematics.csv")
LIT2 = pd.read_csv(LIT2P, dtype=str).set_index("quantity"); LIT3 = pd.read_csv(LIT3P, dtype=str).set_index("quantity")
P("sha256: " + ", ".join(f"{v} {H.sha(os.path.join(AT, v))}" for v in dirs.values()) + f", alpaka1_outer_summary.csv {H.sha(os.path.join(AT, 'alpaka1_digitised', 'alpaka1_outer_summary.csv'))}, adf22_5_literature_values.csv {H.sha(LIT2P)}, adf22web3_2609.06679_A7_values.csv {H.sha(LIT3P)}; velocity columns loaded: {STAGE == 'B' and not SELFTEST}")
KIN = pd.read_csv(KINP).set_index("id") if (STAGE == "B" and not SELFTEST) else None


def lit2(q, col="value"): return float(LIT2.loc[q, col])
def lit3(q, col="value"): return float(LIT3.loc[q, col])


s, p, ge, ob, ou = T["samp"].loc[ID], T["prop"].loc[ID], T["geo"].loc[ID], T["obs"].loc[ID], OUTER.loc[ID]
Z = float(s["z"]); NAME = str(s["name"])
LP32_ALPAKA = float(p["lprime_1e10_kkmspc2"]) * 1e10; ELP32 = float(p["e_lprime"]) * 1e10
I_AD = float(ge["i_alma"]); E_I = 0.5 * (float(ge["e1.3"]) + float(ge["e2.3"]))
R_EXT = float(ou["R_ext_kpc"]); KPA = R_EXT / float(ou["R_ext_arcsec"])
rr = RING[(RING["id"] == ID) & (RING["panel"] == "V")].sort_values("ring"); R_MEAN = float(rr["R_kpc"].iloc[-2:].mean())
# --- the stellar record (CFG284) and the paper's gas record
MSTAR = lit2("Mstar"); EM_HI, EM_LO = lit2("Mstar", "err_hi"), lit2("Mstar", "err_lo")
LOGM0 = math.log10(MSTAR); SIG_HI = math.log10((MSTAR + EM_HI) / MSTAR); SIG_LO = -math.log10((MSTAR - EM_LO) / MSTAR)
RE_STAR, ERE_STAR, N_STAR, BA_STAR = lit2("F444W_Re"), lit2("F444W_Re", "err_hi"), lit2("F444W_sersic_n"), lit2("F444W_axis_ratio")
RE_DUST, BA_DUST = lit2("alma870_Re"), lit2("alma870_axis_ratio")
I_F444W, I_870 = math.degrees(math.acos(BA_STAR)), math.degrees(math.acos(BA_DUST))
RE_G = RE_STAR
LOGLP10, SLP10 = lit3("logLp_CO10"), lit3("logLp_CO10", "err_hi"); LP10 = 10 ** LOGLP10
LOGLP32P, R31, LOGMMOL = lit3("logLp_CO32"), lit3("r31"), lit3("logMmol")
SDV10, SDV32 = lit3("S_CO10_dv"), lit3("S_CO32_dv")
ALPHA = {"S0": 0.0, "S1": 0.8, "S2": 3.6, "G1": 0.8, "G2": 1.36, "G3": 3.6}
STARS = {"S0": True, "S1": True, "S2": True, "G1": False, "G2": False, "G3": False}
ROWS = ["S0", "S1", "S2", "G1", "G2", "G3"]
LABEL = {"S0": f"ALPAKA 24 {NAME} [stars only]", "S1": f"ALPAKA 24 {NAME} [stars + CO(1-0) gas a0.8]", "S2": f"ALPAKA 24 {NAME} [stars + CO(1-0) gas a3.6 (published)]",
         "G1": f"ALPAKA 24 {NAME} [CO(1-0) gas only a0.8]", "G2": f"ALPAKA 24 {NAME} [CO(1-0) gas only a1.36]", "G3": f"ALPAKA 24 {NAME} [CO(1-0) gas only a3.6 (published)]"}
FAMILY = {"S0": "stars only", "S1": "stars + gas", "S2": "stars + gas", "G1": "gas only", "G2": "gas only", "G3": "gas only"}
GCL = {"S0": "D (stars only: Huang+25 SED M*; no gas; lower limit)", "S1": "S (JVLA CO(1-0) L'; alpha_CO 0.8 lower limit) + SED M*", "S2": "S (JVLA CO(1-0) L'; alpha_CO 3.6 published M_mol) + SED M*",
       "G1": "S (JVLA CO(1-0) L'; alpha_CO 0.8 lower limit; no stars)", "G2": "S (JVLA CO(1-0) L'; alpha_CO 1.36 DSFG standard; no stars)", "G3": "S (JVLA CO(1-0) L'; alpha_CO 3.6 published M_mol; no stars)"}
LAWV = {k: H.LAWS[k](Z) for k in ("FLAT", "H(z)", "PROXY")}
VEXT = EVHI = EVLO = SIG = float("nan")
if STAGE == "B" and not SELFTEST:
    k = KIN.loc[ID]
    VEXT, EVHI, EVLO, SIG = float(k["vext_kms"]), float(k["vext_errhi"]), float(k["vext_errlo"]), float(k["sigma_ext_kms"])
P(f"row: ID {ID} {NAME} z {Z:.3f}  R_ext {R_EXT:.3f} kpc  i_ALMA {I_AD:.0f} +- {E_I:.0f} | gas: log L'(1-0) {LOGLP10} +- {SLP10} (L' {LP10:.4e}), log L'(3-2) paper {LOGLP32P}, ALPAKA L'(3-2) {LP32_ALPAKA:.3e}, r31 {R31}, published log M_mol {LOGMMOL} | stars: M* {MSTAR:.3e} (log {LOGM0:.5f} +{SIG_HI:.5f} -{SIG_LO:.5f}), R_e {RE_STAR} kpc | laws at z: FLAT {LAWV['FLAT']:.3f}, PROXY {LAWV['PROXY']:.3f}, H(z) {LAWV['H(z)']:.3f}")


# ---------------------------------------------------------------- geometry (CFG284's)
def b_proj(n): return float(gammaincinv(2 * n, 0.5))


def sigma_unit(R, n, Re):
    b = b_proj(n); Se = 1.0 / (2 * math.pi * n * math.exp(b) * b ** (-2 * n) * math.exp(gammaln(2 * n)) * Re ** 2)
    return Se * np.exp(-b * ((R / Re) ** (1.0 / n) - 1.0))


_HC = {}


def hankel_g_unit(n, Re, Rk, NRp=4000, Rmax_f=14.0, NK=24000, Kmax_f=60.0, chunk=2000):
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


def gobs_gbar(row="S0", vm="pub", inc="adopt", rad="ext", refac=1.0, sph=False, gas_fac=1.0, ts=0.0, tg=0.0, re_s=None, re_g=None, sersic=False, V=None, SG=None, Lp=None, Ms=None, i_deg=None, spec=None):
    """g_obs and g_bar [m s^-2] of a row (stars?, alpha_CO) under a knob setting; `spec` = (stars?, alpha) overrides the row; Ms / Lp may be arrays (the Monte Carlo)."""
    stars_, alpha_ = (STARS[row], ALPHA[row]) if spec is None else spec
    R = R_EXT if rad == "ext" else R_MEAN
    Ms_ = (MSTAR if Ms is None else Ms) * 10 ** ts
    Mg = alpha_ * (LP10 if Lp is None else Lp) * gas_fac * 10 ** tg
    Rs = (RE_STAR if re_s is None else re_s) * refac
    Rg = (RE_G if re_g is None else re_g) * refac
    f = H.gsph if sph else H.gdisc
    gstar = 0.0
    if stars_:
        gstar = Ms_ * float(hankel_g_unit(N_STAR, Rs, np.array([R]))[0]) if sersic else f(Ms_, Rs, R)
    gb = gstar + (f(Mg, Rg, R) if alpha_ > 0 else 0.0)
    go = None
    if STAGE == "B":
        sg = SIG if SG is None else SG
        V2 = (VEXT if V is None else V) ** 2 + {"pub": 0.0, "a168": 1.68 * sg ** 2, "a336": 3.36 * sg ** 2}[vm]
        i_new = i_deg if i_deg is not None else {"adopt": I_AD, "lo": max(5.0, I_AD - E_I), "hi": min(85.0, I_AD + E_I)}[inc]
        go = V2 * (math.sin(math.radians(I_AD)) / math.sin(math.radians(i_new))) ** 2 / R * H.G2SI
    return go, gb


GB = {r: float(gobs_gbar(r)[1]) for r in ROWS}
GSTAR = float(H.gdisc(MSTAR, RE_STAR, R_EXT)); GUN_GAS = float(H.gdisc(LP10, RE_G, R_EXT))            # stellar force; gas force per unit alpha_CO at the measured L'(1-0)
Y = {r: GB[r] / A0C for r in ROWS}
NUY = {r: float(NU(np.array([Y[r]]))[0]) for r in ROWS}
P("baryon side: " + "; ".join(f"{r} ({FAMILY[r]}, alpha {ALPHA[r]}): g_bar {GB[r]:.4e} y {Y[r]:.3f}" for r in ROWS) + f"; g_* {GSTAR:.4e}; gas force per unit alpha_CO {GUN_GAS:.4e}")

KNOB_LIST = [("R_e x1.5 (stars and gas)", dict(refac=1.5)), ("R_e /1.5 (stars and gas)", dict(refac=1 / 1.5)), ("stars R_e +1 sigma", dict(re_s=RE_STAR + ERE_STAR)), ("stars R_e -1 sigma", dict(re_s=RE_STAR - ERE_STAR)),
             ("spherical (enclosed mass as a point mass)", dict(sph=True)), ("gas at R_ext/1.2 (CFG283's R_e)", dict(re_g=R_EXT / 1.2)), ("gas at the 870 um dust R_e", dict(re_g=RE_DUST)), ("stars as the Sersic n = 3.21 thin disc (Hankel)", dict(sersic=True)),
             ("pressure +1.68 sigma^2", dict(vm="a168")), ("pressure +3.36 sigma^2", dict(vm="a336")),
             ("inclination -1 sigma", dict(inc="lo")), ("inclination +1 sigma", dict(inc="hi")), (f"inclination from the F444W axis ratio ({I_F444W:.1f} deg)", dict(i_deg=I_F444W)), (f"inclination from the 870 um axis ratio ({I_870:.1f} deg)", dict(i_deg=I_870)),
             ("V_ext at R_mean of the last two rings", dict(rad="mean")), ("kernel P2", dict(nu=NUP2)), ("M* x 10^-0.30", dict(ts=-0.30)), ("M* x 10^+0.30", dict(ts=+0.30)), ("M* x 10^-0.50 (AGN contamination)", dict(ts=-0.50)),
             ("gas: helium x 1.36", dict(gas_fac=1.36))]
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
    """alpha_CO (applied to the measured L'(1-0)) at which the median residual is zero for a law with a0 = s_law x canonical, given the stellar force gstar (0 for the gas-only family); nan if no non-negative conversion exists"""
    hi = (go - gstar) / GUN_GAS
    if hi <= 0: return float("nan")
    def too_high(a):                                                         # True if s*(alpha) is above the law, i.e. more gas is needed
        gb = gstar + a * GUN_GAS; ls, st = H.s_status(np.array([go / gb]), np.array([gb]))
        if st == "ceiling": return True
        if st == "floor": return False
        return ls > math.log10(s_law)
    if gstar > 0 and not too_high(0.0): return float("nan")                  # even the stars alone give s* below the law
    lo = 0.0 if gstar > 0 else 1e-6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if too_high(mid): lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)


# ================================================================== STAGE A
if STAGE == "A":
    P("\nSTAGE A  THE ENGINEERING PRE-FLIGHT (no velocity column is loaded; no g_obs, D, delta or s* is formed)")
    d_m = abs(math.log10(3.6 * LP10) - LOGMMOL); d_r = abs((LOGLP32P - LOGLP10) - math.log10(R31)); d_l32 = abs(10 ** LOGLP32P - LP32_ALPAKA) / ELP32
    d_ms = max(abs(lit3("logMstar") - LOGM0), abs(lit3("logMstar", "err_hi") - SIG_HI), abs(lit3("logMstar", "err_lo") - SIG_LO))
    check("C1 CONTROL: the paper's record is self-consistent: log(3.6 L'(1-0)) equals the published log M_mol to 0.01 dex; log L'(3-2) - log L'(1-0) equals log r31 to 0.02 dex; the paper's L'(3-2) equals ALPAKA's table value within its 1 sigma; the stellar mass and its errors in the paper's Table 1 equal CFG284's record to the table's rounding (0.006 dex)",
          f"|log(3.6 L') - log M_mol| {d_m:.4f}; |log r31 check| {d_r:.4f}; |L'(3-2) paper - ALPAKA| / sigma {d_l32:.2f}; M* differences {d_ms:.4f} dex", d_m < 0.01 and d_r < 0.02 and d_l32 < 1.0 and d_ms < 0.006 and all(np.isfinite([LOGLP10, SLP10, R31, LOGMMOL, MSTAR, RE_STAR])))
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
        ls, unb = H.s_star(NU(np.array([GB["S1"] / (A0C * st_)])), np.array([GB["S1"]])); d4 = max(d4, abs(ls - math.log10(st_)) if not unb else 9.0)
    check("C4 CONTROL: the noiseless world D = nu(g_bar / (a0 s_true)) returns s_true to 1e-6 dex for s_true = 0.5, 1, 2.5 on the S1 baryons", f"max |d log10 s| {d4:.1e}", d4 < 1e-6)
    r284 = json.load(open(os.path.join(CFG, "CFG284_adf22_5_with_stars", "cfg284_stageB_results.json")))["numbers"]["rows"]
    d5 = abs(GB["S0"] / r284["B0"]["GB"] - 1)
    check("C5 CONTINUITY with CFG284: the S0 g_bar equals CFG284's committed B0 g_bar to 1e-9 relative (only the baryon value is read)", f"relative deviation {d5:.1e} ({GB['S0']:.6e} vs {r284['B0']['GB']:.6e})", d5 < 1e-9)
    r283 = json.load(open(os.path.join(CFG, "CFG283_alpaka24_gas_only", "cfg283_stageB_results.json")))["numbers"]["rows"]
    c5b = float(gobs_gbar(spec=(False, 0.8), Lp=LP32_ALPAKA, re_g=R_EXT / 1.2)[1]); d5b = abs(c5b / r283["B1"]["GB"] - 1)
    check("C5b CONTINUITY with CFG283: gas only at 0.8 x the ALPAKA L'(3-2) in the R_ext/1.2 disc equals CFG283's committed B1 g_bar to 1e-9 relative", f"relative deviation {d5b:.1e} ({c5b:.6e} vs {r283['B1']['GB']:.6e})", d5b < 1e-9)
    nuo = 115.2712 / (1 + 3.09536); DLa, DLb = dl_mpc(3.09536), dl_mpc(3.09536, 70.0, 0.30)
    La = 3.25e7 * SDV10 * nuo ** -2 * DLa ** 2 * (1 + 3.09536) ** -3; Lb = 3.25e7 * SDV10 * nuo ** -2 * DLb ** 2 * (1 + 3.09536) ** -3
    check("C6 CONTROL (load-bearing): the tabulated L'(1-0) equals the line-flux formula L' = 3.25e7 S dv nu_obs^-2 D_L^2 (1+z)^-3 (nu_rest 115.2712 GHz) to 0.05 dex for flat LCDM 67.4 / 0.315 and for the paper's 70 / 0.30",
          f"S dv = {SDV10} Jy km/s; nu_obs {nuo:.3f} GHz; D_L {DLa:.1f} / {DLb:.1f} Mpc; formula {La:.3e} / {Lb:.3e} vs table {LP10:.3e} (log differences {math.log10(La / LP10):+.3f} / {math.log10(Lb / LP10):+.3f})", abs(math.log10(La / LP10)) < 0.05 and abs(math.log10(Lb / LP10)) < 0.05)
    P("\nA1  BARYON SIDE AND THE CFG240 READING (noiseless world; lever = d log10 s* / d(baryon dex); ILL-CONDITIONED iff |lever| >= 10 or not computable)")
    ILL, LEV = {}, {}
    for r in ROWS:
        lv, fl = H.lever1(np.array([NUY[r]]), np.array([GB[r]])); LEV[r] = lv; ILL[r] = bool(fl or abs(lv) >= 10)
        P(f"    {r} ({FAMILY[r]}, alpha {ALPHA[r]}): g_bar {GB[r]:.3e}  y {Y[r]:.3f}  nu(y) {NUY[r]:.4f}  lever {lv:+.2f}{' (flag)' if fl else ''}  {'ILL-CONDITIONED' if ILL[r] else 'conditioned'}")
    P("\nA2  KNOB EFFECTS ON g_bar (dex relative to the nominal; baryon side only; " + " / ".join(ROWS) + ")")
    A2 = {}
    for nm, kw in KNOB_LIST:
        if KGROUP[nm] in ("pressure", "inclination", "kernel") or nm.startswith("V_ext"): continue
        kk = {k_: v_ for k_, v_ in kw.items() if k_ != "nu"}
        A2[nm] = [math.log10(float(gobs_gbar(r, **kk)[1]) / GB[r]) for r in ROWS]
        P(f"    {nm}: " + " / ".join(f"{x_:+.3f}" for x_ in A2[nm]))
    P(f"\nA3  M_gas by row: " + ", ".join(f"{r} {ALPHA[r] * LP10:.3e}" for r in ROWS if ALPHA[r] > 0) + f"; M* {MSTAR:.3e}; the thin-disc inclinations {I_F444W:.1f} / {I_870:.1f} deg against the kinematic {I_AD:.0f} +- {E_I:.0f}: g_obs factors {(math.sin(math.radians(I_AD)) / math.sin(math.radians(I_F444W))) ** 2:.3f} / {(math.sin(math.radians(I_AD)) / math.sin(math.radians(I_870))) ** 2:.3f} (no velocity)")
    pfd1 = all(ok for n, ok, lb in CHK if lb)
    P("\nDECISIONS (the frozen map)"); P(f"  PF-D1 ESTIMATOR, GEOMETRY AND BARYON SIDE VALIDATED: {pfd1} (controls C1-C6, C5b)")
    he = {"HE1": bool(4.1 <= Y["G1"] <= 4.5 and 7.0 <= Y["G2"] <= 7.7 and 18.7 <= Y["G3"] <= 20.1 and 9.2 <= Y["S1"] <= 9.8 and 23.5 <= Y["S2"] <= 25.7 and abs(Y["S0"] - 5.19) < 0.02)}
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 9; HE2-HE9 are scored at stage B):")
    P(f"    HE1: y: G1 in [4.1, 4.5], G2 in [7.0, 7.7], G3 in [18.7, 20.1], S1 in [9.2, 9.8], S2 in [23.5, 25.7], S0 = 5.19: {'hit' if he['HE1'] else 'MISS (kept as it falls)'}  (y {', '.join(f'{r} {Y[r]:.3f}' for r in ROWS)})")
    NUM.update(inputs=dict(z=Z, LP10=LP10, SLP10=SLP10, R_ext=R_EXT, R_mean=R_MEAN, i=I_AD, ei=E_I, Mstar=MSTAR, GB=GB, GSTAR=GSTAR, GUN_GAS=GUN_GAS, y=Y, nuy=NUY, La=La, Lb=Lb, i_F444W=I_F444W, i_870=I_870), lever=LEV, ill=ILL, knob_gbar_dex=A2, hand_estimates=he, pf=dict(PF_D1=bool(pfd1)))

# ================================================================== STAGE B
if STAGE == "B":
    P("\nSTAGE B  THE MEASUREMENT" + (" (SELFTEST)" if SELFTEST else "") + (" (MUTATE: V_ext and sigma_ext x 2)" if MUTATE else ""))
    rngS = np.random.default_rng(2850)
    if SELFTEST:
        gob = GB["S1"] * float(NU(np.array([GB["S1"] / (2.0 * A0C)]))[0]) * 10 ** rngS.normal(0, 0.15)
        VEXT = math.sqrt(gob * R_EXT / H.G2SI); EVHI = EVLO = 0.10 * VEXT; SIG = 0.10 * VEXT
        P("SELFTEST: V_ext fabricated from the law at s_true = 2 on the S1 baryons (+0.15 dex scatter on g_obs); the real velocities are not used")
    if MUTATE:
        VEXT *= 2.0; EVHI *= 2.0; EVLO *= 2.0; SIG *= 2.0
    RES = {}

    def solve(row, **kw):
        kw = dict(kw); nu = kw.pop("nu", NU)
        go, gb = gobs_gbar(row, **kw)
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
        Lpd = 10 ** H.split_normal(rng, LOGLP10, SLP10, SLP10, n)
        Msd = 10 ** H.split_normal(rng, LOGM0, SIG_HI, SIG_LO, n)
        return Vd ** 2 / R_EXT * H.G2SI * facd, Lpd, Msd

    def gbar_draws(stars_, alpha_, Lpd, Msd):
        return (H.gdisc(Msd, RE_STAR, R_EXT) if stars_ else 0.0) + (H.gdisc(alpha_ * Lpd, RE_G, R_EXT) if alpha_ > 0 else 0.0)

    def mc_fraction(stars_, alpha_, go_nom, seed_label, B=B_MC):
        """Monte Carlo no-root fraction for an arbitrary (stars?, alpha) set (the ladder); same draws as a main row"""
        rng = np.random.default_rng(zlib.crc32(seed_label.encode()) % 100000)
        god, Lpd, Msd = mc_draws(rng, VEXT, EVHI, EVLO, B); gbd = gbar_draws(stars_, alpha_, Lpd, Msd)
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C)
        return float(np.mean(ud))

    MDYN = VEXT ** 2 * R_EXT / H.G_KPC
    gobs_nom = float(gobs_gbar("S0")[0]); gstar_nom = float(gobs_gbar("S0")[1])
    for r in ROWS:
        lab = LABEL[r]; stars_, alpha_ = STARS[r], ALPHA[r]
        ls0, st0, go0, gb0 = solve(r); D0 = go0 / gb0
        rng = np.random.default_rng(zlib.crc32(("285|" + lab).encode()) % 100000)
        god, Lpd, Msd = mc_draws(rng, VEXT, EVHI, EVLO, B_MC)
        gbd = gbar_draws(stars_, alpha_, Lpd, Msd)
        lsd, ud = H.AI.implied((god / gbd)[:, None], gbd[:, None], NU, A0C); q, frn = H.rooted_pct(lsd, ud)
        Dd = god / gbd
        frac_floor = float(np.mean(ud & (Dd <= 1.0))); frac_ceiling = float(np.mean(ud & (Dd > 1.0)))
        dFd = np.log10(god / (gbd * NU(gbd / A0C))); dq = [float(v) for v in np.percentile(dFd, [16, 84])]
        dF0 = float(np.log10(go0 / (gb0 * float(NU(np.array([gb0 / A0C]))[0]))))
        bands = H.band_solutions(np.array([D0]), np.array([gb0]))
        nan2 = (float("nan"), True)
        gas_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(r, tg=s_)[1])]), np.array([float(gobs_gbar(r, tg=s_)[1])])) for s_ in (-0.671, -0.213, 0.213, 0.671)} if alpha_ > 0 else {s_: nan2 for s_ in (-0.671, -0.213, 0.213, 0.671)}
        star_b = {s_: H.s_star(np.array([go0 / float(gobs_gbar(r, ts=s_)[1])]), np.array([float(gobs_gbar(r, ts=s_)[1])])) for s_ in (-0.30, -0.15, 0.15, 0.30)} if stars_ else {s_: nan2 for s_ in (-0.30, -0.15, 0.15, 0.30)}
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
        gst = gstar_nom if stars_ else 0.0
        a_D1 = (go0 - gst) / GUN_GAS if go0 > gst else float("nan")
        eqs = {k_: eq_alpha(LAWV[k_], go0, gst) for k_ in ("FLAT", "PROXY", "H(z)")}
        sval = H.s_val_status(ls0, st0)
        resol = "RESOLVED-ROOT" if frn <= 0.16 else ("RESOLVED-FLOOR" if frn >= 0.84 else "UNRESOLVED")
        lo95 = 10 ** q[0] if np.isfinite(q[0]) else float("nan"); hi95 = 10 ** q[4] if np.isfinite(q[4]) else float("nan")
        vac = int(resol == "RESOLVED-ROOT" and np.isfinite(lo95) and lo95 >= LAWV["H(z)"])
        below = int(resol == "RESOLVED-ROOT" and np.isfinite(hi95) and hi95 < LAWV["H(z)"])
        RES[r] = dict(row=r, label=lab, family=FAMILY[r], alpha=alpha_, z=Z, GO=go0, GB=gb0, D=D0, y=Y[r], ls=ls0, status=st0, s=sval, q=q, frac_mc_noroot=frn, frac_mc_floor=frac_floor, frac_mc_ceiling=frac_ceiling, resolution=resol, delta_FLAT=dF0, dF_lo68=dq[0], dF_hi68=dq[1],
                      bands={f"{k_:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in bands.items()}, gas_bands={f"{k_:+.3f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in gas_b.items()},
                      star_bands={f"{k_:+.2f}": dict(ls=v[0], unb=v[1], s=H.s_val(*v)) for k_, v in star_b.items()}, knobs=kn, knob_D_dex=kD, knob_status=kst, group_max=gmax, recipe_half=half, n_knobs_with_root=n_root, n_knobs_to_floor=n_floor, n_knobs=len(KNOB_LIST),
                      lever=lv_nl, ill=bool(lf_nl or (np.isfinite(lv_nl) and abs(lv_nl) >= 10)), delta_floor=dflo, delta_to_s1=d1, alpha_D1=a_D1, alpha_eq=eqs, vacuous=vac, below_rival=below, M_gas=alpha_ * LP10, M_star=MSTAR if stars_ else 0.0)
        R_ = RES[r]
        P(f"  {lab}: g_obs {go0:.4e}  g_bar {gb0:.4e}  D {D0:.4f}  delta_FLAT {dF0:+.3f} [{dq[0]:+.3f}, {dq[1]:+.3f}]  y {Y[r]:.3f}  status {st0.upper()}" + (f"  s* <= {10 ** ls0:.4g} (a0 <= {10 ** ls0 * 0.93603:.4g}e-10)" if st0 == "root" else "") + f"  [{resol}]")
        P(f"      Monte Carlo (B = {B_MC}): draws without a root {frn:.3f} (floor {frac_floor:.3f}, ceiling {frac_ceiling:.3f}); rooted 68 % [{10 ** q[1] if np.isfinite(q[1]) else float('nan'):.4g}, {10 ** q[3] if np.isfinite(q[3]) else float('nan'):.4g}]  95 % [{lo95:.4g}, {hi95:.4g}]  median {10 ** q[2] if np.isfinite(q[2]) else float('nan'):.4g}")
        b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        P(f"      bands: all baryons +-0.15 [{b15[0]:.4g}, {b15[1]:.4g}]{' (no-root corner)' if b15[2] else ''}  +-0.30 [{b30[0]:.4g}, {b30[1]:.4g}]{' (no-root corner)' if b30[2] else ''}")
        P(f"      Delta_floor {dflo:+.3f} dex; baryon shift for s* = 1: {d1:+.3f} dex; alpha_CO (x L'(1-0)) at D = 1: {a_D1:.4f}; for FLAT {eqs['FLAT']:.4f}, PROXY {eqs['PROXY']:.4f}, H(z) {eqs['H(z)']:.4f}; lever (noiseless) {lv_nl:+.2f}{' ILL-CONDITIONED' if R_['ill'] else ' (conditioned)'}; variants with a root {n_root}/{len(KNOB_LIST)} (to a floor {n_floor}); recipe half-width {half:.3f}" + ("; VACUOUS (D2)" if vac else "") + ("; BELOW THE RIVAL (D3)" if below else ""))
        P("      knobs (Delta log10 s*; -- = the base or the variant has no root; [status; Delta log10 D]): " + "; ".join(f"{nm} " + ("--" if kn[nm] is None else f"{kn[nm]:+.3f}") + f" [{kst[nm]}; {kD[nm]:+.3f}]" for nm, _ in KNOB_LIST))
        P("      knob groups (max |Delta log10 s*|): " + (", ".join(f"{g_} {v:.3f}" for g_, v in gmax.items()) if gmax else "none (no root at the base)"))
    MGAS = {r: ALPHA[r] * LP10 for r in ROWS}
    P(f"\n  context: M_dyn(< R_ext) = V_ext^2 R_ext / G = {MDYN:.3e} Msun (a scale); (M* + M_gas(0.8))/M_dyn {(MSTAR + MGAS['S1']) / MDYN:.3f}; (M* + M_gas(3.6))/M_dyn {(MSTAR + MGAS['S2']) / MDYN:.3f}; M_gas(3.6)/M_dyn {MGAS['G3'] / MDYN:.3f}; M*/M_dyn {MSTAR / MDYN:.3f}")
    NUM["context"] = dict(M_dyn=MDYN, S1_over_Mdyn=(MSTAR + MGAS["S1"]) / MDYN, S2_over_Mdyn=(MSTAR + MGAS["S2"]) / MDYN, G3_over_Mdyn=MGAS["G3"] / MDYN)
    # ---------------------------------------------------------------- the conversion ladder (main run only): assumed conversions, not data
    if not MUTATE and not SELFTEST:
        lad = []
        P("\n  CONVERSION LADDER (assumed alpha_CO x the measured L'(1-0); NOT data): nominal D, status, s*, Monte Carlo no-root fraction, resolution")
        for fam, st_ in (("gas only", False), ("stars + gas", True)):
            for a_ in (0.8, 1.0, 1.36, 2.1, 3.6, 4.36):
                go_l, gb_l = gobs_gbar(spec=(st_, a_)); D_l = go_l / gb_l; ls_l, stt = H.s_status(np.array([D_l]), np.array([gb_l]))
                fr = mc_fraction(st_, a_, go_l, f"285|ladder|{fam}|{a_}")
                rs = "RESOLVED-ROOT" if fr <= 0.16 else ("RESOLVED-FLOOR" if fr >= 0.84 else "UNRESOLVED")
                lad.append(dict(family=fam, alpha=a_, D=D_l, status=stt, s=H.s_val_status(ls_l, stt), frac_mc_noroot=fr, resolution=rs))
                P(f"    {fam:12s} alpha {a_:5.2f}: M_gas {a_ * LP10:.3e}  D {D_l:.3f}  {stt.upper():5s}" + (f"  s* <= {10 ** ls_l:.3g}" if stt == "root" else "          ") + f"  no-root {fr:.3f}  {rs}")
        NUM["ladder"] = lad
    # ---------------------------------------------------------------- SELFTEST: 100 worlds per set on the law at s_true = 2
    if SELFTEST:
        NUM["selftest"] = {}
        for rs_ in ("G1", "S1"):
            P(f"\n  SELFTEST (100 worlds on the {rs_} baryons): V_ext fabricated from the law at s_true = 2, 0.15 dex scatter on g_obs, 10 % V errors; Monte Carlo B = 1,000 per world; the L'(1-0) and M* errors drawn as in the main run")
            rW = np.random.default_rng(28500 + (0 if rs_ == "G1" else 1)); cnt = {"root": 0, "floor": 0, "ceiling": 0}; sroot, cover = [], 0
            for w in range(100):
                gobw = GB[rs_] * float(NU(np.array([GB[rs_] / (2.0 * A0C)]))[0]) * 10 ** rW.normal(0, 0.15)
                Vw = math.sqrt(gobw * R_EXT / H.G2SI)
                lsw, stw = H.s_status(np.array([gobw / GB[rs_]]), np.array([GB[rs_]])); cnt[stw] += 1
                if stw != "root": continue
                godw, Lpdw, Msdw = mc_draws(rW, Vw, 0.10 * Vw, 0.10 * Vw, 1000); gbdw = gbar_draws(STARS[rs_], ALPHA[rs_], Lpdw, Msdw)
                lsdw, udw = H.AI.implied((godw / gbdw)[:, None], gbdw[:, None], NU, A0C); qw, _ = H.rooted_pct(lsdw, udw)
                sroot.append(10 ** lsw)
                if np.isfinite(qw[0]) and qw[0] <= math.log10(2.0) <= qw[4]: cover += 1
            nroot = cnt["root"]
            P(f"    status of the fabricated worlds: root {cnt['root']}, floor {cnt['floor']}, ceiling {cnt['ceiling']}; of the {nroot} rooted worlds the 95 % interval contains s = 2 in {cover}; s* of the rooted worlds: median {np.median(sroot):.3g}, 16-84 % [{np.percentile(sroot, 16):.3g}, {np.percentile(sroot, 84):.3g}]" if nroot else "    no rooted world")
            NUM["selftest"][rs_] = dict(counts=cnt, rooted=nroot, covered=cover, s_median=float(np.median(sroot)) if nroot else None, s_16_84=[float(np.percentile(sroot, 16)), float(np.percentile(sroot, 84))] if nroot else None)
    NUM["rows"] = RES
    P("\nCONTROLS (stage B)")
    if MUTATE:
        main = json.load(open(os.path.join(HERE, "cfg285_stageB_results.json")))["numbers"]["rows"]
        bad = 0.0; nm_ = 0; n0 = sum(1 for r in ROWS if main[r]["status"] == "root")
        for r in ROWS:
            R_ = RES[r]
            if R_["status"] == "root":
                nm_ += 1; bad = max(bad, abs(math.log10(R_["GB"] / inv_nu(R_["D"]) / A0C) - R_["ls"]))
        check("M2 MUTATE=1 (reactivity): V_ext and sigma_ext x 2; rows with a root satisfy the closed-form inversion of their own (D, g_bar) to 1e-6 dex and their number is at least the main run's", f"rows with a root: mutated {nm_}, main {n0}; max |d log10 s*| against the independent inversion {bad:.1e}", bad < 1e-6 and nm_ >= n0)
    else:
        d1m = 0.0
        for r in ROWS:
            R_ = RES[r]
            if R_["status"] != "root": continue
            la, ua = H.AI.implied(np.array([R_["D"]]), np.array([R_["GB"]]), NU, A0A)
            if not ua[0]: d1m = max(d1m, abs(float(la[0]) + math.log10(A0A / A0C) - R_["ls"]))
        check("M1 CONTROL: the alt footing implies the same absolute a0 in every row with a root", f"max |d log10| = {d1m:.1e} ({sum(1 for r in ROWS if RES[r]['status'] == 'root')} rows with a root)", d1m < 1e-9)
        check("M3 six rows, all ID 24", f"rows {[RES[r]['label'] for r in ROWS]}", len(RES) == 6 and all(RES[r]["z"] == Z for r in ROWS))
        ok6 = True
        for fam in ("stars only", "stars + gas", "gas only"):
            mem = [r for r in ROWS if FAMILY[r] == fam]
            for key in ("D1", "FLAT", "PROXY", "H(z)"):
                v = [RES[r]["alpha_D1"] if key == "D1" else RES[r]["alpha_eq"][key] for r in mem]
                ok6 = ok6 and (all(np.isnan(v)) or (all(np.isfinite(v)) and max(abs(a / v[0] - 1) for a in v) < 1e-9))
        check("M6 CONTROL: the alpha_CO equivalents agree across the rows of a family (same stars or none, same gas disc) to 1e-9 relative", f"stars + gas D = 1: {[RES[r]['alpha_D1'] for r in ('S1', 'S2')]}; gas only D = 1: {[RES[r]['alpha_D1'] for r in ('G1', 'G2', 'G3')]}", ok6)
        worst = 0.0
        for r_ in ("S1", "G1"):
            for k_ in ("FLAT", "PROXY", "H(z)"):
                a_ = RES[r_]["alpha_eq"][k_]
                if np.isfinite(a_):
                    gbq = (gstar_nom if STARS[r_] else 0.0) + a_ * GUN_GAS; lq, _ = H.s_status(np.array([RES[r_]["GO"] / gbq]), np.array([gbq])); worst = max(worst, abs(lq - math.log10(LAWV[k_])))
        check("M7 CONTROL: each law-equivalent alpha_CO returns its law's s to 1e-6 dex when re-solved", f"max |d log10 s| {worst:.1e}", worst < 1e-6)
    if not MUTATE and not SELFTEST:
        r284 = json.load(open(os.path.join(CFG, "CFG284_adf22_5_with_stars", "cfg284_stageB_results.json")))["numbers"]["rows"]["B0"]
        d_go = abs(RES["S0"]["GO"] / r284["GO"] - 1); d_D = abs(RES["S0"]["D"] / r284["D"] - 1); d_s = abs(RES["S0"]["s"] / r284["s"] - 1)
        check("M5 CONTINUITY with CFG284: g_obs equals CFG284's committed GO, and S0's D and s* equal CFG284's B0, to 1e-9 relative", f"relative deviations g_obs {d_go:.1e}, D {d_D:.1e}, s* {d_s:.1e}", max(d_go, d_D, d_s) < 1e-9)
        r283 = json.load(open(os.path.join(CFG, "CFG283_alpaka24_gas_only", "cfg283_stageB_results.json")))["numbers"]["rows"]["B1"]
        go5, gb5 = gobs_gbar(spec=(False, 0.8), Lp=LP32_ALPAKA, re_g=R_EXT / 1.2); d5b = abs((go5 / gb5) / r283["D"] - 1)
        check("M5b CONTINUITY with CFG283: with the stars removed, L'(1-0) replaced by the ALPAKA L'(3-2), alpha 0.8 and R_e = R_ext/1.2 the gas-only D equals CFG283's committed D_B1 to 1e-9 relative", f"relative deviation {d5b:.1e}", d5b < 1e-9)
    # ---------------------------------------------------------------- hand estimates scored (frozen in section 9)
    he = {}
    S0_, S1_, S2_, G1_, G2_, G3_ = (RES[r] for r in ROWS)
    if not MUTATE and not SELFTEST:
        he["HE2"] = bool(1.95 <= G1_["D"] <= 2.20 and G1_["status"] == "root" and 8.0 <= G1_["s"] <= 12.5 and 1.15 <= G2_["D"] <= 1.30 and G2_["status"] == "root" and 1.8 <= G2_["s"] <= 3.6 and 0.42 <= G3_["D"] <= 0.49 and G3_["status"] == "floor"
                         and 0.90 <= S1_["D"] <= 0.99 and S1_["status"] == "floor" and 0.33 <= S2_["D"] <= 0.39 and S2_["status"] == "floor")
        he["HE3"] = bool(G1_["frac_mc_noroot"] <= 0.02 and 0.02 <= G2_["frac_mc_noroot"] <= 0.15 and G3_["frac_mc_noroot"] >= 0.99 and 0.40 <= S1_["frac_mc_noroot"] <= 0.70 and S2_["frac_mc_noroot"] >= 0.99
                         and G1_["resolution"] == "RESOLVED-ROOT" and G2_["resolution"] == "RESOLVED-ROOT" and G3_["resolution"] == "RESOLVED-FLOOR" and S2_["resolution"] == "RESOLVED-FLOOR" and S1_["resolution"] == "UNRESOLVED")
        eS, eG = S1_["alpha_eq"], G1_["alpha_eq"]
        he["HE4"] = bool(0.65 <= S1_["alpha_D1"] <= 0.75 and 0.52 <= eS["FLAT"] <= 0.63 and 0.33 <= eS["PROXY"] <= 0.42 and 0.13 <= eS["H(z)"] <= 0.20 and 1.55 <= G1_["alpha_D1"] <= 1.75 and 1.45 <= eG["FLAT"] <= 1.65 and 1.20 <= eG["PROXY"] <= 1.45 and 1.00 <= eG["H(z)"] <= 1.25)
        lad = {(d_["family"], d_["alpha"]): d_ for d_ in NUM["ladder"]}
        he["HE5"] = bool(all(lad[("gas only", a_)]["status"] == "root" for a_ in (0.8, 1.0, 1.36)) and all(lad[("gas only", a_)]["status"] == "floor" for a_ in (2.1, 3.6, 4.36)) and all(lad[("stars + gas", a_)]["status"] == "floor" for a_ in (0.8, 1.0, 1.36, 2.1, 3.6, 4.36)))
        kn1, ks1 = G1_["knobs"], G1_["knob_status"]; nm_f444 = f"inclination from the F444W axis ratio ({I_F444W:.1f} deg)"; nm_870 = f"inclination from the 870 um axis ratio ({I_870:.1f} deg)"
        he["HE6"] = bool(0.35 <= G1_["recipe_half"] <= 0.75 and all(ks1[n_] == "root" and kn1[n_] is not None and 0.25 <= kn1[n_] <= 0.45 for n_ in (nm_f444, nm_870)) and ks1["R_e x1.5 (stars and gas)"] == "root" and 0.2 <= kn1["R_e x1.5 (stars and gas)"] <= 0.4
                         and ks1["gas: helium x 1.36"] == "root" and -0.4 <= kn1["gas: helium x 1.36"] <= -0.2)
        he["HE9"] = bool(1.00 <= (MSTAR + MGAS["S1"]) / MDYN <= 1.12 and 2.6 <= (MSTAR + MGAS["S2"]) / MDYN <= 2.9 and 2.0 <= MGAS["G3"] / MDYN <= 2.3)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE2 (nominal D, status, s*: G1 1.95-2.20 / root / 8-12.5; G2 1.15-1.30 / root / 1.8-3.6; G3 0.42-0.49 / floor; S1 0.90-0.99 / floor; S2 0.33-0.39 / floor): {'hit' if he['HE2'] else 'MISS (kept as it falls)'}  (D {', '.join(f'{r} {RES[r]['D']:.4f}' for r in ROWS)}; s* G1 {G1_['s']:.4g}, G2 {G2_['s']:.4g})")
        P(f"    HE3 (no-root fractions G1 <= 0.02, G2 0.02-0.15, G3 >= 0.99, S1 0.40-0.70, S2 >= 0.99; resolutions): {'hit' if he['HE3'] else 'MISS (kept as it falls)'}  ({', '.join(f'{r} {RES[r]['frac_mc_noroot']:.3f} {RES[r]['resolution']}' for r in ROWS)})")
        P(f"    HE4 (equivalents: stars+gas D=1 0.65-0.75, FLAT 0.52-0.63, PROXY 0.33-0.42, H(z) 0.13-0.20; gas only D=1 1.55-1.75, FLAT 1.45-1.65, PROXY 1.20-1.45, H(z) 1.00-1.25): {'hit' if he['HE4'] else 'MISS (kept as it falls)'}  (stars+gas {S1_['alpha_D1']:.4f}; {eS['FLAT']:.4f}, {eS['PROXY']:.4f}, {eS['H(z)']:.4f}; gas only {G1_['alpha_D1']:.4f}; {eG['FLAT']:.4f}, {eG['PROXY']:.4f}, {eG['H(z)']:.4f})")
        P(f"    HE5 (ladder: gas only root at 0.8/1.0/1.36 and floor at 2.1/3.6/4.36; stars + gas floor everywhere): {'hit' if he['HE5'] else 'MISS (kept as it falls)'}")
        P(f"    HE6 (G1 knobs: half-width 0.35-0.75; thin-disc inclinations +0.25..+0.45; R_e x1.5 +0.2..+0.4; helium -0.2..-0.4): {'hit' if he['HE6'] else 'MISS (kept as it falls)'}  (half {G1_['recipe_half']:.3f}; groups {G1_['group_max']})")
        P(f"    HE9 (context: (M*+M_gas(0.8))/M_dyn 1.00-1.12; (M*+M_gas(3.6))/M_dyn 2.6-2.9; M_gas(3.6)/M_dyn 2.0-2.3): {'hit' if he['HE9'] else 'MISS (kept as it falls)'}  ({(MSTAR + MGAS['S1']) / MDYN:.3f}, {(MSTAR + MGAS['S2']) / MDYN:.3f}, {MGAS['G3'] / MDYN:.3f})")
    if MUTATE:
        he["HE7"] = bool(G1_["status"] == "root" and 180 <= G1_["s"] <= 360 and G2_["status"] == "root" and 95 <= G2_["s"] <= 190 and S1_["status"] == "root" and 70 <= S1_["s"] <= 140 and S2_["status"] == "root" and 12 <= S2_["s"] <= 28 and G3_["status"] == "root" and 22 <= G3_["s"] <= 45)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE7 (MUTATE=1: G1 180-360, G2 95-190, S1 70-140; S2 gains a root 12-28; G3 gains a root 22-45): {'hit' if he['HE7'] else 'MISS (kept as it falls)'}  ({', '.join(f'{r} {RES[r]['status']} {RES[r]['s']:.4g}' for r in ROWS)})")
    if SELFTEST:
        f1 = NUM["selftest"]["G1"]["counts"]["floor"] / 100.0; f2 = NUM["selftest"]["S1"]["counts"]["floor"] / 100.0
        he["HE8"] = bool(0.10 <= f1 <= 0.35 and 0.25 <= f2 <= 0.50)
        P("\nHAND ESTIMATES SCORED (frozen in FROZEN_CRITERIA.md section 9):")
        P(f"    HE8 (SELFTEST: the fraction of worlds at the floor in [10 %, 35 %] on the G1 baryons and [25 %, 50 %] on the S1 baryons): {'hit' if he['HE8'] else 'MISS (kept as it falls)'}  ({f1:.2f}, {f2:.2f})")
    NUM["hand_estimates_B"] = he
    # ---------------------------------------------------------------- the points file
    cols = H.CHART_HEADER + ["recipe_half_dex", "recipe_lo", "recipe_hi", "n_knobs_with_root", "y", "lever", "ill_conditioned", "delta_FLAT", "delta_FLAT_lo68", "delta_FLAT_hi68", "D", "frac_mc_noroot", "frac_mc_ceiling",
                              "gas_in_lo", "gas_in_hi", "gas_out_lo", "gas_out_hi", "star_in_lo", "star_in_hi", "star_out_lo", "star_out_hi", "delta_floor", "delta_to_s1", "status", "resolution", "family", "alpha_CO", "alpha_CO_at_D1", "alpha_CO_FLAT",
                              "alpha_CO_PROXY", "alpha_CO_Hz", "vacuous", "below_rival", "M_star", "M_gas", "limit", "flags_FLAT", "flags_H(z)", "flags_PROXY", "quality"]
    check("M4 CONTROL: the first 18 columns of the points file equal chart_a0z_points.csv's header", f"{H.chart_header_check()}", H.chart_header_check())
    rows = []
    for r in ROWS:
        R_ = RES[r]; st = R_["status"]; q = R_["q"]; nanE = (float("nan"),) * 3
        bands = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["bands"].items()}; b15 = H.band_edges(bands, -0.15, 0.15); b30 = H.band_edges(bands, -0.30, 0.30)
        gbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["gas_bands"].items()}; sbn = {float(k_): (v["ls"], v["unb"]) for k_, v in R_["star_bands"].items()}
        gi = H.band_edges(gbn, -0.213, 0.213) if ALPHA[r] > 0 else nanE; go_ = H.band_edges(gbn, -0.671, 0.671) if ALPHA[r] > 0 else nanE
        si = H.band_edges(sbn, -0.15, 0.15) if STARS[r] else nanE; so = H.band_edges(sbn, -0.30, 0.30) if STARS[r] else nanE
        empty = 1000.0 if st == "ceiling" else FLOOR
        lo68, hi68 = (10 ** q[1], 10 ** q[3]) if np.isfinite(q[1]) else (empty, empty); lo95, hi95 = (10 ** q[0], 10 ** q[4]) if np.isfinite(q[0]) else (empty, empty)
        fl = H.flags_for(Z, lo95, hi95, b15[:2], b30[:2], st == "root"); half = R_["recipe_half"]; sstar = R_["s"]; eq = R_["alpha_eq"]
        extra = [R_["y"], R_["lever"], int(R_["ill"]), R_["delta_FLAT"], R_["dF_lo68"], R_["dF_hi68"], R_["D"], R_["frac_mc_noroot"], R_["frac_mc_ceiling"], gi[0], gi[1], go_[0], go_[1], si[0], si[1], so[0], so[1],
                 R_["delta_floor"], R_["delta_to_s1"], st, R_["resolution"], R_["family"], R_["alpha"], R_["alpha_D1"], eq["FLAT"], eq["PROXY"], eq["H(z)"], R_["vacuous"], R_["below_rival"], R_["M_star"], R_["M_gas"]]
        lim = "baryons are lower limits (alpha_CO 0.8 and/or stars only): s* is an upper bound" if r in ("S0", "S1", "G1") else "a conversion-dependent class-S row (alpha_CO 1.36 or 3.6): not a limit"
        q_ = (f"{R_['family']}; alpha_CO {R_['alpha']}; " + {"root": "has a root" + (": s* is an UPPER bound" if r in ("S0", "S1", "G1") else " (a conversion-dependent row)"), "floor": "FLOOR: no root, D <= 1" + (" (the published gas mass 3.6 x L'(1-0) alone exceeds the dynamics)" if r == "G3" else ""), "ceiling": f"CEILING: D = {R_['D']:.1f} > 1 but s* > 1000: vacuous"}[st]
              + f"; {R_['resolution']} (Monte Carlo no-root fraction {R_['frac_mc_noroot']:.2f})" + ("; VACUOUS" if R_["vacuous"] else "") + ("; ILL-CONDITIONED (|lever| >= 10)" if R_["ill"] else "; conditioned (|lever| < 10)")
              + f"; JVLA CO(1-0) L' {LP10:.2e} (beam 3.3 x 2.6 arcsec, disc scale assumed); X-ray AGN host; M* one CIGALE fit ({SIG_HI:.2f}/-{SIG_LO:.2f} dex); kinematic i {I_AD:.0f} vs thin-disc {I_F444W:.0f}/{I_870:.0f} deg; protocluster SSA22")
        rows.append(["CFG285", R_["label"], GCL[r], f"{Z:.4f}", f"{Z:.4f}", int(st == "floor"), f"{sstar:.6g}", f"{sstar * 0.93603:.6g}", f"{lo68:.6g}", f"{hi68:.6g}", f"{lo95:.6g}", f"{hi95:.6g}",
                     f"{b15[0]:.6g}", f"{b15[1]:.6g}", b15[2], f"{b30[0]:.6g}", f"{b30[1]:.6g}", b30[2], f"{half:.4f}" if np.isfinite(half) else "nan", f"{sstar * 10 ** (-half):.6g}" if np.isfinite(half) else "nan", f"{sstar * 10 ** half:.6g}" if np.isfinite(half) else "nan", R_["n_knobs_with_root"],
                     *[("nan" if (isinstance(v, float) and not np.isfinite(v)) else (f"{v:.6g}" if isinstance(v, float) else v)) for v in extra], lim, fl["FLAT"], fl["H(z)"], fl["PROXY"], q_])
    H.write_points(os.path.join(HERE, f"cfg285_points{SFX}.csv"), cols, rows)
    P(f"\n  points written: cfg285_points{SFX}.csv ({len(rows)} rows)")

nf = sum(1 for _, ok, lb in CHK if lb and not ok)
P(f"\n{sum(ok for _, ok, _ in CHK)}/{len(CHK)} checks pass; load-bearing failures: {nf}   ({time.time() - T0:.0f} s)")
open(os.path.join(HERE, f"cfg285{SFX}.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(stage=STAGE, mutate=MUTATE, selftest=SELFTEST, checks=[dict(name=n, ok=ok, load_bearing=lb) for n, ok, lb in CHK], numbers=H.jc(NUM)), open(os.path.join(HERE, f"cfg285{SFX}_results.json"), "w"), indent=1)
sys.exit(1 if nf else 0)
