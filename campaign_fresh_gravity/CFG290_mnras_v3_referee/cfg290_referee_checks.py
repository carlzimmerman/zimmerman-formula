#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cfg290_referee_checks.py -- independent re-derivations made by the CFG290 referee of the MNRAS v3 manuscript
(qwen_claude_field_theory/papers_2026/mnras_submission_2026_v3/, commit 32f9a609c).  Written from scratch; it does NOT import
paper_numbers.py, so agreement is a check of the manuscript's arithmetic by separately written code.  Reads only; writes
cfg290_referee_checks_results.json next to itself.  kappa = 1/2 is FITTED; the cold mass is still required.

  R1  abstract length (plain whitespace count, and LaTeX-stripped count)
  R2  RC100 closed-form inversion on the CORRECTED transcription: the slope, (a) with all rows, (b) without RC100's own two
      eq.-8 rows (67, 83: V_c^2 < 3.36 sigma0^2, so V_rot(R_e)^2 < 0), (c) without all 16 flagged rows (the 2 + the 14 with
      V_rot(R_e)/sigma0 < 2.3), and (d) the comparator: what slope the halo-emergent and H(z) laws give when fitted the SAME
      way (OLS of log a0 on z at RC100's own redshifts), against the paper's '0 -> 2.5 mean' slopes it calls 'over this range'
  R3  the design odds: (a) a Monte Carlo check of the closed-form expected ln B (eq. lnB) for N = 4, sigma_m = 0.20; (b) the
      PROBABILITY of actually reaching 20:1, and of evidence pointing the WRONG way, at the paper's '20:1' designs; (c) the same
      odds at the halo-emergent value for the halo mass the gate actually selects (M200 ~ 1e11 Msun, Dutton-Maccio: +0.23 dex)
  R4  the shared-calibration table: a Monte Carlo check of one cell (delta_c = 0.10, N = 4, sigma_m = 0.20, halo law)
  R5  kappa pulls of estimator A under the repository's own H0-convention audit (kappa_h0_convention_audit_2026.py): the
      committed 0.465 is the MIXED convention (SPARC Hubble-flow distances at H0 = 73, rho_Lambda at H0 = 67.4)
  R6  the 'likelihood ratio e^-0.02 from the two together' multiplies two non-independent likelihoods; each one alone
  R7  SPARC Hubble-flow count (the paper's '97'); MIGHTEE-HI digitised colour groups (one colour = one galaxy?)
"""
import os, re, csv, json, math
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)   # spurious Accelerate matmul warnings in multivariate_normal; results match the closed form

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
V3 = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026", "mnras_submission_2026_v3")
OUT = {}
def P(*a): print(*a, flush=True)
def head(s): P(""); P("=" * 100); P(s); P("=" * 100)

# ---------------------------------------------------------------------------------------------------------------- R1
head("R1  ABSTRACT LENGTH")
tex = open(os.path.join(V3, "mnras_a0_lambda_v3.tex")).read()
ab = tex[tex.index(r"\begin{abstract}") + len(r"\begin{abstract}"):tex.index(r"\end{abstract}")].strip()
plain = len(ab.split())
stripped = re.sub(r"\$[^$]*\$", " MATH ", ab)                      # one word per math span
stripped = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", stripped)
nstrip = len(stripped.split())
P(f"  plain whitespace count {plain};  math spans counted as one word {nstrip};  MNRAS limit 250")
OUT["R1"] = dict(plain=plain, math_as_one=nstrip)

# ---------------------------------------------------------------------------------------------------------------- R2
head("R2  RC100 INVERSION: FLAGGED ROWS, AND THE RIGHT COMPARATOR SLOPE")
OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + np.asarray(z, float))**3 + OL)
fN = lambda x: np.log(1 + x) - x / (1 + x)
h = 0.674
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * np.asarray(z, float)**1.21); b = -0.101 + 0.026 * np.asarray(z, float)
    return 10**(a + b * np.log10(M * h / 1e12))
def d_halo(z, M=1e12):
    c0, cz = c_DM14(M, 0.0), c_DM14(M, z)
    return np.log10(E(z)**(4 / 3) * (cz**2 / fN(cz)) / (c0**2 / fN(c0)))
rows = list(csv.DictReader(open(os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv"))))
EQ8 = {"67", "83"}
CUT = {"41", "43", "44", "47", "60", "61", "66", "68", "70", "75", "84", "88", "98", "99"}       # CFG289 posthoc list (CFG287)
# re-derive the two flags from the table itself (paper's eq. 8 at R_e: V_rot^2 = V_c^2 - 3.36 sigma0^2; the cut V_rot/sigma0 >= 2.3)
eq8_re, cut_re = set(), set()
for r in rows:
    vc, s0 = float(r["Vc_Re_kms"]), float(r["sigma0_kms"])
    v2 = vc**2 - 3.36 * s0**2
    if v2 < 0: eq8_re.add(r["idx"])
    elif math.sqrt(v2) / s0 < 2.3: cut_re.add(r["idx"])
P(f"  re-derived from the table: eq.-8 violators {sorted(eq8_re, key=int)};  below the V_rot/sigma0 = 2.3 cut at R_e: {len(cut_re)} rows")
P(f"  agree with CFG287/CFG289's lists: eq8 {eq8_re == EQ8}, cut {cut_re == CUT}")
def inv(drop=set()):
    z, la = [], []
    for r in rows:
        if r["idx"] in drop: continue
        f, g = float(r["fDM_within_Re"]), float(r["g_Re_ms2"])
        if not (0.02 < f < 0.98): continue
        z.append(float(r["z"])); la.append(math.log10((1 - f) * g / math.log(1 / f)**2))
    z, la = np.array(z), np.array(la)
    s = np.polyfit(z, la, 1)[0]
    rng = np.random.default_rng(290)
    bs = np.std([np.polyfit(z[i], la[i], 1)[0] for i in (rng.integers(0, len(z), len(z)) for _ in range(4000))])
    return z, la, float(s), float(bs)
z_all, la_all, s_all, e_all = inv()
res = {}
for tag, drop in (("all", set()), ("no_eq8", EQ8), ("no_16_flagged", EQ8 | CUT)):
    z_, la_, s_, e_ = inv(drop)
    sl_h = float(np.polyfit(z_, d_halo(z_), 1)[0]); sl_H = float(np.polyfit(z_, np.log10(E(z_)), 1)[0])
    res[tag] = dict(N=len(z_), slope=s_, err=e_, sig_const=s_ / e_, halo_ols_slope=sl_h, Hz_ols_slope=sl_H,
                    sig_halo_ols=(sl_h - s_) / e_, sig_Hz_ols=(sl_H - s_) / e_, sig_halo_paper=(0.1311 - s_) / e_, sig_Hz_paper=(0.2304 - s_) / e_)
    P(f"  {tag:14s} N {len(z_):3d}: slope {s_:+.3f} +/- {e_:.3f} (constant {s_/e_:+.1f} sigma);  halo law fitted the same way at these z: {sl_h:+.3f}"
      f" ({(sl_h - s_)/e_:.1f} sigma; with the paper's 0->2.5 mean 0.131: {(0.1311 - s_)/e_:.1f});  H(z) fitted: {sl_H:+.3f} ({(sl_H - s_)/e_:.1f} sigma; paper's 0.230: {(0.2304 - s_)/e_:.1f})")
d06, d25 = float(d_halo(0.6)), float(d_halo(2.5)); H06, H25 = float(np.log10(E(0.6))), float(np.log10(E(2.5)))
P(f"  mean slope over 0.6 < z < 2.5 (end points): halo {(d25 - d06)/1.9:+.3f}, H(z) {(H25 - H06)/1.9:+.3f};  over 0 < z < 2.5: halo {d25/2.5:+.3f}, H(z) {H25/2.5:+.3f}")
OUT["R2"] = dict(flags=dict(eq8=sorted(eq8_re, key=int), n_cut=len(cut_re), match_cfg287=(eq8_re == EQ8 and cut_re == CUT)), fits=res,
                 range_slopes=dict(halo_06_25=(d25 - d06) / 1.9, Hz_06_25=(H25 - H06) / 1.9, halo_0_25=d25 / 2.5, Hz_0_25=H25 / 2.5))

# ---------------------------------------------------------------------------------------------------------------- R3
head("R3  THE DESIGN ODDS: CLOSED FORM vs MONTE CARLO, PROBABILITY OF 20:1, AND THE HALO MASS THE GATE SELECTS")
n_ = lambda y: -(math.sqrt(y) / 2) / math.expm1(math.sqrt(y))
s_int = 0.034 / abs(n_(0.3))                              # the paper's intrinsic term (y = 0.3)
s_h = 0.132                                                # the paper's halo-to-halo term
def lnB_closed(N, sm, mu, sh=s_h):
    s0 = math.hypot(sm, s_int); s1 = math.hypot(s0, sh)
    e0 = N * (math.log(s1 / s0) - 0.5 + (s0**2 + mu**2) / (2 * s1**2)); e1 = N * (math.log(s0 / s1) - 0.5 + (s1**2 + mu**2) / (2 * s0**2))
    return e0, e1
def lnB_mc(N, sm, mu, sh=s_h, sc=0.0, M=200000, seed=7):
    """simulate N galaxies (+ a shared offset sc), compute the exact Gaussian ln B (constant vs halo law); both truths"""
    rng = np.random.default_rng(seed)
    s0v = sm**2 + s_int**2; s1v = s0v + sh**2
    C0 = s0v * np.eye(N) + sc**2 * np.ones((N, N)); C1 = s1v * np.eye(N) + sc**2 * np.ones((N, N))
    i0, i1 = np.linalg.inv(C0), np.linalg.inv(C1); ld0, ld1 = np.linalg.slogdet(C0)[1], np.linalg.slogdet(C1)[1]
    m1 = np.full(N, mu)
    def lnL(x, m, ic, ld): d = x - m; return -0.5 * np.einsum("ij,jk,ik->i", d, ic, d) - 0.5 * ld
    out = {}
    for truth, C, m in (("const", C0, np.zeros(N)), ("halo", C1, m1)):
        x = rng.multivariate_normal(m, C, size=M)
        lb = lnL(x, np.zeros(N), i0, ld0) - lnL(x, m1, i1, ld1)            # ln[L(const)/L(halo)]
        lb = lb if truth == "const" else -lb                                 # evidence FOR the true hypothesis
        out[truth] = dict(mean=float(lb.mean()), p20=float((lb > math.log(20)).mean()), pwrong=float((lb < 0).mean()),
                          p_wrong20=float((lb < -math.log(20)).mean()), median_odds=float(math.exp(np.median(lb))))
    return out
R3 = {}
for N, sm in ((1, 0.13), (2, 0.10), (3, 0.13), (4, 0.20)):
    cf = lnB_closed(N, sm, 0.328); mc = lnB_mc(N, sm, 0.328)
    R3[f"N{N}_s{sm}"] = dict(closed=cf, mc=mc)
    P(f"  N = {N}, sigma_m = {sm:.2f}, Delta = 0.328: closed-form <ln B> = {cf[0]:.3f} / {cf[1]:.3f};  MC {mc['const']['mean']:.3f} / {mc['halo']['mean']:.3f}"
      f"  (table odds {math.exp(min(cf)):.1f}:1).  P(reach 20:1) = {mc['const']['p20']:.2f} (const true) / {mc['halo']['p20']:.2f} (halo true);"
      f"  P(evidence the WRONG way) = {mc['const']['pwrong']:.2f} / {mc['halo']['pwrong']:.2f};  P(20:1 the wrong way) = {mc['const']['p_wrong20']:.3f} / {mc['halo']['p_wrong20']:.3f}")
# the idealised single-pair rule sigma = Delta/2.45: ln B ~ N(m, 2m) with m = ln 20
m = math.log(20); from math import erf
Phi = lambda x: 0.5 * (1 + erf(x / math.sqrt(2)))
P(f"  the idealised rule sigma = Delta/sqrt(2 ln 20): ln B ~ N({m:.2f}, {math.sqrt(2*m):.2f}^2):  P(ln B > ln 20) = {1 - Phi(0):.2f};  P(ln B < 0) = {Phi(-m/math.sqrt(2*m)):.3f}")
# the gate selects M_b ~ 2e9-1e10 at z ~ 2.5, i.e. M200 ~ 1e11 Msun: the Dutton-Maccio halo law there
d11 = float(d_halo(2.5, M=1e11)); d3e11 = float(d_halo(2.5, M=3e11))
P(f"  halo-emergent Delta at z = 2.5: M200 = 1e11 -> {d11:+.3f};  3e11 -> {d3e11:+.3f};  1e12 (the paper's decision value) -> {float(d_halo(2.5)):+.3f}")
for N, sm in ((2, 0.10), (3, 0.13), (4, 0.20), (6, 0.20), (8, 0.20)):
    o11 = math.exp(min(lnB_closed(N, sm, d11))); o12 = math.exp(min(lnB_closed(N, sm, 0.328)))
    R3[f"M1e11_N{N}_s{sm}"] = dict(odds_1e11=o11, odds_1e12=o12)
    P(f"     N = {N}, sigma_m = {sm:.2f}: odds {o12:7.1f}:1 at Delta = 0.328  ->  {o11:6.1f}:1 at Delta = {d11:.3f}")
OUT["R3"] = R3; OUT["R3"]["ideal_rule"] = dict(p_reach=0.5, p_wrong=Phi(-m / math.sqrt(2 * m))); OUT["R3"]["delta_1e11"] = d11; OUT["R3"]["delta_3e11"] = d3e11

# ---------------------------------------------------------------------------------------------------------------- R4
head("R4  SHARED-CALIBRATION CELL BY MONTE CARLO (delta_c = 0.10, N = 4, sigma_m = 0.20, halo law)")
Abar = 1 / abs(n_(0.2)) - 1
mc4 = lnB_mc(4, 0.20, 0.328, sc=Abar * 0.10)
P(f"  A_bar(0.2) = {Abar:.3f};  MC <ln B> = {mc4['const']['mean']:.3f} / {mc4['halo']['mean']:.3f} -> odds {math.exp(min(mc4['const']['mean'], mc4['halo']['mean'])):.2f}:1 (Table 10: 4.2:1);"
      f"  P(reach 20:1) {mc4['const']['p20']:.2f} / {mc4['halo']['p20']:.2f}")
OUT["R4"] = mc4

# ---------------------------------------------------------------------------------------------------------------- R5
head("R5  ESTIMATOR A UNDER THE REPOSITORY'S OWN H0-CONVENTION AUDIT")
A_conv = {"committed MIXED (D_HF at H0 = 73, rho_Lambda at 67.4)": (0.465, 0.076), "R1 Planck-consistent (OPERATIVE in the audit)": (0.450, 0.074),
          "R2a H0 = 73, Omega_L fixed": (0.430, 0.070), "R2b H0 = 73, omega_m fixed": (0.416, 0.068)}
k_hor = math.sqrt(8 * math.pi / 3) / (2 * math.pi)
R5 = {}
for k, (v, s) in A_conv.items():
    R5[k] = dict(kappa=v, err=s, pull_half=(0.5 - v) / s, pull_2pi=(k_hor - v) / s)
    P(f"  {k:55s} kappa = {v:.3f} +/- {s:.3f}: 1/2 at {(0.5 - v)/s:+.2f} sigma, cH_Lambda/2pi at {(k_hor - v)/s:+.2f} sigma")
P("  Fig. 2(b) grey bar for A is hard-coded [0.450, 0.465] (R1..MIXED); the audit's full box is [0.416, 0.465]. For B the bar is [0.492, 0.589] (R2b..R1).")
OUT["R5"] = R5

# ---------------------------------------------------------------------------------------------------------------- R6
head("R6  THE LIKELIHOOD RATIO BETWEEN 1/2 AND 0.461")
MEAS = [("A", 0.465, 0.076), ("B", 0.547, 0.175)]
lr = {nm: -0.5 * ((0.5 - k) / s)**2 + 0.5 * ((k_hor - k) / s)**2 for nm, k, s in MEAS}
P(f"  ln LR(1/2 : 0.461): A alone {lr['A']:+.3f}; B alone {lr['B']:+.3f}; summed (treats A and B as independent) {lr['A'] + lr['B']:+.3f}")
OUT["R6"] = lr

# ---------------------------------------------------------------------------------------------------------------- R7
head("R7  SPARC HUBBLE-FLOW COUNT; MIGHTEE-HI COLOUR GROUPS")
nhf = 0          # whitespace parse: the MRT data rows are wider than the header's byte layout (CFG287 S01b), so byte slicing fails
for ln in open(os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p_ = ln.split()
    if len(p_) > 18 and p_[0][0].isalpha() and p_[1].isdigit() and p_[4].isdigit() and int(p_[4]) == 1: nhf += 1
P(f"  SPARC galaxies with f_D = 1 (Hubble flow, H0 = 73 assumed by SPARC): {nhf}")
mrows = list(csv.DictReader(open(os.path.join(ROOT, "deepseek_push", "data2", "mightee2025_rar_digitized_points.csv"))))
groups = {}
for r in mrows: groups.setdefault((r["color_r"], r["color_g"], r["color_b"]), []).append(float(r["log10_gbar"]))
sizes = sorted(len(v) for v in groups.values())
P(f"  MIGHTEE-HI digitised: {len(mrows)} points in {len(groups)} colour groups (the survey has 19 galaxies); group sizes {sizes}")
win = math.log10(0.2 * 9.3624e-11)
big = sorted(((len(v), sum(1 for x in v if x < win), max(v) - min(v)) for v in groups.values()), reverse=True)[:3]
P(f"  the three largest groups (points, points in the window, log g_bar span): {big}")
OUT["R7"] = dict(sparc_hubble_flow=nhf, mightee_groups=len(groups), mightee_sizes=sizes)

# ---------------------------------------------------------------------------------------------------------------- R8
head("R8  THE HALO MASS OF A GATE-PASSING DISC AT z = 2.5, AND DESMOND (2023)'s a0 ON THE PAPER'S TWO FOOTINGS")
G_, MSUN_, MPC_ = 6.6743e-11, 1.98847e30, 3.0856775814913673e22
Hz25 = 67.4e3 / MPC_ * float(E(2.5))
R8 = {}
for Vf in (85.0, 106.0, 130.0):
    for vratio in (1.0, 1.2):                    # V_f / V_200 between 1 and 1.2 (an NFW V_max/V_200 for c ~ 4 is ~1.1)
        V200 = Vf * 1e3 / vratio; M200 = V200**3 / (10 * G_ * Hz25) / MSUN_
        R8[f"Vf{Vf:.0f}_r{vratio}"] = dict(M200=M200, delta_halo=float(d_halo(2.5, M=M200)))
        P(f"  V_f = {Vf:5.1f} km/s, V_f/V_200 = {vratio}: M200(z = 2.5) = {M200:.2e} Msun -> Dutton-Maccio halo law +{float(d_halo(2.5, M=M200)):.3f} dex")
A_L = 2.99792458e8 * math.sqrt(G_ * 0.685 * 3 * (67.4e3 / MPC_)**2 / (8 * math.pi * G_)); A_C = A_L / math.sqrt(0.685)
a_d, s_d = 1.19e-10, math.hypot(0.04e-10, 0.09e-10)               # Desmond (2023), stat and sys in quadrature
kL, sL = a_d / A_L, s_d / A_L
P(f"  Desmond (2023) a0 = (1.19 +/- 0.04 +/- 0.09)e-10 -> kappa_Lambda = {kL:.3f} +/- {sL:.3f}: 1/2 at {(kL - 0.5)/sL:.1f} sigma, 0.461 at {(kL - k_hor)/sL:.1f} sigma,"
  f" cH0/2pi (0.557) at {(kL - k_hor/math.sqrt(0.685))/sL:.1f} sigma, 1/2 on rho_crit (kappa_Lambda {0.5*A_C/A_L:.3f}) at {(kL - 0.5*A_C/A_L)/sL:.1f} sigma")
R8["desmond2023"] = dict(kappa_L=kL, err=sL, pull_half=(kL - 0.5) / sL, pull_2pi=(kL - k_hor) / sL)
OUT["R8"] = R8

# ---------------------------------------------------------------------------------------------------------------- R9
head("R9  ESTIMATOR B AND THE STANDARD FIT WHEN SPARC'S HUBBLE-FLOW DISTANCES ARE PUT ON THE PLANCK H0 (the audit's R1)")
# SPARC's f_D = 1 distances assume H0 = 73 (MRT note 2); rho_Lambda uses 67.4.  R1: D_HF x 73/67.4, i.e. g_obs of those galaxies / 1.0831
# (g_bar = V_bar^2/R is distance-free for one galaxy).  Independent re-implementation of the paper's two fits (quality cut 10%, +0.034 dex).
from scipy.optimize import minimize_scalar
import glob
fD = {}
for ln in open(os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p_ = ln.split()
    if len(p_) > 18 and p_[0][0].isalpha() and p_[1].isdigit() and p_[4].isdigit(): fD[p_[0]] = int(p_[4])
Kc = 1e6 / (3.0856775814913673e19)
nu_ = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def load(UD, UB, hf_scale=1.0):
    gb, go, ew, gi = [], [], [], []
    for k_, f in enumerate(sorted(glob.glob(os.path.join(ROOT, "real_research", "data", "sparc_data", "*_rotmod.dat")))):
        d = np.genfromtxt(f, comments="#")
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < 0.10); R, V, eV, Vg, Vd, Vb = R[m], V[m], eV[m], Vg[m], Vd[m], Vb[m]
        v2 = np.sign(Vg) * Vg**2 + UD * Vd**2 + UB * Vb**2; ok = v2 > 0
        if ok.sum() == 0: continue
        sc = hf_scale if fD.get(os.path.basename(f).replace("_rotmod.dat", "")) == 1 else 1.0
        gb.append(v2[ok] / R[ok] * Kc); go.append(V[ok]**2 / R[ok] * Kc / sc); ew.append(2 * eV[ok] / V[ok] / math.log(10))
    return np.concatenate(gb), np.concatenate(go), np.concatenate(ew)
def fit_std(gb, go, ew):
    s2 = ew**2 + 0.034**2
    return 10**minimize_scalar(lambda la: np.sum((np.log10(go) - np.log10(gb * nu_(gb / 10**la)))**2 / s2), bounds=(-10.6, -9.4), method="bounded", options=dict(xatol=1e-7)).x
def fit_shape(gb, go, ew):
    w = 1 / (ew**2 + 0.034**2)
    def prof(la):
        r = np.log10(go) - np.log10(gb * nu_(gb / 10**la)); C = np.sum(w * r) / np.sum(w); return np.sum(w * (r - C)**2)
    return 10**minimize_scalar(prof, bounds=(-10.8, -9.2), method="bounded", options=dict(xatol=1e-7)).x
R9 = {}
for lab, sc in (("as tabulated (MIXED)", 1.0), ("R1: HF distances x 73/67.4", 73.0 / 67.4)):
    g1, g2, e1 = load(0.6, 0.7, sc); kB_ = fit_shape(g1, g2, e1) / A_L
    g1, g2, e1 = load(0.5, 0.7, sc); kS_ = fit_std(g1, g2, e1) / A_L
    R9[lab] = dict(kappa_B_06_07=kB_, kappa_std_05_07=kS_)
    P(f"  {lab:28s}: estimator B (Ups 0.6/0.7) kappa = {kB_:.3f};  standard fit (Ups 0.5/0.7) kappa = {kS_:.3f}")
from scipy.optimize import brentq
for lab, sc in (("as tabulated (MIXED)", 1.0), ("R1: HF distances x 73/67.4", 73.0 / 67.4)):
    ud = brentq(lambda u: fit_std(*load(u, 0.7, sc)) / A_L - 0.5, 0.40, 0.85, xtol=1e-3)
    R9[lab]["Ups_disc_for_half_std"] = ud
    P(f"  {lab:28s}: the standard fit gives kappa = 1/2 at Upsilon_disc = {ud:.3f} (bulge 0.7)")
OUT["R9"] = R9

json.dump(OUT, open(os.path.join(HERE, "cfg290_referee_checks_results.json"), "w"), indent=1, default=float)
P("\nwrote cfg290_referee_checks_results.json")
