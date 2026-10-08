#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg484_record.py -- the record table for CFG484 (data only, no physics).

Each row is a completion ("chassis") from the record, scored against the frozen gate list G1-G14 and the B-carrying
gates H1-H6 of FROZEN_CRITERIA.md. Every status cites the lane that sets it. Rules (frozen):
  FAIL  only where a committed lane, a recorded no-go (closure_map/ACTIONS_AND_NOGOS.md N1-N22) or a computation in
        CFG484 shows the gate fails within its scope;
  PASS  only where a committed lane computes it, CFG484 computes it, or a standard GR theorem applies (tag LIT-GR);
  NA    the gate's object does not exist in the completion (one-line proof in the note);
  LEN   passes only under a lenient reading the record lists as an owner call / stated uncertainty;
  COND  passes only under a stated, untested condition;
  UNT   untested.
Memory-only or summariser-only facts never upgrade a status to PASS. "[U]" marks astra-lane results (unreviewed).

The NC1 / NC2 rows are NOT here: their statuses come from the computations in cfg484_chassis_search.py.
"""

GATES_G = ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13", "G14"]
GATES_H = ["H1", "H2", "H3", "H4", "H5", "H6"]

GATE_NAMES = {
    "G1": "strong hyperbolicity + criterion B",
    "G2": "lapse / instantaneous-sector ellipticity",
    "G3": "F2a lapse kernel",
    "G4": "strong coupling",
    "G5": "negative-phantom-lobe health",
    "G6": "PPN alpha2",
    "G7": "PPN alpha1",
    "G8": "binary-pulsar dipole",
    "G9": "cosmological G / BBN",
    "G10": "G_N > 0",
    "G11": "radiative stability",
    "G12": "black-hole regularity (reading S)",
    "G13": "GW170817 c_T = c",
    "G14": "Cassini + Solar System",
    "H1": "law carried (declared kernel)",
    "H2": "messenger available",
    "H3": "attractor + support of the cold fluid",
    "H4": "switch OFF outside bound halos (legal term)",
    "H5": "fluid-baryon coupling only via gravity, no species",
    "H6": "a0-Lambda tie carried",
}


def S(code, note):
    return (code, note)


# ---- shared status blocks for the khronon chassis (CFG467 table, strict readings, alpha_c in L340's window) ----
_CHK_G = {
    "G1": S("PASS", "CFG292/XC2 B6: real speeds iff 0 < alpha_c < 2 (PROOF, linear frozen-coefficient); window inside"),
    "G2": S("PASS", "CFG294 S4b / CFG329: det = 4 N alpha k^4 > 0 for alpha_c > 0 (PROOF)"),
    "G3": S("PASS", "CFG294 S4c / CFG312: allowed for alpha_c in (0, 1/2) (PROOF)"),
    "G4": S("PASS", "XC1 A4: strict edge 1.8e-16..3.7e-16 below the window (NUM from LIT formula)"),
    "G5": S("PASS", "L340 H4: [9.624e-14, inf) strict (window edge = L340's estimate)"),
    "G6": S("PASS", "CFG291 exact alpha2: window <= 3.2e-9 (LIT bound)"),
    "G7": S("PASS", "alpha1 = -4 alpha_c (CFG291, L340 P1; KM3)"),
    "G8": S("PASS", "CFG291/CFG311: 625/625 window points (NUM with LIT formulas)"),
    "G9": S("PASS", "L350 G1/G5: |alpha|/2 < 0.1 on the leaf-average branch"),
    "G10": S("PASS", "L350 G1 / CFG320 K4: G_N = G/(1 - alpha/2) > 0"),
    "G11": S("LEN", "CFG320/CFG467: strict (no hierarchy) only in the 3/81 sliver c2 >= 0.038, alpha <= 1.18e-13; "
                    "full window needs the Pospelov-Shang hierarchy reading"),
    "G12": S("FAIL", "CFG318/CFG319 count 4 vs 5 for every alpha_c > 0 (+RB2019, FHB2021 LIT): no fully regular "
                     "moving hole; CFG467 strict set {0}"),
    "G13": S("PASS", "beta = 0 forced by c_T = 1 (CFG467 'GW170817 fixes beta only')"),
    "G14": S("PASS", "KM3 gamma = beta = 1; CFG357 Q2 within 2 sigma for xi >= 0.027 pc; L340 S1 Saturn-monopole floor "
                     "0.045 pc (heat filter xi declared)"),
}
_CHK_H = {
    "H1": S("PASS", "L340: static QUMOND sector with nu_mono (needs C >= 0, L340 H)"),
    "H2": S("PASS", "CFG373 G1: the lapse gradient IS the total field; P2 target local in it, zero constants"),
    "H3": S("COND", "CFG373 G3: reaction sink only if relaxation induces K ~ Gamma/c (assumed); CFG381: khronon alone "
                    "gives no force, needs a fluid-khronon coupling (+1); CFG472/473: support in the transition is "
                    "nonlocal"),
    "H4": S("COND", "no committed legal field-reading gate on this chassis (N10 flux switch, N14 varied gate, N15 "
                    "theta-gate ghost); only a fluid-sector first-order switch (CFG478 legal, NR; CFG482 SED PASS) "
                    "remains, chassis-independent and not covariant"),
    "H5": S("PASS", "fluid feels gravity of all real mass only (working model); no species"),
    "H6": S("PASS", "XR20 T1 Henneaux-Teitelboim tie: TIED (kappa chosen), 0 local DOF, +1 global"),
}


def _merge(base, **over):
    d = dict(base)
    d.update(over)
    return d


_UNT_G = {g: S("UNT", "not computed on the record") for g in GATES_G}
_UNT_H = {h: S("UNT", "not computed on the record") for h in GATES_H}

ROWS = [
    dict(id="R01", name="C-H/K chassis, strict (L340 khronon, beta = 0)",
         sources="L340, CFG467 (and its sources CFG291/292/294/312/318/319/320/329, XC1/XC2, L350)",
         G=_CHK_G, H=_CHK_H,
         constants=dict(n=3, names="alpha_c, c_2, xi (heat-filter width), declared; + switch constants",
                        counted_on_record=True)),

    dict(id="R02", name="C-H/K at alpha_c = 0 (minimal Horava)",
         sources="CFG467 G1-G5, XC1, XC2, CFG319 C1",
         G=_merge(_CHK_G,
                  G1=S("FAIL", "CFG292: no real speeds at alpha_c = 0; Jacobson-Pulakkat 2025 Cauchy problem fails (XC2)"),
                  G2=S("FAIL", "CFG294 S4b: det = 4 N alpha k^4 = 0"),
                  G3=S("FAIL", "CFG467 G3 excludes {0}"),
                  G4=S("FAIL", "XC1: M_SC = sqrt(alpha) M_P c_s collapses at alpha_c = 0"),
                  G5=S("FAIL", "L340 H4: inertia negative at the top k for alpha = 0 (PROOF, large-k limit)"),
                  G8=S("UNT", "CFG467: alpha <= 0 untested for pulsars"),
                  G11=S("UNT", "CFG467: not shown allowed at 0"),
                  G12=S("PASS", "CFG319 control C1: stealth maximal-slicing hole fully regular at alpha_c = 0")),
         H=_CHK_H,
         constants=dict(n=2, names="c_2, xi; + switch", counted_on_record=True)),

    dict(id="R03", name="C-H/K with reading W for black holes (CFG467 option 1)",
         sources="CFG467 (option C of CFG319 accepted; owner call)",
         G=_merge(_CHK_G,
                  G11=S("PASS", "restricted to CFG320's sliver c2 >= 0.038, alpha in [9.624e-14, 1.18e-13] (strict)"),
                  G12=S("LEN", "reading W: regular outside the universal horizon, integrable x^-0.382 singularity on it, "
                               "exterior imprint <= 3e-13 (CFG319 option C); owner call")),
         H=_CHK_H,
         constants=dict(n=3, names="alpha_c, c_2, xi; no new constant", counted_on_record=True)),

    dict(id="R04", name="C-H/K plus a Horava UV sector M_* (CFG467 option 2)",
         sources="CFG467 option 2; CFG320 hierarchy reading",
         G=_merge(_CHK_G,
                  G11=S("COND", "if M_* <= 9.9e8 GeV realises CFG320's hierarchy (one constant for G11 and G12); "
                                "untested"),
                  G12=S("UNT", "UH regularisation by higher spatial derivatives: argument in CFG319, never computed")),
         H=_CHK_H,
         constants=dict(n=4, names="alpha_c, c_2, xi, M_*", counted_on_record=False)),

    dict(id="R05", name="Candidate B's current working model on C-H/K (settling + khronon-lapse messenger)",
         sources="WORKING_MODEL_SETTLED_PHANTOM_2026-10-06, CFG373, CFG381, CFG472, CFG473 (CFG462/CFG483 results "
                 "uncommitted: not cited)",
         G=_merge(_CHK_G,
                  G1=S("UNT", "chassis part PASS (CFG292); the coupled fluid-khronon settling system's principal symbol "
                              "is not computed")),
         H=_merge(_CHK_H,
                  H3=S("COND", "CFG373 G3 sink assumption K ~ Gamma/c; CFG381 +1 coupling; CFG472 target not a "
                               "hydrostatic equilibrium in the transition; CFG473 holding force nonlocal")),
         constants=dict(n=4, names="alpha_c, c_2, xi, lambda_x (fluid-khronon coupling, CFG381); + switch",
                        counted_on_record=True)),

    dict(id="R06", name="V0 covariant action (CV1-CV4; region kernel; MS5 cap)",
         sources="chk_v0_2026 CV1-CV4, dark_energy_2026 DE12/DE13, mond_sector_gate_2026 MS1-MS5 (N14)",
         G=_merge(_CHK_G,
                  G1=S("FAIL", "DE12/DE13 (N14): the varied region gate gives a k^0 negative pressure on baryons, "
                               "c_gate 1500-3700 km/s vs gas 37-117 km/s (gradient instability); no harmless repair; "
                               "the data passes use a prescribed mask, which is not an action")),
         H=_merge(_CHK_H, H4=S("FAIL", "N14: the gate as a varied term is obstructed (DE12/13, XR15)")),
         constants=dict(n=None, names=">= 9 declared (alpha_c, c_2, xi, m, sigma, x_c0, p, w, v_cap) + epsilon fitted",
                        counted_on_record=False)),

    dict(id="R07", name="Derivation-chain action (FP7/FP14 root + XR20 tie + H_K1 + FK1)",
         sources="closure_map/ACTIONS_AND_NOGOS row 4; derivation_chain_2026 FP2/FP7/FP14/FP22/FP23; XR20; XR25",
         G=_merge(_UNT_G,
                  G7=S("UNT", "alpha1 = -4 alpha_c - 8C/(1+C) (closure map); C at Solar wavenumbers not read here"),
                  G12=S("FAIL", "XR25: the c2 -> infinity limit is singular at universal horizons (closure map 'OPEN'); "
                                "alpha_c > 0 also meets CFG319's count"),
                  G13=S("PASS", "c_T = 1 (FP2, FP7, XR25)")),
         H=_merge(_UNT_H,
                  H1=S("PASS", "P2 exact in spherical symmetry (FP7 R7d)"),
                  H4=S("FAIL", "no ownership; band-pass separator squeezed: KiDS with web field +111..+153 vs +9 (FP23)"),
                  H6=S("PASS", "XR20 T1 TIED")),
         constants=dict(n=None, names="L_Lambda 2.9 Mpc declared, c_y chosen after scoring, epsilon fitted, alpha_c",
                        counted_on_record=False)),

    dict(id="R08", name="AeST v9 embedding / FC-AeST",
         sources="closure_2026/V9_PPN_KILL_VERDICT.md (N7)",
         G=_merge(_UNT_G,
                  G7=S("FAIL", "N7: alpha1 = -2(K_B + 2) on the healthy locus 0 < K_B <= 0.25 (linearised about the "
                               "cosmological background; solar background unchecked)"),
                  G6=S("UNT", "FC-AeST + c2*: alpha2 = 1/lam_s + 2/(K_B lam_s^2) (N7); value not re-read here")),
         H=_merge(_UNT_H, H3=S("FAIL", "closure map: AeST needs dust at full Omega_dm; does not explain a0")),
         constants=dict(n=None, names="K_B, lambda_s, mu, kinetic function", counted_on_record=False)),

    dict(id="R09", name="FC-KH khronometric f(a)",
         sources="closure_2026/fc_kh_terminal/FC_KH_PAPER_vNEXT.md (N6)",
         G=_merge(_UNT_G,
                  G14=S("FAIL", "N6 (yq)' theorem: radial stability iff (yq)' >= 0, and exact-GR UV forces q = 0: the "
                                "Cassini-vs-ghost pincer (one horn fails Cassini, the other is a ghost)")),
         H=_UNT_H,
         constants=dict(n=None, names="f(a)", counted_on_record=False)),

    dict(id="R10", name="Blanchet-Skordis khronon dust (BS24)",
         sources="bs_khronon_2026 BSK1, BSX1, BSX3 (N8)",
         G=_merge(_UNT_G,
                  G14=S("UNT", "BSK1: hiding the inner instability above ~1e3 a0 meets the ephemeris bound "
                                "(Cassini-vs-ghost pincer returns; BS24 has no filter); not scored as a number")),
         H=_merge(_UNT_H,
                  H3=S("FAIL", "BSK1: with BS24's GR recovery the static halo is unstable wherever the phantom falls, "
                               "rate^2 = (2 + 2/n) GM/r^3 (inner MW e-fold 1-4 Myr); N8 BSX3 I1: for ANY K, "
                               "mu_eff^2 = k_J^2 (1 + c_ad^2), KiDS needs 1/k_J <= 0.22 Mpc vs MOND lensing "
                               "1/mu_eff >= 10 Mpc (x46); dust budget ends at 0.13-0.67 Mpc")),
         constants=dict(n=None, names="K(Q), mu, lambda_D", counted_on_record=False)),

    dict(id="R11", name="Astra CA4/CA5 common action [U]",
         sources="common_action_2026_09_26/action/FINAL_ACTION.md; AS233, AS234, AS236, AS239 (unreviewed) (N22)",
         G=_merge(_UNT_G,
                  G7=S("FAIL", "[U] AS233: alpha1 = 4(alpha + 2 c2)/(2 - c2), O(1) at the reference cell"),
                  G6=S("UNT", "[U] AS234: alpha2 extraction obstructed (R = -2 rho/7)"),
                  G13=S("UNT", "[U] AS239-240: c_T = N/b"),
                  G9=S("UNT", "[U] AS236/AS252: G_cosm/G_N = c_N")),
         H=_merge(_UNT_H,
                  H4=S("FAIL", "FINAL_ACTION: full-on state 'impossible on the declared compact leaf', L361 screening "
                               "absent, gate not bound-only"),
                  H6=S("FAIL", "FINAL_ACTION section 1: a0-vacuum 'an optional input, not a consequence'")),
         constants=dict(n=None, names="alpha, c2, c_N, ell, b, five carrier masses/couplings", counted_on_record=False)),

    dict(id="R12", name="Astra IC20-IC28 integrable clock",
         sources="closure_map row (IC28; MUTATE not checked)",
         G=_merge(_UNT_G, G1=S("UNT", "lapse degeneration reported; 'full theory OPEN'")),
         H=_UNT_H,
         constants=dict(n=None, names="m, kappa, U(u^2)", counted_on_record=False)),

    dict(id="R13", name="Generated phantom GP0-GP5 + vacuum-gated L357-L361 (non-relativistic)",
         sources="generated_phantom_2026 GP1-GP5; g03_audit_2026 L357-L361, L363; paper34_audit P34d",
         G={g: S("UNT", "no relativistic embedding of its own; the record's embedding is V0 (R06)") for g in GATES_G},
         H=_merge(_UNT_H,
                  H3=S("FAIL", "L363/GP3: private phantom + LCDM-like dark component fails cosmic shear (R 1.5-4.7); "
                               "GP5: carrier still in galaxies at z = 2.5 (+0.82..+1.05 dex)")),
         constants=dict(n=None, names="lambda (free, BK2), thresholds, p, carrier kick/decay", counted_on_record=False)),

    dict(id="R14", name="Dark-energy gate DE1-DE13 (gate as a varied term)",
         sources="dark_energy_2026 DE7, DE12, DE13 (N14)",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "N14: a threshold gate flat at both ends has W'' of both signs; the instability lands on "
                               "what the gate reads (metric k^4, DE7; baryons, DE12); DE13 no harmless repair")),
         H=_merge(_UNT_H, H4=S("FAIL", "N14")),
         constants=dict(n=None, names="gate width, x_c0, p", counted_on_record=False)),

    dict(id="R15", name="MOND-sector gate MS1-MS5 (non-relativistic; cap as action term)",
         sources="mond_sector_gate_2026 MS1-MS5",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "MS5: the kappa-cap's fourth-order bracket B[W''U + W'/2] changes sign in the layer, so "
                               "DE7's k^4 repair is still needed (unrepaired = unstable)")),
         H=_merge(_UNT_H, H4=S("COND", "MS1-MS5: switch on baryons + cap ~325 km/s is a design target; mechanism open")),
         constants=dict(n=None, names="v_cap (declared), (v_cap/c)^2 = 1.18e-6, x_c0, p, w", counted_on_record=False)),

    dict(id="R16", name="FRIED_CHICKEN frame flip (EH on the matter metric; dark sector on g)",
         sources="FRIED_CHICKEN.md rows 1-10 + banner; qwen_claude_field_theory/closure_2026/frame_flip_2026.py",
         G=_merge(_UNT_G,
                  G1=S("COND", "row 7: no ghost, no gradient instability, no Cherenkov (K'' > 0 over 45 decades); full "
                               "principal symbol not computed"),
                  G13=S("PASS", "frame_flip A1: gravitons and photons share g~, c_T = c_gamma identically"),
                  G14=S("COND", "rows 4-5: monopole 4e-28 x Mars budget, Q2 0.08-0.21 x ceiling, on the mu_10 kernel "
                                "(not recomputed on nu_mono)")),
         H=_merge(_UNT_H,
                  H3=S("UNT", "row 10 (amplitude law) OPEN; local-EOS / baryon-coupled-pressure / local-selection "
                              "routes excluded (collapse_2026, local_selection_2026)"),
                  H2=S("FAIL", "banner: the g_b, grad g_b construction from a local covariant action without an "
                               "independent dark density is fourth order with a ghost (dark_sector_honesty_2026)")),
         constants=dict(n=None, names="B (disformal), K(X) of the dark field", counted_on_record=False)),

    dict(id="R17", name="GR + dark field, no MOND field (CFG2/5/9/10/FG004; CFG43/44)",
         sources="CFG2_A, CFG5, CFG9, CFG10, CFG7_groundstate_fg004, CFG43, CFG44 (N20); closure_map row",
         G="GR_CHASSIS",   # filled by cfg484_chassis_search.py with the same GR-chassis block as NC1 (same gravity
                           # sector), with G1 for the full system UNT (no fluid dynamics specified on the record)
         H=_merge(_UNT_H,
                  H1=S("PASS", "CFG9: P2 the only locally virialised point-mass law; CFG10 (ii) within 0.002-0.003 dex "
                               "of P2 on SPARC"),
                  H2=S("FAIL", "CFG44 B3: local closures excluded (far-shell theorem); the spherical tidal closure is "
                               "local but discs differ 3-15x; no messenger specified"),
                  H3=S("FAIL", "CFG44: every EOS/local/action closure excluded under GR + real mass; CFG5 SPARC "
                               "0.164/0.160 vs 0.145/0.142 dex, 2 load-bearing fails"),
                  H6=S("PASS", "CFG43 existence result: the a0-Lambda tie written into the fluid sector (Lambda "
                               "global, no new local DOF, a0 flat), kappa chosen; its scoped no-go is about the "
                               "barotropic saturating cap as the law's producer (needs nu*), not the tie")),
         constants=dict(n=None, names="none declared (principles only, no Lagrangian)", counted_on_record=False)),

    dict(id="R18", name="Superfluid dark matter, Berezhiani-Khoury (door 4)",
         sources="CFG122 (b7d41c302), referee CFG154",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "CFG122 G5.1: the MOND-carrying branch X < 0 has c_s^2 = 2X/m < 0 (gradient "
                               "instability; 1 kpc mode e-folds in ~4.5 Myr at m = 1 eV)"),
                  G14=S("FAIL", "CFG122 G5.4: unscreened 10.9/12.0 x Cassini, 6e8 x ephemeris; a0-line reading "
                                "ephemeris 3.9e4 x; phase-boundary screening impossible")),
         H=_merge(_UNT_H,
                  H3=S("FAIL", "CFG122 Branch S G1.1: 0/3600 cells reach the target"),
                  H5=S("FAIL", "direct phonon-baryon coupling (the force ontology; violates the working model's rule)")),
         constants=dict(n=3, names="m, alpha/Lambda, thermalisation rate (CFG122 G4)", counted_on_record=True)),

    dict(id="R19", name="Dipolar dark matter / gravitational polarisation (door 3)",
         sources="CFG121 (16fca9acd), referee CFG157",
         G=_merge(_UNT_G,
                  G1=S("COND", "CFG121 G5 S2: V_U passes; V_B is a ghost only in a relativistic completion (untested)"),
                  G14=S("COND", "CFG121 S4: uncapped monopole a0/2 (468x the line); safe only through the medium-density "
                                "cap, which fails G1c")),
         H=_merge(_UNT_H,
                  H3=S("FAIL", "CFG121 G1/G1c/G2: medium budget needs Q^2/kappa_I >= ~140 vs <= 0.16/1.2 from growth")),
         constants=dict(n=2, names="Q*, kappa_I* (CFG121 G4)", counted_on_record=True)),

    dict(id="R20", name="BIMOND (door 13)",
         sources="CFG232",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "CFG232 G5a: ghost for 13a/13b-i/13b-ii (reproduction of WF2/L70)"),
                  G14=S("FAIL", "CFG232 G5b: Q2 fails (a property of the bare law), also for 13c")),
         H=_merge(_UNT_H, H3=S("FAIL", "CFG232 G1-C fails for every sub-variant")),
         constants=dict(n=None, names="interaction function (by inversion)", counted_on_record=False)),

    dict(id="R21", name="Covariant emergent gravity (door 12)",
         sources="CFG231",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "CFG231 A3: a vector with an attractive static force needs a wrong-sign (ghost) kinetic "
                               "term"),
                  G14=S("FAIL", "CFG231: K1 Solar-System tail Q2 = 6.1e3 x the bound")),
         H=_merge(_UNT_H, H3=S("FAIL", "CFG231: G1 fails for all eight variants")),
         constants=dict(n=None, names="elastic/vector coefficients", counted_on_record=False)),

    dict(id="R22", name="Mimetic (door 10)",
         sources="CFG124, referee CFG152",
         G=_merge(_UNT_G,
                  G1=S("FAIL", "CFG124: classes C, D, E1 fail health; class A healthy but carries no coupling")),
         H=_merge(_UNT_H, H3=S("FAIL", "CFG124 G1: no stationary state; target missed for A-D and E")),
         constants=dict(n=None, names="higher-derivative coefficients", counted_on_record=False)),

    dict(id="R23", name="Nonlocal metric Deser-Woodard / RR (door 9)",
         sources="CFG123, referee CFG153",
         G=_UNT_G,
         H=_merge(_UNT_H, H3=S("FAIL", "CFG123 G1-A: |rho_eff/rho_target| <= 6e-11 (shortfall >= 1.65e10)")),
         constants=dict(n=None, names="m (RR mass)", counted_on_record=False)),

    dict(id="R24", name="Modified-inertia field theory (baryon 4-acceleration dressing)",
         sources="real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md section 5.1; TOE map wall 2",
         G=_merge(_UNT_G,
                  G1=S("UNT", "TOE map wall 2: Milgrom 1994, MI with both limits must be time-nonlocal; no covariant "
                              "completion of dS-Unruh MI exists"),
                  G14=S("FAIL", "Reading A: a constant a0/2 = 4.68e-11 (canon) at every planet, excluded 1017x "
                                "(Mercury) to 33429x (Mars) by INPOP/EPM; the gated version is a separate mitigation")),
         H=_merge(_UNT_H,
                  H5=S("FAIL", "MOND as baryon inertia (force ontology); CFG447: an EFE-blind force is excluded by "
                               "DR3 (7.7 sigma)")),
         constants=dict(n=None, names="kernel K, gate omega_c (gated version)", counted_on_record=False)),

    dict(id="R25", name="Closed families: condensate/DBI v9 dark sector (N9); CQ gravity (L313/L314)",
         sources="condensate_pincer_2026 (N9, memory-level); L313/L314",
         G=_UNT_G,
         H=_merge(_UNT_H,
                  H3=S("FAIL", "N9: charge dust cannot be CMB/forest-cold and absent from galaxies; CQ gravity closed as "
                               "the phantom source (L313/L314)")),
         constants=dict(n=None, names="-", counted_on_record=False)),
]
