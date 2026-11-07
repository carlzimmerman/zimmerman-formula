#!/usr/bin/env python3
"""QX31 (FROZEN_CRITERIA.md, 99e2469342): do LCDM assumptions inside the data products make the growth / CMB-lensing failures?
Re-grades with the record's machinery read only:
  A  WG2-WG6 law-alone CMB-lensing SHAPE (wg6_shape_diag cases + 2 alt-footing runs), projection copied unchanged from WG6/WG2
  B  QX3 iter2 G2 mu_min at the G1 worst corner        C  QX3 iter3 closest member        D  QX27 G6b closest graded row
  E  record-sized items (QX15 foreground freedom, EB1b, KiDS shift statistic, forest line)
Variants: V0 record rule (CMB-marged W X + M X - F); V1 W X only; V2 full PS1 linear correction at FFP10 lensed CMB;
bounds V3 (most generous model covariance), V4 (+5 % per-bin diagonal), V5 (V3 + V4).
  python3 qx31.py            -> qx31.json / qx31.out
  python3 qx31.py --mutate   -> qx31_MUTATE.json / .out  (twin: every variant replaced by V0; must reproduce the record, all shifts 0)
kappa = 1/2 FITTED; not theory closed.  1 thread."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import warnings; warnings.filterwarnings("ignore", category=RuntimeWarning)   # Accelerate matmul flags; values checked finite
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../.."))
REB = os.path.join(REPO, "rebuild_2026_10_22")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))

# ====================================================================== likelihood products
D = LB.load_pr4()                                         # CMB-marged: d, W, M (PP), F, C
S = LB.STEM
def _win5(fn):
    w = np.loadtxt(fn, ndmin=2); out = np.zeros((4, LB.LMAX + 1))
    for row in w:
        L = int(row[0])
        if 2 <= L <= LB.LMAX: out[:, L] = row[1:5]
    return out
MW = np.array([_win5(os.path.join(LB.PR4D, S + f"_lens_delta_window/window{b}.dat")) for b in range(1, 10)])   # (9, 4[TT EE TE PP], L)
F_PS1 = np.loadtxt(os.path.join(LB.PR4D, S + "_lensing_fiducial_correction.dat"))[:, 1]
C_PS1 = np.loadtxt(os.path.join(LB.PR4D, S + "_cov.dat"))
t = np.loadtxt(os.path.join(LB.PR4D, "FFP10_wdipole_lensedCls.dat"))
CMB = np.zeros((3, LB.LMAX + 1)); Lt = t[:, 0].astype(int); m = Lt <= LB.LMAX
CMB[0, Lt[m]] = t[m, 1]; CMB[1, Lt[m]] = t[m, 2]; CMB[2, Lt[m]] = t[m, 4]    # TT, EE, TE (D_ell, muK^2)
XF = LB.load_ffp10()
CMBTERM = sum(LB.wsum(MW[:, i, :], CMB[i]) for i in range(3))                # sum_XY M^XY C^XY_FFP10, per bin
d = D["d"]; Cm = D["C"]; n = D["n"]
LINE_A = float(CHI2.ppf(0.99, 8))

def parts(X, V):
    """B(A) = A u + c and the base covariance for variant V."""
    if MUT or V in ("V0", "V3", "V4", "V5"):
        u = LB.wsum(D["W"], X) + LB.wsum(D["M"], X); c = -D["F"]; C = Cm
    elif V == "V1":
        u = LB.wsum(D["W"], X); c = np.zeros(n); C = Cm
    elif V == "V2":
        u = LB.wsum(D["W"], X) + LB.wsum(MW[:, 3, :], X); c = CMBTERM - F_PS1; C = C_PS1
    if not MUT and V in ("V4", "V5"):
        C = C + np.diag((0.05 * d) ** 2)
    return u, c, C

def chi2_fixedcov(u, c, C, A=None):
    Ci = np.linalg.inv(C)
    if A is None:
        A = LB.qform(u, Ci, d - c) / LB.qform(u, Ci)
    r = A * u + c - d; return LB.qform(r, Ci), A

def chi2_modelcov(u, c, C, A):
    B = A * u + c; s = np.maximum(1.0, B / d); Cs = C * np.outer(s, s)
    r = B - d; return LB.qform(r, np.linalg.inv(Cs))

def shape_chi2(X, V):
    """shape chi^2 after best amplitude (A >= 0) for variant V; returns (chi2, A)."""
    u, c, C = parts(X, V)
    c0, A0 = chi2_fixedcov(u, c, C)
    if MUT or V not in ("V3", "V5"):
        return c0, A0
    f = lambda la: chi2_modelcov(u, c, C, math.exp(la))
    grid = np.linspace(math.log(A0) - 8, math.log(A0) + 8, 321); vals = [f(x) for x in grid]; j = int(np.argmin(vals))
    r = minimize_scalar(f, bounds=(grid[max(j - 1, 0)], grid[min(j + 1, len(grid) - 1)]), method="bounded", options={"xatol": 1e-6})
    return float(min(r.fun, vals[j])), float(math.exp(r.x if r.fun <= vals[j] else grid[j]))

VARS = ["V0", "V1", "V2", "V3", "V4", "V5"]
ADM = ["V1", "V2"]
RES = dict(lane="QX31", criteria="99e2469342", mode="MUTATE twin (all variants = V0)" if MUT else "main", line_A=LINE_A,
           note="kappa = 1/2 FITTED; not theory closed")
P(f"QX31 {'MUTATE twin' if MUT else 'main'}: data-product assumptions vs the growth / CMB-lensing failures. kappa = 1/2 FITTED; not theory closed.")

# ====================================================================== checks K1, K2, K3
k1m = LB.pr4_chi2(D, XF)
B_ps1_fid = LB.wsum(D["W"], XF) + LB.wsum(MW[:, 3, :], XF) + CMBTERM - F_PS1
k1p = LB.qform(B_ps1_fid - d, np.linalg.inv(C_PS1))
k2 = float(np.max(np.abs((CMBTERM + LB.wsum(MW[:, 3, :], XF)) / F_PS1 - 1)))
RES["K1"] = dict(marged_ffp10=k1m, marged_ref=8.3724, ps1_ffp10=k1p, ps1_ref=8.7094,
                 pass_=bool(abs(k1m - 8.3724) <= 0.01 and abs(k1p - 8.7094) <= 0.01))
RES["K2"] = dict(max_rel_dev=k2, pass_=bool(k2 <= 1e-3))
P(f"K1 package unit tests: CMB-marged FFP10 chi2 {k1m:.4f} (CFG917 8.3724), PS1 FFP10 {k1p:.4f} (CFG917 8.7094) -> {'PASS' if RES['K1']['pass_'] else 'FAIL'}")
# Amendment A1 (post-result, disclosed): the frozen K1 references are CFG917's package unit tests at the package's own test
# cosmology, not FFP10 through this rule.  K1' compares with the record's FFP10-through-rule value (QX3 iter2 K1, iter2.json).
_k1rec = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust", "iter2.json")))["K1_ffp10_chi2"]
RES["K1prime_A1"] = dict(marged_ffp10=k1m, record_iter2_K1=_k1rec, pass_=bool(abs(k1m - _k1rec) <= 1e-6))
P(f"K1' (A1): CMB-marged FFP10 chi2 {k1m:.6f} vs record QX3 iter2 K1 {_k1rec:.6f} -> {'PASS' if RES['K1prime_A1']['pass_'] else 'FAIL'} (PS1 at FFP10 {k1p:.4f}: no record value, reported)")
P(f"K2 F_PS1 = sum M^XY C^XY_FFP10 + M^PP X_FFP10: max rel dev {k2:.2e} (line 1e-3) -> {'PASS' if RES['K2']['pass_'] else 'FAIL'}")
P(f"   size of the corrections at FFP10 (bandpower units, per bin / data): marged F/d {np.round(D['F'] / d, 4).tolist()}")
P(f"   PS1 CMB-spectrum part sum M^XY C^XY / d {np.round(CMBTERM / d, 2).tolist()} (cancels against F_PS1 at the fiducial)")

# ====================================================================== Part A: WG law-alone shapes (projection copied from WG6 shape diag)
sys.path.insert(0, os.path.join(REB, "WG6_screened_phantom_web")); import wg6_pm; PM = wg6_pm.B          # read only (as wg6_shape_diag)
H = PM.H; CH = 2997.92458 / H; ZS = 1090.0
LS = np.arange(8, LB.LMAX + 1); L4 = (LS * (LS + 1.0)) ** 2 / (2 * math.pi)
def geom(bg):                                                       # wg6_shape_diag.py, unchanged
    E, _ = PM.background(bg)
    z = np.concatenate([np.linspace(0.0, 10.0, 8001), np.geomspace(10.0, ZS, 4001)[1:]])
    f = CH / np.array([E(1 / (1 + zz)) for zz in z])
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(z))]); chis = float(chi[-1])
    cg = np.concatenate([np.geomspace(1e-3, 100.0, 160), np.linspace(100.0, chis, 700)[1:]])
    w = np.zeros_like(cg); w[1:] += 0.5 * np.diff(cg); w[:-1] += 0.5 * np.diff(cg)
    q = 2.0 * (chis - cg) / (cg * chis)
    return dict(cg=cg, zg=np.interp(cg, chi, z), ker=w * q ** 2 / cg ** 2, chis=chis)
GEO = {bg: geom(bg) for bg in ("B2", "B2D")}
def snap_tables(run):                                               # unchanged
    kny = math.pi * run["N"] / run["L"] * H; kcut = 0.5 * kny; tabs = []
    for s in sorted(run["snaps"], key=lambda s: s["z"]):
        k = np.array(s["k"]) * H; Pp = np.array(s["P_psi"]) / H ** 3
        d2 = k ** 3 * Pp / (2 * math.pi ** 2); mm = (k <= kcut) & (d2 > 0)
        lk, ld = np.log(k[mm]), np.log(d2[mm])
        hi = (k[mm] >= kcut / 2)
        slope = float(np.polyfit(lk[hi], ld[hi], 1)[0]) if hi.sum() >= 3 else -4.0
        tabs.append(dict(z=s["z"], lk=lk, ld=ld, slope=slope))
    return tabs, kcut
def logd2(t_, lkq):                                                 # unchanged (zero_beyond False)
    lk, ld = t_["lk"], t_["ld"]; out = np.interp(lkq, lk, ld); hi = lkq > lk[-1]
    return np.where(hi, ld[-1] + t_["slope"] * (lkq - lk[-1]), out)
def project(run):                                                   # unchanged (zero_beyond False)
    g = GEO[run["bg"]]; tabs, kcut = snap_tables(run)
    zs = np.array([t_["z"] for t_ in tabs]); lz = np.log1p(zs); C = np.zeros(len(LS))
    for chi, z, kw in zip(g["cg"], g["zg"], g["ker"]):
        k = (LS + 0.5) / chi; lkq = np.log(k)
        if z >= zs[-1]:
            i0 = i1 = len(tabs) - 1; tt = 0.0
        else:
            i1 = int(np.searchsorted(zs, z)); i0 = max(i1 - 1, 0); tt = 0.0 if i1 == i0 else (math.log1p(z) - lz[i0]) / (lz[i1] - lz[i0])
        ld = (1 - tt) * logd2(tabs[i0], lkq) + tt * logd2(tabs[i1], lkq)
        C += kw * 2 * math.pi ** 2 * np.exp(ld) / k ** 3
    X = np.zeros(LB.LMAX + 1); X[LS] = L4 * C; return X

CASES = [("WG2 R0 law off, B2, A_s 1e-9, 128^3", "WG2_bare_law_web_lensing/runs/R0_TIE_B2_As1e-09_N128_s200_zon50_canonical.json", 1308, "canonical"),
         ("WG2 R1 a0 flat, B2, A_s 2.1e-9, 128^3", "WG2_bare_law_web_lensing/runs/R1_TIE_B2_As2.1e-09_N128_s200_zon50_canonical.json", 1574, "canonical"),
         ("WG2 R1 a0 flat, B2, A_s 2.1e-9, 192^3", "WG2_bare_law_web_lensing/runs/R1_TIE_B2_As2.1e-09_N192_s200_zon50_canonical.json", 1582, "canonical"),
         ("WG3 T1tau0, B2, A_s 1e-9, 128^3", "WG3_bound_only_web_rule/runs/T1T0_TIE_B2_As1e-09_N128_s200_zon50_canonical.json", 1572, "canonical"),
         ("WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 128^3", "WG4_a0_tracks_de_web/runs/R1_DE_B2D_As2.1e-09_N128_s200_zon50_canonical.json", 1589, "canonical"),
         ("WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 192^3", "WG4_a0_tracks_de_web/runs/R1_DE_B2D_As2.1e-09_N192_s200_zon50_canonical.json", 1594, "canonical"),
         ("WG6 screened 100 Mpc, B2D, A_s 1e-9, 128^3", "WG6_screened_phantom_web/runs/R1Y0.01_DE_B2D_As1e-09_N128_s200_zon50_canonical.json", 261, "canonical"),
         ("WG6 screened 33 Mpc, B2D, A_s 2.1e-9, 128^3", "WG6_screened_phantom_web/runs/R1Y0.03_DE_B2D_As2.1e-09_N128_s200_zon50_canonical.json", 126, "canonical"),
         ("WG6 screened 33 Mpc, B2D, A_s 2.1e-9, 192^3", "WG6_screened_phantom_web/runs/R1Y0.03_DE_B2D_As2.1e-09_N192_s200_zon50_canonical.json", 137, "canonical"),
         ("WG2 R1 a0 flat, B2, A_s 2.1e-9, 128^3 [alt]", "WG2_bare_law_web_lensing/runs/R1_TIE_B2_As2.1e-09_N128_s200_zon50_alt.json", None, "alt"),
         ("WG4 R1 a0 tracks rho_DE, B2D, A_s 2.1e-9, 128^3 [alt]", "WG4_a0_tracks_de_web/runs/R1_DE_B2D_As2.1e-09_N128_s200_zon50_alt.json", None, "alt")]
# record per-bin (plain W) values from wg6_shape_diag.out for the reproduce check
REC_BINS = {}
for line in open(os.path.join(REB, "WG6_screened_phantom_web", "wg6_shape_diag.out")):
    for nm, _, _, _ in CASES:
        if line.strip().startswith(nm + " ") and "|" in line:
            REC_BINS[nm] = [float(x) for x in line.split("|")[0][len("  " + nm):].split()]

def label(S_rec, S_line, S_adm):
    gap = S_rec - S_line
    if any(s <= S_line for s in S_adm): return "ARTEFACT"
    mv = max(abs(s - S_rec) for s in S_adm)
    return "PARTIAL" if mv >= 0.25 * gap else "ROBUST"

P(""); P(f"== A. CMB-lensing SHAPE, law alone (shape chi2 after best amplitude, 8 dof; line {LINE_A:.2f})")
P("   case | footing | " + " | ".join(VARS) + " | bin1/bin9 model/data (V0, V1, V2) | label")
RES["A"] = []; okA = True
for nm, f, srec, foot in CASES:
    run = json.load(open(os.path.join(REB, f))); X = project(run)
    plain = LB.wsum(D["W"], X) / d
    rep_bins = (nm not in REC_BINS) or bool(np.all(np.abs(plain / np.array(REC_BINS[nm]) - 1) <= 5e-3))
    Sv = {V: shape_chi2(X, V) for V in VARS}
    rep_S = (srec is None) or abs(Sv["V0"][0] - srec) <= 1.0
    okA = okA and rep_bins and rep_S
    ends = {V: (parts(X, V)[0] + parts(X, V)[1]) / d for V in ("V0", "V1", "V2")}
    s_rec = Sv["V0"][0]
    lab = label(s_rec, LINE_A, [Sv[V][0] for V in ADM])
    bnd = [V for V in ("V3", "V4", "V5") if Sv[V][0] <= LINE_A]
    lab_full = lab + ("" if not bnd else f", NOT ROBUST to bound {'/'.join(bnd)}") if lab == "ROBUST" else lab
    vmax = max(ADM, key=lambda V: abs(Sv[V][0] - s_rec)); worse = Sv[vmax][0] > s_rec
    toward = max([s_rec - Sv[V][0] for V in ADM] + [0.0]) / (s_rec - LINE_A)
    if lab == "PARTIAL": lab_full = f"PARTIAL as frozen ({vmax} {'WORSENS' if worse else 'eases'} the failure); largest move toward a pass {toward:.3f} of gap"
    row = dict(case=nm, footing=foot, file=f, record_shape_chi2=srec, reproduce_bins=rep_bins, reproduce_S=rep_S,
               S={V: Sv[V][0] for V in VARS}, A={V: Sv[V][1] for V in VARS},
               bin1_over_data={V: float(ends[V][0]) for V in ends}, bin9_over_data={V: float(ends[V][-1]) for V in ends},
               gap=s_rec - LINE_A, toward_pass_frac=max([s_rec - Sv[V][0] for V in ADM] + [0.0]) / (s_rec - LINE_A), max_admissible_move=max(abs(Sv[V][0] - s_rec) for V in ADM),
               move_frac_of_gap=max(abs(Sv[V][0] - s_rec) for V in ADM) / (s_rec - LINE_A), label=lab_full)
    RES["A"].append(row)
    P(f"   {nm:<52} | {foot:<9} | " + " | ".join(f"{Sv[V][0]:8.1f}" for V in VARS)
      + f" | {ends['V0'][0]:.3g}/{ends['V0'][-1]:.3g}, {ends['V1'][0]:.3g}/{ends['V1'][-1]:.3g}, {ends['V2'][0]:.3g}/{ends['V2'][-1]:.3g}"
      + f" | move {row['move_frac_of_gap']:.3f} of gap -> {lab_full}" + ("" if (rep_bins and rep_S) else "  [REPRODUCE MISS]"))
RES["A_reproduce_pass"] = okA
P(f"   MUTATE-twin reproduce of wg6_shape_diag (per bin 5e-3, shape chi2 within 1): {'PASS' if okA else 'FAIL'}")

# K3 (bite): the pipeline sees the correction terms: scale the phi-phi windows x10 on the WG2 R1 128^3 case
run = json.load(open(os.path.join(REB, CASES[1][1]))); X = project(run)
u0 = LB.wsum(D["W"], X); M10 = 10 * LB.wsum(D["M"], X)
c_b, _ = chi2_fixedcov(u0 + M10, -10 * D["F"], Cm); c_0, _ = chi2_fixedcov(u0 + LB.wsum(D["M"], X), -D["F"], Cm); c_1, _ = chi2_fixedcov(u0, np.zeros(n), Cm)
RES["K3_bite"] = dict(V0=c_0, V1=c_1, M_x10=c_b, dist_V0_V1=abs(c_0 - c_1), dist_x10=abs(c_b - c_1),
                      bites=bool(abs(c_b - c_1) >= 5 * max(abs(c_0 - c_1), 1e-6)))
P(f"K3 bite (M x10 on WG2 R1 128^3): |S - S_V1| {abs(c_0 - c_1):.1f} -> {abs(c_b - c_1):.1f} -> {'BITES' if RES['K3_bite']['bites'] else 'DOES NOT BITE'}")

# ====================================================================== Parts B-D: QX3 iter2 / iter3 / QX27 growth Delta chi^2 (CLASS)
I2DIR = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust"); sys.path.insert(0, I2DIR)
import iter2 as I2                                                  # read only (main guarded)
it2 = json.load(open(os.path.join(I2DIR, "iter2.json")))
worst = max(it2["G1"], key=lambda r: r["chi2_min"])
ob, od, H0, ns = worst["omega_b"], worst["omega_d_best"], worst["H0"], worst["n_s"]; h = H0 / 100
Mc = I2.run_class(ob, od, H0, ns, pk=True); X0 = I2.X_of(Mc)
kgrid = np.logspace(-4, 1, 70); zgrid = np.linspace(0.02, I2.ZPK, 120)
lna_t = np.linspace(math.log(1 / 3500.0), 0.0, 4000)
lnH_t = np.array([math.log(Mc.Hubble(1 / math.exp(x) - 1)) for x in lna_t]); dlnH_t = np.gradient(lnH_t, lna_t)
H0c = Mc.Hubble(0.0); Om_b0 = ob / h ** 2; Om_d0 = od / h ** 2; ai = 1 / 3401.0; adec = 1 / 1091.0
lnz = np.log(1 / (1 + zgrid)); nk = len(kgrid)
def solve(jeansfn):
    """iter3's / QX27's implicit-midpoint solver, copied unchanged; jeansfn(a) -> (k/(a k_J))^2 array or 0."""
    grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 6001), lnz]))
    y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai
    rec = {}; tset = {float(x): i for i, x in enumerate(lnz)}; I4 = np.eye(4)[None, :, :]
    for k_ in range(len(grid) - 1):
        hh = grid[k_ + 1] - grid[k_]; lna = 0.5 * (grid[k_] + grid[k_ + 1]); a = math.exp(lna)
        E2 = math.exp(2 * np.interp(lna, lna_t, lnH_t)) / H0c ** 2; dl = float(np.interp(lna, lna_t, dlnH_t))
        Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; on = a > adec
        jeans = jeansfn(a)
        A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Od * (1 - jeans); A[:, 1, 1] = -(2 + dl)
        if on:
            A[:, 1, 2] = 1.5 * Ob; A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Od; A[:, 3, 2] = 1.5 * Ob; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * hh * A, ((I4 + 0.5 * hh * A) @ y[:, :, None]))[:, :, 0]
        tt = float(grid[k_ + 1])
        if tt in tset: rec[tset[tt]] = y.copy()
    dm = np.empty((nk, len(zgrid)))
    for jz in range(len(zgrid)):
        yy = rec[jz]; a = 1 / (1 + zgrid[jz]); E2 = math.exp(2 * np.interp(math.log(a), lna_t, lnH_t)) / H0c ** 2
        Od = Om_d0 * a ** -3 / E2; Ob = Om_b0 * a ** -3 / E2; dm[:, jz] = (Od * yy[:, 0] + Ob * yy[:, 2]) / (Od + Ob)
    return dm
REF = solve(lambda a: 0.0)
S0V = {V: shape_chi2(X0, V)[0] for V in VARS}
def dchi2_all(jeansfn):
    R = solve(jeansfn) / REF; Sl = I2.limber_ratio(Mc, H0, kgrid, zgrid, R); Xs = X0 * Sl
    return {V: shape_chi2(Xs, V)[0] - S0V[V] for V in VARS}
P(""); P(f"== B-D. growth Delta chi^2 at the iter2 G1 worst corner (omega_b {ob}, omega_d {od:.4f}, H0 {H0}, n_s {ns}); "
         f"reference chi2 per variant " + ", ".join(f"{V} {S0V[V]:.2f}" for V in VARS))
# B: iter2 mu grid (beta = 0, k_J = mu)
mus = np.logspace(0, 5, 26); rec_rows = [g for g in it2["G2"] if g["corner"] == [ob, H0, ns]][0]["rows"]
rowsB = []; okB = True
for mu, rr in zip(mus, rec_rows):
    dv = dchi2_all(lambda a, mu=mu: (kgrid / (a * mu)) ** 2); rowsB.append(dict(mu=float(mu), record=rr["dchi2"], **dv))
    okB = okB and abs(dv["V0"] - rr["dchi2"]) <= 0.05 + 1e-3 * abs(rr["dchi2"])
def mu_min_of(V):
    for i in range(len(rowsB)):
        if all(x[V] <= I2.DCHI2_LINE for x in rowsB[i:]): return rowsB[i]["mu"]
    return None
MUMAX = 79.43282347242821
mmin = {V: mu_min_of(V) for V in VARS}
okB = okB and abs(mmin["V0"] / 25118.864315095823 - 1) < 1e-6
gapB = math.log10(mmin["V0"] / MUMAX)
moveB = max(abs(math.log10(mmin[V] / mmin["V0"])) for V in ADM)
labB = "ARTEFACT" if any(mmin[V] <= MUMAX for V in ADM) else ("PARTIAL" if moveB >= 0.25 * gapB else "ROBUST")
bndB = [V for V in ("V3", "V4", "V5") if mmin[V] <= MUMAX]
if labB == "ROBUST" and bndB: labB += f", NOT ROBUST to bound {'/'.join(bndB)}"
at79 = min(rowsB, key=lambda x: abs(math.log(x["mu"] / MUMAX)))
RES["B"] = dict(rows=rowsB, mu_min=mmin, mu_max=MUMAX, gap_dex=gapB, max_admissible_move_dex=moveB, reproduce=okB,
                dchi2_at_mu_max={V: at79[V] for V in VARS}, label=labB)
P("   B iter2 mu_min (Mpc^-1): " + ", ".join(f"{V} {mmin[V]:.4g}" for V in VARS) + f"  vs mu_max {MUMAX:.1f}; gap {gapB:.2f} dex, "
  f"admissible move {moveB:.3f} dex -> {labB}" + ("" if okB else "  [REPRODUCE MISS]"))
P("     Delta chi2 at mu 79.4: " + ", ".join(f"{V} {at79[V]:.1f}" for V in VARS) + " (line 4)")
# C: iter3 closest member
it3 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter3_barotropic_family", "iter3.json")))
cb, cm0, crec = it3["closest"]["beta"], it3["closest"]["mu0"], it3["closest"]["dchi2"]
dvC = dchi2_all(lambda a: (kgrid / (a * cm0 * a ** (3 * cb))) ** 2)
def labCD(rec, dv):
    gap = rec - I2.DCHI2_LINE; mv = max(abs(dv[V] - dv["V0"]) for V in ADM)
    lab = "ARTEFACT" if any(dv[V] <= I2.DCHI2_LINE for V in ADM) else ("PARTIAL" if mv >= 0.25 * gap else "ROBUST")
    bnd = [V for V in ("V3", "V4", "V5") if dv[V] <= I2.DCHI2_LINE]
    return (lab + (f", NOT ROBUST to bound {'/'.join(bnd)}" if (lab == "ROBUST" and bnd) else "")), mv, gap
labC, mvC, gapC = labCD(crec, dvC); okC = abs(dvC["V0"] - crec) <= 0.1
RES["C"] = dict(beta=cb, mu0=cm0, record=crec, dchi2=dvC, gap=gapC, max_admissible_move=mvC, reproduce=okC, label=labC)
P(f"   C iter3 closest (beta {cb:.1f}, mu0 {cm0:.4g}): " + ", ".join(f"{V} {dvC[V]:.2f}" for V in VARS)
  + f" (record {crec:.2f}); move {mvC:.2f} of gap {gapC:.1f} -> {labC}" + ("" if okC else "  [REPRODUCE MISS]"))
# D: QX27 G6b closest graded row (n 6 canonical; sigma0 from qx27.json; z_h 10, adiabatic sigma0/a)
q27 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX27_tail_retention_sector", "qx27.json")))
s0 = q27["per_n"]["6.0"]["canonical"]["sigma1d"]; a_h = 1 / 11.0
def kJ_phys(a): return math.sqrt(1.5 * Om_d0 * a ** -3) * H0 / (s0 / a)
dvD = dchi2_all(lambda a: 0.0 if a <= a_h else (kgrid / (a * kJ_phys(a))) ** 2)
labD, mvD, gapD = labCD(230.9, dvD); okD = abs(dvD["V0"] - 230.9) <= 0.1
RES["D"] = dict(n=6.0, footing="canonical", sigma0=s0, record=230.9, dchi2=dvD, gap=gapD, max_admissible_move=mvD, reproduce=okD, label=labD)
P(f"   D QX27 G6b n 6 canonical (sigma0 {s0:.1f} km/s): " + ", ".join(f"{V} {dvD[V]:.2f}" for V in VARS)
  + f" (record 230.9); move {mvD:.2f} of gap {gapD:.1f} -> {labD}" + ("" if okD else "  [REPRODUCE MISS]"))
P("   (a0 does not enter B-D at linear order, QX3 assumption A-web: the labels hold for both footings.)")
Mc.struct_cleanup()

# ====================================================================== Part E: record-sized items
P(""); P("== E. record-sized items")
E = {}
# QX15: foreground-nuisance freedom (QX15 KA-P2 side finding) vs the baryons-only gap
for foot, dch in (("canonical", 172848.0), ("alt", 166612.0)):
    fr = 732.0 / (dch - 25.0)
    E[f"QX15_{foot}"] = dict(gap=dch - 25.0, foreground_freedom=732.0, frac=fr, label="ROBUST" if fr < 0.25 else "PARTIAL")
    P(f"   QX15 MB baryons-only [{foot}]: Delta chi2 {dch:.0f} vs line 25; all CamSpec nuisance freedom 732 = {fr:.4f} of gap -> {E[f'QX15_{foot}']['label']}")
# KiDS shift statistic: exact cancellation of g_obs rescale; radius conversion moves by delta ln D_A
def DA(z, Om, hh):
    zz = np.linspace(0, z, 4001); Ez = np.sqrt(Om * (1 + zz) ** 3 + 1 - Om)
    return 2997.92458 / hh * float(np.sum(0.5 * (1 / Ez[1:] + 1 / Ez[:-1]) * np.diff(zz))) / (1 + z)
dl = {z: math.log(DA(z, 0.3085, 0.674) / DA(z, 0.2793, 0.70)) for z in (0.15, 0.25, 0.35)}
dmax = max(abs(v) for v in dl.values())
kids = []
for nm, sh in (("QX10 C3 (smallest)", 0.15), ("QX10 C2 (largest)", 0.27)):
    bound = 3 * sh * dmax; gap = sh - 0.05
    kids.append(dict(case=nm, shift=sh, bound=bound, gap=gap, frac=bound / gap, label="ROBUST" if bound < 0.25 * gap else "PARTIAL"))
E["KiDS"] = dict(dlnDA=dl, rows=kids, multiplicative_rescale_effect_on_shift=0.0)
P(f"   KiDS shift statistic: g_obs rescale T cancels exactly (0); delta ln D_A native/fiducial at z_l 0.15/0.25/0.35 = "
  + ", ".join(f"{dl[z]:+.4f}" for z in dl))
for r in kids:
    P(f"     {r['case']}: shift {r['shift']:.2f} vs line 0.05, bound |d shift| <= {r['bound']:.4f} = {r['frac']:.3f} of gap -> {r['label']}")
# forest line: thermal-history / emulator range through L319's alpha(m) ~ m^-1.11 (published WDM bound range 1.9-5.3 keV, PROVISIONAL)
fac = (5.3 / 1.9) ** 1.11
for nm, lam in (("QX27 G6c smallest", 491.7), ("QX27 G6c largest", 1024.0)):
    line = 0.646; frlog = math.log(fac) / math.log(lam / line); frlin = (fac - 1) * line / (lam - line)
    E[f"forest_{nm}"] = dict(lambda_J=lam, line=line, line_loosened=line * fac, frac_log=frlog, frac_lin=frlin,
                             label="ROBUST" if max(frlog, frlin) < 0.25 else "PARTIAL")
    P(f"   forest {nm}: lambda_J(z 3) {lam:.1f} Mpc vs line {line}; thermal-history range loosens the line x{fac:.2f} to {line * fac:.2f} Mpc "
      f"= {frlog:.3f} of the gap in log ({frlin:.4f} linear) -> {E[f'forest_{nm}']['label']}")
E["EB1b"] = dict(label="ROBUST", note="the failing step (collapse redshift of baryon clumps) uses no external data product; "
                 "QSO1's mass and z enter only the timing gate, which no clump reaches before z 0.48 (p05)")
P(f"   EB1b: no data product enters the failing step (collapse before z 0.48 at p05 vs QSO1's z 7.05) -> ROBUST")
RES["E"] = E

RES["checks_pass_as_frozen"] = bool(RES["K1"]["pass_"])
RES["checks_pass"] = bool(RES["K1prime_A1"]["pass_"] and RES["K2"]["pass_"] and RES["A_reproduce_pass"] and okB and okC and okD
                          and (MUT or RES["K3_bite"]["bites"]))
P(""); P(f"K1 as frozen: {'PASS' if RES['K1']['pass_'] else 'FAIL (wrong reference values; Amendment A1)'}")
P(f"All checks (K1' per A1, K2, reproduce A-D{'' if MUT else ', K3 bite'}): {'PASS' if RES['checks_pass'] else 'FAIL'}")
P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
json.dump(RES, open(os.path.join(HERE, f"qx31{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"qx31{TAG}.out"), "w").write("\n".join(OUT) + "\n")
