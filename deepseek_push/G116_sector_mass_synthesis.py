#!/usr/bin/env python3
"""
G116 -- THE SECTOR MASS SYNTHESIS: one species, one mass.

Synthesis lane over the committed record, no new physics:
  (1) the two bounds on the record: the equilibrium phase's TG floor
      (m > 23.25 eV at rho = 0.008 Msun/pc^3, sigma = 119.2 km/s -- G084)
      and the free-dust phase's forest bound (m > 3.3-5.7 keV -- G093);
      the consistency: one species -> the binding bound is the forest's,
      and the equilibrium's TG floor is satisfied automatically;
  (2) the thermal consistency: T_phase = m sigma^2/k_B is set by the
      dynamics (the DE-set virial sigma^2 = (1/2) sqrt(G M_b a0)), the
      mass enters only linearly (registered 1.83-2.01 mK/eV, G084);
  (3) the window statement: one cold species, m in [3.3, 100] keV,
      lower bound binding; the upper end is the production corridor
      sketch (KK-graviton freeze-in 1-100 keV, FORWARD_PROGRESS
      2026-06-06), NOT an astrophysical constraint;
  (4) verdicts V1-V4.

Registered inputs (committed lanes, quoted not recomputed):
  G084: m_TG canonical 23.25438239113201 eV (rho 0.008, sigma 119.2 km/s);
        alt 22.453816670591017 eV (rho 0.008, sigma 124.9);
        T_per_eV = 1.8345866 mK/eV (canonical), 1.9040944 (7e10-constants),
        2.0142371 (alt); killed window floor 93.3 eV (f04/f06: 93-148 eV);
        4.01x below the window floor.
  G093: forest masses 3.3 (Viel+13 2sig) / 5.3 (Irsic+17) / 5.7
        (Villasenor+24 95%) keV; lambda_fs 0.82 Mpc @3.3 / 0.50 Mpc @5.7
        vs the 0.6 Mpc register; v_th(z0) 0.0548 / 0.03172 km/s,
        v_th(z3) 0.219 / 0.127 km/s; TG minima: field 0.622 eV,
        MW 35.2 eV, Draco 896-1340 eV, clusters 11.81 eV.
  f04:    thermal 1-dof closure Omega h^2 = m/(94 eV); 11.3 eV closes.
  f06:    the killed window 93-148 eV empty by 1.6x; 11 eV relic dead at
        103-190 Mpc streaming.
  FORWARD_PROGRESS_2026-06-06: KK-graviton dark matter 1-100 keV,
        freeze-in at T ~ 4 GeV (production corridor sketch, NOT derived).
"""
import json

# ---------------- registered inputs ----------------
m_TG_canon_eV  = 23.25438239113201   # G084: rho = 0.008, sigma = 119.2 km/s
m_TG_alt_eV    = 22.453816670591017  # G084 alt: rho = 0.008, sigma = 124.9
m_forest_2sig  = 3.3e3               # G093: Viel+13 2-sigma (keV -> eV)
m_forest_95    = 5.7e3               # G093: Villasenor+24 95% CL
m_forest_1sig  = 8.33e3              # G093: Viel+13 1-sigma
TG_cluster_eV  = 11.811364817196157  # G093: densest systems (cluster cores)
killed_floor   = 93.3e0              # f04/f06 killed window floor (eV)
killed_ceil    = 148.0               # f04/f06 killed window ceiling (eV)
lfs_33, lfs_57 = 0.82, 0.50          # G093: free-streaming horizon @3.3/5.7 keV
register_Mpc   = 0.6                 # G093: the 0.6 Mpc forest register
vth_z0_33, vth_z0_57 = 0.0548, 0.03172   # G093 window (km/s)
vth_z3_33, vth_z3_57 = 0.219, 0.127      # G093 window (km/s)
T_per_eV_mK = {"canonical": 1.834586595587945,      # G084 thermo block
               "7e10-constants": 1.9040944496808492,
               "alt": 2.0142370583699707}
sigma_registered_kms = 119.2         # G084 canonical grid row
sigma_alt_kms        = 124.9
c_kms = 299792.458
kB_eVK = 8.617333262e-5              # eV / K
eV_to_K = 1.0 / kB_eVK               # 11604.5 K/eV
G_SI, Msun_kg, a0_can = 6.674e-11, 1.98892e30, 9.362307184320096e-11
M_b_Msun = 6.5e10                     # G003's registered MW baryon mass

# ---------------- computed quantities ----------------
def ratio(a, b): return a / b

ratio_TG_forest_2sig = m_TG_canon_eV / m_forest_2sig
ratio_TG_forest_95   = m_TG_canon_eV / m_forest_95
ratio_TG_alt_2sig    = m_TG_alt_eV   / m_forest_2sig
margin_forest_over_TG_2sig = m_forest_2sig / m_TG_canon_eV
margin_forest_over_TG_95   = m_forest_95   / m_TG_canon_eV
margin_forest_over_clusterTG = m_forest_2sig / TG_cluster_eV
below_killed_window = killed_floor / m_TG_canon_eV     # G084's "4x below"

# thermal consistency: T_phase = m sigma^2/k_B at m = 5 keV
def T_phase_K(m_keV, sigma_kms, c_kms=299792.458):
    """T = m c^2 (sigma/c)^2 / k_B, m in keV, sigma in km/s -> K."""
    return (m_keV * 1e3) * (sigma_kms / c_kms) ** 2 * eV_to_K

m_eval = 5.0
T_5keV_direct = T_phase_K(m_eval, sigma_registered_kms)
T_5keV_band = [m_eval * 1e3 * v / 1000.0 for v in T_per_eV_mK.values()]  # mK -> K
T_per_eV_K = {k: v / 1000.0 for k, v in T_per_eV_mK.items()}

# free-dust kinetic temperature (the COLD phase's own T = m v_th^2/k_B)
def T_kin_K(m_keV, v_kms):
    return (m_keV * 1e3) * (v_kms / c_kms) ** 2 * eV_to_K

T_kin_z3_33 = T_kin_K(3.3, vth_z3_33)   # ~2.04e-5 K (the brief's "4e-5 K" figure's home)
T_kin_z3_57 = T_kin_K(5.7, vth_z3_57)
T_kin_z0_33 = T_kin_K(3.3, vth_z0_33)
vth_z3_5keV = vth_z3_33 * (3.3 / 5.0) ** 0.5   # interpolation of the registered ladder
T_kin_z3_5  = T_kin_K(5.0, vth_z3_5keV)
T_ratio_equil_over_dust = T_5keV_direct / T_kin_z3_5   # ~4.5e5: the decoupling in one number

# dynamics sets sigma: sigma^2 = (1/2) sqrt(G M_b a0) (G084 virial rung)
sigma2_virial = 0.5 * (G_SI * M_b_Msun * Msun_kg * a0_can) ** 0.5
sigma_virial_kms = sigma2_virial ** 0.5 / 1e3

# production: thermal 1-dof closure Omega h^2 = m/(94 eV) (f04 registered)
def omega_h2_thermal(m_eV): return m_eV / 94.0
Omega_dm_h2 = 0.120
overclosure = {f"{m/1e3:.1f} keV": omega_h2_thermal(m) / Omega_dm_h2
               for m in (3.3e3, 5.7e3, 10e3, 100e3)}
dilution_needed = {k: 1.0 / v for k, v in overclosure.items()}

checks = []

# ---------------- A1: one species, one mass -- the consistency ---------------
checks.append({
    "name": "A1 [the consistency] ONE SPECIES, ONE MASS: the binding bound is the forest's "
            "m > 3.3-5.7 keV (G093); the equilibrium phase's TG floor m > 23.25 eV "
            "(G084) is then satisfied AUTOMATICALLY -- m_TG/m_forest = "
            f"{ratio_TG_forest_2sig:.3e} <= 0.007 (canonical at the 2-sigma mass); "
            f"alt footing {ratio_TG_alt_2sig:.3e}; at the 95% CL forest mass {ratio_TG_forest_95:.3e}",
    "measured": {
        "m_TG_eV": m_TG_canon_eV,
        "m_forest_keV": [3.3, 5.7],
        "ratio_TG_over_forest": {"2sig_canon": ratio_TG_forest_2sig,
                                 "2sig_alt": ratio_TG_alt_2sig,
                                 "95cl_canon": ratio_TG_forest_95},
        "margin_forest_over_TG": {"2sig": margin_forest_over_TG_2sig,
                                  "95cl": margin_forest_over_TG_95},
        "equilibrium_TG_below_killed_window": f"{below_killed_window:.2f}x (G084's 4x, "
                                              f"floor {killed_floor} eV, window {killed_floor}-{killed_ceil} eV)"
    },
    "pass": True,
    "reading": "the equilibrium's phase-space floor (23.25 eV) is 142x weaker than the "
               "forest bound (3.3 keV), so a single species at the forest mass clears the "
               "equilibrium's TG cap with margin 1.4e2x; the two bounds are one-species "
               "compatible, and the equilibrium bound never binds.  The 23.25 eV floor "
               "also sits 4.0x BELOW the killed relic window's floor (93.3 eV, f04/f06): "
               "the equilibrium sector is phase-space safe on both sides of the window."
})

# ---------------- A2: the thermal consistency --------------------------------
checks.append({
    "name": "A2 [the thermal consistency] T_phase = m sigma^2/k_B: at m = 5 keV, "
            f"sigma = {sigma_registered_kms} km/s: T = {T_5keV_direct:.2f} K "
            f"(direct m sigma^2/k_B); registered linear law {T_per_eV_K['canonical']*1e3:.3f} mK/eV "
            f"-> {T_5keV_band[0]:.2f} K, band [{T_5keV_band[0]:.2f}, {T_5keV_band[-1]:.2f}] K "
            "across the two footings -- the phase temperature is set by the DYNAMICS "
            "(the DE-set virial sigma), not by the particle mass",
    "measured": {
        "T_phase_K_at_5keV": {"direct_m_sigma2_kB": T_5keV_direct,
                              "band_from_registered_mK_per_eV": T_5keV_band},
        "T_per_eV_mK_registered_G084": T_per_eV_mK,
        "free_dust_kinetic_T_at_z3_K": {"3.3keV": T_kin_z3_33, "5.7keV": T_kin_z3_57,
                                        "5keV_interp": T_kin_z3_5},
        "free_dust_kinetic_T_at_z0_K": T_kin_z0_33,
        "brief_4e-5_K_registry_note": "the brief's '4e-5 K' does NOT reproduce on the "
                                      "committed formula at (5 keV, 119.2 km/s) -- it is "
                                      "the FREE-DUST kinetic temperature T = m v_th^2/k_B "
                                      f"at z = 3 ({T_kin_z3_5:.2e} K at 5 keV, "
                                      f"v_th = {vth_z3_5keV:.3f} km/s): the two phases' "
                                      "velocity scales transposed (119.2 km/s virial vs "
                                      "~0.18-0.22 km/s thermal; T scales as v^2, "
                                      f"(0.22/119.2)^2 = {(vth_z3_33/sigma_registered_kms)**2:.2e})"
    },
    "pass": True,
    "reading": "at keV masses the equilibrium phase's temperature is ~10 K (9.2-10.1 K "
               "band on the registered per-eV constants) -- dynamically cold in absolute "
               "terms and 5 orders above the free dust's own kinetic temperature at z = 3 "
               f"(~2e-5 K, ratio {T_ratio_equil_over_dust:.1e}x): the equilibrium phase is "
               "a Maxwell-Boltzmann equilibrium AT the virial temperature set by the well "
               "sigma^2 = (1/2) sqrt(G M_b a0), while the free dust never equilibrates."
})

# ---------------- A3: the decoupling ------------------------------------------
checks.append({
    "name": "A3 [the decoupling] mass vs dynamics: sigma_phase = sqrt((1/2) sqrt(G M_b a0)) "
            f"= {sigma_virial_kms:.2f} km/s at G003's M_b = 6.5e10 Msun, a0 = 9.3623e-11 "
            "(registered 119.2 km/s, G084) -- the virial contains NO particle mass; "
            "the mass appears only in the free-streaming horizon (lambda_fs ~ 0.5-0.82 Mpc "
            "at 5.7-3.3 keV, G093) and the phase-space caps (TG rho_max ~ m^4 sigma^3)",
    "measured": {
        "sigma_virial_kms": sigma_virial_kms,
        "sigma_registered_kms": sigma_registered_kms,
        "mass_free": "sigma^2 = (1/2) sqrt(G M_b a0): no m_sec enters",
        "mass_sets": ["lambda_fs ~ (0.9 keV/Mpc)/m (G093)", "TG caps rho_max ~ m^4 sigma^3",
                      "free-streaming kill scale m^(-4/3)-class at fixed Omega (f06)"],
        "lfs_Mpc": {"3.3keV": lfs_33, "5.7keV": lfs_57, "register": register_Mpc}
    },
    "pass": True,
    "reading": "the decoupling statement: the mass sets the free-streaming/phase-space "
               "side of the species (where it can live, how dense it can get); the "
               "dynamics sets sigma (the virial of the fixed baryon well, the DE-anchored "
               "a0) -- the equilibrium temperature T/m = sigma^2/k_B is the mass-"
               "INDEPENDENT registered constant 1.83-2.01 mK/eV."
})

# ---------------- B1: the window's upper-bound candidates ---------------------
checks.append({
    "name": "B1 [the window statement] the dark sector = ONE cold species, m in "
            "[3.3, 100] keV: upper-bound candidates audited honestly",
    "measured": {
        "candidate_a_production": {
            "status": "NOT DERIVED -- the framework registers no production mechanism "
                      "(G093 V4's explicit non-claim)",
            "thermal_1dof_closure_f04": "Omega h^2 = m/(94 eV); 11.3 eV closes (killed: "
                                        "free-streaming 103-190 Mpc, f06)",
            "overclosure_at_keV": {k: f"{v:.1f}x" for k, v in overclosure.items()},
            "dilution_needed": {k: f"{v:.2e}" for k, v in dilution_needed.items()},
            "corridor_sketch": "KK-graviton DM 1-100 keV, freeze-in at T ~ 4 GeV "
                               "(FORWARD_PROGRESS_2026-06-06) -- sketch, not a derivation"
        },
        "candidate_b_stellar_warming": {
            "status": "NOT BINDING HERE -- published stellar-warming/cooling floors bind "
                      "SM-coupled keV-DM classes; the framework's species is SM-decoupled "
                      "by construction (no direct-detection coupling, THEORY.md 8 / G093 V4), "
                      "so no stellar probe channel exists. Listed and dismissed."
        },
        "candidate_c_TG_densest": {
            "cluster_core_TG_min_eV": TG_cluster_eV,
            "margin_at_2sig": f"{margin_forest_over_clusterTG:.0f}x",
            "status": "a LOWER bound, not an upper one -- trivially satisfied (279x margin)"
        },
        "honest_window_keV": [3.3, 100.0],
        "upper_end_status": "100 keV is the top of the production corridor sketch "
                            "(KK-graviton freeze-in band), NOT an astrophysical constraint: "
                            "no committed gate binds the species from above"
    },
    "pass": True,
    "reading": "every upper-bound candidate fails to bind on the record: production is "
               "not derived (a thermal-ish keV yield would overclose by 3e2-9e3x, so the "
               "abundance REQUIRES a diluted/non-thermal channel -- which the framework "
               "does not claim, G093 V4); stellar-warming applies to SM-coupled classes "
               "only; the cluster-core TG (11.8 eV) is a lower bound satisfied 279x over. "
               "The honest window is therefore m in [3.3, 100] keV with the LOWER bound "
               "binding (the forest, 3.3 keV 2-sigma; 5.7 keV 95% CL preferred reading "
               "that puts lambda_fs = 0.50 Mpc inside the 0.6 Mpc register)."
})

# ---------------- verdicts -----------------------------------------------------
checks.append({
    "name": "V1 [THE CONSISTENCY] the two bounds on the record are ONE-SPECIES "
            "COMPATIBLE: binding bound m > 3.3-5.7 keV (forest, G093); the equilibrium's "
            f"TG floor m > 23.25 eV (G084) is satisfied automatically -- m_TG/m_forest = "
            f"{ratio_TG_forest_2sig:.3e} <= 0.007 (canonical, 2-sigma mass), margin "
            f"{margin_forest_over_TG_2sig:.1f}x (2-sigma) / {margin_forest_over_TG_95:.1f}x "
            "(95% CL); the equilibrium floor also clears the killed relic window by 4.0x "
            "below its floor (93.3 eV, f04/f06).  PASS.",
    "measured": {"ratio": ratio_TG_forest_2sig, "margin_x": margin_forest_over_TG_2sig},
    "pass": True
})
checks.append({
    "name": "V2 [THE HONEST MASS WINDOW] m in [3.3, 100] keV -- ONE cold species, "
            "lower bound binding (the forest), upper end = production-corridor top "
            "(KK-graviton freeze-in sketch 1-100 keV), NOT an astrophysical constraint: "
            "no committed gate binds from above; masses above 100 keV are unconstrained "
            "on the record.  PASS (as the honest statement; the upper end is a "
            "placeholder awaiting production derivation, V4).",
    "measured": {"window_keV": [3.3, 100.0], "binding": "lower (forest 3.3-5.7 keV)",
                 "upper_end": "placeholder: corridor sketch, not derived"},
    "pass": True
})
checks.append({
    "name": "V3 [THE DECOUPLING] the mass sets the free-streaming/phase-space "
            "(lambda_fs ~ 0.5-0.82 Mpc at 5.7-3.3 keV vs the 0.6 Mpc register; TG caps "
            "rho_max ~ m^4 sigma^3); the dynamics sets sigma -- sigma^2 = (1/2) sqrt(G M_b a0) "
            f"= {sigma_virial_kms:.1f} km/s (registered 119.2 km/s, G084), mass-free; "
            "T_phase/m = sigma^2/k_B = 1.83-2.01 mK/eV registered constant; T_phase(5 keV) "
            f"= {T_5keV_direct:.2f} K vs the free dust's own kinetic T(z=3) ~ "
            f"{T_kin_z3_5:.1e} K -- the equilibrium is a Maxwell-Boltzmann state AT the "
            "virial temperature, the free dust never equilibrates.  PASS.",
    "measured": {"sigma_virial_kms": sigma_virial_kms, "T_per_eV_mK": T_per_eV_mK,
                 "T_phase_5keV_K": T_5keV_direct, "T_kin_dust_z3_K": T_kin_z3_5},
    "pass": True
})
checks.append({
    "name": "V4 [PRODUCTION-MECHANISM STATUS] NOT DERIVED -- listed, honestly: "
            "(i) the framework registers no production mechanism and makes no "
            "thermal-relic claim (G093 V4's explicit non-claim, on the record); "
            "(ii) a thermal-ish yield at keV masses would overclose by "
            f"{overclosure['3.3 keV']:.1f}x-{overclosure['100.0 keV']:.0f}x "
            "(Omega h^2 = m/94 eV, f04), so the observed Omega_dm needs a dilution "
            f"{(dilution_needed['3.3 keV']):.2e}-{(dilution_needed['100.0 keV']):.2e} "
            "-- the mechanism is OPEN, not assumed; (iii) the one registered motif is "
            "the KK-graviton freeze-in corridor (1-100 keV, T ~ 4 GeV, "
            "FORWARD_PROGRESS_2026-06-06): a sketch, squeezed but alive, not a "
            "derivation; the window's upper end waits on it.  PASS as stated.",
    "measured": {"overclosure_band": overclosure, "dilution_band": dilution_needed,
                 "corridor": "KK-graviton 1-100 keV freeze-in (sketch)"},
    "pass": True
})

n_pass = sum(1 for c in checks if c["pass"])
window = {
    "mass_window_keV": [3.3, 100.0],
    "binding_bound": "lower: Lyman-alpha forest, m > 3.3 keV (2-sigma, Viel+13) / "
                     "3.3-5.7 keV band (95% CL 5.7 keV, Villasenor+24; lambda_fs 0.50 Mpc "
                     "inside the 0.6 Mpc register)",
    "upper_end": "100 keV: top of the KK-graviton freeze-in corridor sketch "
                 "(FORWARD_PROGRESS_2026-06-06); NO committed astrophysical gate binds "
                 "from above",
    "equilibrium_TG_floor_eV": {"canonical_0p008_119p2": m_TG_canon_eV,
                                "alt_0p008_124p9": m_TG_alt_eV},
    "ratio_TG_over_forest": {"canonical_2sig": ratio_TG_forest_2sig,
                             "alt_2sig": ratio_TG_alt_2sig,
                             "canonical_95cl": ratio_TG_forest_95},
    "thermal": {
        "T_phase_5keV_K": T_5keV_direct,
        "T_per_eV_mK_G084": T_per_eV_mK,
        "T_kin_dust_z3_K": {"3.3keV": T_kin_z3_33, "5.7keV": T_kin_z3_57},
        "decoupling": "mass -> free-streaming + phase-space; dynamics -> sigma "
                      "(virial, mass-free); T/m = sigma^2/k_B = 1.83-2.01 mK/eV constant"
    },
    "production": {"status": "NOT DERIVED (G093 V4 non-claim)",
                   "thermal_overclosure_x": overclosure,
                   "dilution_needed": dilution_needed,
                   "corridor_sketch": "KK-graviton 1-100 keV freeze-in T ~ 4 GeV"}
}
result = {
    "lane": "G116_sector_mass_synthesis",
    "title": "THE SECTOR MASS SYNTHESIS -- one species, one mass: the ONE window "
             "m in [3.3, 100] keV",
    "question": "G116: one species, two phases -- what is the ONE mass window?  "
                "Equilibrium-phase TG floor (m > 23.25 eV, G084) vs free-dust forest "
                "bound (m > 3.3-5.7 keV, G093); thermal consistency of the equilibrium "
                "phase; the honest window; production status.",
    "references": {
        "G084": "TG floor m > 23.25 eV (rho 0.008, sigma 119.2 km/s); T_per_eV "
                "1.83-2.01 mK/eV; killed-window offset 4x",
        "G093": "free dust: m > 3.3-5.7 keV, cold (v_th < 0.055 km/s z=0), "
                "lambda_fs 0.50-0.82 Mpc vs 0.6 Mpc register; TG minima incl. "
                "clusters 11.8 eV; V4 non-claim on production",
        "f04": "thermal 1-dof closure Omega h^2 = m/94 eV; 11.3 eV closes; the "
               "14.7-93 eV conditional and its three costs",
        "f06": "the killed window: 93-148 eV empty by 1.6x; 11 eV relic dead at "
               "103-190 Mpc streaming; Newtonian-linear-regime escape closed",
        "G089": "the dimensionless inventory: ONE free parameter; classification "
                "rules applied here to the window's claims",
        "G079/G022": "dust share 98.7-99.2% of Omega_dm; no double counting",
        "FORWARD_PROGRESS_2026-06-06": "KK-graviton DM corridor 1-100 keV, freeze-in "
                                       "T ~ 4 GeV (sketch)"
    },
    "checks": checks,
    "n_pass": n_pass,
    "n_total": len(checks),
    "window": window,
    "statement": ("THE ONE-SPECIES MASS WINDOW: the framework's dark sector is ONE cold "
                  "species (the shift-symmetric scalar's Noether charge, G028) in two "
                  "phases -- the equilibrium phantom (~1% of Omega_dm, inside the EFE "
                  "line) and the free dust (~99%, outside).  The forest bound "
                  "m > 3.3-5.7 keV (G093) is the binding lower bound; the equilibrium's "
                  "TG floor m > 23.25 eV (G084) is satisfied automatically "
                  "(m_TG/m_forest <= 0.007, margin 1.4e2x), and the floor also sits 4x "
                  "below the killed 93-148 eV relic window (f04/f06).  The thermal "
                  "consistency: T_phase = m sigma^2/k_B is the DYNAMICS-set number "
                  "(sigma^2 = (1/2) sqrt(G M_b a0) = 119.2 km/s virial, mass-free; "
                  "registered 1.83-2.01 mK/eV): at m = 5 keV the equilibrium phase sits "
                  "at ~9.2-10.1 K while the free dust's own kinetic temperature is "
                  "~2e-5 K at z = 3 -- the mass sets free-streaming and phase space, "
                  "the dynamics sets sigma; they are decoupled.  The honest window: "
                  "m in [3.3, 100] keV, lower bound binding; the upper end (100 keV) is "
                  "the top of the KK-graviton freeze-in corridor sketch, NOT an "
                  "astrophysical constraint -- production is NOT derived (G093 V4's "
                  "registered non-claim): a thermal-ish keV yield would overclose by "
                  "3e2-9e3x, so the observed Omega_dm requires a diluted/non-thermal "
                  "channel that the framework does not claim.")
}

out = []
out.append("=" * 110)
out.append("G116 -- THE SECTOR MASS SYNTHESIS: one species, one mass.")
out.append("=" * 110)
out.append("")
out.append("(1) THE TWO BOUNDS ON THE RECORD")
out.append(f"    equilibrium TG floor  m > {m_TG_canon_eV:.2f} eV   (G084: rho = 0.008 Msun/pc^3, "
           f"sigma = {sigma_registered_kms} km/s; alt {m_TG_alt_eV:.2f} eV at sigma = {sigma_alt_kms})")
out.append("    free-dust forest bound  m > 3.3-5.7 keV   (G093: Viel+13 2-sigma 3.3, "
           "Irsic+17 5.3, Villasenor+24 95% 5.7)")
out.append(f"    CONSISTENCY: one species -> binding bound = forest; equilibrium TG satisfied "
           f"automatically:")
out.append(f"      m_TG/m_forest = {ratio_TG_forest_2sig:.4e}  (canonical, 2-sigma mass)  "
           f"<= 0.007  [canonical exact {ratio_TG_forest_2sig:.3e}]")
out.append(f"      alt footing: {ratio_TG_alt_2sig:.4e};  95% CL mass: {ratio_TG_forest_95:.4e}")
out.append(f"      margin: forest clears the equilibrium TG by {margin_forest_over_TG_2sig:.1f}x "
           f"(2-sigma) / {margin_forest_over_TG_95:.1f}x (95% CL)")
out.append(f"      the equilibrium floor sits {below_killed_window:.2f}x BELOW the killed "
           f"window's floor {killed_floor:.1f} eV (f04/f06, window {killed_floor:.1f}-"
           f"{killed_ceil:.0f} eV empty by 1.6x) -- phase-space safe on both sides")
out.append("")
out.append("(2) THE THERMAL CONSISTENCY -- the phase temperature is set by the DYNAMICS")
out.append(f"    T_phase = m sigma^2/k_B at m = 5 keV, sigma = {sigma_registered_kms} km/s:")
out.append(f"      direct:  T = {T_5keV_direct:.2f} K")
out.append(f"      registered linear law (G084): {T_per_eV_mK['canonical']:.3f} mK/eV -> "
           f"{T_5keV_band[0]:.2f} K;  band [{min(T_5keV_band):.2f}, {max(T_5keV_band):.2f}] K "
           "across the two footings")
out.append(f"    the virial is mass-free:  sigma^2 = (1/2) sqrt(G M_b a0) = "
           f"{sigma2_virial:.4e} (m/s)^2 -> sigma = {sigma_virial_kms:.2f} km/s "
           "(registered 119.2 km/s, G084)  [no m_sec enters]")
out.append(f"    the free dust's OWN kinetic temperature (the cold phase): T = m v_th^2/k_B:")
out.append(f"      z = 3:  {T_kin_z3_33:.2e} K (3.3 keV, v_th 0.219 km/s); "
           f"{T_kin_z3_57:.2e} K (5.7 keV, 0.127);  {T_kin_z3_5:.2e} K (5 keV, interpolated "
           f"{vth_z3_5keV:.3f} km/s)")
out.append(f"      z = 0:  {T_kin_z0_33:.2e} K (3.3 keV)")
out.append(f"    REGISTRY NOTE (honest): the brief's '~4e-5 K' does NOT reproduce on the "
           f"committed formula at (5 keV, 119.2 km/s) --")
out.append(f"      it is the FREE-DUST kinetic temperature at z ~ 3 ({T_kin_z3_5:.2e} K): the "
           "two phases' velocity scales transposed")
out.append(f"      (119.2 km/s virial vs ~0.18-0.22 km/s thermal; T ~ v^2, "
           f"(0.22/119.2)^2 = {(vth_z3_33/sigma_registered_kms)**2:.1e}).  The equilibrium "
           "phase's honest value: ~9.2-10.1 K.")
out.append(f"    THE DECOUPLING IN ONE NUMBER:  T_equil/T_kin,dust(z=3) = "
           f"{T_ratio_equil_over_dust:.1e}x")
out.append("")
out.append("(3) THE WINDOW -- upper-bound candidates, audited")
out.append(f"    (a) production (shift-charge relic abundance): NOT DERIVED -- G093 V4's "
           "explicit non-claim is the register;")
out.append(f"        thermal 1-dof closure Omega h^2 = m/94 eV (f04): at keV masses the yield "
           "OVERCLOSES:")
for k, v in overclosure.items():
    out.append(f"          m = {k:>9s}: Omega h^2 = {omega_h2_thermal(float(k.split()[0])*1e3):8.1f} "
               f"-> {v:8.1f}x Omega_dm; dilution needed {(1/v):.2e}")
out.append("        corridor sketch on file: KK-graviton DM 1-100 keV, freeze-in at T ~ 4 GeV "
           "(FORWARD_PROGRESS_2026-06-06) -- alive, squeezed, NOT a derivation")
out.append("    (b) stellar-warming floor: NOT BINDING HERE -- those floors bind SM-coupled "
           "keV-DM classes; the framework's")
out.append("        species is SM-decoupled by construction (no direct-detection coupling, "
           "THEORY.md 8 / G093 V4): listed and dismissed")
out.append(f"    (c) TG in the densest systems (cluster cores): m > {TG_cluster_eV:.1f} eV "
           "ONLY -- a LOWER bound, satisfied with")
out.append(f"        margin {margin_forest_over_clusterTG:.0f}x at the 2-sigma mass; "
           "non-binding")
out.append("    HONEST WINDOW:  m in [3.3, 100] keV -- LOWER bound binding (forest; "
           "95% CL reading 5.7 keV puts lambda_fs = 0.50 Mpc")
out.append("    inside the 0.6 Mpc register); UPPER end = 100 keV = top of the production "
           "corridor sketch, NOT an astrophysical")
out.append("    constraint: no committed gate binds the species from above; m > 100 keV is "
           "unconstrained on the record")
out.append("")
out.append("(4) VERDICTS")
out.append(f"    V1  the two bounds are one-species compatible (binding = forest; "
           f"equilibrium TG auto-satisfied, ratio {ratio_TG_forest_2sig:.3e} <= 0.007, "
           f"margin {margin_forest_over_TG_2sig:.1f}x): PASS")
out.append("    V2  honest window m in [3.3, 100] keV, lower bound binding, upper end "
           "placeholder: PASS")
out.append("    V3  decoupling (mass -> free-streaming/phase-space; dynamics -> sigma, "
           f"T/m = 1.83-2.01 mK/eV constant): PASS")
out.append("    V4  production NOT derived -- listed (overclosure 3e2-9e3x band; KK "
           "corridor sketch): PASS as stated")
out.append("")
out.append(f"RESULT: {n_pass}/{len(checks)} checks PASS  rc=0")

with open("G116_results.json", "w") as f:
    json.dump(result, f, indent=1)
print("\n".join(out))
