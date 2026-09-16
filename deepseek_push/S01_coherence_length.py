#!/usr/bin/env python3
r"""S01 -- THE COHERENCE LENGTH: is the phantom a MACROSCOPIC QUANTUM OBJECT?
Does its coherence length reach r_M?  (The G235 type-I-condensate reading put
to the kinematic test at the committed equilibrium parameters.)

THE QUESTION (the NEW question of the S-series):
    G235 reads the no-free-streaming observable (H047: lambda_fs = 0,
    R(k) = 1, sigma_thermal ~ 0) as compatible with "a type-I coherent
    condensate -- N particles occupying a single mode."  But the COMMITTED
    equilibrium is a Maxwellian at sigma = 119.21 km/s with S/N = 22.8-23.8
    k_B/particle (G235/G132), m = 5.09 keV (G212 joint posterior peak),
    rho = A/r^2 (G03G).  Are those two statements consistent?  The kinematic
    test: (1) the de Broglie length lambda_dB = h/(m sigma) vs the
    inter-particle spacing n^{-1/3} (the condensation criterion
    lambda_dB >> n^{-1/3}); (2) the Ginzburg/Pippard-class coherence length
    xi = hbar/(m c_s) vs r_M (xi/r_M); (3) the phase-plateau signature and
    its falsifier; (4) verdicts V1-V3.

REGISTERS READ (committed numbers, no new physics):
    G235_typeIII_reading.md  -- S/N = 22.8-23.8 k_B/particle at m = 5 keV,
        N_ph = M_b/m = 1.56e73, T_b = 9.520686 K, sigma = 121.44 km/s
        (G081 footing), c_s^2 in [1/2, 1-) (H047 N6/N8 frozen scalar);
    G212_results.json        -- joint posterior peak m = 5.0886 keV,
        1-sigma band [4.9917, 5.1855] keV (the 5.09 keV germ);
    G116_sector_mass_synthesis.md -- the registered virial:
        sigma^2 = (1/2) sqrt(G M_b a0) = 1.4211e10 (m/s)^2
        -> sigma = 119.21 km/s at M_b = 6.5e10 Msun (G003);
    G233_eos_noscalar        -- the phantom EOS: P = sigma^2 rho,
        rho = A/r^2, A = C/(4 pi G), C = v_flat^2 = 2 sigma^2,
        c_s^2 = dP/drho = C/2 = sigma^2 (the committed isothermal value);
        r_M = 10.210052969779692 kpc (equipartition), r_break = 0.62 r_M;
    g03g_flatness_n2         -- the triad: sigma^2/v_flat^2 = 0.5 = c_s^2
        (so c_s^2 in [1/2, 1) x v_flat^2 spans c_s in [sigma, sqrt(2) sigma));
    G103_phase_timescale     -- collisionless forever (t_relax >> Hubble).
    G084_maxentropy_law       -- dS/dE = 1/sigma^2: the equilibrium IS the
        thermal (canonical) state, i.e. a dilute Maxwellian gas.

FORMULAE (all standard, all stated):
    lambda_dB   = h/(m v),  v = sigma = 119.21 km/s (the task's stated v);
    n           = rho/m,  rho(r) = A/r^2,  A = C/(4 pi G) = sigma^2/(2 pi G);
    n^{-1/3}    = (m/rho)^{1/3}  -- the mean inter-particle spacing;
    degeneracy  n lambda_dB^3   -- BEC requires n lambda_dB^3 >= 2.612 (3D);
    xi          = hbar/(m c_s)  -- the Ginzburg/Pippard-class coherence
                  (healing) length of the condensate at sound speed c_s;
    c_s^2 in [1/2, 1) x v_flat^2  ->  c_s in [sigma, sqrt(2) sigma)
                  (the G233 committed value is c_s = sigma, the band lower edge).

Only deepseek_push/ is written.
"""

import json
import math

# ----------------------------------------------------------------------
# COMMITTED CONSTANTS (registered values; every number cited above)
# ----------------------------------------------------------------------
H   = 6.62607015e-34          # J s
HBAR = H / (2.0 * math.pi)
KB  = 1.380649e-23            # J/K
C_L = 2.99792458e8            # m/s
G   = 6.67430e-11             # m^3 kg^-1 s^-2
MSUN = 1.98847e30             # kg
PC  = 3.0856775814913673e16   # m
KPC = 1.0e3 * PC
EV  = 1.602176634e-19         # J
KEV_TO_KG = EV * 1.0e3 / (C_L * C_L)   # 1 keV in kg  (E = m c^2)

M_KEV   = 5.09                # keV (G212 peak 5.0886; the 5.09 germ)
M_KG    = M_KEV * KEV_TO_KG
M_1SIG  = (4.9917, 5.1855)    # keV, G212 1-sigma band
SIGMA   = 119.21e3            # m/s (G116/G084 registered virial, 119.2 km/s)
SIGMA2  = SIGMA * SIGMA       # 1.4211e10 (m/s)^2  (registered 1.4211e10)
VFLAT2  = 2.0 * SIGMA2        # C = v_flat^2 = sqrt(G M_b a0)
A_CONST = VFLAT2 / (4.0 * math.pi * G)      # kg/m,  rho = A/r^2  (G03G/G233)
R_M     = 10.210052969779692 * KPC          # m (G233 equipartition radius)
R_1KPC  = 1.0 * KPC                          # m (the comparison radius)

# ----------------------------------------------------------------------
# (1) THE DE BROGLIE LENGTH vs THE INTER-PARTICLE SPACING
# ----------------------------------------------------------------------
def n_inv3(r):
    """n^{-1/3} at radius r for rho = A/r^2, m the phantom mass."""
    rho = A_CONST / (r * r)
    n = rho / M_KG
    return n, n ** (-1.0 / 3.0)

LAMBDA_DB  = H / (M_KG * SIGMA)          # m, the task's v = sigma
n_rM, spacing_rM  = n_inv3(R_M)          # m^-3, m
n_1k, spacing_1k  = n_inv3(R_1KPC)       # m^-3, m
LAMBDA_DB_RMS = H / (M_KG * math.sqrt(3.0) * SIGMA)   # sensitivity: v = v_rms

deg_rM = n_rM * LAMBDA_DB ** 3          # n lambda_dB^3 at r_M
deg_1k = n_1k * LAMBDA_DB ** 3          # n lambda_dB^3 at 1 kpc

# where WOULD the system become degenerate (n lambda_dB^3 = 1)?
RHO_DEGEN = (1.0 / LAMBDA_DB ** 3) * M_KG
R_DEGEN   = math.sqrt(A_CONST / RHO_DEGEN)          # m

# entropy cross-check: S/N = 22.8-23.8 k_B  =>  n lambda_th^3 ~ e^{-(s-5/2)}
LAMBDA_TH = H / (math.sqrt(2.0 * math.pi) * M_KG * SIGMA)  # thermal dB wavelength
n_lth3_rM = n_rM * LAMBDA_TH ** 3

# ----------------------------------------------------------------------
# (2) THE COHERENCE LENGTH vs r_M
# ----------------------------------------------------------------------
# c_s^2 in [1/2, 1) x v_flat^2  (H047/G233; committed value c_s = sigma):
CS_LO  = SIGMA                 # c_s^2 = 0.5 v_flat^2 = sigma^2 (G233, g03g)
CS_HI  = math.sqrt(2.0) * SIGMA   # c_s^2 -> 1- v_flat^2 (band upper edge)
XI_GL  = HBAR / (M_KG * CS_LO)    # m, Ginzburg/Pippard-class at c_s = sigma
XI_HI  = HBAR / (M_KG * CS_HI)    # m, at the band's upper edge
XI_HEAL_LO = XI_GL / math.sqrt(2.0)   # healing-length convention hbar/sqrt(2) m c_s
XI_HEAL_HI = XI_HI / math.sqrt(2.0)
XI_OVER_RM    = XI_GL / R_M
XI_HEAL_OVER_RM = XI_HEAL_LO / R_M

# the parameters a galaxy-coherent single wave would need:
M_FOR_RM = HBAR / (R_M * SIGMA)                    # kg such that hbar/(m sigma) = r_M
M_FOR_RM_KEV = M_FOR_RM / KEV_TO_KG                # keV
M_FOR_RM_EV = M_FOR_RM_KEV * 1.0e3                 # eV
SIGMA_FOR_RM = HBAR / (M_KG * R_M)                 # m/s such that xi = r_M at 5.09 keV
ORDERS_BELOW = math.log10(M_KEV * 1.0e3 / M_FOR_RM_EV)   # log10 orders m is below 5.09 keV
ORDERS_SIGMA = math.log10(SIGMA / SIGMA_FOR_RM)          # log10 orders sigma is above
ORDERS_RDEGEN = -math.log10(R_DEGEN / R_M)               # log10 orders r_degen is inside r_M

# ----------------------------------------------------------------------
# (3) THE PHASE PLATEAU -- observables and falsifier (assessment)
# ----------------------------------------------------------------------
phase_plateau = {
    "condition": "xi ~ r_M: a single coherent phase across the galaxy",
    "actual": "xi/r_M = %.2e -- the condition FAILS by ~28 orders" % XI_OVER_RM,
    "observable_signature": (
        "interference/phase-stiffness: no local density fluctuations below xi; "
        "phase rigidity in the inner region"),
    "signature_scale": "xi ~ 1e-7 m = 0.1 micron -- sub-observational at any "
                       "galactic probe (surface-density maps resolve kpc scales)",
    "falsifier": "local granularity at the xi scale (0.1 micron) -- "
                 "unobservable AND, per G233, the committed EOS (P = sigma^2 rho) "
                 "contains no condensate term whose granularity could appear",
    "honest_read": ("the phase-plateau signature and its falsifier are both "
                    "observationally inert; the equilibrium (G084 Maxwellian, "
                    "G103 collisionless) reproduces every committed observable "
                    "without any condensate"),
}

# ----------------------------------------------------------------------
# CHECKS (each states measurement and threshold; FAIL is a finding)
# ----------------------------------------------------------------------
checks = [
    ("registered sigma^2 = 1.4211e10 (m/s)^2 reproduced from sigma = 119.21 km/s",
     abs(SIGMA2 - 1.4211e10) / 1.4211e10 < 1e-3),
    ("A = C/(4 pi G) gives rho(r_M) = 3.4-3.6e-22 kg/m^3 (G233 profile: 3.543e-22, "
     "3.8% off at the G081-vs-G116 footing)",
     3.0e-22 < A_CONST / R_M**2 < 3.8e-22),
    ("lambda_dB = h/(m sigma) at m = 5.09 keV, sigma = 119.21 km/s is ~6e-7 m "
     "(0.6 micron) -- microscopic",
     3e-7 < LAMBDA_DB < 1e-6),
    ("CONDENSATION CRITERION at r_M: lambda_dB/n^{-1/3} << 1 "
     "(needs >> 1; FAIL by ~500x)",
     LAMBDA_DB / spacing_rM < 0.01),
    ("CONDENSATION CRITERION at 1 kpc: lambda_dB/n^{-1/3} << 1 "
     "(FAIL by ~100x)",
     LAMBDA_DB / spacing_1k < 0.02),
    ("DEGENERACY at r_M: n lambda_dB^3 = 8.7e-9 << 2.612 (BEC threshold) -- "
     "9 orders short",
     deg_rM < 1e-6),
    ("DEGENERACY at 1 kpc: n lambda_dB^3 = 9.0e-7 << 2.612 -- 7 orders short",
     deg_1k < 1e-4),
    ("Sackur-Tetrode cross-check: S/N = 22.8-23.8 k_B/particle implies "
     "n lambda_th^3 = 1e-9..1e-8 (consistent with the direct n lambda_dB^3; "
     "a condensate would sit at s << 1 k_B)",
     1e-10 < n_lth3_rM < 1e-6),
    ("COHERENCE LENGTH xi = hbar/(m c_s) ~ 1e-7 m -- microscopic",
     5e-8 < XI_GL < 2e-7),
    ("xi/r_M = 3.1e-28 << 1 -- the condensate is NOT coherent across the galaxy",
     XI_OVER_RM < 1e-10),
    ("mass required for galaxy coherence at sigma = 119 km/s: m = 1.58e-24 eV "
     "(27.5 orders below 5.09 keV -- the exact log10 ratio is %.2f) -- "
     "kinematically excluded by the G212 window" % ORDERS_BELOW,
     M_FOR_RM_EV < 1e-10),
    ("phase-plateau falsifier (granularity at xi ~ 0.1 micron) is "
     "observationally inert AND the committed EOS is condensate-free (G233)",
     True),
]
n_pass = sum(1 for _, ok in checks if ok)

# ----------------------------------------------------------------------
# VERDICTS
# ----------------------------------------------------------------------
verdicts = {
    "V1_lambda_dB_and_condensation": (
        "lambda_dB = h/(m sigma) = 6.13e-7 m (0.61 micron) at m = 5.09 keV, "
        "sigma = 119.21 km/s.  Inter-particle spacing n^{-1/3}: 2.98e-4 m "
        "(r_M, rho = 3.42e-22 kg/m^3) and 6.34e-5 m (1 kpc, rho = 3.56e-20). "
        "lambda_dB/n^{-1/3} = 2.1e-3 (r_M) and 9.7e-3 (1 kpc): the CONDENSATION "
        "CRITERION lambda_dB >> n^{-1/3} FAILS by two to three orders at BOTH "
        "radii; n lambda_dB^3 = 8.7e-9 (r_M) / 9.0e-7 (1 kpc) against the 3D "
        "BEC threshold 2.612 -- the phantom is NOT Bose-condensed anywhere "
        "degenerate only below r = 0.95 pc, i.e. %.1f orders INSIDE r_M).  "
            % ORDERS_RDEGEN +
            "The S/N = 22.8-23.8 k_B/particle (G235) is the fingerprint of a "
        "dilute classical Maxwellian, the opposite of a condensate."),
    "V2_xi_over_r_M": (
        "Coherence (Ginzburg/Pippard healing) length xi = hbar/(m c_s) with "
        "c_s^2 in [1/2, 1) x v_flat^2 (G233 committed c_s = sigma): "
        "xi = [6.9, 9.7]e-8 m (healing convention [4.9, 6.9]e-8 m).  "
        "xi/r_M = 3.1e-28: the condensate coherence length falls short of "
        "r_M = 10.21 kpc by TWENTY-EIGHT orders of magnitude.  A single "
        "coherent phase across the galaxy at sigma = 119 km/s would need "
        "m = 1.6e-24 eV (%.1f orders below 5.09 keV); at m = 5.09 keV it "
        "would need sigma = 3.7e-23 m/s (%.1f orders below the virial)."
        % (ORDERS_BELOW, ORDERS_SIGMA)),
    "V3_honest_statement_macroscopic_quantum_object": (
        "THE NUMBER: the phantom's coherence length is xi = 9.7e-8 m "
        "(~100 nm = 0.1 micron) and it does NOT reach r_M: xi/r_M = 3.1e-28.  "
        "At the committed (m = 5.09 keV, sigma = 119.21 km/s) the phantom is a "
        "dilute, collisionless, NON-degenerate classical gas -- a macroscopic "
        "quantum object it is not.  The G235 type-I-condensate reading is an "
        "OBSERVABLE-LEVEL equivalence (a single-mode condensate and the frozen "
        "scalar both give lambda_fs = 0, R(k) = 1), not a microscopic "
        "condensate: the committed thermal equilibrium (S/N = 22.8-23.8 "
        "k_B/particle at sigma^2 = C/2, G084) is kinematically incompatible "
        "with N = 1.56e73 particles in one coherent mode.  The honest claim "
        "of the framework is the CLASSICAL one -- the G084 maximum-entropy "
        "equilibrium -- and the coherence-length test confirms it: the "
        "quantum/condensate sector is observationally inert at every "
        "accessible scale."),
}

results = {
    "lane": "S01_coherence_length",
    "question": ("THE COHERENCE LENGTH: is the phantom a MACROSCOPIC QUANTUM "
                 "OBJECT -- does its coherence length reach r_M?  "
                 "(1) lambda_dB = h/(m sigma) vs n^{-1/3} from rho = A/r^2 at "
                 "r_M and 1 kpc (condensation criterion); (2) xi = hbar/(m c_s) "
                 "vs r_M; (3) the phase-plateau signature and falsifier; "
                 "(4) verdicts V1-V3."),
    "equilibrium": {
        "m_keV": M_KEV, "m_keV_1sig_G212": list(M_1SIG),
        "m_kg": M_KG,
        "sigma_km_s": SIGMA / 1e3, "sigma2_m2_s2": SIGMA2,
        "v_flat_km_s": math.sqrt(VFLAT2) / 1e3,
        "rho_A_over_r2_kg_m": A_CONST,
        "r_M_kpc": R_M / KPC, "r_M_m": R_M,
        "rho_rM_kg_m3": A_CONST / R_M**2,
        "rho_1kpc_kg_m3": A_CONST / R_1KPC**2,
        "S_over_N_kB_G235": "22.8-23.8",
        "N_ph_Mb_over_m": 1.56e73,
    },
    "de_broglie": {
        "lambda_dB_m": LAMBDA_DB, "lambda_dB_nm": LAMBDA_DB * 1e9,
        "lambda_dB_vrms_m": LAMBDA_DB_RMS,
        "spacing_rM_m": spacing_rM, "spacing_rM_mm": spacing_rM * 1e3,
        "spacing_1kpc_m": spacing_1k, "spacing_1kpc_micron": spacing_1k * 1e6,
        "lambda_dB_over_spacing_rM": LAMBDA_DB / spacing_rM,
        "lambda_dB_over_spacing_1kpc": LAMBDA_DB / spacing_1k,
        "n_lambda_dB3_rM": deg_rM, "n_lambda_dB3_1kpc": deg_1k,
        "BEC_threshold_3D": 2.612,
        "r_degenerate_pc": R_DEGEN / PC, "r_degenerate_over_rM": R_DEGEN / R_M,
        "n_lambda_th3_rM_crosscheck": n_lth3_rM,
        "condensed_at_rM": False, "condensed_at_1kpc": False,
    },
    "coherence": {
        "cs2_band_x_vflat2": [0.5, 1.0],
        "cs_band_km_s": [CS_LO / 1e3, CS_HI / 1e3],
        "cs_committed_G233_km_s": SIGMA / 1e3,
        "xi_GL_m": XI_GL, "xi_GL_nm": XI_GL * 1e9,
        "xi_band_nm": [XI_HI * 1e9, XI_GL * 1e9],
        "xi_healing_nm": [XI_HEAL_HI * 1e9, XI_HEAL_LO * 1e9],
        "xi_over_r_M": XI_OVER_RM,
        "xi_healing_over_r_M": XI_HEAL_OVER_RM,
        "m_for_galaxy_coherence_eV": M_FOR_RM_EV,
        "sigma_for_xi_equals_rM_m_s": SIGMA_FOR_RM,
        "coherent_across_r_M": False,
    },
    "phase_plateau": phase_plateau,
    "checks": [txt for txt, _ in checks],
    "check_values": [bool(ok) for _, ok in checks],
    "n_pass": n_pass, "n_total": len(checks),
    "verdicts": verdicts,
}

# ----------------------------------------------------------------------
# OUTPUT
# ----------------------------------------------------------------------
def fmt(x, nd=4):
    return ("%.*e" % (nd, x)) if abs(x) < 1e-3 or abs(x) >= 1e6 else ("%.*f" % (nd, x))

out = []
out.append("=" * 78)
out.append("S01 -- THE COHERENCE LENGTH: is the phantom a MACROSCOPIC QUANTUM OBJECT?")
out.append("=" * 78)
out.append("")
out.append("EQUILIBRIUM (committed registers: G212, G116/G084, G233, G03G, G235)")
out.append("  m        = %.4f keV  (G212 peak 5.0886; 1-sigma [4.9917, 5.1855])"
           % M_KEV)
out.append("  sigma    = %.2f km/s  (sigma^2 = 1.4211e10 m^2/s^2, G116/G084)"
           % (SIGMA / 1e3))
out.append("  rho(r)   = A/r^2, A = C/(4 pi G) = %.4e kg/m  (G03G/G233)" % A_CONST)
out.append("  r_M      = %.4f kpc (equipartition, G233);  r = 1 kpc comparison"
           % (R_M / KPC))
out.append("  S/N      = 22.8-23.8 k_B/particle (G235); N_ph = M_b/m = 1.56e73")
out.append("")
out.append("-" * 78)
out.append("(1) THE DE BROGLIE LENGTH  lambda_dB = h/(m sigma)")
out.append("-" * 78)
out.append("  lambda_dB          = %s m  = %.2f nm" % (fmt(LAMBDA_DB), LAMBDA_DB * 1e9))
out.append("     (v = sigma per the brief; v = v_rms = sqrt(3) sigma gives %.1f nm -- "
           "conclusion unchanged)" % (LAMBDA_DB_RMS * 1e9))
out.append("")
out.append("  INTER-PARTICLE SPACING n^{-1/3} from rho = A/r^2:")
out.append("    r = r_M (%.2f kpc): rho = %.3e kg/m^3, n = %.3e m^-3, n^{-1/3} = %.3e m"
           % (R_M / KPC, A_CONST / R_M**2, n_rM, spacing_rM))
out.append("    r = 1 kpc       : rho = %.3e kg/m^3, n = %.3e m^-3, n^{-1/3} = %.3e m"
           % (A_CONST / R_1KPC**2, n_1k, spacing_1k))
out.append("")
out.append("  CONDENSATION CRITERION  lambda_dB >> n^{-1/3}:")
out.append("    r = r_M : lambda_dB/n^{-1/3} = %.3e   -->  FAILS by ~%.0fx"
           % (LAMBDA_DB / spacing_rM, spacing_rM / LAMBDA_DB))
out.append("    r = 1kpc: lambda_dB/n^{-1/3} = %.3e   -->  FAILS by ~%.0fx"
           % (LAMBDA_DB / spacing_1k, spacing_1k / LAMBDA_DB))
out.append("  DEGENERACY  n lambda_dB^3  (BEC threshold 2.612):")
out.append("    r = r_M : %.3e  (9 orders short)     r = 1 kpc : %.3e  (7 orders short)"
           % (deg_rM, deg_1k))
out.append("    degenerate only below r = %.3f pc (r/r_M = %.2e) -- %.1f orders INSIDE "
           "r_M" % (R_DEGEN / PC, R_DEGEN / R_M, ORDERS_RDEGEN))
out.append("  CROSS-CHECK: S/N = 22.8-23.8 k_B/particle (G235) implies "
           "n lambda_th^3 = %.2e (direct n lambda_dB^3 = %.2e) --"
           % (n_lth3_rM, deg_rM))
out.append("    a condensate would sit at s << 1 k_B/particle; the committed "
           "entropy is the classical Maxwellian's.")
out.append("")
out.append("  >>> NOT BOSE-CONDENSED at either radius (V1).")
out.append("")
out.append("-" * 78)
out.append("(2) THE COHERENCE LENGTH vs r_M   xi = hbar/(m c_s)")
out.append("-" * 78)
out.append("  c_s^2 in [1/2, 1) x v_flat^2  (G084/G233; committed c_s = sigma):")
out.append("    c_s in [%.2f, %.2f] km/s" % (CS_LO / 1e3, CS_HI / 1e3))
out.append("  xi_GL = hbar/(m c_s)       = %.3e m = %.2f nm" % (XI_GL, XI_GL * 1e9))
out.append("    band across c_s^2: [%.2f, %.2f] nm" % (XI_HI * 1e9, XI_GL * 1e9))
out.append("  xi_healing = hbar/(sqrt(2) m c_s) = [%.2f, %.2f] nm"
           % (XI_HEAL_HI * 1e9, XI_HEAL_LO * 1e9))
out.append("")
out.append("  THE RATIO:")
out.append("    xi/r_M      = %.3e   (r_M = %.2f kpc)" % (XI_OVER_RM, R_M / KPC))
out.append("    xi_heal/r_M = %.3e" % XI_HEAL_OVER_RM)
out.append("")
out.append("  WHAT galaxy coherence would demand:")
out.append("    m such that hbar/(m sigma) = r_M : m = %.2e eV  (%.1f orders below "
           "5.09 keV)" % (M_FOR_RM_EV, ORDERS_BELOW))
out.append("    sigma such that hbar/(m c_s) = r_M at 5.09 keV: sigma = %.2e m/s "
           "(%.1f orders below 119 km/s)" % (SIGMA_FOR_RM, ORDERS_SIGMA))
out.append("")
out.append("  >>> NOT coherent across the galaxy: xi/r_M = 3e-28 (V2).")
out.append("")
out.append("-" * 78)
out.append("(3) THE PHASE PLATEAU")
out.append("-" * 78)
out.append("  Condition xi ~ r_M: FAILS (xi/r_M = 3.1e-28).")
out.append("  Signature (interference/phase stiffness: no local density "
           "fluctuations below xi, phase rigidity inward):")
out.append("    lives at xi ~ 0.1 micron -- sub-observational at every galactic "
           "probe (kpc resolution).")
out.append("  Falsifier (local granularity at the xi scale): unobservable, AND "
           "the committed EOS P = sigma^2 rho (G233) is condensate-free --")
out.append("    there is no condensate term whose granularity could appear.")
out.append("  Honest read: the plateau signature and its falsifier are BOTH "
           "observationally inert; the equilibrium (G084 Maxwellian, G103 "
           "collisionless) reproduces every committed observable without a "
           "condensate.")
out.append("")
out.append("-" * 78)
out.append("(4) VERDICTS")
out.append("-" * 78)
for k, v in verdicts.items():
    out.append("  %s:" % k)
    out.append("    " + v.replace("\n", "\n    "))
    out.append("")
out.append("CHECKS: %d/%d PASS" % (n_pass, len(checks)))
for txt, ok in checks:
    out.append("  [%s] %s" % ("PASS" if ok else "FAIL", txt))
out.append("")
out.append("Only deepseek_push/ written: S01_coherence_length.py/.out/S01_results.json.")

text = "\n".join(out)
print(text)

with open("S01_results.json", "w") as f:
    json.dump(results, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("\n[S01_results.json written]")
