#!/usr/bin/env python3
"""targets_sm.py -- high-precision Standard-Model targets for the million-monkeys engine.

Values: PDG/CODATA-class, entered 2026-08-15 with GENEROUS sigmas where the entry is not
CODATA-exact.  T101 verifies internal consistency; ANY surplus result must re-verify its
target against the current PDG before escalation.  'field' notes whether the measured
quantity is (so far as known) algebraic-independent -- the corpus's number-field
obstruction (project_particle_numerology) is the standing PRIOR: searches are permitted,
claims must beat chance AND address the obstruction.
"""
SM_TARGETS = {
    "alpha_inv":     dict(v=137.035999177, s=2.1e-8,  note="CODATA22 inverse fine structure"),
    "alpha_s_MZ":    dict(v=0.1180,        s=0.0009,  note="strong coupling at M_Z"),
    "sin2thW_msbar": dict(v=0.23122,       s=4e-5,    note="weak mixing, MS-bar at M_Z"),
    "sin2thW_onsh":  dict(v=0.22305,       s=3e-4,    note="weak mixing, on-shell (VERIFY)"),
    "mW_over_mZ":    dict(v=0.88136,       s=2.5e-4,  note="W/Z mass ratio (VERIFY vs PDG avg)"),
    "mH_over_v":     dict(v=0.50872,       s=8e-4,    note="125.25/246.2196 (VERIFY)"),
    "yt_top":        dict(v=0.7009,        s=2.5e-3,  note="m_t/v (VERIFY)"),
    "mmu_over_me":   dict(v=206.7682827,   s=5e-6,    note="muon/electron mass"),
    "mtau_over_mmu": dict(v=16.8170,       s=1.5e-3,  note="tau/muon mass"),
    "mp_over_me":    dict(v=1836.15267343, s=1.1e-7,  note="proton/electron mass"),
    "mn_over_mp":    dict(v=1.00137841931, s=5e-10,   note="neutron/proton mass"),
    "koide_Q":       dict(v=0.666661,      s=7e-6,    note="Koide charged-lepton Q (POSITIVE CONTROL: engine must find 2/3)"),
    "ckm_lambda":    dict(v=0.22501,       s=7e-4,    note="Wolfenstein lambda (Cabibbo)"),
    "ckm_A":         dict(v=0.826,         s=0.015,   note="Wolfenstein A"),
    "ckm_rhobar":    dict(v=0.1591,        s=0.0094,  note="Wolfenstein rho-bar"),
    "ckm_etabar":    dict(v=0.3523,        s=0.0073,  note="Wolfenstein eta-bar"),
    "ckm_delta_rad": dict(v=1.144,         s=0.035,   note="CKM CP phase, radians (VERIFY)"),
    "pmns_s2_12":    dict(v=0.307,         s=0.012,   note="solar mixing sin^2"),
    "pmns_s2_23":    dict(v=0.558,         s=0.021,   note="atmospheric sin^2 (octant unresolved)"),
    "pmns_s2_13":    dict(v=0.02195,       s=5.8e-4,  note="reactor sin^2"),
    "pmns_delta_pi": dict(v=1.19,          s=0.22,    note="PMNS CP phase / pi (weak)"),
    "ns_scalar":     dict(v=0.9649,        s=0.0042,  note="scalar spectral index (Planck18)"),
    "omega_b_h2":    dict(v=0.02237,       s=1.5e-4,  note="baryon density (Planck18)"),
    "omega_c_h2":    dict(v=0.1200,        s=1.2e-3,  note="cold DM density (Planck18)"),
}
