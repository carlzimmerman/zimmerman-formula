#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG288 SEEDING ROW (CAMB) -- THE OWNER'S QUESTION: COULD THE COLD COMPONENT BE DARK ENERGY CONVERTING TO COLD DUST AT z_seed,
E.G. AS A BYPRODUCT OF RECOMBINATION (z ~ 1100)?

Frozen in FROZEN_CRITERIA.md section 6 (committed before this script; its sha256 is printed below).  In one line each:
  REFERENCE  Planck-2018 best-fit LambdaCDM (omega_b 0.02237, omega_c 0.1200, H0 67.36, tau 0.0544, ln 1e10 A_s 3.044, n_s 0.9649,
             one 0.06 eV neutrino), CAMB 1.6.6, lmax 2500, lens_potential_accuracy 1, accuracy boosts 2, linear lensing.
  MODEL      omch2 = 1e-6; a seed fluid w_s(a) = w_e + (0 - w_e)(1 + tanh((ln a - ln a_s)/Delta))/2, w_e = -0.999, Delta = 0.05,
             rest-frame cs2 = 0, energy conserved (rho_s from the exact integral of 3(1 + w_s)), omega_s(today) = 0.1200 - 1e-6.  CAMB
             carries one dark-energy component, so the separate cosmological constant is folded in: the fluid carries
             rho_Lambda + rho_s with w_tot = (-rho_Lambda + w_s rho_s)/(rho_Lambda + rho_s) via set_w_a_table (exactly Lambda + seed at
             linear order: Lambda carries no perturbation or momentum).  Before seeding the fluid holds the vacuum energy rho_c(a_s).
  GRID       z_seed = 1100 (recombination), 3400, 1e4, 1e5, 1e6; control 1e7.
  COMPARE    (a) H0 fixed at 67.36; (b) theta*-matched (H0 re-solved so CAMB's thetastar equals the reference's).  (b) decides.
  RULE       S_TT = max_{30<=l<=1000} |C_l^TT/C_l^TT,ref - 1| (lensed): EXCLUDED if > 1%; INDISTINGUISHABLE if <= 0.1% (only if C-FLUID
             and C-EARLY pass); else UNDECIDED (needs the Planck likelihood; no binned data on disk).
  CONTROLS   C-REF (100 theta_MC within 0.0006 of 1.04092); C-BG (CAMB's rho_de(a)/rho_de(1) = the analytic one to 1e-3); C-FLUID (the
             combined fluid with dust at all times = LambdaCDM to 0.1% in TT and EE, 2 <= l <= 2500); C-EARLY (seeding at 1e7 = LambdaCDM
             to 0.1%, comparison (a)).
MODES: MUTATE=0 main; MUTATE=1 C-EARLY's z_seed replaced by 1100 -- its "reproduces LambdaCDM" check must FAIL (rc 1).
kappa = 1/2 FITTED.  No dark-matter particle species; the cold MASS is still required.  This is not a Planck likelihood fit: the
precision scale is declared and approximate.  Nothing here says the theory is closed or that the data favour the framework.
Run: python3 campaign_fresh_gravity/CFG288_one_field_dark_sector/cfg288_seeding_camb.py   (MUTATE=1 for the control)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json, time, hashlib
import numpy as np
from scipy.optimize import brentq
import camb
from camb import model as cmodel

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG7_common as C

MODE = int(os.environ.get("MUTATE", "0"))
SLUG = "cfg288_seeding_camb" + (f"_MUTATE{MODE}" if MODE else "")
R = C.Report(SLUG, False)
P, check, num = R.P, R.check, R.num
T0 = time.time()
P(__doc__.split("Run: python3")[0].strip())
FROZEN = os.path.join(HERE, "FROZEN_CRITERIA.md")
P(f"\n  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(FROZEN, 'rb').read()).hexdigest()}")
P(f"  CAMB version {camb.__version__}")
if MODE == 1:
    P("\n  *** MUTATE=1: C-EARLY seeded at z = 1100 instead of 1e7 -- its 'reproduces LambdaCDM' check must FAIL ***")
LB0 = MODE == 0

# ================================================================================================ frozen settings
OB, OC, H0REF, TAU, LNAS, NS, MNU = 0.02237, 0.1200, 67.36, 0.0544, 3.044, 0.9649, 0.06
AS = math.exp(LNAS) * 1e-10
THETA_MC_PLANCK = 1.04092
OCH2_TINY = 1e-6
OS_TODAY = OC - OCH2_TINY
W_E, DELTA, CS2 = -0.999, 0.05, 0.0
LMAX = 2500
ZMAIN = [1100.0, 3400.0, 1e4, 1e5, 1e6]
Z_CTRL = 1100.0 if MODE == 1 else 1e7
TT_EXCL, TT_INDIST = 1e-2, 1e-3
CTRL_TOL = 1e-3
FSKY = 0.6


def logcosh(u):
    u = np.abs(u)
    return u + np.log1p(np.exp(-2 * u)) - math.log(2.0)


def seed_profile(a, zs, delta=DELTA, w_e=W_E):
    """w_s(a), rho_s(a)/rho_s(1), and the converted fraction F(a); zs = None means dust at all times (C-FLUID)."""
    a = np.asarray(a, float)
    if zs is None:
        return np.zeros_like(a), a ** -3.0, np.ones_like(a)
    lna, lnas = np.log(a), -math.log(1 + zs)
    u = (lna - lnas) / delta; u0 = (0.0 - lnas) / delta
    F = 0.5 * (1 + np.tanh(u))
    ws = w_e + (0.0 - w_e) * F
    # exact: ln(rho_s(a)/rho_s(1)) = 3 int_{ln a}^{0} (1 + w_s) dln a'
    I = (1 + w_e) * (-lna) + (-w_e) / 2 * ((-lna) + delta * (logcosh(u0) - logcosh(u)))
    return ws, np.exp(3 * I), F


def a_table(zs):
    a = np.geomspace(1e-10, 1.0, 6000)
    if zs is not None:
        lnas = -math.log(1 + zs)
        a = np.concatenate([a, np.exp(np.linspace(lnas - 0.5, min(lnas + 0.5, 0.0), 3000))])
    a = np.unique(a); a = a[a <= 1.0]
    if not np.isclose(a[-1], 1.0):
        a = np.append(a, 1.0)
    a[-1] = 1.0
    return a


def make_params(H0, kind, zs=None, delta=DELTA, w_e=W_E, lensing=True):
    """kind: 'ref' (LambdaCDM), 'fluid' (dust at all times in the fluid), 'seed' (seeded at zs)."""
    common = dict(H0=H0, ombh2=OB, tau=TAU, As=AS, ns=NS, mnu=MNU, omk=0, lmax=LMAX)
    if kind == "ref":
        p = camb.set_params(omch2=OC, **common)
        info = {}
    else:
        p = camb.set_params(omch2=OCH2_TINY, dark_energy_model="fluid", **common)
        Ode = camb.get_background(p, no_thermo=True).get_Omega("de", z=0)
        h = H0 / 100.0
        Os = OS_TODAY / h ** 2
        OL = Ode - Os
        if OL <= 1e-6:
            raise ValueError(f"no room for Lambda: Omega_de {Ode:.4f} < Omega_s {Os:.4f}")
        a = a_table(zs if kind == "seed" else None)
        ws, rs, F = seed_profile(a, zs if kind == "seed" else None, delta, w_e)
        wtot = (-OL + ws * rs * Os) / (OL + rs * Os)
        p.DarkEnergy.set_w_a_table(a, wtot)
        p.DarkEnergy.cs2 = CS2
        info = dict(Ode=Ode, Os=Os, OL=OL, zs=zs, delta=delta, w_e=w_e, kind=kind)
    p.set_for_lmax(LMAX, lens_potential_accuracy=1 if lensing else 0)
    p.NonLinear = cmodel.NonLinear_none
    p.Accuracy.AccuracyBoost = 2.0; p.Accuracy.lSampleBoost = 2.0; p.Accuracy.lAccuracyBoost = 2.0
    p.DoLensing = lensing
    return p, info


def thetastar(H0, kind, zs=None, delta=DELTA, w_e=W_E):
    p, _ = make_params(H0, kind, zs, delta, w_e)
    return camb.get_background(p).get_derived_params()["thetastar"]


def solve_H0(target, kind, zs=None, delta=DELTA, w_e=W_E, lo=40.0, hi=120.0):
    f = lambda H: thetastar(H, kind, zs, delta, w_e) - target
    grid = np.linspace(lo, hi, 17)
    vals = []
    for H in grid:
        try:
            vals.append((H, f(H)))
        except Exception:
            pass
    for (h1, f1), (h2, f2) in zip(vals[:-1], vals[1:]):
        if f1 * f2 <= 0:
            return brentq(f, h1, h2, xtol=1e-7, rtol=1e-12)
    return None


def run_full(p):
    res = camb.get_results(p)
    sp_ = res.get_cmb_power_spectra(p, CMB_unit="muK", spectra=["lensed_scalar", "unlensed_scalar"])
    Ls, Us = sp_["lensed_scalar"], sp_["unlensed_scalar"]
    return dict(TT=Ls[:LMAX + 1, 0], EE=Ls[:LMAX + 1, 1], TTu=Us[:LMAX + 1, 0], EEu=Us[:LMAX + 1, 1],
                thetastar=res.get_derived_params()["thetastar"], cosmomc=100 * res.cosmomc_theta(),
                zeq_camb=res.get_derived_params()["zeq"], res=res)


ELL = np.arange(LMAX + 1)


def maxdev(x, y, l0, l1):
    sl = slice(l0, l1 + 1)
    return float(np.max(np.abs(x[sl] / y[sl] - 1)))


def peaks(D):
    out = []
    for lo, hi in ((150, 300), (400, 650), (700, 950)):
        i = lo + int(np.argmax(D[lo:hi + 1]))
        out.append((i, float(D[i])))
    return out


def z_eq(res, info, kind):
    a = np.geomspace(1e-8, 1e-2, 40001)
    d = res.get_background_densities(a, vars=["photon", "neutrino", "nu", "baryon", "cdm", "de"])
    rad = d["photon"] + d["neutrino"] + d["nu"]
    if kind == "ref":
        mat = d["baryon"] + d["cdm"]
    else:
        ws, rs, F = seed_profile(a, info["zs"] if kind == "seed" else None, info["delta"], info["w_e"])
        frac_s = rs * info["Os"] / (info["OL"] + rs * info["Os"])
        mat = d["baryon"] + d["cdm"] + F * frac_s * d["de"]
    diff = mat - rad
    idx = np.where(diff >= 0)[0]
    if len(idx) == 0:
        return float("nan")
    i = idx[0]
    if i == 0:
        return 1 / a[0] - 1
    a_eq = a[i - 1] + (a[i] - a[i - 1]) * (0 - diff[i - 1]) / (diff[i] - diff[i - 1])
    return 1 / a_eq - 1


def cbg(res, info, kind):
    a = np.geomspace(1e-9, 1.0, 200)
    rho, w = res.get_dark_energy_rho_w(a)
    ws, rs, F = seed_profile(a, info["zs"] if kind == "seed" else None, info["delta"], info["w_e"])
    ana = (info["OL"] + rs * info["Os"]) / (info["OL"] + info["Os"])
    return float(np.max(np.abs(rho / ana - 1)))


def stats(m, ref):
    s = dict(
        S_TT=maxdev(m["TT"], ref["TT"], 30, 1000), S_EE=maxdev(m["EE"], ref["EE"], 30, 1000),
        S_TT_2_29=maxdev(m["TT"], ref["TT"], 2, 29), S_TT_1001_2500=maxdev(m["TT"], ref["TT"], 1001, 2500),
        S_EE_2_29=maxdev(m["EE"], ref["EE"], 2, 29), S_EE_1001_2500=maxdev(m["EE"], ref["EE"], 1001, 2500),
        S_TT_unlensed=maxdev(m["TTu"], ref["TTu"], 30, 1000), S_EE_unlensed=maxdev(m["EEu"], ref["EEu"], 30, 1000),
        dtheta_rel=m["thetastar"] / ref["thetastar"] - 1)
    pm, pr = peaks(m["TT"]), peaks(ref["TT"])
    s["peaks_model"] = pm; s["peaks_ref"] = pr
    s["H1_H3_model"] = pm[0][1] / pm[2][1]; s["H1_H3_ref"] = pr[0][1] / pr[2][1]
    s["H2_H1_model"] = pm[1][1] / pm[0][1]; s["H2_H1_ref"] = pr[1][1] / pr[0][1]
    s["dH1_H3_pct"] = 100 * (s["H1_H3_model"] / s["H1_H3_ref"] - 1)
    s["dH2_H1_pct"] = 100 * (s["H2_H1_model"] / s["H2_H1_ref"] - 1)
    sl = slice(30, 2001)
    s["dchi2_CV_TT"] = float(np.sum((2 * ELL[sl] + 1) * FSKY / 2 * (m["TT"][sl] / ref["TT"][sl] - 1) ** 2))
    return s


def verdict(S_TT, ctrl_ok):
    if S_TT > TT_EXCL:
        return "EXCLUDED"
    if S_TT <= TT_INDIST and ctrl_ok:
        return "INDISTINGUISHABLE"
    return "UNDECIDED"


def model_row(zs, kind="seed", delta=DELTA, w_e=W_E, do_b=True, label=None):
    row = dict(z_seed=zs, kind=kind, delta=delta, w_e=w_e, label=label)
    for attempt in (0, 1):
        try:
            pa, info = make_params(H0REF, kind, zs, delta, w_e)
            ma = run_full(pa)
            break
        except Exception as e:  # frozen: retry once with Delta = 0.1
            if attempt == 0 and kind == "seed":
                P(f"      CAMB failed for z_seed {zs:g} (Delta {delta}): {e!r}; retrying with Delta = 0.1 (frozen rule)")
                delta = 0.1; row["delta"] = delta; row["retry"] = True
            else:
                row["error"] = repr(e); row["verdict"] = "NOT COMPUTED"
                return row
    row["a"] = stats(ma, REF); row["a"]["H0"] = H0REF
    row["a"]["zeq"] = z_eq(ma["res"], info, kind)
    row["a"]["cbg"] = cbg(ma["res"], info, kind)
    row["a"]["OL"] = info["OL"]
    if kind == "seed":
        ws, rs, F = seed_profile(np.array([1 / (1 + zs)]), zs, delta, w_e)
        d = ma["res"].get_background_densities(np.array([1 / (1 + zs)]), vars=["tot", "de"])
        frac_s = rs * info["Os"] / (info["OL"] + rs * info["Os"])
        row["f_pre"] = float((frac_s * d["de"] / d["tot"])[0])
        row["rho_s_at_seed_over_rhoL"] = float((rs * info["Os"] / info["OL"])[0])
    row["full_a"] = ma
    if do_b:
        Hb = solve_H0(REF["thetastar"], kind, zs, delta, w_e)
        if Hb is None:
            row["b"] = None
            row["decides"] = "a (no theta*-match in H0 [40, 120])"
        else:
            pb, infob = make_params(Hb, kind, zs, delta, w_e)
            mb = run_full(pb)
            row["b"] = stats(mb, REF); row["b"]["H0"] = Hb
            row["b"]["zeq"] = z_eq(mb["res"], infob, kind); row["b"]["cbg"] = cbg(mb["res"], infob, kind)
            row["b"]["OL"] = infob["OL"]
            row["decides"] = "b"
    return row


# ================================================================================================ reference + controls
R.banner("REFERENCE: Planck-2018 best-fit LambdaCDM")
pref, _ = make_params(H0REF, "ref")
REF = run_full(pref)
zeq_ref = z_eq(REF["res"], {}, "ref")
pr = peaks(REF["TT"])
P(f"    100 theta_MC = {REF['cosmomc']:.5f} (Planck 1.04092); 100 theta* = {REF['thetastar']:.5f}; z_eq (this lane's definition) = {zeq_ref:.1f}, "
  f"CAMB zeq = {REF['zeq_camb']:.1f}")
P(f"    TT peaks (l, D_l): {[(l, round(v, 1)) for l, v in pr]};  H1/H3 = {pr[0][1] / pr[2][1]:.4f}, H2/H1 = {pr[1][1] / pr[0][1]:.4f}   {R.el()}")
check("C-REF the reference's CAMB 100 theta_MC is within 0.0006 of Planck's 1.04092",
      f"100 theta_MC = {REF['cosmomc']:.5f} (diff {REF['cosmomc'] - THETA_MC_PLANCK:+.5f})", abs(REF["cosmomc"] - THETA_MC_PLANCK) <= 6e-4,
      load_bearing=LB0)
num("reference", dict(cosmomc=REF["cosmomc"], thetastar=REF["thetastar"], zeq=zeq_ref, zeq_camb=REF["zeq_camb"], peaks=pr))

ROWS = {}
CBG = {}
if MODE == 0:
    R.banner("C-FLUID: the combined fluid with dust at all times (no seeding) against real CDM")
    rf = model_row(None, kind="fluid", do_b=False, label="C-FLUID")
    mf = rf["full_a"]
    dTT = maxdev(mf["TT"], REF["TT"], 2, LMAX); dEE = maxdev(mf["EE"], REF["EE"], 2, LMAX)
    P(f"    max |dC/C| 2..2500: TT {dTT:.2e}, EE {dEE:.2e}; C-BG {rf['a']['cbg']:.2e}; z_eq {rf['a']['zeq']:.1f}   {R.el()}")
    CFLUID_OK = dTT <= CTRL_TOL and dEE <= CTRL_TOL
    check("C-FLUID the dust + Lambda combined fluid (cs2 = 0) reproduces LambdaCDM lensed TT and EE to <= 0.1% over 2 <= l <= 2500",
          f"TT {dTT:.2e}, EE {dEE:.2e}", CFLUID_OK, load_bearing=True)
    CBG["C-FLUID"] = rf["a"]["cbg"]
    num("C_FLUID", dict(dTT=dTT, dEE=dEE, cbg=rf["a"]["cbg"], zeq=rf["a"]["zeq"]))
else:
    CFLUID_OK = None

R.banner(f"C-EARLY: seeding at z = {Z_CTRL:g}" + (" [MUTATE: must FAIL]" if MODE == 1 else ""))
rc_ = model_row(Z_CTRL, do_b=(MODE == 0), label="C-EARLY")
if "error" in rc_:
    P(f"    C-EARLY NOT COMPUTED: {rc_['error']}")
    CEARLY_OK = False
    check(f"C-EARLY seeding at z = {Z_CTRL:g} reproduces LambdaCDM lensed TT and EE to <= 0.1% (2 <= l <= 2500), comparison (a)",
          f"NOT COMPUTED: {rc_['error']}", False, load_bearing=True)
else:
    mc = rc_["full_a"]
    dTT = maxdev(mc["TT"], REF["TT"], 2, LMAX); dEE = maxdev(mc["EE"], REF["EE"], 2, LMAX)
    CEARLY_OK = dTT <= CTRL_TOL and dEE <= CTRL_TOL
    P(f"    max |dC/C| 2..2500: TT {dTT:.2e}, EE {dEE:.2e}; S_TT(30-1000) {rc_['a']['S_TT']:.2e}; f_pre {rc_.get('f_pre', float('nan')):.2e}; "
      f"C-BG {rc_['a']['cbg']:.2e}   {R.el()}")
    check(f"C-EARLY seeding at z = {Z_CTRL:g} reproduces LambdaCDM lensed TT and EE to <= 0.1% (2 <= l <= 2500), comparison (a)"
          + (" [MUTATE: must FAIL]" if MODE == 1 else ""),
          f"TT {dTT:.2e}, EE {dEE:.2e}", CEARLY_OK, load_bearing=True)
    CBG[f"C-EARLY z{Z_CTRL:g}"] = rc_["a"]["cbg"]
    num("C_EARLY", dict(z=Z_CTRL, dTT=dTT, dEE=dEE, cbg=rc_["a"]["cbg"], f_pre=rc_.get("f_pre")))
    ROWS[f"{Z_CTRL:g}"] = rc_

# ================================================================================================ main grid
if MODE == 0:
    R.banner("MAIN GRID: dark energy converting to cold dust at z_seed (decision on (b), theta*-matched, lensed TT, 30 <= l <= 1000)")
    CTRL_OK = bool(CFLUID_OK and CEARLY_OK)
    for zs in ZMAIN:
        r = model_row(zs, label="main")
        ROWS[f"{zs:g}"] = r
        if "error" in r:
            P(f"    z_seed {zs:g}: NOT COMPUTED ({r['error']})")
            continue
        CBG[f"main z{zs:g}"] = r["a"]["cbg"]
        S_dec = (r["b"] if r["b"] is not None else r["a"])["S_TT"]
        r["verdict"] = verdict(S_dec, CTRL_OK)
        P(f"    z_seed {zs:>8g}: f_pre {r['f_pre']:.3e} (rho_s/rho_L at seeding {r['rho_s_at_seed_over_rhoL']:.3e})  {R.el()}")
        for k in ("a", "b"):
            s = r[k]
            if s is None:
                P(f"       ({k}) no theta*-match in H0 [40, 120]")
                continue
            P(f"       ({k}) H0 {s['H0']:.3f}: S_TT {s['S_TT']:.3e}, S_EE {s['S_EE']:.3e}, S_TT unlensed {s['S_TT_unlensed']:.3e}, "
              f"S_TT(2-29) {s['S_TT_2_29']:.2e}, S_TT(1001-2500) {s['S_TT_1001_2500']:.2e}; dtheta*/theta* {s['dtheta_rel']:+.3e}; "
              f"H1/H3 {s['H1_H3_model']:.4f} ({s['dH1_H3_pct']:+.2f}%), H2/H1 {s['H2_H1_model']:.4f} ({s['dH2_H1_pct']:+.2f}%); "
              f"z_eq {s['zeq']:.1f}; dchi2_CV {s['dchi2_CV_TT']:.3g}; C-BG {s['cbg']:.1e}")
        P(f"       VERDICT ({r['decides']}): {r['verdict']}")
    # reported rows (never verdicts)
    R.banner("REPORTED ROWS (never verdicts): transition width, early w, lensing off (= the unlensed S_TT printed above)")
    REP = {}
    for zs, dl, we in ((1100.0, 0.02, W_E), (1100.0, 0.2, W_E), (1e5, 0.02, W_E), (1e5, 0.2, W_E), (1e5, 0.05, -0.99)):
        r = model_row(zs, delta=dl, w_e=we, label="reported")
        key = f"z{zs:g}_Delta{dl}_we{we}"
        if "error" in r:
            P(f"    {key}: NOT COMPUTED ({r['error']})"); REP[key] = dict(error=r["error"]); continue
        sdec = r["b"] if r["b"] is not None else r["a"]
        REP[key] = dict(S_TT_b=(r["b"] or {}).get("S_TT"), S_TT_a=r["a"]["S_TT"], H0_b=(r["b"] or {}).get("H0"), would_be=verdict(sdec["S_TT"], CTRL_OK),
                        f_pre=r["f_pre"], cbg=r["a"]["cbg"])
        CBG[f"rep {key}"] = r["a"]["cbg"]
        P(f"    {key}: S_TT (a) {r['a']['S_TT']:.3e}, (b) {REP[key]['S_TT_b'] if REP[key]['S_TT_b'] is None else format(REP[key]['S_TT_b'], '.3e')}; "
          f"f_pre {r['f_pre']:.3e}; would read {REP[key]['would_be']}   {R.el()}")
    num("reported", REP)

# ================================================================================================ C-BG over every model run
cbg_max = max(CBG.values()) if CBG else float("nan")
P(f"\n    C-BG: CAMB's rho_de(a)/rho_de(1) vs the analytic (rho_L + rho_s(a))/(rho_L + rho_s(1)), max over runs and 200 a in [1e-9, 1]: {cbg_max:.2e}")
check("C-BG CAMB's dark-energy density history equals the analytic Lambda + seed history to 1e-3 relative for every model run (comparison (a))",
      "; ".join(f"{k} {v:.1e}" for k, v in CBG.items()), cbg_max <= 1e-3, load_bearing=LB0)

# ================================================================================================ the seeding table and the verdict rows
if MODE == 0:
    R.banner("THE SEEDING TABLE")
    P(f"    {'z_seed':>8s} {'f_pre':>10s} {'S_TT(a)':>10s} {'S_TT(b)':>10s} {'H0(b)':>8s} {'dH1/H3%':>8s} {'z_eq':>8s} {'verdict':>18s}")
    TABLE = []
    for zs in ZMAIN + [1e7]:
        r = ROWS.get(f"{zs:g}")
        if r is None or "error" in r:
            P(f"    {zs:8g}  NOT COMPUTED"); TABLE.append(dict(z_seed=zs, verdict="NOT COMPUTED")); continue
        b = r["b"]
        vd = r.get("verdict", verdict((b or r["a"])["S_TT"], CTRL_OK)) if zs != 1e7 else ("control: " + verdict((b or r["a"])["S_TT"], CTRL_OK))
        P(f"    {zs:8g} {r['f_pre']:10.3e} {r['a']['S_TT']:10.3e} {(b['S_TT'] if b else float('nan')):10.3e} {(b['H0'] if b else float('nan')):8.3f} "
          f"{(b or r['a'])['dH1_H3_pct']:+8.2f} {(b or r['a'])['zeq']:8.1f} {vd:>18s}")
        TABLE.append(dict(z_seed=zs, f_pre=r["f_pre"], S_TT_a=r["a"]["S_TT"], S_TT_b=(b["S_TT"] if b else None), H0_b=(b["H0"] if b else None),
                          S_EE_b=(b["S_EE"] if b else None), dH1_H3_pct=(b or r["a"])["dH1_H3_pct"], dH2_H1_pct=(b or r["a"])["dH2_H1_pct"],
                          zeq=(b or r["a"])["zeq"], dtheta_a=r["a"]["dtheta_rel"], dchi2_CV_b=(b or r["a"])["dchi2_CV_TT"], verdict=vd,
                          decides=r.get("decides")))
    num("seeding_table", TABLE)
    # z_req for G-ONSET (frozen section 3): smallest main z_seed rated INDISTINGUISHABLE with every larger grid value too; else 1e7
    zreq = None
    for zs in sorted(ZMAIN):
        later = [ROWS[f"{z:g}"].get("verdict") for z in ZMAIN if z >= zs]
        if all(v == "INDISTINGUISHABLE" for v in later):
            zreq = zs; break
    if zreq is None:
        zreq = 1e7 if CEARLY_OK else None
    P(f"\n    z_req (G-ONSET, frozen definition) = {zreq}")
    num("z_req", zreq)
    r1100 = ROWS.get("1100")
    v1100 = r1100.get("verdict") if r1100 else "NOT COMPUTED"
    check("SEED-1100 [the owner's case; finding] dark energy converting to cold dust at recombination (z = 1100) is not excluded by the CMB "
          "(verdict INDISTINGUISHABLE or UNDECIDED)",
          f"verdict {v1100}; S_TT (b) = {((r1100 or {}).get('b') or {}).get('S_TT')}; f_pre = {(r1100 or {}).get('f_pre')}",
          v1100 in ("INDISTINGUISHABLE", "UNDECIDED"), load_bearing=True)
    for zs in ZMAIN[1:]:
        r = ROWS.get(f"{zs:g}")
        v = r.get("verdict") if r else "NOT COMPUTED"
        check(f"SEED-{zs:g} [finding] seeding at z = {zs:g} is not excluded (INDISTINGUISHABLE or UNDECIDED)", f"verdict {v}",
              v in ("INDISTINGUISHABLE", "UNDECIDED"), load_bearing=False)
    num("rows", {k: {kk: vv for kk, vv in r.items() if kk != "full_a"} for k, r in ROWS.items()})

# ================================================================================================ POST-FREEZE REPORTED ROWS
# Added AFTER the criteria were frozen and after the first run, at the coordinator's relay of an owner question ("what about BAO ... can we
# use that to get closure?").  No frozen verdict, check or z_req depends on anything in this block; it prints and stores numbers only.
if MODE == 0:
    R.banner("POST-FREEZE REPORTED ROWS (added after the criteria; no frozen verdict depends on them): BAO sound horizon and a0(z) under an evolving DE")
    ZB = (0.5, 1.0, 2.3)
    C_KMS = 299792.458
    def bao(res):
        rd = res.get_derived_params()["rdrag"]
        DM = np.array([res.comoving_radial_distance(z) for z in ZB])            # flat: D_M = comoving radial distance
        DH = np.array([C_KMS / res.hubble_parameter(z) for z in ZB])
        return rd, DM, DH
    rd_ref, DM_ref, DH_ref = bao(REF["res"])
    P(f"    reference: r_d = {rd_ref:.3f} Mpc, z_eq = {zeq_ref:.1f}; D_M/r_d at z = 0.5, 1.0, 2.3: {np.round(DM_ref / rd_ref, 3).tolist()}; "
      f"D_H/r_d: {np.round(DH_ref / rd_ref, 3).tolist()}")
    P("    precision scales (declared, approximate): Planck r_d ~ 0.2%; DESI DR2 BAO ratios ~ 0.3-1% per bin")
    P(f"    {'row':>10s} {'r_d [Mpc]':>10s} {'dr_d/r_d':>10s} {'z_eq':>8s}   shift of D_M/r_d and D_H/r_d at z = 0.5 / 1.0 / 2.3 (comparison (a): H0 and late-time "
      f"expansion fixed)          {'r_d(b)':>8s} {'H0(b)':>7s}")
    BAO = {}
    rows_bao = [("C-FLUID", rf if MODE == 0 else None)] + [(f"{z:g}", ROWS.get(f"{z:g}")) for z in ZMAIN + [1e7]]
    for lab, r in rows_bao:
        if r is None or "error" in r:
            continue
        rd, DM, DH = bao(r["full_a"]["res"])
        sDM = (DM / rd) / (DM_ref / rd_ref) - 1
        sDH = (DH / rd) / (DH_ref / rd_ref) - 1
        late = float(max(np.max(np.abs(DM / DM_ref - 1)), np.max(np.abs(DH / DH_ref - 1))))
        rdb = None
        if r.get("b"):
            pb_, _ = make_params(r["b"]["H0"], r["kind"], r["z_seed"], r["delta"], r["w_e"])
            rdb = camb.get_background(pb_).get_derived_params()["rdrag"]
        BAO[lab] = dict(rd=rd, drd_rel=rd / rd_ref - 1, zeq=r["a"]["zeq"], shift_DM_over_rd=sDM.tolist(), shift_DH_over_rd=sDH.tolist(),
                        late_time_distance_change_max=late, rd_b=rdb, H0_b=(r["b"] or {}).get("H0") if r.get("b") else None,
                        vs_planck_rd_0p2pct="exceeds" if abs(rd / rd_ref - 1) > 2e-3 else "within",
                        vs_desi_0p3pct="exceeds" if np.max(np.abs(sDM)) > 3e-3 else "within")
        P(f"    {lab:>10s} {rd:10.3f} {rd / rd_ref - 1:+10.3e} {r['a']['zeq']:8.1f}   D_M/r_d {' / '.join(f'{x:+.2e}' for x in sDM)};  "
          f"D_H/r_d {' / '.join(f'{x:+.2e}' for x in sDH)}  (late-time distances moved <= {late:.1e})  "
          f"{(format(rdb, '8.3f') if rdb else '     n/a')} {(format(r['b']['H0'], '7.3f') if r.get('b') else '    n/a')}")
    num("POSTFREEZE_BAO", dict(reference=dict(rd=rd_ref, zeq=zeq_ref, DM_over_rd=(DM_ref / rd_ref).tolist(), DH_over_rd=(DH_ref / rd_ref).tolist()),
                               rows=BAO, z=list(ZB), precision_declared=dict(planck_rd=2e-3, desi_dr2_per_bin=(3e-3, 1e-2))))
    # a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) on the canonical footing, for the DESI DR2 CPL triples committed in CFG6_a0z_branches.py
    src6 = open(os.path.join(LANES, "CFG6_a0z_branches.py")).read()
    i6 = src6.index("D273 = {")
    j6 = src6.index("}", src6.index("Union3", i6)) + 1
    D273 = eval(src6[i6 + len("D273 = "):j6], {"dict": dict, "__builtins__": {}})
    P("\n    a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) on the canonical footing (a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED), CPL w(a) = w0 + wa(1 - a),")
    P("    DESI DR2 triples as committed in campaign_fresh_gravity/CFG6_a0z_branches.py (D273):")
    A0Z = {}
    for name, pr_ in D273.items():
        w0, wa = pr_["w0"], pr_["wa"]
        vals = {z: math.sqrt((1 + z) ** (3 * (1 + w0 + wa)) * math.exp(-3 * wa * z / (1 + z))) for z in (0.4, 1.0, 2.0)}
        A0Z[name] = dict(w0=w0, wa=wa, a0z_over_a00={str(k): v for k, v in vals.items()})
        P(f"      {name:10s} (w0 {w0:+.3f}, wa {wa:+.2f}):  z = 0.4: {vals[0.4]:.4f};  z = 1: {vals[1.0]:.4f};  z = 2: {vals[2.0]:.4f}")
    P("      (w = -1, the construction of this lane: a0(z)/a0(0) = 1 exactly at every z.  An evolving DE is NOT what the one-field construction's")
    P("       vacuum term gives; if DESI's evolution holds, the vacuum term would have to be replaced by a rolling field, outside this lane.)")
    num("POSTFREEZE_a0z_CPL", A0Z)

num("mode", MODE)
P(f"\n  run time {time.time() - T0:.0f} s.  kappa = 1/2 FITTED; the cold mass is still required; not a likelihood fit; nothing here says the theory is closed.")
nf = R.write(here=HERE)
sys.exit(1 if nf else 0)
