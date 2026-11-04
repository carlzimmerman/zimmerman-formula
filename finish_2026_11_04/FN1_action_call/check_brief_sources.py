"""FN1 check_brief: the checked fragments. Each row is (fragment in DECISION_BRIEF.md, source file relative to the repo root,
literal in that source). Criteria 72f9d70fd6. kappa = 1/2 FITTED; not theory closed."""
Q = "rebuild_2026_10_22/"; C = "campaign_fresh_gravity/"; P = "qwen_claude_field_theory/papers_2026/"; FN = "finish_2026_11_04/FN1_action_call/"
V3S = "covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md"; C6P = Q + "C6P_cassini_high_precision/README.md"; AX1 = Q + "AX1_action_for_law/README.md"
P67 = P + "PAPER67_galaxy_law_and_what_it_leaves_2026.tex"; P58 = P + "PAPER58_doors_push_2026.tex"; ADD = "hunt_2026/SUPPORT_BRIEF_FOR_ASTRA_2026-09-04_ADDENDUM.md"
B = FN + "FN1b_fixed_length_static/"; SM = B + "fn1b_small.out"; MWC = B + "fn1b_mw_canonical.out"; MWA = B + "fn1b_mw_alt.out"; LAB = B + "fn1b_label.out"; CR = B + "FROZEN_CRITERIA.md"
L = [
 # header and footings
 ("canonical a0 = 9.3603e-11", Q + "THEORY_STATEMENT_2026-10-26.md", "9.3603"), ("alt 1.1312e-10", Q + "THEORY_STATEMENT_2026-10-26.md", "1.1312"),
 ("requirement 12", P67, "12 & have an action"),
 # bottom line and option (a)
 ("1.69–5.18× Hees", AX1, "1.69–5.18× Hees"),
 ("rms 0.054 / 0.054 dex", V3S, "rms 0.054 / 0.054 dex"),
 ("clean PASS on both footings", C6P, "Solar-System gate is a clean PASS on both footings"),
 ("≥ 4.85e7 inside Hees 9.0e-27", C6P, "≥ 4.85e7 inside Hees 9.0e-27"), ("≥ 5.70e7 (Hees)", C6P, "≥ 5.70e7 (Hees)"),
 ("Mars 0.173 of bound at 24 pc", C6P, "Mars 0.173 of bound at 24 pc"),
 ("≤ 3.2e-14 of the double pulsar", V3S, "≤ 3.2e-14 of the double pulsar"),
 ("closes with 3 DOF", V3S, "closes with 3 DOF"),
 ("**UNDECIDED, reading PASS**", AX1, "**UNDECIDED, reading PASS**"),
 ("1.5–1.7 × the law in 0.3–1 Mpc", V3S, "1.5–1.7 × the law in 0.3–1 Mpc"),
 ("σ₈/σ₈,dust 0.003–0.005", V3S, "σ₈/σ₈,dust 0.003–0.005"),
 ("μ_K ≥ 1.84e8 h/Mpc", V3S, "μ_K ≥ 1.84e8 h/Mpc"),
 ("Antlia II 24σ, MW ultra-faints 12.6σ", V3S, "Antlia II 24σ, MW ultra-faints 12.6σ"),
 ("K_z(1.1 kpc) 92–97 vs 66.4 ± 2.2", V3S, "K_z(1.1 kpc) 92–97 vs 66.4 ± 2.2"),
 ("|s₁ − s₂| < 7e-7", V3S, "|s₁ − s₂| < 7e-7"),
 ("L★ ≥ 21.7 / 22.9 pc", V3S, "L★ ≥ 21.7 / 22.9 pc"),
 ("**≥ 24.0 pc**", C + "CFG820_stiffness_from_globulars/README.md", "**≥ 24.0 pc**"), ("≥ 24.7 pc", C + "CFG820_stiffness_from_globulars/README.md", "≥ 24.7 pc"),
 ("5.75–22 pc", C + "CFG821_stiffness_from_dsph/README.md", "5.75–22 pc"), ("Draco 9.6 vs 4.6", C + "CFG821_stiffness_from_dsph/README.md", "Draco 9.6 vs 4.6"),
 ("c² √(Λ/32π)", V3S, "c² √(Λ/32π)"),
 ("L★ of at least 24 pc", C + "CFG820_stiffness_from_globulars/README.md", "**≥ 24.0 pc**"),
 # option (b) background
 ("L*² = 2 r_M ℓ_γ", C + "CFG691_stiffness_window/README.md", "L*² = 2 r_M ℓ_γ"),
 ("Theorem 8", ADD, "Theorem 8"),
 ("margin 2.8e7, 4.0e7", Q + "AS3_ppn_and_khronon_scalar/README.md", "margin 2.8e7, 4.0e7"),
 ("sigma8 ratio 0.0757, 0.0817", Q + "AS3_ppn_and_khronon_scalar/README.md", "sigma8 ratio 0.0757, 0.0817"), ("line 0.95", Q + "AS3_ppn_and_khronon_scalar/README.md", "line 0.95"),
 # option (c)
 ("2.44–4.59× the Hees line (canonical)", P58, "2.44--4.59$\\times$ the Hees et al.\\ (2014) $2\\sigma$ line (canonical)"),
 ("2.85–5.19× (alt)", P58, "2.85--5.19$\\times$ (alternative)"),
]
# phrases quoted from the record (no number, but the quote must be exact)
L += [
 ("This is law S", V3S, "This is law S"), ("STRUCTURAL GAP", V3S, "STRUCTURAL GAP"),
 ("As a galaxy-scale law, v3s is complete and passes", V3S, "As a galaxy-scale law, v3s is complete and passes"),
 ("As a theory of gravity and cosmology,\nv3s fails", V3S, "As a theory of gravity and cosmology, v3s fails"),
 ("the cold-dust abundance (an initial condition)", V3S, "the cold-dust abundance (an initial condition)"),
 ("It has no action and supplies no dust-like term for the CMB", P67, "It has no action and supplies no dust-like term for the CMB"),
 ("nonlinear code started from a cap-consistent state", V3S, "nonlinear code started from a cap-consistent state"),
 ("UNDECIDED under the frozen rule", V3S, "UNDECIDED** under the frozen rule"),
 ("PASS on a condition", V3S, "Binary pulsars | PASS on a condition"), ("strong-field sensitivity uncomputed", V3S, "strong-field sensitivity uncomputed"),
 ("NOTHING FORCED", Q + "KF1_argon_kappa_routes/README.md", "NOTHING FORCED"),
 ("INCONSISTENT", C + "CFG821_stiffness_from_dsph/README.md", "INCONSISTENT"),
 ("the same mechanism as L★ in another form", AX1, "the same mechanism as L★ in another form"), ("no action for it\n  exists", AX1, "no action for it exists"),
 ("localising the filter adds a propagating mode", ADD, "localising the filter adds a propagating mode"),
 ("v3's scalar pair", Q + "AS3_ppn_and_khronon_scalar/README.md", "v3's scalar pair"),
 ("None is selected, and the a0 sector's action stays open.", P67, "None is selected, and the $a_0$ sector's action stays open."),
 ("The a₀ sector's action stays open", Q + "OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md", "The a₀ sector's action stays open"),
 ("AN1's rerun and AN2 both read NO VERDICT", Q + "AN1_aest_nonlinear_dust/README.md", "Rerun landed: `README_V3.md`, NO VERDICT, numbers only"), ("AN1's rerun and AN2 both read NO VERDICT", Q + "AN2_aest_3d_fold/README.md", "NO VERDICT, numbers only"),
]

# header
L += [("item 1 of the finish push", "finish_2026_11_04/README.md", "| 1. Action call | `FN1_action_call/`"),
      ("Requirement 12", P67, "12 & have an action"), ("row 12", P67, "12 & have an action"),
      ("open; 0 of 717 in AS2's Tier A", P67, "have an action & open; 0 of 717 in AS2's Tier A; unscreened classes fail $Q_2$ (AX1); only v3s's screen passes the Solar System (C6P)")]
# FN1b, option (b): bottom line and text
L += [("0.024 to 2 kpc", CR, "L ∈ {0.024, 0.1, 0.25, 0.5, 1.0, 2.0} kpc"),
      ("The Milky Way passes only at 2 kpc", LAB, "R  [alt      ] L 2.000 kpc: T0   38 cells"), ("The Milky Way passes only at 2 kpc", LAB, "R  [canonical] L 2.000 kpc: T0    2 cells"),
      ("the dwarfs read 6/24", SM, "T2 [canonical] L 2.000 kpc: R E1 6/24"), ("the dwarfs read 6/24", SM, "T2 [alt] L 2.000 kpc: R E1 6/24"),
      ("0.1 kpc, where no Milky Way cell passes", LAB, "R  [canonical] L 0.100 kpc: T0    0 cells"), ("0.1 kpc, where no Milky Way cell passes", LAB, "R  [alt      ] L 0.100 kpc: T0    0 cells"),
      ("MW cells of 1,375", MWC, "in-prior cells 1375 (KT13/KT14: 1375)"), ("line 15/24", CR, "T2 passes at ≥ 15/24 (CZ2's line)"),
      ("(NOT EVALUABLE at L = 0.024 kpc)", LAB, "LABEL SO [canonical]: UNDECIDED (NOT EVALUABLE at L = 0.024 kpc)"),
      ("KT14's smoothing test at 24 pc reads 1.5e-02", MWC, "KT14 C3 xi 0.024: radial max rel 1.5e-02"), ("KT14's smoothing test at 24 pc reads 1.5e-02", MWA, "KT14 C3 xi 0.024: radial max rel 1.5e-02"),
      ("against its 1e-3 line", CR, "(line 1e-3)"),
      ("SPARC at 24 pc (4.7e-01)", SM, "SPARC max 4.7e-01"),
      ("peak RSS 1.31 GiB", MWA, "peak RSS 1.31 GB"), ("a 1 GB target", CR, "a 1 GB RSS target")]
# FN1b table rows (form R; canonical / alt)
R1 = "| 0.024 | 0 / 0 | 18 / 18 | NOT EVALUABLE (V4) | 7.41e-10 / 8.68e-10 | FAILS: T0 |"
R2 = "| 0.1 | 0 / 0 | 16 / 16 | SURVIVES SPARC | 1.02e-11 / 1.20e-11 | FAILS: T0 |"
R3 = "| 0.25 | 0 / 0 | 14 / 14 | SURVIVES SPARC | 6.55e-13 / 7.68e-13 | FAILS: T0, T2 |"
R4 = "| 0.5 | 0 / 0 | 12 / 13 | SURVIVES SPARC | 8.19e-14 / 9.60e-14 | FAILS: T0, T2 |"
R5 = "| 1.0 | 0 / 0 | 9 / 10 | HURT | 1.02e-14 / 1.20e-14 | FAILS: T0, T2, T3 |"
R6 = "| 2.0 | 2 [GRID-DEPENDENT] / 38 | 6 / 6 | FAILS SPARC | 1.28e-15 / 1.50e-15 | FAILS: T2, T3 |"
for row, L_, kp, d1, d2, sp, q1, q2, lab in ((R1, "0.024", "0.024", 18, 18, "R rms 0.2469 d +0.0778 med -0.0309 FAILS SPARC", "7.41e-10", "8.68e-10", "FAILS: T0"),
                                           (R2, "0.100", "0.1", 16, 16, "R rms 0.1697 d +0.0006 med +0.0192 SURVIVES SPARC", "1.02e-11", "1.20e-11", "FAILS: T0"),
                                           (R3, "0.250", "0.25", 14, 14, "R rms 0.1691 d -0.0000 med +0.0273 SURVIVES SPARC", "6.55e-13", "7.68e-13", "FAILS: T0, T2"),
                                           (R4, "0.500", "0.5", 12, 13, "R rms 0.1722 d +0.0031 med +0.0317 SURVIVES SPARC", "8.19e-14", "9.60e-14", "FAILS: T0, T2"),
                                           (R5, "1.000", "1.0", 9, 10, "R rms 0.1866 d +0.0175 med +0.0450 HURT", "1.02e-14", "1.20e-14", "FAILS: T0, T2, T3"),
                                           (R6, "2.000", "2.0", 6, 6, "R rms 0.2298 d +0.0607 med +0.0677 FAILS SPARC", "1.28e-15", "1.50e-15", "FAILS: T2, T3")):
    L += [(row, SM, f"T2 [canonical] L {L_} kpc: R E1 {d1}/24"), (row, SM, f"T2 [alt] L {L_} kpc: R E1 {d2}/24"),
          (row, SM, f"({q1} x ceiling"), (row, SM, f"({q2} x ceiling"), (row, LAB, f"L {L_} kpc: T0"), (row, LAB, f"->  {lab}")]
    if L_ != "0.024": L += [(row, SM, sp)]
L += [(R1, SM, "R  [canonical] L 0.024: T1 P T2 P T3 F T4 P  NOT EVALUABLE: ['T3']"), (R6, LAB, "R  [alt      ] L 2.000 kpc: T0   38 cells"), (R6, LAB, "[GRID-DEPENDENT]")]
