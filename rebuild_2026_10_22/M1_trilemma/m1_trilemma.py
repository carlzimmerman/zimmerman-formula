#!/usr/bin/env python3
"""M1_trilemma: a way through the v3/v4 trilemma, or a proof that there is none.

Criteria: FROZEN_CRITERIA.md (committed alone first, 3298c74815).  Routes:
  R1  a Khronon J with J'(0) = 0 that equals J_x (mu = x/(1+x)) above x_min  (v3 family)
  R2  screening without gamma_L that tolerates a twisting aether             (v4 family)
  R3  v4's FRW runaway escape (C7), only if R2 has a way through

Read-only reuse: F3's two-fluid growth model and model-A/B backgrounds (re-implemented here, reproduced first, M0);
the record's SPARC loader (campaign_fresh_gravity/CFG4_common.py); B21 RAR files; C1, C6, D10, E2 JSONs.
kappa = 1/2 FITTED.  Footings never pooled.  No dark-matter particle.  Not "theory closed".
Run: OMP_NUM_THREADS=1 nice -n 15 python3 m1_trilemma.py      (M1_MUTATE=1 for the mutation run)
"""
import os, sys, json, math, time, resource
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import erf

T0 = time.time()
MUT = os.environ.get("M1_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUT else ""
OUTF = os.path.join(HERE, f"m1_trilemma{TAG}.out")
JSONF = os.path.join(HERE, f"m1_trilemma_results{TAG}.json")
LINES, CHK, RES = [], {}, {"mutate": MUT, "criteria_commit": "3298c74815"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LINES.append(s)


def check(name, ok, val, thr):
    CHK[name] = dict(ok=bool(ok), value=str(val), threshold=thr)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


def rel(a, b):
    return abs(a / b - 1.0)


# ------------------------------------------------------------------------------------------------ constants
G_SI, C_SI = 6.67430e-11, 2.99792458e8
PC = 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
AU = 1.495978707e11
GMSUN = 1.32712440018e20
MSUN = GMSUN / G_SI
RSUN = 6.957e8                                   # IAU nominal solar radius
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}  # doors BRIEF footings (kappa = 1/2 FITTED)
FOOTS = ("canonical", "alt")
GKMS = 1e6 / KPC                                 # (km/s)^2 / kpc -> m/s^2
UPS_D, UPS_B = 0.5, 0.7                          # SPS (SURVEY-CALIBRATION)

P(f"M1_trilemma{'  [MUTATE: J_Y sign flipped in the PN hold equation; cubic galileon reduced with r^0]' if MUT else ''}"
  f"   criteria 3298c74815   kappa = 1/2 FITTED; footings never pooled")

# ================================================================================================ R1b(i): PN kernel
P("\n=== R1b(i): khronon-dust kernel s(k; f0) from the BS24 post-Newtonian system (BSK1 L15-21 transcription) ===")
k, mu, f0, G, r0, rb = sp.symbols("k mu f_0 G rho_0 rho_b", positive=True)
dr_t, dr_b, Xi, phi, sig_dot = sp.symbols("delta_rho_tau delta_rho_b Xi phi sigmadot")
JY = f0 - 1                                      # J_Y at Y = 0
JY_used = -JY if MUT else JY                     # MUTATE: sign of J_Y flipped
# Fourier (grad^2 -> -k^2), linear about homogeneous rho_0, frozen coefficients:
#   hold:      4 pi G drho_tau = -[div(J_Y grad Xi) + mu^2 Xi]   -> (J_Y k^2 - mu^2) Xi
#   Poisson:   -k^2 phi = 4 pi G (drho_b + drho_tau)
#   lapse:     Xi = phi - sigma_dot ;   continuity: ddot(drho_tau) = rho_0 lap(sigma_dot) = -rho_0 k^2 sigma_dot
sol = sp.solve([sp.Eq(4 * sp.pi * G * dr_t, (JY_used * k ** 2 - mu ** 2) * Xi),
                sp.Eq(-k ** 2 * phi, 4 * sp.pi * G * (dr_b + dr_t)),
                sp.Eq(Xi, phi - sig_dot)], [Xi, phi, sig_dot], dict=True)[0]
dd_tau = sp.simplify(-r0 * k ** 2 * sol[sig_dot])                 # ddot(drho_tau)
s_kernel = sp.simplify(sp.diff(dd_tau, dr_t) / (4 * sp.pi * G * r0))
cross = sp.simplify(sp.diff(dd_tau, dr_b) / (4 * sp.pi * G * r0))
s_expected = (mu ** 2 - f0 * k ** 2) / ((1 - f0) * k ** 2 + mu ** 2)
res_s = sp.simplify(s_kernel - s_expected)
res_bsk2 = sp.simplify(s_kernel.subs(f0, 0) - mu ** 2 / (k ** 2 + mu ** 2))
res_jeans = sp.simplify(s_kernel.subs(f0, 1) - (1 - k ** 2 / mu ** 2))
ds_df0 = sp.simplify(sp.diff(s_expected, f0))
res_ds = sp.simplify(ds_df0 + k ** 4 / ((1 - f0) * k ** 2 + mu ** 2) ** 2)
ok_M1 = all(sp.simplify(e) == 0 for e in (res_s, res_bsk2, res_jeans, res_ds, cross - 1))
RES["R1b_i"] = dict(s=str(s_kernel), cross_coefficient=str(cross), ds_df0=str(ds_df0),
                    residuals=[str(res_s), str(res_bsk2), str(res_jeans), str(res_ds)],
                    reading="s decreases strictly in f0 = 1 + J'(0) at every k > 0: J'(0) = 0 (f0 = 1, Jeans) holds the "
                            "dust MORE than J_x (f0 = 0, BSK2); baryons pull the dust with coefficient 1 at every k")
P(f"  s(k; f0) = {s_kernel};  baryon->dust coefficient = {cross};  ds/df0 = {ds_df0}")
check("M1", ok_M1, f"residuals s:{res_s} BSK2:{res_bsk2} Jeans:{res_jeans} ds/df0:{res_ds}; cross-1:{sp.simplify(cross - 1)}",
      "all exactly 0")

# ================================================================================================ R1b(ii): K-shape identity
P("\n=== R1b(ii): late-time Jeans scale = static mass for any K analytic at Q = 1 with K'(1) = 0 ===")
eps = sp.symbols("epsilon", positive=True)
c3, c4, c5 = sp.symbols("c3 c4 c5", real=True)
Qs = 1 + eps
Kf = mu ** 2 * eps ** 2 + c3 * eps ** 3 + c4 * eps ** 4 + c5 * eps ** 5
Kp = sp.diff(Kf, eps); Kpp = sp.diff(Kf, eps, 2)
rho8 = Qs * Kp - Kf                              # 8 pi G rho / c^4
cs2 = Kp / (Qs * Kpp)
kJ2 = sp.simplify((rho8 / 2) / cs2)              # 4 pi G rho / c_s^2
lim_kJ2 = sp.limit(kJ2, eps, 0)
ok_M2 = sp.simplify(lim_kJ2 - mu ** 2) == 0 and sp.simplify(lim_kJ2 - Kpp.subs(eps, 0) / 2) == 0
ser = sp.series(kJ2, eps, 0, 2).removeO()
RES["R1b_ii"] = dict(kJ2_limit=str(lim_kJ2), series=str(sp.simplify(ser)),
                     Qbar_minus_1_at_cap="filled below",
                     reading="for Q_bar - 1 << 1 (a >> (H0/mu_K)^(2/3), i.e. a >~ 1e-3 at the BS cap) the dust Jeans "
                             "wavenumber is K''(1)/2 = mu_K^2: the same constant BS24 Eq. 39 caps from galaxies; the "
                             "K shape away from Q = 1 acts only before a ~ 1e-3, which F3's a_i = 1e-3 start already "
                             "treats as GR")
P(f"  lim_(Q->1) 4 pi G rho / c_s^2 = {lim_kJ2};  series: {sp.simplify(ser)}")
check("M2", ok_M2, f"limit {lim_kJ2} == mu^2 == K''(1)/2", "exact")

# ================================================================================================ growth machinery
from classy import Class


def make_E(Om, h, rad=True):
    Or = (4.18e-5 / h ** 2) if rad else 0.0
    OL = 1.0 - Om - Or
    return (lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL))


def growth(kk, mu_h, Om, Ob, h, f0=None, ft_of_a=None, a_i=1e-3, a_eval=None):
    """F3's two-fluid sub-horizon model (baryons feel all mass; khronon self-term x s), kernel
    s = (1 - f x^2)/((1 - f) x^2 + 1), x = k/(a mu): f = 0 BSK2, f = 1 Jeans.  Returns delta_m(k, a)/delta_m(mu -> inf)."""
    Ek = make_E(Om, h); OK = Om - Ob; kk = np.asarray(kk, float); n = len(kk)

    def s_of(a, mu_):
        if mu_ is None:
            return np.ones(n)
        f = f0 if ft_of_a is None else ft_of_a(a)
        x2 = (kk / (a * mu_)) ** 2
        return (1.0 - f * x2) / ((1.0 - f) * x2 + 1.0)

    def solve(mu_):
        def rhs(x, st):
            a = math.exp(x); E = Ek(a); e_ = 1e-6
            dlnE = (math.log(Ek(a * math.exp(e_))) - math.log(Ek(a * math.exp(-e_)))) / (2 * e_)
            dens = 1.5 * a ** -3 / E ** 2
            db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
            src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s_of(a, mu_))
            return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
        st0 = np.full(4 * n, a_i)
        te = None if a_eval is None else np.log(np.asarray(a_eval))
        so = solve_ivp(rhs, [math.log(a_i), 0.0], st0, method="DOP853", rtol=1e-7, atol=1e-12, t_eval=te)
        Y = so.y if a_eval is not None else so.y[:, -1:]
        return (Ob * Y[:n] + OK * Y[2 * n:3 * n]) / Om
    out = solve(mu_h) / solve(None)
    return out if a_eval is not None else out[:, 0]


def class_run(wb, wc, h, lnA, ns, tau, zmax=4.0):
    c = Class()
    c.set({"omega_b": wb, "omega_cdm": wc, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "N_ur": 3.044,
           "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": zmax})
    c.compute()
    return c


KS = np.geomspace(1e-4, 50.0, 1500)
KT = np.geomspace(1e-3, 3.0, 36)
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3


def sig8(Pk, T=None):
    Pk = Pk if T is None else Pk * T ** 2
    return math.sqrt(np.trapz(Pk * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))


def s8_ratio(Pk, mu_h, Om, Ob, h, f0=None, ft_of_a=None, a_i=1e-3):
    T = growth(KT, mu_h, Om, Ob, h, f0=f0, ft_of_a=ft_of_a, a_i=a_i)
    Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
    return sig8(Pk, Tf) / sig8(Pk), T


c2b = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]["lcdm_refit"]
wbA, wcA, thA, lnAA, nsA, tauA = c2b["params"]; hA = c2b["chi2"]["H0"] / 100.0
cA = class_run(wbA, wcA, hA, lnAA, nsA, tauA)
OmA, ObA = (wbA + wcA) / hA ** 2, wbA / hA ** 2
PkA = np.array([cA.pk_lin(kq * hA, 0.0) for kq in KS]) * hA ** 3
mu_cap = 10.0 / hA                               # mu_K^-1 = 100 kpc physical (BS24 Eq. 39 edge), in h/Mpc
# Q_bar - 1 = 8 pi G rho_K /(2 mu^2 c^2) = 3 Omega_K (H0/c)^2 / (2 mu^2 a^3) at the cap (quadratic K, leading order)
OKA = wcA / hA ** 2
qm1 = {f"{a:g}": 3 * OKA * (1 / 2997.92458) ** 2 / (2 * mu_cap ** 2 * a ** 3) for a in (1e-4, 1e-3, 3e-3, 1e-2)}
RES["R1b_ii"]["Qbar_minus_1_at_cap"] = qm1
P("  dust-limit validity at the BS cap (model A): Q_bar - 1 = " + ", ".join(f"{v:.2e} at a = {k_}" for k_, v in qm1.items()))
f3 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F3_growth_audit", "f3_growth_audit_results.json")))
f3k4 = {k_: v["sigma8_ratio"] for k_, v in f3["K4"]["BS24_Eq39_edge_100kpc"].items() if isinstance(v, dict)}; f3k5 = f3["K5"]["windows"]["jeans_ai0.001"]["mu_min_hMpc"]

# ================================================================================================ M0 + R1b(iii)
P("\n=== M0 + R1b(iii): sigma8 ratio at the BS cap, f0 = 1 (R1: J'(0) = 0) vs f0 = 0 (J_x) ===")
R1b3 = {}
for f0v, lab in ((1.0, "jeans"), (0.0, "bsk2")):
    for a_i in (1e-3, 1e-4):
        r_, _ = s8_ratio(PkA, mu_cap, OmA, ObA, hA, f0=f0v, a_i=a_i)
        R1b3[f"f0={f0v:g}|ai={a_i:g}"] = r_
        P(f"  f0 = {f0v:g} ({lab}), a_i = {a_i:g}: sigma8 ratio {r_:.5f}   (F3: {f3k4[f'{lab}_ai{a_i:g}']:.5f})")
mumin_f1 = 10 ** brentq(lambda lm: s8_ratio(PkA, 10 ** lm, OmA, ObA, hA, f0=1.0, a_i=1e-3)[0] - 0.95, 1.5, 6.0, xtol=1e-3)
devs = [rel(R1b3["f0=1|ai=0.001"], f3k4["jeans_ai0.001"]), rel(R1b3["f0=1|ai=0.0001"], f3k4["jeans_ai0.0001"]),
        rel(R1b3["f0=0|ai=0.001"], f3k4["bsk2_ai0.001"]), rel(R1b3["f0=0|ai=0.0001"], f3k4["bsk2_ai0.0001"])]
check("M0", max(devs) <= 0.01 and rel(mumin_f1, f3k5) <= 0.02,
      f"max rel dev of 4 ratios {max(devs):.2e}; mu_min(f0=1, a_i 1e-3) {mumin_f1:.2f} vs F3 {f3k5:.2f} h/Mpc",
      "<= 1% and <= 2%")
diag = {}
for f0v in (0.01, 0.1, 0.5):
    diag[f"{f0v:g}"] = s8_ratio(PkA, mu_cap, OmA, ObA, hA, f0=f0v, a_i=1e-3)[0]
P("  diagnostic (reported only), a_i 1e-3: " + "; ".join(f"f0 {k_}: {v:.4f}" for k_, v in diag.items()))
# reported only (added post-result, no frozen line): the K-shape door at its most generous. Q_bar - 1 = 7e-3 at a = 3e-3,
# so any analytic K is in the dust limit (k_J = mu_K to < 1 %) from there on; starting GR growth at a_i = 3e-3 is the
# upper bound any K shape can buy.
kdoor = {f"f0={f0v:g}|ai=0.003": s8_ratio(PkA, mu_cap, OmA, ObA, hA, f0=f0v, a_i=3e-3)[0] for f0v in (1.0, 0.0)}
P("  K-shape door, reported only: GR growth until a = 3e-3, then the dust limit: " + "; ".join(f"{k_} {v:.4f}" for k_, v in kdoor.items()))
mono = [R1b3["f0=0|ai=0.001"], diag["0.01"], diag["0.1"], diag["0.5"], R1b3["f0=1|ai=0.001"]]
R1_lin_pass = R1b3["f0=1|ai=0.001"] >= 0.95
RES["R1b_iii"] = dict(mu_cap_hMpc=mu_cap, ratios=R1b3, K_shape_door_ai3em3_reported_only=kdoor, mu_min_f0_1_ai1em3=mumin_f1, gap_factor=mumin_f1 / mu_cap,
                      diagnostic_f0=diag, monotone_decreasing_in_f0=bool(all(np.diff(mono) < 0)),
                      F3_reference=dict(K4=f3k4, K5_mu_min_jeans=f3k5),
                      pass_line="sigma8 ratio(f0=1, a_i=1e-3) >= 0.95 at mu_K <= 14.8 h/Mpc", R1_linear_growth="PASS" if R1_lin_pass else "FAIL")
P(f"  R1 linear growth line: ratio(f0=1, a_i=1e-3) = {R1b3['f0=1|ai=0.001']:.4f} vs 0.95 -> {'PASS' if R1_lin_pass else 'FAIL'}; "
  f"mu_min = {mumin_f1:.0f} h/Mpc = {mumin_f1 / mu_cap:.1f} x the cap; monotone decreasing in f0 over [0, .01, .1, .5, 1]: "
  f"{RES['R1b_iii']['monotone_decreasing_in_f0']}")

# ================================================================================================ R1a: data x_min
P("\n=== R1a: the lowest field strength at which data require the law ===")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C  # noqa: E402  (the record's SPARC loader)
GAL = C.load_sparc()
pts = []
for g in GAL:
    m = g["meta"]
    if m is None or m["Q"] > 2 or m["Inc"] < 30:
        continue
    R, V, eV = g["R"], g["Vobs"], g["eV"]
    gbar = (g["Vgas"] * np.abs(g["Vgas"]) + UPS_D * g["Vdisk"] * np.abs(g["Vdisk"]) + UPS_B * g["Vbul"] * np.abs(g["Vbul"])) / R * GKMS
    ggas = g["Vgas"] * np.abs(g["Vgas"]) / R * GKMS
    gstar = (UPS_D * g["Vdisk"] * np.abs(g["Vdisk"]) + UPS_B * g["Vbul"] * np.abs(g["Vbul"])) / R * GKMS
    ok = (R > 0) & (V > 0) & (eV / np.where(V > 0, V, 1) <= 0.10) & (gbar > 0)
    for i in np.where(ok)[0]:
        pts.append((g["name"], R[i], V[i] ** 2 / R[i] * GKMS, gbar[i], ggas[i], gstar[i], m["RHI"], m["Vflat"]))
names = [p_[0] for p_ in pts]
Rk = np.array([p_[1] for p_ in pts]); gobs = np.array([p_[2] for p_ in pts]); gbar = np.array([p_[3] for p_ in pts])
ggas = np.array([p_[4] for p_ in pts]); gstar = np.array([p_[5] for p_ in pts]); RHI = np.array([p_[6] for p_ in pts])
B21D = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
b = np.loadtxt(os.path.join(B21D, "Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"))
gobs_b21 = 4 * 4.52e-30 * b[:, 1] / b[:, 4] * 3.086e16
snr = b[:, 1] / b[:, 3]
i_b = int(np.where(snr >= 3)[0][np.argmin(b[snr >= 3, 0])])
readme_check = 4 * 4.52e-30 * (b[0, 1] / b[0, 4]) * 3.086e16
check("M3", len(GAL) == 175 and abs(gobs_b21[0] / readme_check - 1) < 1e-12 and len(pts) > 1000,
      f"{len(GAL)} rotmod files; {len(pts)} SPARC points kept (Q<=2, i>=30, eV/V<=0.1); B21 g_obs[0] {gobs_b21[0]:.4e} = README formula",
      "175 files, conversion exact")
c6 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C6_literal_cassini", "c6_literal_cassini_results.json")))
d10 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar", "d10_native_lstar_results.json")))


def law_x(y):                                    # AQUAL mu = x/(1+x): x^2/(1+x) = y
    return (y + np.sqrt(y * y + 4 * y)) / 2


R1a = {}
for fo in FOOTS:
    a0 = A0[fo]
    xo = gobs / a0
    x_sp1, x_sp99 = float(np.percentile(xo, 1)), float(np.percentile(xo, 99))
    x_b21 = float(gobs_b21[i_b] / a0)
    x_min_all = min(x_sp1, x_b21)
    F = lambda x: x * x / (1 + x)
    xe_ss = [c6["inputs"]["E"][fo][e]["ge"] / c6["inputs"]["a0"][fo] for e in ("E0", "E1", "E2", "E3")]
    xe_gc = {}
    for cl in ("Pal 4", "Pal 14"):
        Rg = d10["clusters"][cl]["RGC"] * KPC
        xe_gc[cl] = [float(law_x(G_SI * M * MSUN / (Rg + 3 * KPC) ** 2 / a0)) for M in d10["MW_Mb"][fo].values()]
    R1a[fo] = dict(x_SPARC_p1=x_sp1, x_SPARC_min=float(xo.min()), x_SPARC_p99=x_sp99, x_B21_lowest_S3=x_b21,
                   B21_gbar_bin=float(b[i_b, 0]), B21_snr=float(snr[i_b]),
                   x_min_with_B21=x_min_all, x_min_SPARC_only=x_sp1,
                   x_t_max_with_B21=F(x_min_all), x_t_max_SPARC_only=F(x_sp1),
                   nonforcing=dict(wide_binaries_x_e=xe_ss, D10_globulars_x_e=xe_gc,
                                   E3="dwarfs need MORE than the law (E3 +0.89 dex); they set no x_min"))
    P(f"  [{fo}] SPARC x_obs p1 {x_sp1:.3e} (min {xo.min():.3e}, p99 {x_sp99:.2f}); B21 lowest S/N>=3 bin (g_bar {b[i_b, 0]:.2e}, "
      f"S/N {snr[i_b]:.1f}): x {x_b21:.3e} -> x_min {x_min_all:.3e} (SPARC only {x_sp1:.3e}); T1: x_t <= {F(x_min_all):.2e} "
      f"(SPARC only {F(x_sp1):.2e}); WB x_e {min(xe_ss):.2f}-{max(xe_ss):.2f}; Pal 4/14 x_e "
      f"{min(min(v) for v in xe_gc.values()):.3f}-{max(max(v) for v in xe_gc.values()):.3f} (they demand Newton)")
RES["R1a"] = R1a

# ================================================================================================ R1b(iv): physical regime
P("\n=== R1b(iv): is the Y = 0 expansion the physical one?  rms field of the modes whose kernel differs (a mu < k < 10 h/Mpc) ===")
OM886, H886 = 0.2976015949416498, 0.6856426703851345
wbB, hB = wbA, H886; wcB = OM886 * hB ** 2 - wbB
cB = class_run(wbB, wcB, hB, lnAA, nsA, tauA, zmax=1000.0)
OmB, ObB = OM886, wbB / hB ** 2
PkB0 = np.array([cB.pk_lin(kq * hB, 0.0) for kq in KS]) * hB ** 3
s8B_own, s8B_cl = sig8(PkB0), cB.sigma8()
check("M4", rel(s8B_own, s8B_cl) <= 1e-3, f"model B sigma8 own {s8B_own:.5f} vs CLASS {s8B_cl:.5f}", "<= 1e-3")
mu_capB = 10.0 / hB
H0B = hB * 1e5 / MPC
AG = [1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0]
KQ = np.geomspace(1e-4, 10.0, 300)              # h/Mpc
Tsup = growth(KQ, mu_capB, OmB, ObB, hB, f0=1.0, a_i=1e-3, a_eval=AG)   # f0 = 1 suppression (lower estimate)


def g_rms(a, klo, khi, T=None):
    sel = (KQ >= klo) & (KQ <= khi)
    if sel.sum() < 3:
        return None
    z = 1.0 / a - 1.0
    Pk = np.array([cB.pk_lin(kq * hB, z) for kq in KQ[sel]])         # Mpc^3, k in 1/Mpc
    if T is not None:
        Pk = Pk * T[sel] ** 2
    I = np.trapz(Pk, KQ[sel] * hB) / (2 * math.pi ** 2)               # Mpc^2
    return 1.5 * H0B ** 2 * OmB / a ** 2 * math.sqrt(I) * MPC


R1b4 = {fo: {} for fo in FOOTS}
gall = {}
for j, a in enumerate(AG):
    g_lo = g_rms(a, a * mu_capB, 10.0)
    g_lo_sup = g_rms(a, a * mu_capB, 10.0, T=Tsup[:, j])
    g_all = g_rms(a, 1e-4, 10.0)
    gall[a] = g_all
    for fo in FOOTS:
        a0 = A0[fo]; xt = R1a[fo]["x_t_max_with_B21"]; xt2 = R1a[fo]["x_t_max_SPARC_only"]
        row = dict(x_all=g_all / a0, x_kgt_amu=None if g_lo is None else g_lo / a0,
                   x_kgt_amu_f0_1_suppressed=None if g_lo_sup is None else g_lo_sup / a0)
        for key, xt_ in (("with_B21", xt), ("SPARC_only", xt2)):
            for col, xr in (("dustlimit", row["x_kgt_amu"]), ("suppressed", row["x_kgt_amu_f0_1_suppressed"])):
                if xr is not None:
                    z_ = math.sqrt(3) * xt_ / xr
                    row[f"ratio_{col}_to_xt_{key}"] = xr / xt_
                    row[f"P(x<xt)_{col}_{key}"] = float(erf(z_ / math.sqrt(2)) - math.sqrt(2 / math.pi) * z_ * math.exp(-z_ * z_ / 2))
            if row["x_kgt_amu"] is not None:
                row["ratio_dustlimit_to_xmin_" + key] = row["x_kgt_amu"] / (R1a[fo]["x_min_with_B21"] if key == "with_B21" else R1a[fo]["x_min_SPARC_only"])
        R1b4[fo][f"{a:g}"] = row
for fo in FOOTS:
    P(f"  [{fo}] a: x_all | x(k>a mu) | x(k>a mu, f0=1 suppressed) | x/x_t,max(B21) dust-limit (suppressed) | P(x < x_t,max) -- "
      f"x_t,max {R1a[fo]['x_t_max_with_B21']:.2e} (SPARC only {R1a[fo]['x_t_max_SPARC_only']:.2e})")
    for a in AG:
        r_ = R1b4[fo][f"{a:g}"]
        if r_["x_kgt_amu"] is None:
            P(f"     a {a:<6g}: {r_['x_all']:.3e} | (empty k range: a mu > 10 h/Mpc)")
        else:
            P(f"     a {a:<6g}: {r_['x_all']:.3e} | {r_['x_kgt_amu']:.3e} | {r_['x_kgt_amu_f0_1_suppressed']:.3e} | "
              f"{r_['ratio_dustlimit_to_xt_with_B21']:.2e} ({r_['ratio_suppressed_to_xt_with_B21']:.2e}) | "
              f"{r_['P(x<xt)_dustlimit_with_B21']:.1e} ({r_['P(x<xt)_suppressed_with_B21']:.1e})  [SPARC-only: ratio "
              f"{r_['ratio_dustlimit_to_xt_SPARC_only']:.2f} ({r_['ratio_suppressed_to_xt_SPARC_only']:.2f}), P "
              f"{r_['P(x<xt)_dustlimit_SPARC_only']:.1e} ({r_['P(x<xt)_suppressed_SPARC_only']:.1e}); x/x_min {r_['ratio_dustlimit_to_xmin_with_B21']:.2f}"
              f" / {r_['ratio_dustlimit_to_xmin_SPARC_only']:.2f}]")
phys = {}
for fo in FOOTS:
    mr = lambda key: min(R1b4[fo][k_][key] for k_ in R1b4[fo] if key in R1b4[fo][k_])
    phys[fo] = dict(min_ratio_dustlimit_B21=mr("ratio_dustlimit_to_xt_with_B21"), min_ratio_dustlimit_SPARC_only=mr("ratio_dustlimit_to_xt_SPARC_only"),
                    min_ratio_suppressed_B21=mr("ratio_suppressed_to_xt_with_B21"), min_ratio_suppressed_SPARC_only=mr("ratio_suppressed_to_xt_SPARC_only"),
                    Y0_expansion_physical=bool(mr("ratio_dustlimit_to_xt_with_B21") <= 1.0),
                    Y0_expansion_physical_SPARC_only_variant=bool(mr("ratio_dustlimit_to_xt_SPARC_only") <= 1.0),
                    rule="FROZEN: dust-limit x_N,rms (k > a mu) vs x_t,max from x_min = min(SPARC p1, B21); SPARC-only and suppressed columns reported")
RES["R1b_iv"] = dict(table=R1b4, summary=phys, mu_capB_hMpc=mu_capB,
                     note="x is |grad phi|/a0 of the dust-limit field in the modes a mu < k < 10 h/Mpc; the khronon "
                          "acceleration |grad Xi| obeys |Xi_k| >= 4 pi G drho_tau/(k^2+mu^2) for every f0 in [0,1], i.e. "
                          ">= (Omega_tau/Omega_m)/2 of this at k >= a mu; the f0 = 1-suppressed column is a lower estimate")
P("  summary (frozen rule: dust-limit column vs x_t,max with B21): " + "; ".join(
    f"{fo}: min x/x_t,max {phys[fo]['min_ratio_dustlimit_B21']:.1f} -> Y = 0 expansion physical: {phys[fo]['Y0_expansion_physical']} "
    f"[SPARC-only variant: min ratio {phys[fo]['min_ratio_dustlimit_SPARC_only']:.2f} -> {phys[fo]['Y0_expansion_physical_SPARC_only_variant']}; "
    f"suppressed column min ratios {phys[fo]['min_ratio_suppressed_B21']:.2f} / {phys[fo]['min_ratio_suppressed_SPARC_only']:.4f}]" for fo in FOOTS))
# mean-field WKB estimate (reported only): f_t(a) = f(x) + x f'(x)/3 at x = x_all(a)
lna = np.log(AG)
mf = {}
for fo in FOOTS:
    xa = np.array([gall[a] / A0[fo] for a in AG])

    def ft(a, xa=xa):
        x = math.exp(np.interp(math.log(a), lna, np.log(xa)))
        return x / (1 + x) + x / (1 + x) ** 2 / 3.0
    mf[fo] = dict(sigma8_ratio=s8_ratio(PkB0, mu_capB, OmB, ObB, hB, ft_of_a=ft, a_i=1e-3)[0],
                  f_t_at_a={f"{a:g}": ft(a) for a in AG})
    P(f"  [{fo}] mean-field WKB ESTIMATE (not a verdict): sigma8 ratio {mf[fo]['sigma8_ratio']:.4f}; f_t(a) "
      + ", ".join(f"{a}:{v:.3f}" for a, v in mf[fo]["f_t_at_a"].items()))
RES["R1b_iv"]["mean_field_estimate"] = mf

# ================================================================================================ R1c: health + Cassini
P("\n=== R1c: health (C5) of an explicit R1 construction, and the Cassini carry-over (C6) ===")
R1c = {}
ok5 = True
for fo in FOOTS:
    xmin = R1a[fo]["x_min_with_B21"]; Fm = xmin * xmin / (1 + xmin); xt = Fm / 2.0

    def F_R1(x):
        x = np.asarray(x, float)
        t = np.clip((x - xt) / (xmin - xt), 0, 1)
        S = 3 * t * t - 2 * t ** 3
        Fb = xt + (Fm - xt) * S
        return np.where(x <= xt, x, np.where(x < xmin, Fb, x * x / (1 + x)))

    def dF_R1(x):
        x = np.asarray(x, float)
        t = np.clip((x - xt) / (xmin - xt), 0, 1)
        dS = 6 * t * (1 - t) / (xmin - xt)
        return np.where(x <= xt, 1.0, np.where(x < xmin, (Fm - xt) * dS, (2 * x + x * x) / (1 + x) ** 2))
    xg = np.geomspace(1e-8, 1e4, 20001)
    f_ = F_R1(xg) / xg; dF = dF_R1(xg)
    okh = bool(np.all(f_ >= 0) and np.all(f_ <= 1 + 1e-15) and np.all(dF >= 0) and np.all(dF <= 1 + 1e-15) and np.all(np.diff(F_R1(xg)) >= 0))
    xe = np.array([c6["inputs"]["E"][fo][e]["ge"] / c6["inputs"]["a0"][fo] for e in ("E0", "E1", "E2", "E3")])
    fJ, dJ = xe / (1 + xe), (2 * xe + xe * xe) / (1 + xe) ** 2
    idd = float(max(np.max(np.abs(F_R1(xe) / xe / fJ - 1)), np.max(np.abs(dF_R1(xe) / dJ - 1))))
    q2 = max(v["over_Hees_upper"] for k_, v in c6["R1_physical"].items() if k_.startswith(fo + "|"))
    q2_24 = max(v["over_Hees_upper"] for k_, v in c6["R1_physical"].items() if k_.startswith(fo + "|24|"))
    R1c[fo] = dict(x_t=xt, x_min=xmin, health_grid_pass=okh, f_equals_1_below_xt=True, M_T_at_Y0="infinite (edge of C5)",
                   identity_at_x_e=idd, C6_max_Q2_over_Hees_upper=q2, C6_max_Q2_over_Hees_upper_24pc=q2_24,
                   cassini="PASS" if (idd <= 1e-12 and q2 <= 1) else "FAIL")
    ok5 = ok5 and okh and idd <= 1e-12
    P(f"  [{fo}] x_t {xt:.3e}, x_min {xmin:.3e}: 0<=f<=1, 0<=F'<=1, F monotone on 1e-8..1e4: {okh}; f, F' at C6 x_e "
      f"{xe.min():.2f}-{xe.max():.2f} identical to J_x (max rel {idd:.1e}); C6 max Q2/Hees upper {q2:.2e} (24 pc {q2_24:.2e}) "
      f"-> Cassini {R1c[fo]['cassini']}")
check("M5", ok5, "R1 construction meets C5's inequalities on the grid; identity at x_e exact", "all grid points; <= 1e-12")
RES["R1c"] = R1c

# ================================================================================================ R2: theorem T2 (law forms)
P("\n=== R2: theorem T2 -- health makes the anomaly non-decreasing in g (AeST / A33 static sector) ===")
u, a0s = sp.symbols("u a_0", positive=True)
Rcap = u ** 2 / (a0s - u)
gofu = u + Rcap
ML = sp.simplify(sp.diff(gofu, u))
Rp = sp.simplify(sp.diff(Rcap, u))
okT2 = sp.simplify(ML - 1 - Rp) == 0 and sp.simplify(Rp - u * (2 * a0s - u) / (a0s - u) ** 2) == 0
check("M7", okT2, f"M_L = dg/du = {ML}; R' = {Rp} >= 0 on [0, a0)", "exact")
pb = c6["inputs"]["planet_bounds"]
T2 = {}
for fo in FOOTS:
    x99 = R1a[fo]["x_SPARC_p99"]; uf = A0[fo] * x99 / (1 + x99)
    u1 = A0[fo] * 0.5                            # reported only: the law's anomaly at x = 1 (50 % of g, well measured)
    T2[fo] = dict(x99=x99, u_floor=uf, u_floor_over_bounds={pl: uf / pb[pl][1] for pl in pb},
                  reported_only_floor_at_x1=dict(u=u1, over_bounds={pl: u1 / pb[pl][1] for pl in pb}))
    P(f"  [{fo}] SPARC x99 {x99:.2f} -> any C5-healthy AeST/A33 law matching SPARC has planet anomaly >= {uf:.3e} m/s^2 = "
      + ", ".join(f"{pl} {uf / pb[pl][1]:.2e}x" for pl in pb) + " its bound; reported only, floor at x = 1 (u = a0/2): "
      + ", ".join(f"{pl} {0.5 * A0[fo] / pb[pl][1]:.2e}x" for pl in pb))
RES["R2_T2"] = T2

# ================================================================================================ R2a: galileons
P("\n=== R2a: Horndeski galileons of the AeST scalar (Vainshtein) ===")
r = sp.symbols("r", positive=True)
chi = sp.Function("chi"); Psi = sp.Function("Psi")
uu, up = sp.symbols("u u_p")
# Cartesian check of the spherical Hessian invariants on the x-axis
xs, ys, zs = sp.symbols("xs ys zs", real=True)
f_r = sp.Function("chi_r")
R_ = sp.sqrt(xs ** 2 + ys ** 2 + zs ** 2)
chiC = f_r(R_)
H = sp.Matrix(3, 3, lambda i, j: sp.diff(chiC, [xs, ys, zs][i], [xs, ys, zs][j]))
grad2 = sum(sp.diff(chiC, v) ** 2 for v in (xs, ys, zs))
r1 = sp.symbols("r1", positive=True)
on_axis = {ys: 0, zs: 0}


def ax(e):
    return sp.simplify(e.subs(on_axis).subs(xs, r1).doit())


trH = ax(H.trace()); trH2 = ax((H * H).trace()); detH = ax(H.det()); g2 = ax(grad2)
# replace derivatives by u, u'
def to_u(e):
    e = e.replace(lambda q: isinstance(q, sp.Derivative) and q.derivative_count == 2, lambda q: up)
    e = e.replace(lambda q: isinstance(q, sp.Derivative) and q.derivative_count == 1, lambda q: uu)
    return sp.simplify(e)
trH, trH2, detH, g2 = to_u(trH), to_u(trH2), to_u(detH), to_u(g2)
L3s = g2 * trH                                   # |grad chi|^2 lap chi
L4s = g2 * (trH ** 2 - trH2)                     # |grad chi|^2 [(lap chi)^2 - (dd chi)^2]
L5s = g2 * 6 * detH                              # |grad chi|^2 [(tr)^3 - 3 tr tr2 + 2 tr3] = 6 det in 3D
meas3 = (1 if MUT else r1 ** 2)                  # MUTATE: cubic reduced with r^0 instead of the r^2 measure


def flux(Lr):                                    # E = dL/du - d/dr dL/du'  (the conserved radial flux of the chi equation)
    U = sp.Function("U")(r1); Up = sp.Derivative(U, r1); Upp = sp.Derivative(U, (r1, 2))
    dLdu = sp.diff(Lr, uu).subs({uu: U, up: Up}); dLdup = sp.diff(Lr, up).subs({uu: U, up: Up})
    E = sp.expand(dLdu - sp.diff(dLdup, r1))
    upp = sp.Symbol("u_pp")
    E = E.subs(Upp, upp).subs(Up, up).subs(U, uu)
    return sp.simplify(E)


E3_ = flux(meas3 * L3s); E4_ = flux(r1 ** 2 * L4s); E5_ = flux(r1 ** 2 * L5s)
ok_red = sp.simplify(E3_ - 4 * r1 * uu ** 2) == 0 and sp.simplify(E4_ - 4 * uu ** 3) == 0 and sp.simplify(E5_) == 0
# galileon EoM blind to a uniform external gradient: EL of L3 in Cartesian depends on second derivatives only
cx = sp.Function("c")(xs, ys, zs)
L3c = sum(sp.diff(cx, v) ** 2 for v in (xs, ys, zs)) * sum(sp.diff(cx, v, 2) for v in (xs, ys, zs))
from sympy.calculus.euler import euler_equations
EL3 = sp.expand(euler_equations(L3c, cx, [xs, ys, zs])[0].lhs)
bx, by, bz = sp.symbols("b_x b_y b_z", real=True)
c2f = sp.Function("c2")(xs, ys, zs)
EL3_shift = sp.simplify(EL3.subs(cx, c2f + bx * xs + by * ys + bz * zs).doit() - EL3.subs(cx, c2f).doit())
HH = sp.Matrix(3, 3, lambda i, j: sp.diff(cx, [xs, ys, zs][i], [xs, ys, zs][j]))
EL3_vs_gal = sp.simplify(sp.expand(EL3) - sp.expand(-2 * (HH.trace() ** 2 - (HH * HH).trace())))
order_EL3 = max((d.derivative_count for d in EL3.atoms(sp.Derivative)), default=0)
# I1's tilted-slice discriminant: Omega = gamma^2 omega^2, kappa perp w
A_, B_, M_, w_, kq, Om_ = sp.symbols("A B M w kappa2 Omega", positive=True)
disp = sp.expand(Om_ - (A_ * (kq + w_ ** 2 * Om_) ** 2 + B_ * (kq + w_ ** 2 * Om_) + M_ ** 2))
pc_ = sp.Poly(disp, Om_).all_coeffs()
disc = sp.simplify(pc_[1] ** 2 - 4 * pc_[0] * pc_[2])
kc2 = sp.solve(sp.Eq(disc, 0), kq)
kc2_I1 = (1 - B_ * w_ ** 2) ** 2 / (4 * A_ * w_ ** 2) - M_ ** 2 * w_ ** 2
ok_I1 = any(sp.simplify(sol_ - kc2_I1) == 0 for sol_ in kc2)
lim_A0 = sp.limit(kc2_I1.subs({B_: sp.Rational(1, 4), w_: 1}), A_, 0, "+")
# AeST static sector (C1/E2 form, spherical) + galileons on chi: the chi Euler-Lagrange equation is -d/dr of the flux
#   r^2 [(Psi' - chi')/K - W'(chi')] + c3 E3 + c4 E4, and Psi's gives r^2 (Psi' - chi') = K m(r): so K W'(u) = g_N + (K/r^2)(c3 E3 + c4 E4)
Kc, c3g, c4g = sp.symbols("K c_3 c_4", positive=True)
Wf = sp.Function("W"); Ps = sp.Function("Psi")(r1); ch = sp.Function("chi")(r1); rhoF = sp.Function("rho")(r1)
uc, ucp = sp.diff(ch, r1), sp.diff(ch, r1, 2)
Lr_full = r1 ** 2 * (-(sp.diff(Ps, r1) - uc) ** 2 / (2 * Kc) - Wf(uc) - rhoF * Ps) \
    + c3g * meas3 * L3s.subs({uu: uc, up: ucp}) + c4g * r1 ** 2 * L4s.subs({uu: uc, up: ucp})
ELs = euler_equations(Lr_full, [Ps, ch], r1)
EL_chi = ELs[1].lhs                              # euler_equations returns [Psi, chi] in order
flux_c = r1 ** 2 * ((sp.diff(Ps, r1) - uc) / Kc - sp.Subs(sp.Derivative(Wf(sp.Symbol("q")), sp.Symbol("q")), sp.Symbol("q"), uc).doit()) \
    + c3g * 4 * r1 * uc ** 2 + c4g * 4 * uc ** 3
res_flux = sp.simplify(sp.expand(EL_chi + sp.diff(flux_c, r1)))
res_flux2 = sp.simplify(sp.expand(EL_chi - sp.diff(flux_c, r1)))
ok_flux = (res_flux == 0) or (res_flux2 == 0)
RES["R2a_reduction_AeST_flux_residual"] = [str(res_flux), str(res_flux2)]
ok_M6 = ok_red and ok_flux and EL3_shift == 0 and EL3_vs_gal == 0 and order_EL3 == 2 and ok_I1 and lim_A0 == sp.oo
check("M6", ok_M6, f"E3 = {E3_}, E4 = {E4_}, E5 = {E5_}; AeST+galileon chi flux exact: {ok_flux}; EL(L3) shift-blind: {EL3_shift == 0}; EL(L3) = -2[(tr H)^2 - tr H^2]: "
      f"{EL3_vs_gal == 0}; EL order {order_EL3}; I1 kappa_c^2 reproduced: {ok_I1}; kappa_c -> {lim_A0} as A -> 0+",
      "E3 = 4 r u^2, E4 = 4 u^3, E5 = 0; exact")
RES["R2a_reduction"] = dict(E3=str(E3_), E4=str(E4_), E5=str(E5_), EL3_order=order_EL3, I1_kappa_c2=str(kc2_I1),
                            law="R(u) + (r3/r) u^2/a0 + (r4/r)^2 u^3/a0^2 = g_N  (signs that screen; the opposite signs anti-screen)")


def Rlaw(uu_, a0):
    return uu_ * uu_ / (a0 - uu_)


def solve_u(gN, rr_, a0, r3=0.0, r4=0.0, n=200):
    lo = np.zeros_like(gN); hi = np.full_like(gN, a0 * (1 - 1e-15))
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        val = Rlaw(mid, a0) + (r3 / rr_) * mid ** 2 / a0 + (r4 / rr_) ** 2 * mid ** 3 / a0 ** 2 - gN
        hi = np.where(val > 0, mid, hi); lo = np.where(val > 0, lo, mid)
    return 0.5 * (lo + hi)


deep = gbar < 0.1 * A0["canonical"]
rS = Rk * KPC
R2a = {}
for fo in FOOTS:
    a0 = A0[fo]
    req = {}
    for pl, (rpl, ub) in pb.items():
        gN = GMSUN / rpl ** 2
        req[pl] = dict(r3_min_m=rpl * a0 * (gN - Rlaw(ub, a0)) / ub ** 2,
                       r4_min_m=rpl * a0 * math.sqrt((gN - Rlaw(ub, a0)) / ub ** 3))
    r3m = max(v["r3_min_m"] for v in req.values()); r4m = max(v["r4_min_m"] for v in req.values())
    dk = deep if fo == "canonical" else gbar < 0.1 * a0
    gb = gbar[dk]; rr_ = rS[dk]
    u_law = solve_u(gb, rr_, a0)
    cost = {}
    for lab, (r3, r4) in {"cubic": (r3m, 0.0), "quartic": (0.0, r4m), "mix_0.1": (0.1 * r3m, math.sqrt(0.9) * r4m),
                          "mix_0.5": (0.5 * r3m, math.sqrt(0.5) * r4m), "mix_0.9": (0.9 * r3m, math.sqrt(0.1) * r4m)}.items():
        ug = solve_u(gb, rr_, a0, r3, r4)
        dl = np.log10((gb + ug) / (gb + u_law))
        cost[lab] = dict(r3_pc=r3 / PC, r4_pc=r4 / PC, median_dlog_g=float(np.median(dl)), p10=float(np.percentile(dl, 10)),
                         p90=float(np.percentile(dl, 90)))
    # every member used for the cost meets every planet bound (pure and mixed): check
    mix_ok = True
    for pl, (rpl, ub) in pb.items():
        gN = GMSUN / rpl ** 2
        for th in (0.0, 0.1, 0.5, 0.9, 1.0):
            u_ = solve_u(np.array([gN]), np.array([rpl]), a0, th * r3m, math.sqrt(1 - th) * r4m)[0]
            mix_ok = mix_ok and bool(u_ <= ub * (1 + 1e-6))
    R2a[fo] = dict(required=req, r3_min_pc=r3m / PC, r4_min_pc=r4m / PC, n_deep=int(dk.sum()), sparc_cost=cost,
                   G_pass=bool(min(abs(v["median_dlog_g"]) for v in cost.values()) <= 0.05), all_members_meet_planet_bounds=mix_ok)
    P(f"  [{fo}] planets need r3 >= {r3m / PC:.3e} pc ({r3m / MPC / 1e3:.2f} Gpc) or r4 >= {r4m / PC:.3e} pc; SPARC deep points "
      f"(N {int(dk.sum())}) median dlog g: " + "; ".join(f"{k_} {v['median_dlog_g']:+.3f}" for k_, v in cost.items())
      + f" -> (G) {'PASS' if R2a[fo]['G_pass'] else 'FAIL'}")
RES["R2a"] = R2a

# ================================================================================================ R2b: density / curvature keyed
P("\n=== R2b: density- and curvature-keyed couplings ===")
Phi_sun = GMSUN / RSUN / C_SI ** 2
Phi_gc = {cl: G_SI * 1.6 * d10["clusters"][cl]["LV"] * MSUN / (d10["clusters"][cl]["rhl"] * PC) / C_SI ** 2 for cl in ("Pal 4", "Pal 14")}
vf = np.array([g["meta"]["Vflat"] for g in GAL if g["meta"] is not None and g["meta"]["Vflat"] > 0])
Phi_gal_min, Phi_gal_max = (vf.min() * 1e3) ** 2 / C_SI ** 2, (vf.max() * 1e3) ** 2 / C_SI ** 2
inc_fail = min(Phi_gc.values()) < Phi_gal_min
dec_fail = Phi_sun > Phi_gal_max
b1 = dict(Phi_sun=Phi_sun, Phi_globulars=Phi_gc, Phi_SPARC_min_Vflat2=Phi_gal_min, Phi_SPARC_max_Vflat2=Phi_gal_max,
          increasing_rule_fails=bool(inc_fail), decreasing_rule_fails=bool(dec_fail), verdict="NO-GO" if (inc_fail and dec_fail) else "OPEN")
P(f"  b1 potential-keyed: Sun {Phi_sun:.2e}, Pal 4 {Phi_gc['Pal 4']:.2e}, Pal 14 {Phi_gc['Pal 14']:.2e} (must screen) vs SPARC "
  f"|Phi| >= V_flat^2/c^2 in [{Phi_gal_min:.2e}, {Phi_gal_max:.2e}] (must not): increasing rule fails {inc_fail} "
  f"(Pal 14 is {Phi_gal_min / min(Phi_gc.values()):.0f}x shallower than the shallowest galaxy); decreasing rule fails {dec_fail} -> {b1['verdict']}")
# b2: stars screened as MOND sources (the Sun is a main-sequence star): anomaly from gas only
b2 = {}
for fo in FOOTS:
    a0 = A0[fo]
    sel = (gbar < 0.1 * a0) & (gstar > np.maximum(ggas, 0))
    gb, gg = gbar[sel], np.maximum(ggas[sel], 0)
    u_all = solve_u(gb, rS[sel], a0); u_gas = solve_u(gg, rS[sel], a0)
    dl = np.log10((gb + u_gas) / (gb + u_all))
    b2[fo] = dict(n=int(sel.sum()), median_dlog_g=float(np.median(dl)), p10=float(np.percentile(dl, 10)), p90=float(np.percentile(dl, 90)),
                  G_pass=bool(abs(np.median(dl)) <= 0.05))
    P(f"  b2 [{fo}] body-density (stars screened as sources), SPARC deep star-dominated points N {sel.sum()}: median dlog g "
      f"{np.median(dl):+.3f} (p10 {np.percentile(dl, 10):+.3f}) -> (G) {'PASS' if b2[fo]['G_pass'] else 'FAIL'}")
b2["test_body_variant"] = ("EXTERNAL premise (not on disk): Pal 4/Pal 14 (D10) and dSph (E3) dispersions are both measured on red giants, "
                           "so a test-body density rule cannot screen one and not the other")
# b3: ambient field-point density (CONDITIONAL on external inputs)
n_sw_sat = 5.0 / (c6["inputs"]["R_Saturn_AU"]) ** 2          # cm^-3, EXTERNAL (n_sw(1 AU) = 5 cm^-3, r^-2)
MSUN_PC3_TO_H_CM3 = MSUN / PC ** 3 / 1.6735575e-27 / 1e6
b3 = {}
for fo in FOOTS:
    a0 = A0[fo]
    sel = gbar < 0.1 * a0
    inside = Rk[sel] <= RHI[sel]
    frac = float(inside.mean())
    rows = {}
    for hz in (100.0, 300.0, 1000.0):
        nHI = 1.0 / (2 * hz) * MSUN_PC3_TO_H_CM3
        rows[f"{hz:g}"] = dict(n_HI_at_RHI=nHI, exceeds_solar_wind_at_Saturn=bool(nHI > n_sw_sat), exceeds_LISM_0p1=bool(nHI > 0.1))
    hz_crit = 1.0 / (2 * n_sw_sat / MSUN_PC3_TO_H_CM3)
    b3[fo] = dict(frac_deep_inside_RHI=frac, by_hz=rows, n_sw_Saturn=n_sw_sat, hz_crit_pc=hz_crit,
                  verdict="NO-GO (CONDITIONAL)" if (frac > 0.5 and rows["300"]["exceeds_solar_wind_at_Saturn"]) else "OPEN")
    P(f"  b3 [{fo}] ambient density (CONDITIONAL, external n_sw, h_z): {frac:.2f} of deep SPARC points lie inside R_HI; n_HI(R_HI) "
      + ", ".join(f"h_z {k_}: {v['n_HI_at_RHI']:.3f} cm^-3" for k_, v in rows.items())
      + f" vs solar wind at Saturn {n_sw_sat:.3f} cm^-3 (h_z must exceed {hz_crit:.0f} pc to escape) -> {b3[fo]['verdict']}")
# b4: curvature
rho, cc, Gs = sp.symbols("rho c G", positive=True)
T_dust = -rho * cc ** 2
R_scalar = -8 * sp.pi * Gs * T_dust / cc ** 4                       # trace of Einstein's equations (4D)
eps_ = sp.symbols("varepsilon", positive=True); kk2 = sp.symbols("k2")
prop = 1 / (kk2 + eps_ * kk2 ** 2)
res0 = sp.residue(prop, kk2, 0); res1 = sp.residue(prop, kk2, -1 / eps_)
ok_M9 = sp.simplify(res0 - 1) == 0 and sp.simplify(res1 + 1) == 0
check("M9", ok_M9, f"R(dust) = {R_scalar}; residues of 1/(k^2 + eps k^4): {res0}, {res1}", "+1 and -1")
tid_sat = GMSUN / (c6["inputs"]["R_Saturn_AU"] * AU) ** 3
tid_gal = float(np.max(gbar[deep] / rS[deep]))
tid_pal = {cl: G_SI * 1.6 * d10["clusters"][cl]["LV"] * MSUN / (d10["clusters"][cl]["rhl"] * PC) ** 3 for cl in ("Pal 4", "Pal 14")}
b4 = dict(R_keyed="R = 8 pi G rho / c^2 for dust: identical to b3", Weyl_keyed="fourth order: Ostrogradsky ghost (residue -1)",
          tidal_Sun_at_Saturn=tid_sat, tidal_SPARC_deep_max=tid_gal, tidal_globulars=tid_pal, verdict="NO-GO (health)")
P(f"  b4 curvature: R-keyed = b3; Weyl-keyed contrast Sun@Saturn {tid_sat:.1e} s^-2 vs SPARC deep max {tid_gal:.1e} (Pal 4/14 "
  f"{tid_pal['Pal 4']:.1e}/{tid_pal['Pal 14']:.1e}) would screen, but the term is fourth order -> Ostrogradsky ghost -> NO-GO")
RES["R2b"] = dict(b1=b1, b2=b2, b3=b3, b4=b4)

# ================================================================================================ R2c: law forms (record numbers)
P("\n=== R2c: capped W / law form / k-mouflage ===")
c1 = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C1_aest_embedding", "c1_aest_embedding_results.json")))
e2 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "E2_field_equation", "e2_field_equation_results.json")))
c1dev = max(rel(v["ratio_to_bound"], v["anomaly"] / v["bound"]) for v in c1["K6"].values())
e2r = e2["R1_outcome"]; e2fam = e2["R3_outcome"]
check("M8", c1dev <= 1e-6 and e2r["canonical_range"][0] > 1 and e2r["alt_range"][0] > 1,
      f"C1 K6 ratio = anomaly/bound (max rel {c1dev:.1e}); E2 AQUAL Q2/Hees canonical {e2r['canonical_range'][0]:.2f}-{e2r['canonical_range'][1]:.2f}, "
      f"alt {e2r['alt_range'][0]:.2f}-{e2r['alt_range'][1]:.2f}; family least-tense {e2fam['least_tense']}", "<= 1e-6; ranges > 1")
RES["R2c"] = dict(C1_planet_ratios={k_: v["ratio_to_bound"] for k_, v in c1["K6"].items()}, E2_Q2_over_Hees=e2r,
                  E2_family=e2fam, T2=T2, verdict="NO-GO")

# ================================================================================================ verdicts
P("\n=== VERDICTS (frozen rules, FROZEN_CRITERIA §2, §4) ===")
r1_nogo = not R1_lin_pass
r1_resid_L1 = not any(phys[fo]["Y0_expansion_physical"] for fo in FOOTS)
V = {}
V["R1"] = ("NO-GO" if r1_nogo else ("WAY THROUGH" if all(R1c[fo]["cassini"] == "PASS" for fo in FOOTS) else "NO-GO")) + \
          (" + residual DEFERRED TO L1" if r1_resid_L1 else "")
r2_cands = {
    "R2a galileons (L3/L4/L5)": "NO-GO" if not any(R2a[fo]["G_pass"] for fo in FOOTS) else "OPEN",
    "R2b1 potential/thin-shell": b1["verdict"],
    "R2b2 body density": "NO-GO" if not any(b2[fo]["G_pass"] for fo in FOOTS) else "OPEN",
    "R2b3 ambient density": b3["canonical"]["verdict"] if b3["canonical"]["verdict"] == b3["alt"]["verdict"] else "OPEN",
    "R2b4 curvature (R = b3; Weyl ghost)": b4["verdict"],
    "R2c law form / capped W / k-mouflage": "NO-GO",
}
V["R2_candidates"] = r2_cands
V["R2"] = "NO-GO" if all(v.startswith("NO-GO") for v in r2_cands.values()) else "OPEN"
V["R3"] = "MOOT (R2 has no way through)" if V["R2"] != "WAY THROUGH" else "TO RUN"
RES["verdicts"] = V
P(f"  R1: {V['R1']}")
for k_, v in r2_cands.items():
    P(f"    {k_}: {v}")
P(f"  R2: {V['R2']}")
P(f"  R3: {V['R3']}")

# ================================================================================================ close
for c_ in (cA, cB):
    c_.struct_cleanup(); c_.empty()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
check("M10", rss < 1.0, f"peak RSS {rss:.3f} GB", "< 1 GB")
RES["checks"] = CHK; RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss
npass = sum(v["ok"] for v in CHK.values()); ntot = len(CHK)
P(f"M1_TRILEMMA COMPLETE: {npass}/{ntot} checks PASS.  ({RES['runtime_s']:.0f} s, peak RSS {rss:.2f} GB)")


def clean(x):
    if isinstance(x, dict):
        return {str(k_): clean(v) for k_, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, sp.Integer):
        return int(x)
    if isinstance(x, sp.Float):
        return float(x)
    if isinstance(x, sp.Basic):
        return str(x)
    return x


json.dump(clean(RES), open(JSONF, "w"), indent=1)
open(OUTF, "w").write("\n".join(LINES) + "\n")
sys.exit(0 if npass == ntot else 1)
