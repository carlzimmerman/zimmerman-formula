#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
paper_numbers.py -- every number quoted in the MNRAS manuscript `mnras_a0_lambda_v3.tex` that is not printed by one
of the repository estimators (those are re-run by reproduce_all.sh):

    real_research/reviews/mi_btfr_intercept_kappa_door_2026.py          -> kappa = 0.465 +/- 0.076, the 9.47% floor
    real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py -> kappa = 0.551 +/- 0.043 (shape-only)
    real_research/reviews/kappa_h0_convention_audit_2026.py             -> the H0-convention shifts
    real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.py -> the like-for-like footing comparison (S7h)

Sections (each ends in checks that CAN fail; exit code 1 if any does):
    S1  the relation, step by step: rho_crit, rho_Lambda, c sqrt(G rho_Lambda), a0, the four equivalent forms, Z
    S2  the standard radial-acceleration fit on SPARC and its mass-to-light degeneracy  (kappa against Upsilon_disc)
    S3  the candidate coefficients, the mass-budget floor, and the H0 lock
    S4  the redshift laws: constant, H(z), the LambdaCDM emergent scale (NFW + concentration-mass relation),
        the density mapping under DESI DR2 w0-wa; the error amplification of the kernel inversion; the 20:1 rule;
        (v3) the same rule with a COMMON-MODE baryonic-mass calibration error, which does not average down, and the
        Fisher conditioning of a0 with the mass scale free (an independent re-computation of the CFG240 table)
    S5  the closed-form inversion of the RC100 dark-matter fractions, on the CORRECTED transcription of Table 3
        (v3; real_research/data/rc100_nestorshachar2023_table3_CORRECTED.csv, CFG289), with the original
        transcription re-run beside it so that every number the correction moves is printed old -> new
    S6  the deep regime (g_bar < 0.2 a0) in SPARC and MIGHTEE-HI: the per-galaxy slope against the kernel's own slope at the
        same points, the amplitude and its dependence on the stellar mass-to-light convention, and the pitfall of ratios
        fitted to the rotation curves themselves
    S7  (v3) the high-redshift record after 2026-09-25, read from the committed outputs of the repository lanes that
        produced it (MUSE-DARK by baryon route, KURVS, MIGHTEE-HI/LADUMA, z = 4-14, the gas-calibration bracket, the
        source-table audit, and the like-for-like footing comparison of the coefficient).  A check that only confirms
        that the text quotes a committed number is labelled 'identity': the evidence lies in the lane, which carries
        its own frozen criteria and controls.  A check that re-derives a comparison from those numbers is 'data'.
Both densities are carried throughout: rho_Lambda (a0 = 9.36e-11) and rho_crit (a0 = 1.13e-10).
Run from anywhere:  python3 paper_numbers.py        Output: paper_numbers.json next to this file.
"""
import os, sys, glob, json, math, re
import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SPARC = os.path.join(ROOT, "real_research", "data", "sparc_data")
RC100 = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3_CORRECTED.csv")   # CFG289 (51c70923f)
RC100_ORIG = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3.csv")      # the earlier transcription (17 wrong cells)
RC100_SHA256 = "a1778d75476ede17da690e09fc1176b68455f22778e5de8ef39b66a0cb19398f"
CFG = os.path.join(ROOT, "campaign_fresh_gravity")

OUT, FAILS, NCHK = {}, [], [0]
KINDS = {}
KIND_TEXT = {"identity": "algebra or arithmetic on stated inputs: certifies the arithmetic, can fail only by a coding error, carries NO evidence",
             "model": "evaluates a published model or relation at stated inputs: can fail if the model is mis-implemented, carries no evidence",
             "data": "can fail on the data",
             "injection": "feeds an estimator synthetic data with a KNOWN a0 (or trend) built on the real baryons: proves the estimator measures, not echoes"}
def P(*a): print(*a, flush=True)
KIND_BY_ID = {"S1a": "identity", "S1b": "identity", "S1c": "identity", "S2d": "identity", "S3a": "identity", "S3b": "identity",
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
check("S1a the four forms of the kappa = 1/2 relation are one number", max(abs(x/a0_L - 1) for x in (f2, f3, f4, a_nat)) < 1e-9,
      f"max relative difference {max(abs(x/a0_L - 1) for x in (f2, f3, f4, a_nat)):.1e}")
check("S1b Z = sqrt(32 pi/3) identically (no data content: H cancels)", abs(Z - math.sqrt(32*math.pi/3)) < 1e-12, f"Z = {Z:.6f}")
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
def load_sparc(UD=0.5, UB=0.7, qcut=0.10, GS=1.0, bulgeless=False):
    """g_bar, g_obs, error in log10 g_obs, number of galaxies.  GS rescales the gas mass; bulgeless keeps V_bul = 0 galaxies only.
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
        gb.append(v2[ok] / R[ok] * K); go.append(V[ok]**2 / R[ok] * K); ew.append(2 * eV[ok] / V[ok] / math.log(10)); gi.append(np.full(ok.sum(), ng))
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
rows = []
P(f"  {'Upsilon_disc':>12} {'a0 [1e-10]':>11} {'kappa(rho_L)':>13} {'kappa(rho_crit)':>16} {'rms [dex]':>10}")
for UD in (0.40, 0.50, 0.60, 0.70, 0.80):
    g1, g2, e1, _ = load_sparc(UD=UD)
    a0, rms = fit_a0(g1, g2, e1)
    rows.append(dict(UD=UD, a0=a0, kappa_L=a0 / A_L, kappa_C=a0 / A_C, rms=rms))
    P(f"  {UD:12.2f} {a0/1e-10:11.3f} {a0/A_L:13.3f} {a0/A_C:16.3f} {rms:10.3f}")
ud_half = brentq(lambda u: fit_a0(*load_sparc(UD=u)[:3])[0] / A_L - 0.5, 0.45, 0.80, xtol=1e-4)
ud_half_C = brentq(lambda u: fit_a0(*load_sparc(UD=u)[:3])[0] / A_C - 0.5, 0.40, 0.80, xtol=1e-4)
P(f"  kappa = 1/2 exactly needs Upsilon_disc = {ud_half:.3f} (rho_Lambda) or {ud_half_C:.3f} (rho_crit), bulge fixed at 0.7")
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
P(f"  ==> kappa_B = {kB:.2f} +/- {sB:.2f}   (dominated by the BULGE mass-to-light ratio; the repository's 0.551 +/- 0.043 held Ups_bul fixed at 0.7)")
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
OUT["S2"] = dict(deep_band=deep, injection=inj, shape_only=shape, kappa_B=kB, sigma_B=sB, B_budget=dict(ml_disc=ml_disc, ml_bul=ml_bul, ml_grid=ml_all, gas=gas, stat=statB), bulgeless=bl,
                 shape_immunity=imm, standard_move_10pc=std_move, n_gal=ngal, n_pts=int(len(gb)), table=rows, ud_for_half_L=ud_half, ud_for_half_C=ud_half_C,
                 fixed_L=dict(UD=uL, rms=rL), fixed_C=dict(UD=uC, rms=rC))
r05 = [r for r in rows if abs(r["UD"] - 0.5) < 1e-9][0]
check("S2a at Upsilon_disc = 0.5 the fit returns the literature a0 = 1.2e-10 within 5%", abs(r05["a0"] / 1.2e-10 - 1) < 0.05, f"a0 = {r05['a0']:.3e}")
check("S2b the degeneracy is steep: kappa moves by more than 0.15 between Upsilon_disc = 0.5 and 0.7", rows[1]["kappa_L"] - rows[3]["kappa_L"] > 0.15,
      f"{rows[1]['kappa_L']:.3f} -> {rows[3]['kappa_L']:.3f}")
check("S2d the shape-only estimator is immune to a common distance rescaling (< 1e-5): the free offset absorbs it by construction", imm < 1e-5,
      f"{imm:.1e}")
check("S2d2 while the standard fit is not: a 10 per cent common rescaling moves it by more than 15 per cent", std_move > 0.15, f"{std_move*100:.1f}%")
check("S2e the replication agrees with the repository's estimator B at Upsilon_bul = 0.7, Upsilon_disc = 0.5 and 0.7 (0.529, 0.574) within 0.01",
      abs(grid[(0.5, 0.7)] - 0.529) < 0.01 and abs(grid[(0.7, 0.7)] - 0.574) < 0.01, f"{grid[(0.5, 0.7)]:.3f}, {grid[(0.7, 0.7)]:.3f}")
check("S2f AGAINST THE EARLIER ERROR BAR: the bulge mass-to-light ratio moves estimator B by more than twice the 0.043 previously quoted",
      ml_bul > 2 * 0.043, f"bulge term {ml_bul:.3f}; total {sB:.3f}")
check("S2g the deep band (g_bar < 0.1 a0, quality-cut, error-weighted) gives kappa between 0.40 and 0.60 for Upsilon_disc 0.5-0.7",
      all(0.40 < deep[u]["kappa"] < 0.60 for u in deep), ", ".join(f"{deep[u]['kappa']:.3f}" for u in deep))
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
# ---- estimator A (repository script): its correction Q(y) is evaluated at an assumed a0.  Does that assumption do the work?
import subprocess
_rA = subprocess.run([sys.executable, "mi_btfr_intercept_kappa_door_2026.py"], cwd=os.path.join(ROOT, "real_research", "reviews"), capture_output=True, text=True)
_m = re.search(r"frozen-y estimate ([0-9.e+-]+) .*?self-consistent fixed point ([0-9.e+-]+) .*?ALT-footing selection\+argument ([0-9.e+-]+)", _rA.stdout)
A_frozen, A_selfc, A_alt = (float(x) for x in _m.groups())
P(f"  estimator A: correction evaluated at the canonical a0 {A_frozen:.4e}; at its own output (fixed point) {A_selfc:.4e} ({(A_selfc/A_frozen-1)*100:+.2f}%);"
  f" selection and correction at the 21% higher alternative a0 {A_alt:.4e} ({(A_alt/A_frozen-1)*100:+.1f}%)")
OUT["A_selfconsistency"] = dict(frozen=A_frozen, fixed_point=A_selfc, alt=A_alt)
check("I4 estimator A is not an echo of the a0 at which its correction is evaluated: iterating to its own output moves it by < 1 per cent, and a 21 per cent change of that a0 moves it by < 10 per cent",
      _rA.returncode == 0 and abs(A_selfc / A_frozen - 1) < 0.01 and abs(A_alt / A_frozen - 1) < 0.10,
      f"{(A_selfc/A_frozen-1)*100:+.2f}%, {(A_alt/A_frozen-1)*100:+.1f}%", kind="injection")

head("S3  CANDIDATE COEFFICIENTS, THE MASS-BUDGET FLOOR, THE H0 LOCK")
k_hor = math.sqrt(8 * math.pi / 3) / (2 * math.pi)             # a0 = c H_Lambda / 2 pi  (the Lambda form of the classical coincidence)
cands = [("c H_Lambda/2pi (Milgrom 2020, eq. 3)", k_hor), ("1/2 (this paper)", 0.5),
         ("c H0/2pi (Milgrom 2020, eq. 3)", k_hor / math.sqrt(OL)), ("c H0/6 (Verlinde 2017)", math.sqrt(8*math.pi/3) / 6 / math.sqrt(OL)),
         ("c H_Lambda (Unruh T = de Sitter T)", math.sqrt(8*math.pi/3)), ("2 c H_Lambda (Milgrom 1999)", 2 * math.sqrt(8*math.pi/3))]
MEAS = [("BTFR intercept", 0.465, 0.076), ("shape-only", round(kB, 3), round(sB, 3))]      # A: repository script; B: computed above
P(f"  {'candidate':42} {'kappa':>7}   pulls: " + "   ".join(m[0] for m in MEAS))
ctab = []
for name, k in cands:
    pulls = [(k - m[1]) / m[2] for m in MEAS]
    ctab.append(dict(name=name, kappa=k, pulls=pulls))
    P(f"  {name:42} {k:7.4f}   " + "   ".join(f"{p:+6.2f} sigma" for p in pulls))
sU, sG = 0.168, 0.115
floor = sU * sG / math.hypot(sU, sG); fstar = sG**2 / (sU**2 + sG**2)
grid = np.linspace(0, 1, 200001); floor_num = np.min(np.hypot(grid * sU, (1 - grid) * sG))
P(f"  mass-budget floor: s_U = {sU}, s_G = {sG}:  s_U s_G/sqrt(s_U^2+s_G^2) = {floor*100:.2f}% at f_* = {fstar:.3f}  (numerical minimum {floor_num*100:.2f}%)")
a_half_planck = 0.5 * A_L
A_shoes = c * math.sqrt(G * OL * 3 * (H0_SHOES * 1e3 / MPC)**2 / (8 * math.pi * G))
a_hor_shoes = k_hor * A_shoes
P(f"  H0 lock (fixed Omega_Lambda): a0(kappa=1/2, H0={H0_KMS}) = {a_half_planck:.4e};  a0(kappa={k_hor:.4f}, H0={H0_SHOES}) = {a_hor_shoes:.4e};  ratio {a_hor_shoes/a_half_planck:.4f}")
P(f"     because kappa ratio {k_hor/0.5:.4f} against H0 ratio {H0_KMS/H0_SHOES:.4f}")
om_h2 = OM * (H0_KMS / 100)**2                                  # the CMB holds Omega_m h^2, not Omega_Lambda
OL_shoes = 1 - om_h2 / (H0_SHOES / 100)**2
A_shoes_fixom = c * math.sqrt(G * OL_shoes * 3 * (H0_SHOES * 1e3 / MPC)**2 / (8 * math.pi * G))
k_fixom = a_half_planck / A_shoes_fixom
P(f"  variant, Omega_m h^2 held instead: Omega_Lambda(SH0ES) = {OL_shoes:.3f}; the coefficient that reproduces a0(1/2, Planck) is {k_fixom:.4f} ({(k_fixom/k_hor-1)*100:+.1f}% from {k_hor:.4f})")
for nm, kk, ss in MEAS:
    P(f"  a0 as an H0 meter at frozen kappa = 1/2 (fixed Omega_Lambda): {nm}: H0 = {H0_KMS*kk/0.5:.1f} +/- {H0_KMS*ss/0.5:.1f} km/s/Mpc")
sep = 1 - k_hor / 0.5
P(f"  separation of 1/2 from {k_hor:.4f}: {sep*100:.1f}% in a0 = {abs(math.log10(k_hor/0.5)):.3f} dex;  3 sigma needs {sep/3*100:.1f}% on a0")
lnLR = sum(-0.5 * ((0.5 - m[1]) / m[2])**2 + 0.5 * ((k_hor - m[1]) / m[2])**2 for m in MEAS)
P(f"  ln[L(1/2)/L({k_hor:.3f})] from the two measurements = {lnLR:+.2f}")
w = [1 / m[2]**2 for m in MEAS]; kbar = sum(wi * m[1] for wi, m in zip(w, MEAS)) / sum(w); chi2 = sum(((m[1] - kbar) / m[2])**2 for m in MEAS)
P(f"  the two estimators differ by {(MEAS[1][1]-MEAS[0][1])/math.hypot(MEAS[0][2], MEAS[1][2]):.2f} sigma (not independent: same galaxies); inverse-variance mean {kbar:.3f} is NOT quoted")
OUT["S3"] = dict(candidates=ctab, floor=floor, f_star=fstar, kappa_horizon=k_hor, lock_ratio=a_hor_shoes / a_half_planck, lnLR=lnLR, sep_percent=sep * 100,
                 kappa_fixed_omh2=k_fixom, OL_shoes=OL_shoes, H0_meter=[(m[0], H0_KMS*m[1]/0.5, H0_KMS*m[2]/0.5) for m in MEAS])
check("S3a the closed-form floor equals the numerical minimum", abs(floor - floor_num) < 1e-6, f"{floor*100:.2f}%")
check("S3b the H0 lock: the two (kappa, H0) pairs predict the same a0 to better than 0.5%", abs(a_hor_shoes / a_half_planck - 1) < 5e-3,
      f"{(a_hor_shoes/a_half_planck - 1)*100:+.2f}%")
check("S3c 1/2 is inside 1.5 sigma of both measurements; Milgrom-1999's 2cH_Lambda is outside 5 sigma of both",
      all(abs(p) < 1.5 for p in ctab[1]["pulls"]) and all(abs(p) > 5 for p in ctab[5]["pulls"]))
check("S3d the data do not single out 1/2: at least three candidates lie within 2.2 sigma of both measurements",
      sum(all(abs(p) < 2.2 for p in r["pulls"]) for r in ctab) >= 3, f"{sum(all(abs(p) < 2.2 for p in r['pulls']) for r in ctab)} candidates inside 2.2 sigma of both")

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
P(f"  z = 2.5 density mapping under DESI DR2 w0-wa: " + ", ".join(f"{k} {v:+.3f}" for k, v in L25["desi"].items()) + "  (NOT this paper's prediction; shown for scale)")
P(f"  check of the gmax route against the closed law: ratio {g25/g0:.4f} vs E^(4/3) c^2/f(c) ratio {ratio_halo(2.5):.4f}")
ln20 = math.log(20.0)
sig_halo = L25["dm14"] / math.sqrt(2 * ln20); sig_Hz = L25["Hz"] / math.sqrt(2 * ln20)
P(f"  20:1 rule: two point hypotheses Delta apart, Gaussian error sigma: expected ln B = Delta^2/(2 sigma^2) >= ln 20  =>  sigma <= Delta/sqrt(2 ln 20) = Delta/{math.sqrt(2*ln20):.3f}")
P(f"     constant vs halo-emergent at z = 2.5: Delta = {L25['dm14']:.3f} -> sigma <= {sig_halo:.3f} dex;   constant vs H(z): Delta = {L25['Hz']:.3f} -> sigma <= {sig_Hz:.3f} dex")
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
s_halo_obj = 0.5 * (math.log10(ratio_halo(2.5, dlogc=+dc)) - math.log10(ratio_halo(2.5, dlogc=-dc)))
P(f"  a single object: +/-{dc} dex concentration scatter moves its halo-emergent expectation by +/-{s_halo_obj:.3f} dex")
s_int = 0.034                                       # intrinsic scatter of the relation in log g_obs (Desmond 2023)
P(f"  intrinsic scatter of the relation ({s_int} dex in g_obs) amplified through the inversion: " +
  ", ".join(f"y = {a['y']}: {s_int*a['A_obs']:.3f} dex" for a in amp[:3]))
def expected_lnB(N, s_meas, mu, s_intr, s_h):
    """expected ln Bayes factor for N objects; H0: N(0, s0^2), H1: N(mu, s1^2) with s1^2 = s0^2 + s_h^2. Returns (truth H0, truth H1)."""
    s0 = math.hypot(s_meas, s_intr); s1 = math.hypot(s0, s_h)
    e0 = N * (math.log(s1 / s0) - 0.5 + (s0**2 + mu**2) / (2 * s1**2))
    e1 = N * (math.log(s0 / s1) - 0.5 + (s1**2 + mu**2) / (2 * s0**2))
    return e0, e1
P(f"  expected odds (the smaller of the two truths), Delta = {L25['dm14']:.3f} dex, intrinsic {s_int*amp[2]['A_obs']:.3f} dex (y = 0.3), halo scatter {s_halo_obj:.3f} dex on the LambdaCDM side:")
P(f"  {'sigma_meas':>10} " + " ".join(f"{'N = '+str(N):>12}" for N in (1, 2, 3, 4)))
dec = []
for sm in (0.08, 0.10, 0.13, 0.20):
    odds = [math.exp(min(expected_lnB(N, sm, L25["dm14"], s_int * amp[2]["A_obs"], s_halo_obj))) for N in (1, 2, 3, 4)]
    dec.append(dict(sigma_meas=sm, odds=odds))
    P(f"  {sm:10.2f} " + " ".join(f"{o:11.1f}:1" for o in odds))
# ---- measurement budgets.  Lensing conserves surface density, so g_bar is magnification-free while g_obs = V^2/R ~ mu^(1/2):
#      d log a0 = A_obs [2 dV/V / ln10  (+)  0.5 dlog mu]  (+)  A_bar dlog M_b     (quadrature), evaluated at y = 0.2
nb = float(n_slope(0.2)); Aob, Aba = 1 / abs(nb), 1 / abs(nb) - 1
P(f"  measurement budgets at y = 0.2 (A_obs = {Aob:.2f}, A_bar = {Aba:.2f}; a magnification error enters as A_obs/2 = {Aob/2:.2f}):")
budgets = []
for dv, dm, dmu in ((0.025, 0.04, 0.04), (0.03, 0.06, 0.05), (0.05, 0.10, 0.06)):
    tot = math.sqrt((Aob * 2 * dv / math.log(10))**2 + (Aba * dm)**2 + (Aob * 0.5 * dmu)**2)
    budgets.append(dict(dV=dv, dlogM=dm, dlogmu=dmu, total=tot))
    P(f"     dV/V = {dv*100:.1f}%, dlog M_b = {dm:.2f}, dlog mu = {dmu:.2f}  ->  sigma_meas = {tot:.3f} dex")
ideal = math.exp(L25["dm14"]**2 / (2 * 0.134**2))
P(f"  (idealised: no intrinsic and no halo scatter, total 0.134 dex, one object: {ideal:.1f}:1)")
OUT["S4"] = dict(laws=laws, gmax_z0=g0, gmax_z25=g25, r200_z0_kpc=r0, c_z0=float(c0_), sigma_needed_halo=sig_halo, sigma_needed_Hz=sig_Hz, amplification=amp,
                 massdep=massdep, halo_range={str(k): v for k, v in hrange.items()}, budgets=budgets, vmax_scaling_z25=vm25, halo_scatter_single=s_halo_obj, intrinsic_amp=[s_int * a["A_obs"] for a in amp[:3]], decision=dec)
# ---- what a gate-passing galaxy looks like
GAM = 1.2                                            # disc-versus-point-mass factor at the last measured radius (SPARC median 1.19)
sig_gate = 0.3 * 1.0e-10 / (GAM * G) * KPC**2 / MSUN  # Msun per kpc^2:  M_b < sig_gate R^2
gate = []
for Mb, R in ((2e9, 4.0), (5e9, 6.0), (1e10, 8.0)):
    yb = GAM * G * Mb * MSUN / (R * KPC)**2 / 1.0e-10
    Vf = (float(nu(yb))**2 * yb * GAM * G * Mb * MSUN * 1.0e-10)**0.25 / 1e3
    gate.append(dict(Mb=Mb, R_kpc=R, y=yb, Vf_kms=Vf))
P(f"  the gate g_bar < 0.3 a0 (a0 = 1e-10, Gamma = {GAM}) reads M_b < {sig_gate:.2e} (R/kpc)^2 Msun; examples: " +
  "; ".join(f"M_b = {g_['Mb']:.0e}, R = {g_['R_kpc']:.0f} kpc -> y = {g_['y']:.2f}, V_f = {g_['Vf_kms']:.0f} km/s" for g_ in gate))
OUT["S4"]["gate_surface_density"] = sig_gate; OUT["S4"]["gate_examples"] = gate
check("S4j the gate selects low-mass discs: the three examples pass y < 0.3 and rotate at 80-130 km/s", all(g_["y"] < 0.3 and 80 < g_["Vf_kms"] < 130 for g_ in gate),
      ", ".join(f"{g_['Vf_kms']:.0f}" for g_ in gate) + " km/s")
check("S4k the three quoted measurement budgets give 0.10, 0.13 and 0.20 dex", all(abs(b["total"] - t) < 0.006 for b, t in zip(budgets, (0.10, 0.13, 0.20))),
      ", ".join(f"{b['total']:.3f}" for b in budgets))
check("S4l four galaxies at 0.20 dex also exceed 20:1", dec[3]["odds"][3] > 20, f"{dec[3]['odds'][3]:.0f}:1")
check("S4h the smallest structural LambdaCDM expectation in the grid is still a rise of more than 0.2 dex at z = 2.5",
      min(min(v.values()) for v in massdep.values()) > 0.2, f"min {min(min(v.values()) for v in massdep.values()):+.3f}, max {max(max(max(v.values()) for v in massdep.values()), vm25):+.3f}")
check("S4i AGAINST THE ONE-OBJECT CLAIM: with intrinsic and halo-to-halo scatter included, one object at 0.13 dex does NOT reach 20:1, three objects at 0.10 dex do",
      dec[2]["odds"][0] < 20 and dec[1]["odds"][2] > 20, f"one at 0.13: {dec[2]['odds'][0]:.1f}:1; three at 0.10: {dec[1]['odds'][2]:.1f}:1")
check("S4a the closed law E^(4/3) c^2/f(c) is the ratio of NFW central accelerations at fixed M200", abs(g25 / g0 / ratio_halo(2.5) - 1) < 1e-9)
check("S4b the central acceleration of a 1e12 Msun NFW halo today is within a factor 2 of the galactic scale 1.2e-10", 0.5 < g0 / 1.2e-10 < 2.0, f"{g0:.2e}")
check("S4c halo-emergent law at z = 2.5 is a factor 2.0-2.3 (0.30-0.36 dex) for the Dutton-Maccio relation at 1e12 Msun", 0.30 < L25["dm14"] < 0.36, f"{10**L25['dm14']:.3f} = {L25['dm14']:+.3f} dex")
check("S4d the required single-object precision is 0.13 dex", abs(sig_halo - 0.13) < 0.01, f"{sig_halo:.3f}")
check("S4e deep limit n -> -1/2 (a0 = g_obs^2/g_bar) and the amplification at y = 0.3 stays below 1.7 (baryons) and 2.7 (kinematics)",
      abs(n_deep + 0.5) < 1e-4 and amp[2]["A_bar"] < 1.7 and amp[2]["A_obs"] < 2.7, f"A_bar = {amp[2]['A_bar']:.2f}, A_obs = {amp[2]['A_obs']:.2f}")
check("S4f at the accelerations of published z > 0.5 samples (1.7-6.4 a0) the kinematic amplification is 4-9", 4 < amp[4]["A_obs"] < 5 and 8.5 < amp[6]["A_obs"] < 9.5,
      f"{amp[4]['A_obs']:.1f} - {amp[6]['A_obs']:.1f}")
check("S4g even the density mapping under DESI w0-wa stays within 0.15 dex of zero at z = 2.5, far from the halo and H(z) laws",
      all(abs(v) < 0.15 for v in L25["desi"].values()))

# ---- (v3) THE SAME RULE WITH A COMMON-MODE CALIBRATION OF THE BARYONIC MASS.  The table above treats every error as independent
#      between galaxies.  A calibration shared by the whole sample (an alpha_CO scale, a stellar-mass zero point) does not average
#      down: Delta_i = c + e_i (+ h_i + Delta under the halo law), c ~ N(0, s_C^2) common, s_C = A_bar * delta_c.  The expected log
#      Bayes factor is the Kullback-Leibler divergence of two N-variate normals with covariance s^2 I + s_C^2 J (eigenvalues s^2
#      (N-1 times) and s^2 + N s_C^2 along the unit vector), means 0 and Delta along the unit vector.
def expected_lnB_shared(N, s_meas, mu, s_intr, s_h, s_c):
    s0v = s_meas**2 + s_intr**2; s1v = s0v + s_h**2
    l0, l1 = s0v + N * s_c**2, s1v + N * s_c**2
    def kl(av, al, bv, bl):
        return 0.5 * ((N - 1) * (av / bv - 1 - math.log(av / bv)) + (al / bl - 1 - math.log(al / bl)) + N * mu**2 / bl)
    return kl(s0v, l0, s1v, l1), kl(s1v, l1, s0v, l0)
_red = max(abs(a - b) for N in (1, 2, 3, 4, 10) for sm in (0.08, 0.10, 0.13, 0.20)
           for a, b in zip(expected_lnB_shared(N, sm, L25["dm14"], s_int * amp[2]["A_obs"], s_halo_obj, 0.0),
                           expected_lnB(N, sm, L25["dm14"], s_int * amp[2]["A_obs"], s_halo_obj)))
s_intr_d = s_int * amp[2]["A_obs"]
P(f"  common-mode calibration (v3): baryonic-mass calibration error delta_c shared by every galaxy, s_C = A_bar delta_c at y = 0.2 (A_bar = {Aba:.2f});"
  f" the shared-term formula reduces to the independent one at s_C = 0 to {_red:.1e}")
P(f"  {'delta_c':>8} {'s_C':>6} {'halo, N=4 @0.20':>16} {'halo, N=4 @0.10':>16} {'halo, N=10 @0.20':>17} {'H(z), N=4 @0.20':>16} {'halo: Delta/s_C':>16} {'H(z): Delta/s_C':>16}")
SHARED = []
for dcal in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
    sc = Aba * dcal
    oh4 = math.exp(min(expected_lnB_shared(4, 0.20, L25["dm14"], s_intr_d, s_halo_obj, sc)))
    oh4b = math.exp(min(expected_lnB_shared(4, 0.10, L25["dm14"], s_intr_d, s_halo_obj, sc)))
    oh10 = math.exp(min(expected_lnB_shared(10, 0.20, L25["dm14"], s_intr_d, s_halo_obj, sc)))
    lnz = min(expected_lnB_shared(4, 0.20, L25["Hz"], s_intr_d, 0.0, sc))
    oz4 = math.exp(min(lnz, 700.0))
    zh = L25["dm14"] / sc if sc > 0 else float("inf"); zz_ = L25["Hz"] / sc if sc > 0 else float("inf")
    SHARED.append(dict(delta_c=dcal, s_C=sc, halo_N4_020=oh4, halo_N4_010=oh4b, halo_N10_020=oh10, Hz_N4_020=oz4, halo_mean_limit=zh, Hz_mean_limit=zz_))
    P(f"  {dcal:8.2f} {sc:6.3f} {oh4:15.1f}:1 {oh4b:15.1f}:1 {oh10:16.1f}:1 {min(oz4, 1e6):15.0f}:1 {zh:16.2f} {zz_:16.2f}")
dc_need_halo = L25["dm14"] / math.sqrt(2 * ln20) / Aba; dc_need_Hz = L25["Hz"] / math.sqrt(2 * ln20) / Aba
P(f"  20:1 from the sample means alone (any N; expected ln B -> Delta^2/(2 s_C^2)) needs delta_c <= {dc_need_halo:.3f} dex (halo law) and <= {dc_need_Hz:.3f} dex (H(z) law)")
def _gas_to_bary(dgas, fg=0.5): return math.log10(1 - fg + fg * 10**dgas)
GASB = {d: (_gas_to_bary(d), _gas_to_bary(-d)) for d in (0.2, 0.7)}
P(f"  a gas-mass scale error of +/-0.2 and +/-0.7 dex at a gas fraction of 0.5 is " +
  "; ".join(f"{d}: {a:+.3f}/{b:+.3f} dex" for d, (a, b) in GASB.items()) + " on the baryonic mass")
OUT["S4"]["shared"] = SHARED; OUT["S4"]["delta_c_needed"] = dict(halo=dc_need_halo, Hz=dc_need_Hz); OUT["S4"]["gas_to_baryon"] = {str(k): v for k, v in GASB.items()}

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
        return f"${m_:.1f}\\times10^{e_}$:1"
    if x >= 100: return f"{int(round(x, -int(math.floor(math.log10(x))) + 1))}:1"
    if x >= 10: return f"{x:.0f}:1"
    return f"{x:.1f}:1"
SHARED_ROWS = []
for r in SHARED[:5]:
    lim = ("--", "--") if r["s_C"] == 0 else (f"{r['halo_mean_limit']:.1f}", f"{r['Hz_mean_limit']:.1f}")
    SHARED_ROWS.append(f"{r['delta_c']:.2f} & {r['s_C']:.3f} & {fmt_odds(r['halo_N4_020'])} & {fmt_odds(r['halo_N4_010'])} & {fmt_odds(r['Hz_N4_020'])} & {lim[0]} & {lim[1]}\\\\")
P("  rows of the table of shared-calibration odds (as typeset):"); [P("     " + r_) for r_ in SHARED_ROWS]
_tex = open(os.path.join(HERE, "mnras_a0_lambda_v3.tex")).read()
_tab = _tex[_tex.index(r"\label{tab:shared}"):]; _tab = _tab[_tab.index(r"\midrule") + len(r"\midrule"):_tab.index(r"\bottomrule")]
_typeset = [l_.strip() for l_ in _tab.strip().splitlines() if l_.strip()]
check("S4m the shared-calibration odds reduce to the independent-error odds when the common term vanishes (1e-12)", _red < 1e-12, f"{_red:.1e}", kind="identity")
check("S4n AGAINST THE DESIGN: a common-mode baryonic-mass calibration error of 0.10 dex drops four galaxies at 0.20 dex from >20:1 to <5:1 against the halo law, and 20:1 from the sample means needs delta_c <= 0.09 dex (halo) and <= 0.16 dex (H(z)) whatever N",
      SHARED[0]["halo_N4_020"] > 20 and SHARED[2]["halo_N4_020"] < 5 and 0.08 < dc_need_halo < 0.095 and 0.15 < dc_need_Hz < 0.165,
      f"{SHARED[0]['halo_N4_020']:.0f}:1 -> {SHARED[2]['halo_N4_020']:.1f}:1; delta_c {dc_need_halo:.3f} / {dc_need_Hz:.3f}", kind="model")
check("S4r the table of shared-calibration odds in the manuscript is exactly the computed one", _typeset == SHARED_ROWS, f"{len(_typeset)} rows typeset", kind="identity")
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
    s_halo = math.log10(ratio_halo(2.5)) / 2.5; s_Hz = float(np.log10(E(2.5))) / 2.5
    _P(f"  a0 = (1 - f_DM) g_obs / [ln(1/f_DM)]^2 for {len(zz)} of {len(rows)} galaxies (f_DM in (0.02, 0.98)); z = {zz.min():.2f} - {zz.max():.2f}")
    _P(f"  median a0 = {10**np.median(la):.3e} m s^-2;  16-84%: {10**np.percentile(la,16):.2e} - {10**np.percentile(la,84):.2e};  median y = {np.median(yy):.2f}")
    y16, y50, y84 = np.percentile(yy, [16, 50, 84])
    _P(f"  accelerations probed: y = g_bar/a0 16/50/84% = {y16:.2f}/{y50:.2f}/{y84:.2f};  {int((yy < 0.3).sum())} of {len(yy)} below 0.3;  A_obs there = {1/abs(float(n_slope(y16))):.1f}/{1/abs(float(n_slope(y50))):.1f}/{1/abs(float(n_slope(y84))):.1f}")
    _P(f"  d log10 a0/dz = {slope:+.4f} +/- {bs.std():.4f} (bootstrap);  constant: 0 ({slope/bs.std():+.1f} sigma);  halo-emergent mean slope {s_halo:+.4f} ({(slope-s_halo)/bs.std():+.1f} sigma);  H(z) mean slope {s_Hz:+.4f} ({(slope-s_Hz)/bs.std():+.1f} sigma)")
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
        tilt.append(dict(beta=beta, n=int(ok_.sum()), slope=float(st), err=float(bt), sig_const=float(st / bt), sig_halo=float((s_halo - st) / bt)))
    _P("  baryonic-mass calibration drift beta [dex per unit z]  ->  slope, and its distance from constant / from the halo law:")
    for t in tilt:
        _P(f"     beta {t['beta']:+.3f}: N {t['n']:3d}, slope {t['slope']:+.3f} +/- {t['err']:.3f};  constant {t['sig_const']:+.1f} sigma;  halo law {t['sig_halo']:+.1f} sigma")
    # one galaxy sits exactly on the f_DM = 0.02 edge of the inversion; admitting it:
    edge = (fr >= 0.02 - 1e-12) & (fr < 0.98)
    la_e = np.log10((1 - fr[edge]) * gr[edge] / np.log(1 / fr[edge])**2); slope_edge = float(np.polyfit(zr[edge], la_e, 1)[0])
    _P(f"  admitting the one galaxy at the f_DM = 0.02 edge: slope {slope:+.3f} -> {slope_edge:+.3f} (N {int(edge.sum())}), a {abs(slope_edge - slope)/bs.std():.1f} sigma move from one object")
    beta_halo2 = max((t["beta"] for t in tilt if t["sig_halo"] < 2.0 and t["beta"] < 0), default=None)
    beta_const2 = max((t["beta"] for t in tilt if abs(t["sig_const"]) > 2.0 and t["beta"] < 0), default=None)
    _P(f"  the halo law comes within 2 sigma at beta = {beta_halo2}; constancy goes 2 sigma off at beta = {beta_const2}")
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
R5o = rc100_run(RC100_ORIG, verbose=False)     # the earlier transcription, run by the same code, for the old -> new table
_A = R5["_arrays"]
zz, la, yy, icpt, bs = _A["zz"], _A["la"], _A["yy"], _A["icpt"], _A["bs"]
sg, eg, sy, ey, slope_edge, t1, k1m = _A["sg"], _A["eg"], _A["sy"], _A["ey"], _A["slope_edge"], _A["t1"], _A["k1m"]
slope, tilt, injR, weak_H = R5["slope"], R5["tilt"], R5["injection"], R5["weakest_excl_Hz"]
s_halo, s_Hz, beta_halo2, beta_const2 = R5["slope_halo"], R5["slope_Hz"], R5["beta_halo_within_2sigma"], R5["beta_const_2sigma_off"]
OUT["S5"] = {k_: v for k_, v in R5.items() if k_ != "_arrays"}
OUT["S5_original_transcription"] = {k_: v for k_, v in R5o.items() if k_ != "_arrays"}
# ---- the transcription correction itself (CFG289): which cells changed, and what that does to every quoted RC100 number
import hashlib
_sha = hashlib.sha256(open(RC100, "rb").read()).hexdigest()
_rf, _ro = list(csv.DictReader(open(RC100))), list(csv.DictReader(open(RC100_ORIG)))
_prim = ("name", "z", "logMbar_Msun", "Re_kpc", "fDM_within_Re", "Vc_Re_kms", "sigma0_kms")
_chg = {f: [int(a["idx"]) for a, b in zip(_rf, _ro) if a[f] != b[f]] for f in _prim}
_flip = [int(a["idx"]) for a, b in zip(_rf, _ro) if a["deepMOND_g_lt_a0"] != b["deepMOND_g_lt_a0"]]
P(f"  RC100 transcription correction (CFG289): corrected file sha256 {_sha[:16]}...; changed primary cells by column: " +
  ", ".join(f"{f} {len(v)}" for f, v in _chg.items() if v) + f"; total {sum(len(v) for v in _chg.values())}; deep-regime flag flips in row(s) {_flip}")
_inv_rows = sorted(set(_chg["fDM_within_Re"]) | set(_chg["Vc_Re_kms"]))
P(f"  cells that enter the inversion (f_DM, and V_c through g = V_c^2/R_e): rows {_inv_rows}")
RC100_MOVES = []
for lab, kk, fmt in (("slope d log a0/dz", "slope", "+.3f"), ("its bootstrap error", "slope_err", ".3f"), ("median a0 [m s^-2]", "median_a0", ".3e"),
                     ("scatter about the fit [dex]", "scatter", ".3f"), ("slope | log g_obs", "slope_ctrl_gobs", "+.3f"), ("slope | log y", "slope_ctrl_y", "+.3f"),
                     ("weakest exclusion of the halo slope [sigma]", "weakest_excl_halo", ".2f"), ("weakest exclusion of the H(z) slope [sigma]", "weakest_excl_Hz", ".2f"),
                     ("slope with the f_DM = 0.02 edge galaxy", "slope_with_edge_galaxy", "+.3f"), ("corr(log a0, log y)", "scatter_corr_la_y", "+.2f"),
                     ("16th percentile of a0 [m s^-2]", None, ".3e")):
    old = R5o[kk] if kk else R5o["a0_16_84"][0]; new = R5[kk] if kk else R5["a0_16_84"][0]
    RC100_MOVES.append(dict(quantity=lab, old=float(old), new=float(new)))
    P(f"     {lab:46s} {format(old, fmt):>11s} -> {format(new, fmt):>11s}")
for t_o, t_n in zip(R5o["tilt"], R5["tilt"]):
    RC100_MOVES.append(dict(quantity=f"drift beta {t_o['beta']:+.3f}: slope", old=t_o["slope"], new=t_n["slope"]))
    P(f"     drift beta {t_o['beta']:+.3f}: slope {t_o['slope']:+.3f} -> {t_n['slope']:+.3f} (constant {t_o['sig_const']:+.1f} -> {t_n['sig_const']:+.1f} sigma; halo {t_o['sig_halo']:+.1f} -> {t_n['sig_halo']:+.1f} sigma)")
OUT["S5_correction"] = dict(sha256=_sha, changed=_chg, deep_flag_flips=_flip, inversion_rows=_inv_rows, moves=RC100_MOVES)
check("S5a the inversion is exact: nu(y) (1 - f_DM) = 1 at y = [ln(1/f_DM)]^2", abs(nu(math.log(1/0.37)**2) * (1 - 0.37) - 1) < 1e-12)
check("S5e AGAINST INTEREST: a baryonic-mass calibration drift of at most 0.05 dex per unit z brings the halo law within 2 sigma (the result is calibration-conditional)",
      beta_halo2 is not None and beta_halo2 >= -0.05, f"beta = {beta_halo2}")
check("S5f AGAINST INTEREST: the independent KMOS3D replication (L332) failed, and a third to a half of its z > 1.9 galaxies rotate below their own Newtonian baryons",
      (not t1["ok"]) and "0.27-0.54" in k1m, k1m[:80])
check("S5g the tilt table at beta = 0 reproduces the main fit exactly (same galaxies, same slope)",
      [t for t in tilt if t["beta"] == 0.0][0]["n"] == len(zz) and abs([t for t in tilt if t["beta"] == 0.0][0]["slope"] - slope) < 1e-9, kind="identity")
check("I5 the inversion recovers injected trends (0, halo law, H(z)) to 0.02 dex per unit z when f_DM obeys the kernel", all(abs(a - b) < 0.02 for a, b, _ in injR),
      ", ".join(f"{a:+.3f}->{b:+.3f}" for a, b, _ in injR), kind="injection")
check("S5b the RC100 trend is consistent with constant a0 within 2.5 sigma and more than 3 sigma below the halo-emergent mean slope",
      abs(slope / bs.std()) < 2.5 and (s_halo - slope) / bs.std() > 3.0, f"{slope:+.3f} +/- {bs.std():.3f}")
check("S5c no decline is claimed: the slope is within 2.5 sigma of zero under every treatment", abs(slope) < 2.5 * bs.std() and abs(sg) < 2.5 * eg and abs(sy) < 2.5 * ey)
check("S5d AGAINST INTEREST: the 3.9 sigma does not survive every control -- the weakest exclusion of the halo-emergent slope is below 3 sigma, and that is the number to quote",
      min((s_halo - slope) / bs.std(), (s_halo - sg) / eg, (s_halo - sy) / ey) < 3.0, f"weakest {min((s_halo-slope)/bs.std(), (s_halo-sg)/eg, (s_halo-sy)/ey):.1f} sigma")
def _rc100_verdicts(R):
    """the RC100 statements of the text, evaluated on one transcription: (S5b, S5c, S5d, S5e)"""
    A_ = R["_arrays"]; se = A_["bs"].std()
    b_ = abs(R["slope"] / se) < 2.5 and (R["slope_halo"] - R["slope"]) / se > 3.0
    c_ = abs(R["slope"]) < 2.5 * se and abs(A_["sg"]) < 2.5 * A_["eg"] and abs(A_["sy"]) < 2.5 * A_["ey"]
    d_ = R["weakest_excl_halo"] < 3.0
    e_ = R["beta_halo_within_2sigma"] is not None and R["beta_halo_within_2sigma"] >= -0.05
    return (b_, c_, d_, e_)
check("S5h the corrected RC100 transcription is the CFG289 file (sha256) and differs from the earlier one in exactly 17 primary cells: 5 names, 9 baryonic masses, 1 dark-matter fraction, 2 circular velocities; three of them enter the inversion; one deep-regime flag flips (row 44)",
      _sha == RC100_SHA256 and [len(_chg[f]) for f in ("name", "logMbar_Msun", "fDM_within_Re", "Vc_Re_kms")] == [5, 9, 1, 2] and sum(len(v) for v in _chg.values()) == 17 and _flip == [44]
      and len(_inv_rows) == 3,
      ", ".join(f"{f} {len(v)}" for f, v in _chg.items() if v), kind="identity")
check("S5i the correction changes no RC100 statement of the text (S5b-S5e evaluate the same on both transcriptions) and moves the slope by less than 0.001 dex per unit z (< 0.1 sigma)",
      _rc100_verdicts(R5) == _rc100_verdicts(R5o) and abs(R5["slope"] - R5o["slope"]) < min(0.1 * R5["slope_err"], 0.001) and R5["N"] == R5o["N"] == 99,
      f"slope {R5o['slope']:+.4f} -> {R5['slope']:+.4f}; verdicts {_rc100_verdicts(R5o)} -> {_rc100_verdicts(R5)}")

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
    m = (R > 0) & (V > 0) & (eV > 0) & (eV / V < 0.10)
    v2 = (np.sign(Vg) * Vg**2 + _ml[nm] * (Vd**2 + Vb**2))[m]; ok = v2 > 0
    if ok.sum() == 0: continue
    kb.append(v2[ok] / R[m][ok] * K); ko.append(V[m][ok]**2 / R[m][ok] * K); ke.append((2 * eV[m] / V[m] / math.log(10))[ok]); ki.append(np.full(ok.sum(), len(ki)))
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
check("S6g at a fixed Upsilon_K = 0.6 (the survey's own refit) they agree within 2.5 sigma at every SPARC disc ratio",
      all(abs(z_) < 2.5 for z_ in z6), ", ".join(f"{z_:+.1f}" for z_ in z6))
check("S6h the SPARC window amplitude brackets kappa_Lambda = 1/2 across Upsilon_disc = 0.5-0.7", kS[0] > 0.5 > kS[2], ", ".join(f"{k_:.3f}" for k_ in kS))
check("S6i PITFALL: per-galaxy ratios fitted to the curves (log-correlation > 0.8 with the Newtonian no-dark-matter ratio) lower the window kappa by a factor above 1.5 at every disc ratio",
      r_kin > 0.8 and min(fac_kin) > 1.5, f"r = {r_kin:.3f}; factors " + ", ".join(f"{x_:.2f}" for x_ in fac_kin))
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
# ---- the coefficient like-for-like on H0: profile likelihood over SPARC with the stellar mass-to-light ratio free per galaxy
_pl = open(os.path.join(ROOT, "real_research", "reviews", "mi_a0_profile_likelihood_milgrom_footing_2026.out")).read()
PL = {}
for key, pat in (("half_L", r"kappa = 1/2\s+\(THE FRAMEWORK\)"), ("twopi_L", r"kappa = 1/2pi \(Milgrom 2020\)"), ("half_crit", r"alt footing rho_tot/cH0"), ("twopi_H0", r"Milgrom cH0/2pi \(own footing\)"), ("free", r"free best fit")):
    mm = re.search(pat + r"\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", _pl)
    PL[key] = dict(a0=float(mm.group(1)), ratio=float(mm.group(2)), dchi2=float(mm.group(3)), sig_ind=float(mm.group(4)), sig_clu=float(mm.group(5)))
_cl = re.search(r"sigma\(a0\)/a0, galaxy-clustered\s+=\s+([0-9.]+)%", _pl)
PL["clustered_pct"] = float(_cl.group(1))
P("  profile likelihood (SPARC, Upsilon free per galaxy, gas fixed): " + "; ".join(f"{k_} a0 {v['a0']:.4f}e-10 dchi2 {v['dchi2']:.2f} ({v['sig_clu']:.2f} sigma clustered)" for k_, v in PL.items() if k_ != "clustered_pct") +
  f"; clustered error {PL['clustered_pct']:.2f}%")
S7["footing"] = PL
OUT["S7"] = S7
check("S7a MUSE-DARK by route (CFG262, CFG236) as quoted: route rises +0.57 +/- 0.09 / -0.11 +/- 0.49 / +0.04 +/- 0.14 dex between the thirds at z 0.52 and 1.20 (H(z) +0.18); mass drift -0.72 [-0.97, -0.50] dex/z (-0.43 [-0.72, -0.15] at fixed SED mass); needed SED bias 1.8-2.2 dex/z",
      [round(MD[r]["d"], 2) for r in ("i", "ii", "iii")] == [0.57, -0.11, 0.04] and [round(MD[r]["sd"], 2) for r in ("i", "ii", "iii")] == [0.09, 0.49, 0.14]
      and round(MD["i"]["rival"], 2) == 0.18 and [round(z_, 2) for z_ in MDz] == [0.52, 0.88, 1.20]
      and [round(_m236["b"], 2), round(_m236["lo"], 2), round(_m236["hi"], 2)] == [-0.72, -0.97, -0.50] and [round(_t236["R198"], 1), round(_t236["R199a"], 1)] == [1.8, 2.2]
      and [round(x, 2) for x in _dM] == [-0.43, -0.72, -0.15], kind="identity")
check("S7b the MUSE-DARK rise travels with the baryon route: the fitted-mass route rises >5 sigma above constancy and >3 sigma above H(z), while neither SED route excludes either law at 2 sigma",
      MD["i"]["d"] / MD["i"]["sd"] > 5 and (MD["i"]["d"] - MD["i"]["rival"]) / MD["i"]["sd"] > 3
      and all(abs(MD[r]["d"]) / MD[r]["sd"] < 2 and abs(MD[r]["d"] - MD[r]["rival"]) / MD[r]["sd"] < 2 for r in ("ii", "iii")),
      ", ".join(f"({r}) {MD[r]['d']/MD[r]['sd']:+.1f} / {(MD[r]['d']-MD[r]['rival'])/MD[r]['sd']:+.1f} sigma" for r in ("i", "ii", "iii")))
check("S7c KURVS as quoted (CFG140/160/165/189/194): outer g_bar/a0 0.06-0.67; cell +3.3/-0.1 sigma; measured markers +2.4/-0.4; mu 1.5 +1.2/-2.1; alpha x 0.6 +1.3/-2.0; 4.5 per cent velocity scale; likelihood ratio 0.5-1.7",
      len(KY) == 10 and (min(KY), max(KY)) == (0.06, 0.67) and [round(x, 1) for x in KZ["cell"]] == [3.3, -0.1] and list(KZ["markers"]) == [2.4, -0.4]
      and [round(x, 1) for x in KZ["mu15"]] == [1.2, -2.1] and [round(x, 1) for x in KZ["alpha06"]] == [1.3, -2.0] and round((1 - KVS) * 100, 1) == 4.5
      and round(min(KLR), 1) == 0.5 and round(max(KLR), 1) == 1.7, kind="identity")
check("S7d AGAINST INTEREST, and its limits: at the pre-declared KURVS cell the constant law is >3 sigma high and H(z) fits, but the lean (constant above +2 sigma, H(z) within 2 sigma) ends at 1.5 M* of gas, at 0.6 of the pressure calibration and for a <5 per cent lower velocity scale, and the nuisance-marginalised likelihood ratio is below 2",
      KZ["cell"][0] > 3 and abs(KZ["cell"][1]) < 2 and KZ["mu15"][0] < 2 and KZ["alpha06"][0] < 2 and 0.95 < KVS < 1 and max(KLR) < 2,
      f"cell {KZ['cell'][0]:+.2f}/{KZ['cell'][1]:+.2f}; mu1.5 {KZ['mu15'][0]:+.2f}; alpha0.6 {KZ['alpha06'][0]:+.2f}; v {KVS:.3f}; LR max {max(KLR):.2f}")
check("S7e MIGHTEE-HI/LADUMA as quoted (CFG279, CFG258): b = -1.04 +/- 1.51; anchored a1 +5.23 +/- 1.05 vs -4.80 +/- 0.76; empirical/formal 5.2; formal z > 3 under constancy in 11-32 per cent of mocks; H(z) x1.045 at z = 0.09",
      [round(MB[0], 2), round(MB[1], 2)] == [-1.04, 1.51] and (MA["varying"]["a1"], MA["varying"]["err"], MA["constant 0.6"]["a1"], MA["constant 0.6"]["err"]) == (5.23, 1.05, -4.8, 0.76)
      and round(M258["ratio"], 1) == 5.2 and (round(M258["z3_none"] * 100), round(M258["z3_B"] * 100)) == (11, 32) and round(M_rival, 3) == 1.045
      and (round(MPF, 1), round(MPR, 1)) == (-0.7, -1.0) and round(MA["varying"]["a1"] / MA["varying"]["err"]) == 5, kind="identity")
check("S7f the MIGHTEE-HI/LADUMA within-sample slope is consistent with both laws (|pull| < 2), and the SPARC-anchored slope changes sign with the mass-to-light convention",
      abs(MPF) < 2 and abs(MPR) < 2 and MA["varying"]["a1"] > 0 > MA["constant 0.6"]["a1"], f"pulls {MPF:+.2f} / {MPR:+.2f}")
_B1, _B2, _B3 = _b269["B1 4<=z<6|COMPLETE"], _b269["B2 6<=z<8|COMPLETE"], _b269["B3 8<=z<=15|COMPLETE"]
check("S7g z >= 4 as quoted (CFG269): complete pools z 4-6 (14 objects) P 1.45-1.94 and z 8-14 P 1.28-1.32 MARGINAL at 0.15 dex and NOT POSSIBLE at 0.30 dex; z 6-8 one object, NOT POSSIBLE",
      _B1["n"] == 14 and [round(x, 2) for x in _B1["P_range"]] == [1.45, 1.94] and [round(x, 2) for x in _B3["P_range"]] == [1.28, 1.32]
      and _B1["verdict"] == _B3["verdict"] == "MARGINAL" and set(_B1["G1_verdicts"]) == set(_B3["G1_verdicts"]) == {"NOT POSSIBLE"}
      and _B2["n"] == 1 and _B2["verdict"] == "NOT POSSIBLE" and _B3["n"] == 2 and round(sum(_B3["P_range"]) / 2, 1) == 1.3, kind="identity")
check("S7h no complete (stars + gas) pool at z >= 4 separates the two laws (P < 2), and every stars-only pool that does carries the gas-limited flag",
      all(v["P_range"][1] < 2 for k_, v in _b269.items() if k_.endswith("COMPLETE"))
      and all(v["G4"] for k_, v in _b269.items() if k_.endswith("LOWER-LIMIT") and v["verdict"] == "SEPARATES"))
check("S7i the gas-prescription bracket at z ~ 2.2 (CFG224b, quoted in PAPER38 as 0.2-0.7 dex) is 0.21-0.67 dex", (round(GAS[0], 2), round(GAS[1], 2)) == (0.21, 0.67), kind="identity")
check("S7j the source-table audit (CFG287) as quoted: 22 sources (KURVS not among them), 3703 sampled cells in 29 tables with no transcription mismatch; no erratum registered for any published source paper",
      AUD["cells"] == 3703 and AUD["tables"] == 29 and AUD["fails"] == 0 and AUD["passed"] and AUD["errata"] == 0 and AUD["registered"] == 0
      and AUD["sources"] == 22 and not AUD["kurvs_in"], kind="identity")
check("S7k the footing comparison as quoted: best fit 1.08e-10 with a 5.4 per cent clustered error; dchi2 63.9 / 154.3 / 7.0 / 5.3 (1.8 / 2.8 / 0.6 / 0.5 sigma clustered) for 1/2 and 1/2pi on rho_Lambda, 1/2 on rho_crit and Milgrom's cH0/2pi",
      round(PL["free"]["a0"], 2) == 1.08 and round(PL["clustered_pct"], 1) == 5.4
      and [round(PL[k_]["dchi2"], 1) for k_ in ("half_L", "twopi_L", "half_crit", "twopi_H0")] == [63.9, 154.3, 7.0, 5.3]
      and [round(PL[k_]["sig_clu"], 1) for k_ in ("half_L", "twopi_L", "half_crit", "twopi_H0")] == [1.8, 2.8, 0.6, 0.5], kind="identity")
check("S7l like-for-like on H0 the data do not separate 1/2 from 1/2pi (both within 1 sigma clustered, dchi2 differing by < 2); 1/2 is ahead of 1/2pi only with both placed on the rho_Lambda footing",
      PL["half_crit"]["sig_clu"] < 1 and PL["twopi_H0"]["sig_clu"] < 1 and abs(PL["half_crit"]["dchi2"] - PL["twopi_H0"]["dchi2"]) < 2 and PL["half_L"]["dchi2"] < PL["twopi_L"]["dchi2"],
      f"{PL['half_crit']['dchi2']:.2f} vs {PL['twopi_H0']['dchi2']:.2f}")

# ----------------------------------------------------------------------------------------------------------------
json.dump(OUT, open(os.path.join(HERE, "paper_numbers.json"), "w"), indent=1, default=float)
P(""); P(f"RESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
for k_ in ("identity", "model", "data", "injection"):
    P(f"   {len(KINDS.get(k_, [])):2d} {k_:9s} -- {KIND_TEXT[k_]}")
OUT["check_kinds"] = {k_: len(v) for k_, v in KINDS.items()}
json.dump(OUT, open(os.path.join(HERE, "paper_numbers.json"), "w"), indent=1, default=float)
if __name__ == "__main__":
    sys.exit(1 if FAILS else 0)
