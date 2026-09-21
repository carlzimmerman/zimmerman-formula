#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
paper_numbers.py -- every number quoted in the MNRAS manuscript `mnras_a0_lambda_v2.tex` that is not printed by one
of the three repository estimators (those are re-run by reproduce_all.sh):

    real_research/reviews/mi_btfr_intercept_kappa_door_2026.py          -> kappa = 0.465 +/- 0.076, the 9.47% floor
    real_research/reviews/mi_distance_free_gbar_estimator_sparc_2026.py -> kappa = 0.551 +/- 0.043 (shape-only)
    real_research/reviews/kappa_h0_convention_audit_2026.py             -> the H0-convention shifts

Sections (each ends in checks that CAN fail; exit code 1 if any does):
    S1  the relation, step by step: rho_crit, rho_Lambda, c sqrt(G rho_Lambda), a0, the four equivalent forms, Z
    S2  the standard radial-acceleration fit on SPARC and its mass-to-light degeneracy  (kappa against Upsilon_disc)
    S3  the candidate coefficients, the mass-budget floor, and the H0 lock
    S4  the redshift laws: constant, H(z), the LambdaCDM emergent scale (NFW + concentration-mass relation),
        the density mapping under DESI DR2 w0-wa; the error amplification of the kernel inversion; the 20:1 rule
    S5  the closed-form inversion of the RC100 dark-matter fractions
Both densities are carried throughout: rho_Lambda (a0 = 9.36e-11) and rho_crit (a0 = 1.13e-10).
Run from anywhere:  python3 paper_numbers.py        Output: paper_numbers.json next to this file.
"""
import os, sys, glob, json, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SPARC = os.path.join(ROOT, "real_research", "data", "sparc_data")
RC100 = os.path.join(ROOT, "real_research", "data", "rc100_nestorshachar2023_table3.csv")

OUT, FAILS, NCHK = {}, [], [0]
def P(*a): print(*a, flush=True)
def check(name, ok, detail=""):
    NCHK[0] += 1
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
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
OUT["S2"] = dict(shape_only=shape, kappa_B=kB, sigma_B=sB, B_budget=dict(ml_disc=ml_disc, ml_bul=ml_bul, ml_grid=ml_all, gas=gas, stat=statB), bulgeless=bl,
                 shape_immunity=imm, standard_move_10pc=std_move, n_gal=ngal, n_pts=int(len(gb)), table=rows, ud_for_half_L=ud_half, ud_for_half_C=ud_half_C,
                 fixed_L=dict(UD=uL, rms=rL), fixed_C=dict(UD=uC, rms=rC))
r05 = [r for r in rows if abs(r["UD"] - 0.5) < 1e-9][0]
check("S2a at Upsilon_disc = 0.5 the fit returns the literature a0 = 1.2e-10 within 5%", abs(r05["a0"] / 1.2e-10 - 1) < 0.05, f"a0 = {r05['a0']:.3e}")
check("S2b the degeneracy is steep: kappa moves by more than 0.15 between Upsilon_disc = 0.5 and 0.7", rows[1]["kappa_L"] - rows[3]["kappa_L"] > 0.15,
      f"{rows[1]['kappa_L']:.3f} -> {rows[3]['kappa_L']:.3f}")
check("S2d the shape-only estimator is immune to a common distance rescaling (< 1e-5) while the standard fit is not (> 15%)", imm < 1e-5 and std_move > 0.15,
      f"{imm:.1e} vs {std_move*100:.1f}%")
check("S2e the replication agrees with the repository's estimator B at Upsilon_bul = 0.7, Upsilon_disc = 0.5 and 0.7 (0.529, 0.574) within 0.01",
      abs(grid[(0.5, 0.7)] - 0.529) < 0.01 and abs(grid[(0.7, 0.7)] - 0.574) < 0.01, f"{grid[(0.5, 0.7)]:.3f}, {grid[(0.7, 0.7)]:.3f}")
check("S2f AGAINST THE EARLIER ERROR BAR: the bulge mass-to-light ratio moves estimator B by more than twice the 0.043 previously quoted",
      ml_bul > 2 * 0.043, f"bulge term {ml_bul:.3f}; total {sB:.3f}")
check("S2c kappa = 1/2 needs a disc mass-to-light ratio inside the population-synthesis range 0.4-0.8", 0.4 < ud_half < 0.8 and 0.4 < ud_half_C < 0.8,
      f"{ud_half:.2f} / {ud_half_C:.2f}")

# ================================================================================================================
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
check("S3d the data do not single out 1/2: at least three candidates lie inside 2 sigma of both measurements... or fail",
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

# ================================================================================================================
head("S5  THE CLOSED-FORM INVERSION OF THE RC100 DARK-MATTER FRACTIONS")
import csv
rows = list(csv.DictReader(open(RC100)))
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
P(f"  a0 = (1 - f_DM) g_obs / [ln(1/f_DM)]^2 for {len(zz)} of {len(rows)} galaxies (f_DM in (0.02, 0.98)); z = {zz.min():.2f} - {zz.max():.2f}")
P(f"  median a0 = {10**np.median(la):.3e} m s^-2;  16-84%: {10**np.percentile(la,16):.2e} - {10**np.percentile(la,84):.2e};  median y = {np.median(yy):.2f}")
y16, y50, y84 = np.percentile(yy, [16, 50, 84])
P(f"  accelerations probed: y = g_bar/a0 16/50/84% = {y16:.2f}/{y50:.2f}/{y84:.2f};  {int((yy < 0.3).sum())} of {len(yy)} below 0.3;  A_obs there = {1/abs(float(n_slope(y16))):.1f}/{1/abs(float(n_slope(y50))):.1f}/{1/abs(float(n_slope(y84))):.1f}")
P(f"  d log10 a0/dz = {slope:+.4f} +/- {bs.std():.4f} (bootstrap);  constant: 0 ({slope/bs.std():+.1f} sigma);  halo-emergent mean slope {s_halo:+.4f} ({(slope-s_halo)/bs.std():+.1f} sigma);  H(z) mean slope {s_Hz:+.4f} ({(slope-s_Hz)/bs.std():+.1f} sigma)")
dfdm = np.polyfit(zz, np.log10([float(r["fDM_within_Re"]) for r in rows if 0.02 < float(r["fDM_within_Re"]) < 0.98]), 1)[0]
P(f"  what drives it: d log10 f_DM/dz = {dfdm:+.3f}  (the published fall of the dark-matter fraction with redshift); the inversion is monotone in f_DM")
# ---- is the trend a selection effect?  control for a measured acceleration (independent of a0) and, separately, for the inferred y
lgo = np.array([math.log10(float(r["g_Re_ms2"])) for r in rows if 0.02 < float(r["fDM_within_Re"]) < 0.98])
def partial(cols):
    X = np.c_[np.ones_like(zz), zz, *cols]
    b = np.linalg.lstsq(X, la, rcond=None)[0]
    B = np.array([np.linalg.lstsq(X[i], la[i], rcond=None)[0] for i in (rng.integers(0, len(zz), len(zz)) for _ in range(4000))])
    return float(b[1]), float(B[:, 1].std()), float(np.std(la - X @ b))
sg, eg, rg = partial([lgo]); sy, ey, ry = partial([np.log10(yy)])
P(f"  scatter about the fit: {np.std(la - (icpt + slope*zz)):.2f} dex;  corr(log a0_hat, log y_hat) = {np.corrcoef(la, np.log10(yy))[0,1]:+.2f}  (noise in f_DM moves a0_hat and y_hat oppositely)")
P(f"  controlling for log g_obs (measured, a0-free):   d log a0/dz = {sg:+.3f} +/- {eg:.3f}   -> halo-emergent mean slope disfavoured at {(s_halo-sg)/eg:.1f} sigma")
P(f"  controlling for log y_hat (absorbs noise AND part of any real signal): {sy:+.3f} +/- {ey:.3f}   -> {(s_halo-sy)/ey:.1f} sigma")
weak_H = min((s_Hz - slope) / bs.std(), (s_Hz - sg) / eg, (s_Hz - sy) / ey)
P(f"  weakest exclusion of the H(z) mean slope over the three treatments: {weak_H:.1f} sigma")
P(f"  range of the redshift slope over the three treatments: {min(slope, sg, sy):+.2f} to {max(slope, sg, sy):+.2f};  weakest exclusion of the halo-emergent slope: {min((s_halo-slope)/bs.std(), (s_halo-sg)/eg, (s_halo-sy)/ey):.1f} sigma")
OUT["S5"] = dict(N=int(len(zz)), slope=float(slope), slope_err=float(bs.std()), median_a0=float(10**np.median(la)), median_y=float(np.median(yy)),
                 slope_halo=s_halo, slope_Hz=s_Hz, dlogfdm_dz=float(dfdm), scatter=float(np.std(la - (icpt + slope*zz))),
                 slope_ctrl_gobs=sg, err_ctrl_gobs=eg, slope_ctrl_y=sy, err_ctrl_y=ey,
                 y_percentiles=[float(y16), float(y50), float(y84)], n_below_gate=int((yy < 0.3).sum()), weakest_excl_Hz=float(weak_H))
check("S5a the inversion is exact: nu(y) (1 - f_DM) = 1 at y = [ln(1/f_DM)]^2", abs(nu(math.log(1/0.37)**2) * (1 - 0.37) - 1) < 1e-12)
check("S5b the RC100 trend is consistent with constant a0 within 2.5 sigma and more than 3 sigma below the halo-emergent mean slope",
      abs(slope / bs.std()) < 2.5 and (s_halo - slope) / bs.std() > 3.0, f"{slope:+.3f} +/- {bs.std():.3f}")
check("S5c no decline is claimed: the slope is within 2.5 sigma of zero under every treatment", abs(slope) < 2.5 * bs.std() and abs(sg) < 2.5 * eg and abs(sy) < 2.5 * ey)
check("S5d AGAINST INTEREST: the 3.9 sigma does not survive every control -- the weakest exclusion of the halo-emergent slope is below 3 sigma, and that is the number to quote",
      min((s_halo - slope) / bs.std(), (s_halo - sg) / eg, (s_halo - sy) / ey) < 3.0, f"weakest {min((s_halo-slope)/bs.std(), (s_halo-sg)/eg, (s_halo-sy)/ey):.1f} sigma")

# ----------------------------------------------------------------------------------------------------------------
json.dump(OUT, open(os.path.join(HERE, "paper_numbers.json"), "w"), indent=1, default=float)
P(""); P(f"RESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
if __name__ == "__main__":
    sys.exit(1 if FAILS else 0)
