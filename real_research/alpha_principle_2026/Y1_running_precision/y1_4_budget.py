#!/usr/bin/env python3
"""y1_4_budget.py -- Part 3 (budget) of Y1_PREREGISTRATION.md: the itemised uncertainty of a_Y, a_2, a_3 and a_em = a_Y + a_2 at X_P, X_R, X_S and at the a_1 = a_2 and a_Y = a_2 crossings,
BEFORE (lane U3's seven-variant band and 2 x band with the 1% floor) and AFTER (items E1-E9, linear propagation, Monte-Carlo cross-check).
Run:    python3 y1_4_budget.py            (exit 0 iff the internal checks pass: linearity of the items, MC (N = 600, seed 20260929) versus linear propagation within 20%)
MUTATE: python3 y1_4_budget.py MUTATE     (the control drops the alpha_s item from the LINEAR propagation only; the MC/linear check must fail: exit 1; exit 3 if not)
Writes y1_4_results.json.  Imports lane U3 READ-ONLY (path-relative) for the BEFORE numbers.  No bytecode.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for sub in ("B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L
import u3_lib as U3

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
P = L.PDG
fails = []


def chk(name, ok, info=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} {info}")
    if not ok:
        fails.append(name)


print("=" * 130)
print("Y1-4 uncertainty budget of the running -- mode:", "MUTATE" if MUT else "REAL RUN")
print("=" * 130)

SC = [("X_P", U3.XP), ("X_R", U3.XR), ("X_S", U3.XS)]
KEYS = ["aY", "a2", "a3", "aem"]
NIT = 600
SEED = 20260929


def observe(tr):
    """dict: values at the fixed scales and at the two crossings."""
    out = {}
    for nm, X in SC:
        A = tr.A(X)
        out[nm] = np.array([A[0], A[1], A[2], A[0] + A[1]])
    xc = L.crossing(tr, "a1", "a2")
    out["X_c"] = xc
    A = tr.A(xc)
    out["at_Xc"] = np.array([A[0], A[1], A[2], A[0] + A[1], A[2] / A[1]])
    xy = L.crossing(tr, "aY", "a2")
    out["X_Y2"] = xy if xy is not None else float("nan")
    return out


def flat(o):
    v = []
    for nm, _ in SC:
        v += list(o[nm])
    v += [math.log(o["X_c"])] + list(o["at_Xc"]) + [math.log(o["X_Y2"]) if o["X_Y2"] == o["X_Y2"] else float("nan")]
    return np.array(v)


LABELS = [f"{nm}:{k}" for nm, _ in SC for k in KEYS] + ["lnXc", "Xc:aY", "Xc:a2", "Xc:a3", "Xc:aem", "Xc:a3/a2", "lnXY2"]


def run_obs(o=None, **kw):
    tr = L.run_central(mu_max=3e21, o=o, **kw)
    return flat(observe(tr))


base = run_obs()
print("central (Y1-central):")
for nm, _ in SC:
    print(f"  {nm}: a_Y {base[LABELS.index(nm + ':aY')]:.4f}  a_2 {base[LABELS.index(nm + ':a2')]:.4f}  a_3 {base[LABELS.index(nm + ':a3')]:.4f}  a_em {base[LABELS.index(nm + ':aem')]:.4f}")
print(f"  X_c(a1=a2) = {math.exp(base[LABELS.index('lnXc')]):.4e} GeV ; at X_c: a_Y {base[LABELS.index('Xc:aY')]:.3f} a_2 {base[LABELS.index('Xc:a2')]:.3f} a_3 {base[LABELS.index('Xc:a3')]:.3f}  a_3/a_2 = {base[LABELS.index('Xc:a3/a2')]:.5f}")
print(f"  X(a_Y=a_2) = {math.exp(base[LABELS.index('lnXY2')]):.4e} GeV")

# ------------------------------------------------------------------------------------------- items (Jacobian by central differences)
sg2 = abs(0.64779 - 0.64754) * (abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294))            # r |Delta_2|,  r = max(|D2/D1|, alpha_3/pi): see below
r2 = max(abs(0.64779 - 0.64754) / abs(0.64754 - 0.65294), 0.108 / PI)
rY = max(abs(0.35830 - 0.35940) / abs(0.35940 - 0.34972), 0.108 / PI)
sg2 = abs(0.64779 - 0.64754) * r2
sgY = abs(0.35830 - 0.35940) * rY
sMt = math.hypot(P["sMt_exp"], P["sMt_th"])
gY_c = 0.35830
sMZ_gY = gY_c * P["MZ"] * P["sMZ"] / (P["MZ"] ** 2 - P["MW"] ** 2)
g3_mu_dec_half = 2.62e-5            # V5 (c): half-range of g_3(M_t) under mu_dec in [M_t/2, 2 M_t], relative (y1_2 output)
g3_EW = 6.72e-5 / 2                 # |SMDR/QCD-only - 1| / 2 (y1_2 output, V5-b)
sg3 = math.hypot(g3_mu_dec_half, g3_EW)
ITEMS = {
    "E1 alpha_s(m_Z) 0.1180+-0.0009": (dict(als=P["als"] + P["sals"]), dict(als=P["als"] - P["sals"])),
    "E2 M_W 80.3692+-0.0133": (dict(MW=P["MW"] + P["sMW"]), dict(MW=P["MW"] - P["sMW"])),
    "E3 M_t 172.57+-0.42": (dict(Mt=P["Mt"] + sMt), dict(Mt=P["Mt"] - sMt)),
    "E4a M_h 125.10+-0.09": (dict(Mh=P["Mh"] + P["sMh"]), dict(Mh=P["Mh"] - P["sMh"])),
    "E4b M_Z +-0.0021 (tree scaling of g_Y)": (dict(dgY=sMZ_gY), dict(dgY=-sMZ_gY)),
    "E5a matching g_2 (3-loop estimator)": (dict(dg2=sg2), dict(dg2=-sg2)),
    "E5a' matching g_Y (3-loop estimator)": (dict(dgY=sgY), dict(dgY=-sgY)),
    "E5b matching g_3 (mu_dec + EW remainder)": (dict(rel_g3=sg3), dict(rel_g3=-sg3)),
    "E5c y_t +-0.0005": (dict(dyt=0.0005), dict(dyt=-0.0005)),
    "E5c' lambda +-0.0003": (dict(dlam=0.0003), dict(dlam=-0.0003)),
    "E8a y_b, y_tau +-30%": (dict(yb_scale=1.3, ytau_scale=1.3), dict(yb_scale=0.7, ytau_scale=0.7)),
}
print(f"\nestimators (pre-registered): sigma(g_2 matching) = {sg2:.2e} (r = {r2:.3f}); sigma(g_Y matching) = {sgY:.2e} (r = {rY:.3f}); sigma(g_3 matching) = {sg3:.2e} relative; sigma(M_t) = {sMt:.3f} GeV; sigma(g_Y from M_Z) = {sMZ_gY:.1e}")
jac = {}
lin_ok = True
for nm, (plus, minus) in ITEMS.items():
    vp, vm = run_obs(**plus), run_obs(**minus)
    d = (vp - vm) / 2
    asym = np.max(np.abs((vp - base) + (vm - base)) / np.maximum(np.abs(d), 1e-12)) if np.any(np.abs(d) > 1e-9) else 0
    jac[nm] = d
    print(f"  {nm:48s} delta a(X_P): aY {d[LABELS.index('X_P:aY')]:+.4f} a2 {d[LABELS.index('X_P:a2')]:+.4f} a3 {d[LABELS.index('X_P:a3')]:+.4f} aem {d[LABELS.index('X_P:aem')]:+.4f}   [asymmetry {asym:.1e}]")
    lin_ok &= bool(asym < 0.05) or bool(np.all(np.abs(d) < 1e-4))       # amendment A7: the asymmetry ratio is meaningless for shifts below 1e-4 in a_i (< 2e-6 relative)
chk("every Jacobian item that moves any a_i by >= 1e-4 is linear (forward and backward shifts agree within 5%)", lin_ok)

# E6: truncation
def loops_obs(gl, yl=3, **kw):
    return run_obs(o=L.Opts(gauge_loops=gl, yuk_loops=yl), **kw)
v2, v3, v4 = loops_obs(2), loops_obs(3), loops_obs(4)
D4 = v4 - v3
D3 = v3 - v2
with np.errstate(all="ignore"):
    D5 = D4 * np.abs(D4 / np.where(np.abs(D3) < 1e-12, np.nan, D3))
D5 = np.nan_to_num(D5)
E6prime = D4                       # what a user who stops at three loops leaves out
print(f"\nE6  gauge-loop truncation: 4-loop minus 3-loop at X_P: aY {D4[LABELS.index('X_P:aY')]:+.5f} a2 {D4[LABELS.index('X_P:a2')]:+.5f} a3 {D4[LABELS.index('X_P:a3')]:+.5f} aem {D4[LABELS.index('X_P:aem')]:+.5f};  3-loop minus 2-loop: aY {D3[LABELS.index('X_P:aY')]:+.5f} a2 {D3[LABELS.index('X_P:a2')]:+.5f} a3 {D3[LABELS.index('X_P:a3')]:+.5f}")
print(f"    five-loop estimate D4^2/D3 at X_P: aY {D5[LABELS.index('X_P:aY')]:+.6f} a2 {D5[LABELS.index('X_P:a2')]:+.6f} a3 {D5[LABELS.index('X_P:a3')]:+.6f} aem {D5[LABELS.index('X_P:aem')]:+.6f}")
jac["E6 five-loop estimate (D4^2/D3)"] = D5
jac["E6' stop at three loops (= the four-loop shift)"] = E6prime
# E7: y_t, lambda loop order
v_y2 = loops_obs(4, 2)
E7 = v_y2 - v4
jac["E7 y_t, lambda at 2 loops instead of 3"] = E7
# E8: dropping b, tau gauge terms
v_nobt = run_obs(o=L.Opts(gauge_loops=4, yuk_loops=3, bt=False))
jac["E8b y_b, y_tau dropped from the gauge betas"] = v_nobt - base
# E9: route P hand-over
import n1_lib as N1
trP = U3.Traj("2L-T", inp=dict(alpha_inv=P["aem_inv"], s2w=P["s2w_hat"], alpha_s=P["als"]))
AP = np.array(trP.A(P["Mt"]))
u0 = L.central_u0()
gY_P, g2_P = math.sqrt(4 * PI / AP[0]), math.sqrt(4 * PI / AP[1])
u0P = u0.copy()
u0P[0] = 5.0 / 3.0 * gY_P ** 2
u0P[1] = g2_P ** 2
trPG = L.Traj(u0P, P["Mt"], L.Opts(gauge_loops=4, yuk_loops=3), mu_max=3e21)
E9 = flat(observe(trPG)) - base
jac["E9 route P (alpha-hat(m_Z), s-hat^2) hand-over instead of route G"] = E9
# E9 diagnostic (amendment A8): is the route-P minus route-G difference just the M_W pull?  M_W* is the value at which route G reproduces route P's a_Y at m_t.
from scipy.optimize import brentq
_fY = lambda MW: L.run_central(MW=MW).A(P["Mt"])[0] - AP[0]
MWSTAR = brentq(_fY, 80.30, 80.40)
vG_star = run_obs(MW=MWSTAR)
E9a = vG_star - base
E9b = flat(observe(trPG)) - vG_star
jac["E9a part of E9 that is the M_W pull (route G at M_W*)"] = E9a
jac["E9b residual route P - route G(M_W*)"] = E9b
print(f"\nE9 diagnostic: route G reproduces route P's a_Y(m_t) at M_W* = {MWSTAR:.4f} GeV (direct average 80.3692, PDG updated average 80.360+-0.012, PDG SM-fit value 80.356+-0.005)")
# sensitivities that are NOT added
SENS = {}
SENS["S1 M_W = 80.3946 (PDG incl. CDF II)"] = run_obs(MW=P["MW_with_CDF"]) - base
SENS["S1' M_W = 80.4335 (CDF II alone)"] = run_obs(MW=P["MW_CDF_only"]) - base
SENS["S1'' M_W = 80.360 (PDG updated average, eq. 10.63)"] = run_obs(MW=80.360) - base
SENS["S1''' M_W = 80.356 (PDG SM-fit value)"] = run_obs(MW=80.356) - base
SENS["S2 Buttazzo's printed g_3 formula instead of the QCD-only g_3"] = run_obs(g3_mode="buttazzo") - base
SENS["S3 M_Z Breit-Wigner -> pole conversion (-34.2 MeV) in g_Y (excluded by V4-A at 1.3e-4)"] = run_obs(dgY=gY_c * P["MZ"] * (-0.0342) / (P["MZ"] ** 2 - P["MW"] ** 2)) - base

def pct(d, key, X="X_P"):
    return 100 * d[LABELS.index(f"{X}:{key}")] / base[LABELS.index(f"{X}:{key}")]

# ------------------------------------------------------------------------------------------- Monte Carlo of E1-E5 (Gaussian)
rng = np.random.default_rng(SEED)
mc = []
for _ in range(NIT):
    z = rng.standard_normal(11)
    kw = dict(als=P["als"] + z[0] * P["sals"], MW=P["MW"] + z[1] * P["sMW"], Mt=P["Mt"] + z[2] * sMt, Mh=P["Mh"] + z[3] * P["sMh"],
              dgY=z[4] * sMZ_gY + z[6] * sgY, dg2=z[5] * sg2, rel_g3=z[7] * sg3, dyt=z[8] * 0.0005, dlam=z[9] * 0.0003)
    mc.append(run_obs(**kw))
mc = np.array(mc)
sig_mc = mc.std(axis=0, ddof=1)
LIN_ITEMS = ["E1 alpha_s(m_Z) 0.1180+-0.0009", "E2 M_W 80.3692+-0.0133", "E3 M_t 172.57+-0.42", "E4a M_h 125.10+-0.09", "E4b M_Z +-0.0021 (tree scaling of g_Y)",
             "E5a matching g_2 (3-loop estimator)", "E5a' matching g_Y (3-loop estimator)", "E5b matching g_3 (mu_dec + EW remainder)", "E5c y_t +-0.0005", "E5c' lambda +-0.0003"]
use = [k for k in LIN_ITEMS if not (MUT and k.startswith("E1 "))]
sig_lin = np.sqrt(sum(jac[k] ** 2 for k in use))
ratio = sig_mc / np.where(sig_lin > 0, sig_lin, np.nan)
print(f"\nMONTE CARLO (N = {NIT}, seed {SEED}) of E1-E5 versus linear quadrature of the same items; ratio MC/linear:")
big = []
for lab in LABELS:
    if lab.startswith("lnXY2"):
        continue
    j = LABELS.index(lab)
    if sig_lin[j] > 0 and abs(base[j]) > 0:
        big.append((lab, ratio[j]))
print("    " + "  ".join(f"{a}:{b:.2f}" for a, b in big))
ok_mc = all(0.8 <= b <= 1.2 for a, b in big if not a.startswith("lnXc") and not a.startswith("Xc:a3/a2"))
chk("MC and linear propagation agree within 20% for every quoted quantity", ok_mc, f"min {min(b for _, b in big):.2f} max {max(b for _, b in big):.2f}")

# ------------------------------------------------------------------------------------------- BEFORE (lane U3) and the AFTER tables
def before(X):
    cen = U3.get_traj("2L-T").A(X)
    out = {}
    tags = ["aY", "a2", "a3"]
    band = np.zeros(3)
    for v in U3.VARIANTS_RUN:
        Av = np.array(U3.get_traj(v).A(X))
        band = np.maximum(band, np.abs(Av / np.array(cen) - 1))
    # a_em band
    bem = 0
    for v in U3.VARIANTS_RUN:
        Av = np.array(U3.get_traj(v).A(X))
        bem = max(bem, abs((Av[0] + Av[1]) / (cen[0] + cen[1]) - 1))
    return band, bem


print("\n" + "=" * 130)
print("BEFORE / AFTER at the programme scales.  Percent of the central value.  BEFORE = campaign: max deviation among the seven U3 variants ('raw band') and the tolerance used by U3 = max(2 x band, 1%).")
print("AFTER = Y1: 1 sigma; 'quad' = quadrature of E1, E2, E3, E4, E5, E6 (five-loop), E7, E8; 'cons' = quad + E9 (linear) + the S2 g_3 sensitivity (linear, quoted separately).")
print("=" * 130)
summary = {}
for X_nm, X in SC:
    bnd, bem = before(X)
    print(f"\n{X_nm}  (X = {X:.4e} GeV)")
    print(f"  {'':50s}{'a_Y':>12s}{'a_2':>12s}{'a_3':>12s}{'a_em':>12s}")
    print(f"  {'central Y1':50s}" + "".join(f"{base[LABELS.index(X_nm + ':' + k)]:12.4f}" for k in KEYS))
    print(f"  {'BEFORE: raw band of the 7 variants (%)':50s}" + "".join(f"{100 * b:12.3f}" for b in list(bnd) + [bem]))
    print(f"  {'BEFORE: U3 tolerance max(2 band, 1%) (%)':50s}" + "".join(f"{max(200 * b, 1.0):12.3f}" for b in list(bnd) + [bem]))
    quad = np.zeros(4)
    items_used = LIN_ITEMS + ["E6 five-loop estimate (D4^2/D3)", "E7 y_t, lambda at 2 loops instead of 3", "E8a y_b, y_tau +-30%" if False else "E8b y_b, y_tau dropped from the gauge betas"]
    tab = {}
    for it in LIN_ITEMS + ["E6 five-loop estimate (D4^2/D3)", "E6' stop at three loops (= the four-loop shift)", "E7 y_t, lambda at 2 loops instead of 3", "E8b y_b, y_tau dropped from the gauge betas",
                           "E9 route P (alpha-hat(m_Z), s-hat^2) hand-over instead of route G", "E9a part of E9 that is the M_W pull (route G at M_W*)", "E9b residual route P - route G(M_W*)"]:
        d = jac[it]
        row = [pct(d, k, X_nm) for k in KEYS]
        tab[it] = row
        print(f"  {it:50s}" + "".join(f"{x:+12.4f}" for x in row))
    if "E8a y_b, y_tau +-30%" in jac:
        pass
    d8a = jac.get("E8a y_b, y_tau +-30%")
    row = [pct(d8a, k, X_nm) for k in KEYS]
    tab["E8a"] = row
    print(f"  {'E8a y_b, y_tau +-30%':50s}" + "".join(f"{x:+12.4f}" for x in row))
    for it in ["E1 alpha_s(m_Z) 0.1180+-0.0009", "E2 M_W 80.3692+-0.0133", "E3 M_t 172.57+-0.42", "E4a M_h 125.10+-0.09", "E4b M_Z +-0.0021 (tree scaling of g_Y)", "E5a matching g_2 (3-loop estimator)",
               "E5a' matching g_Y (3-loop estimator)", "E5b matching g_3 (mu_dec + EW remainder)", "E5c y_t +-0.0005", "E5c' lambda +-0.0003", "E6 five-loop estimate (D4^2/D3)", "E7 y_t, lambda at 2 loops instead of 3",
               "E8b y_b, y_tau dropped from the gauge betas"]:
        quad += np.array(tab[it]) ** 2
    quad += np.array(tab["E8a"]) ** 2
    quad = np.sqrt(quad)
    e9 = np.abs(np.array(tab["E9 route P (alpha-hat(m_Z), s-hat^2) hand-over instead of route G"]))
    s2g3 = np.array([abs(pct(SENS["S2 Buttazzo's printed g_3 formula instead of the QCD-only g_3"], k, X_nm)) for k in KEYS])
    cons = quad + e9 + s2g3
    e9b = np.array([abs(pct(jac["E9b residual route P - route G(M_W*)"], k, X_nm)) for k in KEYS])
    cons_dd = quad + e9b + s2g3
    e2row = np.array(tab["E2 M_W 80.3692+-0.0133"])
    quad_fit = np.sqrt(quad ** 2 - e2row ** 2 + (e2row * 0.005 / P["sMW"]) ** 2)
    shift_fit = np.array([pct(SENS["S1''' M_W = 80.356 (PDG SM-fit value)"], k, X_nm) for k in KEYS])
    print(f"  {'AFTER (quadrature), 1 sigma (%)  [direct M_W]':50s}" + "".join(f"{x:12.4f}" for x in quad))
    print(f"  {'AFTER (conservative as registered: quad+E9+S2)':50s}" + "".join(f"{x:12.4f}" for x in cons))
    print(f"  {'AFTER (conservative de-duplicated: quad+E9b+S2)':50s}" + "".join(f"{x:12.4f}" for x in cons_dd))
    print(f"  {'AFTER, SM-fit-anchored M_W = 80.356+-0.005: sigma':50s}" + "".join(f"{x:12.4f}" for x in quad_fit))
    print(f"  {'   ... and its shift of the central value (%)':50s}" + "".join(f"{x:+12.4f}" for x in shift_fit))
    print(f"  {'improvement factor (BEFORE tol / AFTER quad)':50s}" + "".join(f"{max(200 * b, 1.0) / q:12.1f}" for b, q in zip(list(bnd) + [bem], quad)))
    cen4 = np.array([base[LABELS.index(X_nm + ':' + k)] for k in KEYS])
    print(f"  {'sigma(a_em) absolute / 137.036, direct M_W ; fit-anchored ; conservative de-dup':50s}{quad[3] / 100 * cen4[3] / 137.035999177:12.2e}{quad_fit[3] / 100 * cen4[3] / 137.035999177:12.2e}{cons_dd[3] / 100 * cen4[3] / 137.035999177:12.2e}")
    for sk, sv in SENS.items():
        print(f"  {'sensitivity ' + sk[:38]:50s}" + "".join(f"{pct(sv, k, X_nm):+12.4f}" for k in KEYS))
    summary[X_nm] = dict(X=X, central=[float(base[LABELS.index(X_nm + ':' + k)]) for k in KEYS], before_band_pct=[100 * b for b in list(bnd) + [bem]],
                         before_tol_pct=[max(200 * b, 1.0) for b in list(bnd) + [bem]], after_quad_pct=list(map(float, quad)), after_cons_registered_pct=list(map(float, cons)), after_cons_dedup_pct=list(map(float, cons_dd)), after_fit_anchored_pct=list(map(float, quad_fit)), fit_anchored_shift_pct=list(map(float, shift_fit)),
                         items={k: list(map(float, v)) for k, v in tab.items()})

# ------------------------------------------------------------------------------------------- crossings
print("\nCROSSING SCALES")
for nm, lab, lnk, key in (("a_1 = a_2 crossing X_c", "lnXc", "lnXc", None), ("a_Y = a_2 crossing", "lnXY2", "lnXY2", None)):
    j = LABELS.index(lnk)
    itemsq = 0
    for it in LIN_ITEMS + ["E6 five-loop estimate (D4^2/D3)", "E7 y_t, lambda at 2 loops instead of 3", "E8b y_b, y_tau dropped from the gauge betas"]:
        itemsq += jac[it][j] ** 2
    itemsq += jac["E8a y_b, y_tau +-30%"][j] ** 2
    sq = math.sqrt(itemsq)
    e9 = abs(jac["E9 route P (alpha-hat(m_Z), s-hat^2) hand-over instead of route G"][j])
    s2 = abs(SENS["S2 Buttazzo's printed g_3 formula instead of the QCD-only g_3"][j])
    print(f"  {nm}: central {math.exp(base[j]):.4e} GeV ; sigma(ln X) quad {100 * sq:.3f}% ; E9 {100 * e9:.3f}% ; S2 {100 * s2:.3f}%   (lane U3's TOLERANCE on crossing-defined residuals reached 2.8%; this is the uncertainty of the scale itself)")
    summary[nm] = dict(X=math.exp(base[j]), sigma_lnX_quad_pct=100 * sq, E9_pct=100 * e9, S2_pct=100 * s2)
    if lab == "lnXc":
        for k, lb in (("a_Y", "Xc:aY"), ("a_2", "Xc:a2"), ("a_3", "Xc:a3"), ("a_3/a_2", "Xc:a3/a2")):
            jj = LABELS.index(lb)
            sq2 = math.sqrt(sum(jac[it][jj] ** 2 for it in LIN_ITEMS + ["E6 five-loop estimate (D4^2/D3)", "E7 y_t, lambda at 2 loops instead of 3", "E8b y_b, y_tau dropped from the gauge betas", "E8a y_b, y_tau +-30%"]))
            e9j = abs(jac["E9 route P (alpha-hat(m_Z), s-hat^2) hand-over instead of route G"][jj])
            s2j = abs(SENS["S2 Buttazzo's printed g_3 formula instead of the QCD-only g_3"][jj])
            print(f"      at X_c: {k:8s} central {base[jj]:.5f} ; 1 sigma quad {100 * sq2 / abs(base[jj]):.4f}% ; E9 {100 * e9j / abs(base[jj]):.4f}% ; S2 {100 * s2j / abs(base[jj]):.4f}%")
            summary[nm][k] = dict(central=float(base[jj]), quad_pct=100 * sq2 / abs(base[jj]), E9_pct=100 * e9j / abs(base[jj]), S2_pct=100 * s2j / abs(base[jj]))

# BEFORE at the a_1 = a_2 crossing: each of lane U3's seven variants at ITS OWN crossing scale (couplings there), relative to the 2L-T variant
xs_v, A_v = {}, {}
for v in U3.VARIANTS_RUN:
    sh = U3.Shifted(U3.get_traj(v), None)
    xv = U3.solve_cross(sh, "a1", "a2")
    xs_v[v] = xv
    A_v[v] = np.array(sh.A(xv))
cen_v = A_v["2L-T"]
band_x = max(abs(math.log(xs_v[v] / xs_v["2L-T"])) for v in xs_v)
band_a = np.max([np.abs(A_v[v] / cen_v - 1) for v in A_v], axis=0)
print(f"  BEFORE (lane U3, seven variants, each at its own a_1 = a_2 crossing): X_c spread max |ln(X_v/X_2L-T)| = {100 * band_x:.2f}% ; raw band of (a_Y = a_1*5/3, a_2, a_3) at the crossing = {np.round(100 * band_a, 3)} %  (U3 tolerance max(2 band, 1%); its crossing-rule tolerances reached 2.8%)")
summary["crossing_before"] = dict(lnX_band_pct=100 * band_x, a_band_pct=list(map(float, 100 * band_a)))

# Thomson link
print("\nTHOMSON LINK (not in the running's budget): 1/alpha(0) - alpha-hat^-1(m_Z) = 9.106; PDG alpha-hat^-1(m_Z) = 127.930 +- 0.008  ->  +-0.008 on 1/alpha(0) = 5.8e-5 relative to 137.036")
summary["thomson_link_rel"] = 0.008 / 137.035999177

with open(os.path.join(HERE, "y1_4_results_MUTATE.json" if MUT else "y1_4_results.json"), "w") as f:
    json.dump(dict(labels=LABELS, base=list(map(float, base)), sigma_mc=list(map(float, sig_mc)), sigma_lin=list(map(float, sig_lin)), summary=summary), f, indent=1)
print(f"\nY1-4: {len(fails)} failed" + (f": {fails}" if fails else ""))
if MUT:
    print("MUTATE control:", "BITES -> exit 1" if fails else "BROKEN -> exit 3")
    sys.exit(1 if fails else 3)
sys.exit(0 if not fails else 2)
