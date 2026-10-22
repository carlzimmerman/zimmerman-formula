#!/usr/bin/env python3
"""D7_turnoff_yt -- origin of the strong-field turn-off P5 and its scale y_t.

Checks K1-K11 exactly as frozen in FROZEN_CRITERIA.md (commit f2e0423a60).
Deterministic, no network, single thread.  `--mutate` swaps the canonical kernel
for the RAR kernel (tail coefficient 0) and writes *_MUTATE outputs.
"""
import json
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."
OUT = f"{HERE}/d7_turnoff_yt{TAG}.out"
JSON = f"{HERE}/d7_turnoff_yt_results{TAG}.json"

# ---------------------------------------------------------------- constants (labelled)
c = 2.99792458e8
G = 6.67430e-11
GM_SUN = 1.32712440018e20
MSUN = 1.98847e30
AU = 1.495978707e11
PC = 3.0856775814913673e16
A0_CAN = 9.36e-11            # canonical footing (BRIEF rule 3)
A0_ALT = 1.13e-10            # alt footing
LAMBDA = 1.0890e-52          # m^-2, A28 / A4 input
B_E = 3.66e-14               # A4 Earth 2-sigma constant-anomaly bound (external)
Z = 2 * math.sqrt(8 * math.pi / 3)
KAPPA_TH = Z / (4 * math.pi)  # thermal POSTULATE (A75)
LSTAR_PC = 24.0               # A20/A61 window floor; window 24-90 pc
U_GAL = 0.566                 # A60: galactic u at the Sun in a0 units (external)
# A4 section D6 published per-planet bounds (m/s^2); Uranus/Neptune have none (stand-ins excluded)
PLANETS = {"Mercury": (0.387, 4.6e-14), "Venus": (0.723, 8.0e-14), "Earth": (1.000, 8.7e-15),
           "Mars": (1.524, 1.4e-15), "Jupiter": (5.204, 5.6e-13), "Saturn": (9.583, 7.0e-15)}
# A26 (external input, quoted only)
A26 = {"N_below": 45, "step_dex": 0.453, "step_err": 0.099, "sigma_vs_medium_first": 21.0}
# record values to reproduce (external)
REC = {"yt_quoted": 66.2999, "yt_32pi": 66.3803, "yt_alt": 46.0148,
       "yt_th_a": 77.85, "yt_th_b": 77.944, "kap_lo": 0.3415, "kap_hi": 0.5265}

lines, checks, numbers = [], [], {}


def log(s):
    print(s)
    lines.append(s)


def check(kid, ok, value, thr, note=""):
    checks.append({"id": kid, "pass": bool(ok), "value": value, "threshold": thr, "note": note})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


# ---------------------------------------------------------------- kernels: h(y) = y (nu - 1)
def h_can(y):
    y = np.asarray(y, dtype=float)
    return 2 * y / (np.sqrt(y * y + 4 * y) + y)   # = (sqrt(y^2+4y)-y)/2, cancellation-free


def h_rar(y):
    y = np.asarray(y, dtype=float)
    s = np.minimum(np.sqrt(y), 700.0)
    return y / np.expm1(s)


h = h_rar if MUTATE else h_can


def hprime(y, d=1e-6):
    return (h(y * (1 + d)) - h(y * (1 - d))) / (2 * y * d)


def F(Y):
    """closure integral F(Y) = int_0^inf h(y)/(1+(y/Y)^2) dy = Y int_0^{pi/2} h(Y tan th) dth."""
    val, _ = quad(lambda th: Y * float(h(Y * math.tan(th))), 0, math.pi / 2, limit=400,
                  epsabs=1e-13, epsrel=1e-12)
    return val


def root_yt(N):
    try:
        return brentq(lambda Y: F(Y) - N, 1e-3, 1e5, xtol=1e-12)
    except ValueError:
        return float("nan")


N_CAN = LAMBDA * c ** 4 / A0_CAN ** 2
N_ALT = LAMBDA * c ** 4 / A0_ALT ** 2
N_32PI = 32 * math.pi
N_TH = 8 * math.pi / KAPPA_TH ** 2
numbers.update(N_Lambda_can=N_CAN, N_Lambda_alt=N_ALT, N_32pi=N_32PI, N_thermal=N_TH,
               kappa_thermal=KAPPA_TH, Z=Z)

# ================================================================ K1 tail of the canonical law
yy = sp.symbols("y", positive=True)
nu_sym = (1 + sp.sqrt(1 + 4 / yy)) / 2
g_s, gN_s, a_s = sp.symbols("g g_N a0", positive=True)
# g = a0 y nu solves g_N = g^2/(g+a0)
res = sp.simplify((a_s * yy * nu_sym) ** 2 / (a_s * yy * nu_sym + a_s) - a_s * yy)
diff_form = sp.simplify(nu_sym - 1 - (sp.sqrt(1 + 4 / yy) - 1) / 2)
tail_can = sp.limit(yy * (nu_sym - 1), yy, sp.oo)
tail_quad = sp.limit(yy * (sp.sqrt(1 + 1 / yy) - 1), yy, sp.oo)
tail_used = float(h(1e12))
numbers.update(tail_canonical_sym=str(tail_can), tail_quadrature_sym=str(tail_quad),
               tail_kernel_in_use=tail_used, law_residual=str(res))
check("K1", res == 0 and diff_form == 0 and tail_can == 1 and tail_quad == sp.Rational(1, 2)
      and abs(tail_used - 1) < 1e-6,
      f"law_res={res} nu-1_form_res={diff_form} c_can={tail_can} c_quad={tail_quad} c_used={tail_used:.6g}",
      "residuals 0; c_can=1; c_quad=1/2; kernel in use has c=1")

# ================================================================ K2 bare anomaly at 1.5 AU
r15 = 1.5 * AU
gN15 = GM_SUN / r15 ** 2
out2 = {}
for lab, a0 in (("can", A0_CAN), ("alt", A0_ALT)):
    y = gN15 / a0
    anom = a0 * float(h(y))
    out2[lab] = {"y": y, "anomaly": anom, "ratio_to_BE": anom / B_E,
                 "quadrature_ratio": a0 * y / (math.sqrt(y * y + y) + y) / B_E}
numbers["K2_1p5AU"] = out2
check("K2", out2["can"]["ratio_to_BE"] > 1 and out2["alt"]["ratio_to_BE"] > 1,
      f"can={out2['can']['ratio_to_BE']:.2f}xB_E alt={out2['alt']['ratio_to_BE']:.2f}xB_E "
      f"(quadrature {out2['can']['quadrature_ratio']:.1f}/{out2['alt']['quadrature_ratio']:.1f})",
      ">1 on both footings => turn-off needed")


# ================================================================ K3 EFE on the phantom source
def f_nu1(y):  # nu - 1 as function of y
    return float(h(y)) / y


def fprime(y, d=1e-7):
    return (f_nu1(y * (1 + d)) - f_nu1(y * (1 - d))) / (2 * y * d)


def phantom_src(r, cth, a0, ge_vec):
    """div[(nu-1) g] off-source = f'(|g|)|g| ghat.J.ghat, J = GM(3 rr - I)/r^3 (uniform g_e adds no J)."""
    sth = math.sqrt(max(0.0, 1 - cth * cth))
    rhat = np.array([sth, 0.0, cth])
    gs = -GM_SUN / r ** 2 * rhat
    g = gs + ge_vec
    gm = np.linalg.norm(g)
    gh = g / gm
    J = GM_SUN / r ** 3 * (3 * np.outer(rhat, rhat) - np.eye(3))
    y = gm / a0
    return fprime(y) / a0 * gm * float(gh @ J @ gh)


out3 = {}
xs, ws = np.polynomial.legendre.leggauss(64)
for lab, a0 in (("can", A0_CAN), ("alt", A0_ALT)):
    gNe = U_GAL ** 2 / (1 - U_GAL) * a0  # Newtonian galactic field from A60's u_gal (law inverse)
    ge = np.array([0.0, 0.0, gNe])  # along the polar axis; the angular grid covers all relative angles
    iso = phantom_src(r15, 1.0, a0, np.zeros(3))
    rel = [abs(phantom_src(r15, x, a0, ge) / phantom_src(r15, x, a0, np.zeros(3)) - 1) for x in xs]
    # angle-averaged (monopole => Gauss-law radial anomaly) ratio
    avg_emb = sum(w * phantom_src(r15, x, a0, ge) for x, w in zip(xs, ws)) / 2
    avg_iso = sum(w * phantom_src(r15, x, a0, np.zeros(3)) for x, w in zip(xs, ws)) / 2
    rM = math.sqrt(GM_SUN / a0)
    out3[lab] = {"gNe_over_a0": gNe / a0, "max_rel_change": max(rel),
                 "monopole_ratio": avg_emb / avg_iso, "tidal_est_over_a0": r15 / rM,
                 "r_M_AU": rM / AU, "iso_src": iso}
numbers["K3_EFE"] = out3
ok3 = all(out3[k]["max_rel_change"] < 0.5 and out3[k]["tidal_est_over_a0"] < 1e-2 for k in out3)
check("K3", ok3,
      f"max|drho/rho| can={out3['can']['max_rel_change']:.2e} alt={out3['alt']['max_rel_change']:.2e}; "
      f"monopole ratio {out3['can']['monopole_ratio']:.9f}; tidal a0*r/r_M={out3['can']['tidal_est_over_a0']:.2e}a0",
      "<0.5 and tidal<1e-2 a0 => EFE cannot buy x2557")

# ================================================================ K5 closure roots (needed by K4)
yt_q = root_yt(N_CAN)
yt_32 = root_yt(N_32PI)
yt_alt = root_yt(N_ALT)
yt_th = root_yt(N_TH)
numbers.update(yt_quoted=yt_q, yt_32pi=yt_32, yt_alt=yt_alt, yt_thermal=yt_th,
               F_supremum_check=F(1e6))
rel = lambda a, b: abs(a / b - 1)
ok5 = (not math.isnan(yt_q)) and rel(yt_q, REC["yt_quoted"]) < 1e-3 and rel(yt_32, REC["yt_32pi"]) < 1e-3 \
    and rel(yt_alt, REC["yt_alt"]) < 1e-3
numbers["thermal_vs_record"] = {"vs_77.85": (yt_th / REC["yt_th_a"] - 1) if not math.isnan(yt_th) else None,
                                "vs_77.944": (yt_th / REC["yt_th_b"] - 1) if not math.isnan(yt_th) else None,
                                "N_thermal_used": N_TH,
                                "yt_at_N_118.6": root_yt(118.6)}
# K4 printed after K5 values exist, but numbered as frozen
# ================================================================ K4 patched anomaly at 1.5 AU
out4 = {}
for lab, a0, yt in (("can_kappa_half", A0_CAN, yt_q), ("alt", A0_ALT, yt_alt), ("thermal", A0_CAN, yt_th)):
    y = gN15 / a0
    an = a0 * float(h(y)) / (1 + (y / yt) ** 2) if not math.isnan(yt) else float("nan")
    out4[lab] = {"y_t": yt, "anomaly": an, "ratio_to_BE": an / B_E}
numbers["K4_patched_1p5AU"] = out4
check("K4", all(v["ratio_to_BE"] < 1 for v in out4.values()),
      " ".join(f"{k}={v['ratio_to_BE']:.2e}" for k, v in out4.items()), "<1 (x B_E) all three")
check("K5", ok5,
      f"y_t quoted={yt_q:.4f} 32pi={yt_32:.4f} alt={yt_alt:.4f} thermal(8pi/kth^2={N_TH:.3f})={yt_th:.3f}",
      "record 66.2999/66.3803/46.0148 to 1e-3; thermal reported vs 77.85 and 77.944")

# ================================================================ K6 bijection kappa <-> y_t
Ygrid = np.geomspace(1, 1e4, 400)
Fv = np.array([F(Y) for Y in Ygrid])
mono = bool(np.all(np.diff(Fv) > 0))
kap_of = lambda Y: math.sqrt(8 * math.pi / F(Y))
k_lo, k_hi = kap_of(140.0), kap_of(60.0)
numbers.update(kappa_at_yt140=k_lo, kappa_at_yt60=k_hi, F_monotone=mono)
check("K6", mono and rel(k_lo, REC["kap_lo"]) < 1e-3 and rel(k_hi, REC["kap_hi"]) < 1e-3,
      f"monotone={mono} band[60,140] -> kappa[{k_lo:.4f},{k_hi:.4f}]", "record [0.3415,0.5265] to 1e-3")

# ================================================================ K7 direct observability of y_t
ytop = 140.0
pl = {}
for name, (rau, bnd) in PLANETS.items():
    y = GM_SUN / (rau * AU) ** 2 / A0_CAN
    an = A0_CAN * float(h(y)) / (1 + (y / ytop) ** 2)
    pl[name] = {"signal": an, "bound": bnd, "ratio": an / bnd}
best = max(pl, key=lambda k: pl[k]["ratio"])
# wide binaries: max over y in [3, 3000] of |g(60)-g(140)|/g, canonical
ys = np.geomspace(3, 3000, 4000)
gfix = lambda y, yt: y + h(y) / (1 + (y / yt) ** 2)
fr = np.abs(gfix(ys, 60.0) - gfix(ys, 140.0)) / gfix(ys, 140.0)
iwb = int(np.argmax(fr))
s_wb = math.sqrt(2 * GM_SUN / (ys[iwb] * A0_CAN)) / AU
numbers["K7"] = {"planets_yt140": pl, "best_planet": best, "wb_max_frac_dg": float(fr[iwb]),
                 "wb_at_y": float(ys[iwb]), "wb_sep_AU_2Msun": s_wb,
                 "signal_scaling": "Delta g ~ a0 (y_t/y)^2  (r^4 growth)"}
ok7 = pl[best]["ratio"] < 1 and fr[iwb] < 0.01
check("K7", ok7,
      f"best planet {best} signal/bound={pl[best]['ratio']:.2e} (y_t=140); WB max|dg/g|(60 vs 140)="
      f"{fr[iwb]*100:.3f}% at y={ys[iwb]:.1f} (s={s_wb:.0f} AU)", "<1 and <1% => y_t not measurable now")

# ================================================================ K8 stiffness = mass threshold
# units a0 = 1, L* = 1, GM = m (m = M/M_crit); balance g_N = u^2/(1-u) + u/r^2 (constant-u hedgehog term)
def u_loc(m, r):
    gN = m / r ** 2
    fn = lambda u: u * u / (1 - u) + u / r ** 2 - gN
    return brentq(fn, 0.0, 1 - 1e-15, xtol=1e-300, rtol=1e-14)


out8 = {}
for m in (1e-3, 1e3):
    yv = np.geomspace(66.3 / 10, 66.3 * 10, 81)
    rv = np.sqrt(m / yv)
    uv = np.array([u_loc(m, r) for r in rv])
    # neglected derivative terms: (u'' + 2u'/r)/2 vs kept max(u^2/(1-u), u/r^2)
    lr = np.log(rv)
    du = np.gradient(uv, rv)
    d2u = np.gradient(du, rv)
    negl = np.abs(0.5 * (d2u + 2 * du / rv))
    kept = np.maximum(uv ** 2 / (1 - uv), uv / rv ** 2)
    frac_off = float(np.mean(uv < 0.5))
    # gradient/saturation ratio at y = 1e4 (saturated regime only meaningful for m >> 1)
    rr = math.sqrt(m / 1e4)
    uu = u_loc(m, rr)
    ratio = (uu / rr ** 2) / (uu * uu / (1 - uu))
    out8[str(m)] = {"frac_y_in_[yt/10,10yt]_with_anomaly_below_half": frac_off,
                    "u_at_y66": float(np.interp(66.3, yv, uv)),
                    "max_neglected_over_kept": float(np.max(negl[2:-2] / kept[2:-2])),
                    "grad_over_sat_at_y1e4": ratio, "Mcrit_over_M": 1 / m}
numbers["K8_stiffness"] = out8
a, b = out8["0.001"], out8["1000.0"]
ok8 = (a["frac_y_in_[yt/10,10yt]_with_anomaly_below_half"] == 1.0 and
       b["frac_y_in_[yt/10,10yt]_with_anomaly_below_half"] == 0.0 and
       rel(b["grad_over_sat_at_y1e4"], 1e-3) < 0.05 and
       a["max_neglected_over_kept"] < 0.05 and b["max_neglected_over_kept"] < 0.05)
check("K8", ok8,
      f"M=1e-3Mc: u(y=66)={a['u_at_y66']:.2e}a0, off on {a['frac_y_in_[yt/10,10yt]_with_anomaly_below_half']:.0%}; "
      f"M=1e3Mc: u(y=66)={b['u_at_y66']:.4f}a0, off on {b['frac_y_in_[yt/10,10yt]_with_anomaly_below_half']:.0%}; "
      f"grad/sat(y=1e4)={b['grad_over_sat_at_y1e4']:.4e} vs Mc/M=1e-3; negl<= "
      f"{max(a['max_neglected_over_kept'], b['max_neglected_over_kept']):.1e}",
      "mass threshold, not y threshold")

# ================================================================ K9 Sun vs M_crit
out9 = {}
for lab, a0 in (("can", A0_CAN), ("alt", A0_ALT)):
    for L in (24.0, 90.0):
        Mc = a0 * (L * PC) ** 2 / G / MSUN
        aP = GM_SUN / (L * PC) ** 2
        out9[f"{lab}_L{int(L)}"] = {"M_crit_Msun": Mc, "Msun_over_Mcrit": 1 / Mc, "aP_over_BE": aP / B_E}
numbers["K9"] = out9
numbers["A26_external"] = A26
check("K9", all(v["Msun_over_Mcrit"] < 1 for v in out9.values()),
      f"Msun/Mcrit in [{min(v['Msun_over_Mcrit'] for v in out9.values()):.2e},"
      f"{max(v['Msun_over_Mcrit'] for v in out9.values()):.2e}]; a_P/B_E<= "
      f"{max(v['aP_over_BE'] for v in out9.values()):.2e}; A26 rejects that side at {A26['sigma_vs_medium_first']} sigma",
      "Sun below M_crit for all (footing, L*)")

# ================================================================ K10 gate representability
out10 = {}
okk = True
for yt in (60.0, yt_q, yt_th, 140.0, yt_alt):
    if math.isnan(yt):
        okk = False
        continue
    A = lambda y: float(h(y)) / (1 + (y / yt) ** 2)
    pk = minimize_scalar(lambda ly: -A(math.exp(ly)), bounds=(math.log(1e-2), math.log(1e5)),
                         method="bounded", options={"xatol": 1e-12})
    ypk = math.exp(pk.x)
    Apk = A(ypk)
    tgt = 0.5 * Apk
    y1 = brentq(lambda y: A(y) - tgt, 1e-8, ypk, xtol=1e-14)
    y2 = brentq(lambda y: A(y) - tgt, ypk, 1e9, xtol=1e-12)
    g1, g2 = y1 + A(y1), y2 + A(y2)
    resid = abs(A(y1) - A(y2))
    mono_g = bool(np.all(np.diff([yy_ + A(yy_) for yy_ in np.geomspace(1e-3, 1e6, 3000)]) > 0))
    out10[f"{yt:.3f}"] = {"y_peak": ypk, "u_max_over_a0": Apk, "pair_g_over_a0": [g1, g2],
                          "pair_residual": resid, "g_of_y_monotone": mono_g}
    okk = okk and (y2 > y1 * 10) and resid < 1e-10 and mono_g
numbers["K10_gate"] = out10
k10v = out10.get(f"{yt_q:.3f}", {})
check("K10", okk and len(out10) == 5,
      f"y_t=66.30: peak y={k10v.get('y_peak', float('nan')):.2f}, u_max={k10v.get('u_max_over_a0', float('nan')):.4f}a0, "
      f"same u at g={k10v.get('pair_g_over_a0', [0, 0])[0]:.4f}a0 and {k10v.get('pair_g_over_a0', [0, 0])[1]:.1f}a0 "
      f"(res {k10v.get('pair_residual', 1):.1e}); non-monotone at all 5 y_t",
      "u(g) non-monotone => W'(u) double-valued => P5 not a gate potential")

# ================================================================ K11 frozen scale candidates
sig_c = math.sqrt(A0_CAN * LSTAR_PC * PC)        # sigma_c from L* = sigma_c^2/a0 (canonical anchor)
Rstar = (c / sig_c) ** 2                          # c^2/(a0 L*) = (c/sigma_c)^2, footing-independent
pts = {"can_kappa_half": (N_CAN, yt_q), "alt": (N_ALT, yt_alt), "thermal": (N_TH, yt_th)}
exps = [-2, -1, -0.5, 0, 0.5, 1, 2]
hits = []
best = None
for mexp in exps:
    for nexp in exps:
        if mexp == 0 and nexp == 0:
            continue
        devs = {}
        for k, (N, yt) in pts.items():
            X = math.sqrt(N / 3)  # cH_Lambda/a0 at that point
            yc = X ** mexp * Rstar ** nexp
            devs[k] = yc / yt - 1 if not math.isnan(yt) else float("nan")
        worst = max(abs(v) for v in devs.values())
        if best is None or worst < best[0]:
            best = (worst, mexp, nexp, devs)
        if all(abs(v) < 0.05 for v in devs.values()):
            hits.append((mexp, nexp, devs))
fifth = {k: Rstar ** 0.2 / yt - 1 for k, (N, yt) in pts.items()}
twoX2 = {k: 2 * N / 3 / yt - 1 for k, (N, yt) in pts.items()}
numbers["K11"] = {"Rstar": Rstar, "sigma_c_kms": sig_c / 1e3, "n_candidates": 48, "three_point_hits": hits,
                  "closest": {"worst_dev": best[0], "m": best[1], "n": best[2], "devs": best[3]},
                  "disclosed_Rstar_fifth_root": {"value": Rstar ** 0.2, "devs": fifth,
                                                 "label": "numerology (exponent outside frozen set)"},
                  "record_A28_2X2_devs": {"devs": twoX2, "label": "A28 near-miss; coefficient 2 inserted"}}
check("K11", len(hits) == 0 and not math.isnan(best[0]),
      f"0/{48} three-point hits; closest m={best[1]} n={best[2]} worst dev {best[0]*100:.0f}%; "
      f"R*^(1/5)={Rstar**0.2:.2f}: can {fifth['can_kappa_half']*100:+.1f}% alt {fifth['alt']*100:+.1f}% "
      f"th {fifth['thermal']*100:+.1f}% (numerology)", "no member within 5% on all three points")

npass = sum(c_["pass"] for c_ in checks)
log(f"D7_TURNOFF_YT COMPLETE: {npass}/{len(checks)} checks PASS.")
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSON, "w") as fh:
    json.dump({"lane": "D7_turnoff_yt", "mutate": MUTATE, "checks": checks, "numbers": numbers,
               "constants": {"a0_can": A0_CAN, "a0_alt": A0_ALT, "Lambda": LAMBDA, "B_E": B_E,
                             "Lstar_pc": LSTAR_PC, "u_gal_A60": U_GAL, "GM_sun": GM_SUN}},
              fh, indent=1, default=lambda o: o if not isinstance(o, np.generic) else o.item())
sys.exit(0 if npass == len(checks) else 1)
