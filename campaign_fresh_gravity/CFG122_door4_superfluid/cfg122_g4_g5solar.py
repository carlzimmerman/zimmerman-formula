#!/usr/bin/env python3
"""CFG122 G4 (constant count) and G5.4 (Solar System, explicit statement; both a0 footings; readings A and B; phase-boundary screening).
G4: PASS iff the number of untied new constants is 0 (the a0 tie alpha^3 Lam^2 N_a / M_Pl = kappa c sqrt(G rho_L) is admitted as the CFG43-type stated equivalent).
G5.4: (i) Cassini |gamma - 1| = 2 eps/(1+eps) <= 2.3e-5; (ii) WEP eta <= 1e-15 (MICROSCOPE), 1.4e-13 (LLR); (iii) sunward anomaly <= 1.27e-5 a0; (iv) phase-boundary screening.
Inputs recalled from the literature (UNVERIFIED, flagged): the Cassini, MICROSCOPE, LLR and ephemeris bounds are the frozen file's / the pricing script's values; isotopic masses below.
Run: python3 cfg122_g4_g5solar.py"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import *

R = Report("cfg122_g4_g5solar")
P, check = R.P, R.check

# =================================================================== G4
R.banner("G4  constants beyond kappa = 1/2 and Omega_c h^2 = 0.12")
consts = [
    ("m", "the mass of the condensate field's quanta (still required; nothing fixes it)", "untied"),
    ("alpha (or Lam)", "after the a0 tie alpha^3 Lam^2/M_Pl = a0, one of the pair remains free (a0 fixes only the combination)", "untied"),
    ("a0 tie", "alpha^3 Lam^2 N_a/M_Pl = kappa c sqrt(G rho_Lambda), N_a = 1 derived (S0.1); a RELATION among BK constants: postulated, not derived from the action", "admitted as the stated equivalent (postulated)"),
    ("T = m sigma^2 factor", "convention factor between the halo dispersion and the condensate temperature (reported at x 1/2 and x 2)", "convention, not tied"),
    ("normal-phase halo mass and concentration", "imported LCDM functions (Moster+2013: 4 numbers, Duffy+2008: 2 numbers), not derived by the door", "external per-halo function"),
    ("thermalisation rate", "needed to say whether the cold cosmological background condenses; not fixed by the EFT", "untied (UV-completion dependent)"),
]
for c_ in consts:
    P(f"  - {c_[0]:38s}: {c_[1]}  [{c_[2]}]")
n_untied = sum(1 for c_ in consts if c_[2].startswith("untied"))
R.num("G4_constants", consts)
R.num("G4_untied_count", n_untied)
R.verdict("G4", "PASS" if n_untied == 0 else "FAIL", f"{n_untied} independent untied new constants (m; one of alpha/Lambda; plus, outside the EFT, the thermalisation rate), against the line 0; the a0 tie is a postulated relation, not a derivation; the imported halo functions are additional per-halo inputs")

# =================================================================== G5.4
G_SI, MSUN_KG, AU_M = 6.674e-11, 1.98892e30, 1.495978707e11
GME, R_E, H_MIC = 3.986004418e14, 6.371e6, 7.1e5
g_sun_1AU = G_SI * MSUN_KG / AU_M ** 2
g_micro = GME / (R_E + H_MIC) ** 2
BOUND_CASSINI, BOUND_MIC, BOUND_LLR, S_EPH = 2.3e-5, 1e-15, 1.4e-13, 1.27e-5
# baryon number over atomic mass (u) for the composition-dependent coupling (dominant isotopes; RECALLED atomic masses, unverified):
ISO = {"48Ti": (48, 47.94794), "195Pt": (195, 194.96479), "56Fe": (56, 55.93494), "28Si": (28, 27.97693)}
BoverMu = {k: A / mu for k, (A, mu) in ISO.items()}
d_TiPt = abs(BoverMu["48Ti"] - BoverMu["195Pt"])
d_FeSi = abs(BoverMu["56Fe"] - BoverMu["28Si"])
R.banner("G5.4  Solar System: 1 AU and MICROSCOPE altitude, both footings, readings A (a0-line anomaly, saturating) and B (BK unscreened sqrt(a0 g))")
P(f"  g_sun(1 AU) = {g_sun_1AU:.4e} m/s^2;  g(MICROSCOPE, 710 km) = {g_micro:.4f} m/s^2;  Delta(B/mu): Ti-Pt {d_TiPt:.3e}, Fe-Si {d_FeSi:.3e}   [recalled isotope masses, unverified]")
res = {}
for foot in FOOTINGS:
    a0 = A0_SI[foot]
    nu = lambda g: math.sqrt(1 + a0 / g)
    readings = {"A": lambda g: (nu(g) - 1.0) * g, "B": lambda g: math.sqrt(a0 * g)}
    for rn, fa in readings.items():
        aS, aE = fa(g_sun_1AU), fa(g_micro)
        eps = aS / g_sun_1AU
        gm1 = 2 * eps / (1 + eps)
        eta_mic = d_TiPt * aE / g_micro
        eta_llr = d_FeSi * aS / g_sun_1AU
        anomaly = aS / a0
        res[(foot, rn)] = dict(a_sun=aS, eps=eps, gamma_minus_1=gm1, eta_mic=eta_mic, eta_llr=eta_llr, anomaly_over_a0=anomaly)
        P(f"  [{foot}] reading {rn}: a_phi(1 AU) = {aS:.4e} m/s^2 = {anomaly:.4g} a0;  eps = {eps:.3e};  |gamma - 1| = {gm1:.3e} ({gm1 / BOUND_CASSINI:.3g} x Cassini);  "
          f"eta_MICROSCOPE = {eta_mic:.3e} ({eta_mic / BOUND_MIC:.3g} x);  eta_LLR = {eta_llr:.3e} ({eta_llr / BOUND_LLR:.3g} x);  sunward anomaly / (s a0) = {anomaly / S_EPH:.3g}")
R.num("G5.4_readings", {f"{k[0]}|{k[1]}": v for k, v in res.items()})
pass_i = {k: v["gamma_minus_1"] <= BOUND_CASSINI for k, v in res.items()}
pass_ii = {k: (v["eta_mic"] <= BOUND_MIC and v["eta_llr"] <= BOUND_LLR) for k, v in res.items()}
pass_iii = {k: v["anomaly_over_a0"] <= S_EPH for k, v in res.items()}
P(f"  pass (i) Cassini: {pass_i};  (ii) WEP: {pass_ii};  (iii) ephemeris ceiling: {pass_iii}")

# (iv) phase-boundary screening: T/T_c for the ambient DM at 1 AU vs at the MW's r_M (same local density and dispersion; BK's criterion)
R.banner("G5.4 (iv)  phase-boundary screening: is the condensate absent at 1 AU and present at the galaxy's r_M?")
sig_loc = 150e3 / C_SI                                   # 150 km/s in units of c
rho_loc = 0.4e9 * (1.973269804e-5) ** 3
nfw_mw = NFW(6e10)
rho_at_rM = float(nfw_mw.rho(float(rM(6e10 * MSUN_EV, a0_nat("canonical")))))
rho_at_sun = float(nfw_mw.rho(8.2 * KPC_EV))
P(f"  MW-like halo (M_* = 6e10): NFW density at r_M(6e10) = {float(rM(6e10 * MSUN_EV, a0_nat('canonical'))) / KPC_EV:.2f} kpc is {rho_at_rM / rho_at_sun:.3f} of that at the Sun's 8.2 kpc; local DM density 0.4 GeV/cm^3 = {rho_loc:.3e} eV^4 (recalled, unverified)")
rows = []
for mm in (1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1e3):
    Tc = 2 * math.pi / mm * (rho_loc / mm / ZETA32) ** (2.0 / 3.0)
    T = mm * sig_loc ** 2
    Tc_rM = 2 * math.pi / mm * (rho_loc * rho_at_rM / rho_at_sun / mm / ZETA32) ** (2.0 / 3.0)
    rows.append((mm, T / Tc, T / Tc_rM))
    P(f"  m = {mm:8.3g} eV: T/T_c at 1 AU (ambient) = {T / Tc:.4g};  at the galaxy's r_M = {T / Tc_rM:.4g};  condensate at 1 AU: {'YES' if T < Tc else 'no'};  at r_M: {'YES' if T < Tc_rM else 'no'}")
screen_ok = any((r_[1] >= 1.0) and (r_[2] < 1.0) for r_ in rows)
P(f"  a screening plane point (absent at 1 AU AND present at r_M) among these m: {screen_ok}. Same density (to a factor {rho_at_rM / rho_at_sun:.2f}) and the same dispersion => the same phase at both places.")
R.num("G5.4_iv", rows)
# the door's own algebra at 1 AU (post hoc, labelled): gradient term vs the ambient X-bar
R.banner("G5.4 (post hoc, labelled)  the door's own algebra at 1 AU: gradient term p^2/2m against the ambient galactic X-bar (<= m V^2, V = 250 km/s)")
aM = a0_nat("canonical")
Msun_ev = MSUN_EV
r1 = AU_EV
gr_frac = []
for mm in (1e-3, 1e-1, 1.0, 1e1, 1e3):
    for aa in (1e-2, 1.0, 1e2):
        Lm = float(lam_tie(mm, aa, aM))
        C = mm * aa * Msun_ev / (4 * math.pi * r1 ** 2 * MPL)
        D = C * C / (16 * mm ** 4)
        grad = math.sqrt(D)                                  # p^2/2m in the gradient-dominated limit  = sqrt(D)
        Ybar = mm * (250e3 / C_SI) ** 2
        gr_frac.append((mm, aa, grad / Ybar))
P("  p^2/(2m) at 1 AU divided by the ambient m V^2 (>> 1: the gradient regime = unscreened sqrt(a0 g_N), Reading B):")
for mm, aa, v in gr_frac:
    P(f"    m = {mm:8.3g} eV, alpha = {aa:6.3g}: {v:.3g}")
R.num("G5.4_posthoc_gradient_over_ambient", gr_frac)
allB = all(v > 1 for (_, _, v) in gr_frac if _ <= 100)
n_screen = sum(1 for (_, _, v) in gr_frac if v < 1)
P(f"  cells of this sample where the ambient term would dominate at 1 AU (screened, linear regime): {n_screen}/{len(gr_frac)}")
overall_ok = any(pass_i[(f, 'B')] and pass_ii[(f, 'B')] and pass_iii[(f, 'B')] for f in FOOTINGS) or screen_ok
fmt = lambda foot, rn, key, bound: f"{res[(foot, rn)][key] / bound:.3g}"
R.verdict("G5.4", "PASS" if overall_ok else "FAIL",
          "Reading B (BK unscreened): Cassini " + str([fmt(f, "B", "gamma_minus_1", BOUND_CASSINI) for f in FOOTINGS]) + " x bound, MICROSCOPE " + str([fmt(f, "B", "eta_mic", BOUND_MIC) for f in FOOTINGS])
          + " x, ephemeris " + str([fmt(f, "B", "anomaly_over_a0", S_EPH) for f in FOOTINGS]) + " x; Reading A: Cassini " + str([fmt(f, "A", "gamma_minus_1", BOUND_CASSINI) for f in FOOTINGS])
          + " x, MICROSCOPE " + str([fmt(f, "A", "eta_mic", BOUND_MIC) for f in FOOTINGS]) + " x, ephemeris " + str([fmt(f, "A", "anomaly_over_a0", S_EPH) for f in FOOTINGS]) + f" x; phase-boundary screening: {screen_ok}")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
