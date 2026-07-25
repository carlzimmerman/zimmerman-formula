#!/usr/bin/env python3
"""
archive_inventory_d2_2026.py -- D-2 ARCHIVE CHECK: is the z~2 DEC-vs-RISE a0(z) measurement
ALREADY TAKEN?  A real, citable inventory of JWST + ALMA/PdBI archival holdings on LENSED
low-mass rotators at z = 1.5-2.5, with the framework's own g_bar/a0 and dilution lever
computed for every object where the published data permit it.
==============================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework: a0 = c H_Lambda / Z,
Z = sqrt(32 pi/3) = 5.78881, canonical a0(0) = 9.355e-11 m/s^2 (alt footing cH0/Z = 1.1305e-10);
NOTE for the archivist: the committed parent a0z_fork_likelihood_2026.py has a DOCSTRING typo
("Z = ... = 5.7863"); its CODE computes np.sqrt(32*np.pi/3) = 5.78881 correctly, so no result
anywhere is affected.  Recorded here so the number is not propagated further.
its OWN interpolation g_obs = sqrt(g_bar^2 + g_bar a0)  <=>  the EXACT a0-line
      E := g_obs^2 - g_bar^2 = a0 * g_bar .
nu = sqrt(1+1/y) is Milgrom 1999 (PLA 253:273 Eq.9) -- WELLHEAD CREDIT; the framework's
distinctive content is the cH_Lambda/Z coefficient + the MI completion.  McCulloch (MiHsC)
credited for the rising Hubble-horizon branch.  a0's VALUE and the HORIZON CHOICE are POSITS.
No TOE.  No "theory closed".  Exit 0 = the inventory ran, NOT a verdict on the theory.

ROLE IN THE THREE-QUESTION DESIGN (D-1 targets / D-2 archive / D-3 error budget): this file is
D-2 ONLY.  It does NOT recompute the systematic floor (that is D-3) and it does NOT invent
targets (that is D-1).  It answers exactly one question: DOES THE ARCHIVE ALREADY CONTAIN,
TODAY, a sample that can measure a0 at z~2 to the two bars set by the committed parents?

THE TWO BARS (from the committed parents; the a0(z)/a0(0) RATIO is FOOTING-INDEPENDENT, so
both bars are identical under cH_Lambda/Z and cH0/Z):
   desitter_unruh_horizon_fork_2026.py : DEC = sqrt(rho_DE) -> 0.874 @ z=2 ; RISE = E(z) ->
       3.005 @ z=2 ; ratio 3.44x ; a CRUDE ~37% a0 precision separates them at 3 sigma.
   a0z_fork_likelihood_2026.py        : a PRIOR-ROBUST 20:1 Bayes factor on DEC-vs-RISE needs
       sigma(a0) ~ 10.9% at z=2 ; and the framework-DERIVED dilution lever L = 1/(1+2y),
       y = g_bar/a0, is why massive HSB samples are non-diagnostic (L=0.126 Ubler z=2.3,
       L=0.078 Amvrosiadis) while near-a0 lensed samples are (L=0.477 Jeanneau, 0.671 Big Wheel).
   highz_a0_fork_confront_2026.py     : the decisive spec is z~2-3, DEEP-MOND-SELECTED
       g_bar < 0.3 a0, N ~ 15-40, and NO current sample meets the g_bar < 0.3 a0 cut.
ESTIMATOR PRE-REGISTRATION (estimator_bias_mocks.py, resolved): any a0 estimator used here or
downstream must be MEDIAN-LIKE.  GLS is biased HIGH by >= 10.3 pp and is BANNED.  This file
therefore reports MEDIANS of the per-object y = g_bar/a0 distributions, never a GLS mean.

HONESTY RAILS (a manufactured "the archive already has it" and a manufactured "the archive has
nothing" are penalized EQUALLY):
 * Every program, survey and object below is REAL and citable; each carries its arXiv/DOI/ALMA
   project code.  Anything I could not verify from a primary source is tagged CANDIDATE-TO-CHECK
   and is EXCLUDED from the verdict arithmetic.
 * The GAS side is not waved away as "hard": the actual archival CO/[CII] detections and
   UPPER LIMITS are tabulated with their alpha_CO, and the upper limits are counted as
   NON-detections, not quietly promoted.
 * The KINEMATICS side is not waved away either: lensed AO/IFU Halpha kinematics at z~2 DO
   exist in quantity (~60-90 objects across 5 real samples).  The gap is stated precisely --
   it is NOT "no data", it is "no OVERLAP + no deep-MOND radii + no gas masses".
 * Spectral-resolution gates are computed from published instrument specs, and the distinction
   between LINE-WIDTH resolution (sigma_inst) and VELOCITY-CENTROID precision
   (~sigma_inst / SNR) is made explicitly, so a low-R mode is not dismissed by conflating them.
"""
import numpy as np

np.seterr(all="ignore")
BAR = "=" * 104

# ---------------------------------------------------------------- framework constants
Z_CONST = np.sqrt(32 * np.pi / 3)
A0_CAN, A0_ALT = 9.355e-11, 1.1305e-10        # canonical cH_Lambda/Z ; alt cH0/Z
G = 6.674e-11
MSUN = 1.98892e30
KPC = 3.0857e19
CKMS = 299792.458

# the two bars, and the fork at z=2 (footing-independent ratio; see the committed parents)
DEC_Z2, RISE_Z2 = 0.874, 3.005
BAR_3SIG = 0.37          # ~37% a0 precision at z=2 -> 3 sigma DEC-vs-RISE mechanism call
BAR_20TO1 = 0.109        # ~10.9% -> prior-robust 20:1 Bayes factor DEC-vs-RISE
DEEP_MOND_CUT = 0.30     # the decisive selection: g_bar < 0.3 a0

print(BAR)
print("D-2 ARCHIVE CHECK -- does a usable z~1.5-2.5 LENSED deep-MOND a0(z) sample exist TODAY?")
print(BAR)
print(f"  a0 = c H_Lambda / Z,  Z = {Z_CONST:.4f};  canonical a0(0) = {A0_CAN:.3e} m/s^2, "
      f"alt = {A0_ALT:.3e}.")
print(f"  Fork at z=2 (footing-INDEPENDENT ratio): DEC={DEC_Z2:.3f}  RISE={RISE_Z2:.3f}  "
      f"-> {RISE_Z2/DEC_Z2:.2f}x apart.")
print(f"  BAR-A (3 sigma mechanism call)      : sigma(a0)/a0 <= {100*BAR_3SIG:.0f}%")
print(f"  BAR-B (prior-robust 20:1 Bayes)     : sigma(a0)/a0 <= {100*BAR_20TO1:.1f}%")
print(f"  SELECTION the parents require       : g_bar < {DEEP_MOND_CUT} a0  (deep-MOND, lever L -> 1)")
print("  ESTIMATOR PRE-REGISTERED: MEDIAN-LIKE only.  GLS is BANNED (biased high >= 10.3 pp).")


def lever(y):
    """Framework-DERIVED bTFR/mass-axis a0-lever L = 1/(1+2y), y = g_bar/a0 (deep-MOND -> 1)."""
    return 1.0 / (1.0 + 2.0 * y)


def g_bar_of(M_bar_msun, R_kpc):
    """Newtonian baryonic acceleration at radius R (point-mass proxy; ~20% of a thin-disk
    value at 2.2 R_d -- adequate for a REGIME classification, which is all D-2 needs)."""
    return G * M_bar_msun * MSUN / (R_kpc * KPC) ** 2


def R_at_y(M_bar_msun, y, a0=A0_CAN):
    """Radius (kpc) at which g_bar = y * a0 for a given baryonic mass."""
    return np.sqrt(G * M_bar_msun * MSUN / (y * a0)) / KPC


def v_framework(M_bar_msun, R_kpc, a0=A0_CAN):
    """Framework's OWN prediction: g_obs = sqrt(g_bar^2 + g_bar a0)  ->  V = sqrt(R g_obs)."""
    gb = g_bar_of(M_bar_msun, R_kpc)
    go = np.sqrt(gb ** 2 + gb * a0)
    return np.sqrt(R_kpc * KPC * go) / 1e3          # km/s


# ==========================================================================================
# 1. SPECTRAL-RESOLUTION AND WAVELENGTH GATES -- which archival MODES can do kinematics at all
# ==========================================================================================
print("\n" + BAR)
print("1. INSTRUMENT GATES -- which archival spectroscopic MODES can even do z~2 kinematics")
print(BAR)
# Published specs: NIRSpec prism R~100; NIRISS GR150 WFSS R~150 (0.8-2.2 um, JDox);
# NIRSpec medium gratings R~1000, high-res R~2700 (JDox; Rigby+2024 ApJ TEMPLATES);
# NIRCam WFSS R~1600 over 2.4-5.0 um (JDox); KMOS YJ/H/K R~3400/4000/4200 (ESO);
# Keck OSIRIS R~3600; MUSE 0.465-0.93 um R~1770-3590 (ESO).
MODES = [
    # name, R, lambda_min_um, lambda_max_um, note
    ("NIRSpec PRISM (MSA)          ", 100, 0.60, 5.30, "CANUCS/UNCOVER workhorse"),
    ("NIRISS GR150 WFSS            ", 150, 0.80, 2.20, "CANUCS/GLASS grism"),
    ("NIRCam WFSS (grism)          ", 1600, 2.40, 5.00, "MAGNIF / ALT"),
    ("NIRSpec medium gratings      ", 1000, 0.70, 5.30, "M gratings"),
    ("NIRSpec HIGH-RES gratings    ", 2700, 0.70, 5.30, "TEMPLATES LBGs; IFU or MSA"),
    ("VLT/KMOS YJ,H,K              ", 4000, 0.80, 2.50, "KLASS/KLEVER/KLENS (seeing-limited)"),
    ("Keck OSIRIS + LGS-AO         ", 3600, 1.00, 2.40, "Leethochawalit+16 / OLAS"),
    ("VLT/MUSE                     ", 2500, 0.465, 0.93, "MUSE-DARK (Jeanneau) -- z ceiling"),
]
HA_REST, OII_REST, PAB_REST = 0.65628, 0.37275, 1.28215      # um
ZLO, ZHI = 1.5, 2.5
print(f"  Kinematics need a line inside the mode's band AND enough R.  Window z={ZLO}-{ZHI}:")
print(f"    H-alpha  observed {HA_REST*(1+ZLO):.2f}-{HA_REST*(1+ZHI):.2f} um")
print(f"    [OII]    observed {OII_REST*(1+ZLO):.2f}-{OII_REST*(1+ZHI):.2f} um")
print(f"    Pa-beta  observed {PAB_REST*(1+ZLO):.2f}-{PAB_REST*(1+ZHI):.2f} um")
print(f"\n  {'mode':30} {'R':>6} {'sig_inst':>10} {'centroid@S/N=10':>16} {'Ha in band':>11} "
      f"{'KIN-CAPABLE':>12}  note")
print("       (sig_inst and centroid in km/s)")
print("  " + "-" * 112)
gate_rows = []
for name, R, lo, hi, note in MODES:
    sig_inst = CKMS / (2.355 * R)                  # FWHM->sigma conversion of the LSF
    cen10 = sig_inst / 10.0                        # centroid ~ sigma_inst/SNR (photon limit)
    ha_ok = (lo <= HA_REST * (1 + ZLO)) and (HA_REST * (1 + ZHI) <= hi)
    ha_part = (lo <= HA_REST * (1 + ZHI)) and (hi >= HA_REST * (1 + ZLO))
    tag = "FULL" if ha_ok else ("partial" if ha_part else "NO")
    # kinematics-capable at z=1.5-2.5 requires BOTH gates: line in band AND R >= 1000
    kin = "YES" if (ha_ok and R >= 1000) else "no"
    gate_rows.append((name.strip(), R, sig_inst, cen10, tag, kin))
    print(f"  {name:30} {R:>6d} {sig_inst:>10.0f} {cen10:>16.1f} {tag:>11} {kin:>12}  {note}")
print("\n  HONEST READING (both directions):")
print("   * sigma_inst is the LINE-WIDTH floor; the VELOCITY CENTROID goes as ~sigma_inst/SNR,")
print("     so a moderate-R mode is NOT automatically disqualified.  R~1600 grism at SNR=10")
print(f"     gives ~{CKMS/(2.355*1600)/10:.0f} km/s centroids -- usable in principle.")
print("   * BUT the published grism-kinematics demonstration (MAGNIF, arXiv:2310.09327) returned")
print("     v_rot = 58 (+53/-35) km/s, i.e. ~+91%/-60% -- because a slitless 2D spectrum")
print("     degenerately mixes morphology with velocity.  Grism kinematics is REAL but coarse.")
print("   * DECISIVE gate for the z=1.5-2.5 window: NIRCam WFSS (2.4-5.0 um) CANNOT see H-alpha")
print(f"     until z > {2.40/HA_REST - 1:.2f}; NIRISS WFSS and NIRSpec PRISM have R <= 150, i.e.")
print("     sigma_inst >= 850 km/s, so even at SNR=10 the centroid floor is ~85 km/s -- larger")
print("     than the ENTIRE rotation signal of a low-mass z~2 rotator.  MUSE cannot reach the")
print(f"     window at all: its red cutoff puts [OII] at z <= {0.93/OII_REST - 1:.2f}.")
print("   => at z=1.5-2.5 only NIRSpec R>=1000 (IFU or MSA slit-stepping) and ground-based")
print("      near-IR IFUs (KMOS seeing-limited, OSIRIS/ERIS AO) are kinematics-capable.")

# ==========================================================================================
# 2. THE KINEMATICS SIDE OF THE ARCHIVE (JWST first, then ground-based lensed IFU)
# ==========================================================================================
# fields: label, instrument/mode, N, z range, lensed?, logM* range, in-window N (1.5-2.5),
#         gas mass available?, RC reaches deep-MOND?, citation
KIN = [
    dict(lab="TEMPLATES ERS 1355", inst="NIRSpec IFU R~2700 (2 LBGs) / R~1000 (2 DSFGs)",
         N=4, zr="1.329, 2.925, 3.760, 4.225", lensed=True, logM="8.77-10.79",
         nwin=0, gas="SPT0418 only ([CII], massive)", deep="no (2 LBGs bracket the window)",
         cite="Rigby+2024 ApJ 976:78 doi:10.3847/1538-4357/ad7501 ; STScI ERS 1355",
         note="mu = 52.7 / 95 / 6.6 / 29.5 ; M* = 5.95e8, 1.46e9, 6.1e10, 1.53e10. "
              "The two HIGH-R lensed LBGs sit at z=1.329 and z=2.925 -- they BRACKET "
              "1.5<z<2.5 and land in neither."),
    dict(lab="MSA-3D (Cycle 1)", inst="NIRSpec MSA slit-stepping -> IFS cubes",
         N=30, zr="0.5-1.7", lensed=False, logM="~9-11", nwin=3,
         gas="no CO; SED/scaling only", deep="no (HSB, rotation-selected, NOT lensed)",
         cite="Espejo Salcedo+2026 arXiv:2606.27853 (30 SFGs; 23 'golden')",
         note="This is compilation point [1].  NOT lensed, so no magnification lever; "
              "only the z=1.68 tail enters the window."),
    dict(lab="CANUCS GTO 1208", inst="NIRISS WFSS R~150 + NIRSpec MSA PRISM R~100",
         N=0, zr="0.2-9 (5 clusters)", lensed=True, logM="7-11", nwin=0,
         gas="no", deep="no -- resolution gate fails",
         cite="STScI GO/GTO 1208 (Willott); CANUCS DR1 arXiv:2506.21685",
         note="A370, MACS0416, MACS0417, MACS1149, MACS1423.  Medium-resolution MSA exists "
              "ONLY in the MACS1149 FLANKING field, i.e. not on the strongly lensed arcs. "
              "R<=150 => sigma_inst >= 850 km/s: NO kinematics."),
    dict(lab="UNCOVER GO 2561", inst="NIRSpec MSA PRISM R~100 (~700 targets) + NIRCam",
         N=0, zr="0.3-13 (A2744)", lensed=True, logM="6-11", nwin=0,
         gas="no", deep="no -- resolution gate fails",
         cite="UNCOVER treasury (Bezanson/Labbe); see e.g. arXiv:2409.11457",
         note="Prism only: R~100.  Superb redshifts and masses, ZERO kinematic power."),
    dict(lab="GLASS-JWST ERS 1324", inst="NIRISS WFSS R~150 + NIRSpec MSA + NIRCam",
         N=0, zr="0.3-9 (A2744)", lensed=True, logM="7-11", nwin=0,
         gas="no", deep="no -- resolution gate fails",
         cite="Treu+2022 ApJ 935:110 ; GLASS-JWST ERS 1324",
         note="Same gate as CANUCS."),
    dict(lab="MAGNIF GO 2883", inst="NIRCam WFSS R~1600, medium bands, Frontier Fields",
         N=0, zr="4.5, 6.3 (Ha); z=8.34 disk", lensed=True, logM="7-10", nwin=0,
         gas="no", deep="no -- H-alpha out of band below z=2.66",
         cite="Sun+ MAGNIF, arXiv:2503.03829 ; lensed z=8.34 disk arXiv:2310.09327",
         note="Proves grism dynamical modelling works (v_rot=58 +53/-35 km/s) but the "
              "2.4-5.0 um band cannot see H-alpha in the z=1.5-2.5 window."),
    dict(lab="ALT GO 3516", inst="NIRCam grism R~1600 (A2744)",
         N=0, zr="0.2-8.5 (1630 sources)", lensed=True, logM="<8.5 for 1015 objects", nwin=0,
         gas="no", deep="no kinematics derived",
         cite="Naidu, Matthee+ 'All the Little Things', arXiv:2410.01874",
         note="THE lensed-DWARF CATALOG: 1015 sources less massive than the SMC. A target "
              "list, not a kinematic dataset.  Feeds D-1, not D-2."),
    dict(lab="Leethochawalit+2016", inst="Keck OSIRIS + LGS-AO IFU (R~3600)",
         N=15, zr="~1.2-2.4 (mean z~2)", lensed=True, logM="~9.0-9.6", nwin=12,
         gas="NO", deep="no -- Ha extent ~ few kpc, not the outer disk",
         cite="Leethochawalit+2016 ApJ 820:84 (arXiv:1509.01279)",
         note="CSWA11/15/19/20/28/31/128/139/159/165, Abell773, J0744, J1038, J1148, J1206. "
              "mu = 1.9-42.  ~45% show ordered rotation.  NO gas masses."),
    dict(lab="OLAS I (Hirtenstein+2019)", inst="Keck OSIRIS + AO IFU",
         N=17, zr="1.2-2.3", lensed=True, logM="8.0-9.8", nwin=13,
         gas="NO", deep="no -- integrated sigma + gradients, no extended RCs",
         cite="Hirtenstein+2019 ApJ 880:54 doi:10.3847/1538-4357/ab113e",
         note="mu = 1.52-20.2; integrated sigma ~34-105 km/s.  The paper does NOT present "
              "extended rotation curves.  NO gas masses."),
    dict(lab="KLASS (Girard+2020)", inst="VLT/KMOS seeing-limited IFU (~0.6\")",
         N=44, zr="0.6-2.3", lensed=True, logM="8.1-11.0 (median 9.5)", nwin=15,
         gas="SED-derived only", deep="no -- V/sigma median ~2.5",
         cite="Girard+2020 MNRAS 497:173 doi:10.1093/mnras/staa1907 (arXiv:2006.14633)",
         note="6 clusters (A2744, MACS0416, MACS1149, MACS2129, RXJ1347, RXJ2248). "
              "CANDIDATE-TO-CHECK: the kinematic subsample appears to restrict to LOW "
              "magnification (mu <~ 5) to avoid shear/differential magnification -- i.e. "
              "the magnification lever is deliberately NOT used."),
    dict(lab="KLEVER (Curti+2020)", inst="VLT/KMOS YJ+H+K (R~3400-4200), seeing-limited",
         N=35, zr="1.2-2.5 (lensed subsample of ~200)", lensed=True, logM="~9-10.5", nwin=30,
         gas="NO", deep="no -- seeing-limited, metallicity-focused",
         cite="Curti+2020 MNRAS 492:821 doi:10.1093/mnras/stz3379 (arXiv:1910.13451)",
         note="CLASH + Frontier Fields lensed arcs.  The largest z~2 LENSED resolved-"
              "spectroscopy sample in the archive; published products are metallicity "
              "maps/gradients, not deep-MOND rotation curves."),
    dict(lab="ALMA-ALPAKA", inst="ALMA CO/[CI] high-res (3DBAROLO RCs)",
         N=28, zr="0.5-3.5", lensed=False, logM=">10.4 (massive)", nwin=9,
         gas="YES (that is the tracer)", deep="NO -- massive HSB, g_bar >> a0",
         cite="Rizzo+2023 A&A 679:A129 (ALMA-ALPAKA I)",
         note="This is the shape of what EXISTS: excellent cold-gas RCs, wrong regime."),
    dict(lab="Lelli+2023 cold disks", inst="ALMA CO multi-J, z~1.5-2.2",
         N=2, zr="1.47, 2.24", lensed=False, logM="~11 (massive MS)", nwin=2,
         gas="YES", deep="NO -- massive; flat RC to 8 kpc, sigma_CO <~ 15 km/s",
         cite="Lelli+2023 A&A 672:A106 (arXiv:2302.00030)",
         note="Key for D-3, not D-2: COLD tracers at cosmic noon really do reach "
              "sigma <~ 15 km/s, far below warm-ionized 45-60 km/s."),
]
print("\n" + BAR)
print("2. KINEMATICS SIDE OF THE ARCHIVE (z=1.5-2.5 relevance).  'nwin' = objects in window")
print(BAR)
print(f"  {'sample / program':26} {'N':>4} {'nwin':>5} {'lensed':>7} {'logM*':>16} "
      f"{'gas mass?':>26} deep-MOND RC?")
print("  " + "-" * 102)
for k in KIN:
    print(f"  {k['lab']:26} {k['N']:>4d} {k['nwin']:>5d} {str(k['lensed']):>7} "
          f"{k['logM']:>16} {k['gas']:>26} {k['deep']}")
n_lensed_win = sum(k["nwin"] for k in KIN if k["lensed"] and k["N"] > 0)
n_deep = sum(k["nwin"] for k in KIN if k["deep"].lower().startswith("yes"))
print("  " + "-" * 102)
print(f"  LENSED objects with SOME resolved kinematics in 1.5<z<2.5 : ~{n_lensed_win}")
print(f"  ... of which a published RC reaches the deep-MOND regime  :  {n_deep}")
print("\n  Provenance (every row REAL and citable):")
for k in KIN:
    print(f"    {k['lab']:26} {k['inst']}")
    print(f"    {'':26} {k['cite']}")
    print(f"    {'':26} {k['note']}")

# ==========================================================================================
# 3. THE GAS SIDE OF THE ARCHIVE (ALMA / PdBI): M_gas is MANDATORY -- both the deep-MOND cut
#    and g_bar need it, and at z>0.5 HI is inaccessible (hence the SKA2/ngVLA endgame).
# ==========================================================================================
# Verified from primary sources.  M_mol in Msun, alpha_CO stated.  det=True -> detection.
GAS = [
    dict(name="MACS0451-arc", z=2.013, mu=49.0, Mstar=2.5e9, Mgas=4.0e9, det=True,
         line="CO(3-2) 4-5 sigma", res=False, fac="IRAM PdBI",
         cite="Dessauges-Zavadsky+2015 A&A 577:A50 (arXiv:1408.0816), Tab.1/Tab.3",
         extra="alpha_CO=4.36 (Galactic). [CII] ALSO detected, ALMA 2011.0.00130.S "
               "(arXiv:1502.03842) -- COMPACT/unresolved. Ha KINEMATICS EXIST: Jones+2010 "
               "MNRAS 404:1247, ~60 pc source-plane res, dv_pp = 80 +/- 20 km/s."),
    dict(name="A68-C0", z=1.5864, mu=30.0, Mstar=2.0e10, Mgas=2.6e10, det=True,
         line="CO(2-1) 11 sigma", res=False, fac="IRAM PdBI",
         cite="Dessauges-Zavadsky+2015 A&A 577:A50", extra="alpha_CO=4.36; UNRESOLVED."),
    dict(name="A68-HLS115", z=1.5869, mu=15.0, Mstar=9.6e9, Mgas=2.4e10, det=True,
         line="CO(2-1) 14 sigma", res=False, fac="IRAM PdBI",
         cite="Dessauges-Zavadsky+2015 A&A 577:A50", extra="alpha_CO=4.36; UNRESOLVED."),
    dict(name="A68-h7", z=2.15, mu=3.0, Mstar=8.7e10, Mgas=7.4e10, det=True,
         line="CO(3-2) 3-4 sigma", res=False, fac="IRAM 30m (single dish)",
         cite="Dessauges-Zavadsky+2015 A&A 577:A50", extra="massive; single-dish, no imaging."),
    dict(name="SGAS J0033 (D-Z+24)", z=2.225, mu=27.9, Mstar=10 ** 9.81, Mgas=4.0e9, det=True,
         line="CO(3-2)", res=False, fac="ALMA ACA (compact array)",
         cite="Dessauges-Zavadsky+2024 A&A (aa51892-24), Tab.1; ALMA 2018.1.01142.S, "
              "2021.2.00092.S, 2022.1.00916.S",
         extra="the ONLY CO DETECTION in the whole 12-arc low-mass lensed sample that lands "
               "inside 1.5<z<2.5.  ACA => spatially UNRESOLVED by construction."),
    dict(name="SGAS J0837 (D-Z+24)", z=2.385, mu=22.1, Mstar=10 ** 9.26, Mgas=1.2e9, det=False,
         line="CO(3-2) UPPER LIMIT", res=False, fac="ALMA ACA",
         cite="Dessauges-Zavadsky+2024 A&A (aa51892-24), Tab.1", extra="non-detection."),
    dict(name="SGAS J1429 (D-Z+24)", z=1.905, mu=8.6, Mstar=10 ** 9.58, Mgas=1.5e9, det=False,
         line="CO(3-2) UPPER LIMIT", res=False, fac="ALMA ACA",
         cite="Dessauges-Zavadsky+2024 A&A (aa51892-24), Tab.1", extra="non-detection."),
    dict(name="A2218-Mult", z=3.104, mu=14.0, Mstar=np.nan, Mgas=1.7e10, det=False,
         line="CO(3-2) UPPER LIMIT", res=False, fac="IRAM PdBI",
         cite="Dessauges-Zavadsky+2015 A&A 577:A50", extra="out of window (z=3.1)."),
]
print("\n" + BAR)
print("3. GAS SIDE OF THE ARCHIVE -- lensed, M*<~1e10.5, CO/[CII] at cosmic noon")
print(BAR)
print(f"  {'object':22} {'z':>6} {'mu':>6} {'M*':>10} {'M_gas':>10} {'det?':>5} "
      f"{'resolved?':>10}  facility / line")
print("  " + "-" * 102)
for g in GAS:
    ms = "n/a" if not np.isfinite(g["Mstar"]) else f"{g['Mstar']:.2e}"
    print(f"  {g['name']:22} {g['z']:>6.3f} {g['mu']:>6.1f} {ms:>10} {g['Mgas']:>10.2e} "
          f"{('YES' if g['det'] else 'LIMIT'):>5} {('yes' if g['res'] else 'NO'):>10}  "
          f"{g['fac']} {g['line']}")
in_win_det = [g for g in GAS if g["det"] and ZLO <= g["z"] <= ZHI]
in_win_low = [g for g in in_win_det if np.isfinite(g["Mstar"]) and g["Mstar"] < 1e10]
print("  " + "-" * 102)
print(f"  CO/[CII] DETECTIONS inside 1.5<z<2.5 on LENSED targets            : {len(in_win_det)}")
print(f"  ... with M* < 1e10 (the low-mass / deep-MOND-capable regime)     : {len(in_win_low)}"
      f"  ({', '.join(g['name'] for g in in_win_low)})")
print(f"  ... SPATIALLY RESOLVED (needed for a gas velocity field)         : "
      f"{sum(1 for g in GAS if g['res'])}")
print("\n  BLIND-SURVEY CROSS-CHECK (the strongest single archive statement):")
print("    ALMA Lensing Cluster Survey (ALCS), 33 massive clusters, the LARGEST-AREA ALMA")
print("    cluster survey: the blind line search yields SEVEN line emitters total -- FOUR CO")
print("    emitters at z=0.8-1.1 (three of which are multiple images of the SAME galaxy) and")
print("    ONE [CII] at z=6.071.  => ZERO blind CO detections in 1.5<z<2.5.")
print("    Nagao+2026 ApJ 998:42 doi:10.3847/1538-4357/ae2472 (arXiv:2511.20748);")
print("    ALCS = ALMA 2018.1.00035.L (PI Kohno) + archival.")
print("\n  Provenance:")
for g in GAS:
    print(f"    {g['name']:22} {g['cite']}")
    print(f"    {'':22} {g['extra']}")

# ==========================================================================================
# 4. THE CROSS-MATCH -- which archival objects have BOTH resolved kinematics AND a gas mass?
# ==========================================================================================
print("\n" + BAR)
print("4. THE CROSS-MATCH: lensed + z in [1.5,2.5] + resolved kinematics + a GAS MASS")
print(BAR)
BOTH = [g for g in GAS if g["det"] and ZLO <= g["z"] <= ZHI
        and "KINEMATICS EXIST" in g["extra"]]
print(f"  Objects satisfying ALL FOUR requirements simultaneously: N = {len(BOTH)}")
for g in BOTH:
    print(f"    -> {g['name']} (z={g['z']}, mu={g['mu']:.0f}, M*={g['Mstar']:.2e}, "
          f"M_gas={g['Mgas']:.2e})")
print("\n  Why the two sides do not overlap (stated precisely, not hand-waved):")
print("   * The KINEMATICS samples are drawn from CASSOWARY/CLASH/Frontier-Field ARC catalogs")
print("     selected on rest-UV/optical brightness (Leethochawalit, OLAS, KLASS, KLEVER).")
print("   * The GAS samples are drawn from Herschel-Lensing-Survey IR/submm detections and")
print("     SGAS arcs selected for CO feasibility (Dessauges-Zavadsky 2015/2024).")
print("   * Those two selections are nearly DISJOINT: IR-bright enough for CO at M*<1e10 and")
print("     UV-bright enough for AO Ha are different objects.  One historical exception exists")
print("     -- the MACS0451 arc -- because it is both extremely magnified (mu~49) and")
print("     IR-detected by Herschel.")

# ==========================================================================================
# 5. FOR THE ONE OBJECT THAT HAS BOTH: does it reach the deep-MOND cut g_bar < 0.3 a0?
# ==========================================================================================
print("\n" + BAR)
print("5. THE N=1 CANDIDATE, TESTED AGAINST THE PARENTS' OWN SELECTION CUT")
print(BAR)
obj = BOTH[0]
Mbar = obj["Mstar"] + obj["Mgas"]        # alpha_CO=4.36 already includes He
print(f"  {obj['name']}: z={obj['z']}, mu={obj['mu']:.0f}, M*={obj['Mstar']:.2e}, "
      f"M_gas={obj['Mgas']:.2e} -> M_bar={Mbar:.2e} Msun (f_gas={obj['Mgas']/Mbar:.2f})")
R_ARCH = [1.0, 2.0, 3.0]     # the radii the PUBLISHED Ha kinematics actually cover ("a few kpc")
print(f"  {'R [kpc]':>9} {'g_bar [m/s^2]':>15} {'y=g_bar/a0':>12} {'lever L':>9} "
      f"{'V_fw [km/s]':>11}     regime")
print("  " + "-" * 92)
ys, ys_arch = [], []
for R in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]:
    gb = g_bar_of(Mbar, R)
    y = gb / A0_CAN
    ys.append(y)
    if R in R_ARCH:
        ys_arch.append(y)
    reg = ("DEEP-MOND (passes cut)" if y < DEEP_MOND_CUT else
           "near-a0" if y < 2 else "Newtonian-ish")
    flag = " <- ARCHIVAL Ha extent" if R in R_ARCH else ""
    print(f"  {R:>9.1f} {gb:>15.3e} {y:>12.3f} {lever(y):>9.3f} "
          f"{v_framework(Mbar, R):>10.1f}     {reg}{flag}")
R_cut = R_at_y(Mbar, DEEP_MOND_CUT)
V_cut = v_framework(Mbar, R_cut)
print(f"\n  Radius at which g_bar = {DEEP_MOND_CUT} a0 (canonical footing): "
      f"R = {R_cut:.2f} kpc, where the framework predicts V = {V_cut:.0f} km/s.")
print(f"  Same on the ALT footing (a0={A0_ALT:.3e}): R = {R_at_y(Mbar, DEEP_MOND_CUT, A0_ALT):.2f} kpc"
      f" -- the FOOTING shifts the cut radius by only "
      f"{100*abs(R_at_y(Mbar,DEEP_MOND_CUT,A0_ALT)/R_cut-1):.0f}%, so this conclusion is "
      f"footing-robust.")
Y_ARCH = float(np.median(ys_arch))          # MEDIAN-LIKE, over the ARCHIVAL radii only
L_ARCH = lever(Y_ARCH)
print("  MEDIAN-LIKE readout (pre-registered; GLS banned).  Two DIFFERENT medians, kept apart")
print("  so the archive is not flattered by radii it never observed:")
print(f"     over the ARCHIVAL Ha radii (1-3 kpc) : median y = {Y_ARCH:.2f}  -> lever L = {L_ARCH:.3f}")
print(f"     over the full tabulated grid (1-8 kpc): median y = {np.median(ys):.2f}  -> "
      f"lever L = {lever(np.median(ys)):.3f}  (ASPIRATIONAL -- no tracer out there today)")
print("\n  VERDICT ON THE N=1 OBJECT (honest, both directions):")
print(f"   * GOOD: it is gas-DOMINATED (f_gas={obj['Mgas']/Mbar:.2f}), low-mass, mu~49, and it")
print("     already has BOTH a published gas mass and published resolved Ha kinematics.")
print(f"   * BAD: the published Ha kinematics span only a few kpc, where y = 1-2.4 -- the")
print(f"     NEAR-a0/Newtonian regime, NOT the deep-MOND cut.  Reaching y<{DEEP_MOND_CUT} needs")
print(f"     tracer out to R ~ {R_cut:.1f} kpc.  At the ARCHIVAL radii the lever is only "
      f"L ~ {L_ARCH:.2f}, not ~1 --")
print("     i.e. this object is closer to the diluted Ubler/Amvrosiadis class than to the")
print("     deep-MOND class the parents require.")
print("   * WORSE: Jones+2010 report TWO Ha peaks ~2 kpc apart with DIFFERENT rotation")
print("     patterns -- i.e. a possible MERGER.  A merger cannot enter an a0 estimator.")
print("   * AND: the CO(3-2) is a 4-5 sigma UNRESOLVED detection whose flux is confined to the")
print("     southern part of the arc, so differential magnification is unmodelled -> the gas")
print("     mass carries an unquantified aperture/lensing systematic on top of alpha_CO.")

# ==========================================================================================
# 6. WHAT sigma(a0) COULD THE ARCHIVE DELIVER TODAY?  (regime-limited, not floor-limited)
# ==========================================================================================
print("\n" + BAR)
print("6. THE ARCHIVE'S CEILING TODAY -- N=1 near-a0 object vs the two bars")
print(BAR)
# In the framework's own a0-line, a0 = (g_obs^2 - g_bar^2)/g_bar.  Propagating V and M_bar:
#   d ln a0 / d ln V   = 4 g_obs^2 / (g_obs^2 - g_bar^2) = 4 (1+y)/1 ... evaluate exactly.
def dlna0_dlnV(y):
    """|d ln a0 / d ln V| on the a0-line with g_obs^2 = a0^2 y(y+1), g_bar = a0 y."""
    return 4.0 * (1.0 + y)          # = 4 g_obs^2/(g_obs^2-g_bar^2), exact for the framework
def dlna0_dlnM(y):
    """|d ln a0 / d ln M_bar| at fixed V, R (g_bar prop M_bar)."""
    return 1.0 + 2.0 * y            # = 1/L, the inverse dilution lever
ymed = Y_ARCH
print(f"  Framework sensitivities at the ARCHIVAL regime y = {ymed:.2f} (median-like, 1-3 kpc):")
print(f"    |d ln a0 / d ln V|     = 4(1+y) = {dlna0_dlnV(ymed):.2f}   (deep-MOND limit 4.00)")
print(f"    |d ln a0 / d ln M_bar| = 1+2y   = {dlna0_dlnM(ymed):.2f}   (deep-MOND limit 1.00)")
print("  ^ this IS the dilution penalty, seen from the error-propagation side: away from")
print("    deep-MOND the SAME velocity error buys a WORSE a0, exactly as lever L<1 says.")
print("\n  A single archival object, using ONLY the two errors the archive itself publishes:")
print("    velocity:  dv_pp = 80 +/- 20 km/s  -> sigma_ln V = 0.25  (inclination NOT included)")
print("    gas mass:  alpha_CO ~ 0.3 dex, propagated in LOG space through f_gas ->")
sig_V = 20.0 / 80.0
F_GAS = obj["Mgas"] / Mbar
sig_M = F_GAS * 0.30 * np.log(10.0)                # 0.3 dex on M_gas -> ln-space on M_bar
print(f"               sigma_ln M_bar = f_gas * 0.30 dex * ln10 = {F_GAS:.2f}*0.691 = {sig_M:.3f}")
sig_a0_1 = np.hypot(dlna0_dlnV(ymed) * sig_V, dlna0_dlnM(ymed) * sig_M)
print(f"    sigma(a0)/a0 (one object, published errors only) = {100*sig_a0_1:.0f}%   "
      f"[V term {100*dlna0_dlnV(ymed)*sig_V:.0f}%, mass term {100*dlna0_dlnM(ymed)*sig_M:.0f}%]")
for N in [1, 15, 40]:
    s = sig_a0_1 / np.sqrt(N)
    print(f"    N={N:>2d} identical such objects (pure sqrt-N, NO coherent floor): "
          f"{100*s:>6.0f}%   vs BAR-A {100*BAR_3SIG:.0f}% "
          f"[{'PASS' if s <= BAR_3SIG else 'FAIL'}]  vs BAR-B {100*BAR_20TO1:.1f}% "
          f"[{'PASS' if s <= BAR_20TO1 else 'FAIL'}]")
print("  *** But N=1 is all the archive has, and sqrt-N is unavailable. ***")
# --- MANDATORY COUNTER-RAIL: do NOT let the archive's failure masquerade as a physics wall ---
print("\n  COUNTERFACTUAL (rail against a manufactured NO-GO -- illustrative only; the real")
print("  error budget is D-3's job).  Take the SAME object and the SAME 0.3-dex gas-calibration")
print("  error, but (i) select it in the deep-MOND regime y=0.15 (coefficients collapse to")
print("  4 and 1) and (ii) buy a purpose-designed velocity error instead of inheriting 25%:")
print(f"    {'sigma_ln V':>12} {'sigma(a0) per obj':>18} {'N=15':>9} {'N=40':>9}   bars A/B at N=40")
for sV in [0.25, 0.10, 0.05]:
    s1 = np.hypot(dlna0_dlnV(0.15) * sV, dlna0_dlnM(0.15) * sig_M)
    s15, s40 = s1 / np.sqrt(15), s1 / np.sqrt(40)
    print(f"    {sV:>12.2f} {100*s1:>17.0f}% {100*s15:>8.0f}% {100*s40:>8.0f}%   "
          f"A:{'PASS' if s40 <= BAR_3SIG else 'FAIL'}  "
          f"B:{'PASS' if s40 <= BAR_20TO1 else 'FAIL'}")
print("  Reading: the deep-MOND SELECTION alone (y 2.42 -> 0.15) buys a factor")
print(f"  ~{np.hypot(dlna0_dlnV(2.42)*0.25, dlna0_dlnM(2.42)*sig_M)/np.hypot(dlna0_dlnV(0.15)*0.25, dlna0_dlnM(0.15)*sig_M):.1f}"
      " in sigma(a0) at FIXED data quality -- the framework-derived lever is a REAL gain and")
print("  it is why the archive's 423% is a statement about the ARCHIVE, not about feasibility.")
print("  Note also that in the deep-MOND limit the GAS-CALIBRATION term stops being amplified")
print(f"  (coefficient 1 instead of {dlna0_dlnM(2.42):.1f}), so alpha_CO ceases to dominate.")
print("  NOTE: this is deliberately the OPTIMISTIC arithmetic -- it omits inclination,")
print("  beam smearing, pressure support and the merger flag.  Even so, one archival object")
print(f"  gives ~{100*sig_a0_1:.0f}%, i.e. it MISSES BAR-A ({100*BAR_3SIG:.0f}%) by "
      f"{sig_a0_1/BAR_3SIG:.1f}x and BAR-B by {sig_a0_1/BAR_20TO1:.1f}x.")
print("  The full coherent floor is D-3's computation, NOT this file's.")

# ==========================================================================================
# 7. VERDICT
# ==========================================================================================
print("\n" + BAR)
print("7. D-2 VERDICT")
print(BAR)
print(f"""  NO USABLE ARCHIVAL SAMPLE EXISTS TODAY.  New observing time IS required.  The gap is
  NOT "there is no data" -- it is a three-way MISMATCH, and each leg is separately verified:

  (a) JWST KINEMATICS on lensed z~1.5-2.5 low-mass rotators: the big lensing-cluster programs
      that DO cover these objects (CANUCS 1208, UNCOVER 2561, GLASS-JWST 1324) are PRISM
      (R~100) or NIRISS-WFSS (R~150) -- sigma_inst >= 850 km/s, no kinematics at all.  The
      kinematics-capable JWST modes have barely been pointed at lensed cosmic-noon SFGs:
      TEMPLATES (ERS 1355) has NIRSpec-IFU R~2700 on exactly TWO lensed LBGs, at z=1.329 and
      z=2.925 -- they BRACKET the z~2 window and land in neither.  MSA-3D's slit-stepping
      (the technique that SHOULD be used) was run on 30 UNLENSED field SFGs at 0.5<z<1.7.
      NIRCam-grism kinematics (MAGNIF, ALT) cannot see H-alpha below z=2.66 and, where
      demonstrated, returns v_rot to only ~+91%/-60%.
  (b) ALMA GAS MASSES for the same objects: the entire lensed low-mass cosmic-noon CO archive
      is ~17 targets across Dessauges-Zavadsky+2015 (IRAM PdBI) and +2024 (ALMA ACA).  Inside
      1.5<z<2.5 with M*<1e10 there is essentially ONE CO detection (SGAS J0033, z=2.225) plus
      the MACS0451 arc; BOTH are spatially UNRESOLVED, and the +2024 sample is mostly UPPER
      LIMITS.  The blind check is decisive: ALCS, 33 clusters, the largest-area ALMA cluster
      survey, finds ZERO CO emitters in 1.5<z<2.5.
  (c) THE OVERLAP: exactly ONE archival object has lensing + z in window + published resolved
      kinematics + a published gas mass -- the MACS0451 arc (z=2.013, mu~49, M*=2.5e9,
      M_gas=4.0e9).  It fails the parents' own selection: at the radii where the H-alpha
      kinematics exist it sits at median y = g_bar/a0 = {Y_ARCH:.1f} (lever L = {L_ARCH:.2f}), it would
      need tracer out to R ~ {R_cut:.1f} kpc to satisfy g_bar<0.3a0, its CO is unresolved and
      confined to one part of the arc (unmodelled differential magnification), and Jones+2010
      flag it as a possible MERGER.  Using only its own published errors it yields
      sigma(a0)/a0 ~ {100*sig_a0_1:.0f}% -- short of BAR-A (37%) and far short of BAR-B (11%).

  WHAT THE ARCHIVE *DOES* USEFULLY CONTAIN (do not undersell it -- this is real and it lowers
  the cost of the new program a lot):
   * A ready-made TARGET LIST: ALT (GO 3516) has 1630 spectroscopic sources behind A2744 with
     1015 below the SMC in stellar mass, and CANUCS/UNCOVER supply prism redshifts + masses +
     lens models on five more clusters.  Selection can be done from the archive for free.
   * ~60-90 lensed z~1.2-2.5 objects with SOME resolved H-alpha kinematics (KLEVER 35,
     KLASS 15-in-window, Leethochawalit 12, OLAS 13) -- enough to pre-select which arcs are
     rotation-dominated BEFORE spending NIRSpec IFU time.
   * The existence proofs that each half of the technique works: the Cosmic Snake / A521
     (z~1.04) have ~100 pc RESOLVED ALMA CO plus ionized-gas kinematics, and ALPAKA/Lelli+2023
     deliver flat cold-gas RCs with sigma_CO <~ 15 km/s at cosmic noon -- both at the WRONG
     mass (10^10.5-10^11), which is exactly the "kinematics exist for massive HSB" diagnosis.

  So the honest D-2 answer is the expected one: the measurement is NOT in the archive.  It is,
  however, ARCHIVE-PREPARED -- targets, lens models, and rotation-dominance pre-screening are
  already public; what must be bought is (i) NIRSpec-IFU or MSA slit-stepping R>=1000 H-alpha
  on lensed M*<1e9.5 arcs at z~1.5-2.5, and (ii) RESOLVED ALMA CO (12-m array, not ACA) or
  [CII] on the SAME arcs.  Both footings carried; the DEC/RISE ratio is footing-independent.
  Estimator pre-registration stands: MEDIAN-LIKE, never GLS.  No 'theory closed'.""")

# ---------------------------------------------------------------- self-checks
assert abs(RISE_Z2 / DEC_Z2 - 3.44) < 0.01, "fork ratio at z=2 must be 3.44x"
assert abs(lever(0.0) - 1.0) < 1e-12, "deep-MOND lever must be 1"
assert lever(6.0) < 0.09, "massive-HSB lever must be tiny"
assert len(BOTH) == 1, "the cross-match must return exactly one archival object"
assert 2.40 / HA_REST - 1 > 2.5, "NIRCam WFSS must NOT reach H-alpha inside the window"
assert 0.93 / OII_REST - 1 < 1.55, "MUSE must top out near z~1.5"
assert CKMS / (2.355 * 150) > 800, "NIRISS WFSS sigma_inst must exceed 800 km/s"
assert sig_a0_1 > BAR_3SIG, "the single archival object must MISS bar-A (else re-derive)"
assert R_cut > 4.0, "the deep-MOND radius for the N=1 object must exceed its Ha extent"
print(f"\n  SELF-CHECK OK: fork {RISE_Z2/DEC_Z2:.2f}x @ z=2; lever(0)=1, lever(6)={lever(6.0):.3f}; "
      f"cross-match N={len(BOTH)};")
print(f"  NIRCam-WFSS Ha floor z>{2.40/HA_REST-1:.2f}; MUSE [OII] ceiling z<{0.93/OII_REST-1:.2f}; "
      f"NIRISS sigma_inst={CKMS/(2.355*150):.0f} km/s;")
print(f"  N=1 archival sigma(a0)={100*sig_a0_1:.0f}% > bar-A {100*BAR_3SIG:.0f}%; "
      f"R(y=0.3)={R_cut:.1f} kpc.  EXIT 0 (ran; an ARCHIVE audit, not a verdict on the theory).")
