"""
dwarf_ecc_sigma_pilot_data.py
=================================================================================
PILOT DATASET for the framework's NATIVE non-adiabatic-inertia prediction:
  At fixed pericenter + mass, a RADIAL-PLUNGE (high-ecc) diffuse MW/LG dwarf
  runs HOTTER (higher internal sigma_los) than a CIRCULAR (low-ecc) one of the
  same mass and same closest-approach distance, because time-nonlocal inertia
  (response to the de Sitter horizon Unruh bath, ONE clock H_Lambda) reads the
  ACCELERATION HISTORY: a plunge sheds adiabatic external loading -> drops
  deeper into deep-MOND -> hotter. SIGN = theorem (plunge -> hotter); magnitude
  is theta(y)-kernel-hostage (factor ~2). MODIFIED-GRAVITY-IMPOSSIBLE: a field/
  metric MOND (AQUAL/QUMOND/AeST) external-field effect is INSTANTANEOUS, so at
  fixed pericenter it predicts EXACTLY ZERO sigma-vs-ecc correlation for any a0
  (Milgrom 2022). CDM/LCDM ~ 0 too.

  Footing (sealed): a0 = c*H_Lambda/Z = 9.36e-11 m/s^2 (pure-Lambda, de Sitter).
  Framework's OWN interpolation g_obs = sqrt(g_bar^2 + g_bar*a0); NEVER McGaugh nu.

  This file is DATA ONLY (no fabrication). Every numeric value carries a SOURCE
  citation; unavailable values are None. Confidence flag per dwarf (high/med/low).
  DO NOT git-push.

=================================================================================
PRE-SPECIFIED TEST (registered here BEFORE any fit, to block p-hacking)
---------------------------------------------------------------------------------
H1 (framework):  Within the DIFFUSE / non-adiabatic carrier subset (low internal
                 frequency: large r_half, low sigma^2/r_half), residual internal
                 sigma after controlling for mass (M_dyn or M_* and r_half) and
                 for pericenter (the EFE / tidal proxy) correlates POSITIVELY
                 with orbital eccentricity. Predicted amplitude ~19-28% hotter
                 for radial vs circular at matched pericenter (theta(0)~2..e).
H0 (MG/CDM):     Zero partial correlation of sigma with eccentricity at fixed
                 pericenter and mass.
Discriminating axis: Gaia DR3/EDR3 orbital ECCENTRICITY, measured per object.
Primary statistic:   partial Spearman rho(sigma_los, ecc | r_peri, mass-proxy)
                     on the diffuse carrier subset (and, separately, full sample).
Sign convention:     POSITIVE rho supports H1; ~0 or negative supports H0.
PRIME CONFOUND:      TIDAL HEATING. Radial plungers (small r_peri, high ecc) are
                     also tidally stirred -> also hotter -> MIMICS H1. CONTROL:
                     (a) restrict / regress on r_peri (and r_peri/r_tidal where
                         available) as a tidal proxy -- the prediction is the
                         RESIDUAL ecc-correlation AT FIXED pericenter;
                     (b) tides predict a DIFFERENT radial sigma profile + a host-
                         stripping morphology signature (separable w/ resolved
                         kinematics) -- flagged but not in this catalog;
                     (c) Crater II & Antlia II are the cleanest carriers: very
                         large r_peri (24, 38 kpc) so MINIMAL tidal heating, yet
                         non-circular (ecc 0.71, 0.56) -> tide-clean plunge test.
Both-ways honesty:   If the partial correlation vanishes once pericenter/mass are
                     controlled, report NULL. Do not manufacture a signal.
=================================================================================

SOURCES (per-value citations use these keys)
  [P22]  Pace, Erkal & Li 2022, ApJ 940, 136 (arXiv:2205.05699)
         - Table 1: r_h(arcmin), distance d(kpc), M_V, v_los, sigma_los, errors.
         - Table 3: r_peri, r_apo, ecc -- FIDUCIAL = MW+LMC potential ("LMC"),
                    plus the no-LMC ("nL") values. Gaia EDR3 proper motions.
         All sigma_los and ALL orbital params in this file are P22 (homogeneous,
         single-source -> minimizes cross-catalog systematics for the pilot).
  [S19]  Simon 2019, ARA&A 57, 375 -- ultra-faint dwarf review (consistency
         cross-check on sigma_los for UFDs; not the primary number here).
  [Mc12] McConnachie 2012, AJ 144, 4 -- Local Group compilation (cross-check).
  Cross-checks were consulted; the loaded numbers are P22 unless noted.

DERIVED:
  r_half[pc] = r_h[arcmin] * (pi/180/60) * d[kpc] * 1000   (azimuthally-averaged
              elliptical half-light; ellipticity from P22 not propagated here).
  dens_proxy = sigma_los^2 / r_half[pc]  (km^2/s^2/pc) -- crude central-density /
              internal-frequency proxy; LOW => diffuse => low omega_in => the
              non-adiabatic carrier regime the framework flags (omega_ext~omega_in
              reachable at pericenter). HIGH => dense => stays adiabatic (control).

CARRIER vs CONTROL classification (carrier=True): pre-specified on the PHYSICS,
not on sigma. A dwarf is a non-adiabatic CARRIER if it is DIFFUSE
(dens_proxy < ~0.02, i.e. very low internal frequency -- Crater II & Antlia II
sit ~25x below the classical-dwarf locus, matching Milgrom's own "omega_ex~omega_in
in some MW/M31 dwarfs" flag) AND on a non-circular orbit. Everything denser is an
adiabatic CONTROL (Fornax/Sculptor/Draco etc.). The diffuse-but-also-large-r_half
mid cases (Sextans, UMi, CVn I) are 'borderline' -- kept, flagged.
"""

# a0 footing (for any downstream y = omega_ext/omega_in / regime calc; not used to fit)
A0 = 9.36e-11          # m/s^2, c*H_Lambda/Z, pure-Lambda de Sitter
CH_LAMBDA = 5.42e-10   # m/s^2

import math
def _rhpc(arcmin, d_kpc):
    return arcmin * (math.pi / 180.0 / 60.0) * d_kpc * 1000.0

# -----------------------------------------------------------------------------
# DWARFS. ecc/peri/apo: '_lmc' = fiducial MW+LMC (P22 Table 3 cols rperi/rapo/ecc);
# '_nl' = no-LMC (P22 cols with superscript nL). sigma_los, sigma_err, r_h_arcmin,
# dist_kpc, M_V from P22 Table 1.
# -----------------------------------------------------------------------------
dwarfs = [
    # ===== NON-ADIABATIC CARRIERS (diffuse, low omega_in, non-circular) =====
    {
        "name": "Crater II",
        "sigma_los": 2.7, "sigma_err": 0.3,            # [P22] T1 (Caldwell+17/Fu+19)
        "r_h_arcmin": 31.2, "dist_kpc": 117.5, "M_V": -8.2,  # [P22] T1
        "ecc_lmc": 0.71, "r_peri_lmc": 24.0, "r_apo_lmc": 138.1,   # [P22] T3 (MW+LMC)
        "ecc_nl": 0.59,  "r_peri_nl": 35.8,  "r_apo_nl": 137.1,    # [P22] T3 (no-LMC)
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": True, "regime": "non-adiabatic",
        "confidence": "high",
        "note": "Prime carrier: extremely diffuse (huge r_half ~1.1 kpc, lowest "
                "dens_proxy), eccentric (0.71). Large r_peri=24kpc => TIDE-CLEAN. "
                "Source NATIVE table: a_ext/a0~0.46, y~2.6 NON-ADIABATIC.",
    },
    {
        "name": "Antlia II",
        "sigma_los": 5.71, "sigma_err": 1.08,          # [P22] T1 (Torrealba+19)
        "r_h_arcmin": 76.2, "dist_kpc": 132.0, "M_V": -9.03,
        "ecc_lmc": 0.56, "r_peri_lmc": 38.2, "r_apo_lmc": 137.2,
        "ecc_nl": 0.48,  "r_peri_nl": 50.7,  "r_apo_nl": 144.7,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": True, "regime": "non-adiabatic",
        "confidence": "high",
        "note": "Prime carrier: largest r_half (~2.9 kpc), low density, eccentric "
                "(0.56), r_peri=38kpc TIDE-CLEAN. Source NATIVE: a_ext/a0~0.35, "
                "y~2.5 NON-ADIABATIC.",
    },

    # ===== ADIABATIC CONTROLS (dense / compact) =====
    {
        "name": "Fornax",
        "sigma_los": 12.1, "sigma_err": 0.2,           # [P22] T1
        "r_h_arcmin": 19.9, "dist_kpc": 147.2, "M_V": -13.46,
        "ecc_lmc": 0.33, "r_peri_lmc": 76.7, "r_apo_lmc": 152.7,
        "ecc_nl": 0.31,  "r_peri_nl": 85.2,  "r_apo_nl": 160.0,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Dense control. Source NATIVE: y~0.20 ADIABATIC (stays "
                "cold-circular-like). Near-circular, large r_peri.",
    },
    {
        "name": "Sculptor",
        "sigma_los": 9.2, "sigma_err": 1.1,            # [P22] T1
        "r_h_arcmin": 11.17, "dist_kpc": 83.9, "M_V": -10.82,
        "ecc_lmc": 0.54, "r_peri_lmc": 44.9, "r_apo_lmc": 145.7,
        "ecc_nl": 0.32,  "r_peri_nl": 55.0,  "r_apo_nl": 105.3,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Dense control. NOTE ecc is LMC-sensitive (0.54 MW+LMC vs 0.32 "
                "no-LMC) -- carry both; do not over-read its eccentricity.",
    },
    {
        "name": "Draco",
        "sigma_los": 9.1, "sigma_err": 1.2,            # [P22] T1
        "r_h_arcmin": 9.67, "dist_kpc": 75.8, "M_V": -8.71,
        "ecc_lmc": 0.30, "r_peri_lmc": 58.0, "r_apo_lmc": 106.3,
        "ecc_nl": 0.41,  "r_peri_nl": 40.4,  "r_apo_nl": 95.6,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Dense control, near-circular, densest classical dwarf.",
    },
    {
        "name": "Carina",
        "sigma_los": 6.6, "sigma_err": 1.2,            # [P22] T1
        "r_h_arcmin": 10.1, "dist_kpc": 105.6, "M_V": -9.43,
        "ecc_lmc": 0.18, "r_peri_lmc": 77.9, "r_apo_lmc": 108.1,
        "ecc_nl": 0.10,  "r_peri_nl": 104.6, "r_apo_nl": 114.4,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Control: MOST circular classical dwarf (ecc 0.18) -- valuable "
                "low-ecc anchor. p_LMC=0.28.",
    },
    {
        "name": "Leo I",
        "sigma_los": 9.2, "sigma_err": 0.4,            # [P22] T1
        "r_h_arcmin": 3.65, "dist_kpc": 258.2, "M_V": -11.78,
        "ecc_lmc": 0.79, "r_peri_lmc": 47.5, "r_apo_lmc": 401.5,
        "ecc_nl": 0.86,  "r_peri_nl": 42.9,  "r_apo_nl": 532.8,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Control: dense+luminous but VERY high ecc (0.79). A high-ecc "
                "DENSE object => tests whether ecc-sigma signal is density-gated "
                "(framework: dense stays adiabatic, should NOT be hot-for-its-mass).",
    },
    {
        "name": "Leo II",
        "sigma_los": 7.4, "sigma_err": 0.4,            # [P22] T1
        "r_h_arcmin": 2.52, "dist_kpc": 233.0, "M_V": -9.74,
        "ecc_lmc": 0.58, "r_peri_lmc": 61.4, "r_apo_lmc": 230.0,
        "ecc_nl": 0.63,  "r_peri_nl": 54.3,  "r_apo_nl": 240.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "adiabatic",
        "confidence": "high",
        "note": "Dense control, compact.",
    },
    {
        "name": "Sextans",
        "sigma_los": 7.9, "sigma_err": 1.3,            # [P22] T1
        "r_h_arcmin": 16.5, "dist_kpc": 92.5, "M_V": -8.72,
        "ecc_lmc": 0.27, "r_peri_lmc": 82.2, "r_apo_lmc": 143.7,
        "ecc_nl": 0.41,  "r_peri_nl": 82.8,  "r_apo_nl": 196.4,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "high",
        "note": "Borderline: moderately diffuse (r_half ~0.44 kpc) but near-"
                "circular, large r_peri => stays adiabatic. Mid-density anchor.",
    },
    {
        "name": "Ursa Minor",
        "sigma_los": 8.6, "sigma_err": 0.3,            # [P22] T1
        "r_h_arcmin": 18.3, "dist_kpc": 76.2, "M_V": -9.03,
        "ecc_lmc": 0.29, "r_peri_lmc": 55.7, "r_apo_lmc": 99.8,
        "ecc_nl": 0.37,  "r_peri_nl": 41.8,  "r_apo_nl": 91.4,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "high",
        "note": "Borderline: extended (r_half ~0.41 kpc) but warm+near-circular.",
    },
    {
        "name": "Canes Venatici I",
        "sigma_los": 7.6, "sigma_err": 0.4,            # [P22] T1
        "r_h_arcmin": 7.12, "dist_kpc": 210.0, "M_V": -8.8,
        "ecc_lmc": 0.46, "r_peri_lmc": 84.5, "r_apo_lmc": 229.8,
        "ecc_nl": 0.58,  "r_peri_nl": 68.7,  "r_apo_nl": 256.5,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "high",
        "note": "Borderline: large r_peri (~85 kpc) => tide-clean but mid density.",
    },

    # ===== ULTRA-FAINTS (low-mass; faster internal omega; mostly controls/borderline) =====
    {
        "name": "Bootes I",
        "sigma_los": 4.6, "sigma_err": 0.7,            # [P22] T1
        "r_h_arcmin": 9.97, "dist_kpc": 66.0, "M_V": -6.02,
        "ecc_lmc": 0.31, "r_peri_lmc": 37.9, "r_apo_lmc": 71.7,
        "ecc_nl": 0.40,  "r_peri_nl": 35.3,  "r_apo_nl": 80.9,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "med",
        "note": "Source NATIVE flags y~0.57 BORDERLINE. Near-circular, small "
                "r_peri (~38kpc) => some tidal exposure; tidal-confound watch.",
    },
    {
        "name": "Hercules",
        "sigma_los": 5.1, "sigma_err": 0.9,            # [P22] T1 (elongated/tidal)
        "r_h_arcmin": 5.63, "dist_kpc": 130.6, "M_V": -5.83,
        "ecc_lmc": 0.60, "r_peri_lmc": 67.4, "r_apo_lmc": 253.8,
        "ecc_nl": 0.63,  "r_peri_nl": 56.8,  "r_apo_nl": 237.5,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "med",
        "note": "High ecc (0.60) UFD; known elongated/possibly tidally disrupting "
                "=> sigma may be tidally inflated (CONFOUND, flag low-med).",
    },
    {
        "name": "Tucana II",
        "sigma_los": 8.6, "sigma_err": 3.55,           # [P22] T1 (large err)
        "r_h_arcmin": 12.89, "dist_kpc": 58.0, "M_V": -3.8,
        "ecc_lmc": 0.45, "r_peri_lmc": 44.8, "r_apo_lmc": 114.4,
        "ecc_nl": 0.67,  "r_peri_nl": 35.6,  "r_apo_nl": 178.9,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "low",
        "note": "Extended low-lum UFD, but sigma very uncertain (8.6+/-3.55) and "
                "ecc LMC-sensitive (0.45 vs 0.67). Low confidence; keep, downweight.",
    },
    {
        "name": "Coma Berenices",
        "sigma_los": 4.6, "sigma_err": 0.8,            # [P22] T1
        "r_h_arcmin": 5.64, "dist_kpc": 42.0, "M_V": -4.38,
        "ecc_lmc": 0.23, "r_peri_lmc": 42.5, "r_apo_lmc": 68.1,
        "ecc_nl": 0.31,  "r_peri_nl": 42.4,  "r_apo_nl": 80.4,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "med",
        "note": "Compact, near-circular UFD control.",
    },
    {
        "name": "Ursa Major II",
        "sigma_los": 6.7, "sigma_err": 1.4,            # [P22] T1 (Simon&Geha; binary-corrected ~5.6 in S19)
        "r_h_arcmin": 13.8, "dist_kpc": 34.7, "M_V": -4.25,
        "ecc_lmc": 0.34, "r_peri_lmc": 41.4, "r_apo_lmc": 83.3,
        "ecc_nl": 0.44,  "r_peri_nl": 39.3,  "r_apo_nl": 102.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "low",
        "note": "Extended UFD but sigma inflated by binaries/tides; [S19] notes "
                "binary-corrected sigma ~5.6. Near-circular. Low confidence.",
    },
    {
        "name": "Canes Venatici II",
        "sigma_los": 4.6, "sigma_err": 0.8,            # [P22] T1
        "r_h_arcmin": 1.52, "dist_kpc": 160.0, "M_V": -5.17,
        "ecc_lmc": 0.66, "r_peri_lmc": 47.5, "r_apo_lmc": 234.0,
        "ecc_nl": 0.64,  "r_peri_nl": 46.0,  "r_apo_nl": 201.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "med",
        "note": "Compact high-ecc UFD; dense control.",
    },
    {
        "name": "Segue 1",
        "sigma_los": 3.7, "sigma_err": 1.25,           # [P22] T1
        "r_h_arcmin": 3.62, "dist_kpc": 23.0, "M_V": -1.3,
        "ecc_lmc": 0.44, "r_peri_lmc": 19.8, "r_apo_lmc": 47.9,
        "ecc_nl": 0.45,  "r_peri_nl": 19.5,  "r_apo_nl": 48.5,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "low",
        "note": "Tiny dense UFD, SMALL r_peri (~20kpc) => strong tidal exposure "
                "(CONFOUND). Densest object => adiabatic control by framework.",
    },
    {
        "name": "Carina II",
        "sigma_los": 3.4, "sigma_err": 1.0,            # [P22] T1
        "r_h_arcmin": 8.69, "dist_kpc": 37.4, "M_V": -4.57,
        "ecc_lmc": 0.72, "r_peri_lmc": 29.2, "r_apo_lmc": 176.0,
        "ecc_nl": 0.78,  "r_peri_nl": 28.9,  "r_apo_nl": 227.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "low",
        "note": "Likely LMC satellite (p_LMC=1.0); high ecc (0.72) but LMC-"
                "associated orbit => orbit interpretation murky. Downweight.",
    },
    {
        "name": "Aquarius II",
        "sigma_los": 5.4, "sigma_err": 2.15,           # [P22] T1
        "r_h_arcmin": 5.10, "dist_kpc": 107.9, "M_V": -4.36,
        "ecc_lmc": 0.49, "r_peri_lmc": 55.1, "r_apo_lmc": 145.9,
        "ecc_nl": 0.31,  "r_peri_nl": 77.9,  "r_apo_nl": 115.6,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "low",
        "note": "Diffuse-ish low-lum UFD but sigma very uncertain and ecc LMC-"
                "sensitive. Keep, downweight.",
    },
    {
        "name": "Leo IV",
        "sigma_los": 3.3, "sigma_err": 1.7,            # [P22] T1
        "r_h_arcmin": 2.54, "dist_kpc": 151.4, "M_V": -4.99,
        "ecc_lmc": 0.44, "r_peri_lmc": 66.8, "r_apo_lmc": 153.7,
        "ecc_nl": 0.38,  "r_peri_nl": 81.8,  "r_apo_nl": 153.7,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "low",
        "note": "Compact UFD, sigma uncertain. Control.",
    },
    {
        "name": "Leo V",
        "sigma_los": 3.2, "sigma_err": 1.55,           # [P22] T1
        "r_h_arcmin": 1.00, "dist_kpc": 169.0, "M_V": -4.4,
        "ecc_lmc": 0.35, "r_peri_lmc": 165.8, "r_apo_lmc": 189.1,
        "ecc_nl": 0.40,  "r_peri_nl": 137.9,  "r_apo_nl": None,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "low",
        "note": "Compact distant UFD, very large r_peri. Control.",
    },
    {
        "name": "Ursa Major I",
        "sigma_los": 7.0, "sigma_err": 1.0,            # [P22] T1
        "r_h_arcmin": 8.31, "dist_kpc": 97.3, "M_V": -5.13,
        "ecc_lmc": 0.35, "r_peri_lmc": 49.9, "r_apo_lmc": 103.5,
        "ecc_nl": 0.37,  "r_peri_nl": 46.5,  "r_apo_nl": 102.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "borderline",
        "confidence": "med",
        "note": "Extended UFD (elongated), near-circular. sigma may be tidally "
                "affected. Borderline.",
    },
    {
        "name": "Hydra II",
        "sigma_los": None, "sigma_err": None,          # [P22] T1: no resolved sigma
        "r_h_arcmin": None, "dist_kpc": 151.0, "M_V": None,
        "ecc_lmc": 0.56, "r_peri_lmc": 99.2, "r_apo_lmc": 237.3,
        "ecc_nl": 0.61,  "r_peri_nl": 80.4,  "r_apo_nl": 214.6,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "unknown",
        "confidence": "low",
        "note": "Orbit known but NO measured sigma_los in P22 -> sigma=None. "
                "Cannot enter the sigma test; listed for completeness.",
    },
    {
        "name": "Reticulum II",
        "sigma_los": 3.6, "sigma_err": 0.85,           # [P22] T1; S19/Minor cross-ref
        "r_h_arcmin": 6.30, "dist_kpc": 31.4, "M_V": -3.1,
        "ecc_lmc": 0.28, "r_peri_lmc": 37.0, "r_apo_lmc": 69.6,
        "ecc_nl": 0.36,  "r_peri_nl": 25.3,  "r_apo_nl": 52.7,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "control",
        "confidence": "low",
        "note": "LMC-associated (p_LMC=0.96), near-circular compact UFD. Control. "
                "Orbit murky due to LMC tie.",
    },
    {
        "name": "Triangulum II",
        "sigma_los": None, "sigma_err": None,          # [P22] T1: no robust sigma (upper limit only)
        "r_h_arcmin": 2.50, "dist_kpc": 28.4, "M_V": -1.6,
        "ecc_lmc": 0.75, "r_peri_lmc": 12.2, "r_apo_lmc": 85.6,
        "ecc_nl": 0.78,  "r_peri_nl": 12.6,  "r_apo_nl": 100.1,
        "M_star_Msun": None, "M_dyn_Msun": None,
        "r_tidal_kpc": None, "r_peri_over_r_tidal": None,
        "carrier": False, "regime": "unknown",
        "confidence": "low",
        "note": "Very high ecc (0.75) + tiny r_peri (12kpc, strong tides) but "
                "sigma is only an upper limit -> None. Cannot enter test.",
    },
]

# -----------------------------------------------------------------------------
# Fill derived fields (r_half_pc, dens_proxy) where inputs exist.
# -----------------------------------------------------------------------------
for d in dwarfs:
    if d["r_h_arcmin"] is not None and d["dist_kpc"] is not None:
        d["r_half_pc"] = round(_rhpc(d["r_h_arcmin"], d["dist_kpc"]), 1)
    else:
        d["r_half_pc"] = None
    if d["sigma_los"] is not None and d["r_half_pc"]:
        d["dens_proxy"] = round(d["sigma_los"] ** 2 / d["r_half_pc"], 4)
    else:
        d["dens_proxy"] = None


def usable_for_test():
    """Dwarfs with BOTH a measured sigma AND an eccentricity -> enter the test."""
    return [d for d in dwarfs
            if d["sigma_los"] is not None and d["ecc_lmc"] is not None]


def carriers():
    return [d for d in dwarfs if d["carrier"]]


def controls():
    return [d for d in dwarfs if not d["carrier"] and d["regime"] != "unknown"]


if __name__ == "__main__":
    use = usable_for_test()
    sig = [d["sigma_los"] for d in use]
    ecc = [d["ecc_lmc"] for d in use]
    print(f"Total dwarfs listed : {len(dwarfs)}")
    print(f"Usable (sigma & ecc): {len(use)}")
    print(f"sigma_los range     : {min(sig):.1f} - {max(sig):.1f} km/s")
    print(f"ecc (MW+LMC) range  : {min(ecc):.2f} - {max(ecc):.2f}")
    print(f"Carriers            : {[d['name'] for d in carriers()]}")
    print(f"Controls (regime)   :")
    for d in dwarfs:
        flag = "CARRIER" if d["carrier"] else d["regime"].upper()
        print(f"  {d['name']:20s} sig={str(d['sigma_los']):5s} "
              f"ecc={str(d['ecc_lmc']):4s} peri={str(d['r_peri_lmc']):6s} "
              f"r_half={str(d['r_half_pc']):7s}pc dens={str(d['dens_proxy']):7s} "
              f"[{d['confidence']}] {flag}")
