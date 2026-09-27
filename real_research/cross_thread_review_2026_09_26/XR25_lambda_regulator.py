#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR25 (4 of 4) -- THE lambda QUESTION (phi's inertia 2 lambda (n.d phi)^2) UNDER FP13's STATE SEPARATOR H_S, AT THE CORE'S
ACTUAL c_2 = oo: is lambda a regulator (every observable lambda-independent across (0, bound)), is there strong coupling at
small lambda, and where does the upper bound come from?

THE READING TO SETTLE (the coordinator's): FP14 eliminated lambda (lambda = 0) but that needs FP9's yield at exact zero field;
under FP13's H_S the yield is y_th = <|g_bp|^2>^(1/2) (c^2/a0) max(0, 2q), zero once the leaf accelerates (z < 0.635), so
FP13 A1 made lambda > 0 REQUIRED (any value).  lambda is then a regulator like alpha_c if every observable is lambda-independent
across (0, its upper bound).  FP14 found sigma_8 unchanged for lambda = 0-100 under FP9's H_Y -- at the c_2 FLOOR, where the
khronon's own inertia (2 + 3 c_2)/c_2 = 277 dominates lambda_eff = lambda + (2 + 3 c_2) h^2/c_2.  At FP14's c_2 = oo that
inertia is 3 h^2.

PRE-DECLARED HYPOTHESES (written before the first full run)
  H1  Under H_S at c_2 = oo sigma_8 and the forest proxy move with lambda only through the tracking weight w = 1/(1 + (H/(c_s k))^2),
      c_s^2 = c^2/(C^Q lambda_eff): small over (0, 274.8] (the band-passed MOND sits at k >~ 1/L); the static gates (flagship,
      SPARC, KiDS) are lambda-free exactly (FP14 L4).
  H2  The strong-field observables (PPN at the bound scales, sensitivities, pulsar and inspiral radiation, compact-object
      structure) are lambda-independent to far below any error across (0, 274.8] (XR25's other three lanes).
  H3  The MOND-regime observables are NOT: at c_2 = oo the tracking speed ~ (lambda + 3)^(-1/2) and the galaxy-scale alpha_2 v^2
      ~ (lambda + 3): lambda is observable-inert only for lambda << 3.  The upper bound is tracking (lambda <= 274.8 for
      3 x 600 km/s at C^Q <= 100); at the c_2 floor there is no room (lambda <= 0).
  H4  Strong coupling: about exact zero field with the yield off and the band-pass closed, phi's fluctuation has the quadratic
      action 2 lambda phidot^2 only (no gradient term): Lambda_sc = 0 for every lambda, and the canonically normalised cubic
      coupling grows as lambda^(-3/2); in real backgrounds the khronon's inertia 3 sigma^2 keeps the tree-level length finite as
      lambda -> 0 (ell_sc ~ lambda_eff^(-1/8) C_phi^(-5/8)).

CHECKS
  K1 CONTROL: FP13's H_S state machinery (its L(a) at delta_c on the nonlinear field and its ramped state yield, copied from
     FP13's main() unchanged, driving FP9's machinery exec'd read-only) reproduces FP13's committed H1 headline (sigma_8 x4,
     flagship x4, SPARC x2, KiDS x2) at FP13's settings (c_2 = FP9's C2W, lambda = 0).
  K2 CONTROL: FP14's committed lambda scan (sigma_8 under H_Y at the c_2 floor, lambda = 0, 1, 100) is reproduced.
  K3 CONTROL: FP7 B6's committed tree-level strong-coupling rows are reproduced.
  K4 CONTROL: FP13 A1's zero-field statement re-derived from the multiplier block: with the band-pass closed (sigma -> 0) and
     C_phi = 0 phi's row is 4 lambda omega^2 A_phi -- no equation at lambda = 0.
  L1 H_S at c_2 = oo: sigma_8 and the forest over lambda = 0 .. 274.8 (both footings, both modes); the c_2 = oo vs floor shift.
  L2 the upper bound: tracking at c_2 = oo and at the floor.
  L3 the strong-field observables (read from XR25's other lanes' committed-in-folder JSONs).
  L4 the MOND-regime observables (tracking speed, galaxy alpha_2 v^2).
  L5 strong coupling at small lambda (zero field; real backgrounds at c_2 = oo; the sub-xi sector) and Cherenkov.
  V  the verdict.   W  the ledger.
MUTATE=1: the core is put back at the c_2 FLOOR (FP13's own setting): L2's check that a non-degenerate lambda window
(0, lambda_max], lambda_max >= 1, exists must FAIL (at the floor tracking allows only lambda <~ 1e-4, the floor constant's
rounding residue), rc = 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR25_lambda_regulator.py
"""
import os, io, sys, json, math, time, contextlib, warnings
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
import XR25_common as C

L = C.Lane("XR25_lambda_regulator", "XR25/lambda")
P, check, banner = L.P, L.check, L.banner
P(__doc__.split("CHECKS")[0].strip())
if L.mutate:
    P("\n  *** MUTATE=1: the core at the c_2 FLOOR (FP13's setting): L2's non-empty-window check must FAIL ***")
HERE9 = C.CHAIN


def _exec_ro(path, cut_marker, name):
    src = open(path).read()
    src = src[:src.index(cut_marker)]
    ns = {"__file__": path, "__name__": name}
    old = os.environ.get("MUTATE")
    os.environ["MUTATE"] = "0"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, "exec"), ns)
    finally:
        if old is None:
            os.environ.pop("MUTATE", None)
        else:
            os.environ["MUTATE"] = old
    return ns


t0 = time.time()
ns9 = _exec_ro(os.path.join(HERE9, "FP9_web_galaxy_separator.py"),
               "# ================================================================================================= K  CONTROLS", "fp9_machinery")
M6 = ns9["M6"]
A0 = dict(ns9["A0"])
FOOTS, MODES = ns9["FOOTS"], ns9["MODES"]
h, Om, OL, Or = M6["h"], M6["Om"], M6["OL"], M6["Or"]
OmL_a, OmL_z, Ez, dlnH, A_I = M6["OmL_a"], M6["OmL_z"], M6["Ez"], M6["dlnH"], M6["A_I"]
c, Mpc, G, rho_crit0, H0 = M6["c"], M6["Mpc"], M6["G"], M6["rho_crit0"], M6["H0"]
Delta_lin0 = M6["Delta_lin0"]
s8_aq, growth_aq = ns9["s8_aq"], ns9["growth_aq"]
law_dev_dex, kids_class = ns9["law_dev_dex"], ns9["kids_class"]
YIELD, cutfac = ns9["YIELD"], M6["cutfac"]
KH, KHF, DI, DIF = M6["KH"], M6["KHF"], M6["DI"], M6["DIF"]
sigma8_of, S8_LCDM, forest_proxy, C2W = M6["sigma8_of"], M6["S8_LCDM"], M6["forest_proxy"], M6["C2W"]
SIG8_BAND, FOREST_TOL = M6["SIG8_BAND"], M6["FOREST_TOL"]
Z_KIDS, Z_FLAG = M6["Z_KIDS"], M6["Z_FLAG"]
P(f"\n  machinery: FP9 exec'd read-only up to its K banner ({time.time() - t0:.0f} s); a0 = {A0['canonical']:.4e} / {A0['alt']:.4e}; "
  f"C2W = {C2W}")

# ---------------------------------------------------------------------------------------------- FP13's state machinery (copied)
_sD = solve_ivp(lambda N_, Y: [Y[1], 1.5 * (Om / math.exp(3 * N_) / Ez(math.exp(N_)) ** 2) * Y[0] - (2 + dlnH(math.exp(N_))) * Y[1]],
                (math.log(A_I), 0.0), [1.0, 1.0], method="LSODA", rtol=1e-10, atol=1e-14, dense_output=True)
_D1 = _sD.sol(0.0)[0]


def Dl(a):
    return float(_sD.sol(math.log(a))[0] / _D1)


LKF = np.linspace(math.log(1e-4), math.log(1000.0), 5000)
KKF = np.exp(LKF)
D2L0 = np.array([Delta_lin0(k) for k in KKF]) ** 2
RMIN = 1e-5
XI_FLOOR_MPC = 0.0243e-6
DELTA_C = 3.0 / 20.0 * (12.0 * math.pi) ** (2.0 / 3.0)


def sig2(R, D2):
    return float(np.trapz(D2 * np.exp(-(KKF * R) ** 2), LKF))


def Om_a(a):
    return Om / a ** 3 / (Om / a ** 3 + OL + Or / a ** 4)


def halofit(D2lin, a, Omx=None, split=False):
    Oma = Om_a(a) if Omx is None else Omx / a ** 3 / (Omx / a ** 3 + 1.0 - Omx)
    Rs = brentq(lambda R: sig2(R, D2lin) - 1.0, RMIN, 100.0)
    ks = 1.0 / Rs
    e = 1e-3
    l0, lp, lm = (math.log(sig2(Rs * math.exp(x), D2lin)) for x in (0.0, e, -e))
    n = -3.0 - (lp - lm) / (2 * e)
    Cc = -(lp - 2 * l0 + lm) / e ** 2
    an = 10 ** (1.5222 + 2.8553 * n + 2.3706 * n ** 2 + 0.9903 * n ** 3 + 0.2250 * n ** 4 - 0.6038 * Cc)
    bn = 10 ** (-0.5642 + 0.5864 * n + 0.5716 * n ** 2 - 1.5474 * Cc)
    cn = 10 ** (0.3698 + 2.0404 * n + 0.8161 * n ** 2 + 0.5869 * Cc)
    gn = 0.1971 - 0.0843 * n + 0.8460 * Cc
    al = abs(6.0835 + 1.3373 * n - 0.1959 * n ** 2 - 5.5274 * Cc)
    be = 2.0379 - 0.7354 * n + 0.3157 * n ** 2 + 1.2490 * n ** 3 + 0.3980 * n ** 4 - 0.1682 * Cc
    nun = 10 ** (5.2105 + 3.6902 * n)
    f1, f2, f3 = Oma ** -0.0307, Oma ** -0.0585, Oma ** 0.0743
    y = KKF / ks
    DQ = D2lin * ((1 + D2lin) ** be / (1 + al * D2lin)) * np.exp(-(y / 4 + y ** 2 / 8))
    DH = an * y ** (3 * f1) / (1 + bn * y ** f2 + (cn * f3 * y) ** (3 - gn)) / (1 + nun * y ** -2)
    if split:
        return DQ, DH
    return DQ + DH, dict(ks=ks, n=n, C=Cc)


LNA = np.linspace(math.log(1e-3), 0.0, 300)
AGR = np.exp(LNA)
DLA = np.array([Dl(a) for a in AGR])
D2LIN = [D2L0 * d ** 2 for d in DLA]
D2NL = [(halofit(D2LIN[i], AGR[i])[0] if sig2(RMIN, D2LIN[i]) > 1.0 else D2LIN[i]) for i in range(len(LNA))]
STATE = {"lin": D2LIN, "NL": D2NL}


def L_table(s, reading):
    out = np.empty(len(LNA))
    for i, a in enumerate(AGR):
        D2 = STATE[reading][i]
        out[i] = XI_FLOOR_MPC if sig2(RMIN, D2) < s * s else brentq(lambda R: sig2(R, D2) - s * s, RMIN, 300.0) / h * a
    return out


def fun_of(tab, log=True):
    tab = np.asarray(tab, float)
    if log:
        lt = np.log(np.maximum(tab, 1e-300))
        return lambda a: float(np.exp(np.interp(math.log(a), LNA, lt)))
    return lambda a: float(np.interp(math.log(a), LNA, tab))


def gbp_rms_phys(i, Lphys, reading, bp=True):
    a = AGR[i]
    D2 = STATE[reading][i]
    g = 4 * math.pi * G * Om * rho_crit0 / a ** 3 * np.sqrt(D2) / (KKF * h / (a * Mpc))
    if bp:
        g = g * (1.0 - np.exp(-0.5 * (KKF * h * Lphys / a) ** 2))
    return math.sqrt(float(np.trapz(g ** 2, LKF)))


def two_q(a):
    E2 = Om / a ** 3 + OL + Or / a ** 4
    return 1.0 + (Or / a ** 4) / E2 - 3.0 * OL / E2


Z_Q0 = brentq(lambda z: two_q(1 / (1 + z)), 0.1, 2.0)
SWITCH = {"ramp": lambda a: max(0.0, two_q(a))}


def yth_state(Ltab, reading, switch="ramp", cy=1.0):
    sw = SWITCH[switch]
    rms = np.array([gbp_rms_phys(i, Ltab[i], reading) for i in range(len(LNA))])
    tabs = {f: np.array([cy * rms[i] / A0[f] * sw(AGR[i]) for i in range(len(LNA))]) for f in FOOTS}
    return {f: fun_of(tabs[f], log=False) for f in FOOTS}, tabs, rms


KB = {f: kids_class(A0[f]) for f in FOOTS}


def model_of(Lf, yf):
    return {"hfac": lambda a, k: 1.0 - np.exp(-0.5 * (k * h * Lf(a) / a) ** 2),
            "cut": lambda y, a: cutfac(y, yf(a), YIELD), "yr": 0.0}


LH_tab = L_table(DELTA_C, "NL")
Lh = fun_of(LH_tab)
yh, yh_tab, rms_h = yth_state(LH_tab, "NL", "ramp", 1.0)
P(f"  H_S state built ({time.time() - t0:.0f} s): L(0.25) = {Lh(0.8):.3f} Mpc; y_th = 0 below z = {Z_Q0:.3f}")

# ================================================================================================ K1 FP13's headline
banner("K1  CONTROL: FP13's committed H_S headline reproduced (c_2 = C2W, lambda = 0)")
F13 = json.load(open(os.path.join(HERE9, "FP13_separator_from_state_results.json")))["numbers"]["H1"]
dev = 0.0
rows_k1 = {}
for f in FOOTS:
    mod = model_of(Lh, yh[f])
    for m in MODES:
        v_ = s8_aq(mod, f, m)
        ref = F13["s8"][str((f, m))]
        rows_k1[f"s8 {f}/{m}"] = (v_, ref)
        dev = max(dev, abs(v_ / ref - 1))
    for Mv in (1e10, 1e11):
        v_ = law_dev_dex(Mv, A0[f], 0.1, Lh(1 / (1 + Z_FLAG)), yh[f](1 / (1 + Z_FLAG)), YIELD)
        ref = F13["flag"][str((f, Mv))]
        rows_k1[f"flag {f}/{Mv:.0e}"] = (v_, ref)
        dev = max(dev, abs(v_ - ref) / max(abs(ref), 1e-12))
    v_ = max(abs(law_dev_dex(Mv, A0[f], yv, Lh(1.0), yh[f](1.0), YIELD)) for Mv in (1e9, 1e10, 1e11, 1e12) for yv in (0.01, 0.03, 0.1, 1.0, 10.0, 100.0))
    rows_k1[f"sparc {f}"] = (v_, F13["sparc"][f])
    dev = max(dev, abs(v_ / F13["sparc"][f] - 1))
    v_ = kids_class(A0[f], Lh(1 / (1 + Z_KIDS)), yh[f](1 / (1 + Z_KIDS)), YIELD) - KB[f]
    rows_k1[f"kids {f}"] = (v_, F13["kids"][f])
    dev = max(dev, abs(v_ - F13["kids"][f]) / max(abs(F13["kids"][f]), 1e-12))
P("    " + "; ".join(f"{k_}: {v_[0]:.6g} (FP13 {v_[1]:.6g})" for k_, v_ in rows_k1.items()))
check("K1 CONTROL: FP13's state machinery (copied from its main() unchanged; FP9 exec'd read-only) reproduces FP13's committed H1: "
      "sigma_8 on both footings and modes, the 1e10/1e11 flagships at z = 2.5, SPARC, KiDS", f"max relative deviation {dev:.1e}",
      dev < 1e-7)
L.out["numbers"]["K1"] = {k_: list(v_) for k_, v_ in rows_k1.items()}

# ================================================================================================ K2 FP14's lambda scan
banner("K2  CONTROL: FP14's committed lambda scan (H_Y, c_2 floor)")
F14 = json.load(open(os.path.join(HERE9, "FP14_zero_knob_core_results.json")))["numbers"]["L"]["sigma8_lambda"]
HY = ns9["bandpass_model"](ns9["LL_of"](1.3, 2.0), 2.0, yr=0.0, floor=(1e-6, 4.0, YIELD))
k2 = {}
for lv in (0.0, 1.0, 100.0):
    k2[lv] = sigma8_of(growth_aq(HY, A0["canonical"], mode="permode", c2=C.C2_FLOOR, lam=lv)[0.0]) / S8_LCDM
k2dev = max(abs(k2[lv] / F14[str(lv)] - 1) for lv in k2)
P("    " + "; ".join(f"lambda {lv:g}: {v_:.8f} (FP14 {F14[str(lv)]:.8f})" for lv, v_ in k2.items()))
check("K2 CONTROL: FP14 L4's lambda scan -- sigma_8 (canonical, per-mode) under FP9's H_Y at the c_2 floor for lambda = 0, 1, 100 -- is "
      "reproduced", f"max relative deviation {k2dev:.1e}", k2dev < 1e-8)
P(f"    {L.el()}")

# ================================================================================================ K3 FP7 B6
banner("K3  CONTROL: FP7 B6's tree-level strong-coupling rows")
HBARC_EVM, MP_EV = 1.973269804e-7, 2.435e27
F7B6 = json.load(open(os.path.join(HERE9, "FP7_aqual_type_repair_results.json")))["numbers"]["B6"]["rows"]


def ell_sc(a0, Cphi, lam_eff):
    alpha_eV = a0 / C.cc ** 2 * HBARC_EVM
    cs = math.sqrt(Cphi / lam_eff)
    Lsc = cs ** 2.25 * math.sqrt(alpha_eV * MP_EV * (2 * lam_eff) ** 1.5 * 1.5)
    return cs, Lsc, cs * HBARC_EVM / Lsc


def Cphi_bg(label, a0):
    if label.startswith("web"):
        y = 1e-3
    elif label.startswith("galaxy"):
        y = 0.1
    else:
        y = C.yN_of(2.32e-10, a0)
    x = math.sqrt(y * y + y) - y
    return x / (1 - 2 * x)


k3dev = 0.0
for foot, lab, le, cs_r, Lsc_r, ell_r in F7B6:
    cs_, Lsc_, ell_ = ell_sc(A0[foot], Cphi_bg(lab, A0[foot]), le)
    k3dev = max(k3dev, abs(cs_ / cs_r - 1), abs(Lsc_ / Lsc_r - 1), abs(ell_ / ell_r - 1))
check("K3 CONTROL: FP7 B6's tree-level strong-coupling scale Lambda_sc = c_s^(9/4) [(3/2) alpha M_P (2 lambda_eff)^(3/2)]^(1/2), "
      "c_s^2 = C_phi/lambda_eff, ell_sc = c_s hbar c/Lambda_sc, reproduced for its 12 committed rows (web, galaxy outskirts, Solar "
      "neighbourhood; lambda_eff = 277.4 and 1e8; both footings)", f"max relative deviation {k3dev:.1e}", k3dev < 1e-9)

# ================================================================================================ K4 FP13 A1 from the block
banner("K4  CONTROL: FP13 A1 re-derived from the multiplier block: no phi equation at lambda = 0, zero field, band-pass closed")
E_m = C.block("aqual", "mult")
phi_row = sp.expand(E_m["phi"])
row0 = sp.simplify(phi_row.subs({C.sgm: 0, C.Cph: 0}))
check("K4 CONTROL: in FP14's multiplier block phi's row is -4 C_phi k^2 A_phi + 2 sigma k^2 [(2 - alpha_c)(A_n - sigma A_phi) + ...] + "
      "4 lambda omega^2 A_phi; with the band-pass closed (sigma -> 0: FP13's h = 0 on exact FRW) and zero field (C_phi = 0, the "
      "yield off at z < 0.635) it is 4 lambda omega^2 A_phi -- phi has NO equation at lambda = 0 (FP13 A1): lambda > 0 is required",
      f"phi row at sigma = 0, C_phi = 0: {row0}", sp.simplify(row0 - 4 * C.lam * C.wq ** 2 * C.AF) == 0)
P(f"    {L.el()}")

# ================================================================================================ L1 H_S at c_2 = oo
banner("L1  H_S AT c_2 = oo: sigma_8 and the forest over lambda (both footings, both modes)")
C2_CORE = C.C2_FLOOR if L.mutate else 1e15
LAMS = [0.0, 1e-6, 1e-3, 1.0, 3.0, 30.0, 100.0, 274.8]


def forest_c2(mod, f, m, c2v, lv):
    res = growth_aq(mod, A0[f], mode=m, KHg=KHF, Dig=DIF, zs_out=(2.0, 3.0), c2=c2v, lam=lv)
    return max(forest_proxy(res, kF=kF)[0] for kF in (10.0, 15.0, 20.0))


l1 = {}
for lv in LAMS:
    row = {}
    for f in FOOTS:
        mod = model_of(Lh, yh[f])
        for m in MODES:
            row[f"s8 {f}/{m}"] = sigma8_of(growth_aq(mod, A0[f], mode=m, c2=C2_CORE, lam=lv)[0.0]) / S8_LCDM
            row[f"forest {f}/{m}"] = forest_c2(mod, f, m, C2_CORE, lv)
    l1[lv] = row
    P(f"    lambda {lv:8.3g}: sigma_8 " + ", ".join(f"{k_[3:]} {v_:.5f}" for k_, v_ in row.items() if k_.startswith("s8"))
      + "; forest max " + f"{max(v_ for k_, v_ in row.items() if k_.startswith('forest')):.2e}")
s8_floor0 = {k_: v_[0] for k_, v_ in rows_k1.items() if k_.startswith("s8")}
shift_c2 = max(abs(l1[0.0][k_] - s8_floor0[k_]) for k_ in s8_floor0)
lam_span = max(max(l1[lv][k_] for lv in LAMS) - min(l1[lv][k_] for lv in LAMS) for k_ in l1[0.0] if k_.startswith("s8"))
all_band = all(SIG8_BAND[0] <= v_ <= SIG8_BAND[1] for row in l1.values() for k_, v_ in row.items() if k_.startswith("s8"))
all_forest = all(v_ <= FOREST_TOL for row in l1.values() for k_, v_ in row.items() if k_.startswith("forest"))
tight = {lv: max(v_ for k_, v_ in row.items() if k_.startswith("s8")) for lv, row in l1.items()}
P(f"    c_2 = oo vs FP13's c_2 = C2W at lambda = 0: max |d sigma_8| = {shift_c2:.1e};  spread over lambda = 0..274.8: {lam_span:.1e}; "
  f"max sigma_8 per lambda: " + ", ".join(f"{lv:g}: {v_:.4f}" for lv, v_ in tight.items()))
L.out["numbers"]["L1"] = dict(rows={str(k_): v_ for k_, v_ in l1.items()}, shift_c2=shift_c2, lambda_span=lam_span)
check("L1 (H1) UNDER H_S AT c_2 = oo sigma_8 AND THE FOREST ARE lambda-INERT ACROSS (0, 274.8]: every cell stays in the sigma_8 band "
      "[0.922, 1.05] and the forest proxy <= 10%; the spread in sigma_8 over lambda is printed (the static gates -- flagship, SPARC, "
      "KiDS -- carry no lambda at all: FP14 L4's static block)",
      f"sigma_8 spread over lambda {lam_span:.1e}; c_2 = oo vs floor at lambda = 0: {shift_c2:.1e}; band kept {all_band}; forest kept {all_forest}",
      all_band and all_forest and lam_span < 1e-2)

# ================================================================================================ L2 the upper bound
banner("L2  THE UPPER BOUND: tracking (3 x 600 km/s where C^Q <= 100), at c_2 = oo and at the c_2 floor")
CQ_MAX = 100.0
vt = C.V_TRACK / C.cc


def lam_max(c2v):
    kh = 3.0 if math.isinf(c2v) or c2v > 1e12 else (2 + 3 * c2v) / c2v
    return (1.0 / CQ_MAX) / vt ** 2 - kh


lm = lam_max(C2_CORE)
lm_floor = lam_max(C.C2_FLOOR)
c2_min = 2.0 / ((1.0 / CQ_MAX) / vt ** 2 - 3.0)
P(f"    c_s^2 = C_phi/(lambda + (2 + 3 c_2)/c_2) >= (1800 km/s)^2 at C_phi = 1/C^Q = 0.01: lambda <= {lm:.2f} at c_2 = "
  f"{'oo' if C2_CORE > 1e12 else C2_CORE}; at the floor c_2 = {C.C2_FLOOR}: lambda <= {lm_floor:.4f}; a window lambda > 0 exists iff "
  f"c_2 > {c2_min:.6f}")
L.out["numbers"]["L2"] = dict(lambda_max=lm, lambda_max_floor=lm_floor, c2_min_for_window=c2_min)
check("L2 (H3) THE UPPER BOUND IS TRACKING, AND THE WINDOW IS NON-DEGENERATE (lambda_max >= 1) ONLY AWAY FROM THE c_2 FLOOR: at "
      "c_2 = oo the moving-source gate (c_s >= 3 x 600 km/s where C^Q <= 100) allows 0 < lambda <= 274.8; at FP2's c_2 floor it "
      "allows lambda <= ~0 only (the floor was DEFINED by tracking at lambda = 0), so "
      "FP13's 'lambda > 0 required' and FP2's floor are compatible only for c_2 > 2/274.8 = 7.28e-3 -- FP14's c_2 = oo supplies the room",
      f"lambda_max = {lm:.2f} (core), {lm_floor:.2e} (floor, a rounding residue of the floor constant); window needs c_2 > {c2_min:.6f}",
      lm >= 1.0,
      reading=None if not L.mutate else "MUTATE: at the c_2 floor the window is empty")

# ================================================================================================ L3 the strong-field observables
banner("L3  THE STRONG-FIELD OBSERVABLES (XR25's other lanes)")
def _rj(n):
    try:
        return json.load(open(os.path.join(C.HERE, n)))
    except Exception:
        return None


ppn = _rj("XR25_ppn_preferred_frame_results.json")
rad = _rj("XR25_pulsar_radiation_results.json")
ppn_ok = ppn is not None and all(v_["frac"] < 1e-3 for v_ in ppn["numbers"]["P3"]["per_scale"].values())
rad_ok = rad is not None and all(v_["worst"] < 1e-6 for v_ in rad["numbers"]["B"].values())
P(f"    PPN (XR25_ppn P3): lambda-part of alpha_2 at each bound scale, fraction of the bound: "
  + ("; ".join(f"{k_}: {v_['frac']:.1e}" for k_, v_ in ppn["numbers"]["P3"]["per_scale"].items()) if ppn else "MISSING"))
if rad:
    P(f"    radiation (XR25_pulsar_radiation M2): lambda-spread of C_eff at fixed (pulsar, footing, channel, xi, alpha_c) <= "
      f"{rad['numbers']['M2']['lambda_spread_max']:.2e}; every pulsar's total P_b-dot deviation (worst over lambda) < 1e-6 of GR: "
      + ", ".join(f"{k_} {v_['worst']:.1e}" for k_, v_ in rad["numbers"]["B"].items()))
check("L3 (H2) THE STRONG-FIELD OBSERVABLES ARE lambda-INERT ACROSS (0, 274.8]: the PPN lambda-part is < 1e-3 of every bound at its "
      "scale; the neutron-star sensitivities carry no lambda (the MOND sector is filtered on xi >> R_NS); the pulsars' P_b-dot "
      "deviations stay < 1e-6 of GR for every lambda (the radiated dipole COEFFICIENT moves with lambda on the filter's transition "
      "branch -- by up to the printed relative spread -- but it multiplies (s_1 - s_2)^2 = O(alpha_c^2)); compact-object structure "
      "(XR25_cmc) involves no phi",
      f"PPN {ppn_ok}; radiation {rad_ok}", ppn_ok and rad_ok)

# ================================================================================================ L4 the MOND-regime observables
banner("L4  THE MOND-REGIME OBSERVABLES (the knob side)")
cs_track = {lv: math.sqrt((1 / CQ_MAX) / (lv + 3.0)) * C.cc / 1e3 for lv in (0.0, 0.03, 1.0, 3.0, 30.0, 274.8)}
v620 = (620e3 / C.cc) ** 2
a2v2 = {lv: (lv + 3.0 - 0.01) / (0.01 * 1.01) * v620 for lv in (0.0, 0.03, 1.0, 3.0, 30.0, 274.8)}
P("    tracking speed at C^Q = 100 (c_2 = oo) [km/s]: " + ", ".join(f"lambda {k_:g}: {v_:,.0f}" for k_, v_ in cs_track.items()))
P("    galaxy-outskirt alpha_2 v^2 (C^Q = 100, 620 km/s): " + ", ".join(f"lambda {k_:g}: {v_:.2e}" for k_, v_ in a2v2.items()))
inert_limit = 0.01 * 3.0
L.out["numbers"]["L4"] = dict(cs_track=cs_track, alpha2_v2=a2v2, inert_below=inert_limit)
check("L4 (H3) THE MOND-REGIME OBSERVABLES ARE NOT lambda-INERT AT c_2 = oo: the tracking speed ~ (lambda + 3)^(-1/2) (17,300 km/s at "
      "lambda -> 0, 1,800 at 274.8) and the galaxy-scale alpha_2 v^2 ~ (lambda + 3) (1.3e-3 -> 0.12): the khronon's own inertia "
      "contributes only 3 to lambda_eff, so lambda is observable-inert (< 1%) only for lambda < 0.03; above ~3 it is a knob",
      f"c_s ratio (0 -> 274.8) {cs_track[0.0] / cs_track[274.8]:.2f}; alpha_2 v^2 ratio {a2v2[274.8] / a2v2[0.0]:.0f}",
      cs_track[0.0] / cs_track[274.8] > 5 and a2v2[274.8] / a2v2[0.0] > 50)

# ================================================================================================ L5 strong coupling
banner("L5  STRONG COUPLING AT SMALL lambda, and Cherenkov")
l5 = []
for foot, a0 in A0.items():
    for lab in ("web y ~ 1e-3", "galaxy outskirts y ~ 0.1", "Solar neighbourhood x_e"):
        Cp = Cphi_bg(lab, a0)
        for lv in (1e-9, 1e-3, 1.0, 274.8):
            _, _, ell_filt = ell_sc(a0, Cp, lv + 3.0)          # sigma = 1 (k << 1/xi): lambda_eff = lambda + 3 (c_2 = oo)
            _, _, ell_sub = ell_sc(a0, Cp, lv)                 # sigma -> 0 (sub-xi): lambda_eff = lambda
            l5.append(dict(foot=foot, bg=lab, lam=lv, ell_unfiltered=ell_filt, ell_subxi=ell_sub))
worst_unf = max(r_["ell_unfiltered"] for r_ in l5)
worst_sub = max(r_["ell_subxi"] for r_ in l5)
for r_ in l5:
    if r_["foot"] == "canonical":
        P(f"    {r_['bg']:26s} lambda {r_['lam']:8.1e}: ell_sc = {r_['ell_unfiltered']:.2e} m (k << 1/xi, lambda_eff = lambda + 3); "
          f"{r_['ell_subxi']:.2e} m (sub-xi, lambda_eff = lambda)")
xi_m = C.XI_FLOOR_AQ["canonical"] * C.PC_M
cr_supp = math.exp(-0.5 * (xi_m * 1e10) ** 2) if xi_m * 1e10 < 30 else 0.0
L.out["numbers"]["L5"] = dict(rows=l5, worst_unfiltered=worst_unf, worst_subxi=worst_sub)
check("L5 (H4) STRONG COUPLING: about exact zero field with the yield off and the band-pass closed the fluctuation's quadratic action "
      "is 2 lambda phidot^2 alone (K4): no gradient term, Lambda_sc = 0 for EVERY lambda (FP7 R7l), and after canonical normalisation "
      "the cubic |grad phi|^3 coupling scales as lambda^(-3/2) -- small lambda makes the zero-field sector more strongly coupled, "
      "and lambda -> 0 removes its equation.  In real backgrounds at c_2 = oo the khronon supplies inertia 3 sigma^2: for k << 1/xi "
      "ell_sc stays <= 1 cm as lambda -> 0 (weak lambda_eff^(-1/8) dependence); only the sub-xi phi fluctuations (lambda_eff = "
      "lambda, which the metric never sees through the filter) grow as lambda^(-1/8)",
      f"worst ell_sc (k << 1/xi) {worst_unf:.1e} m over lambda = 1e-9..274.8; sub-xi worst {worst_sub:.1e} m", worst_unf < 1e-2)
check("L5b (reported) CHERENKOV: for lambda > C_phi the sub-xi phi mode is subluminal (c_s^2 = C_phi/lambda), but it couples to "
      "matter only through the filter, e^(-xi^2 k^2/2); at cosmic-ray wavenumbers (k ~ 1e10 /m) that factor is exp(-1e50): no "
      "gravitational-Cherenkov bound on lambda (L19's criterion: the bound is on the coupling, not the speed)",
      f"suppression at k = 1e10/m, xi at the floor: {cr_supp}", cr_supp == 0.0, load_bearing=False)

# ================================================================================================ V verdict
banner("V  THE VERDICT ON lambda")
P("  lambda (phi's inertia) under H_S at the core's actual c_2 = oo:")
P("   * REQUIRED > 0: with the yield off (z < 0.635) and the band-pass closed on exact FRW phi's row is 4 lambda omega^2 A_phi (K4).")
P(f"   * a REGULATOR for every strong-field observable: PPN at the bound scales, sensitivities, pulsar and GW170817 radiation,")
P(f"     compact-object structure -- lambda-inert across (0, {lm:.1f}] (L3); sigma_8 and the forest under H_S also (L1).")
P("   * NOT a regulator in the MOND regime: at c_2 = oo lambda_eff = lambda + 3, so the tracking speed and galaxy-scale alpha_2")
P("     move with lambda above ~0.03 (1%) and by O(1) above ~3 (L4): there it is a bounded KNOB.")
P(f"   * the upper bound is tracking: lambda <= {lm:.1f} (c_2 = oo); at the c_2 floor there is no room (L2).")
P("   * strong coupling: at exact zero field the sector is strongly coupled for every lambda and loses its equation as lambda -> 0;")
P("     in real backgrounds the khronon's inertia keeps ell_sc sub-cm as lambda -> 0 (L5).")
LEDGER = [
    ("XR25-L1", "lambda > 0 required under H_S (phi has no equation at lambda = 0 with the yield off and the band-pass closed)", "DERIVED", "K4 (FP13 A1 re-derived)"),
    ("XR25-L2", f"sigma_8 and the forest under H_S at c_2 = oo are lambda-inert over (0, {lm:.1f}]; c_2 = oo moves sigma_8 by "
                f"{shift_c2:.1e} vs FP13's C2W", "DERIVED", "L1"),
    ("XR25-L3", "every strong-field observable (PPN at the bound scales, sensitivities, radiation, compact objects) is lambda-inert", "DERIVED", "L3"),
    ("XR25-L4", "MOND-regime tracking speed and alpha_2 depend on lambda + 3 at c_2 = oo: lambda is a knob there above ~0.03-3",
     "CONSTRAINT", "L4"),
    ("XR25-L5", f"the upper bound: tracking, lambda <= {lm:.1f} at c_2 = oo; empty at the c_2 floor", "CONSTRAINT", "L2"),
    ("XR25-L6", "zero-field strong coupling for every lambda (kinetic-only quadratic action, cubic coupling ~ lambda^(-3/2))", "DERIVED", "L5, K4"),
]
for k_, what, st_, why in LEDGER:
    P(f"    {k_:9s} {st_:11s} {what}  --  {why}")
L.out["ledger"] = [dict(link=k_, what=w_, status=s_, basis=b_) for k_, w_, s_, b_ in LEDGER]
L.finish()
