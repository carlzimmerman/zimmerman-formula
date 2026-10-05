#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
paper_numbers.py -- every number quoted in the MNRAS manuscript `mnras_a0_lambda_v3.tex` (v3.4) that is not printed by
one of the repository estimators (those are re-run here as subprocesses, or by reproduce_all.sh):

    real_research/reviews/mi_btfr_intercept_kappa_door_2026.py          -> estimator A on SPARC's tabulated distances, the floor
    real_research/reviews/kappa_h0_convention_audit_2026.py             -> estimator A's Hubble-flow weight q_HF and its four conventions
    real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py -> the earlier form of estimator B (reproduce_all.sh step 2)
    real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py -> its committed output is REPLICATED here (estimator C, S3)

THE H0 CONVENTION (v3.1).  SPARC's 97 Hubble-flow distances (f_D = 1) assume H0 = 73 (SPARC master table, note 2); rho_Lambda
is built from H0 = 67.4.  Every SPARC kappa in the paper is computed with those distances multiplied by 73/67.4 (the
"Planck-consistent" convention R1 of the repository audit; it divides g_obs of those galaxies by 1.083 and leaves g_bar
unchanged).  The headline estimators are also given on SPARC's tabulated distances (MIXED) and with rho_Lambda rebuilt at
H0 = 73 (R2a: Omega_Lambda fixed; R2b: Omega_m h^2 fixed): the convention box of S3.

Sections (each ends in checks that CAN fail; exit code 1 if any does):
    S1  the relation, step by step: rho_crit, rho_Lambda, c sqrt(G rho_Lambda), a0, the equivalent forms
    S2  the standard radial-acceleration fit on SPARC and its mass-to-light degeneracy; estimator B (shape only); injections
    S3  estimators A, B, C (C = the profile likelihood with Upsilon free per galaxy, re-implemented with equation (nu)),
        the convention box, the candidate coefficients, published values converted to kappa, the floor, the H0 lock
    S4  the redshift laws; the error amplification; the gate and the HALO MASS it selects (v3.1: the decision value is the
        LambdaCDM rise for that halo mass, not for 1e12 Msun); the design: expected log-odds, the probability of reaching
        20:1 and of misleading evidence (Monte Carlo), the concentration-mass relation as a shared model systematic, the
        common-mode baryonic-mass calibration, and the Fisher conditioning with the mass scale free (CFG240)
    S5  RC100 on the journal table (CFG305).  v3.2: the PRIMARY route is framework-native (CFG303 route B: SED stellar mass
        from the table plus scaling-relation gas in a thin disc, through the law; CFG303's committed functions exec'd read-only);
        the closed-form inversion of the tabulated (halo-model) dark fractions is the labelled COMPARISON, with its calibration
        drift, RC100's own internally flagged rows and the prior-tracking of f_DM (CFG217 G2, read).  v3.3 (CFG310): the native route's
        censoring by redshift (floor fraction, rank tests, a Tobit-type slope), and its column-6 stellar masses against the journal
    S6  the deep regime (g_bar < 0.2 a0) in SPARC and MIGHTEE-HI: slope, amplitude, the colour-group caveat, the pitfall
    S7  the high-redshift record, read from committed lane outputs (MUSE-DARK, KURVS, MIGHTEE-HI/LADUMA, z >= 4, the gas
        bracket, the source-table audit).  A check that only confirms that the text quotes a committed number, or that
        re-does arithmetic on committed numbers, is labelled 'identity': the evidence lies in the lane.
Check kinds: identity (no evidence), model (evaluates a published model), data (can fail on the data), injection (feeds an
estimator synthetic data with a known answer).
Both densities are carried throughout: rho_Lambda (a0 = 9.36e-11) and rho_crit (a0 = 1.13e-10).  kappa = 1/2 is FITTED.
Run from anywhere:  python3 paper_numbers.py        Output: paper_numbers.json next to this file.
"""
import os, sys, glob, json, math, re
import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SPARC = os.path.join(ROOT, "real_research", "data", "sparc_data")
RC100 = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3_PUBLISHED.csv")   # v3.2: the journal table (ApJ 944:78, Table B1), CFG305 (6c907be69)
RC100_CORR = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")   # CFG289 (51c70923f): arXiv v1, as used by v3/v3.1
RC100_ORIG = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3.csv")      # the earliest transcription (17 wrong cells)
RC100_SHA256 = "8a7ed57a99be67995890c5f1293ecf7ac19d84dea60533b1d0d2c8901aa930e7"                 # PUBLISHED (CFG305)
RC100_CORR_SHA256 = "a1778d75476ede17da690e09fc1176b68455f22778e5de8ef39b66a0cb19398f"            # CORRECTED (CFG289)
CFG = os.path.join(ROOT, "campaign_fresh_gravity")

OUT, FAILS, NCHK = {}, [], [0]
KINDS = {}
KIND_TEXT = {"identity": "algebra or arithmetic on stated inputs: certifies the arithmetic, can fail only by a coding error, carries NO evidence",
             "model": "evaluates a published model or relation at stated inputs: can fail if the model is mis-implemented, carries no evidence",
             "data": "can fail on the data",
             "injection": "feeds an estimator synthetic data with a KNOWN a0 (or trend) built on the real baryons: proves the estimator measures, not echoes"}
def P(*a): print(*a, flush=True)
KIND_BY_ID = {"S1a": "identity", "S1b": "identity", "S1c": "identity", "S2d": "identity", "S2e": "identity", "S3a": "identity", "S3b": "identity",
              "S4a": "identity", "S4d": "identity", "S4e": "identity", "S4f": "identity", "S4j": "identity", "S4k": "identity", "S5a": "identity",
              "S4b": "model", "S4c": "model", "S4g": "model", "S4h": "model", "S4i": "model", "S4l": "model"}
def check(name, ok, detail="", kind=None):
    kind = kind or KIND_BY_ID.get(name.split()[0], "data")
    assert kind in KIND_TEXT
    NCHK[0] += 1; KINDS.setdefault(kind, []).append(name)
    P(f"  [{'PASS' if ok else 'FAIL'}] [{kind}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def head(s): P(""); P("=" * 110); P(s); P("=" * 110)

# ----------------------------------------------------------------------------------------------------------------
# constants and cosmological inputs (stated in the paper's Table 1)
c = 299792458.0                  # m/s (exact)
G = 6.67430e-11                  # m^3 kg^-1 s^-2 (CODATA 2018)
MPC = 3.0856775814913673e22      # m
KPC = MPC / 1e3
MSUN = 1.98847e30                # kg
HBAR_EVS = 6.582119569e-16       # eV s
EV = 1.602176634e-19             # J
H0_KMS, OL, OM = 67.4, 0.685, 0.315          # Planck 2018 (rounded as in the text)
H0_SHOES = 73.04                              # Riess et al. 2022
H0_SPARC_HF = 73.0                            # the H0 behind SPARC's Hubble-flow distances (master table, note 2)
HF_R1 = H0_SPARC_HF / H0_KMS                  # R1: those distances x 73/67.4 -> g_obs / 1.083 (g_bar is distance-free)
OMH2 = OM * (H0_KMS / 100)**2                 # the CMB holds Omega_m h^2

def nu(y):
    """The radial-acceleration function of McGaugh, Lelli & Schombert (2016); form of Milgrom & Sanders (2008)."""
    y = np.asarray(y, float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))
def n_slope(y):
    """n(y) = d ln nu / d ln y = -(sqrt y / 2)/(e^{sqrt y} - 1);  -> -1/2 in the deep regime, -> 0 in the Newtonian."""
    s = np.sqrt(np.asarray(y, float))
    return -(s / 2.0) / np.expm1(s)

# ================================================================================================================
head("S1  THE RELATION, STEP BY STEP")
H0 = H0_KMS * 1e3 / MPC
rho_crit = 3 * H0**2 / (8 * math.pi * G)
rho_L = OL * rho_crit
A_L = c * math.sqrt(G * rho_L)               # c sqrt(G rho_Lambda): the only acceleration in (c, G, rho_Lambda)
A_C = c * math.sqrt(G * rho_crit)
a0_L, a0_C = 0.5 * A_L, 0.5 * A_C
H_L = H0 * math.sqrt(OL)
Lam = 3 * H_L**2 / c**2
R_dS = c / H_L
Z = c * H_L / a0_L
P(f"  H0 = {H0_KMS} km/s/Mpc = {H0:.5e} s^-1")
P(f"  rho_crit = 3 H0^2/(8 pi G) = {rho_crit:.4e} kg m^-3")
P(f"  rho_Lambda = Omega_Lambda rho_crit = {rho_L:.4e} kg m^-3        (Omega_Lambda = {OL})")
P(f"  G rho_Lambda = {G*rho_L:.4e} s^-2 ;  sqrt = {math.sqrt(G*rho_L):.4e} s^-1")
P(f"  c sqrt(G rho_Lambda) = {A_L:.4e} m s^-2      <- the unique acceleration built from (c, G, rho_Lambda)")
P(f"  kappa = 1/2:  a0 = {a0_L:.4e} m s^-2   (rho_Lambda);   {a0_C:.4e} m s^-2   (rho_crit);  ratio {a0_C/a0_L:.4f} = 1/sqrt(Omega_Lambda)")
P(f"  H_Lambda = H0 sqrt(Omega_Lambda) = {H_L:.5e} s^-1 ;  c H_Lambda = {c*H_L:.4e} ;  c H0 = {c*H0:.4e} m s^-2")
P(f"  Lambda = 3 H_Lambda^2/c^2 = {Lam:.4e} m^-2 ;  de Sitter radius c/H_Lambda = {R_dS:.4e} m = {R_dS/MPC/1e3:.2f} Gpc")
P(f"  Z = c H_Lambda / a0 = {Z:.4f} ;  sqrt(32 pi/3) = {math.sqrt(32*math.pi/3):.4f}")
f2 = c**2 * math.sqrt(Lam / (32 * math.pi)); f3 = c * H_L / math.sqrt(32 * math.pi / 3); f4 = c**2 / (math.sqrt(32 * math.pi / 3) * R_dS)
rhoE_eV4 = rho_L * c**2 / EV * (HBAR_EVS * c)**3           # energy density in eV^4 (hbar = c = 1)
M_L = rhoE_eV4 ** 0.25                                      # eV
M_P = math.sqrt(HBAR_EVS * EV * c / G) * c**2 / EV          # non-reduced Planck mass in eV
a_nat = M_L**2 / (2 * M_P) / HBAR_EVS * c                   # eV -> s^-1 -> m s^-2
P(f"  four forms: (c/2)sqrt(G rho_L) = {a0_L:.6e};  c^2 sqrt(Lambda/32pi) = {f2:.6e};  cH_L/sqrt(32pi/3) = {f3:.6e};  c^2/(sqrt(32pi/3) R_dS) = {f4:.6e}")
P(f"  natural units: M_Lambda = rho_Lambda^(1/4) = {M_L*1e3:.3f} meV ;  M_P = {M_P:.4e} eV ;  M_Lambda^2/(2 M_P) -> {a_nat:.6e} m s^-2")
l0 = c**2 / a0_L
P(f"  l0 = c^2/a0 = {l0:.4e} m ;  Lambda l0^2 = {Lam*l0**2:.4f} ;  32 pi = {32*math.pi:.4f}")
OUT["S1"] = dict(H0_si=H0, rho_crit=rho_crit, rho_L=rho_L, A_L=A_L, a0_L=a0_L, a0_C=a0_C, cH_L=c*H_L, cH0=c*H0, Lambda=Lam,
                 R_dS_Gpc=R_dS/MPC/1e3, Z=Z, M_Lambda_meV=M_L*1e3, M_P_eV=M_P)
def A_L_at(h_kms, mode="OL"):
    """c sqrt(G rho_Lambda) at another H0: Omega_Lambda fixed ('OL', R2a) or Omega_m h^2 fixed ('omh2', R2b)."""
    Hs = h_kms * 1e3 / MPC; OLh = OL if mode == "OL" else 1 - OMH2 / (h_kms / 100)**2
    return c * math.sqrt(G * OLh * 3 * Hs**2 / (8 * math.pi * G))
check("S1a the four forms of the kappa = 1/2 relation are one number", max(abs(x/a0_L - 1) for x in (f2, f3, f4, a_nat)) < 1e-9,
      f"max relative difference {max(abs(x/a0_L - 1) for x in (f2, f3, f4, a_nat)):.1e}")
check("S1c a0(rho_Lambda) = 9.36e-11 and a0(rho_crit) = 1.13e-10 to three figures", abs(a0_L/9.36e-11 - 1) < 1e-3 and abs(a0_C/1.13e-10 - 1) < 2e-3,
      f"{a0_L:.4e}, {a0_C:.4e}")

# ================================================================================================================
head("S2  THE STANDARD RADIAL-ACCELERATION FIT ON SPARC, AND ITS MASS-TO-LIGHT DEGENERACY")
K = 1e6 / KPC                     # (km/s)^2/kpc -> m s^-2
SIG_INT = 0.034                   # intrinsic scatter floor in dex (Desmond 2023), as in the repository estimator
_CACHE = {}
def _read(f):
    if f not in _CACHE: _CACHE[f] = np.genfromtxt(f, comments="#")
    return _CACHE[f]
GAL_INDEX = [None]
# SPARC distance methods from the master table (whitespace parse; f_D = 1 is Hubble flow at H0 = 73, note 2)
SPARC_MRT = os.path.join(ROOT, "real_research", "data", "SPARC_Lelli2016c.mrt")
FD = {}
for _ln in open(SPARC_MRT):
    _p = _ln.split()
    if len(_p) > 18 and _p[0][0].isalpha() and _p[1].isdigit() and _p[4].isdigit(): FD[_p[0]] = int(_p[4])
N_HF = sum(1 for v in FD.values() if v == 1)
def load_sparc(UD=0.5, UB=0.7, qcut=0.10, GS=1.0, bulgeless=False, hf=HF_R1):
    """g_bar, g_obs, error in log10 g_obs, number of galaxies.  GS rescales the gas mass; bulgeless keeps V_bul = 0 galaxies only.
    hf rescales the Hubble-flow (f_D = 1) distances: HF_R1 = 73/67.4 (the paper's convention), 1.0 = SPARC as tabulated.
    A distance factor f leaves g_bar = V_bar^2/R unchanged (V_bar^2 ~ D, R ~ D) and divides g_obs = V^2/R by f.
    The galaxy index of every point is left in GAL_INDEX[0] for galaxy-level bootstraps."""
    gb, go, ew, gi, ng = [], [], [], [], 0
    for f in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        d = _read(f)
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        if bulgeless and np.any(Vb > 0): continue
        m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < qcut)
        R, V, eV, Vg, Vd, Vb = R[m], V[m], eV[m], Vg[m], Vd[m], Vb[m]
        v2 = GS * np.sign(Vg) * Vg**2 + UD * Vd**2 + UB * Vb**2
        ok = v2 > 0
        if ok.sum() == 0: continue
        sc = hf if FD.get(os.path.basename(f).replace("_rotmod.dat", "")) == 1 else 1.0
        gb.append(v2[ok] / R[ok] * K); go.append(V[ok]**2 / R[ok] * K / sc); ew.append(2 * eV[ok] / V[ok] / math.log(10)); gi.append(np.full(ok.sum(), ng))
        ng += 1
    GAL_INDEX[0] = np.concatenate(gi)
    return np.concatenate(gb), np.concatenate(go), np.concatenate(ew), ng
def fit_a0(gb, go, ew):
    s2 = ew**2 + SIG_INT**2
    f = lambda la: np.sum((np.log10(go) - np.log10(gb * nu(gb / 10**la)))**2 / s2)
    r = minimize_scalar(f, bounds=(-10.6, -9.4), method="bounded", options=dict(xatol=1e-7))
    a0 = 10**r.x
    res = np.log10(go) - np.log10(gb * nu(gb / a0))
    return a0, float(np.sqrt(np.mean(res**2)))
gb, go, ew, ngal = load_sparc()
P(f"  SPARC: {ngal} galaxies, {len(gb)} points with velocity error < 10%;  g_bar spans {gb.min():.2e} - {gb.max():.2e} m s^-2")
P(f"  H0 convention: {N_HF} galaxies have Hubble-flow distances (f_D = 1, H0 = {H0_SPARC_HF:g}); they are multiplied by {HF_R1:.4f} (R1) unless stated")
# replication on SPARC's TABULATED distances (McGaugh, Lelli & Schombert 2016 used them): Upsilon 0.5 / 0.7
a_tab05, rms_tab05 = fit_a0(*load_sparc(UD=0.5, hf=1.0)[:3])
P(f"  replication, tabulated distances, Upsilon_disc 0.5: a0 = {a_tab05:.3e} (McGaugh+2016: 1.20e-10), rms {rms_tab05:.3f} dex")
rows = []
P(f"  {'Upsilon_disc':>12} {'a0 [1e-10]':>11} {'kappa(rho_L)':>13} {'kappa(rho_crit)':>16} {'rms [dex]':>10}")
for UD in (0.40, 0.50, 0.60, 0.70, 0.80):
    g1, g2, e1, _ = load_sparc(UD=UD)
    a0, rms = fit_a0(g1, g2, e1)
    rows.append(dict(UD=UD, a0=a0, kappa_L=a0 / A_L, kappa_C=a0 / A_C, rms=rms))
    P(f"  {UD:12.2f} {a0/1e-10:11.3f} {a0/A_L:13.3f} {a0/A_C:16.3f} {rms:10.3f}")
ud_half = brentq(lambda u: fit_a0(*load_sparc(UD=u)[:3])[0] / A_L - 0.5, 0.35, 0.80, xtol=1e-4)
ud_half_C = brentq(lambda u: fit_a0(*load_sparc(UD=u)[:3])[0] / A_C - 0.5, 0.30, 0.80, xtol=1e-4)
ud_half_tab = brentq(lambda u: fit_a0(*load_sparc(UD=u, hf=1.0)[:3])[0] / A_L - 0.5, 0.35, 0.80, xtol=1e-4)
ud_half_C_tab = brentq(lambda u: fit_a0(*load_sparc(UD=u, hf=1.0)[:3])[0] / A_C - 0.5, 0.30, 0.80, xtol=1e-4)
P(f"  kappa = 1/2 exactly needs Upsilon_disc = {ud_half:.3f} (rho_Lambda) or {ud_half_C:.3f} (rho_crit), bulge fixed at 0.7;"
  f"  on the tabulated distances {ud_half_tab:.3f} / {ud_half_C_tab:.3f}")
# residual scatter with a0 FIXED at the two predicted values, stellar mass-to-light free (one global number)
def rms_fixed(a0fix):
    f = lambda u: (lambda g1, g2, e1, _: np.sqrt(np.mean((np.log10(g2) - np.log10(g1 * nu(g1 / a0fix)))**2)))(*load_sparc(UD=u))
    r = minimize_scalar(f, bounds=(0.3, 1.2), method="bounded", options=dict(xatol=1e-3))
    return r.x, float(r.fun)
uL, rL = rms_fixed(a0_L); uC, rC = rms_fixed(a0_C)
P(f"  a0 fixed at {a0_L:.3e}: least-scatter Upsilon_disc = {uL:.2f}, rms = {rL:.3f} dex;   fixed at {a0_C:.3e}: {uC:.2f}, {rC:.3f} dex")
# ---- ESTIMATOR B, computed here in full: the shape-only fit (free vertical offset), its distance immunity, and its error budget
def fit_shape(gb_, go_, ew_):
    s2 = ew_**2 + SIG_INT**2; w = 1 / s2
    def prof(la):
        r = np.log10(go_) - np.log10(gb_ * nu(gb_ / 10**la)); C = np.sum(w * r) / np.sum(w)      # the offset is linear: solve it exactly
        return np.sum(w * (r - C)**2)
    r = minimize_scalar(prof, bounds=(-10.8, -9.2), method="bounded", options=dict(xatol=1e-7))
    return 10**r.x
UD_C, UB_C = 0.6, 0.7                                 # centre of the adopted mass-to-light ranges: disc 0.5-0.7, bulge 0.6-0.8
P(f"  ESTIMATOR B, shape-only (free vertical offset):")
P(f"  {'':>14}" + "".join(f"{'Ups_bul = '+str(ub):>16}" for ub in (0.6, 0.7, 0.8)))
grid = {}
for UD in (0.5, 0.6, 0.7):
    rowk = []
    for UB in (0.6, 0.7, 0.8):
        g1, g2, e1, _ = load_sparc(UD=UD, UB=UB); grid[(UD, UB)] = fit_shape(g1, g2, e1) / A_L; rowk.append(grid[(UD, UB)])
    P(f"  Ups_disc = {UD:3.1f} " + "".join(f"{k_:16.3f}" for k_ in rowk))
kB = grid[(UD_C, UB_C)]
# the same estimator on SPARC's TABULATED distances (the earlier convention), and the four-convention box
kB_tab = fit_shape(*load_sparc(UD=UD_C, UB=UB_C, hf=1.0)[:3]) / A_L
B_tab_rep = {u: fit_shape(*load_sparc(UD=u, UB=0.7, hf=1.0)[:3]) / A_L for u in (0.5, 0.7)}
BOX_B = {"R1": kB, "MIXED": kB_tab, "R2a": kB_tab * A_L / A_L_at(H0_SPARC_HF, "OL"), "R2b": kB_tab * A_L / A_L_at(H0_SPARC_HF, "omh2")}
P(f"  estimator B convention box: " + ", ".join(f"{k_} {v_:.3f}" for k_, v_ in BOX_B.items()))
ml_disc = 0.5 * (grid[(0.7, UB_C)] - grid[(0.5, UB_C)]); ml_bul = 0.5 * (grid[(UD_C, 0.8)] - grid[(UD_C, 0.6)])
ml_all = 0.5 * (max(grid.values()) - min(grid.values()))
gas = 0.5 * abs(fit_shape(*load_sparc(UD=UD_C, UB=UB_C, GS=1.115)[:3]) - fit_shape(*load_sparc(UD=UD_C, UB=UB_C, GS=0.885)[:3])) / A_L
g1, g2, e1, ng_ = load_sparc(UD=UD_C, UB=UB_C); gidx = GAL_INDEX[0].copy()
rngB = np.random.default_rng(20260921); sel = [np.where(gidx == k_)[0] for k_ in range(ng_)]
boot = []
for _ in range(300):
    idx = np.concatenate([sel[k_] for k_ in rngB.integers(0, ng_, ng_)]); boot.append(fit_shape(g1[idx], g2[idx], e1[idx]) / A_L)
statB = float(np.std(boot))
sB = math.sqrt(ml_all**2 + gas**2 + statB**2)
P(f"  kappa_B = {kB:.3f} at (Ups_disc, Ups_bul) = ({UD_C}, {UB_C});  errors: disc M/L {ml_disc:.3f}, bulge M/L {ml_bul:.3f}, full M/L grid half-range {ml_all:.3f}, gas scale (11.5%) {gas:.3f}, bootstrap over galaxies {statB:.3f}")
P(f"  ==> kappa_B = {kB:.2f} +/- {sB:.2f}   (R1; dominated by the BULGE mass-to-light ratio; the repository's 0.551 +/- 0.043 held Ups_bul fixed at 0.7 on the tabulated distances; tabulated centre {kB_tab:.3f})")
g1r, g2r, e1r, _ = load_sparc(); a_ref = fit_shape(g1r, g2r, e1r)
imm = max(abs(fit_shape(g1r, g2r / (1 + d), e1r) / a_ref - 1) for d in (0.05, 0.10))
std_move = abs(fit_a0(g1r, g2r / 1.10, e1r)[0] / fit_a0(g1r, g2r, e1r)[0] - 1)
P(f"  a common distance rescaling of 5 and 10 per cent moves the shape-only a0 by {imm:.1e} (fractional) and the standard fit by {std_move*100:.1f}% (10 per cent case)")
bl = []
for UD in (0.5, 0.6, 0.7):
    gq, gw, ee, nbl = load_sparc(UD=UD, bulgeless=True); bl.append(fit_shape(gq, gw, ee) / A_L)
P(f"  bulgeless galaxies only ({nbl} galaxies, {len(gq)} points, g_bar < {gq.max()/a0_L:.0f} a0): kappa_B = " + ", ".join(f"{b_:.2f}" for b_ in bl) + " at Ups_disc = 0.5, 0.6, 0.7  -> the lever arm is too short; no help")
shape = [dict(UD=k_[0], UB=k_[1], kappa_L=v_) for k_, v_ in grid.items()]
# ---- the deep band, where the stars carry less of the mass: quality-cut and error-weighted (the paper's convention), and the
#      against-interest variant with every point given equal weight
deep = {}
for UD in (0.5, 0.6, 0.7):
    g1, g2, e1, _ = load_sparc(UD=UD, UB=0.7); md = g1 < 0.1 * a0_L
    q1, q2, q3, _ = load_sparc(UD=UD, UB=0.7, qcut=10.0); mq = q1 < 0.1 * a0_L
    f_unw = lambda la, X=q1[mq], Y=q2[mq]: np.sum((np.log10(Y) - np.log10(X * nu(X / 10**la)))**2)
    a_unw = 10**minimize_scalar(f_unw, bounds=(-11.5, -9.0), method="bounded", options=dict(xatol=1e-8)).x
    deep[UD] = dict(kappa=fit_a0(g1[md], g2[md], e1[md])[0] / A_L, n=int(md.sum()), kappa_unweighted_all=a_unw / A_L, n_all=int(mq.sum()))
P("  deep band g_bar < 0.1 a0 (bulge 0.7): kappa = " + ", ".join(f"{deep[u]['kappa']:.3f} (N {deep[u]['n']})" for u in deep) + " at Upsilon_disc = 0.5, 0.6, 0.7")
P("     every point, equal weight (no quality cut): " + ", ".join(f"{deep[u]['kappa_unweighted_all']:.3f}" for u in deep) + "  <- points with >10% velocity errors pull it down")
# ---- INJECTION TESTS: synthetic g_obs built on the REAL g_bar with a KNOWN a0, realistic noise; every estimator must return it
rngI = np.random.default_rng(314159)
g1, g2, e1, _ = load_sparc(UD=0.5, UB=0.7); sig_pt = np.sqrt(e1**2 + SIG_INT**2)
inj = dict(standard=[], shape=[], shape_std_bias=[], deep=[])
for fac in (0.7, 1.0, 1.3):
    a_in = fac * a0_L
    syn = g1 * nu(g1 / a_in) * 10**(rngI.normal(0, 1, g1.size) * sig_pt)
    inj["standard"].append(fit_a0(g1, syn, e1)[0] / a_in)
    off = 10**0.08                                   # a common 20 per cent distance-scale error shifts g_obs by 0.08 dex
    inj["shape"].append(fit_shape(g1, syn * off, e1) / a_in)
    inj["shape_std_bias"].append(fit_a0(g1, syn * off, e1)[0] / a_in)
    md = g1 < 0.1 * a0_L
    inj["deep"].append(fit_a0(g1[md], syn[md], e1[md])[0] / a_in)
P("  injection (a0 = 0.7, 1.0, 1.3 x canonical, real g_bar, noise = quoted errors + 0.034 dex): returned / injected")
P("     standard fit " + ", ".join(f"{v:.3f}" for v in inj["standard"]) + ";  deep band " + ", ".join(f"{v:.3f}" for v in inj["deep"]))
P("     with a +0.08 dex common offset (a 20% distance error): shape-only " + ", ".join(f"{v:.3f}" for v in inj["shape"]) +
  ";  the standard fit, for contrast, " + ", ".join(f"{v:.3f}" for v in inj["shape_std_bias"]))
OUT["S2"] = dict(deep_band=deep, injection=inj, shape_only=shape, kappa_B=kB, sigma_B=sB, kappa_B_tab=kB_tab, box_B=BOX_B, a0_tab_05=a_tab05,
                 ud_for_half_L_tab=ud_half_tab, ud_for_half_C_tab=ud_half_C_tab, B_budget=dict(ml_disc=ml_disc, ml_bul=ml_bul, ml_grid=ml_all, gas=gas, stat=statB), bulgeless=bl,
                 shape_immunity=imm, standard_move_10pc=std_move, n_gal=ngal, n_pts=int(len(gb)), table=rows, ud_for_half_L=ud_half, ud_for_half_C=ud_half_C,
                 fixed_L=dict(UD=uL, rms=rL), fixed_C=dict(UD=uC, rms=rC))
r05 = [r for r in rows if abs(r["UD"] - 0.5) < 1e-9][0]
check("S2a REPLICATION: on SPARC's tabulated distances at Upsilon_disc = 0.5 the fit returns the literature a0 = 1.2e-10 within 5%", abs(a_tab05 / 1.2e-10 - 1) < 0.05, f"a0 = {a_tab05:.3e}")
check("S2a2 the Planck-consistent distances LOWER the standard-fit a0 (the Hubble-flow g_obs fall by 1/1.083): at Upsilon_disc = 0.5 by 5-15 per cent",
      0.85 < r05["a0"] / a_tab05 < 0.95, f"{r05['a0']:.3e} vs {a_tab05:.3e} ({(r05['a0']/a_tab05-1)*100:+.1f}%)")
check("S2b the degeneracy is steep: kappa moves by more than 0.15 between Upsilon_disc = 0.5 and 0.7", rows[1]["kappa_L"] - rows[3]["kappa_L"] > 0.15,
      f"{rows[1]['kappa_L']:.3f} -> {rows[3]['kappa_L']:.3f}")
check("S2d the shape-only estimator is immune to a common distance rescaling (< 1e-5): the free offset absorbs it by construction", imm < 1e-5,
      f"{imm:.1e}")
check("S2d2 while the standard fit is not: a 10 per cent common rescaling moves it by more than 15 per cent", std_move > 0.15, f"{std_move*100:.1f}%")
check("S2e on the tabulated distances the replication agrees with the repository's earlier estimator B at Upsilon_bul = 0.7, Upsilon_disc = 0.5 and 0.7 (0.529, 0.574) within 0.01 (code replication)",
      abs(B_tab_rep[0.5] - 0.529) < 0.01 and abs(B_tab_rep[0.7] - 0.574) < 0.01, f"{B_tab_rep[0.5]:.3f}, {B_tab_rep[0.7]:.3f}")
check("S2f AGAINST THE EARLIER ERROR BAR: the bulge mass-to-light ratio moves estimator B by more than twice the 0.043 previously quoted",
      ml_bul > 2 * 0.043, f"bulge term {ml_bul:.3f}; total {sB:.3f}")
check("S2g restricting the fit to the deep band (g_bar < 0.1 a0, quality-cut, error-weighted) does NOT remove the mass-to-light dependence: kappa moves by more than 0.08 across Upsilon_disc 0.5-0.7",
      deep[0.5]["kappa"] - deep[0.7]["kappa"] > 0.08, ", ".join(f"{deep[u]['kappa']:.3f}" for u in deep))
check("S2h AGAINST INTEREST: giving every deep point equal weight (no quality cut) lowers kappa by at least 0.05 at every Upsilon",
      all(deep[u]["kappa"] - deep[u]["kappa_unweighted_all"] > 0.05 for u in deep), ", ".join(f"{deep[u]['kappa_unweighted_all']:.3f}" for u in deep))
check("I1 the standard fit returns the injected a0 to 2 per cent at 0.7, 1.0 and 1.3 x canonical", max(abs(v - 1) for v in inj["standard"]) < 0.02,
      ", ".join(f"{v:.3f}" for v in inj["standard"]), kind="injection")
check("I2 the shape-only estimator returns the injected a0 to 3 per cent through a 0.08 dex common offset that biases the standard fit by > 15 per cent",
      max(abs(v - 1) for v in inj["shape"]) < 0.03 and min(abs(v - 1) for v in inj["shape_std_bias"]) > 0.15,
      "shape " + ", ".join(f"{v:.3f}" for v in inj["shape"]) + "; standard " + ", ".join(f"{v:.3f}" for v in inj["shape_std_bias"]), kind="injection")
check("I3 the deep-band fit returns the injected a0 to 5 per cent", max(abs(v - 1) for v in inj["deep"]) < 0.05, ", ".join(f"{v:.3f}" for v in inj["deep"]), kind="injection")
check("S2c kappa = 1/2 needs a disc mass-to-light ratio inside the population-synthesis range 0.4-0.8", 0.4 < ud_half < 0.8 and 0.4 < ud_half_C < 0.8,
      f"{ud_half:.2f} / {ud_half_C:.2f}")

# ================================================================================================================
# ---- estimator A (repository script, run on SPARC's TABULATED distances): its correction Q(y) is evaluated at an assumed a0
import subprocess
_rA = subprocess.run([sys.executable, "mi_btfr_intercept_kappa_door_2026.py"], cwd=os.path.join(ROOT, "real_research", "reviews"), capture_output=True, text=True)
_m = re.search(r"frozen-y estimate ([0-9.e+-]+) .*?self-consistent fixed point ([0-9.e+-]+) .*?ALT-footing selection\+argument ([0-9.e+-]+)", _rA.stdout)
A_frozen, A_selfc, A_alt = (float(x) for x in _m.groups())
A_TOTAL_PCT = float(re.search(r"TOTAL sigma\(a0\)/a0\s+([0-9.]+)%", _rA.stdout).group(1))
P(f"  estimator A: correction evaluated at the canonical a0 {A_frozen:.4e}; at its own output (fixed point) {A_selfc:.4e} ({(A_selfc/A_frozen-1)*100:+.2f}%);"
  f" selection and correction at the 21% higher alternative a0 {A_alt:.4e} ({(A_alt/A_frozen-1)*100:+.1f}%); total error {A_TOTAL_PCT:.2f}%")
OUT["A_selfconsistency"] = dict(frozen=A_frozen, fixed_point=A_selfc, alt=A_alt, total_pct=A_TOTAL_PCT)
check("S2i estimator A is not an echo of the a0 at which its correction is evaluated: iterating to its own output moves it by < 1 per cent, and a 21 per cent change of that a0 moves it by < 10 per cent (a sensitivity test on the real data)",
      _rA.returncode == 0 and abs(A_selfc / A_frozen - 1) < 0.01 and abs(A_alt / A_frozen - 1) < 0.10,
      f"{(A_selfc/A_frozen-1)*100:+.2f}%, {(A_alt/A_frozen-1)*100:+.1f}%", kind="data")
# ---- the repository's H0-convention audit: estimator A's exposure to the Hubble-flow distances is their WEIGHT fraction q_HF,
#      a0_A ~ (D_HF)^(-2 q_HF) exactly (its check C3), so R1 = MIXED x (73/67.4)^(-2 q_HF)
_rH = subprocess.run([sys.executable, os.path.join(ROOT, "real_research", "reviews", "kappa_h0_convention_audit_2026.py")], cwd=ROOT, capture_output=True, text=True)
_aud = {k_: float(re.search(pat, _rH.stdout).group(1)) for k_, pat in (
    ("q_HF", r"q_HF = ([0-9.]+), against"), ("MIXED", r"committed \(MIXED: numerator 73, denominator [0-9.]+\)\s+kappa = ([0-9.]+)"),
    ("R1", r"R1  h = [0-9.]+ everywhere\s+kappa = ([0-9.]+)"), ("R2a", r"R2a h = 73 everywhere, Omega_L fixed\s+kappa = ([0-9.]+)"),
    ("R2b", r"R2b h = 73 everywhere, omega_m fixed \(Om_L=[0-9.]+\) kappa = ([0-9.]+)"))}
q_HF = _aud["q_HF"]
kA_tab = A_frozen / A_L; sA_tab = kA_tab * A_TOTAL_PCT / 100
kA = kA_tab * HF_R1**(-2 * q_HF); sA = kA * A_TOTAL_PCT / 100           # R1 at H0 = 67.4 (the audit's R1 is at 67.36: 0.02% apart)
BOX_A = {"R1": kA, "MIXED": kA_tab, "R2a": kA_tab * A_L / A_L_at(H0_SPARC_HF, "OL"), "R2b": kA_tab * A_L / A_L_at(H0_SPARC_HF, "omh2")}
P(f"  H0-convention audit: q_HF = {q_HF};  estimator A box: " + ", ".join(f"{k_} {v_:.4f}" for k_, v_ in BOX_A.items()) +
  f"  (audit prints MIXED {_aud['MIXED']}, R1 {_aud['R1']}, R2a {_aud['R2a']}, R2b {_aud['R2b']})")
P(f"  ==> estimator A (R1) kappa = {kA:.3f} +/- {sA:.3f}   [tabulated distances: {kA_tab:.3f} +/- {sA_tab:.3f}]")
check("S3e estimator A's convention box reproduces the repository audit (R1, MIXED, R2a, R2b) to 0.002, with the paper's H0 = 67.4 in place of the audit's 67.36",
      _rH.returncode == 0 and all(abs(BOX_A[k_] - _aud[k_]) < 0.002 for k_ in ("R1", "MIXED", "R2a", "R2b")),
      ", ".join(f"{k_} {BOX_A[k_]:.4f}/{_aud[k_]:.4f}" for k_ in ("R1", "MIXED", "R2a", "R2b")), kind="identity")

head("S3  ESTIMATOR C (PROFILE LIKELIHOOD), THE CONVENTION BOX, CANDIDATES, PUBLISHED VALUES, THE FLOOR, THE H0 LOCK")
# ---- ESTIMATOR C: the profile likelihood of real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py (Upsilon_disc
#      free per galaxy on a grid, Upsilon_bul = 1.4 Upsilon_disc, every point with V > 0, velocity errors clipped at 1 km/s, an
#      intrinsic scatter set by chi^2/dof = 1).  (i) REPLICATION: with that script's own transition function g_obs^2 = g_bar^2 +
#      g_bar a0, its constants, its grids and SPARC's tabulated distances, this code must return its committed table.  (ii) THE
#      PAPER'S ESTIMATOR C: the same likelihood with equation (nu), the R1 distances, a finer Upsilon grid, the scatter set at the
#      best fit, a continuous minimum and a galaxy bootstrap.  The committed script's function is then a SYSTEMATIC of C.
def _pl_load(hf, gs=1.0, ugrid=None, kpc_m=KPC):
    out = []
    for f in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
        d = _read(f)
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        m = np.isfinite(R) & np.isfinite(V) & (R > 0) & (V > 0)
        if m.sum() < 3: continue
        sc = hf if FD.get(os.path.basename(f).replace("_rotmod.dat", "")) == 1 else 1.0
        Rm = R[m] * kpc_m; Vv = V[m]; ee = np.clip(eV[m], 1.0, None)
        gbar = (gs * np.sign(Vg[m]) * Vg[m]**2)[None, :] + ugrid[:, None] * (Vd[m]**2 + 1.4 * Vb[m]**2)[None, :]
        gbar = gbar * 1e6 / Rm[None, :]
        out.append((gbar, np.log10((Vv * 1e3)**2 / Rm / sc), (ee / Vv) * 2 / math.log(10)))
    return out
def _g_alpha1(gb, a0): return np.sqrt(gb * gb + gb * a0)
def _g_nu(gb, a0): return gb * nu(gb / a0)
def _pl_gal(S, a0, sig, kern):
    """per galaxy: the chi^2 minimised over the Upsilon grid, and its number of points"""
    ch, nn = np.empty(len(S)), np.empty(len(S))
    for j, (gbar, lgo, so) in enumerate(S):
        ok = gbar > 0
        with np.errstate(invalid="ignore", divide="ignore"):
            r = lgo[None, :] - np.log10(kern(np.where(ok, gbar, 1.0), a0))
        c2 = np.sum(np.where(ok, r * r / (so**2 + sig**2)[None, :], 0.0), axis=1); n = ok.sum(1)
        c2 = np.where(n > 0, c2, np.inf); k = int(np.argmin(c2)); ch[j], nn[j] = c2[k], n[k]
    return ch, nn
def _pl_tot(S, a0, sig, kern):
    ch, nn = _pl_gal(S, a0, sig, kern); return float(ch.sum()), int(nn.sum()), len(S)
def _pl_sig(S, a0, kern, lo=0.001, hi=0.6, it=40):
    for _ in range(it):
        mid = 0.5 * (lo + hi); ch, npt, nU = _pl_tot(S, a0, mid, kern)
        lo, hi = (mid, hi) if ch / (npt - nU - 1) > 1.0 else (lo, mid)
    return 0.5 * (lo + hi)
def _pl_min(tot, agrid):
    i = int(np.clip(np.argmin(tot), 1, len(agrid) - 2)); A_ = np.polyfit(np.log(agrid[i-1:i+2]), tot[i-1:i+2], 2)
    return math.exp(-A_[1] / (2 * A_[0]))
UG_C = np.linspace(0.05, 3.0, 296)
AGRID_C = A_L * 0.5 * np.exp(np.linspace(math.log(0.55), math.log(1.75), 81))
def estimator_C(kern=_g_nu, hf=HF_R1, gs=1.0, nboot=300, seed=20261002):
    S = _pl_load(hf, gs, UG_C)
    sig = _pl_sig(S, a0_L, kern)                                    # first pass at the canonical value, then at the best fit
    for _ in range(2):
        C_ = np.array([_pl_gal(S, a, sig, kern)[0] for a in AGRID_C]).T
        ab = _pl_min(C_.sum(0), AGRID_C); sig = _pl_sig(S, ab, kern)
    C_ = np.array([_pl_gal(S, a, sig, kern)[0] for a in AGRID_C]).T; ab = _pl_min(C_.sum(0), AGRID_C)
    rng_ = np.random.default_rng(seed); ng_ = C_.shape[0]
    bs_ = [math.log(_pl_min(C_[rng_.integers(0, ng_, ng_)].sum(0), AGRID_C)) for _ in range(nboot)]
    npt_ = int(sum(int((g_[0][0] > -np.inf).size) for g_ in S))
    return dict(a0=ab, kappa=ab / A_L, se_ln=float(np.std(bs_)), sig_int=sig, n_gal=ng_, n_pts=int(sum(g_[1].size for g_ in S)))
# (i) the replication of the committed script, with its own constants (c 2.998e8, G 6.674e-11, kpc 3.0857e19, H0 2.184e-18)
_c_l, _G_l, _kpc_l, _H0_l = 2.998e8, 6.674e-11, 3.0857e19, 2.184e-18
_A0FW = (_c_l / 2) * math.sqrt(_G_l * OL * 3 * _H0_l**2 / (8 * math.pi * _G_l)); _A0ALT = 1.13e-10
_S_rep = _pl_load(1.0, 1.0, np.linspace(0.05, 3.0, 119), kpc_m=_kpc_l)
_sig_rep = _pl_sig(_S_rep, _A0FW, _g_alpha1, it=45)
_scan = np.array(sorted(set(np.concatenate([np.linspace(0.70, 1.45, 31) * _A0FW, [_A0FW, _A0ALT, _c_l * _H0_l / (2 * math.pi)]]))))
_chs = np.array([_pl_tot(_S_rep, a, _sig_rep, _g_alpha1)[0] for a in _scan]); _imin = int(np.argmin(_chs))
_Z_FW = math.sqrt(32 * math.pi / 3)
REP = {nm: _pl_tot(_S_rep, a, _sig_rep, _g_alpha1)[0] - _chs[_imin] for nm, a in (("half_L", _A0FW), ("twopi_L", _A0FW * _Z_FW / (2 * math.pi)),
                                                                                  ("half_crit", _A0ALT), ("twopi_H0", _c_l * _H0_l / (2 * math.pi)))}
REP["best"] = float(_scan[_imin]); REP["sig_int"] = _sig_rep
_pl_out = open(os.path.join(ROOT, "real_research", "reviews", "mi_a0_profile_likelihood_milgrom_footing_2026.out")).read()
_PLC = {}
for key, pat in (("half_L", r"kappa = 1/2\s+\(THE FRAMEWORK\)"), ("twopi_L", r"kappa = 1/2pi \(Milgrom 2020\)"), ("half_crit", r"alt footing rho_tot/cH0"),
                 ("twopi_H0", r"Milgrom cH0/2pi \(own footing\)"), ("best", r"free best fit")):
    mm = re.search(pat + r"\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", _pl_out); _PLC[key] = (float(mm.group(1)), float(mm.group(3)))
P(f"  REPLICATION of the committed profile likelihood (g_obs^2 = g_bar^2 + g_bar a0, tabulated distances): best {REP['best']:.4e} (committed {_PLC['best'][0]}e-10);"
  f" dchi2 " + ", ".join(f"{k_} {REP[k_]:.2f} ({_PLC[k_][1]})" for k_ in ("half_L", "twopi_L", "half_crit", "twopi_H0")))
check("S3f the profile-likelihood code reproduces the committed script's table exactly (best fit to 1e-4, each dchi2 to 0.01) when given that script's transition function, constants, grids and distances (code replication)",
      abs(REP["best"] / (_PLC["best"][0] * 1e-10) - 1) < 1e-4 and all(abs(REP[k_] - _PLC[k_][1]) < 0.01 for k_ in ("half_L", "twopi_L", "half_crit", "twopi_H0")),
      f"best {REP['best']:.4e}", kind="identity")
# (ii) estimator C with equation (nu): R1, the tabulated distances, the other transition function, and the gas scale (+-11.5%)
EC = estimator_C()
EC_tab = estimator_C(hf=1.0, nboot=100)
EC_a1 = estimator_C(kern=_g_alpha1, nboot=100)
EC_gp = estimator_C(gs=1.115, nboot=1); EC_gm = estimator_C(gs=0.885, nboot=1)
kC = EC["kappa"]; C_stat = kC * EC["se_ln"]; C_gas = 0.5 * abs(EC_gm["kappa"] - EC_gp["kappa"]); C_fn = 0.5 * abs(EC_a1["kappa"] - kC)
sC = math.sqrt(C_stat**2 + C_gas**2 + C_fn**2)
BOX_C = {"R1": kC, "MIXED": EC_tab["kappa"], "R2a": EC_tab["kappa"] * A_L / A_L_at(H0_SPARC_HF, "OL"), "R2b": EC_tab["kappa"] * A_L / A_L_at(H0_SPARC_HF, "omh2")}
P(f"  ESTIMATOR C (equation nu, R1): a0 = {EC['a0']:.3e}, kappa = {kC:.3f};  stat (galaxy bootstrap) {C_stat:.3f} ({EC['se_ln']*100:.1f}%), gas scale +-11.5% {C_gas:.3f},"
  f" transition function (half the difference to g^2 = g_bar^2 + g_bar a0, which gives {EC_a1['kappa']:.3f}) {C_fn:.3f}  ->  kappa_C = {kC:.2f} +/- {sC:.2f};"
  f"  sigma_int {EC['sig_int']:.4f} dex; {EC['n_gal']} galaxies, {EC['n_pts']} points")
P(f"  estimator C convention box: " + ", ".join(f"{k_} {v_:.3f}" for k_, v_ in BOX_C.items()) + f";  the other function on the tabulated distances would give about the committed {_PLC['best'][0]/ (A_L/1e-10):.3f}")
OUT["S3_C"] = dict(EC=EC, EC_tab=EC_tab, EC_alpha1=EC_a1, gas_plus=EC_gp["kappa"], gas_minus=EC_gm["kappa"], kappa=kC, sigma=sC, budget=dict(stat=C_stat, gas=C_gas, function=C_fn),
                   box=BOX_C, replication=REP)
check("S3h AGAINST A SINGLE-FUNCTION READING: the transition function moves estimator C by more than its statistical error (the committed script's function is a systematic of C, not a third footing test)",
      abs(EC_a1["kappa"] - kC) > C_stat, f"{kC:.3f} vs {EC_a1['kappa']:.3f}; stat {C_stat:.3f}")
k_hor = math.sqrt(8 * math.pi / 3) / (2 * math.pi)             # a0 = c H_Lambda / 2 pi  (the Lambda form of the classical coincidence)
k_crit_half = 0.5 * A_C / A_L                                   # kappa_Lambda of a0 = (1/2) c sqrt(G rho_crit)
cands = [("c H_Lambda/2pi (Milgrom 2020, eq. 3)", k_hor), ("1/2 (this paper)", 0.5),
         ("c H0/2pi (Milgrom 2020, eq. 3)", k_hor / math.sqrt(OL)), ("c H0/6 (Verlinde 2017)", math.sqrt(8*math.pi/3) / 6 / math.sqrt(OL)),
         ("c H_Lambda (Unruh T = de Sitter T)", math.sqrt(8*math.pi/3)), ("2 c H_Lambda (Milgrom 1999)", 2 * math.sqrt(8*math.pi/3))]
MEAS = [("A: Tully-Fisher intercept", kA, sA), ("B: shape only", kB, sB), ("C: profile likelihood", kC, sC)]      # all on R1
P(f"  {'candidate':42} {'kappa':>7}   pulls: " + "   ".join(m[0] for m in MEAS))
ctab = []
for name, k in cands:
    pulls = [(k - m[1]) / m[2] for m in MEAS]
    ctab.append(dict(name=name, kappa=k, pulls=pulls))
    P(f"  {name:42} {k:7.4f}   " + "   ".join(f"{p:+6.2f} sigma" for p in pulls))
P(f"  1/2 on rho_crit (a0 = 1.13e-10) is kappa_Lambda = {k_crit_half:.3f}: pulls " + ", ".join(f"{(k_crit_half - m[1])/m[2]:+.2f}" for m in MEAS))
# ---- the likelihood ratio between 1/2 and 1/2pi, EACH estimator alone (they share galaxies; no product is formed)
LNLR = {m[0][0]: -0.5 * ((0.5 - m[1]) / m[2])**2 + 0.5 * ((k_hor - m[1]) / m[2])**2 for m in MEAS}
P("  ln[L(1/2)/L(1/2pi)] per estimator: " + ", ".join(f"{k_} {v_:+.2f}" for k_, v_ in LNLR.items()))
# ---- published values of a0 converted to kappa on both footings (inputs as published; distance conventions as each paper's)
PUB = [("McGaugh+2016", "SPARC", r"fixed: 0.5 / 0.7", 1.20e-10, math.hypot(0.02, 0.24) * 1e-10),
       ("Desmond 2023", "SPARC", r"free (joint inference)", 1.19e-10, math.hypot(0.04, 0.09) * 1e-10),
       ("Varasteanu+2025", "MIGHTEE-HI", r"resolved SED fits", 1.69e-10, 0.13e-10),
       ("Varasteanu+2025", "MIGHTEE-HI", r"$\Upsilon_K=0.6$ fixed", 1.08e-10, 0.09e-10),
       ("Varasteanu+2026", "MIGHTEE-HI/LADUMA", r"fiducial (varying)", 1.50e-10, 0.05e-10)]
PUBT = []
for nm, smp, ups, a_, e_ in PUB:
    kL_, sL_ = a_ / A_L, e_ / A_L
    PUBT.append(dict(paper=nm, sample=smp, upsilon=ups, a0=a_, err=e_, kappa_L=kL_, s_L=sL_, kappa_C=a_ / A_C, s_C=e_ / A_C, pull_half_L=(kL_ - 0.5) / sL_, pull_half_C=(a_ / A_C - 0.5) / (e_ / A_C)))
    P(f"  {nm:16s} {smp:18s} a0 = {a_/1e-10:.2f} +/- {e_/1e-10:.2f}: kappa_Lambda {kL_:.3f} +/- {sL_:.3f} (1/2 at {(kL_-0.5)/sL_:+.1f} sigma), kappa_crit {a_/A_C:.3f} (1/2 at {(a_/A_C-0.5)/(e_/A_C):+.1f} sigma)")
DES = PUBT[1]
DES_pulls = dict(half=(DES["kappa_L"] - 0.5) / DES["s_L"], hor=(DES["kappa_L"] - k_hor) / DES["s_L"], H0twopi=(DES["kappa_L"] - k_hor / math.sqrt(OL)) / DES["s_L"],
                 half_crit=(DES["kappa_L"] - k_crit_half) / DES["s_L"])
P(f"  Desmond (2023): kappa_Lambda = {DES['kappa_L']:.3f} +/- {DES['s_L']:.3f}: 1/2 at {DES_pulls['half']:.1f} sigma, 1/2pi at {DES_pulls['hor']:.1f}, cH0/2pi at {DES_pulls['H0twopi']:.1f}, 1/2 on rho_crit at {DES_pulls['half_crit']:.1f}")
_r290 = json.load(open(os.path.join(CFG, "CFG290_mnras_v3_referee", "cfg290_referee_checks_results.json")))
check("S3g AGAINST INTEREST: Desmond (2023)'s a0 = (1.19 +/- 0.04 +/- 0.09)e-10 puts kappa = 1/2 at more than 2.5 sigma on the rho_Lambda footing and within 1 sigma on the rho_crit footing; the arithmetic reproduces the CFG290 referee (R8) to 0.01",
      DES_pulls["half"] > 2.5 and abs(DES_pulls["half_crit"]) < 1 and abs(DES["kappa_L"] - _r290["R8"]["desmond2023"]["kappa_L"]) < 0.01 and abs(DES_pulls["half"] - _r290["R8"]["desmond2023"]["pull_half"]) < 0.05,
      f"kappa {DES['kappa_L']:.3f} +/- {DES['s_L']:.3f}; 1/2 at {DES_pulls['half']:.2f}, rho_crit 1/2 at {DES_pulls['half_crit']:.2f}", kind="identity")
sU, sG = 0.168, 0.115
floor = sU * sG / math.hypot(sU, sG); fstar = sG**2 / (sU**2 + sG**2)
grid = np.linspace(0, 1, 200001); floor_num = np.min(np.hypot(grid * sU, (1 - grid) * sG))
P(f"  mass-budget floor: s_U = {sU}, s_G = {sG}:  s_U s_G/sqrt(s_U^2+s_G^2) = {floor*100:.2f}% at f_* = {fstar:.3f}  (numerical minimum {floor_num*100:.2f}%)")
a_half_planck = 0.5 * A_L
A_shoes = c * math.sqrt(G * OL * 3 * (H0_SHOES * 1e3 / MPC)**2 / (8 * math.pi * G))
a_hor_shoes = k_hor * A_shoes
P(f"  H0 lock (fixed Omega_Lambda): a0(kappa=1/2, H0={H0_KMS}) = {a_half_planck:.4e};  a0(kappa={k_hor:.4f}, H0={H0_SHOES}) = {a_hor_shoes:.4e};  ratio {a_hor_shoes/a_half_planck:.4f}")
P(f"     because kappa ratio {k_hor/0.5:.4f} against H0 ratio {H0_KMS/H0_SHOES:.4f}")
om_h2 = OMH2
OL_shoes = 1 - om_h2 / (H0_SHOES / 100)**2
A_shoes_fixom = c * math.sqrt(G * OL_shoes * 3 * (H0_SHOES * 1e3 / MPC)**2 / (8 * math.pi * G))
k_fixom = a_half_planck / A_shoes_fixom
P(f"  variant, Omega_m h^2 held instead: Omega_Lambda(SH0ES) = {OL_shoes:.3f}; the coefficient that reproduces a0(1/2, Planck) is {k_fixom:.4f} ({(k_fixom/k_hor-1)*100:+.1f}% from {k_hor:.4f})")
# ---- a0 as an H0 meter at kappa = 1/2, SELF-CONSISTENTLY: the Hubble-flow distances are rebuilt at the H0 being solved for.
#      A: a0_A(h) = a0_A(67.4) (h/67.4)^(2 q_HF) and a0(1/2, h) ~ h  =>  h = 67.4 (kappa_A / 1/2)^(1/(1 - 2 q_HF)).
#      B: solved directly, kappa_B(h) = shape fit with D_HF x 73/h, over c sqrt(G rho_Lambda(h)), = 1/2.
hA = H0_KMS * (kA / 0.5)**(1 / (1 - 2 * q_HF)); shA = hA * (sA / kA) / (1 - 2 * q_HF)
_kBh = lambda h_: fit_shape(*load_sparc(UD=UD_C, UB=UB_C, hf=H0_SPARC_HF / h_)[:3]) / A_L_at(h_, "OL")
hB = brentq(lambda h_: _kBh(h_) - 0.5, 50.0, 110.0, xtol=1e-3)
_dB = (math.log(_kBh(hB * 1.02)) - math.log(_kBh(hB / 1.02))) / (2 * math.log(1.02)); shB = hB * (sB / 0.5) / abs(_dB)
P(f"  a0 as an H0 meter at kappa = 1/2, self-consistent: A: H0 = {hA:.1f} +/- {shA:.1f};  B: H0 = {hB:.1f} +/- {shB:.1f} (d ln kappa_B/d ln h = {_dB:+.2f})")
sep = 1 - k_hor / 0.5
P(f"  separation of 1/2 from {k_hor:.4f}: {sep*100:.1f}% in a0 = {abs(math.log10(k_hor/0.5)):.3f} dex;  3 sigma needs {sep/3*100:.1f}% on a0")
OUT["S3"] = dict(candidates=ctab, floor=floor, f_star=fstar, kappa_horizon=k_hor, kappa_crit_half=k_crit_half, lock_ratio=a_hor_shoes / a_half_planck, lnLR=LNLR, sep_percent=sep * 100,
                 kappa_fixed_omh2=k_fixom, OL_shoes=OL_shoes, H0_meter=dict(A=(hA, shA), B=(hB, shB), dlnkB_dlnh=_dB), box_A=BOX_A, box_B=BOX_B, box_C=BOX_C,
                 meas=[(m[0], m[1], m[2]) for m in MEAS], published=PUBT, desmond_pulls=DES_pulls, q_HF=q_HF)
check("S3a the closed-form floor equals the numerical minimum", abs(floor - floor_num) < 1e-6, f"{floor*100:.2f}%")
check("S3b the H0 lock: the two (kappa, H0) pairs predict the same a0 to better than 0.5%", abs(a_hor_shoes / a_half_planck - 1) < 5e-3,
      f"{(a_hor_shoes/a_half_planck - 1)*100:+.2f}%")
check("S3c 1/2 is inside 1.5 sigma of all three estimators; Milgrom-1999's 2cH_Lambda is outside 5 sigma of all three",
      all(abs(p) < 1.5 for p in ctab[1]["pulls"]) and all(abs(p) > 5 for p in ctab[5]["pulls"]))
check("S3d the data do not single out 1/2: at least three candidates lie within 2.2 sigma of all three estimators",
      sum(all(abs(p) < 2.2 for p in r["pulls"]) for r in ctab) >= 3, f"{sum(all(abs(p) < 2.2 for p in r['pulls']) for r in ctab)} candidates inside 2.2 sigma of all three")
check("S3i on either common footing Milgrom's 2pi form is at least as close to estimators A and C as 1/2 is (cH_Lambda/2pi vs 1/2 on rho_Lambda; cH0/2pi vs (1/2)c sqrt(G rho_crit))",
      all(abs((k_hor - m[1]) / m[2]) <= abs((0.5 - m[1]) / m[2]) and abs((k_hor / math.sqrt(OL) - m[1]) / m[2]) <= abs((k_crit_half - m[1]) / m[2]) for m in (MEAS[0], MEAS[2])),
      "; ".join(f"{m[0][0]}: {(k_hor-m[1])/m[2]:+.2f} vs {(0.5-m[1])/m[2]:+.2f}, {(k_hor/math.sqrt(OL)-m[1])/m[2]:+.2f} vs {(k_crit_half-m[1])/m[2]:+.2f}" for m in (MEAS[0], MEAS[2])))
# ---- the three kappa tables, generated here and checked against the manuscript (typeset = computed)
def _fp(p_): return f"${p_:+.0f}$" if abs(p_) >= 9.95 else ("$0.0$" if abs(p_) < 0.05 else f"${p_:+.1f}$")
_CNAMES = [r"$cH_\Lambda/2\pi$ \citep{Milgrom2020}", r"$\tfrac12c\sqrt{G\rho_\Lambda}$ (working value)", r"$cH_0/2\pi$ \citep{Milgrom2020}",
           r"$cH_0/6$ \citep{Verlinde2017}", r"$cH_\Lambda$ (Unruh $=$ de Sitter temperature)", r"$2cH_\Lambda$ \citep{Milgrom1999}"]
CAND_ROWS = [f"{nm} & {r_['kappa']:.3f} & " + " & ".join(_fp(p_) for p_ in r_["pulls"]) + r" \\" for nm, r_ in zip(_CNAMES, ctab)]
CAND_ROWS[4] = CAND_ROWS[4].replace(f"{ctab[4]['kappa']:.3f}", f"{ctab[4]['kappa']:.2f}"); CAND_ROWS[5] = CAND_ROWS[5].replace(f"{ctab[5]['kappa']:.3f}", f"{ctab[5]['kappa']:.2f}")
CAND_ROWS.append(r"$\tfrac12c\sqrt{G\rho_{\rm crit}}$ & " + f"{k_crit_half:.3f} & " + " & ".join(_fp((k_crit_half - m[1]) / m[2]) for m in MEAS) + r" \\")
CONV_ROWS = [f"{lab} & {bx['R1']:.3f} & {bx['MIXED']:.3f} & {bx['R2a']:.3f} & {bx['R2b']:.3f}" + r" \\" for lab, bx in
             (("A: Tully--Fisher intercept", BOX_A), ("B: shape only", BOX_B), ("C: profile likelihood", BOX_C))]
_PNAMES = [r"\citet{McGaugh2016}", r"\citet{Desmond2023}", r"\citet{Varasteanu2025}", r"\citet{Varasteanu2025}", r"\citet{Varasteanu2026}"]
PUB_ROWS = [f"{nm} & {r_['sample']} & {r_['upsilon']} & ${r_['a0']/1e-10:.2f}\\pm{r_['err']/1e-10:.2f}$ & ${r_['kappa_L']:.2f}\\pm{r_['s_L']:.2f}$ & ${r_['kappa_C']:.2f}\\pm{r_['s_C']:.2f}$" + r" \\"
            for nm, r_ in zip(_PNAMES, PUBT)]
for lab, (nm_, k_, s_) in zip(("estimator A", "estimator B", "estimator C"), MEAS):
    PUB_ROWS.append(f"this paper, {lab} & SPARC & " + {"estimator A": r"0.5--0.7 (budget)", "estimator B": r"grid, Table~\ref{tab:shape}", "estimator C": r"free per galaxy"}[lab]
                    + f" & ${k_*A_L/1e-10:.2f}\\pm{s_*A_L/1e-10:.2f}$ & ${k_:.2f}\\pm{s_:.2f}$ & ${k_*A_L/A_C:.2f}\\pm{s_*A_L/A_C:.2f}$" + r" \\")
P("  rows of the candidate table (as typeset):"); [P("     " + r_) for r_ in CAND_ROWS]
P("  rows of the convention table (as typeset):"); [P("     " + r_) for r_ in CONV_ROWS]
P("  rows of the published-values table (as typeset):"); [P("     " + r_) for r_ in PUB_ROWS]
_tex3 = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
def _rows3(label):
    if r"\label{" + label + "}" not in _tex3: return []
    t_ = _tex3[_tex3.index(r"\label{" + label + "}"):]; t_ = t_[t_.index(r"\midrule") + len(r"\midrule"):t_.index(r"\bottomrule")]
    return [l_.strip() for l_ in t_.strip().splitlines() if l_.strip() and not l_.strip().startswith(r"\midrule")]
check("S3j the candidate, convention and published-values tables in the manuscript are exactly the computed ones",
      _rows3("tab:cands") == CAND_ROWS and _rows3("tab:conv") == CONV_ROWS and _rows3("tab:pub") == PUB_ROWS,
      f"{len(_rows3('tab:cands'))}/{len(_rows3('tab:conv'))}/{len(_rows3('tab:pub'))} rows typeset", kind="identity")
# v3.3 (CFG310 #6, #14): the abstract quotes kappa on both footings, and stays within 250 words on both counts used by make_upload_bundle.py
_ab3 = _tex3[_tex3.index(r"\begin{abstract}") + len(r"\begin{abstract}"):_tex3.index(r"\end{abstract}")].strip()
_crit_pulls = [(k_crit_half - m[1]) / m[2] for m in MEAS]
AB_WORDS = (len(_ab3.split()), len(re.sub(r"\\[a-zA-Z]+", "", re.sub(r"\$[^$]*\$", " X ", _ab3)).split()))
OUT["abstract_words"] = dict(plain=AB_WORDS[0], math_spans_as_words=AB_WORDS[1])
check("S3k the abstract carries both footings (on the critical density 1/2 lies 2.1-2.2 sigma from estimators A and C, as Table 6 computes) and is at most 250 words by a plain count and with math spans as words",
      f"{min(_crit_pulls[0], _crit_pulls[2]):.1f}--{max(_crit_pulls[0], _crit_pulls[2]):.1f}$\\sigma$ from two" in _ab3 and max(AB_WORDS) <= 250,
      f"pulls A/C {_crit_pulls[0]:+.2f}/{_crit_pulls[2]:+.2f}; words {AB_WORDS[0]} / {AB_WORDS[1]}", kind="identity")


# ================================================================================================================
head("S4  THE REDSHIFT LAWS, THE ERROR AMPLIFICATION, THE 20:1 RULE")
E = lambda z: np.sqrt(OM * (1 + np.asarray(z, float))**3 + OL)
fN = lambda x: np.log(1 + x) - x / (1 + x)
h = H0_KMS / 100
def c_DM14(M, z):      # Dutton & Maccio (2014), NFW, c200, M in Msun (their Eqs 10-11 with M h /1e12)
    a = 0.520 + (0.905 - 0.520) * np.exp(-0.617 * z**1.21); b = -0.101 + 0.026 * z
    return 10**(a + b * np.log10(M * h / 1e12))
def c_D08(M, z):       # Duffy et al. (2008), c200, full sample
    return 5.71 * (M * h / 2e12)**(-0.084) * (1 + z)**(-0.47)
def ratio_halo(z, cfun=c_DM14, M=1e12, dlogc=0.0):
    c0, cz = cfun(M, 0.0), cfun(M, z) * 10**dlogc
    return E(z)**(4 / 3) * (cz**2 / fN(cz)) / (c0**2 / fN(c0))
def gmax_nfw(M, z, cfun=c_DM14):
    """central (maximum) acceleration of an NFW halo: G M c^2 / (2 f(c) r200^2), r200 from 200 rho_crit(z)."""
    Hz = H0 * E(z); r200 = (G * M * MSUN / (100 * Hz**2))**(1 / 3); cc = cfun(M, z)
    return G * M * MSUN * cc**2 / (2 * fN(cc) * r200**2), r200 / KPC, cc
g0, r0, c0_ = gmax_nfw(1e12, 0.0); g25, r25, c25_ = gmax_nfw(1e12, 2.5)
P(f"  NFW, M200 = 1e12 Msun, z = 0:   r200 = {r0:.0f} kpc, c = {c0_:.2f}, g_max = G M c^2/(2 f(c) r200^2) = {g0:.3e} m s^-2 = {g0/1.2e-10:.2f} x 1.2e-10")
P(f"  NFW, M200 = 1e12 Msun, z = 2.5: r200 = {r25:.0f} kpc, c = {c25_:.2f}, g_max = {g25:.3e} m s^-2;  ratio {g25/g0:.3f}")
DESI = {"Pantheon+": (-0.838, -0.62), "DESY5": (-0.752, -0.86), "Union3": (-0.667, -1.09)}
def dens_map(z, w0, wa): return 0.5 * np.log10((1 + z)**(3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z)))
ztab = (1.0, 2.0, 2.5, 3.0)
P(f"  Delta = log10[a0(z)/a0(0)] in dex")
P(f"  {'z':>4} {'constant':>9} {'H(z)':>8} {'halo DM14':>10} {'[range]':>17} {'halo D08':>9} {'rho_DE map (DESY5)':>19}")
laws = []
for z in ztab:
    lo = min(math.log10(ratio_halo(z, M=M, dlogc=d)) for M in (1e11, 1e12, 1e13) for d in (-0.11, 0, 0.11))
    hi = max(math.log10(ratio_halo(z, M=M, dlogc=d)) for M in (1e11, 1e12, 1e13) for d in (-0.11, 0, 0.11))
    row = dict(z=z, flat=0.0, Hz=float(np.log10(E(z))), dm14=float(np.log10(ratio_halo(z))), dm14_lo=lo, dm14_hi=hi,
               d08=float(np.log10(ratio_halo(z, cfun=c_D08))), desi={k: float(dens_map(z, *v)) for k, v in DESI.items()})
    laws.append(row)
    P(f"  {z:4.1f} {0.0:9.3f} {row['Hz']:8.3f} {row['dm14']:10.3f} [{lo:+.3f},{hi:+.3f}] {row['d08']:9.3f} {row['desi']['DESY5']:19.3f}")
L25 = [r for r in laws if r["z"] == 2.5][0]
LIMBACH_Z = 1.2                                     # the highest redshift of the Tully-Fisher data of Limbach, Psaltis & Ozel (2008)
L12 = dict(Hz=float(np.log10(E(LIMBACH_Z))), halo=float(np.log10(ratio_halo(LIMBACH_Z))))
P(f"  at z = {LIMBACH_Z} (Limbach et al. 2008's limit): H(z) law {L12['Hz']:+.3f} dex, halo law (1e12) {L12['halo']:+.3f} dex; at z = 2 the H(z) factor is {float(E(2.0)):.2f}")
P(f"  z = 2.5 density mapping under DESI DR2 w0-wa: " + ", ".join(f"{k} {v:+.3f}" for k, v in L25["desi"].items()) + "  (NOT this paper's prediction; shown for scale)")
P(f"  check of the gmax route against the closed law: ratio {g25/g0:.4f} vs E^(4/3) c^2/f(c) ratio {ratio_halo(2.5):.4f}")
ln20 = math.log(20.0)
P(f"  error amplification of the kernel inversion  a0 = g_bar/y,  nu(y) = g_obs/g_bar :")
P(f"     d ln a0 = (1 + 1/n) d ln g_bar - (1/n) d ln g_obs,   n = d ln nu/d ln y")
P(f"  {'y = g_bar/a0':>13} {'n':>8} {'A_bar=|1+1/n|':>14} {'A_obs=1/|n|':>12} {'sigma(log a0) for 0.10 dex M_b, 5% V':>38}")
amp = []
for y in (0.01, 0.1, 0.3, 1.0, 1.7, 3.0, 6.4):
    n = float(n_slope(y)); Ab, Ao = abs(1 + 1 / n), 1 / abs(n)
    s = math.hypot(Ab * 0.10, Ao * 2 * 0.05 / math.log(10))
    amp.append(dict(y=y, n=n, A_bar=Ab, A_obs=Ao, sigma_example=s))
    P(f"  {y:13.2f} {n:8.4f} {Ab:14.2f} {Ao:12.2f} {s:38.3f}")
n_deep = float(n_slope(1e-10))
# ---- how robust is the LambdaCDM side?  (i) halo mass and concentration-mass relation, (ii) a second structural scaling,
#      (iii) the halo-to-halo concentration scatter seen by a SINGLE object
P(f"  the halo-emergent law at z = 2.5 (dex), by halo mass and concentration-mass relation [central-acceleration scaling E^(4/3) c^2/f(c)]:")
massdep = {}
for M in (1e11, 1e12, 1e13):
    massdep[f"{M:.0e}"] = dict(dm14=float(np.log10(ratio_halo(2.5, M=M))), d08=float(np.log10(ratio_halo(2.5, cfun=c_D08, M=M))))
    P(f"     M200 = {M:.0e}:  Dutton-Maccio {massdep[f'{M:.0e}']['dm14']:+.3f}   Duffy {massdep[f'{M:.0e}']['d08']:+.3f}")
P(f"  range of the halo-emergent law over M200 = 1e11-1e13 and the two concentration-mass relations (median concentrations):")
hrange = {}
for z in ztab:
    v = [float(np.log10(ratio_halo(z, cfun=cf, M=M))) for cf in (c_DM14, c_D08) for M in (1e11, 1e12, 1e13)]
    hrange[z] = (min(v), max(v)); P(f"     z = {z}: [{min(v):+.3f}, {max(v):+.3f}]")
def ratio_vmax(z, cfun=c_DM14, M=1e12):
    """second structural scaling: the Tully-Fisher-type ratio V_max^4/(G M) at fixed baryon-to-halo mass ratio.
    V_200 = (10 G M H)^(1/3), V_max^2 = 0.216 V_200^2 c/f(c)  =>  V_max^4/M ~ E^(4/3) [c/f(c)]^2 at fixed M."""
    c0, cz = cfun(M, 0.0), cfun(M, z)
    return E(z)**(4 / 3) * (cz / fN(cz))**2 / (c0 / fN(c0))**2
vm25 = float(np.log10(ratio_vmax(2.5)))
P(f"  second structural scaling, V_max^4/(G M) at fixed M_b/M_halo:  {10**vm25:.3f} = {vm25:+.3f} dex at z = 2.5  (a larger M_b/M_halo at high z lowers it one-for-one)")
dc = 0.11                                           # halo-to-halo scatter in log10 c (Dutton & Maccio 2014)
s_int = 0.034                                       # intrinsic scatter of the relation in log g_obs (Desmond 2023)
P(f"  intrinsic scatter of the relation ({s_int} dex in g_obs) amplified through the inversion: " +
  ", ".join(f"y = {a['y']}: {s_int*a['A_obs']:.3f} dex" for a in amp[:3]))
s_intr_d = s_int * amp[2]["A_obs"]
# ---- (v3.1) THE GATE AND THE HALO MASS IT SELECTS.  g_bar(R_out) < 0.3 a0 with a0 = the working value 9.36e-11 and
#      g_bar = Gamma G M_b / R^2 (Gamma = 1.2).  A gate-passing disc's V_f follows from equation (btfr); at z = 2.5 its halo has
#      V_200 = V_f / r with r = V_f/V_200 = 1.0-1.2 (an NFW V_max/V_200 at c ~ 4 is ~1.1), so M_200 = V_200^3 / (10 G H(z)).
#      The decision value is the Dutton-Maccio halo law at THAT mass (central example, r = 1.1), not at 1e12 Msun.
GAM = 1.2                                            # disc-versus-point-mass factor at the last measured radius (SPARC median 1.19)
sig_gate = 0.3 * a0_L / (GAM * G) * KPC**2 / MSUN    # Msun per kpc^2:  M_b < sig_gate R^2
sig_gate_1e10 = 0.3 * 1.0e-10 / (GAM * G) * KPC**2 / MSUN
gate = []
for Mb, R in ((2e9, 4.0), (5e9, 6.0), (1e10, 8.0)):
    yb = GAM * G * Mb * MSUN / (R * KPC)**2 / a0_L
    Vf = (float(nu(yb))**2 * yb * GAM * G * Mb * MSUN * a0_L)**0.25 / 1e3
    gate.append(dict(Mb=Mb, R_kpc=R, y=yb, Vf_kms=Vf))
P(f"  the gate g_bar < 0.3 a0 (a0 = {a0_L:.3e}, Gamma = {GAM}) reads M_b < {sig_gate:.3e} (R/kpc)^2 Msun (with a0 = 1.0e-10: {sig_gate_1e10:.3e}); examples: " +
  "; ".join(f"M_b = {g_['Mb']:.0e}, R = {g_['R_kpc']:.0f} kpc -> y = {g_['y']:.2f}, V_f = {g_['Vf_kms']:.0f} km/s" for g_ in gate))
VRAT = (1.0, 1.1, 1.2)
def m200_of_vf(Vf_kms, z, r): return (Vf_kms * 1e3 / r)**3 / (10 * G * H0 * float(E(z))) / MSUN
GH = []
for g_ in gate:
    for r in VRAT:
        M_ = m200_of_vf(g_["Vf_kms"], 2.5, r)
        GH.append(dict(Mb=g_["Mb"], Vf=g_["Vf_kms"], r=r, M200=M_, dm14=float(np.log10(ratio_halo(2.5, M=M_))), d08=float(np.log10(ratio_halo(2.5, cfun=c_D08, M=M_)))))
        P(f"     M_b {g_['Mb']:.0e}, V_f {g_['Vf_kms']:5.1f} km/s, V_f/V_200 {r}: M_200(z = 2.5) = {M_:.2e} Msun -> halo law Dutton-Maccio {GH[-1]['dm14']:+.3f}, Duffy {GH[-1]['d08']:+.3f}")
M_GATE = m200_of_vf(gate[1]["Vf_kms"], 2.5, 1.1)
DELTA_GATE = float(np.log10(ratio_halo(2.5, M=M_GATE))); DELTA_GATE_D08 = float(np.log10(ratio_halo(2.5, cfun=c_D08, M=M_GATE)))
GATE_M = (min(x["M200"] for x in GH), max(x["M200"] for x in GH)); GATE_D = (min(x["dm14"] for x in GH), max(x["dm14"] for x in GH))
GATE_D08 = (min(x["d08"] for x in GH), max(x["d08"] for x in GH))
s_halo_obj = 0.5 * (math.log10(ratio_halo(2.5, M=M_GATE, dlogc=+dc)) - math.log10(ratio_halo(2.5, M=M_GATE, dlogc=-dc)))
s_halo_1e12 = 0.5 * (math.log10(ratio_halo(2.5, dlogc=+dc)) - math.log10(ratio_halo(2.5, dlogc=-dc)))
P(f"  DECISION VALUE: central gate example (M_b 5e9, V_f {gate[1]['Vf_kms']:.0f} km/s, V_f/V_200 = 1.1): M_200 = {M_GATE:.2e} Msun -> Delta_halo(2.5) = {DELTA_GATE:+.3f} (Dutton-Maccio);"
  f" Duffy at the same mass {DELTA_GATE_D08:+.3f} (concentration-mass relation spread {DELTA_GATE_D08-DELTA_GATE:+.3f} dex)")
P(f"  gate range: M_200 = {GATE_M[0]:.1e}-{GATE_M[1]:.1e} Msun; Dutton-Maccio {GATE_D[0]:+.3f} to {GATE_D[1]:+.3f}; Duffy {GATE_D08[0]:+.3f} to {GATE_D08[1]:+.3f};"
  f" halo-to-halo scatter (+/-{dc} dex in log c) at the gate mass {s_halo_obj:.3f} dex (at 1e12: {s_halo_1e12:.3f})")
# the gate column of the laws table: the same disc (V_f of the central example, V_f/V_200 = 1.1) at each redshift
for row in laws:
    row["gate"] = float(np.log10(ratio_halo(row["z"], M=m200_of_vf(gate[1]["Vf_kms"], row["z"], 1.1))))
P("  halo law for the gate's central disc at z = " + ", ".join(f"{r_['z']}: {r_['gate']:+.3f}" for r_ in laws))
_r290R8 = _r290["R8"]
_r8ok = all(abs(_r290R8[f"Vf{Vf:.0f}_r{rr}"]["delta_halo"] - float(np.log10(ratio_halo(2.5, M=m200_of_vf(Vf, 2.5, rr))))) < 0.005 for Vf in (85.0, 106.0, 130.0) for rr in (1.0, 1.2))
# ---- THE DESIGN.  N galaxies each give Delta_i = log10[a0_hat/a0(0)].  Constancy: Delta_i ~ N(0, s0^2); the halo law: N(Delta, s1^2),
#      s0^2 = sigma_m^2 + sigma_int^2, s1^2 = s0^2 + sigma_h^2.  Two SHARED terms enter as covariance b J (J = matrix of ones):
#      a baryonic-mass calibration error shared by the sample (b = (A_bar delta_c)^2, under both hypotheses) and the uncertainty
#      of the LambdaCDM prediction itself (b = sigma_sys^2, under the halo law only: a composite hypothesis with a Gaussian prior on
#      Delta).  For covariance a I + b J the inverse and determinant are closed-form, so the exact ln B and the expected ln B
#      (a Kullback-Leibler divergence) are computed for any N.  'Odds' below = exp(expected ln B), the smaller of the two truths;
#      the PROBABILITY of reaching 20:1 and of evidence pointing the wrong way come from Monte Carlo.
def _kl_cs(N, mu, aP, bP, aQ, bQ):
    lp, lq = aP + N * bP, aQ + N * bQ
    return 0.5 * ((N - 1) * (aP / aQ - 1 - math.log(aP / aQ)) + (lp / lq - 1 - math.log(lp / lq)) + N * mu**2 / lq)
def elnB_design(N, sm, mu, s_sys=0.0, s_c=0.0, s_h=None, s_i=None):
    s_h = s_halo_obj if s_h is None else s_h; s_i = s_intr_d if s_i is None else s_i
    a0v = sm**2 + s_i**2; a1v = a0v + s_h**2; b0, b1 = s_c**2, s_c**2 + s_sys**2
    return _kl_cs(N, mu, a0v, b0, a1v, b1), _kl_cs(N, mu, a1v, b1, a0v, b0)
def _lnL_cs(x, m, a, b):
    N_ = x.shape[1]; d_ = x - m; S_ = d_.sum(1)
    return -0.5 * (np.einsum("ij,ij->i", d_, d_) - b * S_**2 / (a + N_ * b)) / a - 0.5 * ((N_ - 1) * math.log(a) + math.log(a + N_ * b))
def mc_design(N, sm, mu, s_sys=0.0, s_c=0.0, s_h=None, s_i=None, M=40000, seed=7):
    s_h = s_halo_obj if s_h is None else s_h; s_i = s_intr_d if s_i is None else s_i
    rng_ = np.random.default_rng(seed); a0v = sm**2 + s_i**2; a1v = a0v + s_h**2; b0, b1 = s_c**2, s_c**2 + s_sys**2; out = {}
    x = rng_.normal(0, math.sqrt(a0v), (M, N)) + (rng_.normal(0, s_c, (M, 1)) if s_c > 0 else 0.0)
    lb = _lnL_cs(x, 0.0, a0v, b0) - _lnL_cs(x, mu, a1v, b1)
    out["const"] = dict(mean=float(lb.mean()), p20=float((lb > ln20).mean()), pwrong=float((lb < 0).mean()))
    x = rng_.normal(0, math.sqrt(a1v), (M, N)) + mu + (rng_.normal(0, s_c, (M, 1)) if s_c > 0 else 0.0) + (rng_.normal(0, s_sys, (M, 1)) if s_sys > 0 else 0.0)
    lb = _lnL_cs(x, mu, a1v, b1) - _lnL_cs(x, 0.0, a0v, b0)
    out["halo"] = dict(mean=float(lb.mean()), p20=float((lb > ln20).mean()), pwrong=float((lb < 0).mean()))
    return out
def odds_design(N, sm, mu, **kw): return math.exp(min(min(elnB_design(N, sm, mu, **kw)), 700.0))
def n_expected20(sm, mu, **kw): return next(N for N in range(1, 2000) if odds_design(N, sm, mu, **kw) >= 20)
def n_power(sm, mu, target=0.9, **kw):
    def pw(N):
        m_ = mc_design(N, sm, mu, M=20000, **kw); return min(m_["const"]["p20"], m_["halo"]["p20"])
    lo, hi = 1, 8
    while pw(hi) < target: lo, hi = hi, hi * 2
    while hi - lo > 1:
        mid = (lo + hi) // 2; lo, hi = (mid, hi) if pw(mid) < target else (lo, mid)
    return hi
# (a) the Monte Carlo against the closed form, and against the CFG290 referee's R3 at the old decision value (1e12 Msun)
_r3 = _r290["R3"]; MCCHK = []
for N_, sm_ in ((2, 0.10), (3, 0.13), (4, 0.20)):
    e_ = elnB_design(N_, sm_, L25["dm14"], s_h=s_halo_1e12); m_ = mc_design(N_, sm_, L25["dm14"], s_h=s_halo_1e12, M=200000)
    MCCHK.append((abs(m_["const"]["mean"] / e_[0] - 1), abs(m_["halo"]["mean"] / e_[1] - 1), abs(m_["const"]["p20"] - _r3[f"N{N_}_s{sm_}"]["mc"]["const"]["p20"]), abs(m_["halo"]["p20"] - _r3[f"N{N_}_s{sm_}"]["mc"]["halo"]["p20"])))
P("  Monte Carlo vs closed form and vs CFG290 R3 (Delta = 0.328, 1e12 Msun): max |MC/closed - 1| " + f"{max(max(x[0], x[1]) for x in MCCHK):.4f}; max |P(20:1) - R3| {max(max(x[2], x[3]) for x in MCCHK):.3f}")
# (b) the design at the gated decision value: N for EXPECTED 20:1 and N for 20:1 WITH 90 PER CENT PROBABILITY, without and with the
#     concentration-mass relation carried as a shared prior width sigma_sys on the halo law's Delta
SIGSYS = (0.0, 0.10, 0.20); SMS = (0.10, 0.13, 0.20)
DESIGN = {}
for sm in SMS:
    for ss in SIGSYS:
        Ne = n_expected20(sm, DELTA_GATE, s_sys=ss); Np = n_power(sm, DELTA_GATE, s_sys=ss)
        mcN = mc_design(Ne, sm, DELTA_GATE, s_sys=ss, M=100000)
        DESIGN[(sm, ss)] = dict(N_expected=Ne, N_power90=Np, odds_at_Ne=odds_design(Ne, sm, DELTA_GATE, s_sys=ss),
                                p20_at_Ne=(mcN["const"]["p20"], mcN["halo"]["p20"]), pwrong_at_Ne=(mcN["const"]["pwrong"], mcN["halo"]["pwrong"]))
        P(f"  sigma_m {sm:.2f}, sigma_sys {ss:.2f}: expected 20:1 needs N = {Ne:3d} (odds {DESIGN[(sm, ss)]['odds_at_Ne']:.0f}:1; there P(20:1) = {mcN['const']['p20']:.2f} const / {mcN['halo']['p20']:.2f} halo,"
          f" P(wrong way) = {mcN['const']['pwrong']:.3f} / {mcN['halo']['pwrong']:.3f});  20:1 with 90 per cent probability needs N = {Np}")
one013 = odds_design(1, 0.13, DELTA_GATE); four020 = odds_design(4, 0.20, DELTA_GATE); two010 = odds_design(2, 0.10, DELTA_GATE); three013 = odds_design(3, 0.13, DELTA_GATE)
mc4 = mc_design(4, 0.20, DELTA_GATE, M=100000)
P(f"  at the gated value: one object at 0.13 dex {one013:.1f}:1; two at 0.10 {two010:.1f}:1; three at 0.13 {three013:.1f}:1; four at 0.20 {four020:.1f}:1 (P(20:1) {mc4['const']['p20']:.2f} / {mc4['halo']['p20']:.2f}) -- the v3 designs")
sig_halo = DELTA_GATE / math.sqrt(2 * ln20); sig_Hz = L25["Hz"] / math.sqrt(2 * ln20)
P(f"  idealised one-pair rule sigma <= Delta/sqrt(2 ln 20): gated halo law {sig_halo:.3f} dex; H(z) {sig_Hz:.3f} dex (P(20:1) = 0.50 and P(wrong way) = {0.5*(1+math.erf(-ln20/math.sqrt(2*ln20)/math.sqrt(2))):.2f} at that sigma)")
# the sample-mean error of the recommended design (Fig. 4 bars): N for expected 20:1 at 0.20 dex
N_REC = DESIGN[(0.20, 0.0)]["N_expected"]
SE_REC = (math.sqrt((0.20**2 + s_intr_d**2) / N_REC), math.sqrt((0.20**2 + s_intr_d**2 + s_halo_obj**2) / N_REC))
P(f"  recommended design N = {N_REC} at 0.20 dex: standard error of the sample mean {SE_REC[0]:.3f} dex (constancy) / {SE_REC[1]:.3f} dex (halo law)")
# ---- measurement budgets.  Lensing conserves surface density, so g_bar is magnification-free while g_obs = V^2/R ~ mu^(1/2):
#      d log a0 = A_obs [2 dV/V / ln10  (+)  0.5 dlog mu]  (+)  A_bar dlog M_b     (quadrature), evaluated at y = 0.2
nb = float(n_slope(0.2)); Aob, Aba = 1 / abs(nb), 1 / abs(nb) - 1
P(f"  measurement budgets at y = 0.2 (A_obs = {Aob:.2f}, A_bar = {Aba:.2f}; a magnification error enters as A_obs/2 = {Aob/2:.2f}):")
budgets = []
for dv, dm, dmu in ((0.025, 0.04, 0.04), (0.03, 0.06, 0.05), (0.05, 0.10, 0.06)):
    tot = math.sqrt((Aob * 2 * dv / math.log(10))**2 + (Aba * dm)**2 + (Aob * 0.5 * dmu)**2)
    budgets.append(dict(dV=dv, dlogM=dm, dlogmu=dmu, total=tot))
    P(f"     dV/V = {dv*100:.1f}%, dlog M_b = {dm:.2f}, dlog mu = {dmu:.2f}  ->  sigma_meas = {tot:.3f} dex")
OUT["S4"] = dict(laws=laws, gmax_z0=g0, gmax_z25=g25, r200_z0_kpc=r0, c_z0=float(c0_), sigma_needed_halo=sig_halo, sigma_needed_Hz=sig_Hz, amplification=amp,
                 massdep=massdep, halo_range={str(k): v for k, v in hrange.items()}, budgets=budgets, vmax_scaling_z25=vm25, halo_scatter_single=s_halo_obj,
                 halo_scatter_1e12=s_halo_1e12, intrinsic_amp=[s_int * a["A_obs"] for a in amp[:3]], gate_surface_density=sig_gate, gate_surface_density_a0_1e10=sig_gate_1e10,
                 gate_examples=gate, gate_halos=GH, M_gate=M_GATE, delta_gate=DELTA_GATE, delta_gate_D08=DELTA_GATE_D08, gate_M_range=GATE_M, gate_D_range=GATE_D, gate_D08_range=GATE_D08,
                 design={f"{k_[0]}|{k_[1]}": v_ for k_, v_ in DESIGN.items()}, one_013=one013, two_010=two010, three_013=three013, four_020=four020, four_020_p20=(mc4["const"]["p20"], mc4["halo"]["p20"]),
                 N_rec=N_REC, se_rec=SE_REC)
check("S4j the gate selects low-mass discs: the three examples pass y < 0.3 and rotate at 80-130 km/s", all(g_["y"] < 0.3 and 80 < g_["Vf_kms"] < 130 for g_ in gate),
      ", ".join(f"{g_['Vf_kms']:.0f}" for g_ in gate) + " km/s")
check("S4k the three quoted measurement budgets give 0.10, 0.13 and 0.20 dex", all(abs(b["total"] - t) < 0.006 for b, t in zip(budgets, (0.10, 0.13, 0.20))),
      ", ".join(f"{b['total']:.3f}" for b in budgets))
check("S4c2 the gate's discs sit in M_200 = 3e10-2e11 Msun haloes at z = 2.5, where the Dutton-Maccio law gives +0.15 to +0.27 dex; the halo masses reproduce the CFG290 referee's R8 cases to 0.005 dex",
      2e10 < GATE_M[0] and GATE_M[1] < 2.5e11 and 0.15 < GATE_D[0] and GATE_D[1] < 0.27 and _r8ok, f"M {GATE_M[0]:.1e}-{GATE_M[1]:.1e}; Delta {GATE_D[0]:+.3f} to {GATE_D[1]:+.3f}", kind="model")
check("S4t the concentration-mass relation is a model systematic of ~0.2 dex: at the gate's halo mass Duffy et al. exceed Dutton & Maccio by more than 0.15 dex",
      DELTA_GATE_D08 - DELTA_GATE > 0.15, f"{DELTA_GATE_D08:+.3f} vs {DELTA_GATE:+.3f}", kind="model")
check("S4s the design Monte Carlo reproduces the closed-form expected ln B to 2 per cent and the CFG290 referee's P(20:1) at the old decision value to 0.02",
      max(max(x[0], x[1]) for x in MCCHK) < 0.02 and max(max(x[2], x[3]) for x in MCCHK) < 0.02, kind="model")
check("S4l AGAINST THE v3 DESIGN: at the gated decision value the v3 designs (two at 0.10, three at 0.13, four at 0.20 dex) all fall below 10:1, and four at 0.20 dex reach 20:1 in fewer than half the trials",
      max(two010, three013, four020) < 10 and max(mc4["const"]["p20"], mc4["halo"]["p20"]) < 0.5, f"{two010:.1f}, {three013:.1f}, {four020:.1f}:1", kind="model")
check("S4u AGAINST EXPECTED-ODDS SIZING: at every sigma_m, reaching 20:1 with 90 per cent probability needs at least 1.5 times the N that gives expected 20:1, and at that N the evidence points the wrong way in more than 3 per cent of trials",
      all(DESIGN[(sm, 0.0)]["N_power90"] >= 1.5 * DESIGN[(sm, 0.0)]["N_expected"] and max(DESIGN[(sm, 0.0)]["pwrong_at_Ne"]) > 0.03 for sm in SMS), kind="model")
check("S4v carrying the concentration-mass relation as a shared 0.10 dex prior width on the halo law at least doubles the N for expected 20:1 at 0.20 dex",
      DESIGN[(0.20, 0.10)]["N_expected"] >= 2 * DESIGN[(0.20, 0.0)]["N_expected"], f"{DESIGN[(0.20, 0.0)]['N_expected']} -> {DESIGN[(0.20, 0.10)]['N_expected']}", kind="model")
check("S4h the smallest structural LambdaCDM expectation in the grid, including the gate's lightest haloes, is still a rise of more than 0.15 dex at z = 2.5",
      min(min(min(v.values()) for v in massdep.values()), GATE_D[0]) > 0.15, f"min {min(min(min(v.values()) for v in massdep.values()), GATE_D[0]):+.3f}, max {max(max(max(v.values()) for v in massdep.values()), vm25):+.3f}")
check("S4i AGAINST THE ONE-OBJECT CLAIM: with intrinsic and halo-to-halo scatter included, one object at 0.13 dex gives less than 5:1 at the gated value",
      one013 < 5, f"{one013:.1f}:1")
check("S4a the closed law E^(4/3) c^2/f(c) is the ratio of NFW central accelerations at fixed M200", abs(g25 / g0 / ratio_halo(2.5) - 1) < 1e-9)
check("S4b the central acceleration of a 1e12 Msun NFW halo today is within a factor 2 of the galactic scale 1.2e-10", 0.5 < g0 / 1.2e-10 < 2.0, f"{g0:.2e}")
check("S4c halo-emergent law at z = 2.5 is a factor 2.0-2.3 (0.30-0.36 dex) for the Dutton-Maccio relation at 1e12 Msun (the RC100 comparator)", 0.30 < L25["dm14"] < 0.36, f"{10**L25['dm14']:.3f} = {L25['dm14']:+.3f} dex")
check("S4d the idealised one-pair precision for the gated value is Delta/2.45", abs(sig_halo - DELTA_GATE / 2.448) < 1e-3, f"{sig_halo:.3f}")
check("S4e deep limit n -> -1/2 (a0 = g_obs^2/g_bar) and the amplification at y = 0.3 stays below 1.7 (baryons) and 2.7 (kinematics)",
      abs(n_deep + 0.5) < 1e-4 and amp[2]["A_bar"] < 1.7 and amp[2]["A_obs"] < 2.7, f"A_bar = {amp[2]['A_bar']:.2f}, A_obs = {amp[2]['A_obs']:.2f}")
check("S4f at the accelerations of published z > 0.5 samples (1.7-6.4 a0) the kinematic amplification is 4-9", 4 < amp[4]["A_obs"] < 5 and 8.5 < amp[6]["A_obs"] < 9.5,
      f"{amp[4]['A_obs']:.1f} - {amp[6]['A_obs']:.1f}")
check("S4g even the density mapping under DESI w0-wa stays within 0.15 dex of zero at z = 2.5, far from the halo and H(z) laws",
      all(abs(v) < 0.15 for v in L25["desi"].values()))

# ---- THE SAME DESIGN WITH A COMMON-MODE CALIBRATION OF THE BARYONIC MASS.  A calibration shared by the whole sample (an alpha_CO
#      scale, a stellar-mass zero point) does not average down: sigma_C = A_bar delta_c enters both hypotheses as b J.  Along the
#      direction of the mean the variance is s^2/N + sigma_C^2, so the sample means cannot separate by more than Delta/sigma_C.
def expected_lnB_independent(N, s_meas, mu, s_intr, s_h):
    s0 = math.hypot(s_meas, s_intr); s1 = math.hypot(s0, s_h)
    return (N * (math.log(s1 / s0) - 0.5 + (s0**2 + mu**2) / (2 * s1**2)), N * (math.log(s0 / s1) - 0.5 + (s1**2 + mu**2) / (2 * s0**2)))
_red = max(abs(a - b) for N in (1, 2, 3, 4, 10) for sm in (0.08, 0.10, 0.13, 0.20)
           for a, b in zip(elnB_design(N, sm, DELTA_GATE), expected_lnB_independent(N, sm, DELTA_GATE, s_intr_d, s_halo_obj)))
N_A, N_B = DESIGN[(0.20, 0.0)]["N_expected"], DESIGN[(0.10, 0.0)]["N_expected"]
P(f"  common-mode calibration: delta_c shared by every galaxy, s_C = A_bar delta_c at y = 0.2 (A_bar = {Aba:.2f}); designs N = {N_A} at 0.20 dex and N = {N_B} at 0.10 dex;"
  f" the shared-term formula reduces to the independent one at s_C = 0 to {_red:.1e}")
SHARED = []
for dcal in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
    sc = Aba * dcal
    oA = odds_design(N_A, 0.20, DELTA_GATE, s_c=sc); oB = odds_design(N_B, 0.10, DELTA_GATE, s_c=sc)
    pA = mc_design(N_A, 0.20, DELTA_GATE, s_c=sc, M=40000); pA = min(pA["const"]["p20"], pA["halo"]["p20"])
    oz = odds_design(N_A, 0.20, L25["Hz"], s_c=sc, s_h=0.0)
    zh = DELTA_GATE / sc if sc > 0 else float("inf"); zz_ = L25["Hz"] / sc if sc > 0 else float("inf")
    SHARED.append(dict(delta_c=dcal, s_C=sc, halo_NA_020=oA, halo_NA_020_p20=pA, halo_NB_010=oB, Hz_NA_020=oz, halo_mean_limit=zh, Hz_mean_limit=zz_))
    P(f"  delta_c {dcal:4.2f}  s_C {sc:5.3f}:  halo N={N_A} @0.20 {oA:9.1f}:1 (P(20:1) {pA:.2f});  halo N={N_B} @0.10 {oB:9.1f}:1;  H(z) N={N_A} @0.20 {min(oz, 1e30):10.3g}:1;  Delta/s_C {zh:.2f} / {zz_:.2f}")
dc_need_halo = DELTA_GATE / math.sqrt(2 * ln20) / Aba; dc_need_Hz = L25["Hz"] / math.sqrt(2 * ln20) / Aba
P(f"  20:1 from the sample means alone (any N; expected ln B -> Delta^2/(2 s_C^2)) needs delta_c <= {dc_need_halo:.3f} dex (gated halo law) and <= {dc_need_Hz:.3f} dex (H(z) law)")
# v3.3 (CFG310 #5): the eight-disc design and the 0.06 dex limit are not jointly sufficient.  The N that reaches expected 20:1 against
# the gated halo law at 0.20 dex, as a function of the shared calibration delta_c (and with sigma_sys = 0.10 on top), from the same KL
# computation as Table 12; cross-checked against the CFG310 referee's independent re-implementation (cfg310_shared_calibration_N.out)
NDC = {dc_: n_expected20(0.20, DELTA_GATE, s_c=Aba * dc_) for dc_ in (0.0, 0.02, 0.03, 0.04, 0.05, 0.06)}
ODC8 = {dc_: odds_design(N_A, 0.20, DELTA_GATE, s_c=Aba * dc_) for dc_ in (0.04, 0.05, 0.06)}
NDC_SYS = {dc_: n_expected20(0.20, DELTA_GATE, s_c=Aba * dc_, s_sys=0.10) for dc_ in (0.05,)}
P(f"  N for expected 20:1 at 0.20 dex against the gated halo law vs the shared calibration: " + ", ".join(f"delta_c {k_:.2f} -> {v_}" for k_, v_ in NDC.items())
  + f";  {N_A} discs give " + ", ".join(f"{v_:.1f}:1 at {k_:.2f}" for k_, v_ in ODC8.items()) + f";  delta_c 0.05 with sigma_sys 0.10: N = {NDC_SYS[0.05]}")
_r310N = {float(m_.group(1)): int(m_.group(2)) for m_ in re.finditer(r"delta_c (0\.\d\d): odds at .*?smallest scanned N reaching 20:1: (\d+)",
                                                                      open(os.path.join(CFG, "CFG310_second_referee", "cfg310_shared_calibration_N.out")).read())}
OUT["S4"]["N20_vs_delta_c"] = {f"{k_:.2f}": v_ for k_, v_ in NDC.items()}; OUT["S4"]["odds_NA_vs_delta_c"] = {f"{k_:.2f}": v_ for k_, v_ in ODC8.items()}
OUT["S4"]["N20_delta_c005_sys010"] = NDC_SYS[0.05]
check("S4w AGAINST THE DESIGN (CFG310 #5): eight discs at 0.20 dex reach expected 20:1 only for an exact shared calibration; at delta_c = 0.05 and 0.06 dex about 20 and 34 discs are needed (the referee's independent re-implementation, with its inputs rounded to 0.09/0.13/1.52, agrees within 2 discs: 21 and 36)",
      NDC[0.0] == N_A and ODC8[0.06] < 6 and 18 <= NDC[0.05] <= 23 and 30 <= NDC[0.06] <= 40 and all(abs(NDC[k_] - _r310N[k_]) <= 2 for k_ in NDC),
      ", ".join(f"{k_:.2f}:{v_} (ref {_r310N.get(k_)})" for k_, v_ in NDC.items()), kind="model")
_txd = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
_qd = [f"eight galaxies at 0.20 dex give {ODC8[0.04]:.1f}:1 at $\\delta_c=0.04$ dex and {ODC8[0.06]:.1f}:1 at 0.06 dex", f"need {NDC[0.04]}, {NDC[0.05]} and {NDC[0.06]} galaxies at $\\delta_c=0.04$, 0.05 and 0.06 dex",
       f"({NDC_SYS[0.05]} at 0.05 dex if the concentration", f"{NDC[0.05]} or {NDC[0.06]} if it is shared to 0.05 or 0.06 dex"]
check("S4x the text (Section 4.4, the abstract) quotes the N for 20:1 against the shared calibration as computed", all(q_ in _txd for q_ in _qd), "; ".join(q_ for q_ in _qd if q_ not in _txd) or "all present", kind="identity")
def _gas_to_bary(dgas, fg=0.5): return math.log10(1 - fg + fg * 10**dgas)
GASB = {d: (_gas_to_bary(d), _gas_to_bary(-d)) for d in (0.2, 0.7)}
P(f"  a gas-mass scale error of +/-0.2 and +/-0.7 dex at a gas fraction of 0.5 is " +
  "; ".join(f"{d}: {a:+.3f}/{b:+.3f} dex" for d, (a, b) in GASB.items()) + " on the baryonic mass")
OUT["S4"]["shared"] = SHARED; OUT["S4"]["delta_c_needed"] = dict(halo=dc_need_halo, Hz=dc_need_Hz); OUT["S4"]["gas_to_baryon"] = {str(k): v for k, v in GASB.items()}
OUT["S4"]["shared_designs"] = dict(N_A=N_A, N_B=N_B)

# ---- (v3) THE CONDITIONING OF a0 WITH THE MASS SCALE FREE (CFG240, re-computed here for the paper's kernel).  One calibration
#      factor f on g_bar, the same at every point: g_obs = f g nu(f g/a0).  In log10 units the Fisher rows are (1 - b, b) with
#      b = d log g_obs / d log a0 = -n(y) = sqrt(y)/(2 (e^sqrt(y) - 1)), y = f g/a0.  Deep points (b -> 1/2) and Newtonian points
#      (b -> 0) alone leave (f, a0) degenerate; the design must span both.
def fisher_sigma_a0(ys, sig):
    b = -n_slope(np.asarray(ys, float)); R_ = np.c_[1 - b, b]
    F = R_.T @ R_ / sig**2
    return float(math.sqrt(np.linalg.inv(F)[1, 1]))
def break_even(ymin, N, sig, target=0.1, cap=1e4, step=50):
    grid = ymin * 10**(np.arange(1, int(step * math.log10(cap / ymin)) + 1) / step)
    sv = np.array([fisher_sigma_a0(ymin * (ym / ymin)**(np.arange(N) / (N - 1)), sig) for ym in grid])
    ok_ = sv < target
    stable = None
    for i in range(len(grid)):
        if ok_[i:].all(): stable = float(grid[i]); break
    return stable, float(sv.min()), float(grid[int(np.argmin(sv))])
BE = {ym: break_even(ym, 20, 0.1) for ym in (1e-3, 1e-2, 1e-1)}
for ym, (st, smin, yarg) in BE.items():
    P(f"  Fisher, f free, N = 20 points at 0.1 dex, log-uniform from y = {ym:g}: " + (f"sigma(log a0) < 0.1 dex for every y_max >= {st:.1f}" if st else "no stable break-even below y_max = 1e4") +
      f"; minimum {smin:.4f} dex at y_max = {yarg:.0f}")
_rng4 = np.random.default_rng(240); _worst = np.inf
for _ in range(4000):
    Nd = int(_rng4.integers(2, 60)); bb = _rng4.uniform(0, 0.5, Nd); R_ = np.c_[1 - bb, bb]; F = R_.T @ R_ / 0.1**2
    if np.linalg.det(F) > 1e-9: _worst = min(_worst, math.sqrt(np.linalg.inv(F)[1, 1]) / (3 * 0.1 / math.sqrt(Nd)))
P(f"  the floor sigma(log a0) >= 3 sigma/sqrt(N) (CFG240 T4, any design with b in [0, 1/2]): smallest ratio over 4000 random designs {_worst:.4f}")
_cfg240 = [r for r in json.load(open(os.path.join(CFG, "CFG240_calibration_wall", "CFG240_break_even_table.json")))
           if r.get("record") == "case" and r["kernel"] == "nu_mono" and r["N"] == 20 and r["sigma_dex"] == 0.1 and r["prior_log_f_dex"] is None]
_c240 = {r["y_min"]: r for r in _cfg240}
_agree = all(((BE[ym][0] is None) == (_c240[ym]["y_max_break_even"] is None)) and
             (BE[ym][0] is None or abs(math.log10(BE[ym][0] / _c240[ym]["y_max_break_even"])) < 0.021) and abs(BE[ym][1] - _c240[ym]["sigma_min"]) < 2e-3 for ym in BE)
P(f"  CFG240's committed table (nu_mono = this paper's kernel): " + "; ".join(f"y_min {ym:g}: break-even {_c240[ym]['y_max_break_even']}, minimum {_c240[ym]['sigma_min']:.4f}" for ym in sorted(_c240)))
OUT["S4"]["fisher"] = {str(k): dict(break_even=v[0], sigma_min=v[1], y_at_min=v[2]) for k, v in BE.items()}; OUT["S4"]["T4_worst_ratio"] = _worst
def fmt_odds(x):
    """odds as printed in the tables: two significant figures, powers of ten above 1e4"""
    if x >= 1e4:
        e_ = int(math.floor(math.log10(x))); m_ = x / 10**e_
        return f"${m_:.1f}\\times10^{{{e_}}}$:1"
    if x >= 100: return f"{int(round(x, -int(math.floor(math.log10(x))) + 1))}:1"
    if x >= 10: return f"{x:.0f}:1"
    return f"{x:.1f}:1"
SHARED_ROWS = []
for r in SHARED[:5]:
    lim = ("--", "--") if r["s_C"] == 0 else (f"{r['halo_mean_limit']:.1f}", f"{r['Hz_mean_limit']:.1f}")
    SHARED_ROWS.append(f"{r['delta_c']:.2f} & {r['s_C']:.3f} & {fmt_odds(r['halo_NA_020'])} & {r['halo_NA_020_p20']:.2f} & {fmt_odds(r['halo_NB_010'])} & {fmt_odds(r['Hz_NA_020'])} & {lim[0]} & {lim[1]}\\\\")
P("  rows of the table of shared-calibration odds (as typeset):"); [P("     " + r_) for r_ in SHARED_ROWS]
DESIGN_ROWS = []
for sm in SMS:
    d0 = DESIGN[(sm, 0.0)]
    DESIGN_ROWS.append(f"{sm:.2f} & {d0['N_expected']} & {min(d0['p20_at_Ne']):.2f} & {max(d0['pwrong_at_Ne']):.2f} & {d0['N_power90']} & "
                       + " & ".join(f"{DESIGN[(sm, ss)]['N_expected']} & {DESIGN[(sm, ss)]['N_power90']}" for ss in SIGSYS[1:]) + "\\\\")
P("  rows of the design table (as typeset):"); [P("     " + r_) for r_ in DESIGN_ROWS]
_tex = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
def _typeset_rows(label):
    if r"\label{" + label + "}" not in _tex: return []
    t_ = _tex[_tex.index(r"\label{" + label + "}"):]; t_ = t_[t_.index(r"\midrule") + len(r"\midrule"):t_.index(r"\bottomrule")]
    return [l_.strip() for l_ in t_.strip().splitlines() if l_.strip()]
_typeset = _typeset_rows("tab:shared")
_typeset_design = _typeset_rows("tab:odds")
check("S4m the shared-calibration odds reduce to the independent-error odds when the common term vanishes (1e-12)", _red < 1e-12, f"{_red:.1e}", kind="identity")
check("S4n AGAINST THE DESIGN: a common-mode baryonic-mass calibration error of 0.10 dex drops the recommended design (expected 20:1 at 0.20 dex) below 5:1 against the gated halo law, and 20:1 from the sample means needs delta_c <= 0.06 dex (halo) and about 0.15 dex (H(z)) whatever N",
      SHARED[0]["halo_NA_020"] >= 20 and SHARED[2]["halo_NA_020"] < 5 and 0.05 < dc_need_halo < 0.065 and 0.15 < dc_need_Hz < 0.165,
      f"{SHARED[0]['halo_NA_020']:.0f}:1 -> {SHARED[2]['halo_NA_020']:.1f}:1; delta_c {dc_need_halo:.3f} / {dc_need_Hz:.3f}", kind="model")
check("S4r the table of shared-calibration odds in the manuscript is exactly the computed one", _typeset == SHARED_ROWS, f"{len(_typeset)} rows typeset", kind="identity")
check("S4r2 the design table in the manuscript is exactly the computed one", _typeset_design == DESIGN_ROWS, f"{len(_typeset_design)} rows typeset", kind="identity")
check("S4o a 0.2-0.7 dex gas-mass scale error at a gas fraction of 0.5 is 0.09-0.48 dex on the baryonic mass (arithmetic)",
      abs(min(abs(x) for x in GASB[0.2]) - 0.089) < 0.002 and abs(max(abs(x) for x in GASB[0.7]) - 0.478) < 0.002, kind="identity")
check("S4p the floor sigma(log a0) >= 3 sigma/sqrt(N) holds on 4000 random designs with b in [0, 1/2] (CFG240 T4; with f free)", _worst >= 1 - 1e-9, f"min ratio {_worst:.4f}", kind="identity")
check("S4q the Fisher break-even re-computed here for the paper's kernel reproduces CFG240's committed table (N = 20, 0.1 dex; y_min = 0.001, 0.01, 0.1)", _agree,
      "; ".join(f"{ym:g}: {BE[ym][0]} / {BE[ym][1]:.4f}" for ym in BE), kind="identity")

# ================================================================================================================
head("S5  THE CLOSED-FORM INVERSION OF THE RC100 DARK-MATTER FRACTIONS")
import csv
def rc100_run(path, verbose=True):
    """The S5 analysis on one transcription of RC100 Table 3 (identical code for the corrected and the original file)."""
    _P = P if verbose else (lambda *a, **k: None)
    rows = list(csv.DictReader(open(path)))
    zz, la, yy = [], [], []
    for r in rows:
        try: z, fdm, gobs = float(r["z"]), float(r["fDM_within_Re"]), float(r["g_Re_ms2"])
        except ValueError: continue
        if not (0.02 < fdm < 0.98): continue
        gbar = (1 - fdm) * gobs; y = math.log(1 / fdm)**2
        zz.append(z); la.append(math.log10(gbar / y)); yy.append(y)
    zz, la, yy = np.array(zz), np.array(la), np.array(yy)
    rng = np.random.default_rng(20260921)
    slope, icpt = np.polyfit(zz, la, 1)
    bs = np.array([np.polyfit(zz[i], la[i], 1)[0] for i in (rng.integers(0, len(zz), len(zz)) for _ in range(4000))])
    s_halo = math.log10(ratio_halo(2.5)) / 2.5; s_Hz = float(np.log10(E(2.5))) / 2.5      # mean slopes from z = 0 to 2.5
    # the MATCHED comparators: each law fitted by the same OLS at RC100's own redshifts (RC100's discs are massive, so the halo law is
    # evaluated at 1e12 Msun here, not at the gate's mass)
    s_halo_ols = float(np.polyfit(zz, np.log10(ratio_halo(zz)), 1)[0]); s_Hz_ols = float(np.polyfit(zz, np.log10(E(zz)), 1)[0])
    _P(f"  a0 = (1 - f_DM) g_obs / [ln(1/f_DM)]^2 for {len(zz)} of {len(rows)} galaxies (f_DM in (0.02, 0.98)); z = {zz.min():.2f} - {zz.max():.2f}")
    _P(f"  median a0 = {10**np.median(la):.3e} m s^-2;  16-84%: {10**np.percentile(la,16):.2e} - {10**np.percentile(la,84):.2e};  median y = {np.median(yy):.2f}")
    y16, y50, y84 = np.percentile(yy, [16, 50, 84])
    _P(f"  accelerations probed: y = g_bar/a0 16/50/84% = {y16:.2f}/{y50:.2f}/{y84:.2f};  {int((yy < 0.3).sum())} of {len(yy)} below 0.3;  A_obs there = {1/abs(float(n_slope(y16))):.1f}/{1/abs(float(n_slope(y50))):.1f}/{1/abs(float(n_slope(y84))):.1f}")
    _P(f"  d log10 a0/dz = {slope:+.4f} +/- {bs.std():.4f} (bootstrap);  constant: 0 ({slope/bs.std():+.1f} sigma);  halo-emergent mean slope {s_halo:+.4f} ({(slope-s_halo)/bs.std():+.1f} sigma);  H(z) mean slope {s_Hz:+.4f} ({(slope-s_Hz)/bs.std():+.1f} sigma)")
    _P(f"  matched comparators (OLS at RC100's redshifts): halo law (1e12 Msun) {s_halo_ols:+.4f}, H(z) {s_Hz_ols:+.4f}  (formal distances {(s_halo_ols-slope)/bs.std():.1f} and {(s_Hz_ols-slope)/bs.std():.1f} sigma, conditional on RC100's mass models; NOT quoted)")
    dfdm = np.polyfit(zz, np.log10([float(r["fDM_within_Re"]) for r in rows if 0.02 < float(r["fDM_within_Re"]) < 0.98]), 1)[0]
    _P(f"  what drives it: d log10 f_DM/dz = {dfdm:+.3f}  (the published fall of the dark-matter fraction with redshift); the inversion is monotone in f_DM")
    # ---- is the trend a selection effect?  control for a measured acceleration (independent of a0) and, separately, for the inferred y
    lgo = np.array([math.log10(float(r["g_Re_ms2"])) for r in rows if 0.02 < float(r["fDM_within_Re"]) < 0.98])
    def partial(cols):
        X = np.c_[np.ones_like(zz), zz, *cols]
        b = np.linalg.lstsq(X, la, rcond=None)[0]
        B = np.array([np.linalg.lstsq(X[i], la[i], rcond=None)[0] for i in (rng.integers(0, len(zz), len(zz)) for _ in range(4000))])
        return float(b[1]), float(B[:, 1].std()), float(np.std(la - X @ b))
    sg, eg, rg = partial([lgo]); sy, ey, ry = partial([np.log10(yy)])
    _P(f"  scatter about the fit: {np.std(la - (icpt + slope*zz)):.2f} dex;  corr(log a0_hat, log y_hat) = {np.corrcoef(la, np.log10(yy))[0,1]:+.2f}  (noise in f_DM moves a0_hat and y_hat oppositely)")
    _P(f"  controlling for log g_obs (measured, a0-free):   d log a0/dz = {sg:+.3f} +/- {eg:.3f}   -> halo-emergent mean slope disfavoured at {(s_halo-sg)/eg:.1f} sigma")
    _P(f"  controlling for log y_hat (absorbs noise AND part of any real signal): {sy:+.3f} +/- {ey:.3f}   -> {(s_halo-sy)/ey:.1f} sigma")
    weak_H = min((s_Hz - slope) / bs.std(), (s_Hz - sg) / eg, (s_Hz - sy) / ey)
    _P(f"  weakest exclusion of the H(z) mean slope over the three treatments: {weak_H:.1f} sigma")
    _P(f"  range of the redshift slope over the three treatments: {min(slope, sg, sy):+.2f} to {max(slope, sg, sy):+.2f};  weakest exclusion of the halo-emergent slope: {min((s_halo-slope)/bs.std(), (s_halo-sg)/eg, (s_halo-sy)/ey):.1f} sigma")
    # ---- the result is conditional on the redshift calibration of the baryonic masses.  Tilt M_b by beta dex per unit z about the
    #      sample's mean redshift (g_bar -> g_bar 10^[beta (z - zbar)], g_obs fixed), re-invert, re-fit.
    zr = np.array([float(r["z"]) for r in rows]); fr = np.array([float(r["fDM_within_Re"]) for r in rows]); gr = np.array([float(r["g_Re_ms2"]) for r in rows])
    zbar = float(np.mean(zz)); tilt = []
    for beta in (-0.10, -0.075, -0.05, -0.025, 0.0, 0.025, 0.05):
        gbt = (1 - fr) * gr * 10**(beta * (zr - zbar)); ft = 1 - gbt / gr
        ok_ = (ft > 0.02 + 1e-9) & (ft < 0.98 - 1e-9)          # the same open interval as the main fit (the f_DM = 0.02 edge excluded)
        lat = np.log10(gbt[ok_] / np.log(1 / ft[ok_])**2); zt = zr[ok_]
        st = np.polyfit(zt, lat, 1)[0]
        bt = np.array([np.polyfit(zt[i], lat[i], 1)[0] for i in (rng.integers(0, len(zt), len(zt)) for _ in range(1500))]).std()
        tilt.append(dict(beta=beta, n=int(ok_.sum()), slope=float(st), err=float(bt), sig_const=float(st / bt), sig_halo=float((s_halo - st) / bt),
                         sig_halo_ols=float((s_halo_ols - st) / bt), sig_Hz_ols=float((s_Hz_ols - st) / bt)))
    _P("  baryonic-mass calibration drift beta [dex per unit z]  ->  slope, and its distance from constant / from the halo law:")
    for t in tilt:
        _P(f"     beta {t['beta']:+.3f}: N {t['n']:3d}, slope {t['slope']:+.3f} +/- {t['err']:.3f};  constant {t['sig_const']:+.1f} sigma;  halo law {t['sig_halo']:+.1f} sigma (matched {t['sig_halo_ols']:+.1f});  H(z) matched {t['sig_Hz_ols']:+.1f}")
    # one galaxy sits exactly on the f_DM = 0.02 edge of the inversion; admitting it:
    edge = (fr >= 0.02 - 1e-12) & (fr < 0.98)
    la_e = np.log10((1 - fr[edge]) * gr[edge] / np.log(1 / fr[edge])**2); slope_edge = float(np.polyfit(zr[edge], la_e, 1)[0])
    _P(f"  admitting the one galaxy at the f_DM = 0.02 edge: slope {slope:+.3f} -> {slope_edge:+.3f} (N {int(edge.sum())}), a {abs(slope_edge - slope)/bs.std():.1f} sigma move from one object")
    beta_halo2 = max((t["beta"] for t in tilt if t["sig_halo"] < 2.0 and t["beta"] < 0), default=None)
    beta_halo2_ols = max((t["beta"] for t in tilt if t["sig_halo_ols"] < 2.05 and t["beta"] < 0), default=None)
    beta_Hz1 = max((t["beta"] for t in tilt if t["sig_Hz_ols"] < 1.05 and t["beta"] < 0), default=None)
    beta_const2 = max((t["beta"] for t in tilt if abs(t["sig_const"]) > 2.0 and t["beta"] < 0), default=None)
    _P(f"  the halo law comes within 2 sigma at beta = {beta_halo2} (matched comparator: {beta_halo2_ols}); H(z) within 1 sigma at beta = {beta_Hz1}; constancy goes 2 sigma off at beta = {beta_const2}")
    # ---- RC100's OWN internal flags, re-derived from the table: V_rot(R_e)^2 = V_c^2 - 3.36 sigma0^2 < 0 (their eq. 8), and
    #      V_rot/sigma0 < 2.3 at R_e (their rotation cut).  The slope without those rows.
    EQ8, CUT = set(), set()
    for r in rows:
        v2_ = float(r["Vc_Re_kms"])**2 - 3.36 * float(r["sigma0_kms"])**2
        if v2_ < 0: EQ8.add(r["idx"])
        elif math.sqrt(v2_) / float(r["sigma0_kms"]) < 2.3: CUT.add(r["idx"])
    def _slope_drop(drop):
        zd, ld = [], []
        for r in rows:
            if r["idx"] in drop: continue
            f_ = float(r["fDM_within_Re"])
            if not (0.02 < f_ < 0.98): continue
            zd.append(float(r["z"])); ld.append(math.log10((1 - f_) * float(r["g_Re_ms2"]) / math.log(1 / f_)**2))
        zd, ld = np.array(zd), np.array(ld); rr_ = np.random.default_rng(290)
        return float(np.polyfit(zd, ld, 1)[0]), float(np.std([np.polyfit(zd[i], ld[i], 1)[0] for i in (rr_.integers(0, len(zd), len(zd)) for _ in range(4000))])), len(zd)
    FLAG = dict(eq8=sorted(EQ8, key=int), n_cut=len(CUT), no_eq8=_slope_drop(EQ8), no_flagged=_slope_drop(EQ8 | CUT))
    _P(f"  RC100's own flags: eq.-8 violators (V_rot^2 < 0 at R_e) rows {FLAG['eq8']}; {FLAG['n_cut']} more rows below V_rot/sigma0 = 2.3 at R_e;"
       f" slope without the eq.-8 rows {FLAG['no_eq8'][0]:+.3f} +/- {FLAG['no_eq8'][1]:.3f} (N {FLAG['no_eq8'][2]}), without all {len(EQ8 | CUT)} {FLAG['no_flagged'][0]:+.3f} +/- {FLAG['no_flagged'][1]:.3f} (N {FLAG['no_flagged'][2]})")
    # ---- the independent replication (KMOS3D; Ubler+2017 kinematics x KMOS3D sizes), from its committed lane
    L332 = json.load(open(os.path.join(ROOT, "real_research", "dark_sector_2026", "L332_kmos3d_trend_replication_results.json")))
    k1 = L332["checks"]; k1m = [v for k_, v in k1.items() if k_.startswith("K1")][0]["measured"]; t1 = [v for k_, v in k1.items() if k_.startswith("T1")][0]
    _P(f"  KMOS3D replication (L332): T1 {'PASSED' if t1['ok'] else 'FAILED'} ({t1['measured']});  K1: {k1m}")
    # ---- injection: kernel-consistent synthetic f_DM on the REAL (z, g_bar) with injected trends and noise in f_DM
    rngR = np.random.default_rng(271828); gbr = (1 - fr) * gr; injR = []
    for s_in in (0.0, s_halo, s_Hz):
        rec = []
        for _ in range(300):
            a_z = 1.2e-10 * 10**(s_in * (zr - zbar)); f_t = np.exp(-np.sqrt(gbr / a_z))
            f_o = np.clip(f_t + rngR.normal(0, 0.05, f_t.size), 0.021, 0.979); g_o = gbr / (1 - f_t)
            la_s = np.log10((1 - f_o) * g_o / np.log(1 / f_o)**2); rec.append(np.polyfit(zr, la_s, 1)[0])
        injR.append((s_in, float(np.mean(rec)), float(np.std(rec))))
    _P("  injection (kernel-consistent f_DM with 0.05 noise on the real z, g_bar): injected -> recovered slope: " + ", ".join(f"{a:+.3f} -> {b:+.3f}" for a, b, _ in injR))
    R = dict(slope_with_edge_galaxy=slope_edge, tilt=tilt, beta_halo_within_2sigma=beta_halo2, beta_const_2sigma_off=beta_const2, L332_T1=t1, L332_K1=k1m, injection=injR,
             beta_halo_within_2sigma_matched=beta_halo2_ols, beta_Hz_within_1sigma=beta_Hz1, slope_halo_ols=s_halo_ols, slope_Hz_ols=s_Hz_ols, flags=FLAG,
                     N=int(len(zz)), slope=float(slope), slope_err=float(bs.std()), median_a0=float(10**np.median(la)), median_y=float(np.median(yy)),
                     slope_halo=s_halo, slope_Hz=s_Hz, dlogfdm_dz=float(dfdm), scatter=float(np.std(la - (icpt + slope*zz))),
                     slope_ctrl_gobs=sg, err_ctrl_gobs=eg, slope_ctrl_y=sy, err_ctrl_y=ey,
                     y_percentiles=[float(y16), float(y50), float(y84)], n_below_gate=int((yy < 0.3).sum()), weakest_excl_Hz=float(weak_H))
    R.update(_arrays=dict(zz=zz, la=la, yy=yy, icpt=icpt, bs=bs, sg=sg, eg=eg, sy=sy, ey=ey, slope_edge=slope_edge, t1=t1, k1m=k1m))
    R["weakest_excl_halo"] = float(min((s_halo - slope) / bs.std(), (s_halo - sg) / eg, (s_halo - sy) / ey))
    R["scatter_corr_la_y"] = float(np.corrcoef(la, np.log10(yy))[0, 1])
    R["a0_16_84"] = [float(10**np.percentile(la, 16)), float(10**np.percentile(la, 84))]
    return R

R5 = rc100_run(RC100)                          # the corrected transcription: every number in the text
R5c = rc100_run(RC100_CORR, verbose=False)     # v3.1's input (arXiv v1, CFG289), run by the same code, for the old -> new table
R5o = rc100_run(RC100_ORIG, verbose=False)     # the earliest transcription (kept for the CFG289 record)
_A = R5["_arrays"]
zz, la, yy, icpt, bs = _A["zz"], _A["la"], _A["yy"], _A["icpt"], _A["bs"]
sg, eg, sy, ey, slope_edge, t1, k1m = _A["sg"], _A["eg"], _A["sy"], _A["ey"], _A["slope_edge"], _A["t1"], _A["k1m"]
slope, tilt, injR, weak_H = R5["slope"], R5["tilt"], R5["injection"], R5["weakest_excl_Hz"]
s_halo, s_Hz, beta_halo2, beta_const2 = R5["slope_halo"], R5["slope_Hz"], R5["beta_halo_within_2sigma"], R5["beta_const_2sigma_off"]
OUT["S5"] = {k_: v for k_, v in R5.items() if k_ != "_arrays"}
OUT["S5_original_transcription"] = {k_: v for k_, v in R5o.items() if k_ != "_arrays"}
OUT["S5_corrected_arxiv_v1"] = {k_: v for k_, v in R5c.items() if k_ != "_arrays"}
# ---- the journal table against v3.1's arXiv-v1 transcription (CFG305), and the earlier CFG289 correction, cell by cell
import hashlib
_sha = hashlib.sha256(open(RC100, "rb").read()).hexdigest()
_sha_c = hashlib.sha256(open(RC100_CORR, "rb").read()).hexdigest()
_rf, _rc, _ro = list(csv.DictReader(open(RC100))), list(csv.DictReader(open(RC100_CORR))), list(csv.DictReader(open(RC100_ORIG)))
_prim = ("name", "z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms")
_chg = {f: [int(a["idx"]) for a, b in zip(_rf, _rc) if a[f] != b[f]] for f in _prim}            # PUBLISHED vs CORRECTED (CFG305)
_chg289 = {f: [int(a["idx"]) for a, b in zip(_rc, _ro) if a[f] != b[f]] for f in _prim}         # CORRECTED vs ORIGINAL (CFG289)
_flip289 = [int(a["idx"]) for a, b in zip(_rc, _ro) if a["deepMOND_g_lt_a0"] != b["deepMOND_g_lt_a0"]]
_flip = [int(a["idx"]) for a, b in zip(_rf, _rc) if a["deepMOND_g_lt_a0"] != b["deepMOND_g_lt_a0"]]
P(f"  RC100 journal table (CFG305): sha256 {_sha[:16]}...; against v3.1's arXiv-v1 transcription (sha256 {_sha_c[:16]}...): changed primary cells " +
  ", ".join(f"{f} {v}" for f, v in _chg.items() if v) + f"; total {sum(len(v) for v in _chg.values())}; deep-regime flag flips {_flip}")
P(f"  (the earlier CFG289 correction, arXiv v1 against the first transcription: " + ", ".join(f"{f} {len(v)}" for f, v in _chg289.items() if v) +
  f"; total {sum(len(v) for v in _chg289.values())}; deep-regime flag flips {_flip289})")
_inv_rows = sorted(set(_chg["fDM_within_Re"]) | set(_chg["Vc_Re_kms"]) | set(_chg["Re_kpc"]))
P(f"  cells that enter the inversion (f_DM, and V_c, R_e through g = V_c^2/R_e): rows {_inv_rows}")
RC100_MOVES = []
P("  the f_DM inversion, arXiv-v1 transcription (v3.1) -> journal table (v3.2):")
for lab, kk, fmt in (("N", "N", "d"), ("slope d log a0/dz", "slope", "+.3f"), ("its bootstrap error", "slope_err", ".3f"), ("median a0 [m s^-2]", "median_a0", ".3e"),
                     ("median y", "median_y", ".2f"), ("scatter about the fit [dex]", "scatter", ".3f"), ("slope | log g_obs", "slope_ctrl_gobs", "+.3f"), ("slope | log y", "slope_ctrl_y", "+.3f"),
                     ("weakest exclusion of the halo slope [sigma]", "weakest_excl_halo", ".2f"), ("weakest exclusion of the H(z) slope [sigma]", "weakest_excl_Hz", ".2f"),
                     ("slope with the f_DM = 0.02 edge galaxy", "slope_with_edge_galaxy", "+.3f"), ("corr(log a0, log y)", "scatter_corr_la_y", "+.2f"),
                     ("16th percentile of a0 [m s^-2]", None, ".3e")):
    old = R5c[kk] if kk else R5c["a0_16_84"][0]; new = R5[kk] if kk else R5["a0_16_84"][0]
    RC100_MOVES.append(dict(quantity=lab, old=float(old), new=float(new)))
    P(f"     {lab:46s} {format(old, fmt):>11s} -> {format(new, fmt):>11s}")
for t_o, t_n in zip(R5c["tilt"], R5["tilt"]):
    RC100_MOVES.append(dict(quantity=f"drift beta {t_o['beta']:+.3f}: slope", old=t_o["slope"], new=t_n["slope"]))
    P(f"     drift beta {t_o['beta']:+.3f}: slope {t_o['slope']:+.3f} -> {t_n['slope']:+.3f} (constant {t_o['sig_const']:+.1f} -> {t_n['sig_const']:+.1f} sigma; halo matched {t_o['sig_halo_ols']:+.1f} -> {t_n['sig_halo_ols']:+.1f} sigma; H(z) matched {t_o['sig_Hz_ols']:+.1f} -> {t_n['sig_Hz_ols']:+.1f})")
OUT["S5_correction"] = dict(sha256=_sha, sha256_corrected=_sha_c, changed_vs_arxiv_v1=_chg, changed_cfg289=_chg289, deep_flag_flips=_flip, deep_flag_flips_cfg289=_flip289,
                            inversion_rows=_inv_rows, moves=RC100_MOVES)
check("S5a the inversion is exact: nu(y) (1 - f_DM) = 1 at y = [ln(1/f_DM)]^2", abs(nu(math.log(1/0.37)**2) * (1 - 0.37) - 1) < 1e-12)
_g217 = json.load(open(os.path.join(CFG, "CFG305_published_tables", "C_cfg217_attack_corrected_results_PUBFIX.json")))["numbers"]["G2"]   # CFG217 re-run on the journal table (CFG305)
P(f"  CFG217 G2 (journal table, CFG305 re-run; RC41 overlap with SED stellar and gas masses): Spearman rho(constant-a0 residual, log M_bar,fit - log(M* + M_gas)) = {_g217['rho']:+.2f}, p = {_g217['p']:.3f}, n = {_g217['n']}")
OUT["S5"]["cfg217_G2"] = _g217
FLAG = R5["flags"]; beta_halo2_ols, beta_Hz1 = R5["beta_halo_within_2sigma_matched"], R5["beta_Hz_within_1sigma"]
_tb = {t["beta"]: t for t in tilt}
check("S5e AGAINST INTEREST: the slope is calibration-conditional -- a baryonic-mass drift of -0.05 dex per unit z puts it within 1 sigma of constancy and within 2 sigma of the halo law fitted the same way, -0.075 brings the halo law within 1 sigma, and -0.10 brings the H(z) law within 1 sigma (v3.2 wording, set after seeing the journal-table run: post hoc wording check)",
      abs(_tb[-0.05]["sig_const"]) < 1.0 and _tb[-0.05]["sig_halo_ols"] < 2.0 and _tb[-0.075]["sig_halo_ols"] < 1.0 and _tb[-0.10]["sig_Hz_ols"] < 1.0,
      f"-0.05: const {_tb[-0.05]['sig_const']:+.1f}, halo {_tb[-0.05]['sig_halo_ols']:+.1f}; -0.075: halo {_tb[-0.075]['sig_halo_ols']:+.1f}; -0.10: H(z) {_tb[-0.10]['sig_Hz_ols']:+.1f}")
check("S5f AGAINST INTEREST: the independent KMOS3D replication (L332) failed, and a third to a half of its z > 1.9 galaxies rotate below their own Newtonian baryons (read from the committed lane)",
      (not t1["ok"]) and "0.27-0.54" in k1m, k1m[:80], kind="identity")
check("S5g the tilt table at beta = 0 reproduces the main fit exactly (same galaxies, same slope)",
      [t for t in tilt if t["beta"] == 0.0][0]["n"] == len(zz) and abs([t for t in tilt if t["beta"] == 0.0][0]["slope"] - slope) < 1e-9, kind="identity")
check("I5 the inversion recovers injected trends (0, halo law, H(z)) to 0.02 dex per unit z when f_DM obeys the kernel", all(abs(a - b) < 0.02 for a, b, _ in injR),
      ", ".join(f"{a:+.3f}->{b:+.3f}" for a, b, _ in injR), kind="injection")
check("S5b the RC100 slope is consistent with a constant a0 (within 2.5 sigma) and is negative, i.e. shows no sign of the rise both comparators predict (their matched slopes are positive)",
      abs(slope / bs.std()) < 2.5 and slope < 0 < R5["slope_halo_ols"] < R5["slope_Hz_ols"], f"{slope:+.3f} +/- {bs.std():.3f}; comparators {R5['slope_halo_ols']:+.3f}, {R5['slope_Hz_ols']:+.3f}")
check("S5c no decline is claimed: the slope is within 2.5 sigma of zero under every treatment", abs(slope) < 2.5 * bs.std() and abs(sg) < 2.5 * eg and abs(sy) < 2.5 * ey)
check("S5d RC100's own flagged rows (2 with V_rot^2 < 0 by their eq. 8; 14 below their V_rot/sigma0 = 2.3 cut at R_e) move the slope by less than 0.5 sigma when dropped",
      FLAG["eq8"] == ["67", "83"] and FLAG["n_cut"] == 14 and abs(FLAG["no_eq8"][0] - slope) < 0.5 * bs.std() and abs(FLAG["no_flagged"][0] - slope) < 0.5 * bs.std(),
      f"{slope:+.3f} -> {FLAG['no_eq8'][0]:+.3f} / {FLAG['no_flagged'][0]:+.3f}")
check("S5j AGAINST 'NO MASS MODEL ENTERS': the constant-a0 residual tracks the offset of RC100's fitted baryonic mass from independent SED + gas masses (CFG217 G2: |rho| >= 0.3, p < 0.05; read from the committed lane)",
      _g217["prior_driven"] and abs(_g217["rho"]) >= 0.3 and _g217["p"] < 0.05 and _g217["n"] == 41, f"rho {_g217['rho']:+.2f}, p {_g217['p']:.3f}", kind="identity")
def _rc100_verdicts(R):
    """the RC100 statements of the text, evaluated on one transcription: (S5b, S5c, S5e)"""
    A_ = R["_arrays"]; se = A_["bs"].std()
    b_ = abs(R["slope"] / se) < 2.5 and R["slope"] < 0 < R["slope_halo_ols"] < R["slope_Hz_ols"]
    c_ = abs(R["slope"]) < 2.5 * se and abs(A_["sg"]) < 2.5 * A_["eg"] and abs(A_["sy"]) < 2.5 * A_["ey"]
    tb_ = {t["beta"]: t for t in R["tilt"]}
    e_ = abs(tb_[-0.05]["sig_const"]) < 1.0 and tb_[-0.05]["sig_halo_ols"] < 2.0 and tb_[-0.075]["sig_halo_ols"] < 1.0 and tb_[-0.10]["sig_Hz_ols"] < 1.0
    return (b_, c_, e_)
check("S5h the RC100 input is the journal table built by CFG305 (sha256), and it differs from v3.1's arXiv-v1 transcription (itself the CFG289 file, sha256) in exactly 6 primary cells: row 87 (J0901+1814, refit between arXiv v1 and the journal: log M_baryon, R_e, f_DM, V_c, sigma0) and row 78 (sigma0, our transcription slip); only row 87 enters the inversion; no deep-regime flag flips",
      _sha == RC100_SHA256 and _sha_c == RC100_CORR_SHA256 and sum(len(v) for v in _chg.values()) == 6
      and all(_chg[f] == [87] for f in ("logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms")) and _chg["sigma0_kms"] == [78, 87] and _inv_rows == [87] and not _flip
      and sum(len(v) for v in _chg289.values()) == 17 and _flip289 == [44],
      ", ".join(f"{f} {v}" for f, v in _chg.items() if v), kind="identity")
def _s5e_v31(R):
    """v3.1's S5e wording (tolerances 0.5 / 2.2 / 1.1 / 1.1), kept to record the verdict move"""
    tb_ = {t["beta"]: t for t in R["tilt"]}
    return abs(tb_[-0.05]["sig_const"]) < 0.5 and tb_[-0.05]["sig_halo_ols"] < 2.2 and tb_[-0.075]["sig_halo_ols"] < 1.1 and tb_[-0.10]["sig_Hz_ols"] < 1.1
check("S5i AGAINST INTEREST: the journal table moves the f_DM slope by less than 0.5 sigma (towards zero) and leaves S5b and S5c unchanged, but v3.1's calibration wording (-0.05 within 0.5 sigma of constancy) holds on the arXiv-v1 table and FAILS on the journal table; v3.2 rewords it (S5e)",
      _rc100_verdicts(R5)[:2] == _rc100_verdicts(R5c)[:2] and abs(R5["slope"] - R5c["slope"]) < 0.5 * R5["slope_err"] and R5["N"] == R5c["N"] == 99
      and _s5e_v31(R5c) and not _s5e_v31(R5) and _rc100_verdicts(R5)[2],
      f"slope {R5c['slope']:+.4f} -> {R5['slope']:+.4f} ({(R5['slope'] - R5c['slope']) / R5['slope_err']:+.2f} sigma); v3.1 S5e wording {_s5e_v31(R5c)} -> {_s5e_v31(R5)}; v3.2 wording on the journal table {_rc100_verdicts(R5)[2]}")

# ---- v3.2: the FRAMEWORK-NATIVE route (CFG303 route B), the paper's primary RC100 statement.  No halo-fit quantity enters g_bar:
#      g_bar = M_bar,nat x [CFG216's thin exponential disc at R_e] with M_bar,nat = M*_SED (table column 6, CFG303's transcription)
#      x (1 + mu_t18) (CFG217's Tacconi-type gas fraction); g_obs = V_c(R_e)^2/R_e, the authors' circular velocity (MODEL-OTHER: it is an
#      output of their disc + halo fit).  The same inversion, a0 = g_bar/[ln(1/f)]^2 with f = 1 - g_bar/g_obs, in the same window.
#      CFG303's committed code is exec'd read-only (helpers, xi, the per-galaxy loop, s5_table) and CFG216/CFG217's committed headers
#      supply disc_v2 and mu_t18, exactly as CFG303 loads them.
P("")
P("  RC100, FRAMEWORK-NATIVE ROUTE (CFG303 route B) on the journal table: g_bar from the SED stellar mass + scaling-relation gas (no f_DM, no fitted baryonic mass)")
import tempfile
F303 = os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE.py")
_src303 = open(F303).read()
def _blk303(a, b):
    assert _src303.count(a) == 1 and _src303.count(b) == 1, (a, b)
    return _src303[_src303.index(a):_src303.index(b)]
_ns303 = {"__file__": F303, "__name__": "paper_numbers_exec303", "REPO": ROOT, "CFG": CFG, "LANE": os.path.dirname(F303)}
exec(compile("import os, sys, io, csv, json, math, contextlib, tempfile, time, hashlib\nimport numpy as np\n" + _blk303("def exec_upto(", "def run_block("),
             "cfg303[helpers]", "exec"), _ns303)
_ns216, _ = _ns303["exec_upto"](os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100.py"),
                                 "# ------------------------------------------------------------------------------------------------ data\n")
_ns217, _ = _ns303["exec_upto"](os.path.join(CFG, "CFG217_rc100_attack", "cfg217_attack.py"),
                                 "# ------------------------------------------------------------------------------------------------ data (CFG216's sample)")
_ns303.update(G2SI=_ns216["G2SI"], G_KPC=_ns216["G_KPC"], disc_v2=_ns216["disc_v2"], mu_t18=_ns217["mu_t18"], TMP=tempfile.mkdtemp(prefix="pn_s5n_"))
exec(compile(_blk303("def xi(Re, R):", "def point(label"), "cfg303[xi]", "exec"), _ns303)
exec(compile(_blk303("def s5_table(name, gbcol, sel=None):", "gobsPN = {"), "cfg303[s5_table]", "exec"), _ns303)
_code_gal = _blk303("gal = []\nfor r in rc:", "A = [g for g in gal if g[\"inA\"]]")
_TR = {r["idx"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "rc100_table3_cols5to8_transcribed.csv"), newline=""))}
_RC41 = {r["id"].replace("_", " "): r for r in csv.DictReader(open(os.path.join(ROOT, "data_assembly", "price2021_rc41", "price2021_rc41.csv"), newline=""))}
def native_gal(table):
    """CFG303's per-galaxy loop on one RC100 table; returns its `gal` list (s5_table then reads g_obs, V_c, sigma0 from the same table)"""
    _ns303.update(rc=list(csv.DictReader(open(table, newline=""))), tr=_TR, rc41=_RC41, nsPN={"RC100": table})
    exec(compile(_code_gal, "cfg303[per-galaxy loop]", "exec"), _ns303)
    return _ns303["gal"]
# control: on v3.1's arXiv-v1 table the exec'd route reproduces CFG303's committed S5 numbers (route B and A)
_J303 = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json")))["s5"]
_galc = native_gal(RC100_CORR)
_R5Nc = rc100_run(_ns303["s5_table"]("Bc", [g["gbB"] for g in _galc]), verbose=False)
_R5Ac = rc100_run(_ns303["s5_table"]("Ac", [g["gbA"] for g in _galc], lambda g: g["inA"]), verbose=False)
_d303 = max(max(abs(R_[k] - _J303[s_][k]) / max(abs(_J303[s_][k]), 1e-30) for k in ("slope", "slope_err", "median_a0", "median_y", "weakest_excl_Hz"))
            for R_, s_ in ((_R5Nc, "B"), (_R5Ac, "A")))
# the journal table
GALN = native_gal(RC100)
P(f"  native route B ({len(GALN)} galaxies; SED log M* from CFG303's transcription of column 6, gas mu_t18, thin disc at R_e):")
R5N = rc100_run(_ns303["s5_table"]("B", [g["gbB"] for g in GALN]), verbose=True)
R5A = rc100_run(_ns303["s5_table"]("A", [g["gbA"] for g in GALN], lambda g: g["inA"]), verbose=False)
R5Nm = rc100_run(_ns303["s5_table"]("Bmut", [g["gbB"] * 10**0.2 for g in GALN]), verbose=False)          # MUTATE: native baryons x 10^0.2
_gid = [(1 - g["fd"]) * float(r_["g_Re_ms2"]) for g, r_ in zip(GALN, csv.DictReader(open(RC100)))]
R5Nid = rc100_run(_ns303["s5_table"]("id", _gid), verbose=False)                                          # identity: f_DM's g_bar through the native path
DN = np.array([g["go"] / g["gbB"] for g in GALN])
YNAT = np.array([g["gbB"] for g in GALN]) / a0_L                                                       # native y = g_bar,nat / a0 (eq. a0value), all 100
_tbN = {t["beta"]: t for t in R5N["tilt"]}
_t1 = [g["idx"] for g in GALN if abs(float(_TR[g["idx"]]["logMbaryon"]) - g["lMfit"]) > 1e-9]
P(f"  native: N {R5N['N']} of 100 in the window; {int((DN <= 1).sum())} galaxies have D = g_obs/g_bar,nat <= 1 and {int((DN <= 1 / 0.98).sum())} have f = 1 - 1/D <= 0.02 (outside the window: their native baryons reach >= 98% of the dynamics)")
P(f"  native: slope {R5N['slope']:+.3f} +/- {R5N['slope_err']:.3f}, median a0 {R5N['median_a0']:.3e} (biased high: the window drops the discs at the Newtonian floor), comparators (OLS at the same z) halo {R5N['slope_halo_ols']:+.3f}, H(z) {R5N['slope_Hz_ols']:+.3f}")
P(f"  native drift beta -0.05: slope {_tbN[-0.05]['slope']:+.3f} +/- {_tbN[-0.05]['err']:.3f} (constant {_tbN[-0.05]['sig_const']:+.1f} sigma); beta -0.10: {_tbN[-0.10]['slope']:+.3f} +/- {_tbN[-0.10]['err']:.3f} (H(z) matched {_tbN[-0.10]['sig_Hz_ols']:+.1f} sigma)")
P(f"  native sample A (RC41 overlap, Price+21 SED M* + gas): N {R5A['N']}, slope {R5A['slope']:+.3f} +/- {R5A['slope_err']:.3f}")
P(f"  native y = g_bar,nat/a0 (a0 = {a0_L:.3e}), all 100: median {np.median(YNAT):.2f}, 16-84% {np.percentile(YNAT, 16):.2f}-{np.percentile(YNAT, 84):.2f}, {int((YNAT < 0.3).sum())} below 0.3;"
  f" A_obs at the median {1 / abs(float(n_slope(np.median(YNAT)))):.2f}, A_bar {abs(1 + 1 / float(n_slope(np.median(YNAT)))):.2f} -> 0.2 dex of baryonic mass becomes {0.2 * abs(1 + 1 / float(n_slope(np.median(YNAT)))):.2f} dex in a0")
P(f"  MUTATE (native g_bar x 10^0.2): N {R5N['N']} -> {R5Nm['N']}, median a0 {R5N['median_a0']:.3e} -> {R5Nm['median_a0']:.3e}")
P(f"  control: on the arXiv-v1 table the exec'd route reproduces CFG303's committed S5 (B: N {_R5Nc['N']}, slope {_R5Nc['slope']:+.3f} +/- {_R5Nc['slope_err']:.3f}; A: N {_R5Ac['N']}): max relative difference {_d303:.1e}")
P(f"  native route, arXiv-v1 (CFG303) -> journal: N {_R5Nc['N']} -> {R5N['N']}; slope {_R5Nc['slope']:+.3f} +/- {_R5Nc['slope_err']:.3f} -> {R5N['slope']:+.3f} +/- {R5N['slope_err']:.3f};"
  f" median a0 {_R5Nc['median_a0']:.3e} -> {R5N['median_a0']:.3e}; weakest H(z) exclusion {_R5Nc['weakest_excl_Hz']:.1f} -> {R5N['weakest_excl_Hz']:.1f} sigma")
OUT["S5_native"] = dict(B={k_: v for k_, v in R5N.items() if k_ != "_arrays"}, A={k_: v for k_, v in R5A.items() if k_ != "_arrays"},
                        B_arxiv_v1={k_: v for k_, v in _R5Nc.items() if k_ != "_arrays"}, n_D_le_1=int((DN <= 1).sum()), n_f_le_002=int((DN <= 1 / 0.98).sum()),
                        y_native=dict(median=float(np.median(YNAT)), p16=float(np.percentile(YNAT, 16)), p84=float(np.percentile(YNAT, 84)), n_below_03=int((YNAT < 0.3).sum())),
                        mutate=dict(N=R5Nm["N"], median_a0=R5Nm["median_a0"]), transcription_col7_mismatch=_t1)
check("S5k the native route is CFG303's committed code: on v3.1's arXiv-v1 table it reproduces CFG303's committed S5 numbers for routes B and A (relative 1e-12)", _d303 <= 1e-12 and _R5Nc["N"] == _J303["B"]["N"] and _R5Ac["N"] == _J303["A"]["N"],
      f"max rel diff {_d303:.1e}; N {_R5Nc['N']}/{_R5Ac['N']}", kind="identity")
check("S5l identity replacement: the f_DM route's own g_bar = (1 - f_DM) g_obs sent through the native path reproduces the f_DM inversion with its edge galaxy admitted (floating point puts f_DM = 0.02 inside the open window): N 100 and the same slope",
      R5Nid["N"] == 100 and abs(R5Nid["slope"] - R5["slope_with_edge_galaxy"]) < 1e-9, f"N {R5Nid['N']}; slope {R5Nid['slope']:+.6f} vs {R5['slope_with_edge_galaxy']:+.6f}", kind="identity")
check("S5m the transcription behind the native route (CFG303, arXiv v1 column 7) equals the journal table's log M_baryon except in row 87 (the refit; its SED log M*, column 6, is unchanged at 10.96 in the journal, CFG305)",
      _t1 == ["87"] and abs(float(_TR["87"]["logMstar"]) - 10.96) < 1e-9, f"mismatches {_t1}", kind="identity")
check("I5n on the native baryons the inversion recovers injected trends (0, halo law, H(z)) to 0.02 dex per unit z when the dark fraction obeys the kernel", all(abs(a - b) < 0.02 for a, b, _ in R5N["injection"]),
      ", ".join(f"{a:+.3f}->{b:+.3f}" for a, b, _ in R5N["injection"]), kind="injection")
check("S5n MUTATE: raising every native baryonic mass by 0.2 dex removes galaxies from the window (more reach the Newtonian floor) and lowers the median a0", R5Nm["N"] < R5N["N"] and R5Nm["median_a0"] < R5N["median_a0"],
      f"N {R5N['N']} -> {R5Nm['N']}; median {R5N['median_a0']:.2e} -> {R5Nm['median_a0']:.2e}", kind="injection")
check("S5o AGAINST INTEREST (for any reading that needs a discrepancy): on native baryons at least 30 of the 100 RC100 discs have g_obs <= g_bar,nat at R_e, and about 40 fall outside the inversion window",
      (DN <= 1).sum() >= 30 and 35 <= (DN <= 1 / 0.98).sum() <= 45, f"D <= 1: {int((DN <= 1).sum())}; f <= 0.02: {int((DN <= 1 / 0.98).sum())}")
check("S5p the window-only native RC100 slope (the 59 discs off the floor; a censored sample, S5s) is consistent with a constant a0 (within 2.5 sigma, also when controlled for g_obs and for y) and shows no rise (negative; both comparators positive), and it agrees with the f_DM comparison within 1 sigma",
      abs(R5N["slope"]) < 2.5 * R5N["slope_err"] and R5N["slope"] < 0 < R5N["slope_halo_ols"] < R5N["slope_Hz_ols"] and abs(R5N["slope"] - R5["slope"]) < math.hypot(R5N["slope_err"], R5["slope_err"])
      and abs(R5N["slope_ctrl_gobs"]) < 2.5 * R5N["err_ctrl_gobs"] and abs(R5N["slope_ctrl_y"]) < 2.5 * R5N["err_ctrl_y"],
      f"native {R5N['slope']:+.3f} +/- {R5N['slope_err']:.3f} (| g_obs {R5N['slope_ctrl_gobs']:+.3f} +/- {R5N['err_ctrl_gobs']:.3f}; | y {R5N['slope_ctrl_y']:+.3f} +/- {R5N['err_ctrl_y']:.3f}); f_DM {R5['slope']:+.3f} +/- {R5['slope_err']:.3f}")
check("S5r the journal refit of row 87 leaves the native route unchanged (that disc is at the Newtonian floor on both tables): same N, slope and median a0 as on the arXiv-v1 table",
      R5N["N"] == _R5Nc["N"] and abs(R5N["slope"] - _R5Nc["slope"]) < 1e-12 and abs(R5N["median_a0"] / _R5Nc["median_a0"] - 1) < 1e-12,
      f"N {_R5Nc['N']} -> {R5N['N']}; slope {_R5Nc['slope']:+.4f} -> {R5N['slope']:+.4f}")
check("S5q AGAINST INTEREST: the native slope is calibration-conditional too -- a drift of -0.05 dex per unit z puts it within 1 sigma of constancy",
      abs(_tbN[-0.05]["sig_const"]) < 1.0, f"beta -0.05: {_tbN[-0.05]['slope']:+.3f} +/- {_tbN[-0.05]['err']:.3f} ({_tbN[-0.05]['sig_const']:+.1f} sigma)")

# ---- v3.3 (CFG310 #2): the native route is a CENSORED sample.  A disc outside the window (f <= 0.02: the native baryons supply
#      >= 98 per cent of g_obs) has an implied a0 BELOW the value at the window edge, a0 < a0(f = 0.02) = 0.98 g_obs/[ln 50]^2 (y -> inf
#      as f -> 0).  The floor fraction by redshift, a rank test of floor membership against z, a rank test of a0 against z with the
#      floor discs ranked lowest (the censoring kept), and a Tobit-type censored-regression slope with those per-disc upper limits.
#      Reproduces the CFG310 referee's M3 (computed there from CFG303's per-galaxy CSV, i.e. the arXiv-v1 table; here on the journal table).
from scipy.stats import spearmanr as _spearmanr, norm as _norm
_zN = np.array([g["z"] for g in GALN]); _goN = np.array([g["go"] for g in GALN]); _gbN = np.array([g["gbB"] for g in GALN])
_fN = 1 - _gbN / _goN; _okN = (_fN > 0.02) & (_fN < 0.98); _flN = _fN <= 0.02
_laN = np.where(_okN, np.log10(np.where(_okN, (1 - _fN) * _goN / np.log(1 / np.clip(_fN, 1e-9, None))**2, 1.0)), np.nan)
_lcapN = np.log10(0.98 * _goN / math.log(50.0)**2)                 # the upper limit on log a0 of a floor disc
FLOOR_BINS = []
for lo_, hi_ in ((0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 2.6)):
    m_ = (_zN >= lo_) & (_zN < hi_)
    _lc = np.where(_okN[m_], _laN[m_], -99.0); _med = float(np.median(_lc))
    FLOOR_BINS.append(dict(z=(lo_, hi_), n=int(m_.sum()), floor=int(_flN[m_].sum()), frac=float(_flN[m_].mean()),
                           median_log_a0_censored=None if _med < -50 else _med, median_log_a0_inverted=float(np.nanmedian(_laN[m_]))))
_sp_fl = _spearmanr(_zN, _flN.astype(int)); _sp_inv = _spearmanr(_zN[_okN], _laN[_okN]); _sp_cen = _spearmanr(_zN, np.where(_okN, _laN, -99.0))
def _tobit(z_, y_, cap_, ok_):
    zc_ = z_ - z_.mean()
    def nll(p_):
        a_, b_, ls_ = p_; s_ = math.exp(ls_); mu_ = a_ + b_ * zc_
        return -(np.sum(_norm.logpdf(y_[ok_], mu_[ok_], s_)) + np.sum(_norm.logcdf((cap_[~ok_] - mu_[~ok_]) / s_)))
    from scipy.optimize import minimize as _min
    r_ = _min(nll, [float(np.nanmedian(y_)), 0.0, math.log(0.4)], method="Nelder-Mead", options=dict(xatol=1e-8, fatol=1e-10, maxiter=20000))
    H_ = np.zeros((3, 3)); h_ = np.array([1e-4, 1e-4, 1e-4])            # numerical Hessian for the slope error
    for i_ in range(3):
        for j_ in range(3):
            e_i = np.eye(3)[i_] * h_[i_]; e_j = np.eye(3)[j_] * h_[j_]
            H_[i_, j_] = (nll(r_.x + e_i + e_j) - nll(r_.x + e_i - e_j) - nll(r_.x - e_i + e_j) + nll(r_.x - e_i - e_j)) / (4 * h_[i_] * h_[j_])
    return float(r_.x[1]), float(math.sqrt(np.linalg.inv(H_)[1, 1])), float(math.exp(r_.x[2]))
TOBIT = _tobit(_zN, np.where(_okN, _laN, 0.0), _lcapN, _okN)
_inA = np.array([g["inA"] for g in GALN]); _dMp = np.array([g["lMs"] - g["lMs_price"] for g in GALN if g["inA"]])
P("  v3.3 the native route as a censored sample (floor: f <= 0.02, an upper limit a0 < 0.98 g_obs/[ln 50]^2):")
for b_ in FLOOR_BINS:
    P(f"     z {b_['z'][0]:.1f}-{b_['z'][1]:.1f}: {b_['floor']:2d} of {b_['n']:2d} at the floor ({b_['frac']*100:.0f}%); median log a0 with the floor discs kept as the lowest values "
      + ("at the floor" if b_["median_log_a0_censored"] is None else f"{b_['median_log_a0_censored']:+.3f}") + f"; inverted discs only {b_['median_log_a0_inverted']:+.3f}")
P(f"     Spearman(z, at the floor) {_sp_fl.statistic:+.3f} (p {_sp_fl.pvalue:.3f}); Spearman(z, log a0) inverted only {_sp_inv.statistic:+.3f} (p {_sp_inv.pvalue:.3f});"
  f" with the floor discs ranked lowest {_sp_cen.statistic:+.3f} (p {_sp_cen.pvalue:.4f})")
P(f"     censored-regression (Tobit-type) slope with the per-disc upper limits: {TOBIT[0]:+.3f} +/- {TOBIT[1]:.3f} dex per unit z (scatter {TOBIT[2]:.2f} dex)")
P(f"     floor discs among the {int(_inA.sum())} with Price et al. (2021) masses (RC41): {int((_flN & _inA).sum())}; CFG303 col-6 SED log M* minus Price+21 SED log M* over those {len(_dMp)}: median {np.median(_dMp):+.3f} dex")
OUT["S5_native"]["censoring"] = dict(bins=[dict(b_, z=list(b_["z"])) for b_ in FLOOR_BINS], spearman_floor=[_sp_fl.statistic, _sp_fl.pvalue],
                                     spearman_inverted=[_sp_inv.statistic, _sp_inv.pvalue], spearman_censored=[_sp_cen.statistic, _sp_cen.pvalue],
                                     tobit=dict(slope=TOBIT[0], err=TOBIT[1], scatter=TOBIT[2]), n_floor_in_RC41=int((_flN & _inA).sum()), n_RC41=int(_inA.sum()),
                                     mstar_minus_price_median=float(np.median(_dMp)))
_r310 = json.load(open(os.path.join(CFG, "CFG310_second_referee", "cfg310_referee_checks_results.json")))["M3"]
check("S5s AGAINST INTEREST (CFG310 #2): the native route is censored in a redshift-dependent way -- 41 floor discs, a floor fraction rising from about a quarter (z < 1) to about a half (z > 2) "
      "with a rank test p < 0.05, and with the floor discs kept as the lowest values the implied a0 FALLS with z (p < 0.05), as the referee found (bin counts and both p identical to its M3)",
      int(_flN.sum()) == 41 and _flN.sum() + _okN.sum() == 100 and FLOOR_BINS[0]["frac"] < 0.3 and FLOOR_BINS[-1]["frac"] > 0.5 and _sp_fl.statistic > 0 and _sp_fl.pvalue < 0.05
      and _sp_cen.statistic < 0 and _sp_cen.pvalue < 0.05 and FLOOR_BINS[-1]["median_log_a0_censored"] is None
      and [(b_["n"], b_["floor"]) for b_ in FLOOR_BINS] == [(r_["n"], r_["floor"]) for r_ in _r310["bins"]]
      and abs(_sp_fl.pvalue - _r310["spearman_floor"][1]) < 1e-9 and abs(_sp_cen.pvalue - _r310["spearman_censored"][1]) < 1e-9,
      ", ".join(f"{b_['floor']}/{b_['n']}" for b_ in FLOOR_BINS) + f"; floor rho {_sp_fl.statistic:+.3f} p {_sp_fl.pvalue:.3f}; censored rho {_sp_cen.statistic:+.3f} p {_sp_cen.pvalue:.4f}")
check("S5u AGAINST INTEREST: with the floor discs carried as upper limits, the censored-regression slope of the native route is negative (the native baryons' calibration drifts with z; no law in Table 3 falls)",
      TOBIT[0] < 0 and TOBIT[0] < R5N["slope"], f"Tobit {TOBIT[0]:+.3f} +/- {TOBIT[1]:.3f}; window-only {R5N['slope']:+.3f}")
_txv = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
_q5 = [f"{FLOOR_BINS[0]['floor']} of {FLOOR_BINS[0]['n']} discs ({FLOOR_BINS[0]['frac']*100:.0f} per cent)", f"{FLOOR_BINS[1]['floor']} of {FLOOR_BINS[1]['n']} and {FLOOR_BINS[2]['floor']} of {FLOOR_BINS[2]['n']}",
       f"{FLOOR_BINS[3]['floor']} of {FLOOR_BINS[3]['n']} ({FLOOR_BINS[3]['frac']*100:.0f} per cent)", f"$p={_sp_fl.pvalue:.3f}$", f"$\\rho={_sp_cen.statistic:.2f}$, $p={_sp_cen.pvalue:.3f}$",
       f"$d\\log_{{10}}\\hat a_0/dz={TOBIT[0]:.2f}\\pm{TOBIT[1]:.2f}$, with a scatter of {TOBIT[2]:.1f} dex", f"(41, of which {int((_flN & _inA).sum())} are among the floor discs above)"]
check("S5v the text quotes the censoring numbers as computed (floor fractions by z, both rank tests, the censored slope and its scatter, the RC41 overlap)",
      all(q_ in _txv for q_ in _q5), "; ".join(q_ for q_ in _q5 if q_ not in _txv) or "all present", kind="identity")
# the stellar masses of the native route: CFG303's transcription of column 6 (arXiv v1 raster) against the journal's Table B1 column 6
# (extract_rc100_journal_col6.py, run on the publisher's PDF, which is not in the repository), and against Price et al. (2021)
RC100_J6 = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_tableB1_logMstar_JOURNAL.csv")
_j6 = {r["idx"]: r for r in csv.DictReader(open(RC100_J6, newline=""))}
_j6_ms = [i_ for i_ in _j6 if abs(float(_j6[i_]["logMstar_journal"]) - float(_TR[i_]["logMstar"])) > 1e-9]
_j6_mb = [r_["idx"] for r_ in csv.DictReader(open(RC100, newline="")) if abs(float(_j6[r_["idx"]]["logMbaryon_journal"]) - float(r_["logMbar_Msun"])) > 1e-9]
P(f"  journal Table B1 column 6 (SED log M*), 100 rows: differs from CFG303's arXiv-v1 transcription in {len(_j6_ms)} rows {_j6_ms}; control: its log M_baryon column differs from the CFG305 journal table in {len(_j6_mb)} rows")
OUT["S5_native"]["journal_col6"] = dict(n=len(_j6), mismatch_mstar=_j6_ms, mismatch_mbaryon_control=_j6_mb)
check("S5t the SED stellar masses of the native route (CFG303's transcription of column 6) equal the journal's Table B1 column 6 in all 100 rows (the extraction's log M_baryon column equals CFG305's journal table, as a control), and agree with Price et al. (2021) to a median of 0.00 dex for the RC41 galaxies",
      len(_j6) == 100 and not _j6_ms and not _j6_mb and abs(float(np.median(_dMp))) < 0.005, f"col 6 mismatches {_j6_ms}; control {_j6_mb}; median vs Price+21 {np.median(_dMp):+.3f}", kind="identity")

# ================================================================================================================
head("S6  THE DEEP REGIME IN TWO SURVEYS: SLOPE AND AMPLITUDE (SPARC and MIGHTEE-HI)")
# Window g_bar < 0.2 a0 at the FIXED canonical a0 (1.87e-11 m s^-2): it keeps 17 of MIGHTEE-HI's 19 galaxies with >= 3 points.
# Slope statistic: per-galaxy least-squares slope of log g_obs on log g_bar over the window (galaxies with >= 3 points), median
# over galaxies.  The kernel's own expectation is the SAME statistic on g_bar nu(g_bar/a0) at the same points.
MIGHTEE_CSV = os.path.join(ROOT, "deepseek_push", "data2", "mightee2025_rar_digitized_points.csv")
CORPUS_V7 = os.path.join(ROOT, "glm53_push", "data", "rotation_curve_corpus_v7.json")
WIN = 0.2 * a0_L
SIG_DIG = 0.036                                    # digitisation error of the MIGHTEE-HI points (dex)
# MIGHTEE-HI's own fits of the same kernel to all radii, Varasteanu et al. (2025), their Table 3, a0 [1e-10 m s^-2]
MIG_T3 = {"fiducial (spatially varying SED ratio, median 0.35)": (1.69, 0.13), "no molecular gas": (2.06, 0.15),
          "fixed Upsilon_K = 0.6": (1.08, 0.09), "radially averaged ratio": (1.47, 0.13)}
beta_of_y = lambda y: 1.0 + n_slope(y)             # d ln g_obs / d ln g_bar = 1 + d ln nu / d ln y
P("  the kernel's local slope beta(y) = 1 + n(y): " + ", ".join(f"y={y:g}: {float(beta_of_y(y)):.3f}" for y in (1e-6, 0.01, 0.05, 0.1, 0.2)))
def ols_b(x, y):
    xm = x.mean(); return float(np.sum((x - xm) * (y - y.mean())) / np.sum((x - xm)**2))
def groups_in_window(gbar, gidx):
    m = gbar < WIN
    return {k_: np.where(m & (gidx == k_))[0] for k_ in np.unique(gidx[m]) if np.sum(m & (gidx == k_)) >= 3}
def pg_median(gbar, gobs, grp):
    return float(np.median([ols_b(np.log10(gbar[i]), np.log10(gobs[i])) for i in grp.values()]))
def slope_test(gbar, gobs, grp, a0ref, draws=2000, seed=20260925):
    """median per-galaxy slope of the data, of the kernel at a0ref at the same points, and a paired galaxy bootstrap"""
    keys = list(grp); kern = gbar * nu(gbar / a0ref)
    bd = np.array([ols_b(np.log10(gbar[grp[k_]]), np.log10(gobs[grp[k_]])) for k_ in keys])
    bk = np.array([ols_b(np.log10(gbar[grp[k_]]), np.log10(kern[grp[k_]])) for k_ in keys])
    rng_ = np.random.default_rng(seed); dd, db = [], []
    for _ in range(draws):
        p_ = rng_.integers(0, len(keys), len(keys)); dd.append(np.median(bd[p_]) - np.median(bk[p_])); db.append(np.median(bd[p_]))
    return dict(n_gal=len(keys), n_pts=int(sum(len(v) for v in grp.values())), beta=float(np.median(bd)), beta_kernel=float(np.median(bk)),
                delta=float(np.median(bd) - np.median(bk)), se_delta=float(np.std(dd)), se_beta=float(np.std(db)))
def amp_fit(gbar, gobs, ew_, gidx, draws=300, seed=7):
    """a0 of equation (4) fitted in the window (errors: quoted + 0.034 dex), galaxy bootstrap on ln a0"""
    m = gbar < WIN; a0w = fit_a0(gbar[m], gobs[m], ew_[m])[0]
    keys = np.unique(gidx[m]); sel_ = {k_: np.where(m & (gidx == k_))[0] for k_ in keys}
    rng_ = np.random.default_rng(seed); la_ = []
    for _ in range(draws):
        idx = np.concatenate([sel_[k_] for k_ in rng_.choice(keys, len(keys))]); la_.append(math.log(fit_a0(gbar[idx], gobs[idx], ew_[idx])[0]))
    return dict(a0=a0w, se_ln=float(np.std(la_)), kappa_L=a0w / A_L, kappa_C=a0w / A_C, n_pts=int(m.sum()), n_gal=int(len(keys)))
# ---- MIGHTEE-HI (digitised; the marker colour encodes each galaxy's baryonic surface density, so one colour = one galaxy)
import csv as _csv
_rows = list(_csv.DictReader(open(MIGHTEE_CSV)))
mgb = np.array([10**float(r["log10_gbar"]) for r in _rows]); mgo = np.array([10**float(r["log10_gobs"]) for r in _rows])
_cols = {}; mgi = np.array([_cols.setdefault((r["color_r"], r["color_g"], r["color_b"]), len(_cols)) for r in _rows])
mew = np.full(mgb.size, SIG_DIG)
mig_grp = groups_in_window(mgb, mgi)
S6 = dict(window=WIN, beta_of_y={str(y): float(beta_of_y(y)) for y in (1e-6, 0.01, 0.05, 0.1, 0.2)}, sparc={}, mightee={})
S6["mightee"]["slope_L"] = slope_test(mgb, mgo, mig_grp, a0_L); S6["mightee"]["slope_C"] = slope_test(mgb, mgo, mig_grp, a0_C)
S6["mightee"]["amp"] = amp_fit(mgb, mgo, mew, mgi)
_gsz = {k_: int((mgi == k_).sum()) for k_ in np.unique(mgi)}; _big = max(_gsz, key=_gsz.get)
_big_span = float(np.ptp(np.log10(mgb[mgi == _big])))
_keep = mgi != _big; _grp_nb = groups_in_window(mgb[_keep], mgi[_keep])
S6["mightee"]["slope_L_without_largest_group"] = slope_test(mgb[_keep], mgo[_keep], _grp_nb, a0_L)
S6["mightee"]["colour_groups"] = dict(n_groups=len(_gsz), largest=_gsz[_big], largest_span_dex=_big_span, sizes=sorted(_gsz.values()))
S6["mightee"]["n_points_total"] = int(mgb.size); S6["mightee"]["n_groups_total"] = len(_cols); S6["mightee"]["n_in_window"] = int((mgb < WIN).sum())
S6["mightee"]["table3"] = {k_: dict(a0=v_[0] * 1e-10, err=v_[1] * 1e-10, kappa_L=v_[0] * 1e-10 / A_L, kappa_C=v_[0] * 1e-10 / A_C, se_ln=v_[1] / v_[0]) for k_, v_ in MIG_T3.items()}
# ---- SPARC at three disc ratios (bulge 0.7, velocity errors < 10 per cent)
for UD in (0.5, 0.6, 0.7):
    g1, g2, e1, _ = load_sparc(UD=UD, UB=0.7); gi1 = GAL_INDEX[0].copy()
    grp1 = groups_in_window(g1, gi1)
    S6["sparc"][UD] = dict(slope_L=slope_test(g1, g2, grp1, a0_L), slope_C=slope_test(g1, g2, grp1, a0_C), amp=amp_fit(g1, g2, e1, gi1))
# ---- pooled slope (inverse variance over SPARC at one disc ratio + MIGHTEE-HI), and the power against slopes the kernel does not have
for UD in (0.5, 0.6, 0.7):
    a_, b_ = S6["sparc"][UD]["slope_L"], S6["mightee"]["slope_L"]
    w_ = np.array([1 / a_["se_delta"]**2, 1 / b_["se_delta"]**2]); d_ = np.array([a_["delta"], b_["delta"]])
    wb_ = np.array([1 / a_["se_beta"]**2, 1 / b_["se_beta"]**2]); bb_ = np.array([a_["beta"], b_["beta"]])
    pb, pse = float(np.sum(wb_ * bb_) / np.sum(wb_)), float(1 / math.sqrt(np.sum(wb_)))
    S6["sparc"][UD]["pooled"] = dict(delta=float(np.sum(w_ * d_) / np.sum(w_)), se_delta=float(1 / math.sqrt(np.sum(w_))), beta=pb, se_beta=pse,
                                     z_075=(0.75 - pb) / pse, z_1=(1.0 - pb) / pse)
P(f"  window g_bar < {WIN:.3e} m s^-2 (0.2 a0 at the canonical value);  MIGHTEE-HI: {S6['mightee']['n_in_window']} of {mgb.size} digitised points, "
  f"{len(mig_grp)} of {len(_cols)} galaxies with >= 3 points")
P(f"  {'sample':22s} {'N_gal':>5s} {'N_pts':>5s} {'beta':>6s} {'+/-':>5s} {'kernel':>6s} {'delta':>7s} {'+/-':>5s} {'z':>6s} | {'kernel(crit)':>12s} {'z':>6s} | {'kappa_L':>7s} {'+/-':>5s} {'kappa_C':>7s}")
def _row(lab, d):
    sL, sC, am = d["slope_L"], d["slope_C"], d["amp"]
    P(f"  {lab:22s} {sL['n_gal']:5d} {sL['n_pts']:5d} {sL['beta']:6.3f} {sL['se_beta']:5.3f} {sL['beta_kernel']:6.3f} {sL['delta']:+7.3f} {sL['se_delta']:5.3f} {sL['delta']/sL['se_delta']:+6.2f} | "
      f"{sC['beta_kernel']:12.3f} {sC['delta']/sC['se_delta']:+6.2f} | {am['kappa_L']:7.3f} {am['kappa_L']*am['se_ln']:5.3f} {am['kappa_C']:7.3f}")
for UD in (0.5, 0.6, 0.7): _row(f"SPARC Ups_disc = {UD}", S6["sparc"][UD])
_row("MIGHTEE-HI (digitised)", S6["mightee"])
for UD in (0.5, 0.6, 0.7):
    p_ = S6["sparc"][UD]["pooled"]
    P(f"  pooled with SPARC at {UD}: delta {p_['delta']:+.3f} +/- {p_['se_delta']:.3f} (z {p_['delta']/p_['se_delta']:+.2f});  beta {p_['beta']:.3f} +/- {p_['se_beta']:.3f}: "
      f"{p_['z_075']:.1f} sigma from 0.75, {p_['z_1']:.1f} sigma from 1")
P("  MIGHTEE-HI's own fits (Varasteanu et al. 2025, Table 3):  " + ";  ".join(f"{k_}: a0 = {v_['a0']/1e-10:.2f}e-10, kappa_L = {v_['kappa_L']:.3f} +/- {v_['kappa_L']*v_['se_ln']:.3f}" for k_, v_ in S6["mightee"]["table3"].items()))
P(f"  our window fit to the digitised points: a0 = {S6['mightee']['amp']['a0']/1e-10:.3f}e-10 ({(S6['mightee']['amp']['a0']/1.69e-10-1)*100:+.1f}% from their fiducial)")
_cg = S6["mightee"]["colour_groups"]; _mw0 = S6["mightee"]["slope_L_without_largest_group"]
P(f"  colour groups: {_cg['n_groups']} for the survey's 19 galaxies; largest {_cg['largest']} points spanning {_cg['largest_span_dex']:.2f} dex in g_bar; without it: {_mw0['n_gal']} galaxies, beta {_mw0['beta']:.3f} +/- {_mw0['se_beta']:.3f} vs kernel {_mw0['beta_kernel']:.3f} (z {_mw0['delta']/_mw0['se_delta']:+.2f})")
def zamp(a, sa, b, sb):          # difference in ln a0, in combined standard errors
    return (math.log(a) - math.log(b)) / math.sqrt(sa**2 + sb**2)
for key_ in ("fiducial (spatially varying SED ratio, median 0.35)", "fixed Upsilon_K = 0.6"):
    t_ = S6["mightee"]["table3"][key_]
    zs = [zamp(t_["a0"], t_["se_ln"], S6["sparc"][UD]["amp"]["a0"], S6["sparc"][UD]["amp"]["se_ln"]) for UD in (0.5, 0.6, 0.7)]
    S6["mightee"]["table3"][key_]["z_vs_sparc"] = zs
    P(f"  MIGHTEE-HI [{key_}] minus SPARC (Ups_disc 0.5/0.6/0.7), in combined sigma of ln a0: " + ", ".join(f"{z_:+.1f}" for z_ in zs))
# ---- injection: the slope statistic returns a known slope (kernel-consistent data; a pure power law of slope 0.75)
g1, g2, e1, _ = load_sparc(UD=0.6, UB=0.7); gi1 = GAL_INDEX[0].copy(); grp1 = groups_in_window(g1, gi1)
rng6 = np.random.default_rng(662607); sig1 = np.sqrt(e1**2 + SIG_INT**2); sigm = np.sqrt(SIG_DIG**2 + SIG_INT**2)
inj6 = dict(kernel_sparc=[], kernel_mig=[], p075_sparc=[], p075_mig=[])
bk_s = pg_median(g1, g1 * nu(g1 / a0_L), grp1); bk_m = pg_median(mgb, mgb * nu(mgb / a0_L), mig_grp)
for _ in range(200):
    inj6["kernel_sparc"].append(pg_median(g1, g1 * nu(g1 / a0_L) * 10**(rng6.normal(0, 1, g1.size) * sig1), grp1) - bk_s)
    inj6["kernel_mig"].append(pg_median(mgb, mgb * nu(mgb / a0_L) * 10**(rng6.normal(0, 1, mgb.size) * sigm), mig_grp) - bk_m)
    inj6["p075_sparc"].append(pg_median(g1, a0_L * (g1 / a0_L)**0.75 * 10**(rng6.normal(0, 1, g1.size) * sig1), grp1))
    inj6["p075_mig"].append(pg_median(mgb, a0_L * (mgb / a0_L)**0.75 * 10**(rng6.normal(0, 1, mgb.size) * sigm), mig_grp))
inj6s = {k_: (float(np.mean(v_)), float(np.std(v_))) for k_, v_ in inj6.items()}
P("  injection (200 draws; quoted errors + 0.034 dex; digitisation 0.036 dex): returned minus kernel slope, SPARC "
  f"{inj6s['kernel_sparc'][0]:+.4f} +/- {inj6s['kernel_sparc'][1]:.3f}, MIGHTEE {inj6s['kernel_mig'][0]:+.4f} +/- {inj6s['kernel_mig'][1]:.3f};  "
  f"a slope-0.75 power law returns {inj6s['p075_sparc'][0]:.4f} (SPARC), {inj6s['p075_mig'][0]:.4f} (MIGHTEE)")
S6["injection"] = inj6s
# ---- the pitfall: per-galaxy disc ratios fitted to the rotation curves themselves (an earlier compilation), applied to disc and bulge
_corp = json.load(open(CORPUS_V7)); _ml = {g_["galaxy"]: g_["m2l_disk"] for g_ in _corp["galaxies"] if g_.get("survey") == "SPARC" and g_.get("m2l_disk")}
kb, ko, ke, ki, mlk, mln = [], [], [], [], [], []
for f in sorted(glob.glob(os.path.join(SPARC, "*_rotmod.dat"))):
    nm = os.path.basename(f).replace("_rotmod.dat", "")
    d = _read(f)
    if nm not in _ml or d.ndim != 2 or d.shape[1] < 6: continue
    R, V, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
    S_, T_ = Vd**2 + Vb**2, V**2 - np.sign(Vg) * Vg**2; okn = S_ > 0
    if okn.sum() >= 3: mlk.append(_ml[nm]); mln.append(float(np.sum(T_[okn] * S_[okn]) / np.sum(S_[okn]**2)))
    _sc = HF_R1 if FD.get(nm) == 1 else 1.0                                   # the paper's distance convention, as everywhere
    m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < 0.10)
    v2 = (np.sign(Vg) * Vg**2 + _ml[nm] * (Vd**2 + Vb**2))[m]; ok = v2 > 0
    if ok.sum() == 0: continue
    kb.append(v2[ok] / R[m][ok] * K); ko.append(V[m][ok]**2 / R[m][ok] * K / _sc); ke.append((2 * eV[m] / V[m] / math.log(10))[ok]); ki.append(np.full(ok.sum(), len(ki)))
kb, ko, ke, ki = (np.concatenate(x_) for x_ in (kb, ko, ke, ki))
r_kin = float(np.corrcoef(np.log10(mlk), np.log10(np.clip(mln, 1e-3, None)))[0, 1])
amp_kin = amp_fit(kb, ko, ke, ki)
fac_kin = [S6["sparc"][UD]["amp"]["a0"] / amp_kin["a0"] for UD in (0.5, 0.6, 0.7)]
S6["kinematic_ratios"] = dict(n=len(mlk), median=float(np.median(mlk)), max=float(np.max(mlk)), r_log=r_kin, amp=amp_kin, factor_vs_population=fac_kin)
P(f"  PITFALL: per-galaxy disc ratios fitted to the curves (median {np.median(mlk):.2f}, max {np.max(mlk):.1f}; log-correlation with the Newtonian no-dark-matter ratio r = {r_kin:.3f}, N = {len(mlk)}):")
P(f"     window kappa_L = {amp_kin['kappa_L']:.3f} +/- {amp_kin['kappa_L']*amp_kin['se_ln']:.3f}, lower than the population-ratio values by a factor " + ", ".join(f"{x_:.2f}" for x_ in fac_kin))
OUT["S6"] = S6
check("S6a the kernel's local slope is 1/2 in the deep limit and 0.60 at y = 0.2 (beta = 1 + n(y))",
      abs(float(beta_of_y(1e-6)) - 0.5) < 1e-3 and abs(float(beta_of_y(0.2)) - 0.603) < 0.002, f"{float(beta_of_y(1e-6)):.4f}, {float(beta_of_y(0.2)):.4f}", kind="identity")
check("S6b the per-galaxy deep slope agrees with the kernel's own slope at the same points: |z| < 3 for SPARC at each disc ratio, for MIGHTEE-HI, and pooled",
      all(abs(S6["sparc"][u]["slope_L"]["delta"] / S6["sparc"][u]["slope_L"]["se_delta"]) < 3 and abs(S6["sparc"][u]["pooled"]["delta"] / S6["sparc"][u]["pooled"]["se_delta"]) < 3 for u in (0.5, 0.6, 0.7))
      and abs(S6["mightee"]["slope_L"]["delta"] / S6["mightee"]["slope_L"]["se_delta"]) < 3,
      ", ".join(f"{S6['sparc'][u]['slope_L']['delta']/S6['sparc'][u]['slope_L']['se_delta']:+.2f}" for u in (0.5, 0.6, 0.7)) + f"; MIGHTEE {S6['mightee']['slope_L']['delta']/S6['mightee']['slope_L']['se_delta']:+.2f}")
check("S6c the same data exclude the Newtonian slope (beta = 1) at more than 5 sigma, pooled, at every disc ratio",
      all(S6["sparc"][u]["pooled"]["z_1"] > 5 for u in (0.5, 0.6, 0.7)), ", ".join(f"{S6['sparc'][u]['pooled']['z_1']:.1f}" for u in (0.5, 0.6, 0.7)))
check("I6 the slope statistic measures: on kernel-consistent data it is unbiased to 0.01, and on a slope-0.75 power law it returns 0.75 to 0.01",
      abs(inj6s["kernel_sparc"][0]) < 0.01 and abs(inj6s["kernel_mig"][0]) < 0.01 and abs(inj6s["p075_sparc"][0] - 0.75) < 0.01 and abs(inj6s["p075_mig"][0] - 0.75) < 0.01,
      f"{inj6s['kernel_sparc'][0]:+.4f}, {inj6s['kernel_mig'][0]:+.4f}; {inj6s['p075_sparc'][0]:.4f}, {inj6s['p075_mig'][0]:.4f}", kind="injection")
check("S6e the window fit to the digitised MIGHTEE-HI points reproduces the survey's own fiducial a0 (1.69e-10) within 5 per cent",
      abs(S6["mightee"]["amp"]["a0"] / 1.69e-10 - 1) < 0.05, f"{S6['mightee']['amp']['a0']:.3e}")
# ---- a straight line across ALL SPARC points in the window (exposed to galaxy-to-galaxy offsets), against the kernel at the same points
pooled_all = {}
for UD in (0.5, 0.6, 0.7):
    g1, g2, e1, _ = load_sparc(UD=UD, UB=0.7); gi1 = GAL_INDEX[0].copy(); m = g1 < WIN
    keys = np.unique(gi1[m]); sel_ = {k_: np.where(m & (gi1 == k_))[0] for k_ in keys}; rng_ = np.random.default_rng(5)
    kern_ = lambda gg: np.log10(gg * nu(gg / a0_L))
    bd_, bk_ = ols_b(np.log10(g1[m]), np.log10(g2[m])), ols_b(np.log10(g1[m]), kern_(g1[m]))
    dd_ = []
    for _ in range(1000):
        idx = np.concatenate([sel_[k_] for k_ in rng_.choice(keys, len(keys))])
        dd_.append(ols_b(np.log10(g1[idx]), np.log10(g2[idx])) - ols_b(np.log10(g1[idx]), kern_(g1[idx])))
    pooled_all[UD] = dict(beta=bd_, beta_kernel=bk_, se=float(np.std(dd_)), z=float((bd_ - bk_) / np.std(dd_)))
S6["sparc_all_points"] = pooled_all
P("  one straight line across all SPARC points in the window: " + ";  ".join(f"Ups {u}: {v['beta']:.3f} vs kernel {v['beta_kernel']:.3f} (z {v['z']:+.2f})" for u, v in pooled_all.items()))
OUT["S6"] = S6
zf = S6["mightee"]["table3"]["fiducial (spatially varying SED ratio, median 0.35)"]["z_vs_sparc"]; z6 = S6["mightee"]["table3"]["fixed Upsilon_K = 0.6"]["z_vs_sparc"]
kS = [S6["sparc"][u]["amp"]["kappa_L"] for u in (0.5, 0.6, 0.7)]
check("S6d a straight line across all SPARC points in the window, exposed to galaxy-to-galaxy offsets, also agrees with the kernel's (|z| < 2 at every disc ratio)",
      all(abs(v["z"]) < 2 for v in pooled_all.values()), ", ".join(f"{v['z']:+.2f}" for v in pooled_all.values()))
check("S6f AGAINST INTEREST: at MIGHTEE-HI's own SED mass-to-light ratios the two surveys disagree on a0 by more than 3 sigma at every SPARC disc ratio",
      all(z_ > 3 for z_ in zf), ", ".join(f"{z_:+.1f}" for z_ in zf))
check("S6g AGAINST FULL AGREEMENT: at a fixed Upsilon_K = 0.6 (the survey's own refit) the two surveys agree within 2.5 sigma for SPARC Upsilon_disc 0.5 and 0.6 but not at 0.7, and going from the SED ratios to the fixed ratio moves the disagreement by more than 4 sigma at every disc ratio",
      z6[0] < 2.5 and z6[1] < 2.5 and z6[2] > 2.5 and all(a_ - b_ > 4 for a_, b_ in zip(zf, z6)), ", ".join(f"{z_:+.1f}" for z_ in z6))
check("S6h the SPARC window amplitude brackets kappa_Lambda = 1/2 across Upsilon_disc = 0.5-0.7", kS[0] > 0.5 > kS[2], ", ".join(f"{k_:.3f}" for k_ in kS))
check("S6i PITFALL: per-galaxy ratios fitted to the curves (log-correlation > 0.8 with the Newtonian no-dark-matter ratio) lower the window kappa by a factor above 1.5 at every disc ratio",
      r_kin > 0.8 and min(fac_kin) > 1.5, f"r = {r_kin:.3f}; factors " + ", ".join(f"{x_:.2f}" for x_ in fac_kin))
_mw = S6["mightee"]["slope_L_without_largest_group"]
check("S6k the MIGHTEE-HI slope result does not hinge on the colour-group identification: without the largest group (11 points spanning 0.22 dex in g_bar, possibly two galaxies) the per-galaxy slope still agrees with the kernel's (|z| < 2)",
      S6["mightee"]["colour_groups"]["n_groups"] == 18 and S6["mightee"]["colour_groups"]["largest"] == 11 and abs(_mw["delta"] / _mw["se_delta"]) < 2,
      f"{_mw['n_gal']} galaxies, beta {_mw['beta']:.3f} vs kernel {_mw['beta_kernel']:.3f} (z {_mw['delta']/_mw['se_delta']:+.2f})")
check("S6j the pooled per-galaxy slope excludes a slope of 0.75 at more than 4 sigma at every disc ratio",
      all(S6["sparc"][u]["pooled"]["z_075"] > 4 for u in (0.5, 0.6, 0.7)), ", ".join(f"{S6['sparc'][u]['pooled']['z_075']:.1f}" for u in (0.5, 0.6, 0.7)))

# ================================================================================================================
head("S7  THE HIGH-REDSHIFT RECORD AFTER 2026-09-25, READ FROM THE COMMITTED LANE OUTPUTS")
def _J(*parts): return json.load(open(os.path.join(CFG, *parts)))
S7 = {}
# ---- MUSE-DARK: the implied a0 in redshift thirds by baryon route (CFG262, reading bD) and the route contrast (CFG236)
_m262 = _J("CFG262_musedark_zthirds_by_route", "cfg262_stageB_results.json")["numbers"]
MD = {r: _m262["diff"][f"bD|{r}"] for r in ("i", "ii", "iii")}
MDz = [_m262["rows"][f"z{k}-routei-bD"]["z"] for k in (1, 2, 3)]
_m236 = _J("CFG236_musedark_referee", "CFG236_main_results.json")["P1"]["dstar"]
_c236 = _J("CFG236_musedark_referee", "CFG236_attack_c_results.json")
_t236 = _c236["decision"]["tau_star_i"]; _dM = (_c236["C3"]["dM"], *_c236["C3"]["dM_ci"])          # the drift at fixed SED stellar mass
for r, lab in (("i", "fitted DC14 masses"), ("ii", "SED M* + H2"), ("iii", "SED M*, no H2")):
    d = MD[r]; P(f"  MUSE-DARK route ({r}) {lab:18s}: log s*(third 3) - log s*(third 1) = {d['d']:+.3f} +/- {d['sd']:.3f}  (H(z) expects {d['rival']:+.3f}; constancy 0)"
                 f"  -> {d['d']/d['sd']:+.1f} sigma from constancy, {(d['d']-d['rival'])/d['sd']:+.1f} sigma from H(z)")
P(f"  thirds at z = " + " / ".join(f"{z:.2f}" for z in MDz) + f";  fitted-minus-SED mass drift {_m236['b']:+.3f} [{_m236['lo']:+.3f}, {_m236['hi']:+.3f}] dex per unit z (N {_m236['n']});"
  f" at fixed SED stellar mass {_dM[0]:+.3f} [{_dM[1]:+.3f}, {_dM[2]:+.3f}]; SED-mass bias needed to restore the rise on route (ii): {_t236['R198']:.2f} / {_t236['R199a']:.2f} dex per unit z")
S7["musedark"] = dict(routes=MD, z_thirds=MDz, drift=_m236, drift_fixed_mstar=_dM, tau_star=_t236)
# ---- the MUSE-DARK and KURVS lanes invert the repository's monotone function nu_mono (CFG4_common), not equation (nu) itself
sys.path.insert(0, CFG)
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()):
    import CFG4_common as _K4
_yy = np.logspace(-3, 2, 5001); _dnu = np.abs(_K4.nu_mono(_yy) / nu(_yy) - 1)
NUMONO = dict(max_below_1=float(_dnu[_yy <= 1].max()), max_1_100=float(_dnu[_yy > 1].max()), y_first_1e6=float(_yy[np.argmax(_dnu > 1e-6)]))
P(f"  the lanes' nu_mono against equation (nu): max |dnu/nu| {NUMONO['max_below_1']:.1e} for y <= 1, {NUMONO['max_1_100']*100:.2f}% for 1 < y <= 100 (first exceeds 1e-6 at y = {NUMONO['y_first_1e6']:.2f})")
S7["nu_mono"] = NUMONO
check("S7m the lanes' interpolating function equals equation (nu) to 1e-6 for y <= 1 and to 2.5 per cent for 1 < y <= 100", NUMONO["max_below_1"] < 1e-6 and NUMONO["max_1_100"] < 0.025,
      f"{NUMONO['max_below_1']:.1e}, {NUMONO['max_1_100']*100:.2f}%", kind="model")
# ---- KURVS-CDFS at z ~ 1.5 (CFG140, CFG160, CFG165, CFG189, CFG194)
_l140 = [l for l in open(os.path.join(CFG, "CFG140_kurvs_a0z.out")) if "KURVS-3 z 1.54" in l][0]
KY = [float(x) for x in re.findall(r"g_bar/a0 ([0-9.]+)", _l140)]
_k160 = _J("CFG160_kurvs_kretschmer_results.json")["numbers"]
_kc = _k160["decision_cell"]["P4 primary"]; _ka = _k160["decision_cell"]["alpha x 0.6"]; _km = _k160["grids"]["P4 primary"]["grid"]["1.5|0.0|canonical"]
KZ = dict(cell=(_kc["df"] / _kc["edf"], _kc["dh"] / _kc["edh"]), alpha06=(_ka["df"] / _ka["edf"], _ka["dh"] / _ka["edh"]), mu15=(_km["df"] / _km["edf"], _km["dh"] / _km["edh"]))
_h1 = [c_ for c_ in _J("CFG189_kurvs_measured_markers", "cfg189_measured_markers_results.json")["checks"] if c_["name"].startswith("H1")][0]["detail"]
_mm = re.search(r"reads flat ([+-][0-9.]+) sigma, rival ([+-][0-9.]+)", _h1); KZ["markers"] = (float(_mm.group(1)), float(_mm.group(2)))
KVS = _J("CFG194_measured_markers_referee", "CFG194_attacks_a_results.json")["A8"]["cross"]["flat=+2 (lean rival ends below)"]
_pw = _J("CFG165_kurvs_referee", "CFG165_power_results.json"); KLR = [_pw[f"165|{n}|LR"][k] for n in ("N1", "N2") for k in ("gauss", "kde")]
P(f"  KURVS: outermost points at g_bar/a0 = {min(KY):.2f}-{max(KY):.2f} (N {len(KY)});  decision cell (Kretschmer pressure, mu 0.67): constant {KZ['cell'][0]:+.1f} sigma, H(z) {KZ['cell'][1]:+.1f} sigma;"
  f" alpha x 0.6: {KZ['alpha06'][0]:+.1f} / {KZ['alpha06'][1]:+.1f};  mu 1.5: {KZ['mu15'][0]:+.1f} / {KZ['mu15'][1]:+.1f};  measured outer markers: {KZ['markers'][0]:+.1f} / {KZ['markers'][1]:+.1f}")
P(f"  KURVS: the lean ends for a coherent velocity scale {KVS:.4f} ({(1-KVS)*100:.1f} per cent lower); likelihood ratio (rival/constant) with gas and pressure as nuisances {min(KLR):.2f}-{max(KLR):.2f}")
S7["kurvs"] = dict(y_outer=[min(KY), max(KY)], z=KZ, v_scale=KVS, LR=KLR)
# ---- MIGHTEE-HI / LADUMA (CFG279 from the published fits; CFG258 mocks)
_n279 = _J("CFG279_mightee_published_values", "cfg279_results.json")["numbers"]
MB = _n279["b_E2"]; MPF = _n279["pulls"]["FLAT"]["F"]["pull"]; MPR = _n279["pulls"]["RIVAL"]["F"]["pull"]
_tab = _n279["reported_only"]["table"]
MA = {u: [r for r in _tab if r["sample"] == "MIGHTEE+LADUMA+SPARC" and r["upsilon"] == u and r["relation"] == "RAR"][0] for u in ("varying", "constant 0.6")}
_f258 = _J("CFG258_mightee_a0z_preflight", "cfg258_posthoc_formal_results.json")
M258 = dict(ratio=_f258["off"]["E1 library anchor"]["ratio_sd_over_formal"], z3_none=_f258["off"]["E1 library anchor"]["frac_z_gt3"], z3_B=_f258["B"]["E1 library anchor"]["frac_z_gt3"])
M_rival = float(E(0.09))
P(f"  MIGHTEE-HI/LADUMA: within-sample slope b = a1/a0 = {MB[0]:+.2f} +/- {MB[1]:.2f} per unit z (constancy {MPF:+.2f} sigma, H(z) {MPR:+.2f} sigma); a0 ~ H(z) changes a0 by x{M_rival:.3f} at z = 0.09")
P(f"  MIGHTEE-HI/LADUMA anchored to SPARC: a1 = {MA['varying']['a1']:+.2f} +/- {MA['varying']['err']:.2f} (varying M/L) vs {MA['constant 0.6']['a1']:+.2f} +/- {MA['constant 0.6']['err']:.2f} (constant 0.6) x 1e-10 per unit z;"
  f" mocks: empirical/formal scatter {M258['ratio']:.1f}, formal z > 3 under constancy in {M258['z3_none']*100:.0f}-{M258['z3_B']*100:.0f} per cent")
S7["mightee"] = dict(b=MB, pull_flat=MPF, pull_rival=MPR, anchored=MA, cfg258=M258, rival_x=M_rival)
# ---- z >= 4 (CFG269): the power P = gap / larger error, common-mode calibration c = 0.15 dex (G1: c = 0.30)
_b269 = _J("CFG269_highest_z_dynamics", "cfg269_results.json")["bins"]
_c269 = [l_ for l_ in open(os.path.join(CFG, "CFG269_highest_z_dynamics", "cfg269_discriminate.out")) if "] C1 HZQ rows" in l_][0]
C269_C1_FAIL = "[FAIL]" in _c269
P(f"  CFG269's committed run, its own frozen control C1: {_c269.strip()[:150]}")
for k_, v in _b269.items():
    P(f"  CFG269 {k_:24s} n {v['n']:3d}  P {v['P_range'][0]:.2f}-{v['P_range'][1]:.2f}  {v['verdict']:13s}  at c = 0.30: {', '.join(v['G1_verdicts'])}  {'; '.join(v['G4'])}")
S7["z4_14"] = {k_: dict(n=v["n"], P=v["P_range"], verdict=v["verdict"], G1=v["G1_verdicts"], G4=v["G4"]) for k_, v in _b269.items()}
# ---- the gas calibration at z ~ 2.2: ACE's dust-to-CO ratio against Stripe82 (CFG224b), the prescription bracket of PAPER38
_ace = _J("CFG224_gas_calibration", "cfg224b_conversion_drift_results.json")["ace"]
GAS = (abs(_ace["posthoc"]["delta_slope1"]), abs(_ace["delta"]))
P(f"  gas prescriptions at z ~ 2.2 (ACE vs Stripe82 at fixed metallicity, by metallicity slope): {GAS[0]:.2f}-{GAS[1]:.2f} dex")
S7["gas_bracket"] = GAS
# ---- the source-table audit (CFG287)
_a287 = _J("CFG287_source_table_integrity", "cfg287_results.json")
_tr = {k_: v for k_, v in _a287["transcription"].items() if "status" in v}      # the 29 transcribed tables (the verbatim-fragment check is separate)
AUD = dict(tables=len(_tr), cells=sum(v.get("sample_n", v.get("cells", 0)) if "sample_n" in v else v.get("cells", 0) for v in _tr.values()),
           fails=sum(v.get("sample_fail", 0) + len(v.get("fail_paper_values", [])) for v in _tr.values()),
           papers=sum(1 for v in _a287["versions"]["papers"].values() if v["erratum"].startswith("none registered")),
           errata=sum(1 for v in _a287["versions"]["papers"].values() if not (v["erratum"].startswith("none registered") or v["erratum"] == "n/a")),
           registered=len(_a287["versions"]["summary"]["registered_errata"]), passed=all(v["status"] == "PASS" for v in _tr.values()),
           sources=len(_a287["sources"]), kurvs_in=any("KURVS" in k_.upper() for k_ in _a287["sources"]))
P(f"  CFG287 audit: {AUD['cells']} sampled cells in {AUD['tables']} tables, {AUD['fails']} transcription mismatches; {AUD['papers']} published papers with no erratum registered, {AUD['errata']} with one (registered list: {AUD['registered']})")
S7["audit"] = AUD
OUT["S7"] = S7
check("S7a MUSE-DARK by route (CFG262, CFG236) as quoted: route rises +0.57 +/- 0.09 / -0.11 +/- 0.49 / +0.04 +/- 0.14 dex between the thirds at z 0.52 and 1.20 (H(z) +0.18); mass drift -0.72 [-0.97, -0.50] dex/z (-0.43 [-0.72, -0.15] at fixed SED mass); needed SED bias 1.8-2.2 dex/z",
      [round(MD[r]["d"], 2) for r in ("i", "ii", "iii")] == [0.57, -0.11, 0.04] and [round(MD[r]["sd"], 2) for r in ("i", "ii", "iii")] == [0.09, 0.49, 0.14]
      and round(MD["i"]["rival"], 2) == 0.18 and [round(z_, 2) for z_ in MDz] == [0.52, 0.88, 1.20]
      and [round(_m236["b"], 2), round(_m236["lo"], 2), round(_m236["hi"], 2)] == [-0.72, -0.97, -0.50] and [round(_t236["R198"], 1), round(_t236["R199a"], 1)] == [1.8, 2.2]
      and [round(x, 2) for x in _dM] == [-0.43, -0.72, -0.15], kind="identity")
check("S7b the MUSE-DARK rise depends on the baryon route: the fitted-mass route rises >5 sigma above constancy and >3 sigma above H(z), while neither SED route excludes either law at 2 sigma",
      MD["i"]["d"] / MD["i"]["sd"] > 5 and (MD["i"]["d"] - MD["i"]["rival"]) / MD["i"]["sd"] > 3
      and all(abs(MD[r]["d"]) / MD[r]["sd"] < 2 and abs(MD[r]["d"] - MD[r]["rival"]) / MD[r]["sd"] < 2 for r in ("ii", "iii")),
      ", ".join(f"({r}) {MD[r]['d']/MD[r]['sd']:+.1f} / {(MD[r]['d']-MD[r]['rival'])/MD[r]['sd']:+.1f} sigma" for r in ("i", "ii", "iii")), kind="identity")
check("S7c KURVS as quoted (CFG140/160/165/189/194): outer g_bar/a0 0.06-0.67; cell +3.3/-0.1 sigma; measured markers +2.4/-0.4; mu 1.5 +1.2/-2.1; alpha x 0.6 +1.3/-2.0; 4.5 per cent velocity scale; likelihood ratio 0.5-1.7",
      len(KY) == 10 and (min(KY), max(KY)) == (0.06, 0.67) and [round(x, 1) for x in KZ["cell"]] == [3.3, -0.1] and list(KZ["markers"]) == [2.4, -0.4]
      and [round(x, 1) for x in KZ["mu15"]] == [1.2, -2.1] and [round(x, 1) for x in KZ["alpha06"]] == [1.3, -2.0] and round((1 - KVS) * 100, 1) == 4.5
      and round(min(KLR), 1) == 0.5 and round(max(KLR), 1) == 1.7, kind="identity")
check("S7d AGAINST INTEREST, and its limits: at the pre-declared KURVS cell the constant law is >3 sigma high and H(z) fits, but the lean (constant above +2 sigma, H(z) within 2 sigma) ends at 1.5 M* of gas, at 0.6 of the pressure calibration and for a <5 per cent lower velocity scale, and the nuisance-marginalised likelihood ratio is below 2",
      KZ["cell"][0] > 3 and abs(KZ["cell"][1]) < 2 and KZ["mu15"][0] < 2 and KZ["alpha06"][0] < 2 and 0.95 < KVS < 1 and max(KLR) < 2,
      f"cell {KZ['cell'][0]:+.2f}/{KZ['cell'][1]:+.2f}; mu1.5 {KZ['mu15'][0]:+.2f}; alpha0.6 {KZ['alpha06'][0]:+.2f}; v {KVS:.3f}; LR max {max(KLR):.2f}", kind="identity")
check("S7e MIGHTEE-HI/LADUMA as quoted (CFG279, CFG258): b = -1.04 +/- 1.51; anchored a1 +5.23 +/- 1.05 vs -4.80 +/- 0.76; empirical/formal 5.2; formal z > 3 under constancy in 11-32 per cent of mocks; H(z) x1.045 at z = 0.09",
      [round(MB[0], 2), round(MB[1], 2)] == [-1.04, 1.51] and (MA["varying"]["a1"], MA["varying"]["err"], MA["constant 0.6"]["a1"], MA["constant 0.6"]["err"]) == (5.23, 1.05, -4.8, 0.76)
      and round(M258["ratio"], 1) == 5.2 and (round(M258["z3_none"] * 100), round(M258["z3_B"] * 100)) == (11, 32) and round(M_rival, 3) == 1.045
      and (round(MPF, 1), round(MPR, 1)) == (-0.7, -1.0) and round(MA["varying"]["a1"] / MA["varying"]["err"]) == 5, kind="identity")
check("S7f the MIGHTEE-HI/LADUMA within-sample slope is consistent with both laws (|pull| < 2), and the SPARC-anchored slope changes sign with the mass-to-light convention",
      abs(MPF) < 2 and abs(MPR) < 2 and MA["varying"]["a1"] > 0 > MA["constant 0.6"]["a1"], f"pulls {MPF:+.2f} / {MPR:+.2f}", kind="identity")
_B1, _B2, _B3 = _b269["B1 4<=z<6|COMPLETE"], _b269["B2 6<=z<8|COMPLETE"], _b269["B3 8<=z<=15|COMPLETE"]
check("S7g z >= 4 as described (CFG269, read): every complete (stars + gas) pool is NOT POSSIBLE at a 0.30 dex common calibration, and the committed run FAILS its own frozen control C1 (disclosed in the text)",
      all(set(v["G1_verdicts"]) == {"NOT POSSIBLE"} for k_, v in _b269.items() if k_.endswith("COMPLETE")) and C269_C1_FAIL, _c269.strip()[:90], kind="identity")
check("S7h no complete (stars + gas) pool at z >= 4 separates the two laws (P < 2), and every stars-only pool that does carries the gas-limited flag",
      all(v["P_range"][1] < 2 for k_, v in _b269.items() if k_.endswith("COMPLETE"))
      and all(v["G4"] for k_, v in _b269.items() if k_.endswith("LOWER-LIMIT") and v["verdict"] == "SEPARATES"), kind="identity")
check("S7i the gas-prescription bracket at z ~ 2.2 (CFG224b, quoted in PAPER38 as 0.2-0.7 dex) is 0.21-0.67 dex", (round(GAS[0], 2), round(GAS[1], 2)) == (0.21, 0.67), kind="identity")
# v3.3 (CFG310 #10): the method of the bracket, as described in Appendix B (read from CFG224b's committed output)
_txb = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
GASM = dict(n=_ace["N"], mean=float(np.mean(_ace["Race"])), zlo=min(_ace["Zace"]), zhi=max(_ace["Zace"]), s82lo=_ace["s82"]["zmin"], s82hi=_ace["s82"]["zmax"],
            slope=_ace["s82"]["b"], slope_se=_ace["posthoc"]["slope_se"], noslope=abs(_ace["posthoc"]["delta_noslope"]))
_qb = [f"the {GASM['n']} ACE galaxies", f"mean ${GASM['mean']:.2f}$ dex", f"$12+\\log({{\\rm O/H}})={GASM['zlo']:.2f}$--{GASM['zhi']:.2f}", f"span only {GASM['s82lo']:.2f}--{GASM['s82hi']:.2f}",
       f"(${GASM['slope']:.2f}\\pm{GASM['slope_se']:.2f}$ per dex of metallicity", f"lies {GAS[1]:.2f} dex below it; with no slope, {GASM['noslope']:.2f} dex", f"(post hoc), {GAS[0]:.2f} dex"]
check("S7i2 Appendix B describes the bracket's method with CFG224b's committed numbers (ACE N, mean ratio, metallicity ranges, local slope, the three extrapolations)",
      all(q_ in _txb for q_ in _qb), "; ".join(q_ for q_ in _qb if q_ not in _txb) or "all present", kind="identity")
S7["gas_method"] = GASM
check("S7j the source-table audit (CFG287) as quoted: 22 sources (KURVS not among them), 3703 sampled cells in 29 tables with no transcription mismatch; no erratum registered for any published source paper",
      AUD["cells"] == 3703 and AUD["tables"] == 29 and AUD["fails"] == 0 and AUD["passed"] and AUD["errata"] == 0 and AUD["registered"] == 0
      and AUD["sources"] == 22 and not AUD["kurvs_in"], kind="identity")

# ---- v3.2: the high-redshift record on FRAMEWORK-NATIVE inputs (no halo-fit quantity on the baryon side), read from committed lanes:
#      CFG303 (MUSE-DARK, KURVS, CRISTAL), CFG308 (CRISTAL stress test), CFG307 (ALESS 122.1 stress test), CFG305 (Umehata+25 journal fit)
_n303m = _J("CFG303_lcdm_free_inputs", "cfg303_musedark_LCDMFREE_results.json")
MDN = dict(iii=_n303m["diff"]["noHI (primary)|bD|iii"], ii_rows=[_n303m["rows"][f"noHI (primary)|z{k}-routeii-bD"] for k in (1, 2, 3)],
           iii_rows=[_n303m["rows"][f"noHI (primary)|z{k}-routeiii-bD"] for k in (1, 2, 3)], flags=_n303m["flags_primary"], checks=_n303m["checks"])
P(f"  MUSE-DARK native (CFG303; thin disc of the SED stellar mass, no H I, no f_DM or fitted mass): route (iii) z3 - z1 = {MDN['iii']['d']:+.3f} +/- {MDN['iii']['sd']:.3f} (H(z) {MDN['iii']['rival']:+.3f});"
  f" route (ii) s* " + " / ".join("NO ROOT" if r_["no_root"] else f"{r_['s']:.2f}" for r_ in MDN["ii_rows"]) + f" (third 3: D < 1 in {MDN['ii_rows'][2]['n_D_lt1']} of {MDN['ii_rows'][2]['n']});"
  f" flat inside 95% in {MDN['flags']['FLAT']}/6 rows, H(z) in {MDN['flags']['H(z)']}/6")
_n303k = _J("CFG303_lcdm_free_inputs", "cfg303_kurvs_LCDMFREE_results.json")
_kc = [c_ for m_ in _n303k["classes_free"].values() for c_ in m_.values()]
KN = dict(primary=_n303k["classes_free"]["primary"], n=len(_kc), lean_flat=_kc.count("lean flat"), lean_rival=_kc.count("lean rival"), neither=_kc.count("neither"),
          P2=_n303k["cells"]["primary"]["P2"], checks=_n303k["checks"])
P(f"  KURVS native (CFG303; measured markers, the record's analytic pressure models P0-P3 instead of the simulation-calibrated correction): primary classes {KN['primary']};"
  f" over {KN['n']} (marker set x prescription) cells: lean flat {KN['lean_flat']}, lean rival {KN['lean_rival']}, neither {KN['neither']}; P2 flat {KN['P2']['cell']['flat'][0]:+.3f}, rival {KN['P2']['cell']['rival'][0]:+.3f} dex")
_n303c = _J("CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json")["points"]["CRISTAL"]
CRN = {k_: dict(s=v["s"], flat_in=v["flags"]["FLAT"]["in95"], Hz_in=v["flags"]["H(z)"]["in95"]) for k_, v in _n303c.items()}
_c308 = _J("CFG308_cristal_stress_test", "cfg308_cristal_stress_results.json")
C308 = dict(decision=_c308["decision"], n=_c308["fractions"]["n"], H_excl=_c308["fractions"]["frac_H_excl"], F_excl=_c308["fractions"]["frac_F_excl"],
            noroot=_c308["fractions"]["n_point_no_root"], loo_stable=_c308["loo_stable"], checks=_c308["checks"])
P(f"  CRISTAL native (CFG303): " + "; ".join(f"{k_[:40]} s* {v['s']:.2f} flat {'in' if v['flat_in'] else 'OUT'} H(z) {'in' if v['Hz_in'] else 'OUT'}" for k_, v in CRN.items()))
P(f"  CRISTAL stress test (CFG308): {C308['decision']} over {C308['n']} cells: H(z) excluded at 95% in {C308['H_excl']*100:.1f}%, flat in {C308['F_excl']*100:.1f}%; no root in {C308['noroot']}; leave-one-out stable {C308['loo_stable']}; checks {C308['checks']}")
_c307 = _J("CFG307_aless122_stress_test", "cfg307_stress_results.json")
A307 = dict(z=_c307["z"], s=_c307["committed"]["cell"]["s"], decision=_c307["decision"]["primary"], checks=_c307["checks"],
            oat=sorted(v["ls"] for ax in _c307["oat"].values() for v in ax.values() if v.get("state") == "root"),
            oat_noroot=sum(1 for ax in _c307["oat"].values() for v in ax.values() if v.get("state") != "root"))
P(f"  ALESS 122.1 stress test (CFG307): z {A307['z']:.2f}; committed s* {A307['s']:.2f}; {A307['decision']['decision']} over {A307['decision']['N']} cells: no root {A307['decision']['f_noroot']*100:.1f}%,"
  f" flat inside 95% {A307['decision']['f_FLAT_inside']*100:.1f}%, flat excluded {A307['decision']['f_FLAT_excl']*100:.1f}%, H(z) excluded {A307['decision']['f_Hz_excl']*100:.1f}%;"
  f" one-axis s* range {10**A307['oat'][0]:.2f}-{10**A307['oat'][-1]:.1f} with {A307['oat_noroot']} no-root level(s)")
_u305 = _J("CFG305_published_tables", "cfg305_adf22_geometry_results.json")
U305 = dict(same_resolution=all(v["resolution"][0] == v["resolution"][1] and v["status"][0] == v["status"][1] for v in _u305["posthoc_rows"].values()),
            n=len(_u305["posthoc_rows"]), checks=_u305["checks"])
P(f"  Umehata+25 journal 870 um fit (CFG305): statuses and resolutions of the {U305['n']} ADF22.5 rows unchanged: {U305['same_resolution']}")
S7["native"] = dict(musedark=MDN, kurvs=KN, cristal=CRN, cristal_stress=C308, aless122=A307, umehata_journal=U305)
check("S7o MUSE-DARK on native baryons as quoted (CFG303, read): with SED stellar masses alone the implied a0 changes by -0.26 +/- 0.28 dex between the outer thirds (H(z) +0.18); with molecular gas added the highest third has no root (baryons exceed the model dynamics in 21 of its 36 galaxies); the lane's controls pass",
      (round(MDN["iii"]["d"], 2), round(MDN["iii"]["sd"], 2), round(MDN["iii"]["rival"], 2)) == (-0.26, 0.28, 0.18) and MDN["ii_rows"][2]["no_root"]
      and (MDN["ii_rows"][2]["n_D_lt1"], MDN["ii_rows"][2]["n"]) == (21, 36) and MDN["checks"]["passed"] == MDN["checks"]["n"], kind="identity")
check("S7p no MUSE-DARK native route shows a rise: route (iii) falls (z3 - z1 < 0) and route (ii) has no root in the highest third (read from CFG303)",
      MDN["iii"]["d"] < 0 and MDN["ii_rows"][2]["no_root"], f"{MDN['iii']['d']:+.3f}", kind="identity")
check("S7q KURVS without the simulation-calibrated pressure correction as quoted (CFG303, read): the primary analytic model (P2) reads 'neither' (both laws under-predict), and over the 24 marker-set x prescription cells 4 lean to constancy, 7 to the rival and 13 to neither; the lane's controls pass",
      KN["primary"]["P2"] == "neither" and (KN["n"], KN["lean_flat"], KN["lean_rival"], KN["neither"]) == (24, 4, 7, 13) and KN["P2"]["cell"]["flat"][0] > 0 and KN["P2"]["cell"]["rival"][0] > 0
      and KN["checks"]["passed"] == KN["checks"]["n"], kind="identity")
check("S7r CRISTAL on native inputs as quoted (CFG303, CFG308, read): no native CRISTAL point excludes a constant a0 at 95%, and the 1008-cell stress test is NOT DISCRIMINATING (H(z) excluded in 59%, constancy in 24% of cells), stable under leave-one-out; its controls pass",
      all(v["flat_in"] for v in CRN.values()) and C308["decision"] == "NOT DISCRIMINATING" and C308["n"] == 1008 and round(C308["H_excl"] * 100) == 59 and round(C308["F_excl"] * 100) == 24
      and C308["loo_stable"] and C308["checks"]["passed"] == C308["checks"]["n"], kind="identity")
check("S7s ALESS 122.1 as quoted (CFG307, read): the 540-cell stress test is NOT ROBUST (no root in 44%, constancy inside the 95% interval in 29%), and over one axis at a time the implied a0 runs from no root to about 20 times the local value; its controls pass",
      A307["decision"]["decision"] == "NOT ROBUST" and A307["decision"]["N"] == 540 and round(A307["decision"]["f_noroot"] * 100) == 44 and round(A307["decision"]["f_FLAT_inside"] * 100) == 29
      and A307["oat_noroot"] >= 1 and 15 < 10**A307["oat"][-1] < 25 and all(A307["checks"]), kind="identity")
# ---- v3.3 (CFG310 #1, #8, #9): the native rows reported against interest, symmetrically
_ii = MDN["ii_rows"]
P(f"  v3.3 MUSE-DARK route (ii) (SED M* + H2, native): s* " + " / ".join("no root" if r_["no_root"] else f"{r_['s']:.2f}" for r_ in _ii)
  + "; FLAT inside the 95% interval: " + " / ".join(str(r_["flags95"]["FLAT"]) for r_ in _ii) + "; D < 1 in " + " / ".join(f"{r_['n_D_lt1']}/{r_['n']}" for r_ in _ii))
check("S7u AGAINST INTEREST (CFG310 #1): with molecular gas (route ii) the native MUSE-DARK scale is about a quarter of the local value in the first two thirds (s* 0.22, 0.27) and has no root in the third, so constancy lies outside the 95% interval in 2 of 3 thirds; D < 1 in 13/37, 14/36 and 21/36 galaxies",
      [round(r_["s"], 2) for r_ in _ii[:2]] == [0.22, 0.27] and _ii[2]["no_root"] and [r_["flags95"]["FLAT"] for r_ in _ii] == [True, False, False]
      and [(r_["n_D_lt1"], r_["n"]) for r_ in _ii] == [(13, 37), (14, 36), (21, 36)], kind="identity")
_kp = KN["P2"]["cell"]; _app0 = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
P(f"  v3.3 KURVS native P2 cell: constancy under-predicts by {_kp['flat'][0]:+.3f} +/- {_kp['flat'][1]:.3f} dex ({_kp['flat'][0]/_kp['flat'][1]:.1f} sigma), the rival by {_kp['rival'][0]:+.3f} +/- {_kp['rival'][1]:.3f} ({_kp['rival'][0]/_kp['rival'][1]:.1f} sigma)")
check("S7v AGAINST INTEREST (CFG310 #8): at the native P2 cell both laws under-predict the outer accelerations, constancy by +0.38 dex (6.8 sigma) and the rival by +0.23 dex (4.3 sigma), so the rival is closer; more analytic cells lean to the rival (7) than to constancy (4)",
      (round(_kp["flat"][0], 2), round(_kp["rival"][0], 2)) == (0.38, 0.23) and round(_kp["flat"][0] / _kp["flat"][1], 1) == 6.8 and round(_kp["rival"][0] / _kp["rival"][1], 1) == 4.3
      and KN["lean_rival"] > KN["lean_flat"] and all(f"$+{_kp[k_][0]:.2f}\\pm{_kp[k_][1]:.2f}$ dex (${_kp[k_][0]/_kp[k_][1]:.1f}\\sigma$)" in _app0 for k_ in ("flat", "rival")), kind="identity")
_ad = A307["decision"]
check("S7w ALESS 122.1 reported like CRISTAL (CFG310 #9): constancy excluded in 27% of the 540 cells, always from above, H(z) in 15%; the committed native s* is 8.8",
      round(_ad["f_FLAT_excl"] * 100) == 27 and _ad["f_FLAT_below"] == 0.0 and round(_ad["f_Hz_excl"] * 100) == 15 and round(A307["s"], 1) == 8.8, kind="identity")
check("S7t the Umehata+25 journal 870 um fit (CFG305, read) changes no status or resolution of the ADF22.5 rows (the text says so)", U305["same_resolution"] and U305["n"] >= 6, kind="identity")

# ---- v3.4 (2026-10-05): the MIGHTEE-HI width-chain note (PAPER40, Zenodo 10.5281/zenodo.23142559) quoted in Section 3.8, read from
#      its committed outputs: the pooled a0 of the primary (rest-frame) chain (CFG309, 47 discs) and the low end of the single-dish
#      flux range (PAPER40_figures_numbers.json).  Such a check carries no evidence; it certifies the quotation.
_f309 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG309_mightee_width_frame/cfg309_cfg301chain_stageB_FRAME_results.json")))["numbers"]["pooled"]
_p40 = json.load(open(os.path.join(ROOT, "qwen_claude_field_theory/papers_2026/PAPER40_figures_numbers.json")))["post_hoc_rows"]["single_dish_range"]
_mtxt = f"$a_0={_p40['lo']/1e-10:.2f}$--${_f309['a0']/1e-10:.2f}\\times10^{{-10}}$ m s$^{{-2}}$ for {_f309['n']} mostly gas-dominated discs"
P(f"  v3.4 PAPER40 (MIGHTEE-HI width chain) as quoted: a0 {_p40['lo']/1e-10:.3f}--{_f309['a0']/1e-10:.3f} e-10, n = {_f309['n']}, deep-regime y quantiles {_f309['y_q']}")
check("S7x the MIGHTEE-HI width-chain note as quoted (PAPER40, read): a0 = 0.90--1.31e-10 m s^-2 (single-dish low end to the catalogue-flux pooled value) for 47 discs, all in the deep regime (upper y quartile < 0.2), and the text prints exactly these values",
      _f309["n"] == 47 and round(_f309["a0"] / 1e-10, 2) == 1.31 and round(_p40["lo"] / 1e-10, 2) == 0.90 and _f309["y_q"][-1] < 0.2
      and _mtxt in open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read(), _mtxt, kind="identity")

# ---- Appendix C quotes the number of checks of each kind; this last check (an identity) compares the text with the tally,
#      counting itself
_app = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
_words = {"Five": 5, "Six": 6, "Seven": 7, "Eleven": 11, "Twelve": 12, "Thirteen": 13, "Fourteen": 14, "Fifteen": 15}
_mm = re.search(r"Of its (\d+) checks, (\d+) are identities.*?([\w-]+) evaluate published models.*?([\w-]+) can fail on the data\. ([\w-]+) are injection tests", _app, re.S)
_txt = None
if _mm:
    def _num(w): return int(w) if w.isdigit() else _words.get(w, {"Thirty": 30, "Twenty-eight": 28, "Twenty-nine": 29, "Thirty-one": 31, "Thirty-two": 32, "Twenty-seven": 27, "Thirty-three": 33, "Thirty-four": 34, "Thirty-five": 35}.get(w, -1))
    _txt = (int(_mm.group(1)), int(_mm.group(2)), _num(_mm.group(3)), _num(_mm.group(4)), _num(_mm.group(5)))
_tally = (NCHK[0] + 1, len(KINDS.get("identity", [])) + 1, len(KINDS.get("model", [])), len(KINDS.get("data", [])), len(KINDS.get("injection", [])))
check("S7n Appendix C quotes the tally of checks by kind exactly (total, identity, model, data, injection; this check included)", _txt == _tally, f"text {_txt}, tally {_tally}", kind="identity")
# ----------------------------------------------------------------------------------------------------------------
json.dump(OUT, open(os.path.join(HERE, "paper_numbers.json"), "w"), indent=1, default=float)
P(""); P(f"RESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
for k_ in ("identity", "model", "data", "injection"):
    P(f"   {len(KINDS.get(k_, [])):2d} {k_:9s} -- {KIND_TEXT[k_]}")
OUT["check_kinds"] = {k_: len(v) for k_, v in KINDS.items()}
json.dump(OUT, open(os.path.join(HERE, "paper_numbers.json"), "w"), indent=1, default=float)
if __name__ == "__main__":
    sys.exit(1 if FAILS else 0)
