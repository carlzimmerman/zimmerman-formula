#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG291 -- KHRONON DIPOLE RADIATION IN BINARY PULSARS OVER THE FILTERED C-H/K WINDOW (recipe G7 / G11-G12).
Criteria frozen and committed first: campaign_fresh_gravity/CFG291_khronon_binary_pulsar/FROZEN_CRITERIA.md (9b2bc6fe0).

THE CHASSIS (L340; XC1): I_CHK = I_CH + c^3/(16 pi G) Int sqrt(-g)[alpha_c a.a - c_2 K^2], beta = 0, with C-H's heat
filter S = exp((xi^2/2) Delta) on the MOND kernel nu_mono.  Above k ~ 1/xi the filter removes the C-H sector and the
khronon IS the BPS khronon with alpha = alpha_c, lambda = c_2, beta = 0 (XC1 A3).  Neutron stars and orbits sit far
above 1/xi; the khronon's radiated wavelength at orbital frequencies does not (section N/WZ below).

ADOPTED: Barausse 2019 (PRD 100 084053) flux and coefficients; Yagi et al. 2014 (PRL 112 161101) Pb-dot form; Foster
2007 (PRD 76 084033) eq. 70 weak-field sensitivity; the khronometric PPN alpha1, alpha2; Peters-Mathews.
DERIVED HERE: the wave-zone factor R_l for the khronon's MOND-regime clock inertia (decoupling limit, XC1 A1/A3/A5).

MUTATE=1 scores lambda_K = 2 (c_2 = 1): the window gate must flag it (rc = 1).  Outputs carry _MUTATE.
Run from anywhere:  python3 campaign_fresh_gravity/CFG291_khronon_binary_pulsar/cfg291_khronon_binary_pulsar.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "cfg291_khronon_binary_pulsar"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "CFG291", "mutate": MUTATE, "frozen_criteria_commit": "9b2bc6fe0", "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def rel(p):
    return os.path.relpath(p, REPO)


P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: the scored window is lambda_K = 2 (c_2 = 1); the window gate must FAIL (rc = 1) ***")

# ================================================================================================ constants and inputs
C_SI = 299792458.0
G_SI = 6.67430e-11
T_SUN = 4.925490947e-6                     # G M_sun / c^3 [s]
GM_SUN = T_SUN * C_SI**3
PC = 3.0856775814913673e16
DAY = 86400.0
MPL_RED = 2.435e18                         # GeV (as XC1)
LHC_GEV = 1.3e4
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}     # kappa = 1/2 FITTED (canonical); alt footing (XC1 FOOT)
GEXT = 2.32e-10                            # L340 S1: the Galactic field at the Sun (m/s^2)
OMEGA_OVER_M_MAX = 0.3                     # frozen |Omega/m| upper bound for every neutron star
V_CM = 600e3 / C_SI                        # frozen: L340's tracking velocity scale
R_NS = 12e3                                # nominal NS radius, used only for a displayed filter exponent

L340F = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")
L350F = os.path.join(REPO, "real_research", "g03_audit_2026", "L350_chk_cosmological_G_gate_results.json")
XC1F = os.path.join(REPO, "real_research", "extra_crispy_2026", "XC1_strong_coupling_chk_results.json")
L340 = json.load(open(L340F)); L350 = json.load(open(L350F)); XC1 = json.load(open(XC1F))
AC_MIN, AC_MAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
C2_MIN, C2_MAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
S1 = L340["numbers"]["S1"]
XI_FLOORS_PC = sorted({0.031, 0.045} | {round(v[k], 5) for v in S1.values() for k in ("xi_Q2", "xi_M")})
CAPS = sorted(float(r["c2_ceiling"]) for r in L350["numbers"]["G2"]["rows"] if r.get("c2_ceiling") is not None)
XC1_CS = (XC1["numbers"]["A9"]["cs_uv_min"], XC1["numbers"]["A9"]["cs_uv_max"])

P(f"\n  inputs ({rel(L340F)}): alpha_c in [{AC_MIN:.6e}, {AC_MAX:.3e}], c_2 in [{C2_MIN:.6e}, {C2_MAX:.6e}]")
P(f"  xi floors (recipe I5 + L340 S1) [pc]: {XI_FLOORS_PC};  L350 Planck-era c_2 ceilings: {[f'{c:.2e}' for c in CAPS]}")
P(f"  XC1 A9 committed UV khronon speeds: {XC1_CS[0]:.4e} c .. {XC1_CS[1]:.4e} c")
OUT["numbers"]["inputs"] = {"alpha_c": [AC_MIN, AC_MAX], "c2": [C2_MIN, C2_MAX], "xi_floors_pc": XI_FLOORS_PC,
                            "L350_caps": CAPS, "a0": A0, "GEXT": GEXT, "Omega_over_m_max": OMEGA_OVER_M_MAX,
                            "V_CM_over_c": V_CM, "sources": [rel(L340F), rel(L350F), rel(XC1F)]}

# pulsar systems (FROZEN_CRITERIA sec. 4); lo/hi = allowed delta at 2 sigma / 95%
SYSTEMS = {
    "J1738+0333": dict(Pb_d=0.3547907398724, e=3.4e-7, m1=1.46, m2=0.181, kind="NS-WD", lo=-(2.0 + 2 * 3.7) / 27.7,
                       hi=(2 * 3.6 - 2.0) / 27.7, GR_pub=(-27.7e-15, 1.5e-15, 1.9e-15),
                       src="Freire+2012 MNRAS 423 3328 (Table 1; abstract)"),
    "J0348+0432": dict(Pb_d=0.102424062722, e=2.0e-6, m1=2.01, m2=0.172, kind="NS-WD", lo=1.05 - 2 * 0.18 - 1,
                       hi=1.05 + 2 * 0.18 - 1, GR_pub=(-0.258e-12, 0.008e-12, 0.011e-12),
                       src="Antoniadis+2013 Science 340 6131 (Table 1)"),
    "J0737-3039A/B": dict(Pb_d=0.10225, e=0.0877775, m1=1.338185, m2=1.248868, kind="NS-NS", lo=-1.3e-4, hi=1.3e-4,
                          GR_pub=None, src="Kramer+2021 PRX 11 041050 (abstract: 1.3e-4 at 95%)"),
}
for nm, s in SYSTEMS.items():
    P(f"  {nm:14s} P_b = {s['Pb_d']} d, e = {s['e']:.3g}, m = {s['m1']}/{s['m2']} Msun ({s['kind']}): "
      f"allowed delta in [{s['lo']:+.4g}, {s['hi']:+.4g}]   [{s['src']}]")
OUT["numbers"]["systems"] = {k: {kk: vv for kk, vv in v.items()} for k, v in SYSTEMS.items()}

# ================================================================================================ C9 the kernel
banner("C9  THE KERNEL nu_mono, reimplemented from the recipe/L340 definition, against L340's committed A1 numbers")
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P)); DELTA = 0.05
Y_STAR = brentq(lambda y: float(dh_rar(y)) - DELTA * H_P / (y + Y_P), 1.0, Y_P)
LYG = np.linspace(-12, 12, 240001); YG = 10**LYG
DH_MONO = np.maximum(dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
H_STAR = float(np.interp(math.log10(Y_STAR), LYG, H_MONO))
def h_mono(y):
    y = np.asarray(y, float)
    tail = H_STAR + DELTA * H_P * np.log((y + Y_P) / (Y_STAR + Y_P))      # exact above y* (h' = delta h_p/(y+y_p))
    return np.where(y <= 1e11, np.interp(np.log10(np.maximum(y, 1e-12)), LYG, H_MONO), tail)
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + h_mono(y) / y
def CL_of(nuf, y):
    y = np.asarray(y, float); e = 1e-5
    return ((y * (1 + e)) * nuf(y * (1 + e)) - (y * (1 - e)) * nuf(y * (1 - e))) / (2 * y * e) - 1.0
ys = np.logspace(-3, 4, 1401)
minCT = float((nu_mono(ys) - 1).min()); minCL = float(CL_of(nu_mono, ys).min())
A1ref = L340["numbers"]["A1"]
tail_vs_grid = float(abs(h_mono(np.array([2e10]))[0] / (H_STAR + DELTA * H_P * math.log((2e10 + Y_P) / (Y_STAR + Y_P))) - 1))
P(f"    y_p = {Y_P:.6f} (L340 {A1ref['y_p']:.6f}), h_p = {H_P:.6f} (L340 {A1ref['h_p']:.6f}), y* = {Y_STAR:.5f}")
P(f"    min C_T = {minCT:.6e} (L340 {A1ref['min_CT']:.6e}), min C_L = {minCL:.6e} (L340 {A1ref['min_CL']:.6e})")
P(f"    closed-form tail above y* vs the grid integral at y = 2e10: relative difference {tail_vs_grid:.1e}")
okC9 = (abs(Y_P / A1ref["y_p"] - 1) < 1e-4 and abs(H_P / A1ref["h_p"] - 1) < 1e-4 and abs(minCT / A1ref["min_CT"] - 1) < 1e-4
        and abs(minCL / A1ref["min_CL"] - 1) < 1e-4 and abs(Y_STAR - 2.3374) < 1e-4 and tail_vs_grid < 1e-6)
OUT["numbers"]["C9"] = {"y_p": Y_P, "h_p": H_P, "y_star": Y_STAR, "min_CT": minCT, "min_CL": minCL}
check("C9 nu_mono reproduces L340's y_p, h_p, min C_T, min C_L to 1e-4 and y* = 2.3374", f"y* = {Y_STAR:.5f}; "
      f"ratios {Y_P / A1ref['y_p']:.7f}, {H_P / A1ref['h_p']:.7f}, {minCT / A1ref['min_CT']:.6f}, {minCL / A1ref['min_CL']:.6f}", okC9)

# ================================================================================================ formulas (sympy)
banner("FORMULAS  Barausse 2019 eqs. 15-22, khronometric PPN; C2 the published alpha, beta -> 0 limit; C3, C4")
al, be, la, kk = sp.symbols('alpha beta lambda k', positive=True)
c0sq_s = (la + be) * (2 - al) / (al * (1 - be) * (2 + 3 * la + be))
cT_s = 1 / sp.sqrt(1 - be)
a1_s = 4 * (al - 2 * be) / (be - 1)
a2_s = (al - 2 * be) * (-be**2 + be * (al - 3) + al + la * (-1 - 3 * be + 2 * al)) / ((be - 1) * (la + be) * (al - 2))
Z_s = (a1_s - 2 * a2_s) * (1 - be) / (3 * (2 * be - al))
c0_s = sp.sqrt(c0sq_s)
A1_s = 1 / cT_s + 3 * al * (Z_s - 1)**2 / (2 * c0_s * (2 - al))
A2_s = 2 * (Z_s - 1) / ((al - 2) * c0_s**3)
A3_s = 2 / (3 * al * (2 - al) * c0_s**5)
B_s = 1 / (9 * al * c0_s**5 * (2 - al))
Cd_s = 4 / (3 * c0_s**3 * al * (2 - al))
# beta = 0 closed forms (exact; Z - 1 simplified to avoid cancellation)
Zm1_b0 = sp.factor(sp.simplify((Z_s - 1).subs(be, 0)))
a1_b0 = sp.simplify(a1_s.subs(be, 0)); a2_b0 = sp.factor(sp.simplify(a2_s.subs(be, 0)))
P(f"    beta = 0:  alpha1 = {a1_b0};  alpha2 = {a2_b0};  Z - 1 = {Zm1_b0};  c0^2 = {sp.factor(c0sq_s.subs(be, 0))};  c_T = {cT_s.subs(be, 0)}")
f_c0sq = sp.lambdify((al, la), c0sq_s.subs(be, 0), "math")
f_a1 = sp.lambdify((al, la), a1_b0, "math"); f_a2 = sp.lambdify((al, la), a2_b0, "math")
f_Zm1 = sp.lambdify((al, la), Zm1_b0, "math")

def coeffs(alpha, lam):
    """Barausse 2019 eqs. 18-22 at beta = 0 (c_T = 1)."""
    c0 = math.sqrt(f_c0sq(alpha, lam)); zm1 = f_Zm1(alpha, lam)
    return dict(c0=c0, Zm1=zm1, A1m1=3 * alpha * zm1**2 / (2 * c0 * (2 - alpha)), A2=2 * zm1 / ((alpha - 2) * c0**3),
                A3=2 / (3 * alpha * (2 - alpha) * c0**5), B=1 / (9 * alpha * c0**5 * (2 - alpha)),
                C=4 / (3 * c0**3 * alpha * (2 - alpha)), a1=f_a1(alpha, lam), a2=f_a2(alpha, lam))

# C2: the published limit, along two rays beta = 0 and beta = alpha/3
lims = {}
for ray, sub in (("beta=0", {be: 0}), ("beta=alpha/3", {be: al / 3})):
    lims[ray] = [sp.limit(sp.simplify(expr.subs(sub)), al, 0, '+') for expr in (A1_s, A2_s, A3_s, B_s, Cd_s)]
P(f"    alpha -> 0 limits of (A1, A2, A3, B, C): {lims}")
okC2 = all(l_[0] == 1 and all(x == 0 for x in l_[1:]) for l_ in lims.values()) and cT_s.subs(be, 0) == 1
check("C2 Barausse 2019's stated limit: as alpha, beta -> 0 (lambda != 0) A1 -> 1 and A2, A3, B, C -> 0; c_T = 1 at beta = 0",
      str(lims), okC2, "in that limit the khronon's speed diverges and every non-GR radiative coefficient vanishes")

# C3: record cross-checks
cs_xc1 = [math.sqrt(f_c0sq(a_, c_)) for a_ in (AC_MIN, AC_MAX) for c_ in (min([round(c, 6) for c in CAPS] + [C2_MIN]), C2_MAX)]   # XC1 rounds caps to 6 dp
a2dev = max(abs(f_a2(a_, c_) / (-a_ / 2) - 1) for a_ in np.logspace(math.log10(AC_MIN), math.log10(AC_MAX), 9)
            for c_ in np.logspace(math.log10(C2_MIN), math.log10(C2_MAX), 9))
P(f"    c0 at XC1's corners: {min(cs_xc1):.4e} .. {max(cs_xc1):.4e} c  (XC1 A9 committed: {XC1_CS[0]:.4e} .. {XC1_CS[1]:.4e})")
P(f"    alpha1 at beta = 0: {a1_b0} ;  max |alpha2/(-alpha_c/2) - 1| over W1 = {a2dev:.2e}")
okC3 = (abs(min(cs_xc1) / XC1_CS[0] - 1) < 5e-5 and abs(max(cs_xc1) / XC1_CS[1] - 1) < 5e-5
        and sp.simplify(a1_b0 + 4 * al) == 0 and a2dev < 1e-6)
check("C3 F1's c0 reproduces XC1's committed UV speeds (4 s.f.); alpha1 = -4 alpha_c exactly and alpha2 -> -alpha_c/2 "
      "within 1e-6 over W1 (L340 P1's formulas)", f"{min(cs_xc1):.4e}/{max(cs_xc1):.4e} c; alpha2 dev {a2dev:.1e}", okC3)

# C4: the map alpha = alpha_c, lambda = c_2 (XC1 A1 decoupling speed c0^2 = c_2/alpha)
amap, cmap = 1e-12, 1e-6
ratios = {nm: f_c0sq(amap, f(cmap)) / (cmap / amap) for nm, f in (("lambda=c_2", lambda c: c), ("lambda=c_2/2", lambda c: c / 2),
                                                                  ("lambda=2c_2", lambda c: 2 * c))}
P(f"    F1 c0^2 / (c_2/alpha) at alpha = {amap}, c_2 = {cmap}: " + ", ".join(f"{k_}: {v_:.6f}" for k_, v_ in ratios.items()))
okC4 = abs(ratios["lambda=c_2"] - 1) < 1e-5 and abs(ratios["lambda=c_2/2"] - 1) > 0.4 and abs(ratios["lambda=2c_2"] - 1) > 0.4
check("C4 the map alpha = alpha_c, beta = 0, lambda = c_2: F1's speed matches XC1's decoupling-limit c_2/alpha to "
      "O(alpha, lambda); the wrong maps lambda = c_2/2 and 2 c_2 fail", str({k_: round(v_, 6) for k_, v_ in ratios.items()}), okC4,
      "L340's action alpha_c a.a - c_2 K^2 is the BPS covariant alpha- and lambda-term term by term (mostly-plus signature)")
OUT["numbers"]["formulas"] = {"alpha1_b0": str(a1_b0), "alpha2_b0": str(a2_b0), "Zm1_b0": str(Zm1_b0),
                              "C2_limits": {k_: [str(x) for x in v_] for k_, v_ in lims.items()}, "C3_cs": cs_xc1,
                              "C3_alpha2_dev": a2dev, "C4_ratios": ratios}

# ================================================================================================ C1 GR reproduction
banner("C1  GR Pb-dot (Peters-Mathews) from each paper's own masses, against the published GR predictions")
def fe(e):
    return (1 + 73 / 24 * e**2 + 37 / 96 * e**4) / (1 - e**2)**3.5
def ge(e):
    return (1 + e**2 / 2) / (1 - e**2)**2.5
def pbdot_gr(s):
    Pb = s["Pb_d"] * DAY; m = s["m1"] + s["m2"]
    return -(192 * math.pi / 5) * (2 * math.pi / Pb)**(5 / 3) * T_SUN**(5 / 3) * s["m1"] * s["m2"] / m**(1 / 3) * fe(s["e"])
C1rows = {}
for nm, s in SYSTEMS.items():
    v = pbdot_gr(s); C1rows[nm] = v
    if s["GR_pub"]:
        c_, up, dn = s["GR_pub"]
        P(f"    {nm:14s}: computed {v:.4e} s/s; published {c_:.3e} (+{up:.1e}/-{dn:.1e}); ratio {v / c_:.5f}")
    else:
        P(f"    {nm:14s}: computed {v:.5e} s/s (reading: no GR value read from the source; masses from a secondary page)")
okC1 = True
for nm in ("J1738+0333", "J0348+0432"):
    c_, up, dn = SYSTEMS[nm]["GR_pub"]; v = C1rows[nm]
    okC1 &= (c_ - dn <= v <= c_ + up) and abs(v / c_ - 1) < 0.01
OUT["numbers"]["C1"] = C1rows
check("C1 Peters-Mathews with the papers' masses reproduces J1738+0333's -27.7 fs/s and J0348+0432's -0.258 ps/s "
      "inside their quoted intervals and within 1%", "; ".join(f"{k_}: {v_:.4e}" for k_, v_ in C1rows.items()), okC1)

# ================================================================================================ near zone numbers
banner("N  THE NEAR ZONE: y at the orbit, the filter exponents, the filtered binary source (both footings)")
def orbit(s):
    Pb = s["Pb_d"] * DAY; m = s["m1"] + s["m2"]
    a = (GM_SUN * m * (Pb / (2 * math.pi))**2)**(1 / 3)
    v2 = (2 * math.pi * T_SUN * m / Pb)**(2 / 3)
    return Pb, m, a, v2
NZ = {}
xi_min = min(XI_FLOORS_PC) * PC
for nm, s in SYSTEMS.items():
    Pb, m, a, v2 = orbit(s); mu_over_m = s["m1"] * s["m2"] / m**2
    gN = GM_SUN * m / a**2; w = 2 * math.pi / Pb
    row = {"a_m": a, "v2": v2, "gN": gN}
    for foot, a0 in A0.items():
        y = gN / a0
        row[f"y_orb_{foot}"] = y; row[f"nu_minus_1_unfiltered_{foot}"] = float(nu_mono(np.array([y]))[0] - 1)
    row["filter_exponent_orbit"] = -(xi_min / a)**2; row["filter_exponent_NS"] = -(xi_min / R_NS)**2
    row["filtered_source_quadrupole_suppression"] = mu_over_m * (a / xi_min)**2
    row["filter_exponent_tensor_GW"] = -(xi_min * 2 * w / C_SI)**2
    NZ[nm] = row
    P(f"    {nm:14s} a = {a:.3e} m, v^2/c^2 = {v2:.3e}; y_orb = {row['y_orb_canonical']:.2e} (canon) / {row['y_orb_alt']:.2e} (alt); "
      f"unfiltered nu_mono - 1 = {row['nu_minus_1_unfiltered_canonical']:.1e}")
    P(f"    {'':14s} filter exponent at the orbit -(xi/a)^2 = {row['filter_exponent_orbit']:.2e}, at a NS -(xi/R)^2 = "
      f"{row['filter_exponent_NS']:.1e}, tensor GW -(xi k_GW)^2 = {row['filter_exponent_tensor_GW']:.2e}; "
      f"time-varying filtered source / static = (mu/m)(a/xi)^2 = {row['filtered_source_quadrupole_suppression']:.1e}")
OUT["numbers"]["near_zone"] = NZ
okN = all(r["filter_exponent_orbit"] < -1e9 and r["filter_exponent_tensor_GW"] < -1e5 and r["filtered_source_quadrupole_suppression"] < 1e-10
          for r in NZ.values())
check("N the near zone and the tensor waves are screened: the MOND kernel never sees the orbit (filter exponent < -1e9), "
      "the tensor-GW wavenumber (< -1e5), or more than 1e-10 of the binary's time-varying source",
      "; ".join(f"{k_}: {v_['filter_exponent_orbit']:.1e} / {v_['filter_exponent_tensor_GW']:.1e} / {v_['filtered_source_quadrupole_suppression']:.0e}"
                for k_, v_ in NZ.items()), okN,
      "even unfiltered, nu_mono - 1 at the orbit is ~1e-12 (y ~ 1e12): the near zone is GR + the BPS khronon", load_bearing=False)

# ================================================================================================ the wave zone
banner("WZ  THE WAVE ZONE: the khronon's radiated wavenumber vs 1/xi, and the factor R_l (derived, decoupling limit)")
def yN_of(a0):
    return brentq(lambda y: float(nu_mono(np.array([y]))[0]) * y - GEXT / a0, 1e-6, GEXT / a0 * 1.5, xtol=1e-14)
ENV_C0 = {}
for foot, a0 in A0.items():
    yv = yN_of(a0)
    ENV_C0[f"C_T y_N={yv:.3f} ({foot})"] = float(nu_mono(np.array([yv]))[0] - 1)
    ENV_C0[f"C_L y_N={yv:.3f} ({foot})"] = float(CL_of(nu_mono, np.array([yv]))[0])
ENV_C0["C_T y=2.3 (XC1 row)"] = float(nu_mono(np.array([2.3]))[0] - 1)
ENV_C0["C_L y=2.3 (XC1 row)"] = float(CL_of(nu_mono, np.array([2.3]))[0])
P("    Galactic-background constitutive coefficients C_0: " + ", ".join(f"{k_}: {v_:.4f}" for k_, v_ in ENV_C0.items()))
C0_MAX = max(ENV_C0.values())

def R_factor(alpha, lam, w, xi, C0, ell):
    """R_l = (k*/k_UV)^(2l-1) * 2 B k*/F'(k*), F(k) = B k^2 - alpha_eff(k) (w/c)^2 (FROZEN_CRITERIA F9)."""
    c0sq = f_c0sq(alpha, lam); B = alpha * c0sq; q2 = (w / C_SI)**2
    kUV = math.sqrt(q2 / c0sq)
    if C0 <= 0:
        return 1.0, kUV, kUV, alpha
    def aeff(k):
        Cx = C0 * math.exp(-(xi * k)**2); return alpha + 2 * Cx / (1 + Cx)
    F = lambda lk: B * math.exp(2 * lk) - aeff(math.exp(lk)) * q2
    lo, hi = math.log(kUV), math.log(kUV * math.sqrt((alpha + 2) / alpha) * 1.01)
    if F(lo) >= 0:
        ks = kUV
    else:
        ks = math.exp(brentq(F, lo, hi, xtol=1e-13, rtol=1e-13))
    Cx = C0 * math.exp(-(xi * ks)**2)
    daeff = 2 * (-2 * xi**2 * ks * Cx) / (1 + Cx)**2
    Fp = 2 * B * ks - daeff * q2
    return (ks / kUV)**(2 * ell - 1) * (2 * B * ks / Fp), ks, kUV, aeff(ks)

# C5 controls of the wave-zone model
Rzero = R_factor(1e-9, 0.02, 7e-4, xi_min, 0.0, 1)[0]
def logslope(f, x, h=1e-4):
    return (math.log(f(x * (1 + h))) - math.log(f(x * (1 - h)))) / (math.log(1 + h) - math.log(1 - h))
a_s, l_s = 1e-14, 1e-7
expo = {
    "C: dlnC/dlnalpha": logslope(lambda a_: coeffs(a_, l_s)["C"], a_s), "C: dlnC/dlnlambda": logslope(lambda l_: coeffs(a_s, l_)["C"], l_s),
    "A3: dlnA3/dlnalpha": logslope(lambda a_: coeffs(a_, l_s)["A3"], a_s), "A3: dlnA3/dlnlambda": logslope(lambda l_: coeffs(a_s, l_)["A3"], l_s)}
def P_model(alpha, lam, ell, w=7e-4):          # UV power of a k^ell source: k_UV^(2l-1)/(2B)
    c0sq = f_c0sq(alpha, lam); kUV = math.sqrt((w / C_SI)**2 / c0sq); return kUV**(2 * ell - 1) / (2 * alpha * c0sq)
expo_m = {"l=1 alpha": logslope(lambda a_: P_model(a_, l_s, 1), a_s), "l=1 lambda": logslope(lambda l_: P_model(a_s, l_, 1), l_s),
          "l=2 alpha": logslope(lambda a_: P_model(a_, l_s, 2), a_s), "l=2 lambda": logslope(lambda l_: P_model(a_s, l_, 2), l_s)}
P(f"    R_1 with C_0 = 0: {Rzero};  Barausse exponents: " + ", ".join(f"{k_} = {v_:+.4f}" for k_, v_ in expo.items()))
P(f"    model exponents (k^l source): " + ", ".join(f"{k_} = {v_:+.4f}" for k_, v_ in expo_m.items()))
okC5 = (Rzero == 1.0 and abs(expo["C: dlnC/dlnalpha"] - expo_m["l=1 alpha"]) < 1e-3 and abs(expo["C: dlnC/dlnlambda"] - expo_m["l=1 lambda"]) < 1e-3
        and abs(expo["A3: dlnA3/dlnalpha"] - expo_m["l=2 alpha"]) < 1e-3 and abs(expo["A3: dlnA3/dlnlambda"] - expo_m["l=2 lambda"]) < 1e-3
        and abs(expo_m["l=1 alpha"] - 0.5) < 1e-3 and abs(expo_m["l=1 lambda"] + 1.5) < 1e-3 and abs(expo_m["l=2 alpha"] - 1.5) < 1e-3
        and abs(expo_m["l=2 lambda"] + 2.5) < 1e-3)
OUT["numbers"]["C5"] = {"R_C0_zero": Rzero, "barausse_exponents": expo, "model_exponents": expo_m}
check("C5 the wave-zone model: R = 1 exactly at C_0 = 0; a k^1 source reproduces the exponents of Barausse's C "
      "(+1/2 in alpha, -3/2 in lambda) and a k^2 source those of A3 (+3/2, -5/2)", f"{expo} vs {expo_m}", okC5,
      "a time-derivative coupling would give 1/(alpha c0) instead: the sensitivity couples through u_i ~ d_i pi")

def env_R(alpha, lam, w, ell):
    """maximum computed R over the committed xi floors and the Galactic C_0 cells (FROZEN_CRITERIA sec. 7)."""
    best = None
    for xi_pc in XI_FLOORS_PC:
        for lab, C0 in ENV_C0.items():
            r = R_factor(alpha, lam, w, xi_pc * PC, C0, ell)
            if best is None or r[0] > best[0][0]:
                best = (r, xi_pc, lab)
    return best

# a display row for each system at the W1 corners
WZ = {}
for nm, s in SYSTEMS.items():
    Pb, m, a, v2 = orbit(s); w = 2 * math.pi / Pb
    for (acv, c2v) in ((AC_MIN, C2_MIN), (AC_MAX, C2_MIN), (AC_MIN, C2_MAX), (AC_MAX, C2_MAX)):
        (R1, ks, kUV, aeff), xib, lab = env_R(acv, c2v, w, 1)
        WZ[f"{nm} alpha_c={acv:.2e} c2={c2v:.3e}"] = {"R1": R1, "xi_k*": xib * PC * ks, "xi_kUV": xib * PC * kUV,
                                                         "alpha_eff/alpha_c": aeff / acv, "filter_at_k*": math.exp(-(xib * PC * ks)**2),
                                                         "lambda_k*_pc": 2 * math.pi / ks / PC, "xi_pc": xib, "cell": lab,
                                                         "R1_universal": math.sqrt(1 + 2 / acv)}
for k_, v_ in WZ.items():
    if k_.startswith("J1738"):
        P(f"    {k_}: k_UV xi = {v_['xi_kUV']:.2f}, k* xi = {v_['xi_k*']:.2f} (wavelength {v_['lambda_k*_pc']:.3f} pc), "
          f"e^-(xi k*)^2 = {v_['filter_at_k*']:.1e}, alpha_eff/alpha_c = {v_['alpha_eff/alpha_c']:.2e}, R_1 = {v_['R1']:.3g} "
          f"(universal bound {v_['R1_universal']:.2e})  [{v_['cell']}, xi {v_['xi_pc']} pc]")
OUT["numbers"]["wave_zone_corners"] = WZ
mono_xi = [R_factor(AC_MAX, C2_MIN, 2 * math.pi / (SYSTEMS["J1738+0333"]["Pb_d"] * DAY), x_ * PC, C0_MAX, 1)[0] for x_ in (0.031, 0.045, 0.1, 1.0)]
P(f"    R_1 vs xi (0.031, 0.045, 0.1, 1 pc) at alpha_max, c2_min, J1738, C_0 max: {[f'{r_:.3g}' for r_ in mono_xi]} (decreasing: "
  f"{all(np.diff(mono_xi) < 0)})")
check("WZ the khronon's radiated wavelength at orbital frequencies is comparable to xi (k* xi ~ 3-5), so the heat filter does "
      "NOT screen the wave zone: the MOND clock inertia raises alpha_eff at k* above alpha_c; R_1 decreases with xi",
      f"J1738 corners alpha_eff/alpha_c {min(v_['alpha_eff/alpha_c'] for k_, v_ in WZ.items() if k_.startswith('J1738')):.2e}"
      f"..{max(v_['alpha_eff/alpha_c'] for k_, v_ in WZ.items() if k_.startswith('J1738')):.2e}; R_1 {min(v_['R1'] for v_ in WZ.values()):.3g}.."
      f"{max(v_['R1'] for v_ in WZ.values()):.3g}; R_1(xi) decreasing {all(np.diff(mono_xi) < 0)}",
      all(np.diff(mono_xi) < 0) and all(1.0 <= v_["alpha_eff/alpha_c"] for v_ in WZ.values()),
      "contrary to the expectation that the filter screens everything: it screens the near zone, not the khronon's pc-scale wave zone",
      load_bearing=False)

# POST HOC (written after the first run showed R_1 is not monotone in xi): R against its universal bound on extended grids
ph = {"max_R1": 0.0, "max_R1_over_universal": 0.0}
for acv in (AC_MIN, 1e-11, AC_MAX):
    for c2v in (C2_MIN, C2_MAX):
        for nm, s in SYSTEMS.items():
            w = 2 * math.pi / (s["Pb_d"] * DAY)
            for xi_pc in (0.031, 0.045, 0.1, 0.3, 1.0, 3.0, 10.0, 100.0):
                for C0 in (1e-4, 1e-3, 0.008, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0):
                    r1 = R_factor(acv, c2v, w, xi_pc * PC, C0, 1)[0]
                    ph["max_R1"] = max(ph["max_R1"], r1)
                    ph["max_R1_over_universal"] = max(ph["max_R1_over_universal"], r1 / math.sqrt(1 + 2 / acv))
OUT["numbers"]["post_hoc_R_extended"] = ph
P(f"    POST HOC: over xi 0.031-100 pc and C_0 1e-4-10 at the W1 corners: max R_1 = {ph['max_R1']:.3g}; "
  f"max R_1 / universal bound = {ph['max_R1_over_universal']:.3e}")
check("POST HOC R_1 never exceeds its universal bound sqrt(1 + 2/alpha_c) on extended xi and C_0 grids, so scoring with the "
      "universal factor covers every environment and every xi >= floor", f"max R_1/universal {ph['max_R1_over_universal']:.2e}; max R_1 {ph['max_R1']:.3g}",
      ph["max_R1_over_universal"] <= 1.0, "the frozen primary (max over the committed floors) is not the max over xi >= floor; the universal row is",
      load_bearing=False)

# ================================================================================================ the scorer
def sens(bracket, alpha, lam):
    if bracket == "B0":
        return 0.0
    c = coeffs(alpha, lam)
    s1 = abs(c["a1"] - 2 * c["a2"] / 3) * OMEGA_OVER_M_MAX
    return {"B1": s1, "B2": 3 * s1, "B3": OMEGA_OVER_M_MAX * lam}[bracket]

def score_point(alpha, lam, s_sys, bracket, Rmode, Rcache=None, ds_override=None, with_fs=True):
    """returns (delta_min, delta_max, delta_dip, delta_quad, s_crit, pass).  with_fs=False drops the
    [(1-s1)(1-s2)]^(2/3) strong-field-G factor (degenerate with GR-based mass inference; reading only)."""
    Pb, m, a, v2 = orbit(s_sys); w = 2 * math.pi / Pb
    c = coeffs(alpha, lam)
    if Rmode == "computed":
        R1, R2 = Rcache if Rcache is not None else Rpair(alpha, lam, s_sys)
    else:
        R1 = math.sqrt(1 + 2 / alpha); R2 = (1 + 2 / alpha)**1.5
    sNS = sens(bracket, alpha, lam)
    ds = sNS if ds_override is None else ds_override
    if s_sys["kind"] == "NS-WD":
        s1, s2 = (sNS, 0.0); S = sNS * s_sys["m2"] / m
    else:
        s1, s2 = (sNS, 0.0); S = sNS
    if ds_override is not None:
        s1, s2, S = ds_override, 0.0, 0.0
    fs = ((1 - s1) * (1 - s2))**(2 / 3) if with_fs else 1.0
    dq = fs * (1 + (c["A1m1"] + S * c["A2"] + S * S * c["A3"]) * R2) - 1
    vterm = ((18 / 5) * c["A3"] * V_CM**2 + ((6 / 5) * c["A3"] + 36 * c["B"]) * V_CM**2) * R2
    eratio = ge(s_sys["e"]) / fe(s_sys["e"])
    ddip = (5 / 32) * ds**2 * (c["C"] * R1 * eratio + vterm) / v2
    dmin, dmax = ddip - abs(dq), ddip + abs(dq)
    scrit = math.sqrt(s_sys["hi"] * 32 * v2 / (5 * c["C"] * R1 * eratio))
    ok = (s_sys["lo"] <= dmin) and (dmax <= s_sys["hi"])
    return dmin, dmax, ddip, dq, scrit, ok

def Rpair(alpha, lam, s_sys):
    Pb = s_sys["Pb_d"] * DAY; w = 2 * math.pi / Pb
    r1 = env_R(alpha, lam, w, 1)[0][0]
    r2c = env_R(alpha, lam, 2 * w, 2)
    r2 = max(r2c[0][0], (r2c[0][3] / alpha)**1.5)        # quadrupole-order terms: the generous bound (F9)
    return r1, r2

def in_window(alpha, c2):
    gcos_gn = (2 - alpha) / (2 + 3 * c2)
    return (AC_MIN * (1 - 1e-12) <= alpha <= AC_MAX * (1 + 1e-12)) and (C2_MIN * (1 - 1e-12) <= c2 <= C2_MAX * (1 + 1e-12)), abs(gcos_gn - 1)

BRACKETS = ("B0", "B1", "B2", "B3", "B3d")       # B3d = B3 without the strong-field-G factor (reading)
def score_window(ac_grid, c2_grid, label):
    res = {b: {r: {nm: np.zeros((len(ac_grid), len(c2_grid)), bool) for nm in SYSTEMS} for r in ("computed", "universal")} for b in BRACKETS}
    tension = {b: {r: np.zeros((len(ac_grid), len(c2_grid))) for r in ("computed", "universal")} for b in BRACKETS}
    margin_B2 = np.full((len(ac_grid), len(c2_grid)), np.inf)
    worst = {}
    maxdip = {}
    for i, acv in enumerate(ac_grid):
        for j, c2v in enumerate(c2_grid):
            for nm, s in SYSTEMS.items():
                Rc = Rpair(acv, c2v, s)
                for b in BRACKETS:
                    for rmode in ("computed", "universal"):
                        dmin, dmax, ddip, dq, scrit, ok = score_point(acv, c2v, s, "B3" if b == "B3d" else b, rmode,
                                                                      Rcache=Rc if rmode == "computed" else None, with_fs=(b != "B3d"))
                        res[b][rmode][nm][i, j] = ok
                        t = max(dmax / s["hi"], dmin / s["lo"] if s["lo"] < 0 else 0)
                        tension[b][rmode][i, j] = max(tension[b][rmode][i, j], t)
                        key = (b, rmode)
                        if key not in maxdip or ddip > maxdip[key][0]:
                            maxdip[key] = (ddip, acv, c2v, nm)
                        if key not in worst or t > worst[key][0]:
                            worst[key] = (t, acv, c2v, nm, ddip, dq)
                        if b == "B2" and rmode == "computed":
                            margin_B2[i, j] = min(margin_B2[i, j], scrit / max(sens("B2", acv, c2v), 1e-300))
    return res, tension, margin_B2, worst, maxdip

# ================================================================================================ W1 (or MUTATE)
NA = 25
AC_GRID = np.logspace(math.log10(AC_MIN), math.log10(AC_MAX), NA)
C2_GRID_W1 = np.array([1.0]) if MUTATE else np.logspace(math.log10(C2_MIN), math.log10(C2_MAX), NA)
banner(("MUTATE  lambda_K = 2 (c_2 = 1)" if MUTATE else "W1  THE PRIMARY WINDOW (L340 P1)") +
       f": {len(AC_GRID)} x {len(C2_GRID_W1)} points x 3 systems x 4 brackets x (computed, universal) wave-zone factor")
gate_rows = [in_window(a_, c_) for a_ in AC_GRID for c_ in C2_GRID_W1]
gate_ok = all(g[0] for g in gate_rows) and max(g[1] for g in gate_rows) <= 0.1
P(f"    window gate: all points inside L340 P1: {all(g[0] for g in gate_rows)}; max plain-branch |G_cos/G_N - 1| = {max(g[1] for g in gate_rows):.4f} (BBN 0.1)")
check("WINDOW the scored points lie in the frozen chassis window and satisfy its plain-branch BBN condition "
      "|G_cos/G_N - 1| = |(2 - alpha_c)/(2 + 3 c_2) - 1| <= 0.1 (L340 P1, L350 G1)",
      f"inside: {all(g[0] for g in gate_rows)}; max |G_cos/G_N - 1| = {max(g[1] for g in gate_rows):.4f}", gate_ok,
      "MUTATE (lambda_K = 2) must fail this row" if not MUTATE else "lambda_K = 2 is outside the window and fails BBN in the plain branch")
res1, ten1, marg1, worst1, maxdip1 = score_window(AC_GRID, C2_GRID_W1, "W1")
summary1 = {}
for b in BRACKETS:
    for rmode in ("computed", "universal"):
        allpass = np.logical_and.reduce([res1[b][rmode][nm] for nm in SYSTEMS])
        t, acv, c2v, nm, ddip, dq = worst1[(b, rmode)]
        summary1[f"{b}/{rmode}"] = {"n_pass": int(allpass.sum()), "n": int(allpass.size), "max_tension": t,
                                    "per_system_n_pass": {k_: int(res1[b][rmode][k_].sum()) for k_ in SYSTEMS},
                                    "worst": {"alpha_c": acv, "c2": c2v, "system": nm, "delta_dip": ddip, "delta_quad": dq}}
        P(f"    {b} {rmode:9s}: {int(allpass.sum()):4d}/{allpass.size} points pass all three systems; max delta/limit = {t:.3e} "
          f"(alpha_c {acv:.2e}, c_2 {c2v:.3e}, {nm}; delta_dip {ddip:.2e}, delta_quad {dq:+.2e});  per system "
          + ", ".join(f"{k_} {int(res1[b][rmode][k_].sum())}" for k_ in SYSTEMS))
P(f"    B2 margin in sensitivity, min over the window and systems: s_crit / s_B2 >= {marg1.min():.3e}")
for b in ("B1", "B2"):
    for rmode in ("computed", "universal"):
        d_, a_, c_, n_ = maxdip1[(b, rmode)]
        summary1[f"{b}/{rmode}"]["max_delta_dip"] = {"value": d_, "alpha_c": a_, "c2": c_, "system": n_}
        P(f"    largest dipole delta, {b} {rmode:9s}: {d_:.3e} (alpha_c {a_:.2e}, c_2 {c_:.3e}, {n_})")
for b in ("B3", "B3d"):
    for nm in SYSTEMS:
        bad = ~res1[b]["computed"][nm]
        cmin = float(C2_GRID_W1[np.where(bad.any(axis=0))[0].min()]) if bad.any() else None
        summary1[f"{b}/computed"].setdefault("smallest_failing_c2", {})[nm] = cmin
        P(f"    {b} computed, {nm}: smallest failing c_2 on the grid = {cmin if cmin is None else f'{cmin:.4e}'}")
OUT["numbers"]["W1" if not MUTATE else "MUTATE"] = {"summary": summary1, "min_scrit_over_sB2": float(marg1.min()),
                                                     "alpha_grid": AC_GRID.tolist(), "c2_grid": C2_GRID_W1.tolist(),
                                                     "log10_tension_B2_computed": np.round(np.log10(np.maximum(ten1["B2"]["computed"], 1e-300)), 2).tolist(),
                                                     "log10_tension_B3_computed": np.round(np.log10(np.maximum(ten1["B3"]["computed"], 1e-300)), 2).tolist()}
# per-system s_crit at the corners (reading)
scr = {}
for nm, s in SYSTEMS.items():
    for (acv, c2v) in ((AC_MIN, C2_GRID_W1.min()), (AC_MAX, C2_GRID_W1.min()), (AC_MAX, C2_GRID_W1.max())):
        out_ = score_point(acv, c2v, s, "B2", "computed", Rcache=Rpair(acv, c2v, s))
        scr[f"{nm} alpha_c={acv:.2e} c2={c2v:.3e}"] = {"s_crit": out_[4], "s_B1": sens("B1", acv, c2v), "s_B2": sens("B2", acv, c2v),
                                                        "s_B3": sens("B3", acv, c2v), "delta_dip_B2": out_[2]}
for k_, v_ in scr.items():
    P(f"    s_crit {k_}: {v_['s_crit']:.3e}   (s_B1 {v_['s_B1']:.2e}, s_B2 {v_['s_B2']:.2e}, s_B3 {v_['s_B3']:.2e}); B2 dipole delta {v_['delta_dip_B2']:.2e}")
OUT["numbers"]["s_crit_corners"] = scr

# ================================================================================================ W3 the record window
W3 = {}
if not MUTATE:
    banner("W3  THE RECORD WINDOW 1 < lambda_K <= 1.10 (c_2 in [1e-12, 0.10]): surviving sub-windows per bracket")
    C2_W3 = np.logspace(-12, -1, 49)
    res3, ten3, marg3, worst3, maxdip3 = score_window(AC_GRID, C2_W3, "W3")
    def edge(mask):           # smallest c_2 such that every c_2' >= c_2 on the grid passes for every alpha_c
        colok = mask.all(axis=0)
        if colok.all():
            return float(C2_W3[0])
        bad = np.where(~colok)[0]
        return float(C2_W3[bad.max() + 1]) if bad.max() + 1 < len(C2_W3) else float("nan")
    for b in BRACKETS:
        for rmode in ("computed", "universal"):
            allpass = np.logical_and.reduce([res3[b][rmode][nm] for nm in SYSTEMS])
            W3[f"{b}/{rmode}"] = {"n_pass": int(allpass.sum()), "n": int(allpass.size), "c2_edge_all_alpha": edge(allpass),
                                  "max_tension": worst3[(b, rmode)][0]}
            P(f"    {b} {rmode:9s}: {int(allpass.sum()):4d}/{allpass.size} pass; radiation passes at every alpha_c for c_2 >= {edge(allpass):.3e}")
    a2ok = np.array([[abs(coeffs(a_, c_)["a2"]) <= 1.6e-9 for c_ in C2_W3] for a_ in AC_GRID])
    bbn_edge = (2 - AC_MAX) / 0.9 / 3 - 2 / 3          # (2 - alpha)/(2 + 3 c2) >= 0.9
    W3["PPN_alpha2_edge"] = edge(a2ok); W3["BBN_plain_branch_c2_max"] = bbn_edge; W3["L350_caps"] = CAPS
    P(f"    PPN |alpha-hat2| <= 1.6e-9 at every alpha_c for c_2 >= {edge(a2ok):.3e};  plain-branch BBN ceiling c_2 <= {bbn_edge:.4f}; "
      f"L350 Planck ceilings {CAPS[0]:.2e}..{CAPS[-1]:.2e} (plain branch)")
    OUT["numbers"]["W3"] = W3

# ================================================================================================ C6 alpha_c -> 0
banner("C6  alpha_c -> 0 at fixed lambda: the flux vanishes and the khronon becomes strongly coupled (XC1, recipe P7)")
c6 = {}
ok6 = True
for lam in (C2_MIN, C2_MAX):
    alphas = np.logspace(math.log10(AC_MIN), -40, 28)
    for b in ("B1", "B2"):
        for rmode in ("computed", "universal"):
            dd = [score_point(a_, lam, SYSTEMS["J1738+0333"], b, rmode)[2] for a_ in alphas]
            dec = all(np.diff(np.log10(dd)) < 0); drop = dd[-1] / dd[0]
            c6[f"lambda={lam:.3e} {b} {rmode}"] = {"delta_dip_first": dd[0], "delta_dip_last": dd[-1], "monotone": dec}
            ok6 &= dec and drop < 1e-30
            P(f"    lambda {lam:.3e} {b} {rmode:9s}: delta_dip {dd[0]:.2e} -> {dd[-1]:.2e} as alpha_c {alphas[0]:.1e} -> {alphas[-1]:.0e}; monotone {dec}")
    ksc = [math.sqrt(a_) * MPL_RED * (math.sqrt(f_c0sq(a_, lam))**-0.5) for a_ in alphas]
    a_strong = next((a_ for a_, k_ in zip(alphas, ksc) if k_ < 1e3 * LHC_GEV), None)
    c6[f"lambda={lam:.3e} k_sc"] = {"k_sc_first_GeV": ksc[0], "k_sc_last_GeV": ksc[-1], "alpha_where_below_1e3_LHC": a_strong}
    ok6 &= all(np.diff(ksc) < 0) and a_strong is not None
    P(f"    lambda {lam:.3e}: XC1 strong-coupling momentum {ksc[0]:.2e} GeV -> {ksc[-1]:.2e} GeV; below 1e3 x LHC once alpha_c < {a_strong:.1e}")
    d3 = [score_point(a_, lam, SYSTEMS["J1738+0333"], "B3", "universal")[2] for a_ in alphas]
    c6[f"lambda={lam:.3e} B3 universal (reading)"] = {"first": d3[0], "last": d3[-1]}
    P(f"    (reading) B3 with the universal factor: delta_dip {d3[0]:.2e} -> {d3[-1]:.2e} (does not vanish: only strong coupling stops it)")
OUT["numbers"]["C6"] = c6
check("C6 as alpha_c -> 0 the B1/B2 khronon flux vanishes monotonically (computed and universal wave-zone factor) and "
      "XC1's strong-coupling momentum falls below 1e3 x the LHC: alpha_c > 0 is load-bearing a fourth time",
      "; ".join(f"{k_}: {v_}" for k_, v_ in c6.items() if "k_sc" in k_), ok6,
      "flux ~ alpha_c^(5/2) (UV) and <= alpha_c^2 (universal) under the published brackets; the theory is strongly coupled first")

# ================================================================================================ C8 injection
banner("C8  INJECTION: |s1 - s2| = 1.01 / 0.99 s_crit at alpha_c max, c_2 min of the scored grid")
inj = {}
okC8 = True
for nm, s in SYSTEMS.items():
    acv, c2v = AC_MAX, float(C2_GRID_W1.min())
    Rc = Rpair(acv, c2v, s)
    scrit = score_point(acv, c2v, s, "B0", "computed", Rcache=Rc)[4]
    # s_crit is defined for the dipole alone (FROZEN_CRITERIA sec. 5), so the injection drops the strong-field-G factor
    # [(1-s1)(1-s2)]^(2/3); the first run included it and 0.99 s_crit failed on that factor (disclosed in the README)
    hi_ = score_point(acv, c2v, s, "B0", "computed", Rcache=Rc, ds_override=1.01 * scrit, with_fs=False)
    lo_ = score_point(acv, c2v, s, "B0", "computed", Rcache=Rc, ds_override=0.99 * scrit, with_fs=False)
    inj[nm] = {"s_crit": scrit, "pass_at_1.01": hi_[5], "pass_at_0.99": lo_[5], "delta_1.01": hi_[1], "delta_0.99": lo_[1]}
    okC8 &= (not hi_[5]) and lo_[5]
    P(f"    {nm:14s}: s_crit = {scrit:.4e};  1.01 s_crit -> delta {hi_[1]:.4e} pass={hi_[5]};  0.99 s_crit -> delta {lo_[1]:.4e} pass={lo_[5]}")
OUT["numbers"]["C8"] = inj
check("C8 the scorer flags an injected dipole just above s_crit and passes one just below, for every system", str({k_: (v_['pass_at_1.01'], v_['pass_at_0.99']) for k_, v_ in inj.items()}), okC8)

# ================================================================================================ PPN reading
banner("PPN  alpha1, alpha2 over the scored grid against the record's bounds (data_assembly/DOOR11_LITERATURE_2026-09-29.md)")
ppn = {}
for (acv, c2v) in ((AC_MIN, C2_GRID_W1.min()), (AC_MIN, C2_GRID_W1.max()), (AC_MAX, C2_GRID_W1.min()), (AC_MAX, C2_GRID_W1.max())):
    c = coeffs(acv, c2v); ppn[f"alpha_c={acv:.2e} c2={c2v:.3e}"] = {"alpha1": c["a1"], "alpha2": c["a2"]}
    P(f"    alpha_c {acv:.3e}, c_2 {c2v:.4e}: alpha1 = {c['a1']:+.4e}, alpha2 = {c['a2']:+.6e}")
a1max = max(abs(v_["alpha1"]) for v_ in ppn.values()); a2max = max(abs(v_["alpha2"]) for v_ in ppn.values())
P(f"    bounds: |alpha-hat1| < 2.1e-5 (Liu+2020), -3.5e-5 < alpha-hat1 < 3.3e-5 (Shao & Wex 2012), alpha1 (LLR) = (-0.7 +/- 1.8)e-4; "
  f"|alpha-hat2| < 1.6e-9 (Shao+2013), |alpha2| < 2.4e-7 (secondary)")
OUT["numbers"]["PPN"] = {"corners": ppn, "max_abs_alpha1": a1max, "max_abs_alpha2": a2max}
check("PPN (reading) over the scored grid |alpha1| <= 1.3e-8 << 2.1e-5 and |alpha2| <= 1.6e-9 (the window's top edge is set by "
      "alpha-hat2 itself, so the top corner sits on the bound by construction; strong-field alpha-hat = alpha (1 + O(s)))",
      f"max |alpha1| {a1max:.3e}, max |alpha2| {a2max:.6e}", a1max < 2.1e-5 and a2max <= 1.6e-9 * (1 + 1e-6), load_bearing=False)

# ================================================================================================ VERDICT
banner("VERDICT (frozen rule, FROZEN_CRITERIA sec. 7)")
lb_controls = [n for n, ok, lb in CH if lb and n.split()[0] in ("C1", "C2", "C3", "C4", "C5", "C6", "C8", "C9") and not ok]
def npass(b, r):
    return summary1[f"{b}/{r}"]["n_pass"]
NTOT = summary1["B0/computed"]["n"]
kill_any = any(npass(b, "computed") < NTOT for b in ("B1", "B2"))
kill_all = all(npass(b, "computed") == 0 for b in ("B1", "B2"))
b3_fail = npass("B3", "computed") < NTOT
b2u_fail = npass("B2", "universal") < NTOT or npass("B1", "universal") < NTOT
if lb_controls:
    verdict = "OPEN"
elif MUTATE:
    verdict = "MUTATE (window gate test; no chassis verdict)"
elif kill_all:
    verdict = "KILL"
elif kill_any:
    verdict = "CONDITIONAL (sub-window survives; KILL outside it)"
elif b3_fail or b2u_fail:
    verdict = "CONDITIONAL"
else:
    verdict = "PASS (at the stated scope)"
OUT["verdict"] = verdict
OUT["verdict_inputs"] = {"failed_controls": lb_controls, "B1B2_computed_any_fail": kill_any, "B3_computed_any_fail": b3_fail,
                         "B1B2_universal_any_fail": b2u_fail}
P(f"  failed load-bearing controls: {lb_controls or 'none'}")
P(f"  W1 under B0/B1/B2 with the computed wave-zone factor: {npass('B0','computed')}/{npass('B1','computed')}/{npass('B2','computed')} of {NTOT} pass")
P(f"  W1 under B3 (counterfactual) computed: {npass('B3','computed')}/{NTOT} (dipole-only B3d: {npass('B3d','computed')}/{NTOT});  "
  f"B1/B2 universal: {npass('B1','universal')}/{npass('B2','universal')}/{NTOT}")
P(f"  VERDICT: {verdict}")
P(f"  Time {time.time() - T0:.0f} s.")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_pass"], OUT["n_fail_load_bearing"] = len(CH), sum(1 for _, ok, _ in CH if ok), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
