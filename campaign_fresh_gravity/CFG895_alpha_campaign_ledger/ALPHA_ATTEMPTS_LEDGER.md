# Ledger of attempts on the fine-structure constant (CFG895, 2026-10-20)

**Nothing in this ledger derives alpha.** Alpha remains an INPUT and kappa = 1/2 remains FITTED. The Standard-Model mass and coupling sector is walled.

This ledger lists every attempt on 1/alpha = 137.035999177 (CODATA 2022, Thomson limit) found in the repository, grouped by mechanism family. The search ran through:

* `real_research/alpha_principle_2026/` and `real_research/alpha_schwinger_2026/`;
* the Lean files in `fable_independent_2026/lean_2026/`;
* `fine_structure_puzzle/` (FSP-000 to FSP-011) and the untracked root files `FINE_STRUCTURE_HANDOFF_TO_CLAUDE.md` and `..._SOURCES.json`;
* `project_atomos/`, `qwen_38_experiment/`, `opus_48_extended_research/`, `sonnet55_push/`, `data_assembly/`, `hy4_push/`, `sol61_push/`, `real_research/reviews/` and `real_research/*.md`;
* the legacy quarantine `ai_slop/`;
* memory-referenced lanes (AH1–AH8, AS1–AS4, FSP-xxx, particle numerology).

Thirty other directories had no attempt, only uses of the word or of alpha as an input: every gemini, grok, glm, hermes, nemotron, openai, deepseek, opus_49 and argon directory, plus campaign_fresh_gravity, hunt_2026, theory_2026, book and docs. EXT01 and EXT02 (the external notes on the 32π puzzle) concern a0, not alpha, and are not listed.

**Columns.**
* **Fam** is the mechanism family; the codes are defined at the end.
* **1/α produced** is the value the attempt output, or "not selected" when alpha remained a free direction.
* **Trials** counts graded value trials: numerical outputs for a coupling compared against a target. The suffix `R` marks rule-search counts. `-` means no graded value: the result was structural, free, or an audit.
* **Commit** is the lane's commit. Short hashes come from `git log`. FSP-001 to FSP-010 are committed only on branch `codex/fine-structure-claude-handoff` (6ce8eec12) and are untracked on main.

Counts and the attempt counter are produced by `cfg895_check.py` (see `README.md`).

## FP: running couplings, fixed points, UV boundary values, multiple-point principle

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| B | FP | real_research/alpha_principle_2026/B_rg_asymptotic_safety | Reproduces the literature fixed point of quantum gravity for hypercharge, g_Y* = 4π sqrt(6 f_g/41) | Harst-Reuter toy (charged fermions only) 75.2–77.1; Eichhorn-Versteegen EH 92.914 | NOT PREDICTED: depends on the truncation; 137 needs f_g = 0.009805, 4.89× smaller | 2 | a628e8a66 |
| AS1 | FP | alpha_principle_2026/AS1_fg_r2_truncation | f_g once in EH + R², Litim type I (pre-registered) | none | NOT COMPLETED at gate G1: Eichhorn-Versteegen (4.8)-(4.9) cannot be rebuilt (the vacuum-term sign differs); the design error was ours | 1 | 4811df3f0 / 3d8900c10 |
| AS2 | FP | alpha_principle_2026/AS2_fg_cpr_scheme | Every choice taken from CPR 0805.2909 | none | NOT COMPLETED: the root at n = 1 misses CPR Table 1 by 0.33–0.37%, consistent with a misprint in that table | 1 | c1789e555 / 7df554f35 |
| AS3 | FP | alpha_principle_2026/AS3_fg_cpr_reanchored | AS2 re-anchored on CPR numbers that agree with each other; EH + SM, then R² + SM | EH reference 95.578 (f_g 0.03883); graded 95.270 or 95.706 | NOT DIAGNOSTIC: two admissible roots. Only TT gravitons couple, so R² drops out of f_g | 1 | c9935aa03 / 0c3ccc779 |
| AS4 | FP | alpha_principle_2026/AS4_fg_weyl2 | EH + C² + R², following BMS 0902.4630 | EH reference 96.373; the only in-domain root 91.045 is inadmissible | NOT PREDICTED: no admissible root. Disclosed: the frozen admissibility rule also rejects BMS's published pure-gravity fixed point | 1 | 3ac042714 / 999af4285 |
| U3 | FP | alpha_principle_2026/U3_invented_uv_boundary | 13 invented UV boundary principles (34 variants), scored on all three couplings at once | nearest variant that fixes alpha: 133.2 | KILLED: 33 DEAD, 1 UNDECIDED (post hoc, fixes no alpha), 0 survive | 34 | 44502b882 |
| X1 | FP | alpha_principle_2026/X1_spectrum_meets_boundary | Algebraic spectrum meets a forced UV boundary under the zero-knob rule | absolute rules miss alpha(0) by 56–240% | KILLED: 0 LEAD, 2 RE-FIT (three 27s of E6 need 2 mass knobs and fail the proton lifetime), 13 DEAD | 81 | 8a216d86f |
| Z1 | FP | alpha_principle_2026/Z1_common_scale | Is there any scale where the three SM couplings meet? | not selected | Structural: in an SM desert the minimum spread is 7.6–8.4% (30σ); no 'equal couplings at X' rule can work | - | 0e6b410fe |
| B1 | FP | alpha_principle_2026/B1_multiple_point | Bennett-Nielsen gauge MPP predictions vs Y1 | 1/alpha(0) 138.35 ± 8.28 | CONSISTENT (weak): uncertainties of 8–15%; a flat guess would also pass (~3%); the U(1) enhancement factor was chosen. Later withdrawn as a three-coupling result (B4) | 3 | c56c04a1a |
| B2 | FP | alpha_principle_2026/B2_lattice_mpp | Own lattice Monte Carlo behind B1 | SU(2) 49.9 ± 2.8 + 2.3; SU(3) 66.7 ± 11.1 | SU(2) PASS-WEAK; SU(3) and U(1) UNDECIDED (the 3% target was not met) | 3 | c32cee80f |
| B3 | FP | alpha_principle_2026/B3_u1_enhancement_model | Audit of the U(1) enhancement model behind B1 | not selected | CONDITIONAL-WEAK: factor 6 named before the lattice; 6→8.04 interpolation and q = 1 CHOSEN | - | ff0da226f |
| B4 | FP | alpha_principle_2026/B4_sharper_lattice | Wang-Landau lattice for the SU(2) and SU(3) triple points | SU(2) 50.55 ± 0.42 (or 48.25); SU(3) 67.70 ± 1.63 | SU(3) FAIL (z +3.6); SU(2) PASS-WEAK but depends on convention. The MPP hint is withdrawn | 2 | a2e13e766 |
| FSP-U1 | FP | fine_structure_puzzle/uv_selection | Full-rank matrix fixed point with a one-loop gravity ansatz; Yukawa correlations | not selected | Shape obligation resolved; the absolute coupling, the gravity coefficient and the branch are not derived | - | branch 6ce8eec12 |
| FSP-U2 | FP | fine_structure_puzzle/uv_selection | Restricted SM inverse boundary problem: fit two Yukawas, predict g_Y | g_Y about 13% low | KILLED at the stated approximation (the held-out prediction fails); independently reimplemented | 1 | branch 6ce8eec12 |
| ATOMOS-RG | FP | project_atomos/rg_flow_correspondence.py | Framework kernel K(z) read as an RG flow and compared with SM beta functions | not selected | NO SM DOOR: the dictionary gate fails by about 24 orders; matches no better than decoys. A remembered '137' was a bug (reviews/two_loop_vs_alpha_2026.py) | - | 28eddee617 |
| Q05-32PI | FP | sonnet55_push/puzzle_32pi/agents/Q_yang_mills_anomaly | Dimensional transmutation sized to rho_Lambda needs b0 g² ≈ 1.12 | not alpha_em (83 / 124 / 207 for SU2 / SU3 / SU5) | A fit with two free numbers; decoys fit equally well | - | 243a089c9e |

## GEO: geometric, topological and algebraic

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| G | GEO | alpha_principle_2026/G_topological_anomaly; Lean ALPHA_G1, ALPHA_G3 | Anomalies, topology, GUT embedding, duality fixed points | not selected | Fixes integers, charge ratios and coupling ratios; the overall coupling stays free | - | a628e8a66 / ecf3d3ffae |
| W1 | GEO | alpha_principle_2026/W1_division_algebras | Division algebras and exceptional structures (Furey, F4/E6) | not selected | No coupling forced: they fix charges and N_c = 3; one 1/g² per simple factor stays free | - | afc46dd06 |
| N1 | GEO | alpha_principle_2026/N1_joint_couplings | Joint over-determination of (alpha_Y, alpha_2, alpha_3); S², CP²×S², SU(5)/SO(10) | ratio maps only | KILLED: S² ratio −19.6%; product map 0/72; desert GUT misses alpha_3 by −11.6% | 81 | f97ff3c52 |
| ATOMOS-S1 | GEO | project_atomos/notes/SECTOR1_GAUGE_GEOMETRY.md | SU(5) embedding with sin²θ_W = 3/8 ties alpha_em, alpha_s and alpha_GUT | not selected | Couplings FREE (alpha_GUT is free); the minimal-SM interlock fails the precision test | - | af57df5d40 |

## QED: vacuum polarisation, QED self-consistency, non-perturbative QED

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| W2 | QED | alpha_principle_2026/W2_nonperturbative_qed | Critical coupling for chiral breaking; Landau pole placed at a Planck scale; quasi-fixed points; large-N_f UV zero; Ward identity | critical alpha_c = 1.0477 (about 140× the Thomson value); Landau-pole variants miss by 40–52% | KILLED: 20 pre-registered hit-tests, all DEAD; charge ratios exact, overall scale free | 20 | 59086daff |
| FSP-S | QED | fine_structure_puzzle/spectral_route | Spectral positivity, compactness and anomaly constraints on the induced local coefficient | not selected | Refuted in the stated class: the local coefficient is not fixed; a scale ratio remains | - | branch 6ce8eec12 |

## GRAV: gravity-coupled (photon–graviton, gauge–gravity unification)

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| N3 | GRAV | alpha_principle_2026/N3_graviton_coefficient | Gauge coefficient inherited from the graviton (MacDowell-Mansouri, Lisi-Smolin-Speziale, Plebanski, graviweak) | alpha_G ~ (4/3) G Lambda ~ 4e-122 where a coefficient exists | Tied to G Lambda (~1e-122), absent, free, or mixed with a free label | - | f97ff3c52 |
| M3-MM | GRAV | alpha_principle_2026/M_red_team/m3_ds_gauge_coupling.py | SO(4,1) MacDowell-Mansouri, reading 1/g² from the action's coefficient | alpha_MM ~ 1e-121 to 1e-117 | KILLED by about 120 orders | 1 | 442b3253e |

## WGC: gravity–charge bounds and extremality

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| A | WGC | alpha_principle_2026/A_wgc_extremal; Lean ALPHA_A | WGC, Dirac + extremality, RN-dS special points | not selected | Gives inequalities, or alpha re-expressed as the size of the minimal magnetic object. Its post-hoc 'alpha(m_P) ≈ 1/132, within 0.6% of Z' remark is VOID (a b_Y bug found by lane M) | - | a628e8a66 / ecf3d3ffae |
| Q5 | WGC | alpha_principle_2026/Q5_extremality_corrections | Extremality corrections, BPS towers, Planck-size object | not selected | One free linear form in the operator coefficients; the BPS coupling is a free modulus; corrections of 1e-3 to 30% | - | d17455901 |

## HOR: horizon, de Sitter, thermodynamic

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| AH1 | HOR | real_research/alpha_schwinger_2026/ah1_schwinger_ds2.py | Schwinger/Unruh pair production in dS₂ (scalar) | 5 natural handles: 50.3, 12.6, 1.27, 0.32, 421 | NO-GO: the rate depends on e only through lambda = eE/H², so alpha is a free direction; ties span at least 1e12 | 5 | 5db88bfc2 / 147b1498c |
| AH2 | HOR | alpha_schwinger_2026/ah2_induced_current_ds2.py | Induced current in dS₂ | not selected | NO-GO: sigma H = (e²/H²) g(mu), with g spanning more than 12 decades | - | 5823f6bfe |
| AH3 | HOR | fable_independent_2026/lean_2026/AH3_alpha_nogo.lean | Lean certificates for the AH1/AH2 no-go | not selected | 10 theorems: no function of lambda recovers e or alpha. Certifies the premise-to-conclusion step only | - | 86f3c7a9a |
| AH4 | HOR | alpha_schwinger_2026/ah4_induced_current_ds4.py | Induced current in dS₄ (scalar) | not selected | NO-GO: sigma/H = alpha G(mu); the ln(m/H) term is the one-loop running; alpha is an input | - | 0c72bfdec |
| N5 | HOR | alpha_principle_2026/N5_dS2_fermions | Charged Dirac fermions in dS₂ | not selected | Depends on mass; critical damping e²/H² = π/4 only for an exactly massless fermion | - | f97ff3c52 |
| Q1 | HOR | alpha_principle_2026/Q1_ds4_fermions; Lean ALPHA_Q1 | Charged Dirac fermion in dS₄ | not selected | sigma/H = alpha G_f(M), with G_f depending on mass and no threshold | - | d6dc6b73a |
| Q2 | HOR | alpha_principle_2026/Q2_nonminimal_conformal; Lean ALPHA_Q2 | Non-minimal coupling and the conformal threshold lambda_c = 1/2 | not selected | Fixes eE/H², not e; not a lead | - | 68e220efb |
| S1 | HOR | alpha_principle_2026/S1_vector_bosons | Charged Proca boson in dS₄ | not selected | No finite renormalised current; the coupled block diverges logarithmically; still OPEN (needs a covariant regulator and a Higgs completion) | - | 61f3895cf |
| S2 | HOR | alpha_principle_2026/S2_fermion_independent | Independent check of Q1 (light and heavy limits) | not selected | Supports Q1 to 3e-10 and 1.2e-11 | - | a73fdaf3b |
| T1 | HOR | alpha_principle_2026/T1_stationary_field | Self-sustained electric field in dS₄: alpha G_f(M) = −2 | needs m/H = 2.3e-281 | KILLED: every known species is about 1e81 short | 1 | 3fc2f20b1 |
| U1 | HOR | alpha_principle_2026/U1_invented_horizon_principles | 18 invented horizon principles, 47 variants | number-returning variants miss by at least 2.6e-4 | KILLED: 16 DEAD, 2 inert | 47 | 566d925f0 |
| U2 | HOR | alpha_principle_2026/U2_programme_native_model; Lean ALPHA_CFG47_U2 | Capped horizon condensate; charge as a unit winding | contact bypass gives alpha = 2π (861× the target); Lean 1/alpha_c = 4Z² = 134.04 at kappa = 1/2 | KILLED: no charge quantum (closed windings act as dipoles); retired | 2 | 9a001366a / ecf3d3ffae |

## STR: string theory, Kaluza–Klein, extra dimensions, supergravity

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| AH6 | STR | alpha_schwinger_2026/ah6_kaluza_klein.py | Kaluza-Klein: alpha_n = 4 n² l_P²/R² | flux N = 23 gives 132.25; N = 24 gives 144 | Alpha traded for R (R = 23.41 l_P); the electron cannot carry graviphoton charge | 2 | e39f0bfcc |
| F | STR | alpha_principle_2026/F_kk_stabilization; Lean ALPHA_F | Radion stabilisation by the Casimir energy; Freund-Rubin S² | not selected | Matching Lambda gives R ~ 1e30 l_P; R = 23.4 l_P needs 114.5 decades of cancellation | - | a628e8a66 / 7838d30479 |
| H | STR | alpha_principle_2026/H_string_heterotic | Heterotic tree map; minimal-string one-loop running with levels (5/3, 1, 1) | 146.09–146.60 | KILLED (+6.6 to +7.0%); tree map has rank 3; the O(1) convention is unresolved | 3 | 190cb6920 |
| Q3 | STR | alpha_principle_2026/Q3_salam_sezgin; Lean ALPHA_F_Q3 | Salam-Sezgin 6D gauged supergravity | best of 16 misses by 41% | KILLED: the flux is forced to N = 1, but the dilaton is a flat direction | 16 | 57793f8f1 |
| FSP-A | STR | fine_structure_puzzle/archive_audit | Audit of the old no-gos; quantum lifting of Q3 | not selected | A finite coefficient stays free; the stable ansatz minimum is AdS; open pending a full theory | - | branch 6ce8eec12 |

## EMG: emergent, induced, species and holographic count

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| C | EMG | alpha_principle_2026/C_holographic_species | Emergence at the species scale (1/e² = 0 at Lambda) | toy 70.4–71.7 (target/toy 1.91–1.95); SM chain hypercharge residual 59.8 | KILLED: needs about 8.6 extra unit-Y fermions, i.e. the walled masses | 3 | a628e8a66 |
| J | EMG | alpha_principle_2026/J_emergent_condensate | Emergent photon from a condensate: alpha⁻¹ = (N_eff/3π) ln(Lambda²/mu²) + const | not selected | N_eff and Lambda/mu are not derived; the dark-fluid order parameter cannot supply them | - | 190cb6920 |
| N2 | EMG | alpha_principle_2026/N2_emergence_tower | Emergence with a forced KK tower | 128.1, 151.7, 152.2 | KILLED: R is a free modulus spent on one coupling | 3 | 29cc0c4a6 |
| N4 | EMG | alpha_principle_2026/N4_holographic_count | Holographic count: the geometry depends only on alpha N² | best miss 10% | KILLED: 45 trials, 0 of 90 candidate-target pairs clear the bar | 45 | f3852db78 |

## DIL: dilatons, attractors, varying alpha, common fields

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| E | DIL | alpha_principle_2026/E_dynamical_attractor | Damour-Polyakov, runaway and de Sitter attractors: alpha = 1/(k B_F(phi_m)) | not selected | The value is the free B_F(phi_m) | - | a628e8a66 |
| FSP-B | DIL | fine_structure_puzzle/atomic_bridge/scalar_bridge | Common scalar for the gauge and mass sectors: alpha⁻¹ = (4π k_γ/a) ln(C_N M_U/m_N) | not selected | M_U and the common function are not derived; an exact counterfamily changes alpha | - | branch 6ce8eec12 |
| VARY | DIL | real_research/reviews/mi_varying_constants_bridge_2026.py | Does alpha track rho_DE as a0 does? | not selected | NO: clocks bound the tracking exponent to about 1e-18 or less | - | e2a3f2f420 |

## QCD: QCD vacuum, proton and atomic matching (the fine-structure puzzle programme)

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| FSP-Q | QCD | fine_structure_puzzle/atomic_bridge/qcd_mass | QCD vacuum in de Sitter, Delta eps = c_H H Lambda³ (premise of arXiv:2506.14182), with R = c_H/C_p³ = Hbar/(K G m_p³) | not selected | Conditional: c_H is not computed; a local null curve exists while the quark mass is free | - | branch 6ce8eec12 |
| FSP-H | QCD | fine_structure_puzzle/atomic_bridge/hydrogen | The framework's static action continued to hydrogen: δV = G m_e m_p r/L*² | not selected | Shift of about 1e-78 Hz; independent of a_M; no selection | - | branch 6ce8eec12 |
| FSP-I | QCD | fine_structure_puzzle/atomic_bridge/coordinator | Atomic energy minimisation over alpha | not selected | At fixed masses the energy is concave in alpha, so this class cannot select an isolated alpha | - | branch 6ce8eec12 |
| FSP-003 | QCD | fine_structure_puzzle/qcd_prediction | Chiral EM response; a direct S⁴ pion determinant (zero linear-H term); BPS comparison; QCD zero modes | not selected | Partial: no physical R(alpha) | - | branch 6ce8eec12 |
| FSP-004 | QCD | fine_structure_puzzle/qcd_completion | Closed monopole and dual ensembles; static J sectors; anomalous contact sector | not selected | Partial: the retained linear term is absent in closed models | - | branch 6ce8eec12 |
| FSP-005 | QCD | fine_structure_puzzle/qcd_closure | Angular Hessian bounds; wall heat; first neutral interaction diagram | not selected | Partial: charge and curvature limits do not commute | - | branch 6ce8eec12 |
| FSP-006 | QCD | fine_structure_puzzle/qcd_physical_matching | A finite proton subtraction stencil free of alpha; same-theory cancellation | not selected | Partial | - | branch 6ce8eec12 |
| FSP-007 | QCD | fine_structure_puzzle/qcd_sea_curvature | Disconnected current moments; sea OPE; two-pion curvature response | not selected | Partial | - | branch 6ce8eec12 |
| FSP-008 | QCD | fine_structure_puzzle/qcd_global_kernel | Full Born kernel; 2+1 sea estimator; closed sphere functions | not selected | Partial | - | branch 6ce8eec12 |
| FSP-009 | QCD | fine_structure_puzzle/qcd_nonborn_vacuum | Non-Born band; unconditioned sphere estimator; flavor Ward closure | not selected | Partial: charge exchange blocks the Ward reconstruction | - | branch 6ce8eec12 |
| FSP-010 | QCD | fine_structure_puzzle/qcd_hard_vacuum | Hard matching (5/2; gluon 3/4, 17/4); closed SU(3) K1 partition; charged-sea beta kappa⁴ coefficient | not selected | Partial: no linear inverse-size term in the calculated sectors; physical A and A_u not established | - | branch 6ce8eec12 |
| FSP-011 | QCD | fine_structure_puzzle/qcd_full_proton | Exact isospin split M_u^p = Born^(0) + M_u^(p−n)/2 + N0 | not selected | Partial: N0 needs a lattice production job (not started); the 5.03–5.89 MeV/e² partial sum is NOT M_u^p | - | 7db7931cf |
| CFG895-B2 | QCD | campaign_fresh_gravity/CFG895_alpha_campaign_ledger/cfg895_check.py | Leverage of the FSP selection equation R(alpha) = Hbar/(K G m_p³) | not selected | NOT DIAGNOSTIC by construction: d ln R/d ln alpha = O(5e-4), so sigma(ln alpha) ≥ 11 (H0 bracket) and ≥ 1.7 at 1%; kappa cancels | - | this lane |

## SEL: anthropic, landscape and consistency bounds (not derivations)

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| I | SEL | alpha_principle_2026/I_selection_consistency | Landau pole, nuclear and atomic stability, the stellar window | bands (e.g. 0.77–1.09 alpha_0) | Bands hundreds to thousands of times wider than 1e-3, not a point | - | 190cb6920 |
| I3 | SEL | I_selection_consistency/i3_vacuum_energy_alpha.py | Hartle-Hawking/Coleman extremum: d Lambda_eff/d alpha = 0 at two-loop QED | not selected | The extremum depends on a scheme choice (the scale mu of the vacuum counterterm) | - | 190cb6920 |

## NUM: numerology and formula or rule searches [FLAG: not mechanisms]

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| A1 | NUM | alpha_principle_2026/A1_kz_rule_search | 5,488,000 zero-knob rules c π^r Z^p kappa^q at 8 scales | none | 0 real hits; decoys give P_chance 0.001 (powered null) | 5488000R | 6996007564 / d2cadcdc09 |
| A2 | NUM | alpha_principle_2026/A2_kz_rule_search_tier2 | 30,530,688 rules with a wider grammar | none | 0 hits, but P_chance 0.01425 fails the power criterion, so the null is weak; the budget is spent | 30530688R | 2d5fff0fb / fb6f8828c |
| ATOMOS-NULL | NUM | project_atomos/PAPER_ATOMOS_NULL.v2.md | Exhaustive values to depth 10 from the germs {3, sqrt(8π/3)}, scored against 19 SM targets | none | CLEAN NULL: 0 hits for 1/alpha(0) among 42,534,139 distinct values; alpha(M_Z) 50 in-window hits, 0 certified (published null, zenodo 21654272) | 42534139R | c6927551ef / 28eddee617 |
| ANGLE-CEIL | NUM | real_research/reviews/mi_angles_search_ceiling_2026.py | Information pricing of germ searches (1/alpha(0) is worth 31.6 bits) | none | NO-GO: past the look-elsewhere ceiling before reaching the needed depth | - | 3fd85d4596 |
| L-4Z2P3 | NUM | ai_slop/research/ALPHA_DERIVATION_AUDIT_MAY2026.md; real_research/reviews/false_discovery_rate.py | alpha⁻¹ = 4Z² + 3 = 128π/3 + 3 (BriareusFlow search output) | 137.04129 (+3.9e-5) | FDR-DEAD: an arbitrary target is hit this closely 19.9% of the time; the '4' has 5 justifications. Publicly RETRACTED 2026-06-23 | 34073R | 999f94dfe / efaa11a19e |
| L-SELF | NUM | ai_slop/research/geometric_closure/self_referential_alpha.py | alpha⁻¹ + alpha = 4Z² + 3 | 137.03399 (−1.5e-5) | Ad hoc adjustment (repo's own audit); retracted with the base formula | - | 999f94dfe |
| L-12PI | NUM | ai_slop/analysis/alpha_verification.py; reviews/alpha_12pi_identity_audit_2026.py; Lean AH8; lane T2 | alpha⁻¹ + alpha − 12π alpha² = 4Z² + 3, sold as 'two-loop' | holds to 1.8e-8 only with alpha as input; the bare form is 3.9e-5 | Artefact: the corrections are the leftover rewritten as a series in alpha; 12π is 0.12% off the exact coefficient (37.74–37.75); not a QED series (T2) | - | fa18a1a108 / 7b31b12b8 / 4a0b7db40 |
| L-PI600 | NUM | ai_slop/research/ALPHA_BREAKTHROUGH.md; opus_48_extended_research/reviews/PARTICLE_BRIDGE_FRESH_EYES_2026-06-17.md | 4Z² + 3 − π/600 | 137.03605 (+3.7e-7) | A fitted correction; FDR-dead | - | 999f94dfe / 3688531f89 |
| L-PIPOW | NUM | ai_slop/research/ALPHA_DERIVATION_SUMMARY.md | (277/6)π − 8 and (199/5)π + 12 | 137.03686 and 137.03539 | Search output; no mechanism | - | 999f94dfe |
| L-P33 | NUM | ai_slop/website/src/app/all-derivations/page.tsx | 137 is the 33rd prime and floor(Z²) = 33 | 137 (−0.76%) | Numerology; covered by a site banner | - | 999f94dfe |
| L-HOLO | NUM | ai_slop/research/ALPHA_RIGOROUS_DERIVATION.md; first_principles/derive_alpha_from_holography.py; foundations/Z2_KALUZA_KLEIN_DERIVATION.py | Justification stories for 4Z²+3: Cartan generators × Z², Friedmann D²·(8π/3) + N_gen, R²/(4 l_P²), boundary DOF counting | 137.0413 | ASSUMED, NOT PROVEN (repo's audit); target-first; retracted | - | 999f94dfe |
| L-TOPO | NUM | ai_slop/research/RIGOROUS_ALPHA_DERIVATION.md; SIGNATURE_OPERATOR_DERIVATION.md; CHERN_SIMONS_ANALYSIS.md; ALPHA_COMBINATORIC_PROOF.md | APS index 2χ(S²) Z² + b1(T³); signature operator; θ = 4Z²+3; cube combinatorics; cube lattice | 137.0413 | The '+3 from generations' is ASSUMED; target-first; retracted | - | 999f94dfe |
| L-RG | NUM | ai_slop/research/computational_math/holographic_alpha_derivation.py; proofs/alpha_ir_fixed_point_rg.py; ALPHA_RUNNING_VERIFICATION.md | 'Holographic IR fixed point' in AdS5×T³/Z2; a KK tower absorbing loops; Δalpha⁻¹ = 9 to M_Z | 137.0413 | Fails the sign test (alpha⁻¹ falls with energy, about 128 at M_Z); retracted | - | 999f94dfe / f1535b7d8d |
| L-MISC | NUM | ai_slop/research (overnight_results, STANDARD_MODEL_COUPLINGS.md) | alpha_em = Omega_b/(Z+1) (0.49%); 24 Z − 2; (Z²+Z)/2 + 4 (broken code); A_s = 3 alpha⁴/4; theta_QCD = alpha^Z | various | Search output; no mechanism | - | 59e1868de / 999f94dfe |
| L-PN | NUM | opus_48_extended_research/reviews/PROTON_ELECTRON_MASS_RATIO_2026-06-17.md; real_research/PROTON_ELECTRON_BRIDGE_VERDICT_2026-06-06.md | m_p/m_e = alpha⁻¹·2Z²/5, or (4Z²+3)·67/5 | implied 136.984 | NUMEROLOGY, FDR 0 (the '2/5' has 4+ justifications); built on the dead formula | - | 68475110aa / 623cb91e7b |
| Q38-0010 | NUM | qwen_38_experiment/LEDGER.md (seed 0010) | alpha⁻¹ ≈ (71/3) Z | 137.00 (−2.7e-4) | DISCARD: dense rationals; the seed's own kill clause fires | - | b062ad4a25 / 86861f925a |
| Q38-0073 | NUM | qwen_38_experiment/seeds/archive_20260914/refereed/ref_0073.md | m_p/m_e = 13 alpha⁻¹ | implied 141.24 (+3.1%) | DISCARD: fails for every N from 12 to 15 | - | 86861f925a |
| Q38-SEEDS | NUM | qwen_38_experiment/LEDGER.md (10 seeds) | 'One shared number does two jobs, one of them alpha⁻¹' | none without a free dial | DISCARD (blind referee): circular or convention-grade | - | 86861f925a |
| Q38-T102 | NUM | qwen_38_experiment/mm_search.py, TASKS.md | Planned FDR-counted monomial sweep of alpha_inv | none | Never run | - | 82b222822c |

## EXT: published or external claims audited by the record

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| K | EXT | alpha_principle_2026/K_literature_audit | 16 published claims (Eddington, Gilson, Wyler, Rosen, Sherbon, combinatorial hierarchy, Bleger, Atiyah, BSBM, Johnson-Baker-Willey/Adler) | misses 2.6e-4 to 3.3e-11 | None clears the bar (Bleger: 3.3e-11 but five integers, P = 0.90); JBW/Adler is dead in QED; Atiyah has no evaluable computation | 16 | 087c41203 |
| Q4 | EXT | alpha_principle_2026/Q4_unaudited_claims | Six claims from 2025–26 (Relator, Kosmoplex, Xu, Bleger, Gilson, Reinisch) | Kosmoplex 137.0359991003; Xu repaired 137.1016 | Nothing is a result; Relator clears the bar's letter only if its family is taken as 2^25 | 6 | f4bac5e53 |
| R1 | EXT | alpha_principle_2026/R1_relator_followup | Adversarial re-implementation of Relator | printed equations give 137.0359986396 (−3.9e-9) | ADJUSTED-TO-DATA: the reported value is not a consequence of the printed equations (same claim as in Q4; not counted twice) | - | 4791a4f45 |
| SINGH | EXT | project_atomos/notes/KOIDE_DIRAC_BRIDGE.md | Quoted: alpha from J3(O) and triality (arXiv:2304.01213) | about 137.04 as quoted | NOT AUDITED for alpha (loose end; grade it with lane D's checker) | - | e585150254 |
| CAHILL | EXT | data_assembly/DOOR11_LITERATURE_2026-09-29.md | 'Dynamical 3-space' flow coefficient alpha ≈ 1/137 | alpha inserted, not predicted | Rejected: a dimensionless coefficient gives BTFR slope 2 and no acceleration scale | - | 23bff38f6d |

## META: no attempt (bars, harnesses, audits, red team, obstruction theorems)

| ID | Fam | Where | Mechanism | 1/α produced | Verdict (why) | Trials | Commit |
|---|---|---|---|---|---|---|---|
| AH5-AH7 | META | alpha_schwinger_2026/ah5_dimensional_obstruction.py; Lean AH7 | Buckingham pi: (c, G, Lambda) form no number; adding hbar gives only x = Lambda l_P² | (1/2) ln(1/x) = 139.97, reported, not scored | Structural: alpha is an independent dimensionless group, not a power of x | - | 4dc1a546a / eeb3eb73b |
| D | META | alpha_principle_2026/D_calibration_bar | The look-elsewhere bar and alpha_bar_checker.py | no derivation proposed | Bar: P < 1e-3, miss ≤ 5e-10 or the route's own precision, 0 fitted reals, scale stated | - | a628e8a66 / 1d23899e6 |
| V1 | META | alpha_principle_2026/V1_exactness_harness | Precision of the measurements | no derivation proposed | Cs and Rb recoil values are 5.49σ apart; agreement to about 9 digits | - | a8485b847 |
| M | META | alpha_principle_2026/M_red_team | Red team of lanes A–J | no derivation proposed | Closures sound; found lane A's b_Y bug | - | 442b3253e |
| P | META | alpha_principle_2026/P_claim_audit | Claim audit of the status document | no derivation proposed | 32 of 49 statements supported, 15 overstated, 2 unsupported; no number wrong | - | 8ff6026b6 |
| Y1 | META | alpha_principle_2026/Y1_running_precision | Validated SM running (4-loop gauge) | no derivation proposed | Central values at M_P: 55.234 / 49.203 / 52.971 (alpha_em 104.437); sigma(alpha_em) 8.8e-4 | - | f73411efe / e6d9add5c |
| YM1 | META | alpha_principle_2026/YM1_instanton_peek | Post-hoc table of S_i = 2π/alpha_i against Z² and 32π² | none asserted | Descriptive; not pre-registered; no match; inside A1/A2's grammar | - | 80af40bf79 |
| T2 | META | alpha_principle_2026/T2_series_class | Is the 12π identity a QED loop series? | no derivation proposed | No: the coefficients lie outside the QED class (PSLQ); random residuals are matched as often | - | 4a0b7db40 |
| FDR-AUD | META | real_research/reviews/false_discovery_rate.py; is_Z_special.py; geometric_closure_audit.py; real_research/can_another_number_do_it.py; reviews/toe_boundary_2026_07/Z_SM_bridge_pslq.py | False-discovery and number-field audits of the legacy formulas | no derivation proposed | 4Z²+3 carries about 0 bits; Z is not special; a random base does better; no SM bridge (number-field obstruction) | - | efaa11a19e / b031e9ab44 / 8ce52d6e95 |
| FSP-N | META | fine_structure_puzzle/normalization_gate | Physical pole projection and charge-normalisation gate | no derivation proposed | Gate established for a finite tree-level EFT | - | branch 6ce8eec12 |
| TOE-GUARD | META | fable_independent_2026/lean_2026/TOE_BEST_ATTEMPT_2026_10_12.lean | Theorem matching_is_not_deriving | no derivation proposed | A methodological guard | - | 5e0b67a135 |
| HY4-D199 | META | hy4_push/H050_200_MORE_DOORS.md | The question 'Does the framework fix alpha?' | none | Listed only, never executed | - | e94226a890 |

## Family codes

* **FP**: running coupling, fixed point, UV boundary value, MPP.
* **GEO**: geometric, topological or algebraic.
* **QED**: vacuum polarisation, QED self-consistency, non-perturbative QED.
* **GRAV**: gravity-coupled (photon–graviton, gauge–gravity unification).
* **WGC**: gravity–charge bounds and extremality.
* **HOR**: horizon, de Sitter, thermodynamic.
* **STR**: strings, Kaluza–Klein, extra dimensions, supergravity.
* **EMG**: emergent, induced, species, holographic count.
* **DIL**: dilaton, attractor, varying alpha, common field.
* **QCD**: QCD-vacuum, proton or atomic matching.
* **SEL**: anthropic or consistency bands (not a derivation).
* **NUM**: numerology, formula or rule search (flag).
* **EXT**: external claims audited.
* **META**: no attempt (bar, harness, audit, obstruction theorem).

## Public statements (for the owner; nothing was edited)

* The front page of the site (`ai_slop/website/src/app/page.tsx`, f68ed2505) carries the retraction of 2026-06-23, which covers the alpha, mass-ratio and TOE claims.
* Several pages and components still show the old alpha formulas. They sit behind the RouteNotice banner, which covers alpha:
  * `src/app/why-z2/page.tsx` and `src/app/all-derivations/page.tsx`;
  * `src/components/GeometricVisualization.tsx`, `ZConnectionWeb.tsx` and `Derivation.tsx`.
* `src/app/topology/page.tsx` also still claims alpha ("all from topology"), but its RouteNotice entry covers only the topology rejection, not alpha.
* The static HTML papers carry no banner:
  * `public/Z2_FRAMEWORK_v4.0.0.html` ("we prove α⁻¹ = 4Z²+3 is the IR fixed point");
  * `public/LAGRANGIAN_FROM_GEOMETRY_v4.0.4/v4.0.5/v5.3.0/v5.4.0.html`.
* Whether these files are deployed was not checked.
* The `ai_slop/` Zenodo v6/v7 drafts and the publisher-pitch drafts still state the 'two-loop' claim.
* Under the record's rules, only the owner decides about public content.

## Post-ledger attempts (appended by the orchestrator)
| CFG896 | HIGGS/FP | campaign_fresh_gravity/CFG896_alpha_D02_higgs_boundary | Door D02: Higgs boundary conditions (λ=0, β_λ=0, Veltman, MPP at M_P/M_red; singles and joint pairs) solved for g_Y | β_λ=0: 162.06 / 149.32; others NOT DIAGNOSTIC (σ 3.3–14.2) | 11 NOT DIAGNOSTIC, 2 KILLED (+10.2σ/+7.9σ); joint α–M_W 98% correlated (one test) | 13 | cfc23448b / b2fa5ad0d / 9c1069bb0 |
| CFG901 | FP | campaign_fresh_gravity/CFG901_alpha_D03_own_content_fg | Door D03: AS f_g with SM + 3 ν_R, CPR-EH graded | 96.504 (reported 96.24/96.65, 97.27, 93.30) | KILLED: z = −6.51 vs σ_route 6.230; ν_R shift ≪ σ (content loophole closed) | 1 | f1e4cb90d / ced3bd06b / 4845e8377 |
| CFG906 | FP | campaign_fresh_gravity/CFG906_alpha_D04_unimodular_as | Door D04: unimodular AS f_g (det g fixed, TDiff, no λ), TT + σ, M-eq measure | 105.628 graded (g* = 0.852, f_g = g/(12π)); variants 91.58–106.27 | KILLED: z = −5.04 vs σ_route 6.230; σ = −2/5 of TT; 137 needs g* 0.370; all 72 declared variants KILLED | 1 | 29fb5fdc0 / b6422c0f7 |
| CFG907 | GEO/FP | campaign_fresh_gravity/CFG907_alpha_D07_ncg_spectral_action | Door D07: NCG spectral action with the entropy cutoff f_0 = ln 2; boundary g_3² = g_2² = (5/3)g'², g² f_0/2π² = 1/4 at Λ = μ_23; Y1 running | 78.354 graded (1/α_U = 1.765 vs 46.14, ×26); configurations 69.8–85.0 | KILLED: z_Y −67.7, z_A −72.3; all 8 configurations KILLED; run-down non-perturbative | 1 | 088b4e0b2 / 2bac4efb6 / 4b8b675f9 / eaf6007cb |
