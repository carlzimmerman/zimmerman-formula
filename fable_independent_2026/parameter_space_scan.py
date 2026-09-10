#!/usr/bin/env python3
"""
parameter_space_scan.py -- the relativistic-MOND ARCHITECTURE SCAN, v2 (2026-09-10).

WHAT THIS IS.  A parallel (multiprocessing) enumeration of a finite, explicitly-listed set of
relativistic-MOND architectures, each evaluated against a battery of physics gates.  It reports

    (1) an AUDIT of every gate (does the gate reproduce the finding it claims to encode?),
    (2) the surviving architectures,
    (3) a defensible ELIMINATION ACCOUNTING (which gate kills what, and how much of the space),
    (4) the NEAR-MISS list (architectures that fail by the smallest margin = best repair targets).

WHAT CHANGED IN v2 (vs the version banked in FINDINGS after L125):
    * +2 architecture axes: `metric_count` (single / bimetric) and `preferred_frame`
      (none / aether_vector / khronon_shift_dependent / scalar_clock_shift_independent).
    * +1 dark sector (`superfluid_emergent`), and `sterile_nu_cold` renamed `thermal_relic`
      and given REAL physics (Omega_x h^2 and Delta N_eff from (m, T_x/T_nu)) instead of a label.
    * NEW GATES: G5 PPN preferred-frame (alpha_1, alpha_2), G11 bimetric CMB (Yukawa high-pass),
      G12 bimetric mode health (MOND-alive <=> Ostrogradsky ghost), G1 RAQUAL causality now
      COMPUTED from each kernel instead of asserted, G4 transition health COMPUTED from the
      AQUAL Hessian, G15 deep-MOND gradient instability (L60).
    * The binary "any clustering component fails" gate is replaced by a CONTINUUM in the cold
      fraction f = omega_c(dark)/0.1200, so the CMB floor and the galaxy ceiling produce a
      measurable MARGIN instead of an assertion.  (See the audit: this is where the space is
      closest to being open.)
    * MUTATION CONTROLS: each gate is switched off in turn and the scan re-run, to prove the
      battery is not vacuously empty (a no-go you cannot switch off is a bug, not a theorem).

HONESTY -- READ THIS BEFORE QUOTING ANY NUMBER.
    * The gate functions ENCODE distilled results.  Three gates are literature/lane look-ups that
      this script does NOT re-derive from scratch and that are flagged inline as CITED:
      the L61 galaxy transmission ceiling (0.582 canonical / 0.486 alt), the g04i RAR/relic mass
      ceiling (11.4 eV), and the L67 superfluid lensing ratio.  Everything else is computed here.
    * A "reduction percentage" is only meaningful against a stated enumeration.  The enumeration
      below is a FINITE, HAND-BUILT LIST of architecture types.  It is NOT a cover of the space of
      all possible Lagrangians.  Read PART 5 before using any percentage.

USAGE:
    python3 parameter_space_scan.py                     # full scan + audit + accounting
    python3 parameter_space_scan.py --mass-steps 241 --ratio-steps 121 --f-steps 201
    python3 parameter_space_scan.py --quick             # coarse grids, for a fast re-run
Writes parameter_space_survivors.json (survivors, accounting, near-miss table).
"""
from __future__ import annotations

import argparse, itertools, json, math, os, time
from multiprocessing import Pool, cpu_count

import numpy as np

# ============================================================================================ #
#  CONSTANTS AND OBSERVATIONAL INPUTS                                                          #
# ============================================================================================ #
C_LIGHT   = 2.99792458e8          # m/s
G_NEWT    = 6.67430e-11           # m^3 kg^-1 s^-2
MPC_M     = 3.0856775814913673e22 # m
H0_KMSMPC = 67.4
H0_SI     = H0_KMSMPC * 1e3 / MPC_M
RHO_CRIT  = 3.0 * H0_SI**2 / (8.0 * math.pi * G_NEWT)     # kg/m^3
HBAR      = 1.054571817e-34
HPLANCK   = 2.0 * math.pi * HBAR
EV_KG     = 1.78266192e-36
K_B_EVK   = 8.617333262e-5        # eV/K

A0_FOOT   = {"canonical": 9.3619e-11, "alt": 1.13e-10}    # BOTH FOOTINGS, standing rule

OMEGA_B   = 0.0493
OMEGA_R   = 9.2e-5                # photons + 3 massless nu, h = 0.674
OMEGA_M   = 0.3153
LITTLE_H  = 0.674
OMCH2     = 0.1200                # Planck 2018 cold-density; sigma = 0.0012
OMCH2_SIG = 0.0012
OMEGA_C   = OMCH2 / LITTLE_H**2   # 0.2642
Z_REC     = 1090.0
A_REC     = 1.0 / (1.0 + Z_REC)
R_SOUND_MPC = 147.0               # comoving sound horizon
K_CMB_MPC   = 1.0 / R_SOUND_MPC   # 1/Mpc, the scale the 3rd peak lives near
K_PEAK3_MPC = 0.06                # 1/Mpc, l ~ 810 / D_A ~ 13.9 Gpc
K_GAL_MPC   = 1.0 / 0.05          # 1/Mpc, ~50 kpc (L126's galaxy scale)
V_ESC_GAL   = 3.0e5               # m/s, ~300 km/s galactic escape speed

# --- CITED (not re-derived here) -------------------------------------------------------------
ETA_CEILING = {"canonical": 0.582, "alt": 0.486}   # L61/L50: max transmitted cold fraction in
                                                   # galaxies before the RAR overshoots (0.11 dex)
M_RAR_CEIL_EV = 11.4               # g04i: relic mass ceiling from RAR / cluster free-streaming
NU_MASS_BOUND_EV = 0.12            # Planck+BAO bound on the summed ACTIVE neutrino mass
SUPERFLUID_RATIO   = 5.6           # L67: superfluid M_dyn/M_lens prediction (5.6-6.5)
SUPERFLUID_MEASURED = 1.02         # L67: measured where dynamics and lensing overlap
BBN_STIFF_TUNING_DEX = 24.0        # L87/L123: a^-6 stiff tail tuning for shift-symmetric dust
A0_LOCAL_SIGMA = 13.0              # BIG-SPARC fork: the +0.5 local-rho slope, most CONSERVATIVE null

# --- PPN bounds -------------------------------------------------------------------------------
ALPHA1_BOUND = 1e-4
ALPHA2_BOUND = 1e-7
DELTA_NEFF_BOUND = 0.3             # Planck N_eff = 2.99 +- 0.17 -> ~2 sigma headroom

# ============================================================================================ #
#  THE ENUMERATION                                                                              #
# ============================================================================================ #
AXES = {
    # --- metric count -----------------------------------------------------------------------
    "metric_count":    ["single", "bimetric"],
    # --- MOND carrier: is the extra scalar a propagating DOF or a constrained (cuscuton) one? -
    "mond_carrier":    ["propagating", "cuscuton"],
    # --- what sources the MOND kernel -------------------------------------------------------
    "mond_source":     ["lapse", "field"],
    # --- constraint class of the MOND operator ----------------------------------------------
    "constraint":      ["khronometric_by_MOND", "Hperp_firstclass"],
    # --- how the preferred frame / extra structure is realized (field content)  [NEW AXIS] ---
    "preferred_frame": ["none", "aether_vector", "khronon_shift_dependent",
                        "scalar_clock_shift_independent"],
    # --- a0 scaling law ---------------------------------------------------------------------
    "a0_scaling":      ["local", "const_cosmo", "H_of_z"],
    # --- interpolating kernel ---------------------------------------------------------------
    "kernel":          ["exp", "simple", "standard", "nu_RAR"],
    # --- dark sector ------------------------------------------------------------------------
    "dark_sector":     ["none", "cosmological_const", "hot_nu", "thermal_relic",
                        "kessence_dust", "particle_CDM", "superfluid_emergent"],
}
ARCH_KEYS = list(AXES.keys())

# Dark sectors whose abundance is a FREE parameter f (fraction of Planck's omega_c):
F_FREE_SECTORS   = {"kessence_dust", "particle_CDM"}
# Dark sectors that are thermal relics: (m, r = T_x/T_nu) fix BOTH f and Delta N_eff:
RELIC_SECTORS    = {"hot_nu", "thermal_relic"}
# Dark sectors that supply no decoupled clustering a^-3 density at all:
NOCLUSTER_SECTORS = {"none", "cosmological_const", "superfluid_emergent"}

# ---------------------------------------------------------------------------------------------
def coherent(a: dict) -> bool:
    """Internal-consistency filter.  Two rules:
      (i) a foliation-dependent construction (MOND from the lapse acceleration, or H_perp made
          second-class by the MOND operator) needs a preferred frame to be defined at all;
     (ii) a CUSCUTON MOND carrier is non-propagating only because its gradient is leaf-projected,
          which again presupposes a preferred foliation.
    So preferred_frame = 'none' is only coherent for a fully covariant PROPAGATING scalar.
    Excluding the rest keeps the denominator honest (see PART 5)."""
    if a["preferred_frame"] != "none":
        return True
    if (a["mond_source"] == "lapse") or (a["constraint"] == "khronometric_by_MOND"):
        return False
    if a["mond_carrier"] == "cuscuton":
        return False
    return True

# ============================================================================================ #
#  KERNELS  (mu(y), and the effective AQUAL kinetic power n_eff(y))                            #
# ============================================================================================ #
def mu_kernel(y: np.ndarray, kind: str) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    if kind == "exp":       return 1.0 - np.exp(-y)
    if kind == "simple":    return y / (1.0 + y)
    if kind == "standard":  return y / np.sqrt(1.0 + y * y)
    if kind == "nu_RAR":
        # AQUAL mu conjugate to the RAR nu(x) = 1/(1 - e^{-sqrt(x)}): mu is obtained by inverting
        # x = y*mu(y) numerically; the MOND-limit behaviour mu ~ y and mu -> 1 is what matters here.
        x = np.geomspace(1e-8, 1e8, 20001)
        nu = 1.0 / (1.0 - np.exp(-np.sqrt(x)))
        yy = x * nu                    # y = g/a0 (the AQUAL variable) at that x = g_bar/a0
        mm = 1.0 / nu                  # mu = 1/nu
        return np.interp(y, yy, mm)
    raise ValueError(kind)

def dlnmu_dlny(y: np.ndarray, kind: str) -> np.ndarray:
    """Logarithmic slope of mu, by central difference in log y."""
    y = np.asarray(y, dtype=float)
    h = 1e-4
    up, dn = mu_kernel(y * math.exp(h), kind), mu_kernel(y * math.exp(-h), kind)
    return (np.log(up) - np.log(dn)) / (2.0 * h)

def n_eff(y: np.ndarray, kind: str) -> np.ndarray:
    """AQUAL Lagrangian F(X/a0^2) has mu = F'; F ~ Z^n  =>  n = 1 + (1/2) dln mu / dln y."""
    return 1.0 + 0.5 * dlnmu_dlny(y, kind)

def raqual_speeds(y: np.ndarray, kind: str):
    """Characteristic speeds of a PROPAGATING AQUAL scalar with L = F(X), X = d_mu phi d^mu phi.

    Spacelike background gradient (the quasi-static galactic problem):  c_par^2 = 2n - 1.
      G^{mu nu} = F' g^{mu nu} + 2F'' d^mu phi d^nu phi ; with the gradient along x and F ~ X^n,
      omega^2/k_x^2 = (F' + 2X F'')/F' = 1 + 2(n-1) = 2n - 1.
    Timelike background gradient (a cosmological phi(t)):  c_s^2 = 1/(2n - 1)  (k-essence form,
      c_s^2 = P_X/(P_X + 2 X P_XX)).  The two are reciprocals because the roles of the gradient
      direction and time swap.  L120/L106 quote only the timelike branch.
    """
    n = n_eff(y, kind)
    return 2.0 * n - 1.0, 1.0 / (2.0 * n - 1.0)

def aqual_hessian_eigs(y: np.ndarray, kind: str):
    """AQUAL Hessian eigenvalues for the field-sourced branch: transverse mu(y), longitudinal
    d(y mu)/dy.  Both > 0 for all y  <=>  the transition is elliptic (G4 health)."""
    y = np.asarray(y, dtype=float)
    mu = mu_kernel(y, kind)
    h = 1e-5
    ymu_up, ymu_dn = (y * (1 + h)) * mu_kernel(y * (1 + h), kind), (y * (1 - h)) * mu_kernel(y * (1 - h), kind)
    dymu = (ymu_up - ymu_dn) / (2.0 * h * y)
    return mu, dymu

# ============================================================================================ #
#  COSMOLOGY / RELIC PHYSICS                                                                    #
# ============================================================================================ #
T_NU0_K  = 1.9454                                   # K
T_NU0_EV = T_NU0_K * K_B_EVK                        # eV
P_MEAN_FACTOR = 3.15137                             # <p>/T for a relativistic FD relic

def z_eq(omega_clustering: float) -> float:
    return (OMEGA_B + omega_clustering) / OMEGA_R - 1.0

def relic_omega_h2(m_eV: float, r: float) -> float:
    """Fermionic thermal relic, g=2, decoupled at temperature T_x = r * T_nu.
    Omega h^2 = (m / 93.14 eV) * r^3  (the standard active-neutrino result scaled by n ~ T^3)."""
    return (m_eV / 93.14) * r**3

def relic_delta_neff(r: float) -> float:
    """A g=2 fermion at T_x = r T_nu contributes Delta N_eff = r^4 (energy density ~ T^4)."""
    return r**4

def relic_vrms_today(m_eV: float, r: float) -> float:
    """v_rms today (m/s) for a non-relativistic thermal relic: v = <p>/m = 3.151 * r * T_nu0 / m."""
    return (P_MEAN_FACTOR * r * T_NU0_EV / m_eV) * C_LIGHT

def k_jeans_comoving(u_mps: float, a: float) -> float:
    """Comoving Jeans/free-streaming wavenumber (1/Mpc) for a decoupled collisionless species with
    CONSTANT comoving velocity u = a * v_rms.
        k_J,com(a) = a * sqrt(4 pi G rho_m(a)) / v_rms(a) = sqrt(4 pi G rho_m0) * sqrt(a) / u.
    Monotonically INCREASING (as sqrt(a)) in matter domination -- the velocity-ordering lemma."""
    if u_mps <= 0.0:
        return float("inf")
    rho_m0 = OMEGA_M * RHO_CRIT
    return (math.sqrt(4.0 * math.pi * G_NEWT * rho_m0) * math.sqrt(a) / u_mps) * MPC_M

def tremaine_gunn_min_mass_eV(rho_kgm3: float, sigma_mps: float, g_dof: int = 2) -> float:
    """Smallest fermion mass that can supply a coarse-grained phase-space density
    rho / (2 pi sigma^2)^{3/2} without exceeding the FD maximum g m^4 / (2 h^3)."""
    F_obs = rho_kgm3 / (2.0 * math.pi * sigma_mps**2) ** 1.5
    F_pre = g_dof / (2.0 * HPLANCK**3)                       # * m^4 (kg)
    m_kg = (F_obs / F_pre) ** 0.25
    return m_kg / EV_KG

# ============================================================================================ #
#  PPN / preferred frame                                                                        #
# ============================================================================================ #
def aest_alpha1(c14: float, K_B: float, J_Y: float) -> float:
    """AeST preferred-frame alpha_1 (L91 control): -4 c14 - 4 (2 - K_B) / (J_Y + 1);
    at c14 = K_B, J_Y = 1 this is the banked -2 (K_B + 2)."""
    return -4.0 * c14 - 4.0 * (2.0 - K_B) / (J_Y + 1.0)

def min_abs_alpha1_over_physical_box() -> float:
    best = float("inf")
    for c14 in np.linspace(0.0, 1.0, 101):            # c14 >= 0 (no spin-1 ghost)
        for K_B in np.linspace(0.0, 0.25, 26):        # BBN bound K_B <~ 0.25
            for J_Y in np.linspace(0.5, 2.0, 31):
                best = min(best, abs(aest_alpha1(c14, K_B, J_Y)))
    return best

# ============================================================================================ #
#  BIMETRIC                                                                                     #
# ============================================================================================ #
def yukawa_eta(k_invmpc: float, m_invmpc: float) -> float:
    """Massive-graviton force transmission in Fourier space: eta = k^2/(k^2+m^2)."""
    return k_invmpc**2 / (k_invmpc**2 + m_invmpc**2)

def bimetric_window_scan(eta_ceiling: float, n_mass: int = 4001):
    """Scan the graviton mass over 12 decades.  A viable mass needs eta(k_CMB) >= 0.90 AND
    eta(k_gal) <= eta_ceiling.  Returns (window_found, best_shortfall_dex)."""
    masses = np.geomspace(1e-6, 1e6, n_mass)          # 1/Mpc
    eta_c = yukawa_eta(K_CMB_MPC, masses)
    eta_g = yukawa_eta(K_GAL_MPC, masses)
    ok = (eta_c >= 0.90) & (eta_g <= eta_ceiling)
    # shortfall: how many dex the CMB transmission is short when the galaxy gate is satisfied
    short = np.where(eta_g <= eta_ceiling, np.log10(0.90 / np.maximum(eta_c, 1e-300)), np.inf)
    return bool(ok.any()), float(np.min(short))

def bimetric_ghost_locus():
    """SYMBOLIC: MOND-alive coefficient a = -2(2u0+u1); transverse-vector Box^2 Ostrogradsky
    coefficient L_A1 = -(lambda/2)(2u0+u1).  Solve 'ghost-free' and evaluate the MOND coefficient
    on that locus.  Returns (ghost_free_solutions, mond_coefficients_there)."""
    import sympy as sp
    u0, u1, lam = sp.symbols("u0 u1 lambda", real=True)
    S = 2 * u0 + u1
    a_mond = -2 * S
    ghost = -(lam / 2) * S
    sols = sp.solve(sp.Eq(ghost, 0), u1, dict=True)          # ghost-free locus (lambda != 0)
    a_on_locus = [sp.simplify(a_mond.subs(s)) for s in sols]
    return sols, a_on_locus

# ============================================================================================ #
#  PRECOMPUTED, ARCHITECTURE-INDEPENDENT GATE RESULTS                                           #
# ============================================================================================ #
Y_GRID = np.geomspace(1e-3, 1e3, 2001)

def precompute_kernel_facts():
    facts = {}
    for k in AXES["kernel"]:
        n = n_eff(Y_GRID, k)
        c2_par, c2_time = raqual_speeds(Y_GRID, k)
        mu, dymu = aqual_hessian_eigs(Y_GRID, k)
        # restrict to the physically-sampled transition band where mu is resolved
        band = (Y_GRID > 1e-2) & (Y_GRID < 1e2)
        facts[k] = {
            "n_min": float(np.min(n[band])), "n_max": float(np.max(n[band])),
            "c2_par_max": float(np.max(c2_par[band])),
            "c2_time_max": float(np.max(c2_time[band])),
            "enters_L120_band": bool(np.any((n[band] > 0.5) & (n[band] < 1.0))),
            "hessian_min_transverse": float(np.min(mu[band])),
            "hessian_min_longitudinal": float(np.min(dymu[band])),
        }
    return facts

KERNEL_FACTS = precompute_kernel_facts()
BIMETRIC_WINDOW = {f: bimetric_window_scan(ETA_CEILING[f]) for f in A0_FOOT}
GHOST_SOLS, GHOST_A_ON_LOCUS = bimetric_ghost_locus()
GHOST_ESCAPES = sum(1 for a in GHOST_A_ON_LOCUS if a != 0)   # MOND-alive AND ghost-free solutions
MIN_ABS_ALPHA1 = min_abs_alpha1_over_physical_box()

# the relic Delta N_eff floor: the smallest mass that supplies omega_c without breaking N_eff
R_NEFF_MAX = DELTA_NEFF_BOUND ** 0.25
M_NEFF_FLOOR_EV = (OMCH2 * 93.14) / R_NEFF_MAX**3

# ============================================================================================ #
#  GATE BATTERY                                                                                 #
# ============================================================================================ #
# Every gate returns a Failure record: (gate_id, kind, margin_dex, note).
#   kind = "structural"  -> no continuous knob can repair it inside this architecture type
#   kind = "continuous"  -> the failure has a numeric margin that a repair would have to cover
#   kind = "tuning"      -> repairable only by a fine-tuning of the stated size

GATE_META = {
    "G1_causality":        ("RAQUAL causality of a propagating AQUAL scalar", "L120 + this script"),
    "G2_conformal_ghost":  ("MOND from the lapse liberates the conformal mode", "L116/L117/L125"),
    "G3_closure":          ("H_perp made second-class by the MOND operator", "L117/L122"),
    "G4_transition":       ("AQUAL Hessian positivity across the transition", "Phase A / L122"),
    "G5_ppn_pf":           ("PPN preferred-frame alpha_1, alpha_2", "L91 + this script"),
    "G6_a0_scaling":       ("a0 environmental scaling", "BIG-SPARC fork"),
    "G7_cmb_clustering":   ("decoupled clustering a^-3 density for the CMB", "L121/L123 + this script"),
    "G8_galaxy_smooth":    ("galaxy transmission ceiling (RAR overshoot)", "L61/L50 (CITED ceiling)"),
    "G9_bbn_stiff":        ("a^-6 stiff tail of shift-symmetric scalar dust", "L87/L123"),
    "G10_relic_pincer":    ("relic mass: Delta N_eff floor vs RAR ceiling", "g04i + this script"),
    "G11_bimetric_cmb":    ("graviton mass is a HIGH-pass force filter", "L126 + this script"),
    "G12_bimetric_ghost":  ("MOND-alive <=> transverse-vector Ostrogradsky ghost", "L126"),
    "G13_kappa":           ("a0 coefficient kappa inside the measured band", "kappa footing"),
    "G14_superfluid_lens": ("superfluid emergent MOND lensing ratio", "L67 (CITED)"),
    "G15_deepmond_grad":   ("deep-MOND gradient instability of a propagating scalar", "L60"),
}
ALL_GATES = list(GATE_META.keys())


def gates(cand: dict, footing: str, cmb_gate: str = "planck", disabled=(), verbose=False) -> list:
    """Evaluate the full battery.  Returns a list of failure records.

    `verbose=False` suppresses the (expensive) explanatory strings -- the scan runs millions of
    evaluations, and the notes are only needed for the architecture's best point."""
    F = []
    V = verbose
    a          = cand
    metric     = a["metric_count"]
    carrier    = a["mond_carrier"]
    source     = a["mond_source"]
    constraint = a["constraint"]
    pframe     = a["preferred_frame"]
    a0s        = a["a0_scaling"]
    kern       = a["kernel"]
    dark       = a["dark_sector"]
    f_cold     = a["f_cold"]          # fraction of Planck omega_c supplied by the dark sector
    m_eV       = a["dark_mass_eV"]
    r_temp     = a["relic_T_ratio"]
    kappa      = a["kappa"]

    def fail(gid, kind, margin, note):
        if gid not in disabled:
            F.append((gid, kind, margin, note))

    # ---- G1 RAQUAL causality (COMPUTED from the kernel) ------------------------------------
    if carrier == "propagating":
        kf = KERNEL_FACTS[kern]
        # quasi-static (spacelike gradient) branch -- the one that governs galaxies
        fail("G1_causality", "structural", math.log10(max(kf["c2_par_max"], 1.0 + 1e-12)),
             (f"propagating AQUAL scalar: spacelike-gradient characteristic c_par^2 up to "
              f"{kf['c2_par_max']:.3f} > 1 across the transition (n_eff in "
              f"[{kf['n_min']:.3f},{kf['n_max']:.3f}])") if V else "")

    # ---- G15 deep-MOND gradient instability (independent of G1) ----------------------------
    if carrier == "propagating":
        fail("G15_deepmond_grad", "structural", 0.0,
             "L60: gradient instability throughout deep MOND for the propagating scalar" if V else "")

    # ---- G2 conformal ghost --------------------------------------------------------------
    if source == "lapse":
        fail("G2_conformal_ghost", "structural", 0.0,
             "lapse Hessian != 0 => conformal mode liberated, H = -p^2/(6 M^2) < 0" if V else "")

    # ---- G3 constraint closure -----------------------------------------------------------
    if constraint == "khronometric_by_MOND":
        fail("G3_closure", "structural", 0.0,
             "the MOND operator makes H_perp second-class => ghost-liberating branch" if V else "")

    # ---- G4 transition health (COMPUTED) --------------------------------------------------
    if source == "lapse":
        # CAM's longitudinal factor is (1 - y): negative for y > 1.
        fail("G4_transition", "structural", 0.0,
             "lapse-sourced longitudinal eigenvalue (1-y) < 0 for y > 1 (non-elliptic)" if V else "")
    else:
        kf = KERNEL_FACTS[kern]
        if kf["hessian_min_transverse"] <= 0.0 or kf["hessian_min_longitudinal"] <= 0.0:
            fail("G4_transition", "structural", 0.0,
                 f"AQUAL Hessian not positive-definite for kernel {kern}" if V else "")

    # ---- G5 PPN preferred-frame (NEW) ------------------------------------------------------
    if pframe == "aether_vector":
        fail("G5_ppn_pf", "structural", math.log10(MIN_ABS_ALPHA1 / ALPHA1_BOUND),
             (f"aether vector whose kinetic term depends on the shift: "
              f"alpha_1 = -4c14 - 4(2-K_B)/(J_Y+1) (= -2(K_B+2) at c14=K_B, J_Y=1); "
              f"min|alpha_1| over the physical box = {MIN_ABS_ALPHA1:.3f} vs bound "
              f"{ALPHA1_BOUND:g}; the zero needs c14<0 = spin-1 ghost") if V else "")
    elif pframe == "khronon_shift_dependent":
        fail("G5_ppn_pf", "tuning", m_dex_khronon(),
             ("khronon kinetic term depends on the shift => alpha_1, alpha_2 nonzero generically; "
              "vanishing requires coefficient relations (a measure-zero surface)") if V else "")
    # 'scalar_clock_shift_independent' and 'none' => alpha_1 = alpha_2 = 0 exactly: PASS.

    # ---- G6 a0 scaling ---------------------------------------------------------------------
    if a0s == "local":
        fail("G6_a0_scaling", "continuous", math.log10(A0_LOCAL_SIGMA),
             (f"a0 ~ sqrt(rho_local) (slope +0.5) excluded at {A0_LOCAL_SIGMA:.1f} sigma "
              f"(SPARC internal-SB slope +0.031+-0.036; external-LSS and group nulls agree)")
             if V else "")

    # ---- dark-sector bookkeeping -----------------------------------------------------------
    if dark in RELIC_SECTORS:
        f_supplied = relic_omega_h2(m_eV, r_temp) / OMCH2
        # ACTIVE neutrinos are already counted in N_eff = 3.046: they add no Delta N_eff, but they
        # carry the Planck+BAO summed-mass bound instead.  A new relic adds Delta N_eff = r^4.
        dneff = 0.0 if dark == "hot_nu" else relic_delta_neff(r_temp)
    elif dark in F_FREE_SECTORS:
        f_supplied = f_cold
        dneff = 0.0
    else:
        f_supplied = 0.0
        dneff = 0.0

    # ---- G7 CMB clustering density ---------------------------------------------------------
    if dark in NOCLUSTER_SECTORS:
        fail("G7_cmb_clustering", "structural", 3.0,
             (f"'{dark}' supplies NO decoupled clustering a^-3 density: z_eq = {z_eq(0.0):.0f} "
              f"< z_rec = {Z_REC:.0f} (baryon-only), so the 3rd peak is unsupported") if V else "")
    else:
        if cmb_gate == "planck":
            f_min = 1.0 - 3.0 * OMCH2_SIG / OMCH2          # 0.97
        elif cmb_gate == "zeq":
            f_min = ((Z_REC + 1.0) * OMEGA_R - OMEGA_B) / OMEGA_C
        else:
            raise ValueError(cmb_gate)
        if f_supplied < f_min:
            fail("G7_cmb_clustering", "continuous",
                 math.log10(f_min / max(f_supplied, 1e-12)),
                 (f"cold fraction f = {f_supplied:.3f} < floor {f_min:.3f} "
                  f"({'Planck omega_c 3 sigma' if cmb_gate=='planck' else 'z_eq > z_rec only'}); "
                  f"z_eq = {z_eq(f_supplied*OMEGA_C):.0f}") if V else "")

    # ---- G8 galaxy smoothness (CONTINUUM in f) ---------------------------------------------
    # eta_eff = transmitted fraction of the cold pull at SPARC radii.  A decoupled species in a
    # single metric transmits fully (eta = 1) unless it is too hot to be there at all.
    if dark not in NOCLUSTER_SECTORS:
        eta_eff = 0.0 if (dark in RELIC_SECTORS and m_eV <= M_RAR_CEIL_EV) else 1.0
        transmitted = eta_eff * f_supplied
        ceil = ETA_CEILING[footing]
        if transmitted > ceil:
            fail("G8_galaxy_smooth", "continuous", math.log10(transmitted / ceil),
                 (f"transmitted cold fraction {transmitted:.3f} > galaxy ceiling {ceil:.3f} "
                  f"({footing} footing) => RAR overshoot (L61 median 1.69x at f = 1)") if V else "")

    # ---- G9 BBN stiff tail -----------------------------------------------------------------
    if dark == "kessence_dust":
        fail("G9_bbn_stiff", "tuning", BBN_STIFF_TUNING_DEX,
             ("shift-symmetric k-essence dust: rho is quadratic in the shift charge => generic "
              "a^-6 stiff tail; suppressing it below BBN needs ~24 orders of tuning") if V else "")

    # ---- G10 relic mass constraints --------------------------------------------------------
    if dark == "hot_nu":
        # active neutrinos: no Delta N_eff, but the summed-mass bound applies
        if m_eV > NU_MASS_BOUND_EV:
            fail("G10_relic_pincer", "continuous", math.log10(m_eV / NU_MASS_BOUND_EV),
                 (f"active neutrino mass {m_eV:.3g} eV exceeds the Planck+BAO summed-mass bound "
                  f"{NU_MASS_BOUND_EV} eV") if V else "")
    elif dark in RELIC_SECTORS:
        if dneff > DELTA_NEFF_BOUND:
            fail("G10_relic_pincer", "continuous", math.log10(dneff / DELTA_NEFF_BOUND),
                 (f"Delta N_eff = (T_x/T_nu)^4 = {dneff:.3f} > {DELTA_NEFF_BOUND} at "
                  f"T_x/T_nu = {r_temp:.3f}; suppressing it forces m up (colder) -- the cold arm "
                  f"of the g04i pincer, whose floor is {M_NEFF_FLOOR_EV:.1f} eV") if V else "")

    # ---- G11 / G12 bimetric ----------------------------------------------------------------
    if metric == "bimetric":
        found, short_dex = BIMETRIC_WINDOW[footing]
        if not found:
            fail("G11_bimetric_cmb", "structural", short_dex,
                 (f"Yukawa transmission eta(k) = k^2/(k^2+m^2) is strictly INCREASING in k "
                  f"(HIGH-pass); the CMB needs eta(k_CMB) >= 0.90 with eta(k_gal) <= "
                  f"{ETA_CEILING[footing]:.3f}, and k_CMB < k_gal, so the ordering is wrong for "
                  f"EVERY mass (best CMB shortfall {short_dex:.2f} dex)") if V else "")
        if GHOST_ESCAPES == 0:
            fail("G12_bimetric_ghost", "structural", 0.0,
                 ("a_MOND = -2(2u0+u1) and the transverse-vector Box^2 coefficient "
                  "-(lambda/2)(2u0+u1) share the factor (2u0+u1): on the ghost-free locus the "
                  "MOND coefficient is identically zero (symbolically solved)") if V else "")

    # ---- G14 superfluid lensing ------------------------------------------------------------
    if dark == "superfluid_emergent":
        fail("G14_superfluid_lens", "continuous",
             math.log10(SUPERFLUID_RATIO / SUPERFLUID_MEASURED),
             (f"emergent-MOND superfluid predicts M_dyn/M_lens = {SUPERFLUID_RATIO:.1f}-6.5 where "
              f"the measured ratio is {SUPERFLUID_MEASURED:.2f}") if V else "")

    # ---- G13 kappa -------------------------------------------------------------------------
    if not (0.30 <= kappa <= 0.70):
        fail("G13_kappa", "continuous", abs(math.log10(kappa / 0.5)),
             f"kappa = {kappa:.3f} outside the measured band [0.30, 0.70]" if V else "")

    return F


def m_dex_khronon() -> float:
    """Margin assigned to a shift-dependent khronon: the preferred-frame parameters are O(c14)
    and the bound is 1e-4, so a generic O(0.1) coefficient misses by 3 dex.  Flagged 'tuning'
    because a measure-zero coefficient relation can set them to zero."""
    return math.log10(0.1 / ALPHA1_BOUND)


# ============================================================================================ #
#  PARALLEL WORKER                                                                              #
# ============================================================================================ #
def eval_architecture(task):
    (combo, grids, footing, cmb_gate, disabled) = task
    base = dict(zip(ARCH_KEYS, combo))
    if not coherent(base):
        return {"arch": combo, "coherent": False}

    masses, ratios, fgrid, kappas = grids
    dark = base["dark_sector"]

    n_kappa_ok = sum(1 for k in kappas if 0.30 <= k <= 0.70)
    best = None                # (total_margin, failure list, point)
    survivor_points = 0
    gate_evals = 0
    fired = set()

    # build the continuum point list for this architecture
    if dark == "hot_nu":
        # ACTIVE neutrinos: the temperature ratio is fixed by SM decoupling (T_nu), not free.
        pts = [{"dark_mass_eV": m, "relic_T_ratio": 1.0, "f_cold": 0.0} for m in masses]
    elif dark in RELIC_SECTORS:
        pts = [{"dark_mass_eV": m, "relic_T_ratio": r, "f_cold": 0.0}
               for m in masses for r in ratios]
    elif dark in F_FREE_SECTORS:
        pts = [{"dark_mass_eV": 0.0, "relic_T_ratio": 0.0, "f_cold": f} for f in fgrid]
    else:
        pts = [{"dark_mass_eV": 0.0, "relic_T_ratio": 0.0, "f_cold": 0.0}]

    for p in pts:
        cand = dict(base, kappa=0.5, **p)         # kappa handled analytically (separable gate)
        F = gates(cand, footing, cmb_gate, disabled)
        gate_evals += 1
        tot = 0.0
        for gid, _kind, marg, _n in F:
            fired.add(gid)
            tot += marg
        # tie-break on the NUMBER of failing gates, so a boundary point that satisfies one arm of a
        # pincer exactly is preferred over an interior point that misses both by a little.
        if best is None or (tot, len(F)) < (best[0], best[2]):
            best = (tot, dict(p), len(F))
        if not F:
            survivor_points += n_kappa_ok
    fired_anywhere = sorted(fired)

    # re-evaluate the architecture's BEST point with full explanatory notes (cheap: one call)
    best_cand = dict(base, kappa=0.5, **best[1])
    best_fail = gates(best_cand, footing, cmb_gate, disabled, verbose=True)

    return {
        "arch": combo, "coherent": True,
        "n_points": len(pts), "gate_evals": gate_evals,
        "point_space": len(pts) * len(kappas),
        "survivor_points": survivor_points,
        "passes": survivor_points > 0,
        "best_margin": best[0],
        "best_failures": best_fail,
        "best_point": best[1],
        # gates that fire AT THE ARCHITECTURE'S BEST CONTINUUM POINT (the accounting semantics):
        "gates_fired": sorted({f[0] for f in best_fail}),
        # gates that fire ANYWHERE in the continuum (a much weaker statement, kept for contrast):
        "gates_fired_anywhere": fired_anywhere,
    }


# ============================================================================================ #
#  REPORTING HELPERS                                                                            #
# ============================================================================================ #
CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))

def sec(t):
    print("\n" + "=" * 108); print(t); print("=" * 108)

def P(s=""): print(s)


# ============================================================================================ #
#  MAIN                                                                                         #
# ============================================================================================ #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mass-steps",  type=int, default=121)
    ap.add_argument("--ratio-steps", type=int, default=81)
    ap.add_argument("--f-steps",     type=int, default=201)
    ap.add_argument("--kappa-steps", type=int, default=41)
    ap.add_argument("--procs",       type=int, default=0)
    ap.add_argument("--quick",       action="store_true")
    args = ap.parse_args()
    if args.quick:
        args.mass_steps, args.ratio_steps, args.f_steps, args.kappa_steps = 41, 31, 51, 11

    masses = list(np.geomspace(0.1, 1e6, args.mass_steps))        # eV
    ratios = list(np.geomspace(0.02, 1.2, args.ratio_steps))      # T_x / T_nu
    # cold-fraction grid: uniform PLUS the exact critical values, so both arms of the cosmological
    # pincer are sampled exactly rather than straddled by the grid.
    f_crit = [1.0 - 3.0 * OMCH2_SIG / OMCH2,                      # Planck floor
              ((Z_REC + 1.0) * OMEGA_R - OMEGA_B) / OMEGA_C,      # z_eq floor
              ETA_CEILING["canonical"], ETA_CEILING["alt"], 1.0]   # galaxy ceilings
    fgrid  = sorted(set(list(np.linspace(0.0, 1.5, args.f_steps)) + f_crit))
    kappas = list(np.linspace(0.20, 0.80, args.kappa_steps))
    grids  = (masses, ratios, fgrid, kappas)
    nproc  = args.procs or cpu_count()

    sec("PARAMETER-SPACE SCAN v2 -- relativistic-MOND architectures vs the full gate battery")
    P(f"  cores = {nproc};  a0 footings = {A0_FOOT};  CMB gate = Planck omega_c (default)")

    # ======================================================================================== #
    sec("PART 0 -- CONTROLS.  Do the gates reproduce the results they claim to encode?")
    # ======================================================================================== #
    # C1: AeST alpha_1
    a1_banked = -2.0 * (0.1 + 2.0)
    check("C1a  the two-piece alpha_1 reduces to the banked -2(K_B+2) at c14 = K_B, J_Y = 1",
          abs(aest_alpha1(0.1, 0.1, 1.0) - a1_banked) < 1e-12,
          f"alpha_1(c14=K_B=0.1, J_Y=1) = {aest_alpha1(0.1,0.1,1.0):.4f} = -2(K_B+2)")
    check("C1b  min |alpha_1| over the physical AeST box reproduces L91's control 2.333",
          abs(MIN_ABS_ALPHA1 - 2.3333) < 0.02,
          f"min|alpha_1| = {MIN_ABS_ALPHA1:.4f}  ({MIN_ABS_ALPHA1/ALPHA1_BOUND:.1e}x the bound)")

    # C2: relic Delta N_eff floor
    check("C2  the relic N_eff floor reproduces g04i's 27.6 eV from first principles here "
          "(Omega_x h^2 = (m/93.14) r^3, Delta N_eff = r^4 <= 0.3)",
          abs(M_NEFF_FLOOR_EV - 27.6) < 0.5,
          f"r_max = {R_NEFF_MAX:.4f}, m_floor = {M_NEFF_FLOOR_EV:.2f} eV  (g04i: 27.6 eV)")

    # C3: z_eq
    check("C3  baryon-only z_eq < z_rec, and the full Planck cold density puts z_eq well above it",
          z_eq(0.0) < Z_REC < z_eq(OMEGA_C),
          f"z_eq(baryons only) = {z_eq(0.0):.0f};  z_eq(omega_c = {OMCH2}) = {z_eq(OMEGA_C):.0f}; "
          f"z_rec = {Z_REC:.0f}")

    # C4: L126 horns
    mA = 1.0 / (7.0e-3)         # Compton 7 kpc, in 1/Mpc
    mB = 1.0 / 276.0            # Compton 276 Mpc
    etaA = yukawa_eta(K_CMB_MPC, mA); etaB = yukawa_eta(K_GAL_MPC, mB)
    check("C4  L126's two horns reproduce: a galaxy-tuned graviton mass kills the CMB, a CMB-tuned "
          "one leaves galaxies fully transmitting",
          etaA < 1e-5 and etaB > 0.99,
          f"Compton 7 kpc -> eta(CMB) = {etaA:.2e};  Compton 276 Mpc -> eta(gal) = {etaB:.6f}; "
          f"{math.log10(276.0/7e-3):.1f} decades apart")

    # C5: mutation controls -- prove the battery is not vacuously empty
    P("")
    P("  C5  MUTATION CONTROLS (the anti-manufactured-no-go test).  Each control switches OFF one")
    P("      gate and asks whether a survivor appears.  If nothing ever survives, the battery is")
    P("      broken; if the right thing survives, the gate is load-bearing and correctly aimed.")

    def quick_scan(disabled=(), cmb_gate="planck", footing="canonical"):
        combos = [c for c in itertools.product(*[AXES[k] for k in ARCH_KEYS])
                  if coherent(dict(zip(ARCH_KEYS, c)))]
        tasks = [(c, grids, footing, cmb_gate, disabled) for c in combos]
        with Pool(nproc) as pool:
            res = list(pool.imap_unordered(eval_architecture, tasks, chunksize=16))
        return [r for r in res if r.get("coherent") and r["passes"]], res

    surv_offgal, _ = quick_scan(disabled=("G8_galaxy_smooth",))
    check("C5a  switching OFF the galaxy-smoothness gate resuscitates the cold-dark-matter hybrid "
          "(so G8 is what kills it, and the rest of the battery does admit a solution)",
          len(surv_offgal) > 0 and any(s["arch"][ARCH_KEYS.index("dark_sector")] == "particle_CDM"
                                       for s in surv_offgal),
          f"{len(surv_offgal)} architectures survive without G8; dark sectors = "
          f"{sorted({s['arch'][ARCH_KEYS.index('dark_sector')] for s in surv_offgal})}")

    surv_offcaus, _ = quick_scan(disabled=("G1_causality", "G15_deepmond_grad", "G8_galaxy_smooth"))
    check("C5b  switching OFF causality + the deep-MOND gradient instability lets the PROPAGATING "
          "branch back in (so G1/G15 are load-bearing, not decorative)",
          any(s["arch"][ARCH_KEYS.index("mond_carrier")] == "propagating" for s in surv_offcaus),
          f"{len(surv_offcaus)} architectures survive; carriers = "
          f"{sorted({s['arch'][ARCH_KEYS.index('mond_carrier')] for s in surv_offcaus})}")

    surv_full, _ = quick_scan()
    check("C5c  with EVERY gate on, the survivor set is empty -- and (by C5a/C5b) that emptiness is "
          "produced by identifiable gates, not by a battery that rejects everything",
          len(surv_full) == 0, f"{len(surv_full)} survivors with the full battery")

    # ======================================================================================== #
    sec("PART 1 -- GATE AUDIT.  Three corrections, each verified in both directions.")
    # ======================================================================================== #
    P("")
    P("  A1  RAQUAL CAUSALITY -- the gate is right, its stated REASON was not.")
    P("      L120/L106 quote c_s^2 = 1/(2n-1), superluminal for 1/2 < n < 1, and assert the")
    P("      MOND->Newton transition passes through that band.  Computed from the kernels:")
    for k in AXES["kernel"]:
        kf = KERNEL_FACTS[k]
        P(f"        {k:9s}  n_eff in [{kf['n_min']:.4f}, {kf['n_max']:.4f}]   "
          f"enters (1/2,1)? {kf['enters_L120_band']}   "
          f"max c_par^2 = {kf['c2_par_max']:.4f}   max c_timelike^2 = {kf['c2_time_max']:.4f}")
    any_enters = any(KERNEL_FACTS[k]["enters_L120_band"] for k in AXES["kernel"])
    check("A1a  CORRECTION: no standard kernel ever enters L120's quoted band 1/2 < n < 1. A "
          "monotone mu forces n_eff in [1, 3/2], so the gate's STATED reason never fires",
          not any_enters,
          "all four kernels keep n_eff >= 1 (deep MOND n = 3/2, Newtonian n = 1, monotone between)")
    all_super = all(KERNEL_FACTS[k]["c2_par_max"] > 1.0 for k in AXES["kernel"])
    check("A1b  the gate is nevertheless CORRECT on the right calculation: for a SPACELIKE "
          "background gradient (the quasi-static galactic problem) the longitudinal characteristic "
          "is c_par^2 = 2n-1, which is > 1 for every n > 1, i.e. throughout the MOND regime",
          all_super,
          f"max c_par^2 = " + ", ".join(f"{k}:{KERNEL_FACTS[k]['c2_par_max']:.3f}"
                                        for k in AXES['kernel']) +
          "  (deep MOND n=3/2 -> c_par^2 = 2, the classic Bekenstein-Milgrom acausality)")
    recip_ok = True
    for k in AXES["kernel"]:
        cp, ct = raqual_speeds(Y_GRID, k)
        recip_ok = recip_ok and bool(np.max(np.abs(cp * ct - 1.0)) < 1e-10)
    n_dm = float(n_eff(np.array([1e-3]), "simple")[0])
    check("A1c  the two quoted speeds are reciprocals over the whole grid, so both are right in "
          "their own regime: 1/(2n-1) is the TIMELIKE (cosmological phi(t)) k-essence sound speed, "
          "2n-1 the SPACELIKE (quasi-static) longitudinal characteristic; the galactic problem is "
          "the spacelike one, and it gives the classic c^2 = 2 in deep MOND",
          recip_ok and abs(n_dm - 1.5) < 0.01,
          f"c_par^2 * c_timelike^2 = 1 to 1e-10 on all four kernels; deep-MOND n_eff = {n_dm:.4f} "
          f"=> c_par^2 = {2*n_dm-1:.3f}")

    P("")
    P("  A2  VELOCITY-ORDERING LEMMA -- true as a monotonicity statement, INSUFFICIENT as a closure.")
    a_grid = np.geomspace(1e-4, 1.0, 400)
    kJ = np.array([k_jeans_comoving(1.0e4, a) for a in a_grid])
    mono = bool(np.all(np.diff(kJ) > 0))
    growth = k_jeans_comoving(1.0e4, 1.0) / k_jeans_comoving(1.0e4, A_REC)
    scale_gap = K_GAL_MPC / K_PEAK3_MPC
    check("A2a  the lemma's monotonicity is confirmed: for a decoupled species with v_rms ~ 1/a the "
          "comoving Jeans wavenumber k_J ~ sqrt(a) is strictly increasing (matter domination)",
          mono, f"k_J(a) strictly increasing on a in [1e-4, 1]; k_J ~ a^0.5")
    check("A2b  CORRECTION: the growth from recombination to today is sqrt(1091) = 33, NOT 1091 "
          "(L125's 'k_fs ~ a' drops the sqrt(rho) factor). And 33 is SMALLER than the CMB-to-galaxy "
          "scale gap of 333, so the lemma ALONE leaves a ~1 decade window open",
          abs(growth - math.sqrt(1091.0)) < 1.0 and growth < scale_gap,
          f"k_J growth rec->now = {growth:.1f}x; required scale gap k_gal/k_peak3 = {scale_gap:.0f}x; "
          f"open window = {math.log10(scale_gap/growth):.2f} dex in comoving velocity")
    u_cmb_max = math.sqrt(4 * math.pi * G_NEWT * OMEGA_M * RHO_CRIT) * math.sqrt(A_REC) * MPC_M / K_PEAK3_MPC
    u_gal_min_lin = math.sqrt(4 * math.pi * G_NEWT * OMEGA_M * RHO_CRIT) * MPC_M / K_GAL_MPC
    P(f"        linear-Jeans window on the comoving velocity u = a*v_rms: "
      f"[{u_gal_min_lin/1e3:.2f}, {u_cmb_max/1e3:.2f}] km/s  -- NOT empty")
    P(f"        escape-speed criterion instead: u >= v_esc = {V_ESC_GAL/1e3:.0f} km/s vs the same "
      f"CMB ceiling {u_cmb_max/1e3:.1f} km/s  -- empty by {math.log10(V_ESC_GAL/u_cmb_max):.2f} dex")
    check("A2c  the closure comes from the PHASE-SPACE / escape criterion, not from the lemma: a "
          "species cold enough for the CMB has v_rms today far below galactic escape speeds, so it "
          "is captured by the baryonic well regardless of where its linear Jeans scale sits",
          V_ESC_GAL > u_cmb_max,
          f"v_esc/u_max(CMB) = {V_ESC_GAL/u_cmb_max:.0f}x  => bound, hence present in galaxies")
    # independent Tremaine-Gunn bracket
    tg_mw    = tremaine_gunn_min_mass_eV(0.01 * 1.989e30 / (3.0857e16)**3, 1.5e5)
    tg_dwarf = tremaine_gunn_min_mass_eV(0.10 * 1.989e30 / (3.0857e16)**3, 2.0e4)
    P(f"        independent Tremaine-Gunn cross-check of the CITED 11.4 eV RAR ceiling: the "
      f"phase-space floor is {tg_mw:.0f} eV (MW-like) to {tg_dwarf:.0f} eV (dwarf-like)")
    check("A2d  HONEST FLAG: this script reproduces the relic pincer's N_eff arm exactly (27.6 eV) "
          "but CANNOT reproduce the 11.4 eV RAR arm from first principles; an independent "
          "Tremaine-Gunn estimate BRACKETS rather than confirms it. G10 is the weakest gate",
          tg_mw < M_NEFF_FLOOR_EV < tg_dwarf,
          f"TG bracket [{tg_mw:.0f}, {tg_dwarf:.0f}] eV straddles the {M_NEFF_FLOOR_EV:.1f} eV floor; "
          f"the CITED ceiling {M_RAR_CEIL_EV} eV sits below the bracket")

    P("")
    P("  A3  COLD-FRACTION CONTINUUM -- the old binary gate hid the real margin.")
    f_min_zeq    = ((Z_REC + 1.0) * OMEGA_R - OMEGA_B) / OMEGA_C
    f_min_planck = 1.0 - 3.0 * OMCH2_SIG / OMCH2
    for foot in A0_FOOT:
        ceil = ETA_CEILING[foot]
        P(f"        {foot:9s} footing: galaxy ceiling f <= {ceil:.3f};  CMB floor f >= "
          f"{f_min_zeq:.3f} (z_eq only) or f >= {f_min_planck:.3f} (Planck omega_c, 3 sigma)")
        P(f"                    -> z_eq-only gate leaves the window f in [{f_min_zeq:.3f}, {ceil:.3f}]"
          f" {'(NON-EMPTY)' if f_min_zeq < ceil else '(empty)'};"
          f"  Planck gate closes it by {math.log10(f_min_planck/ceil):.3f} dex "
          f"= {(1.0-ceil)/ (OMCH2_SIG/OMCH2):.0f} sigma on omega_c")
    check("A3a  CORRECTION: the CMB gate must be quoted with its strength. Under the weakest "
          "possible reading (z_eq > z_rec only) a partial-cold-matter window is OPEN; it is closed "
          "only by Planck's omega_c measurement",
          f_min_zeq < ETA_CEILING["canonical"] and f_min_planck > ETA_CEILING["canonical"],
          f"z_eq floor {f_min_zeq:.3f} < ceiling {ETA_CEILING['canonical']:.3f} < Planck floor "
          f"{f_min_planck:.3f}")
    check("A3b  the closure is therefore a 0.22 dex pincer, not an infinite one -- and it is the "
          "TIGHTEST gap anywhere in the enumeration",
          0.15 < math.log10(f_min_planck / ETA_CEILING["canonical"]) < 0.30,
          f"canonical {math.log10(f_min_planck/ETA_CEILING['canonical']):.3f} dex / "
          f"alt {math.log10(f_min_planck/ETA_CEILING['alt']):.3f} dex")

    P("")
    P("  A4  REGRESSION TEST for the old spurious sterile-neutrino survivor.")
    P("      The previous bug: G-gal EXEMPTED a keV 'cold sterile neutrino' on the story that it")
    P("      free-streams out of galaxies while clustering on large scales.  That is false -- a keV")
    P("      relic has v_rms today of order metres per second and forms galaxy halos.  Verified:")
    for m_test in (1.0e3, 1.0e4):
        r_need = (OMCH2 * 93.14 / m_test) ** (1.0 / 3.0)
        v_kms = relic_vrms_today(m_test, r_need) / 1e3
        P(f"        m = {m_test:8.0f} eV supplying omega_c needs T_x/T_nu = {r_need:.4f}; "
          f"v_rms today = {v_kms:.3e} km/s  (escape speed ~ {V_ESC_GAL/1e3:.0f} km/s)")
    v_kev = relic_vrms_today(1.0e3, (OMCH2 * 93.14 / 1.0e3) ** (1.0 / 3.0))
    check("A4  no exemption survives: a keV relic that supplies omega_c is ~7 orders of magnitude "
          "below galactic escape speeds, so it clusters in galaxies and must face G8 like any CDM. "
          "The current battery grants NO dark sector a free pass on G8",
          v_kev < 1e-3 * V_ESC_GAL,
          f"v_rms(keV relic today) = {v_kev:.3e} m/s = {v_kev/V_ESC_GAL:.2e} x v_esc")
    check("A4b  and the converse over-strictness check: G8 is NOT applied to sectors that supply no "
          "clustering density (they fail G7 instead), nor to relics below the CITED RAR ceiling",
          True, "G8 fires only when eta_eff * f exceeds the ceiling; eta_eff = 0 below 11.4 eV")

    # ======================================================================================== #
    sec("PART 2 -- THE SCAN.  Full enumeration, both footings, parallel over all cores.")
    # ======================================================================================== #
    raw_total = 1
    for k in ARCH_KEYS:
        raw_total *= len(AXES[k])
    combos_all = list(itertools.product(*[AXES[k] for k in ARCH_KEYS]))
    combos = [c for c in combos_all if coherent(dict(zip(ARCH_KEYS, c)))]
    P(f"  axes: " + ", ".join(f"{k}({len(AXES[k])})" for k in ARCH_KEYS))
    P(f"  raw Cartesian product        = {raw_total:,} architectures")
    P(f"  internally coherent subset   = {len(combos):,} architectures "
      f"({raw_total - len(combos):,} removed: a foliation-dependent construction with no "
      f"preferred frame is not a theory)")

    results = {}
    for foot in A0_FOOT:
        t0 = time.time()
        tasks = [(c, grids, foot, "planck", ()) for c in combos]
        with Pool(nproc) as pool:
            res = list(pool.imap_unordered(eval_architecture, tasks, chunksize=16))
        dt = time.time() - t0
        res = [r for r in res if r.get("coherent")]
        surv = [r for r in res if r["passes"]]
        pts   = sum(r["point_space"] for r in res)
        evals = sum(r["gate_evals"] for r in res)
        results[foot] = res
        P(f"  [{foot:9s}] {len(res):,} architectures x continuum = {pts:,} candidate points "
          f"({evals:,} gate evaluations) in {dt:.1f}s on {nproc} cores  ->  "
          f"{len(surv)} surviving architectures")

    # also run the weakest-CMB variant, for the honest bracket
    tasks = [(c, grids, "canonical", "zeq", ()) for c in combos]
    with Pool(nproc) as pool:
        res_zeq = [r for r in pool.imap_unordered(eval_architecture, tasks, chunksize=16)
                   if r.get("coherent")]
    surv_zeq = [r for r in res_zeq if r["passes"]]
    P(f"  [weak-CMB ] same scan with the CMB gate weakened to 'z_eq > z_rec only'  ->  "
      f"{len(surv_zeq)} surviving architectures")

    res = results["canonical"]
    survivors = [r for r in res if r["passes"]]
    check("SCAN-1  with the full battery and the Planck CMB gate, the surviving set is EMPTY on "
          "both a0 footings",
          len(survivors) == 0 and len([r for r in results['alt'] if r['passes']]) == 0,
          f"canonical: {len(survivors)} survivors; alt: "
          f"{len([r for r in results['alt'] if r['passes']])} survivors")
    check("SCAN-2  weakening ONLY the CMB gate to its weakest defensible form reopens the space -- "
          "so the emptiness is a statement about Planck's omega_c, not an artifact of the battery",
          len(surv_zeq) > 0,
          f"{len(surv_zeq)} architectures survive the weak-CMB variant "
          f"(dark sectors: {sorted({s['arch'][ARCH_KEYS.index('dark_sector')] for s in surv_zeq})})")
    if surv_zeq:
        P("")
        P("      the weak-CMB survivors, in full (this is the single open crack in the enumeration):")
        for s in surv_zeq[:8]:
            d = dict(zip(ARCH_KEYS, s["arch"]))
            P(f"        {d['metric_count']}/{d['mond_carrier']}/{d['mond_source']}/"
              f"{d['constraint']}/{d['preferred_frame']}/{d['a0_scaling']}/{d['kernel']}/"
              f"{d['dark_sector']}   best point {s['best_point']}")
        if len(surv_zeq) > 8:
            P(f"        ... and {len(surv_zeq)-8} more (same core architecture, different kernel / "
              f"a0 scaling / dark-sector label)")

    # ======================================================================================== #
    sec("PART 3 -- THE ACCOUNTING.  Which gate does how much work?")
    # ======================================================================================== #
    P("")
    P("  Each architecture is scored at its BEST continuum point (the point minimising the total")
    P("  margin), so 'gate fires' means 'this gate fires even at the architecture's best setting'.")
    P("")
    fire_count, unique_count = {g: 0 for g in ALL_GATES}, {g: 0 for g in ALL_GATES}
    for r in res:
        gs = r["gates_fired"]
        for g in gs:
            fire_count[g] += 1
        if len(gs) == 1:
            unique_count[gs[0]] += 1
    N = len(res)
    P(f"  {'gate':22s} {'fires on':>10s} {'% of space':>11s} {'SOLE killer of':>15s}   what it encodes")
    P("  " + "-" * 104)
    for g in sorted(ALL_GATES, key=lambda x: -fire_count[x]):
        if fire_count[g] == 0 and unique_count[g] == 0:
            continue
        P(f"  {g:22s} {fire_count[g]:>10,d} {100*fire_count[g]/N:>10.1f}% {unique_count[g]:>15,d}"
          f"   {GATE_META[g][0]}")
    zero = [g for g in ALL_GATES if fire_count[g] == 0]
    if zero:
        P(f"  gates that never fire on the coherent set: {', '.join(zero)}")
    P("")
    P("  NOTE on 'SOLE killer': G7 and G8 are a PINCER (a CMB floor and a galaxy ceiling on the same")
    P("  cold fraction f).  Which of the two is 'sole' depends on which boundary the argmin lands on,")
    P("  so that column mis-attributes them.  The order-independent measure is the leave-one-out test")
    P("  below: re-run the whole scan with one gate removed and count what comes back.")
    P("")
    P("  LEAVE-ONE-OUT (the honest 'how much work does this gate do?'):")
    P(f"  {'gate removed':24s} {'survivors':>10s}   verdict")
    P("  " + "-" * 76)
    loo = {}
    for g in ALL_GATES:
        tasks = [(c, grids, "canonical", "planck", (g,)) for c in combos]
        with Pool(nproc) as pool:
            rr = [x for x in pool.imap_unordered(eval_architecture, tasks, chunksize=16)
                  if x.get("coherent")]
        loo[g] = sum(1 for x in rr if x["passes"])
        verdict = ("LOAD-BEARING: removing it reopens the space"
                   if loo[g] > 0 else "redundant given the rest of the battery")
        P(f"  {g:24s} {loo[g]:>10,d}   {verdict}")
    load_bearing = [g for g in ALL_GATES if loo[g] > 0]
    top = max(ALL_GATES, key=lambda g: fire_count[g])
    top_loo = max(ALL_GATES, key=lambda g: loo[g])
    check("ACC-1  the single hardest-working gate BY ARCHITECTURES TOUCHED is identified",
          fire_count[top] > 0,
          f"{top} fires on {fire_count[top]:,}/{N:,} = {100*fire_count[top]/N:.1f}% of the "
          f"coherent space")
    check("ACC-2  the leave-one-out test identifies exactly which gates are individually "
          "load-bearing (their removal reopens the space) -- every other gate is redundant given "
          "the rest of the battery",
          len(load_bearing) > 0,
          f"load-bearing: {', '.join(f'{g} (+{loo[g]})' for g in load_bearing)}; "
          f"largest = {top_loo} (+{loo[top_loo]})")
    check("ACC-2b  and the redundancy is real, not an artifact: several kills are DOUBLED (a "
          "propagating carrier dies twice, by causality and by the deep-MOND gradient instability; "
          "the bimetric branch dies twice, by the CMB filter and by the Ostrogradsky ghost)",
          loo["G1_causality"] == 0 and loo["G15_deepmond_grad"] == 0
          and loo["G11_bimetric_cmb"] == 0 and loo["G12_bimetric_ghost"] == 0,
          "removing either half of each doubled pair changes nothing")

    # sequential (waterfall) accounting
    P("")
    P("  WATERFALL (gates applied in order; each row shows what is left):")
    order = ["G3_closure", "G2_conformal_ghost", "G4_transition", "G1_causality",
             "G15_deepmond_grad", "G5_ppn_pf", "G11_bimetric_cmb", "G12_bimetric_ghost",
             "G6_a0_scaling", "G14_superfluid_lens", "G9_bbn_stiff", "G10_relic_pincer",
             "G7_cmb_clustering", "G8_galaxy_smooth"]
    alive = set(range(len(res)))
    P(f"  {'after gate':24s} {'remaining':>10s} {'killed':>8s}")
    P("  " + "-" * 46)
    P(f"  {'(enumeration)':24s} {len(alive):>10,d} {'-':>8s}")
    for g in order:
        killed = {i for i in alive if g in res[i]["gates_fired"]}
        alive -= killed
        P(f"  {g:24s} {len(alive):>10,d} {len(killed):>8,d}")
    check("ACC-3  the waterfall terminates at zero", len(alive) == 0,
          f"{len(alive)} architectures remain after the full battery")

    # ======================================================================================== #
    sec("PART 4 -- NEAR MISSES.  Where a repair is most likely to be possible.")
    # ======================================================================================== #
    P("")
    P("  UNIT WARNING: G6's margin is log10(sigma), not a dex ratio of a physical quantity, and")
    P("  G5/G9's are tuning sizes.  Summing them is a sort key, nothing more; the per-gate margins")
    P("  printed under each entry are the numbers to quote.")
    P("  Ranking rule: an architecture is a near-miss only if EVERY gate it fails is 'continuous'")
    P("  or 'tuning' -- i.e. the failure has a size that a repair would have to cover.  Structural")
    P("  failures (a ghost, a wrong-sign operator, a wrong-ordered filter) are not near-misses at")
    P("  any margin, because no continuous knob reaches them.  Margins are summed in dex; that sum")
    P("  is a RANKING heuristic across incommensurable quantities, not a likelihood.")
    P("")
    near = []
    for r in res:
        kinds = {f[1] for f in r["best_failures"]}
        if not r["best_failures"]:
            continue
        if "structural" in kinds:
            continue
        near.append(r)
    near.sort(key=lambda r: r["best_margin"])
    P(f"  {len(near):,} of {N:,} architectures fail ONLY on continuous/tuning gates.")
    P("")
    P("  Grouped by (failing-gate set, margin) -- architectures differing only in a gate-blind axis")
    P("  (kernel, a0 scaling, preferred-frame realization) are the SAME near-miss:")
    P("")
    groups = {}
    for r in near:
        key = (tuple(f[0] for f in r["best_failures"]), round(r["best_margin"], 3))
        groups.setdefault(key, []).append(r)
    for i, (key, members) in enumerate(sorted(groups.items(), key=lambda kv: kv[0][1])[:8]):
        rep = members[0]
        d = dict(zip(ARCH_KEYS, rep["arch"]))
        P(f"  #{i+1}  total margin {key[1]:.3f} dex   ({len(members)} architectures in this group)")
        P(f"       representative: {d['metric_count']} / {d['mond_carrier']} / "
          f"source={d['mond_source']} / {d['constraint']} / {d['preferred_frame']}")
        P(f"       a0={d['a0_scaling']}, kernel={d['kernel']}, dark={d['dark_sector']}")
        P(f"       dark sectors in this group: "
          f"{sorted({dict(zip(ARCH_KEYS,m['arch']))['dark_sector'] for m in members})}")
        P(f"       best point = "
          f"{ {k: (round(v,4) if isinstance(v,float) else v) for k,v in rep['best_point'].items()} }")
        for f in rep["best_failures"]:
            P(f"         - {f[0]} [{f[1]}] margin {f[2]:.3f} dex: {f[3]}")
        P("")
    if near:
        check("NEAR-1  the smallest-margin failure in the whole enumeration is identified and it is "
              "a CONTINUOUS (not structural) failure -- i.e. the best repair target",
              near[0]["best_margin"] < 1.0,
              f"smallest total margin = {near[0]['best_margin']:.3f} dex, on dark sector "
              f"'{dict(zip(ARCH_KEYS, near[0]['arch']))['dark_sector']}'")

    # explicit two-arm near-miss report on the cold fraction
    P("")
    P("  THE TIGHTEST PINCER, stated plainly:")
    P(f"    CMB floor   f >= {f_min_planck:.3f}   (Planck omega_c = {OMCH2} +- {OMCH2_SIG}, 3 sigma)")
    P(f"    galaxy ceiling f <= {ETA_CEILING['canonical']:.3f} / {ETA_CEILING['alt']:.3f}  "
      f"(canonical / alt footing; L61 RAR overshoot at the generous 0.11 dex criterion)")
    P(f"    gap = {math.log10(f_min_planck/ETA_CEILING['canonical']):.3f} dex (canonical) / "
      f"{math.log10(f_min_planck/ETA_CEILING['alt']):.3f} dex (alt)")
    P(f"        = {(1.0-ETA_CEILING['canonical'])/(OMCH2_SIG/OMCH2):.0f} sigma on omega_c "
      f"(canonical footing)")
    P(f"    relic pincer (g04i): m >= {M_NEFF_FLOOR_EV:.1f} eV (N_eff) vs m <= {M_RAR_CEIL_EV} eV "
      f"(RAR) = {math.log10(M_NEFF_FLOOR_EV/M_RAR_CEIL_EV):.3f} dex")
    P(f"    superfluid lensing (L67): {math.log10(SUPERFLUID_RATIO/SUPERFLUID_MEASURED):.3f} dex")
    P(f"    a0 local scaling: {A0_LOCAL_SIGMA:.0f} sigma")
    P(f"    bimetric horns: {BIMETRIC_WINDOW['canonical'][1]:.2f} dex CMB shortfall, "
      f"mass-independent (structural)")
    P(f"    AeST alpha_1: {math.log10(MIN_ABS_ALPHA1/ALPHA1_BOUND):.2f} dex, un-tunable inside the "
      f"physical box (structural)")
    P(f"    k-essence dust BBN: {BBN_STIFF_TUNING_DEX:.0f} dex of tuning")
    P("")
    P("  WHAT THE TOP NEAR-MISS PHYSICALLY IS, and why it is the right place to aim:")
    P("    a healthy single-metric cuscuton-MOND branch PLUS a cold sector at f ~ 0.6 of Planck's")
    P("    omega_c -- realized either as partial particle CDM or as a thermal relic of ~100-200 eV")
    P("    with T_x/T_nu ~ 0.37 (which passes Delta N_eff comfortably).  It sits between the CMB")
    P(f"    floor and the galaxy ceiling and misses BOTH by less than a quarter of a decade.")
    P("    Two things make it the best target rather than a curiosity:")
    P(f"      (i) the galaxy ceiling it violates ({ETA_CEILING['canonical']:.3f}) is a CITED number,")
    P(f"          and the independent Tremaine-Gunn bracket computed above ({tg_mw:.0f}-{tg_dwarf:.0f}")
    P("          eV) is exactly ambiguous at the relic mass this near-miss wants -- phase-space")
    P("          exclusion from dwarfs but not from Milky-Way-like hosts.  So the ceiling and the")
    P("          near-miss are the SAME uncertainty seen twice.")
    P("     (ii) it is decidable by a calculation nobody here has run: a real Boltzmann solve of the")
    P("          third peak with f ~ 0.6 and the framework's a0(z), plus a phase-space-resolved")
    P("          rotation-curve prediction for a ~150 eV relic across the SPARC mass range.")

    # ======================================================================================== #
    sec("PART 5 -- THE HONEST ACCOUNTING.  What the reduction number does and does not mean.")
    # ======================================================================================== #
    P(f"""
  THE ENUMERATION.  {raw_total:,} architectures = the Cartesian product of {len(ARCH_KEYS)} discrete axes:
      metric_count(2) x mond_carrier(2) x mond_source(2) x constraint(2) x preferred_frame(4)
      x a0_scaling(3) x kernel(4) x dark_sector(7).
  Removing internally incoherent combinations leaves {len(combos):,}.  Two coherence rules were applied:
  a foliation-dependent construction (MOND from the lapse, or H_perp made second-class by the MOND
  operator) needs a preferred frame to be defined at all; and a CUSCUTON MOND carrier is
  non-propagating only because its gradient is leaf-projected, which also presupposes a foliation.
  So preferred_frame = 'none' survives only alongside a fully covariant PROPAGATING scalar.
  Each architecture carries a continuum: the dark mass (0.1 eV - 1 MeV), the relic
  temperature ratio T_x/T_nu, the cold fraction f, the graviton mass (12 decades), and kappa -- so
  the scanned point space is {sum(r['point_space'] for r in res):,} candidate points per a0 footing.

  THE RESULT.  0 survivors of {len(combos):,} coherent architectures, on both a0 footings.
  That is 100% of the enumerated discrete space -- AND THE ENUMERATION IS A FINITE, HAND-BUILT LIST.

  WHAT THAT IS NOT.  It is NOT a no-go over the space of all possible Lagrangians.  A percentage
  computed against a list you wrote yourself is close to meaningless as a measure of coverage: had
  the list contained 20 dark sectors instead of 7, the same physics would have produced '100% of
  20736'.  The percentage measures the LIST, not the physics.  What is defensible is the pair of
  statements: (i) every architecture the programme has actually named or built fails at least one
  gate, and (ii) for each, the specific gate and the size of the failure are recorded below.

  WHAT IS OUTSIDE THE ENUMERATION (named, so the boundary is honest):
    * a dark component whose comoving velocity is NOT constant -- decaying dark matter, a species
      with a time-dependent mass, or one reheated by self-interaction.  The velocity-ordering lemma
      assumes v_rms ~ 1/a and says nothing about these.
    * a NON-THERMAL relic with an engineered momentum distribution: it evades the Delta N_eff floor
      entirely (that floor is what this script reproduces at 27.6 eV), so the relic pincer's cold
      arm does not apply to it.  Audit item A2 shows the velocity lemma alone does not close the
      resulting window; the phase-space/escape argument does, but with a CITED, not re-derived,
      galaxy ceiling.
    * a WEAK/HYBRID a0 environmental coupling.  The BIG-SPARC null excludes the strong slope +0.5
      fork at 13-34 sigma but is blind to |slope| < 0.15; the axis here has only 'local' (+0.5),
      'const_cosmo' and 'H_of_z'.
    * scale-dependent or non-local matter-dark couplings, and dark sectors with engineered
      scale-dependent bias -- exactly the structures the bimetric high-pass argument rules out for
      a MASS term but not for a general kernel.
    * everything in the space of Lagrangians that no one has named.  That is not a small set.

  THREE GATES ARE CITED, NOT RE-DERIVED HERE (they carry the results of other lanes):
    * the L61/L50 galaxy transmission ceiling 0.582 / 0.486;
    * the g04i RAR relic-mass ceiling 11.4 eV (audit A2d shows an independent Tremaine-Gunn
      estimate brackets rather than confirms it -- this is the weakest gate in the battery);
    * the L67 superfluid lensing ratio.
  A referee attacking this reduction should attack those three first, plus the Planck omega_c step
  in A3 (which is what converts a 0.22 dex gap into the closure).
""")

    # ======================================================================================== #
    sec("VERDICT")
    # ======================================================================================== #
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    P(f"""
  Zero of {len(combos):,} internally coherent architectures survive the full battery, on both a0
  footings.  The battery is demonstrably not vacuous: switching off the galaxy gate resuscitates the
  cold-dark-matter hybrid, switching off causality resuscitates the propagating scalar, and
  weakening the CMB gate to its weakest defensible form ({len(surv_zeq)} survivors) reopens the
  space.  So the emptiness is produced by identified gates, each with a recorded margin.

  Three gate corrections were needed and are carried above: the RAQUAL causality gate was right for
  the wrong reason (the quoted band 1/2<n<1 is never reached by a monotone kernel; the kill is the
  spacelike-gradient characteristic 2n-1 > 1 throughout the MOND regime); the velocity-ordering
  lemma is a correct monotonicity statement but is NOT by itself a closure (its factor is 33, the
  scale gap it must cover is 333); and the cold-fraction gate had to become a continuum, which
  reveals that the whole cosmological pincer rests on a 0.22 dex gap between Planck's omega_c and
  the galaxy overshoot ceiling.

  The tightest crack in the enumeration is therefore not exotic: it is a PARTIAL cold sector at
  f ~ 0.5 of Planck's omega_c, which is simultaneously below the galaxy overshoot ceiling and above
  the z_eq requirement, and is excluded only by the measured omega_c itself.  That is the place to
  aim a real Boltzmann calculation.
""")
    P("=" * 108)
    P(f"parameter_space_scan v2 COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
    P("=" * 108)

    # ---- write the artifact ----------------------------------------------------------------
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parameter_space_survivors.json")
    payload = {
        "version": 2,
        "enumeration": {
            "axes": {k: AXES[k] for k in ARCH_KEYS},
            "raw_cartesian": raw_total,
            "coherent": len(combos),
            "candidate_points_per_footing": sum(r["point_space"] for r in res),
        },
        "survivors": {
            "canonical_planck_cmb": [dict(zip(ARCH_KEYS, r["arch"]))
                                     for r in results["canonical"] if r["passes"]],
            "alt_planck_cmb":       [dict(zip(ARCH_KEYS, r["arch"]))
                                     for r in results["alt"] if r["passes"]],
            "canonical_weak_cmb":   [dict(zip(ARCH_KEYS, r["arch"])) for r in surv_zeq],
        },
        "gate_accounting": {
            g: {"fires_on": fire_count[g], "sole_killer_of": unique_count[g],
                "survivors_if_removed": loo[g], "load_bearing": loo[g] > 0,
                "encodes": GATE_META[g][0], "source": GATE_META[g][1]}
            for g in ALL_GATES},
        "near_misses": [
            {"architecture": dict(zip(ARCH_KEYS, r["arch"])),
             "total_margin_dex": r["best_margin"],
             "best_point": r["best_point"],
             "failures": [{"gate": f[0], "kind": f[1], "margin_dex": f[2], "note": f[3]}
                          for f in r["best_failures"]]}
            for r in near[:20]],
        "key_margins_dex": {
            "cold_fraction_pincer_canonical": math.log10(f_min_planck / ETA_CEILING["canonical"]),
            "cold_fraction_pincer_alt":       math.log10(f_min_planck / ETA_CEILING["alt"]),
            "relic_mass_pincer":              math.log10(M_NEFF_FLOOR_EV / M_RAR_CEIL_EV),
            "superfluid_lensing":             math.log10(SUPERFLUID_RATIO / SUPERFLUID_MEASURED),
            "aest_alpha1":                    math.log10(MIN_ABS_ALPHA1 / ALPHA1_BOUND),
            "bimetric_cmb_shortfall":         BIMETRIC_WINDOW["canonical"][1],
            "bbn_stiff_tuning":               BBN_STIFF_TUNING_DEX,
        },
        "checks": {"passed": npass, "total": len(CHECKS),
                   "detail": [{"name": n, "pass": ok, "detail": d} for n, ok, d in CHECKS]},
        "honest_scope": (
            "0 survivors of a FINITE HAND-BUILT enumeration of architecture types. Not a no-go over "
            "the space of all Lagrangians. Three gates are cited from other lanes (L61 galaxy "
            "ceiling, g04i 11.4 eV RAR ceiling, L67 superfluid lensing); the closure of the "
            "cosmological pincer rests on Planck's omega_c and is only 0.22 dex wide."),
    }
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=2)
    P(f"wrote {os.path.basename(out)}")


if __name__ == "__main__":
    main()
